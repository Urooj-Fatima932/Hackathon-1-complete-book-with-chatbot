---
name: "book-content-author"
description: "Help structure and organize textbook content: chapter outlines, section headers, examples, exercises, and cross-references. Activates when user mentions writing or structuring book content."
version: "1.0.0"
---

# Book Content Authoring Skill

## When to Use This Skill
- User asks to "write a chapter" or "organize book content"
- User mentions lessons, exercises, examples, or modules
- User wants consistent formatting across chapters

## How This Skill Works
1. Generate chapter outline based on topic
2. Maintain consistent formatting (headings, bullet points, examples)
3. Add learning objectives and exercises
4. Link concepts across chapters (cross-references)
5. Suggest improvements to clarity and flow

## Output Format
- Chapter title and number
- Section headers
- Learning objectives
- Example code or scenarios
- Exercises
- Notes / cross-references

## Example
**Input**: "Write Chapter 2 on ROS2 in my Physical AI textbook"
**Output**:
- **Chapter 2**: Introduction to ROS2
- **Sections**:
  1. ROS2 Basics
  2. Installation & Setup
  3. Nodes & Topics
  4. Simple Robot Example
  5. Exercises
- Learning objectives: understand ROS2 architecture, write basic publisher/subscriber nodes
- Notes: link to Chapter 1 concepts on sensors
