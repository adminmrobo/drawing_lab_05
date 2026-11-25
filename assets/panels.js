/* 구조 먼저 그리기 연구실 05 · 콘티 편 — 실험 패널 모음 (외부 라이브러리 없음) */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var C={teal:'#0f8f84',orange:'#e8731a',navy:'#1e2f6e',blue:'#2458d6',green:'#13733a',red:'#c9302c',purple:'#6b4fb0',grid:'#e3e8ee',muted:'#5b6874',ink:'#16212b'};
var KFONT='"IBM Plex Sans KR","Malgun Gothic","Noto Sans KR",sans-serif';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var P={};

/* ---------- 공용 도구 ---------- */
function el(tag,a,parent){var e=document.createElementNS(NS,tag);for(var k in a){if(a[k]!=null)e.setAttribute(k,a[k]);}if(parent)parent.appendChild(e);return e;}
function ktxt(p,x,y,s,a){a=a||{};var t=el('text',{x:x,y:y,'font-size':a.size||13,fill:a.fill||C.muted,'font-family':KFONT,'text-anchor':a.anchor||'start','font-weight':a.weight||'normal'},p);t.textContent=s;return t;}
function svgOf(h,W,H,label){h.innerHTML='';return el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'실험 그림: '+(label||noteOf(h))},h);}
function noteOf(h){var n=h.parentNode&&h.parentNode.querySelector('.ph small');return n?n.textContent:'';}
function canvasOf(h,W,H,mw){h.innerHTML='';var c=document.createElement('canvas');c.width=W;c.height=H;c.style.width='100%';c.style.maxWidth=(mw||W*1.2)+'px';c.style.margin='0 auto';c.style.height='auto';c.style.display='block';c.style.borderRadius='10px';c.setAttribute('role','img');c.setAttribute('aria-label','실험 그림: '+noteOf(h));h.appendChild(c);return c;}
function out(h){return h.parentNode.querySelector('.readout');}
function ctl(h){return h.parentNode.querySelector('.ctrl');}
function f2(v,d){d=d==null?2:d;if(d===0)return String(Math.round(v));var m=Math.pow(10,d);var s=(Math.round(v*m)/m).toFixed(d);s=s.replace(/\.?0+$/,'');if(s==='-0')s='0';return s;}
function num(v,d){return v<0?'−'+f2(-v,d):f2(v,d);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function hex(c){c=c.replace('#','');return[parseInt(c.substr(0,2),16),parseInt(c.substr(2,2),16),parseInt(c.substr(4,2),16)];}
function rgb(a){return 'rgb('+a.map(function(v){return Math.round(clamp(v,0,255));}).join(',')+')';}
function mix(c1,c2,t){var a=hex(c1),b=hex(c2);return rgb([lerp(a[0],b[0],t),lerp(a[1],b[1],t),lerp(a[2],b[2],t)]);}
function shade(c,k){var a=hex(c);return rgb([a[0]*k,a[1]*k,a[2]*k]);}
function rad(d){return d*Math.PI/180;}
function seg(h,sel,cb){var bs=ctl(h).querySelectorAll(sel);bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b);});});}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function onIn(inp,f){inp.addEventListener('input',f);}
function svgPt(s,e){var m=s.getScreenCTM().inverse();var q=s.createSVGPoint();q.x=e.clientX;q.y=e.clientY;return q.matrixTransform(m);}

function board(el_,items){el_.innerHTML=items.map(function(it){return '<div class="'+(it[2]?'good':'bad')+'"><span>'+it[0]+'</span><b>'+it[1]+'</b></div>';}).join('');}
function say(el_,lines){el_.innerHTML=lines.map(function(l){return '<div class="line"><img src="../assets/chars/'+l[0]+'_'+l[1]+'.webp" alt="" width="48" height="48"><div class="bub"><b>'+l[2]+'</b>'+l[3]+'</div></div>';}).join('');}
function missions(el_,state,touched){el_.querySelectorAll('li').forEach(function(li,i){if(touched&&state[i])li.classList.add('done');});}
var DONE={};
/* ===================== 콘티 그리기 도구 (SVG) ===================== */
var PC={ink:'#3a3f47',soft:'#9aa5b1',guide:'#e0337f',paper:'#ffffff',hot:'#e8731a',fill:'#dfe6ee'};
var BEAT=[['시작','#2458d6'],['전개','#0f8f84'],['전환','#e8731a'],['끝','#6b4fb0']];
var EMO=[3,5,6,4,8,7,9,5];
var DUR=[3,1.5,3,3,3,2.5,3,5];
var CUT_TXT=[['연구소 앞에 선다 — 인물과 장소 소개','멈춰 서서 두리번','걱정 · 초파리가 없어졌다'],
 ['찾기 시작','오른쪽으로 달린다','서두름'],
 ['연구소 복도로 들어간다','안쪽으로 걷는다(뒷모습)','긴장'],
 ['창밖을 본다','오른쪽 창을 바라봄','멈칫 · 조용함'],
 ['단서를 알아챈다','고개를 들어 오른쪽 위를 봄','깨달음 · 날개가 반짝였다'],
 ['계단을 오른다','오른쪽 위로 올라감(앙각)','결의'],
 ['옥상 문을 연다','몸 전체로 문을 민다','각오 · 문틈으로 빛'],
 ['옥상에서 초파리를 만난다','밖으로 나섬(넓어짐)','안도 · 새 출발']];
var CUT_SHOT=['원경','전신','전신(뒷모습)','허리 위','얼굴','전신(앙각)','허리 위','원경'];
function pth(s,d,a){a=a||{};return el('path',{d:d,fill:a.fill||'none',stroke:a.stroke||PC.ink,'stroke-width':a.w||2,'stroke-linecap':'round','stroke-linejoin':'round','stroke-dasharray':a.dash||null,opacity:a.op==null?null:a.op},s);}
function ln(s,x1,y1,x2,y2,a){a=a||{};return el('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:a.stroke||PC.ink,'stroke-width':a.w||2,'stroke-linecap':'round','stroke-dasharray':a.dash||null,opacity:a.op==null?null:a.op},s);}
function P2(x,y){return x.toFixed(1)+','+y.toFixed(1);}
function wrapT(t,n){var out=[],cur='';t.split(' ').forEach(function(w){if((cur+' '+w).trim().length>n&&cur){out.push(cur);cur=w;}else cur=(cur?cur+' ':'')+w;});if(cur)out.push(cur);var o2=[];out.forEach(function(l){while(l.length>n+2){o2.push(l.slice(0,n));l=l.slice(n);}o2.push(l);});return o2;}
function wtxt(s,x,y,t,n,lh,a){wrapT(t,n).forEach(function(l,i){ktxt(s,x,y+i*lh,l,a);});}
function pick(h,sel){return ctl(h).querySelector(sel);}
function rv(h,name){var e=pick(h,'[name='+name+']');return e?(e.type==='checkbox'?e.checked:(e.tagName==='SELECT'?e.value:+e.value)):null;}
function allIn(h,f){ctl(h).querySelectorAll('input,select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
function bg(s,W,H){el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);}
function seg2(h,cb){var bs=ctl(h).querySelectorAll('button[data-v]');bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b.dataset.v);});});}
function verdict(ok,txt){return '<span style="color:'+(ok?C.green:C.red)+';font-weight:700">'+(ok?'✔ ':'⚠ ')+txt+'</span>';}
function frame(s,x,y,w,h,a){a=a||{};return el('rect',{x:x,y:y,width:w,height:h,fill:a.fill||PC.paper,stroke:a.stroke||PC.ink,'stroke-width':a.w||1.6,rx:a.rx||0},s);}
var CLIPN=0;
function clipTo(s,x,y,w,h){var id='cl'+(++CLIPN)+'_'+Math.floor(Math.random()*1e6);var d=el('defs',{},s);var c=el('clipPath',{id:id},d);el('rect',{x:x,y:y,width:w,height:h},c);return el('g',{'clip-path':'url(#'+id+')'},s);}
function arrow(s,x1,y1,x2,y2,a){a=a||{};var col=a.stroke||PC.ink,w=a.w||2.4,ang=Math.atan2(y2-y1,x2-x1),L=a.head||10;
  if(a.hollow){var nx=-Math.sin(ang)*w*1.6,ny=Math.cos(ang)*w*1.6;var bx=x2-Math.cos(ang)*L,by=y2-Math.sin(ang)*L;
    el('path',{d:'M'+P2(x1+nx,y1+ny)+' L'+P2(bx+nx,by+ny)+' L'+P2(bx+nx*2.6,by+ny*2.6)+' L'+P2(x2,y2)+' L'+P2(bx-nx*2.6,by-ny*2.6)+' L'+P2(bx-nx,by-ny)+' L'+P2(x1-nx,y1-ny)+'Z',fill:'#fff',stroke:col,'stroke-width':1.8,'stroke-linejoin':'round'},s);return;}
  ln(s,x1,y1,x2-Math.cos(ang)*L*0.6,y2-Math.sin(ang)*L*0.6,{stroke:col,w:w,dash:a.dash});
  el('path',{d:'M'+P2(x2,y2)+' L'+P2(x2-Math.cos(ang-0.45)*L,y2-Math.sin(ang-0.45)*L)+' L'+P2(x2-Math.cos(ang+0.45)*L,y2-Math.sin(ang+0.45)*L)+'Z',fill:col},s);}
/* 마네킹 머리: 동그라미 + 십자선. dir: 1 오른쪽, -1 왼쪽, 0 정면, 2 뒷모습. up: 위를 보는 정도(-1~1) */
function mhead(s,x,y,r,dir,o){o=o||{};var col=o.stroke||PC.ink,w=o.w||1.8;el('circle',{cx:x,cy:y,r:r,fill:o.fill||'#fff',stroke:col,'stroke-width':w},s);
  var up=o.up||0;var ey=y+r*0.1-up*r*0.35;
  if(dir===2){pth(s,'M'+P2(x-r,y)+' Q'+P2(x,y+r*0.25)+' '+P2(x+r,y),{stroke:col,w:1,op:.5});return;}
  var cxl=x+(dir===0?0:dir*r*0.45);
  pth(s,'M'+P2(cxl,y-r)+' Q'+P2(cxl+(dir===0?0:dir*r*0.28),y)+' '+P2(cxl,y+r),{stroke:col,w:1.2,op:.85});
  pth(s,'M'+P2(x-r*(dir===-1?1:0.95),ey)+' Q'+P2(x+(dir===0?0:dir*r*0.25),ey+r*0.22)+' '+P2(x+r*(dir===1?1:0.95),ey),{stroke:col,w:1.2,op:.85});
  if(dir!==0&&o.nose!==false)pth(s,'M'+P2(x+dir*r*0.98,ey+r*0.05)+' l'+P2(dir*r*0.18,r*0.18)+' l'+P2(-dir*r*0.16,r*0.05),{stroke:col,w:1.2});}
/* 마네킹 전신. o: x(두 발 가운데), y(바닥), h(키), dir, pose:'stand'|'walk'|'run'|'push'|'climb'|'carry'|'look', lean(도), up(시선) */
function fig(s,o){var x=o.x,y=o.y,h=o.h,dir=o.dir==null?1:o.dir,pose=o.pose||'stand',col=o.stroke||PC.ink,w=o.w||Math.max(1.4,h/90),r=h/15;
  var sd=(dir===0||dir===2)?0:dir,g=el('g',{},s);var lean=rad(o.lean||({run:14,push:24,climb:10,carry:-9}[pose]||0))*(sd||1);
  var hip=[x,y-h*0.48];var tl=h*0.33;var nk=[hip[0]+Math.sin(lean)*tl,hip[1]-Math.cos(lean)*tl];var hd=[nk[0]+Math.sin(lean)*r*1.3,nk[1]-Math.cos(lean)*r*1.3];
  if(pose==='carry')hip=[x+sd*h*0.03,y-h*0.47];
  // 다리
  var st=h*({stand:0.05,look:0.05,walk:0.16,run:0.24,push:0.26,climb:0.12,carry:0.12}[pose]||0.05);
  var f1=[x+sd*st,y],f2=[x-sd*st,y];if(pose==='climb'){f1=[x+sd*st,y-h*0.09];}
  if(pose==='run'){f2=[x-sd*st*1.1,y-h*0.08];}
  if(sd===0){f1=[x+st*0.6+h*0.04,y];f2=[x-st*0.6-h*0.04,y];}
  [f1,f2].forEach(function(f,i){var kx=(hip[0]+f[0])/2+(sd||1)*h*0.03*(i?-0.2:1),ky=(hip[1]+f[1])/2;pth(g,'M'+P2(hip[0],hip[1])+' Q'+P2(kx,ky)+' '+P2(f[0],f[1]),{stroke:col,w:w});pth(g,'M'+P2(f[0],f[1])+' l'+P2((sd||(i?-1:1))*h*0.05,0),{stroke:col,w:w});});
  // 몸통(가운데 축)
  pth(g,'M'+P2(hip[0],hip[1])+' Q'+P2((hip[0]+nk[0])/2-(sd||0)*h*0.02,(hip[1]+nk[1])/2)+' '+P2(nk[0],nk[1]),{stroke:col,w:w*1.6});
  el('ellipse',{cx:hip[0],cy:hip[1],rx:h*0.045,ry:h*0.028,fill:'#fff',stroke:col,'stroke-width':w},g);
  var ch=[hip[0]+Math.sin(lean)*tl*0.72,hip[1]-Math.cos(lean)*tl*0.72];
  el('ellipse',{cx:ch[0],cy:ch[1],rx:h*0.05,ry:h*0.085,fill:'#fff',stroke:col,'stroke-width':w,transform:'rotate('+(lean*180/Math.PI).toFixed(1)+' '+ch[0].toFixed(1)+' '+ch[1].toFixed(1)+')'},g);
  // 팔
  var sh=[nk[0]-Math.sin(lean)*h*0.03,nk[1]+Math.cos(lean)*h*0.03];var al=h*0.38;
  function arm(a1,a2,i){var e=[sh[0]+Math.sin(a1)*al/2,sh[1]+Math.cos(a1)*al/2];var hnd=[e[0]+Math.sin(a2)*al/2,e[1]+Math.cos(a2)*al/2];pth(g,'M'+P2(sh[0],sh[1])+' L'+P2(e[0],e[1])+' L'+P2(hnd[0],hnd[1]),{stroke:col,w:w,op:i?0.7:1});el('circle',{cx:hnd[0],cy:hnd[1],r:h*0.018,fill:'#fff',stroke:col,'stroke-width':w*0.8},g);return hnd;}
  var d=sd||1,hands=[];
  if(pose==='push'){hands.push(arm(d*rad(95)-lean*0,d*rad(95),0),arm(d*rad(85),d*rad(88),1));}
  else if(pose==='run'){hands.push(arm(d*rad(55),d*rad(140),0),arm(-d*rad(45),d*rad(10),1));}
  else if(pose==='walk'||pose==='climb'){hands.push(arm(d*rad(25),d*rad(40),0),arm(-d*rad(22),-d*rad(5),1));}
  else if(pose==='carry'){hands.push(arm(d*rad(40),d*rad(100),0),arm(d*rad(35),d*rad(95),1));}
  else if(pose==='look'){hands.push(arm(d*rad(8),d*rad(4),0),arm(-d*rad(8),d*rad(0),1));}
  else {hands.push(arm(rad(12),rad(4),0),arm(-rad(12),-rad(4),1));}
  mhead(g,hd[0],hd[1],r,dir,{stroke:col,w:w,up:o.up});
  if(pose==='carry'){var bw=h*0.2;el('rect',{x:hands[0][0]-(d>0?0:bw),y:hands[0][1]-bw*0.85,width:bw,height:bw,fill:'#efe3cf',stroke:col,'stroke-width':w},g);}
  return {g:g,hip:hip,neck:nk,head:hd,r:r,hands:hands,f1:f1,f2:f2};}
