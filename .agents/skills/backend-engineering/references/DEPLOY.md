<!-- Source: BACKEND_GUIDELINES(1).md, section DEPLOY. Original rule numbers preserved, qualified with BE. -->

## DEPLOY

- **BE.DEPLOY1 M** Identify the release artifact, runtime/config, target environment, DB/cache/event dependencies, rollout order, compatibility window, health signals, and stop/rollback criteria for consequential releases.
- **BE.DEPLOY2 M** Distinguish liveness from readiness; a process can be alive but unable to serve safely. Ensure readiness and graceful shutdown align with actual drain and dependency behavior.
- **BE.DEPLOY3 M** Preserve compatibility during mixed old/new deployments: requests, messages, schema, cache representations, queued jobs, and external clients may outlive one release.
- **BE.DEPLOY4 S** Use canary/staged/feature-flag rollout for high-risk changes where supported; do not mandate a new rollout platform for a low-risk patch.
- **BE.DEPLOY5 M** Define rollback and forward-fix limits honestly: code rollback cannot undo destructive database changes, sent emails/payments, key rotation, or externally observed side effects.
- **BE.DEPLOY6 M** Run environment-appropriate post-deploy checks of health, critical domain flow, auth, latency/error signals, queue lag, and unexpected schema/permission failures.
- **BE.DEPLOY7 M** Version and securely publish artifacts; retain enough provenance/configuration context to reproduce or investigate the deployed release.
- **BE.DEPLOY8 S** Prefer immutable artifacts deployed with environment-specific configuration over rebuilding code per environment when the platform permits.
- **BE.DEPLOY9 M** Ensure migrations, indexes, backfills, rollouts, and rollback sequencing do not require unsafe global downtime unless such downtime is explicitly approved and communicated.
- **BE.DEPLOY10 M** Handle startup, termination, signal forwarding, worker job draining, connection release, and health state for the real container/process supervisor.
- **BE.DEPLOY11 S** Keep deployment automation understandable and minimal; do not replace proven release tooling or add an orchestrator as part of a routine application feature.
- **BE.DEPLOY12 M** Review secrets, cloud permissions, network policies, public exposure, resource limits, and ingress paths affected by deployment manifests/IaC changes.
- **BE.DEPLOY13 M** Make production changes through authorized auditable paths, with safeguards against wrong-environment targeting and deliberate review for destructive operations.
- **BE.DEPLOY14 S** Track meaningful release and delivery metrics (lead time, failed changes, recovery) without treating raw deployment frequency as an excuse to bypass safety gates.
