#!/usr/bin/env python3
"""
extract-frames.py — PDF se saari images nikaal ke frames/ me rakh deta hai.

Use:
    python3 tools/extract-frames.py

Kya karta hai:
  1. frames/ folder me jitni bhi .pdf files hain, sab kholta hai
  2. Har page se saari embedded images nikaalta hai
  3. Agar page image-free hai (screenshot-style PDF), to poora page render karta hai
  4. Sab ko frames/me/ me rakhta hai, saaf naam ke saath
  5. Duplicate aur chhoti images skip karta hai

Kuch install karne ki zaroorat nahi — requirements already hain.
"""

import os
import sys
import hashlib

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("pymupdf nahi mila. Chalaiye: pip install pymupdf")

from PIL import Image
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES_DIR = os.path.join(ROOT, "frames")
OUT_DIR = os.path.join(FRAMES_DIR, "me")

MIN_W = 220        # se chhoti images skip
MIN_H = 220


def sha(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()[:12]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    pdfs = []
    for base in (FRAMES_DIR, ROOT, os.path.join(ROOT, "uploads")):
        if os.path.isdir(base):
            for f in sorted(os.listdir(base)):
                if f.lower().endswith(".pdf"):
                    p = os.path.join(base, f)
                    if p not in pdfs:
                        pdfs.append(p)

    if not pdfs:
        print("Koi PDF nahi mili.")
        print(f"PDF yahan daalo: {FRAMES_DIR}")
        print("Phir dobara chalaiye.")
        return

    seen = set()
    total = 0

    for pdf_path in pdfs:
        name = os.path.splitext(os.path.basename(pdf_path))[0]
        safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)
        print(f"\n📄 {os.path.basename(pdf_path)}")

        try:
            doc = pymupdf.open(pdf_path)
        except Exception as e:
            print(f"   ✗ khul nahi payi: {e}")
            continue

        page_count = len(doc)
        print(f"   {page_count} page")

        for pno in range(page_count):
            page = doc[pno]
            imgs = page.get_images(full=True)
            pulled = 0

            for idx, info in enumerate(imgs):
                xref = info[0]
                try:
                    raw = doc.extract_image(xref)
                except Exception:
                    continue
                if not raw:
                    continue

                data = raw.get("image", b"")
                if not data:
                    continue

                h = sha(data)
                if h in seen:
                    continue

                try:
                    im = Image.open(io.BytesIO(data))
                except Exception:
                    continue

                w, hgt = im.size
                if w < MIN_W or hgt < MIN_H:
                    continue

                seen.add(h)
                total += 1
                pulled += 1

                out = os.path.join(OUT_DIR, f"{safe}_p{pno+1:02d}_{idx+1:02d}.png")
                try:
                    im.convert("RGB").save(out, "PNG")
                except Exception as e:
                    print(f"   ✗ save fail: {e}")
                    continue

            # page me embedded image nahi mili → poora page render karo
            if pulled == 0:
                try:
                    pix = page.get_pixmap(dpi=150)
                    data = pix.tobytes("png")
                    h = sha(data)
                    if h not in seen and pix.width >= MIN_W and pix.height >= MIN_H:
                        seen.add(h)
                        total += 1
                        out = os.path.join(OUT_DIR, f"{safe}_p{pno+1:02d}_full.png")
                        with open(out, "wb") as fh:
                            fh.write(data)
                        print(f"   page {pno+1}: poora page render kiya")
                except Exception as e:
                    print(f"   ✗ page render fail {pno+1}: {e}")

        doc.close()

    print(f"\n{'='*50}")
    print(f"✅ {total} images nikaali gayi")
    print(f"📁 {OUT_DIR}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
