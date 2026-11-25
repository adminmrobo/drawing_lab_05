# -*- coding: utf-8 -*-
"""부마다 '프롬프트로 직접 만들어 보기' 실습. A 프롬프트는 make_requests.py(이 페이지 그림을 만드는 프롬프트)에서 가져온다.
res: 실제 결과 기록. 그림을 만들기 전에는 '아직 만들지 않음'을 그대로 적고, 그림이 들어오면 A·B를 나란히 보고 실제로 달라진 점을 적는다."""

PENDING = "실제 결과: 아직 그림을 만들지 않았습니다. A·B 그림이 들어오면 나란히 놓고 실제로 무엇이 달라졌는지(또는 달라지지 않았는지) 이 자리에 적습니다."

def T(key, title, goal, b_title, b_text, check, tip=None, b_key=None, res=PENDING):
    return dict(key=key, title=title, goal=goal, b_title=b_title, b_text=b_text, check=check, tip=tip, img=key, b_imgs=[b_key or key + "_b"], res=res)

MAKE = {
1: [
 T("b1_haru_8cuts", "여덟 컷 썸네일을 한 장에", "이야기의 네 덩어리를 컷 번호와 함께 문장으로 넣어, 여덟 컷 연필 콘티를 한 장으로 받습니다.",
   "B — 원리 빼기: 목적이 같은 여덟 컷", "Same image, keep the same layout. Change only: make all eight panels show the same thing — the mannequin standing in front of the building at the same size — so the story does not move forward. Still no text.",
   [("1·8컷은 멀리, 5컷은 얼굴 가까이 — 컷마다 샷이 다른가", "02_camera.html#s1"), ("2컷은 오른쪽, 3컷은 안쪽 — 이야기가 앞으로 가는가", "#s1"), ("B 결과를 보고 '어느 컷을 빼도 모른다'는 느낌이 드는지 비교", "06_failure_lab.html#f1")],
   tip="그림 속에 컷 번호·글자가 생기면 'no text, no panel numbers'를 덧붙여 다시 만듭니다. 세 줄은 그림 밖, 문장으로 적습니다(2단계).", res="실제 결과: A는 요청대로 연필 마네킹 여덟 컷이 나와 1·8컷은 넓게, 5컷은 머리 가까이, 2·6·7컷은 움직임이 보입니다. B는 '같은 레이아웃'이라고 했는데도 채색된 하루가 건물 앞에 같은 자세로 선 그림 여덟 장으로 바뀌었습니다. 그림체는 달라졌지만 '목적이 같은 여덟 컷'이 얼마나 지루한지는 오히려 더 분명하게 보입니다."),
 T("b1_moa_emotion", "감정 세 가지를 같은 크기로", "같은 샷 크기에서 감정 낱말만 바꿔, 감정 줄이 그림을 어떻게 바꾸는지 봅니다.",
   "B — 원리 빼기: 감정 낱말 지우기", "Same image, keep the same framing. Change only: remove all emotion words — give all three panels the same pleasant neutral smile. Still no text.",
   [("왼쪽·가운데·오른쪽 표정이 걱정·깨달음·결심으로 구별되나", "#s3"), ("가운데 얼굴이 오른쪽 위를 올려다보나(시선 잇기)", "03_flow.html#s4"), ("B 결과에서 세 컷이 한 컷처럼 보이는지 비교", "#s2")], res="실제 결과: A는 걱정·놀람·결심이 잘 구별됩니다. 다만 가운데 놀란 얼굴의 시선이 요청한 오른쪽 위가 아니라 왼쪽 위입니다. B는 표정만 바꾸라고 했지만 하루·모아·안경 쓴 남성(박사 아님)의 전신 세 장이 나와 비교가 되지 않았습니다. 같은 대화에서 차이가 엉뚱하게 나오면 새 대화에서 B 문장을 넣은 전체 프롬프트로 처음부터 만드세요."),
],
2: [
 T("b2_haru_shots", "샷 크기 다섯 가지", "같은 하루를 원경부터 얼굴까지 다섯 샷으로 받아, 화면에 들어가는 머리 수를 직접 세어 봅니다.",
   "B — 원리 빼기: 모두 전신", "Same image, keep the same layout. Change only: show Haru as a full body shot, head to toe, in all five panels. Still no text.",
   [("원경 → 얼굴로 갈수록 화면에 들어가는 머리 수가 줄어드나 — 받은 그림 위에 머리 높이를 재어 세기", "#s1"), ("다섯 컷 모두 같은 하루(번 2개, 남색 줄)인가", "05_ai_cuts.html#s2"), ("B 결과에서 다섯 장이 한 장처럼 보이는지 비교", None)], res="실제 결과: A는 원경 → 얼굴로 다섯 샷이 고르게 가까워졌습니다. B는 '모두 전신'을 요청했지만 하루가 아니라 시아의 설정 시트가 나왔습니다. 같은 대화의 앞 그림(참고 그림)을 따라간 것으로 보입니다."),
 T("b2_eyelevel", "복도의 다섯 사람", "눈높이 선이 다섯 사람의 눈을 지나는지, 거리에 따라 크기가 줄어드는지 선을 그어 확인합니다.",
   "B — 원리 빼기: 모두 같은 크기", "Same image, keep the same framing. Change only: draw all five people at exactly the same size regardless of their distance. Still no text.",
   [("가까운 사람과 먼 사람의 머리 끝을 이은 선이 소실점으로 모이나", "#s2"), ("눈높이 선(가로선) 하나가 다섯 사람의 눈을 지나나", "#s2"), ("B 결과에서 먼 사람이 거인처럼 보이는지 비교(6부 f3)", "06_failure_lab.html#f3")], res="실제 결과: A는 멀수록 작아지지만 가까운 하루의 눈이 다른 사람들보다 높아 눈높이 선이 다섯 사람의 눈을 지나지 않습니다 — 원근 문장을 넣어도 틀릴 수 있다는 좋은 검사 사례입니다. B는 받았지만 요청에 없던 인물들이 나오고 그중 한 명의 옷차림이 이 시리즈의 규칙과 맞지 않아 싣지 않았습니다."),
],
3: [
 T("b3_direction", "방향을 잇는 두 컷", "2컷(오른쪽으로 걷기)과 3컷(복도로 들어가는 뒷모습)이 한 방향으로 이어지는지 봅니다.",
   "B — 원리 빼기: 가상선 넘기", "Same image, keep the same framing. Change only: in the right panel, show Sia from the side walking toward the LEFT side of the frame instead of from behind. Still no text.",
   [("왼쪽 컷에서 시아가 화면 오른쪽으로 걷나", "#s1"), ("오른쪽 컷이 뒷모습(선 위에서 찍은 다리 컷)인가", "#s1"), ("B 결과에서 시아가 되돌아가는 것처럼 보이는지 비교(6부 f2)", "06_failure_lab.html#f2")], res="실제 결과: A는 오른쪽으로 걷는 옆모습 → 복도 뒷모습으로 잘 이어집니다. B는 방향 비교 대신 하루와 시아의 설정 시트 그림이 나와 실패했습니다. 가상선 넘기 비교는 6부 f2 그림으로 보세요."),
 T("b3_eyeline", "시선을 잇는 두 컷", "앞 컷의 시선 방향과 다음 컷 대상의 자리가 같은 쪽인지 봅니다.",
   "B — 원리 빼기: 대상을 반대쪽에", "Same image, keep the same framing. Change only: in the right panel, move the glinting wings to the LOWER LEFT corner of the frame. Still no text.",
   [("왼쪽 컷의 하루가 오른쪽 위를 보고, 오른쪽에 여백이 있나", "02_camera.html#s4"), ("오른쪽 컷의 날개가 오른쪽 위에 있나", "#s4"), ("B 결과에서 '하루가 이것을 보았다'가 약해지는지 비교", None)], res="실제 결과: A는 하루의 오른쪽 위 시선과 하늘 오른쪽 위의 반짝임이 맞습니다. B는 날개가 왼쪽 아래로 가긴 했지만 하늘 대신 시아 전신 두 장과 큰 흰 날개가 나와, 시선 비교로는 쓰기 어렵습니다."),
],
4: [
 T("b4_doctor_axis", "중심축 세 가지", "곧게 선 자세·C자·S자를 나란히 받아, 받은 그림 위에 중심축을 직접 그어 봅니다.",
   "B — 원리 빼기: 가운데 자세를 곧게", "Same image, keep the same framing. Change only: in the middle pose, keep the Professor's body perfectly upright with only his arms reaching to the door. Still no text.",
   [("가운데 자세의 머리~받침 발이 C자로 휘었나 — 그림 위에 선을 그어 확인", "#s1"), ("오른쪽 자세가 위아래 반대로 비틀린 S자인가", "#s1"), ("B 결과에서 문이 가벼워 보이는지 비교(6부 f5)", "06_failure_lab.html#f5")], res="실제 결과: A의 가운데 자세는 몸 전체가 문 쪽으로 기운 곧은 사선이고, 오른쪽은 비튼 걷기 자세입니다. B는 가운데만 곧게 하라고 했지만 꼬마 체형 박사의 픽셀 스프라이트가 나와 실패했습니다. 곧은 자세의 실패 예는 6부 f5 그림이 대신 보여 줍니다."),
 T("b4_haru_prop", "가벼운 우산과 무거운 상자", "들고 있는 물건의 무게가 몸의 기울기로 보이는지 봅니다.",
   "B — 원리 빼기: 무거운 상자를 곧게", "Same image, keep the same framing. Change only: in the right panel, keep Haru standing perfectly straight while carrying the heavy box. Still no text.",
   [("오른쪽 하루가 상자 반대쪽(뒤)으로 기울었나", "#s3"), ("무릎이 살짝 굽고 두 발이 벌어졌나", "#s2"), ("B 결과에서 상자가 가벼워 보이는지 비교", None)], res="실제 결과: A의 상자 그림은 무릎은 굽혔지만 상체가 뒤로 기울지 않고 상자 위로 숙였습니다. 연습 과제 4-d2의 상자 그림이 오히려 뒤로 기운 모습을 더 잘 보여 줍니다. B는 곧게 선 하루가 나왔지만 요청에 없던 박사가 함께 들어갔습니다."),
],
5: [
 T("b5_sketch_to_cut", "썸네일에서 완성 컷으로", "왼쪽 썸네일과 오른쪽 완성 컷의 인물 자리·크기·자세가 같은지 봅니다. 실제로는 썸네일을 첨부하고 강도를 골라 만드는 과정을 한 장으로 보여 주는 그림입니다.",
   "B — 원리 빼기: 구도를 무시한 완성", "Same image. Change only: in the right panel, ignore the sketch composition — put Haru in the center of the frame facing the viewer, smiling, with the door behind her. Still no text.",
   [("왼쪽과 오른쪽의 인물 자리·크기·기울기가 같은가", "#s3"), ("오른쪽 컷에 연필선·글자가 남지 않았나", "#s3"), ("B 결과에서 7컷의 '각오'가 사라지는지 비교", "01_beats.html#s3")],
   tip="직접 해 볼 때는 썸네일을 그려(또는 이 그림의 왼쪽을 잘라) 첨부하고, 도구의 참고 이미지 강도를 0.35~0.6에서 시작하세요.", res="실제 결과: A는 썸네일의 밀기 자세와 문 자리가 완성 컷에 그대로 남았습니다. B는 구도를 무시하라는 문장대로 정면에서 웃는 하루가 되어 7컷의 '각오'가 사라졌습니다. 이 부의 A·B 중 의도가 가장 분명하게 드러난 짝입니다."),
 T("b5_haru_anchor", "기준 시트와 세 컷", "기준 시트를 옆에 둔 세 컷에서 고정값이 모두 지켜지는지 봅니다.",
   "B — 원리 빼기: 이름만으로 따로 만들기", "In three NEW conversations with NO reference images attached, make one panel each using only the name 'Haru, a lab assistant with pink hair': running toward the right / looking out a window / pushing a door. Then place the three results side by side.",
   [("세 컷 모두 정수리 번 2개와 앞머리 가운데 남색 줄이 있나", "#s2"), ("옷(라벤더 후드 + 흰 랩코트)이 같은가", "#s2"), ("B 세 장을 나란히 놓으면 다른 사람처럼 보이는지 비교(6부 f6)", "06_failure_lab.html#f6")],
   tip="B는 일부러 기준 없이 따로 만든 세 장입니다. 한 번의 요청에 여러 변화를 넣지 않습니다.", res="실제 결과: A는 세 컷 모두 번 두 개·가운데 남색 줄·라벤더 후드가 지켜졌습니다. B(기준 없이 이름만)는 분홍 포니테일에 회색 옷을 입은 다른 사람이 나왔고, 첫 컷은 왼쪽으로 달렸습니다. 기준 시트가 왜 필요한지 가장 잘 보여 주는 결과입니다."),
],
6: [
 T("f2_flip", "뒤집힌 방향 고치기", "실패 그림 f2를 고치는 문장 조각으로 다시 만들어, 진단(③ 흐름)이 맞았는지 확인합니다.",
   "B — 고치는 조각 넣기", "Same image, keep the same framing. Change only: in the right panel, Sia walks toward the RIGHT side of the frame, the same screen direction as the left panel. Still no text.",
   [("두 컷 모두 시아가 화면 오른쪽으로 걷나", "03_flow.html#s1"), ("배경·옷·빛은 그대로인가", None), ("고친 뒤 '되돌아간다'는 느낌이 사라졌나", None)], b_key="f2_fixed", res="실제 결과: f2 그림을 첨부하고 방향 문장을 넣었지만, 결과는 f2와 거의 같아 방향이 여전히 반대였습니다. 첨부한 그림을 그대로 따라 그린 경우입니다. f2를 첨부하지 않고 새 대화에서 만든 연습 과제 6-d1에서는 방향이 바로잡혔습니다."),
 T("f6_drift", "바뀌는 캐릭터 고치기", "실패 그림 f6을 기준 시트 첨부와 부분 수정으로 고칩니다.",
   "B — 기준 시트 첨부 + 부분 수정", "Attach refs/haru_sheet.png. Use the image edit / inpainting tool on the second and third panels only, painting over the hair and the hoodie. Prompt: Haru with two round hair buns on top, a thick navy streak down the center of the bangs, lavender hoodie under an open white lab coat, exactly as in the reference sheet. Keep everything else unchanged.",
   [("세 컷 모두 번 2개·가운데 남색 줄·라벤더 후드인가", "05_ai_cuts.html#s2"), ("칠하지 않은 곳(동작·배경)은 그대로인가", "05_ai_cuts.html#s4"), ("고친 곳과 나머지가 따로 놀지 않나", None)], b_key="f6_fixed", res="실제 결과: 부분 수정으로 후드는 세 컷 모두 라벤더가 됐지만, 번은 하나뿐이고 남색은 앞머리 가운데 줄이 아니라 머리띠처럼 남았습니다. 고정값을 하나씩 나눠 칠하고 'exactly two round hair buns'처럼 개수까지 적어 다시 고쳐야 합니다."),
],
}
