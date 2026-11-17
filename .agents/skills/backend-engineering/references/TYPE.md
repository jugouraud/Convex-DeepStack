<!-- Source: BACKEND_GUIDELINES(1).md, section TYPE. Original rule numbers preserved, qualified with BE. -->

## TYPE

- **BE.TYPE1 M** Treat all external input and persisted/serialized payloads as data requiring validation proportionate to the trust boundary; compile-time types do not enforce runtime contracts.
- **BE.TYPE2 S** Use the project's established static types/typed interfaces; model meaningful alternatives and errors explicitly without opaque generic type machinery for simple cases.
- **BE.TYPE3 M** Preserve absent vs null vs empty vs zero vs false vs default semantics across APIs, database reads, updates, and patch operations.
- **BE.TYPE4 M** Specify serialization behavior for dates, time zones, decimals, large integers, binary data, Unicode, enumerations, and unknown fields; test cross-language/consumer behavior where relevant.
- **BE.TYPE5 M** Do not bypass validation using unchecked casts, `any`-equivalents, fabricated type guards, or unverified deserialization in security/financial/data-integrity paths.
- **BE.TYPE6 S** Prefer one source of truth for schemas and generated types where it actually prevents drift; avoid duplicated or circular codegen pipelines for a single local endpoint.
- **BE.TYPE7 M** Keep internal domain types distinct from public DTOs when privacy, compatibility, or invariant risk requires it; never serialize internal secrets or privileged fields by default.
- **BE.TYPE8 S** Model finite states as explicit tagged alternatives where illegal combinations or partial updates would otherwise be easy to produce.
- **BE.TYPE9 M** Use exhaustive or explicit handling for newly introduced protocol/event enum variants at safety-critical boundaries; choose deliberate unknown-value compatibility behavior.
