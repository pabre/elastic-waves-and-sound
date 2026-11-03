"""시뮬레이터 HTML을 GitHub Pages용 완전한 웹 문서로 바꿔 _site/ 폴더에 만든다.

원본 HTML은 Claude 아티팩트 형식(<!doctype>, <html>, <head> 없이 내용만 있음)이라
그대로 올리면 브라우저가 호환(quirks) 모드로 그린다. 여기서 문서 골격을 붙이고,
목록 페이지의 아티팩트 링크를 사이트 안 상대 경로로 바꾼다.

    python build.py
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_site"

# 목록(index.html) 카드가 가리키는 아티팩트 → 사이트 안 파일
ARTIFACT_TO_FILE = {
    "VsJd2zRQ7gr9AZd1X4xsrQ": "shm.html",
    "6V3sBxRdRToyHfeVZcb7b6": "wave-basics.html",
    "3zqejLTFnanX5BfhxgHNgv": "reflection.html",
    "G9M8EbMEvKXLnHLW9w7VSm": "doppler.html",
    "2TuyLaTnnJt9yD3HWfJ81f": "interference.html",
    "SGdBbu727LpyutkRSQpwPM": "noise-cancel.html",
    "G1Cr7BwHPi2dHhNTPmgDVJ": "standing-wave.html",
    "SNE477yRRXQbWR8k28iBrk": "instruments.html",
    "9oxpRD4K7t94JHFcPuGVhb": "resonance-tube.html",
}

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%230b6b70'/%3E"
    "%3Cpath d='M4 16c3-7 6-7 8 0s5 7 8 0 5-7 8 0' fill='none' stroke='white' "
    "stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E"
)

HEAD = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="{FAVICON}">
<style>
body {{ margin: 0; }}
a.tag {{ text-decoration: none; transition: border-color .15s, color .15s; }}
a.tag:hover {{ color: var(--accent); border-color: var(--accent); }}
/* 휴대폰: 단원 표시는 숨겨도 목록으로 가는 '←' 단추는 남긴다 */
@media (max-width: 600px) and (orientation: portrait), (max-height: 500px) and (orientation: landscape) {{
  a.tag {{ display: inline-flex !important; align-items: center; justify-content: center; min-width: 30px; min-height: 30px; padding: 0 8px; font-size: 16px; font-weight: 700; color: var(--ink); }}
  a.tag .tag-txt {{ display: none; }}
}}
</style>
"""

ARTIFACT_META = '<meta name="claude:viewport-fit-sides" content="cover">\n'
TAG_RE = re.compile(r'<span class="tag">(.*?)</span>')
CARD_RE = re.compile(
    r'href="https://claude\.ai/artifact/([A-Za-z0-9]+)" target="_blank" rel="noopener"'
)


def card_link(m: re.Match) -> str:
    artifact_id = m.group(1)
    if artifact_id not in ARTIFACT_TO_FILE:
        raise SystemExit(f"index.html: 모르는 아티팩트 링크 {artifact_id}")
    return f'href="{ARTIFACT_TO_FILE[artifact_id]}"'


def build_page(src: pathlib.Path) -> str:
    body = src.read_text(encoding="utf-8")
    if body.lstrip().lower().startswith("<!doctype"):
        return body
    body = body.replace(ARTIFACT_META, "", 1)
    if src.name == "index.html":
        body = CARD_RE.sub(card_link, body)
    else:
        # 제목 위 단원 표시를 목록으로 돌아가는 링크로
        body, n = TAG_RE.subn(
            r'<a class="tag" href="./" title="시뮬레이터 목록으로" aria-label="시뮬레이터 목록으로">←<span class="tag-txt"> \1</span></a>', body, count=1
        )
        if n != 1:
            raise SystemExit(f"{src.name}: 단원 표시(.tag)를 찾지 못함")
    return HEAD + body + "\n</html>\n"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    pages = sorted(ROOT.glob("*.html"))
    for src in pages:
        (OUT / src.name).write_text(build_page(src), encoding="utf-8", newline="\n")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    missing = set(ARTIFACT_TO_FILE.values()) - {p.name for p in pages}
    if missing:
        raise SystemExit(f"없는 파일: {sorted(missing)}")
    print(f"{len(pages)}개 페이지 → {OUT}")


if __name__ == "__main__":
    main()
