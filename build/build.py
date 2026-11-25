# -*- coding: utf-8 -*-
"""구조 먼저 그리기 연구실 05 · 콘티 편 — 페이지 빌드.
python3 build/build.py 로 index.html, 01~06 페이지, practice/index.html, practice/template.html 을 다시 만든다.
그림 파일(assets/img/{키}.webp)이 있으면 넣고, 없으면 '그림 준비 중' 자리만 둔다."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2, P3
from content_b import P4, P5, P6
from content_make import MAKE
from make_requests import PROMPTS, CONV_OF, ATTACH_OF
from img_notes import ALT, DRILL_RES, RETRY_RES, RETRY3_RES
from content_drill import DRILL, RETRY, BASE_OF, RETRY3
from content_book import P8, S32, S16, S8, BEATS, STORY_LINE, sheet_prompt, cut_prompt, attach_for, DONE, KEY, MAKE8, DRILL8, CODE_KO
from make_requests_book import BOOK_PROMPTS, BOOK_CONV_OF, BOOK_ATTACH_OF
PROMPTS.update(BOOK_PROMPTS); CONV_OF.update(BOOK_CONV_OF); ATTACH_OF.update(BOOK_ATTACH_OF)
MAKE[8] = MAKE8; DRILL[8] = DRILL8

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = "v1.0"
DATE = "2026-11-26"
SITE = "https://adminmrobo.github.io/drawing_lab_05/"
FACE_SITE = "https://adminmrobo.github.io/drawing_lab_03/"
CLOTH_SITE = "https://adminmrobo.github.io/structure_first_drawing_lab_01/"
FIRST_SITE = "https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"
REPO = "https://github.com/adminmrobo/drawing_lab_05"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
RENDER = "https://adminmrobo.github.io/ai_rendering/"
CHARREPO = "https://github.com/adminmrobo/fruitfly-lab-expressions"
SERIES = "구조 먼저 그리기 연구실 05 · 콘티 편"
E = html.escape
PARTS = [P1, P2, P3, P4, P5, P6]

CH = {
 "doctor": ("박사", "해설 · 감독 + 모델(4부). 짙은 머리의 흰 줄, 굵은 눈썹, 청록 사각 안경"),
 "haru": ("조수 하루", "예시 콘티의 주인공 · 모델(2부) + 수식 상자 담당. 정수리 번 2개와 앞머리 가운데 남색 줄"),
 "sia": ("시아", "인턴1 · 모델(3부, 하루의 대역으로 걷기). 흑발, 머리 장식 없음"),
 "moa": ("모아", "인턴2 · 모델(1부, 컷마다 감정 연기). 흰 프릴 머리띠와 왼쪽 귀 위 흰 리본"),
 "jupanbot": ("주판봇", "콘티 작가 A. 첫 컷부터, 그림부터 서두른다 — 흔한 실수 담당"),
 "fruitfly": ("초파리 연구원", "콘티 작가 B. 목적과 원리부터 의심한다. \"이걸 눌러 봐\""),
 "x1": ("X1", "평가단. 이야기가 읽히는지 본다"),
 "x2": ("X2", "평가단. 원리를 본다"),
 "x3": ("X3", "평가단. 자연스러움을 본다"),
}
COLOR = {"doctor": "doc", "haru": "asst", "fruitfly": "fly", "jupanbot": "robo", "sia": "sia", "moa": "moa", "x1": "x", "x2": "x", "x3": "x"}

ABBR = [("콘티(그림 콘티)", "영상·만화의 장면을 컷 단위로 나눠 작은 그림과 글로 적은 설계도. 일본어 絵コンテ, 영어 storyboard"),
        ("컷", "카메라가 끊기지 않고 한 번에 보여 주는 한 장면. 콘티에서는 그림 하나"), ("썸네일", "엄지손톱만 하게 빨리 그린 작은 밑그림"),
        ("세 줄", "컷 아래 적는 목적 · 흐름·동작 · 감정·보충"), ("샷 크기", "인물을 화면에 얼마나 크게 담나. 원경(LS)·전신(FS)·무릎 위(KS)·허리 위(WS)·가슴 위(BS)·얼굴(CU)"),
        ("눈높이 선(EL)·소실점(VP)", "카메라 눈높이에 그은 가로선(지평선)과, 멀어지는 평행선이 모이는 점"), ("앙각·부감", "아래에서 올려다보는 앵글과 위에서 내려다보는 앵글"),
        ("가상선(180도 규칙)", "인물의 움직임이나 두 사람을 잇는 선. 카메라를 한쪽에만 두어 화면 방향을 지킨다"), ("팬·줌", "카메라가 옆으로 도는 것과 가까워지는(멀어지는) 것"),
        ("프레임", "영상을 이루는 그림 한 장. 애니메이션·영화는 1초에 24프레임이 흔하다"), ("중심축(라인 오브 액션)", "머리에서 체중 실린 발까지 흐르는 몸의 큰 선"),
        ("기준 시트(일관성 기준)", "캐릭터의 정면·옆·뒤, 얼굴, 옷을 모은 기준 그림"), ("강도(이미지 투 이미지)", "첨부한 밑그림을 AI가 얼마나 다시 그릴지 정하는 값"),
        ("부분 수정(인페인팅)", "칠한 영역만 다시 그리고 나머지는 그대로 두는 AI 기능")]

KG = [
 ("method/four-beats", "Method", "네 덩어리로 컷 나누기", "Splitting a story into four beats", "01_beats.html", "#s1", "시작·전개·전환·끝에 2컷씩. 전체 길이 = 컷 수 × 한 컷 길이"),
 ("method/three-lines", "Method", "컷의 세 줄", "Three lines per cut", "01_beats.html", "#s2", "목적 · 흐름·동작 · 감정·보충을 짧은 동사로 적는다"),
 ("concept/emotion-curve", "Concept", "감정 곡선", "Emotion curve", "01_beats.html", "#s3", "변화량 = 이번 컷 − 앞 컷, 절정은 6~7컷, 절정 앞에 한 번 내린다"),
 ("method/thumbnail", "Method", "썸네일 밑그림", "Thumbnail sketch", "01_beats.html", "#s4", "동그라미 머리 + 십자선 + 선 몇 개, 한 컷 1분"),
 ("concept/shot-size", "Concept", "샷 크기", "Shot size", "02_camera.html", "#s1", "머리 하나의 화면 높이 = 화면 높이 ÷ 화면에 들어가는 머리 수"),
 ("concept/eye-level", "Concept", "눈높이 선과 소실점", "Eye level line and vanishing point", "02_camera.html", "#s2", "크기는 거리에 반비례, 눈높이 선은 모두의 같은 높이를 지난다"),
 ("concept/camera-angle", "Concept", "앵글(앙각·부감)", "Camera angle", "02_camera.html", "#s3", "카메라가 낮으면 지평선이 아래로·인물이 크게, 높으면 위로·작게"),
 ("method/lead-room", "Method", "시선 여백과 3분할", "Lead room and rule of thirds", "02_camera.html", "#s4", "바라보는 쪽 여백 ÷ 반대쪽 여백 ≈ 2"),
 ("concept/axis-line", "Concept", "가상선(180도 규칙)", "The 180-degree rule", "03_flow.html", "#s1", "카메라는 선의 한쪽에만, 넘을 땐 정면·뒷모습 컷"),
 ("method/motion-arrows", "Method", "움직임 화살표", "Motion arrows", "03_flow.html", "#s2", "인물은 속이 찬 화살표, 카메라는 속이 빈 화살표, 줌은 끝 화면 틀"),
 ("concept/cut-timing", "Concept", "컷 길이와 프레임", "Cut timing and frames", "03_flow.html", "#s3", "프레임 수 = 컷 길이(초) × 24"),
 ("method/eyeline-match", "Method", "시선 잇기", "Eyeline match", "03_flow.html", "#s4", "앞 컷에서 바라본 방향에 다음 컷의 대상을 둔다"),
 ("concept/line-of-action", "Concept", "중심축", "Line of action", "04_pose.html", "#s1", "휜 정도 = 곧은 선에서 가장 멀리 떨어진 거리 ÷ 중심축 길이"),
 ("concept/balance", "Concept", "무게중심과 받침", "Center of gravity and base of support", "04_pose.html", "#s2", "가중 평균. 받침 안이면 안정, 밖이면 움직임"),
 ("method/prop-weight", "Method", "소품 무게 보이기", "Showing the weight of props", "04_pose.html", "#s3", "몸이 옮겨 갈 거리 = 물건 무게 × 거리 ÷ 몸무게"),
 ("method/silhouette", "Method", "실루엣 점검", "Silhouette check", "04_pose.html", "#s4", "검게 칠해도 팔다리가 몸통에서 떨어져 보이게, 과장은 중심축이 무너지기 전까지"),
 ("method/cut-prompt", "Method", "컷 문장 여덟 조각", "Eight-part cut prompt", "05_ai_cuts.html", "#s1", "샷·앵글·인물·동작·방향·감정·배경·빛 + 금지"),
 ("method/reference-sheet", "Method", "일관성 기준 시트", "Consistency reference sheet", "05_ai_cuts.html", "#s2", "여덟 장 모두 맞을 확률 = (한 장 맞을 확률)⁸"),
 ("method/sketch-strength", "Method", "밑그림 강도", "Image-to-image strength", "05_ai_cuts.html", "#s3", "다시 그리는 단계 = 전체 단계 × 강도, 0.35~0.6에서 시작"),
 ("method/key-cut", "Method", "기준 컷 먼저", "Key cut first", "05_ai_cuts.html", "#s4", "기준 컷을 확정하고 같은 대화에서 이어 만들며 틀린 컷만 부분 수정"),
 ("method/conti-diagnosis", "Method", "콘티 진단 순서", "Storyboard diagnosis order", "06_failure_lab.html", "#s1", "이야기 → 카메라 → 흐름 → 포즈 → 고정값"),
 ("application/conti-failures", "Application", "콘티·컷 실패 8종", "Eight storyboard failures", "06_failure_lab.html", "#fails", "목적 없는 컷·뒤집힌 방향·거인·떠 있는 사람·뻣뻣한 자세·바뀌는 캐릭터·막힌 시선·바뀌는 빛"),
 ("open/age-drift", "OpenQuestion", "나이가 어려 보이는 쏠림", "Apparent age drift", "06_failure_lab.html", "#drift", "큰 머리·작은 몸·낮은 눈 줄·짧은 코가 겹치면 어려 보인다. 성인 나이와 비율을 적어 막는다"),
 ("application/practice", "Application", "실전 연습장", "Practice simulator", "practice/index.html", "#bench", "콘티 작업대·카메라 촬영장·컷 문장 공방·진단 데스크"),
 ("application/template", "Application", "빈 콘티 양식", "Blank storyboard template", "practice/template.html", "#tpl", "여덟 컷 · 세 줄 · 샷과 길이를 적는 인쇄용 양식"),
 ("method/conti-book", "Method", "콘티 북 만들기", "Making a storyboard book", "08_conti_book.html", "#s1", "한 문장 이야기 → 네 덩어리 × 컷 수 → 표 → 8컷 시트 → 완성 컷"),
 ("method/cut-splitting", "Method", "컷 쪼개기", "Splitting cuts", "08_conti_book.html", "#s2", "8 → 16 → 32, 한 컷 길이 = 전체 길이 ÷ 컷 수, 쪼갠 컷은 목적이 달라야"),
 ("method/table-prompt", "Method", "콘티 표 프롬프트", "Storyboard table prompt", "08_conti_book.html", "#s3", "이야기 + 컷 수 + 표의 열 + 규칙을 대화형 AI에"),
 ("method/sheet-prompt", "Method", "스케치 시트 프롬프트", "Storyboard sheet prompt", "08_conti_book.html", "#s4", "8컷씩 나눠 그리고 둘째 장부터 앞 시트 첨부, 실루엣 규칙"),
 ("method/sketch-to-cut", "Method", "콘티로 완성 컷 만들기", "From storyboard to finished cut", "08_conti_book.html", "#s5", "그 컷만 잘라 첨부, 구도만 참고, 기준 컷 먼저, 덩어리마다 두 컷"),
 ("analogy/pizza", "Analogy", "피자 나누기", "Cutting a pizza", "08_conti_book.html", "#s1", "먼저 4등분해 두면 8·16조각도 고르게"),
 ("analogy/travel-plan", "Analogy", "여행 일정", "Planning a trip", "01_beats.html", "#s1", "출발과 도착을 먼저 정하면 일정이 한쪽으로 쏠리지 않는다"),
 ("analogy/rail-track", "Analogy", "기찻길 끝", "Railway tracks meeting", "02_camera.html", "#s2", "두 레일이 만나는 점이 소실점, 그 높이가 내 눈높이"),
 ("analogy/football", "Analogy", "축구 중계 카메라", "Football broadcast camera", "03_flow.html", "#s1", "카메라가 반대편 스탠드로 넘어가면 공격 방향이 뒤집혀 보인다"),
 ("analogy/bow", "Analogy", "활 당기기", "Drawing a bow", "04_pose.html", "#s1", "휜 모양만 봐도 힘이 들어간 것을 안다"),
 ("analogy/hair-salon", "Analogy", "단골 미용실 사진", "Showing a photo at the hair salon", "05_ai_cuts.html", "#s2", "'지난번처럼'보다 사진을 보여 줘야 같게 나온다"),
]
KG_EDGES = [("method/four-beats","motivates","method/three-lines"),("method/three-lines","motivates","concept/emotion-curve"),("concept/emotion-curve","motivates","method/thumbnail"),
 ("method/thumbnail","motivates","concept/shot-size"),("concept/shot-size","motivates","concept/eye-level"),("concept/eye-level","motivates","concept/camera-angle"),("concept/camera-angle","motivates","method/lead-room"),
 ("method/lead-room","motivates","concept/axis-line"),("concept/axis-line","motivates","method/motion-arrows"),("method/motion-arrows","motivates","concept/cut-timing"),("concept/cut-timing","motivates","method/eyeline-match"),
 ("method/eyeline-match","motivates","concept/line-of-action"),("concept/line-of-action","motivates","concept/balance"),("concept/balance","motivates","method/prop-weight"),("method/prop-weight","motivates","method/silhouette"),
 ("method/silhouette","motivates","method/cut-prompt"),("method/cut-prompt","motivates","method/reference-sheet"),("method/reference-sheet","motivates","method/sketch-strength"),("method/sketch-strength","motivates","method/key-cut"),
 ("method/key-cut","motivates","method/conti-diagnosis"),("method/conti-diagnosis","usedIn","application/conti-failures"),("method/reference-sheet","explains","open/age-drift"),("concept/shot-size","explains","open/age-drift"),
 ("concept/emotion-curve","explains","concept/shot-size"),("concept/emotion-curve","explains","concept/camera-angle"),("method/three-lines","explains","method/cut-prompt"),("method/thumbnail","explains","method/sketch-strength"),
 ("concept/axis-line","explains","application/conti-failures"),("concept/eye-level","explains","application/conti-failures"),
 ("analogy/travel-plan","explains","method/four-beats"),("analogy/rail-track","explains","concept/eye-level"),("analogy/football","explains","concept/axis-line"),("analogy/bow","explains","concept/line-of-action"),("analogy/hair-salon","explains","method/reference-sheet"),
 ("method/cut-prompt","usedIn","application/practice"),("application/practice","motivates","method/conti-book"),("method/conti-book","motivates","method/cut-splitting"),("method/cut-splitting","motivates","method/table-prompt"),
 ("method/table-prompt","motivates","method/sheet-prompt"),("method/sheet-prompt","motivates","method/sketch-to-cut"),("method/four-beats","explains","method/conti-book"),("method/sketch-strength","explains","method/sketch-to-cut"),
 ("method/key-cut","explains","method/sketch-to-cut"),("method/reference-sheet","explains","method/sheet-prompt"),("analogy/pizza","explains","method/conti-book"),("method/three-lines","usedIn","application/template"),("concept/shot-size","usedIn","application/practice")]
REFS = [
 dict(id="user_refs_2026", title="참고 이미지 5장 — 그림 콘티 템플릿(흑백·인쇄용 8컷), 원근과 인물 크기 도해, 어린이·성인 얼굴 비교, 손에 든 물건과 자세의 중심축 도해, 캐릭터 일관성 기준 시트 예시", author="사용자 제공 자료", year=2026, note="콘티 양식(목적·흐름·감정 세 줄), 눈높이 선과 소실점, 성인 얼굴 신호, 중심축·물건 무게·과장, 일관성 기준 시트의 원리만 참고. 그림·문장·도식·구성은 옮기지 않고 연구실 캐릭터와 실험으로 새로 구성"),
 dict(id="katz_1991_shot", title="Film Directing Shot by Shot: Visualizing from Concept to Screen", author="Steven D. Katz", year=1991, note="Michael Wiese Productions — 콘티(스토리보드)로 장면과 카메라를 설계하는 방법"),
 dict(id="bordwell_2019_filmart", title="Film Art: An Introduction (12th ed.)", author="David Bordwell, Kristin Thompson, Jeff Smith", year=2019, note="McGraw-Hill — 샷 크기·앵글, 180도 규칙(가상선), 시선 일치 같은 편집의 연속성"),
 dict(id="thomas_1981_illusion", title="The Illusion of Life: Disney Animation", author="Frank Thomas, Ollie Johnston", year=1981, note="Abbeville Press — 연출(스테이징)·실루엣·과장 같은 애니메이션 원칙"),
 dict(id="loomis_1951_drawing", title="Successful Drawing", author="Andrew Loomis", year=1951, note="Viking Press — 눈높이 선(지평선)과 소실점, 같은 키의 인물을 거리에 맞춰 놓는 법"),
 dict(id="meng_2022_sdedit", title="SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations", author="Chenlin Meng et al.", year=2022, note="ICLR 2022. arXiv:2108.01073 — 밑그림에 잡음을 더한 뒤 다시 그려 구도를 남기는 방식(강도의 원리)"),
 dict(id="rombach_2022_ldm", title="High-Resolution Image Synthesis with Latent Diffusion Models", author="Robin Rombach et al.", year=2022, note="CVPR 2022. arXiv:2112.10752 — 글 지시로 그림을 만드는 확산 모델(이미지 투 이미지·부분 수정 포함)"),
 dict(id="lugmayr_2022_repaint", title="RePaint: Inpainting using Denoising Diffusion Probabilistic Models", author="Andreas Lugmayr et al.", year=2022, note="CVPR 2022. arXiv:2201.09865 — 칠한 영역만 다시 그리는 방식"),
 dict(id="ruiz_2023_dreambooth", title="DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation", author="Nataniel Ruiz et al.", year=2023, note="CVPR 2023. arXiv:2208.12242 — 여러 그림에서 같은 대상을 지키는 문제(캐릭터 일관성)"),
 dict(id="prev_03", title="구조 먼저 그리기 연구실 03 · 얼굴 편", author="안상선", year=2026, note="앞 편. 얼굴 기준선과 AI 얼굴 문장. https://adminmrobo.github.io/drawing_lab_03/"),
 dict(id="prev_01", title="구조 먼저 그리기 연구실 01 · 옷장 편", author="안상선", year=2026, note="옷 주름·그림자와 AI·VFX. https://adminmrobo.github.io/structure_first_drawing_lab_01/"),
 dict(id="prev_series", title="구조 먼저 보는 캐릭터 그리기 연구실", author="안상선", year=2026, note="첫 시리즈. 구조·빛·주름 기초와 확산 모델·프롬프트 기초. https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"),
]
FOOT_LINKS = [("index.html", "목차")] + [(P["file"], f"{P['no']}부") for P in PARTS] + [("practice/index.html", "7부 실전 연습장"), ("08_conti_book.html", "8부 콘티 북"), ("practice/template.html", "빈 콘티 양식")]

def footer(pre=""):
    links = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in FOOT_LINKS) + f' · <a href="{REPO}">저장소</a>'
    refs = "".join(f"<tr><td>[{i+1}]</td><td>{E(r['author'])} ({r['year']}). {E(r['title'])}</td><td>{E(r['note'])}</td></tr>" for i, r in enumerate(REFS))
    return f"""<footer><div class="wrap">