/* 예시 콘티 한 컷 그리기 */
function drawCut(s,i,X,Y,W,H,o){o=o||{};var g=clipTo(s,X,Y,W,H);el('rect',{x:X,y:Y,width:W,height:H,fill:'#fff'},g);var col=PC.ink,soft=PC.soft;
  var gy=Y+H*0.82;
  if(i===0){ln(g,X,gy,X+W,gy,{stroke:soft,w:1.3});[[0.08,0.3,0.3],[0.4,0.18,0.42],[0.62,0.3,0.34]].forEach(function(b){var bx=X+W*b[0],bw=W*b[1],bh=H*b[2]*1.4;el('rect',{x:bx,y:gy-bh,width:bw,height:bh,fill:'none',stroke:soft,'stroke-width':1.3},g);for(var k=0;k<3;k++)ln(g,bx+bw*0.2,gy-bh+bh*(0.25+k*0.22),bx+bw*0.8,gy-bh+bh*(0.25+k*0.22),{stroke:soft,w:1,op:.6});});
    fig(g,{x:X+W*0.5,y:gy+H*0.05,h:H*0.32,dir:0,pose:'stand'});}
  if(i===1){ln(g,X,gy,X+W,gy,{stroke:soft,w:1.3});ln(g,X+W*0.75,Y+H*0.2,X+W*0.75,gy,{stroke:soft,w:1.3});pth(g,'M'+P2(X+W*0.68,Y+H*0.25)+' q'+P2(W*0.07,-H*0.15)+' '+P2(W*0.14,0),{stroke:soft,w:1.3});
    fig(g,{x:X+W*0.38,y:gy,h:H*0.62,dir:1,pose:'run'});arrow(g,X+W*0.55,gy+H*0.08,X+W*0.72,gy+H*0.08,{w:1.8,head:8});}
  if(i===2){var vx=X+W*0.5,vy=Y+H*0.42;[[X,Y],[X+W,Y],[X,Y+H],[X+W,Y+H]].forEach(function(p){ln(g,p[0],p[1],vx+(p[0]-vx)*0.18,vy+(p[1]-vy)*0.18,{stroke:soft,w:1.2});});el('rect',{x:vx-W*0.09,y:vy-H*0.13,width:W*0.18,height:H*0.25,fill:'none',stroke:soft,'stroke-width':1.2},g);
    fig(g,{x:vx,y:Y+H*0.86,h:H*0.5,dir:2,pose:'walk'});arrow(g,vx+W*0.12,Y+H*0.85,vx+W*0.12,Y+H*0.68,{w:1.6,head:7});}
  if(i===3){el('rect',{x:X+W*0.62,y:Y+H*0.12,width:W*0.32,height:H*0.62,fill:'none',stroke:soft,'stroke-width':1.4},g);ln(g,X+W*0.78,Y+H*0.12,X+W*0.78,Y+H*0.74,{stroke:soft,w:1.2});
    var f=fig(g,{x:X+W*0.3,y:Y+H*1.55,h:H*1.5,dir:1,pose:'look'});arrow(g,f.head[0]+f.r*1.4,f.head[1],X+W*0.58,f.head[1]-H*0.04,{w:1.6,head:7});}
  if(i===4){var hx=X+W*0.46,hy=Y+H*0.56,r=H*0.34;pth(g,'M'+P2(hx-r*0.8,Y+H)+' Q'+P2(hx-r*0.2,hy+r*0.9)+' '+P2(hx,hy+r*0.95)+' Q'+P2(hx+r*0.3,hy+r*0.9)+' '+P2(hx+r*0.9,Y+H),{w:1.8});mhead(g,hx,hy,r,1,{up:0.7,w:1.8});
    [[0.78,0.2,0.88,0.12],[0.8,0.34,0.92,0.32],[0.2,0.22,0.12,0.14]].forEach(function(q){ln(g,X+W*q[0],Y+H*q[1],X+W*q[2],Y+H*q[3],{w:1.6});});
    el('rect',{x:X+W*0.84,y:Y+H*0.06,width:W*0.12,height:H*0.3,fill:'none',stroke:soft,'stroke-width':1.2},g);}
  if(i===5){for(var k=0;k<7;k++){var yy=Y+H*(0.95-k*0.12),xx=X+W*(0.05+k*0.1);ln(g,xx,yy,xx+W*0.55,yy-H*0.03,{stroke:soft,w:1.2});ln(g,xx,yy,xx,yy-H*0.12,{stroke:soft,w:1.2});}
    fig(g,{x:X+W*0.45,y:Y+H*0.8,h:H*0.62,dir:1,pose:'climb'});arrow(g,X+W*0.62,Y+H*0.45,X+W*0.78,Y+H*0.25,{w:1.8,head:8});}
  if(i===6){el('rect',{x:X+W*0.66,y:Y+H*0.05,width:W*0.26,height:H*0.95,fill:'#f4f6f8',stroke:soft,'stroke-width':1.4},g);el('circle',{cx:X+W*0.7,cy:Y+H*0.55,r:H*0.035,fill:'none',stroke:soft},g);
    ln(g,X+W*0.92,Y+H*0.05,X+W*0.97,Y+H*0.95,{stroke:PC.hot,w:1.2,op:.6});fig(g,{x:X+W*0.42,y:Y+H*1.45,h:H*1.35,dir:1,pose:'push'});}
  if(i===7){var hz=Y+H*0.66;ln(g,X,hz,X+W,hz,{stroke:soft,w:1.2});[[0.05,0.1],[0.13,0.16],[0.22,0.08],[0.62,0.13],[0.7,0.2],[0.8,0.1],[0.88,0.15]].forEach(function(b){el('rect',{x:X+W*b[0],y:hz-H*b[1],width:W*0.07,height:H*b[1],fill:'none',stroke:soft,'stroke-width':1},g);});
    ln(g,X,Y+H*0.88,X+W,Y+H*0.86,{stroke:soft,w:1.3});fig(g,{x:X+W*0.66,y:Y+H*0.9,h:H*0.36,dir:2,pose:'stand'});el('circle',{cx:X+W*0.82,cy:Y+H*0.2,r:2.5,fill:PC.hot},g);
    pth(g,'M'+P2(X+W*0.79,Y+H*0.2)+' q'+P2(-4,-5)+' '+P2(-8,0)+' M'+P2(X+W*0.85,Y+H*0.2)+' q'+P2(4,-5)+' '+P2(8,0),{stroke:PC.hot,w:1.2});}
  frame(s,X,Y,W,H,{fill:'none',w:o.bw||1.6});
  if(o.num!==false)ktxt(s,X+5,Y+14,'CUT '+(i+1),{size:11,fill:PC.soft});}
/* 실험 0: 예시 콘티 한 장 */
P.p0_sample=function(h){var nc=(h.clientWidth||800)<600?2:4,W=nc===4?760:388,H=nc===4?560:1100;var s=svgOf(h,W,H,'예시 콘티 여덟 컷 — 하루, 초파리를 찾아 옥상까지');bg(s,W,H);
  for(var i=0;i<8;i++){var c=i%nc,r=Math.floor(i/nc),X=12+c*186,Y=12+r*274,w=176,hh=99;drawCut(s,i,X,Y,w,hh);
    var labs=['목적','흐름·동작','감정·보충'];labs.forEach(function(l,k){var yy=Y+hh+20+k*44;ktxt(s,X,yy,l,{size:10.5,fill:C.teal,weight:'bold'});
      var L=wrapT(CUT_TXT[i][k],k===0?12:9);L.forEach(function(t,j){ktxt(s,X+(k===0?34:58),yy+j*15,t,{size:10.5,fill:C.ink});});ln(s,X,yy+(L.length-1)*15+7,X+w,yy+(L.length-1)*15+7,{stroke:'#d5dbe2',w:1});});}
  out(h).innerHTML='여덟 컷 · 한 컷 평균 3초 · 장면 길이 약 <b>24초</b>. 1·8컷은 원경, 5컷은 얼굴, 6컷은 앙각입니다. 이 콘티를 1~5부가 함께 씁니다.';};

/* ===================== 1부 콘티의 뼈대 ===================== */
P.p1_beats=function(h){var W=560,H=300;
  function draw(){var v=[rv(h,'a'),rv(h,'b'),rv(h,'c'),rv(h,'d')],sec=rv(h,'sec');var tot=v[0]+v[1]+v[2]+v[3];var s=svgOf(h,W,H);bg(s,W,H);
    var slots=Math.max(8,tot),cols=Math.max(4,Math.ceil(slots/2)),cw=(W-30)/cols-8,k=0;
    for(var b=0;b<4;b++){for(var j=0;j<v[b];j++){var c=k%cols,r=Math.floor(k/cols),X=15+c*(cw+8),Y=30+r*110;var over=k>=8;el('rect',{x:X,y:Y,width:cw,height:80,rx:6,fill:over?'#fdeceb':mix(BEAT[b][1],'#ffffff',0.82),stroke:over?C.red:BEAT[b][1],'stroke-width':2},s);ktxt(s,X+cw/2,Y+36,(k+1)+'컷',{size:13,anchor:'middle',fill:C.ink,weight:'bold'});ktxt(s,X+cw/2,Y+56,over?'넘침':BEAT[b][0],{size:12,anchor:'middle',fill:over?C.red:BEAT[b][1]});k++;}}
    for(;k<8;k++){var c2=k%cols,r2=Math.floor(k/cols),X2=15+c2*(cw+8),Y2=30+r2*110;el('rect',{x:X2,y:Y2,width:cw,height:80,rx:6,fill:'#fff',stroke:'#c3cbd5','stroke-width':1.5,'stroke-dasharray':'5 4'},s);ktxt(s,X2+cw/2,Y2+46,'비어 있음',{size:12,anchor:'middle'});}
    BEAT.forEach(function(b,i){el('rect',{x:15+i*110,y:254,width:14,height:14,rx:3,fill:b[1]},s);ktxt(s,34+i*110,266,b[0]+' '+v[i]+'컷',{size:12.5,fill:C.ink});});
    var zero=v.map(function(x,i){return x===0?BEAT[i][0]:null;}).filter(Boolean);
    out(h).innerHTML='합계 <b>'+tot+'컷</b> × '+f2(sec,1)+'초 = 장면 길이 <b>'+f2(tot*sec,1)+'초</b>. '+verdict(tot===8,tot===8?'여덟 컷이 딱 맞음':(tot>8?(tot-8)+'컷 넘침 — 다른 덩어리에서 빼세요':(8-tot)+'컷 비어 있음'))+' · '+
      verdict(zero.length===0,zero.length===0?'네 덩어리 모두 있음':zero.join('·')+' 덩어리가 0컷 — 이야기가 끊깁니다');}
  allIn(h,draw);draw();};
