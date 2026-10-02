#!/usr/bin/env python3
"""
Copy Box v2 — one-tap copy for the WHOLE AI-FILM-PROMPTS.md, exactly in the
order it is written in the markdown.

  · the 4 main prompts get big cards
  · every other copy-worthy part (tables, checklists, order blocks) gets a row
  · one button copies the whole file

The page is built from the markdown at load time, so it can never go stale.

Routes:
  /                 the tap-to-copy page
  /all              whole markdown as plain text
  /prompt/<1-4>     one prompt as plain text
  /md               download the markdown
  /pdf              download the PDF
  /health           plain ok

Usage: python3 tools/copy_box.py --port 8001
"""
import argparse
import html
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
MD_PATH = os.path.join(ROOT, "AI-FILM-PROMPTS.md")
PDF_PATH = os.path.join(ROOT, "AI-FILM-PROMPTS.pdf")
COPY_MD = os.path.join(ROOT, "PROMPTS-COPY.md")
COPY_PDF = os.path.join(ROOT, "PROMPTS-COPY.pdf")

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
PROMPT_RE = re.compile(r"^\s*[1-4]?\ufe0f?\u20e3?\s*PROMPT\s*([1-4])\s*[\u2013\u2014\-]")
MIN_CODE = 1            # chars — EVERY step gets its own button
MIN_TABLE = 1
KIND_LABEL = {"code": "block", "table": "table", "text": "text"}


# ------------------------------------------------------------------ parsing
def read_units():
    """Every copy-worthy piece of the markdown, in document order."""
    try:
        md = open(MD_PATH, encoding="utf-8").read()
    except OSError:
        return [], ""
    lines = md.split("\n")
    units, stack = [], []
    in_code, buf, start = False, [], 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if in_code:
            if s.startswith("```"):
                in_code = False
                txt = "\n".join(buf).strip()
                if len(txt) >= MIN_CODE:
                    units.append(make_unit(stack, txt, "code", start))
            else:
                buf.append(ln)
            i += 1
            continue

        if s.startswith("```"):
            in_code, buf, start = True, [], i
            i += 1
            continue

        m = HEAD_RE.match(s)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            stack = [h for h in stack if h[0] < level] + [(level, text)]
            i += 1
            continue

        if s.startswith("|"):
            tbl, j = [], i
            while j < len(lines) and lines[j].strip().startswith("|"):
                tbl.append(lines[j].strip())
                j += 1
            txt = "\n".join(tbl).strip()
            if len(txt) >= MIN_TABLE:
                units.append(make_unit(stack, txt, "table", i))
            i = j
            continue
        i += 1

    # mark prompts and number everything
    for n, u in enumerate(units):
        u["id"] = "u%d" % n
        u["step"] = n + 1
        u["prompt_num"] = prompt_number(u["title"])
    for u in units:
        if u["prompt_num"]:
            u["kind"] = "prompt"
    return units, md


def p3_parts():
    """PROMPT 3 ke 3 hisse — wahi kataav jo chat me bheja gaya."""
    hit = [u for u in read_units()[0] if u["prompt_num"] == 3]
    if not hit:
        return []
    lines = hit[0]["text"].split("\n")
    try:
        c1 = next(i for i, l in enumerate(lines)
                  if l.strip().startswith("INTIMATE close lenses"))
        c2 = next(i for i, l in enumerate(lines)
                  if l.strip().startswith("NOW WRITE ONE CARD")) + 1
    except StopIteration:
        c1, c2 = len(lines) // 3, 2 * len(lines) // 3
    parts = ["\n".join(ch) for ch in (lines[:c1], lines[c1:c2], lines[c2:])]
    return [t.rstrip() for t in parts]


def make_unit(stack, text, kind, line):
    title = ""
    for lvl, t in reversed(stack):
        title = t
        break
    clean = re.sub(r"[#*`]", "", title).strip()
    return {"title": clean or "—", "text": text, "kind": kind, "line": line,
            "words": len(text.split()), "prompt_num": None, "id": "",
            "step": 0}


def prompt_number(title):
    m = PROMPT_RE.match(title)
    return int(m.group(1)) if m else None


def read_prompts():
    units, _ = read_units()
    return sorted([u for u in units if u["prompt_num"]],
                  key=lambda u: u["prompt_num"])


