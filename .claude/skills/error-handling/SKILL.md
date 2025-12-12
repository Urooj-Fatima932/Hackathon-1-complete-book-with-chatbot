---
name: "error-handling"
description: "Provide consistent and clear error handling for APIs, modules, and features. Activates when user mentions errors, exceptions, or failure cases."
version: "1.0.0"
---

# Error Handling Skill

## When to Use This Skill
- User asks to "handle errors" or "manage exceptions"
- User mentions API failures, crashes, or invalid data
- User wants clear, actionable error messages

## How This Skill Works
1. Identify potential error types (validation, network, database, runtime)
2. Decide on error response type (raise exception, return error code, fallback)
3. Define error message clarity (descriptive, user-friendly, or developer-focused)
4. Decide fail-fast or fail-gracefully strategy
5. Ensure logging or tracking for debugging and analytics

## Output Format
- Error type
- Handling strategy
- Message template
- Optional logging / monitoring instructions

## Example
**Input**: "Handle errors in user registration API"
**Output**:
- ValidationError: raise ValueError, "Username must be 3-50 characters"
- DatabaseError: log error, return 500, "Database unavailable"
- NetworkError: retry 3 times, then return 503, "Service temporarily unavailable"
- UnexpectedError: log, alert admin, return 500, "Unexpected server error"