<h3>출처·참고</h3>
<div class="tbl"><table><thead><tr><th>#</th><th>자료</th><th>어디에 썼나</th></tr></thead><tbody>{refs}</tbody></table></div>
<h3>예시값·설명용 숫자</h3>
<p>컷 수와 한 컷 길이(3초), 감정 세기(0~10), 썸네일 시간(1분·15분), 샷별 머리 개수, 거리와 화면 크기, 시선 여백 비(2), 휜 정도(10%·20%), 덩어리 무게(몸통 6·머리 1·다리 3), 몸무게 60kg과 물건 무게, 과장 점수, 한 장 맞을 확률(0.8~0.99), 강도(0.35~0.6)와 단계 수, 만드는 순서의 점수, 평가단 점수는 모두 원리를 보이기 위한 예시값입니다. 실제 작품·도구·사람마다 다릅니다.</p>
<p>등장인물은 모두 성인 연구원입니다(하루·시아·모아는 20대, 박사는 30대 성인 남성). 예시 콘티의 인물도 키가 머리 7.5개인 성인 비율로 그립니다. 다른 작품의 캐릭터를 닮은 그림은 만들지 않습니다.</p>
<p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: <a href="{CHARREPO}">fruitfly-lab-expressions</a>.</p>
<p>글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p>
<p>{links}</p>
</div></footer>
<script src="{pre}assets/panels.js"></script>
</body></html>
"""

def face(k, e="e13", pre="", cls=""):
    n = CH[k][0]
    return f'<img src="{pre}assets/chars/{k}_{e}.webp" alt="{E(n)}" width="96" height="96" loading="lazy"{(" class=%s" % cls) if cls else ""}>'

def has_img(key):
    return os.path.exists(os.path.join(ROOT, "assets", "img", key + ".webp"))

def art(key, alt, ar="16/9", cap=None, pre="", cls=""):
    if key in ALT:
        if cap == alt:
            cap = ALT[key]
        alt = ALT[key]
    cap_html = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    if has_img(key):
        return f'<figure class="art {cls}" data-img="{key}"><img src="{pre}assets/img/{key}.webp" alt="{E(alt)}" loading="lazy" decoding="async">{cap_html}</figure>'
    return (f'<figure class="art {cls}" data-img="{key}"><div class="ph-art" style="--ar:{ar}" role="img" aria-label="{E(alt)}">'
            f'<b>그림 준비 중 · {key}</b><span>{E(alt)}</span></div>{cap_html}</figure>')

def head(title, desc, og, path, pre=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/og/{og}"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
<meta name="author" content="안상선">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/lab.css">
</head>
<body data-root="{pre}">
<div id="prog"></div>
"""

