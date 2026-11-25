# -*- coding: utf-8 -*-
"""다시 만들 그림 요청 꾸러미(docs/image_requests_retry) 생성. python3 build/make_requests_retry.py
2026-11-26 결과에서 배운 것: ① 'Same image. Change only' 한 줄 요청은 같은 대화의 앞 그림·참고 그림을 따라가 설정 시트나 다른 인물이 나오기 쉽다 → 새 대화에서 전체 프롬프트로.
② 고칠 그림을 첨부하면 그 모양을 그대로 따라 그린다(f2_fixed) → 고칠 그림은 첨부하지 않는다. ③ 원근은 '눈이 한 가로선 위'를 더 구체적으로 적는다."""
import os, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import body, fail, who, LAB, ANI, END

EYE = ("Camera height equals the standing eye height of the people, so the horizon line — where the corridor's floor and ceiling lines converge — is at exactly the same height as every person's eyes. "
       "All pairs of eyes lie on ONE straight horizontal line across the whole image, the nearest person's eyes included. Nearer people look bigger because their bodies extend further BELOW that line (their feet are lower in the frame); their heads rise only slightly above it.")
ONLY = "Only the characters described below appear; no other people."
R1 = [
 body("b1_moa_emotion_b", "01_beats.html", "1부 직접 만들기 B(다시)", "B 결과 — 같은 가슴 위 크기의 모아 세 장이 모두 같은 무난한 미소", "16:9",
      "Three panels side by side, the same chest-up framing in each, of " + who("moa") + ". All three panels show exactly the same pleasant neutral smile, the same gaze straight ahead, no other emotion.",
      ONLY + " Same lighting from the upper left in all three panels. Thin light gray borders between panels."),
 body("b2_haru_shots_b", "02_camera.html", "2부 직접 만들기 B(다시)", "B 결과 — 다섯 장 모두 같은 크기의 하루 전신", "16:9",
      "Five vertical panels side by side, the same character " + who("haru") + " in the same calm pose and the same bright lab hallway. All five panels use exactly the same framing: full body, head to toe, the same size in every panel.",
      ONLY + " Same light from the upper left in all panels. Thin light gray borders between panels.", bg=None),
 body("b2_eyelevel", "02_camera.html", "2부 2단계(다시)", "낮의 연구소 긴 복도에서 키가 비슷한 연구원 다섯 명이 안쪽으로 멀어지며 서 있는 그림 — 멀수록 작아지고, 다섯 명의 눈이 한 가로선 위에 나란함", "16:9",
      "A long, bright research institute corridor in one-point perspective, the vanishing point at the far end in the center. " + who("haru") + " stands closest on the left, her full body visible; four more adult researchers in white lab coats over modest shirts and long trousers, all the same real height, stand farther and farther down the corridor on the same floor.",
      EYE + " " + ONLY, bg=None),
 body("b2_eyelevel_b", "02_camera.html", "2부 직접 만들기 B(다시)", "B 결과 — 같은 복도에서 멀고 가까운 것과 상관없이 다섯 명이 모두 같은 크기로 그려져 먼 사람이 거인처럼 보임", "16:9",
      "The same long bright research institute corridor in one-point perspective. " + who("haru") + " stands closest on the left; four adult researchers in white lab coats over modest shirts and long trousers stand farther down the corridor.",
      "Intentional mistake for a teaching page: draw all five people at exactly the SAME size regardless of distance, so the far ones look like giants compared with the corridor. " + ONLY, bg=None),
]
R2 = [
 body("b3_direction_b", "03_flow.html", "3부 직접 만들기 B(다시)", "B 결과 — 왼쪽 컷은 오른쪽으로 걷는 시아, 오른쪽 컷은 같은 길을 왼쪽으로 걷는 시아의 옆모습", "16:9",
      "Two panels side by side on the same sunny path in front of " + LAB + ". Left panel: full body side view of " + who("sia") + " walking toward the RIGHT side of the frame. Right panel: the same Sia, full body side view, walking toward the LEFT side of the frame.",
      ONLY + " Same afternoon light from the left in both panels. Thin light gray border between panels.", bg=None),
 body("b3_eyeline_b", "03_flow.html", "3부 직접 만들기 B(다시)", "B 결과 — 왼쪽 컷의 하루는 오른쪽 위를 보는데, 오른쪽 하늘 컷의 작은 날개는 왼쪽 아래에 있음", "16:9",
      "Two panels side by side. Left panel: waist-up shot of " + who("haru") + " standing on the LEFT third of the frame inside a bright corridor, looking toward the UPPER RIGHT out of a large window. "
      "Right panel: the view out of the window — blue sky above a rooftop edge, no people, and a tiny pair of translucent insect wings glinting in the LOWER LEFT corner of the frame.",
      "The wings are tiny, the size of a fingernail in the frame. Thin light gray border between panels.", bg=None),
 body("b4_doctor_axis_b", "04_pose.html", "4부 직접 만들기 B(다시)", "B 결과 — 박사의 세 자세 중 가운데 문 밀기 자세가 몸은 곧게 선 채 팔만 뻗은 모습", "16:9",
      "Three full-body poses of " + who("doctor") + " side by side, an adult man with adult proportions (not chibi). Left: standing straight and relaxed. Middle: in front of a large heavy metal door, his body perfectly upright and stiff like a pole, feet together, only his arms reaching out to touch the door. Right: walking and twisting to look back over his shoulder.",
      ONLY + " Anime illustration, not pixel art. Light from the upper left."),
 body("b4_haru_prop", "04_pose.html", "4부 3단계(다시)", "하루가 물건을 든 두 장면 — 왼쪽은 가벼운 우산을 들고 곧게 선 하루, 오른쪽은 무거운 실험 상자를 앞으로 안고 상체를 뒤로 기울인 하루", "16:9",
      "Two full-body side-view panels of " + who("haru") + ". Left: holding a closed light folding umbrella loosely at her side, standing upright and relaxed. "
      "Right: carrying a big heavy cardboard lab box in front of her chest with both arms; her upper body clearly leans BACKWARD behind her hips to counterbalance the weight (not bending forward over the box), knees slightly bent, feet apart, arms strained.",
      ONLY + " Light from the upper left. Thin light gray border between panels."),
 body("b4_haru_prop_b", "04_pose.html", "4부 직접 만들기 B(다시)", "B 결과 — 무거운 상자를 안고도 몸을 곧게 세운 하루(상자가 가벼워 보임)", "16:9",
      "Two full-body side-view panels of " + who("haru") + ". Left: holding a closed light folding umbrella, standing upright. Right: carrying a big heavy cardboard lab box in front of her with both arms while standing perfectly straight and upright, no lean, legs straight.",
      ONLY + " Light from the upper left. Thin light gray border between panels."),
]
R3 = [
 body("f2_fixed", "06_failure_lab.html", "6부 고치기(다시)", "고치기 결과 — 두 컷 모두 시아가 같은 길을 화면 오른쪽으로 걸어 방향이 이어짐", "16:9",
      "Two consecutive panels side by side on the same sunny path in front of " + LAB + ". In BOTH panels, full body side view of " + who("sia") + " walking toward the RIGHT side of the frame — the same screen direction in both cuts; in the right panel she is a few steps further along.",
      ONLY + " Same afternoon light from the left in both panels. Thin light gray border between panels.", bg=None),
 body("f6_fixed", "06_failure_lab.html", "6부 고치기(다시)", "고치기 결과 — 세 컷 모두 정수리 번 두 개, 앞머리 가운데 남색 줄, 라벤더 후드의 같은 하루", "16:9",
      "Three story panels side by side of " + who("haru") + ": running toward the right in a bright lab; looking out a window; pushing a door. "
      "In every panel she has EXACTLY TWO round hair buns on top of her head and ONE thick navy streak down the CENTER of her bangs (not a headband), and the same lavender hoodie under an open white lab coat — identical to the attached reference sheet.",
      ONLY + " Thin light gray borders between panels.", bg=None),
 body("d4_corridor_eye", "02_camera.html", "2부 연습 과제 d2(다시)", "복도 앞·가운데·안쪽의 하루·시아·모아 — 멀수록 작아지고 세 사람의 눈이 한 가로선 위에 있음", "16:9",
      "A long bright research institute corridor in one-point perspective, vanishing point at the far end in the center. " + who("haru") + " stands closest on the left with her full body visible, " + who("sia") + " stands in the middle distance, " + who("moa") + " stands far down the corridor. All three are the same real height and stand on the same floor.",
      EYE + " " + ONLY, bg=None),
]
CONV = [("R01_part1_2", "1·2부 다시 만들기 (모두 새 대화)", "refs/moa_anime_base.png·moa_sheet.png (b1) / refs/haru_anime_base.png·haru_sheet.png (b2)", R1),
        ("R02_part3_4", "3·4부 다시 만들기 (모두 새 대화)", "해당 캐릭터의 anime_base·sheet (시아·하루·박사)", R2),
        ("R03_fix", "6부 고치기·연습 과제 다시 (새 대화, 고칠 그림 첨부 금지)", "f2_fixed: refs/sia_anime_base.png · f6_fixed: refs/haru_sheet.png + haru_anime_base.png · d4: 하루·시아·모아 anime_base", R3)]