# ------------------------------------------------------------------ page
PAGE = """<!doctype html>
<html lang="hi"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COPY BOX &mdash; AI-FILM-PROMPTS v10 &middot; har step ka button</title>
<style>
  :root{--bg:#0d1117;--card:#161b22;--line:#2a3038;--ink:#e8edf3;
    --soft:#9aa7b4;--acc:#e8890c;--acc2:#ffb454;--ok:#2ea043;--bad:#d1242f}
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  body{margin:0;background:var(--bg);color:var(--ink);padding:14px 12px 60px;
    font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
    "Noto Sans",sans-serif}
  h1{font-size:22px;margin:2px 0 4px;color:var(--acc2)}
  .kicker{color:var(--soft);font-size:13.5px;margin:0 0 14px}
  .box{background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:12px 14px;font-size:14px;margin:0 0 14px}
  .box b{color:var(--acc)}
  .warn{border-left:3px solid var(--bad);background:#1f1214;border-radius:0 10px
    10px 0;margin:0 0 16px;padding:9px 12px;font-size:14px;color:#ffc9c9}
  h2.sec{font-size:13px;letter-spacing:1.4px;text-transform:uppercase;
    color:var(--soft);margin:22px 2px 10px;font-weight:700}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;
    margin:0 0 14px;overflow:hidden}
  .head{padding:13px 15px 8px}
  .num{display:inline-block;background:#1c2530;color:var(--acc2);font-weight:700;
    font-size:12.5px;padding:3px 9px;border-radius:99px;margin-bottom:7px}
  .title{font-size:17px;font-weight:700;margin:0 0 3px;word-wrap:break-word}
  .sub{color:var(--soft);font-size:13px;margin:0}
  .btn{display:block;width:calc(100% - 30px);margin:10px 15px 14px;border:0;
    border-radius:12px;padding:16px;font-size:17px;font-weight:700;
    background:var(--acc);color:#17130a;cursor:pointer;letter-spacing:.3px}
  .btn:active{transform:scale(.985)}
  .btn.ok{background:var(--ok);color:#fff}
  .btn.bad{background:var(--bad);color:#fff}
  .btn.all{background:#243040;color:#ffd79a;border:1px solid #37455a}
  .row{display:flex;align-items:center;gap:10px;padding:11px 13px;
    border-top:1px solid var(--line)}
  .row:first-child{border-top:0}
  .row .meta{flex:1;min-width:0}
  .row .t{font-size:14.4px;font-weight:600;overflow:hidden;text-overflow:ellipsis;
    white-space:nowrap}
  .row .k{color:var(--soft);font-size:11.6px;margin-top:2px}
  .mini{flex:0 0 auto;border:0;border-radius:9px;padding:11px 13px;font-size:13px;
    font-weight:700;background:#26303d;color:#ffd79a;cursor:pointer}
  .mini.ok{background:var(--ok);color:#fff}
  .mini.bad{background:var(--bad);color:#fff}
  details{margin:0 15px 14px}
  .row details{margin:6px 0 0}
  summary{color:var(--soft);font-size:13px;cursor:pointer;padding:5px 0}
  pre{margin:7px 0 0;background:#0b0f14;border:1px solid var(--line);
    border-radius:10px;padding:11px;font:11.6px/1.42 ui-monospace,monospace;
    color:#c9d5e1;max-height:42vh;overflow:auto;white-space:pre-wrap;
    word-break:break-word;user-select:text}
  .foot{color:var(--soft);font-size:12.5px;text-align:center;margin-top:26px;
    line-height:1.8}
  a{color:var(--acc2)}
</style></head><body>
<h1>COPY BOX</h1>
<p class="kicker">AI-FILM-PROMPTS &middot; MASTER v10 &middot; poori file,
hissa hissa &mdash; <b>har STEP par apna ek-tap COPY button</b></p>

<div class="box">
  <b>Order:</b> PROMPT 1 &rarr; PROMPT 2 &rarr; PROMPT 3 &rarr; (images + clips)
  &rarr; PROMPT 4<br>
  <b>Ek ke baad ek.</b> Beech me kuch apne se mat jodo.
</div>
<div class="warn">
  AI 2nd step me hi video prompt banaye to bolo:
  <b>&ldquo;Step 3 abhi nahi. Sirf portraits do.&rdquo;</b>
</div>

<a class="btn all" style="display:block;text-align:center;text-decoration:none"
   href="/save">&#128190; FILE SAVE / DOWNLOAD karo</a>
<button class="btn all" onclick="copyIt('allmd', this, 'POORI FILE COPY')">
&#128203; POORI FILE COPY KARO (__ALLW__ words)</button>

<h2 class="sec">4 main prompts &mdash; har step ka apna button</h2>
__MAIN__

<h2 class="sec">PROMPT 3 &mdash; 3 hisse (ek hissa = ek button)</h2>
<div class="box" style="font-size:13.5px">
  PROMPT 3 bahut bada hai. Chat me bhejna ho to ek-ek hissa copy karo:
  <b>PART 1 &rarr; PART 2 &rarr; PART 3</b>, isi order me, ek ke baad ek.
  Poora ek saath chahiye to upar wala <b>&#128203; COPY PROMPT 3</b> dabao.
</div>
__P3PARTS__

<h2 class="sec">baaki sab &mdash; isi order me (__NREST__ parts)</h2>
<div class="card">
__REST__
</div>

<p class="foot">
  <b>Download / save:</b>
  <a href="/save">&#128190; SAVE page</a> &middot;
  <a href="/zip" target="_blank" rel="noopener">zip</a> &middot;
  <a href="/prompts" target="_blank" rel="noopener">PROMPTS-COPY.md</a> &middot;
  <a href="/prompts-pdf" target="_blank" rel="noopener">PROMPTS-COPY.pdf</a><br>
  nayi tab me kholo:
  <a href="/view/prompts-md" target="_blank" rel="noopener">md text</a> &middot;
  <a href="/view/prompts-pdf" target="_blank" rel="noopener">pdf</a> &middot;
  <a href="/view/main-pdf" target="_blank" rel="noopener">poori file pdf</a><br>
  fixed file: <b>AI-FILM-PROMPTS.md</b> &mdash; purani file PURANI_FILES/ me hai
</p>

<pre id="allmd" hidden>__ALLMD__</pre>

<script>
async function copyIt(id, btn, label){
  const el = document.getElementById(id);
  if(!el) return;
  const text = el.textContent;
  let ok = false;
  try{
    if(navigator.clipboard && window.isSecureContext){
      await navigator.clipboard.writeText(text); ok = true;
    }
  }catch(e){ ok = false; }
  if(!ok){
    const ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly','');
    ta.style.position='fixed'; ta.style.top='-1000px'; ta.style.opacity='0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    try{ ok = document.execCommand('copy'); }catch(e){ ok = false; }
    document.body.removeChild(ta);
  }
  if(ok){
    btn.classList.add('ok');
    btn.textContent = '\u2705 COPY HO GAYA';
  }else{
    btn.classList.add('bad');
    btn.textContent = 'text select kiya \u2014 copy dabao';
    const d = el.closest('details'); if(d) d.open = true;
    const r = document.createRange(); r.selectNodeContents(el);
    const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    el.scrollIntoView({block:'center'});
  }
  setTimeout(function(){
    btn.classList.remove('ok','bad');
    btn.textContent = label;
  }, 3000);
}
</script>
</body></html>
"""

