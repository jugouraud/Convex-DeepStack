# backend-engineering: code addendum

> Read with `docs/agent-policy/core/CODE.md`; common rules live in CORE.CODE. Original IDs not listed here are aliases, not removed from archival sources.

- **BE.CODE5 M** Follow repository formatter, linter, typechecker, error model, dependency direction, and runtime conventions. Do not broadly suppress diagnostics or change global rules to accommodate a local patch.
- **BE.CODE6 M** Keep error ownership clear: distinguish expected domain rejection, transient dependency failure, cancellation, programmer defects, and unknown outcomes; do not swallow or silently reinterpret errors.
- **BE.CODE8 M** Preserve externally observable semantics, including response codes, ordering, side effects, audit events, schema and serialization formats, unless the change requires coordinated migration.
- **BE.CODE10 M** Make resource ownership and cleanup reviewable: open/close, acquire/release, start/stop, commit/rollback, subscribe/unsubscribe, and cancellation must pair on every path.
- **BE.CODE11 S** Prefer immutable value handling and small mutation scopes where practical; do not use shared mutable state when a request-scoped or pure representation suffices.
- **BE.CODE12 M** Do not implement important monetary, decimal, or identity logic using lossy conversions, ambiguous string normalization, or implicit coercion that violates the domain contract.
