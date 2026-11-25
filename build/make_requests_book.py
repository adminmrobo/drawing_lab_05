# -*- coding: utf-8 -*-
"""8부 콘티 북 그림 요청 꾸러미(docs/image_requests_book) 생성. python3 build/make_requests_book.py
프롬프트 원본은 content_book.py(시트·완성 컷)와 make_requests.py(표지 형식)이다. build.py도 여기서 BOOK_PROMPTS를 가져가 '직접 만들어 보기'에 쓴다."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import cover, who, CH, ENDS, SKETCH, ANI, END
from content_book import S32, sheet_prompt, cut_prompt, attach_for, DONE, KEY, SIL

def it(key, page, part, alt, prompt, style): return (key, page, part, alt, prompt, style)
PG = "08_conti_book.html"
B1 = [cover("cover_08", PG, "8부 콘티 북", "연구실 벽에 32장의 작은 콘티가 네 줄로 붙어 있고, 하루가 마지막 장을 붙이며 박사·시아·모아·초파리·주판봇·평가단이 지켜보는 장면",
            "a bright lab wall covered with 32 small blank sketch sheets pinned in four rows of eight, a step stool and a box of pins.",
            [who("haru") + ", in the center on a small step stool pinning the last sheet", who("doctor") + ", on the left pointing at the first row", who("sia") + " and " + who("moa") + ", on the right holding more sheets",
             CH["fly"] + ", hovering near the top", CH["bot"] + ", at the bottom right holding one huge single sheet, comic contrast", CH["judges"] + " sitting in front"],
            "four rows of small sheets forming one long path from morning (left) to sunset (right).", "joyful, accomplished, a whole day told in pictures.")]
B2 = [it("sheet_8", PG, "8부 1단계", "하루의 하루를 8컷으로 줄인 연필 콘티 시트 — 두 줄 네 장, 침실에서 일어나는 원경부터 오른쪽 위를 바라보는 하루의 얼굴 샷까지", sheet_prompt(8, 1), "sketch"),
      it("sheet_16_1", PG, "8부 2단계", "하루의 하루 16컷 중 시트 1(1~8컷)의 연필 스케치 — 알람에 깨는 침실부터 연구소 정문 도착까지", sheet_prompt(16, 1), "sketch"),
      it("sheet_16_2", PG, "8부 2단계", "하루의 하루 16컷 중 시트 2(9~16컷)의 연필 스케치 — 로비에서 박사를 만나는 컷부터 결정하는 하루의 얼굴 샷까지", sheet_prompt(16, 2), "sketch")]
TIT = {1: "집(1~8컷) — 침실에서 현관까지", 2: "출근길(9~16컷) — 골목에서 연구소 정문까지", 3: "만남(17~24컷) — 로비에서 모두 모이기까지", 4: "업무(25~32컷) — 콘티 회의에서 완성까지"}
B3 = [it(f"sheet_32_{k}", PG, "8부 예제", f"하루의 하루 32컷 시트 {k} · {TIT[k]} 연필 스케치 — 두 줄 네 장", sheet_prompt(32, k), "sketch") for k in range(1, 5)]
def done(c): r = S32[c - 1]; return it(f"done_c{c:02d}", PG, "8부 5단계", f"완성 컷 {c} — {r[1]}({r[5]}, {r[6]}): {r[2]}", cut_prompt(c, "crop"), "anime")
B4 = [done(c) for c in [KEY, 2, 8, 11]]
B5 = [done(c) for c in [16, 18, 23, 32]]
B6 = [it("ab_sheet18", PG, "8부 5단계 비교", "비교 — 시트 3을 통째로 첨부하고 18컷만 만들라고 한 결과(여러 컷 그림이나 연필 그림체가 남는지 확인하는 그림)", cut_prompt(18, "sheet"), "anime")]
CONV = [("B01_cover", "8부 표지 (픽셀아트, 16:9)", "refs 전부", B1),
        ("B02_sheets_8_16", "8컷 시트 1장 + 16컷 시트 2장 (연필 콘티)", "첨부 없음. 16컷 시트 2는 같은 대화에서 시트 1 결과를 첨부", B2),
        ("B03_sheets_32", "32컷 시트 4장 (연필 콘티) — 같은 대화에서 차례로", "첨부 없음. 시트 2부터는 바로 앞 시트 결과를 첨부", B3),
        ("B04_done_A", "완성 컷 A — 기준 컷 31을 먼저", "컷마다 '첨부할 것' 참고(시트에서 그 컷만 잘라 낸 그림 + 등장인물 기준 그림 + 기준 컷)", B4),
        ("B05_done_B", "완성 컷 B — 아홉 명이 나오는 23·32 포함", "컷마다 '첨부할 것' 참고. 23·32컷은 기준 그림이 많으니 하루·박사·시아·모아 기준 그림을 우선", B5),
        ("B06_compare", "비교 — 시트 통째로 첨부 (새 대화)", "sheet_32_3 시트 전체 + 하루·박사 기준 그림", B6)]
ATT = {**{f"done_c{c:02d}": attach_for(c, "crop") for c in DONE}, "ab_sheet18": attach_for(18, "sheet")}
BOOK_PROMPTS = {i[0]: i for c in CONV for i in c[3]}
BOOK_CONV_OF = {i[0]: c[0] for c in CONV for i in c[3]}
BOOK_ATTACH_OF = {c[0]: c[2] for c in CONV}
# '직접 만들어 보기' B 문장 결과 그림
MAKE_B = [("sheet_32_1_b", "sheet_32_1", "Same sheet, keep the same layout. Change only: remove the character silhouette rules — draw every figure as an identical plain mannequin with no hair, glasses, robot or insect features. Still no text."),
          ("done_c31_b", "done_c31", "In a NEW conversation with NO sketch attached (only refs/haru_anime_base.png), make cut 31 from the text alone: close-up of Haru looking up with determination in a meeting room. Compare the camera and direction with done_c31.")]
DRILL_IMGS = ["d16_moa_sheet", "d17_moa_crop", "d17_moa_whole"]

HEAD_S = ("콘티 북 페이지에 넣을 연필 콘티 시트를 한 장씩 차례로 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 흑백 연필 스케치, 인물은 동그라미 머리와 십자선의 단순한 마네킹이지만 실루엣 규칙으로 누구인지 알아볼 수 있게\n"
          "- 등장인물은 모두 성인. 잠옷은 단정한 긴소매\n- 그림 안에 글자·숫자·컷 번호 금지(빈 틀과 빈 줄은 허용)\n- 둘째 장부터는 첨부한 앞 시트와 같은 그림체·선 굵기·실루엣으로")
HEAD_D = ("콘티 북 페이지에 넣을 완성 컷을 한 장씩 차례로 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 첨부한 스케치는 구도·카메라·자세만 참고하고, 그림은 깨끗한 애니풍 채색으로\n"
          "- 첨부한 캐릭터 기준 그림의 외형(얼굴·머리·색·장식)을 똑같이 지킬 것. 모두 20대 성인(박사는 30대 성인 남성)\n- 그림 안에 글자·숫자·로고 금지, 유명 애니 캐릭터와 닮으면 다시 만들 것\n- 첫 그림(31컷)을 기준 컷으로 확정한 뒤, 나머지에는 기준 컷도 함께 첨부")
README = """# 그림 요청 꾸러미 — 8부 콘티 북 「하루의 하루」

