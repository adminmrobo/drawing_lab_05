/* ===================== 8부 콘티 북 (BOOK 데이터는 build.py가 앞에 넣는다) ===================== */
var BCOL=['#2458d6','#0f8f84','#e8731a','#6b4fb0'];
function promptBox(h,title){var pb=document.createElement('div');pb.className='promptbox';pb.innerHTML='<b>'+title+'</b><pre aria-live="polite"></pre><button type="button" class="btn copy">복사하기</button>';h.appendChild(pb);return pb.querySelector('pre');}
function cutsOf(n){return n===8?BOOK.s8:n===16?BOOK.s16:BOOK.s32;}
P.p8_beats=function(h){var W=560,H=330;
  function draw(){var n=+rv(h,'n'),sec=rv(h,'sec');var s=svgOf(h,W,H);bg(s,W,H);var per=n/4,rows=n/8,cw=52,ch=40;
    for(var i=0;i<n;i++){var r=Math.floor(i/8),c=i%8,X=78+c*58,Y=24+r*66,b=Math.floor(i/per);el('rect',{x:X,y:Y,width:cw,height:ch,rx:4,fill:mix(BCOL[b],'#ffffff',0.8),stroke:BCOL[b],'stroke-width':1.6},s);ktxt(s,X+cw/2,Y+25,String(i+1),{size:12.5,anchor:'middle',fill:C.ink,weight:'bold'});}
    for(var r2=0;r2<rows;r2++){el('rect',{x:72,y:18+r2*66,width:58*8+4,height:52,rx:6,fill:'none',stroke:C.ink,'stroke-width':2.2},s);ktxt(s,12,49+r2*66,'시트 '+(r2+1),{size:12,fill:C.ink,weight:'bold'});}
    var y0=24+rows*66+16;BOOK.beats.forEach(function(b,i){el('rect',{x:22+i*130,y:y0,width:14,height:14,rx:3,fill:BCOL[i]},s);ktxt(s,41+i*130,y0+12,b+' '+per+'컷',{size:12.5,fill:C.ink});});
    out(h).innerHTML=n+'컷 = 네 덩어리 × <b>'+per+'컷</b> · 길이 '+n+' × '+f2(sec,1)+'초 = <b>'+f2(n*sec,1)+'초</b>'+(n*sec>=60?' (약 '+Math.floor(n*sec/60)+'분 '+Math.round(n*sec%60)+'초)':'')+' · 시트 <b>'+(n/8)+'장</b>. '+(n===32?verdict(true,'덩어리마다 8컷 — 만남에서 아홉 명을 다 만날 수 있습니다'):n===8?verdict(false,'덩어리마다 2컷 — 아홉 명을 만나기엔 컷이 모자랍니다'):'덩어리마다 4컷 — 만남을 둘씩 묶어야 합니다');}
  allIn(h,draw);draw();};
P.p8_split=function(h){var W=560,H=380;
  function box(s,X,Y,w,hh,n,txt,shot,col,emo){el('rect',{x:X,y:Y,width:w,height:hh,rx:6,fill:mix(col,'#ffffff',0.85),stroke:col,'stroke-width':1.8},s);ktxt(s,X+6,Y+15,n+'컷 · '+shot+(emo!=null?' · 감정 '+emo:''),{size:10.5,fill:col,weight:'bold'});wtxt(s,X+6,Y+32,txt,Math.max(6,Math.floor(w/12)),14,{size:11,fill:C.ink});}
  function draw(){var c=+rv(h,'c');var s=svgOf(h,W,H);bg(s,W,H);var b=Math.floor((c-1)/2),col=BCOL[b];
    ktxt(s,10,22,'8컷',{size:12,fill:C.muted,weight:'bold'});ktxt(s,10,132,'16컷',{size:12,fill:C.muted,weight:'bold'});ktxt(s,10,252,'32컷',{size:12,fill:C.muted,weight:'bold'});
    var a=BOOK.s8[c-1];box(s,170,8,230,70,a[0],a[1],a[2],col);
    [0,1].forEach(function(j){var q=BOOK.s16[(c-1)*2+j];box(s,50+j*240,118,230,70,q[0],q[1],q[2],col);ln(s,285,78,165+j*240,118,{stroke:col,w:1.4,dash:'4 3'});});
    for(var j=0;j<4;j++){var q2=BOOK.s32[(c-1)*4+j];box(s,10+j*137,238,130,120,q2[0],q2[1]+' — '+q2[2],q2[5],col,q2[4]);ln(s,165+Math.floor(j/2)*240,188,75+j*137,238,{stroke:col,w:1.2,dash:'3 3'});}
    var e=[0,1,2,3].map(function(j){return BOOK.s32[(c-1)*4+j][4];});
    out(h).innerHTML='8컷의 '+c+'번이 16컷의 '+(2*c-1)+'·'+(2*c)+'번, 32컷의 '+(4*c-3)+'~'+(4*c)+'번이 됩니다. 쪼갠 네 컷의 감정: '+e.join(' → ')+'. '+verdict(true,'네 컷의 목적이 모두 다릅니다(같은 장면 되풀이 없음)');}
  allIn(h,draw);draw();};
