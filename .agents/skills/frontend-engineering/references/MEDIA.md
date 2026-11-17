<!-- Source: FRONTEND_GUIDELINES(2).md, section MEDIA. Original rule numbers preserved, qualified with FE. -->

## MEDIA

- **FE.MEDIA1 M** Provide correct intrinsic image/video dimensions or stable aspect ratios to prevent avoidable layout shift; keep responsive media within the available layout.
- **FE.MEDIA2 S** Deliver appropriate image formats, compression, responsive sources and sizes; optimize the bytes the browser actually downloads, not just source file dimensions.
- **FE.MEDIA3 S** Lazy-load below-the-fold media when beneficial; do **not** lazy-load the actual likely LCP image by default. Use preload/fetch priority only for identified critical resources.
- **FE.MEDIA4 M** Supply meaningful alt text/captions or decorative semantics as appropriate; complex charts require a usable nonvisual description or data alternative when meaningful.
- **FE.MEDIA5 S** Limit font files, glyph ranges, weight variants and blocking behavior; use deliberate fallbacks and check layout stability, language coverage and readability.
- **FE.MEDIA6 M** Prevent autoplay or motion/audio behavior that conflicts with accessible/user-controlled playback requirements; supply controls and captions/transcripts where applicable.
- **FE.MEDIA7 S** Use consistent SVG/icon semantics and sizes; decorative icons should not become redundant screen-reader output, while icon-only controls need accessible names.
- **FE.MEDIA8 M** Treat externally sourced SVG, HTML media embeds, fonts and dynamic images as security/privacy/performance dependencies; sanitize or isolate active content where needed.
