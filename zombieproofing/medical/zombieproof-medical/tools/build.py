#!/usr/bin/env python3
"""Build the complete 6x9 PDF, EPUB 3, HTML and Markdown from local sources.

Python 3.12+; no network, accounts, API keys or external executables required.
All clinical content is in manuscript/*.md; review status is in book.json.
"""
from __future__ import annotations
import argparse
import html
import json
import re
import shutil
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from lxml import html as LH
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, Image, KeepTogether, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
PAPER = colors.HexColor('#f3ead8')
INK = colors.HexColor('#1c1712')
RUST = colors.HexColor('#8c3014')
OLIVE = colors.HexColor('#3e4a32')
MUTED = colors.HexColor('#655d50')
RULE = colors.HexColor('#d2c4aa')
WIDTH, HEIGHT = 6*inch, 9*inch
MARGIN = .66*inch
TEXT = WIDTH-2*MARGIN
REFS = json.loads((ROOT/'references.json').read_text(encoding='utf-8'))
META = json.loads((ROOT/'book.json').read_text(encoding='utf-8'))
REF_IDS = {r['id'] for r in REFS}


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', s)
    return s


def md_html(s: str) -> str:
    """A small, explicit parser for this book's Markdown subset, not arbitrary HTML."""
    lines=s.splitlines(); result=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        m=re.match(r'^(#{1,3})\s+(.+)$',line)
        if m:
            n=len(m[1]);result.append(f'<h{n}>{inline(m[2])}</h{n}>');i+=1;continue
        if line.startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|\-]+\|$',lines[i+1].strip()):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in cells): rows.append(cells)
                i+=1
            table=['<table><thead><tr>']
            table += [f'<th>{inline(c)}</th>' for c in rows[0]]
            table += ['</tr></thead><tbody>']
            for row in rows[1:]:
                table+=['<tr>']+[f'<td>{"&#160;" if re.fullmatch(r"_+",c) else inline(c)}</td>' for c in row]+['</tr>']
            result.append(''.join(table)+'</tbody></table>');continue
        if line.startswith('> '):
            chunk=[]
            while i<len(lines) and lines[i].strip().startswith('> '):
                chunk.append(lines[i].strip()[2:]);i+=1
            result.append('<blockquote><p>'+inline(' '.join(chunk))+'</p></blockquote>');continue
        if re.match(r'^(?:- |\d+\. )',line):
            ordered=bool(re.match(r'^\d+\.',line));tag='ol' if ordered else 'ul';items=[]
            pattern=r'^\d+\.\s+' if ordered else r'^-\s+'
            while i<len(lines) and re.match(pattern,lines[i].strip()):
                items.append(re.sub(pattern,'',lines[i].strip()));i+=1
            result.append('<'+tag+'>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</'+tag+'>');continue
        chunk=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|>|\||- |\d+\. )',lines[i].strip()):
            chunk.append(lines[i].strip());i+=1
        result.append('<p>'+inline(' '.join(chunk))+'</p>')
    return '\n'.join(result)


def inner(node) -> str:
    return (html.escape(node.text or '',quote=False)+''.join(ET.tostring(x,encoding='unicode',method='xml') for x in node))


def register_fonts() -> None:
    fonts={
        'Literata':'literata-latin-400-normal.ttf',
        'Literata-Bold':'literata-latin-700-normal.ttf',
        'Literata-Italic':'literata-latin-400-italic.ttf',
        'Fraunces':'fraunces-latin-600-normal.ttf',
        'Fraunces-Italic':'fraunces-latin-500-italic.ttf',
    }
    for name,file in fonts.items(): pdfmetrics.registerFont(TTFont(name,str(ROOT/'fonts'/file)))
    pdfmetrics.registerFontFamily('Literata',normal='Literata',bold='Literata-Bold',italic='Literata-Italic',boldItalic='Literata-Bold')
    pdfmetrics.registerFontFamily('Fraunces',normal='Fraunces',bold='Fraunces',italic='Fraunces-Italic',boldItalic='Fraunces-Italic')


