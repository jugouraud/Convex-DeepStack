<!-- Source: FRONTEND_GUIDELINES(2).md, section TYPE. Original rule numbers preserved, qualified with FE. -->

## TYPE

- **FE.TYPE1 S** Prefer TypeScript where the project uses it; keep static types accurate, maintainable and useful at module boundaries rather than maximizing type-level cleverness.
- **FE.TYPE2 M** Do not bypass unknown data with unchecked `any`, double assertions or fabricated type predicates; validate external payloads at their receiving trust boundary when consequential.
- **FE.TYPE3 S** Model distinct UI states with discriminated unions or equivalent explicit representation when illegal combinations would otherwise be possible.
- **FE.TYPE4 M** Preserve nullability and absence semantics: `undefined`, `null`, missing, empty, loading and error may represent different contracts. Avoid truthiness checks for meaningful `0`, `false` or empty strings.
- **FE.TYPE5 S** Type public component props, event handlers, hook return values and service APIs sufficiently to expose contracts; infer obvious local types.
- **FE.TYPE6 M** Distinguish compile-time types from runtime guarantees; never rely on a TypeScript interface as API validation or authorization.
- **FE.TYPE7 S** Use schema generation or shared contracts only when it avoids real drift; do not introduce a second source of truth by duplicating incompatible DTO definitions.
- **FE.TYPE8 M** Respect browser/native data boundaries such as `File`, `FormData`, `URL`, `Date`, numeric parsing and serialized `BigInt`/`undefined`; test actual conversion behavior.
