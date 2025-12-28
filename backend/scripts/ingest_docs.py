"""
Document Ingestion Script for Qdrant Vector Database

This script reads markdown/mdx files from the Docusaurus documentation,
chunks them, generates embeddings, and stores them in Qdrant for RAG.

Usage:
    python scripts/ingest_docs.py

Environment variables required (in .env):
    - COHERE_API_KEY
    - QDRANT_URL
    - QDRANT_API_KEY
    - DATABASE_URL
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Tuple
import uuid

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import settings
from src.core.database import AsyncSessionLocal
from src.models.document import Document, DocumentChunk
from src.services.embedding_service import EmbeddingService
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
import cohere


class DocumentIngester:
    """Handles ingestion of documents into Qdrant and PostgreSQL"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        self.collection_name = "document_chunks"
        self.chunk_size = 1000  # Characters per chunk
        self.chunk_overlap = 200  # Overlap between chunks

    async def ensure_collection_exists(self):
        """Ensure the Qdrant collection exists with correct configuration"""
        try:
            collections = await self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                print(f"Creating collection: {self.collection_name}")
                await self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # Cohere embed-english-v3.0 dimension
                        distance=models.Distance.COSINE
                    )
                )
                print(f"[OK] Collection '{self.collection_name}' created successfully")
            else:
                print(f"[OK] Collection '{self.collection_name}' already exists")
        except Exception as e:
            print(f"[ERROR] Error ensuring collection exists: {e}")
            raise

    def chunk_text(self, text: str, metadata: dict) -> List[Tuple[str, dict]]:
        """
        Split text into overlapping chunks

        Returns:
            List of (chunk_text, chunk_metadata) tuples
        """
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                if break_point > self.chunk_size * 0.7:  # At least 70% of chunk size
                    end = start + break_point + 1
                    chunk = text[start:end]

            chunk_metadata = {
                **metadata,
                "chunk_index": chunk_index,
                "chunk_start": start,
                "chunk_end": end
            }

            chunks.append((chunk.strip(), chunk_metadata))
            chunk_index += 1
            start = end - self.chunk_overlap

        return chunks

    def read_markdown_file(self, file_path: Path) -> Tuple[str, dict]:
        """
        Read a markdown/mdx file and extract content and metadata

        Returns:
            Tuple of (content, metadata)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from first heading or filename
            title = None
            for line in content.split('\n')[:20]:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            if not title:
                title = file_path.stem.replace('-', ' ').title()

            # Create metadata
            metadata = {
                "title": title,
                "source_file": str(file_path),
                "source_type": "markdown",
                "url": self._file_path_to_url(file_path)
            }

            return content, metadata

        except Exception as e:
            print(f"[ERROR] Error reading file {file_path}: {e}")
            return "", {}

    def _file_path_to_url(self, file_path: Path) -> str:
        """Convert file path to documentation URL"""
        # Convert: my-website/docs/Module-1-ROS2/Week-1/file.mdx
        # To: /docs/Module-1-ROS2/Week-1/file

        parts = file_path.parts
        try:
            docs_index = parts.index('docs')
            url_parts = parts[docs_index + 1:]  # Skip 'docs' directory
            url_path = '/'.join(url_parts)
            # Remove file extension
            url_path = url_path.replace('.mdx', '').replace('.md', '')
            return f"/docs/{url_path}"
        except (ValueError, IndexError):
            return f"/{file_path.name}"

    async def ingest_file(self, file_path: Path, db_session):
        """Ingest a single file into the database and vector store"""
        print(f"\n[FILE] Processing: {file_path.name}")

        # Read file
        content, metadata = self.read_markdown_file(file_path)
        if not content:
            print(f"  [WARN] Skipping empty file")
            return 0

        print(f"  Content length: {len(content)} characters")

        # Check if document already exists
        from sqlalchemy.future import select
        result = await db_session.execute(select(Document).filter_by(url=metadata["url"]))
        existing_doc = result.scalar_one_or_none()
        if existing_doc:
            print(f"  [WARN] Document already exists (URL: {metadata['url']}), skipping...")
            return 0

        # Create document record
        doc_id = uuid.uuid4()
        document = Document(
            id=doc_id,
            title=metadata["title"],
            content=content,
            url=metadata["url"],
            source_type=metadata["source_type"],
            metadata_=metadata
        )
        db_session.add(document)

        # Chunk the content
        chunks = self.chunk_text(content, metadata)
        print(f"  Split into {len(chunks)} chunks")

        # Process chunks in batches
        batch_size = 10
        total_ingested = 0

        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            chunk_texts = [chunk[0] for chunk in batch_chunks]

            # Generate embeddings
            try:
                embeddings = await self.embedding_service.create_embeddings(
                    texts=chunk_texts,
                    input_type="search_document"
                )
            except Exception as e:
                print(f"  [ERROR] Error generating embeddings: {e}")
                continue

            # Store in Qdrant and PostgreSQL
            points = []
            for j, (chunk_text, chunk_metadata) in enumerate(batch_chunks):
                chunk_id = str(uuid.uuid4())
                chunk_index = chunk_metadata["chunk_index"]

                # Create PostgreSQL record
                db_chunk = DocumentChunk(
                    id=uuid.UUID(chunk_id),
                    document_id=doc_id,
                    content=chunk_text,
                    chunk_index=chunk_index,
                    embedding_vector_id=chunk_id,
                    token_count=len(chunk_text.split())
                )
                db_session.add(db_chunk)

                # Create Qdrant point
                point = models.PointStruct(
                    id=chunk_id,
                    vector=embeddings[j],
                    payload={
                        "content": chunk_text,
                        "document_id": str(doc_id),
                        "chunk_index": chunk_index,
                        "title": metadata["title"],
                        "url": metadata["url"]
                    }
                )
                points.append(point)

            # Upload to Qdrant
            try:
                await self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                total_ingested += len(points)
                print(f"  [OK] Ingested batch {i//batch_size + 1} ({len(points)} chunks)")
            except Exception as e:
                print(f"  [ERROR] Error uploading to Qdrant: {e}")

        # Commit database changes
        await db_session.commit()
        print(f"  [OK] Total chunks ingested: {total_ingested}")
        return total_ingested

    async def ingest_directory(self, docs_dir: Path):
        """Ingest all markdown files from a directory"""
        print(f"\n{'='*60}")
        print(f"[INGEST] Starting Document Ingestion")
        print(f"{'='*60}")
        print(f"Documentation directory: {docs_dir}")

        # Ensure Qdrant collection exists
        await self.ensure_collection_exists()

        # Find all markdown files
        md_files = list(docs_dir.glob('**/*.md'))
        mdx_files = list(docs_dir.glob('**/*.mdx'))
        all_files = md_files + mdx_files

        print(f"\nFound {len(all_files)} documentation files")
        print(f"  - .md files: {len(md_files)}")
        print(f"  - .mdx files: {len(mdx_files)}")

        if not all_files:
            print("[ERROR] No files found to ingest!")
            return

        # Get async database session
        total_chunks = 0
        successful_files = 0

        async with AsyncSessionLocal() as db_session:
            try:
                for file_path in all_files:
                    try:
                        chunks = await self.ingest_file(file_path, db_session)
                        total_chunks += chunks
                        if chunks > 0:
                            successful_files += 1
                    except Exception as e:
                        print(f"[ERROR] Error processing {file_path.name}: {e}")
                        continue

                print(f"\n{'='*60}")
                print(f"[OK] Ingestion Complete!")
                print(f"{'='*60}")
                print(f"Files processed: {successful_files}/{len(all_files)}")
                print(f"Total chunks ingested: {total_chunks}")
                print(f"{'='*60}\n")

            except Exception as e:
                print(f"[ERROR] Fatal error during ingestion: {e}")
                await db_session.rollback()


async def main():
    """Main entry point"""
    # Get the docs directory
    project_root = Path(__file__).parent.parent.parent  # Go up to project root
    docs_dir = project_root / "my-website" / "docs"

    if not docs_dir.exists():
        print(f"[ERROR] Documentation directory not found: {docs_dir}")
        print("Please update the docs_dir path in the script")
        return

    # Create ingester and run
    ingester = DocumentIngester()
    await ingester.ingest_directory(docs_dir)


if __name__ == "__main__":
    print("\n[START] Document Ingestion Script")
    print("=" * 60)
    asyncio.run(main())
