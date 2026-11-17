<!-- Source: FRONTEND_GUIDELINES(2).md, section DS. Original rule numbers preserved, qualified with FE. -->

## DS

- **FE.DS1 S** Prefer existing design-system components/tokens/patterns to bespoke controls; evaluate deviations against consistency, accessibility and actual product need.
- **FE.DS2 M** Keep reusable component contracts explicit: states, variants, disabled/loading behavior, keyboard behavior, composition rules, tokens and ownership of ARIA/IDs.
- **FE.DS3 S** Distinguish semantic design tokens (role/intent) from raw scales (color/space/type); avoid duplicating equivalent tokens or tying every token to a specific page.
- **FE.DS4 M** Treat a shared component change as a multi-consumer change: verify representative affected variants, themes, densities, directions and focus states.
- **FE.DS5 S** Maintain a small documented public API for shared components; deprecate incompatible props/variants with a migration path rather than silently breaking consumers.
- **FE.DS6 S** Maintain visual rhythm and affordance consistency without enforcing decorative uniformity across materially different use cases.
- **FE.DS7 M** Avoid making inaccessible visual patterns authoritative simply because they appear in a mockup; escalate conflicting requirements and implement an accessible equivalent.
