<!-- Source: AGENTS_v1.6(1).md / LOG; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## LOG

- CORE.LOG1 M Return stable bounded useful errors, no stack/SQL/internal paths/secrets/raw upstream or rejected data; account for authentication/recovery enumeration incl status/timing.
- CORE.LOG2 M Allowlist telemetry fields; exclude secrets and unnecessary personal content across logs/traces/analytics/exception capture; safely serialize and bound untrusted values.
- CORE.LOG3 M Record relevant security outcomes with minimal protected actor/resource/action/result/context; correlate failures; protect telemetry access/integrity; define retention/deletion.
- CORE.LOG4 M Bound logging work/failures so diagnostics cannot exhaust resources or silently bypass required security decisions.
- CORE.LOG5 S Use few meaningful metrics, bounded label cardinality, and aggregated repeated failures; distributed tracing only for operational benefit.
