#!/usr/bin/env bash
# get_fonts.sh — fetch every font md2pdf.py needs into /home/user/fonts
#
# The sandbox resets installed packages and loose folders between turns, so
# this script is kept in the repo and re-run whenever the PDF build complains
# about a missing font. Safe to run any number of times.
set -u
DEST="${1:-/home/user/fonts}"
mkdir -p "$DEST"
B="repos/notofonts/noto-fonts/contents/hinted/ttf"
SYS="/usr/share/fonts/truetype/dejavu"
ok=0; fail=0

have() { [ -s "$DEST/$1" ] && echo "  -- $1 already here" && ok=$((ok+1)) && return 0; return 1; }

fetch() {  # repo path  filename
  have "$2" && return
  if gh api "$B/$1/$2" -H "Accept: application/vnd.github.raw" > "$DEST/$2" 2>/dev/null \
     && [ -s "$DEST/$2" ]; then
    echo "  ok $2"; ok=$((ok+1))
  else
    echo "  FAIL $2"; rm -f "$DEST/$2"; fail=$((fail+1))
  fi
}

copy() {  # system file  filename
  have "$2" && return
  if cp "$SYS/$1" "$DEST/$2" 2>/dev/null; then echo "  ok $2 (system)"; ok=$((ok+1));
  else echo "  FAIL $2"; fail=$((fail+1)); fi
}

echo "fonts -> $DEST"
fetch NotoSans        NotoSans-Regular.ttf
fetch NotoSans        NotoSans-Bold.ttf
fetch NotoSans        NotoSans-Italic.ttf
fetch NotoSans        NotoSans-BoldItalic.ttf
fetch NotoSansMono    NotoSansMono-Regular.ttf
fetch NotoSansMono    NotoSansMono-Bold.ttf
fetch NotoSansSymbols2 NotoSansSymbols2-Regular.ttf

if [ ! -s "$DEST/OpenMoji-black-glyf.ttf" ]; then
  if gh api repos/hfg-gmuend/openmoji/contents/font/OpenMoji-black-glyf/OpenMoji-black-glyf.ttf \
       -H "Accept: application/vnd.github.raw" > "$DEST/OpenMoji-black-glyf.ttf" 2>/dev/null \
     && [ -s "$DEST/OpenMoji-black-glyf.ttf" ]; then
    echo "  ok OpenMoji-black-glyf.ttf"; ok=$((ok+1))
  else
    echo "  (skipped OpenMoji — emoji fall back to symbols)"; rm -f "$DEST/OpenMoji-black-glyf.ttf"
  fi
else
  echo "  -- OpenMoji already here"; ok=$((ok+1))
fi

copy DejaVuSans.ttf       DejaVuSans.ttf
copy DejaVuSans-Bold.ttf  DejaVuSans-Bold.ttf
copy DejaVuSansMono.ttf   DejaVuSansMono.ttf
copy DejaVuSansMono-Bold.ttf DejaVuSansMono-Bold.ttf

echo "done: $ok ready, $fail failed"
exit 0
