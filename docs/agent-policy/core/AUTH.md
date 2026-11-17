<!-- Source: AGENTS_v1.6(1).md / AUTH; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## AUTH

- CORE.AUTH1 M Deny unless explicit policy permits; cover every protected path and actor/tenant/object/action/field scope; missing/failed policy cannot grant access.
- CORE.AUTH2 M Derive principal/tenant membership from verified context; authorize selectors; scope caches/search/jobs/storage/downloads and handle revocation/stale permissions.
- CORE.AUTH3 M Verify token signature/authenticity, allowed algorithms/trusted keys, issuer, audience, expiry, and token type with maintained identity implementations.
- CORE.AUTH4 M Protect session credentials; Secure/HttpOnly/appropriate SameSite/narrow cookies; rotate on login/privilege changes, expire/invalidate; risk-based step-up/reauthentication.
- CORE.AUTH5 M Use appropriate framework CSRF defenses for ambient browser credentials; no GET mutations. CORS is not authorization; preserve TLS, auth, escaping, and CSRF defaults.
