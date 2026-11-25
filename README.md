# 구조 먼저 그리기 연구실 05 · 콘티 편 — 콘티 먼저, 컷은 그다음

이야기를 여덟 컷으로 나누고, 카메라·컷 잇기·자세를 정한 콘티를 먼저 짠 뒤, 그 콘티를 근거로 그림 생성 AI에게 컷 그림을 만들게 하는 방법을 실험으로 익힙니다. 콘티·컷 실패 8종 진단, 실전 연습장, 인쇄용 빈 콘티 양식까지.

- 사이트: https://adminmrobo.github.io/drawing_lab_05/
- 글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 구성
| 부 | 페이지 | 내용 |
|---|---|---|
| 목차 | `index.html` | 세 줄 요약, 예시 콘티 8컷, 편 목록, 전체 흐름, 한눈에 보는 기준값, 등장인물, 원리와 출처 |
| 1부 | `01_beats.html` | 콘티의 뼈대 — 네 덩어리, 세 줄, 감정 곡선, 썸네일 (모델 모아) |
| 2부 | `02_camera.html` | 카메라 — 샷 크기, 눈높이 선과 소실점, 앵글, 시선 여백 (모델 하루) |
| 3부 | `03_flow.html` | 컷 잇기 — 가상선, 움직임 화살표, 컷 길이와 프레임, 시선 잇기 (모델 시아) |
| 4부 | `04_pose.html` | 포즈와 연기 — 중심축, 무게중심, 소품 무게, 실루엣 (모델 박사·하루) |
| 5부 | `05_ai_cuts.html` | AI로 컷 만들기 — 여덟 조각, 기준 시트, 밑그림 강도, 기준 컷 먼저 |
| 6부 | `06_failure_lab.html` | 실패 사례 실험실 — 진단 순서, 실패 8종, 나이 쏠림 막기 |
| 7부 | `practice/index.html` | 실전 연습장 — 콘티 작업대, 카메라 촬영장, 컷 문장 공방, 진단 데스크 |
| 부록 | `practice/template.html` | 인쇄용 빈 콘티 양식(가로 A4) |

## 원리와 출처
사용자가 제공한 참고 이미지 5장(8컷 그림 콘티 템플릿, 원근과 인물 크기 도해, 어린이·성인 얼굴 비교, 중심축 도해, 캐릭터 일관성 기준 시트)에서 원리만 가져왔고, 그림·문장·도식·구성은 옮기지 않았습니다. 그 밖의 출처(Katz 1991, Bordwell·Thompson·Smith 2019, Thomas·Johnston 1981, Loomis 1951, Meng 외 2022, Rombach 외 2022, Lugmayr 외 2022, Ruiz 외 2023)는 각 페이지 바닥글에 있습니다. 숫자는 모두 설명용 예시값입니다.

## 그림
그림은 아직 들어오지 않았습니다(페이지는 '그림 준비 중' 자리로 완성 상태). 요청 꾸러미:
- `docs/image_requests/` — 표지 8 · 본문 11 · 실패 8 (27장)
- `docs/image_requests_make/` — '직접 만들어 보기' 비교 그림 12장(A 결과를 받은 뒤)
- `docs/image_requests_drill/` — 연습 과제 예상 결과 17장
- 한꺼번에: `docs/구조먼저그리기연구실_05_콘티편_그림요청.zip`

## 빌드와 점검
```
python3 build/build.py && python3 build/check_numbers.py && python3 build/make_og.py
python3 -m http.server 8765 &   # 아래 두 점검용
python3 build/check_pages.py && python3 build/check_missions.py
```
작성 방침: `docs/WRITING_POLICY.md` · 페르소나 검사: `docs/persona_review.md`

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions).