CARD = """<div class="card">
  <div class="head">
    <span class="num">PROMPT __NUM__ &middot; __WORDS__ words</span>
    <p class="title">__TITLE__</p>
    <p class="sub">__SUB__</p>
  </div>
  <button class="btn" data-label="&#128203; COPY PROMPT __NUM__"
    onclick="copyIt('__ID__', this, '&#128203; COPY PROMPT __NUM__')">
    &#128203; COPY PROMPT __NUM__</button>
  <details><summary>poora prompt padho</summary>
    <pre id="__ID__">__TEXT__</pre></details>
</div>"""

ROW = """<div class="row">
  <div class="meta">
    <div class="t">__TITLE__</div>
    <div class="k">STEP __STEP__ &middot; __KIND__ &middot; __WORDS__ words</div>
    <details><summary>dekho</summary><pre id="__ID__">__TEXT__</pre></details>
  </div>
  <button class="mini" data-label="COPY"
    onclick="copyIt('__ID__', this, 'COPY')">COPY</button>
</div>"""

PARTCARD = """<div class="card">
  <div class="head">
    <span class="num">PROMPT 3 &middot; PART __K__ / 3</span>
    <p class="title">PROMPT 3 &mdash; PART __K__ / 3</p>
    <p class="sub">__WORDS__ words &middot; ek tap me copy, phir agla part</p>
  </div>
  <button class="btn" onclick="copyIt('__ID__', this, '&#128203; COPY P3 PART __K__')">
    &#128203; COPY P3 PART __K__</button>
  <details><summary>poora part padho</summary>
    <pre id="__ID__">__TEXT__</pre></details>
</div>"""

