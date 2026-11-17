<!-- Source: BACKEND_GUIDELINES(1).md, section SEC. Original rule numbers preserved, qualified with BE. -->

## SEC

- **BE.SEC1 M** Establish a concise threat model for high-impact entrypoints: assets, actors, trust boundaries, abuse cases, attacker-controlled inputs, and required security controls.
- **BE.SEC2 M** Validate and constrain untrusted data at receiving boundaries; use parameterization and context-safe APIs for SQL/NoSQL queries, templates, shell, paths, URLs, LDAP, and other interpreters.
- **BE.SEC3 M** Enforce authorization independently of client-side affordances and upstream assertions; check object/tenant/field policies for every privileged backend action.
- **BE.SEC4 M** Reject unsafe deserialization and arbitrary type/function loading from untrusted bytes; avoid executable object graphs, gadget chains, `eval`, or unchecked dynamic code construction.
- **BE.SEC5 M** Prevent SSRF through allowlisted destinations or equivalent strong destination policy, redirect checks, DNS/IP handling, protocol limits, and protection of cloud metadata/internal networks where relevant.
- **BE.SEC6 M** Protect file paths and object keys from traversal, symlink race, archive extraction traversal, unsafe temp files, and confused-deputy access; use safe filesystem APIs and isolation.
- **BE.SEC7 M** Enforce request size, parsing depth, decompression ratio, regex/algorithmic complexity, allocation, and per-actor resource limits against denial of service.
- **BE.SEC8 M** Use structured output escaping, templating, and content security measures as appropriate; backend-rendered HTML, emails, Markdown, logs, and downstream commands have distinct injection contexts.
- **BE.SEC9 M** Classify and restrict privileged endpoints, internal dashboards, admin jobs, debug modes, profiling, stack traces, health details, and management ports; 'internal' is not sufficient authentication.
- **BE.SEC10 M** Verify third-party callbacks/webhooks with the provider's supported signing/authentication procedure and replay window; do not trust an unverified source IP or payload field alone.
- **BE.SEC11 M** Keep secrets, credentials, private keys, signing tokens, and sensitive configuration out of code/artifacts/test logs; rotate/revoke exposed credentials through approved procedures.
- **BE.SEC12 M** Apply security updates and dependency advisories proportionately, review the reachable impact, and preserve reproducible inputs; do not blindly disable vulnerability gates or upgrade everything in an unrelated patch.
- **BE.SEC13 S** Prefer established security primitives/framework middleware when they actually enforce the required threat boundary; avoid custom cryptographic authentication and 'security by obscure URL'.
- **BE.SEC14 M** Use least privilege for database, broker, object-storage, and cloud identities, separating read/write/migration/backup/admin capabilities where risk warrants.
- **BE.SEC15 M** Log security-relevant events with integrity, privacy, and retention controls; do not make audit evidence forgeable by untrusted fields or expose it to ordinary callers.
- **BE.SEC16 M** Protect multi-step authorization against time-of-check/time-of-use gaps and stale decisions for consequential effects; revalidate at authoritative commit/side-effect boundaries as needed.
- **BE.SEC17 S** Use OWASP ASVS verification requirements and relevant cheat sheets as a security checklist; select appropriate assurance level rather than claiming universal compliance from a library.
- **BE.SEC18 M** Review dependency/plugin/build-time code as part of the trust surface, including install scripts, code generators, CI steps, and transitive packages.
