---
name: "performance-check"
description: "Provide guidance on performance considerations for features, APIs, or queries. Activates when user mentions speed, latency, or optimization."
version: "1.0.0"
---

# Performance Optimization Skill

## When to Use This Skill
- User asks to "optimize performance" or "check speed"
- User mentions slow APIs, large datasets, or efficiency concerns
- Quick guidance on bottlenecks without full deep-dive

## How This Skill Works
1. Assess expected data volume (small, medium, large)
2. Identify latency requirements (real-time, batch, offline)
3. Highlight obvious N+1 query risks
4. Suggest caching strategies (if repeated queries)
5. Recommend suitable data structures (hash, tree, list)
6. Suggest profiling if needed

## Output Format
- Potential bottlenecks
- Suggested optimizations
- Quick action items

## Example
**Input**: "Check performance of fetching user posts"
**Output**:
- Data volume: ~50k posts
- Latency requirement: <200ms
- N+1 query risk: Yes, fetching posts and comments separately
- Caching: Cache popular queries
- Data structures: Hash index for user→posts, post→comments
- Recommendation: Profile endpoint, optimize queries, implement caching