STEPROW = """<div class="row">
  <div class="meta">
    <div class="t">__TITLE__</div>
    <div class="k">__WORDS__ words
      <details><summary>dekho</summary><pre id="__ID__">__TEXT__</pre></details>
    </div>
  </div>
  <button class="mini" onclick="copyIt('__ID__', this, 'COPY')">COPY</button>
</div>"""

STEP_MARK = re.compile(r"^(?:[\u2460-\u2473\u3251-\u3259]\s|PART\s+\d|STEP\s+[A-Z0-9])")
BANNER = re.compile(r"^[\u2501\u2500=\u2550]{2,}\s*(.+?)\s*[\u2501\u2500=\u2550]{2,}$")
SUBID = re.compile(r"^\d[A-Z]\.\s+\S")


def step_head(line):
    """Ek line step ka sir hai? — sirf asli structural markers."""
    t = line.strip()
    if not t or line[:1] == " ":
        return None
    if STEP_MARK.match(t):
        return t[:74]
    m = BANNER.match(t)
    if m and 4 <= len(m.group(1)) <= 74:
        return m.group(1)[:74]
    if SUBID.match(t):
        return t[:74]
    return None


def split_steps(text):
    """Ek prompt ke andar ke steps — har step ka apna COPY button."""
    lines = text.split("\n")
    cut = [i for i, l in enumerate(lines) if step_head(l)]
    if len(cut) < 2:
        return []
    out = []
    for k, i in enumerate(cut):
        j = cut[k + 1] if k + 1 < len(cut) else len(lines)
        body = "\n".join(lines[i:j]).strip()
        out.append((step_head(lines[i]), body))
    return out


SUB_FOR = {
    1: "STORY LOCK &middot; route &middot; shot list &mdash; apni kahani neeche likho",
    2: "sirf portraits &amp; duniya &mdash; yahan video prompt nahi banta",
    3: "har shot ka card &mdash; smoke/fog number, 4&ndash;6 camera, action-attach",
    4: "gaana &middot; caption &middot; hashtag &middot; Nepal timing",
}


