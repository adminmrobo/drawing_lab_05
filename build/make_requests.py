# -*- coding: utf-8 -*-
"""Genspark 그림 요청 꾸러미(docs/image_requests) 생성. python3 build/make_requests.py
페이지의 '프롬프트로 직접 만들어 보기' A 프롬프트도 여기서 가져간다(이 파일이 원본)."""
import os, csv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests")
PIX = "Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2–3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.\nMatch the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.\nBright daytime laboratory mood, soft natural sunlight through large windows, clean white walls, light lavender, mint and pink accents."
ANI = "Art style: high-quality anime illustration, clean confident lineart, two-tone cel shading, natural adult proportions (about 7.5 heads tall).\nMatch the attached reference images exactly (face, hair, colors, accessories). All characters are adults in their twenties (the Professor is an adult man in his thirties); modest outfits exactly as described."
SKETCH = "Art style: rough graphite pencil storyboard sketch on plain white paper, loose confident lines, figures drawn as simple mannequins (circle heads with a cross line showing the face direction, simple stick-and-cylinder bodies), background reduced to a floor line and a few big shapes, no shading or only light hatching, black and gray only.\nThe figures are adult proportions (about 7.5 heads tall)."
END = "No text, no letters, no numbers, no logos, no watermark, no revealing clothing, not childlike, no school uniform, not resembling any famous anime character."
ENDS = "No text, no letters, no numbers, no captions, no panel numbers, no logos, no watermark (thin empty panel borders are fine)."
ENDC = "No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands."
SAFE = "Composition: every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); bottom-left corner plain and bright."
CH = {
 "haru": "Haru (adult lab assistant, long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top, small ahoge, big blue eyes)",
 "sia": "Sia (adult maid intern, long straight jet-black hair, no headdress, gray eyes, small silver earrings)",
 "moa": "Moa (adult maid intern, long ash-beige wavy hair, white frilled maid headband with a white ribbon over her LEFT ear, amber eyes)",
 "doctor": "the Professor (adult male scientist in his thirties, adult male build, dark charcoal spiky hair with a white streak at the front, very thick black eyebrows, teal rectangular glasses)",
 "fly": "the Fruit Fly researcher (tiny cartoon fruit fly, large red compound eyes, retro dark blue helmet with a yellow-white stripe, colorful dangling cables, tiny white lab coat, translucent wings)",
 "bot": "AbaBot (boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, small tank treads)",
 "judges": "three small cute dark navy silhouette judges with white dot eyes (one with a pink side-ponytail bow, one with a beret and teal round glasses, one with a cat-ear hood and yellow pompoms) holding blank score paddles",
}
OUT = {"haru": "lavender hoodie with white drawstrings over a white t-shirt, open white knee-length lab coat",
       "sia": "charcoal-black long-sleeved maid dress, large gray bow at the collar, long white frilled apron",
       "moa": "camel knit cardigan over a white blouse, red and navy plaid bow tie, white frilled apron",
       "doctor": "white lab coat over a black vest, white shirt and black tie"}
def who(k, outfit=None): return CH[k] + ", wearing " + (outfit or OUT[k])
def cover(file, page, part, alt, scene, chars, meta, mood):
    p = f"Website top cover illustration, wide 16:9.\n{PIX}\nScene: {scene}\nCharacters:\n  " + ";\n  ".join(chars) + f".\nVisual metaphor: {meta}\n{SAFE}\nMood: {mood}\n{ENDC}"
    return (file, page, part, alt, p, "pixel")
def body(file, page, part, alt, ratio, scene, extra="", bg="Plain off-white studio background."):
    p = ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\n{ANI}\n{scene}\n" + (extra + "\n" if extra else "") + (bg + "\n" if bg else "") + END)
    return (file, page, part, alt, p, "anime")
def sketch(file, page, part, alt, scene, extra=""):
    p = f"Storyboard sketch, wide 16:9.\n{SKETCH}\n{scene}\n" + (extra + "\n" if extra else "") + ENDS
    return (file, page, part, alt, p, "sketch")

