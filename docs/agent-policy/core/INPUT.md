<!-- Source: AGENTS_v1.6(1).md / INPUT; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## INPUT

- CORE.INPUT1 M Validate receiving trust-boundary data; trust established internal types. Reassess after new boundaries, meaning-changing transforms, or mutable security-state changes.
- CORE.INPUT2 M Specify media/encoding/version, shape/required/null/unknown fields, coercion, ranges/units/cross-field rules, duplicates, cost limits, rejection, and writable fields.
- CORE.INPUT3 M Bound bytes during receipt before buffering/parsing; bound decompression and parser work/depth/items separately; Content-Length or post-parse schemas alone are insufficient.
- CORE.INPUT4 M Use maintained restricted parsers; no eval/exec, untrusted pickle/executable artifacts, unsafe YAML constructors, external entities, or unnecessary active format features.
- CORE.INPUT5 M Define duplicate/repeated-parameter semantics; reject security-relevant ambiguity; decode expected encodings before checks, prevent later reinterpretation, align all parsers/proxies.
- CORE.INPUT6 M Enforce finite numeric domain/precision/overflow rules and strict coercion policy; use bounded whole-value checks and safe regex work limits.
- CORE.INPUT7 S Preserve legitimate Unicode/punctuation; normalize only by field policy before comparison/uniqueness; reject malformed encoding/invalid controls. No universal sanitizer or client-only enforcement.