def styles() -> dict[str,ParagraphStyle]:
    base=dict(fontName='Literata',fontSize=10.15,leading=15.1,textColor=INK,spaceAfter=7.5,splitLongWords=True,allowWidows=0,allowOrphans=0)
    p=ParagraphStyle('Body',**base)
    out={'body':p}
    def add(name,**kw): out[name]=ParagraphStyle(name,parent=p,**kw)
    add('lede',fontSize=10.7,leading=16.1,spaceAfter=11)
    add('h1',fontName='Fraunces',fontSize=24,leading=27,spaceAfter=14,keepWithNext=True)
    add('h2',fontName='Fraunces',fontSize=13.5,leading=17,spaceBefore=12,spaceAfter=6,keepWithNext=True)
    add('h3',fontName='Fraunces',fontSize=11.8,leading=15.5,spaceBefore=9,spaceAfter=5,keepWithNext=True)
    add('kicker',fontName='Fraunces',fontSize=8.2,leading=12,textColor=RUST,spaceAfter=7,keepWithNext=True)
    add('caption',fontName='Fraunces-Italic',fontSize=9.1,leading=12.2,textColor=MUTED,spaceBefore=4,spaceAfter=14)
    add('list',leftIndent=13,firstLineIndent=-10,spaceAfter=6)
    add('quote',fontName='Fraunces',fontSize=10.7,leading=15.1,spaceAfter=0,textColor=OLIVE)
    add('table',fontSize=8.9,leading=12.2,spaceAfter=0,allowWidows=1,allowOrphans=1)
    add('th',fontName='Fraunces',fontSize=9.2,leading=12.1,spaceAfter=0,textColor=OLIVE)
    add('small',fontSize=8.7,leading=12.5,textColor=MUTED,spaceAfter=6)
    add('ref',fontSize=9.3,leading=13.3,spaceAfter=3)
    add('url',fontSize=7.8,leading=10.6,textColor=RUST,spaceAfter=11,wordWrap='CJK')
    add('part',fontName='Fraunces',fontSize=30,leading=34,textColor=INK,spaceAfter=18)
    add('partblurb',fontName='Fraunces-Italic',fontSize=14,leading=19,textColor=OLIVE)
    return out


class Heading(Paragraph):
    def __init__(self,text,style,key=None,level=0):
        super().__init__(text,style);self.key=key;self.toclevel=level;self.plain=re.sub('<[^>]*>','',text)


class Cover(Flowable):
    def __init__(self):
        super().__init__()
        self.width=WIDTH
        self.height=HEIGHT-.1
    def draw(self):
        c=self.canv
        c.setFillColor(PAPER);c.rect(0,0,WIDTH,HEIGHT,stroke=0,fill=1)
        c.saveState();path=c.beginPath();path.rect(0,147,WIDTH,HEIGHT-147);c.clipPath(path,stroke=0,fill=0)
        c.drawImage(str(ROOT/'art'/'cover.jpg'),0,0,width=WIDTH,height=HEIGHT,mask='auto');c.restoreState()
        c.setFillColor(PAPER);c.rect(0,0,WIDTH,147,stroke=0,fill=1)
        c.setFillColor(RUST);c.setFont('Fraunces',8.3);c.drawString(30,126,'A FIELD MANUAL  /  VOLUME IV')
        c.setFillColor(INK);c.setFont('Fraunces',33);c.drawString(29,88,'Zombieproof');c.drawString(29,55,'Medical')
        c.setFillColor(OLIVE);c.setFont('Fraunces-Italic',11.4);c.drawString(30,29,META['subtitle'])
        c.setFont('Fraunces',8.1);c.drawRightString(WIDTH-29,12,'whispr.dev')


class BookDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(WIDTH,HEIGHT),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=.65*inch,bottomMargin=.7*inch,title=META['title'],author=META['publisher'],subject='Illustrated civilian first-aid and preparedness guide; editorial edition, not clinically reviewed',creator='whispr.dev / local book build',pageCompression=1)
        self.page_by_id={};self.current_section=''
        normal=Frame(MARGIN,.7*inch,TEXT,HEIGHT-1.35*inch,id='text',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        full=Frame(0,0,WIDTH,HEIGHT,id='full',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate('Cover',[full]),PageTemplate('Silent',[normal]),PageTemplate('Normal',[normal],onPage=self.running)])
    def beforeDocument(self):
        self.page_by_id={};self.current_section=''
    def running(self,c,d):
        c.saveState();c.setFillColor(MUTED);c.setFont('Fraunces',7.8)
        c.drawString(MARGIN,HEIGHT-27,'ZOMBIEPROOF MEDICAL');c.drawRightString(WIDTH-MARGIN,HEIGHT-27,'VOLUME IV')
        c.setStrokeColor(RULE);c.setLineWidth(.4);c.line(MARGIN,HEIGHT-32,WIDTH-MARGIN,HEIGHT-32)
        c.setFont('Literata',8);c.drawString(MARGIN,26,'whispr.dev');c.drawRightString(WIDTH-MARGIN,26,str(d.page));c.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Heading) and f.key:
            self.page_by_id[f.key]=self.page
            self.canv.bookmarkPage(f.key)
            label=(str(int(f.key[2:]))+'. '+f.plain) if re.fullmatch(r'ch\d\d',f.key) else f.plain
            self.canv.addOutlineEntry(label,f.key,level=0,closed=False)
            self.notify('TOCEntry',(f.toclevel,label,self.page,f.key))


