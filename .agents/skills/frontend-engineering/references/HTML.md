<!-- Source: FRONTEND_GUIDELINES(2).md, section HTML. Original rule numbers preserved, qualified with FE. -->

## HTML

- **FE.HTML1 M** Use semantic document landmarks and correct native elements: links for navigation, buttons for actions, real headings, lists, tables, labels and form controls where applicable.
- **FE.HTML2 M** Preserve valid DOM structure, unique IDs where required, legal element nesting, accessible names, and links with meaningful destinations; do not build interactions from clickable `div`/`span` without necessity.
- **FE.HTML3 M** Provide accurate document language, character encoding, viewport configuration and descriptive titles; maintain sensible page heading hierarchy and page-region landmarks.
- **FE.HTML4 S** Prefer native forms, browser validation primitives and semantic inputs; use custom controls only where platform controls cannot meet documented interaction requirements.
- **FE.HTML5 M** Use the correct distinction between `<button>` action and `<a href>` navigation. Ensure form buttons have deliberate `type` and links do not abuse dummy `href` values.
- **FE.HTML6 M** Give meaningful media accessible alternatives; use empty `alt` for purely decorative images, appropriate captions/transcripts where required and explanatory text for information-bearing visuals.
- **FE.HTML7 S** Keep DOM reading and focus order meaningful independently of decorative visual positioning; avoid order-changing CSS or DOM duplication that creates confusing assistive output.
- **FE.HTML8 S** Use built-in `loading`, `decoding`, resource hints and image dimension hints deliberately; avoid loading hints that compete with critical content.
- **FE.HTML9 M** Serialize untrusted server data into HTML/scripts with context-appropriate escaping; JSON serialization alone is not a universal HTML or script-context escape.
- **FE.HTML10 S** Keep metadata and structured content accurate, stable and tied to the actual page; avoid duplicate conflicting titles, descriptions or canonical URLs.