P.p1_lines=function(h){var W=560,H=330;var GUESS=[['왜 이 컷이 있는지 몰라 빼도 될 것 같다','인물이 어디로 움직이는지 모른다','어떤 얼굴을 할지 몰라 무난한 미소를 고른다']];
  function draw(){var i=+rv(h,'cut'),on=[rv(h,'l0'),rv(h,'l1'),rv(h,'l2')];var s=svgOf(h,W,H);bg(s,W,H);drawCut(s,i,20,20,300,169);
    var labs=['목적','흐름·동작','감정·보충'];labs.forEach(function(l,k){var y=222+k*34;ktxt(s,20,y,l,{size:12.5,fill:C.teal,weight:'bold'});ln(s,20,y+8,320,y+8,{stroke:'#d5dbe2',w:1});ktxt(s,95,y,on[k]?CUT_TXT[i][k]:'(비어 있음)',{size:12.5,fill:on[k]?C.ink:C.red});});
    var n=on.filter(Boolean).length;ktxt(s,350,40,'이 컷을 받은 사람이 채우는 것',{size:13,fill:C.ink,weight:'bold'});
    var y0=70;on.forEach(function(o,k){if(o)return;var t=GUESS[0][k];el('rect',{x:345,y:y0-16,width:200,height:58,rx:6,fill:'#fff7ec',stroke:C.orange},s);ktxt(s,353,y0+2,labs[k]+' 없음 →',{size:11.5,fill:C.orange,weight:'bold'});wtxt(s,353,y0+21,t,15,14,{size:11});y0+=68;});
    if(n===3){el('rect',{x:345,y:54,width:200,height:60,rx:6,fill:'#ecf7ef',stroke:C.green},s);ktxt(s,353,78,'세 줄이 다 있음',{size:12.5,fill:C.green,weight:'bold'});ktxt(s,353,98,'누가 봐도 같은 컷을 떠올림',{size:11.5});}
    out(h).innerHTML=(i+1)+'컷 · 세 줄 중 <b>'+n+' / 3</b>. '+verdict(n===3,n===3?'그림이 거칠어도 같은 컷으로 읽힙니다':'빠진 '+(3-n)+'줄은 받은 사람(또는 AI)이 제멋대로 채웁니다');}
  allIn(h,draw);draw();};
P.p1_curve=function(h){var W=560,H=320,v=[5,5,5,5,5,5,5,5],x0=60,bw=56,base=270,unit=22;
  seg2(h,function(m){v=m==='flat'?[5,5,5,5,5,5,5,5]:m==='up'?[2,3,4,5,6,7,8,9]:EMO.slice();draw();});
  h.addEventListener('click',function(e){var s=h.querySelector('svg');if(!s)return;var p=svgPt(s,e);var i=Math.floor((p.x-x0)/(bw+6));if(i<0||i>7)return;v[i]=clamp(Math.round((base-p.y)/unit),0,10);draw();});
  function draw(){var s=svgOf(h,W,H);bg(s,W,H);for(var k=0;k<=10;k+=2){var y=base-k*unit;ln(s,x0-6,y,x0+8*(bw+6),y,{stroke:'#e3e8ee',w:1});ktxt(s,x0-10,y+4,String(k),{size:11,anchor:'end'});}
    var mx=Math.max.apply(null,v),pk=v.indexOf(mx);var pts=[];
    v.forEach(function(val,i){var X=x0+i*(bw+6);el('rect',{x:X,y:base-10*unit,width:bw,height:10*unit,fill:'transparent',style:'cursor:pointer'},s);el('rect',{x:X+8,y:base-val*unit,width:bw-16,height:Math.max(2,val*unit),rx:4,fill:i===pk?C.orange:mix(C.teal,'#ffffff',0.45)},s);ktxt(s,X+bw/2,base+18,(i+1)+'컷',{size:11.5,anchor:'middle',fill:C.ink});pts.push(P2(X+bw/2,base-val*unit));});
    pth(s,'M'+pts.join(' L'),{stroke:C.navy,w:2.4});v.forEach(function(val,i){el('circle',{cx:x0+i*(bw+6)+bw/2,cy:base-val*unit,r:4,fill:C.navy},s);});
    var d=[],up=0,dn=0;for(var i=1;i<8;i++){var q=v[i]-v[i-1];d.push((q>0?'+':q<0?'−':'')+Math.abs(q));if(q>0)up++;if(q<0)dn++;}
    var dipBefore=false;for(var j=1;j<=pk;j++){if(v[j]<v[j-1])dipBefore=true;}
    out(h).innerHTML='변화량: '+d.join(', ')+' · 오름 <b>'+up+'</b>번, 내림 <b>'+dn+'</b>번 · 절정 <b>'+(pk+1)+'컷('+mx+')</b>. '+verdict(pk===5||pk===6,(pk===5||pk===6)?'절정이 끝 바로 앞':'절정이 6~7컷이 아님')+' · '+verdict(dipBefore&&up>=3,dipBefore&&up>=3?'절정 앞에 한 번 내려감':(up===0&&dn===0?'오르내림이 없어 밋밋함':'절정 앞에 쉬는 컷이 없음'));}
  draw();};
P.p1_thumb=function(h){var W=560,H=300;var T=[1,5,15];
  function draw(){var sz=rv(h,'size'),lv=+rv(h,'lv'),fx=rv(h,'fix');var s=svgOf(h,W,H);bg(s,W,H);var fw=sz*20,fh=fw*9/16,X=20,Y=20+(135-fh/2)*0.5;
    frame(s,X,Y,fw,fh);var g=clipTo(s,X,Y,fw,fh);var gy=Y+fh*0.85;ln(g,X,gy,X+fw,gy,{stroke:PC.soft,w:Math.max(0.6,fw/200)});
    var f=fig(g,{x:X+fw*0.35,y:gy,h:fh*0.7,dir:1,pose:'walk',w:Math.max(0.7,fw/160)});
    if(lv>=1){el('rect',{x:X+fw*0.6,y:Y+fh*0.15,width:fw*0.3,height:fh*0.55,fill:'none',stroke:PC.soft,'stroke-width':Math.max(0.6,fw/220)},g);el('ellipse',{cx:f.hip[0],cy:(f.hip[1]+f.neck[1])/2,rx:fh*0.08,ry:fh*0.18,fill:'none',stroke:PC.ink,'stroke-width':Math.max(.5,fw/260),opacity:.6},g);}
    if(lv>=2){var rr=rng(7);for(var k=0;k<24;k++){el('rect',{x:X+fw*(0.62+(k%4)*0.07),y:Y+fh*(0.18+Math.floor(k/4)*0.085),width:fw*0.045,height:fh*0.055,fill:'none',stroke:PC.soft,'stroke-width':Math.max(.4,fw/400)},g);}
      for(var m=0;m<40;m++){el('circle',{cx:f.head[0]+(rr()-.5)*fh*0.22,cy:f.hip[1]+(rr()-.7)*fh*0.4,r:Math.max(.4,fw/300),fill:PC.ink,opacity:.5},g);}
      el('circle',{cx:f.head[0]+fh*0.025,cy:f.head[1],r:Math.max(.4,fw/250),fill:PC.ink},g);}
    var read=lv===0?true:(lv===1?sz>=4:sz>=9);var t=T[lv],tot=8*t*(1+fx);
    ktxt(s,300,60,'그림 크기 '+sz+'cm · '+['도형만','윤곽','세부까지'][lv],{size:13,fill:C.ink,weight:'bold'});ktxt(s,300,90,'한 컷 약 '+t+'분(예시값)',{size:12.5});ktxt(s,300,114,'8컷 × '+t+'분 × (1 + 고친 '+fx+'번) = '+tot+'분',{size:12.5,fill:C.ink});
    ktxt(s,300,150,read?'큰 모양(머리·몸 방향·땅 선)이 읽힙니다':'세부가 점과 얼룩이 되어 사람이 묻힙니다',{size:12.5,fill:read?C.green:C.red,weight:'bold'});
    out(h).innerHTML='콘티 한 장 시간 <b>'+tot+'분</b>'+(tot>=60?' (약 '+f2(tot/60,1)+'시간)':'')+'. '+verdict(read,read?'이 크기에서 읽힘':'이 크기에서는 세부가 오히려 방해')+' · '+verdict(tot<=40,tot<=40?'고치기 부담 없음':'고칠 때마다 시간이 많이 듭니다');}
  allIn(h,draw);draw();};

/* ===================== 2부 카메라 ===================== */
var SHOTS=[['원경(LS)',20],['전신(FS)',9],['무릎 위(KS)',6.5],['허리 위(WS)',4.5],['가슴 위(BS)',3],['얼굴(CU)',1.5]];
P.p2_shot=function(h){var W=560,H=330;
  function draw(){var k=+rv(h,'shot'),px=rv(h,'px');var s=svgOf(h,W,H);bg(s,W,H);var X=70,Y=20,FW=440,FH=FW*9/16;var heads=SHOTS[k][1],hp=FH/heads;
    var g=clipTo(s,X,Y,FW,FH);el('rect',{x:X,y:Y,width:FW,height:FH,fill:'#fff'},g);var figH=7.5*hp;var top=Y+hp*(k===0?heads*0.55:0.6);
    if(k===0){ln(g,X,top+figH,X+FW,top+figH,{stroke:PC.soft,w:1});el('rect',{x:X+FW*0.6,y:top+figH-FH*0.55,width:FW*0.25,height:FH*0.55,fill:'none',stroke:PC.soft},g);}
    fig(g,{x:X+FW*0.42,y:top+figH,h:figH,dir:0,pose:'stand',w:Math.max(1.4,Math.min(4,figH/90))});frame(s,X,Y,FW,FH,{fill:'none',w:2});
    for(var i=0;i<=Math.min(heads,24);i++){var yy=Y+i*hp;if(yy>Y+FH+0.5)break;ln(s,X-14,yy,X-4,yy,{stroke:PC.guide,w:1.6});}
    ktxt(s,X-18,Y+FH/2,'머리 '+f2(heads,1)+'개',{size:12,anchor:'end',fill:PC.guide,weight:'bold'});
    ktxt(s,X,Y+FH+28,SHOTS[k][0]+' — 화면 높이에 머리 약 '+f2(heads,1)+'개',{size:13,fill:C.ink,weight:'bold'});
    var hpx=px/heads;out(h).innerHTML='화면 높이 '+px+'px ÷ 머리 '+f2(heads,1)+'개 = 머리 하나 <b>'+f2(hpx,1)+'px</b>. '+(k<=1?'장소와 움직임이 먼저 보입니다(예시 콘티 1·2·3·6·8컷).':k>=4?'얼굴과 마음이 먼저 보입니다(예시 콘티 5컷).':'몸짓과 표정이 함께 보입니다(예시 콘티 4·7컷).');}
  allIn(h,draw);draw();};
P.p2_vp=function(h){var W=560,H=320;pick(h,'[name=fixed]').checked=true;
  function draw(){var cam=rv(h,'eye')/100,gap=rv(h,'gap'),fixed=rv(h,'fixed');var s=svgOf(h,W,H);bg(s,W,H);var hz=120,vx=380,f=300,ds=[2,2+gap,2+2*gap,2+3*gap,2+4*gap];
    [[0,H],[W,H],[0,0],[W,0]].forEach(function(p){ln(s,p[0],p[1],vx,hz,{stroke:'#e3e8ee',w:1});});
    ln(s,0,hz,W,hz,{stroke:PC.guide,w:1.8,dash:'7 5'});ktxt(s,8,hz-6,'눈높이 선',{size:12,fill:PC.guide,weight:'bold'});el('circle',{cx:vx,cy:hz,r:4,fill:PC.guide},s);ktxt(s,vx+8,hz-6,'소실점',{size:11.5,fill:PC.guide});
    var sz0=f*1/ds[0],info=[],heads=[],feet=[];
    ds.forEach(function(d,i){var foot=hz+f*cam/d,sz=fixed?sz0:f/d,x=vx-f*1.1/d;fig(s,{x:x,y:foot,h:sz,dir:1,pose:'stand',w:Math.max(1,sz/70)});heads.push([x,foot-sz]);feet.push([x,foot]);info.push(Math.round(sz));});
    if(!fixed){ln(s,heads[0][0],heads[0][1],vx,hz,{stroke:C.teal,w:1.2,dash:'4 4'});ln(s,feet[0][0],feet[0][1],vx,hz,{stroke:C.teal,w:1.2,dash:'4 4'});}
    var hit=fixed?'사람마다 다른 곳':'모두 키의 '+Math.round(cam*100)+'% 높이';
    out(h).innerHTML='거리 '+ds.map(function(d){return f2(d,1)+'m';}).join(' · ')+' → 크기 '+info.join(' · ')+'px. 눈높이 선이 지나는 곳: <b>'+hit+'</b>'+(Math.abs(cam-0.93)<0.04&&!fixed?'(모두의 눈)':'')+'. '+
      verdict(!fixed,fixed?'멀어도 크기가 같아 먼 사람이 거인처럼 보입니다(6부 f3)':'거리 2배면 크기 1/2 — 머리 끝선·발끝선이 소실점으로 모입니다');}
  allIn(h,draw);draw();};