def nav(links, pre=""):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="{pre}index.html">구조 먼저 그리기 <i>· 콘티 편</i></a><div class="links">{a}</div></div></nav>\n'

def cover(key, cap, cast, pre=""):
    if has_img(key):
        return f'<div class="cover"><div class="frame" data-img="{key}"><img class="art" src="{pre}assets/img/{key}.webp" alt="{E(cap)}" width="1600" height="900" fetchpriority="high" decoding="async"></div></div>\n'
    # 그림이 오기 전 픽셀 대체 표지: 네모 격자 + 상자·원기둥 마네킹(픽셀 블록) + 픽셀 캐릭터
    cells = []
    for x in range(0, 1600, 40):
        for y in range(0, 900, 40):
            if (x // 40 + y // 40) % 2 == 0:
                cells.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="#f3f6fa"/>')
    px = []
    for i in range(8):
        fx, fy = 900 + (i % 4) * 150, 150 + (i // 4) * 230
        px.append(f'<rect x="{fx}" y="{fy}" width="130" height="80" fill="#ffffff" stroke="#1e2f6e" stroke-width="8"/>')
        for k in range(3):
            px.append(f'<rect x="{fx}" y="{fy + 100 + k * 30}" width="130" height="8" fill="#c3cbd5"/>')
        px.append(f'<rect x="{fx + 55}" y="{fy + 20 - (i * 3 % 12)}" width="20" height="20" fill="#e0337f" opacity=".6"/>')
    bl = "".join(px)
    easel = ""
    imgs = "".join(face(k, e, pre) for k, e in cast)
    return f"""<div class="cover"><div class="frame" data-img="{key}"><svg class="grid" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" shape-rendering="crispEdges">{''.join(cells)}{easel}{bl}</svg>
<span class="cap">{E(cap)}</span><span class="badge">표지 그림 준비 중 · {key}</span><div class="cast" style="image-rendering:pixelated">{imgs}</div></div></div>
"""

def three(a, b, c, abbr):
    dl = "".join(f"<dt>{E(x)}</dt><dd>{E(y)}</dd>" for x, y in abbr)
    return f"""<div class="three"><h2>처음 오신 분께 — 세 줄 요약</h2><ul>
<li><b>무엇을</b>: {E(a)}</li><li><b>왜 알아야 하나</b>: {E(b)}</li><li><b>어디에 쓰나</b>: {E(c)}</li></ul>
<p>그림 실력·코드·수식을 몰라도 됩니다. 실험을 눌러 보며 따라오세요.</p>
<details class="abbr"><summary>낱말·약어 풀이 (펼치기)</summary><dl>{dl}</dl></details></div>\n"""

def talk(lines, pre=""):
    out = []
    for k, e, t in lines:
        side = " r" if k in ("moa", "sia", "haru") else ""
        out.append(f'<div class="line{side}">{face(k, e, pre)}<div class="bub"><b style="color:var(--c-{COLOR[k]})">{E(CH[k][0])}</b>{E(t)}</div></div>')
    return '<div class="talk">' + "".join(out) + "</div>"

def quiz(q, opts, ans, ok, no):
    b = "".join(f'<button type="button">{E(o)}</button>' for o in opts)
    return f'<div class="quiz" data-ans="{ans}"><div class="qq">확인 퀴즈 — {E(q)}</div><div class="opts">{b}</div><div class="fb" aria-live="polite"></div><span class="qok" hidden>{E(ok)}</span><span class="qno" hidden>{E(no)}</span></div>'

def panel(no, i, p):
    return (f'<div class="panel"><div class="ph"><b>실험 {no}-{i}</b><small>{E(p["note"])}</small></div>'
            f'<div id="pp-{p["key"]}" data-panel="{p["key"]}"></div><div class="ctrl">{p["ctrl"]}</div><div class="readout" aria-live="polite"></div></div>')

def mathbox(m):
    tries = "".join(f"<div>{E(t)}</div>" for t in m["tries"])
    pcs = "".join(f"<tr><td class='m'>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in m["pieces"])
    return f"""<div class="box mathbox"><h4>수식이 어려운 조수가 대신 묻습니다</h4>
<div class="q">{face('haru','e04')}<div><b>조수</b> {E(m['ask'])}</div></div>
<div class="easy"><b>말로 하면</b> — {E(m['words'])}</div>
<div class="try"><b>숫자로 한 번 해 보기</b>{tries}</div>
<p><b>학교 수학으로 보면</b> — {E(m['school'])}</p>
<div class="fx">{E(m['formula'])}</div>
<table><thead><tr><th>식 조각</th><th>뜻</th></tr></thead><tbody>{pcs}</tbody></table>
<div class="q">{face('haru','e16')}<div><b>조수</b> {E(m['comment'])}</div></div></div>"""

def step(P, i, s):
    no = P["no"]
    labels = ["무엇이 문제인가", "그냥 하면 막히는 곳", "이렇게 푼다"]
    why = "".join(f"<li><b>{labels[k]}</b> — {E(x)}</li>" for k, x in enumerate(s["why"]))
    whybox = f'<div class="box why"><h4>왜 이렇게 하나</h4><ol>{why}</ol><div class="easy"><b>쉽게 말하면</b> — {E(s["easy"])}</div></div>'
    calm = talk([("doctor", "e08", "여기서 한 번 멈춰도 괜찮아요. 식이 낯설면 건너뛰고 아래 실험부터 눌러 보세요. 숫자는 실험이 대신 계산해 줍니다.")])
    duo = f'<div class="duo">{whybox}{mathbox(s["math"])}</div>{calm}' if s.get("math") else f'<div style="margin:16px 0">{whybox}</div>'
    solve = "".join(f"<p>{E(x)}</p>" for x in s["solve"])
    extra = ""
    img = art(s["img"][0], s["img"][1], s["img"][2], s["img"][1], cls="tall" if s["img"][2] == "2/3" else "") if s.get("img") else ""
    q = s["quiz"]
    return f"""<section class="room" id="{s['id']}"><div class="wrap">
<div class="roomno">{no}부 · {i}단계</div>
<h2>{E(s['title'])}</h2><p class="muted">{E(s['sub'])}</p>
<div class="tags"><span class="tag how">{E(s['how'])}</span><span class="tag day">{E(s['day'])}</span></div>
{duo}
<div class="pair"><div class="box"><h4>일상으로 치면</h4><p>{E(s['daily'])}</p></div><div class="box ml"><h4>그림·영상 현장에서는</h4><p>{E(s['field'])}</p></div></div>
{talk(s['talk'])}
{panel(no, i, s['panel'])}
<div class="solve"><h4>풀이</h4>{solve}</div>
{extra}{img}
<div class="solve"><h4>AI 결과, 그대로 써도 될까?</h4><p>{E(s['ai'][0])}</p><details class="code"><summary>답 보기</summary><p>{E(s['ai'][1])}</p></details></div>
<div class="limit"><b>주의할 점</b> — {E(s['limit'])}</div>
{quiz(q[0], q[1], q[2], q[3], q[4])}
</div></section>
"""

def judge(J):
    rows = ""
    for idx, item in enumerate(J["items"]):
        a, b = J["a"][1][idx], J["b"][1][idx]
        mx = 8 if "8개" in item else 10
        rows += f'<span>{E(item)}</span><span class="bar" title="{J["a"][0]} {a}"><i style="width:{a/mx*100:.0f}%"></i></span><span class="bar" title="{J["b"][0]} {b}"><i style="width:{b/mx*100:.0f}%;background:var(--teal)"></i></span>'
    sa, sb = sum(J["a"][1]), sum(J["b"][1])
    tbl = "".join(f"<tr><td>{E(it)}</td><td>{J['a'][1][k]}</td><td>{J['b'][1][k]}</td></tr>" for k, it in enumerate(J["items"]))
    return f"""<section class="room" id="judge"><div class="wrap"><div class="roomno">평가단 채점</div><h2>{E(J['title'])}</h2>
{talk(J['setup'])}
<div class="judge"><h4>평가단 X1·X2·X3 채점</h4>
<div class="score"><span></span><b>{E(J['a'][0])}</b><b>{E(J['b'][0])}</b>{rows}</div>
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>항목</th><th>{E(J['a'][0])}</th><th>{E(J['b'][0])}</th></tr></thead><tbody>{tbl}<tr><th>합계</th><th>{sa}</th><th>{sb}</th></tr></tbody></table></div>
{talk(J['comments'])}</div>
{talk(J['result'])}
<p class="hint">점수는 이야기 속 예시입니다. 실제 그림을 평가한 값이 아닙니다.</p>
</div></section>
"""

def summary(P):
    rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in P["summary"])
    return f"""<section id="sum"><div class="wrap"><h2>{P['no']}부 정리</h2>
<div class="tbl"><table><thead><tr><th>주제</th><th>한 줄</th><th>작업에서는</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
"""

def outro(P):
    return f"""<section id="outro"><div class="wrap"><h2>다음으로</h2>{talk(P['outro'])}
<div class="next"><a href="{P['prev'][0]}">{E(P['prev'][1])}</a><a href="{P['next'][0]}">{E(P['next'][1])}</a></div></div></section>
"""

def failcard(f):
    note = f'<p class="hint">{E(f["note"])}</p>' if f.get("note") else ""
    return f"""<div class="failcard" id="{f['key'].split('_')[0]}"><h3>{E(f['title'])}</h3><div class="failgrid">
{art(f['key'], f['alt'], f['ar'])}
<div><p><span class="chip">증상</span>{E(f['symptom'])}</p>
{quiz(f['q'], f['opts'], f['ans'], f['ok'], f['no'])}
<p><span class="chip">연결된 원리</span><a href="{f['link'][0]}">{E(f['link'][1])}</a></p>
<div class="promptbox"><b>고치는 프롬프트 조각</b><pre>{E(f['fix'])}</pre></div>{note}</div></div></div>"""

# ---------------- 지식 색인
def kg_block(page, pages):
    nodes = [dict(id="lab:" + i, type=t, label=dict(ko=ko, en=en), page=p, anchor=a, definition=dict(ko=d), source="lab:work/structure_first_drawing_05")
             for i, t, ko, en, p, a, d in KG if p in pages]
    ids = {n["id"] for n in nodes}
    edges = [dict(s="lab:" + s, p=p, o="lab:" + o) for s, p, o in KG_EDGES if "lab:" + s in ids and "lab:" + o in ids]
    raw = dict(version="1.3", page=page, series=SERIES, nodes=nodes, edges=edges)
    ld = {"@context": {"@vocab": "urn:lab:", "skos": "http://www.w3.org/2004/02/skos/core#", "schema": "https://schema.org/"},
          "@graph": [{"@id": "urn:" + n["id"], "@type": n["type"], "skos:prefLabel": [{"@value": n["label"]["ko"], "@language": "ko"}, {"@value": n["label"]["en"], "@language": "en"}],
                      "skos:definition": n["definition"]["ko"], "schema:url": SITE + n["page"] + n["anchor"]} for n in nodes]}
    meta = dict(title=page, series=SERIES, creator=[dict(name="안상선", role="author", affiliation="(주)M-Robo")], date=DATE, version=VER, license="캐릭터·그림 무단 사용 금지")
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section id="kg"><div class="wrap"><h2>지식 색인 — 이 페이지의 낱말 찾기</h2>
<p class="muted">이 페이지에 나온 개념·방법·비유·쓰임을 모았습니다. 검색하고, "설명 보러 가기"로 본문에 돌아갑니다.</p><div id="kg-mount"></div></div></section>
<section id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미 내려받기</h2>
<p class="muted">지식 색인을 출처와 함께 파일로 내려받습니다. 서지 관리는 BibTeX·RIS, 온톨로지 편집은 Turtle, 그래프 도구는 CSV, 여러 페이지 합치기는 kg.json입니다.</p><div id="export-mount"></div></div></section>
<script type="application/json" id="kg-raw">{J(raw)}</script>
<script type="application/ld+json" id="kg-ld">{J(ld)}</script>
<script type="application/json" id="refs-csl">{J(REFS)}</script>
<script type="application/json" id="page-meta">{J(meta)}</script>
"""

REFS_DL = ["haru_anime_base.png", "sia_anime_base.png", "moa_anime_base.png", "haru_sheet.png", "sia_sheet.png", "moa_sheet.png", "doctor_sheet.png", "fruitfly_sprites_6.png", "jupanbot_ref_genspark_v0.png", "pixel_style_ref_prev_cover.png"]
def make_section(P):
    tasks = MAKE.get(P["no"])
    if not tasks:
        return ""
    refs = " · ".join(f'<a href="assets/refs/{f}" download>{f.replace(".png", "")}</a>' for f in REFS_DL)
    out = f"""<section class="room" id="make"><div class="wrap"><div class="roomno">{P['no']}부 · 직접 만들기</div><h2>프롬프트로 직접 만들어 보기</h2>
<div class="box"><p>이 부에서 배운 원리를 그림 생성 AI(Genspark 등)로 직접 확인합니다. <b>A</b>는 이 페이지 그림을 실제로 만든 프롬프트, <b>B</b>는 원리를 하나 빼거나 바꾼 비교용 문장입니다.</p>
<ol style="margin:6px 0 0;padding-left:20px"><li>새 대화를 열고 아래 '첨부'에 적힌 참고 그림을 올립니다.</li><li>A를 붙여 넣어 만들고, 확인표로 결과를 점검합니다.</li><li>같은 대화에 B를 이어 붙여 다시 만들고, A 결과와 나란히 비교합니다. 구도가 흔들리면 'keep the same framing'을 덧붙입니다.</li><li>같은 대화에서 차이가 약하면 새 대화에서 처음부터 만들어 보세요. 결과는 매번 다릅니다.</li></ol>
<p class="hint" style="margin-top:8px">참고 그림 내려받기: {refs}</p></div>"""
    for i, t in enumerate(tasks, 1):
        A = PROMPTS[t["key"]][4]
        att = ATTACH_OF[CONV_OF[t["key"]]]
        ar = "16/9" if "16:9" in A.split("\n")[0] else "2/3"
        alt = PROMPTS[t["img"]][3]
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in t["check"])
        k = t["b_imgs"][0]
        bbox = f'<div class="promptbox"><b>{E(t["b_title"])}</b><pre>{E(t["b_text"])}</pre><button type="button" class="btn copy">복사하기</button></div>'
        bpart = f'<div class="pair">{bbox}<div>{art(k, "비교 결과 — " + t["b_title"], ar, "B 결과")}</div></div>'
        res = f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t["res"])}</p>' if t.get("res") else ""
        tip = f'<p class="hint">{E(t["tip"])}</p>' if t.get("tip") else ""
        out += f"""<div class="failcard" id="make{i}"><h3>실습 {i} · {E(t['title'])}</h3><p>{E(t['goal'])}</p>
<div class="pair"><div class="promptbox"><b>A — 이 페이지 그림을 실제로 만든 프롬프트</b><p class="hint">첨부: {E(att)}</p><pre>{E(A)}</pre><button type="button" class="btn copy">복사하기</button></div>
<div>{art(t['img'], alt, ar, "A 결과 — Genspark로 만든 그림")}</div></div>
{bpart}<h4>결과에서 확인할 것</h4><ol>{chk}</ol>{res}{tip}</div>"""
    return out + "</div></section>"

def res_html(no, did):
    t = DRILL_RES.get(f"{no}-{did}")
    if t and f"{no}-{did}" in RETRY:
        t = t.replace("실제 결과:", "1차 시도 결과:", 1)
    return f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t)}</p>' if t else ""

def retry_html(no, did, shown):
    r = RETRY.get(f"{no}-{did}")
    if not r:
        return ""
    out = f'<div class="box" style="border-left:4px solid var(--blue);margin-top:14px"><h4 style="margin-top:0">다시 시도 — 1차 결과는 위에 그대로 두고, 방법을 바꿔 다시 받습니다</h4><p>{E(r["why"])}</p>'
    for lab, how, pr, key, alt, ar, ok in r["items"]:
        pic = "" if key in shown else f"<div>{art(key, alt, ar, alt)}</div>"
        out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div>{pic}</div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
    rr = RETRY_RES.get(f"{no}-{did}")
    if rr:
        col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[rr[0]]
        out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">다시 시도 결과 · {rr[0]}</b> — {E(rr[1])}</p>'
    r3 = RETRY3.get(f"{no}-{did}")
    if r3:
        out += f'<h4>3차 시도 — 새 대화에서 크게 과장해 다시 받습니다</h4><p>{E(r3["why"])}</p>'
        for lab, how, pr, key, alt, ar, ok in r3["items"]:
            out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
        r3r = RETRY3_RES.get(f"{no}-{did}")
        if r3r:
            col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[r3r[0]]
            out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">3차 시도 결과 · {r3r[0]}</b> — {E(r3r[1])}</p>'
    return out + "</div>"

def drill_section(P):
    ds = DRILL.get(P["no"])
    if not ds:
        return ""
    keys = [p[2] for d in ds for p in d["prompts"]]
    made = "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다. 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다." if all(has_img(k) for k in keys) else "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다(아직 받지 않은 그림은 '그림 준비 중'). 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다."
    out = f"""<section class="room" id="drill"><div class="wrap"><div class="roomno">{P['no']}부 · 연습 과제</div><h2>프롬프트 연습 과제</h2>
<div class="box"><p>이 부의 원리를 내 손으로 프롬프트에 옮겨 보는 과제 두 개입니다. 과제마다 <b>목표 → 순서 → 넣을 프롬프트 → 확인할 것 → 예상 결과 → 자주 생기는 문제</b> 순서로 적었습니다. {made} 결과는 매번 조금씩 다르니, 그림이 똑같지 않아도 '확인할 것'이 맞으면 성공입니다.</p></div>"""
    for i, d in enumerate(ds, 1):
        steps = "".join(f"<li>{E(x)}</li>" for x in d["steps"])
        prs = ""
        for lab, pr, key, alt, ar in d["prompts"]:
            prs += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>"""
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in d["check"])
        tr = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in d["trouble"])
        out += f"""<div class="failcard" id="{d['id']}"><h3>연습 {i} · {E(d['title'])}</h3>
<p><span class="chip">목표</span>{E(d['goal'])}</p><p><span class="chip">왜 이 연습인가</span>{E(d['why'])}</p>
<p class="hint">첨부할 참고 그림: {E(d['attach'])} — 참고 그림은 위 <a href="#make">직접 만들어 보기</a>에서 내려받을 수 있습니다.</p>
<h4>순서</h4><ol>{steps}</ol>
<h4>넣을 프롬프트와 예상 결과</h4>{prs}
<h4>확인할 것</h4><ol>{chk}</ol>
<div class="easy"><b>예상 결과</b> — {E(d['expect'])}</div>{res_html(P['no'], d['id'])}{retry_html(P['no'], d['id'], [p[2] for p in d['prompts']])}
<h4>자주 생기는 문제와 대처</h4><div class="tbl"><table><thead><tr><th>문제</th><th>이렇게 고칩니다</th></tr></thead><tbody>{tr}</tbody></table></div>
<p><span class="chip">더 해 보기</span>{E(d['more'])}</p></div>"""
    return out + "</div></section>"


