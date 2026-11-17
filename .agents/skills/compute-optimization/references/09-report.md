## 9. Mandatory deliverable template for an optimization task

An agent should finish its work with this succinct, evidence-backed report:

```markdown
## Goal and constraints
- Original task / user-visible metric:
- Accuracy / data restrictions:
- Environment and representative inputs:

## Baseline and dominant bottleneck
- Command + environment + reproducible input:
- Whole-job wall time (cold/warm, n, spread):
- Profiler evidence and Amdahl / roofline bound:

## Candidate changes
1. CPU algorithm / memory / threading / compiler: ...
2. Remote GPU design and transfer path (if permitted): ...

## Correctness
- Differential and edge-case tests; numerical errors:

## Results
| Candidate | Whole-job cold | Whole-job warm | Compute | Upload/download | H2D/D2H | RAM/VRAM | Pass? |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Decision
- Winner for one cold job:
- Winner for N repeated jobs / crossover N:
- Robustness, quota, cost, privacy, remaining bottleneck:
- Kept/reverted changes and reproduction instructions:
```

**Never bury “GPU device-only” speedup in the primary result.** If you cannot measure a required stage, explicitly say so and downgrade the confidence of the recommendation.

---
