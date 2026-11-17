<!-- Source: BACKEND_GUIDELINES(1).md, section OBS. Original rule numbers preserved, qualified with BE. -->

## OBS

- **BE.OBS1 M** Define actionable service signals for production-critical paths: request success/denial/failure, latency distribution, saturation, queue age, dependency errors, and domain integrity outcomes where meaningful.
- **BE.OBS2 M** Use structured logs with stable event names, severity, safe correlation identifiers, and bounded payloads; do not log raw secrets or full sensitive records by default.
- **BE.OBS3 S** Propagate trace/request/operation IDs through HTTP/RPC/jobs/messages using supported standards where available; protect tracing baggage from untrusted or secret-bearing values.
- **BE.OBS4 M** Keep metric label/tag cardinality bounded; never label by arbitrary user ID, email, full URL, raw query, request body, or unbounded exception string.
- **BE.OBS5 M** Make errors diagnosable while retaining safe external responses: log expected business rejection differently from bugs, unknown outcomes, and dependency failures.
- **BE.OBS6 S** Use OpenTelemetry or the established telemetry stack when it genuinely simplifies cross-service correlation; avoid a new observability platform for a local patch.
- **BE.OBS7 M** Align alerts with user-impacting SLO burn, data integrity, and urgent operational action where possible; avoid alert storms, unactionable alerts, and noisy symptom duplicates.
- **BE.OBS8 M** Observe migration progress, queue backlogs, consumer lag, DLQ, replication lag, backup status, and release health where those mechanisms are relied upon.
- **BE.OBS9 S** Sample or aggregate high-volume diagnostic events deliberately; preserve security/financial audit requirements separately from probabilistically sampled tracing.
- **BE.OBS10 M** Protect telemetry pipelines with access control, redaction, retention, cross-region policy, and incident-response auditability; observability must not bypass privacy rules.
- **BE.OBS11 M** When claiming incident improvement or latency changes, identify measurement windows and affected populations; a graph without comparable traffic is not sufficient evidence.
- **BE.OBS12 S** Prefer a small stable dashboard per service/customer journey over numerous decorative metrics; connect observed symptoms to plausible remediation paths.
- **BE.OBS13 M** Document runbook links and alert ownership for high-severity pages; do not create on-call alerts with no defined responder, diagnosis, or escalation path.
