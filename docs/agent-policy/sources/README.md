# Source archive — historical policy snapshots

`original-rulebooks.zip` contains all four untouched supplied Markdown sources.
These are for traceability and policy revision, **not** everyday Codex context.
Keeping originals compressed prevents normal `rg` searches from finding duplicate
historical rule IDs before the canonical active rules.

```sh
unzip -l docs/agent-policy/sources/original-rulebooks.zip
unzip -p docs/agent-policy/sources/original-rulebooks.zip AGENTS_v1.6.md
```

The canonical lookup table is `docs/agent-policy/RULE_INDEX.tsv`.