P.p2_angle=function(h){var W=560,H=320;
  function draw(){var cam=rv(h,'cam');var s=svgOf(h,W,H);bg(s,W,H);var X=40,Y=15,FW=480,FH=270;var g=clipTo(s,X,Y,FW,FH);el('rect',{x:X,y:Y,width:FW,height:FH,fill:'#fff'},g);
    var hz=Y+FH/2-cam*1.9;var sc=1-cam/220;ln(g,X,hz,X+FW,hz,{stroke:PC.guide,w:1.8,dash:'7 5'});
    for(var k=0;k<6;k++){var yy=hz+(Y+FH-hz)*(0.15+k*0.17);ln(g,X,yy,X+FW,yy,{stroke:'#e3e8ee',w:1});}
    var fh=200*sc,fy=Y+FH*0.92+cam*0.6;fig(g,{x:X+FW*0.45,y:fy,h:fh,dir:1,pose:'climb',up:cam<0?0.3:-0.3});
    if(cam<-8)for(var j=0;j<5;j++){ln(g,X+FW*(0.6+j*0.07),Y+FH,X+FW*(0.62+j*0.05),hz+10,{stroke:PC.soft,w:1});}
    frame(s,X,Y,FW,FH,{fill:'none',w:2});ktxt(s,X+FW+6,hz+4,'지평선',{size:11.5,fill:PC.guide});
    var nm=Math.abs(cam)<10?'눈높이':(cam<0?'앙각(아래에서 올려다보기)':'부감(위에서 내려다보기)');var feel=Math.abs(cam)<10?'담담하고 안정된 느낌':(cam<0?'인물이 크고 단단해 보임 — 결의·힘':'인물이 작고 외로워 보임 — 넓은 세상·쓸쓸함');
    out(h).innerHTML='카메라 '+(cam>0?'+':'')+cam+' → <b>'+nm+'</b>. 지평선이 화면 '+(cam<-5?'아래쪽':cam>5?'위쪽':'가운데')+'에 있습니다. '+feel+'. '+(cam<=-20?verdict(true,'6컷 「결의」에 알맞은 앵글'):'');}
  allIn(h,draw);draw();};
P.p2_lead=function(h){var W=560,H=320,dir=1;seg2(h,function(v){dir=+v;draw();});
  function draw(){var xp=rv(h,'x')/100;var s=svgOf(h,W,H);bg(s,W,H);var X=40,Y=15,FW=480,FH=270;var g=clipTo(s,X,Y,FW,FH);el('rect',{x:X,y:Y,width:FW,height:FH,fill:'#fff'},g);
    [1,2].forEach(function(k){ln(g,X+FW*k/3,Y,X+FW*k/3,Y+FH,{stroke:'#c3cbd5',w:1.2,dash:'5 5'});ln(g,X,Y+FH*k/3,X+FW,Y+FH*k/3,{stroke:'#c3cbd5',w:1.2,dash:'5 5'});});
    var cx=X+FW*xp;var f=fig(g,{x:cx,y:Y+FH*2.1,h:FH*2.2,dir:dir,pose:'look'});arrow(g,f.head[0]+dir*f.r*1.3,f.head[1],f.head[0]+dir*f.r*3.2,f.head[1],{stroke:C.orange,w:2,head:9});
    frame(s,X,Y,FW,FH,{fill:'none',w:2});var front=dir>0?(1-xp):xp,back=dir>0?xp:(1-xp);var ratio=front/back;var third=Math.min(Math.abs(xp-1/3),Math.abs(xp-2/3))<0.07;
    var W1=1200,fx=Math.round(W1*xp);
    out(h).innerHTML='화면 너비 1200 기준 인물 가운데 '+fx+' · 바라보는 쪽 여백 '+Math.round(W1*front)+' ÷ 반대쪽 '+Math.round(W1*back)+' = <b>'+f2(ratio,2)+'</b>. '+
      verdict(ratio>=1.5&&ratio<=3.5,ratio<1?'시선 앞이 막혀 답답합니다(6부 f7)':ratio<1.5?'여백이 조금 부족합니다':ratio>3.5?'인물이 화면 끝에 밀려 있습니다':'시선 앞이 트여 편안합니다')+' · '+verdict(third,third?'1/3 선 근처':'1/3 선에서 벗어남');}
  allIn(h,draw);draw();};

/* ===================== 3부 컷 잇기 ===================== */
P.p3_line=function(h){var W=560,H=420;
  function draw(){var a=rad(rv(h,'ang'));var s=svgOf(h,W,H);bg(s,W,H);var cx=150,cy=120,R=90;
    ktxt(s,20,22,'위에서 본 배치',{size:12.5,fill:C.ink,weight:'bold'});el('rect',{x:cx-130,y:cy,width:260,height:R+20,fill:'rgba(15,143,132,.07)'},s);ktxt(s,cx+60,cy+R+12,'카메라를 둘 쪽',{size:11,fill:C.teal});
    ln(s,cx-135,cy,cx+135,cy,{stroke:PC.guide,w:2,dash:'8 5'});ktxt(s,cx-130,cy-8,'가상선',{size:11.5,fill:PC.guide,weight:'bold'});
    el('circle',{cx:cx,cy:cy,r:9,fill:'#1E1B22'},s);arrow(s,cx+10,cy,cx+50,cy,{stroke:'#1E1B22',w:2.4,head:9});ktxt(s,cx-14,cy-14,'시아 →',{size:11.5,fill:C.ink});
    var px=cx+Math.cos(a)*R,py=cy-Math.sin(a)*R;el('rect',{x:px-10,y:py-7,width:20,height:14,rx:3,fill:C.blue,transform:'rotate('+(-(a*180/Math.PI)+90).toFixed(1)+' '+px.toFixed(1)+' '+py.toFixed(1)+')'},s);ln(s,px,py,cx,cy,{stroke:C.blue,w:1.2,dash:'3 3'});ktxt(s,px+12,py-8,'카메라',{size:11,fill:C.blue});
    var sn=Math.sin(a),cs=Math.cos(a),view;if(Math.abs(sn)<0.26)view=cs>0?'front':'back';else view=sn<0?'right':'left';
    var X=300,Y=40,FW=240,FH=135;frame(s,X,Y,FW,FH);ktxt(s,X,Y-8,'카메라 화면',{size:12.5,fill:C.ink,weight:'bold'});var g=clipTo(s,X,Y,FW,FH);var gy=Y+FH*0.85;ln(g,X,gy,X+FW,gy,{stroke:PC.soft,w:1});
    var dir=view==='right'?1:view==='left'?-1:view==='front'?0:2;fig(g,{x:X+FW/2,y:gy,h:FH*0.7,dir:dir,pose:'walk'});
    if(dir===1||dir===-1)arrow(g,X+FW/2+dir*30,gy+10,X+FW/2+dir*80,gy+10,{w:2,head:8});else arrow(g,X+FW*0.8,gy+8,X+FW*0.8,gy-(dir===0?-14:14),{w:1.6,head:7});
    var Y2=230;frame(s,X,Y2,FW,FH);ktxt(s,X,Y2-8,'앞 컷(2컷)',{size:12.5,fill:C.ink,weight:'bold'});var g2=clipTo(s,X,Y2,FW,FH);ln(g2,X,Y2+FH*0.85,X+FW,Y2+FH*0.85,{stroke:PC.soft,w:1});fig(g2,{x:X+FW/2,y:Y2+FH*0.85,h:FH*0.7,dir:1,pose:'run'});arrow(g2,X+FW/2+30,Y2+FH*0.85+10,X+FW/2+80,Y2+FH*0.85+10,{w:2,head:8});
    var txt={right:'화면에서 오른쪽으로 걷습니다 — 2컷과 같은 방향',left:'화면에서 왼쪽으로 걷습니다 — 되돌아가는 것처럼 보입니다',front:'선 위(정면) — 다가오는 다리 컷',back:'선 위(뒷모습) — 멀어지는 다리 컷(예시 콘티 3컷)'}[view];
    out(h).innerHTML='카메라 '+rv(h,'ang')+'° · 선의 '+(sn<-0.26?'오른쪽(시아 기준)':sn>0.26?'왼쪽(시아 기준)':'위')+' → '+verdict(view!=='left',txt);}
  allIn(h,draw);draw();};
var ARW={walk:['인물이 오른쪽으로 걷는다','인물 옆에 속이 찬 화살표','walking toward the right, mid-stride'],up:['인물이 위로 오른다','인물 옆에 위로 향한 속이 찬 화살표','climbing the stairs, moving up'],
  pan:['카메라가 오른쪽으로 돈다(팬)','화면 밖에 속이 빈 화살표','(한 장 그림에는 없음) — 넓은 배경을 이어 붙인 가로 긴 그림으로 대신'],zoom:['카메라가 가까워진다(줌 인)','화면 안에 끝 화면 틀','(한 장 그림에는 없음) — 시작 그림과 끝 그림을 따로 만든다'],
  follow:['인물이 오르고 카메라도 따라간다','속이 찬 화살표 + 화면 밖 속이 빈 화살표','climbing the stairs, camera following from below']};
P.p3_arrows=function(h){var W=560,H=300;
  function draw(){var k=rv(h,'kind');var s=svgOf(h,W,H);bg(s,W,H);var X=80,Y=30,FW=380,FH=214;var g=clipTo(s,X,Y,FW,FH);el('rect',{x:X,y:Y,width:FW,height:FH,fill:'#fff'},g);var gy=Y+FH*0.88;
    if(k==='up'||k==='follow'){for(var i=0;i<6;i++){var yy=Y+FH*(0.95-i*0.13),xx=X+FW*(0.1+i*0.12);ln(g,xx,yy,xx+FW*0.4,yy,{stroke:PC.soft,w:1.1});}fig(g,{x:X+FW*0.42,y:Y+FH*0.8,h:FH*0.6,dir:1,pose:'climb'});arrow(g,X+FW*0.62,Y+FH*0.55,X+FW*0.76,Y+FH*0.3,{w:2.6,head:10});}
    else{ln(g,X,gy,X+FW,gy,{stroke:PC.soft,w:1.1});fig(g,{x:X+FW*0.42,y:gy,h:FH*0.7,dir:1,pose:k==='walk'?'walk':'stand'});if(k==='walk')arrow(g,X+FW*0.56,gy-FH*0.3,X+FW*0.78,gy-FH*0.3,{w:2.6,head:10});}
    frame(s,X,Y,FW,FH,{fill:'none',w:2});
    if(k==='pan')arrow(s,X+FW*0.3,Y+FH+22,X+FW*0.85,Y+FH+22,{hollow:true,w:3,head:16});
    if(k==='follow')arrow(s,X+FW+22,Y+FH*0.85,X+FW+22,Y+FH*0.2,{hollow:true,w:3,head:16});
    if(k==='zoom'){el('rect',{x:X+FW*0.28,y:Y+FH*0.12,width:FW*0.36,height:FH*0.36*FW/FH*9/16*FH/FW*16/9,fill:'none',stroke:C.blue,'stroke-width':2,'stroke-dasharray':'7 4'},s);
      [[X,Y,X+FW*0.28,Y+FH*0.12],[X+FW,Y,X+FW*0.64,Y+FH*0.12]].forEach(function(q){arrow(s,q[0],q[1],q[2],q[3],{stroke:C.blue,w:1.4,head:7});});ktxt(s,X+FW*0.46,Y+FH*0.12-6,'끝 화면',{size:11.5,fill:C.blue,anchor:'middle'});}
    var A=ARW[k];out(h).innerHTML='<b>'+A[0]+'</b> — 콘티에는 '+A[1]+'. AI 문장으로는: <i>'+A[2]+'</i>';}
  allIn(h,draw);draw();};
P.p3_time=function(h){var W=560,H=300,d=DUR.slice();d[4]=0.5;var cutSel=pick(h,'[name=cut]'),secIn=pick(h,'[name=sec]');
  cutSel.addEventListener('change',function(){secIn.value=d[+cutSel.value];draw();});secIn.addEventListener('input',function(){d[+cutSel.value]=+secIn.value;draw();});
  seg2(h,function(){d=DUR.slice();secIn.value=d[+cutSel.value];draw();});
  function draw(){var c=+cutSel.value;var s=svgOf(h,W,H);bg(s,W,H);var tot=d.reduce(function(a,b){return a+b;},0);var X=20,Wd=W-40,x=X,base=220;
    d.forEach(function(sec,i){var w=Wd*sec/Math.max(tot,1),eh=EMO[i]*16;el('rect',{x:x+1,y:base-eh,width:Math.max(2,w-2),height:eh,rx:4,fill:i===c?C.orange:mix(C.teal,'#ffffff',0.5),stroke:i===c?C.orange:'none'},s);
      if(w>26)ktxt(s,x+w/2,base+18,(i+1)+'컷',{size:11.5,anchor:'middle',fill:C.ink});if(w>30)ktxt(s,x+w/2,base+36,f2(sec,1)+'초',{size:11,anchor:'middle'});x+=w;});
    ln(s,X,base,X+Wd,base,{stroke:C.ink,w:1.4});ktxt(s,X,24,'막대 너비 = 컷 길이 · 막대 높이 = 감정 세기(1부)',{size:12});
    var sec=d[c],fr=sec*24;var hiEmo=EMO[c]>=8,move=c===1||c===5;var ok=!(hiEmo&&sec<2)&&!(move&&sec>3.5);
    out(h).innerHTML=(c+1)+'컷 '+f2(sec,1)+'초 × 24 = <b>'+f2(fr,1)+'프레임</b> · 전체 <b>'+f2(tot,1)+'초</b> × 24 = '+f2(tot*24,1)+'프레임. '+
      verdict(ok,hiEmo&&sec<2?'감정이 높은 컷인데 너무 짧아 전해지기 전에 지나갑니다':move&&sec>3.5?'이동만 하는 컷이 길어 늘어집니다':'이 컷의 길이가 알맞습니다');}
  draw();};
