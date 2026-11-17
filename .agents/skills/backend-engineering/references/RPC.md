<!-- Source: BACKEND_GUIDELINES(1).md, section RPC. Original rule numbers preserved, qualified with BE. -->

## RPC

- **BE.RPC1 M** Apply this section only for gRPC, GraphQL, internal RPC, binary protocols, or equivalent nontrivial service contracts; do not introduce RPC infrastructure for an ordinary local call.
- **BE.RPC2 M** Define explicit service interface, identity/authorization, deadline, error taxonomy, retry safety, schema evolution, and payload/resource limits.
- **BE.RPC3 M** Propagate request IDs, trace context, cancellation/deadlines, and caller identity through trusted channels; never implicitly forward privileged tokens to arbitrary downstream services.
- **BE.RPC4 M** Preserve wire compatibility during schema changes (field numbering/reservation/default semantics/unknown fields as applicable); verify representative older clients and servers.
- **BE.RPC5 S** Prefer coarse-grained calls where cross-process latency dominates; avoid chatty networks disguised as ordinary in-process method calls.
- **BE.RPC6 M** For GraphQL, enforce per-field/object authorization and bounded query depth/cost, pagination, batching, and introspection policy appropriate to threat model.
- **BE.RPC7 M** For streaming RPC, bound producer/consumer buffers, apply backpressure/cancellation, define reconnect/resume, and avoid claiming exactly-once semantics without end-to-end proof.
- **BE.RPC8 S** Prefer established IDL/code-generation libraries over homegrown serialization or runtime discovery; avoid generated artifacts changing incidentally in a narrow patch.
