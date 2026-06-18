# URL Sourcing Rules for Deep Research

## Authoritative Sources (ALWAYS prefer)
- Official documentation (e.g., `docs.python.org`, `nextjs.org/docs`, `react.dev`)
- Official API references (e.g., `developer.mozilla.org`, `apidocs.example.com`)
- Official usage guides and tutorials from the maintainers
- Source code repositories (e.g., `github.com/org/repo` — only the source, not blog posts)
- Published specifications (e.g., `spec.graphql.org`, `json-schema.org`)

## Prohibited Sources (NEVER use)
- Blog posts (any URL containing "blog" or "news")
- Changelogs and release notes
- Marketing pages and landing pages
- Comparison articles ("X vs Y")
- Medium articles, Dev.to posts, personal blogs
- AI-generated content farms

## Fallback Chain
1. Official docs (primary target)
2. API reference pages
3. Usage guides / tutorials from official sources
4. GitHub README / source code comments
5. ONLY if all above fail: ask the user for better URLs

## Verification
- Every claim MUST include the exact source URL
- If a URL returns 404, try with `research_browse_js` before giving up
- If the content is behind a login wall, note it as "source requires authentication"
