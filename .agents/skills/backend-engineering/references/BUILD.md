<!-- Source: BACKEND_GUIDELINES(1).md, section BUILD. Original rule numbers preserved, qualified with BE. -->

## BUILD

- **BE.BUILD1 M** Reuse established language/runtime versions, dependency manager, lockfiles, build scripts, CI conventions, and source layout unless the task explicitly requires change.
- **BE.BUILD2 M** Require deterministic or reproducible-enough builds from pinned/controlled inputs, documenting unavoidable external inputs and verifying release artifacts rather than trusting developer machines.
- **BE.BUILD3 M** Review new direct/transitive dependencies for security, maintenance, license, runtime compatibility, privileges, and actual necessity; default to no dependency for a local behavior fix.
- **BE.BUILD4 M** Treat package lifecycle scripts, compilers, code generators, container build tools, and CI workflows as trusted execution requiring privilege and secret controls.
- **BE.BUILD5 S** Prefer supported language/runtime/library releases and vendor-maintained packages; introduce custom forks or vendored code only when a clear lifecycle/patch plan exists.
- **BE.BUILD6 M** Run relevant static checks, tests, compilation, schema/contract generation checks, and artifact inspection in CI without silently swallowing failures.
- **BE.BUILD7 M** Keep secrets and privileged credentials out of source, container layers, debug symbols, compiled assets, dependency metadata, and externally accessible build logs.
- **BE.BUILD8 S** Generate SBOM/provenance/attestations and adopt SLSA controls at risk-appropriate levels where governance or threat model warrants; do not claim certification from a checkbox.
- **BE.BUILD9 M** Verify dependency updates and build changes against actual deployed runtime/architecture and data formats; lockfile churn and unrelated platform upgrades are separate changes by default.
- **BE.BUILD10 S** Keep CI fast and proportional using existing caches, parallelism, and scoped checks without masking critical end-to-end security/data-integrity evidence.
- **BE.BUILD11 M** Harden untrusted contribution builds: PR workflows must not expose deploy keys, production secrets, or privileged publishing tokens to attacker-controlled code.
