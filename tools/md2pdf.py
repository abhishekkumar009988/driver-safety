#!/usr/bin/env python3
"""
md2pdf.py — render AI-FILM-PROMPTS.md as a styled A4 PDF.

Why custom: the document is full of box-drawing characters (U+2550), stars and
emoji that no single installed font covers. So we register a small font stack
(Noto Sans / Noto Sans Mono / DejaVu / Noto Sans Symbols 2 / OpenMoji black) and
route every character to the first font in the chain that actually has a glyph
for it. No tofu, no missing boxes.

Fonts live in /home/user/fonts (Noto Sans + Noto Sans Mono + Noto Sans Symbols 2
+ OpenMoji-black, downloaded from the notofonts/noto-fonts and hfg-gmuend/openmoji
repos; DejaVu ships inside matplotlib). Re-fetch them if they are missing, then:

Usage:  python3 tools/md2pdf.py <input.md> <output.pdf>
"""
import os
import re
import sys
import datetime

from fontTools.ttLib import TTFont as FTFont

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, HRFlowable,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Preformatted, Spacer, Table,
                                TableStyle)

# ---------------------------------------------------------------- font stack
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/home/user/fonts"
SYS_TTF = "/usr/share/fonts/truetype/dejavu"

FONTS = {
    "Noto":          os.path.join(FONT_DIR, "NotoSans-Regular.ttf"),
    "Noto-B":        os.path.join(FONT_DIR, "NotoSans-Bold.ttf"),
    "Noto-I":        os.path.join(FONT_DIR, "NotoSans-Italic.ttf"),
    "Noto-BI":       os.path.join(FONT_DIR, "NotoSans-BoldItalic.ttf"),
    "Mono":          os.path.join(FONT_DIR, "NotoSansMono-Regular.ttf"),
    "Mono-B":        os.path.join(FONT_DIR, "NotoSansMono-Bold.ttf"),
    "DejaVu":        os.path.join(FONT_DIR, "DejaVuSans.ttf"),
    "DejaVu-B":      os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"),
    "DejaVuMono":    os.path.join(FONT_DIR, "DejaVuSansMono.ttf"),
    "DejaVuMono-B":  os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf"),
    "Sym2":          os.path.join(FONT_DIR, "NotoSansSymbols2-Regular.ttf"),
    "Emoji":         os.path.join(FONT_DIR, "OpenMoji-black-glyf.ttf"),
}

CHAIN = {
    "r":  ["Noto", "DejaVu", "Sym2", "Emoji"],
    "b":  ["Noto-B", "DejaVu-B", "Sym2", "Emoji"],
    "i":  ["Noto-I", "DejaVu", "Sym2", "Emoji"],
    "bi": ["Noto-BI", "DejaVu-B", "Sym2", "Emoji"],
    "c":  ["Mono", "DejaVuMono", "Sym2", "Emoji"],
    "cb": ["Mono-B", "DejaVuMono-B", "Sym2", "Emoji"],
}

COVERAGE = {}
for name, path in FONTS.items():
    try:
        pdfmetrics.registerFont(TTFont(name, path))
        COVERAGE[name] = set(FTFont(path, fontNumber=0).getBestCmap().keys())
    except Exception as exc:                                   # pragma: no cover
        sys.stderr.write("font %s failed: %s\n" % (name, exc))

# keycap sequences and variation selectors get folded into plain glyphs
KEYCAP = {0x0030: "\u24EA", 0x0031: "\u2460", 0x0032: "\u2461",
          0x0033: "\u2462", 0x0034: "\u2463", 0x0035: "\u2464",
          0x0036: "\u2465", 0x0037: "\u2466", 0x0038: "\u2467",
          0x0039: "\u2468", 0x0023: "\u24D8", 0x002A: "\u24E9"}
