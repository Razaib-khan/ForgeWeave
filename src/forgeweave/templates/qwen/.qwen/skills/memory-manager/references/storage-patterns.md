# Storage Patterns

## Cache Storage (ephemeral, auto-cleaned)
- Location: `.forge/cache/<namespace>/`
- Format: JSON files keyed by content hash
- Use for: HTTP responses, LLM completions, intermediate results
- TTL: Configurable per namespace (default 24h)

## Research Storage (persistent)
- Location: `research/<topic-slug>-*/`
- Format: Markdown with YAML frontmatter
- Use for: Research plans, raw findings, validated reports

## Session Storage (temp, per-session)
- Location: `.forge/sessions/<session-id>/`
- Format: JSON
- Use for: Debugging sessions, hypothesis tracking
- Cleanup: Deleted on session end

## Memory Limits
- Cache: 500MB default
- Research: No limit (gitignored)
- Sessions: 50MB per session
