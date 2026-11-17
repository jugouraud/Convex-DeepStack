<!-- Source: AGENTS_v1.6(1).md / TEST; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## TEST

- CORE.TEST1 M Test behavior/invariants at lowest reliable level; unit-test nontrivial domain logic where practical. No tests solely for annotations, trivial forwarding, private call order, or trusted libraries.
- CORE.TEST2 M Verify SQL/mappings/constraints/transactions on real DB (prefer production engine family), serialization/API/producer–consumer contracts at real boundaries; never mock integration under test.
- CORE.TEST3 M Cover relevant valid/invalid/boundary cases, state transitions, rejection/failure invariants, permission denials, and duplicate effects; use controlled concurrency for race claims.
- CORE.TEST4 S Choose partitions, both sides of boundaries, decision/state tables; parameterize equivalent cases. Use properties/fuzzing for clear invariants and broad input spaces.
- CORE.TEST5 M Use behavior names and clear arrange/act/assert; derive expectations independently; assert observable state or contractually meaningful interactions.
- CORE.TEST6 M Isolate data/resources/accounts; control relevant time/randomness/side effects; no order dependence, arbitrary sleeps, or production credentials/data/services.
- CORE.TEST7 S Use real fast collaborators; stub costly/nondeterministic boundaries. Keep fixtures/scenario values explicit; avoid mock chains, artificial interfaces, and unnecessary harnesses.
- CORE.TEST8 S For confirmed bugs, reproduce intended failure before fixing; retain regression cases. Characterize affected behavior before substantial insufficiently tested refactors.
- CORE.TEST9 M Keep E2E on critical workflows; use stable semantic selectors/readiness, isolated accounts, privacy-safe diagnostics; automate applicable critical workflows.
- CORE.TEST10 M Document test commands; run relevant PR/integration/contract gates; fail on failures. Never weaken assertions, silence tests, discard fixed-bug regressions, or retry indefinitely.
- CORE.TEST11 S Use configured coverage diagnostically, mutation testing selectively; do not chase percentages. Schedule costly performance/resilience checks separately when appropriate.
- CORE.TEST12 M Never mock the subject under test; keep fake behavior consistent with production contracts; verify important integration contracts against real implementations.
- CORE.TEST13 M Review uncovered changed critical branches; investigate reproducible flakes. Temporary quarantine requires a tracked issue and explicit resolution criteria.
