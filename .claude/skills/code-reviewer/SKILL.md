---
name: "code-reviewer"
description: "Performs systematic code reviews checking for security, performance, maintainability, and best practices. Activates when user asks to review code or provide feedback."
version: "1.0.0"
---

# Code Review Skill

## When to Use This Skill
- User asks to "review code" or "check code quality"
- User wants suggestions for improvements in security, performance, or maintainability
- User is preparing hackathon project code for submission or collaboration

## How This Skill Works
1. Check for security issues (e.g., input validation, sensitive data exposure)
2. Analyze performance (loops, memory usage, N+1 queries)
3. Evaluate code style and readability (consistent naming, indentation, comments)
4. Suggest best practices (modularization, DRY principle, reusable functions)
5. Highlight potential bugs or edge cases
6. Provide clear, actionable feedback

## Output Format
- Security: List vulnerabilities and suggestions
- Performance: Potential bottlenecks and improvements
- Code Style: Readability, consistency, naming conventions
- Best Practices: Recommendations for cleaner, maintainable code
- Potential Bugs: Edge cases or logical errors
- Suggested Improvements: Prioritized actionable steps

## Example
**Input**: "Review my Python hackathon project code"
**Output**:
- **Security**:
  - Validate user inputs in API endpoints
  - Avoid hard-coded credentials
- **Performance**:
  - Use list comprehensions instead of loops for filtering
  - Cache repeated database queries
- **Code Style**:
  - Consistent indentation and naming
  - Add docstrings for public functions
- **Best Practices**:
  - Break large functions into smaller reusable functions
  - Follow DRY principle for repeated logic
- **Potential Bugs**:
  - Division by zero not handled
  - Missing error handling on file uploads
- **Suggested Improvements**:
  1. Add input validation functions
  2. Refactor repeated code blocks
  3. Implement caching where needed
