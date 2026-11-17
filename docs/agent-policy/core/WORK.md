<!-- Source: AGENTS_v1.6(1).md / WORK; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## WORK

- CORE.WORK1 M Define observable success, constraints, material assumptions, and the smallest convincing checks before consequential work.
- CORE.WORK2 M Clarify ambiguity changing behavior, APIs, ownership, persistence, security, or irreversible choices; otherwise state a conventional assumption and proceed.
- CORE.WORK3 M Keep edits request-related; match local style. Remove only change-created orphans; leave unrelated cleanup and dead code alone.
- CORE.WORK4 M Choose the smallest correct, readable implementation preserving real boundaries. Reuse existing mechanisms; add abstractions, state, configuration, dependencies, or generality only for demonstrated needs, invariants, or measured benefit.
- CORE.WORK5 M Run applicable existing checks; establish baseline when useful, fix failures, rerun affected checks. Report actual results and unverified behavior honestly.
- CORE.WORK6 M Review the final diff for excess code, speculative behavior, unnecessary abstractions, unrelated edits, boundary violations, leaks, and residual risk. Remove unnecessary additions, rerun affected checks, and treat AI-written code as an untrusted draft.
- CORE.WORK7 M Apply proportional, gated patch passes: scope/test design, implementation, subtraction, runtime-efficiency audit, test-suite audit, and final verification. Critical passes are reduction-first; add code only for a demonstrated requirement, invariant, boundary, or efficiency need. Stop when no justified improvement remains.
- CORE.WORK8 M Facilitate human review with a compact PDF diff report for each delivered patch when PDF generation is available. Render the actual final diff as color-coded code blocks (green additions, red removals, neutral context), identify each file/hunk, and give a concise plain-language reason for each hunk. Explain why, not merely what; keep claims evidence-based and do not omit changed lines for brevity.

### Minimal-patch execution (every code change; WORK4/WORK6/WORK7)

Implement only requested behavior with existing patterns and direct logic. Default the budget for new abstractions, files, dependencies, configuration, and infrastructure to zero; exceed it only with a concrete justification. After implementation, perform a subtraction review even for trivial patches. Minimize moving parts and avoidable runtime work, not merely lines of code. Never weaken domain, security, concurrency, testing, or adopted-boundary requirements for compactness.

### Gated patch passes (WORK7)

1. **Scope and test design (read-only):** Identify the smallest affected boundary and available primitives; define observable behavior, invariants, relevant workload, and the minimum meaningful tests. For confirmed bugs, establish a reproducing regression where practical (TEST8).
2. **Minimal implementation (edits permitted):** Implement the requested behavior directly with focused tests; do not add speculative extensibility, fallback systems, or unrelated refactors.
3. **Subtraction (reduction-first):** Challenge every added helper, abstraction, branch, state variable, dependency, configuration option, and harness. Delete, inline, or consolidate only where clarity and required behavior are preserved. A valid result is no further change.
4. **Runtime-efficiency audit (evidence-gated):** Examine algorithms, repeated work, I/O/queries, allocations, transfers, and hot paths. Remove identifiable waste using simple mechanisms first. Measure consequential optimization claims against representative workloads and baselines (OPT1–OPT3); do not add caches, concurrency, or specialized machinery without demonstrated benefit.
5. **Test-suite audit (reduction-first):** Check changed behavior, boundaries, invariants, and meaningful failure modes; remove redundant cases, private-call assertions, overmocking, and excess fixtures/harnesses. Prefer the lowest reliable layer and real contract/integration checks where required (TEST1–TEST13). Preserve valuable regressions; add missing coverage only for a specific risk.
6. **Final verification (validation-only by default):** Run applicable checks, inspect the final diff and complexity justifications, and report actual test results, measured performance when relevant, and residual uncertainty. Prepare the final diff review (WORK8) after checks. Fix proven failures, then repeat only affected audits and checks.

**Proportional execution:** Trivial changes combine implementation, subtraction, and verification; ordinary patches combine the two audits when practical; performance-sensitive or high-risk changes use distinct passes and measurements. Passes are objectives, not a requirement for separate agents or elaborate reports. Critical passes must not generate features or speculative infrastructure; do not iterate indefinitely.

### Compact PDF diff review (WORK8)

Generate the report from the verified final patch, not an invented example. Start with a short summary and actual check results, then show each diff hunk as a legible, monospaced unified-diff block labeled by path and hunk location. Use green with `+` for added lines, red with `-` for removed lines, and neutral styling for context; do not depend on color alone. Put a one-sentence **why** beside or immediately above each hunk, grouping only hunks with the same rationale. Preserve all added/removed lines, mark omitted unchanged context, and wrap long lines without clipping; paginate rather than shrinking text until unreadable. Aim for one or two pages for small patches, not a fixed page limit. State testing and performance evidence accurately; redact sensitive values and label any omissions. For nontext changes, describe the artifact and review limit rather than fabricating a code diff. If a PDF cannot be created, give the equivalent hunk-by-hunk review in the delivery message and say why.
