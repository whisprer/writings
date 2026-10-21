import { useEffect, useState } from "react";
import { Download, List, X } from "lucide-react";
import computers from "@/content/computers.json";
import engines from "@/content/engines.json";
import radio from "@/content/radio.json";
import water from "@/content/water.json";

type Chapter = {
  n: number;
  id: string;
  part: string;
  title: string;
  html: string;
  plate: string;
  caption: string;
};

type Part = { id: string; numeral: string; title: string; blurb: string };

type Book = {
  id: string;
  title: string;
  titleLines: string[];
  subtitle: string;
  kicker: string;
  volumeLabel: string;
  pdf: string;
  epub: string;
  cover: string;
  frontis: string;
  frontisAlt: string;
  praiseTitle: string;
  titleKicker: string;
  ackNote: string;
  copyright: string[];
  colophon: string[];
  frontisQuote: string;
  frontisSign: string;
  parts: Part[];
  chapters: Chapter[];
  foreword: string;
  preface: string;
  afterword: string;
  praise: { quote: string; sign: string }[];
  coming: { title: string; blurb: string }[];
  folios?: Record<string, number>;
};

const volumes = [water, engines, computers, radio] as Book[];

function Blank({ label }: { label: string }) {
  return (
    <p className="blank">
      <span>{label}</span>
    </p>
  );
}

function Folio({ book, id }: { book: Book; id: string }) {
  const n = book.folios?.[id];
  if (!n) return null;
  return <span className="folio">{n}</span>;
}

function CoverFace({ book }: { book: Book }) {
  return (
    <div className="cover-book">
      <div
        className="cover-art"
        role="img"
        aria-label={`${book.title} cover illustration`}
        style={{ backgroundImage: `url(${book.cover})` }}
      />
      <div className="cover-band">
        <p className="kicker">{book.kicker}</p>
        <h1>
          {book.titleLines[0]}
          <br />
          {book.titleLines[1]}
        </h1>
        <p className="sub">{book.subtitle}</p>
      </div>
    </div>
  );
}