function textPrompt(story,n,two,cast){var per=n/4;var rng=BOOK.beats.map(function(b,i){return b+' '+(i*per+1)+'~'+((i+1)*per)+'컷';}).join(', ');
  var t='너는 애니메이션 콘티 작가야. 아래 이야기로 '+n+'컷 콘티 표를 만들어 줘.\n\n이야기(한 문장): '+story+'\n\n';
  t+='[덩어리] 네 덩어리에 '+per+'컷씩: '+rng+'. (덩어리 이름은 이야기에 맞게 바꿔도 됨)\n';
  if(cast)t+='[등장인물] 하루(20대 성인 연구 조수, 정수리 번 2개), 박사(30대 성인 남성), 시아·모아(20대 성인 인턴), 주판봇(모니터 머리 로봇), 초파리 연구원(작은 초파리), 평가단 X1·X2·X3(작은 심사위원 셋). 모두 성인이고 단정한 옷차림.\n';
  t+='[표의 열] 컷 번호 | 덩어리 | 목적 | 흐름·동작(화면 기준 방향: 오른쪽으로, 오른쪽 위로 등) | 감정·보충 | 감정 세기(0~10) | 샷(원경·전신·허리 위·가슴 위·얼굴) | 앵글(눈높이·앙각·부감) | 길이(초) | 등장인물 | English panel description(한 줄, 그림 생성용)\n';
  t+='[규칙]\n1. 컷마다 목적이 달라야 한다. 같은 장면을 줌만 바꿔 되풀이하지 않는다.\n2. 감정이 가장 높은 컷(절정)은 마지막 덩어리의 끝 바로 앞에 두고, 그 앞에 한 번 내려가는 컷을 둔다.\n3. 인물이 움직이는 방향은 화면 기준으로 적고, 한 덩어리 안에서 방향을 뒤집지 않는다(가상선).\n4. 같은 샷이 세 컷 넘게 이어지지 않게 한다. 덩어리 첫 컷은 장소를 보여 주는 원경이나 전신.\n5. 한 컷 평균 3초, 감정이 높은 컷은 길게, 이동 컷은 짧게.\n6. English panel description에는 글자·숫자를 그리라는 말을 넣지 않는다.\n';
  if(two&&n>8)t+='\n[요청 순서] 먼저 8컷 표만 만들어 줘. 내가 확인하면, 그다음 각 컷을 '+(n/8)+'컷으로 쪼개 '+n+'컷 표를 만들어 줘. 쪼갤 때는 원래 컷의 시작과 끝 사이에 있었던 다른 순간·반응을 꺼내고, 같은 순간을 각도만 바꿔 되풀이하지 않는다.\n';
  else t+='\n표가 길면 '+(n>16?'16컷씩 두 번에':'한 번에')+' 나눠서 보내 줘. 컷 번호 1~'+n+'이 빠짐없이 있어야 한다.\n';
  return t;}
P.p8_text=function(h){h.innerHTML='';var ta=document.createElement('textarea');ta.rows=3;ta.style.cssText='width:100%;font:inherit;padding:8px;border:1.5px solid #c3cbd5;border-radius:8px';ta.value=BOOK.story;ta.setAttribute('aria-label','내가 원하는 이야기(한 문장)');
  var lab=document.createElement('div');lab.innerHTML='<b>내가 원하는 이야기(한 문장)</b> <small class="muted">— 고쳐 써 보세요</small>';h.appendChild(lab);h.appendChild(ta);var pre=promptBox(h,'대화형 AI에 넣을 콘티 표 문장');
  function draw(){var n=+rv(h,'n'),two=rv(h,'two'),cast=rv(h,'cast');var st=ta.value.trim();pre.textContent=textPrompt(st||'(이야기를 적어 주세요)',n,two,cast);
    var ok=st.length>=15;out(h).innerHTML=n+'컷 · 열 11개 · 규칙 6개'+(two&&n>8?' · 두 번에 나눠 요청':'')+'. '+verdict(ok,ok?'이야기 한 문장이 들어 있습니다 — 복사해서 대화형 AI에 넣으세요':'이야기를 한 문장(누가 무엇을 해서 어떻게 되었다)으로 더 적어 주세요');}
  ta.addEventListener('input',draw);allIn(h,draw);draw();};
