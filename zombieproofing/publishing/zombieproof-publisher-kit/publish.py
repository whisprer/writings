#!/usr/bin/env python3
"""Finish the four archived Zombieproof books. Python 3.12+; see README.md."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import mimetypes
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
    from pypdf import PdfReader, PdfWriter
except ImportError as exc:
    raise SystemExit("Run Setup.ps1 (Windows) or setup.sh (Linux) first: " + str(exc))

ROOT = Path(__file__).resolve().parent
BOOKS = ("radio", "computers", "engines", "water")
VERSION = "1.0.0"
FONT_FILES = (
    "fraunces-latin-600-normal.woff", "fraunces-latin-500-italic.woff",
    "literata-latin-400-normal.woff", "literata-latin-400-italic.woff",
    "literata-latin-700-normal.woff",
)
BASE = {
    "author": "", "copyright_holder": "", "copyright_year": 2026,
    "publication_year": 2026, "edition": "First edition", "language": "en-GB",
    "publisher": {"name": "", "city": "", "website": "", "contact": "",
                  "imprint_image": "assets/publisher-imprint.png", "imprint_width_mm": 25},
    "isbn": {"pdf": "", "epub": ""}, "cataloguing_data": "", "printed_in": "",
    "dedication": [], "acknowledgements": [], "biography": [],
    "foreword_credit": {"name": "", "place_and_date": ""},
    "preface_place_and_date": "", "afterword_place_and_date": "", "endorsements": [], "other_titles": [],
    "illustration_credit": "Illustrations prepared for this edition.",
}

EXTRA_CSS = """
/* Repairs to the archived layout and the new publishing matter. */
.cover-band { min-height: 2.15in; height: auto; flex: none; padding-top: .16in; }
.cover-art { min-height: 0; }
.cover-band h1 { font-size: 30pt; }
.cover-band .sub, .title > .sub { font-size: 12pt; line-height: 1.3;
  vertical-align: baseline; margin-top: .09in; }
.cover-author { font-family: Fraunces, serif; font-size: 12pt; margin: .1in 0 .04in; }
.cover-publisher { font-size: 8pt; letter-spacing: .06em; margin: 0; }
.title { padding-top: .65in; break-inside: avoid; }
.title > * { page: silent; }
.title-gap { height: .25in; }
.title-author { font-family: Fraunces, serif; font-size: 17pt; margin: .18in 0 .35in; }
.publisher-device { display: inline-block; height: auto; max-height: .6in; object-fit: contain;
  margin: .16in 0; max-width: 100%; }
.publishing-line { margin: .28em 0; overflow-wrap: anywhere; }
.credit { margin-top: 1em; font-style: italic; }
.copy { font-size: 9pt; line-height: 1.4; }
.dedi { padding-top: .8in; }
.toc-row { display: block; position: relative; padding-left: 1.8em;
  padding-right: 2.6em; margin: .25em 0; }
