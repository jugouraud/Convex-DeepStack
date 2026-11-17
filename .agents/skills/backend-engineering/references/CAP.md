<!-- Source: BACKEND_GUIDELINES(1).md, section CAP. Original rule numbers preserved, qualified with BE. -->

## CAP

- **BE.CAP1 M** Estimate capacity using representative arrival rates, service-time distribution, per-request resource demand, concurrency, fan-out, and downstream limits; do not scale just one tier blindly.
- **BE.CAP2 M** Bound admission, queue length, worker concurrency, connection pools, and per-tenant quotas when untrusted/variable traffic can exhaust finite resources.
- **BE.CAP3 M** Distinguish sustained capacity from short bursts, cold-start effects, autoscale delay, and downstream bottlenecks; set burst/surge protections accordingly.
- **BE.CAP4 S** Favor simple horizontal/vertical scaling only where the bottleneck and state model permit it; scaling workers can worsen DB contention, vendor throttling, and retry storms.
- **BE.CAP5 M** Apply backpressure, overload responses, and load shedding honestly; avoid silent job loss or claiming accepted durable work when none was recorded.
- **BE.CAP6 M** Prevent noisy-neighbor interference where shared infrastructure handles multiple tenants/classes: resource budgets, priority, fairness, and costly-query safeguards as applicable.
- **BE.CAP7 S** Use Little's Law and queueing intuition to investigate rising latency/backlog, but validate model assumptions and avoid presenting capacity estimates as measured SLOs.
- **BE.CAP8 M** Plan capacity for migrations, backups, replays, cache cold starts, failover, and high-traffic rollouts when they can compete with production load.
- **BE.CAP9 S** Monitor saturation signals—CPU, memory/GC, DB/pool limits, queue age, disk/network I/O, and throttling—rather than autoscaling on one misleading metric.
- **BE.CAP10 M** Do not let cost controls bypass security, retention, reliability, or promised consistency; document explicit trade-offs for lower-cost service tiers.
