# frontend-engineering: code addendum

> Read with `docs/agent-policy/core/CODE.md`; common rules live in CORE.CODE. Original IDs not listed here are aliases, not removed from archival sources.

- **FE.CODE3 S** Prefer small typed interfaces with a few meaningful props/arguments. Avoid boolean-prop explosions; use explicit variants for genuinely different behavior.
- **FE.CODE6 M** Use the repository's formatter, linter, typechecker and module conventions. Do not disable diagnostics globally or insert broad suppression without a narrow documented reason.
- **FE.CODE8 M** Preserve public semantics: routes, DOM contracts consumed by tests/integrations, API payloads, analytics event meaning and supported component props unless explicitly changed.
- **FE.CODE9 S** Prefer predictable immutable updates and explicit failure paths over shared mutable state, deep object mutation and broad exception handling.