def sample_details(open_=False):
    return (f'<details class="box" style="margin-top:14px"{" open" if open_ else ""}><summary><b>예시 콘티 「하루, 초파리를 찾아 옥상까지」 펼쳐 보기</b> — 1~5부가 함께 쓰는 여덟 컷</summary>'
            '<div class="panel" style="margin-top:10px"><div class="ph"><b>예시 콘티</b><small>동그라미 머리와 십자선으로 그린 여덟 컷 · 아래 세 줄</small></div>'
            '<div data-panel="p0_sample"></div><div class="ctrl"></div><div class="readout" aria-live="polite"></div></div></details>')

def build_part(P):
    t = f"{SERIES} {P['no']}부 — {P['title']}"
    s = head(t, P["desc"], P["og"], P["file"])
    navl = [(f"#{x['id']}", f"{k+1}단계") for k, x in enumerate(P["steps"])]
    if P.get("fails"): navl += [("#fails", "실패 8종")]
    navl += [("#make", "직접 만들기"), ("#drill", "연습 과제"), ("#judge", "평가"), ("#sum", "정리"), (P["next"][0], "다음 →")]
    s += nav(navl)
    s += cover(P["cover_key"], P["cover_cap"], P["cover_cast"])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">{E(P['kicker'])}</span><h1>{E(P['title'])}</h1><p class="lead">{E(P['lead'])}</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three(*P['three'], ABBR)}</div></section>
