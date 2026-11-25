# 실전 연습장 미션 판정 점검 (로컬 서버 8765번 필요). 직접 조작하기 전에는 미션이 판정되지 않아야 하고, 조작하면 판정돼야 한다.
import asyncio
from playwright.async_api import async_playwright
async def setr(page,sc,name,v):
    await page.evaluate("([sc,n,v])=>{const e=document.querySelector('#'+sc+' [name=\"'+n+'\"]');if(e.type==='checkbox'){e.checked=v;}else e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",[sc,name,v])
async def done(page,sc): return await page.evaluate("sc=>[...document.querySelectorAll('#'+sc+' .missions li')].map(l=>l.classList.contains('done'))",sc)
async def main():
    ok=True
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        page=await b.new_page();await page.route('**/fonts.g*/**',lambda r: r.abort())
        errs=[];page.on("pageerror",lambda e: errs.append(str(e)))
        await page.goto("http://localhost:8765/practice/index.html#bench");await page.wait_for_timeout(800)
        r0=await done(page,'bench');print('bench before',r0);ok&=not any(r0)
        for n,v in [('a',2),('b',2),('c',2),('d',2),('peak',7),('len','24'),('sec',3),('first','ls')]: await setr(page,'bench',n,v)
        r=await done(page,'bench');print('bench after',r);ok&=all(r)
        await page.click('.tabs button[data-t=camera]')
        r0=await done(page,'camera');print('camera before',r0);ok&=not any(r0)
        for t,vals in [('c4',dict(shot='3',cam='eye',face='r',x=30)),('c6',dict(shot='1',cam='low',face='r',x=50)),('c1',dict(shot='0',cam='eye',face='r',x=50)),('c5',dict(shot='5',cam='eye',face='r',x=40))]:
            await setr(page,'camera','target',t)
            for n,v in vals.items(): await setr(page,'camera',n,v)
        r=await done(page,'camera');print('camera after',r);ok&=all(r)
        await page.click('.tabs button[data-t=workshop]')
        r0=await done(page,'workshop');print('workshop before',r0);ok&=not any(r0)
        c5=dict(shot='close-up',angle='eye-level camera',who='haru',act='lifting her head',dir='toward the UPPER RIGHT of the frame',emo='startled realization, eyes wide',bg='next to a large window',light='soft backlight from a window')
        c6=dict(shot='full body shot',angle='low angle shot looking up',who='haru',act='climbing the stairs quickly',dir='toward the UPPER RIGHT of the frame',emo='determined',bg='in a bright stairwell',light='daylight from the top of the stairs')
        for vals in (c5,c6):
            for n,v in vals.items(): await setr(page,'workshop',n,v)
        r=await done(page,'workshop');print('workshop after',r);ok&=all(r)
        await page.click('.tabs button[data-t=desk]')
        SYM=['같은 크기·같은 자세','되돌아가는','거인','공중에 떠','차렷','머리 장식과 옷 색','오른쪽 끝에 붙어','그림자 방향이 반대']
        CA=['컷의 목적이 같음','가상선을 넘음','거리만큼 줄이지 않음','눈높이 선 불일치','중심축이 곧음','고정값이 바뀜','시선 여백 없음','빛 방향이 바뀜']
        r0=await done(page,'desk');print('desk before',r0);ok&=not any(r0)
        for _ in range(60):
            sym=await page.text_content('#desk .sym');k=[i for i,s in enumerate(SYM) if s in sym][0]
            await page.click(f"#desk .deskopts button:text-is('{CA[k]}')");await page.wait_for_timeout(560)
        r=await done(page,'desk');print('desk after',r);ok&=all(r)
        await page.goto("http://localhost:8765/practice/template.html");await page.wait_for_timeout(600)
        await page.click('[data-mode=sample]');await page.wait_for_timeout(200)
        t=await page.text_content('.tsheet');good='단서를 알아챈다' in t;print('template sample',good);ok&=good
        print('errors',errs);ok&=not errs
        await b.close()
    print('미션 점검 통과' if ok else '미션 점검 실패')
asyncio.run(main())
