# Zombieproof Publisher Kit 1.0.0

A local book-finishing script for the supplied **Radio, Computers, Engines and
Water** books. Fill in one JSON form, add your publisher's device, and build
personalised full-colour PDFs, EPUB 3 ebooks and self-contained HTML editions.
The four manuscripts, cover artwork, frontispieces, chapter plates and fonts
are included. You do not need the original web application or its server.

## Windows: first run

Requires native Windows Python **3.12 or newer**. Python 3.14 is suitable.
Use PowerShell in the extracted `zombieproof-publisher-kit` folder.

1. Install the pinned Python packages and the PDF rendering browser:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1
   ```

   This process-scoped policy option does not change your machine's execution
   policy. Setup needs internet access; building books afterwards does not.
   No activation of the virtual environment is required.

2. Open `publishing-details.json` in VS Code. Fill in the empty author,
   publisher name and publisher city fields. Review the years and edition.
   Everything else is optional. Details under `shared` apply to all four
   books. Entries under `books` override the shared values for one book.

3. Put your image at **`assets/publisher-imprint.png`**. A transparent PNG is
   ideal. The mark appears on the title page and colophon, at 25 mm wide by
   default. Change `imprint_width_mm` to adjust it. If you do not want an image,
   set `imprint_image` to `""`. It is not necessary to invent a logo.

4. Check the form, then build all four books:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1 -Check
   powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1
   ```

   Your files appear in `finished\radio`, `finished\computers`,
   `finished\engines` and `finished\water`. Each folder contains:

   - `Zombieproof-Title.pdf`: the complete illustrated, typeset 6 × 9 inch book,
     including its front cover, live contents links and PDF bookmarks.
   - `Zombieproof-Title.epub`: a reflowable ebook with the same personalised
     front/back matter, its own format-specific ISBN and proper ebook metadata.
   - `Zombieproof-Title.html`: a self-contained, offline HTML edition with its
     illustrations and fonts embedded. Print pagination belongs to the PDF;
     HTML is a continuous reading/inspection copy.
   - `build-report.json`: page count, chapter count, PDF contents destinations,
     file sizes and SHA-256 checksums.

To build just one book:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1 -Book engines
```

**Existing editions are protected.** For the next revision, select a fresh
output folder. You can compare editions and keep the previous result:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1 -Output finished-v2
```

## Try it before filling in anything

The demonstration form uses the deliberately obvious author name **Production
Proof** and **Sample Imprint**. It is separate from your real publishing form.
It also demonstrates a dedication, acknowledgements, biography and foreword
credit. The illustrative mark is in `assets/sample-device.svg`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1 -Config demo-details.json -Book engines -Output demo-output
```

## What goes in the form?

JSON requires double quotes, no comments and no trailing commas. Save as UTF-8.
Each array entry is one paragraph, or one item where indicated. An empty string
means no value; an empty array means no entries. Optional sections are removed
when empty; nothing is left as a line for handwriting.

| Field within `shared` or a book override | Meaning |
| --- | --- |
| `author` | Exact byline on cover, title page, signatures and PDF/EPUB metadata. Required. |
| `copyright_holder` | Owner credited on copyright page. Empty defaults to the author. |
| `copyright_year` | Numeric copyright year. |
| `publication_year` | Numeric publication year. |
| `edition` | Such as `First edition` or `Second edition`. |
| `language` | Language tag, initially `en-GB`. |
| `publisher.name` | Publisher/imprint name. Required. |
| `publisher.city` | Publication city/place. Required. |
| `publisher.website` | Optional publisher URL, printed as text. |
| `publisher.contact` | Optional contact email/address, printed as text. |
| `publisher.imprint_image` | File path relative to the JSON form, or `""` for no image. PNG, JPEG or self-contained SVG. |
| `publisher.imprint_width_mm` | Printed width, between 5 and 60 mm. Height is limited proportionately. |
| `isbn.pdf` | PDF/print edition ISBN. Empty omits the ISBN. |
| `isbn.epub` | Separate EPUB ISBN. Empty omits the ISBN. |
| `cataloguing_data` | Optional supplied catalogue data. The script does not invent a catalogue record. |
| `printed_in` | Optional country or printer statement. Empty omits it. |
| `dedication` | Array of dedication paragraphs. Empty removes that page. |
| `acknowledgements` | Array of acknowledgement paragraphs. Empty removes that section. |
| `biography` | Array of biography paragraphs. Empty removes the author bio section. |
| `foreword_credit.name` | Person accepting the supplied foreword byline. Empty leaves it unsigned. |
| `foreword_credit.place_and_date` | Optional foreword location/date. |
| `preface_place_and_date` | Optional location/date under the preface author signature. |
| `afterword_place_and_date` | Optional location/date under the afterword author signature. |
| `endorsements` | Array of real `{ "quote": "...", "credit": "..." }` items. Empty removes dummy praise. |
| `other_titles` | Array of real `{ "title": "...", "description": "..." }` items. Empty removes the speculative forthcoming-books page. |
| `illustration_credit` | Exact artwork credit/disclosure you want on the copyright page. |

All user-entered prose is treated as **plain text**, including `<`, `>` and `&`.
You cannot accidentally insert HTML by pasting an address or quotation.

## Per-book details

The supplied form exposes empty ISBN fields separately for each of the four
books. Do not put a single ISBN in `shared` and reuse it for different books.
ISBN checksums are checked; different books and formats must have different
assigned identifiers. The script does not purchase or assign ISBNs.

You can add any shared field to a specific book's object to replace it for that
book. Objects merge recursively; arrays replace the entire shared array.
For example, the complete contents of the `engines` object can be:

```json
{
  "isbn": { "pdf": "", "epub": "" },
  "dedication": ["For the people who check the oil."],
  "biography": ["Your first biography paragraph.", "Your second paragraph."],
  "publisher": { "city": "Cardiff" }
}
```

These example biography sentences are instructions for the form, not content
included in your real edition. Replace them with your own text if you use them.

If a book needs another author, illustration credit, edition or imprint, put
those fields in its override. A different JSON form can live elsewhere; image
paths are always resolved against that form's folder.

## Existing Edge/Chrome instead of a browser download

Windows users can use an already installed Edge browser. This avoids downloading
another Chromium copy. The automated browser is a separate temporary process;
it does not use your signed-in profile.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1 -UseInstalledBrowser
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build.ps1 -BrowserChannel msedge
```