HEAD = ("해설 페이지에 넣을 그림을 다시 만들려고 해. 아래 규칙을 지켜 줘.\n- **그림 하나마다 새 대화**에서 만들 것(앞 그림을 이어 고치지 말 것)\n- 비율 16:9, 가로 1920px 이상\n"
        "- 첨부한 참고 이미지의 캐릭터 외형(얼굴·머리·색·장식)을 똑같이 지킬 것. 프롬프트에 없는 인물은 넣지 말 것\n- 설정 시트(정면·옆·뒤 나란히)나 픽셀 스프라이트로 바꾸지 말고, 프롬프트에 적힌 패널 구성 그대로\n"
        "- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·짧은 하의·스타킹·교복 느낌·어려 보이는 얼굴 금지\n- 그림 안에 글자·숫자·로고 금지")
README = """# 다시 만들 그림 요청 꾸러미 (2026-11-26)

첫 결과 56장 중 요청과 다르게 나온 그림을 다시 요청합니다. **받으면 같은 이름의 그림을 바꿔 넣습니다.** 다시 만들어도 다르게 나오면 그대로 주세요 — 페이지에 '두 번 시도' 결과로 적습니다.

## 이번 요청에서 바꾼 것
1. **그림 하나 = 새 대화.** 'Same image. Change only …' 한 줄 요청이 같은 대화의 앞 그림을 따라가 설정 시트·다른 인물·픽셀 스프라이트가 나왔기 때문입니다. 모든 프롬프트를 처음부터 다 적었습니다.
2. **고칠 그림은 첨부하지 않습니다.** f2를 첨부했더니 그대로 따라 그렸습니다(새 대화의 d11은 성공).
3. **원근은 '모든 사람의 눈이 한 가로선 위'를 구체적으로** 적었습니다.
4. 모든 프롬프트에 '적힌 인물만 등장'을 넣었습니다.

## 목록
| 파일 | 그림 | 왜 다시 | 첨부 |
|---|---|---|---|
| R01 | b1_moa_emotion_b | 표정 비교 대신 세 인물 전신이 나옴 | moa_anime_base, moa_sheet |
| R01 | b2_haru_shots_b | 시아 설정 시트가 나옴 | haru_anime_base, haru_sheet |
| R01 | b2_eyelevel | 하루의 눈이 다른 사람보다 높음 | haru_anime_base, haru_sheet |
| R01 | b2_eyelevel_b | 요청 외 인물·옷차림이라 싣지 않음 | haru_anime_base, haru_sheet |
| R02 | b3_direction_b | 설정 시트가 나옴 | sia_anime_base, sia_sheet |
| R02 | b3_eyeline_b | 하늘 대신 시아 전신과 큰 날개 | haru_anime_base, haru_sheet |
| R02 | b4_doctor_axis_b | 꼬마 픽셀 스프라이트가 나옴 | doctor_sheet |
| R02 | b4_haru_prop | 상자를 들고 앞으로 숙임(뒤로 기울어야 함) | haru_anime_base, haru_sheet |
| R02 | b4_haru_prop_b | 요청에 없는 박사가 함께 나옴 | haru_anime_base, haru_sheet |
| R03 | f2_fixed | f2를 첨부해 방향이 그대로 | sia_anime_base (f2는 첨부 금지) |
| R03 | f6_fixed | 번 하나·남색 머리띠로 남음 | haru_sheet, haru_anime_base |
| R03 | d4_corridor_eye | 하루의 눈이 다른 둘보다 높음 | haru·sia·moa anime_base |

모두 12장. 저장 이름은 `checklist.csv`의 `file` 열 그대로입니다.
"""
if __name__ == "__main__":
    D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "image_requests_retry")
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for cid, title, att, items in CONV:
        md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n**새 대화마다 먼저 붙여 넣기 ↓**\n```\n{HEAD}\n```\n"
        for file, page, part, alt, prompt, style in items:
            n += 1; rows.append([n, cid[:3], file, page, part, "새 대화", ""])
            md += f"\n---\n## {file} — {part}\n방법: 새 대화에서, 고칠 그림 첨부 없이\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "how", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(README)
    print("retry images", n)
