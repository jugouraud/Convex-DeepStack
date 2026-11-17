<!-- Source: FRONTEND_GUIDELINES(2).md, section PRIV. Original rule numbers preserved, qualified with FE. -->

## PRIV

- **FE.PRIV1 M** Before adding personal-data collection or a vendor SDK, define purpose, fields, precision, recipients, permissions, retention, deletion and applicable consent/legal requirements with the product owner.
- **FE.PRIV2 M** Default optional tracking, social embeds and data sharing to privacy-protective states; enforce decisions in actual script/network loading and server-side processing, not just a banner's appearance.
- **FE.PRIV3 M** Avoid transmitting passwords, tokens, private form values, typed search queries or sensitive page content to logs, analytics, replay, error trackers or URL parameters without an explicitly approved need and controls.
- **FE.PRIV4 S** Prefer local computation, coarse measurements, aggregation, sampling and minimal retention when adequate; do not call pseudonymous IDs or hashed identifiers anonymous without analysis.
- **FE.PRIV5 M** Honor relevant consent changes, opt-outs, deletion and retention policies across client storage, service workers, third-party SDKs and caches where under project control.
- **FE.PRIV6 M** Document cookie/storage purpose and lifetime; distinguish necessary application state from optional profiling/tracking and comply with jurisdiction/project obligations.
- **FE.PRIV7 M** Sanitize/redact analytics properties and crash breadcrumbs by allowlist, including URLs, DOM snapshots, network bodies and accessibility labels that may contain user data.
- **FE.PRIV8 S** Avoid unnecessary session replay and full-content capture; if used, scope, mask and test it deliberately rather than relying on vendor defaults.