def flow_html(content: str, st: dict, section_pages: bool=False) -> list:
    out=[];root=LH.fragment_fromstring(content,create_parent='div');first=True;local=st
    card=dict(st)
    card['body']=ParagraphStyle('cardbody',parent=st['body'],fontSize=11.2,leading=17,spaceAfter=10)
    card['list']=ParagraphStyle('cardlist',parent=st['list'],fontSize=11.2,leading=17,spaceAfter=10)
    for node in root:
        tag=node.tag
        if tag=='h1': continue
        if tag in ('h2','h3'):
            if section_pages and tag=='h2':
                if not node.text_content().startswith('The final check'):out.append(PageBreak())
                local=card if node.text_content().startswith('Card ') else st
            out.append(Paragraph(inner(node),st[tag]));first=False
        elif tag=='p':
            text=inner(node)
            style=st['small'] if node.text_content().startswith('Sources:') else st['lede'] if first else local['body']
            out.append(Paragraph(text,style));first=False
        elif tag in ('ul','ol'):
            for i,li in enumerate(node,1):
                prefix=f'{i}.' if tag=='ol' else '•'
                out.append(Paragraph(html.escape(prefix)+'  '+inner(li),local['list']))
            first=False
        elif tag=='blockquote':
            cell=[Paragraph(inner(x),st['quote']) for x in node]
            t=Table([[cell]],colWidths=[TEXT],hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PAPER),('LINEBEFORE',(0,0),(0,-1),2,OLIVE),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
            out += [Spacer(1,6),t,Spacer(1,10)];first=False
        elif tag=='table':
            raw=node.xpath('.//tr');cols=len(raw[0]);data=[]
            blank=all(not cell.text_content().strip() for row in raw[1:] for cell in row.xpath('./td'))
            for ri,row in enumerate(raw): data.append([Paragraph(inner(c),st['th' if ri==0 else 'table']) for c in row])
            widths=[TEXT/cols]*cols
            if cols==2:widths=[TEXT*.36,TEXT*.64]
            if cols==3 and 'Need' in raw[0].text_content():widths=[TEXT*.24,TEXT*.43,TEXT*.33]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT',minRowHeights=[0]+[27 if blank else 19]*(len(data)-1))
            t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PAPER),('LINEBELOW',(0,0),(-1,0),.7,OLIVE),('LINEBELOW',(0,1),(-1,-1),.35,RULE),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            out += [Spacer(1,5),t,Spacer(1,12)];first=False
        else: raise ValueError(f'Unsupported content block: {tag}')
    return out


def reference_html() -> str:
    intro='<h1>References and source notes</h1><p>Web guidance checked 20 October 2026. References identify sources, not endorsements. Product labels and current professional instructions take precedence over generic summaries. Some earlier training references are included for context.</p>'
    entries=[]
    for r in REFS:
        extra=(' <a href="'+html.escape(r['additional_url'],quote=True)+'">'+html.escape(r['additional_url'])+'</a>') if r.get('additional_url') else ''
        entries.append(f'<div id="{r["id"]}"><p><b>{r["id"]} · {html.escape(r["organisation"])}</b><br/>{html.escape(r["title"])}</p>'+(f'<p><a href="{html.escape(r["url"],quote=True)}">{html.escape(r["url"])}</a></p>' if r['url'] else '<p>Supplied in Documents.tar.gz; not redistributed.</p>')+extra+'</div>')
    return intro+'\n'.join(entries)


def index_html(chapters) -> str:
    s='<h1>Subject finder</h1><p>Chapter links are used so this finder works in print, EPUB and the editable web edition.</p><table><thead><tr><th>Subject</th><th>Chapters</th></tr></thead><tbody>'
    for term,ns in META['subject_finder']:
        s+='<tr><td>'+html.escape(term)+'</td><td>'+', '.join(f'<a href="ch{n:02}.xhtml">{n}</a>' for n in ns)+'</td></tr>'
    return s+'</tbody></table>'


