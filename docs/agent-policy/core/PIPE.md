<!-- Source: AGENTS_v1.6(1).md / PIPE; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## PIPE

- CORE.PIPE1 M For project core workflows: one core step/file, exactly one public `run_<step>()` H1/step, and a separate final orchestrator composing step H1s only.
- CORE.PIPE2 M Never import/call another step's private helpers or depend on its private storage; pass cross-step state/contracts explicitly.
- CORE.PIPE3 S H2/H3 are optional; H1 may call direct code/libraries/helpers. Order imports/types/constants, needed helpers, then H1 preferably last.
- CORE.PIPE4 M Specify stage input/output, failure, artifact ownership, and numerical semantics: shape, units, ordering, dtype/device, score direction where relevant.
- CORE.PIPE5 M For scientific reproducibility record code/model/input/config revisions, split, seed, numerical semantics/tolerance; honor privacy limits. Seed alone does not guarantee reproducibility.