def build_page():
    units, md = read_units()
    prompts = sorted([u for u in units if u["prompt_num"]],
                     key=lambda u: u["prompt_num"])
    rest = [u for u in units if not u["prompt_num"]]

    main = []
    for u in prompts:
        n = u["prompt_num"]
        title = re.sub(r"^[#\s]*[1-4]\ufe0f?\u20e3?\s*", "", u["title"])
        title = re.sub(r"^PROMPT\s*[1-4]\s*[-\u2014\u2013]\s*", "", title)
        main.append(
            CARD.replace("__NUM__", str(n))
                .replace("__TITLE__", html.escape(title.strip()))
                .replace("__SUB__", SUB_FOR.get(n, ""))
                .replace("__WORDS__", str(u["words"]))
                .replace("__ID__", u["id"])
                .replace("__TEXT__", html.escape(u["text"])))

    # PROMPT 3 ke 3 hisse — wahi kataav jo chat me bheja gaya
    parts_html = []
    for k, txt in enumerate(p3_parts(), 1):
        parts_html.append(
            PARTCARD.replace("__K__", str(k))
                    .replace("__WORDS__", str(len(txt.split())))
                    .replace("__ID__", "p3part%d" % k)
                    .replace("__TEXT__", html.escape(txt)))

    rows = []
    for u in rest:
        rows.append(ROW.replace("__TITLE__", html.escape(u["title"]))
                       .replace("__KIND__", KIND_LABEL.get(u["kind"], "part"))
                       .replace("__WORDS__", str(u["words"]))
                       .replace("__STEP__", str(u.get("step", 0)))
                       .replace("__ID__", u["id"])
                       .replace("__TEXT__", html.escape(u["text"])))

    # har prompt ke andar ke steps — apna-apna COPY button
    for card_i, u in enumerate(prompts):
        steps = split_steps(u["text"])
        if not steps:
            continue
        sr = []
        for k, (head, body) in enumerate(steps, 1):
            sid = "s%dp%d" % (u["prompt_num"], k)
            sr.append(STEPROW
                      .replace("__TITLE__",
                               html.escape("STEP %02d · %s" % (k, head)))
                      .replace("__WORDS__", str(len(body.split())))
                      .replace("__ID__", sid)
                      .replace("__TEXT__", html.escape(body)))
        block = ('<details style="margin:0 15px 14px">'
                 '<summary>is prompt ke steps &mdash; har step ka apna button '
                 '(%d steps)</summary>%s</details>') % (len(sr), "".join(sr))
        assert main[card_i].endswith("</div>")
        main[card_i] = main[card_i][:-6] + block + "</div>"

    return (PAGE.replace("__MAIN__", "\n".join(main))
                .replace("__P3PARTS__", "\n".join(parts_html))
                .replace("__REST__", "\n".join(rows) or "<p style='padding:14px'>—</p>")
                .replace("__NREST__", str(len(rows)))
                .replace("__ALLW__", str(len(md.split())))
                .replace("__ALLMD__", html.escape(md)))