def copyright_html() -> str:
    return '<h1>Edition and care notice</h1><p><b>'+META['copyright']+'</b></p><p>'+META['edition']+'<br/>Prepared for and published by whispr.dev. 20 October 2026.</p><p>Original prose, layouts and illustrations prepared for this edition. All rights reserved, except where third-party font licences state otherwise. Referenced organisations retain rights in their own materials. No endorsement is implied.</p><p><b>'+META['review_status']+'</b> Professional clinical review is required before publication as dependable medical instruction. This book supports education and preparedness; it does not diagnose, prescribe, certify competence or replace practical training and professional care.</p><p>Use emergency services whenever available. In the UK, call 999 or 112 for life-threatening emergencies. If help is delayed, continue appropriate first aid and pursue safe clinical advice and handover. Local numbers, services and rules differ outside the UK.</p><p>The zombies and Nigel are fictional. The clinical limits are real. Illustrations are decorative narrative scenes, not demonstrations of medical procedures.</p><p>Set in Fraunces and Literata, using the same 6 × 9 inch format and colour family as the supplied series. Illustrations were created with AI assistance from the series references. Font licence notices accompany the source package.</p>'


def chapters_data():
    result=[]
    for n in range(1,18):
        s=(ROOT/'manuscript'/f'{n:02}.md').read_text(encoding='utf-8')
        title=s.splitlines()[0][2:]
        result.append(dict(n=n,id=f'ch{n:02}',title=title,md=s,html=md_html(s),caption=META['captions'][n-1],alt=META['alt'][n-1]))
    return result