<section><div class="wrap"><h2>오늘의 과제</h2>{talk(P['intro'])}{flow_strip(P['no'])}{sample_details(P['no'] == 1)}</div></section>
"""
    for k, st in enumerate(P["steps"]):
        s += step(P, k + 1, st)
    if P.get("extra"):
        s += P["extra"]()
    if P.get("fails"):
        s += '<section class="room" id="fails"><div class="wrap"><div class="roomno">6부 · 2단계</div><h2>콘티·컷 실패 8종 진단</h2><p class="muted">그림마다 증상을 보고 처음 걸리는 점검 항목을 고른 뒤, 연결된 원리와 고치는 문장 조각을 확인합니다. 여러 컷을 이어 봐야 보이는 실패는 한 그림 안에 컷을 나란히 놓았습니다.</p>'
        s += "".join(failcard(f) for f in P["fails"])
        d = P["drift"]
        s += f'<div class="failcard" id="drift"><h3>{E(d["title"])}</h3>' + "".join(f"<p>{E(x)}</p>" for x in d["body"]) + '<p><span class="chip">연결된 원리</span><a href="05_ai_cuts.html#s2">5부 2단계 기준 시트</a> · <a href="02_camera.html#s1">2부 1단계 샷 크기(머리 개수)</a></p></div></div></section>'
    s += make_section(P)
    s += drill_section(P)
    s += judge(P["judge"]) + summary(P) + outro(P)
    s += kg_block(P["file"].replace(".html", ""), [P["file"]])
    s += footer()
    open(os.path.join(ROOT, P["file"]), "w").write(s)

FLOW = [
 (1, "콘티의 뼈대", "그림부터 그리면 이야기가 끝까지 가지 않는다", "네 덩어리·세 줄·감정 곡선·썸네일"),
 (2, "카메라", "뼈대가 서도 카메라가 늘 같으면 여덟 컷이 한 장처럼 보인다", "샷 크기·눈높이 선·앵글·시선 여백"),
 (3, "컷 잇기", "컷 하나하나가 좋아도 이어 보면 방향과 시선이 끊긴다", "가상선·화살표·컷 길이·시선 잇기"),
 (4, "포즈와 연기", "이어진 컷 속 인물이 뻣뻣하면 감정이 전해지지 않는다", "중심축·무게중심·소품 무게·실루엣"),
 (5, "AI로 컷 만들기", "AI는 콘티를 모른다. 문장과 기준으로 알려 줘야 한다", "여덟 조각·기준 시트·밑그림 강도·기준 컷"),
 (6, "실패 사례 실험실", "문장을 써도 컷은 틀릴 수 있다", "진단 순서와 고치는 조각, 나이 쏠림"),
 (7, "실전 연습장", "배운 것을 한 화면에서 함께 다뤄 본다", "콘티 작업대·카메라 촬영장·문장 공방·진단·빈 양식"),
 (8, "콘티 북", "연습을 마치면 내 이야기, 더 긴 이야기를 콘티로 만들고 싶어진다", "8·16·32컷 쪼개기·표 문장·시트·콘티로 완성 컷"),
]
def flow_strip(cur=None, pre=""):
    files = {P["no"]: P["file"] for P in PARTS}
    files[7] = "practice/index.html"
    files[8] = "08_conti_book.html"
    cells = []
    for n, t, _, _ in FLOW:
        mark = ' style="border-color:var(--orange);background:var(--orange-soft)"' if n == cur else ""
        cells.append(f'<a href="{pre}{files[n]}"{mark}><b>{n}부</b>{E(t)}</a>')
    return '<div class="flowgrid" style="grid-template-columns:repeat(auto-fit,minmax(130px,1fr));margin-top:16px">' + "".join(cells) + "</div>"

def build_index():
    t = f"{SERIES} — 콘티 먼저, 컷은 그다음"
    d = "이야기를 여덟 컷으로 나누고, 카메라와 컷 잇기, 인물의 자세를 정한 콘티를 바탕으로 그림 생성 AI에게 컷 그림을 만들게 하는 방법을 실험으로 익힙니다. 콘티·컷 실패 8종 진단과 빈 콘티 양식까지."
    s = head(t, d, "og_index.jpg", "index.html")
    s += nav([("#howto", "읽는 법"), ("#sample", "예시 콘티"), ("#parts", "편 목록"), ("#map", "전체 흐름"), ("#cast", "등장인물"), ("#source", "원리와 출처")])
    s += cover("cover_index", "연구실 화이트보드 · 여덟 장의 콘티와 연구원들", [("fruitfly", "e09"), ("haru", "e01"), ("sia", "e13"), ("moa", "e19"), ("doctor", "e16"), ("jupanbot", "e16")])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">연구실 특별편 · 그리기와 렌더링 · 다섯 번째 편</span>
<h1>구조 먼저 그리기 연구실 05<br>콘티 편 — 콘티 먼저, 컷은 그다음</h1>
<p class="lead">얼굴 편에서 한 사람의 얼굴을 세웠다면, 이번에는 그 사람이 나오는 <b>장면</b>입니다. 이야기를 여덟 컷으로 나누고, 카메라를 놓고, 컷을 잇고, 자세를 정한 <b>콘티</b>를 먼저 짭니다. 그다음 그 콘티를 근거로 <b>그림 생성 AI에게 컷 그림을 한 장씩 만들게</b> 합니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three("이야기를 여덟 컷으로 나눠 컷마다 목적·흐름·감정을 적고, 샷·눈높이·가상선·자세를 정한 콘티를 짠 뒤, 그 콘티를 문장과 기준 그림으로 바꿔 AI로 컷 그림을 만드는 방법을 익힙니다.", "그림부터 그리면 이야기가 끝까지 가지 않고, AI에게 한 줄로 맡기면 여덟 장이 여덟 사람·여덟 방향으로 나옵니다. 콘티가 있어야 컷이 이어집니다.", "짧은 애니메이션·광고·웹툰의 장면 설계, AI로 연속 컷을 만들기 전의 기획, 팀에 장면을 설명하는 회의, 받은 AI 컷의 검수에 씁니다.", ABBR)}</div></section>
<section id="howto"><div class="wrap"><h2>읽는 순서와 시간</h2><div class="box"><ul style="margin:0;padding-left:20px">
<li><b>처음부터 차례로</b>(권장): 부마다 실험을 눌러 보며 25~35분, 전체 4시간 안팎입니다.</li>
<li><b>앞 편을 안 봤다면</b>: 바로 읽어도 됩니다. 낱말은 다시 설명합니다. 캐릭터 얼굴은 <a href="{FACE_SITE}">03 얼굴 편</a>, 옷은 <a href="{CLOTH_SITE}">01 옷장 편</a>, 빛·확산 모델 기초는 <a href="{FIRST_SITE}">구조 먼저 보는 캐릭터 그리기 연구실</a>에 있습니다.</li>
<li><b>콘티만 짜고 싶다면</b>: 1~4부와 <a href="practice/template.html">빈 콘티 양식</a>. <b>AI 컷이 급하다면</b>: 1부 2단계(세 줄) → 5부 → 6부 → 7부, 막히는 낱말은 각 단계의 링크로 되짚어 보세요.</li>
<li><b>내 이야기로 콘티를 만들고 싶다면</b>: 7부 뒤의 <a href=\"08_conti_book.html\">8부 콘티 북</a> — 이야기를 8·16·32컷 콘티 표로 바꾸는 문장, 스케치 시트 프롬프트, 콘티로 완성 컷을 만드는 프롬프트를 생성기로 만들어 줍니다.</li>
<li>각 부 끝의 <b>평가단 채점</b>은 이야기 속 예시 점수입니다. 확인 퀴즈와 실전 연습장 미션으로 스스로 점검하세요.</li></ul></div></div></section>
<section id="sample"><div class="wrap"><h2>예시 콘티 — 「하루, 초파리를 찾아 옥상까지」</h2>
<p class="muted">이 편의 모든 부가 함께 쓰는 여덟 컷입니다. 인물은 동그라미 머리와 십자선(얼굴 방향)만 있는 마네킹으로 그렸고, 컷마다 아래에 목적·흐름·동작·감정·보충 세 줄을 적었습니다. 1부에서는 이 뼈대를, 2부에서는 카메라를, 3부에서는 컷 사이를, 4부에서는 자세를, 5부에서는 이 콘티로 AI 컷을 만드는 법을 다룹니다.</p>
<div class="panel"><div class="ph"><b>예시 콘티</b><small>두 줄 네 장 · 컷 번호는 그림 왼쪽 위</small></div><div data-panel="p0_sample"></div><div class="ctrl"></div><div class="readout" aria-live="polite"></div></div>
<p class="hint">같은 양식을 인쇄해 직접 채워 볼 수 있습니다 → <a href="practice/template.html">빈 콘티 양식</a></p></div></section>
<section id="parts"><div class="wrap"><h2>편 목록</h2>
<p class="muted">모델은 모아(1부)·하루(2부)·시아(3부)·박사(4부)·모두(5부), 콘티 작가는 주판봇과 초파리, 평가단은 X1·X2·X3, 해설은 박사입니다. 부마다 두 작가가 겨루고 평가단이 점수를 매깁니다.</p>
<div class="cards">
<a class="card" href="01_beats.html">{face("moa","e01")}<span class="n">1부 · 모델 모아</span><h3>콘티의 뼈대</h3><p>네 덩어리, 컷마다 세 줄, 감정 곡선, 썸네일 밑그림.</p></a>
<a class="card" href="02_camera.html">{face("haru","e01")}<span class="n">2부 · 모델 하루</span><h3>카메라</h3><p>샷 크기, 눈높이 선과 소실점, 앵글, 시선 여백.</p></a>
<a class="card" href="03_flow.html">{face("sia","e13")}<span class="n">3부 · 모델 시아</span><h3>컷 잇기</h3><p>가상선, 움직임 화살표, 컷 길이와 프레임, 시선 잇기.</p></a>
<a class="card" href="04_pose.html">{face("doctor","e01")}<span class="n">4부 · 모델 박사 · 손님 하루</span><h3>포즈와 연기</h3><p>중심축, 무게중심과 받침, 소품 무게, 실루엣과 과장.</p></a>
<a class="card" href="05_ai_cuts.html">{face("haru","e19")}<span class="n">5부 · 모델 모두</span><h3>AI로 컷 만들기</h3><p>컷 문장 여덟 조각, 기준 시트, 밑그림 강도, 기준 컷 먼저.</p></a>
<a class="card" href="06_failure_lab.html">{face("jupanbot","e20")}<span class="n">6부 · 의도적 실패 8종</span><h3>실패 사례 실험실</h3><p>증상 → 처음 걸린 곳 → 원리 → 고치는 조각. 나이 쏠림 막기.</p></a>
<a class="card" href="practice/index.html">{face("x2","e16")}<span class="n">7부 · 마지막 장</span><h3>실전 연습장</h3><p>콘티 작업대·카메라 촬영장·컷 문장 공방·진단 데스크, 그리고 빈 콘티 양식.</p></a>
<a class="card" href="08_conti_book.html">{face("haru","e19")}<span class="n">8부 · 주인공 하루 · 모두 출연</span><h3>콘티 북</h3><p>내 이야기를 8·16·32컷 콘티로, 콘티를 다시 Genspark에 줘서 완성 컷으로. 예제는 하루의 하루 32컷.</p></a>
</div></div></section>
<section id="map"><div class="wrap"><h2>전체 흐름 — 1부부터 7부까지 이어지는 순서</h2>{flow_strip()}
<div class="tbl" style="margin-top:16px"><table><thead><tr><th>부</th><th>제목</th><th>이 부를 배우는 까닭</th><th>핵심</th></tr></thead><tbody>
{''.join(f"<tr><td>{n}</td><td>{E(t)}</td><td>{E(a)}</td><td>{E(b)}</td></tr>" for n, t, a, b in FLOW)}</tbody></table></div>
<h3 style="margin-top:22px">한눈에 보는 콘티 기준값 (예시값)</h3>
<div class="tbl"><table><thead><tr><th>항목</th><th>기준</th><th>예시 콘티에서는</th><th>배우는 곳</th></tr></thead><tbody>
<tr><td>컷 나누기</td><td>네 덩어리 × 2컷, 전체 길이 = 컷 수 × 한 컷 길이</td><td>8컷 × 3초 ≈ 24초</td><td><a href="01_beats.html#s1">1부 1단계</a></td></tr>
<tr><td>감정 곡선</td><td>절정은 6~7컷, 절정 앞에 한 번 내림</td><td>3·5·6·4·8·7·9·5 (절정 7컷)</td><td><a href="01_beats.html#s3">1부 3단계</a></td></tr>
<tr><td>샷 크기</td><td>화면 높이에 머리 몇 개(원경 20 · 전신 9 · 허리 위 4.5 · 얼굴 1.5)</td><td>1·8컷 원경, 5컷 얼굴</td><td><a href="02_camera.html#s1">2부 1단계</a></td></tr>
<tr><td>원근</td><td>크기 ∝ 1/거리, 눈높이 선은 모두의 같은 높이</td><td>3컷 복도</td><td><a href="02_camera.html#s2">2부 2단계</a></td></tr>
<tr><td>시선 여백</td><td>바라보는 쪽 ÷ 반대쪽 ≈ 2, 1/3 선</td><td>4컷 왼쪽 1/3에서 오른쪽을 봄</td><td><a href="02_camera.html#s4">2부 4단계</a></td></tr>
<tr><td>방향</td><td>가상선 한쪽, 넘을 땐 정면·뒷모습 컷</td><td>2컷 오른쪽 → 3컷 뒷모습</td><td><a href="03_flow.html#s1">3부 1단계</a></td></tr>
<tr><td>컷 길이</td><td>프레임 = 초 × 24, 감정 컷은 길게</td><td>5컷 3초 = 72프레임</td><td><a href="03_flow.html#s3">3부 3단계</a></td></tr>
<tr><td>자세</td><td>휜 정도 0% 서기 · 20% 힘쓰기, 무게중심은 받침 안</td><td>7컷 C자로 문 밀기</td><td><a href="04_pose.html#s1">4부 1단계</a></td></tr>
<tr><td>AI 컷</td><td>여덟 조각 + 기준 시트, 강도 0.35~0.6, 기준 컷 먼저</td><td>5컷을 기준 컷으로</td><td><a href="05_ai_cuts.html#s1">5부</a></td></tr>
</tbody></table></div>
<p class="hint">이 편은 짧은 한 장면(여덟 컷)의 콘티가 중심입니다. 대사·효과음·음악을 적는 법, 여러 장면을 잇는 구성, 카메라 렌즈의 자세한 원리는 깊게 다루지 않습니다.</p>
<p class="muted" style="margin-top:12px">같은 시리즈: <a href="{FACE_SITE}">03 얼굴 편(얼굴 기준선·AI 얼굴 문장)</a> · <a href="{CLOTH_SITE}">01 옷장 편(옷 주름·그림자)</a> · <a href="{FIRST_SITE}">구조 먼저 보는 캐릭터 그리기 연구실(구조·빛·확산 모델)</a> · <a href="{RENDER}">AI 렌더링 연구실</a></p></div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2><div class="cast-grid">{''.join(f'<div class="who">{face(k, "e01" if k in ("haru","sia","moa") else "e13")}<b>{E(CH[k][0])}</b><span>{E(CH[k][1])}</span></div>' for k in ["doctor","haru","sia","moa","jupanbot","fruitfly","x1","x2","x3"])}</div>
<p class="hint" style="margin-top:10px">하루·시아·모아는 20대 성인 연구원, 박사는 30대 성인 남성입니다. 콘티의 마네킹 인물도 모두 성인 비율로 그립니다.</p></div></section>
<section id="source"><div class="wrap"><h2>원리와 출처</h2>
<p>콘티를 짜는 원리(이야기를 컷으로 나누기, 컷마다 목적·흐름·감정 적기, 샷 크기와 앵글, 가상선과 시선 잇기, 컷 길이)는 영상·애니메이션 연출에서 널리 쓰는 원리이며, Katz(1991), Bordwell·Thompson·Smith(2019)를 참고해 쉽게 풀었습니다. 자세의 중심축·실루엣·과장은 Thomas·Johnston(1981), 눈높이 선과 소실점은 Loomis(1951)를 바탕으로 했습니다.</p>
<p>사용자가 제공한 참고 이미지 다섯 장(흑백 인쇄용 8컷 그림 콘티 템플릿, 원근과 인물 크기 도해, 어린이·성인 얼굴 비교, 손에 든 물건과 자세의 중심축 도해, 캐릭터 일관성 기준 시트 예시)에서는 원리만 가져왔습니다. 그림·문장·도식·구성은 옮기지 않았고, 연구실 캐릭터와 직접 움직이는 실험으로 새로 구성했습니다. 어린이 얼굴 예시는 '어려 보이는 쏠림'을 막는 데만 썼고, 무기를 든 자세 예시는 상자·문·우산으로 바꿨습니다.</p>
<p>밑그림 강도와 부분 수정, 캐릭터 일관성은 확산 모델 연구(Meng 외 2022, Rombach 외 2022, Lugmayr 외 2022, Ruiz 외 2023)를 바탕으로 풀었습니다. 1~7부 그림(표지 8장은 픽셀풍, 본문·실패·연습 그림은 애니풍과 연필 콘티)은 Genspark로 만들었습니다(2026-11-26). 요청과 다르게 나온 곳은 그림 설명과 '실제 결과'에 있는 그대로 적었고, 요청과 다른 인물·옷차림이 나온 비교 그림 1장은 싣지 않았습니다. 8부 콘티 북 그림 22장과, 처음에 요청과 다르게 나와 다시 만든 그림 10장도 반영했습니다(2026-11-26). 요청문은 저장소 <code>docs/image_requests*/</code>에 있습니다. 실험 패널과 예시 콘티 그림은 모두 페이지 안에서 직접 계산해 그립니다.</p></div></section>
"""
    s += kg_block("index", [P["file"] for P in PARTS] + ["practice/index.html", "08_conti_book.html", "practice/template.html"])
    s += footer()
    open(os.path.join(ROOT, "index.html"), "w").write(s)

