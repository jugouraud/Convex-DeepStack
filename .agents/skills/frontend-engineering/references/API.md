<!-- Source: FRONTEND_GUIDELINES(2).md, section API. Original rule numbers preserved, qualified with FE. -->

## API

- **FE.API1 M** Respect documented request/response media types, versions, schemas, statuses, pagination and error contracts; verify breaking changes against real provider/consumer boundaries.
- **FE.API2 M** Handle HTTP non-success statuses distinctly from network exceptions; `fetch` resolving does not mean the server accepted the operation.
- **FE.API3 M** Set appropriate cancellation/timeouts and bounded retries for remote work; retries of mutations require idempotency or an equivalent safe contract. A timeout can leave the outcome unknown.
- **FE.API4 M** Never trust data received from APIs, URL parameters, postMessage, workers, local storage or injected SSR payloads without the validation appropriate to the boundary.
- **FE.API5 S** Avoid request waterfalls: fetch at the earliest appropriate route/server boundary, batch known requests when supported, and measure before introducing preload/prefetch machinery.
- **FE.API6 M** Encode URLs/query parameters correctly using platform APIs; distinguish route segments, search params, origin, fragments and user-influenced redirect destinations.
- **FE.API7 M** Define authorization, credentials, CSRF and CORS expectations with the server; a permissive CORS response is not permission to read another user's data.
- **FE.API8 S** Choose pagination/infinite loading based on task and accessibility; support stable ordering, terminal states, re-entry and back-navigation where relevant.
- **FE.API9 M** Bound file uploads/downloads, streaming buffers and response parsing according to product limits; browser-side checks are supplementary to authoritative server limits.
- **FE.API10 S** Normalize remote errors at a bounded adapter layer while preserving actionable distinctions (offline, auth, permission, validation, rate limit, conflict, server failure).
- **FE.API11 M** For realtime subscriptions/WebSockets/EventSource, authenticate and re-authorize as designed, bound queues, reconnect with backoff, handle ordering/resume and dispose on ownership changes.
- **FE.API12 M** Avoid exposing cross-origin credentials, tokens, private request data or internal service endpoints through logs, query strings and public client bundles.
