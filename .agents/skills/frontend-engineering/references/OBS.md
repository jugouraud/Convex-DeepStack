<!-- Source: FRONTEND_GUIDELINES(2).md, section OBS. Original rule numbers preserved, qualified with FE. -->

## OBS

- **FE.OBS1 M** Define a small set of actionable client signals for consequential journeys: failed navigation/API requests, unhandled exceptions, critical interaction failures and relevant real-user performance.
- **FE.OBS2 M** Minimize and allowlist telemetry content. Redact secrets, tokens, private URLs, sensitive DOM/form values, query parameters and identifying user content before capture.
- **FE.OBS3 S** Correlate frontend errors with request/release context using safe identifiers; control metric-cardinality and avoid unlimited per-user/per-URL labels.
- **FE.OBS4 M** Distinguish actual user-facing errors from intentional cancellations, ad-blocked optional vendors and noncritical third-party faults to avoid misleading dashboards.
- **FE.OBS5 M** If reporting Core Web Vitals, segment by meaningful device/route and use comparable field populations; do not report percentile improvements from unrepresentative small samples.
- **FE.OBS6 S** Use source maps for diagnosis under deliberate access controls; avoid turning production errors into verbose developer-facing overlays or exposing internal stack details to users.
- **FE.OBS7 M** Track telemetry retention/access/consent requirements and verify SDK behavior under privacy choices; observability must not bypass the privacy policy.
- **FE.OBS8 S** Introduce tracing, session replay or new monitoring SDKs only when a concrete debugging or product need outweighs extra bytes, privacy exposure and operations cost.
