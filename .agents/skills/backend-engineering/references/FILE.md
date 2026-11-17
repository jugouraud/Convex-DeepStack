<!-- Source: BACKEND_GUIDELINES(1).md, section FILE. Original rule numbers preserved, qualified with BE. -->

## FILE

- **BE.FILE1 M** Apply this section to uploads, downloads, archives, user-generated media, report exports, object storage, and streaming files; don't add file infrastructure when no such feature exists.
- **BE.FILE2 M** Validate file size/type/content/extension and decompression risks server-side according to purpose; client MIME hints or file names are untrusted.
- **BE.FILE3 M** Prevent path traversal, arbitrary overwrite, archive extraction escape, unsafe temporary files, symlink issues, and object-key authorization bypasses.
- **BE.FILE4 M** Store untrusted active content (HTML/SVG/executables) with isolation, safe content disposition/type, antivirus/sandboxing as risk warrants, and no privileged same-origin execution.
- **BE.FILE5 M** Stream or chunk large input/output and bound memory, disk, processing time, count, and concurrency; do not read unbounded uploads entirely into process memory.
- **BE.FILE6 M** Authorize object operations and signed URL generation on the verified principal, with appropriate expiry, scope, method, tenant, and revocation story.
- **BE.FILE7 M** Define transactional consistency between object storage and DB references: partial uploads, orphan cleanup, retries, versions, and deletion reconciliation.
- **BE.FILE8 S** Prefer platform-supported direct-to-object-store flows when they reduce server bottlenecks without bypassing authorization, integrity, and content controls.
- **BE.FILE9 M** Prevent formula/CSV injection and unsafe document rendering when exporting user-controlled values for spreadsheets or rich formats; escape according to the consumer.
- **BE.FILE10 M** Apply data classification, retention, encryption/access controls, and audit to exports and generated files; temporary files/signed links are still data disclosures.