SAVE_PAGE = """<!doctype html>
<html lang="hi"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FILE SAVE / COPY &mdash; PROMPTS-COPY.md</title>
<style>
  :root{--bg:#0d1117;--card:#161b22;--line:#2a3038;--ink:#e8edf3;
    --soft:#9aa7b4;--acc:#e8890c;--acc2:#ffb454;--ok:#2ea043}
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  body{margin:0;background:var(--bg);color:var(--ink);padding:14px 12px 70px;
    font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
    "Noto Sans",sans-serif}
  h1{font-size:21px;margin:2px 0 6px;color:var(--acc2)}
  .kicker{color:var(--soft);font-size:13.5px;margin:0 0 16px}
  .box{background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:13px 15px;font-size:14.5px;margin:0 0 14px}
  .box b{color:var(--acc)}
  .warn{border-left:3px solid var(--acc);background:#231a0f;border-radius:0 10px
    10px 0;margin:0 0 16px;padding:10px 13px;font-size:14px;color:#ffd9a8}
  .btn{display:block;width:100%;border:0;border-radius:12px;padding:17px;
    font-size:17.5px;font-weight:700;background:var(--acc);color:#17130a;
    cursor:pointer;margin:0 0 10px}
  .btn:active{transform:scale(.985)}
  .btn.ok{background:var(--ok);color:#fff}
  .btn.ghost{background:#243040;color:#ffd79a;border:1px solid #37455a}
  a.btn{text-decoration:none;text-align:center;display:block}
  textarea{width:100%;height:38vh;background:#0b0f14;border:1px solid var(--line);
    border-radius:10px;color:#c9d5e1;font:12px/1.45 ui-monospace,monospace;
    padding:11px;white-space:pre;-webkit-user-select:text;user-select:text}
  .foot{color:var(--soft);font-size:12.5px;text-align:center;margin-top:22px;
    line-height:1.8}
  h2{font-size:15px;color:var(--acc2);margin:22px 0 8px}
</style></head><body>
<h1>FILE SAVE / COPY</h1>
<p class="kicker">PROMPTS-COPY.md &middot; __WORDS__ words &middot; __KB__ KB
&middot; chaar prompt, chaar alag block</p>

<div class="warn">
  Preview ke andar download button block ho jaata hai — ye normal hai.
  Neeche <b>3 tarike</b> diye hain. Koi ek chal jaayega.
</div>

<h2>Tarika 1 &mdash; TEXT COPY karo (sabse pakka)</h2>
<div class="box">
  Neeche poora file ka text hai. <b>SELECT ALL</b> dabao, phir <b>COPY</b>.
  Uske baad Notes / Gmail / WhatsApp &ldquo;Saved messages&rdquo; me paste karke
  save kar lo. Text wahi hai jo file me hai.
</div>
<button class="btn" onclick="selectAll(this)">1&#65039;&#8419; SELECT ALL</button>
<button class="btn ghost" onclick="copyAll(this)">2&#65039;&#8419; COPY (pooora file)</button>
<textarea id="ta" spellcheck="false" readonly>__TEXT__</textarea>

<h2>Tarika 2 &mdash; nayi tab me kholo</h2>
<div class="box">
  Ye link nayi tab me kholta hai. Wahan browser ka apna
  <b>Download / Share</b> button chalta hai.
</div>
<a class="btn ghost" href="/view/prompts-md" target="_blank" rel="noopener">
  MD &mdash; nayi tab me kholo (text)</a>
<a class="btn ghost" href="/view/prompts-pdf" target="_blank" rel="noopener">
  PDF &mdash; nayi tab me kholo (browser PDF viewer)</a>
<a class="btn ghost" href="/view/main-pdf" target="_blank" rel="noopener">
  Poori file ka PDF &mdash; nayi tab me kholo</a>

<h2>Tarika 3 &mdash; direct download try karo</h2>
<a class="btn ghost" href="/prompts" download="PROMPTS-COPY.md">
  &#11015; PROMPTS-COPY.md download</a>
<a class="btn ghost" href="/prompts-pdf" download="PROMPTS-COPY.pdf">
  &#11015; PROMPTS-COPY.pdf download</a>
<a class="btn ghost" href="/zip" download="AI-FILM-V10.zip">
  &#11015; SAARI FILES (zip)</a>

<p class="foot">
  <a href="/">&#8592; Copy Box (prompt-wise copy)</a>
</p>

<script>
function selectAll(btn){
  const ta = document.getElementById('ta');
  ta.focus(); ta.select(); ta.setSelectionRange(0, ta.value.length);
  btn.classList.add('ok'); btn.textContent = '✅ SELECT HO GAYA — ab COPY dabao';
  try{ document.execCommand('copy'); btn.textContent = '✅ COPY HO GAYA'; }catch(e){}
  setTimeout(()=>{ btn.classList.remove('ok'); btn.textContent = '1️⃣ SELECT ALL'; }, 3000);
}
async function copyAll(btn){
  const ta = document.getElementById('ta');
  const text = ta.value;
  let ok = false;
  try{ if(navigator.clipboard){ await navigator.clipboard.writeText(text); ok = true; } }catch(e){}
  if(!ok){
    ta.focus(); ta.select(); ta.setSelectionRange(0, text.length);
    try{ ok = document.execCommand('copy'); }catch(e){}
  }
  btn.classList.add('ok');
  btn.textContent = ok ? '✅ POORA FILE COPY HO GAYA — ab paste karo'
                       : 'text select kiya — long-press → Copy';
  setTimeout(()=>{
    btn.classList.remove('ok');
    btn.textContent = '2️⃣ COPY (pooora file)';
  }, 3200);
}
</script>
</body></html>
"""