페이지는 완성되어 있고 그림 자리는 '그림 준비 중'입니다. 프롬프트 원본: `build/content_book.py`(시트·완성 컷), `build/make_requests_book.py`.

## 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 장수 | 첨부 | 비고 |
|---|---|---|---|---|
| 1 | prompts/B01_cover.md | 1 | refs 전부 | 픽셀아트 표지 |
| 2 | prompts/B02_sheets_8_16.md | 3 | 없음(16컷 시트 2는 시트 1 첨부) | 연필 콘티 |
| 3 | prompts/B03_sheets_32.md | 4 | 없음(시트 2부터 앞 시트 첨부) | **같은 대화에서 차례로** |
| 4 | prompts/B04_done_A.md | 4 | 잘라 낸 컷 + 기준 그림 | **31컷(기준 컷)을 맨 먼저** |
| 5 | prompts/B05_done_B.md | 4 | 잘라 낸 컷 + 기준 그림 + 31컷 | 23·32컷은 9명 |
| 6 | prompts/B06_compare.md | 1 | 시트 3 전체 | 새 대화, 비교용 |
| 7 | prompts/B07_make_b.md | 2 | 각 파일 설명 참고 | '직접 만들어 보기' B |
| 8 | prompts/B08_drill.md | 3 | 각 파일 설명 참고 | 연습 과제 예상 결과 |

## 잘라 내기
완성 컷은 B03에서 받은 시트에서 **그 컷 하나만 잘라**(사각형 자르기) 첨부합니다. 잘라 낸 그림이 가로 300px보다 작으면 두 배로 키워 첨부합니다. 시트를 통째로 첨부하는 것은 B06 비교 한 장뿐입니다.

## 저장 이름
`checklist.csv`의 `file` 열 그대로(png·jpg). 받으면 WebP로 바꿔 `assets/img/`에 넣습니다.
"""
if __name__ == "__main__":
    from content_book import DRILL8
    D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "image_requests_book")
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for cid, title, att, items in CONV:
        head = HEAD_S if items[0][5] == "sketch" else HEAD_D if items[0][5] == "anime" else None
        md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n"
        if head: md += f"**Genspark에 먼저 붙여 넣기 ↓**\n```\n{head}\n```\n"
        for i in items:
            n += 1; rows.append([n, cid[:3], i[0], i[2], i[5], ""])
            extra = f"\n첨부할 것: {' · '.join(ATT[i[0]])}" if i[0] in ATT else ""
            md += f"\n---\n## {i[0]} — {i[2]}\nalt: {i[3]}{extra}\n```\n{i[4]}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    md = "# B07 · '직접 만들어 보기' 비교 그림 B — " + ", ".join(m[0] for m in MAKE_B) + "\n"
    for k, base, txt in MAKE_B:
        n += 1; rows.append([n, "B07", k, "8부 직접 만들기 B", "B", ""])
        md += f"\n---\n## {k}\n방법: {'A 결과(' + base + ')를 받은 같은 대화에 이어서' if k.startswith('sheet') else '새 대화에서'}\n```\n{txt}\n```\n"
    open(os.path.join(D, "prompts", "B07_make_b.md"), "w").write(md)
    md = "# B08 · 8부 연습 과제 예상 결과 — " + ", ".join(DRILL_IMGS) + "\n"
    for d in DRILL8:
        for lab, prompt, key, alt, ar in d["prompts"]:
            n += 1; rows.append([n, "B08", key, "8부 연습 과제", lab, ""])
            md += f"\n---\n## {key} — 「{d['title']}」 {lab}\n첨부: {d['attach']}\nalt: {alt}\n```\n{prompt}\n```\n"
    open(os.path.join(D, "prompts", "B08_drill.md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "part", "style", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(README)
    print("book images", n)
