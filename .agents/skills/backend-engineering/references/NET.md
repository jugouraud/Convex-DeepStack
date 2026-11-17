<!-- Source: BACKEND_GUIDELINES(1).md, section NET. Original rule numbers preserved, qualified with BE. -->

## NET

- **BE.NET1 M** Use TLS for sensitive/authenticated traffic and current approved protocols; validate certificates/hostnames; do not disable verification to fix a connectivity issue.
- **BE.NET2 M** Establish explicit connection, TLS handshake, request, read/idle, and overall deadlines where relevant; distinguish a timeout from a definitive business rejection.
- **BE.NET3 M** Bound connection pools, keepalive, idle lifetimes, header/body sizes, and concurrent outbound calls; release responses/connections properly to prevent exhaustion.
- **BE.NET4 M** Treat DNS, service discovery, proxies, ingress headers, redirect chains, and IP changes as potentially untrusted; define the allowed trust chain before accepting forwarded identity/client IP.
- **BE.NET5 S** Use existing HTTP clients with appropriate pooling and reuse; avoid per-request client creation, duplicated TLS stacks, and custom protocol parsers without a specific need.
- **BE.NET6 M** Validate and constrain destinations for outbound requests and redirects; defend against SSRF, metadata/loopback/private-network access, DNS rebinding, and unexpected protocol schemes as applicable.
- **BE.NET7 S** Understand load balancer/CDN/mesh behavior before assuming a request reaches one instance, retains session affinity, or preserves headers, status, and timing unaltered.
- **BE.NET8 M** Do not assume reliable networks, fixed latency, in-order delivery across connections, exact packet timing, or that a failed connection means the remote side did nothing.
- **BE.NET9 S** Test local/dev/prod proxy differences and protocol negotiation when affecting connection reuse, upgrade, compression, streaming, or request signing.
