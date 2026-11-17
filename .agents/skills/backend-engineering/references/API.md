<!-- Source: BACKEND_GUIDELINES(1).md, section API. Original rule numbers preserved, qualified with BE. -->

## API

- **BE.API1 M** Define request/response schemas, authentication, authorization, method semantics, status codes, content types, idempotency, pagination, and error contracts; keep implementation and documented contract aligned.
- **BE.API2 M** Honor HTTP semantics where using HTTP: safe methods must not intentionally commit unsafe effects; distinguish `PUT`/`PATCH`/`POST`, caching, validators, redirects, and status codes appropriately.
- **BE.API3 M** Validate size, type, shape, encodings, and resource bounds at the server boundary; frontend constraints are usability hints, not security or integrity enforcement.
- **BE.API4 M** Enforce authorization per action and object/tenant/field at the server; a valid token, hidden UI control, or guessed resource ID is not sufficient authorization.
- **BE.API5 M** Define and test compatibility for public clients, mobile apps, integrations, and concurrent deployments before removing/renaming fields or changing status/error meaning.
- **BE.API6 S** Prefer a consistent machine-readable error envelope (e.g. RFC 9457 where suitable) with safe messages and actionable client codes; avoid exposing stack traces, SQL, or internal topology.
- **BE.API7 M** Make pagination bounded with deterministic ordering and documented cursors/offset behavior; authorize every page and avoid unstable or unbounded list responses.
- **BE.API8 M** Specify mutation idempotency and duplicate handling; a timeout means **outcome unknown**, not necessarily failure, and retries may repeat side effects.
- **BE.API9 S** Use conditional requests, caching, or batch interfaces only where justified by contract and measured usage; do not create excessive network round-trips for avoidable N+1 calls.
- **BE.API10 M** Normalize and encode paths, query parameters, headers, URLs, and redirects with context-aware libraries; do not concatenate user input into privileged destinations.
- **BE.API11 M** Establish limits for body parsing, multipart uploads, decompression, response generation, streaming, and slow clients; reject overload safely.
- **BE.API12 S** Prefer schema-first or contract-first tooling (e.g. OpenAPI) when it reduces consumer drift; tooling does not make implementation correct or a spec automatically backward-compatible.
- **BE.API13 M** Authenticate webhooks and callbacks, protect against replay according to the provider protocol, handle duplicates/out-of-order events, and respond according to acknowledged delivery semantics.
- **BE.API14 M** Define CORS, CSRF, cookie, origin, credential, and reverse-proxy trust behavior separately. CORS is a browser read policy, not authentication or server-side authorization.
- **BE.API15 S** Avoid version numbers that are meaningless placeholders or automatic one-version-per-change churn; adopt versioning/deprecation that matches actual compatibility needs and client lifecycles.
- **BE.API16 M** Preserve legitimate caching/privacy semantics, media-type negotiation, charset/encoding behavior, and resource visibility in public endpoints; test varied Accept/Content-Type behavior when affected.