P.p3_eyeline=function(h){var W=560,H=280;var V={r:[1,0],ru:[0.8,-0.6],l:[-1,0],u:[0,-1],c:[0,0]};var POS={c:[0.5,0.5],r:[0.85,0.5],ru:[0.82,0.18],l:[0.15,0.5],u:[0.5,0.14]};
  function draw(){var lk=rv(h,'look'),ob=rv(h,'obj');var s=svgOf(h,W,H);bg(s,W,H);var Y=40,FW=250,FH=FW*9/16;
    [[20,'앞 컷'],[290,'다음 컷']].forEach(function(q){frame(s,q[0],Y,FW,FH);ktxt(s,q[0],Y-10,q[1],{size:12.5,fill:C.ink,weight:'bold'});});
    var g=clipTo(s,20,Y,FW,FH);var dir=lk==='l'?-1:1;var f=fig(g,{x:20+FW*(dir>0?0.3:0.7),y:Y+FH*2.05,h:FH*2.1,dir:lk==='u'?0:dir,pose:'look',up:(lk==='ru'||lk==='u')?0.8:0});
    var v=V[lk];arrow(g,f.head[0]+v[0]*f.r*1.3,f.head[1]+v[1]*f.r*1.3,f.head[0]+v[0]*f.r*3.4,f.head[1]+v[1]*f.r*3.4,{stroke:C.orange,w:2,head:9});
    var g2=clipTo(s,290,Y,FW,FH);ln(g2,290,Y+FH*0.75,290+FW,Y+FH*0.72,{stroke:PC.soft,w:1.2});var p=POS[ob];var ox=290+FW*p[0],oy=Y+FH*p[1];
    el('circle',{cx:ox,cy:oy,r:5,fill:C.orange},g2);pth(g2,'M'+P2(ox-3,oy)+' q'+P2(-6,-8)+' '+P2(-12,-1)+' M'+P2(ox+3,oy)+' q'+P2(6,-8)+' '+P2(12,-1),{stroke:C.orange,w:1.6});
    [[0,-1],[0.7,-0.7],[1,0],[-0.7,-0.7]].forEach(function(q){ln(g2,ox+q[0]*9,oy+q[1]*9,ox+q[0]*14,oy+q[1]*14,{stroke:C.orange,w:1.2});});
    var match=lk===ob,mid=ob==='c';
    out(h).innerHTML='앞 컷 시선: <b>'+{r:'오른쪽',ru:'오른쪽 위',l:'왼쪽',u:'위'}[lk]+'</b> · 다음 컷 대상: <b>'+{c:'가운데',r:'오른쪽',ru:'오른쪽 위',l:'왼쪽',u:'위'}[ob]+'</b>. '+
      verdict(match,match?'"그것을 보았다"가 설명 없이 읽힙니다':mid?'크게 어긋나지는 않지만 어디서 본 것인지 약합니다':'시선과 대상이 어긋나 두 컷이 따로 읽힙니다');}
  allIn(h,draw);draw();};

/* ===================== 4부 포즈와 연기 ===================== */
function bez(p0,p1,p2,p3,t){var u=1-t;return [u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0],u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]];}
function axisFig(s,o){var cx=o.x,top=o.top,bot=o.bot,L=bot-top,b=o.bend/100,mode=o.mode||'c',col=o.stroke||PC.ink,w=o.w||2.4;
  var hx=cx+b*L*0.9,fx=cx-b*L*0.25;var p0=[hx,top],p3=[fx,bot];var k=mode==='c'?b*L*1.25:b*L*2.2;var p1=[hx-(mode==='c'?k:k),top+L*0.33],p2=[fx-(mode==='c'?k:-k),top+L*0.66];
  var pts=[];for(var i=0;i<=40;i++)pts.push(bez(p0,p1,p2,p3,i/40));
  var dev=0;pts.forEach(function(p){var t=(p[1]-top)/L;var lx=hx+(fx-hx)*t;dev=Math.max(dev,Math.abs(p[0]-lx));});
  var g=el('g',{},s);var P=function(t){return pts[Math.round(clamp(t,0,1)*40)];};
  var hd=P(0.06),nk=P(0.15),ch=P(0.27),hip=P(0.5),kn=P(0.75),ft=P(1);var r=L*0.065;var thick=o.sil?L*0.075:w;var fillC=o.sil?'#1d2330':'#fff',lc=o.sil?'#1d2330':col;
  var d=b>=0?1:-1;var spread=o.spread==null?Math.abs(b)*1.2:o.spread;
  var f2_=[hip[0]+d*(0.18+spread*0.6)*L*0.5,bot];var k2=[(hip[0]+f2_[0])/2+d*L*0.04,(hip[1]+bot)/2];
  pth(g,'M'+P2(hip[0],hip[1])+' Q'+P2(k2[0],k2[1])+' '+P2(f2_[0],f2_[1]),{stroke:lc,w:thick});
  pth(g,'M'+P2(hip[0],hip[1])+' Q'+P2(kn[0],kn[1])+' '+P2(ft[0],ft[1]),{stroke:lc,w:thick});
  pth(g,'M'+P2(hip[0],hip[1])+' Q'+P2(ch[0],ch[1])+' '+P2(nk[0],nk[1]),{stroke:lc,w:o.sil?L*0.16:thick*1.6});
  var armA=o.armA==null?(Math.abs(b)>0.06?95:12):o.armA;var al=L*0.4;
  [0,1].forEach(function(i){var aa=rad(armA-(i?14:0))*d;var e=[ch[0]+Math.sin(aa)*al*0.5,ch[1]-L*0.03+Math.cos(aa)*al*0.5];var hh=[e[0]+Math.sin(aa+d*rad(-8))*al*0.5,e[1]+Math.cos(aa+d*rad(-8))*al*0.5];
    pth(g,'M'+P2(ch[0],ch[1]-L*0.03)+' L'+P2(e[0],e[1])+' L'+P2(hh[0],hh[1]),{stroke:lc,w:thick*(o.sil?0.85:1),op:o.sil?1:(i?0.7:1)});});
  if(o.sil)el('circle',{cx:hd[0],cy:hd[1],r:r*1.1,fill:fillC},g);else mhead(g,hd[0],hd[1],r,b>=0?1:-1,{w:w*0.8});
  return {g:g,pts:pts,dev:dev,L:L,hip:hip,ft:ft,hd:hd};}
P.p4_axis=function(h){var W=560,H=340,mode='c';seg2(h,function(v){mode=v;draw();});
  function draw(){var b=rv(h,'bend');var s=svgOf(h,W,H);bg(s,W,H);ln(s,20,310,W-20,310,{stroke:PC.soft,w:1.3});
    if(b>8)el('rect',{x:400,y:60,width:60,height:250,fill:'#f4f6f8',stroke:PC.soft,'stroke-width':1.5},s);
    var A=axisFig(s,{x:270,top:50,bot:310,bend:b,mode:mode});pth(s,'M'+A.pts.map(function(p){return P2(p[0],p[1]);}).join(' L'),{stroke:PC.guide,w:2.4,op:.8});
    ln(s,A.pts[0][0],A.pts[0][1],A.pts[40][0],A.pts[40][1],{stroke:C.teal,w:1.2,dash:'5 4'});
    var pc=A.dev/A.L*100;var kind=pc<3?'곧은 선 — 서 있는 사람':pc<15?'살짝 휜 '+(mode==='c'?'C자 — 기대거나 가볍게 움직임':'S자 — 걷거나 돌아봄'):'크게 휜 '+(mode==='c'?'C자 — 힘껏 밀거나 당김':'S자 — 크게 비틀거나 춤추듯');
    out(h).innerHTML='중심축 길이 '+Math.round(A.L)+' · 곧은 선에서 가장 멀리 '+f2(A.dev,0)+' → 휜 정도 <b>'+f2(pc,0)+'%</b>. '+kind+'. '+(b>8&&mode==='c'?verdict(pc>=15,pc>=15?'문을 미는 힘이 보입니다':'문 앞에 기대 선 것처럼 보입니다'):'');}
  allIn(h,draw);draw();};
P.p4_balance=function(h){var W=560,H=330;
  function draw(){var lean=rad(rv(h,'lean')),st=rv(h,'step');var s=svgOf(h,W,H);bg(s,W,H);var gy=300,x0=220,sp=st*2.2,fb=x0,ff=x0+sp,pel=[(fb+ff)/2,gy-130],T=110,hr=17;
    el('rect',{x:fb-14,y:gy-6,width:sp+28,height:12,rx:4,fill:'rgba(19,115,58,.25)'},s);ln(s,20,gy,W-20,gy,{stroke:PC.soft,w:1.3});
    var nk=[pel[0]+Math.sin(lean)*T,pel[1]-Math.cos(lean)*T],hd=[pel[0]+Math.sin(lean)*(T+hr*1.3),pel[1]-Math.cos(lean)*(T+hr*1.3)],tm=[pel[0]+Math.sin(lean)*T/2,pel[1]-Math.cos(lean)*T/2];
    pth(s,'M'+P2(pel[0],pel[1])+' L'+P2(fb,gy)+' M'+P2(pel[0],pel[1])+' L'+P2(ff,gy),{w:3});pth(s,'M'+P2(pel[0],pel[1])+' L'+P2(nk[0],nk[1]),{w:5});mhead(s,hd[0],hd[1],hr,1,{w:2});
    pth(s,'M'+P2(nk[0],nk[1]+8)+' l'+P2(28,40)+' M'+P2(nk[0],nk[1]+8)+' l'+P2(-22,38),{w:2.6});
    var cog=(6*tm[0]+1*hd[0]+3*pel[0])/10,cy=(6*tm[1]+hd[1]+3*pel[1])/10;el('circle',{cx:cog,cy:cy,r:6,fill:PC.guide},s);ln(s,cog,cy,cog,gy,{stroke:PC.guide,w:1.6,dash:'5 4'});
    var inside=cog>=fb-14&&cog<=ff+14,ahead=cog>ff+14,front=inside&&cog>ff-10&&rv(h,'lean')>=10;
    var mg=(ff+14-cog)/11;
    out(h).innerHTML='무게중심에서 받침 앞 끝까지 <b>'+(mg<0?'−':'')+f2(Math.abs(mg),1)+'</b>(+ 받침 안, − 받침 밖, 눈금 11px = 1). '+
      (ahead?verdict(false,'받침 앞으로 나감 — 앞으로 넘어지는 그림. 앞발을 더 내디디면 달려 나가는 자세가 됩니다'):cog<fb-14?verdict(false,'받침 뒤로 나감 — 뒤로 넘어지는 그림'):front?verdict(true,'무게가 앞발에 실림 — 달려 나가는 자세(2컷)'):verdict(true,'받침 안 — 서 있거나 버티는 자세'));}
  allIn(h,draw);draw();};
P.p4_prop=function(h){var W=560,H=340;
  function draw(){var w=rv(h,'w'),d=rv(h,'d'),stiff=rv(h,'stiff');var s=svgOf(h,W,H);bg(s,W,H);var M=60,K=160,gy=310,x0=240;var off=w*d/M;var lean=stiff?0:Math.atan2(off*K,0.9*K);
    ln(s,20,gy,W-20,gy,{stroke:PC.soft,w:1.3});el('rect',{x:x0-30,y:gy-6,width:60,height:12,rx:4,fill:'rgba(19,115,58,.25)'},s);
    var pel=[x0-Math.sin(lean)*30,gy-140],T=115,nk=[pel[0]-Math.sin(lean)*T,pel[1]-Math.cos(lean)*T];
    pth(s,'M'+P2(pel[0],pel[1])+' Q'+P2(x0-14,gy-60)+' '+P2(x0-22,gy)+' M'+P2(pel[0],pel[1])+' Q'+P2(x0+18,gy-60)+' '+P2(x0+22,gy),{w:3});pth(s,'M'+P2(pel[0],pel[1])+' L'+P2(nk[0],nk[1]),{w:5});
    mhead(s,nk[0]-Math.sin(lean)*20,nk[1]-Math.cos(lean)*20,16,1,{w:2});var hx=x0+d*K*0.75,hy=nk[1]+70;pth(s,'M'+P2(nk[0],nk[1]+10)+' Q'+P2((nk[0]+hx)/2,nk[1]+40)+' '+P2(hx,hy),{w:2.6});
    var bs=Math.cbrt(w)*22;el('rect',{x:hx-4,y:hy-bs*0.6,width:bs,height:bs,fill:'#efe3cf',stroke:PC.ink,'stroke-width':2},s);
    var bodyX=stiff?x0:x0-off*K,cog=(M*bodyX+w*(hx+bs/2))/(M+w);el('circle',{cx:cog,cy:gy-150,r:6,fill:PC.guide},s);ln(s,cog,gy-150,cog,gy,{stroke:PC.guide,w:1.6,dash:'5 4'});
    var inside=Math.abs(cog-x0)<=30;
    out(h).innerHTML=f2(w,1)+'kg × '+f2(d,1)+'m = '+f2(w*d,2)+' → ÷ 몸무게 60 = 몸이 옮겨 갈 거리 <b>'+f2(off*100,1)+'cm</b>. '+(stiff?verdict(inside,inside?'가벼워서 곧게 서도 버팁니다':'곧게 서면 무게중심이 앞으로 나가 넘어질 듯합니다(6부 f5)'):verdict(true,'몸이 '+f2(off*100,1)+'cm 뒤로 기울어 무게가 보입니다'));}
  allIn(h,draw);draw();};
