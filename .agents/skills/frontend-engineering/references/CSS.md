<!-- Source: FRONTEND_GUIDELINES(2).md, section CSS. Original rule numbers preserved, qualified with FE. -->

## CSS

- **FE.CSS1 S** Prefer modern intrinsic/flexible layout (Grid, Flexbox, logical properties, `minmax`, `clamp`, container queries as supported) over arbitrary pixel-perfect positions.
- **FE.CSS2 M** Preserve usable reflow and avoid unintended horizontal overflow at supported viewports/zoom levels; allow content and localization to grow without clipping essential information.
- **FE.CSS3 S** Keep specificity and selector reach controlled; use existing component scope, tokens, layers and naming conventions; avoid new global overrides or `!important` escalation without a specific reason.
- **FE.CSS4 S** Prefer a small coherent spacing/type/color scale and shared tokens where real consistency exists; avoid one-off token proliferation or extracting every literal into a variable.
- **FE.CSS5 M** Keep focus indicators perceivable, contrast and information semantics intact; do not remove outlines without an equal or better visible replacement.
- **FE.CSS6 M** Respect user motion and contrast preferences where applicable; use `prefers-reduced-motion` for nonessential animation and avoid motion essential to understanding or safety.
- **FE.CSS7 S** Animate compositor-friendly properties when possible; avoid triggering repeated layout/paint for cosmetic effects and measure complex animation on representative devices.
- **FE.CSS8 M** Avoid hiding important content from keyboard/screen-reader users through CSS-only tricks; use correct semantic hidden/inert/expanded states and focus handling.
- **FE.CSS9 S** Use logical properties/directional-safe assets to support writing directions; avoid left/right assumptions when the product localizes.
- **FE.CSS10 M** Define predictable stacking contexts, overlays and scroll containers; guard against obscured focus, trapped scrolling and popovers clipped by ancestors.
- **FE.CSS11 S** Treat responsive behavior as content-driven; choose breakpoints based on layout failure rather than device labels or arbitrary proliferation.
- **FE.CSS12 S** Prefer CSS solutions for styling/layout before runtime measurements, resize handlers or DOM writes; add observers only when CSS cannot express the required behavior.
