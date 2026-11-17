<!-- Source: FRONTEND_GUIDELINES(2).md, section PWA. Original rule numbers preserved, qualified with FE. -->

## PWA

- **FE.PWA1 M** Apply this section only when service workers, offline behavior, installation or push notifications are required; do not install PWA infrastructure by default.
- **FE.PWA2 M** Scope service worker routes, caches and lifecycle deliberately; never cache authenticated/private responses or credentials indiscriminately, and test logout/account switch invalidation.
- **FE.PWA3 M** Define update/activation behavior for active tabs and in-progress forms; prevent old service workers from serving broken asset/API combinations after deployment.
- **FE.PWA4 M** Distinguish offline read-only content, queued edits and confirmed server writes; show accurate status and resolve replay/conflicts/idempotency when reconnecting.
- **FE.PWA5 S** Make installation optional and unobtrusive; ensure ordinary browser navigation works without installation or service worker support.
- **FE.PWA6 M** Request push/notification permissions in clear user context, honor revocation and avoid sensitive information in notification content or unattended lock-screen previews.
- **FE.PWA7 M** Test cache corruption, storage quota, update failure and offline/online transitions for relied-upon offline functionality; do not claim offline support because a service worker merely registers.