P.p4_exag=function(h){var W=560,H=330;
  function draw(){var ex=rv(h,'ex'),sil=rv(h,'sil');var s=svgOf(h,W,H);bg(s,W,H);ln(s,20,300,W-20,300,{stroke:PC.soft,w:1.3});el('rect',{x:420,y:50,width:60,height:250,fill:'#f4f6f8',stroke:PC.soft,'stroke-width':1.5},s);
    var bend=4+ex*0.26;var armA=20+ex*0.9;var collapse=Math.max(0,ex-80);
    axisFig(s,{x:260-collapse*1.2,top:60+collapse*1.5,bot:300,bend:bend,mode:collapse>0?'s':'c',sil:sil,armA:armA,spread:0.1+ex/180});
    var read=Math.min(100,10+ex*1.5),stab=100-collapse*4,score=Math.round(Math.min(read,stab));
    out(h).innerHTML='과장 '+ex+' · 실루엣 읽힘 <b>'+Math.round(read)+'</b> · 중심 안정 <b>'+Math.round(stab)+'</b> → 종합 <b>'+score+'</b>(예시 점수). '+
      verdict(ex>=40&&ex<=80,ex<40?'팔이 몸통에 묻혀 작은 그림에서 동작이 안 읽힙니다':ex>80?'중심축이 무너져 오히려 힘이 빠져 보입니다':'검게 칠해도 미는 동작이 읽히고 힘도 남아 있습니다');}
  allIn(h,draw);draw();};

/* ===================== 5부 AI로 컷 만들기 ===================== */
var CF={shot:[['','(고르기)'],['wide shot','원경'],['full body shot','전신'],['waist-up shot','허리 위'],['close-up','얼굴']],
 angle:[['','(고르기)'],['eye-level camera','눈높이'],['low angle shot looking up','앙각'],['high angle shot looking down','부감']],
 who:[['','(고르기)'],['haru','하루(고정값 포함)'],['haru_name','하루(이름만)']],
 act:[['','(고르기)'],['standing still and looking around','멈춰 두리번'],['running','달리기'],['walking','걷기'],['looking out a window','창밖 보기'],['lifting her head','고개 들기'],['climbing the stairs quickly','계단 오르기'],['pushing a heavy door with her whole body leaning forward','문 밀기']],
 dir:[['','(고르기)'],['toward the RIGHT side of the frame','화면 오른쪽으로'],['toward the UPPER RIGHT of the frame','화면 오른쪽 위로'],['away from the camera, seen from behind','뒷모습(안쪽으로)'],['facing the viewer','정면']],
 emo:[['','(고르기)'],['worried','걱정'],['in a hurry','서두름'],['tense','긴장'],['startled realization, eyes wide','깨달음'],['determined','결의'],['relieved, a new start','안도']],
 bg:[['','(고르기)'],['in front of a research institute building','연구소 앞'],['in a long bright corridor','복도'],['next to a large window','창가'],['in a bright stairwell','계단'],['on a wide rooftop under a big sky','옥상']],
 light:[['','(고르기)'],['afternoon sunlight from the left','오후 햇빛(왼쪽)'],['soft backlight from a window','창 역광'],['daylight from the top of the stairs','계단 위 빛']]};
var CFK=['shot','angle','who','act','dir','emo','bg','light'],CFN={shot:'샷 크기',angle:'앵글',who:'인물',act:'동작',dir:'방향',emo:'감정',bg:'배경',light:'빛'};
var HARU_FIX='Haru (adult lab assistant in her twenties, long straight pink hair with navy streaks, a thick navy streak down the center of the bangs, two round hair buns on top, big blue eyes), wearing a lavender hoodie under an open white lab coat';
var CUTP=[{shot:'wide shot',angle:'eye-level camera',who:'haru',act:'standing still and looking around',dir:'facing the viewer',emo:'worried',bg:'in front of a research institute building',light:'afternoon sunlight from the left'},
 {shot:'full body shot',angle:'eye-level camera',who:'haru',act:'running',dir:'toward the RIGHT side of the frame',emo:'in a hurry',bg:'in front of a research institute building',light:'afternoon sunlight from the left'},
 null,null,
 {shot:'close-up',angle:'eye-level camera',who:'haru',act:'lifting her head',dir:'toward the UPPER RIGHT of the frame',emo:'startled realization, eyes wide',bg:'next to a large window',light:'soft backlight from a window'},
 {shot:'full body shot',angle:'low angle shot looking up',who:'haru',act:'climbing the stairs quickly',dir:'toward the UPPER RIGHT of the frame',emo:'determined',bg:'in a bright stairwell',light:'daylight from the top of the stairs'},
 null,
 {shot:'wide shot',angle:'eye-level camera',who:'haru',act:'walking',dir:'away from the camera, seen from behind',emo:'relieved, a new start',bg:'on a wide rooftop under a big sky',light:'afternoon sunlight from the left'}];
function cutForm(box,onCh){var html='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:6px 10px;width:100%">';
  CFK.forEach(function(k){html+='<label style="display:flex;flex-direction:column;font-size:13px">'+CFN[k]+'<select name="'+k+'">'+CF[k].map(function(o){return '<option value="'+o[0]+'">'+o[1]+'</option>';}).join('')+'</select></label>';});
  box.insertAdjacentHTML('beforeend',html+'</div>');box.querySelectorAll('select').forEach(function(sel){if(CFK.indexOf(sel.name)>=0)sel.addEventListener('change',onCh);});
  function get(){var o={};CFK.forEach(function(k){o[k]=box.querySelector('select[name='+k+']').value;});return o;}
  function set(o){CFK.forEach(function(k){box.querySelector('select[name='+k+']').value=o[k]||'';});}
  return {get:get,set:set};}
function cutPrompt(o){var parts=[],miss=[],warn=[];CFK.forEach(function(k){if(!o[k])miss.push(CFN[k]);});
  if(o.shot)parts.push(o.shot.charAt(0).toUpperCase()+o.shot.slice(1)+(o.angle?', '+o.angle:'')+'.');else if(o.angle)parts.push(o.angle+'.');
  if(o.who)parts.push((o.who==='haru'?HARU_FIX:'Haru, a lab assistant')+(o.act?', '+o.act:'')+(o.dir?', '+o.dir:'')+'.');else if(o.act)parts.push('A character '+o.act+(o.dir?', '+o.dir:'')+'.');
  if(o.emo)parts.push('Emotion: '+o.emo+'.');if(o.bg)parts.push('Background: '+o.bg+'.');if(o.light)parts.push('Light: '+o.light+'.');
  parts.push('Anime illustration, adult proportions. No text, no letters, no numbers, no logos.');
  if(o.shot==='close-up'&&/running|climbing|walking|pushing/.test(o.act))warn.push('얼굴 샷인데 발·몸 동작을 골랐습니다 — 동작이 화면 밖으로 잘립니다.');
  if(o.shot==='wide shot'&&/startled/.test(o.emo))warn.push('원경인데 표정이 중요한 감정입니다 — 얼굴이 작아 안 보입니다.');
  if(o.who==='haru_name')warn.push('이름만으로는 컷마다 캐릭터가 바뀝니다 — 고정값을 넣으세요(5부 2단계).');
  if(o.dir==='facing the viewer'&&/running|climbing/.test(o.act))warn.push('정면으로 달리거나 오르면 앞뒤 컷과 방향이 이어지는지 확인하세요(3부 1단계).');
  var score=8-miss.length-(o.who==='haru_name'?1:0);return {text:parts.join('\n'),score:Math.max(0,score),miss:miss,warn:warn};}
P.p5_prompt=function(h){h.innerHTML='';var F=cutForm(h,draw);var pb=document.createElement('div');pb.className='promptbox';pb.innerHTML='<b>조립된 컷 문장</b><pre aria-live="polite"></pre><button type="button" class="btn">복사하기</button>';h.appendChild(pb);
  var ps=pick(h,'[name=preset]');ps.addEventListener('change',function(){var v=ps.value;if(v!=='')F.set(CUTP[+v]);draw();});
  pb.querySelector('button').addEventListener('click',function(){var t=pb.querySelector('pre').textContent;var b=pb.querySelector('button');if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent='복사했습니다';},function(){b.textContent='직접 선택해 복사하세요';});});
  function draw(){var r=cutPrompt(F.get());pb.querySelector('pre').textContent=r.text;
    out(h).innerHTML='점검표 <b>'+r.score+' / 8</b>'+(r.miss.length?' · 빠진 조각: '+r.miss.join(', '):'')+'. '+(r.warn.length?verdict(false,r.warn[0]):verdict(r.score===8,r.score===8?'여덟 조각이 서로 맞습니다':'조각을 더 채워 보세요'));}
  draw();};
P.p5_anchor=function(h){var W=560,H=240,seed=3;seg2(h,function(){seed++;draw();});
  function draw(){var a=[rv(h,'a0'),rv(h,'a1'),rv(h,'a2'),rv(h,'a3')];var p=0.80+(a[0]?0.12:0)+(a[1]?0.05:0)+(a[2]?0.015:0)+(a[3]?0.01:0);p=Math.min(p,0.995);
    var s=svgOf(h,W,H);bg(s,W,H);var r=rng(seed*97+Math.round(p*1000));var okN=0;
    for(var i=0;i<8;i++){var ok=r()<p;if(ok)okN++;var x=40+i*66,y=90;var col=ok?'#e86aa6':'#e8a27a';
      el('circle',{cx:x-14,cy:y-34,r:ok?9:0.1,fill:col,stroke:PC.ink,'stroke-width':1.4},s);el('circle',{cx:x+14,cy:y-34,r:ok?9:5,fill:col,stroke:PC.ink,'stroke-width':1.4,opacity:ok?1:0.5},s);
      el('circle',{cx:x,cy:y,r:26,fill:'#fff',stroke:PC.ink,'stroke-width':1.6},s);pth(s,'M'+P2(x-26,y-4)+' Q'+P2(x,y-40)+' '+P2(x+26,y-4),{fill:col,stroke:PC.ink,w:1.4});
      ln(s,ok?x:x+12,y-28,ok?x:x+15,y-8,{stroke:'#1e2f6e',w:4});el('circle',{cx:x-8,cy:y+6,r:3,fill:'#2458d6'},s);el('circle',{cx:x+8,cy:y+6,r:3,fill:'#2458d6'},s);
      ktxt(s,x,y+46,(i+1)+'컷',{size:11.5,anchor:'middle',fill:C.ink});ktxt(s,x,y+64,ok?'맞음':'바뀜',{size:11.5,anchor:'middle',fill:ok?C.green:C.red,weight:'bold'});}
    ktxt(s,20,200,'이번에 뽑힌 결과: 여덟 장 중 '+okN+'장이 고정값을 지킴 (다시 뽑기로 여러 번 해 보세요)',{size:12.5});
    out(h).innerHTML='한 장 맞을 확률 <b>'+f2(p,3)+'</b>(예시값) → 여덟 장 모두 맞을 확률 '+f2(p,3)+'⁸ ≈ <b>'+f2(Math.pow(p,8),2)+'</b>. '+verdict(Math.pow(p,8)>=0.7,Math.pow(p,8)>=0.7?'여덟 장이 한 사람으로 이어질 가능성이 높습니다':'여덟 장 중 몇 장은 다른 사람처럼 나오기 쉽습니다');}
  allIn(h,draw);draw();};
P.p5_strength=function(h){var W=560,H=280;
  function draw(){var st=rv(h,'s'),N=rv(h,'steps');var s=svgOf(h,W,H);bg(s,W,H);var Y=40,FW=250,FH=FW*9/16;
    [[20,'밑그림(썸네일)'],[290,'결과']].forEach(function(q){frame(s,q[0],Y,FW,FH);ktxt(s,q[0],Y-10,q[1],{size:12.5,fill:C.ink,weight:'bold'});});
    var g=clipTo(s,20,Y,FW,FH);el('rect',{x:20+FW*0.66,y:Y+FH*0.05,width:FW*0.26,height:FH*0.95,fill:'none',stroke:PC.soft},g);fig(g,{x:20+FW*0.4,y:Y+FH*1.45,h:FH*1.35,dir:1,pose:'push'});
    var g2=clipTo(s,290,Y,FW,FH);var drift=Math.max(0,(st-0.6)/0.4);var X=290;
    el('rect',{x:X,y:Y,width:FW,height:FH,fill:mix('#ffffff','#eef3fb',st)},g2);el('rect',{x:X+FW*(0.66-drift*0.3),y:Y+FH*0.05,width:FW*0.26,height:FH*0.95,fill:mix('#ffffff','#c9d6e6',st),stroke:mix('#9aa5b1','#4a5a70',st)},g2);
    var fx=X+FW*(0.4+drift*0.12),pose=drift>0.5?'stand':'push',dir=drift>0.75?0:1;
    var fg=fig(g2,{x:fx,y:Y+FH*(1.45+drift*0.1),h:FH*(1.35-drift*0.25),dir:dir,pose:pose,stroke:mix('#9aa5b1','#2a2230',st),w:1.6+st*1.6});
    if(st<0.3){var rr=rng(5);for(var k=0;k<30;k++){ln(g2,X+FW*rr(),Y+FH*rr(),X+FW*rr()*1.02,Y+FH*rr()*1.02,{stroke:'#b8c0ca',w:0.6,op:0.6*(1-st/0.3)});}}
    var steps=N*st;var ok=st>=0.35&&st<=0.6;
    out(h).innerHTML='강도 '+f2(st,2)+' × '+N+'단계 = 다시 그리는 단계 <b>'+f2(steps,1)+'</b>(앞쪽 '+f2(N-steps,1)+'단계 몫인 큰 구도는 밑그림을 따름). '+
      verdict(ok,st<0.35?'연필선과 거친 질감이 남습니다':st>0.6?(st>0.8?'구도까지 새로 그려 인물이 가운데로 옮겨 갑니다':'구도가 조금씩 흔들리기 시작합니다'):'구도는 그대로, 그림은 깨끗하게');}
  allIn(h,draw);draw();};
