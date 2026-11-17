<!-- Source: BACKEND_GUIDELINES(1).md, section PRIV. Original rule numbers preserved, qualified with BE. -->

## PRIV

- **BE.PRIV1 M** Define personal-data purpose, legal/contractual basis, fields, precision, recipients, residency, access, retention, deletion, and incident handling with product/legal owners before broadening collection.
- **BE.PRIV2 M** Apply data minimization and scoped access throughout API, database, event streams, logs, traces, support tools, backups, and exports; one redacted endpoint is not sufficient.
- **BE.PRIV3 M** Redact/allowlist structured logs, metrics labels, trace attributes, exception messages, and error reports; do not capture passwords, access tokens, full private payloads, or unrestricted user-generated text by default.
- **BE.PRIV4 M** Honor approved consent, deletion, access/export, retention, and revocation workflows across primary/derived stores, queues, search, caches, and backups within documented capabilities and legal limits.
- **BE.PRIV5 S** Prefer aggregation, sampling, coarse identifiers, and shorter retention where diagnostic value is preserved; pseudonymization is not the same as anonymization.
- **BE.PRIV6 M** Define privacy-safe default behavior for new third-party SDKs, AI providers, analytics, crash/reporting vendors, and data processors before sending them user data.
- **BE.PRIV7 M** Restrict production data in development and testing; use synthetic or properly governed deidentified datasets, and verify data masking where relied upon.
- **BE.PRIV8 M** Keep audit/access logs for sensitive administrative and bulk-data operations as required, with controlled access and immutability properties appropriate to the threat model.
- **BE.PRIV9 S** Record data classification and retention at the table/field/event level when important; do not demand an enterprise catalog for a small service without material governance needs.
