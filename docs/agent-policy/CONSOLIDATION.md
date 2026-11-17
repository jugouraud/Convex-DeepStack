# Consolidation decisions and provenance

The four supplied policy files were reviewed and reorganized into a compact always-loaded `AGENTS.md`, one shared CORE policy, and three specialist Codex skills with selectively readable topic references.

## True consolidation vs safe coexistence

- **WORK1–WORK8:** shared six-pass workflow from AGENTS v1.6 is canonical (`CORE.WORK1`…`CORE.WORK8`). The corresponding FE/BE WORK1–WORK8 are *aliases*, not copied again. Domain-specific supplemental scope/quality/test gates and the actual impact-to-check matrices live in each specialist's `WORK-addendum.md`.
- **Generic CODE principles:** shared names/cohesion/guards/abstraction/style rules live in `CORE.CODE`. FE and BE retain *only* their distinct code-specific lines in `CODE-addendum.md`; remaining frontend/backend CODE IDs are aliases to applicable shared concepts. This is a conceptual consolidation, **not** an assertion that the original wordings were identical.
- **Specialist topics:** intentionally retain `BE.SQL`, `BE.TXN`, `BE.MIG`, `FE.A11Y`, `FE.CSS`, `FE.PWA`, etc., even when they mention shared validation/security/performance concerns. Their contextual consequences and test duties are important; aggressive mechanical sentence deduplication could silently weaken policy. They load on demand, so inactive overlap does not consume prompts.
- **Performance specialist:** keep all original prose, math, CPU/GPU details, Colab CLI procedures, citations and reporting guidance as distinct small reference files. `SKILL.md` holds only routing and nonnegotiable experimental constraints.
- **Literature/reference appendices:** moved to `maintenance-literature.md` to prevent routine code edits loading citations and research catalogues. The untouched source documents are in `sources/original-rulebooks.zip` to prevent duplicate search results.

## Rule identity and strengths

Original numbered IDs are preserved in `RULE_INDEX.tsv` with original namespace, original ID, required strength (`M`/`S`), canonical namespaced ID, active/alias status, and target. Active rules are rendered `CORE.WORK7`, `FE.A11Y2`, `BE.TXN3`, etc. Aliases remain traceable to exact archived source wording. No silent changes to levels. The performance specialist uses prose/section numbering rather than M/S-prefixed rule IDs; each full section was preserved in the reference library.

**Caveat:** A semantic alias is only a consolidation pointer; it is not a proof the two source rules were textually identical. If exact historical wording matters, consult the archived originals before deciding an exception or revising the standard. Source policies are not runtime evidence of conformance.

## Applicability choices

`CORE.PIPE`'s one-file/one-`run_<step>()` H1 convention is kept **optional and conditional** because imposing it on every frontend/backend repo would be incorrect. Similarly, FE.PWA, FE.SEO, BE.RPC, BE.DIST and Colab rules are triggered only when the actual technology/behavior exists.

The original rule requiring a PDF diff review for delivered code patches is preserved. It is *not* imposed on a new guidelines file or invented/undelivered patch. Use the final verified diff; if generation is unavailable use complete human-readable text hunks and disclose the limitation.

## Maintenance

1. Edit the canonical active rule or alias table deliberately; preserve rule IDs and strengths unless the change is documented.
2. Record authoritative references when changing time-sensitive standards or hardware-specific claims; do not treat literature as higher authority than adopted contracts.
3. Run `python tools/audit_policy.py` from the bundle root. It checks source rule coverage, active IDs, references, aliases, and file links.
4. The archived originals are historical source snapshots, not automatically synchronized future counterparts. Document any policy updates rather than claiming they update the original human companion.