.toc-n { position: absolute; left: 0; }
.toc-dots { display: none; }
.pg { position: absolute; right: 0; bottom: 0; }
.table-wrap { break-inside: auto; overflow: visible; }
table { table-layout: auto; overflow-wrap: anywhere; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; break-inside: auto; }
figure, img { max-width: 100%; }
.plate img { max-height: 3.15in; object-fit: contain; }
.frontis img { max-height: 4.1in; object-fit: contain; }
.sign-label { display: none; }
@page :blank { @top-center { content: none; } @bottom-center { content: none; } }
@media screen {
 body { max-width: 6in; margin: 1rem auto; background: white; padding: .35in; }
 .coverpage { width: 100%; height: 8in; }
 section, article { margin-bottom: 2em; }
 .part { height: 5in; }
}
"""


def merge(a: dict, b: dict) -> dict:
    result = copy.deepcopy(a)
    for key, value in b.items():
        result[key] = merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else copy.deepcopy(value)
    return result


def validate_shape(value, model, at="shared"):
    if isinstance(model, dict):
        if not isinstance(value, dict):
            raise ValueError(f"{at} must be an object")
        unknown = set(value) - set(model)
        if unknown:
            raise ValueError(f"Unknown field(s) in {at}: {', '.join(sorted(unknown))}")
        for k, v in value.items():
            validate_shape(v, model[k], at + "." + k)
    elif isinstance(model, list):
        if not isinstance(value, list):
            raise ValueError(f"{at} must be a JSON array")
        shape = ({"quote": "", "credit": ""} if at.endswith("endorsements") else
                 {"title": "", "description": ""} if at.endswith("other_titles") else "")
        for i, v in enumerate(value):
            validate_shape(v, shape, f"{at}[{i}]")
            if isinstance(shape, dict) and (set(v) != set(shape) or any(not str(x).strip() for x in v.values())):
                raise ValueError(f"{at}[{i}] requires all non-empty fields: {', '.join(shape)}")
    elif isinstance(model, int):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 1 <= value <= 9999:
            raise ValueError(f"{at} must be a positive number")
        if not at.endswith("imprint_width_mm") and not isinstance(value, int):
            raise ValueError(f"{at} must be a whole year")
    elif not isinstance(value, str):
        raise ValueError(f"{at} must be text (use an empty string to omit it)")


def valid_isbn(value: str) -> bool:
    n = re.sub(r"[-\s]", "", value).upper()
    if len(n) == 13 and n.isdigit() and n.startswith(("978", "979")):
        return sum(int(x) * (1 if i % 2 == 0 else 3) for i, x in enumerate(n)) % 10 == 0
    if len(n) == 10 and n[:9].isdigit() and (n[-1].isdigit() or n[-1] == "X"):
        return sum((10-i) * (10 if x == "X" else int(x)) for i, x in enumerate(n)) % 11 == 0
    return False


def read_config(path: Path) -> dict:
    def unique(pairs):
        obj = {}
        for k, v in pairs:
            if k in obj:
                raise ValueError(f"Duplicate JSON key: {k}")
            obj[k] = v
        return obj
    cfg = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)
    if not isinstance(cfg, dict) or set(cfg) != {"schema_version", "shared", "books"} or type(cfg["schema_version"]) is not int or cfg["schema_version"] != 1:
        raise ValueError("Expected schema_version: 1, shared: {...}, books: {...}")
    validate_shape(cfg["shared"], BASE)
    if not isinstance(cfg["books"], dict) or set(cfg["books"]) - set(BOOKS):
        raise ValueError("books must contain only radio, computers, engines, water")
    for key, override in cfg["books"].items():
        validate_shape(override, BASE, "books." + key)
    return cfg


def metadata(cfg: dict, book: str, config_dir: Path) -> dict:
    m = merge(merge(BASE, cfg["shared"]), cfg["books"].get(book, {}))
    for label, value in [("author", m["author"]), ("publisher.name", m["publisher"]["name"]),
                         ("publisher.city", m["publisher"]["city"])]:
        if not value.strip():
            raise ValueError(f"{book}: fill in {label}")
    m["copyright_holder"] = m["copyright_holder"].strip() or m["author"]
    if not re.fullmatch(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", m["language"]):
        raise ValueError(f"{book}: language must be a language tag such as en-GB")
    for kind, val in m["isbn"].items():
        if val and not valid_isbn(val):
            raise ValueError(f"{book}: invalid {kind} ISBN checksum")
    if m["isbn"]["pdf"] and re.sub(r"[-\s]", "", m["isbn"]["pdf"]) == re.sub(r"[-\s]", "", m["isbn"]["epub"]):
        raise ValueError(f"{book}: PDF and EPUB ISBNs must differ; omit unassigned ISBNs")
    image = m["publisher"]["imprint_image"]
    if image:
        p = (config_dir / image).resolve()
        if not p.is_file() or p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".svg"):
            raise ValueError(f"{book}: imprint image missing or unsupported: {p}. Use PNG/JPEG/SVG, or set imprint_image to an empty string.")
        if p.suffix.lower() == ".svg":
            node = ET.fromstring(p.read_bytes())
            if node.tag.split("}")[-1] != "svg":
                raise ValueError("Imprint SVG must have an svg root element")
            for el in node.iter():
                if el.tag.split("}")[-1] in ("script", "foreignObject", "image", "use", "style"):
                    raise ValueError("SVG imprint must be self-contained, with no scripts, stylesheets or embedded resources")
                for k, v in el.attrib.items():
                    if k.lower().startswith("on") or "href" in k or "url(" in v.lower():
                        raise ValueError("SVG imprint contains an active or external reference")
        m["imprint_path"] = p
    else:
        m["imprint_path"] = None
    if not 5 <= m["publisher"]["imprint_width_mm"] <= 60:
        raise ValueError("imprint_width_mm must be between 5 and 60")
    return m


def add(soup, parent, text: str, name="p", cls=None):
    el = soup.new_tag(name)
    if cls:
        el["class"] = cls
    el.string = text
    parent.append(el)
    return el


def paragraphs(soup, parent, lines):
    for line in lines:
        if line.strip():
            add(soup, parent, line, cls="publishing-line")


def replace_section(soup, id, heading, lines):
    sec = soup.find(id=id)
    if sec is None:
        raise ValueError(f"Template is missing section {id}")
    if not lines:
        sec.decompose()
        return
    sec.clear()
    add(soup, sec, heading, "h1")
    paragraphs(soup, sec, lines)


def device(soup, parent, m):
    if m["imprint_path"]:
        img = soup.new_tag("img", src="publisher-imprint" + m["imprint_path"].suffix.lower())
        img["alt"] = m["publisher"]["name"] + " publisher's device"
        img["class"] = "publisher-device"
        img["style"] = f'width: {m["publisher"]["imprint_width_mm"]}mm'
        parent.append(img)


def prepare(book: str, m: dict) -> BeautifulSoup:
    soup = BeautifulSoup((ROOT/"books"/book/"template.html").read_text(encoding="utf-8"), "html.parser")
    soup.html["lang"] = m["language"]
    # Recover the exact typefaces from the archived EPUBs; all are bundled locally.
    css = soup.style.string or soup.style.get_text()
    css = re.sub(r"(?:\.\./)+node_modules/@fontsource/[^/]+/files/", "fonts/", css)
    css = css.replace("fraunces-latin-700-normal.woff", "fraunces-latin-600-normal.woff")
    css = css.replace("literata-latin-700-italic.woff", "literata-latin-400-italic.woff")
    soup.style.string = css + EXTRA_CSS
    for key, value in (("author", m["author"]), ("publisher", m["publisher"]["name"])):
        soup.head.append(soup.new_tag("meta", attrs={"name": key, "content": value}))
    band = soup.select_one(".cover-band")
    add(soup, band, m["author"], cls="cover-author")
    add(soup, band, m["publisher"]["name"], cls="cover-publisher")
    title = soup.find(id="title")
    for blank in title.select(".blank"):
        blank.decompose()
    add(soup, title, m["author"], cls="title-author")
    device(soup, title, m)
    paragraphs(soup, title, [m["publisher"]["name"], m["publisher"]["city"]])
    copyright = soup.find(id="copyright")
    data = json.loads((ROOT/"books"/book/"content.json").read_text(encoding="utf-8"))
    copyright.clear()
    add(soup, copyright, "Copyright", "h1")
    paragraphs(soup, copyright, [f'Copyright © {m["copyright_year"]} {m["copyright_holder"]}', data["copyright"][0],
        "Published by " + m["publisher"]["name"], m["publisher"]["city"], m["publisher"]["website"],
        m["publisher"]["contact"], f'{m["edition"]} · {m["publication_year"]}',
        "ISBN: " + m["isbn"]["pdf"] if m["isbn"]["pdf"] else "", m["cataloguing_data"],
        *data["copyright"][1:], m["illustration_credit"],
        "Printed in " + m["printed_in"] if m["printed_in"] else ""])
    replace_section(soup, "dedication", "Dedication", m["dedication"])
    replace_section(soup, "ack", "Acknowledgments", m["acknowledgements"])
    replace_section(soup, "author", "About the author", [m["author"], *m["biography"]] if m["biography"] else [])
    praise = soup.find(id="praise")
    if not m["endorsements"]:
        praise.decompose()
    else:
        heading = praise.h1.get_text()
        praise.clear()
        add(soup, praise, heading, "h1")
        for item in m["endorsements"]:
            q = soup.new_tag("blockquote")
            add(soup, q, item["quote"])
            add(soup, q, "— " + item["credit"], "cite")
            praise.append(q)
    soon = soup.find(id="soon")
    if not m["other_titles"]:
        soon.decompose()
    else:
        soon.clear()
        add(soup, soon, "Also from " + m["publisher"]["name"], "h1")
        for item in m["other_titles"]:
            add(soup, soon, item["title"], "h2")
            add(soup, soon, item["description"])
    for sid, signature in [("foreword", [m["foreword_credit"]["name"], m["foreword_credit"]["place_and_date"]]),
                           ("preface", [m["author"], m["preface_place_and_date"]]),
                           ("afterword", [m["author"], m["afterword_place_and_date"]])]:
        sec = soup.find(id=sid)
        for el in sec.select(".blank, .sign-label"):
            el.decompose()
        for text in signature:
            if text.strip():
                add(soup, sec, text, cls="credit")
    # Remove the specific production instructions, retaining the rest of the prose.
    for sid in ("foreword", "preface", "colophon"):
        for p in list(soup.find(id=sid).find_all("p")):
            text = p.get_text(" ", strip=True)
            if ("blank on purpose" in text or "intentionally blank" in text or
                text.startswith("Leave your name off the title page")):
                if sid == "colophon":
                    p.clear()
                    p.string = "Trim: six by nine inches. " + m["edition"] + "."
                else:
                    p.decompose()
    colophon = soup.find(id="colophon")
    for blank in colophon.select(".blank"):
        blank.decompose()
    device(soup, colophon, m)
    paragraphs(soup, colophon, [m["publisher"]["name"], m["publisher"]["city"]])
    # Remove TOC rows for omitted optional sections. IDs are unchanged elsewhere.
    ids = {x["id"] for x in soup.select("[id]")}
    for row in list(soup.select(".toc-row")):
        if row.get("href", "").lstrip("#") not in ids:
            row.decompose()
        elif row.select_one(".pg"):
            row.select_one(".pg").string = "000"
    if soup.select(".blank"):
        raise ValueError(f"{book}: unhandled blank field in template: " + ", ".join(x.get_text(" ", strip=True) for x in soup.select(".blank")))
    if soup.select("script, iframe, object, embed"):
        raise ValueError(f"{book}: active content in template")
    return soup


def data_uri(path: Path) -> str:
    mime = "font/woff" if path.suffix == ".woff" else mimetypes.guess_type(path.name)[0]
    if not mime:
        raise ValueError(f"Unknown asset type: {path}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def asset_path(book, m, name):
    if name.startswith("publisher-imprint."):
        return m["imprint_path"]
    if name.startswith("fonts/"):
        return ROOT/"fonts"/Path(name).name
    if name.startswith("art/"):
        return ROOT/"books"/book/"art"/Path(name).name
    raise ValueError(f"Unexpected asset reference: {name}")


def standalone(soup, book, m) -> str:
    out = copy.deepcopy(soup)
    for img in out.select("img[src]"):
        img["src"] = data_uri(asset_path(book, m, img["src"]))
    out.style.string = re.sub(r'url\(["\']?([^\)"\']+)["\']?\)',
        lambda match: 'url("' + data_uri(asset_path(book, m, match[1])) + '")', out.style.string)
    return str(out)


def destinations(reader):
    return {key.lstrip("/"): reader.get_destination_page_number(dest) + 1
            for key, dest in reader.named_destinations.items()}


def render_pdf(soup, book, m, target, browser, work):
    page = browser.new_page()
    # The document embeds all assets. No network request is required or allowed.
    page.route(re.compile(r"https?://.*"), lambda route: route.abort())
    raw = work/"pass.pdf"
    try:
        page.emulate_media(media="print")
        for attempt in range(5):
            html = standalone(soup, book, m)
            preview = work/"render.html"
            preview.write_text(html, encoding="utf-8")
            page.goto(preview.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            failed = page.evaluate("Array.from(document.images).filter(i => !i.complete || !i.naturalWidth).map(i => i.alt)")
            if failed:
                raise ValueError("Images failed to load: " + str(failed))
            page.pdf(path=str(raw), prefer_css_page_size=True, print_background=True, outline=True, tagged=True)
            reader = PdfReader(raw)
            dests = destinations(reader)
            changed = False
            for row in soup.select(".toc-row"):
                id = row["href"].lstrip("#")
                if id not in dests:
                    raise ValueError(f"PDF link destination missing: {id}")
                pg = row.select_one(".pg")
                if pg is not None and pg.get_text() != str(dests[id]):
                    pg.string = str(dests[id])
                    changed = True
            if not changed:
                break
        else:
            raise ValueError("Contents pagination did not converge after five passes")
        # Incremental metadata update preserves Chromium's complete tagged object
        # graph, destinations and outline without cloning shared structure nodes.
        writer = PdfWriter(raw, incremental=True)
        writer.add_metadata({"/Title": soup.title.get_text(), "/Author": m["author"],
                             "/Subject": "An illustrated Zombieproof field manual",
                             "/Creator": "Zombieproof Publisher Kit " + VERSION,
                             "/Keywords": "Zombieproof; " + m["publisher"]["name"]})
        with target.open("wb") as stream:
            writer.write(stream)
        result = PdfReader(target)
        if any(abs(float(p.mediabox.width)-432) > 1 or abs(float(p.mediabox.height)-648) > 1 for p in result.pages):
            raise ValueError("Unexpected PDF trim size")
        # Every chapter needs a live destination, not merely a printed contents number.
        for ch in soup.select(".chapter"):
            if ch["id"] not in destinations(result):
                raise ValueError("Missing chapter link: " + ch["id"])
        return {"pages": len(result.pages), "pagination_passes": attempt+1, "toc": dests}
    finally:
        page.close()


XHTML = "http://www.w3.org/1999/xhtml"
OPF = "http://www.idpf.org/2007/opf"
DC = "http://purl.org/dc/elements/1.1/"
EPUB = "http://www.idpf.org/2007/ops"


def xhtml_node(tag):
    node = ET.Element("{" + XHTML + "}" + tag.name)
    for k, value in tag.attrs.items():
        node.set(k, " ".join(value) if isinstance(value, list) else str(value))
    last = None
    for child in tag.children:
        if isinstance(child, Tag):
            last = xhtml_node(child)
            node.append(last)
        elif isinstance(child, NavigableString):
            if last is None:
                node.text = (node.text or "") + str(child)
            else:
                last.tail = (last.tail or "") + str(child)
    return node


def xml_bytes(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def document(title, lang, content):
    root = ET.Element("{" + XHTML + "}html", {"lang": lang, "{http://www.w3.org/XML/1998/namespace}lang": lang})
    head = ET.SubElement(root, "{" + XHTML + "}head")
    ET.SubElement(head, "{" + XHTML + "}title").text = title
    ET.SubElement(head, "{" + XHTML + "}link", {"rel": "stylesheet", "type": "text/css", "href": "style.css"})
    body = ET.SubElement(root, "{" + XHTML + "}body")
    body.append(content)
    return xml_bytes(root)


def render_epub(soup, book, m, target):
    """Rebuild an EPUB 3 from the same personalised DOM, never patch old metadata only."""
    ET.register_namespace("", XHTML)
    ET.register_namespace("epub", EPUB)
    out = copy.deepcopy(soup)
    # PDF ISBN and printed folios do not belong in a reflowable digital edition.
    for p in list(out.find(id="copyright").find_all("p")):
        if p.get_text().startswith("ISBN:"):
            p.decompose()
    if m["isbn"]["epub"]:
        add(out, out.find(id="copyright"), "ISBN: " + m["isbn"]["epub"])
    for el in out.select(".blank-verso, #contents, .title-gap"):
        el.decompose()
    cover = out.select_one(".coverpage")
    cover["id"] = "cover"
    cover.select_one(".cover-art").decompose()
    img = out.new_tag("img", src="art/cover.jpg", alt=out.title.get_text() + " cover illustration")
    cover.insert(0, img)
    sections = out.body.find_all(recursive=False)
    id_files = {el["id"]: el["id"] + ".xhtml" for el in sections}
    for anchor in out.select('a[href^="#"]'):
        id = anchor["href"][1:]
        if id in id_files:
            anchor["href"] = id_files[id] + "#" + id
    files = {}
    for el in sections:
        heading = el.find(["h1", "h2"])
        files[el["id"] + ".xhtml"] = document(heading.get_text(" ",strip=True) if heading else el["id"], m["language"], xhtml_node(el))
    nav = ET.Element("{" + XHTML + "}nav", {"{" + EPUB + "}type": "toc", "id": "toc"})
    ET.SubElement(nav, "{" + XHTML + "}h1").text = "Contents"
    ol = ET.SubElement(nav, "{" + XHTML + "}ol")
    for el in sections:
        if el["id"] in ("cover", "halftitle", "frontis", "copyright"):
            continue
        li = ET.SubElement(ol, "{" + XHTML + "}li")
        heading = el.find(["h1", "h2"])
        label = el.select_one(".label")
        ET.SubElement(li, "{" + XHTML + "}a", {"href": el["id"] + ".xhtml"}).text = (
            (label.get_text(" ",strip=True) + ". ") if label else "") + (heading.get_text(" ",strip=True) if heading else el["id"])
    files["nav.xhtml"] = document("Contents", m["language"], nav)
    css = re.sub(r"@page[^{}]*\{(?:[^{}]|\{[^{}]*\})*\}", "", out.style.string)
    css += """
