# Deployment Guide - Hugging Face Spaces

## Prerequisites

1. **Hugging Face Account** - https://huggingface.co
2. **Git** installed
3. **Docker** installed

## Files Created

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Docker image definition |
| `backend/.env.example` | Environment variables template |
| `backend/ructor.yaml` | HF Spaces configuration |

## Step 1: Prepare Your Repository

```bash
# Go to backend directory
cd backend

# Initialize git (if not already initialized)
git init
git add .
git commit -m "Prepare for HF Spaces deployment"
```

## Step 2: Create a New HF Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `docusaurus-chatbot-backend`
   - **SDK**: Docker
   - **Hardware**: CPU (2 vCPU, 4GB RAM recommended)
3. Click **Create Space**

## Step 3: Push to HF Spaces

```bash
# Install HF CLI
pip install -U huggingface_hub

# Login to Hugging Face
huggingface-cli login

# Add HF as remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/docusaurus-chatbot-backend

# Push to HF
git push space main:main
```

## Step 4: Add Secrets

After pushing, go to your Space: https://huggingface.co/spaces/YOUR_USERNAME/docusaurus-chatbot-backend

1. Click **Settings** → **Variables and secrets**
2. Add the following secrets:

| Variable | Value |
|----------|-------|
| `COHERE_API_KEY` | Your Cohere API key from https://dashboard.cohere.com |
| `QDRANT_URL` | Qdrant Cloud URL (e.g., `https://xxx-xxx.aws.cloud.qdrant.io:6333`) |
| `QDRANT_API_KEY` | Qdrant Cloud API key |
| `DATABASE_URL` | Neon Postgres connection string |

3. Click **Save**

## Step 5: Restart the Space

1. Go to your Space's **Settings** tab
2. Click **Restart** under **Actions**
3. Wait for the space to rebuild (~2-3 minutes)

## Step 6: Test the API

Your backend will be available at:
```
https://YOUR_USERNAME-docusaurus-chatbot-backend.hf.space
```

Test endpoints:
- `GET https://YOUR_USERNAME-docusaurus-chatbot-backend.hf.space/health`
- `GET https://YOUR_USERNAME-docusaurus-chatbot-backend.hf.space/docs` (Swagger UI)

## Step 7: Update Frontend

In `my-website/`, set the environment variable before building:

```bash
# Windows (PowerShell)
$env:REACT_APP_API_BASE_URL="https://YOUR_USERNAME-docusaurus-chatbot-backend.hf.space"

# Build the frontend
cd my-website
npm run build

# Deploy (e.g., to Vercel, Netlify, or GitHub Pages)
```

## Alternative: Deploy Frontend to HF Spaces Too

You can also deploy the Docusaurus site to HF Spaces:

1. Create a new Space: `docusaurus-chatbot-frontend`
2. Use **Static** SDK
3. Push your `my-website/build` folder

## Troubleshooting

### Container fails to start
- Check logs in HF Spaces UI
- Ensure all secrets are added
- Verify `Dockerfile` is in the root of the Space

### 404 on API calls
- Make sure frontend `REACT_APP_API_BASE_URL` points to your backend Space URL
- Check CORS settings in FastAPI

### Slow responses
- Your backend has no GPU - AI responses may be slower
- Consider upgrading to GPU hardware on HF

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────┐
│  Docusaurus     │────▶│  HF Spaces Backend   │────▶│  Qdrant     │
│  Frontend       │     │  (FastAPI + Docker)  │     │  Cloud      │
│  (Static)       │     │                      │     └─────────────┘
└─────────────────┘     └──────────────────────┘           │
                              │                           │
                              ▼                           ▼
                        ┌─────────────┐           ┌─────────────┐
                        │  Cohere     │           │  Neon       │
                        │  API        │           │  Postgres   │
                        └─────────────┘           └─────────────┘
```