FALLBACK = {"\u274c": "\u2717", "\u2b50": "\u2605", "\u2705": "\u2713"}
# tidy emoji that look muddy at 7.5pt in monochrome
PRE_SUB = {"\u2705": "\u2713", "\u274c": "\u2717"}

# ---------------------------------------------------------------- palette
INK        = colors.HexColor("#15181D")
INK_SOFT   = colors.HexColor("#4A5568")
ACCENT     = colors.HexColor("#B4530A")     # deep saffron
ACCENT_2   = colors.HexColor("#7C2D12")
RULE       = colors.HexColor("#D9DEE5")
CODE_BG    = colors.HexColor("#F5F6F8")
CODE_BG_2  = colors.HexColor("#EEF0F4")
TABLE_HD   = colors.HexColor("#1F2937")
TABLE_ALT  = colors.HexColor("#FAFBFC")

PAGE_W, PAGE_H = A4
M_L, M_R, M_T, M_B = 46, 46, 52, 46
USABLE = PAGE_W - M_L - M_R


def pick_font(ch, key):
    """first font in the chain that has a glyph for this character."""
    cp = ord(ch)
    if cp == 0xFE0F:                       # emoji variation selector: drop
        return None
    if cp == 0x20E3:                       # combining keycap -> folded earlier
        return None
    for name in CHAIN[key]:
        if cp in COVERAGE.get(name, ()):
            return name
    return None


KEYCAP_RE = re.compile(r"([0-9#*])\ufe0f?\u20e3")


def fold_keycaps(t):
    """1<FE0F><20E3> -> \u2460, so the digit keeps a real glyph."""
    return KEYCAP_RE.sub(lambda m: KEYCAP.get(ord(m.group(1)), ""), t)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def markup(text, key, preserve_spaces=False):
    """wrap runs of text in <font> tags according to glyph coverage."""
    text = fold_keycaps(text)
    for a, b in PRE_SUB.items():
        text = text.replace(a, b)
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        fname = pick_font(ch, key)
        if fname is None:
            sub = FALLBACK.get(ch)
            if sub:
                fname = pick_font(sub, key)
                ch = sub
            else:
                i += 1
                continue
        run = ch
        i += 1
        while i < n:
            nxt = pick_font(text[i], key)
            if nxt is None:
                sub = FALLBACK.get(text[i])
                if sub and pick_font(sub, key) == fname:
                    run += sub
                    i += 1
                    continue
                if sub:
                    break
                i += 1
                continue
            if nxt != fname:
                break
            run += text[i]
            i += 1
        seg = esc(run)
        if preserve_spaces and i < n:
            seg = re.sub(r" $", "&nbsp;", seg)
        out.append('<font name="%s">%s</font>' % (fname, seg))
    return "".join(out)


TOKEN_RE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*\s][^*]*\*)")


def inline(text, key="r"):
    """prose inline markup: **bold**, *italic*, `code` -> routed <font> runs."""
    parts = []
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        if tok.startswith("`") and tok.endswith("`") and len(tok) > 1:
            parts.append(markup(tok[1:-1], "c", True))
        elif tok.startswith("**") and tok.endswith("**"):
            parts.append(markup(tok[2:-2], "b" if key == "r" else "b"))
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            parts.append(markup(tok[1:-1], "i"))
        else:
            parts.append(markup(tok, key, True))
    return "".join(parts)


def plain_len(text, size, bold=False):
    """approximate rendered width for table sizing."""
    t = fold_keycaps(TOKEN_RE.sub(lambda m: m.group(0).strip("`*"), text))
    try:
        return pdfmetrics.stringWidth(t, "Noto-B" if bold else "Noto", size)
    except Exception:
        return len(t) * size * 0.55


