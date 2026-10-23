# Zombieproof Medical

**How to Keep the Living Living** — Volume IV of the supplied Zombieproof series.

Complete illustrated editorial edition, 1.0.0, 20 October 2026. Published for whispr.dev. The manuscript is AI-assisted and has **not received independent clinical review**. Read SOURCE_REVIEW.md before public release or marketing as medical instruction.

## Read the book

- `build/Zombieproof-Medical.pdf`: typeset 6 × 9 inch reading/print PDF, with cover, frontispiece, running heads, clickable contents, bookmarks, references and subject finder.
- `build/Zombieproof-Medical.epub`: reflowable EPUB 3, with embedded fonts, navigable chapters, image descriptions and local assets.
- `build/Zombieproof-Medical.md`: complete editable manuscript plus bibliography.
- `print.html`: offline HTML edition. Open directly in a modern browser; keep it beside the `fonts`, `art` and `build` folders.

The book contains seventeen chapters, a cover, frontispiece and seventeen chapter illustrations, six emergency reminder cards, reusable care and supply records, and a linked bibliography. The forms are intentionally unfilled reusable records. They are not official clinical forms. Illustrations are narrative art, not procedural medical diagrams.

## Edit

Edit `manuscript/01.md` through `17.md`, the frontmatter and afterword. Update `references.json` when a medical claim or source changes. `book.json` controls the title, subtitle, publisher, part titles, captions, image descriptions and subject finder. Keep review status accurate.

The Markdown subset is deliberate: paragraphs, level 1-3 headings, bold/italic text, simple numbered/bulleted lists, pipe tables and one-paragraph blockquotes. It does not execute embedded HTML, code, templates or external scripts. All assets are local. Reference numbers are identifiers and need not be contiguous.

Keep original illustration PNGs in `art/originals/`; the JPEGs beside them are the assets used in the book. `art/prompts.json` records visual direction and scene briefs. Generated artwork was made using the built-in image-generation tool with the uploaded series art as reference. No source-archive content or third-party clinical PDF collection is redistributed here.

## Rebuild on Windows (PowerShell)

Requires CPython 3.12 or newer. The dependency versions below are those used for the delivered build. No API key, account, Node installation, image generation or network access is needed after dependencies are installed.

```powershell
Set-Location .\zombieproof-medical
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe .\tools\build.py
```

## Rebuild on Linux

```bash
cd zombieproof-medical
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/build.py
```

The build overwrites generated files in `build/` and `print.html`; it preserves the manuscript and art. It checks chapter and asset completeness, known reference identifiers, cover artwork, EPUB XML, local EPUB links and mimetype placement. It records page locations in `build/pagination.json` and structural results in `build/validation.json`.

The delivered files were built in a Linux CPython 3.12 environment. The Windows commands invoke the same portable build; they were not executed on a Windows host. An EPUB reader may apply its own font, colours and pagination. This is a reading/print PDF, not a printer-specific spine/back-cover wrap, press-certified PDF/X file or clinically certified manual.

## Files

```text
zombieproof-medical/
  README.md
  SOURCE_REVIEW.md
  PRODUCTION_CHECKS.md
  book.json
  references.json
  requirements.txt
  print.html
  manuscript/
    frontmatter.md
    01.md ... 17.md
    afterword.md
  art/
    cover.jpg
    frontis.jpg
    ch01.jpg ... ch17.jpg
    prompts.json
    originals/
      cover.png
      frontis.png
      ch01.png ... ch17.png
  fonts/
    LICENSES.txt
    Fraunces and Literata font files (.ttf and .woff)
  tools/
    build.py
  build/
    Zombieproof-Medical.pdf
    Zombieproof-Medical.epub
    Zombieproof-Medical.md
    cover-typeset.jpg
    pagination.json
    validation.json
```

## Scope and main limitation

Civilian first aid, preparedness, delayed access to care, medicine continuity and everyday supportive care, using UK emergency conventions. It contains no invasive procedure tutorials or prescription regimens. Product labels, local arrangements and current professional advice take precedence. **Independent clinical review remains the principal publication requirement.**

Text and edition rights: © 2026 whispr.dev. Font software remains under its own SIL Open Font License; see `fonts/LICENSES.txt`. Referenced organisations are not endorsers.
