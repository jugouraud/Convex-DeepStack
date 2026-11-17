<!-- Source: FRONTEND_GUIDELINES(2).md, section STATE. Original rule numbers preserved, qualified with FE. -->

## STATE

- **FE.STATE1 M** Define the owner and lifecycle of each state category: local UI, URL, server-authoritative, shared client, persisted client and derived state. Avoid multiple unsynchronized sources of truth.
- **FE.STATE2 S** Keep ephemeral state local; promote to context/store only for demonstrated cross-component sharing or lifecycle needs; avoid an app-wide store by default.
- **FE.STATE3 M** Reflect shareable/navigation-relevant state in deliberate URL/query/hash contracts; preserve back/forward and deep links instead of hiding every screen transition in memory.
- **FE.STATE4 S** Derive computed values during render or selectors; use memoization only for measured or evident expensive calculations, not as a correctness mechanism.
- **FE.STATE5 M** Model requests and mutations with explicit pending/success/error/cancelled or stale states where they affect behavior. Prevent stale responses and obsolete mutations from corrupting visible state.
- **FE.STATE6 M** On optimistic updates, define rollback/reconciliation, conflict and duplicate-click behavior; never present a temporary optimistic value as durable success after server rejection.
- **FE.STATE7 M** Treat server data as authoritative for authorization, balances, inventory, ownership and other protected invariants; a client cache or hidden UI cannot grant privileges.
- **FE.STATE8 S** Use one coherent remote-data fetching/cache approach where justified; avoid mixing ad hoc fetch effects, global stores and multiple query libraries without clear ownership.
- **FE.STATE9 M** Scope cached and persisted data by authenticated identity/tenant, data version and relevant permissions; clear or isolate on sign-out/account switch and honor revocation.
- **FE.STATE10 S** Prefer intentional invalidation over complex manual cache mutation; choose stale-time, polling and background refetch according to actual freshness requirements.
- **FE.STATE11 M** Handle repeated actions, navigation during inflight work, request races, refresh, multiple tabs and slow responses for consequential flows.
- **FE.STATE12 S** Avoid effects solely to copy props into state or update another derived value; keep synchronization only for genuinely external systems.
