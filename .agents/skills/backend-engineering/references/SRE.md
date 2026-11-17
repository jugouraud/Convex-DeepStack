<!-- Source: BACKEND_GUIDELINES(1).md, section SRE. Original rule numbers preserved, qualified with BE. -->

## SRE

- **BE.SRE1 M** For production-critical services, define user-relevant service-level indicators and objectives, measurement windows, exclusions, and ownership; do not invent default percentages without product context.
- **BE.SRE2 S** Use error budgets to balance change velocity and reliability where an SLO process exists; account for error-budget policy rather than using it as an automatic release veto.
- **BE.SRE3 M** Establish actionable alerting for material user impact and integrity risk, with owner, severity, diagnosis link, and escalation; don't page on every transient internal error.
- **BE.SRE4 M** Keep runbooks for high-impact service operations: deploy rollback, failover, traffic isolation, token/key compromise, database pressure, queue backlog, restore, and critical vendor outage as applicable.
- **BE.SRE5 M** Define incident command/escalation, safe emergency access, communication responsibilities, and operational action traceability for systems that require on-call response.
- **BE.SRE6 S** Conduct blameless, evidence-based postmortems for consequential incidents; turn repeated failure modes into prioritized corrective actions with owners rather than checklist theater.
- **BE.SRE7 M** Treat toil/operational burden as part of architecture cost: every new queue, cache, datastore, cluster, and service needs an owner, observability, update path, and recovery plan.
- **BE.SRE8 S** Practice game days/fault exercises for high-consequence dependencies when feasible; focus on a plausible hazard and measurable recovery, not random chaos for its own sake.
- **BE.SRE9 M** Measure restoration and incident-detection claims from real tests/incidents or clearly labeled simulations; do not promise an RTO simply because a runbook exists.
- **BE.SRE10 S** Compare release/reliability health using consistent populations and long enough windows; DORA metrics and SLOs are diagnostic tools, not universal performance grades.
- **BE.SRE11 M** Keep an explicit security/compliance escalation path for leaked credentials, integrity compromise, data-loss suspicion, and suspected unauthorized access.
