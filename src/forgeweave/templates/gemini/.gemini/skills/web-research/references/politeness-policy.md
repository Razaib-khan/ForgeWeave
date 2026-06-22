# Web Research: Politeness Policy

## Rate Limiting
- Minimum 1 second between requests to the same domain
- Maximum 5 concurrent requests across all domains
- Maximum 30 requests per domain per minute

## Retry Policy
- On timeout: retry once after 3 seconds
- On 429 (rate limited): wait `Retry-After` header or 10 seconds
- On 5xx: retry once after 5 seconds
- On 404: try Playwright fallback (SPAs may return 404)

## User-Agent
- `ForgeWeave/1.0 (Research Bot; https://github.com/Razaib-khan/forgeweave)`
- Always set a descriptive User-Agent header

## Robots.txt
- Respect `Disallow` rules for `/admin/`, `/api/`, `/private/`
- Allow crawling of public documentation pages
- If blocked by robots.txt, note it and try alternative sources

## Content Limits
- Maximum page size: 5MB per page
- Maximum crawl depth: 1 level (seed URLs only, no recursive following)
- Maximum links extracted per page: 50