LAB = "a bright daytime research institute"
C1 = [
 cover("cover_index", "index.html", "목차", "낮의 연구실에서 화이트보드에 여덟 장의 작은 콘티 종이가 두 줄로 붙어 있고, 하루·시아·모아·박사가 그 앞에 모여 있으며, 초파리와 주판봇이 종이를 붙이고, 평가단이 뒤에 앉은 장면",
   "a bright laboratory studio with a large whiteboard holding eight small blank sketch sheets pinned in two rows of four, a table with pencils, sticky notes and a small camera on a tripod.",
   [who("haru") + ", in the center pointing at the eighth sheet with a smile", who("sia") + ", standing on the left holding a pencil", who("moa") + ", on the right holding a stack of sketch sheets", who("doctor") + ", at the back center with a clipboard",
    CH["fly"] + ", hovering near the top left pinning a sheet", CH["bot"] + ", on the right facing left holding one very detailed drawing", CH["judges"] + " sitting at a small table in the back right"],
   "eight small sheets on the whiteboard connected by a hand-drawn arrow that rises toward the last sheet.", "cheerful, curious, the start of planning a short film."),
 cover("cover_01", "01_beats.html", "1부 콘티의 뼈대", "모아가 여덟 장의 종이를 책상 위에 줄 세우고, 초파리가 작은 보드에 문장 한 줄을 적는 시늉을 하며, 주판봇은 첫 장 하나에만 매달려 공들여 그리는 장면",
   "a corner of the lab studio with a long white desk.",
   [who("moa") + ", in the center leaning over the desk arranging eight small paper sheets in a row", CH["fly"] + ", on the left facing right, holding a teal marker over a small blank board", CH["bot"] + ", on the right facing left, bent over a single sheet drawing intensely", who("doctor") + ", at the back nodding"],
   "a gently rising wavy line drawn under the row of eight sheets like an emotion curve.", "focused, playful, organized."),
 cover("cover_02", "02_camera.html", "2부 카메라", "연구소 복도에서 초파리가 액자 틀 같은 투명판을 들고 하루를 들여다보고, 주판봇이 복도 끝으로 이어지는 가로 줄을 당기는 장면",
   "a long bright research institute corridor with windows on one side, the floor lines converging to one point at the far end.",
   [who("haru") + ", standing in the middle of the corridor facing the viewer", CH["fly"] + ", in the foreground on the left holding up an empty rectangular viewfinder frame toward Haru", CH["bot"] + ", on the right holding a long string stretched horizontally at eye level toward the far end", who("doctor") + ", far down the corridor, small in the distance"],
   "a horizontal string at eye level and floor lines meeting at one vanishing point.", "curious, spacious, bright."),
 cover("cover_03", "03_flow.html", "3부 컷 잇기", "연구소 복도 바닥에 테이프로 붙인 곧은 선 하나 옆을 시아가 오른쪽으로 걸어가고, 초파리가 그 선을 가리키며, 주판봇은 선 반대편에 카메라를 들고 서 있는 장면",
   "a bright corridor with a long straight strip of teal tape on the floor running left to right.",
   [who("sia") + ", walking toward the right along the tape line, mid-stride", CH["fly"] + ", hovering above the tape pointing at it", CH["bot"] + ", standing on the far side of the tape holding a small camera, looking unsure", who("doctor") + ", on the near side holding a tripod camera"],
   "the tape line dividing the floor, with a camera allowed only on one side.", "lively, clear, a little comic."),
]
C2 = [
 cover("cover_04", "04_pose.html", "4부 포즈와 연기", "연구실 창고에서 박사가 큰 상자를 안고 몸을 뒤로 기울이고, 초파리가 박사 몸을 따라 휘어진 선을 공중에 그리며, 하루가 무거운 문 앞에서 지켜보는 장면",
   "a bright lab storage room with shelves of boxes and a heavy metal door with a round handle.",
   [who("doctor") + ", in the center carrying a big cardboard box in front of him, leaning back to balance the weight, knees slightly bent", CH["fly"] + ", above him drawing a glowing curved line along his back in the air", who("haru") + ", on the right standing next to the heavy door, watching and taking notes", CH["bot"] + ", on the left standing perfectly straight holding a tiny box, comic contrast"],
   "one glowing curved line from the Professor's head to his supporting foot.", "energetic, warm, slightly comic."),
 cover("cover_05", "05_ai_cuts.html", "5부 AI로 컷 만들기", "연구실 작업대에서 하루·시아·모아가 콘티 종이를 하나씩 커다란 화면에 넣고, 초파리가 문장 조각 카드들을 고르는 장면",
   "a bright lab workbench with a large monitor showing a blank framed image area, a stack of eight sketch sheets, and colorful blank cards spread on the desk.",
   [who("haru") + ", in the center placing a sketch sheet in front of the monitor", who("sia") + ", on the left holding a reference sheet with three small full-body poses", who("moa") + ", on the right sorting blank cards", CH["fly"] + ", hovering over the cards choosing one", CH["bot"] + ", at the back typing on a keyboard"],
   "blank cards being lined up like puzzle pieces into one long strip that leads to the monitor.", "focused, collaborative, hopeful."),
 cover("cover_06", "06_failure_lab.html", "6부 실패 사례 실험실", "연구실 검수 책상에서 초파리가 돋보기로 실패한 컷 그림들을 살피고, 시아가 그림을 순서대로 놓으며, 주판봇이 머리를 긁는 장면",
   "a bright lab inspection desk with eight small framed pictures laid in a row, a magnifying glass and a checklist board with five blank lines.",
   [CH["fly"] + ", on the left holding a big magnifying glass over one picture", who("sia") + ", in the center arranging the pictures in order", CH["bot"] + ", on the right scratching its head with a confused face", CH["judges"] + " at the back holding blank score paddles"],
   "a magnifying glass revealing a hidden straight line under one of the pictures.", "investigative, light, friendly."),
 cover("cover_07", "practice/index.html", "7부 실전 연습장", "연구실 조종 책상에서 하루가 여러 화면을 조작하고, 박사가 옆에서 가리키며, 초파리와 주판봇이 각자 작은 화면을 맡은 장면",
   "a bright lab control desk with four small screens in a row and a printed blank storyboard sheet with two rows of four empty frames on the desk.",
   [who("haru") + ", in the center operating the controls with determination", who("doctor") + ", standing beside her pointing at a screen", CH["fly"] + ", on the left at a small screen", CH["bot"] + ", on the right at another screen, eager"],
   "four glowing screens connected by one line to the blank storyboard sheet.", "determined, bright, game-like challenge."),
]
C3 = [
 sketch("b1_haru_8cuts", "01_beats.html", "1부 1단계", "하루의 이야기 여덟 컷을 연필로 빠르게 그린 콘티 밑그림 — 두 줄 네 장씩 놓인 작은 그림에 동그라미 머리와 십자선만 있는 인물, 화살표, 배경 몇 줄",
   "One sheet of paper with eight small panels in two rows of four, read left to right, top to bottom. The same young woman mannequin appears in every panel. "
   "Panel 1: wide shot, she stands small in front of a research building on a street. Panel 2: full body side view, she runs toward the right. Panel 3: full body from behind, she walks into a long corridor toward the vanishing point. "
   "Panel 4: waist-up, she stands on the left third of the frame looking out a window on the right. Panel 5: close-up of her mannequin head looking up toward the upper right, small surprise marks. "
   "Panel 6: low angle, she climbs stairs going up. Panel 7: waist-up, she pushes a heavy door with her whole body leaning forward. Panel 8: wide shot, she steps out onto a rooftop with a wide sky and a city skyline, a tiny winged dot in the sky.",
   "Each panel has a thin empty border; under each panel there are three empty ruled lines (left blank)."),
 body("b1_moa_emotion", "01_beats.html", "1부 3단계", "모아가 세 가지 감정을 연기한 얼굴 세 장 — 왼쪽 걱정하는 얼굴, 가운데 깜짝 놀라 깨닫는 얼굴, 오른쪽 결심한 얼굴, 모두 같은 크기의 상반신", "16:9",
   "Three panels side by side, the same chest-up framing in each, of " + who("moa") + ". Left: worried, eyebrows raised in the middle, lips pressed. Middle: startled realization, eyes wide, looking up toward the upper right. Right: determined, slight frown, firm closed mouth, looking straight ahead.",
   "Same lighting from the upper left in all three panels. Thin light gray borders between panels."),
 body("b1_cut5_two", "01_beats.html", "1부 4단계", "같은 5컷을 두 가지로 그린 그림 — 왼쪽은 동그라미 머리와 십자선, 선 몇 개로 그린 연필 썸네일, 오른쪽은 같은 구도로 완성한 하루의 놀란 얼굴 애니풍 그림", "16:9",
   "Two panels side by side with exactly the same composition. Left panel: a rough graphite pencil thumbnail on white paper — a circle head with a cross line turned toward the upper right, two quick lines for the shoulders, a window frame line at the upper right. "
   "Right panel: the same composition finished as a full-color close-up of " + who("haru") + ", looking up toward the upper right with startled realization, soft backlight from a window at the upper right.",
   "The head position, size and direction must match between the two panels.", bg=None),
]
C4 = [
 body("b2_haru_shots", "02_camera.html", "2부 1단계", "같은 하루를 다섯 가지 샷 크기로 나란히 담은 그림 — 원경, 전신, 허리 위, 가슴 위, 얼굴 순서로 점점 가까워지는 다섯 장", "16:9",
   "Five vertical panels side by side, the same character " + who("haru") + " in the same calm pose and the same bright lab hallway, framed at five shot sizes from left to right: "
   "1) wide shot, she is small in the hallway; 2) full body head to toe; 3) waist-up; 4) chest-up; 5) close-up of the face filling the panel.",
   "Same light from the upper left in all panels. Thin light gray borders between panels.", bg=None),
 body("b2_eyelevel", "02_camera.html", "2부 2단계", "낮의 연구소 긴 복도에서 키가 비슷한 연구원 다섯 명이 안쪽으로 멀어지며 서 있는 그림 — 멀수록 작아지고, 다섯 명의 눈이 한 가로선 위에 나란함", "16:9",
   "A long, bright research institute corridor in one-point perspective, the vanishing point at the far end in the center. " + who("haru") + " stands closest on the left; four more adult researchers in white lab coats of the same height stand farther and farther down the corridor on the same floor, each one smaller with distance.",
   "Camera at standing eye level: the horizon line passes through the eyes of all five people. Consistent perspective, feet all on the same floor plane.", bg=None),
 body("b3_direction", "03_flow.html", "3부 1단계", "두 컷을 나란히 놓은 그림 — 왼쪽 컷에서 시아가 연구소 앞길을 오른쪽으로 걷고, 오른쪽 컷에서 같은 시아가 복도 안쪽으로 걸어 들어가는 뒷모습", "16:9",
   "Two panels side by side. Left panel: full body side view of " + who("sia") + ", walking briskly toward the RIGHT side of the frame along a sunny path in front of " + LAB + ". "
   "Right panel: full body view from behind of the same Sia walking away into a long bright corridor toward the vanishing point.",
   "Same afternoon light from the left in both panels. Thin light gray border between panels.", bg=None),
 body("b3_eyeline", "03_flow.html", "3부 4단계", "두 컷을 나란히 놓은 그림 — 왼쪽 컷에서 하루가 창가 왼쪽에 서서 오른쪽 위 창밖을 바라보고, 오른쪽 컷에는 창밖 오른쪽 위 하늘에 작은 날개가 반짝이는 모습", "16:9",
   "Two panels side by side. Left panel: waist-up shot of " + who("haru") + " standing on the LEFT third of the frame inside a bright corridor, looking toward the UPPER RIGHT out of a large window, empty space on the right. "
   "Right panel: the view out of the window — blue sky above a rooftop edge, and a tiny pair of translucent insect wings glinting in the UPPER RIGHT of the frame.",
   "Thin light gray border between panels.", bg=None),
]
C5 = [
 body("b4_doctor_axis", "04_pose.html", "4부 1단계", "박사의 세 가지 자세를 나란히 놓은 그림 — 곧게 서 있는 자세, 몸 전체를 C자로 숙여 큰 문을 미는 자세, 몸을 S자로 비틀어 걸으며 뒤를 돌아보는 자세", "16:9",
   "Three full-body poses of " + who("doctor") + " side by side. Left: standing straight and relaxed. Middle: pushing a large heavy metal door with the whole body leaning forward in a clear C-shaped curve, back foot pushing off the floor. Right: walking and twisting to look back over his shoulder, body in a gentle S-shaped curve.",
   "Light from the upper left. Clear silhouettes, arms separated from the torso."),
 body("b4_haru_prop", "04_pose.html", "4부 3단계", "하루가 물건을 든 두 장면을 나란히 놓은 그림 — 왼쪽은 가벼운 우산을 들고 곧게 선 하루, 오른쪽은 무거운 실험 상자를 앞으로 안고 몸을 뒤로 기울인 하루", "16:9",
   "Two full-body panels of " + who("haru") + ". Left: holding a closed light folding umbrella loosely at her side, standing upright and relaxed. Right: carrying a big heavy cardboard lab box in front of her with both arms, leaning her upper body back to counterbalance, knees slightly bent, feet apart, arms strained.",
   "Light from the upper left. Thin light gray border between panels."),
 body("b5_haru_anchor", "05_ai_cuts.html", "5부 2단계", "하루의 기준 시트(정면·옆·뒤 전신과 얼굴)를 왼쪽에 두고, 오른쪽에 같은 하루가 나오는 세 컷(달리기, 창밖 보기, 문 밀기)을 나란히 놓은 그림", "16:9",
   "Left half: a clean character reference sheet of " + who("haru") + " — front, side and back full-body views standing in a row and one close-up of the face, on white. "
   "Right half: three small story panels of the same Haru with identical hair buns, navy bang streak and outfit: running toward the right in a hallway; waist-up looking out a window to the right; pushing a heavy rooftop door with her whole body.",
   "Every depiction of Haru must keep exactly the same design.", bg=None),
 body("b5_sketch_to_cut", "05_ai_cuts.html", "5부 3단계", "같은 7컷을 두 가지로 놓은 그림 — 왼쪽은 하루가 옥상 문을 미는 연필 썸네일(동그라미 머리와 선), 오른쪽은 같은 구도로 완성한 애니풍 컷", "16:9",
   "Two panels side by side with exactly the same composition. Left panel: a rough graphite pencil thumbnail on white paper — a mannequin with a circle head and cross line, body leaning forward in a C-shaped curve, both hands on a door on the right side. "
   "Right panel: the same composition finished as a full-color waist-up shot of " + who("haru") + " pushing a heavy metal rooftop door with determination, a line of bright daylight coming through the opening door.",
   "Figure position, size and pose must match between the two panels.", bg=None),
]
FAILNOTE = "This is an intentional FAILURE example for a teaching page: draw the mistake described below clearly and convincingly, while everything else stays correct."
def fail(file, alt, ratio, scene, mistake):
    p = ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\n{ANI}\n{FAILNOTE}\n{scene}\nIntentional mistake: {mistake}\n{END}")
    return (file, "06_failure_lab.html", "6부 실패", alt, p, "anime")
