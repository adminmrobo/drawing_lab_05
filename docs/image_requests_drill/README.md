# 그림 요청 꾸러미 3 — '프롬프트 연습 과제' 예상 결과 (17장)

부마다 연습 과제 2개(모두 12개)의 **예상 결과 그림**입니다. 페이지의 과제 프롬프트와 이 요청문의 프롬프트는 같습니다(원본: `build/content_drill.py`).

## 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
| 1 | prompts/D01_part1.md | 3 | d1은 첨부 없음 · d2는 refs/haru_anime_base.png, refs/haru_sheet.png |
| 2 | prompts/D02_part2.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png (+ d4는 sia·moa anime_base) |
| 3 | prompts/D03_part3.md | 4 | refs/sia_anime_base.png, refs/sia_sheet.png, refs/haru_anime_base.png, refs/haru_sheet.png |
| 4 | prompts/D04_part4.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png |
| 5 | prompts/D05_part5.md | 2 | refs/haru_anime_base.png, refs/haru_sheet.png |
| 6 | prompts/D06_part6.md | 2 | f2_flip·f6_drift(사이트 assets/img/), refs/sia_anime_base.png, refs/haru_sheet.png |

## 주의
- 두 장이 짝인 과제(d2·d5·d6·d8·d10)는 **같은 대화에서 차례로** 만듭니다. d3의 두 장은 **서로 다른 새 대화**에서 만듭니다.
- d12_fix_bun은 그림 생성이 아니라 **부분 수정(영역 칠하기)** 기능으로 만듭니다. 칠하는 곳: 둘째·셋째 컷의 머리와 후드(얼굴·손·배경 제외).
- D06(d11·d12)은 꾸러미 1의 실패 그림 f2_flip·f6_drift를 **받은 뒤에** 요청합니다.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png·jpg).
