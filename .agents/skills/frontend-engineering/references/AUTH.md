<!-- Source: FRONTEND_GUIDELINES(2).md, section AUTH. Original rule numbers preserved, qualified with FE. -->

## AUTH

- **FE.AUTH1 M** Enforce authentication and authorization on the server for every protected resource/action/tenant/object/field; client route guards and hidden controls are UX, never security boundaries.
- **FE.AUTH2 M** Derive user/tenant/role from a verified server-side principal, not user-editable frontend state or request parameters; scope APIs, caches, downloads and subscriptions accordingly.
- **FE.AUTH3 M** Use maintained session/OIDC/OAuth implementations appropriate to the flow; do not invent token verification, password storage, cryptographic login or redirect protocols in frontend code.
- **FE.AUTH4 M** Protect browser sessions with server-set `Secure`, `HttpOnly` and appropriately scoped `SameSite` cookies when using cookie sessions; select CSRF defenses appropriate to ambient credentials and threat model.
- **FE.AUTH5 M** Treat token storage/refresh as a threat-model decision; never place session secrets in URLs or expose them in telemetry, browser logs, source files or build artifacts.
- **FE.AUTH6 M** Handle login, logout, expiry, revocation, account/tenant switching, step-up and forbidden responses coherently; invalidate appropriately scoped caches without retaining protected UI data.
- **FE.AUTH7 M** Validate post-login `returnTo` and redirect destinations against a safe policy; prevent open redirects and login CSRF where relevant.
- **FE.AUTH8 S** Keep auth-state UI distinct from resource authorization; show accurate pending/denied/expired states without leaking protected details or relying on a brief client-side hide after rendering.
