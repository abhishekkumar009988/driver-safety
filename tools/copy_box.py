#!/usr/bin/env python3
"""
Copy Box — tap-to-copy page for the four prompts inside AI-FILM-PROMPTS.md.

Opens on the phone, four big COPY buttons, one tap each. Reads the prompts
straight out of the markdown every time the page loads, so it can never go
stale when the prompts are edited.

Routes:
  /                 the tap-to-copy page
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

PROMPT_RE = re.compile(r"^#\s+([1-4]\ufe0f?\u20e3?)\s*PROMPT\s*([1-4])\b(.*)$")
FENCE_RE = re.compile(r"^```(\w*)\s*$")


def read_prompts():
    """-> list of dicts: num, title, sub, text"""
    try:
        md = open(MD_PATH, encoding="utf-8").read()
    except OSError:
        return []
    lines = md.split("\n")
    heads = {}                      # line index -> (num, title)
    for i, ln in enumerate(lines):
        m = PROMPT_RE.match(ln.strip())
        if m:
            heads[i] = (m.group(2), ln.strip().lstrip("# ").strip())

    out, cur = [], None
    in_code = False
    buf = []
    code_start = 0
    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln.strip()):
            if not in_code:
                in_code = True
                buf = []
                code_start = i
            else:
                in_code = False
                best = None
                for hl, val in heads.items():
                    if hl < code_start and (best is None or hl > best):
                        best = hl
                if best is not None and len("\n".join(buf).strip()) > 400:
                    num, title = heads[best]
                    sub = ""
                    for j in range(best + 1, min(best + 6, len(lines))):
                        s = lines[j].strip()
                        if s and not s.startswith("#"):
                            sub = s.strip("> ").strip()
                            break
                    out.append({"num": num, "title": title,
                                "sub": sub, "text": "\n".join(buf).strip()})
                    del heads[best]
            continue
        if in_code:
            buf.append(ln)
    out.sort(key=lambda d: int(d["num"]))
    return out


PAGE = """<!doctype html>
<html lang="hi"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COPY BOX &mdash; AI-FILM-PROMPTS v9</title>
<style>
  :root{
    --bg:#0d1117; --card:#161b22; --line:#2a3038; --ink:#e8edf3;
    --soft:#9aa7b4; --acc:#e8890c; --acc2:#ffb454; --ok:#2ea043; --bad:#d1242f;
  }
  *{box-sizing:border-box; -webkit-tap-highlight-color:transparent}
  body{margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
    "Noto Sans",sans-serif; padding:16px 14px 60px}
  h1{font-size:22px; margin:2px 0 4px; color:var(--acc2); letter-spacing:.3px}
  .kicker{color:var(--soft); font-size:13.5px; margin:0 0 14px}
  .steps{background:var(--card); border:1px solid var(--line); border-radius:12px;
    padding:12px 14px; font-size:14px; margin:0 0 18px}
  .steps b{color:var(--acc)}
  .warn{border-left:3px solid var(--bad); margin:12px 0 20px; padding:8px 12px;
    background:#1f1214; border-radius:0 10px 10px 0; font-size:14px; color:#ffc9c9}
  .card{background:var(--card); border:1px solid var(--line); border-radius:14px;
    margin:0 0 16px; overflow:hidden}
  .head{padding:14px 16px 10px}
  .num{display:inline-block; background:#1c2530; color:var(--acc2); font-weight:700;
    font-size:12.5px; padding:3px 9px; border-radius:99px; margin-bottom:8px}
  .title{font-size:17px; font-weight:700; margin:0 0 3px}
  .sub{color:var(--soft); font-size:13.5px; margin:0}
  .btn{display:block; width:calc(100% - 32px); margin:12px 16px 14px;
    border:0; border-radius:12px; padding:16px; font-size:17px; font-weight:700;
    background:var(--acc); color:#17130a; cursor:pointer; letter-spacing:.3px}
  .btn:active{transform:scale(.985)}
  .btn.ok{background:var(--ok); color:#fff}
  .btn.bad{background:var(--bad); color:#fff}
  details{margin:0 16px 16px}
  summary{color:var(--soft); font-size:13.5px; cursor:pointer; padding:6px 0}
  pre{margin:8px 0 0; background:#0b0f14; border:1px solid var(--line);
    border-radius:10px; padding:12px; font:12px/1.45 ui-monospace,SFMono-Regular,
    Menlo,monospace; color:#c9d5e1; max-height:46vh; overflow:auto;
    white-space:pre-wrap; word-break:break-word; user-select:text}
  .foot{color:var(--soft); font-size:12.5px; text-align:center; margin-top:24px;
    line-height:1.7}
  a{color:var(--acc2)}
</style></head><body>
<h1>COPY BOX</h1>
<p class="kicker">AI-FILM-PROMPTS &middot; MASTER v9 &middot; tumhara fixed prompt system</p>

<div class="steps">
  <b>Kaise use karna hai:</b><br>
  1. PROMPT 1 copy karo &rarr; AI ko do &rarr; neeche apni kahani likho<br>
  2. Uske baad PROMPT 2 &rarr; phir PROMPT 3 &rarr; sabse aakhir me PROMPT 4<br>
  <b>Ek ke baad ek. Jaldi mat karo.</b>
</div>

<div class="warn">
  AI 2nd step me hi video prompt banane lage to usse bolo:
  <b>&ldquo;Step 3 abhi nahi. Sirf portraits do.&rdquo;</b>
</div>
__CARDS__
<p class="foot">
  <a href="/pdf">PDF download</a> &nbsp;&middot;&nbsp; <a href="/md">Markdown download</a><br>
  plain text: <a href="/prompt/1">P1</a> &middot; <a href="/prompt/2">P2</a> &middot;
  <a href="/prompt/3">P3</a> &middot; <a href="/prompt/4">P4</a><br>
  Fixed file: <b>AI-FILM-PROMPTS.md</b> (v9) &mdash; purani file PURANI-FILES/ me hai.
</p>
<script>
async function doCopy(i, btn){
  const el = document.getElementById('t'+i);
  const text = el.textContent;
  let ok = false;
  try{
    if(navigator.clipboard && window.isSecureContext){
      await navigator.clipboard.writeText(text); ok = true;
    }
  }catch(e){ ok = false; }
  if(!ok){
    const ta=document.createElement('textarea');
    ta.value=text; ta.setAttribute('readonly','');
    ta.style.position='fixed'; ta.style.top='-1000px'; ta.style.opacity='0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    try{ ok = document.execCommand('copy'); }catch(e){ ok=false; }
    document.body.removeChild(ta);
  }
  if(ok){
    btn.classList.add('ok'); btn.textContent='\u2705 COPIED \u2014 ab AI me paste karo';
  }else{
    btn.classList.add('bad'); btn.textContent='Neeche text select kiya \u2014 copy dabao';
    const r=document.createRange(); r.selectNodeContents(el);
    const s=window.getSelection(); s.removeAllRanges(); s.addRange(r);
    el.closest('details') && (el.closest('details').open = true);
  }
  setTimeout(function(){
    btn.classList.remove('ok','bad');
    btn.textContent='\U0001F4CB COPY PROMPT '+i;
  }, 3200);
}
</script>
</body></html>
"""

CARD = """<div class="card">
  <div class="head">
    <span class="num">PROMPT __NUM__</span>
    <p class="title">__TITLE__</p>
    <p class="sub">__SUB__</p>
  </div>
  <button class="btn" onclick="doCopy(__NUM__, this)">&#128203; COPY PROMPT __NUM__</button>
  <details><summary>Poora prompt dekho (__WORDS__ words)</summary>
    <pre id="t__NUM__">__TEXT__</pre>
  </details>
</div>"""


def build_page():
    prompts = read_prompts()
    cards = []
    for p in prompts:
        title = re.sub(r"^[1-4]\ufe0f?\u20e3?\s*PROMPT\s*[1-4]\s*[-\u2014]\s*",
                       "", p["title"]).strip()
        cards.append(
            CARD.replace("__NUM__", p["num"])
                .replace("__TITLE__", html.escape(title or p["title"]))
                .replace("__SUB__", html.escape(p["sub"]))
                .replace("__WORDS__", str(len(p["text"].split())))
                .replace("__TEXT__", html.escape(p["text"])))
    return PAGE.replace("__CARDS__", "\n".join(cards) if cards
                        else "<p>AI-FILM-PROMPTS.md nahi mili.</p>")


class Handler(BaseHTTPRequestHandler):
    server_version = "CopyBox/1.0"

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

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path == "/":
            self._send(200, build_page())
        elif path == "/health":
            self._send(200, "ok", "text/plain; charset=utf-8")
        elif path == "/md":
            if os.path.exists(MD_PATH):
                self._send(200, open(MD_PATH, "rb").read(),
                           "text/markdown; charset=utf-8",
                           {"Content-Disposition":
                            'attachment; filename="AI-FILM-PROMPTS.md"'})
            else:
                self._send(404, "no md")
        elif re.match(r"^/(prompt|p)/[1-4]$", path):
            want = path.rsplit("/", 1)[1]
            hit = [x for x in read_prompts() if x["num"] == want]
            if hit:
                self._send(200, hit[0]["text"], "text/plain; charset=utf-8")
            else:
                self._send(404, "no prompt")
        elif path == "/pdf":
            if os.path.exists(PDF_PATH):
                self._send(200, open(PDF_PATH, "rb").read(),
                           "application/pdf",
                           {"Content-Disposition":
                            'attachment; filename="AI-FILM-PROMPTS.pdf"'})
            else:
                self._send(404, "no pdf")
        else:
            self._send(404, "not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--host", default="0.0.0.0")
    a = ap.parse_args()
    found = read_prompts()
    print("Copy Box v1: http://%s:%d" % (a.host, a.port))
    print("  found %d prompts in %s" % (len(found), MD_PATH))
    for p in found:
        print("    prompt %s: %s (%d words)" % (p["num"], p["title"],
                                                len(p["text"].split())))
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
