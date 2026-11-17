<!-- Source: FRONTEND_GUIDELINES(2).md, section COMP. Original rule numbers preserved, qualified with FE. -->

## COMP

- **FE.COMP1 S** Define components by cohesive responsibilities and stable user-visible purpose, not arbitrary line-count thresholds or every visual wrapper.
- **FE.COMP2 S** Compose smaller purposeful parts; avoid giant configurable “universal” components, unnecessary inheritance and complex prop-bag forwarding.
- **FE.COMP3 M** Maintain clear ownership of state, focus, effects, subscriptions, keys, refs and DOM IDs. Do not allow two owners to silently compete over the same state or element.
- **FE.COMP4 S** Keep local transient state local; lift it only when another consumer genuinely needs to coordinate it. Derive values from inputs instead of storing redundant synchronized copies.
- **FE.COMP5 M** Preserve state identity deliberately across lists, reorders, route changes and transitions. Use stable domain keys, not array positions when order/identity can change.
- **FE.COMP6 M** Treat effects/lifecycle callbacks as integration points with external systems, not general-purpose derivation or event dispatch; account for repeated mounting, concurrent rendering and cleanup as applicable.
- **FE.COMP7 S** Avoid creating a shared hook/context/provider for a single-use operation or speculative extensibility. Put reusable behavior where there are proven independent consumers or a meaningful boundary.
- **FE.COMP8 M** Make custom interactive components honor correct semantics, focus and keyboard behavior; reuse mature accessible primitives when they reduce risk.
- **FE.COMP9 S** Keep presentation and business behavior distinct where it improves reuse, but do not impose mandatory “container/presenter” layers on simple components.
- **FE.COMP10 M** Expose controlled/uncontrolled props coherently; do not switch modes unexpectedly or let internal and external values diverge without an explicit contract.
- **FE.COMP11 S** Keep rendering logic readable; extract substantial branches where they represent meaningful states, not merely to eliminate all inline expressions.
- **FE.COMP12 M** On async/SSR boundaries, prevent hydration from generating inconsistent structure/IDs/text from nondeterministic time, randomness, locale, screen size or browser-only data.
