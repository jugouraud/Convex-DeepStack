<!-- Source: FRONTEND_GUIDELINES(2).md, section RELEASE. Original rule numbers preserved, qualified with FE. -->

## RELEASE

- **FE.RELEASE1 M** Define build artifact, configuration, hosting behavior, route fallback, cache layers, security headers, asset paths and environment boundaries for production delivery.
- **FE.RELEASE2 M** Ensure versioned JS/CSS assets and HTML cache behavior are compatible during rolling deployments; avoid stale HTML referring to missing bundles and old clients calling incompatible APIs.
- **FE.RELEASE3 M** For breaking client/server contract changes, define an overlap/migration strategy compatible with open tabs, cached clients and phased server deployment.
- **FE.RELEASE4 S** Roll out consequential UI/behavior changes with appropriate flags, canaries or staged exposure when supported; avoid adding feature-flag machinery for small low-risk changes.
- **FE.RELEASE5 M** For high-risk releases, establish actual stop/rollback criteria and post-deploy checks for user journeys, auth, error rates and relevant performance metrics.
- **FE.RELEASE6 M** Treat CSP, cookies, CORS, cache rules, redirects, CDN/edge rewrites and service-worker registration as functional/security changes requiring environment-level validation.
- **FE.RELEASE7 S** Record notable user-facing changes and deprecation/migration notes; remove obsolete flags, duplicate code and superseded assets only when safe and in scope.
- **FE.RELEASE8 M** When rolling back, account for persisted client data, old service workers, cached bundles, feature flags and server schema/API compatibility; a code rollback alone may not revert browser state.