def make_pdf(chapters,st):
    path=BUILD/'Zombieproof-Medical.pdf';doc=BookDoc(path);story=[Cover(),NextPageTemplate('Silent'),PageBreak()]
    with PILImage.open(ROOT/'art'/'frontis.jpg') as source: front_ratio=source.height/source.width
    front=Image(str(ROOT/'art'/'frontis.jpg'),width=3.15*inch,height=3.15*inch*front_ratio)
    story += [Spacer(1,12),front,Spacer(1,21),Paragraph('The dead may walk.<br/>The living still need care.',ParagraphStyle('frontquote',parent=st['partblurb'],alignment=TA_CENTER)),NextPageTemplate('Silent'),PageBreak()]
    story += [Spacer(1,100),Paragraph('A FIELD MANUAL / VOLUME IV',st['kicker']),Paragraph('Zombieproof<br/>Medical',ParagraphStyle('title',parent=st['part'],fontSize=37,leading=39)),Paragraph(META['subtitle'],st['partblurb']),Spacer(1,97),Paragraph('For the person who came back to check.',st['caption']),Spacer(1,36),Paragraph('whispr.dev',st['h2']),Paragraph('First illustrated editorial edition · 2026',st['small']),NextPageTemplate('Normal'),PageBreak()]
    story += [Paragraph('Edition and care notice',st['h1'])]
    story += flow_html(copyright_html().replace('<h1>Edition and care notice</h1>',''),st)
    story += [PageBreak(),Heading('Contents',st['h1'])]
    toc=TableOfContents();toc.dotsMinLevel=0
    toc.levelStyles=[ParagraphStyle('toc0',fontName='Fraunces',fontSize=10.3,leading=14.5,textColor=OLIVE,spaceBefore=8,leftIndent=0,rightIndent=19),ParagraphStyle('toc1',fontName='Literata',fontSize=9.4,leading=13.5,textColor=INK,leftIndent=10,rightIndent=19,spaceBefore=3)]
    story += [toc,PageBreak(),Heading('How to Keep the Living Living',st['h1'],'foreword')]
    story += flow_html(md_html((ROOT/'manuscript'/'frontmatter.md').read_text(encoding='utf-8')),st)
    parts={p['start']:p for p in META['parts']}
    for ch in chapters:
        if ch['n'] in parts:
            p=parts[ch['n']]
            story += [NextPageTemplate('Silent'),PageBreak(),Spacer(1,220),Paragraph('PART '+p['n'],st['kicker']),Heading(html.escape(p['title']),st['part'],'part'+p['n']),Paragraph(html.escape(p['blurb']),st['partblurb']),NextPageTemplate('Normal')]
        story += [PageBreak(),Paragraph(f'CHAPTER {ch["n"]:02}',st['kicker']),Heading(html.escape(ch['title']),st['h1'],ch['id'],1)]
        art=PILImage.open(ROOT/'art'/f'{ch["id"]}.jpg');ratio=art.height/art.width;art.close()
        story += [Image(str(ROOT/'art'/f'{ch["id"]}.jpg'),width=TEXT,height=TEXT*ratio),Paragraph(html.escape(ch['caption']),st['caption'])]
        story += flow_html(ch['html'],st,section_pages=ch['n']==17)
    story += [PageBreak(),Heading('The Next Person Through the Door',st['h1'],'afterword')]
    story += flow_html(md_html((ROOT/'manuscript'/'afterword.md').read_text(encoding='utf-8')),st)
    story += [PageBreak(),Heading('References and source notes',st['h1'],'references'),Paragraph('Web guidance checked 20 October 2026. These sources are not endorsements. See the edition notice and source notes for limits and review status.',st['body'])]
    for r in REFS:
        title=f'<a name="{r["id"]}"/><b>{r["id"]} · {html.escape(r["organisation"])}</b><br/>{html.escape(r["title"])}'
        group=[Paragraph(title,st['ref'])]
        if r['url']:
            for u in [r['url']]+([r['additional_url']] if r.get('additional_url') else []):
                group.append(Paragraph('<link href="'+html.escape(u,quote=True)+'">'+html.escape(u)+'</link>',st['url']))
        else:group.append(Paragraph('Supplied in Documents.tar.gz; not redistributed.',st['small']))
        story.append(KeepTogether(group))
    story += [PageBreak(),Heading('A note on evidence',st['h1'],'evidence')]
    for p in [
        'The supplied professional field-care collection contributes background on prolonged care, documentation and clinical boundaries. It assumes medical training. Its invasive procedures and professional drug regimens have not been converted into lay instructions.',
        'The older START references explain organisation and reassessment; they do not supply a lay rule for declaring death. The acquisition essay was treated as a research lead, not authority for drug longevity or medical practice.',
        'Where sources differ, this edition follows RCUK 2025 for adult resuscitation and its updated public infant CPR guidance. In particular, call early for an unresponsive adult, start CPR on a bed rather than delaying to move, and use the current infant compression method described in Chapter 15.',
        'Research on extended medicine shelf life does not validate unknown stock. No universal expiry extension, household sterile-processing method or drug-substitution regimen is supplied.',
        'This is the first illustrated editorial edition. Independent clinical review has not occurred. Sources, treatment instructions, medicine statements and quick-reference summaries must be reviewed by appropriately qualified people before publication as dependable medical guidance. The full editorial review notes are included in the source package.'
    ]:story.append(Paragraph(p,st['body']))
    story += [PageBreak(),Heading('Subject finder',st['h1'],'finder'),Paragraph('Chapter numbers remain useful across print and EPUB. The contents gives the starting page for each chapter.',st['body'])]
    data=[[Paragraph('SUBJECT',st['th']),Paragraph('CHAPTERS',st['th'])]]
    for term,ns in META['subject_finder']:
        links=', '.join(f'<link href="#ch{n:02}">{n}</link>' for n in ns)
        data.append([Paragraph(html.escape(term),st['table']),Paragraph(links,st['table'])])
    t=Table(data,colWidths=[TEXT*.76,TEXT*.24],repeatRows=1)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PAPER),('LINEBELOW',(0,0),(-1,-1),.35,RULE),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t)
    doc.multiBuild(story,maxPasses=8)
    (BUILD/'pagination.json').write_text(json.dumps(doc.page_by_id,indent=2),encoding='utf-8')
    return path


