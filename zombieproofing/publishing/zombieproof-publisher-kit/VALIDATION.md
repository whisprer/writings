# Validation record — 20 October 2026

Kit version: 1.0.0. Demonstration form: `demo-details.json`.
The author and publisher used below are explicitly labelled proof identities.

## Complete builds

| Book | Chapters | Final proof pages | PDF / EPUB / HTML |
| --- | ---: | ---: | --- |
| Radio | 38 | 138 | All produced |
| Computers | 17 | 83 | All produced |
| Engines | 17 | 77 | All produced |
| Water | 17 | 63 | All produced |

Page counts will change with your own details and optional sections.

- All four PDFs have a 432 × 648 point trim box (6 × 9 inches).
- All contents numbers converged against actual PDF named destinations.
- Every chapter retained its supplied HTML manuscript and illustration exactly.
- Rendered page contact sheets and selected full-size pages were reviewed.
- Automated inspection found no text bounding boxes outside the trim on any
  page of the four PDFs and no Unicode replacement characters in extracted text.
- MuPDF opened and inspected all four PDFs without repair warnings.
- All four EPUBs passed **EPUBCheck 5.3.0**, using EPUB 3.3 rules, with
  **zero errors and zero warnings**.
- The ten regression tests passed. They cover chapter/plate preservation,
  plain-text escaping, optional-section removal and replacement, book overrides,
  ISBN checksums, configuration typos and duplicate keys, missing imprint images,
  EPUB asset references and format-specific ISBNs, and protection of existing
  output folders.
- The unfilled production form fails early with `fill in author`, as intended.
- All pinned dependencies were successfully resolved and downloaded as wheels
  for **Windows x64 / CPython 3.14**, including the native greenlet dependency.

## Tested environment and limits

Executed on Linux with Python 3.12, Playwright 1.56.0 / Chromium 141.0.7390.37,
Beautiful Soup 4.14.3 and pypdf 6.10.0. Fonts and book art are bundled locally.

The PowerShell launchers have not been executed on a Windows machine here.
Windows dependency-wheel availability was checked; that is not an end-to-end
Windows run. Setup downloads packages and Chromium, unless an installed browser
is explicitly selected. Building a book uses local assets only.

The final PDFs are complete reading editions. Printer-specific interior/cover
separation, bleed, spine geometry, CMYK/PDF-X and physical glossy finishes remain
dependent on the chosen print provider. See README.md.

The manuscripts were preserved, not newly fact-checked. Final author-entered
matter should be proofread after each build, especially unusually long credits.