C6 = [
 fail("f1_same", "네 컷을 이어 놓았는데 둘째부터 넷째 컷이 모두 같은 크기, 같은 자세의 하루 상반신이라 무엇이 달라졌는지 알 수 없는 그림", "16:9",
      "Four panels side by side forming a short story strip with " + who("haru") + " in " + LAB + ". Panel 1: wide shot of her in front of the building.",
      "panels 2, 3 and 4 are almost identical — the same chest-up framing, the same neutral pose and expression, the same plain background — so nothing seems to happen in the story."),
 fail("f2_flip", "두 컷을 나란히 놓았는데 왼쪽 컷의 시아는 오른쪽으로 걷고, 오른쪽 컷의 시아는 같은 길에서 왼쪽으로 걸어 되돌아가는 것처럼 보이는 그림", "16:9",
      "Two panels side by side of " + who("sia") + " walking along the same sunny path in front of " + LAB + ". Left panel: full body side view walking toward the RIGHT.",
      "in the right panel the camera has crossed to the other side, so she walks toward the LEFT side of the frame and looks like she is going back the way she came."),
 fail("f3_giant", "연구소 복도에서 안쪽 멀리 선 연구원이 앞쪽 가까이 선 하루와 같은 크기로 그려져 거인처럼 보이는 그림", "16:9",
      "A long bright research institute corridor in one-point perspective. " + who("haru") + " stands in the foreground on the left. An adult researcher in a white lab coat stands far down the corridor near the vanishing point.",
      "the far researcher is drawn at the same size as Haru even though he is much farther away, so he looks like a giant compared with the corridor."),
 fail("f4_float", "옥상 장면인데 눈높이 선(지평선)이 인물마다 다른 높이를 지나 한 사람은 바닥 위로 떠 있는 것처럼 보이는 그림", "16:9",
      "A sunny rooftop garden with a low railing and a wide sky, a distant city skyline on the horizon. " + who("haru") + " and " + who("moa") + " stand on the rooftop floor at different distances.",
      "the perspective does not match: Moa's feet are placed well above the floor plane for her distance, so she appears to float in the air, and the horizon crosses the two characters at completely different body heights."),
]
C7 = [
 fail("f5_stiff", "박사가 무거운 철문을 미는 장면인데 몸이 곧게 선 채 팔만 뻗어 문에 손을 대고 있는 그림", "2:3",
      "Full body side view of " + who("doctor") + " pushing a heavy metal rooftop door.",
      "his body stands perfectly upright and stiff like a pole, feet together, only his arms reach out to touch the door, so it looks like the door weighs nothing."),
 fail("f6_drift", "하루가 나오는 세 컷을 나란히 놓았는데 컷마다 정수리 번이 없어지거나 앞머리 남색 줄 자리가 바뀌어 다른 사람처럼 보이는 그림", "16:9",
      "Three story panels side by side of Haru (adult lab assistant with long pink hair) in a bright lab: running toward the right; looking out a window; pushing a door.",
      "her design changes in every panel — in the second panel the two hair buns are missing, in the third the navy streak moves to the side and the hoodie turns light blue — so she looks like three different people."),
 fail("f7_wall", "모아가 오른쪽 창밖을 바라보는데 화면 오른쪽 끝에 바짝 붙어 있어 시선 앞이 막혀 답답해 보이는 그림", "16:9",
      "Waist-up shot of " + who("moa") + " in a bright lab corridor, looking toward the RIGHT out of a window.",
      "she is placed at the extreme right edge of the frame with her nose almost touching the right border, and all the empty space is behind her on the left, so the composition feels cramped and blocked."),
 fail("f8_light", "같은 시각 같은 복도의 두 컷을 나란히 놓았는데 왼쪽 컷은 빛이 왼쪽 창에서, 오른쪽 컷은 오른쪽에서 들어와 그림자 방향이 반대인 그림", "16:9",
      "Two consecutive panels side by side of " + who("sia") + " in the same bright corridor at the same time of day: left panel walking, right panel stopping.",
      "the lighting is inconsistent: in the left panel sunlight comes from windows on the left and shadows fall to the right, in the right panel the light comes from the right and shadows fall to the left, as if the sun jumped."),
]
CONV = [("C01_covers_A", "표지 A (픽셀아트, 16:9)", "16:9", "refs 전부", C1), ("C02_covers_B", "표지 B (픽셀아트, 16:9)", "16:9", "refs 전부 + C01에서 받은 cover_index", C2),
        ("C03_part1", "1부 콘티 밑그림·감정", "16:9", "refs/haru_anime_base.png, refs/haru_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png", C3),
        ("C04_part2_3", "2·3부 카메라·컷 잇기", "16:9", "refs/haru_anime_base.png, refs/haru_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png", C4),
        ("C05_part4_5", "4·5부 포즈·AI 컷", "16:9", "refs/doctor_sheet.png, refs/haru_anime_base.png, refs/haru_sheet.png", C5),
        ("C06_fail_A", "6부 실패 A", "16:9", "해당 캐릭터의 refs/*_anime_base.png 또는 *_sheet.png", C6), ("C07_fail_B", "6부 실패 B", "16:9·2:3", "해당 캐릭터의 refs/*_anime_base.png 또는 *_sheet.png (f6은 하루 기준 그림을 첨부하지 않음)", C7)]