body { font-size: 1em; line-height: 1.5; margin: 0; padding: 1em; }
.coverpage { width: auto; height: auto; display: block; }
.cover-band { height: auto; padding: 1em 0; }
.cover-band h1 { font-size: 2.5em; }
.title, .half, .dedi { padding-top: 1em; }
.frontis img { width: 100%; max-width: 25em; max-height: none; }
.part { height: auto; margin: 2em 0; }
.part-inner { position: static; }
.plate img { width: 100%; max-height: none; }
.lede::first-letter { float: none; font-size: 1em; }
.title-author { font-size: 1.5em; }
.publisher-device { max-width: 40%; }
@media screen { body { max-width: none; margin: 0; padding: 1em; } }
"""
    files["style.css"] = css.encode("utf-8")
    for imgpath in (ROOT/"books"/book/"art").glob("*.jpg"):
        files["art/"+imgpath.name] = imgpath.read_bytes()
    for name in FONT_FILES:
        files["fonts/"+name] = (ROOT/"fonts"/name).read_bytes()
    if m["imprint_path"]:
        files["publisher-imprint" + m["imprint_path"].suffix.lower()] = m["imprint_path"].read_bytes()
    package = ET.Element("{"+OPF+"}package", {"version": "3.0", "unique-identifier": "uid"})
    meta = ET.SubElement(package, "{"+OPF+"}metadata")
    identity = m["isbn"]["epub"] or (book + "|" + m["author"] + "|" + m["publisher"]["name"] + "|" + str(m["publication_year"]))
    uid = "urn:isbn:" + re.sub(r"[-\s]", "", identity) if m["isbn"]["epub"] else "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "zombieproof:" + identity))
    ET.SubElement(meta, "{"+DC+"}identifier", {"id": "uid"}).text = uid
    for key, value in [("title", out.title.get_text()), ("creator", m["author"]), ("publisher", m["publisher"]["name"]),
                       ("language", m["language"]), ("date", str(m["publication_year"])),
                       ("rights", f'Copyright © {m["copyright_year"]} {m["copyright_holder"]}. All rights reserved.')]:
        ET.SubElement(meta, "{"+DC+"}"+key).text = value
    ET.SubElement(meta, "{"+OPF+"}meta", {"property": "dcterms:modified"}).text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = ET.SubElement(package, "{"+OPF+"}manifest")
    ids = {}
    for i, name in enumerate(files):
        id = "item" + str(i)
        ids[name] = id
        mime = "application/xhtml+xml" if name.endswith(".xhtml") else "font/woff" if name.endswith(".woff") else mimetypes.guess_type(name)[0]
        attrs = {"id": id, "href": name, "media-type": mime}
        if name == "nav.xhtml": attrs["properties"] = "nav"
        if name == "art/cover.jpg": attrs["properties"] = "cover-image"
        # SVG used directly in an XHTML spine item must be declared as such.
        if name.endswith(".xhtml") and b".svg" in files[name]: attrs["properties"] = "svg"
        ET.SubElement(manifest, "{"+OPF+"}item", attrs)
    spine = ET.SubElement(package, "{"+OPF+"}spine")
    for el in sections:
        ET.SubElement(spine, "{"+OPF+"}itemref", {"idref": ids[el["id"]+".xhtml"]})
        if el["id"] == "copyright":
            ET.SubElement(spine, "{"+OPF+"}itemref", {"idref": ids["nav.xhtml"]})
    files["content.opf"] = xml_bytes(package)
    with zipfile.ZipFile(target, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
        for name, data in files.items():
            z.writestr("OEBPS/"+name, data, compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(target) as z:
        for name in z.namelist():
            if name.endswith((".xhtml", ".xml", ".opf")):
                ET.fromstring(z.read(name))
        if z.infolist()[0].filename != "mimetype" or z.infolist()[0].compress_type != 0:
            raise ValueError("Invalid EPUB container")


def verify_sources(book):
    folder = ROOT/"books"/book
    if not (folder/"template.html").is_file():
        raise ValueError("Missing bundled book: " + book)
    for name in FONT_FILES:
        if not (ROOT/"fonts"/name).is_file():
            raise ValueError("Missing bundled font: " + name)
    expected = json.loads((folder/"content.json").read_text(encoding="utf-8"))
    for id in ["cover", "frontis", *[ch["id"] for ch in expected["chapters"]]]:
        if not (folder/"art"/(id+".jpg")).is_file():
            raise ValueError("Missing illustration: " + id)


def build_one(book, m, output, browser, formats):
    verify_sources(book)
    soup = prepare(book, m)
    slug = "Zombieproof-" + book.capitalize()
    if output.exists():
        raise ValueError(f"Output already exists: {output}. Choose a new --output folder; existing editions are never overwritten.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".publishing-", dir=output.parent) as temporary:
        stage = Path(temporary)
        report = {"kit_version": VERSION, "book": book, "author": m["author"], "publisher": m["publisher"]["name"],
                  "chapters": len(soup.select(".chapter")), "illustrations": len(soup.select("img")), "files": {}}
        if "pdf" in formats:
            report.update(render_pdf(soup, book, m, stage/(slug+".pdf"), browser, stage))
        if "epub" in formats:
            render_epub(soup, book, m, stage/(slug+".epub"))
        if "html" in formats:
            (stage/(slug+".html")).write_text(standalone(soup, book, m), encoding="utf-8")
        for name in ["render.html", "pass.pdf"]:
            (stage/name).unlink(missing_ok=True)
        for path in stage.iterdir():
            report["files"][path.name] = {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        (stage/"build-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        # Completed editions appear only after the entire book has passed validation.
        stage.rename(output)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT/"publishing-details.json")
    parser.add_argument("--book", choices=["all", *BOOKS], default="all")
    parser.add_argument("--output", type=Path, default=ROOT/"finished")
    parser.add_argument("--formats", nargs="+", choices=["pdf", "epub", "html"], default=["pdf", "epub", "html"])
    parser.add_argument("--check", action="store_true", help="Check details, images and templates without producing files")
    parser.add_argument("--browser-channel", choices=["msedge", "chrome"], help="Use installed Edge or Chrome instead of downloaded Chromium")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    try:
        path = args.config.resolve()
        cfg = read_config(path)
        chosen = BOOKS if args.book == "all" else (args.book,)
        records = [(book, metadata(cfg, book, path.parent)) for book in chosen]
        seen_isbns = {}
        for book, m in records:
            for kind, value in m["isbn"].items():
                if value:
                    normalized = re.sub(r"[-\s]", "", value).upper()
                    if normalized in seen_isbns:
                        raise ValueError(f"ISBN reused by {book}/{kind} and {seen_isbns[normalized]}")
                    seen_isbns[normalized] = book + "/" + kind
        for book, m in records:
            verify_sources(book)
            prepare(book, m)
            if not args.check and (args.output.resolve()/book).exists():
                raise ValueError(f"Output already exists: {args.output.resolve()/book}. Choose a new --output folder.")
        if args.check:
            print("Details, fonts, illustrations and templates OK: " + ", ".join(chosen))
            return 0
        browser = None
        manager = None
        try:
            if "pdf" in args.formats:
                from playwright.sync_api import sync_playwright
                manager = sync_playwright().start()
                browser = manager.chromium.launch(channel=args.browser_channel, headless=True)
            for book, m in records:
                print("Building " + book + "...", flush=True)
                report = build_one(book, m, args.output.resolve()/book, browser, args.formats)
                print(f'  Complete: {report.get("pages", "no PDF")} pages; {report["chapters"]} chapters; {len(report["files"])} files', flush=True)
        finally:
            if browser: browser.close()
            if manager: manager.stop()
        print("Finished: " + str(args.output.resolve()))
        return 0
    except (ValueError, OSError, ImportError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        # Playwright has its own exception hierarchy; leave a useful nonzero result.
        print("BUILD FAILED: " + str(exc), file=sys.stderr)
        print("For browser setup run: python -m playwright install chromium", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
