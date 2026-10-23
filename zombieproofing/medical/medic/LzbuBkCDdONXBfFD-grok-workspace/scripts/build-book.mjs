import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { marked } from "marked";

const known = ["engines", "computers", "water", "medic"];
const slug = known.find((name) => process.argv.includes(name)) || "computers";
const matterPath =
  slug === "engines"
    ? "./matter-engines.mjs"
    : slug === "water"
      ? "./matter-water.mjs"
      : slug === "medic"
        ? "./matter-medic.mjs"
        : "./matter.mjs";
const matter = await import(matterPath);
const {
  AFTERWORD,
  BOOK,
  CAPTIONS,
  COLOPHON,
  COMING,
  COPYRIGHT,
  FOREWORD,
  FRONTIS_QUOTE,
  FRONTIS_SIGN,
  PARTS,
  PRAISE,
  PREFACE,
} = matter;

const ROOT = "/workspace";
const SRC = path.join(ROOT, "book", slug, "source");
const ART = path.join(ROOT, "public/book", slug, "art");
const JSON_OUT = path.join(ROOT, "src/content", `${slug}.json`);
const PRINT_HTML = path.join(ROOT, "public/book", slug, "print.html");
const PDF_OUT = path.join(ROOT, "public" + BOOK.pdf);
const EPUB_OUT = path.join(ROOT, "public" + BOOK.epub);

marked.setOptions({ gfm: true, breaks: false });

