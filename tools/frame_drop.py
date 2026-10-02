#!/usr/bin/env python3
"""
Frame Drop Box  v2
==================
Browser se apne computer/phone ki files (frames, screenshots, PDF, video, md)
seedha is workspace me daalne ke liye — aur PDF ko automatically PNG frames me
todne ke liye (taaki agent unhe padh sake).

Chalane ka tarika:
    python3 tools/frame_drop.py --host 0.0.0.0 --port 8000

Uploads yahan:   <repo>/uploads_raw/
PDF->PNG yahan:  <repo>/frames/
"""

import argparse
import email
import json
import mimetypes
import os
import re
import shutil
import sys
import threading
import time
import traceback
from email.policy import default as email_policy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, "uploads_raw")
FRAME_DIR = os.path.join(REPO_ROOT, "frames")
RENDER_DIR = os.path.join(FRAME_DIR, "_rendered")
STAMP_DIR = os.path.join(REPO_ROOT, ".dropbox_state")
MAX_BYTES = 700 * 1024 * 1024
_lock = threading.Lock()

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".heic", ".heif", ".avif", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v", ".3gp"}
PDF_EXT = {".pdf"}
DOC_EXT = {".md", ".txt", ".json", ".csv", ".srt", ".vtt"}

SAFE = re.compile(r"[^A-Za-z0-9._\- ]+")


def safe_name(name: str) -> str:
    name = os.path.basename(str(name).replace("\\", "/"))
    name = SAFE.sub("_", name).strip(" .") or "file"
    stem, ext = os.path.splitext(name)
    stem = stem[:120] or "file"
    return stem + ext.lower()


def unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path
    stem, ext = os.path.splitext(path)
    i = 2
    while True:
        cand = f"{stem}__{i}{ext}"
        if not os.path.exists(cand):
            return cand
        i += 1


def kind_of(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in PDF_EXT:
        return "pdf"
    if ext in DOC_EXT:
        return "doc"
    return "other"


def parse_multipart(body: bytes, ctype: str):
    try:
        raw = b"Content-Type: " + ctype.encode("latin-1") + b"\r\nMIME-Version: 1.0\r\n\r\n" + body
        msg = email.message_from_bytes(raw, policy=email_policy)
    except Exception as exc:
        print(f"[warn] multipart header parse failed: {exc}", flush=True)
        return []
    if not msg.is_multipart():
        return []
    out = []
    for part in msg.iter_parts():
        fname = part.get_filename()
        if not fname:
            continue
        if isinstance(fname, tuple):
            fname = fname[2] if len(fname) > 2 else "file"
        payload = part.get_payload(decode=True)
        if payload:
            out.append((str(fname), payload))
    return out


def list_dir(path, url_prefix):
    items = []
    if not os.path.isdir(path):
        return items
    for entry in sorted(os.listdir(path)):
        full = os.path.join(path, entry)
        if not os.path.isfile(full) or entry.endswith(".part"):
            continue
        items.append({
            "name": entry,
            "size": os.path.getsize(full),
            "kind": kind_of(entry),
            "url": f"{url_prefix}/{entry}",
            "mtime": os.path.getmtime(full),
        })
    return items


def list_all():
    return {
        "raw": list_dir(RAW_DIR, "/raw"),
        "frames": list_dir(FRAME_DIR, "/files"),
        "rendered": list_dir(RENDER_DIR, "/rendered"),
    }


# --------------------------------------------------------------------------- #
#  PDF -> PNG
# --------------------------------------------------------------------------- #
def render_pdfs(dpi: int = 130, only: str | None = None, force: bool = False):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            return {"error": "pymupdf install nahi hai. chalao: pip3 install pymupdf"}

    os.makedirs(RENDER_DIR, exist_ok=True)
    os.makedirs(STAMP_DIR, exist_ok=True)

    pdfs = []
    for base in (RAW_DIR, FRAME_DIR):
        if os.path.isdir(base):
            for f in sorted(os.listdir(base)):
                full = os.path.join(base, f)
                if os.path.isfile(full) and f.lower().endswith(".pdf"):
                    if only and safe_name(f) != safe_name(only):
                        continue
                    pdfs.append(full)

    results, rendered_total, errors = [], 0, []
    for pdf_path in pdfs:
        stem = safe_name(os.path.splitext(os.path.basename(pdf_path))[0])[:60]
        stamp = os.path.join(STAMP_DIR, f"{stem}.stamp")
        try:
            stat = os.stat(pdf_path)
            signature = f"{stat.st_size}:{int(stat.st_mtime)}:{dpi}"
            if not force and os.path.exists(stamp) and open(stamp).read().strip() == signature:
                existing = [f for f in os.listdir(RENDER_DIR) if f.startswith(stem + "_p")]
                if existing:
                    results.append({"pdf": os.path.basename(pdf_path), "pages": len(existing), "cached": True})
                    continue

            doc = pymupdf.open(pdf_path)
            n = doc.page_count
            mat = pymupdf.Matrix(dpi / 72.0, dpi / 72.0)
            made = []
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=mat, alpha=False)
                out = os.path.join(RENDER_DIR, f"{stem}_p{i+1:03d}.png")
                pix.save(out)
                made.append(os.path.basename(out))
            doc.close()
            with open(stamp, "w") as fh:
                fh.write(signature)
            rendered_total += len(made)
            results.append({"pdf": os.path.basename(pdf_path), "pages": n, "files": made[:3], "cached": False})
            print(f"[render] {pdf_path}: {n} pages -> {RENDER_DIR}", flush=True)
        except Exception as exc:
            errors.append({"pdf": os.path.basename(pdf_path), "error": str(exc)})
            print(f"[render-fail] {pdf_path}: {exc}", flush=True)
            traceback.print_exc()

    return {"results": results, "rendered": rendered_total, "errors": errors,
            "out_dir": RENDER_DIR, "total_pdfs": len(pdfs)}


