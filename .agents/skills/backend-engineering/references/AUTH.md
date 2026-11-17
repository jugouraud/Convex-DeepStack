<!-- Source: BACKEND_GUIDELINES(1).md, section AUTH. Original rule numbers preserved, qualified with BE. -->

## AUTH

- **BE.AUTH1 M** Verify authentication with maintained protocols/libraries and explicit trust boundaries; never hand-roll password verification, OAuth/OIDC token parsing, or session protocols when vetted implementations fit.
- **BE.AUTH2 M** Authorize every protected action, object, tenant, field, export, administrative endpoint, and asynchronous job using the verified principal and server-held policy—not caller-supplied roles/IDs.
- **BE.AUTH3 M** Deny by default where no grant applies; implement least privilege and distinguish authentication, tenant membership, resource ownership, role, policy, and step-up requirements.
- **BE.AUTH4 M** Verify token signature, issuer, audience, lifetime, relevant algorithm/key constraints, and intended token type; do not accept an arbitrary signed JWT as an access token for any service.
- **BE.AUTH5 M** Use up-to-date OAuth/OIDC security guidance appropriate to the flow (including RFC 9700); avoid deprecated insecure grants and unsafe redirect/PKCE/client-secret assumptions.
- **BE.AUTH6 M** Bound session lifetime, rotation, revocation, logout, password reset, device/account changes, and token refresh behavior; design for compromised/expired credentials.
- **BE.AUTH7 M** Protect cookie-based sessions with appropriate `Secure`, `HttpOnly`, `SameSite`, scope, rotation, and CSRF controls; know the difference between same-origin, same-site, CORS, and credentialed requests.
- **BE.AUTH8 M** Protect service-to-service identity and permissions with scoped credentials and explicit authorization; mTLS or a private network alone does not grant object-level permissions.
- **BE.AUTH9 M** Prevent cross-tenant data access in reads, writes, background tasks, exports, metrics, and caches; cover denied tenant/object combinations in tests.
- **BE.AUTH10 S** Consider row-level security or policy engines when the actual threat model/complexity merits them; they supplement, not replace, correct principal/context propagation.
- **BE.AUTH11 M** Apply suitable anti-enumeration, abuse, throttling, and audit controls to login, recovery, invite, token minting, and sensitive administrative operations.
- **BE.AUTH12 S** Follow risk-appropriate NIST digital identity guidance and organizational policy; avoid outdated rules such as arbitrary periodic password rotation absent a defined need.
- **BE.AUTH13 M** Keep secret-bearing identity material out of URLs, logs, exceptions, traces, request dumps, source repositories, and untrusted analytics; treat redaction as a tested boundary.