def build_practice():
    pre = "../"
    t = f"{SERIES} 7부 — 실전 연습장"
    d = "콘티 작업대(덩어리·절정·길이), 카메라 촬영장(샷·앵글·자리), 컷 문장 공방(AI 문장), 진단 데스크(실패 맞히기) 네 곳을 직접 운영하며 1~6부를 함께 연습합니다. 인쇄용 빈 콘티 양식도 있습니다."
    s = head(t, d, "og_07.jpg", "practice/index.html", pre)
    s += nav([("#bench", "콘티 작업대"), ("#camera", "카메라 촬영장"), ("#workshop", "공방"), ("#desk", "진단 데스크"), ("#wrap", "마무리"), ("template.html", "빈 양식"), ("../08_conti_book.html", "8부 →")], pre)
    s += cover("cover_07", "연구실 조종 책상 · 실전 연습장", [("haru", "e19"), ("doctor", "e16"), ("fruitfly", "e09"), ("jupanbot", "e16")], pre)
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">7부 · 마지막 장</span><h1>실전 연습장</h1>
<p class="lead">네 곳의 작업대를 직접 운영합니다. <span style="color:var(--green)">초록 조작판</span>은 주어진 환경, <span style="color:var(--blue)">파랑 조작판</span>은 내 결정입니다. 미션은 직접 조작해야 판정됩니다. 다 하고 나면 <a href="template.html">빈 콘티 양식</a>에 내 콘티를 짜 보세요.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section id="practice"><div class="wrap">
<div class="tabs" role="tablist"><button type="button" data-t="bench">콘티 작업대</button><button type="button" data-t="camera">카메라 촬영장</button><button type="button" data-t="workshop">컷 문장 공방</button><button type="button" data-t="desk">진단 데스크</button></div>
"""
    def sc(id_, title, situ, env, me, missions, back, extra_g1=""):
        ms = "".join(f"<li>{E(m)}</li>" for m in missions)
        bk = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in back)
        return f"""<div class="scene" id="{id_}"><h2>{E(title)}</h2><div class="box"><b>상황</b> — {E(situ)}</div>
