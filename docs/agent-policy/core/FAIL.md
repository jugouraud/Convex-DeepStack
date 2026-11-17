<!-- Source: AGENTS_v1.6(1).md / FAIL; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## FAIL

- CORE.FAIL1 S Propagate errors to a handler able to act; avoid blanket catches, redundant translation, speculative recovery, and success-shaped fallbacks.
- CORE.FAIL2 M Set finite remote timeouts/retries and cancellation behavior; retry only safely with bounded backoff/jitter; remote timeout can mean completion is unknown.
- CORE.FAIL3 M Bound exposed work before expense: bytes/expansion/depth/items, CPU/time, queries/results, concurrency/queue, disk/output, fan-out/model cost.
- CORE.FAIL4 M Use appropriate admission/rate/quota controls, including pre-auth work; reject overload predictably, cap retry amplification, release cancelled work/resources.
- CORE.FAIL5 S Measure capacity and recovery needs; distinguish availability from backup/recovery. Add circuit breakers, bulkheads, or tracing only for demonstrated benefit.