function esc(s) {
  const amp = String.fromCharCode(38);
  return String(s)
    .replace(/&/g, amp + "amp;")
    .replace(/</g, amp + "lt;")
    .replace(/>/g, amp + "gt;")
    .replace(/"/g, amp + "quot;");
}

function paras(lines) {
  return lines.map((p) => `<p>${esc(p)}</p>`).join("\n");
}

function readGroup(str, i) {
  if (str[i] !== "{") return { body: "", end: i };
  let depth = 0;
  for (let j = i; j < str.length; j++) {
    if (str[j] === "{") depth += 1;
    else if (str[j] === "}") {
      depth -= 1;
      if (depth === 0) return { body: str.slice(i + 1, j), end: j + 1 };
    }
  }
  return { body: str.slice(i + 1), end: str.length };
}

const SYMBOLS = {
  lambda: "λ",
  pi: "π",
  mu: "μ",
  Omega: "Ω",
  omega: "ω",
  tau: "τ",
  times: "×",
  cdot: "·",
  Delta: "Δ",
  theta: "θ",
  alpha: "α",
  beta: "β",
  sigma: "σ",
  infty: "∞",
  pm: "±",
  leq: "≤",
  geq: "≥",
  approx: "≈",
  rightarrow: "→",
};

function renderTex(src, display) {
  function parse(str) {
    let out = "";
    let i = 0;
    while (i < str.length) {
      if (str[i] === "\\") {
        const n = str[i + 1] || "";
        if (!/[a-zA-Z]/.test(n)) {
          if (n === ",") out += "\u2009";
          else if (n === " ") out += " ";
          else if (n) out += esc(n);
          i += n ? 2 : 1;
          continue;
        }
        let j = i + 1;
        let cmd = "";
        while (j < str.length && /[a-zA-Z]/.test(str[j])) {
          cmd += str[j];
          j += 1;
        }
        if (cmd === "frac") {
          const num = readGroup(str, j);
          const den = readGroup(str, num.end);
          out += `<span class="frac"><span class="num">${parse(num.body)}</span><span class="den">${parse(den.body)}</span></span>`;
          i = den.end;
          continue;
        }
        if (cmd === "sqrt") {
          const g = readGroup(str, j);
          out += `<span class="sqrt">√<span class="rad">${parse(g.body)}</span></span>`;
          i = g.end;
          continue;
        }
        if (cmd === "text" || cmd === "mathrm" || cmd === "textrm") {
          const g = readGroup(str, j);
          out += `<span class="tex-text">${esc(g.body)}</span>`;
          i = g.end;
          continue;
        }
        if (SYMBOLS[cmd]) {
          out += SYMBOLS[cmd];
          i = j;
          continue;
        }
        out += esc(cmd);
        i = j;
        continue;
      }
      if (str[i] === "_" || str[i] === "^") {
        const sup = str[i] === "^";
        let g;
        if (str[i + 1] === "{") g = readGroup(str, i + 1);
        else g = { body: str[i + 1] || "", end: i + 2 };
        out += `<span class="${sup ? "sup" : "sub"}">${parse(g.body)}</span>`;
        i = g.end;
        continue;
      }
      if (str[i] === "{" || str[i] === "}") {
        i += 1;
        continue;
      }
      out += esc(str[i]);
      i += 1;
    }
    return out;
  }
  const inner = parse(src.trim());
  return display ? `<span class="math display">${inner}</span>` : `<span class="math">${inner}</span>`;
}

function extractMath(md) {
  const blocks = [];
  let text = md.replace(/\\\[([\s\S]*?)\\\]/g, (_, tex) => {
    const i = blocks.length;
    blocks.push(renderTex(tex, true));
    return `\n\nZZMATH${i}ZZ\n\n`;
  });
  text = text.replace(/\\\(([\s\S]*?)\\\)/g, (_, tex) => {
    const i = blocks.length;
    blocks.push(renderTex(tex, false));
    return `ZZMATH${i}ZZ`;
  });
  return { text, blocks };
}

function restoreMath(html, blocks) {
  return html.replace(/ZZMATH(\d+)ZZ/g, (_, n) => blocks[Number(n)] || "");
}

function cleanChapter(raw, n) {
  let text = raw.replace(/\r\n/g, "\n");
  text = text.replace(/^#\s+Zombieproof.*\n+/i, "");
  text = text.replace(/\[attached_file:[^\]]+\]/g, "");
  text = text.replace(/\[translate:([^\]]+)\]/g, "$1");
  text = text.replace(/!\[[^\]]*\]\([^)]+\)/g, "");
  text = text.replace(/^\s*---\s*$/gm, "");
  text = text.replace(/\*See the next markdown[\s\S]*?\*/gi, "");
  text = text.replace(/^#{1,3}\s+.*next batch.*$/gim, "");
  text = text.replace(
    /Use the code provided in the source material to program your microcontroller\./g,
    "The draft promised a code listing here and did not include one, so bring a sketch you trust for this board.",
  );

  const patterns = [
    /^(#{1,3}\s*)Chapter\s+\d+\s*[:.—–-]\s*(.+)$/m,
    /^(#{1,3}\s*)Chapter\s*[:.—–-]\s*(.+)$/m,
    /^Chapter\s+\d+\s*[:.—–-]\s*(.+)$/m,
    /^Chapter\s*[:.—–-]\s*(.+)$/m,
  ];
  let title = `Chapter ${n}`;
  for (const p of patterns) {
    const m = text.match(p);
    if (m) {
      title = m[m.length - 1].trim();
      text = text.replace(m[0], "");
      break;
    }
  }
  text = text.replace(/^Chapter\s+\d+\s*[:.—–-].*(?:\n|$)/gm, "");

  if (!/^#{1,3}\s/m.test(text)) {
    const fences = [];
    text = text.replace(/```[\s\S]*?```/g, (block) => {
      const i = fences.length;
      fences.push(block);
      return `\n\nFencehold ${i} stays intact for the listing.\n\n`;
    });
    const blocks = text
      .split(/\n\s*\n/)
      .map((p) => p.trim())
      .filter(Boolean);
    const oneLine = (block) => {
      const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
      return lines.length === 1 ? lines[0] : null;
    };
    const listish = (block) => {
      const line = oneLine(block);
      if (!line) return false;
      if (line.length >= 88 || /[.!?]["”']?$/.test(line) || /^[-*]/.test(line)) return false;
      if (/^[^:\n]{2,48}:\s+\S/.test(line)) return false;
      if (/^Fencehold \d+/.test(line)) return false;
      return true;
    };
    const out = [];
    for (let i = 0; i < blocks.length; i += 1) {
      const block = blocks[i];
      if (listish(block)) {
        let j = i;
        const run = [];
        while (j < blocks.length && listish(blocks[j])) {
          run.push(oneLine(blocks[j]));
          j += 1;
        }
        if (run.length >= 2) {
          out.push(run.map((item) => `- ${item}`).join("\n"));
          i = j - 1;
          continue;
        }
      }
      const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
      if (lines.length >= 2) {
        const head = lines[0];
        const rest = lines.slice(1).join(" ");
        if (head.length < 96 && !/[.!?]["”']?$/.test(head) && rest) {
          out.push(`## ${head}`, rest);
          continue;
        }
      }
      if (lines.length === 1 && block.length < 90 && !/[.!?]["”']?$/.test(block) && !/:$/.test(block) && !/^[-*]/.test(block)) {
        out.push(`## ${block}`);
        continue;
      }
      if (lines.length === 1 && /^[^:\n]{2,48}:\s+\S/.test(block)) {
        const lead = block.split(":")[0];
        const after = block.slice(lead.length + 1).trim();
        const afterWords = after.split(/\s+/).length;
        if (!/[.]/.test(after) && afterWords <= 8) out.push(`## ${block}`);
        else out.push(block.replace(/^([^:]{2,48}):\s*/, "**$1.** "));
        continue;
      }
      out.push(lines.join(" "));
    }
    text = out.join("\n\n");
    text = text.replace(/Fencehold (\d+) stays intact for the listing\./g, (_, n) => fences[Number(n)] || "");
  }

  text = text.replace(/^#\s+/gm, "## ");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return { title: title.replace(/\s+/g, " "), body: text };
}

function mdToHtml(md) {
  const { text, blocks } = extractMath(md);
  let html = marked.parse(text);
  if (typeof html !== "string") html = String(html);
  html = restoreMath(html, blocks);
  if (html.startsWith("<p>")) html = html.replace("<p>", '<p class="lede">');
  html = html.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, "</table></div>");
  return html.trim();
}

function loadChapters() {
  const partOf = new Map();
  for (const part of PARTS) for (const n of part.chapters) partOf.set(n, part.id);
  const order = PARTS.flatMap((part) => part.chapters);
  const chapters = [];
  for (const n of order) {
    const raw = fs.readFileSync(path.join(SRC, `chpt${n}.md`), "utf8");
    const { title, body } = cleanChapter(raw, n);
    const id = `ch${String(n).padStart(2, "0")}`;
    chapters.push({
      n,
      id,
      part: partOf.get(n),
      title,
      html: mdToHtml(body),
      plate: `/book/${slug}/art/${id}.jpg`,
      caption: `Plate ${n}. ${CAPTIONS[n]}`,
    });
  }
  return chapters;
}

function buildModel() {
  const chapters = loadChapters();
  const count = chapters.length;
  return {
    id: slug,
    title: BOOK.title,
    titleLines: BOOK.titleLines,
    subtitle: BOOK.subtitle,
    kicker: BOOK.kicker,
    volumeLabel: BOOK.volumeLabel,
    pdf: BOOK.pdf,
    epub: BOOK.epub,
    cover: BOOK.cover,
    frontis: BOOK.frontis,
    frontisAlt: BOOK.frontisAlt,
    praiseTitle: BOOK.praiseTitle,
    titleKicker: BOOK.titleKicker,
    ackNote: BOOK.ackNote,
    copyright: COPYRIGHT,
    colophon: COLOPHON,
    frontisQuote: FRONTIS_QUOTE,
    frontisSign: FRONTIS_SIGN,
    parts: PARTS.map(({ id, numeral, title, blurb }) => ({ id, numeral, title, blurb })),
    chapters,
    foreword: paras(FOREWORD),
    preface: paras(PREFACE),
    afterword: paras(AFTERWORD),
    praise: PRAISE,
    coming: COMING,
    folios: {},
    chapterCount: count,
    tex: BOOK.tex || "",
  };
}

function tocHtml(model, folios) {
  const folio = (id) => (folios[id] ? esc(String(folios[id])) : "");
  const row = (id, num, title) =>
    `<a class="toc-row" href="#${id}"><span class="toc-n">${esc(num)}</span><span class="toc-t">${esc(title)}</span><span class="toc-dots"></span><span class="pg">${folio(id)}</span></a>`;
  const bits = [
    row("foreword", "", "Foreword"),
    row("preface", "", "A note on the drafts"),
  ];
  for (const part of PARTS) {
    bits.push(`<p class="toc-part">Part ${esc(part.numeral)} · ${esc(part.title)}</p>`);
    for (const n of part.chapters) {
      const ch = model.chapters[n - 1];
      bits.push(row(ch.id, String(ch.n), ch.title));
    }
  }
  bits.push(row("afterword", "", "Afterword"));
  bits.push(row("ack", "", "Acknowledgments"));
  bits.push(row("author", "", "About the author"));
  bits.push(row("soon", "", "Also forthcoming"));
  bits.push(row("colophon", "", "Colophon"));
  return bits.join("\n");
}

function blanks(labels) {
  return labels.map((label) => `<p class="blank"><span>${esc(label)}</span></p>`).join("\n");
}

function renderPrint(model, folios) {
  const chapters = model.chapters
    .map((ch, idx) => {
      const part = PARTS.find((p) => p.chapters[0] === ch.n);
      const opener = part
        ? `<section class="part" id="part${part.id}"><div class="part-inner"><p class="label">Part ${esc(part.numeral)}</p><h1>${esc(part.title)}</h1><p class="blurb">${esc(part.blurb)}</p></div></section>`
        : "";
      return `${opener}
<article class="chapter" id="${ch.id}">
  <p class="label">Chapter ${ch.n}</p>
  <h1>${esc(ch.title)}</h1>
  <figure class="plate"><img src="art/${ch.id}.jpg" alt="${esc(ch.caption)}"/><figcaption>${esc(ch.caption)}</figcaption></figure>
  <div class="prose">${ch.html}</div>
</article>`;
    })
    .join("\n");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>${esc(BOOK.title)}</title>
<style>
${printCss()}
</style>
</head>
<body>
<section class="coverpage">
  <div class="cover-art"></div>
  <div class="cover-band">
    <p class="kicker">${esc(BOOK.kicker)}</p>
    <h1>${BOOK.titleLines[0]}<br/>${BOOK.titleLines[1]}</h1>
    <p class="sub">${esc(BOOK.subtitle)}</p>
  </div>
</section>
<section class="blank-verso"></section>
<section class="half silent-page" id="halftitle">
  <p class="kicker">${esc(BOOK.kicker)}</p>
  <h1>${BOOK.titleLines[0]}<br/>${BOOK.titleLines[1]}</h1>
  <p class="ornament">— · —</p>
</section>
<section class="frontis silent-page" id="frontis">
  <img src="art/frontis.jpg" alt="${esc(BOOK.frontisAlt)}"/>
  <blockquote><p>${esc(FRONTIS_QUOTE)}</p><cite>— ${esc(FRONTIS_SIGN)}</cite></blockquote>
</section>
<section class="title silent-page" id="title">
  <p class="kicker">${esc(BOOK.titleKicker)}</p>
  <h1>${esc(BOOK.title)}</h1>
  <p class="sub">${esc(model.subtitle)}</p>
  <div class="title-gap"></div>
  ${blanks(["Author", "Publisher", "City"])}
</section>
<section class="copy page-front" id="copyright">
  <h1>Copyright</h1>
  <p class="small">Copyright ©</p>
  ${blanks(["Year", "Author"])}
  <p>${esc(COPYRIGHT[0])}</p>
  ${blanks(["Publisher", "Place of publication"])}
  <p class="small">First edition</p>
  ${blanks(["Year of publication", "ISBN", "Cataloguing-in-publication data"])}
  <p>${esc(COPYRIGHT[1])}</p>
  <p class="small">Illustrations made for this edition. Author, dedication, and publisher left blank to be filled in ink.</p>
  ${blanks(["Printed in"])}
</section>
<section class="dedi page-front" id="dedication">
  <h1>Dedication</h1>
  <p class="quiet">For</p>
  ${blanks(["Name", "And, if you like, a line", "And one more"])}
</section>
<section class="praise page-flow" id="praise">
  <h1>${esc(BOOK.praiseTitle)}</h1>
  <p class="note">Stand-in notices, so the page has a shape. Cross them out. Put real readers here.</p>
  ${PRAISE.map((p) => `<blockquote><p>${esc(p.quote)}</p><cite>— ${esc(p.sign)}</cite></blockquote>`).join("\n")}
</section>
<section class="contents page-flow" id="contents">
  <h1>Contents</h1>
  ${tocHtml(model, folios)}
</section>
<section class="plates page-flow" id="plates">
  <h1>List of plates</h1>
  <ol class="plate-list">
    ${model.chapters.map((ch) => `<li><span>${esc(ch.caption)}</span></li>`).join("\n")}
  </ol>
</section>
<section class="matter page-recto" id="foreword">
  <h1>Foreword</h1>
  <div class="prose">${model.foreword}</div>
  <p class="quiet sign-label">The foreword writer signs here.</p>
  ${blanks(["Name", "Place and date"])}
</section>
<section class="matter page-flow" id="preface">
  <h1>A note on the drafts</h1>
  <div class="prose">${model.preface}</div>
</section>
${chapters}
<section class="matter page-recto" id="afterword">
  <h1>Afterword</h1>
  <div class="prose">${model.afterword}</div>
  ${blanks(["Author", "Place and date"])}
</section>
<section class="matter page-flow" id="ack">
  <h1>Acknowledgments</h1>
  <p>The author wishes to thank</p>
  ${blanks(["Name", "Name", "Name"])}
  <p class="quiet">${esc(BOOK.ackNote)}</p>
</section>
<section class="matter page-flow" id="author">
  <h1>About the author</h1>
  ${blanks(["Name"])}
  <p class="quiet">was born in</p>
  ${blanks(["Place"])}
  <p class="quiet">Two or three sentences of biography. Leave this until you are ready to sign the book.</p>
  ${blanks(["A line", "Another", "They live in"])}
</section>
<section class="matter page-recto" id="soon">
  <h1>Also forthcoming</h1>
  <p class="quiet">from</p>
  ${blanks(["Publisher"])}
  <p class="note">Placeholder titles, so the page has the right furniture. Replace them with the real list.</p>
  ${COMING.map((b) => `<h2>${esc(b.title)}</h2><p>${esc(b.blurb)}</p>`).join("\n")}
</section>
<section class="matter page-flow" id="colophon">
  <h1>Colophon</h1>
  ${COLOPHON.map((p) => `<p>${esc(p)}</p>`).join("\n")}
  ${blanks(["Publisher", "City"])}
</section>
</body>
</html>`;
}

function printCss() {
  const face = (family, file, weight, style) => {
    const rel = `../../../node_modules/@fontsource/${file}`;
    const abs = path.join(ROOT, "node_modules/@fontsource", file);
    if (!fs.existsSync(abs)) throw new Error(`Missing font ${file}`);
    return `@font-face{font-family:${family};src:url("${rel}") format("woff");font-weight:${weight};font-style:${style};font-display:swap;}`;
  };
  return `
${face("Fraunces", "fraunces/files/fraunces-latin-600-normal.woff", 600, "normal")}
${face("Fraunces", "fraunces/files/fraunces-latin-700-normal.woff", 700, "normal")}
${face("Fraunces", "fraunces/files/fraunces-latin-500-italic.woff", 500, "italic")}
${face("Literata", "literata/files/literata-latin-400-normal.woff", 400, "normal")}
${face("Literata", "literata/files/literata-latin-400-italic.woff", 400, "italic")}
${face("Literata", "literata/files/literata-latin-700-normal.woff", 700, "normal")}
${face("Literata", "literata/files/literata-latin-700-italic.woff", 700, "italic")}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: Literata, Palatino, serif; font-size: 10.5pt; line-height: 1.45; color: #1c1712; }
@page { size: 6in 9in; margin: 0.68in 0.66in 0.7in 0.66in;
  @top-center { content: "${BOOK.runningHead}"; font-family: Fraunces, serif; font-size: 8pt; letter-spacing: 0.16em; color: #8a7d6b; }
  @bottom-center { content: counter(page); font-family: Literata, serif; font-size: 9pt; color: #4e463c; }
}
@page :first { margin: 0; @top-center { content: none; } @bottom-center { content: none; } }
@page silent { margin: 0.75in 0.7in; @top-center { content: none; } @bottom-center { content: none; } }
.coverpage { width: 6in; height: 9in; display: flex; flex-direction: column; background: #f3ead8; break-after: page; }
.cover-art { flex: 1; background: url("art/cover.jpg") center 28% / cover no-repeat; }
.cover-band { height: 1.72in; padding: 0.22in 0.42in 0.28in; background: #f3ead8; color: #1c1712; }
.cover-band .kicker, .kicker { font-family: Fraunces, serif; letter-spacing: 0.18em; text-transform: uppercase; font-size: 8.5pt; color: #8c3014; margin: 0 0 0.15in; }
.cover-band h1 { font-family: Fraunces, serif; font-weight: 600; font-size: 32pt; line-height: 0.9; margin: 0; }
.cover-band .sub { font-family: Fraunces, serif; font-style: italic; font-weight: 500; font-size: 12pt; margin: 0.12in 0 0; color: #3e4a32; }
h1 { font-family: Fraunces, serif; font-weight: 600; font-size: 22pt; line-height: 1.12; margin: 0 0 0.35em; }
h2 { font-family: Fraunces, serif; font-weight: 600; font-size: 13.5pt; line-height: 1.25; margin: 1.15em 0 0.3em; break-after: avoid; }
h3 { font-family: Fraunces, serif; font-weight: 500; font-size: 12pt; margin: 1em 0 0.25em; break-after: avoid; }
p { margin: 0.45em 0; orphans: 3; widows: 3; hyphens: auto; }
.label { font-family: Fraunces, serif; letter-spacing: 0.16em; text-transform: uppercase; font-size: 9pt; color: #8c3014; margin: 0 0 0.2em; }
.blank-verso { height: 1in; break-after: page; page: silent; }
.half, .frontis, .title { page: silent; break-after: page; }
.half { padding-top: 2.4in; }
.half h1 { font-size: 36pt; line-height: 0.92; }
.ornament { text-align: center; letter-spacing: 0.4em; color: #8c3014; margin-top: 0.6in; }
.frontis img { width: 3.5in; display: block; margin: 0.3in auto 0.35in; }
.frontis blockquote, blockquote { margin: 0.6em 0 0.8em; padding: 0; border: 0; }
blockquote p { font-family: Fraunces, serif; font-style: italic; font-weight: 500; font-size: 13pt; line-height: 1.35; }
cite { display: block; margin-top: 0.35em; font-style: normal; font-size: 9.5pt; color: #4e463c; }
.title { padding-top: 1.5in; }
.title h1 { font-size: 28pt; }
.title .sub { font-family: Fraunces, serif; font-style: italic; font-size: 14pt; color: #3e4a32; }
.title-gap { height: 0.8in; }
.blank { border-bottom: 1px solid #1c1712; margin: 0.85em 0 0.15em; min-height: 1.15em; position: relative; break-inside: avoid; }
.blank span { position: absolute; top: -0.15em; font-family: Fraunces, serif; font-size: 8pt; letter-spacing: 0.14em; text-transform: uppercase; color: #8a7d6b; }
.quiet, .note, .small { color: #4e463c; }
.note { font-style: italic; }
.copy h1, .dedi h1 { font-size: 18pt; }
.page-front { break-before: page; }
.page-flow { break-before: page; }
.page-recto { break-before: right; }
.dedi { break-before: right; padding-top: 1.4in; }
.toc-part { font-family: Fraunces, serif; font-weight: 600; margin: 0.85em 0 0.2em; font-size: 11pt; }
.toc-row { display: flex; align-items: baseline; gap: 0.35em; text-decoration: none; color: inherit; margin: 0.12em 0; break-inside: avoid; }
.toc-n { width: 1.5em; font-variant-numeric: tabular-nums; color: #8c3014; }
.toc-dots { flex: 1; border-bottom: 1px dotted #b7aa94; transform: translateY(-0.18em); min-width: 0.8em; }
.pg { min-width: 1.5em; text-align: right; font-variant-numeric: tabular-nums; }
.plate-list { padding-left: 1.2em; }
.plate-list li { margin: 0.2em 0; }
.part { page: silent; break-before: right; break-after: page; height: 7.4in; position: relative; }
.part-inner { position: absolute; left: 0; right: 0; bottom: 0.4in; }
.part h1 { font-size: 28pt; }
.part .blurb { font-family: Fraunces, serif; font-style: italic; font-weight: 500; font-size: 13pt; }
.chapter { break-before: page; }
.plate { margin: 0.2em 0 0.8em; break-inside: avoid; }
.plate img { width: 100%; height: auto; display: block; }
figcaption { font-family: Fraunces, serif; font-style: italic; font-weight: 500; font-size: 9.5pt; color: #4e463c; margin-top: 0.28em; }
.prose ul, .prose ol { padding-left: 1.15em; margin: 0.4em 0; }
.prose li { margin: 0.18em 0; }
.prose strong { font-weight: 700; }
.prose em { font-style: italic; }
.lede::first-letter { font-family: Fraunces, serif; font-weight: 600; float: left; font-size: 2.7em; line-height: 0.8; padding-right: 0.06em; color: #8c3014; }
.table-wrap { break-inside: avoid; margin: 0.6em 0 0.8em; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; line-height: 1.35; }
th { font-family: Fraunces, serif; font-weight: 600; text-align: left; border-bottom: 1px solid #1c1712; padding: 0.25em 0.45em 0.25em 0; }
td { border-bottom: 1px solid #d2c4aa; padding: 0.28em 0.45em 0.28em 0; vertical-align: top; }
.math { font-family: Fraunces, serif; white-space: nowrap; }
.math.display { display: block; text-align: center; margin: 0.7em 0; white-space: normal; }
.frac { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.92em; line-height: 1.05; margin: 0 0.15em; }
.frac .num { border-bottom: 1px solid currentColor; padding: 0 0.2em 0.04em; }
.frac .den { padding: 0.04em 0.2em 0; }
.sup, .sub { font-size: 0.7em; line-height: 0; }
.sup { vertical-align: super; }
.sub { vertical-align: sub; }
.sqrt .rad { border-top: 1px solid currentColor; padding: 0 0.12em; }
.tex-text { font-family: Literata, serif; font-style: normal; font-size: 0.92em; }
pre { font-family: ui-monospace, monospace; font-size: 8.5pt; line-height: 1.35; background: #e7dcc6; padding: 0.45em 0.55em; white-space: pre-wrap; break-inside: avoid; }
code { font-family: ui-monospace, monospace; font-size: 0.92em; }
`;
}

function stripStreams(s) {
  let out = "";
  let i = 0;
  while (i < s.length) {
    const start = s.indexOf("stream", i);
    if (start === -1) {
      out += s.slice(i);
      break;
    }
    out += s.slice(i, start);
    const end = s.indexOf("endstream", start + 6);
    if (end === -1) break;
    out += "stream\nendstream";
    i = end + "endstream".length;
  }
  return out;
}

function destPages(buf) {
  const stripped = stripStreams(buf.toString("latin1"));
  const hits = [];
  const re = /(\d+)\s+0\s+obj/g;
  let m;
  while ((m = re.exec(stripped))) hits.push({ n: m[1], at: m.index, bodyAt: re.lastIndex });
  const objs = new Map();
  for (let i = 0; i < hits.length; i++) {
    const end = stripped.indexOf("endobj", hits[i].bodyAt);
    const next = i + 1 < hits.length ? hits[i + 1].at : stripped.length;
    const stop = end === -1 || end > next ? next : end;
    objs.set(hits[i].n, stripped.slice(hits[i].bodyAt, stop));
  }
  let pagesRoot = null;
  for (const [id, body] of objs) {
    if (/\/Type\s*\/Catalog/.test(body)) {
      const pm = body.match(/\/Pages\s+(\d+)\s+0\s+R/);
      if (pm) pagesRoot = pm[1];
    }
  }
  const order = [];
  const walk = (id, guard) => {
    if (!id || guard.has(id)) return;
    guard.add(id);
    const body = objs.get(id) || "";
    if (/\/Type\s*\/Page(?!s)/.test(body)) {
      order.push(id);
      return;
    }
    const km = body.match(/\/Kids\s*\[([^\]]*)\]/);
    if (!km) return;
    for (const ref of km[1].matchAll(/(\d+)\s+0\s+R/g)) walk(ref[1], guard);
  };
  if (pagesRoot) walk(pagesRoot, new Set());
  const indexOf = new Map(order.map((id, i) => [id, i + 1]));
  const folios = {};
  const nameRe = /\/(ch\d{2}|part\d+|foreword|preface|afterword|contents|plates|praise|ack|author|soon|colophon|copyright|dedication|halftitle|frontis|title)\s*\[\s*(\d+)\s+0\s+R/g;
  let dm;
  while ((dm = nameRe.exec(stripped))) {
    const page = indexOf.get(dm[2]);
    if (page) folios[dm[1]] = page;
  }
  return folios;
}

async function printPdf(htmlPath, outPath) {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch({ args: ["--no-sandbox", "--disable-dev-shm-usage"] });
  const page = await browser.newPage();
  await page.goto(`file://${htmlPath}`, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: outPath,
    printBackground: true,
    preferCSSPageSize: true,
    outline: true,
    tagged: true,
  });
  await browser.close();
}

function asXml(html) {
  return html
    .replace(/&nbsp;/g, "&#160;")
    .replace(/<br\s*\/?>/g, "<br/>")
    .replace(/<hr\s*\/?>/g, "<hr/>")
    .replace(/<img\b([^>]*?)\/?>/g, (_, attrs) => `<img${attrs.replace(/\s*\/\s*$/, "")}/>`);
}

function xhtmlDoc(title, body, cssHref) {
  return `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
<meta charset="utf-8"/>
<title>${esc(title)}</title>
<link rel="stylesheet" type="text/css" href="${cssHref}"/>
</head>
<body>
${body}
</body>
</html>`;
}

function buildEpub(model) {
  const work = path.join(ROOT, "book/epub");
  fs.rmSync(work, { recursive: true, force: true });
  const oebps = path.join(work, "OEBPS");
  const imgDir = path.join(oebps, "images");
  const fontDir = path.join(oebps, "fonts");
  fs.mkdirSync(imgDir, { recursive: true });
  fs.mkdirSync(fontDir, { recursive: true });
  fs.mkdirSync(path.join(work, "META-INF"), { recursive: true });
  fs.writeFileSync(path.join(work, "mimetype"), "application/epub+zip");
  fs.writeFileSync(
    path.join(work, "META-INF/container.xml"),
    `<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>`,
  );

  const fontFiles = [
    "fraunces/files/fraunces-latin-600-normal.woff",
    "fraunces/files/fraunces-latin-500-italic.woff",
    "literata/files/literata-latin-400-normal.woff",
    "literata/files/literata-latin-400-italic.woff",
    "literata/files/literata-latin-700-normal.woff",
  ];
  for (const rel of fontFiles) {
    const base = path.basename(rel);
    fs.copyFileSync(path.join(ROOT, "node_modules/@fontsource", rel), path.join(fontDir, base));
  }
  fs.copyFileSync(path.join(ART, "cover.jpg"), path.join(imgDir, "cover.jpg"));
  fs.copyFileSync(path.join(ART, "frontis.jpg"), path.join(imgDir, "frontis.jpg"));
  for (const ch of model.chapters) {
    fs.copyFileSync(path.join(ART, `${ch.id}.jpg`), path.join(imgDir, `${ch.id}.jpg`));
  }

  const css = `body{font-family:Literata,Palatino,serif;line-height:1.5;color:#1c1712;background:#f3ead8;margin:0;padding:1.2rem;}
h1{font-family:Fraunces,Palatino,serif;font-weight:600;line-height:1.15;}
h2,h3{font-family:Fraunces,Palatino,serif;line-height:1.25;}
.label,.kicker{font-family:Fraunces,serif;letter-spacing:.16em;text-transform:uppercase;color:#8c3014;font-size:.8rem;}
img{max-width:100%;height:auto;}
figcaption,cite{font-family:Fraunces,serif;font-style:italic;color:#4e463c;}
blockquote p{font-family:Fraunces,serif;font-style:italic;font-size:1.15rem;}
.blank{border-bottom:1px solid #1c1712;min-height:1.4rem;margin:1rem 0 .2rem;position:relative;}
.blank span{position:absolute;top:-.4rem;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:#8a7d6b;font-family:Fraunces,serif;}
table{width:100%;border-collapse:collapse;font-size:.92em;}
th,td{text-align:left;vertical-align:top;padding:.3em .4em .3em 0;border-bottom:1px solid #d2c4aa;}
.lede::first-letter{font-family:Fraunces,serif;font-weight:600;float:left;font-size:3em;line-height:.8;padding-right:.06em;color:#8c3014;}
.math.display{display:block;text-align:center;margin:.8em 0;}
.frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.9em;line-height:1.05;margin:0 .12em;}
.frac .num{border-bottom:1px solid currentColor;padding:0 .2em .04em;}
.frac .den{padding:.04em .2em 0;}
.sup,.sub{font-size:.72em;line-height:0;}
.sup{vertical-align:super;}.sub{vertical-align:sub;}
@font-face{font-family:Fraunces;src:url("fonts/fraunces-latin-600-normal.woff") format("woff");font-weight:600;}
@font-face{font-family:Fraunces;src:url("fonts/fraunces-latin-500-italic.woff") format("woff");font-weight:500;font-style:italic;}
@font-face{font-family:Literata;src:url("fonts/literata-latin-400-normal.woff") format("woff");font-weight:400;}
@font-face{font-family:Literata;src:url("fonts/literata-latin-400-italic.woff") format("woff");font-weight:400;font-style:italic;}
@font-face{font-family:Literata;src:url("fonts/literata-latin-700-normal.woff") format("woff");font-weight:700;}
pre{font-family:ui-monospace,monospace;font-size:.85em;line-height:1.4;background:#e7dcc6;padding:.6em .7em;white-space:pre-wrap;}
code{font-family:ui-monospace,monospace;}`;
  fs.writeFileSync(path.join(oebps, "style.css"), css);

  const docs = [];
  const add = (href, title, body) => {
    fs.writeFileSync(path.join(oebps, href), xhtmlDoc(title, asXml(body), "style.css"));
    docs.push({ href, title, id: href.replace(".xhtml", "") });
  };

  add(
    "cover.xhtml",
    "Cover",
    `<section class="cover"><p class="kicker">${esc(BOOK.kicker)}</p><h1>${esc(BOOK.title)}</h1><p>${esc(BOOK.subtitle)}</p><img src="images/cover.jpg" alt="${esc(BOOK.coverAlt || "Cover illustration")}"/></section>`,
  );
  add(
    "halftitle.xhtml",
    "Half title",
    `<section><p class="kicker">${esc(BOOK.kicker)}</p><h1>${esc(BOOK.title)}</h1></section>`,
  );
  add(
    "frontis.xhtml",
    "Frontispiece",
    `<section><img src="images/frontis.jpg" alt="${esc(BOOK.frontisAlt)}"/><blockquote><p>${esc(FRONTIS_QUOTE)}</p><cite>— ${esc(FRONTIS_SIGN)}</cite></blockquote></section>`,
  );
  add(
    "title.xhtml",
    "Title page",
    `<section><p class="kicker">${esc(BOOK.titleKicker)}</p><h1>${esc(BOOK.title)}</h1><p><em>${esc(model.subtitle)}</em></p>${blanks(["Author", "Publisher", "City"])}</section>`,
  );
  add(
    "copyright.xhtml",
    "Copyright",
    `<section><h1>Copyright</h1><p>Copyright ©</p>${blanks(["Year", "Author"])}<p>${esc(COPYRIGHT[0])}</p>${blanks(["Publisher", "Place of publication", "ISBN"])}<p>${esc(COPYRIGHT[1])}</p><p>The author, dedication, and publisher are left blank on purpose.</p></section>`,
  );
  add(
    "dedication.xhtml",
    "Dedication",
    `<section><h1>Dedication</h1><p>For</p>${blanks(["Name", "A line", "Another"])}</section>`,
  );
  add(
    "praise.xhtml",
    BOOK.praiseTitle,
    `<section><h1>${esc(BOOK.praiseTitle)}</h1><p><em>Stand-in notices, so the page has a shape. Cross them out. Put real readers here.</em></p>${PRAISE.map((p) => `<blockquote><p>${esc(p.quote)}</p><cite>— ${esc(p.sign)}</cite></blockquote>`).join("")}</section>`,
  );
  add("foreword.xhtml", "Foreword", `<section><h1>Foreword</h1><div class="prose">${model.foreword}</div>${blanks(["Name", "Place and date"])}</section>`);
  add("preface.xhtml", "A note on the drafts", `<section><h1>A note on the drafts</h1><div class="prose">${model.preface}</div></section>`);

  for (const part of PARTS) {
    add(
      `part${part.id}.xhtml`,
      `Part ${part.numeral}. ${part.title}`,
      `<section><p class="label">Part ${esc(part.numeral)}</p><h1>${esc(part.title)}</h1><p><em>${esc(part.blurb)}</em></p></section>`,
    );
    for (const n of part.chapters) {
      const ch = model.chapters[n - 1];
      add(
        `${ch.id}.xhtml`,
        `Chapter ${ch.n}. ${ch.title}`,
        `<section><p class="label">Chapter ${ch.n}</p><h1>${esc(ch.title)}</h1><figure><img src="images/${ch.id}.jpg" alt="${esc(ch.caption)}"/><figcaption>${esc(ch.caption)}</figcaption></figure><div class="prose">${ch.html}</div></section>`,
      );
    }
  }
  add("afterword.xhtml", "Afterword", `<section><h1>Afterword</h1><div class="prose">${model.afterword}</div>${blanks(["Author", "Place and date"])}</section>`);
  add("ack.xhtml", "Acknowledgments", `<section><h1>Acknowledgments</h1><p>The author wishes to thank</p>${blanks(["Name", "Name", "Name"])}<p>${esc(BOOK.ackNote)}</p></section>`);
  add("author.xhtml", "About the author", `<section><h1>About the author</h1>${blanks(["Name", "Born in", "A line of biography", "They live in"])}</section>`);
  add(
    "soon.xhtml",
    "Also forthcoming",
    `<section><h1>Also forthcoming</h1><p>from</p>${blanks(["Publisher"])}<p><em>Placeholder titles. Replace them with the real list.</em></p>${COMING.map((b) => `<h2>${esc(b.title)}</h2><p>${esc(b.blurb)}</p>`).join("")}</section>`,
  );
  add(
    "colophon.xhtml",
    "Colophon",
    `<section><h1>Colophon</h1>${COLOPHON.map((p) => `<p>${esc(p)}</p>`).join("")}${blanks(["Publisher", "City"])}</section>`,
  );

  const navItems = docs
    .filter((d) => !["cover", "halftitle", "frontis", "title", "copyright", "dedication", "praise"].includes(d.id) && !d.id.startsWith("part"))
    .map((d) => `<li><a href="${d.href}">${esc(d.title)}</a></li>`)
    .join("\n");
  const partNav = PARTS.map((part) => {
    const kids = part.chapters
      .map((n) => {
        const ch = model.chapters[n - 1];
        return `<li><a href="${ch.id}.xhtml">Chapter ${ch.n}. ${esc(ch.title)}</a></li>`;
      })
      .join("");
    return `<li><a href="part${part.id}.xhtml">Part ${esc(part.numeral)}. ${esc(part.title)}</a><ol>${kids}</ol></li>`;
  }).join("");
  fs.writeFileSync(
    path.join(oebps, "nav.xhtml"),
    xhtmlDoc(
      "Contents",
      `<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>
<li><a href="foreword.xhtml">Foreword</a></li>
<li><a href="preface.xhtml">A note on the drafts</a></li>
${partNav}
<li><a href="afterword.xhtml">Afterword</a></li>
<li><a href="ack.xhtml">Acknowledgments</a></li>
<li><a href="author.xhtml">About the author</a></li>
<li><a href="soon.xhtml">Also forthcoming</a></li>
<li><a href="colophon.xhtml">Colophon</a></li>
</ol></nav>`,
      "style.css",
    ),
  );

  const manifest = [
    `<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>`,
    `<item id="css" href="style.css" media-type="text/css"/>`,
    `<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>`,
    `<item id="img-frontis" href="images/frontis.jpg" media-type="image/jpeg"/>`,
    ...model.chapters.map((ch) => `<item id="img-${ch.id}" href="images/${ch.id}.jpg" media-type="image/jpeg"/>`),
    ...fontFiles.map((rel) => {
      const base = path.basename(rel);
      return `<item id="font-${base.replace(/\W/g, "")}" href="fonts/${base}" media-type="font/woff"/>`;
    }),
    ...docs.map((d) => `<item id="${d.id}" href="${d.href}" media-type="application/xhtml+xml"/>`),
  ].join("\n");
  const spine = ["cover", ...docs.filter((d) => d.id !== "cover").map((d) => d.id)]
    .map((id) => `<itemref idref="${id}"/>`)
    .join("\n");

  fs.writeFileSync(
    path.join(oebps, "content.opf"),
    `<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid" version="3.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">${BOOK.uuid}</dc:identifier>
<dc:title>${esc(BOOK.title)}: ${esc(BOOK.subtitle)}</dc:title>
<dc:language>en</dc:language>
<dc:creator>[Author]</dc:creator>
<dc:publisher>[Publisher]</dc:publisher>
<dc:description>${esc(BOOK.description)}</dc:description>
<meta property="dcterms:modified">${new Date().toISOString().replace(/\.\d+Z$/, "Z")}</meta>
</metadata>
<manifest>
${manifest}
</manifest>
<spine>
${spine}
</spine>
</package>`,
  );

  // nav.xhtml was not in docs; include it only in manifest (already). Spine shouldn't repeat nav.
  void navItems;
  const py = `
import os, zipfile
root = ${JSON.stringify(work)}
out = ${JSON.stringify(EPUB_OUT)}
os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, "w") as z:
    z.write(os.path.join(root, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
    for dirpath, dirs, files in os.walk(root):
        for name in files:
            if name == "mimetype" and dirpath == root:
                continue
            full = os.path.join(dirpath, name)
            arc = os.path.relpath(full, root).replace(os.sep, "/")
            z.write(full, arc, compress_type=zipfile.ZIP_DEFLATED)
print(os.path.getsize(out))
`;
  const size = execFileSync("python3", ["-c", py], { encoding: "utf8" }).trim();
  console.log("epub bytes", size);
}

async function main() {
  fs.mkdirSync(path.dirname(JSON_OUT), { recursive: true });
  fs.mkdirSync(path.dirname(PDF_OUT), { recursive: true });
  const model = buildModel();
  if (CAPTIONS.length !== model.chapters.length + 1) throw new Error("caption count");
  fs.writeFileSync(JSON_OUT, JSON.stringify(model));
  console.log("json", model.chapters.map((c) => `${c.n}. ${c.title}`).join("\n"));
  if (process.argv.includes("--json")) return;

  fs.writeFileSync(PRINT_HTML, renderPrint(model, {}));
  const pass1 = path.join(ROOT, "book/pass1.pdf");
  fs.mkdirSync(path.dirname(pass1), { recursive: true });
  await printPdf(PRINT_HTML, pass1);
  const folios = destPages(fs.readFileSync(pass1));
  console.log("folios", Object.keys(folios).length, JSON.stringify(folios).slice(0, 500));
  model.folios = folios;
  fs.writeFileSync(JSON_OUT, JSON.stringify(model));
  fs.writeFileSync(PRINT_HTML, renderPrint(model, folios));
  await printPdf(PRINT_HTML, PDF_OUT);
  console.log("pdf", fs.statSync(PDF_OUT).size);
  buildEpub(model);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
