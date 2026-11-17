<!-- Source: AGENTS_v1.6(1).md / CODE; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## CODE

- CORE.CODE1 S Use consistent domain vocabulary and intent-revealing names; verbs for operations, predicates for conditions; match name detail to scope.
- CORE.CODE2 S Keep functions/modules cohesive and abstraction levels coherent; make side effects explicit; separate queries from mutations.
- CORE.CODE3 S Use few meaningful parameters; group cohesive data only; prefer explicit modes over ambiguous behavioral booleans.
- CORE.CODE4 S Prefer clear flow and useful guards; reduce nesting/flags; localize repeated dispatch without forcing polymorphism.
- CORE.CODE5 S Use behavioral objects for invariants, records for data; avoid mixed ownership and long internal access chains. Deduplicate knowledge, not coincidental text.
- CORE.CODE6 S Annotate public parameters/returns and important data; use configured static checking. Annotations are not runtime checks. Boundary validation: INPUT; mutable invariants: DATA/AUTH.
- CORE.CODE7 S Follow project/language conventions; name meaningful constants; comment rationale, constraints, or surprises rather than obvious execution.
