<!-- Source: BACKEND_GUIDELINES(1).md, section CONFIG. Original rule numbers preserved, qualified with BE. -->

## CONFIG

- **BE.CONFIG1 M** Distinguish build, deployment, runtime, and request/tenant configuration; define provenance, defaults, validation, ownership, and change semantics for each.
- **BE.CONFIG2 M** Validate required configuration at startup/deployment and fail clearly for unsafe missing settings; never silently fall back to development credentials or permissive production policy.
- **BE.CONFIG3 M** Keep secrets in approved protected facilities with least privilege, rotation, expiry, revocation, and audit; environment variables alone are not an all-purpose secrets-management guarantee.
- **BE.CONFIG4 S** Keep configuration minimal, cohesive, and typed; avoid duplicate env keys, contradictory settings, undocumented flags, and feature toggles with no lifecycle.
- **BE.CONFIG5 M** Treat TLS, CORS, cookies, authentication, trust proxy, rate limits, queue semantics, and storage encryption settings as security/behavior changes requiring review.
- **BE.CONFIG6 M** Document whether config changes require process restart, are dynamically refreshed, or are persisted per tenant; test mixed-version rollout implications when consequential.
- **BE.CONFIG7 S** Use deployment-platform secret/reference injection and explicit configuration contracts rather than committing `.env` files or replicating secrets across repos.
- **BE.CONFIG8 M** Do not let dynamic flags leave incompatible DB/API/event versions or inconsistent authorization policy; define precedence, expiry, rollback, and removal criteria.
- **BE.CONFIG9 S** Prefer fine-grained environment values over giant serialized settings blobs for deploy-specific parameters where discoverability and validation matter.
- **BE.CONFIG10 M** Separate data-plane behavior from control-plane privileges, and do not allow public request data to override trusted internal configuration unintentionally.
