# Production checks

Final build: 20 October 2026. Edition 1.0.0.

- PDF: 99 pages at 6 × 9 inches; 17 chapters and six parts.
- Main chapter text: 14,795 words, including quick-reference cards and record-sheet instructions; frontmatter, afterword and bibliography are additional.
- Artwork: 19 selected illustrations (cover, frontispiece, 17 chapter plates). The chapter 1 satchel emblem was removed; only the corrected plate is distributed.
- References: 51 entries, identified by stable R-numbers. Some identifiers are intentionally non-contiguous.
- Fonts: used Fraunces and Literata faces are embedded/subset in the PDF. WOFF fonts and OFL notices are embedded in the EPUB; TTF and WOFF sources accompany the project.
- PDF checks: all chapters present; no unfinished-product tokens; cover artwork present; all measured text inside page safety bounds; no detected text/image overlap. Bookmarks, linked contents and subject-finder destinations were checked structurally.
- Visual checks: all initial pagination pages were inspected as rendered contact sheets. The revised cover, chapter page, full-page emergency card, handover sheet, observation sheet, supply log, afterword and reference/index pages were inspected at larger scale. Revisions removed split emergency cards, split record-sheet starts, a blank-cover rendering fault and an isolated source-only page. No unresolved clipping or layout faults were observed.
- EPUB checks: first uncompressed mimetype entry, well-formed XML/XHTML/OPF, required local assets and local links validated. A full external EPUBCheck certification and physical-reader test were not performed.
- HTML checks: local image references and internal anchors resolve. A headless-browser visual check was not performed because the browser executable was unavailable; the typeset PDF is the visually verified edition.
- Build: executed successfully with the pinned Python dependencies in requirements.txt on Linux CPython 3.12. Windows commands are documented but were not executed on a Windows host.
- Print limits: no printer-specific back cover, spine wrap, bleed specification or PDF/X certification is claimed. Main cover art is 1024 × 1536 pixels (about 171 ppi over the full 6 × 9 inch trim); most landscape chapter art is 1536 × 1024 pixels (about 328 ppi at the placed width). The EPUB's typeset cover raster adds sharper title lettering but does not invent detail in the source painting.

## Medical review status

This is a complete editorial production, not a clinical certification. Selected official guidance was checked and differences from older material were resolved as described in SOURCE_REVIEW.md. No independent clinician or pharmacist has reviewed the manuscript. That review remains required before public release as dependable medical instruction. Production tests cannot establish clinical safety or treatment accuracy.