# ---------------------------------------------------------------- styles
def S(name, **kw):
    base = dict(fontName="Noto", fontSize=9.6, leading=13.6, textColor=INK,
                alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "h1":    S("h1", fontSize=19, leading=23, textColor=ACCENT_2,
               spaceBefore=2, spaceAfter=2, fontName="Noto-B"),
    "h2":    S("h2", fontSize=13.2, leading=17, textColor=ACCENT,
               spaceBefore=13, spaceAfter=5, fontName="Noto-B"),
    "h3":    S("h3", fontSize=11, leading=14.5, textColor=INK,
               spaceBefore=10, spaceAfter=4, fontName="Noto-B"),
    "body":  S("body", spaceAfter=6.5),
    "quote": S("quote", fontSize=9.4, leading=14, textColor=INK_SOFT,
               leftIndent=11, spaceAfter=6.5, fontName="Noto-I"),
    "li":    S("li", leftIndent=17, bulletIndent=5, spaceAfter=4.2),
    "code":  S("code", fontName="Mono", fontSize=7.55, leading=9.75,
               textColor=INK, backColor=CODE_BG, leftIndent=11, rightIndent=7,
               borderPadding=0, spaceBefore=0, spaceAfter=0),
    "cell":  S("cell", fontSize=8.5, leading=11.4),
    "cellh": S("cellh", fontSize=8.6, leading=11.4, textColor=colors.white,
               fontName="Noto-B"),
    "cover_t": S("cover_t", fontName="Noto-B", fontSize=40, leading=44,
                 textColor=ACCENT_2),
    "cover_s": S("cover_s", fontName="Noto", fontSize=12.5, leading=18,
                 textColor=INK_SOFT),
    "cover_k": S("cover_k", fontName="Noto-B", fontSize=9.4, leading=13,
                 textColor=ACCENT),
    "cover_v": S("cover_v", fontName="Noto", fontSize=9.4, leading=13,
                 textColor=INK),
}


class Outline(Flowable):
    """invisible flowable that drops a PDF bookmark at this point."""
    _n = 0

    def __init__(self, title, level=0):
        Flowable.__init__(self)
        Outline._n += 1
        self.title, self.level = title, level
        self.key = "bm%d" % Outline._n
        self.width = self.height = 0

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, self.level, 0)


# ---------------------------------------------------------------- markdown
def split_md(text):
    blocks, code, tbl = [], [], []
    in_code = False
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if s.startswith("```"):
            if in_code:
                blocks.append(("code", code))
                code = []
                in_code = False
            else:
                if tbl:
                    blocks.append(("table", tbl))
                    tbl = []
                code = []
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(ln)
            i += 1
            continue

        if s.startswith("|"):
            tbl.append(ln)
            i += 1
            continue
        elif tbl:
            blocks.append(("table", tbl))
            tbl = []

        if not s:
            i += 1
            continue
        if re.match(r"^-{3,}$", s):
            blocks.append(("hr", None))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            blocks.append(("h%d" % min(len(m.group(1)), 3), m.group(2).strip()))
            i += 1
            continue
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append(("quote", " ".join(x for x in buf if x)))
            continue
        m = re.match(r"^(\s*)([-*·]|\d+\.)\s+(.*)$", ln)
        if m:
            buf = [m.group(3)]
            i += 1
            while i < len(lines):
                nx = lines[i]
                if not nx.strip():
                    break
                if re.match(r"^(\s*)([-*·]|\d+\.)\s+", nx):
                    break
                if nx.strip() in ("---",) or nx.strip().startswith(("```", "#", "|")):
                    break
                buf.append(nx.strip())
                i += 1
            blocks.append(("li", " ".join(buf)))
            continue
        buf = [s]
        i += 1
        while i < len(lines):
            nx = lines[i]
            ns = nx.strip()
            if not ns or ns.startswith(("```", "#", "|", ">")) \
                    or re.match(r"^(\s*)([-*·]|\d+\.)\s+", nx) \
                    or re.match(r"^-{3,}$", ns):
                break
            buf.append(ns)
            i += 1
        blocks.append(("p", " ".join(buf)))
    if tbl:
        blocks.append(("table", tbl))
    return blocks


