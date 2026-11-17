<!-- Source: BACKEND_GUIDELINES(1).md, section CRYPTO. Original rule numbers preserved, qualified with BE. -->

## CRYPTO

- **BE.CRYPTO1 M** Use vetted maintained libraries and current organization-approved algorithms/modes/protocols; never invent encryption schemes, signature formats, random-number generators, or bespoke password hashing.
- **BE.CRYPTO2 M** Hash passwords with a dedicated modern adaptive password-hashing scheme and unique salts, using current vetted parameters and migration policy; never store recoverable plaintext passwords.
- **BE.CRYPTO3 M** Use cryptographically secure randomness for session IDs, tokens, challenges, nonces, and keys; predictable UUID/timestamps are not substitutes for secret entropy.
- **BE.CRYPTO4 M** Manage keys with explicit ownership, access, environment separation, rotation, revocation, backup/recovery, audit, and disposal; avoid hardcoded secrets and shared long-lived credentials.
- **BE.CRYPTO5 M** Use authenticated encryption and correct nonce/IV handling where encrypting application data; protect integrity, associated context, and key separation, not just confidentiality.
- **BE.CRYPTO6 M** Authenticate and validate signatures using approved trust roots, algorithms, intended key use, issuer/audience/context, and expiration where applicable; avoid algorithm confusion.
- **BE.CRYPTO7 S** Use managed KMS/HSM/secrets facilities when they reduce threat exposure and operations burden; document dependence and recovery before mandating infrastructure.
- **BE.CRYPTO8 M** Classify data-in-transit/at-rest requirements and select appropriate TLS, storage encryption, envelope encryption, and access controls; encryption is not a replacement for authorization.
- **BE.CRYPTO9 M** Handle key compromise, lost keys, partially rotated encrypted records, and provider outages in a documented recovery path; never promise seamless rotation without testing it.