HEAD_PIX = "웹페이지 맨 위에 거는 표지 그림을 한 장씩 차례로 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)\n- 첨부한 참고 이미지의 캐릭터를 같은 외형으로 그릴 것\n- 그림 안에 글자·숫자·로고 금지\n- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게\n아래 영어 프롬프트를 하나씩 써 줘."
HEAD_ANI = "해설 페이지 본문에 넣을 그림을 한 장씩 차례로 만들어 줘.\n- 비율은 각 프롬프트 첫 줄을 따를 것(16:9는 가로 1920px 이상, 2:3은 세로 1536px 이상)\n- 첨부한 참고 이미지의 캐릭터 외형(얼굴·머리·색·장식)을 똑같이 지킬 것\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·과장된 체형·교복 느낌·어려 보이는 얼굴 금지\n- 연필 콘티 그림(Storyboard sketch)은 흑백 연필 밑그림으로, 인물은 동그라미 머리와 십자선의 단순한 마네킹으로\n- 그림 안에 글자·숫자·로고·컷 번호 금지, 유명 애니 캐릭터와 닮으면 다시 만들 것\n아래 영어 프롬프트를 하나씩 써 줘."
PROMPTS = {it[0]: it for _c in CONV for it in _c[4]}
CONV_OF = {it[0]: _c[0] for _c in CONV for it in _c[4]}
ATTACH_OF = {_c[0]: _c[3] for _c in CONV}