export function Manual() {
  const [which, setWhich] = useState<string | null>("water");
  const [open, setOpen] = useState(false);
  const [toc, setToc] = useState(false);
  const [now, setNow] = useState("Half title");
  const [progress, setProgress] = useState(0);
  const data = volumes.find((v) => v.id === which) ?? null;

  useEffect(() => {
    if (window.location.hash) setOpen(true);
  }, []);

  useEffect(() => {
    if (!open) return;
    const nodes = Array.from(document.querySelectorAll<HTMLElement>("[data-spy]"));
    const io = new IntersectionObserver(
      (entries) => {
        const hit = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        const label = hit?.target.getAttribute("data-spy");
        if (label) setNow(label);
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: [0, 0.25, 0.6] },
    );
    nodes.forEach((n) => io.observe(n));
    return () => io.disconnect();
  }, [open, which]);

  useEffect(() => {
    if (!open) return;
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(max > 0 ? window.scrollY / max : 0);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [open, which]);

  const jump = (id: string) => {
    setToc(false);
    setOpen(true);
    requestAnimationFrame(() => {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  };

  const choose = (id: string) => {
    setWhich(id);
    setOpen(false);
    setToc(false);
    setNow("Half title");
    window.scrollTo(0, 0);
  };

  if (!data) {
    return (
      <main className="shelf">
        <div className="shelf-head">
          <p className="kicker">A field manual</p>
          <h1>Zombieproof</h1>
          <p>Four volumes. The blanks inside are for your pen.</p>
        </div>
        <div className="shelf-row">
          {volumes.map((book) => (
            <div key={book.id} className="shelf-book">
              <button type="button" onClick={() => choose(book.id)} aria-label={`Open ${book.title}`}>
                <CoverFace book={book} />
              </button>
              <div className="shelf-meta">
                <span>{book.volumeLabel}</span>
                <span className="shelf-links">
                  <a href={book.pdf} download>
                    PDF
                  </a>
                  <a href={book.epub} download>
                    EPUB
                  </a>
                </span>
              </div>
            </div>
          ))}
        </div>
      </main>
    );
  }

  if (!open) {
    return (
      <main className="gate">
        <CoverFace book={data} />
        <div className="gate-actions">
          <button className="open-btn" type="button" onClick={() => setOpen(true)}>
            Open the manual
          </button>
          <div className="file-row">
            <a href={data.pdf} download>
              <Download size={16} aria-hidden /> PDF
            </a>
            <a href={data.epub} download>
              <Download size={16} aria-hidden /> EPUB
            </a>
          </div>
          <button className="word shelf-back" type="button" onClick={() => setWhich(null)}>
            {data.volumeLabel} · The shelf
          </button>
          <p className="fine">Author, dedication, and publisher are blank inside, on purpose.</p>
        </div>
      </main>
    );
  }

  return (
    <div className="manual">
      <header className="bar">
        <button className="word" type="button" onClick={() => setOpen(false)}>
          {data.title}
        </button>
        <p className="now">{now}</p>
        <div className="bar-actions">
          <button type="button" onClick={() => setToc(true)}>
            <List size={16} aria-hidden /> Contents
          </button>
          <a className="icon-btn" href={data.pdf} download>
            PDF
          </a>
          <a className="icon-btn" href={data.epub} download>
            EPUB
          </a>
        </div>
      </header>
      <div className="progress" aria-hidden>
        <span style={{ width: `${Math.round(progress * 100)}%` }} />
      </div>
      {toc ? (
        <>
          <button className="drawer-back" type="button" aria-label="Close contents" onClick={() => setToc(false)} />
          <nav className="drawer toc" aria-label="Contents">
            <header>
              <h2>Contents</h2>
              <button className="toc-close" type="button" onClick={() => setToc(false)} aria-label="Close">
                <X size={18} />
              </button>
            </header>
            <button type="button" onClick={() => jump("foreword")}>
              Foreword <Folio book={data} id="foreword" />
            </button>
            <button type="button" onClick={() => jump("preface")}>
              A note on the drafts <Folio book={data} id="preface" />
            </button>
            {data.parts.map((part) => (
              <div key={part.id}>
                <p className="part-line">
                  Part {part.numeral} · {part.title}
                </p>
                {data.chapters
                  .filter((ch) => ch.part === part.id)
                  .map((ch) => (
                    <button key={ch.id} type="button" onClick={() => jump(ch.id)}>
                      <span className="num">{ch.n}</span>
                      <span>{ch.title}</span>
                      <Folio book={data} id={ch.id} />
                    </button>
                  ))}
              </div>
            ))}
            <button type="button" onClick={() => jump("afterword")}>
              Afterword
            </button>
            <button type="button" onClick={() => jump("soon")}>
              Also forthcoming
            </button>
          </nav>
        </>
      ) : null}

      <article className="sheet">
        <section className="half" id="halftitle" data-spy="Half title">
          <p className="kicker">{data.kicker}</p>
          <h1>
            {data.titleLines[0]}
            <br />
            {data.titleLines[1]}
          </h1>
        </section>
        <hr className="rule" />
        <section className="frontis" id="frontis" data-spy="Frontispiece">
          <img src={data.frontis} alt={data.frontisAlt} />
          <blockquote>
            <p>{data.frontisQuote}</p>
            <cite>— {data.frontisSign}</cite>
          </blockquote>
        </section>
        <hr className="rule" />
        <section id="title" data-spy="Title page">
          <p className="kicker">{data.titleKicker}</p>
          <h1>{data.title}</h1>
          <p className="note">{data.subtitle}</p>
          <Blank label="Author" />
          <Blank label="Publisher" />
          <Blank label="City" />
        </section>
        <hr className="rule" />
        <section id="copyright" data-spy="Copyright">
          <h1>Copyright</h1>
          <p>Copyright ©</p>
          <Blank label="Year" />
          <Blank label="Author" />
          {data.copyright.map((paragraph) => (
            <p key={paragraph.slice(0, 24)}>{paragraph}</p>
          ))}
          <Blank label="Publisher" />
          <Blank label="Place of publication" />
          <p>First edition</p>
          <Blank label="Year of publication" />
          <Blank label="ISBN" />
          <p className="note">Illustrations made for this edition. The blanks above are for your pen.</p>
        </section>
        <hr className="rule" />
        <section id="dedication" data-spy="Dedication">
          <h1>Dedication</h1>
          <p>For</p>
          <Blank label="Name" />
          <Blank label="And, if you like, a line" />
          <Blank label="And one more" />
        </section>
        <hr className="rule" />
        <section id="praise" data-spy="Early word">
          <h1>{data.praiseTitle}</h1>
          <p className="note">Stand-in notices, so the page has a shape. Cross them out. Put real readers here.</p>
          <div className="praise-list">
            {data.praise.map((p) => (
              <blockquote key={p.sign}>
                <p>{p.quote}</p>
                <cite>— {p.sign}</cite>
              </blockquote>
            ))}
          </div>
        </section>
        <hr className="rule" />
        <section className="toc" id="contents" data-spy="Contents">
          <h1>Contents</h1>
          <button type="button" onClick={() => jump("foreword")}>
            Foreword <Folio book={data} id="foreword" />
          </button>
          <button type="button" onClick={() => jump("preface")}>
            A note on the drafts <Folio book={data} id="preface" />
          </button>
          {data.parts.map((part) => (
            <div key={part.id}>
              <p className="part-line">
                Part {part.numeral} · {part.title}
              </p>
              {data.chapters
                .filter((ch) => ch.part === part.id)
                .map((ch) => (
                  <button key={ch.id} type="button" onClick={() => jump(ch.id)}>
                    <span className="num">{ch.n}</span>
                    <span>{ch.title}</span>
                    <Folio book={data} id={ch.id} />
                  </button>
                ))}
            </div>
          ))}
        </section>
        <hr className="rule" />
        <section id="foreword" data-spy="Foreword">
          <h1>Foreword</h1>
          <div className="prose" dangerouslySetInnerHTML={{ __html: data.foreword }} />
          <p className="note">The foreword writer signs here.</p>
          <Blank label="Name" />
          <Blank label="Place and date" />
        </section>
        <hr className="rule" />
        <section id="preface" data-spy="A note on the drafts">
          <h1>A note on the drafts</h1>
          <div className="prose" dangerouslySetInnerHTML={{ __html: data.preface }} />
        </section>

        {data.parts.map((part) => (
          <div key={part.id}>
            <section className="part-open" id={`part${part.id}`} data-spy={`Part ${part.numeral}`}>
              <p className="label">Part {part.numeral}</p>
              <h2>{part.title}</h2>
              <p className="blurb">{part.blurb}</p>
            </section>
            {data.chapters
              .filter((ch) => ch.part === part.id)
              .map((ch) => (
                <article key={ch.id} id={ch.id} data-spy={`Chapter ${ch.n}`}>
                  <hr className="rule" />
                  <p className="label">Chapter {ch.n}</p>
                  <h1>{ch.title}</h1>
                  <figure className="plate">
                    <img src={ch.plate} alt={ch.caption} />
                    <figcaption>{ch.caption}</figcaption>
                  </figure>
                  <div className="prose" dangerouslySetInnerHTML={{ __html: ch.html }} />
                </article>
              ))}
          </div>
        ))}

        <hr className="rule" />
        <section id="afterword" data-spy="Afterword">
          <h1>Afterword</h1>
          <div className="prose" dangerouslySetInnerHTML={{ __html: data.afterword }} />
          <Blank label="Author" />
          <Blank label="Place and date" />
        </section>
        <hr className="rule" />
        <section id="ack" data-spy="Acknowledgments">
          <h1>Acknowledgments</h1>
          <p>The author wishes to thank</p>
          <Blank label="Name" />
          <Blank label="Name" />
          <Blank label="Name" />
          <p className="note">{data.ackNote}</p>
        </section>
        <hr className="rule" />
        <section id="author" data-spy="About the author">
          <h1>About the author</h1>
          <Blank label="Name" />
          <p>was born in</p>
          <Blank label="Place" />
          <p className="note">Two or three sentences, when you are ready to sign the book.</p>
          <Blank label="A line" />
          <Blank label="They live in" />
        </section>
        <hr className="rule" />
        <section className="matter" id="soon" data-spy="Also forthcoming">
          <h1>Also forthcoming</h1>
          <p>from</p>
          <Blank label="Publisher" />
          <p className="note">Placeholder titles, so the page has the right furniture. Replace them with the real list.</p>
          {data.coming.map((item) => (
            <div key={item.title}>
              <h2>{item.title}</h2>
              <p>{item.blurb}</p>
            </div>
          ))}
        </section>
        <hr className="rule" />
        <section id="colophon" data-spy="Colophon">
          <h1>Colophon</h1>
          {data.colophon.map((paragraph) => (
            <p key={paragraph.slice(0, 24)}>{paragraph}</p>
          ))}
          <Blank label="Publisher" />
          <Blank label="City" />
        </section>
      </article>
    </div>
  );
}