def make_table(rows):
    rows = [r for r in rows if not re.match(r"^\|[\s:\-|]+\|$", r.strip())]
    grid = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        grid.append(cells)
    if not grid:
        return None
    ncol = max(len(r) for r in grid)
    for r in grid:
        while len(r) < ncol:
            r.append("")

    raw = []
    for c in range(ncol):
        w = max(plain_len(r[c], 8.5) for r in grid)
        raw.append(w)
    avail = USABLE - 14 * ncol
    tot = sum(raw) or 1
    widths = [max(46.0, v / tot * avail) for v in raw]
    scale = USABLE / sum(widths)
    widths = [w * scale for w in widths]

    data = []
    for ri, r in enumerate(grid):
        style = ST["cellh"] if ri == 0 else ST["cell"]
        key = "b" if ri == 0 else "r"
        data.append([Paragraph(inline(c, key), style) for c in r])

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
    ]
    for ri in range(2, len(grid), 1):
        if ri % 2 == 0:
            cmds.append(("BACKGROUND", (0, ri), (-1, ri), TABLE_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def build_flowables(blocks, doc_title="AI-FILM-PROMPTS"):
    flow = []
    prev = None
    for kind, payload in blocks:
        if kind == "h1":
            if prev is not None:
                flow.append(Spacer(1, 10))
                flow.append(HRFlowable(width="100%", thickness=1.4,
                                       color=ACCENT, spaceAfter=8))
            plain = TOKEN_RE.sub(lambda m: m.group(0).strip("`*"), payload)
            flow.append(Outline(plain[:80], 0))
            flow.append(Paragraph(inline(payload), ST["h1"]))
            flow.append(Spacer(1, 3))
            flow.append(HRFlowable(width="100%", thickness=0.8, color=RULE))
            flow.append(Spacer(1, 9))
        elif kind == "h2":
            plain2 = TOKEN_RE.sub(lambda m: m.group(0).strip("`*"), payload)
            flow.append(Outline(plain2[:80], 1))
            flow.append(Paragraph(inline(payload), ST["h2"]))
        elif kind == "h3":
            flow.append(Paragraph(inline(payload), ST["h3"]))
        elif kind == "p":
            flow.append(Paragraph(inline(payload), ST["body"]))
        elif kind == "li":
            flow.append(Paragraph(inline(payload), ST["li"],
                                  bulletText="\u2022"))
        elif kind == "quote":
            flow.append(Paragraph(inline(payload), ST["quote"]))
        elif kind == "hr":
            flow.append(Spacer(1, 5))
            flow.append(HRFlowable(width="100%", thickness=0.7, color=RULE))
            flow.append(Spacer(1, 5))
        elif kind == "table":
            t = make_table(payload)
            if t:
                flow.append(Spacer(1, 3))
                flow.append(t)
                flow.append(Spacer(1, 8))
        elif kind == "code":
            lines = payload
            while lines and not lines[-1].strip():
                lines.pop()
            while lines and not lines[0].strip():
                lines.pop(0)
            if not lines:
                prev = kind
                continue
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.7, color=RULE,
                                   spaceAfter=0))
            for ln in lines:
                if not ln.strip():
                    flow.append(Paragraph("&nbsp;", ST["code"]))
                    continue
                indent = len(ln) - len(ln.lstrip(" "))
                txt = "\u00a0" * indent + "  " + ln.strip("\n").lstrip(" ")
                flow.append(Paragraph(markup(txt, "c", True), ST["code"]))
            flow.append(HRFlowable(width="100%", thickness=0.7, color=RULE,
                                   spaceBefore=0))
            flow.append(Spacer(1, 7))
        prev = kind
    return flow


# ---------------------------------------------------------------- document
def footer(canv, doc):
    canv.saveState()
    y = M_B - 20
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.6)
    canv.line(M_L, y + 12, PAGE_W - M_R, y + 12)
    canv.setFont("Noto", 7.6)
    canv.setFillColor(INK_SOFT)
    canv.drawString(M_L, y, "AI-FILM-PROMPTS  \u00b7  MASTER v9")
    canv.drawRightString(PAGE_W - M_R, y, "page %d" % canv.getPageNumber())
    canv.restoreState()