P.p5_batch=function(h){var W=560,H=280,m='key';seg2(h,function(v){m=v;draw();});
  var SC={sheet:['한 장에 여덟 컷',8,3,'높음'],each:['새 대화에서 따로따로',4,8,'낮음'],key:['기준 컷 먼저 + 이어 만들기',8,8,'낮음']};
  function draw(){var n=rv(h,'fix');var s=svgOf(h,W,H);bg(s,W,H);var keys=['sheet','each','key'];
    keys.forEach(function(k,i){var y=24+i*84,on=k===m;ktxt(s,20,y,SC[k][0],{size:13,fill:on?C.orange:C.ink,weight:on?'bold':'normal'});
      var redo=k==='sheet'?(n>0?8:0):n;ktxt(s,540,y,'다시 만드는 그림 '+redo+'장',{size:12,anchor:'end',fill:on?C.orange:C.muted});
      [['일관성',SC[k][1]],['컷별 제어',SC[k][2]]].forEach(function(q,j){var yy=y+14+j*24;el('rect',{x:110,y:yy,width:40*q[1],height:16,rx:4,fill:on?C.teal:'#c9d6e0'},s);ktxt(s,102,yy+12,q[0],{size:11.5,anchor:'end'});ktxt(s,116+40*q[1],yy+12,String(q[1]),{size:11.5});});});
    var redo=m==='sheet'?(n>0?8:0):n;
    out(h).innerHTML=SC[m][0]+' · 고칠 컷 '+n+'개 → 다시 만드는 그림 <b>'+redo+'장</b>, 맞았던 컷이 틀어질 위험 <b>'+SC[m][3]+'</b>(예시 점수). '+
      verdict(m==='key',m==='key'?'일관성과 컷별 제어를 함께 지키고 틀린 컷만 고칩니다':m==='sheet'?'한 컷만 고치려 해도 여덟 컷 전체를 다시 만들어야 합니다':'컷은 정확하지만 캐릭터가 컷마다 흔들립니다');}
  allIn(h,draw);draw();};

/* ===================== 6부 진단 ===================== */
var CHECK6=['① 이야기(컷의 목적)','② 카메라(샷·눈높이·여백)','③ 흐름(방향·시선·빛)','④ 포즈(중심축·무게)','⑤ 고정값(캐릭터·나이)'];
var FAIL6=[0,2,1,1,3,4,1,2];var FAILWHY6=['여러 컷의 목적이 같아 그림도 같습니다.','카메라가 가상선을 넘어 방향이 뒤집혔습니다.','먼 사람의 크기를 거리만큼 줄이지 않았습니다.','눈높이 선이 사람마다 다른 곳을 지나 한 사람이 떠 있습니다.','몸의 중심축이 곧아 무게가 보이지 않습니다.','고정값이 컷마다 달라 다른 사람처럼 보입니다.','바라보는 쪽에 여백이 없어 시선이 막혔습니다.','컷마다 빛의 방향이 바뀌었습니다.'];
P.p6_check=function(h){var c=ctl(h),sel=c.querySelector('select');h.innerHTML='';var list=document.createElement('div');list.style.cssText='display:flex;flex-direction:column;gap:6px';h.appendChild(list);var done=0;
  function build(){list.innerHTML='';done=0;CHECK6.forEach(function(t,i){var b=document.createElement('button');b.type='button';b.className='btn';b.style.textAlign='left';b.textContent=t;b.addEventListener('click',function(){press(i,b);});list.appendChild(b);});out(h).innerHTML='점검표를 <b>위에서부터</b> 눌러 보세요.';}
  function press(i,b){var f=+sel.value,at=FAIL6[f];if(i!==done){out(h).innerHTML='순서대로! 먼저 <b>'+CHECK6[done]+'</b>을 보세요. 이야기에서 고정값 순서입니다.';return;}
    if(i<at){b.style.borderColor=C.green;b.style.background='#ecf7ef';b.textContent=CHECK6[i]+' — 통과';done++;out(h).innerHTML=CHECK6[i]+' 통과. 다음 항목으로.';}
    else{b.style.borderColor=C.red;b.style.background='#fdeceb';b.textContent=CHECK6[i]+' — 여기서 걸림';done=99;out(h).innerHTML='<b>'+CHECK6[i]+'</b>에서 처음 걸렸습니다: '+FAILWHY6[f]+' 아래 실패 카드 f'+(f+1)+'에서 고치는 조각을 보세요.';}}
  sel.addEventListener('change',build);build();};

/* ===================== 실전 연습장 ===================== */
function practice(){tpl();var root=document.getElementById('practice');if(!root)return;var tabs=root.querySelectorAll('.tabs button'),scenes=root.querySelectorAll('.scene');
  function show(id){tabs.forEach(function(b){b.classList.toggle('on',b.dataset.t===id);});scenes.forEach(function(s){s.classList.toggle('on',s.id===id);});if(history.replaceState)history.replaceState(null,'','#'+id);}
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});var hsh=(location.hash||'').slice(1);show([].some.call(scenes,function(s){return s.id===hsh;})?hsh:'bench');
  bench();camera();workshop();desk();}
function wire(S,f){S.querySelectorAll('.ctrl input,.ctrl select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
function bench(){var S=document.getElementById('bench');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var touched=false;
  function upd(e){if(e)touched=true;var tgt=+q('len').value,v=[+q('a').value,+q('b').value,+q('c').value,+q('d').value],pk=+q('peak').value,sec=+q('sec').value,first=q('first').value;var tot=v[0]+v[1]+v[2]+v[3];
    var okSum=tot===8&&v.every(function(x){return x>=1;}),okPk=pk===6||pk===7,okLen=Math.abs(tot*sec-tgt)<0.01,okFirst=first==='ls';
    board(S.querySelector('.board'),[['합계',tot+' / 8컷',okSum],['절정',pk+'컷',okPk],['장면 길이',f2(tot*sec,1)+' / '+tgt+'초',okLen],['첫 컷',{ls:'원경',fs:'전신',cu:'얼굴'}[first],okFirst]]);
    var s=el('svg',{viewBox:'0 0 430 300',role:'img','aria-label':'콘티 작업대 여덟 컷'});var g1=S.querySelector('.g1');g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:430,height:300,fill:'#fbfcfd'},s);
    var k=0;for(var b=0;b<4;b++)for(var j=0;j<v[b];j++){if(k<12){var X=10+(k%4)*104,Y=14+Math.floor(k/4)*92;el('rect',{x:X,y:Y,width:96,height:54,rx:5,fill:k>=8?'#fdeceb':mix(BEAT[b][1],'#ffffff',0.8),stroke:k>=8?C.red:BEAT[b][1],'stroke-width':k+1===pk?3.4:1.6},s);if(k<8)drawCutMini(s,k,X+4,Y+4,88,46,k===0?first:null);ktxt(s,X+48,Y+70,(k+1)+'컷 '+(k>=8?'넘침':BEAT[b][0])+(k+1===pk?' ★':''),{size:11,anchor:'middle',fill:C.ink});}k++;}
    var s2=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'감정 곡선'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s2);var pts=[];for(var i=0;i<8;i++){var e=i+1===pk?9:Math.max(2,9-Math.abs(i+1-pk)*1.6+(i===pk-2?-2:0));pts.push(P2(30+i*42,170-e*16));el('circle',{cx:30+i*42,cy:170-e*16,r:i+1===pk?6:4,fill:i+1===pk?C.orange:C.navy},s2);ktxt(s2,30+i*42,192,String(i+1),{size:11,anchor:'middle'});}
    pth(s2,'M'+pts.join(' L'),{stroke:C.navy,w:2});
    var M=[okSum,okPk&&okSum,okLen&&okFirst&&okSum];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','목표 장면 '+tgt+'초. 여덟 컷 × 한 컷 '+f2(sec,1)+'초 = '+f2(tot*sec,1)+'초.'],['moa','e10','모아',okSum?'네 덩어리가 다 있어요.':'비어 있는 덩어리가 있거나 여덟 컷이 아니에요.'],['fruitfly','e09','초파리',okPk?'절정이 끝 바로 앞이야.':'절정은 6~7컷에 두자.']]);}
  wire(S,upd);upd();}
function drawCutMini(s,i,X,Y,W,H,first){var k=i;if(i===0&&first&&first!=='ls'){var g=clipTo(s,X,Y,W,H);el('rect',{x:X,y:Y,width:W,height:H,fill:'#fff'},g);if(first==='cu')mhead(g,X+W/2,Y+H*0.6,H*0.38,0,{});else fig(g,{x:X+W/2,y:Y+H*0.92,h:H*0.8,dir:0});frame(s,X,Y,W,H,{fill:'none',w:1});return;}drawCut(s,k,X,Y,W,H,{num:false,bw:1});}
var CAM_T={c1:['1컷 장소 소개',{shot:'0',cam:'eye',face:'any',x:'any'}],c4:['4컷 창밖 보기',{shot:'3',cam:'eye',face:'r',x:'left'}],c5:['5컷 깨달음',{shot:'5',cam:'eye',face:'r',x:'any'}],c6:['6컷 결의',{shot:'1',cam:'low',face:'r',x:'any'}]};
function camera(){var S=document.getElementById('camera');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var touched=false,hit={};
  function upd(e){if(e)touched=true;var tk=q('target').value,T=CAM_T[tk][1];var o={shot:q('shot').value,cam:q('cam').value,face:q('face').value,x:+q('x').value};
    var xr=o.x<=40?'left':o.x>=60?'right':'mid';var ok={shot:o.shot===T.shot,cam:o.cam===T.cam,face:T.face==='any'||o.face===T.face,x:T.x==='any'||xr===T.x};var n=Object.keys(ok).filter(function(k){return ok[k];}).length;if(n===4&&touched)hit[tk]=1;
    board(S.querySelector('.board'),[['샷',SHOTS[+o.shot][0],ok.shot],['앵글',{eye:'눈높이',low:'앙각',high:'부감'}[o.cam],ok.cam],['바라보는 쪽',o.face==='r'?'오른쪽':'왼쪽',ok.face],['자리',o.x+'%',ok.x]]);
    var s=el('svg',{viewBox:'0 0 430 260',role:'img','aria-label':'카메라 화면'});var g1=S.querySelector('.g1');g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:430,height:260,fill:'#fbfcfd'},s);
    var X=15,Y=15,FW=400,FH=225;var g=clipTo(s,X,Y,FW,FH);el('rect',{x:X,y:Y,width:FW,height:FH,fill:'#fff'},g);var camv={eye:0,low:-35,high:35}[o.cam];var hz=Y+FH/2-camv*1.6;ln(g,X,hz,X+FW,hz,{stroke:PC.guide,w:1.4,dash:'6 4'});
    [1,2].forEach(function(k){ln(g,X+FW*k/3,Y,X+FW*k/3,Y+FH,{stroke:'#d5dbe2',w:1,dash:'4 4'});});
    var heads=SHOTS[+o.shot][1],hp=FH/heads,fh=7.5*hp*(1-camv/250);var top=Y+hp*(+o.shot===0?heads*0.55:0.6);fig(g,{x:X+FW*o.x/100,y:top+fh,h:fh,dir:o.face==='r'?1:-1,pose:o.cam==='low'?'climb':'look',w:Math.max(1.4,Math.min(4,fh/90)),up:tk==='c5'?0.6:0});
    frame(s,X,Y,FW,FH,{fill:'none',w:2});
    var s2=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'촬영 목표 네 가지'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s2);
    Object.keys(CAM_T).forEach(function(k,i){el('rect',{x:16+i*86,y:40,width:78,height:90,rx:8,fill:hit[k]?'#e8f6ec':'#f2f4f7',stroke:hit[k]?C.green:'#d5dbe2'},s2);ktxt(s2,55+i*86,82,CAM_T[k][0].split(' ')[0]+(hit[k]?' ✓':''),{size:12,anchor:'middle',fill:C.ink});ktxt(s2,55+i*86,100,CAM_T[k][0].split(' ').slice(1).join(' '),{size:10.5,anchor:'middle'});});
    var M=[!!hit.c4,!!hit.c6,Object.keys(hit).length===4];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','목표: '+CAM_T[tk][0]+'. 맞은 항목 '+n+' / 4.'],['haru','e10','하루',ok.shot?'샷 크기가 맞았어요.':'이 컷의 목적에 맞는 샷 크기부터 골라 봐요(2부 1단계).'],['jupanbot','e16','주판봇',n===4?'완벽한 한 컷입니다!':'전신·한가운데가 늘 정답은 아니군요…']]);}
  wire(S,upd);upd();}