def css() -> str:
    return '''@font-face{font-family:Literata;src:url(fonts/literata-latin-400-normal.woff)}
@font-face{font-family:Literata;src:url(fonts/literata-latin-700-normal.woff);font-weight:bold}
@font-face{font-family:Literata;src:url(fonts/literata-latin-400-italic.woff);font-style:italic}
@font-face{font-family:Fraunces;src:url(fonts/fraunces-latin-600-normal.woff);font-weight:600}
@font-face{font-family:Fraunces;src:url(fonts/fraunces-latin-500-italic.woff);font-style:italic}
html{background:#f3ead8;color:#1c1712}body{max-width:44rem;margin:0 auto;padding:1.5rem;font:1rem/1.6 Literata,Georgia,serif}
h1,h2,h3{font-family:Fraunces,Georgia,serif;line-height:1.2;color:#1c1712}h1{font-size:2rem;margin:1rem 0}h2{font-size:1.3rem;margin-top:1.5rem}
a{color:#8c3014;overflow-wrap:anywhere}img{max-width:100%;height:auto}.cover{text-align:center;page-break-after:always}.cover img{max-height:90vh}
section,article{margin-bottom:3rem}figure{margin:1rem 0}figcaption{font:italic .9rem/1.4 Fraunces,Georgia,serif;color:#655d50;margin-top:.5rem}
.kicker{font-family:Fraunces,serif;text-transform:uppercase;letter-spacing:.13em;color:#8c3014;font-size:.8rem}
blockquote{margin:1rem 0;background:#eee4cf;border-left:3px solid #3e4a32;padding:.7rem 1rem;color:#3e4a32}blockquote p{margin:0}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin:1rem 0;table-layout:fixed}th,td{text-align:left;vertical-align:top;padding:.5rem;border-bottom:1px solid #d2c4aa;overflow-wrap:anywhere}th{font-family:Fraunces,serif;background:#eee4cf}td{min-height:1.5rem}
.part{padding:5rem 0 3rem;page-break-before:always}.chapter{page-break-before:always}.note{font-size:.9rem;color:#655d50}.ref{margin-bottom:1.3rem}.ref p{margin:.25rem 0}.ref a{font-size:.8rem}li{margin-bottom:.4rem}
@media print{@page{size:6in 9in;margin:.68in .66in .7in}html,body{background:white}body{padding:0;font-size:10.2pt;line-height:1.5}.cover img{max-height:8in}h1,h2,h3{break-after:avoid}figure,blockquote,tr{break-inside:avoid}thead{display:table-header-group}section,article{margin:0}.part{padding-top:3in}.chapter{break-before:page}}
'''


def make_cover_jpeg():
    """Typeset an ebook cover deterministically from the generated cover illustration."""
    scale=3;w,h=432*scale,648*scale
    source=PILImage.open(ROOT/'art'/'cover.jpg').convert('RGB').resize((w,h),PILImage.Resampling.LANCZOS)
    d=ImageDraw.Draw(source);d.rectangle((0,501*scale,w,h),fill='#f3ead8')
    def f(name,size):return ImageFont.truetype(str(ROOT/'fonts'/name),round(size*scale))
    d.text((30*scale,509*scale),'A FIELD MANUAL  /  VOLUME IV',font=f('fraunces-latin-600-normal.ttf',8.3),fill='#8c3014')
    d.text((29*scale,529*scale),'Zombieproof',font=f('fraunces-latin-600-normal.ttf',33),fill='#1c1712')
    d.text((29*scale,562*scale),'Medical',font=f('fraunces-latin-600-normal.ttf',33),fill='#1c1712')
    d.text((30*scale,609*scale),META['subtitle'],font=f('fraunces-latin-500-italic.ttf',11.4),fill='#3e4a32')
    d.text((350*scale,633*scale),'whispr.dev',font=f('fraunces-latin-600-normal.ttf',8.1),fill='#3e4a32')
    source.save(BUILD/'cover-typeset.jpg',quality=94,optimize=True,subsampling=0)