README = """# 그림 요청 꾸러미 — 구조 먼저 그리기 연구실 05 · 콘티 편

저장소: `adminmrobo/drawing_lab_05` (페이지는 완성 — 그림 자리는 '그림 준비 중'으로 비어 있음)
만드는 도구: Genspark 이미지 · 받은 그림은 zip으로 돌려주시면 됩니다(대화 단위로 나눠 여러 번 주셔도 됩니다).

## 1. 그림 규칙
| 항목 | 규칙 |
|---|---|
| 그림체 | **표지 8장은 16비트 픽셀아트**. 본문 그림은 **애니풍**, 콘티 밑그림 1장(b1_haru_8cuts)은 **흑백 연필 콘티** |
| 배경 | 흰색·밝은 낮 분위기 |
| 캐릭터 고정값 | 하루: 정수리 번 2개 + 앞머리 가운데 남색 줄 / 시아: 흑발·머리 장식 없음 / 모아: 흰 프릴 머리띠 + **왼쪽** 귀 위 흰 리본 / 박사: 흰 줄 있는 짙은 머리, 굵은 눈썹, 청록 사각 안경 |
| 나이·노출 | 모두 20대 성인(박사는 30대 성인 남성, 꼬마 체형 아님). **어려 보이는 얼굴·교복 느낌·노출 금지** |
| 글자 | 그림 안에 글자·숫자·로고·컷 번호 금지(콘티의 빈 틀과 빈 줄은 허용) |
| 여러 컷 그림 | 한 장 안에 컷 여러 개를 나란히 놓는 그림은 컷 사이에 얇은 회색 경계선 |

## 2. 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 그림 수 | 비율 | 첨부 |
|---|---|---|---|---|
| 1 | `prompts/C01_covers_A.md` | 4 | 16:9 픽셀 | refs 전부 |
| 2 | `prompts/C02_covers_B.md` | 4 | 16:9 픽셀 | refs 전부 + C01의 cover_index |
| 3 | `prompts/C03_part1.md` | 3 | 16:9 | haru·moa anime_base, sheet |
| 4 | `prompts/C04_part2_3.md` | 4 | 16:9 | haru·sia anime_base, sheet |
| 5 | `prompts/C05_part4_5.md` | 4 | 16:9 | doctor_sheet, haru anime_base·sheet |
| 6 | `prompts/C06_fail_A.md` | 4 | 16:9 | 해당 캐릭터 기준 그림 |
| 7 | `prompts/C07_fail_B.md` | 4 | 16:9 · f5만 2:3 | 해당 캐릭터 기준 그림(f6은 첨부 없이) |

## 3. 저장 이름
`checklist.csv`의 `file` 열 이름 그대로(png·jpg). 받으면 WebP로 바꿔 `assets/img/`에 넣습니다(표지 1600×900, 가로 1200×675, 세로 600×900).

## 4. 실패 그림 주의
도구가 실수를 자동으로 고쳐 그리면 두 번까지만 다시 시도해 주세요. 그래도 안 되면 그대로 주셔도 됩니다(페이지에서 '결과는 매번 다르다'는 사례로 설명합니다). f6(바뀌는 캐릭터)은 일부러 기준 그림을 첨부하지 않고 만듭니다.
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for cid, title, ratio, att, items in CONV:
        pix = items[0][5] == "pixel"
        md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD_PIX if pix else HEAD_ANI}\n```\n"
        for k, (file, page, part, alt, prompt, style) in enumerate(items):
            n += 1; rows.append([n, cid[:3], file, page, part, "16:9" if "16:9" in prompt.split("\n")[0] else "2:3", style, ""])
            md += f"\n---\n## {k+1}) {file} — {part}\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(README)
    print("prompts", len(CONV), "images", n)
