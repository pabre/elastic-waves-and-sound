# 탄성파와 소리 시뮬레이터

고등학교 「역학과 에너지」 Ⅲ 단원 **탄성파와 소리** 수업에서 교사가 화면에 띄워 설명하며 쓰는 시뮬레이터 모음입니다.
(교과서: 비상교육 『역학과 에너지』 85~122쪽 흐름에 맞춤)

| 소단원 | 시뮬레이터 | 파일 |
|---|---|---|
| 01 단진동 | 용수철 진자 (3D) | `shm.html` |
| 02 탄성파 | 용수철 파동 (3D) | `wave-basics.html` |
| 02 탄성파 | 반사와 투과 | `reflection.html` |
| 03 도플러 효과 | 도플러 효과 | `doppler.html` |
| 04 음파의 간섭 | 두 스피커 간섭 (3D) | `interference.html` |
| 04 음파의 간섭 | 소음 제거 | `noise-cancel.html` |
| 05 정상파 | 정상파 만들기 | `standing-wave.html` |
| 05 정상파 | 가상 악기 | `instruments.html` |
| 05 정상파 | 공기 기둥 공명 | `resonance-tube.html` |

## 사용법

- 공통 단축키: `Space` 재생·정지, `1`~`9` 장면, `F` 전체 화면
- 소리는 화면을 한 번 누른 뒤부터 나옵니다(브라우저 정책).
- 3D 시뮬레이터는 three.js를 CDN에서 불러오므로 인터넷 연결이 필요합니다.

## 구조

- 각 `*.html`은 외부 파일 없이 혼자 동작하는 한 장짜리 페이지입니다(Claude 아티팩트 형식).
- `build.py`가 문서 골격(`<!doctype html>` 등)을 붙이고 목록 링크를 사이트 안 경로로 바꿔 `_site/`를 만듭니다.
- `main` 브랜치에 올리면 GitHub Actions(`.github/workflows/pages.yml`)가 `_site/`를 GitHub Pages로 배포합니다.

내 컴퓨터에서 미리 보기:

```bash
python build.py
python -m http.server 8000 --directory _site
```