def make_html(chapters):
    toc='<h1>Contents</h1><ol>'+''.join(f'<li><a href="#{c["id"]}">{html.escape(c["title"])}</a></li>' for c in chapters)+'</ol>'
    sections=['<section class="cover"><img src="build/cover-typeset.jpg" alt="Zombieproof Medical book cover"/></section>','<section>'+copyright_html()+'</section>','<nav>'+toc+'</nav>','<section>'+md_html((ROOT/'manuscript'/'frontmatter.md').read_text(encoding='utf-8'))+'</section>']
    for c in chapters:
        sections.append(f'<article class="chapter" id="{c["id"]}"><p class="kicker">Chapter {c["n"]}</p><h1>{html.escape(c["title"])}</h1><figure><img src="art/{c["id"]}.jpg" alt="{html.escape(c["alt"],quote=True)}"/><figcaption>{html.escape(c["caption"])}</figcaption></figure>'+re.sub(r'^<h1>.*?</h1>\n?','',c['html'])+'</article>')
    sections += ['<section>'+md_html((ROOT/'manuscript'/'afterword.md').read_text(encoding='utf-8'))+'</section>','<section>'+reference_html()+'</section>']
    finder=index_html(chapters)
    finder=re.sub(r'href="ch(\d+)\.xhtml"',r'href="#ch\1"',finder)
    sections.append('<section>'+finder+'</section>')
    body='\n'.join(sections)
    output='<!doctype html><html lang="en-GB"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>'+META['title']+'</title><style>'+css()+'</style></head><body>'+body+'</body></html>'
    (ROOT/'print.html').write_text(output,encoding='utf-8')
    md='# '+META['title']+'\n\n'+META['subtitle']+'\n\n'+META['copyright']+'\n\n'+META['review_status']+'\n\n'
    md+=(ROOT/'manuscript'/'frontmatter.md').read_text(encoding='utf-8')+'\n\n'
    md+='\n\n'.join(c['md'] for c in chapters)+'\n\n'+(ROOT/'manuscript'/'afterword.md').read_text(encoding='utf-8')+'\n\n# References\n\n'
    md+='\n\n'.join(f'**{r["id"]} — {r["organisation"]}.** {r["title"]}. '+r['url']+(' '+r['additional_url'] if r.get('additional_url') else '') for r in REFS)
    (BUILD/'Zombieproof-Medical.md').write_text(md,encoding='utf-8')


def xhtml(title,body):
    # HTML fragments from the book are normalised into XML for EPUB compatibility.
    root=LH.fragment_fromstring('<div>'+body+'</div>')
    xml=''.join(ET.tostring(x,encoding='unicode',method='xml') for x in root)
    return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en-GB" xml:lang="en-GB"><head><title>'+html.escape(title)+'</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>'+xml+'</body></html>'


def make_epub(chapters):
    out=BUILD/'Zombieproof-Medical.epub';pages=[]
    pages.append(('cover','Cover','<section class="cover"><img src="images/cover.jpg" alt="Zombieproof Medical, How to Keep the Living Living, Volume IV"/></section>'))
    pages.append(('title',META['title'],'<p class="kicker">A field manual / Volume IV</p><h1>Zombieproof Medical</h1><p>'+META['subtitle']+'</p><p>whispr.dev</p><p>'+META['edition']+'</p>'))
    pages.append(('notice','Edition and care notice',copyright_html()))
    pages.append(('frontis','For the watch','<figure><img src="images/frontis.jpg" alt="A friendly zombie rests under a blanket in a cottage"/><figcaption>The dead may walk. The living still need care.</figcaption></figure>'))
    pages.append(('foreword','How to Keep the Living Living',md_html((ROOT/'manuscript'/'frontmatter.md').read_text(encoding='utf-8'))))
    parts={p['start']:p for p in META['parts']}
    for c in chapters:
        if c['n'] in parts:
            p=parts[c['n']];pages.append(('part'+p['n'],p['title'],'<section class="part"><p class="kicker">Part '+p['n']+'</p><h1>'+html.escape(p['title'])+'</h1><p>'+html.escape(p['blurb'])+'</p></section>'))
        body=f'<p class="kicker">Chapter {c["n"]}</p><h1>{html.escape(c["title"])}</h1><figure><img src="images/{c["id"]}.jpg" alt="{html.escape(c["alt"],quote=True)}"/><figcaption>{html.escape(c["caption"])}</figcaption></figure>'+re.sub(r'^<h1>.*?</h1>\n?','',c['html'])
        pages.append((c['id'],c['title'],body))
    pages.append(('afterword','The Next Person Through the Door',md_html((ROOT/'manuscript'/'afterword.md').read_text(encoding='utf-8'))))
    pages.append(('references','References and source notes',reference_html()))
    pages.append(('finder','Subject finder',index_html(chapters)))
    nav='<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'+''.join('<li><a href="'+id+'.xhtml">'+html.escape(title)+'</a></li>' for id,title,_ in pages if id!='cover')+'</ol></nav>'
    ident='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://whispr.dev/zombieproof-medical/1.0.0'))
    manifest=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="css" href="style.css" media-type="text/css"/>','<item id="coverimage" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>']
    manifest += [f'<item id="{id}" href="{id}.xhtml" media-type="application/xhtml+xml"/>' for id,_,_ in pages]
    manifest += [f'<item id="img-{id}" href="images/{id}.jpg" media-type="image/jpeg"/>' for id in ['frontis']+[c['id'] for c in chapters]]
    fonts=sorted((ROOT/'fonts').glob('*.woff'))
    manifest += [f'<item id="font{i}" href="fonts/{p.name}" media-type="font/woff"/>' for i,p in enumerate(fonts)]
    manifest += ['<item id="fontlicense" href="fonts/LICENSES.txt" media-type="text/plain"/>']
    spine='<itemref idref="cover"/><itemref idref="title"/><itemref idref="notice"/><itemref idref="nav"/>'+''.join(f'<itemref idref="{id}"/>' for id,_,_ in pages if id not in ['cover','title','notice'])
    opf='<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en-GB"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">'+ident+'</dc:identifier><dc:title>'+META['title']+'</dc:title><dc:language>en-GB</dc:language><dc:creator>whispr.dev</dc:creator><dc:publisher>whispr.dev</dc:publisher><dc:rights>'+META['copyright']+'</dc:rights><dc:description>Illustrated first-aid and preparedness guide. Complete editorial edition; not independently clinically reviewed.</dc:description><meta property="dcterms:modified">2026-10-20T00:00:00Z</meta></metadata><manifest>'+''.join(manifest)+'</manifest><spine>'+spine+'</spine></package>'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr('OEBPS/content.opf',opf);z.writestr('OEBPS/style.css',css());z.writestr('OEBPS/nav.xhtml',xhtml('Contents',nav.replace('epub:type="toc"','data-epub-type="toc"')).replace('data-epub-type="toc"','epub:type="toc"'))
        for id,title,body in pages:z.writestr('OEBPS/'+id+'.xhtml',xhtml(title,body))
        z.write(BUILD/'cover-typeset.jpg','OEBPS/images/cover.jpg')
        for id in ['frontis']+[c['id'] for c in chapters]:z.write(ROOT/'art'/f'{id}.jpg','OEBPS/images/'+id+'.jpg')
        for p in fonts:z.write(p,'OEBPS/fonts/'+p.name)
        z.write(ROOT/'fonts'/'LICENSES.txt','OEBPS/fonts/LICENSES.txt')
    return out