Use `chrome` instead of `msedge` for installed Google Chrome. PDF rendering needs
a compatible Chromium browser. The default pinned Chromium installation is the
most reproducible option and was used for the supplied build verification.

## Linux

```bash
bash setup.sh
# Edit publishing-details.json and add assets/publisher-imprint.png.
bash build.sh --check
bash build.sh
```

On a minimal Debian/Ubuntu installation, Playwright may report missing system
libraries. Its documented installer is:

```bash
.venv/bin/python -m playwright install-deps chromium
```

That system-package operation may require administrator privileges. Linux
builds were exercised in the supplied test environment; Windows launchers are
provided but were not executed on a Windows machine here.

## Direct Python commands and tests

Windows virtual-environment Python:

```powershell
.\.venv\Scripts\python.exe publish.py --check
.\.venv\Scripts\python.exe publish.py --book water --output edition-water
.\.venv\Scripts\python.exe publish.py --formats epub html --output ebook-only
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On Linux replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.
`--formats epub html` does not launch a browser. `--check` validates publishing
details, template coverage, fonts and expected illustration files; it is not a
PDF layout review. Failed books never appear as complete editions. If a later
book fails in a multi-book run, already completed books remain in the output
folder. Select the failed book explicitly to retry.

## What the builder repairs

- Fills author, publisher, copyright, edition, publication, dedication,
  signature, acknowledgements, biography and imprint locations.
- Removes the specific instructions saying to leave names blank or fill them
  in ink. Preserves the supplied chapters, captions and safety/legal passages.
- Removes invented endorsements and speculative forthcoming titles unless you
  provide real replacements.
- Recovers the supplied Fraunces and Literata font files from the EPUBs and
  bundles them for offline output. Uses the available typeface weights; where
  the original HTML requested absent weights, the nearest bundled face is used.
- Repairs the subtitle style collision and table/preformatted-text behaviour.
- Rebuilds the contents folios from real PDF destinations until they stabilise.
  Links and numbers stay correct when optional pages are added or removed.
- Builds the EPUB from the same personalised book, so its title page and
  copyright page agree with its actual creator/publisher metadata.
- Writes completed editions without overwriting previous ones.

## Print production boundary

The PDF is a full-colour, 6 × 9 inch, complete reading edition with fonts
embedded and the archived illustrations retained at source resolution. The
paper, lamination and glossy finish are chosen with your printer. This kit
does **not** create a printer-specific wraparound cover, calculate a spine,
add bleed, convert to CMYK or certify PDF/X compliance. Those depend on the
printer's trim/bleed template, binding, paper stock and final page count.

The PDF includes a front cover and an intentional blank verso, matching the
supplied design. Do not submit it blindly as a printer's interior-only file.
Once a printer is chosen, prepare the separate interior and cover against its
actual specification. EPUB pagination follows the reader's font and screen.

This is a production/personalisation tool, not an editorial rewrite or a new
technical review of the supplied manuscripts. Before releasing your edition,
read its final proof, confirm the credits and assigned identifiers, and obtain
whatever editorial review your publication requires.

## Files in the kit

```text
publish.py                        Complete builder
publishing-details.json           Your blank publishing form
demo-details.json                 Clearly labelled demonstration form
requirements.txt                  Pinned Python dependencies
Setup.ps1 / Build.ps1              Windows launchers
setup.sh / build.sh                Linux launchers
README.md                         These instructions
VALIDATION.md                     Recorded build checks and practical limits
assets/                           Your device image and a demo SVG
fonts/                            Five recovered font files and OFL licences
books/radio/                      Original print template, content JSON, art
books/computers/                   Original print template, content JSON, art
books/engines/                     Original print template, content JSON, art
books/water/                       Original print template, content JSON, art
tests/test_publisher.py            Configuration/content/EPUB regression tests
```

No Node application, site hosting, login, API key or subscription is required.
The supplied books remain your source materials; no ownership transfer or
additional artwork rights are implied by packaging them in this kit. The
included typefaces retain their SIL Open Font License notices in `fonts/`.

Implementation references:
[Playwright PDF API](https://playwright.dev/python/docs/api/class-page#page-pdf),
[Playwright browsers](https://playwright.dev/python/docs/browsers),
[pypdf documentation](https://pypdf.readthedocs.io/en/stable/),
[EPUB 3.3 specification](https://www.w3.org/TR/epub-33/).