# ------------------------------------------------------------------ server
class Handler(BaseHTTPRequestHandler):
    server_version = "CopyBox/2.0"

    def log_message(self, fmt, *args):
        print("%s %s" % (self.address_string(), fmt % args), flush=True)

    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path, ctype, inline=False, filename=None):
        if not os.path.exists(path):
            self._send(404, "no file", "text/plain; charset=utf-8")
            return
        data = open(path, "rb").read()
        extra = {}
        if inline:
            extra["Content-Disposition"] = "inline"
        elif filename:
            extra["Content-Disposition"] = 'attachment; filename="%s"' % filename
        self._send(200, data, ctype, extra)

    def _save_page(self):
        md = ""
        if os.path.exists(COPY_MD):
            md = open(COPY_MD, encoding="utf-8").read()
        esc_md = html.escape(md)
        page = SAVE_PAGE.replace("__TEXT__", esc_md) \
                        .replace("__WORDS__", str(len(md.split()))) \
                        .replace("__KB__", str(round(len(md) / 1024)))
        self._send(200, page)

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path in ("/", "/steps"):
            self._send(200, build_page())
        elif path == "/health":
            self._send(200, "ok", "text/plain; charset=utf-8")
        elif path == "/all":
            self._send(200, open(MD_PATH, encoding="utf-8").read(),
                       "text/plain; charset=utf-8")
        elif re.match(r"^/prompt/[1-4]$", path):
            want = int(path.rsplit("/", 1)[1])
            hit = [u for u in read_prompts() if u["prompt_num"] == want]
            self._send(200, hit[0]["text"] if hit else "not found",
                       "text/plain; charset=utf-8")
        elif path == "/md":
            self._send(200, open(MD_PATH, "rb").read(),
                       "text/markdown; charset=utf-8",
                       {"Content-Disposition":
                        'attachment; filename="AI-FILM-PROMPTS.md"'})
        elif path == "/zip":
            import io as _io
            import zipfile
            buf = _io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(MD_PATH, "AI-FILM-PROMPTS.md")
                if os.path.exists(PDF_PATH):
                    z.write(PDF_PATH, "AI-FILM-PROMPTS.pdf")
                if os.path.exists(COPY_MD):
                    z.write(COPY_MD, "PROMPTS-COPY.md")
                if os.path.exists(COPY_PDF):
                    z.write(COPY_PDF, "PROMPTS-COPY.pdf")
                box = os.path.join(ROOT, "COPY-BOX.html")
                if os.path.exists(box):
                    z.write(box, "COPY-BOX.html")
                cdir = os.path.join(ROOT, "COPY")
                if os.path.isdir(cdir):
                    for f in sorted(os.listdir(cdir)):
                        z.write(os.path.join(cdir, f), "COPY/" + f)
            self._send(200, buf.getvalue(), "application/zip",
                       {"Content-Disposition":
                        'attachment; filename="AI-FILM-V10.zip"'})
        elif path == "/save":
            self._save_page()
        elif path == "/view/prompts-md":
            self._file(COPY_MD, "text/plain; charset=utf-8", inline=True)
        elif path == "/view/prompts-pdf":
            self._file(COPY_PDF, "application/pdf", inline=True)
        elif path == "/view/main-md":
            self._file(MD_PATH, "text/plain; charset=utf-8", inline=True)
        elif path == "/view/main-pdf":
            self._file(PDF_PATH, "application/pdf", inline=True)
        elif path == "/prompts":
            if os.path.exists(COPY_MD):
                self._send(200, open(COPY_MD, "rb").read(),
                           "text/markdown; charset=utf-8",
                           {"Content-Disposition":
                            'attachment; filename="PROMPTS-COPY.md"'})
            else:
                self._send(404, "no file")
        elif path == "/prompts-pdf":
            if os.path.exists(COPY_PDF):
                self._send(200, open(COPY_PDF, "rb").read(),
                           "application/pdf",
                           {"Content-Disposition":
                            'attachment; filename="PROMPTS-COPY.pdf"'})
            else:
                self._send(404, "no file")
        elif path == "/pdf":
            self._send(200, open(PDF_PATH, "rb").read(), "application/pdf",
                       {"Content-Disposition":
                        'attachment; filename="AI-FILM-PROMPTS.pdf"'})
        else:
            self._send(404, "not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--dump", metavar="FILE",
                    help="page ko file me likho (offline) aur exit")
    a = ap.parse_args()
    if a.dump:
        open(a.dump, "w", encoding="utf-8").write(build_page())
        print("dumped %s (%d bytes)" % (a.dump, os.path.getsize(a.dump)))
        cdir = os.path.join(ROOT, "COPY")
        if os.path.isdir(cdir):
            for k, txt in enumerate(p3_parts(), 1):
                fp = os.path.join(cdir, "prompt-3-part%d.txt" % k)
                open(fp, "w", encoding="utf-8").write(txt + "\n")
                print("  wrote %s (%d words)" % (fp, len(txt.split())))
        return
    units, md = read_units()
    print("Copy Box v2: http://%s:%d" % (a.host, a.port))
    print("  %d copy parts (%d words) from %s"
          % (len(units), len(md.split()), MD_PATH))
    for u in units:
        tag = "PROMPT %s" % u["prompt_num"] if u["prompt_num"] else u["kind"]
        print("    [%-9s] %-58s %5d words" % (tag, u["title"][:58], u["words"]))
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
