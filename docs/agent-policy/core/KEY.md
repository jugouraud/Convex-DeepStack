<!-- Source: AGENTS_v1.6(1).md / KEY; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## KEY

- CORE.KEY1 M No secrets in source/client/URLs/logs/tests/manifests/prompts; approved injection, least privilege, prefer scoped short-lived credentials. Revoke/rotate exposed credentials; deletion does not invalidate historical exposure.
- CORE.KEY2 M Use maintained crypto/protocols and CSPRNG; verify TLS peers; choose threat-appropriate encryption, authenticated modes/nonce discipline, separate key access and lifecycle.
- CORE.KEY3 M Use maintained adaptive salted password hashing (e.g. suitable Argon2id), reviewed work factors; no fast general hashes or reversible password verification storage.
- CORE.KEY4 M Own dependency inventory, vulnerability reporting/impact triage/patch/release; pinning is not patching. Protect build secrets from untrusted contributions; fix causes/equivalent paths and remediate incidents.
