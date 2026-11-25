# -*- coding: utf-8 -*-
"""부마다 '프롬프트 연습 과제' 2개씩(모두 12개). 과제의 프롬프트는 예상 결과 그림을 실제로 만드는 프롬프트와 같다(이 파일이 원본).
python3 build/content_drill.py → docs/image_requests_drill/ 요청 꾸러미 생성.
아직 그림을 받지 않았으므로 '왜 이 연습인가'와 '자주 생기는 문제'는 원리와 앞 편(03 얼굴 편)에서 겪은 일을 근거로 적었다."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import who, ANI, SKETCH, END, ENDS

def P(ratio, scene, extra="", bg="Plain off-white studio background."):
    return ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\n{ANI}\n{scene}\n" + (extra + "\n" if extra else "") + (bg + "\n" if bg else "") + END)
def S(scene, extra=""):
    return f"Storyboard sketch, wide 16:9.\n{SKETCH}\n{scene}\n" + (extra + "\n" if extra else "") + ENDS

LAB = "a bright daytime research institute"
DRILL = {
1: [
 dict(id="d1", title="한 문장과 네 덩어리로 여덟 컷 받기", goal="이야기 한 문장과 네 덩어리(시작·전개·전환·끝)를 컷 번호와 함께 문장으로 넣어, 여덟 컷 연필 썸네일을 한 장으로 받습니다.",
      why="AI에게 '8컷 이야기'라고만 하면 앞쪽 장면이 길어지고 끝이 빠지기 쉽습니다(1부 1단계). 덩어리와 컷 번호를 짝지어 적으면 여덟 자리가 고르게 채워지는지 직접 확인할 수 있습니다.",
      attach="첨부 없음(연필 마네킹으로 그리므로 캐릭터 참고 그림이 필요 없음)",
      steps=["Genspark에서 새 대화를 엽니다.", "아래 프롬프트를 그대로 붙여 넣어 한 장을 만듭니다.",
             "받은 그림의 여덟 컷 아래에 연필로 덩어리 이름(시작·전개·전환·끝)을 적어 봅니다. 두 컷씩 맞게 나뉘었나요?",
             "컷마다 목적을 한 줄씩 적어 봅니다. 목적이 같은 컷이 둘 있으면 그 컷은 6부 f1과 같은 실패입니다.",
             "어긋난 컷이 있으면 같은 대화에 'Same image. Change only: panel N — …' 한 줄로 그 컷만 고칩니다."],
      prompts=[("넣을 프롬프트", S("One sheet with eight small panels in two rows of four, read left to right, top to bottom. Story in one sentence: a young woman lab assistant searches for her lost tiny fruit-fly colleague and finds it on the rooftop. "
                "Panels 1–2 (beginning): she arrives in front of a research building, then runs toward the right. Panels 3–4 (development): she walks into a long corridor, then stops and looks out a window to the right. "
                "Panels 5–6 (turn): close-up as she realizes something, then she climbs stairs seen from a low angle. Panels 7–8 (ending): she pushes a heavy door, then steps onto a wide rooftop under a big sky.",
                "Each panel has a thin empty border. The same mannequin appears in every panel."),
               "d1_thumbs", "예상 결과 — 네 덩어리를 두 컷씩 나눠 그린 여덟 컷 연필 썸네일. 1·8컷은 멀리, 5컷은 얼굴 가까이", "16/9")],
      check=[("여덟 컷이 네 덩어리에 두 컷씩 나뉘었나", "#s1"), ("컷마다 목적이 다르게 읽히나", "#s2"), ("인물이 동그라미 머리 + 십자선의 단순한 마네킹인가", "#s4")],
      expect="두 줄 네 장의 연필 콘티가 나옵니다. 1컷 건물 앞의 작은 인물에서 시작해 8컷 넓은 옥상에서 끝나고, 5컷만 얼굴이 크게 나옵니다. 컷마다 목적이 다르니 그림도 서로 다릅니다.",
      trouble=[("그림 속에 컷 번호나 글자가 생긴다", "'no text, no panel numbers'를 맨 끝에 한 번 더 적고 다시 만듭니다."),
               ("매끈한 완성 그림이 나온다", "'rough pencil thumbnail, no shading'을 첫 줄에 옮깁니다. 그래도 매끈하면 썸네일은 손으로 그리는 편이 빠릅니다(1부 4단계)."),
               ("여덟 컷이 아니라 여섯·아홉 컷이 나온다", "'exactly eight panels, two rows of four'를 덧붙입니다.")],
      more="같은 문장에서 덩어리 배분만 1·1·3·3으로 바꿔 만들어 보고, 끝이 길어진 콘티와 비교해 보세요."),
 dict(id="d2", title="같은 컷, 감정 줄만 바꿔 두 번", goal="5컷(깨달음)을 감정 낱말 없이 한 번, 감정 낱말을 넣어 한 번 만들어, 감정 줄이 그림을 얼마나 바꾸는지 확인합니다.",
      why="감정 줄이 문장에 없으면 AI는 무난한 미소를 고르기 쉽습니다(1부 3단계). 같은 대화에서 감정만 바꾸면 차이가 약할 수 있으니, 약하면 새 대화로 나눕니다(앞 편 03에서 작은 변화가 같은 대화에서 무시된 경험).",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림 두 장을 첨부합니다.", "프롬프트 ①로 감정 낱말 없는 5컷을 만듭니다.", "같은 대화에 프롬프트 ②를 이어 붙입니다(감정만 바뀜).",
             "두 장을 나란히 놓고 눈썹·눈·입·시선이 달라졌는지 봅니다.", "②가 ①과 거의 같으면 새 대화를 열고 ②의 감정 문장을 넣은 전체 프롬프트로 처음부터 만듭니다."],
      prompts=[("① 감정 낱말 없이", P("16:9", "Close-up shot of " + who("haru") + ", inside a bright corridor next to a large window on the right, looking toward the upper right.", "Eye-level camera. Soft backlight from the window."),
                "d2_cut5_plain", "예상 결과 ① — 감정 낱말 없이 만든 5컷. 하루가 오른쪽 위를 보지만 표정은 무난한 미소", "16/9"),
               ("② 같은 대화에 이어서", "Same image, keep the same framing. Change only: her expression is a startled realization — eyes wide open, eyebrows raised, lips slightly parted, as if she just noticed something. Still no text.",
                "d2_cut5_emotion", "예상 결과 ② — 감정 낱말을 넣은 5컷. 눈이 커지고 눈썹이 올라간 깨닫는 얼굴", "16/9")],
      check=[("①과 ②의 샷 크기·시선 방향이 같은가(감정만 바뀌었나)", "02_camera.html#s1"), ("②의 눈썹·눈·입이 깨달음으로 읽히나", "#s3"), ("두 장 모두 같은 하루(번 2개, 남색 줄)인가", "05_ai_cuts.html#s2")],
      expect="①은 오른쪽 위를 보는 무난한 얼굴, ②는 같은 구도에서 눈썹이 올라가고 눈이 커진 깨닫는 얼굴입니다. 감정 낱말 하나로 5컷의 목적(단서를 알아챈다)이 살아납니다.",
      trouble=[("②가 ①과 똑같다", "새 대화에서 ②의 감정 문장을 넣은 전체 프롬프트로 처음부터 만듭니다."),
               ("표정과 함께 구도도 바뀐다", "②에 'keep the same camera, the same head position'을 덧붙입니다."),
               ("놀란 얼굴이 무서운 얼굴이 된다", "'surprised but hopeful, a small spark in the eyes'처럼 감정의 방향을 함께 적습니다.")],
      more="같은 방법으로 1컷(걱정)과 7컷(각오)도 만들어, 1부 3단계 감정 곡선의 높낮이와 표정의 세기를 비교해 보세요."),
],
2: [
 dict(id="d1", title="샷 낱말로 같은 장면 두 번", goal="같은 장면을 'full body shot'과 'close-up'으로 만들어, 받은 그림 위에서 화면에 들어가는 머리 수를 세어 봅니다.",
      why="'가까이', '멀리'는 사람마다, 도구마다 다르게 읽힙니다. 샷 이름과 '화면 아래 끝이 어디를 자르는지'를 함께 적으면 샷이 덜 흔들립니다(2부 1단계).",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트 ①로 전신 샷을 만듭니다.", "새 대화를 하나 더 열고 같은 참고 그림을 첨부한 뒤 프롬프트 ②로 얼굴 샷을 만듭니다.",
             "두 그림에서 하루의 머리 높이를 재어, 화면 높이에 머리가 몇 개 들어가는지 셉니다(전신 약 9개, 얼굴 약 1.5개).", "많이 다르면 '확인할 것'의 링크로 돌아가 샷 표를 다시 보고, 화면 끝이 자르는 곳을 문장에 더합니다."],
      prompts=[("① 전신 샷", P("16:9", "Full body shot of " + who("haru") + " standing in " + LAB + " hallway, from head to toe with a little space above her head and below her feet.", "Eye-level camera. Light from the upper left.", bg=None),
                "d3_shot_full", "예상 결과 ① — 머리부터 발끝까지 담은 하루의 전신 샷", "16/9"),
               ("② 얼굴 샷(새 대화)", P("16:9", "Close-up shot of " + who("haru") + " in " + LAB + " hallway; the bottom edge of the frame cuts just below her chin, her face fills most of the frame height.", "Eye-level camera. Light from the upper left.", bg=None),
                "d3_shot_cu", "예상 결과 ② — 턱 바로 아래에서 잘린 하루의 얼굴 샷", "16/9")],
      check=[("①에서 머리부터 발끝까지 다 보이고 위아래 여백이 조금 있나", "#s1"), ("②에서 얼굴이 화면 높이의 2/3쯤을 채우나", "#s1"), ("두 장 모두 같은 복도·같은 빛인가", None)],
      expect="①은 화면 높이에 머리가 약 9개 들어가는 전신, ②는 머리가 약 1.5개 들어가는 얼굴 샷입니다. 같은 하루, 같은 복도인데 ①은 장소가, ②는 표정이 먼저 보입니다.",
      trouble=[("①에서 발이 잘린다", "'feet fully visible, small floor margin at the bottom'을 덧붙입니다."),
               ("②가 가슴 위까지 넓게 나온다", "'extreme close-up' 대신 'the bottom edge cuts just below the chin'처럼 화면 끝을 적습니다."),
               ("두 그림의 하루가 다른 사람 같다", "두 대화 모두 같은 참고 그림 두 장을 첨부했는지 확인합니다(5부 2단계).")],
      more="허리 위(waist-up)·가슴 위(chest-up)도 만들어 다섯 장을 나란히 놓고, 2부 1단계 실험의 샷 표와 비교해 보세요."),
 dict(id="d2", title="눈높이 선을 문장으로 넣어 복도 원근 맞추기", goal="'눈높이 선이 모두의 눈을 지난다'를 문장으로 넣어 복도 장면을 만들고, 받은 그림 위에 선을 그어 검사합니다.",
      why="원근은 AI가 자주 틀리는 곳입니다(6부 f3·f4). '원근을 맞춰 줘'보다 '눈높이 선이 모두의 눈을 지난다, 모두 같은 키'처럼 검사할 수 있는 말로 적으면 결과를 직접 확인할 수 있습니다.",
      attach="refs/haru_anime_base.png, refs/sia_anime_base.png, refs/moa_anime_base.png",
      steps=["새 대화를 열고 참고 그림 세 장을 첨부합니다.", "프롬프트를 붙여 넣어 한 장을 만듭니다.",
             "받은 그림에서 세 사람의 눈을 이어 가로선을 긋습니다. 한 줄로 이어지나요?", "가장 가까운 사람과 가장 먼 사람의 머리 끝, 발끝을 각각 이어 복도 끝까지 늘립니다. 두 선이 한 점(소실점)에서 만나나요?",
             "어긋나면 같은 대화에 'Same image. Change only: …'로 어긋난 사람 하나만 고칩니다."],
      prompts=[("넣을 프롬프트", P("16:9", "A long bright research institute corridor in one-point perspective, vanishing point at the far end in the center. " + who("haru") + " stands closest on the left, " + who("sia") + " stands in the middle distance, " + who("moa") + " stands far down the corridor.",
                "All three are the same real height and stand on the same floor. Camera at standing eye level: the horizon line passes through the eyes of all three; each person gets smaller with distance.", bg=None),
               "d4_corridor_eye", "예상 결과 — 복도 앞·가운데·안쪽에 선 하루·시아·모아. 멀수록 작고, 세 사람의 눈이 한 가로선 위에 있음", "16/9")],
      check=[("세 사람의 눈이 한 가로선 위에 있나", "#s2"), ("머리 끝선·발끝선이 소실점에서 만나나", "#s2"), ("세 사람의 고정값(번·흑발·머리띠와 왼쪽 리본)이 지켜졌나", "05_ai_cuts.html#s2")],
      expect="세 사람이 멀어질수록 작아지고, 눈이 한 줄로 늘어섭니다. 선을 그어 보면 머리 끝과 발끝이 복도 끝 한 점으로 모입니다. 그림 속에는 선이 없고, 선은 받은 뒤 직접 긋습니다.",
      trouble=[("먼 사람이 너무 크다", "'Same image. Change only: make Moa much smaller, matching her distance'로 한 사람만 고칩니다."),
               ("세 사람이 모두 앞에 나란히 선다", "'at three clearly different distances along the corridor'를 덧붙입니다."),
               ("모아의 리본이 오른쪽에 붙는다", "'white ribbon over her LEFT ear'를 한 번 더 적거나 그 부분만 부분 수정합니다.")],
      more="카메라를 낮춰 'camera at knee height'로 다시 만들고, 눈높이 선이 세 사람의 무릎을 지나는지 확인해 보세요."),
],
3: [
 dict(id="d1", title="방향을 지키는 두 컷 잇기", goal="2컷(오른쪽으로 달리기)과 3컷(복도로 들어가는 뒷모습)을 한 컷씩 만들어 이어 붙이고, 방향이 이어지는지 확인합니다.",
      why="AI는 앞 컷의 방향을 기억하지 못합니다(3부 1단계). 컷마다 '화면의 어느 쪽으로'를 적어야 가상선이 지켜집니다. 앞 편(03)에서는 '왼쪽을 본다'보다 '화면 왼쪽 끝의 무엇을 본다'처럼 적을 때 방향이 잘 지켜졌습니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 시아 참고 그림을 첨부합니다.", "프롬프트 ①로 2컷을 만듭니다.", "같은 대화에 프롬프트 ②를 이어 붙여 3컷을 만듭니다(새 구도).",
             "두 장을 순서대로 나란히 놓고, 시아가 한 방향으로 나아가는지 봅니다.", "②가 옆모습으로 왼쪽을 향하면 가상선을 넘은 것입니다. ②를 새 대화에서 처음부터 만듭니다."],
      prompts=[("① 2컷 — 오른쪽으로", P("16:9", "Full body side view of " + who("sia") + ", running toward the RIGHT side of the frame along a sunny path in front of " + LAB + "; the building entrance is at the right edge of the frame.", "Eye-level camera. Afternoon light from the left.", bg=None),
                "d5_run_right", "예상 결과 ① — 연구소 앞길을 화면 오른쪽으로 달리는 시아의 옆모습", "16/9"),
               ("② 같은 대화에 이어서 — 3컷", "New composition, the next cut. Full body view from BEHIND of the same Sia walking away into a long bright corridor toward the vanishing point in the center. Same afternoon light from the left. Still no text.",
                "d5_corridor_back", "예상 결과 ② — 복도 안쪽으로 걸어 들어가는 시아의 뒷모습", "16/9")],
      check=[("①에서 시아가 화면 오른쪽으로 달리나", "#s1"), ("②가 뒷모습(선 위의 다리 컷)인가", "#s1"), ("두 컷의 빛 방향(왼쪽)이 같은가", "06_failure_lab.html#f8")],
      expect="①은 오른쪽으로 달리는 옆모습, ②는 복도로 들어가는 뒷모습입니다. 이어 놓으면 '건물로 달려가 안으로 들어간다'가 한 흐름으로 읽힙니다.",
      trouble=[("②가 ①과 같은 구도로 나온다", "'New composition'을 첫머리에 두고 'from behind'를 강조합니다. 그래도 같으면 새 대화에서 만듭니다(5부 4단계)."),
               ("①이 왼쪽으로 달린다", "'the building entrance is at the right edge'처럼 목적지를 화면 오른쪽에 둡니다."),
               ("빛 방향이 바뀐다", "두 프롬프트에 같은 빛 문장을 그대로 붙입니다.")],
      more="②를 일부러 'side view walking toward the LEFT'로 만들어, 6부 f2처럼 되돌아가는 느낌이 드는지 비교해 보세요."),
 dict(id="d2", title="시선을 잇는 두 컷", goal="4컷(오른쪽 위를 봄)과 다음 컷(날개 반짝임)을 만들어, 시선 방향과 대상의 자리를 맞춥니다.",
      why="시선과 대상의 자리가 어긋나면 '무엇을 보고 놀랐는지'가 사라집니다(3부 4단계). 대상 컷에 '화면 오른쪽 위'처럼 자리를 적어 시선과 맞춥니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 하루 참고 그림을 첨부합니다.", "프롬프트 ①로 4컷을 만듭니다.", "같은 대화에 프롬프트 ②를 이어 붙여 대상 컷을 만듭니다.",
             "두 장을 나란히 놓고, ①의 시선 끝과 ②의 날개 자리가 같은 쪽인지 봅니다.", "어긋나면 ②만 'Same image. Change only: move the wings to the upper right'로 고칩니다."],
      prompts=[("① 4컷 — 오른쪽 위를 봄", P("16:9", "Waist-up shot of " + who("haru") + " standing on the LEFT third of the frame inside a bright corridor, looking toward the UPPER RIGHT out of a large window; wide empty space on the right side.", "Eye-level camera. Soft daylight from the window on the right.", bg=None),
                "d6_look", "예상 결과 ① — 왼쪽 1/3에 서서 오른쪽 위 창밖을 보는 하루", "16/9"),
               ("② 같은 대화에 이어서 — 대상 컷", "New composition, the next cut: the view out of the window — blue sky above a rooftop edge, a tiny pair of translucent insect wings glinting in the UPPER RIGHT of the frame. No people. Still no text.",
                "d6_glint", "예상 결과 ② — 창밖 하늘 오른쪽 위에 작게 반짝이는 날개", "16/9")],
      check=[("①의 하루가 왼쪽 1/3에서 오른쪽 위를 보나", "02_camera.html#s4"), ("②의 날개가 오른쪽 위에 있나", "#s4"), ("두 장을 이어 보면 '하루가 이것을 보았다'가 읽히나", "#s4")],
      expect="①은 오른쪽에 여백을 둔 하루, ②는 오른쪽 위에 작은 반짝임이 있는 하늘입니다. 이어 보면 하루의 시선이 반짝임으로 곧장 이어집니다.",
      trouble=[("②에 하루가 다시 나온다", "'No people'을 첫 문장 바로 뒤로 옮깁니다."),
               ("날개가 너무 크게 나온다", "'tiny, barely visible glint'처럼 크기를 줄여 적습니다. 5컷의 '깨달음'은 작은 단서에서 시작합니다."),
               ("①의 하루가 화면 가운데에 선다", "'on the left third of the frame'을 첫 문장에 둡니다.")],
      more="②에서 날개를 일부러 왼쪽 아래에 두고 만들어, 시선이 끊기는 느낌을 비교해 보세요."),
],
4: [
 dict(id="d1", title="중심축을 문장으로 넣어 문 밀기", goal="'몸 전체가 C자로 앞으로 기울고, 뒷발로 바닥을 민다'를 문장으로 넣어 7컷을 만들고, 받은 그림 위에 중심축을 그어 봅니다.",
      why="'pushing a door'만 적으면 팔만 뻗는 자세가 나오기 쉽습니다(4부 1단계 AI 결과 상자). 중심축과 받침 발을 함께 적어야 몸 전체가 따라옵니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 하루 참고 그림을 첨부합니다.", "프롬프트를 붙여 넣어 한 장을 만듭니다.",
             "받은 그림에서 머리 꼭대기에서 뒷발 끝까지 선을 그어 봅니다. C자로 휘었나요?", "무게중심(골반)에서 바닥으로 선을 내려 앞발 쪽으로 쏠렸는지 봅니다.", "곧게 서 있으면 같은 대화에 'Same image. Change only: lean her whole body forward …'로 자세만 고칩니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full body side view of " + who("haru") + " pushing a heavy metal rooftop door on the right side of the frame with both hands.",
                "Her whole body leans forward in a clear C-shaped curve from head to back foot, the back foot pushing off the floor, weight on the front leg, head down with effort. Light from the upper left.", bg="Simple bright stairwell background."),
               "d7_push", "예상 결과 — 몸 전체를 C자로 앞으로 기울여 무거운 문을 미는 하루의 옆모습", "2/3")],
      check=[("머리~뒷발이 C자로 휘었나(그림 위에 선 긋기)", "#s1"), ("무게가 앞발에 실렸나", "#s2"), ("검게 칠해도 팔이 몸통에서 떨어져 문으로 뻗어 보이나", "#s4")],
      expect="하루가 문 쪽으로 몸 전체를 기울이고 뒷발로 바닥을 밀어, 문이 무거워 보입니다. 선을 그어 보면 머리에서 뒷발까지 한 줄의 C자가 나옵니다.",
      trouble=[("팔만 뻗고 몸은 곧다", "'leaning forward with the whole body'를 첫 문장으로 옮기고 'not standing upright'를 덧붙입니다."),
               ("너무 기울어 넘어지는 것처럼 보인다", "'feet firmly planted, stable'을 덧붙여 받침을 되살립니다."),
               ("문이 왼쪽에 생긴다", "'the door on the RIGHT side of the frame'처럼 대상의 자리를 적습니다.")],
      more="같은 프롬프트에서 'C-shaped curve'를 빼고 만들어, 6부 f5와 비슷해지는지 비교해 보세요."),
 dict(id="d2", title="무게를 몸으로 보이기", goal="가벼운 우산을 든 하루와 무거운 상자를 든 하루를 차례로 만들어, 물건의 무게가 몸의 기울기로 보이는지 확인합니다.",
      why="무게는 물건의 크기가 아니라 몸의 반응으로 보입니다(4부 3단계). 몸의 반응(뒤로 기울기, 굽은 무릎)을 적지 않으면 상자가 종이처럼 가벼워 보입니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 하루 참고 그림을 첨부합니다.", "프롬프트 ①로 우산 그림을 만듭니다.", "같은 대화에 프롬프트 ②를 이어 붙여 상자 그림을 만듭니다.",
             "두 장의 중심축을 비교합니다. ②가 상자 반대쪽(뒤)으로 기울었나요?", "②가 곧게 서 있으면 새 대화에서 ②의 몸 반응 문장을 넣어 처음부터 만듭니다."],
      prompts=[("① 가벼운 우산", P("2:3", "Full body side view of " + who("haru") + " holding a closed light folding umbrella loosely at her side, standing upright and relaxed.", "Light from the upper left."),
                "d8_umbrella", "예상 결과 ① — 가벼운 우산을 들고 곧게 선 하루", "2/3"),
               ("② 같은 대화에 이어서", "Same image, keep the same framing. Change only: she now carries a big heavy cardboard lab box in front of her with both arms, leaning her upper body back to counterbalance the weight, knees slightly bent, feet apart. Still no text.",
                "d8_box", "예상 결과 ② — 무거운 상자를 앞으로 안고 몸을 뒤로 기울인 하루", "2/3")],
      check=[("①은 곧고, ②는 뒤로 기울었나", "#s3"), ("②의 무릎이 굽고 발이 벌어졌나", "#s2"), ("두 장 모두 같은 하루인가", "05_ai_cuts.html#s2")],
      expect="①은 거의 곧게 선 자세, ②는 상자 반대쪽으로 몸이 기울고 무릎이 굽은 자세입니다. 같은 상자 크기라도 무게는 몸의 기울기로 보입니다.",
      trouble=[("②가 곧게 서 있다", "'leaning back to counterbalance'를 첫머리에 두고 'not standing straight'를 덧붙입니다."),
               ("상자를 너무 가볍게 든다(한 손)", "'with both arms, arms strained'를 덧붙입니다."),
               ("②에서 구도가 바뀐다", "'keep the same framing'을 확인하고, 그래도 바뀌면 새 대화에서 처음부터 만듭니다.")],
      more="상자를 몸에서 멀리 든 자세('holding the box far out in front')로 만들어, 거리가 길수록 더 기우는지 4부 3단계 실험과 비교해 보세요."),
],
5: [
 dict(id="d1", title="여덟 조각으로 기준 컷 만들기", goal="5컷을 여덟 조각(샷·앵글·인물·동작·방향·감정·배경·빛)의 문장으로 만들어 기준 컷으로 확정합니다.",
      why="기준 컷은 나머지 일곱 컷의 바탕입니다(5부 4단계). 여덟 조각을 모두 채워 두면, 기준 컷을 고칠 때 어느 조각을 바꿀지 바로 보입니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 하루 참고 그림 두 장을 첨부합니다.", "아래 프롬프트를 붙여 넣습니다. 줄마다 한 조각입니다.",
             "받은 그림을 기준 시트와 나란히 놓고 고정값(번 2개, 가운데 남색 줄, 라벤더 후드, 흰 랩코트)을 하나씩 확인합니다.",
             "틀린 곳은 그 부분만 부분 수정으로 고칩니다. 다 맞으면 이 그림을 '기준 컷'으로 저장합니다.", "이 대화를 닫지 말고 다음 과제(d2)에 그대로 씁니다."],
      prompts=[("넣을 프롬프트(여덟 조각)", P("16:9", "Shot: close-up. Angle: eye level. Character: " + who("haru") + ". Action: lifting her head. Direction: looking toward the UPPER RIGHT of the frame. "
                "Emotion: startled realization, eyes wide, eyebrows raised. Background: bright corridor next to a large window on the right. Light: soft backlight from the window, afternoon.", bg=None),
               "d9_keycut", "예상 결과 — 여덟 조각으로 만든 5컷 기준 컷. 오른쪽 위를 올려다보며 깨닫는 하루의 얼굴 샷", "16/9")],
      check=[("여덟 조각이 모두 그림에 보이나(샷·앵글·방향·감정·배경·빛)", "#s1"), ("고정값 네 가지가 기준 시트와 같은가", "#s2"), ("1부 d2 ②와 비교해 같은 하루인가", None)],
      expect="얼굴이 화면을 채우는 하루가 오른쪽 위 창 쪽을 올려다보며 놀란 얼굴을 하고, 창에서 들어온 빛이 머리 가장자리를 밝힙니다. 이 그림이 나머지 컷의 기준이 됩니다.",
      trouble=[("뒤쪽 조각(배경·빛)이 무시된다", "중요한 조각을 앞에 둡니다. 이 컷의 목적에 필요한 샷·감정·방향을 먼저, 배경·빛을 뒤에 둡니다."),
               ("앞머리 남색 줄이 옆으로 간다", "그 부분만 칠해 'thick navy streak down the CENTER of the bangs'로 부분 수정합니다."),
               ("얼굴 샷인데 손이 들어와 가린다", "'hands out of frame'을 덧붙입니다.")],
      more="같은 여덟 조각에서 '앵글'만 'slight low angle'로 바꿔 만들어, 감정의 세기가 달라지는지 비교해 보세요."),
 dict(id="d2", title="기준 컷에 이어 6컷 만들기", goal="d1의 기준 컷을 만든 대화에서 6컷(계단을 오르는 앙각 전신)을 이어 만들어, 캐릭터가 유지되는지 확인합니다.",
      why="같은 대화에서 이어 만들면 캐릭터는 잘 지켜지지만, 앞 그림의 구도를 지나치게 따라 하기 쉽습니다(5부 4단계). 'New composition'으로 구도가 바뀐다는 것을 먼저 알립니다.",
      attach="d1에서 만든 기준 컷이 있는 대화 그대로(참고 그림 두 장 포함)",
      steps=["d1의 대화를 그대로 엽니다.", "아래 프롬프트를 이어 붙입니다.", "받은 6컷과 기준 컷을 나란히 놓고 고정값이 같은지 봅니다.",
             "6컷이 기준 컷과 같은 얼굴 샷으로 나오면, 새 대화를 열어 기준 컷과 기준 시트만 첨부하고 같은 프롬프트로 다시 만듭니다.", "고정값이 하나라도 틀리면 그 부분만 부분 수정합니다."],
      prompts=[("같은 대화에 이어서 — 6컷", "New composition, the next cut — do not reuse the previous framing. Shot: full body. Angle: low angle from the bottom of the stairs looking up. Character: the same Haru, exactly the same design as the key cut. "
                "Action: climbing the stairs quickly. Direction: moving toward the upper right of the frame. Emotion: determined. Background: a bright stairwell. Light: daylight from a window at the top of the stairs. Still no text, adult proportions.",
                "d10_next", "예상 결과 — 기준 컷에 이어 만든 6컷. 계단 아래에서 올려다본 하루가 오른쪽 위로 계단을 오르는 전신", "16/9")],
      check=[("구도가 기준 컷과 달리 앙각 전신으로 바뀌었나", "02_camera.html#s3"), ("번 2개·가운데 남색 줄·옷이 기준 컷과 같은가", "#s2"), ("오른쪽 위로 움직여 4·5컷의 시선 방향과 이어지나", "03_flow.html#s4")],
      expect="계단 아래에서 올려다본 하루가 오른쪽 위로 계단을 올라갑니다. 얼굴은 작아졌지만 머리 모양과 옷은 기준 컷과 같아, 같은 사람이 같은 이야기 속에서 움직이는 것으로 읽힙니다.",
      trouble=[("기준 컷과 같은 얼굴 샷이 나온다", "새 대화를 열고 기준 컷 + 기준 시트만 첨부해 같은 프롬프트로 만듭니다."),
               ("앙각이 지나쳐 발만 크다", "'slight low angle, camera at knee height'로 정도를 적습니다(2부 3단계)."),
               ("하루가 왼쪽 위로 오른다", "'moving toward the upper RIGHT'를 첫머리 가까이 옮깁니다.")],
      more="같은 방법으로 7컷과 8컷까지 이어 만들어, 7부 '컷 문장 공방'의 문장과 비교해 보세요."),
],
6: [
 dict(id="d1", title="뒤집힌 방향 고치기", goal="실패 그림 f2의 오른쪽 컷을 화면 기준 방향 문장으로 다시 만들어, ③ 흐름의 진단이 맞았는지 확인합니다.",
      why="방향 실패는 얼굴이나 옷을 고쳐도 낫지 않습니다(6부 1단계). 화면 기준 방향 하나만 바꿔 다시 만들면 원인이 맞았는지 바로 보입니다.",
      attach="f2_flip(사이트 assets/img/f2_flip.webp — 그림을 받은 뒤), refs/sia_anime_base.png",
      steps=["새 대화를 열고 f2 그림과 시아 참고 그림을 첨부합니다.", "아래 프롬프트로 오른쪽 컷만 다시 만듭니다.", "왼쪽 컷과 나란히 놓고 시아가 한 방향으로 걷는지 봅니다.",
             "오른쪽 컷의 배경·빛이 왼쪽 컷과 다르면 빛 문장을 덧붙여 다시 만듭니다(f8).", "그래도 왼쪽으로 걸으면 f2 그림을 첨부하지 않고 새 대화에서 만듭니다(앞 편 03에서 바로잡을 그림을 첨부하면 그 모양을 따라 그린 경험)."],
      prompts=[("넣을 프롬프트", P("16:9", "Full body side view of " + who("sia") + ", walking briskly toward the RIGHT side of the frame along the same sunny path in front of " + LAB + ", the same screen direction as the previous cut.", "Eye-level camera on the same side of the path as before. Afternoon light from the left.", bg=None),
               "d11_fix_dir", "예상 결과 — 같은 길에서 다시 화면 오른쪽으로 걷는 시아", "16/9")],
      check=[("시아가 화면 오른쪽으로 걷나", "03_flow.html#s1"), ("빛이 왼쪽에서 오나(왼쪽 컷과 같은가)", "#f8"), ("f2의 왼쪽 컷과 이어 놓으면 한 흐름인가", "#f2")],
      expect="시아가 왼쪽 컷과 같은 방향(오른쪽)으로 걸어, 두 컷을 이어 놓으면 '계속 앞으로 간다'로 읽힙니다.",
      trouble=[("여전히 왼쪽으로 걷는다", "f2 그림을 첨부하지 말고, 'the building entrance at the right edge of the frame'처럼 목적지를 화면 오른쪽에 둡니다."),
               ("배경이 왼쪽 컷과 달라진다", "'the same path, the same trees and building'을 덧붙입니다."),
               ("시아의 고정값이 바뀐다", "참고 그림을 다시 첨부하고 'no headdress, jet-black hair'를 적습니다.")],
      more="일부러 카메라를 정면(선 위)에 두고 'walking toward the camera'로 만들어, 다리 컷을 거치면 방향을 바꿔도 덜 어색한지 확인해 보세요."),
 dict(id="d2", title="바뀌는 캐릭터를 부분 수정으로 고치기", goal="실패 그림 f6에서 틀린 두 컷의 머리와 옷만 칠해 기준 시트대로 고칩니다. 맞은 컷은 그대로 둡니다.",
      why="여덟 컷 중 몇 장만 틀렸을 때 전체를 다시 만들면 맞았던 컷이 틀어질 수 있습니다(5부 2단계). 틀린 곳만 칠하는 부분 수정이 가장 안전합니다.",
      attach="f6_drift(사이트 assets/img/f6_drift.webp — 그림을 받은 뒤), refs/haru_sheet.png",
      steps=["도구의 부분 수정(영역 칠하기) 화면에서 f6 그림을 엽니다.", "둘째·셋째 컷의 머리(번·앞머리)와 후드만 칠합니다. 얼굴·손·배경은 칠하지 않습니다.", "기준 시트를 첨부하고 아래 문장을 넣습니다.",
             "결과를 기준 시트와 나란히 놓고 고정값을 확인합니다.", "칠한 곳 경계가 어색하면 칠한 영역을 조금 넓혀 다시 수정합니다."],
      prompts=[("부분 수정 문장", "Inpainting only inside the painted areas (hair and hoodie of panels 2 and 3). Haru: two round hair buns on top, a thick navy streak down the CENTER of the bangs, lavender hoodie with white drawstrings under an open white lab coat — exactly as in the attached reference sheet. Keep everything outside the painted areas unchanged. Adult proportions. No text, no letters, no numbers, no logos.",
                "d12_fix_bun", "예상 결과 — 둘째·셋째 컷의 머리와 후드만 고쳐 세 컷 모두 같은 하루가 된 그림", "16/9")],
      check=[("세 컷 모두 번 2개·가운데 남색 줄·라벤더 후드인가", "05_ai_cuts.html#s2"), ("칠하지 않은 곳(동작·배경·첫 컷)이 그대로인가", None), ("칠한 경계가 어색하지 않은가", None)],
      expect="둘째·셋째 컷의 하루에 번 두 개와 가운데 남색 줄이 돌아오고 후드가 라벤더색이 됩니다. 동작과 배경은 그대로라, 세 컷이 다시 한 사람의 이야기로 읽힙니다.",
      trouble=[("칠한 곳이 그대로다", "칠한 영역을 머리 윤곽 바깥까지 조금 넓히고 문장 첫머리에 'Replace the hair'를 둡니다."),
               ("얼굴까지 바뀐다", "얼굴을 칠하지 않았는지 확인합니다. 바뀌었으면 얼굴은 칠하지 않고 다시 합니다."),
               ("번이 셋 이상 생긴다", "'exactly two round hair buns'로 개수를 적습니다.")],
      more="고친 세 컷과 f6을 나란히 놓고, 6부 진단 데스크에서 f6의 원인(⑤ 고정값)을 다시 맞혀 보세요."),
],
}

CONV_D = [("D01_part1", "1부 연습 과제", "d1은 첨부 없음 · d2는 refs/haru_anime_base.png, refs/haru_sheet.png", ["d1_thumbs", "d2_cut5_plain", "d2_cut5_emotion"]),
          ("D02_part2", "2부 연습 과제", "refs/haru_anime_base.png, refs/haru_sheet.png (+ d4는 sia·moa anime_base)", ["d3_shot_full", "d3_shot_cu", "d4_corridor_eye"]),
          ("D03_part3", "3부 연습 과제", "refs/sia_anime_base.png, refs/sia_sheet.png, refs/haru_anime_base.png, refs/haru_sheet.png", ["d5_run_right", "d5_corridor_back", "d6_look", "d6_glint"]),
          ("D04_part4", "4부 연습 과제", "refs/haru_anime_base.png, refs/haru_sheet.png", ["d7_push", "d8_umbrella", "d8_box"]),
          ("D05_part5", "5부 연습 과제", "refs/haru_anime_base.png, refs/haru_sheet.png", ["d9_keycut", "d10_next"]),
          ("D06_part6", "6부 연습 과제 (실패 그림을 받은 뒤)", "f2_flip·f6_drift(사이트 assets/img/), refs/sia_anime_base.png, refs/haru_sheet.png", ["d11_fix_dir", "d12_fix_bun"])]
HOW = {"d2_cut5_emotion": "d2_cut5_plain을 만든 같은 대화에 이어서", "d3_shot_cu": "새 대화에서(d3_shot_full과 따로)", "d5_corridor_back": "d5_run_right를 만든 같은 대화에 이어서",
       "d6_glint": "d6_look을 만든 같은 대화에 이어서", "d8_box": "d8_umbrella를 만든 같은 대화에 이어서", "d10_next": "d9_keycut을 만든 같은 대화에 이어서",
       "d11_fix_dir": "f2_flip 그림을 받은 뒤 새 대화에서", "d12_fix_bun": "f6_drift 그림에서 '부분 수정(영역 칠하기)' — 둘째·셋째 컷의 머리와 후드만 칠하기"}
RETRY = {}
RETRY3 = {}
BASE_OF = {}

def items():
    out = {}
    for no, ds in DRILL.items():
        for d in ds:
            for lab, prompt, key, alt, ar in d["prompts"]:
                out[key] = (no, d["title"], lab, prompt, alt, ar)
    return out

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    D = os.path.join(ROOT, "docs", "image_requests_drill"); os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    IT = items(); rows = []; n = 0
    HEAD = ("해설 페이지의 '프롬프트 연습 과제' 예상 결과 그림을 한 장씩 차례로 만들어 줘.\n- 비율은 각 프롬프트 첫 줄을 따를 것(16:9는 가로 1920px 이상, 2:3은 세로 1536px 이상)\n"
            "- 첨부한 참고 이미지의 캐릭터 외형(얼굴·머리·색·장식)을 똑같이 지킬 것\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·과장된 체형·교복 느낌·어려 보이는 얼굴 금지\n"
            "- 그림 안에 글자·숫자·로고·컷 번호 금지\n- '같은 대화에 이어서'라고 적힌 그림은 바로 앞 그림을 바탕으로 적힌 것만 바꿀 것('New composition'이라고 적힌 것은 구도를 새로 잡을 것)")
    for cid, title, att, keys in CONV_D:
        md = f"# {cid[:3]} · {title} — " + ", ".join(keys) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD}\n```\n"
        for k in keys:
            no, dt, lab, prompt, alt, ar = IT[k]; n += 1
            how = HOW.get(k, "새로 만들기")
            rows.append([n, cid[:3], k, f"0{no}", dt, lab, ar.replace("/", ":"), how, ""])
            md += f"\n---\n## {k} — {no}부 「{dt}」 {lab}\n방법: {how}\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "part", "drill", "prompt", "ratio", "how", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 3 — '프롬프트 연습 과제' 예상 결과 ({n}장)

부마다 연습 과제 2개(모두 12개)의 **예상 결과 그림**입니다. 페이지의 과제 프롬프트와 이 요청문의 프롬프트는 같습니다(원본: `build/content_drill.py`).

## 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
""" + "".join(f"| {i+1} | prompts/{c[0]}.md | {len(c[3])} | {c[2]} |\n" for i, c in enumerate(CONV_D)) + """
## 주의
- 두 장이 짝인 과제(d2·d5·d6·d8·d10)는 **같은 대화에서 차례로** 만듭니다. d3의 두 장은 **서로 다른 새 대화**에서 만듭니다.
- d12_fix_bun은 그림 생성이 아니라 **부분 수정(영역 칠하기)** 기능으로 만듭니다. 칠하는 곳: 둘째·셋째 컷의 머리와 후드(얼굴·손·배경 제외).
- D06(d11·d12)은 꾸러미 1의 실패 그림 f2_flip·f6_drift를 **받은 뒤에** 요청합니다.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png·jpg).
""")
    print("drill images", n)
