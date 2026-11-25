# -*- coding: utf-8 -*-
"""본문 '숫자로 한 번 해 보기'·퀴즈 숫자와 평가 점수 검산. python3 build/check_numbers.py"""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2, P3
from content_b import P4, P5, P6
ok = True
def chk(name, got, want, tol=0.01):
    global ok
    good = abs(got - want) <= tol
    ok &= good
    print(("OK " if good else "XX "), name, round(got, 4), "기대", want)
EMO = [3, 5, 6, 4, 8, 7, 9, 5]; DUR = [3, 1.5, 3, 3, 3, 2.5, 3, 5]
# 1부
chk("1-1 합계", 2 + 2 + 2 + 2, 8); chk("1-1 길이", 8 * 3, 24); chk("1-1 퀴즈", 8 * 3, 24)
d = [EMO[i] - EMO[i - 1] for i in range(1, 8)]
chk("1-3 변화량 첫", d[0], 2); chk("1-3 변화량 4컷", d[2], -2); chk("1-3 변화량 5컷", d[3], 4)
chk("1-3 오름 횟수", sum(1 for x in d if x > 0), 4); chk("1-3 내림 횟수", sum(1 for x in d if x < 0), 3); chk("1-3 절정 컷", EMO.index(max(EMO)) + 1, 7)
chk("1-4 썸네일", 8 * 1, 8); chk("1-4 자세히", 8 * 15, 120); chk("1-4 두 번 고침 썸", 8 * 1 * 3, 24); chk("1-4 두 번 고침 자세히", 8 * 15 * 3, 360)
# 2부
chk("2-1 여백", 9 - 7.5, 1.5); chk("2-1 머리 px", 900 / 9, 100)
chk("2-2 4m", 300 * 2 / 4, 150); chk("2-2 6m", 300 * 2 / 6, 100)
chk("2-4 앞 여백", 1200 - 400, 800); chk("2-4 비", 800 / 400, 2)
# 3부
chk("3-3 5컷 프레임", 3 * 24, 72); chk("3-3 2컷 프레임", 1.5 * 24, 36); chk("3-3 전체 초", sum(DUR), 24); chk("3-3 전체 프레임", sum(DUR) * 24, 576); chk("3-3 퀴즈", 2.5 * 24, 60)
# 4부
chk("4-1 10%", 20 / 200 * 100, 10); chk("4-1 20%", 40 / 200 * 100, 20)
chk("4-2 무게중심", (6 * 10 + 1 * 16 + 3 * 8) / 10, 10)
chk("4-3 1.5kg", 1.5 * 0.6, 0.9); chk("4-3 1.5kg 거리", 0.9 / 60, 0.015, 0.0001); chk("4-3 15kg", 15 * 0.6 / 60, 0.15, 0.0001); chk("4-3 퀴즈", 3 * 0.6 / 60, 0.03, 0.0001)
# 5부
chk("5-2 0.9^8", 0.9 ** 8, 0.43, 0.005); chk("5-2 0.97^8", 0.97 ** 8, 0.78, 0.005); chk("5-2 0.99^8", 0.99 ** 8, 0.92, 0.005); chk("5-2 이름만 0.8^8", 0.8 ** 8, 0.17, 0.005); chk("5-2 퀴즈", 0.9 * 0.9, 0.81)
chk("5-3 0.4", 30 * 0.4, 12); chk("5-3 0.8", 30 * 0.8, 24); chk("5-3 0.2", 30 * 0.2, 6); chk("5-3 퀴즈", 40 * 0.5, 20)
for P in (P1, P2, P3, P4, P5, P6):
    J = P["judge"]; sa, sb = sum(J["a"][1]), sum(J["b"][1]); txt = J["result"][0][2]
    good = f"{sb} : 주판봇 {sa}" in txt; ok &= good
    print(("OK " if good else "XX "), P["no"], "부 평가", sb, ":", sa, txt[:22])
print("전체 통과" if ok else "검산 실패"); sys.exit(0 if ok else 1)