function workshop(){var S=document.getElementById('workshop');if(!S)return;var touched=false;var F=cutForm(S.querySelector('.ow'),function(){touched=true;upd();});var job=S.querySelector('[name=job]');job.addEventListener('change',function(){touched=true;upd();});var hit5=false,hit6=false;
  function upd(){var o=F.get();var r=cutPrompt(o);S.querySelector('.g1 pre').textContent=r.text;var need={key:['who','emo','shot'],next:['dir','act','light'],wide:['bg','shot']}[job.value];var jobOk=need.every(function(k){return o[k];})&&(job.value!=='key'||o.who==='haru')&&(job.value!=='wide'||o.shot==='wide shot');
    if(touched&&o.shot==='close-up'&&o.angle==='eye-level camera'&&/startled/.test(o.emo)&&/UPPER RIGHT/.test(o.dir)&&o.who==='haru')hit5=true;
    if(touched&&o.shot==='full body shot'&&/low angle/.test(o.angle)&&/climbing/.test(o.act)&&/UPPER RIGHT/.test(o.dir)&&o.emo==='determined'&&o.who==='haru')hit6=true;
    board(S.querySelector('.board'),[['점검표',r.score+' / 8',r.score===8],['요청 상황 맞춤',jobOk?'맞음':'부족',jobOk],['충돌 경고',r.warn.length+'개',r.warn.length===0],['5컷·6컷',(hit5?'5✓ ':'5 · ')+(hit6?'6✓':'6'),hit5&&hit6]]);
    var s=el('svg',{viewBox:'0 0 360 260',role:'img','aria-label':'점검표 막대'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s);CFK.forEach(function(k,i){var ok=!!o[k];el('rect',{x:76,y:14+i*30,width:ok?260:40,height:20,rx:4,fill:ok?C.teal:'#e3e8ee'},s);ktxt(s,70,29+i*30,CFN[k],{size:12.5,anchor:'end',fill:C.ink});});
    var M=[r.score===8&&r.warn.length===0,hit5,hit6];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','요청 상황: '+job.options[job.selectedIndex].text+'. '+(jobOk?'필요한 조각이 들어 있다.':'이 상황에 꼭 필요한 조각이 빠졌다.')],['haru','e10','하루','점검표 '+r.score+' / 8'+(r.miss.length?', 빠진 것: '+r.miss.join(', '):'!')],['fruitfly','e09','초파리',r.warn.length?r.warn[0]:'충돌 없음. 조각이 서로 맞아.']]);}
  var cp=S.querySelector('.copy');if(cp)cp.addEventListener('click',function(){var t=S.querySelector('.g1 pre').textContent;if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){cp.textContent='복사했습니다';},function(){cp.textContent='직접 선택해 복사하세요';});});upd();}
var DESK_CA=['컷의 목적이 같음','가상선을 넘음','거리만큼 줄이지 않음','눈높이 선 불일치','중심축이 곧음','고정값이 바뀜','시선 여백 없음','빛 방향이 바뀜'];
var DESK_SYM=['둘째부터 넷째 컷이 같은 크기·같은 자세라 이야기가 앞으로 가지 않는다','오른쪽으로 걷던 인물이 다음 컷에서 왼쪽으로 걸어 되돌아가는 것 같다','복도 끝 멀리 있는 사람이 앞사람만큼 커서 거인 같다','같은 바닥에 선 사람 중 한 명이 공중에 떠 보인다','무거운 문을 민다는데 몸은 차렷이고 팔만 뻗었다','같은 인물인데 컷마다 머리 장식과 옷 색이 다르다','오른쪽을 보는 인물이 화면 오른쪽 끝에 붙어 답답하다','같은 시각 같은 복도인데 컷마다 그림자 방향이 반대다'];
function desk(){var S=document.getElementById('desk');if(!S)return;var CA=DESK_CA,SYM=DESK_SYM;
  var cur=0,streak=0,seen={},wrong=0,right=0,touched=false;var r=rng(Date.now()%9999+1);
  function next(){cur=Math.floor(r()*8);S.querySelector('.sym').textContent='증상: '+SYM[cur];var o=S.querySelector('.deskopts');o.innerHTML='';
    var opts=[cur];while(opts.length<4){var k=Math.floor(r()*8);if(opts.indexOf(k)<0)opts.push(k);}opts.sort(function(){return r()-.5;});
    opts.forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=CA[k];b.addEventListener('click',function(){touched=true;if(k===cur){streak++;right++;seen[cur]=1;b.classList.add('ok');setTimeout(next,500);}else{streak=0;wrong++;b.classList.add('no');}upd();});o.appendChild(b);});}
  function upd(){var n=Object.keys(seen).length;board(S.querySelector('.board'),[['연속 정답',streak,streak>=3],['맞힌 종류',n+' / 8',n===8],['맞힘',right,right>0],['틀림',wrong,wrong===0]]);
    var M=[streak>=3,n===8,right>=5&&wrong===0];if(touched)missions(S.querySelector('.missions'),M,true);
    var s=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'맞힌 실패 종류'});var g=S.querySelector('.g2');g.innerHTML='';g.appendChild(s);CA.forEach(function(t,i){el('rect',{x:16+(i%4)*86,y:20+Math.floor(i/4)*90,width:78,height:70,rx:8,fill:seen[i]?'#e8f6ec':'#f2f4f7',stroke:seen[i]?C.green:'#d5dbe2'},s);ktxt(s,55+(i%4)*86,60+Math.floor(i/4)*90,'f'+(i+1)+(seen[i]?' ✓':''),{size:14,anchor:'middle',fill:C.ink});});
    say(S.querySelector('.talk'),[['doctor','e10','박사','순서: 이야기 → 카메라 → 흐름 → 포즈 → 고정값.'],['sia','e10','시아','연속 '+streak+'개, 맞힌 종류 '+n+' / 8이에요.'],['x2','e09','평가단 X2',wrong?'틀린 건 6부 실패 카드에서 다시 보세요.':'아직 틀린 게 없어요!']]);}
  next();upd();}
/* 빈 콘티 양식 (practice/template.html) */
function tpl(){var T=document.getElementById('tpl');if(!T)return;var sheet=T.querySelector('.tsheet');var mode='blank';
  function render(){sheet.innerHTML='';for(var i=0;i<8;i++){var d=document.createElement('div');d.className='tcut';
      var svg=el('svg',{viewBox:'0 0 320 180',role:'img','aria-label':'컷 '+(i+1)+' 그림 자리'});el('rect',{x:0,y:0,width:320,height:180,fill:'#fff'},svg);
      if(mode==='sample')drawCut(svg,i,0,0,320,180,{bw:2});else{el('rect',{x:1,y:1,width:318,height:178,fill:'#fff',stroke:'#3a3f47','stroke-width':2},svg);ktxt(svg,8,18,'CUT '+(i+1),{size:13,fill:'#9aa5b1'});}
      d.appendChild(svg);var labs=['목적','흐름·동작','감정·보충'];var rows=labs.map(function(l,k){return '<div class="trow"><b>'+l+'</b><span>'+(mode==='sample'?CUT_TXT[i][k]:'')+'</span></div>';}).join('');
      d.insertAdjacentHTML('beforeend',rows+'<div class="trow small"><b>샷·길이</b><span>'+(mode==='sample'?CUT_SHOT[i]+' · '+DUR[i]+'초':'')+'</span></div>');sheet.appendChild(d);}}
  T.querySelectorAll('[data-mode]').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.mode;T.querySelectorAll('[data-mode]').forEach(function(x){x.classList.toggle('on',x===b);});
    var f=T.querySelector('.thead');f.querySelectorAll('[data-sample]').forEach(function(x){x.textContent=mode==='sample'?x.dataset.sample:'';});render();});});
  var pr=T.querySelector('[data-print]');if(pr)pr.addEventListener('click',function(){window.print();});render();}
/* 프롬프트 복사 버튼(직접 만들기 실습) */
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.promptbox .copy');if(!b||b.closest('#workshop'))return;var pre=b.parentNode.querySelector('pre');if(!pre)return;var t=pre.textContent;
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent='복사했습니다';},function(){b.textContent='직접 선택해 복사하세요';});else b.textContent='직접 선택해 복사하세요';});
/* ===================== 퀴즈·지식 색인·꾸러미 ===================== */
function quiz(q){var ans=+q.getAttribute('data-ans');var fb=q.querySelector('.fb');var OK=q.querySelector('.qok'),NO=q.querySelector('.qno');q.querySelectorAll('.opts button').forEach(function(b,i){b.addEventListener('click',function(){q.querySelectorAll('.opts button').forEach(function(x){x.classList.remove('ok','no');});b.classList.add(i===ans?'ok':'no');fb.innerHTML=i===ans?'⭕ '+OK.innerHTML:'❌ '+NO.innerHTML;});});}
function kg(){var raw=document.getElementById('kg-raw');var mount=document.getElementById('kg-mount');if(!raw||!mount)return;var K=JSON.parse(raw.textContent);
  mount.innerHTML='<input class="kg-search" type="search"><div class="kg-list"></div>';var list=mount.querySelector('.kg-list'),inp=mount.querySelector('input');inp.placeholder='개념 찾기 (예: 샷, 가상선, 중심축)';inp.setAttribute('aria-label','지식 색인 검색');
  var TY={Concept:'개념',Method:'방법',Analogy:'비유',Application:'쓰임',OpenQuestion:'열린 질문'};var pre=document.body.getAttribute('data-root')||'';
  function render(){var qv=inp.value.trim().toLowerCase();list.innerHTML=K.nodes.filter(function(n){return !qv||(n.label.ko+' '+n.label.en+' '+n.definition.ko).toLowerCase().indexOf(qv)>=0;}).map(function(n){
    var nb=K.edges.filter(function(e){return e.s===n.id||e.o===n.id;}).map(function(e){var o=e.s===n.id?e.o:e.s;var m=K.nodes.filter(function(x){return x.id===o;})[0];return m?m.label.ko:'';}).filter(Boolean);
    return '<div class="kg-item"><span class="t">'+(TY[n.type]||n.type)+'</span><b>'+n.label.ko+'</b><span class="muted">'+n.label.en+'</span><div>'+n.definition.ko+'</div>'+(nb.length?'<div class="muted" style="font-size:12.5px">이웃: '+nb.join(', ')+'</div>':'')+'<a href="'+pre+n.page+n.anchor+'">설명 보러 가기 →</a></div>';}).join('');}
  inp.addEventListener('input',render);render();var ex=document.getElementById('export-mount');if(!ex)return;
  ex.innerHTML='<div class="exp-btns"><button class="btn" data-x="json">kg.json</button><button class="btn" data-x="ld">JSON-LD</button><button class="btn" data-x="ttl">Turtle (Protégé)</button><button class="btn" data-x="csv">CSV (Neo4j·Gephi)</button><button class="btn" data-x="bib">BibTeX</button><button class="btn" data-x="ris">RIS</button></div>';
  function dl(name,text,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
  var base=K.page;var refs=JSON.parse((document.getElementById('refs-csl')||{textContent:'[]'}).textContent);
  ex.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){var x=b.getAttribute('data-x');
    if(x==='json')dl(base+'.kg.json',JSON.stringify(K,null,2),'application/json');
    if(x==='ld')dl(base+'.jsonld',document.getElementById('kg-ld').textContent,'application/ld+json');
    if(x==='ttl'){var t='@prefix lab: <urn:lab:> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n';K.nodes.forEach(function(n){t+='<urn:'+n.id+'> a lab:'+n.type+' ;\n  skos:prefLabel "'+n.label.ko+'"@ko , "'+n.label.en+'"@en ;\n  rdfs:comment "'+n.definition.ko.replace(/"/g,'\\"')+'"@ko .\n\n';});K.edges.forEach(function(e){t+='<urn:'+e.s+'> lab:'+e.p+' <urn:'+e.o+'> .\n';});dl(base+'.ttl',t,'text/turtle');}
    if(x==='csv'){var c='id,type,label_ko,label_en,anchor\n'+K.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.page+n.anchor].map(function(v){return '"'+String(v).replace(/"/g,'""')+'"';}).join(',');}).join('\n');c+='\n\nsource,relation,target\n'+K.edges.map(function(e){return [e.s,e.p,e.o].join(',');}).join('\n');dl(base+'.csv',c,'text/csv');}
    if(x==='bib')dl(base+'.bib',refs.map(function(r){return '@misc{'+r.id+',\n  title = {'+r.title+'},\n  author = {'+r.author+'},\n  note = {'+(r.note||'')+'},\n  year = {'+r.year+'}\n}';}).join('\n\n'));
    if(x==='ris')dl(base+'.ris',refs.map(function(r){return 'TY  - GEN\nTI  - '+r.title+'\nAU  - '+r.author+'\nPY  - '+r.year+'\nN1  - '+(r.note||'')+'\nER  - ';}).join('\n'));});});}

function boot(){document.querySelectorAll('[data-panel]').forEach(function(h){var k=h.getAttribute('data-panel');if(P[k]){try{P[k](h);}catch(e){h.textContent='실험을 불러오지 못했습니다.';if(window.console)console.warn(k,e);}}});
  document.querySelectorAll('.quiz').forEach(quiz);kg();practice();
  var pr=document.getElementById('prog');if(pr)window.addEventListener('scroll',function(){var d=document.documentElement;pr.style.width=(100*d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