# --------------------------------------------------------------------------- #
#  HTTP
# --------------------------------------------------------------------------- #
PAGE = r"""<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frame Drop Box</title>
<style>
  :root{--bg:#0b0f14;--card:#131a23;--card2:#182230;--line:#25313f;--txt:#e8eef6;
        --dim:#93a4b8;--acc:#22d3a6;--acc2:#38bdf8;--warn:#fbbf24;--red:#f87171}
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 600px at 50% -10%,#16283a 0%,var(--bg) 55%);
       color:var(--txt);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:18px}
  .wrap{max-width:880px;margin:0 auto}
  h1{margin:0 0 4px;font-size:21px}
  .sub{color:var(--dim);font-size:13.5px;margin-bottom:16px}
  .alert{background:#3b1d1d;border:2px solid var(--red);border-radius:14px;padding:16px 18px;margin-bottom:16px}
  .alert b{color:#fca5a5}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin-bottom:16px}
  .step{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}
  .num{flex:none;width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--acc),#0ea5a0);
       color:#04120f;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:15px}
  .step .t{flex:1;padding-top:2px}
  .step .t b{font-size:16px}
  .step .t p{margin:3px 0 0;color:var(--dim);font-size:13px}
  /* NATIVE FILE INPUT — kabhi block nahi hota */
  input[type=file]{width:100%;background:var(--card2);border:2px dashed #2f4256;border-radius:14px;
       padding:16px;color:var(--txt);font-size:15px;cursor:pointer;margin-top:9px}
  input[type=file]::file-selector-button{background:linear-gradient(135deg,var(--acc),#0ea5a0);color:#04120f;
       border:0;font-weight:800;padding:11px 18px;border-radius:10px;cursor:pointer;font-size:15px;margin-right:14px}
  #drop{border:2px dashed #2f4256;border-radius:14px;padding:26px 16px;text-align:center;cursor:pointer;
        transition:.18s;background:var(--card2);margin-top:12px}
  #drop.hot{border-color:var(--acc);background:#122a26;transform:scale(1.01)}
  #drop .big{font-size:28px;margin-bottom:6px}
  #drop b{color:var(--acc)}
  .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
  button{background:linear-gradient(135deg,var(--acc),#0ea5a0);color:#04120f;border:0;font-weight:800;
         padding:12px 18px;border-radius:10px;cursor:pointer;font-size:15px}
  button.ghost{background:transparent;color:var(--txt);border:1px solid var(--line);font-weight:600}
  button:disabled{opacity:.45;cursor:not-allowed}
  #bar{height:10px;background:#0d141c;border-radius:99px;overflow:hidden;margin-top:14px;display:none}
  #bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--acc),var(--acc2));transition:width .15s}
  #stat{color:var(--txt);font-size:14px;margin-top:10px;min-height:22px;font-weight:600}
  ul{list-style:none;padding:0;margin:0}
  li{display:flex;align-items:center;gap:12px;padding:9px 10px;border-bottom:1px solid #1b2430}
  li:last-child{border-bottom:0}
  li img{width:56px;height:56px;object-fit:cover;border-radius:8px;background:#0d141c;border:1px solid var(--line)}
  li .ic{width:56px;height:56px;display:flex;align-items:center;justify-content:center;font-size:22px;
         border-radius:8px;background:#0d141c;border:1px solid var(--line);flex:none}
  li .nm{flex:1;min-width:0}
  li .nm div:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:14px}
  li .sz{color:var(--dim);font-size:12px}
  .pill{font-size:11px;padding:3px 9px;border-radius:99px;border:1px solid var(--line);color:var(--dim);text-decoration:none}
  .ok{color:var(--acc)} .bad{color:var(--red)} .warnc{color:var(--warn)}
  .tabs{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
  .tab{padding:7px 15px;border-radius:99px;border:1px solid var(--line);cursor:pointer;font-size:13px;color:var(--dim)}
  .tab.on{background:#0e2a26;border-color:var(--acc);color:var(--acc)}
  code{background:#0d141c;padding:2px 6px;border-radius:6px;font-size:12.5px;color:var(--acc2)}
  .note{font-size:12.5px;color:var(--dim);border-left:3px solid var(--warn);padding-left:10px;margin-top:12px}
</style>
</head>
<body>
<div class="wrap">
  <h1>📥 Frame Drop Box <span style="font-size:13px;color:#22d3a6">v3</span></h1>
  <div class="sub">Frames · SS · <b>PDF</b> · Video · MD — sab yahan daalo. PDF khud-ba-khud PNG frames ban jayegi.</div>

  <div class="alert" id="alertbox">
    <b>⚠️ Abhi tak 0 file aayi hai.</b>
    <div style="margin-top:6px;font-size:14px">Neeche <b>Step 1</b> me apni PDFs / frames chuno — <b>chunte hi upload apne aap shuru ho jayega</b>, koi button dabane ki zaroorat nahi.</div>
  </div>

  <div class="card">
    <div class="step">
      <div class="num">1</div>
      <div class="t">
        <b>Yahan se files chuno</b> (ek saath saari — 4 PDFs + frames + MD)
        <p>Ye button hamesha chalta hai. Purana version iframe me silently block ho raha tha — ye fix hai.</p>
        <input type="file" id="fi" multiple accept=".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.mp4,.mov,.mkv,.webm,.md,.txt,.json,application/pdf,image/*,video/*">
      </div>
    </div>

    <div class="step">
      <div class="num">2</div>
      <div class="t">
        <b>…ya seedha drag &amp; drop karo</b> (folder bhi)
        <p>Drop karte hi upload chalu.</p>
        <div id="drop">
          <div class="big">🖼️ 📄 🎬</div>
          <b>Yahan chhod do</b> — file/PDF/video
        </div>
        <input type="file" id="di" webkitdirectory directory multiple style="margin-top:10px">
      </div>
    </div>

    <div id="bar"><i></i></div>
    <div id="stat"></div>
    <div class="row">
      <button class="ghost" id="render">📄 PDF → Frames dobara chalao</button>
      <button class="ghost" id="clr">🧹 List refresh</button>
    </div>
    <div class="note">PDF upload karte hi **automatic** PNG frames ban jaate hain (130 DPI). Kuch na ho to "PDF → Frames" dabao.</div>
  </div>

  <div class="card">
    <div class="tabs">
      <span class="tab on" data-t="raw">📦 Uploads <b id="c-raw">0</b></span>
      <span class="tab" data-t="rendered">🖼️ PDF Frames <b id="c-rendered">0</b></span>
      <span class="tab" data-t="frames">🎞️ Frames <b id="c-frames">0</b></span>
    </div>
    <ul id="list"><li style="color:var(--dim)">Abhi kuch nahi…</li></ul>
  </div>
</div>

<script>
const fi=document.getElementById('fi'), di=document.getElementById('di'), drop=document.getElementById('drop');
const bar=document.getElementById('bar'), fill=bar.querySelector('i'), stat=document.getElementById('stat');
const list=document.getElementById('list'), alertbox=document.getElementById('alertbox');
let queue=[], busy=false, view='raw';

function human(n){ if(n<1024)return n+' B'; if(n<1048576)return (n/1024).toFixed(0)+' KB';
  if(n<1073741824)return (n/1048576).toFixed(1)+' MB'; return (n/1073741824).toFixed(2)+' GB'; }

// ---- AUTO UPLOAD: select karte hi ----
fi.onchange=()=>{ if(fi.files.length){ queue=Array.from(fi.files); stat.textContent=queue.length+' file mili → upload shuru…'; upload(); } };
di.onchange=()=>{ if(di.files.length){ queue=Array.from(di.files); stat.textContent=queue.length+' file mili → upload shuru…'; upload(); } };

['dragenter','dragover'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.add('hot')}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.remove('hot')}));
drop.addEventListener('drop',ev=>{ const f=ev.dataTransfer.files; if(f.length){ queue=Array.from(f); upload(); }});
window.addEventListener('dragover',e=>e.preventDefault());
window.addEventListener('drop',e=>e.preventDefault());

document.getElementById('clr').onclick=()=>{ stat.textContent=''; refresh(); };

function upload(){
  if(busy||!queue.length){ if(!queue.length) stat.textContent='⚠️ Pehle file chuno (Step 1)'; return; }
  busy=true;
  const fd=new FormData(); queue.forEach(f=>fd.append('files',f,f.name));
  const xhr=new XMLHttpRequest(); xhr.open('POST','/upload');
  bar.style.display='block';
  xhr.upload.onprogress=e=>{ if(e.lengthComputable){
    const p=e.loaded/e.total*100; fill.style.width=p+'%';
    stat.textContent=`⬆️ Uploading… ${p.toFixed(0)}%  (${human(e.loaded)} / ${human(e.total)})`;}};
  xhr.onload=()=>{ busy=false; bar.style.display='none'; fill.style.width='0';
    try{ const r=JSON.parse(xhr.responseText||'{}');
      if(xhr.status===200){
        const ar=r.auto_render;
        let extra = ar && ar.rendered ? ` · 📄 ${ar.rendered} PDF frames bane` : (ar && ar.error ? ` · ⚠️ ${ar.error}` : '');
        stat.innerHTML='<span class="ok">✔ '+ (r.saved||[]).length +' file pahunch gayi!</span>'+extra;
        alertbox.style.display='none';
        queue=[]; fi.value=''; di.value=''; refresh();
      } else { stat.innerHTML='<span class="bad">✖ Error: '+(r.error||xhr.status)+'</span>'; }
    }catch(e){ stat.innerHTML='<span class="bad">✖ Response samajh nahi aaya</span>'; } };
  xhr.onerror=()=>{busy=false;bar.style.display='none';stat.innerHTML='<span class="bad">✖ Network error — dobara chuno</span>';};
  xhr.send(fd);
}

document.getElementById('render').onclick=async()=>{
  stat.innerHTML='⏳ PDF se frames bana raha hu…';
  try{
    const j=await (await fetch('/api/render',{method:'POST'})).json();
    if(j.error){ stat.innerHTML='<span class="bad">✖ '+j.error+'</span>'; return; }
    stat.innerHTML='<span class="ok">✔ '+j.rendered+' frames bane</span> · '+j.total_pdfs+' PDF mili · '+
      (j.errors&&j.errors.length? '<span class="bad">'+j.errors.length+' error</span>':'sab theek');
    view='rendered'; document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x.dataset.t==='rendered'));
    refresh();
  }catch(e){ stat.innerHTML='<span class="bad">✖ render fail</span>'; }
};

async function refresh(){
  try{
    const j=await (await fetch('/api/list')).json();
    const n={raw:(j.raw||[]).length, rendered:(j.rendered||[]).length, frames:(j.frames||[]).length};
    document.getElementById('c-raw').textContent=n.raw;
    document.getElementById('c-rendered').textContent=n.rendered;
    document.getElementById('c-frames').textContent=n.frames;
    if(n.raw===0 && n.rendered===0){ alertbox.style.display='block'; } else { alertbox.style.display='none'; }
    const items=j[view]||[];
    if(!items.length){ list.innerHTML='<li style="color:var(--dim)">'+(view==='raw'?'Abhi kuch upload nahi hua — Step 1 use karo':'Khali — PDF upload karo ya "PDF → Frames" dabao')+'</li>'; return; }
    list.innerHTML=items.map(f=>{
      const icon = f.kind==='image' ? `<img src="${f.url}" loading="lazy" alt="">`
        : `<div class="ic">${f.kind==='video'?'🎬':f.kind==='pdf'?'📄':f.kind==='doc'?'📝':'📦'}</div>`;
      return `<li>${icon}<div class="nm"><div>${f.name}</div><div class="sz">${human(f.size)} · ${f.kind}</div></div>`+
             `<a class="pill" href="${f.url}" target="_blank">kholo</a></li>`;
    }).join('');
  }catch(e){}
}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  t.classList.add('on'); view=t.dataset.t; refresh();});
refresh(); setInterval(refresh, 6000);
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "FrameDrop/2.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        ua = (self.headers.get("User-Agent") or "-")[:60]
        sys.stderr.write("[%s] %s | %s\n" % (time.strftime("%H:%M:%S"), fmt % args, ua))

    def _send(self, code, body: bytes, ctype="text/plain; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode(), "application/json; charset=utf-8")

    def _serve_file(self, base, path_prefix):
        name = safe_name(unquote(self.path[len(path_prefix):]))
        full = os.path.join(base, name)
        if not os.path.isfile(full):
            return self._send(404, b"not found")
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        size = os.path.getsize(full)
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            try:
                a, _, b = rng[6:].partition("-")
                start = int(a) if a else 0
                end = min(int(b) if b else size - 1, size - 1)
                length = max(0, end - start + 1)
                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(length))
                self.end_headers()
                with open(full, "rb") as fh:
                    fh.seek(start)
                    self.wfile.write(fh.read(length))
                return
            except Exception:
                pass
        with open(full, "rb") as fh:
            data = fh.read()
        return self._send(200, data, ctype, {"Accept-Ranges": "bytes"})

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        if path == "/api/list":
            return self._json(list_all())
        if path == "/healthz":
            return self._send(200, b"ok")
        if path.startswith("/raw/"):
            return self._serve_file(RAW_DIR, "/raw/")
        if path.startswith("/rendered/"):
            return self._serve_file(RENDER_DIR, "/rendered/")
        if path.startswith("/files/"):
            return self._serve_file(FRAME_DIR, "/files/")
        return self._send(404, b"not found")

    def do_HEAD(self):
        return self.do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/render":
            q = urlparse(self.path).query
            only = None
            force = False
            for kv in q.split("&"):
                if kv.startswith("only="):
                    only = unquote(kv[5:])
                if kv.startswith("force="):
                    force = kv[6:].lower() in ("1", "true", "yes")
            return self._json(render_pdfs(only=only, force=force))

        if path != "/upload":
            return self._json({"error": "unknown endpoint"}, 404)

        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            return self._json({"error": "empty body"}, 400)
        if length > MAX_BYTES + 10_000_000:
            return self._json({"error": f"body too large: {length} bytes (limit ~{MAX_BYTES // 1048576} MB/file)"}, 413)

        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype.lower():
            return self._json({"error": "expecting multipart/form-data"}, 415)

        body = bytearray()
        remaining = length
        while remaining > 0:
            chunk = self.rfile.read(min(262144, remaining))
            if not chunk:
                break
            body.extend(chunk)
            remaining -= len(chunk)

        parts = parse_multipart(bytes(body), ctype)
        if not parts:
            return self._json({"error": "multipart body me koi file nahi mili"}, 400)

        os.makedirs(RAW_DIR, exist_ok=True)
        saved, skipped = [], []
        for raw_name, payload in parts:
            try:
                if len(payload) > MAX_BYTES:
                    skipped.append({"name": raw_name, "why": "too large"})
                    continue
                name = safe_name(raw_name)
                with _lock:
                    dest = unique_path(os.path.join(RAW_DIR, name))
                    tmp = dest + ".part"
                    with open(tmp, "wb") as fh:
                        fh.write(payload)
                    os.replace(tmp, dest)
                saved.append(os.path.basename(dest))
                print(f"[saved] {dest} ({len(payload)} bytes)", flush=True)
            except Exception as exc:
                skipped.append({"name": raw_name, "why": str(exc)})
                print(f"[fail] {raw_name}: {exc}", flush=True)

        auto = None
        if any(os.path.splitext(s)[1].lower() == ".pdf" for s in saved):
            try:
                auto = render_pdfs()
            except Exception as exc:
                auto = {"error": str(exc)}

        return self._json({"saved": saved, "skipped": skipped, "auto_render": auto,
                           "dir": RAW_DIR, "rendered_dir": RENDER_DIR})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    for d in (RAW_DIR, FRAME_DIR, RENDER_DIR, STAMP_DIR):
        os.makedirs(d, exist_ok=True)

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    httpd.daemon_threads = True
    print(f"Frame Drop Box v2:  http://{args.host}:{args.port}", flush=True)
    print(f"  uploads -> {RAW_DIR}", flush=True)
    print(f"  frames  -> {RENDER_DIR}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye", flush=True)


if __name__ == "__main__":
    main()