def validate(chapters):
    from pypdf import PdfReader
    missing=[]
    for c in chapters:
        for n in re.findall(r'R\d\d',c['md']):
            if n not in REF_IDS:missing.append((c['id'],n))
        if not (ROOT/'art'/f'{c["id"]}.jpg').is_file():missing.append((c['id'],'art'))
    if missing:raise ValueError(f'Missing references/assets: {missing}')
    reader=PdfReader(BUILD/'Zombieproof-Medical.pdf')
    alltext='\n'.join(p.extract_text() for p in reader.pages)
    for c in chapters:
        if c['title'] not in ' '.join(alltext.split()):raise ValueError('PDF missing chapter '+c['id'])
    for token in ['TODO','TBD','PLACEHOLDER']:
        if token in alltext:raise ValueError('Unfinished text: '+token)
    with zipfile.ZipFile(BUILD/'Zombieproof-Medical.epub') as z:
        infos=z.infolist()
        if infos[0].filename!='mimetype' or infos[0].compress_type!=zipfile.ZIP_STORED:raise ValueError('Invalid EPUB mimetype placement')
        names=set(z.namelist())
        for n in names:
            if n.endswith(('.xml','.xhtml','.opf')):ET.fromstring(z.read(n))
        for n in names:
            if n.endswith('.xhtml'):
                tree=ET.fromstring(z.read(n))
                for node in tree.iter():
                    for attr in ('src','href'):
                        v=node.get(attr)
                        if v and not v.startswith(('https:','http:','#','mailto:')):
                            target=str(Path(n).parent/v.split('#')[0]).replace('\\','/')
                            if target not in names:raise ValueError(f'Broken EPUB reference {n}: {v}')
    if len(reader.pages[0].get('/Resources',{}).get('/XObject',{}))==0:raise ValueError('Cover missing artwork')
    result=dict(chapters=len(chapters),chapter_words=sum(len(c['md'].split()) for c in chapters),illustrations=19,pdf_pages=len(reader.pages),references=len(REFS),epub_xml_and_local_links='passed',missing_assets='none',review_status=META['review_status'])
    (BUILD/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))


def main():
    BUILD.mkdir(exist_ok=True);register_fonts();st=styles();chapters=chapters_data()
    make_cover_jpeg();make_html(chapters);make_pdf(chapters,st);make_epub(chapters);validate(chapters)
    print('Built PDF, EPUB, HTML and full Markdown in',BUILD)


if __name__=='__main__':main()