def cover(canv, doc):
    canv.saveState()
    bands = [(PAGE_H - 118, 5.5, ACCENT_2), (PAGE_H - 124, 2.2, ACCENT)]
    for y, h, c in bands:
        canv.setFillColor(c)
        canv.rect(M_L, y, USABLE, h, stroke=0, fill=1)
    canv.setFont("Noto", 8.4)
    canv.setFillColor(INK_SOFT)
    canv.drawString(M_L, M_B - 20, "fixed master prompt system  \u00b7  "
                                   "4 prompts  \u00b7  Veo 3 grammar")
    canv.drawRightString(PAGE_W - M_R, M_B - 20,
                         datetime.date.today().strftime("%d %B %Y"))
    canv.restoreState()


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "AI-FILM-PROMPTS.md"
    dst = sys.argv[2] if len(sys.argv) > 2 else "AI-FILM-PROMPTS.pdf"
    md = open(src, encoding="utf-8").read()

    doc = BaseDocTemplate(dst, pagesize=A4,
                          leftMargin=M_L, rightMargin=M_R,
                          topMargin=M_T, bottomMargin=M_B,
                          title="AI-FILM-PROMPTS \u2014 MASTER v9",
                          author="AI-FILM-PROMPTS",
                          subject="Fixed 4-prompt film system")
    frame = Frame(M_L, M_B, USABLE, PAGE_H - M_T - M_B, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=footer),
    ])

    # ---- cover page
    story = [Spacer(1, 96),
             Paragraph("AI-FILM-PROMPTS", ST["cover_t"]),
             Spacer(1, 10),
             Paragraph("MASTER v9", S("cv2", fontName="Noto-B", fontSize=17,
                                      leading=21, textColor=ACCENT)),
             Spacer(1, 14),
             Paragraph("Universal film prompt system &nbsp;\u00b7&nbsp; "
                       "story first &nbsp;\u00b7&nbsp; relationship engine "
                       "&nbsp;\u00b7&nbsp; 4\u20136 camera &nbsp;\u00b7&nbsp; "
                       "merge system", ST["cover_s"]),
             Spacer(1, 40)]
    rows = [("1", "STORY + PLAN", "STORY LOCK, route, shot list"),
            ("2", "CHARACTERS + DUNIYA", "portrait image prompts"),
            ("3", "SHOT CARDS", "image + video prompt per shot"),
            ("4", "REACH", "song, caption, hashtags, timing")]
    cdata = [[Paragraph("#", ST["cover_k"]),
              Paragraph("PROMPT", ST["cover_k"]),
              Paragraph("MILEGA", ST["cover_k"])]]
    for n, t, d in rows:
        cdata.append([Paragraph(n, ST["cover_v"]),
                      Paragraph("<b>%s</b>" % esc(t), ST["cover_v"]),
                      Paragraph(esc(d), ST["cover_v"])])
    ct = Table(cdata, colWidths=[26, 190, USABLE - 216], hAlign="LEFT")
    ct.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
    ]))
    story.append(ct)
    story.append(Spacer(1, 46))
    story.append(HRFlowable(width="100%", thickness=1.0, color=RULE))
    story.append(Spacer(1, 9))
    story.append(Paragraph(
        "Ye tumhare pichhle 4014-line file ka <b>fixed</b> version hai \u2014 "
        "nayi file nahi, wahi system, saari bataayi hui galtiyan theek ki hui.",
        ST["body"]))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ---- body
    story += build_flowables(split_md(md))
    doc.build(story)
    print("wrote %s  (%.1f KB)" % (dst, os.path.getsize(dst) / 1024.0))


if __name__ == "__main__":
    main()