P.p8_sheet=function(h){var W=560,H=200;var pre=null;
  function draw(){var n=+rv(h,'n'),kSel=pick(h,'[name=k]'),maxk=n/8;[].forEach.call(kSel.options,function(o){o.disabled=+o.value>maxk;});if(+kSel.value>maxk)kSel.value=String(maxk);var k=+kSel.value;
    var s=svgOf(h,W,H);bg(s,W,H);var cuts=cutsOf(n).slice((k-1)*8,k*8);
    cuts.forEach(function(q,i){var X=14+(i%4)*136,Y=14+Math.floor(i/4)*92,b=Math.floor((q[0]-1)/(n/4));el('rect',{x:X,y:Y,width:128,height:72,fill:'#fff',stroke:C.ink,'stroke-width':1.4},s);
      ktxt(s,X+5,Y+14,'CUT '+q[0],{size:10.5,fill:BCOL[b],weight:'bold'});wtxt(s,X+5,Y+32,q[1],10,13,{size:10.5,fill:C.ink});
      var who=n===32?q[8]:'';who.split('').forEach(function(cc,j){el('circle',{cx:X+118-j*13,cy:Y+62,r:6,fill:{H:'#e86aa6',D:'#4a5568',S:'#1e1b22',M:'#c9a77c',B:'#e8dcc0',F:'#c0392b',X:'#1e2f6e'}[cc],stroke:'#fff','stroke-width':1},s);});});
    if(!pre)pre=promptBox(h,'Genspark에 넣을 시트 프롬프트');pre.textContent=BOOK.sheet[n+'_'+k];
    out(h).innerHTML=n+'컷 콘티의 시트 <b>'+k+' / '+maxk+'</b> (컷 '+((k-1)*8+1)+'~'+(k*8)+'). '+(k>1?'같은 대화에서 시트 '+(k-1)+' 결과를 첨부하고 넣습니다.':'새 대화에서 첨부 없이 시작합니다(연필 마네킹이라 캐릭터 기준 그림 대신 실루엣 규칙을 씁니다).')+(n===32?' 점 색은 등장인물.':'');}
  allIn(h,draw);draw();};
P.p8_cut=function(h){var W=560,H=230;var pre=null,att=null;
  function draw(){var c=+rv(h,'c'),m=rv(h,'m');var q=BOOK.s32[c-1];var k=Math.ceil(c/8),pos=(c-1)%8;var s=svgOf(h,W,H);bg(s,W,H);
    ktxt(s,14,18,'시트 '+k,{size:12,fill:C.ink,weight:'bold'});for(var i=0;i<8;i++){var X=14+(i%4)*58,Y=26+Math.floor(i/4)*44;el('rect',{x:X,y:Y,width:52,height:36,fill:i===pos?'#fff7ec':'#fff',stroke:i===pos?C.orange:C.ink,'stroke-width':i===pos?2.4:1.2},s);ktxt(s,X+26,Y+23,String((k-1)*8+i+1),{size:11,anchor:'middle'});}
    if(m==='sheet'){el('rect',{x:8,y:20,width:244,height:100,fill:'none',stroke:C.red,'stroke-width':2.4,'stroke-dasharray':'6 4'},s);}
    arrow(s,262,72,322,72,{stroke:m==='sheet'?C.red:C.green,w:2.4,head:10});
    var X2=334,Y2=24;el('rect',{x:X2,y:Y2,width:210,height:118,fill:'#fff',stroke:C.ink,'stroke-width':1.6},s);
    if(m==='sheet'){for(var j=0;j<8;j++)el('rect',{x:X2+6+(j%4)*50,y:Y2+10+Math.floor(j/4)*50,width:44,height:42,fill:'#f2f4f7',stroke:'#9aa5b1'},s);ktxt(s,X2+105,Y2+136,'여러 컷 그림이 또 나오기 쉬움',{size:11,anchor:'middle',fill:C.red});}
    else{el('rect',{x:X2+4,y:Y2+4,width:202,height:110,fill:'#eef3fb'},s);fig(s,{x:X2+105,y:Y2+112,h:96,dir:q[0]===18?-1:1,pose:'look'});ktxt(s,X2+105,Y2+136,'구도는 스케치, 그림은 완성 애니풍',{size:11,anchor:'middle',fill:C.green});}
    ktxt(s,14,160,'컷 '+c+' — '+q[1]+' · '+q[5]+' · '+q[6]+(BOOK.done.indexOf(c)>=0?' · ★ 완성할 컷':''),{size:12,fill:C.ink});ktxt(s,14,182,'등장: '+q[9],{size:11.5});
    if(!att){att=document.createElement('div');att.className='box';att.style.marginTop='8px';h.appendChild(att);}if(!pre)pre=promptBox(h,'Genspark에 넣을 완성 컷 프롬프트');
    att.innerHTML='<b>첨부할 것</b> — '+BOOK.attach[c+'_'+m].join(' · ');pre.textContent=BOOK.cut[c+'_'+m];
    out(h).innerHTML=(m==='crop'?verdict(true,'그 컷만 잘라 붙이고 "구도와 자세만 참고"를 적었습니다'):verdict(false,'시트 통째로 — 여러 컷 그림이 다시 나오거나 연필 그림체가 남을 수 있습니다(이번 실험에서는 잘 나왔지만 컷을 잘못 고를 위험이 있음)'))+(c===BOOK.key?' · 이 컷이 <b>기준 컷</b>입니다. 가장 먼저 만드세요.':' · 기준 컷(31컷)을 먼저 만든 뒤 함께 첨부합니다.');}
  allIn(h,draw);draw();};
