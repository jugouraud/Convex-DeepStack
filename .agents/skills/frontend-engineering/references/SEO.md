<!-- Source: FRONTEND_GUIDELINES(2).md, section SEO. Original rule numbers preserved, qualified with FE. -->

## SEO

- **FE.SEO1 M** Apply this section to public content intended for search engines; authenticated/private applications do not require unnecessary SEO infrastructure.
- **FE.SEO2 M** Ensure discoverable pages provide crawlable meaningful content, stable routes and appropriate status codes; do not assume every crawler will execute JavaScript identically.
- **FE.SEO3 S** Supply unique descriptive titles and page-specific descriptions for important public routes; use canonical links only when they reflect real canonical intent.
- **FE.SEO4 M** Prevent accidental indexing of private, staging, duplicate, search-result or sensitive routes through appropriate server/deployment controls; robots directives do not substitute for authorization.
- **FE.SEO5 S** Use structured data only for genuinely represented content and supported vocabularies; do not invent ratings, availability, authors or other schema claims.
- **FE.SEO6 M** Keep internal navigation as actual links with useful `href` values; preserve crawlable pagination/route relationships where public discovery depends on them.
- **FE.SEO7 S** Maintain sitemap, robots and locale alternate links only where applicable; ensure generated paths are correct after deployments and migrations.
- **FE.SEO8 M** Align metadata, canonical URLs, redirects and HTTP status with actual content and publication state; avoid presenting error pages as success-shaped `200` content.
