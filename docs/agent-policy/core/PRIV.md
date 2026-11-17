<!-- Source: AGENTS_v1.6(1).md / PRIV; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## PRIV

- CORE.PRIV1 M Before personal-data flows define purpose/minimum fields+precision, recipients/access, defaults/choices, copies/derivatives, retention/deletion, owner, verification; communicate collection/recipients/controls at use.
- CORE.PRIV2 M Default optional tracking/sharing/public exposure to privacy-protective settings; enforce choices server-side and downstream; assess processors/SDK telemetry and new purposes.
- CORE.PRIV3 S Prefer noncollection, coarse data, local processing, separated identity, or aggregation when sufficient; anonymity claims are constrained by PRIV7.
- CORE.PRIV4 M Implement owned expiry/deletion/correction across applicable originals, derivatives, processors; track partial failures; prevent delayed jobs/replay from recreating deleted data.
- CORE.PRIV5 M Define backup exceptions/expiry/access; reapply deletion before restored availability. Authorize private exports/deletion, limit export lifetime, explicitly select response fields.
- CORE.PRIV6 M Do not retain raw personal data indefinitely for debugging/reproducibility; prefer synthetic/minimal evidence. Match privacy promises to actual behavior; specialist PETs only when justified.
- CORE.PRIV7 M Do not claim anonymity from encryption, hashed IDs, name removal, or aggregation alone; assess linkage, auxiliary information, and small-group disclosure.
