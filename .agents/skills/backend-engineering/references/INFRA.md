<!-- Source: BACKEND_GUIDELINES(1).md, section INFRA. Original rule numbers preserved, qualified with BE. -->

## INFRA

- **BE.INFRA1 M** Apply infrastructure/platform rules to actual cloud, VM, container, orchestration, network, and managed-service resources; do not require Kubernetes or a service mesh by default.
- **BE.INFRA2 M** Define resource/IAM ownership, network trust, environment separation, tagging/accountability, backup/recovery, and lifecycle for infrastructure that production depends on.
- **BE.INFRA3 M** Use least-privilege IAM and network exposure; distinguish application identity, CI identity, human operations, database migration, and emergency recovery roles.
- **BE.INFRA4 M** Review IaC plans/diffs for deletions, replacements, drift, secret exposure, region changes, data-volume lifecycle, and unintended public access before apply.
- **BE.INFRA5 S** Prefer managed/platform-native mechanisms where they reduce demonstrated operations burden; account for vendor limits, lock-in, data locality, outages, and cost.
- **BE.INFRA6 M** Set realistic CPU/memory/disk/network/resource limits and requests for production workloads; understand what termination, OOM, eviction, and autoscaling do to in-flight work.
- **BE.INFRA7 M** Protect stateful storage against accidental destruction, unauthorized snapshots, misconfigured retention, and cross-environment use; test recovery at the intended layer.
- **BE.INFRA8 S** Keep local/staging/prod behavior similar on the failure-prone interfaces (database, auth, broker, network/proxy) while accounting for legitimate environment differences.
- **BE.INFRA9 M** Control east-west traffic/egress to sensitive services where the threat model requires it; shared private networking does not replace application identity and authorization.
- **BE.INFRA10 S** Consider regional/service quotas and provider failure domains in capacity and disaster planning; do not promise multi-region guarantees merely because the provider offers multiple regions.
- **BE.INFRA11 M** Preserve audit trails and rollback plans for security-sensitive infra changes; avoid using privileged admin credentials in routine application pods/build jobs.