<div class="panel"><div class="ph"><b>조작판</b><small>초록 = 환경 · 파랑 = 내 결정</small></div>
<div class="ctrl ctl-env">{env}</div><div class="ctrl ctl-me">{me}</div>
<div class="board" aria-live="polite"></div>
<div class="pair"><div class="g1">{extra_g1}</div><div class="g2"></div></div>
<div class="talk"></div>
<h4>미션</h4><ol class="missions">{ms}</ol></div>
<p class="muted">배운 곳 다시 보기: {bk}</p></div>
"""
    s += sc("bench", "콘티 작업대 — 여덟 컷의 뼈대 세우기", "장면 길이(목표)가 주어집니다. 네 덩어리에 컷을 나누고, 절정 컷과 첫 컷의 샷, 한 컷 길이를 정해 목표에 맞춥니다.",
            '<label>목표 장면 길이 <select name="len"><option value="24" selected>24초</option><option value="16">16초</option><option value="32">32초</option></select></label>',
            '<label>시작 <input type="range" name="a" min="0" max="5" step="1" value="3"></label><label>전개 <input type="range" name="b" min="0" max="5" step="1" value="3"></label><label>전환 <input type="range" name="c" min="0" max="5" step="1" value="1"></label><label>끝 <input type="range" name="d" min="0" max="5" step="1" value="0"></label>'
            '<label>절정 컷 <input type="range" name="peak" min="1" max="8" step="1" value="3"></label><label>한 컷 길이(초) <input type="range" name="sec" min="1" max="5" step="0.5" value="2"></label><label>첫 컷 샷 <select name="first"><option value="cu" selected>얼굴</option><option value="fs">전신</option><option value="ls">원경</option></select></label>',
            ["네 덩어리 모두 1컷 이상, 합계 여덟 컷 맞추기", "합계 여덟 컷을 지킨 채 절정을 6~7컷에 두기", "목표 장면 길이에 맞추고 첫 컷을 원경(장소 소개)으로"],
            [("01_beats.html#s1", "1부 1단계 네 덩어리"), ("01_beats.html#s3", "1부 3단계 감정 곡선"), ("02_camera.html#s1", "2부 1단계 샷 크기")])
    s += sc("camera", "카메라 촬영장 — 컷의 목적에 맞는 카메라", "찍을 컷(목표)이 주어집니다. 샷 크기·앵글·인물의 자리·바라보는 쪽을 골라 컷의 목적에 맞춥니다.",
            '<label>찍을 컷 <select name="target"><option value="c4" selected>4컷 창밖 보기</option><option value="c1">1컷 장소 소개</option><option value="c5">5컷 깨달음</option><option value="c6">6컷 결의</option></select></label>',
            '<label>샷 크기 <select name="shot"><option value="0">원경</option><option value="1" selected>전신</option><option value="2">무릎 위</option><option value="3">허리 위</option><option value="4">가슴 위</option><option value="5">얼굴</option></select></label><label>앵글 <select name="cam"><option value="eye" selected>눈높이</option><option value="low">앙각</option><option value="high">부감</option></select></label><label>바라보는 쪽 <select name="face"><option value="r">오른쪽</option><option value="l" selected>왼쪽</option></select></label><label>인물 자리(%) <input type="range" name="x" min="10" max="90" step="1" value="50"></label>',
            ["4컷(창밖 보기) 맞추기 — 허리 위, 왼쪽 1/3에서 오른쪽을 봄", "6컷(결의) 맞추기 — 전신, 앙각", "찍을 컷 네 가지를 모두 한 번씩 맞추기"],
            [("02_camera.html#s1", "2부 1단계 샷 크기"), ("02_camera.html#s3", "2부 3단계 앵글"), ("02_camera.html#s4", "2부 4단계 시선 여백")])
    s += sc("workshop", "컷 문장 공방 — 콘티 한 컷을 AI 문장으로", "요청 상황에 맞춰 컷 문장을 조립합니다. 여덟 조각을 채우고, 상황에 꼭 필요한 조각을 넣습니다.",
            '<label>요청 상황 <select name="job"><option value="key">기준 컷(인물·감정·샷 중요)</option><option value="next">다음 컷 잇기(방향·동작·빛 중요)</option><option value="wide">장소 소개(배경·원경 중요)</option></select></label>',
            '<div class="ow" style="width:100%"></div>',
            ["점검표 8 / 8을 충돌 경고 없이 채우기", "5컷 문장 만들기 — 얼굴 샷, 눈높이, 하루(고정값), 오른쪽 위, 깨달음", "6컷 문장 만들기 — 전신, 앙각, 하루(고정값), 계단 오르기, 오른쪽 위, 결의"],
            [("05_ai_cuts.html#s1", "5부 1단계 여덟 조각"), ("05_ai_cuts.html#s2", "5부 2단계 기준 시트"), ("03_flow.html#s1", "3부 1단계 가상선")],
            '<div class="promptbox"><b>조립된 컷 문장</b><pre aria-live="polite"></pre><button type="button" class="btn copy">복사하기</button></div>')
    s += sc("desk", "진단 데스크 — 원인 맞히기", "콘티·컷 실패의 증상이 하나씩 들어옵니다. 원인을 고르세요. 순서: 이야기 → 카메라 → 흐름 → 포즈 → 고정값.",
            '<span class="hint">환경: 증상은 무작위로 들어옵니다.</span>',
            '<div style="width:100%"><p class="sym" style="font-weight:600"></p><div class="opts deskopts"></div></div>',
            ["3개 연속 정답", "8종 원인을 모두 한 번 이상 맞히기", "틀리지 않고 5개 맞히기"],
            [("06_failure_lab.html#s1", "6부 진단 순서"), ("06_failure_lab.html#fails", "6부 실패 8종")])
    s += f"""</div></section>
