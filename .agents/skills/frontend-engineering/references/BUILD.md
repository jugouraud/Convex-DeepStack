<!-- Source: FRONTEND_GUIDELINES(2).md, section BUILD. Original rule numbers preserved, qualified with FE. -->

## BUILD

- **FE.BUILD1 M** Reuse the established package manager, lockfile, build pipeline and dependency versions unless the task requires change. Do not rewrite dependency metadata incidentally.
- **FE.BUILD2 M** Distinguish build-time, server-runtime and browser-public variables; only explicitly public nonsecret values may enter browser bundles and HTML.
- **FE.BUILD3 M** Require reproducible CI install/build behavior from locked inputs; verify generated outputs and production bundling rather than relying solely on dev-server success.
- **FE.BUILD4 S** Favor platform/framework defaults and few purposeful plugins; avoid changing bundlers, transpilers, lint configs or test runners to solve a local bug.
- **FE.BUILD5 M** Review new dependencies for maintenance, licensing, transitive risk, size, runtime needs and actual necessity; prefer standard APIs for simple tasks.
- **FE.BUILD6 M** Preserve source-map and artifact access rules: public browser source maps and debug symbols can reveal source or sensitive strings; protect or intentionally publish according to policy.
- **FE.BUILD7 S** Keep bundles tree-shakeable where practical; use targeted imports and split heavy optional modules when it measurably benefits the critical path.
- **FE.BUILD8 M** Ensure the deployed output has no accidental debug flags, test credentials, secrets, private endpoints or internal-only source artifacts.
- **FE.BUILD9 S** Use stable code formatting and existing lint/type rules as routine fast gates; add custom rules only for repeated high-value failures and justify maintenance cost.
- **FE.BUILD10 M** Build hooks/scripts and dependency lifecycle execution must not expose privileged CI secrets to untrusted contributions or packages; follow the organization's supply-chain controls.
