---
name: "input-validation"
description: "Ensure that all inputs in forms, APIs, or modules are valid, within allowed ranges, and handled properly. Activates when user mentions input, validation, or data constraints."
version: "1.0.0"
---

# Input Validation Skill

## When to Use This Skill
- User asks to "validate inputs" or "check data"
- User mentions forms, API requests, or system boundaries
- User wants to prevent crashes, security issues, or invalid data

## How This Skill Works
1. Determine valid input types (string, int, float, list, dict)
2. Identify allowed value ranges
3. Decide on handling invalid input (raise error, default, coerce)
4. Choose strict (reject) or lenient (accept) validation
5. Apply validation at system boundaries (API, DB, UI)

## Output Format
- List of input fields
- Type and range for each
- Suggested validation strategy
- Error handling approach
- Notes on system boundary

## Example
**Input**: "Validate user registration inputs"
**Output**:
- username: string, 3-50 chars, strict, raise ValueError
- password: string, 8-100 chars, strict, raise ValueError
- age: int, 13-120, strict, raise ValueError
- email: string, must contain @, strict, raise ValueError