<section id="wrap"><div class="wrap"><h2>마무리 — 네 작업대를 하나로 묶으면</h2>
<div class="box"><p>콘티 작업대에서 세운 뼈대(덩어리·절정·첫 컷)는 카메라 촬영장의 '컷의 목적'이 되고, 촬영장에서 고른 샷·앵글·자리는 공방의 '샷·앵글·방향' 조각이 됩니다. 진단 데스크에서 틀린 원인은 대부분 앞의 세 곳 중 하나가 빠진 경우입니다. AI 컷 그림은 결국 <b>콘티 한 컷의 결정을 문장과 기준 그림으로 옮기는 일</b>입니다.</p>
<p><b>실제 그림으로 이어 가기</b> — ① <a href="template.html">빈 콘티 양식</a>에 내 이야기 여덟 컷을 짭니다. ② 컷 문장 공방에서 컷마다 문장을 조립해 그림 생성 AI에 넣습니다. ③ 기준 컷을 먼저 확정하고 같은 대화에서 이어 만듭니다. ④ 결과는 각 부의 '프롬프트로 직접 만들어 보기' 확인표로 점검합니다: <a href="{pre}01_beats.html#make">1부</a> · <a href="{pre}02_camera.html#make">2부</a> · <a href="{pre}03_flow.html#make">3부</a> · <a href="{pre}04_pose.html#make">4부</a> · <a href="{pre}05_ai_cuts.html#make">5부</a> · <a href="{pre}06_failure_lab.html#make">6부</a></p>
<p class="hint">주의할 점: 이 연습장의 기준값(두 컷씩 나누기, 절정 6~7컷, 샷별 머리 개수, 판정 범위)은 원리를 보이기 위한 예시입니다. 실제 작품과 도구마다 다릅니다.</p></div>
<div class="next"><a href="{pre}06_failure_lab.html">← 6부 실패 사례 실험실</a><a href="template.html">빈 콘티 양식</a><a href="{pre}08_conti_book.html">8부 콘티 북 →</a></div></div></section>
"""
    s += kg_block("practice_index", ["practice/index.html"])
    s += footer(pre)
    open(os.path.join(ROOT, "practice", "index.html"), "w").write(s)

def build_template():
    pre = "../"
    t = f"{SERIES} — 빈 콘티 양식(인쇄용)"
    d = "여덟 컷, 컷마다 목적·흐름·동작·감정·보충 세 줄과 샷·길이를 적는 인쇄용 빈 콘티 양식. 예시 콘티로 채워 볼 수도 있습니다."
    s = head(t, d, "og_07.jpg", "practice/template.html", pre)
    s += nav([("index.html", "실전 연습장"), (pre + "01_beats.html#s2", "1부 세 줄")], pre)
    s += f"""<header class="hero noprint"><div class="wrap"><span class="kicker">7부 · 부록</span><h1>빈 콘티 양식</h1>
<p class="lead">두 줄 네 장, 여덟 컷짜리 양식입니다. 그림 자리에는 동그라미 머리와 십자선으로 썸네일을 그리고(1부 4단계), 아래 세 줄과 샷·길이를 적습니다. 가로 A4로 인쇄됩니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section id="tpl"><div class="wrap">
<div class="tbtns"><button type="button" class="btn on" data-mode="blank">빈 양식</button><button type="button" class="btn" data-mode="sample">예시 콘티로 채우기</button><button type="button" class="btn" data-print>인쇄하기</button></div>
<div class="thead"><div><b>제목</b><span data-sample="하루, 초파리를 찾아 옥상까지"></span></div><div><b>장면 길이</b><span data-sample="약 24초 · 8컷"></span></div><div><b>작성</b><span data-sample="초파리 연구원"></span></div><div><b>날짜</b><span data-sample="{DATE}"></span></div></div>
<div class="tsheet"></div>
<p class="hint noprint" style="margin-top:12px">적는 요령 — 목적: 이 컷이 이야기에서 맡은 일 · 흐름·동작: 인물과 카메라의 움직임(화면 기준 방향) · 감정·보충: 인물의 마음, 빛·소리 · 샷·길이: 원경/전신/허리 위/얼굴, 초. 다 적었으면 <a href="index.html#workshop">컷 문장 공방</a>에서 컷마다 AI 문장으로 옮겨 보세요.</p>
</div></section>
"""
    s += f"""<footer class="noprint"><div class="wrap"><p>글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER} · 양식은 자유롭게 인쇄해 쓰셔도 됩니다. 캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.</p>
<p>{" · ".join(f'<a href="{pre}{h}">{E(tt)}</a>' for h, tt in FOOT_LINKS)} · <a href="{REPO}">저장소</a></p></div></footer>
<script src="{pre}assets/panels.js"></script>
</body></html>
"""
    open(os.path.join(ROOT, "practice", "template.html"), "w").write(s)

def book_data():
    s32 = [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], "·".join(CODE_KO[c] for c in r[8])] for r in S32]
    sheet = {f"{n}_{k}": sheet_prompt(n, k) for n in (8, 16, 32) for k in range(1, n // 8 + 1)}
    cut = {f"{c}_{m}": cut_prompt(c, "crop" if m == "crop" else "sheet") for c in range(1, 33) for m in ("crop", "sheet")}
    att = {f"{c}_{m}": attach_for(c, "crop" if m == "crop" else "sheet") for c in range(1, 33) for m in ("crop", "sheet")}
    return dict(s32=s32, s16=[list(r) for r in S16], s8=[list(r) for r in S8], beats=BEATS, story=STORY_LINE, sheet=sheet, cut=cut, attach=att, done=DONE, key=KEY)

def book_example():
    tot = sum(r[7] for r in S32)
    rows = ""
    for r in S32:
        k = (r[0] - 1) // 8
        star = " ★" if r[0] in DONE else ""
        rows += f'<tr><td>{r[0]}{star}</td><td>{BEATS[k]}</td><td>{E(r[1])}</td><td>{E(r[2])}</td><td>{E(r[3])}</td><td>{r[4]}</td><td>{E(r[5])}</td><td>{E(r[6])}</td><td>{r[7]}</td><td>{"·".join(CODE_KO[c] for c in r[8])}</td></tr>'
    sheets = "".join(f'<div>{art(f"sheet_32_{k}", BOOK_PROMPTS[f"sheet_32_{k}"][3], "16/9")}</div>' for k in range(1, 5))
    dones = "".join(f'<div>{art(f"done_c{c:02d}", BOOK_PROMPTS[f"done_c{c:02d}"][3], "16/9")}</div>' for c in [KEY] + [c for c in DONE if c != KEY])
    return f"""<section class="room" id="example"><div class="wrap"><div class="roomno">8부 · 예제</div><h2>하루의 하루 — 32컷 콘티 북</h2>
<p class="muted">이야기(한 문장): {E(STORY_LINE)}</p>
<p>생성기(3단계)로 만든 표를 1부 3단계(감정 곡선)와 2부 1단계(샷)로 다듬은 결과입니다. 컷 길이 합계 <b>{f"{tot:g}"}초</b>, 절정은 31컷(감정 9), ★는 완성 컷으로 만든 여덟 컷입니다.</p>
<details class="box"><summary><b>32컷 콘티 표 펼쳐 보기</b> — 목적 · 흐름·동작 · 감정·보충 · 감정 세기 · 샷 · 앵글 · 길이 · 등장</summary>
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>컷</th><th>덩어리</th><th>목적</th><th>흐름·동작</th><th>감정·보충</th><th>세기</th><th>샷</th><th>앵글</th><th>초</th><th>등장</th></tr></thead><tbody>{rows}</tbody></table></div></details>
<h3 style="margin-top:20px">스케치 시트 네 장 (4단계 프롬프트로 만든 그림)</h3>
<div class="pair">{sheets}</div>
<h3 style="margin-top:20px">완성 컷 여덟 장 (5단계 — 기준 컷 31을 먼저)</h3>
<div class="pair">{dones}</div>
<h3 style="margin-top:20px">비교 — 시트를 통째로 첨부하면</h3>
<div class="pair"><div>{art("ab_sheet18", BOOK_PROMPTS["ab_sheet18"][3], "16/9")}</div><div>{art("done_c18", BOOK_PROMPTS["done_c18"][3], "16/9")}</div></div>
<p class="hint">왼쪽은 시트 3 전체를 첨부한 결과, 오른쪽은 18컷만 잘라 첨부한 결과입니다. 실제 결과: 예상과 달리 두 장이 거의 같았습니다. 통째로 첨부해도 18컷 하나만 채색 그림으로 나왔고 연필선도 남지 않았습니다. 이번에는 통째로의 위험이 드러나지 않았지만, 컷을 잘못 고르는 일을 막으려면 잘라서 첨부하는 편이 여전히 확실합니다. 프롬프트는 5단계 생성기에서 컷 18과 첨부 방법을 바꿔 가며 볼 수 있습니다. 요청 꾸러미: <code>docs/image_requests_book/</code></p>
</div></section>
"""

if __name__ == "__main__":
    JS = ["js_base.js", "js_practice_util.js", "js_conti.js", "js_book.js", "js_tail.js"]
    os.makedirs(os.path.join(ROOT, "practice"), exist_ok=True)
    parts = [open(os.path.join(ROOT, "build", f)).read() for f in JS]
    parts.insert(3, "var BOOK=" + json.dumps(book_data(), ensure_ascii=False) + ";\n")
    open(os.path.join(ROOT, "assets", "panels.js"), "w").write("".join(parts))
    build_index()
    for P in PARTS:
        build_part(P)
    build_practice()
    build_template()
    P8["extra"] = book_example
    build_part(P8)
    print("built", len(PARTS) + 4, "pages")
