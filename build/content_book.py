# -*- coding: utf-8 -*-
"""8부 콘티 북 — '내가 원하는 이야기'를 8·16·32컷 콘티로 만들고, 스케치 시트를 Genspark로 그린 뒤, 그 콘티를 다시 Genspark에 줘서 완성 컷을 만든다.
예제: 「하루의 하루」 — 하루가 집에서 일어나 연구실에 가서 모두를 만나고 콘티 회의를 하기까지 32컷.
이 파일이 예제 이야기·시트 프롬프트·완성 컷 프롬프트의 원본이다(build.py가 페이지와 생성기에, make_requests.py가 요청 꾸러미에 쓴다)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import who, ANI, SKETCH, END, ENDS

STORY_LINE = "하루가 아침에 집에서 일어나 출근길을 지나 연구실에 도착하고, 박사·시아·모아·주판봇·초파리·평가단 X1~X3를 모두 만난 뒤, 콘티 회의에서 오늘의 콘티를 완성한다."
BEATS = ["집", "출근길", "만남", "업무"]
# (번호, 목적, 흐름·동작, 감정·보충, 감정 세기, 샷, 앵글, 길이(초), 등장인물, 영어 컷 묘사)
S32 = [
 (1, "아침 침실을 보여 준다", "커튼 사이 햇빛, 이불 속 하루", "고요", 2, "원경", "눈높이", 3, "H", "wide shot of a small tidy bedroom in soft morning light, Haru asleep under the blanket"),
 (2, "알람에 눈을 뜬다", "손을 뻗어 알람을 끈다", "졸림", 3, "얼굴", "부감", 2.5, "H", "close-up from above: Haru opening one sleepy eye, her hand reaching for a ringing alarm clock"),
 (3, "하루를 시작한다", "침대에 앉아 기지개", "상쾌함", 4, "전신", "눈높이", 3, "H", "full body: Haru sitting up on the bed stretching both arms up, in modest long-sleeve pajamas"),
 (4, "정신을 차린다", "세면대에서 세수", "잠이 깸", 4, "허리 위", "눈높이", 2.5, "H", "waist-up: Haru washing her face at a bathroom sink, a mirror on the right"),
 (5, "머리를 묶는다", "거울 앞에서 정수리 번 두 개", "기대", 5, "가슴 위", "눈높이", 3, "H", "chest-up: Haru in front of a mirror tying her two round hair buns"),
 (6, "옷을 입는다", "후드 위에 흰 랩코트를 걸친다", "준비 끝", 5, "전신", "눈높이", 2.5, "H", "full body: Haru putting on a white lab coat over her lavender hoodie, a bag on a chair"),
 (7, "시간이 없다는 걸 안다", "토스트를 물고 오른쪽 벽시계를 봄", "서두름", 6, "허리 위", "눈높이", 2.5, "H", "waist-up: Haru biting a toast while glancing at a wall clock on the right, startled"),
 (8, "집을 나선다", "현관문을 열고 오른쪽으로 나감", "출발", 6, "전신", "눈높이", 3, "H", "full body: Haru opening the front door and stepping out toward the right into bright morning"),
 (9, "동네를 보여 준다", "골목을 오른쪽으로 걷는다", "상쾌함", 5, "원경", "눈높이", 3, "H", "wide shot: a quiet residential alley, small Haru walking toward the right"),
 (10, "버스를 기다린다", "정류장에서 휴대폰을 본다", "여유", 4, "전신", "눈높이", 3, "H", "full body: Haru waiting at a bus stop, looking at her phone"),
 (11, "버스 안", "창가 왼쪽 1/3에 앉아 오른쪽 창밖을 봄", "설렘", 5, "허리 위", "눈높이", 3, "H", "waist-up: Haru sitting by a bus window on the left third of the frame, looking out to the right, the city passing by"),
 (12, "오늘 일을 떠올린다", "고개를 들어 오른쪽 위를 본다", "깨달음 · 오늘은 콘티 회의", 7, "얼굴", "눈높이", 2.5, "H", "close-up: Haru lifting her head toward the upper right, suddenly remembering something"),
 (13, "버스에서 내린다", "오른쪽으로 뛰어내린다", "서두름", 6, "전신", "눈높이", 2, "H", "full body: Haru hopping off a bus and running toward the right"),
 (14, "길을 건넌다", "횡단보도를 오른쪽으로", "긴장", 6, "원경", "부감", 2.5, "H", "wide high angle: Haru crossing a crosswalk toward the right among a few pedestrians"),
 (15, "연구소가 보인다", "멈춰 서서 건물을 올려다봄", "기대", 6, "전신", "앙각", 3, "H", "low angle full body: Haru stopping and looking up at the research institute building ahead"),
 (16, "정문에 도착한다", "출입증을 찍는다", "안도", 5, "허리 위", "눈높이", 2.5, "H", "waist-up: Haru tapping her ID card on the institute entrance gate"),
 (17, "로비로 들어선다", "안쪽으로 걸어 들어감(뒷모습)", "설렘", 5, "전신(뒷모습)", "눈높이", 3, "H", "full body from behind: Haru walking into a bright lobby toward the far end"),
 (18, "박사를 만난다", "왼쪽의 박사가 손을 들어 인사", "반가움", 6, "허리 위(두 사람)", "눈높이", 3, "HD", "waist-up two shot: the Professor on the left raising a hand to greet Haru on the right"),
 (19, "시아·모아를 만난다", "복도에서 둘이 손을 흔든다", "즐거움", 6, "허리 위(세 사람)", "눈높이", 3, "HSM", "waist-up three shot: Sia and Moa waving at Haru in the corridor"),
 (20, "주판봇이 달려온다", "왼쪽에서 바퀴로 달려옴, 하루가 물러섬", "소란", 7, "전신", "낮은 눈높이", 2, "HB", "full body: AbaBot rolling fast toward Haru from the left, Haru stepping back in surprise"),
 (21, "초파리가 날아온다", "하루 어깨에 내려앉는다", "반가움", 7, "가슴 위", "눈높이", 2.5, "HF", "chest-up: the tiny Fruit Fly researcher landing on Haru's shoulder, Haru smiling sideways at it"),
 (22, "평가단을 지나간다", "심사석의 X1~X3가 점수판을 흔든다", "웃음", 6, "허리 위", "눈높이", 2.5, "HX", "waist-up: three small judges at a desk waving blank score paddles at Haru passing by"),
 (23, "모두 모인다", "연구실 한가운데 단체 인사", "소속감", 8, "원경", "살짝 부감", 4, "HDSMBFX", "wide slightly high angle: everyone gathered in the lab — Haru in the center, the Professor, Sia, Moa, AbaBot, the Fruit Fly and the three judges"),
 (24, "자리에 앉는다", "책상에 가방을 내려놓는다", "차분", 5, "허리 위", "눈높이", 2.5, "H", "waist-up: Haru putting her bag down at her desk and sitting"),
 (25, "콘티 회의가 시작된다", "박사가 화이트보드 앞에서 설명", "집중", 6, "허리 위", "눈높이", 3, "D", "waist-up: the Professor at a whiteboard holding eight blank sketch sheets, starting a meeting"),
 (26, "하루가 받아 적는다", "노트에 메모", "진지함", 6, "가슴 위", "부감", 2.5, "H", "chest-up high angle: Haru taking notes in a notebook"),
 (27, "주판봇이 큰 그림을 내민다", "아주 자세한 그림 한 장을 들이민다", "성급함", 6, "허리 위", "눈높이", 2.5, "B", "waist-up: AbaBot proudly holding up one very detailed drawing"),
 (28, "초파리가 한 문장을 제안한다", "작은 빈 보드에 쓰는 시늉", "차분함", 6, "가슴 위", "눈높이", 2.5, "F", "chest-up: the Fruit Fly holding a small blank board and a marker, calm"),
 (29, "시아·모아가 썸네일을 그린다", "포스트잇에 빠르게 그린다", "몰입", 7, "허리 위", "부감", 3, "SM", "waist-up high angle: Sia and Moa quickly sketching tiny thumbnails on sticky notes"),
 (30, "평가단이 점수를 든다", "빈 점수판을 동시에 든다", "긴장", 8, "허리 위", "눈높이", 2.5, "X", "waist-up: the three judges raising blank score paddles at once"),
 (31, "하루가 결정한다", "고개를 들어 오른쪽 위 화이트보드를 본다", "결의 · 절정", 9, "얼굴", "살짝 앙각", 3, "H", "close-up slight low angle: Haru looking up toward the upper right with determination"),
 (32, "콘티가 완성된다", "벽에 붙인 콘티, 창밖 노을", "뿌듯함 · 마무리", 6, "원경", "눈높이", 5, "HDSMBFX", "wide shot: the finished storyboard sheets pinned on the wall, the whole team by the window at sunset"),
]
S16 = [
 (1, "아침 침실, 알람에 깬다", "원경", "wide shot of a morning bedroom, Haru waking to an alarm clock"),
 (2, "기지개를 켜고 세수한다", "전신", "full body: Haru stretching on the bed in modest pajamas, then at the sink"),
 (3, "머리를 묶고 옷을 입는다", "허리 위", "waist-up: Haru in front of a mirror tying her two hair buns, lab coat on"),
 (4, "토스트를 물고 집을 나선다", "전신", "full body: Haru with toast in her mouth opening the front door toward the right"),
 (5, "골목을 지나 정류장으로", "원경", "wide shot: Haru walking toward the right down an alley to a bus stop"),
 (6, "버스 안에서 오늘 일을 떠올린다", "가슴 위", "chest-up: Haru by a bus window, looking up to the upper right, remembering"),
 (7, "내려서 길을 건넌다", "원경", "wide high angle: Haru running across a crosswalk toward the right"),
 (8, "연구소에 도착한다", "전신", "low angle full body: Haru arriving at the research institute gate"),
 (9, "로비에서 박사를 만난다", "허리 위", "waist-up two shot: the Professor greeting Haru in the lobby"),
 (10, "시아·모아, 그리고 주판봇", "전신", "full body: Sia and Moa waving while AbaBot rolls toward Haru from the left"),
 (11, "초파리와 평가단", "허리 위", "waist-up: the Fruit Fly on Haru's shoulder, three judges waving score paddles behind"),
 (12, "모두 모여 인사하고 자리에", "원경", "wide shot: everyone gathered around Haru in the lab"),
 (13, "회의가 시작되고 받아 적는다", "허리 위", "waist-up: the Professor at a whiteboard, Haru taking notes in the foreground"),
 (14, "주판봇의 그림과 초파리의 한 문장", "허리 위", "waist-up two shot: AbaBot holding a detailed drawing, the Fruit Fly holding a small blank board"),
 (15, "썸네일과 점수판", "허리 위", "waist-up: Sia and Moa sketching thumbnails, the judges raising blank paddles"),
 (16, "하루가 결정하고 콘티를 완성한다", "얼굴", "close-up: Haru looking up to the upper right with determination, storyboard sheets behind"),
]
S8 = [
 (1, "아침에 일어난다", "원경", "wide shot: a morning bedroom, Haru waking up and stretching"),
 (2, "준비하고 집을 나선다", "전신", "full body: Haru in her lab coat stepping out of the front door toward the right"),
 (3, "출근길, 오늘 일을 떠올린다", "가슴 위", "chest-up: Haru on a bus by the window, looking up to the upper right"),
 (4, "연구소에 도착한다", "전신", "low angle full body: Haru arriving at the research institute gate"),
 (5, "박사·시아·모아를 만난다", "허리 위", "waist-up: the Professor, Sia and Moa greeting Haru in the lobby"),
 (6, "주판봇·초파리·평가단까지 모두 모인다", "원경", "wide shot: everyone gathered around Haru in the lab"),
 (7, "콘티 회의", "허리 위", "waist-up: the Professor at a whiteboard, the team around the table"),
 (8, "결정하고 콘티를 완성한다", "얼굴", "close-up: Haru looking up to the upper right with determination"),
]
CODE = {"H": "haru", "D": "doctor", "S": "sia", "M": "moa", "B": "bot", "F": "fly", "X": "judges"}
CODE_KO = {"H": "하루", "D": "박사", "S": "시아", "M": "모아", "B": "주판봇", "F": "초파리", "X": "X1~X3"}
REF = {"H": "refs/haru_anime_base.png", "D": "refs/doctor_sheet.png", "S": "refs/sia_anime_base.png", "M": "refs/moa_anime_base.png", "B": "refs/jupanbot_ref_genspark_v0.png", "F": "refs/fruitfly_sprites_6.png"}
SIL = ("Keep every character recognizable by silhouette even in rough sketch form: Haru = slim adult woman with two round hair buns on top of her head and a long open lab coat; "
       "the Professor = taller adult man with spiky hair and rectangular glasses; Sia = adult woman with long straight hair, no accessories; Moa = adult woman with wavy hair and a headband with a small ribbon on her LEFT side; "
       "AbaBot = boxy monitor-head robot on tank treads with a short antenna; the Fruit Fly = tiny insect with round eyes, a helmet and wings; the judges = three small round figures (one with a side bow, one with a beret, one with a cat-ear hood).")

def sheet_prompt(n, k):
    """n컷 콘티의 k번째 시트(8컷) 프롬프트."""
    data = {8: S8, 16: S16, 32: S32}[n]
    rows = data[(k - 1) * 8:k * 8]
    head = f"Storyboard sheet {k} of {n // 8} for the {n}-cut storyboard, wide 16:9.\n{SKETCH}\n"
    cont = "" if k == 1 else "Continue from the attached previous sheet: exactly the same drawing style, line weight and character silhouettes.\n"
    lines = "Eight panels in two rows of four, read left to right, top to bottom. Story: a lab assistant's day from waking up at home to finishing a storyboard meeting at the lab.\n"
    for i, r in enumerate(rows):
        lines += f"Panel {i + 1} (cut {r[0]}): {r[-1]}.\n"
    return head + cont + lines + SIL + "\nEach panel has a thin empty border with three empty ruled lines under it (left blank).\n" + ENDS

def cut_prompt(c, method="crop"):
    r = S32[c - 1]
    sheet, pos = (c - 1) // 8 + 1, (c - 1) % 8 + 1
    chars = [who(CODE[x]) if CODE[x] in ("haru", "sia", "moa", "doctor") else {"bot": "AbaBot (boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray arms, small tank treads)",
             "fly": "the Fruit Fly researcher (tiny cartoon fruit fly, large red compound eyes, retro dark blue helmet with a yellow-white stripe, tiny white lab coat, translucent wings)",
             "judges": "three small cute dark navy silhouette judges with white dot eyes (one with a pink side-ponytail bow, one with a beret and teal round glasses, one with a cat-ear hood) holding blank score paddles"}[CODE[x]] for x in r[8]]
    if method == "crop":
        src = f"The attached sketch is cut {c} cropped from storyboard sheet {sheet} (panel {pos}). Use it ONLY for composition, camera angle and pose; do not copy the pencil style."
    else:
        src = f"The attached image is the whole storyboard sheet {sheet} with eight panels. Make only panel {pos} (cut {c}) as one finished illustration."
    return (f"Finished storyboard cut, wide 16:9.\n{ANI}\n{src}\nCut {c}: {r[-1]}.\nCharacters: " + "; ".join(chars) + f".\nEmotion: {EMO_EN.get(c, '')}.\n"
            "Keep the same camera, framing and screen direction as the sketch.\n" + END)
EMO_EN = {2: "sleepy, just waking", 8: "fresh start, eager", 11: "quiet excitement", 16: "relieved, arriving", 18: "warm greeting", 23: "sense of belonging, cheerful", 31: "determined, the climax of the day", 32: "proud, calm ending"}
DONE = [2, 8, 11, 16, 18, 23, 31, 32]
KEY = 31

def attach_for(c, method="crop"):
    r = S32[c - 1]
    a = [f"sheet_32_{(c - 1) // 8 + 1} 의 {(c - 1) % 8 + 1}번째 컷만 잘라 낸 그림" if method == "crop" else f"sheet_32_{(c - 1) // 8 + 1} 시트 전체"]
    a += [REF[x] for x in r[8] if x in REF]
    if c != KEY:
        a.append(f"done_c{KEY:02d}(기준 컷, 먼저 만든 뒤)")
    return a

P8 = dict(
 no=8, file="08_conti_book.html", og="og_08.jpg", cover_key="cover_08", model="haru",
 title="콘티 북 — 내 이야기를 8·16·32컷 콘티로, 콘티를 다시 완성 컷으로", kicker="8부 · 주인공 하루 · 모두 출연",
 desc="내가 원하는 이야기를 한 문장으로 쓰고, 8·16·32컷 콘티 표로 바꾸는 문장을 만들고, Genspark로 스케치 시트를 그린 뒤, 그 콘티를 다시 Genspark에 줘서 완성 컷을 만듭니다. 예제는 하루의 하루 32컷.",
 lead="이번 주인공은 하루입니다. 집에서 일어나 연구실에 와서 모두를 만나고 콘티 회의를 마치기까지, 하루의 하루를 32컷 콘티 북으로 만듭니다. 주판봇은 '하루의 하루 32컷'이라고 한 줄만 써서 한 장에 그리려 합니다. 초파리는 이야기를 표로 만들고, 시트 네 장으로 나누고, 고른 컷만 완성합니다.",
 three=("내 이야기를 한 문장과 네 덩어리로 정리해 8·16·32컷 콘티 표로 바꾸는 문장(프롬프트)을 만들고, 표를 8컷 시트로 나눠 스케치를 그린 뒤, 그 스케치를 다시 AI에 넣어 완성 컷을 만드는 전 과정을 익힙니다.",
        "1~7부는 이미 짜인 여덟 컷으로 배웠습니다. 내 이야기, 더 긴 이야기(16·32컷)가 되면 컷을 어떻게 나누고, AI에 어떤 순서로 넘겨야 할지 막힙니다.",
        "짧은 애니메이션·웹툰 한 화·광고 영상의 콘티 북, 이야기 회의 자료, AI로 연속 컷을 만드는 작업의 기획서에 씁니다."),
 cover_cap="연구실 벽 · 32장의 작은 콘티를 네 줄로 붙이는 하루와 모두",
 cover_cast=[("haru", "e19"), ("doctor", "e16"), ("fruitfly", "e09"), ("jupanbot", "e16")],
 intro=[("doctor", "e08", "이번엔 하루가 주인공이다. 집에서 일어나 여기 와서 우리를 모두 만나고 회의를 마치기까지. 32컷으로 가 보자."),
        ("jupanbot", "e16", "'하루의 하루 32컷'! 한 장에 서른두 컷 몰아서 그리면 1분이면 끝납니다!"),
        ("fruitfly", "e09", "한 장에 서른두 컷이면 컷 하나가 손톱보다 작아져서 누가 누군지 안 보여. 이야기부터 표로 만들고, 여덟 컷씩 네 장으로 나누자."),
        ("haru", "e14", "제 하루가 콘티가 된다니… 아침에 토스트 먹는 것까지 나와요?")],
 steps=[
  dict(id="s1", title="한 문장 이야기를 네 덩어리로 나누면 컷 수만 바꿔도 된다", sub="이야기를 한 문장으로 쓰고 네 덩어리(여기서는 집·출근길·만남·업무)로 자른 뒤, 컷 수를 8·16·32로 바꿔도 덩어리마다 똑같이 나눕니다",
       how="방법: 네 덩어리 × 컷 수", day="일상: 피자 나누기",
       why=["콘티 북은 8컷보다 긴 이야기를 다룹니다. 컷 수가 늘수록 어디에 컷을 쓸지 헷갈립니다.",
            "처음부터 32컷을 하나씩 적어 나가면 앞쪽(집)에 컷이 몰리고, 정작 중요한 만남과 업무가 급하게 끝납니다.",
            "먼저 한 문장 이야기와 네 덩어리를 정하고, 덩어리마다 컷 수 ÷ 4만큼 나눕니다. 8컷이면 2컷씩, 16컷이면 4컷씩, 32컷이면 8컷씩입니다. 1부 1단계의 원리를 그대로 키운 것입니다."],
       easy="피자를 4조각으로 자르든 8조각·16조각으로 자르든, 먼저 십자로 4등분해 두면 조각 크기가 고르게 나옵니다.",
       math=dict(ask="컷 수가 네 배가 되면 장면도 네 배로 길어져요?",
                 words="한 컷 평균 길이를 그대로 두면 전체 길이는 컷 수에 비례해서 늘어납니다. 시트는 8컷에 한 장이라 컷 수 ÷ 8장이 필요합니다.",
                 tries=["8컷: 덩어리마다 8 ÷ 4 = 2컷, 8 × 3초 = 24초, 시트 1장", "16컷: 덩어리마다 4컷, 16 × 3초 = 48초, 시트 2장", "32컷: 덩어리마다 8컷, 32 × 3초 = 96초, 시트 4장"],
                 school="나눗셈과 비례 — 컷 수가 두 배면 길이도 두 배입니다.",
                 formula="덩어리별 컷 수 = 컷 수 ÷ 4,  전체 길이 ≈ 컷 수 × 한 컷 평균 길이,  시트 수 = 컷 수 ÷ 8",
                 pieces=[("컷 수", "8·16·32 중 하나"), ("4", "이야기의 네 덩어리"), ("한 컷 평균 길이", "예시 3초"), ("8", "시트 한 장에 담는 컷 수(빈 콘티 양식과 같음)")],
                 comment="32컷이면 1분 36초짜리 장면에 시트 네 장! 덩어리마다 여덟 컷이면 '만남'에서 아홉 명을 다 만날 수 있겠어요."),
       daily="여행 일정도 '1박 2일'을 '3박 4일'로 늘릴 때, 출발·관광·식사·귀가 덩어리는 그대로 두고 덩어리마다 일정을 더 넣습니다.",
       field="웹툰 한 화는 수십 컷, 짧은 애니메이션 한 장면은 수십~수백 컷입니다. 연출가는 먼저 장면을 덩어리로 나누고(시퀀스), 덩어리마다 컷 수를 배정한 다음 콘티를 그립니다.",
       talk=[("doctor", "e07", "하루의 하루를 8·16·32컷으로 만들 때, 덩어리마다 몇 컷씩?"),
             ("jupanbot", "e16", "집에서 일어나는 장면에 20컷! 하루 잠옷이 귀여우니까요!"),
             ("fruitfly", "e09", "그럼 우리를 만날 컷이 모자라. 이걸 눌러 봐 — 컷 수를 바꿔 가며 덩어리를 봐."),
             ("haru", "e10", "32컷이면 집·출근길·만남·업무에 8컷씩이에요. 96초, 시트 네 장. 8컷이면 2컷씩이라 저 혼자 지나가는 느낌이고요.")],
       panel=dict(key="p8_beats", note="컷 수를 바꿔 보세요 · 색은 덩어리, 굵은 테두리는 시트 경계", ctrl='<label>컷 수 <select name="n"><option value="8">8컷</option><option value="16">16컷</option><option value="32" selected>32컷</option></select></label><label>한 컷 평균(초) <input type="range" name="sec" min="1.5" max="5" step="0.5" value="3"></label>'),
       solve=["덩어리를 먼저 정하면 컷 수가 바뀌어도 이야기의 무게가 고르게 나뉩니다.",
              "컷 수가 늘면 장면이 길어지고 시트도 늘어납니다. 32컷은 96초 안팎, 시트 네 장입니다.",
              "실제 예제의 컷 길이는 2~5초로 다르게 두어 합계가 조금 다릅니다(아래 예제 표). 덩어리 배분은 그대로 두고 컷마다 길이만 조정합니다."],
       img=("sheet_8", "하루의 하루를 8컷으로 줄인 연필 콘티 시트 — 두 줄 네 장, 침실에서 일어나는 원경부터 오른쪽 위를 바라보는 하루의 얼굴 샷까지", "16/9"),
       ai=("AI에게 '32컷 콘티를 만들어 줘'라고 했더니 집 장면이 15컷이나 됩니다. 어떻게 할까요?",
           "덩어리와 컷 수를 문장에 적습니다. 'four parts of 8 cuts each: home 1–8, commute 9–16, meeting everyone 17–24, work 25–32'처럼 컷 번호 범위까지 적으면 한쪽으로 몰리지 않습니다(3단계 생성기가 자동으로 넣습니다)."),
       limit="덩어리를 똑같이 나누는 것은 출발점입니다. 실제 작품은 중요한 덩어리에 컷을 더 줍니다. 32컷 96초, 한 컷 3초는 예시값입니다.",
       quiz=("32컷 콘티를 8컷짜리 시트에 나눠 그리면 몇 장일까?", ["2장", "4장", "8장"], 1,
             "32 ÷ 8 = 4장입니다.", "시트 한 장에 8컷씩 들어갑니다.")),
  dict(id="s2", title="컷 하나를 둘로 쪼개면 이야기가 자세해진다", sub="8컷의 한 컷을 16컷에서는 두 컷으로, 32컷에서는 네 컷으로 쪼갭니다. 쪼갤 때는 '그 사이에 무슨 일이 있었나'를 묻습니다",
       how="방법: 8 → 16 → 32 쪼개기", day="일상: 요리법 단계",
       why=["같은 이야기를 컷 수만 늘리면, 컷마다 무엇을 새로 보여 줄지 막힙니다.",
            "늘어난 컷을 같은 장면의 다른 각도로만 채우면 6부 f1(목적 없는 컷)이 됩니다.",
            "8컷의 한 컷을 시작과 끝으로 보고, 그 사이에 있었던 일을 하나씩 꺼내 컷으로 만듭니다. 8컷 「준비하고 집을 나선다」는 16컷에서 「머리 묶고 옷 입기 · 토스트 물고 나서기」, 32컷에서 「머리 묶기 · 옷 입기 · 시계 보기 · 현관문」이 됩니다."],
       easy="요리법 '찌개를 끓인다' 한 줄을 '재료 썰기 → 볶기 → 물 붓기 → 간 보기'로 나누면 처음 하는 사람도 따라 할 수 있습니다.",
       math=dict(ask="쪼갤수록 한 컷이 짧아지는 거예요, 장면이 길어지는 거예요?",
                 words="둘 중 하나를 고릅니다. 전체 길이를 그대로 두면 한 컷이 짧아지고, 한 컷 길이를 그대로 두면 전체가 길어집니다.",
                 tries=["8컷 24초에서 한 컷 = 24 ÷ 8 = 3초", "같은 24초를 32컷으로: 한 컷 24 ÷ 32 = 0.75초 — 너무 짧아 읽기 어렵다", "한 컷 3초를 지키면 32컷은 96초 — 이 예제의 선택"],
                 school="나눗셈 — 같은 길이를 더 많이 나누면 하나가 작아집니다.",
                 formula="한 컷 길이 = 전체 길이 ÷ 컷 수",
                 pieces=[("전체 길이", "장면 전체가 화면에 머무는 시간"), ("컷 수", "8 → 16 → 32"), ("0.75초", "감정이 전해지기엔 너무 짧은 길이(3부 3단계)")],
                 comment="0.75초 컷 서른두 개는 정신없겠어요. 그래서 컷을 늘리면 장면도 길어지는 거군요."),
       daily="사진 앨범도 하루를 사진 4장으로 보면 '아침·점심·오후·저녁'이고, 32장으로 보면 '토스트 굽기'처럼 작은 순간까지 담깁니다.",
       field="콘티 작업에서 감독이 '여기 컷 하나 더 넣자'고 하면, 연출가는 앞뒤 컷의 시작과 끝 사이에 생략된 동작이나 반응을 꺼내 새 컷을 만듭니다. 반대로 줄일 때는 목적이 겹치는 컷을 합칩니다.",
       talk=[("doctor", "e07", "8컷의 3번 「출근길, 오늘 일을 떠올린다」를 32컷으로 쪼개면?"),
             ("jupanbot", "e16", "같은 버스 장면을 네 각도에서요! 앞, 뒤, 위, 아래!"),
             ("fruitfly", "e09", "그럼 목적이 다 같아. 이걸 눌러 봐 — 컷 하나가 어떻게 갈라지는지."),
             ("haru", "e10", "골목 → 정류장 → 버스 창가 → 고개를 들며 기억해 냄. 네 컷 목적이 다 달라요. 마지막 컷이 깨달음이라 얼굴 샷이고요.")],
       panel=dict(key="p8_split", note="8컷 중 하나를 고르면 16컷·32컷에서 어떻게 갈라지는지 보입니다", ctrl='<label>8컷 중 <select name="c">' + "".join(f'<option value="{i}"{" selected" if i == 3 else ""}>{i}컷 — {S8[i - 1][1]}</option>' for i in range(1, 9)) + '</select></label>'),
       solve=["8컷의 한 컷은 16컷에서 두 컷, 32컷에서 네 컷이 됩니다. 새로 생긴 컷마다 목적이 다릅니다.",
              "쪼갠 네 컷 안에서도 감정 곡선이 오르내립니다(골목 5 → 정류장 4 → 창가 5 → 깨달음 7). 작은 덩어리 안에도 작은 절정이 생깁니다.",
              "생성기(3단계)에서 '8컷 표를 먼저 만들고, 각 컷을 네 컷으로 쪼개라'고 두 번에 나눠 요청하면 AI도 목적이 겹치지 않게 쪼갭니다."],
       img=("sheet_16_1", "하루의 하루 16컷 중 시트 1(1~8컷)의 연필 스케치 — 알람에 깨는 침실부터 연구소 정문 도착까지", "16/9"),
       ai=("AI에게 8컷 콘티를 32컷으로 늘려 달라고 했더니, 같은 장면을 줌만 다르게 한 컷이 많습니다.",
           "'Split each cut into four cuts. Each new cut must show a different moment or reaction that happened between the start and the end of the original cut — do not repeat the same moment with different zoom.'처럼 쪼개는 규칙을 적습니다."),
       limit="모든 컷을 똑같이 네 개로 쪼갤 필요는 없습니다. 중요한 컷은 더 많이, 이동 컷은 덜 쪼개기도 합니다. 이 예제는 원리를 보이려고 고르게 쪼갰습니다.",
       quiz=("8컷 24초 장면을 길이 그대로 32컷으로 쪼개면 한 컷은 몇 초일까?", ["0.75초", "1.5초", "3초"], 0,
             "24 ÷ 32 = 0.75초입니다. 너무 짧아 이 예제는 한 컷 3초를 지키고 장면을 늘렸습니다.", "전체 길이를 컷 수로 나눠 보세요.")),
  dict(id="s3", title="콘티 표를 요청하는 문장에는 열과 규칙을 적는다", sub="대화형 AI에게 '이야기 + 컷 수 + 표의 열 + 지킬 규칙'을 한 번에 적어 주면, 바로 시트로 옮길 수 있는 콘티 표가 나옵니다",
       how="방법: 콘티 표 프롬프트", day="일상: 엑셀 양식 주기",
       why=["이야기를 32컷으로 나누는 일은 대화형 AI(텍스트)에게 맡길 수 있습니다. 그림은 그다음입니다.",
            "'32컷 콘티 짜 줘'라고만 하면 컷마다 적힌 항목이 들쭉날쭉하고, 샷·방향·감정이 빠져 그림 프롬프트로 옮길 수 없습니다.",
            "표의 열(컷·덩어리·목적·흐름·동작·감정·보충·감정 세기·샷·앵글·길이·등장인물·영어 묘사)과 규칙(덩어리별 컷 수, 절정 위치, 가상선, 같은 샷 3컷 연속 금지, 성인)을 문장에 적습니다. 영어 묘사 열은 4단계 시트 프롬프트에 그대로 붙여 넣습니다."],
       easy="일을 맡길 때 빈 엑셀 양식을 주면, 누가 채워도 같은 모양의 표가 돌아옵니다.",
       daily="설문지도 '자유롭게 써 주세요'보다 항목을 정해 주면 답을 모아 비교하기 쉽습니다.",
       field="AI를 쓰는 콘티 작업자들은 대화형 AI로 컷 표를 먼저 만들고, 사람이 목적·감정 곡선을 고친 뒤 그림 생성 AI로 넘깁니다. 표를 고치는 것이 그림을 다시 만드는 것보다 훨씬 쌉니다.",
       talk=[("doctor", "e07", "하루의 하루를 32컷 표로 만들려면 AI에게 뭐라고 할까?"),
             ("jupanbot", "e16", "'하루의 하루 32컷'! 짧을수록 AI가 좋아합니다!"),
             ("fruitfly", "e09", "그럼 샷도 방향도 없는 표가 와. 이걸 눌러 봐 — 이야기와 컷 수를 넣으면 문장이 만들어져."),
             ("haru", "e10", "열 열두 개, 규칙 여섯 개가 들어간 문장이 나왔어요. 제 이야기 대신 아무 이야기나 넣어도 같은 모양의 표가 오겠네요.")],
       panel=dict(key="p8_text", note="이야기를 고쳐 쓰고 컷 수를 골라 보세요 · 아래 문장을 대화형 AI(Genspark 대화 등)에 그대로 넣습니다", ctrl='<label>컷 수 <select name="n"><option value="8">8컷</option><option value="16">16컷</option><option value="32" selected>32컷</option></select></label><label><input type="checkbox" name="two" checked> 8컷 표부터 만들고 쪼개기(두 번에 나눠 요청)</label><label><input type="checkbox" name="cast" checked> 등장인물 목록 넣기</label>'),
       solve=["열과 규칙이 정해진 문장을 넣으면 이야기가 달라져도 같은 모양의 표가 옵니다.",
              "'두 번에 나눠 요청'을 켜면 8컷 표를 먼저 받아 확인하고, 그다음 각 컷을 쪼개 달라고 합니다. 2단계의 쪼개기 원리가 그대로 들어갑니다.",
              "받은 표는 1부 3단계 감정 곡선과 2부 1단계 샷 표로 한 번 점검하고 고친 뒤 4단계로 넘깁니다. 아래 '하루의 하루 32컷' 표가 이렇게 만들어 다듬은 결과입니다."],
       ai=("대화형 AI가 표를 32줄이 아니라 30줄에서 멈췄습니다.",
           "긴 표는 중간에 끊기기 쉽습니다. 'Output cuts 1–16 now; I will ask for 17–32 next.'처럼 둘로 나눠 받거나, 덩어리별(8컷씩)로 받습니다. 받은 뒤 컷 번호가 1~32까지 빠짐없이 있는지 확인합니다."),
       limit="표 문장은 대화형 AI의 종류에 따라 결과가 다릅니다. 받은 표는 그대로 쓰지 말고 사람이 목적·감정·샷을 점검합니다. 이 문장은 이 페이지의 규칙을 옮긴 예시입니다.",
       quiz=("콘티 표 문장에 '영어 묘사' 열을 넣는 까닭은?", ["표를 예쁘게 하려고", "시트 그림 프롬프트에 그대로 붙여 넣으려고", "길이를 재려고"], 1,
             "영어 묘사 열을 시트 프롬프트의 패널 줄로 그대로 옮깁니다.", "4단계에서 무엇을 만드는지 떠올려 보세요.")),
  dict(id="s4", title="여덟 컷씩 시트로 나눠 그리고 앞 시트를 붙여 잇는다", sub="32컷을 한 장에 그리지 않고 8컷 시트 네 장으로 나눕니다. 둘째 장부터는 앞 시트를 첨부해 같은 그림체와 실루엣으로 잇습니다",
       how="방법: 스케치 시트 프롬프트", day="일상: 연재 만화",
       why=["표가 생겼으니 이제 그림 생성 AI(Genspark)로 콘티 스케치를 그립니다.",
            "32컷을 한 장에 요청하면 컷 하나가 엄지손톱보다 작아져 아홉 명을 구별할 수 없고, 컷 번호·글자가 깨진 무늬로 들어가기 쉽습니다.",
            "8컷 시트(두 줄 네 장)로 나눠 한 장씩 만듭니다. 패널마다 표의 영어 묘사를 한 줄씩 넣고, 등장인물 실루엣 규칙을 붙입니다. 둘째 장부터는 같은 대화에서 앞 시트를 첨부하고 '같은 그림체·실루엣으로 잇기'를 적습니다."],
       easy="연재 만화는 한 화씩 그리되, 지난 화를 옆에 펴 놓고 그림체를 맞춥니다.",
       math=dict(ask="한 장에 32컷을 넣으면 컷이 얼마나 작아져요?",
                 words="시트의 넓이를 컷 수로 나눕니다. 컷이 네 배 많아지면 한 컷의 넓이는 1/4, 가로·세로는 각각 절반이 됩니다.",
                 tries=["가로 1920px 시트에 4장씩: 한 컷 너비 약 1920 ÷ 4 = 480px", "8장씩(32컷을 4줄): 1920 ÷ 8 = 240px", "240px 컷의 인물은 키 100px 안팎 — 머리가 손톱만 해 누구인지 안 보임"],
                 school="나눗셈 — 같은 너비를 더 많이 나누면 하나가 작아집니다.",
                 formula="한 컷 너비 ≈ 시트 너비 ÷ 한 줄의 컷 수",
                 pieces=[("시트 너비", "Genspark 그림의 가로 픽셀(예시 1920)"), ("한 줄의 컷 수", "8컷 시트는 4, 32컷을 한 장에 넣으면 8"), ("머리 크기", "컷이 작아지면 실루엣 표시도 사라진다")],
                 comment="480px과 240px, 너비가 절반이면 넓이는 1/4이네요. 네 장으로 나누는 게 맞아요."),
       daily="단체 사진을 한 장에 100명 넣으면 얼굴을 못 찾지만, 반별로 네 장 찍으면 모두 보입니다.",
       field="AI 그림 작업자들은 여러 컷을 한 장에 받을 때 4~9컷을 넘기지 않는 편입니다. 컷이 많으면 시트를 나누고, 같은 대화에서 앞 결과를 참고 그림으로 붙여 일관성을 지킵니다.",
       talk=[("doctor", "e07", "32컷 스케치, 몇 장으로 그릴까?"),
             ("jupanbot", "e16", "한 장! 서른두 컷을 촘촘하게!"),
             ("fruitfly", "e09", "그럼 X1·X2·X3가 점 세 개가 돼. 이걸 눌러 봐 — 시트를 골라 프롬프트를 봐."),
             ("haru", "e10", "시트 3에 만남 여덟 컷이 들어가요. 실루엣 규칙 덕에 스케치에서도 주판봇은 네모, 초파리는 날개로 구별돼요.")],
       panel=dict(key="p8_sheet", note="컷 수와 시트를 골라 보세요 · 아래 프롬프트가 Genspark에 넣을 그대로입니다", ctrl='<label>컷 수 <select name="n"><option value="8">8컷</option><option value="16">16컷</option><option value="32" selected>32컷</option></select></label><label>시트 <select name="k"><option value="1">1장</option><option value="2">2장</option><option value="3" selected>3장</option><option value="4">4장</option></select></label>'),
       solve=["시트 한 장에 8컷이면 컷이 충분히 커서 실루엣과 방향이 보입니다.",
              "둘째 장부터 앞 시트를 첨부하면 선 굵기와 인물 실루엣이 이어집니다(5부 2단계 기준 시트와 같은 원리).",
              "받은 시트는 빈 콘티 양식(7부 부록)처럼 아래 세 줄을 비워 둡니다. 세 줄은 그림 밖에서 표로 관리합니다."],
       img=("sheet_32_3", "하루의 하루 32컷 중 시트 3(만남, 17~24컷)의 연필 스케치 — 두 줄 네 장, 로비로 들어가는 뒷모습부터 모두 모인 단체 컷과 자리에 앉는 하루까지", "16/9"),
       ai=("둘째 시트의 하루가 첫째 시트와 달리 번 없이 그려졌습니다.",
           "첫째 시트를 첨부했는지 확인하고, 'Haru = two round hair buns on top' 같은 실루엣 규칙을 문장에 다시 붙입니다. 그래도 빠지면 그 컷만 부분 수정으로 번을 그려 넣습니다."),
       limit="8컷 시트는 이 시리즈의 빈 콘티 양식에 맞춘 단위입니다. 도구에 따라 4컷·6컷이 더 안정적일 수 있습니다. 픽셀 수치는 예시값입니다.",
       quiz=("가로 1920px 시트에 한 줄 4컷이면 한 컷 너비는 대략?", ["240px", "480px", "960px"], 1,
             "1920 ÷ 4 = 480px입니다.", "시트 너비를 한 줄의 컷 수로 나눠 보세요.")),
  dict(id="s5", title="콘티를 다시 AI에 주면 완성 컷이 된다 — 잘라서, 기준 컷부터", sub="스케치 시트에서 컷 하나를 잘라 첨부하고, '구도와 자세만 참고'라고 적어 완성 컷을 만듭니다. 감정이 가장 높은 컷을 기준 컷으로 먼저 만듭니다",
       how="방법: 콘티 → 완성 컷", day="일상: 설계도로 집 짓기",
       why=["콘티의 목적은 결국 완성 그림(또는 영상)입니다. 스케치를 버리지 않고 다시 AI에 넣으면 구도가 그대로 살아납니다(5부 3단계).",
            "시트를 통째로 첨부하면 AI가 여러 컷이 든 그림을 다시 그리거나, 연필 그림체까지 따라 합니다. 서른두 컷을 다 완성하려 하면 그림이 너무 많아 일관성도 무너집니다.",
            "① 시트에서 컷 하나만 잘라 첨부하고 ② '구도·카메라·자세만 참고, 완성은 애니풍 채색'을 적고 ③ 등장인물 기준 그림을 함께 붙입니다. 덩어리마다 두 컷씩, 여덟 컷만 완성하고, 감정이 가장 높은 31컷을 기준 컷으로 먼저 만든 뒤 나머지에 기준 컷을 첨부합니다."],
       easy="설계도를 들고 집을 지을 때, 설계도 종이를 벽에 붙이는 게 아니라 그 선을 따라 벽을 세웁니다.",
       math=dict(ask="서른두 컷 중에 여덟 컷만 완성하면 나머지는요?",
                 words="덩어리마다 두 컷씩 골라 전체의 1/4만 완성합니다. 나머지는 같은 방법으로 직접 해 보는 연습으로 남깁니다. 완성 컷도 5부 2단계처럼 장수가 늘수록 모두 맞을 확률이 내려갑니다.",
                 tries=["완성할 컷: 덩어리 4 × 2컷 = 8컷(32컷의 25%)", "한 장 맞을 확률 0.97이면 8장 모두 ≈ 0.97⁸ ≈ 0.78", "32장 모두면 0.97³² ≈ 0.38 — 장수를 줄이고 기준 컷을 먼저 세우는 까닭"],
                 school="곱셈과 거듭제곱 — 5부 2단계와 같은 계산입니다.",
                 formula="완성 컷 수 = 덩어리 수 × 덩어리별 고른 컷,  모두 맞을 확률 = (한 장 확률)^장수",
                 pieces=[("덩어리별 고른 컷", "감정이 높은 컷, 여럿이 모이는 컷"), ("0.97", "기준 시트·고정값을 쓴 한 장 확률(예시값)"), ("기준 컷", "가장 먼저 완성해 나머지에 첨부하는 컷")],
                 comment="32장이면 0.38까지 떨어지네요. 고른 여덟 장부터 확실히 맞추는 게 낫겠어요."),
       daily="결혼식 사진도 수백 장을 찍지만 앨범에는 순서를 대표하는 몇 장만 골라 크게 넣습니다.",
       field="애니메이션은 콘티 다음에 핵심 장면의 '레이아웃'과 '키 비주얼'을 먼저 확정하고 나머지를 맞춥니다. AI 작업에서도 대표 컷을 먼저 승인받고 나머지를 같은 기준으로 만듭니다.",
       talk=[("doctor", "e07", "18컷 '박사를 만난다'를 완성한다. 무엇을 첨부할까?"),
             ("jupanbot", "e16", "시트 3을 통째로요! 앞뒤 컷까지 보면 더 잘 알겠죠!"),
             ("fruitfly", "e09", "그럼 여덟 컷짜리 그림이 또 나와. 이걸 눌러 봐 — 첨부 방법을 바꿔 가며."),
             ("haru", "e10", "18컷만 잘라 붙이고, 박사님과 제 기준 그림, 먼저 만든 31컷을 함께 첨부하니 구도는 스케치 그대로, 얼굴은 우리 그대로예요.")],
       panel=dict(key="p8_cut", note="컷과 첨부 방법을 골라 보세요 · 완성할 여덟 컷은 ★", ctrl='<label>컷 <select name="c">' + "".join(f'<option value="{r[0]}"{" selected" if r[0] == 18 else ""}>{r[0]}컷{" ★" if r[0] in DONE else ""} — {r[1]}</option>' for r in S32) + '</select></label><label>첨부 방법 <select name="m"><option value="sheet" selected>시트 통째로</option><option value="crop">그 컷만 잘라서</option></select></label>'),
       solve=["컷 하나만 잘라 첨부하고 '구도만 참고'를 적으면, 스케치의 카메라와 자세가 완성 컷에 그대로 남습니다.",
              "시트를 통째로 첨부하면 여러 컷 그림이 다시 나오거나 연필 그림체가 남기 쉽습니다. 아래 A/B 비교 그림 두 장으로 직접 확인해 보세요.",
              "기준 컷(31컷)을 먼저 완성하고, 나머지 일곱 컷에는 기준 컷과 등장인물 기준 그림을 함께 첨부합니다. 아홉 명이 모이는 23·32컷은 기준 그림이 많아 가장 어렵습니다. 흔들리면 6부 진단 순서로 원인을 찾습니다."],
       img=("done_c31", "기준 컷으로 먼저 완성한 31컷 — 회의실에서 고개를 들어 오른쪽 위 화이트보드를 바라보는 하루의 얼굴 샷, 결의에 찬 표정", "16/9"),
       ai=("잘라서 첨부했는데도 완성 컷이 스케치와 다른 구도로 나왔습니다.",
           "'Keep the same camera, framing and screen direction as the sketch.'를 첫머리 가까이 옮기고, 도구에 참고 그림 강도 막대가 있으면 낮춥니다(5부 3단계). 그래도 바뀌면 새 대화에서 잘라 낸 컷과 기준 컷만 첨부해 다시 만듭니다."),
       limit="잘라 낸 스케치가 아주 작으면(가로 300px 아래) 구도 참고가 약해집니다. 시트를 크게 받거나 잘라 낸 컷을 두 배로 키워 첨부합니다. 확률 값은 예시값입니다.",
       quiz=("32컷 중 덩어리마다 두 컷씩 완성하면 모두 몇 컷일까?", ["4컷", "8컷", "16컷"], 1,
             "4 × 2 = 8컷입니다.", "덩어리 수에 덩어리별 고른 컷 수를 곱해 보세요.")),
 ],
 judge=dict(title="8부 평가 — 누구의 콘티 북이 완성 컷까지 갔나",
   setup=[("doctor", "e08", "주판봇은 한 줄로 32컷 한 장을, 초파리는 표 → 시트 네 장 → 기준 컷 → 완성 여덟 컷으로 갔다. 평가단, 부탁한다."), ("x1", "e13", "읽힘·원리·자연스러움 각 10점 만점입니다.")],
   items=["읽힘(이야기가 보이나)", "원리(덩어리·쪼개기·시트·기준 컷)", "자연스러움"], a=("주판봇", [3, 2, 4]), b=("초파리", [9, 9, 8]),
   comments=[("x1", "e09", "주판봇의 32컷 한 장은 컷이 너무 작아 저희 셋이 점 세 개로 나왔어요."), ("x2", "e16", "초파리는 표를 먼저 고치고 그렸어요. 시트 네 장의 실루엣이 이어져요."), ("x3", "e04", "31컷 기준 컷 덕에 완성 여덟 장의 하루가 모두 같은 하루예요.")],
   result=[("doctor", "e19", "초파리 26 : 주판봇 9. 긴 이야기일수록 표 → 시트 → 기준 컷 순서가 지름길이다."), ("jupanbot", "e20", "1분 만에 끝났는데 하루가 잠옷 입고 회의에 갔더라고요…")]),
 summary=[("1단계 네 덩어리", "덩어리별 컷 = 컷 수 ÷ 4, 시트 = 컷 수 ÷ 8", "덩어리와 컷 번호 범위를 문장에"),
          ("2단계 쪼개기", "한 컷 길이 = 전체 ÷ 컷 수, 쪼갠 컷은 목적이 달라야", "'그 사이에 무슨 일이 있었나'"),
          ("3단계 표 문장", "열 + 규칙 + 이야기, 8컷 표부터", "받은 표는 사람이 점검"),
          ("4단계 시트", "8컷씩 나눠 그리고 앞 시트 첨부", "실루엣 규칙을 매번"),
          ("5단계 완성 컷", "잘라서 첨부, 기준 컷 먼저, 덩어리마다 두 컷", "구도만 참고, 그림체는 새로")],
 outro=[("doctor", "e08", "이야기가 콘티가 되고, 콘티가 다시 그림이 됐다. 이 순서면 어떤 이야기든 된다."),
        ("fruitfly", "e09", "이제 생성기에 각자 이야기를 넣어 봐. 빈 콘티 양식도 있어."),
        ("haru", "e19", "다음엔 모아 씨의 주말로 해 봐요!")],
 prev=("practice/index.html", "← 7부 실전 연습장"), next=("index.html", "목차로 →"),
)

if __name__ == "__main__":
    print(sum(r[7] for r in S32), "초 ·", len(S32), "컷")
    print(sheet_prompt(32, 3)[:400])

# ---- 8부 '직접 만들어 보기'와 연습 과제 ----
from content_make import T
MAKE8 = [
 T("sheet_32_1", "32컷 시트 1 — 실루엣 규칙의 힘", "시트 1(집, 1~8컷)을 만들어 연필 마네킹으로도 하루가 알아보이는지 봅니다.",
   "B — 원리 빼기: 실루엣 규칙 지우기", "Same sheet, keep the same layout. Change only: remove the character silhouette rules — draw every figure as an identical plain mannequin with no hair, glasses, robot or insect features. Still no text.",
   [("여덟 컷 모두 하루가 번 두 개로 알아보이나", "#s4"), ("컷마다 목적이 달라 보이나(침실 → 현관)", "#s2"), ("B에서 시트 3(만남)을 그린다면 누가 누군지 구별될지 상상해 보기", "#s4")],
   b_key="sheet_32_1_b", tip="실루엣 규칙은 아홉 명이 나오는 시트 3·4에서 더 중요합니다. 시트 1에서 먼저 확인해 두세요."),
 T("done_c31", "기준 컷 — 스케치를 붙였을 때와 안 붙였을 때", "31컷을 스케치를 잘라 붙여 만든 A와, 글만으로 만든 B를 비교해 콘티를 다시 주는 효과를 확인합니다.",
   "B — 원리 빼기: 스케치 없이 글만으로", "In a NEW conversation with NO sketch attached (only refs/haru_anime_base.png), make cut 31 from the text alone: close-up of Haru looking up with determination in a meeting room. Compare the camera and direction with done_c31.",
   [("A의 카메라(살짝 앙각)와 시선(오른쪽 위)이 스케치와 같은가", "#s5"), ("B는 시선 방향·앵글이 스케치와 달라졌는가", "03_flow.html#s4"), ("A·B 모두 같은 하루(번 2개, 가운데 남색 줄)인가", "05_ai_cuts.html#s2")],
   b_key="done_c31_b", tip="A는 시트 4에서 31컷(일곱 번째)만 잘라 첨부합니다."),
]
MOA = [("a sunny rooftop garden in the morning, small Moa watering flower pots", "원경"), ("Moa carrying a basket of herbs down the stairs toward the right", "전신"),
       ("Moa in the lab kitchen kneading bread dough", "허리 위"), ("close-up: Moa peeking into the oven window, hopeful", "얼굴"),
       ("Moa taking a tray of round bread rolls out of the oven, steam rising", "허리 위"), ("Moa walking toward the right with the tray into the bright lab", "전신"),
       ("Haru, Sia and the Professor gathering around the tray, surprised and happy", "허리 위"), ("wide shot: everyone eating bread together by the window", "원경")]
def moa_sheet():
    from make_requests import SKETCH, ENDS
    t = "Storyboard sheet 1 of 1 for the 8-cut storyboard, wide 16:9.\n" + SKETCH + "\nEight panels in two rows of four, read left to right, top to bottom. Story: Moa spends her weekend morning growing herbs on the lab rooftop and baking bread for everyone.\n"
    for i, (d, _) in enumerate(MOA): t += f"Panel {i + 1} (cut {i + 1}): {d}.\n"
    return t + SIL + "\nEach panel has a thin empty border with three empty ruled lines under it (left blank).\n" + ENDS
def moa_cut(method):
    from make_requests import ANI, END
    src = ("The attached sketch is cut 5 cropped from the storyboard sheet. Use it ONLY for composition, camera angle and pose; do not copy the pencil style." if method == "crop"
           else "The attached image is the whole storyboard sheet with eight panels. Make only panel 5 (cut 5) as one finished illustration.")
    return ("Finished storyboard cut, wide 16:9.\n" + ANI + "\n" + src + "\nCut 5: waist-up, " + who("moa") + " taking a tray of round bread rolls out of the oven, steam rising, proud smile.\n"
            "Keep the same camera, framing and screen direction as the sketch.\n" + END)
DRILL8 = [
 dict(id="d1", title="내 이야기로 8컷 시트 만들기", goal="모아의 주말 이야기를 생성기로 8컷 표로 만들고, 표의 영어 묘사로 시트 한 장을 그립니다.",
      why="하루의 하루 32컷은 페이지가 미리 다듬은 예제입니다. 내 이야기로 바꾸면 덩어리 나누기(1단계)와 표 문장(3단계)을 처음부터 직접 해 보게 됩니다. 처음엔 8컷 한 장으로 시작하는 편이 고치기 쉽습니다(1부 4단계).",
      attach="첨부 없음(연필 마네킹 + 실루엣 규칙)",
      steps=["3단계 생성기의 이야기 입력란에 '모아가 주말 아침 연구실 옥상에서 허브를 키우고, 빵을 구워 모두에게 나눠 준다'를 넣고 8컷을 고릅니다.", "나온 문장을 대화형 AI에 넣어 8컷 표를 받습니다.",
             "표를 1부 3단계(감정 곡선)·2부 1단계(샷)로 점검하고 고칩니다.", "표의 영어 묘사를 패널 줄로 옮긴 아래 프롬프트로 Genspark에서 시트를 만듭니다(직접 만든 표와 비교해 보세요).", "모아가 여덟 컷 모두 머리띠와 리본으로 알아보이는지 확인합니다."],
      prompts=[("시트 프롬프트", moa_sheet(), "d16_moa_sheet", "예상 결과 — 모아의 주말 8컷 연필 시트. 옥상 화단 원경에서 시작해 모두 함께 빵을 먹는 원경으로 끝남", "16/9")],
      check=[("네 덩어리에 두 컷씩 나뉘었나", "#s1"), ("4컷(오븐 들여다보기)이 얼굴 샷인가 — 기대가 가장 높은 컷", "01_beats.html#s3"), ("모아가 실루엣(머리띠·왼쪽 리본)으로 알아보이나", "#s4")],
      expect="두 줄 네 장의 연필 시트가 나옵니다. 1·8컷은 넓게, 4컷은 얼굴 가까이, 가운데는 허리 위·전신이 섞입니다. 마네킹이지만 모아는 머리띠로 알아봅니다.",
      trouble=[("컷 번호·글자가 생긴다", "'no text, no panel numbers'를 다시 붙입니다."), ("모아가 마네킹이라 누군지 모르겠다", "실루엣 규칙 문장을 패널 줄 바로 뒤로 옮깁니다."), ("여섯 컷만 나온다", "'exactly eight panels, two rows of four'를 덧붙입니다.")],
      more="같은 이야기를 16컷으로 바꿔 시트 두 장을 만들고, 2단계처럼 한 컷이 어떻게 둘로 갈라지는지 비교해 보세요."),
 dict(id="d2", title="잘라서 vs 통째로 — 내 시트로 완성 컷", goal="d1의 시트에서 5컷을 잘라 첨부한 완성 컷과, 시트를 통째로 첨부한 완성 컷을 비교합니다.",
      why="5단계에서 '잘라서 첨부'를 권했습니다. 내 시트로 두 방법을 직접 비교하면, 통째로 첨부했을 때 여러 컷 그림이나 연필 그림체가 남는지 눈으로 확인할 수 있습니다. 결과는 도구와 그날에 따라 다릅니다.",
      attach="d1에서 받은 시트(① 5컷만 잘라 낸 그림 / ② 시트 전체) + refs/moa_anime_base.png",
      steps=["d1 시트에서 5컷(오븐에서 빵을 꺼냄)만 사각형으로 잘라 둡니다.", "새 대화에서 잘라 낸 그림과 모아 기준 그림을 첨부하고 프롬프트 ①을 넣습니다.", "다른 새 대화에서 시트 전체와 모아 기준 그림을 첨부하고 프롬프트 ②를 넣습니다.",
             "두 결과를 스케치 5컷과 나란히 놓고 구도·카메라·그림체를 비교합니다.", "②가 의외로 잘 나왔다면 그대로 기록하세요 — 결과는 매번 다릅니다."],
      prompts=[("① 잘라서 첨부", moa_cut("crop"), "d17_moa_crop", "예상 결과 ① — 5컷만 잘라 붙여 만든 완성 컷. 스케치와 같은 구도의 모아가 오븐에서 빵을 꺼냄", "16/9"),
               ("② 시트 통째로 첨부(새 대화)", moa_cut("whole"), "d17_moa_whole", "예상 결과 ② — 시트 전체를 붙여 만든 결과. 여러 컷이 든 그림이 나오거나 연필 그림체가 남기 쉬움", "16/9")],
      check=[("①의 구도·카메라가 스케치 5컷과 같은가", "#s5"), ("②에 여러 컷이 들어가거나 연필선이 남았나", "#s5"), ("두 결과 모두 모아의 고정값(머리띠, 왼쪽 리본)이 지켜졌나", "05_ai_cuts.html#s2")],
      expect="①은 스케치 그대로의 구도에 채색된 모아가 나옵니다. ②는 여러 컷짜리 그림으로 나오거나, 한 컷이어도 구도가 스케치와 달라지기 쉽습니다.",
      trouble=[("①도 연필 그림체가 남는다", "'final art in clean anime cel shading, full color'를 덧붙입니다."), ("①의 구도가 바뀐다", "잘라 낸 그림을 두 배로 키워 다시 첨부합니다."), ("리본이 오른쪽에 붙는다", "그 부분만 부분 수정합니다.")],
      more="①로 만든 5컷을 기준 컷 삼아 8컷(모두 함께 빵 먹기)까지 이어 만들어 보세요(5부 4단계)."),
]
