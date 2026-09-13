
(function(){
var deck=document.getElementById('deck');var slides=[].slice.call(document.querySelectorAll('.slide'));
var n=slides.length,i=0;var prog=document.getElementById('prog');
var cnt=document.createElement('div');cnt.style.cssText='position:fixed;left:50%;transform:translateX(-50%);bottom:10px;z-index:30;font-family:JetBrains Mono;font-size:16px;color:#9A9A94';document.body.appendChild(cnt);
var nav=document.createElement('div');nav.style.cssText='position:fixed;right:24px;bottom:24px;z-index:30;display:flex;gap:8px';
nav.innerHTML='<button id="pv">‹</button><button id="nx">›</button>';
[].forEach.call(nav.querySelectorAll('button'),function(b){b.style.cssText='width:44px;height:44px;border:1.5px solid #111;border-radius:999px;background:#fff;color:#111;font-size:20px;cursor:pointer';});
document.body.appendChild(nav);
var inits={};var raf=null;function stopAnim(){if(raf){cancelAnimationFrame(raf);raf=null;}}
function fit(){var s=Math.min(window.innerWidth/1920,window.innerHeight/1080);if(!(s>0)||!isFinite(s))s=1;deck.style.transform='scale('+s+')';}
function show(k){i=(k+n)%n;stopAnim();slides.forEach(function(s,j){s.classList.toggle('on',j===i)});prog.style.width=(i/(n-1)*100)+'%';cnt.textContent=(i+1)+' / '+n;var key=slides[i].dataset.init;if(key&&inits[key])inits[key](slides[i]);}
window.showId=function(id){var el=document.getElementById(id);if(el)show(slides.indexOf(el));};
window.addEventListener('resize',fit);window.addEventListener('load',fit);if(window.ResizeObserver)new ResizeObserver(fit).observe(document.documentElement);
nav.querySelector('#nx').onclick=function(){show(i+1)};nav.querySelector('#pv').onclick=function(){show(i-1)};
addEventListener('keydown',function(e){var t=e.target.tagName;if(t==='INPUT'||t==='BUTTON'){if(e.key===' ')return;}
 if(['ArrowRight',' ','PageDown'].indexOf(e.key)>=0){e.preventDefault();show(i+1);}else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();show(i-1);}
 else if(e.key==='Home')show(0);else if(e.key==='End')show(n-1);else if(e.key==='f'||e.key==='F'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen();}});
var x0=null;addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>60)show(i+(dx<0?1:-1));x0=null;});
var W=[128,64,32,16,8,4,2,1];
var SVGNS="http://www.w3.org/2000/svg";
function svgEl(t,at){var e=document.createElementNS(SVGNS,t);for(var k in at)e.setAttribute(k,at[k]);return e;}
function node(x,y,lab,active){return '<g><rect x="'+(x-46)+'" y="'+(y-34)+'" width="92" height="68" rx="12" fill="'+(active?'#111':'#fff')+'" stroke="#111" stroke-width="2"/><text x="'+x+'" y="'+(y+6)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="18" fill="'+(active?'#fff':'#111')+'">'+lab+'</text></g>';}
function animPackets(svg,pkts){stopAnim();var t0=performance.now();
 function frame(now){var dt=(now-t0)/1000;var g=svg.querySelector('#pk');if(!g){g=svgEl('g',{id:'pk'});svg.appendChild(g);}g.innerHTML='';var alive=false;
  pkts.forEach(function(p){var f=((dt*p.sp)+(p.off||0));if(f<0)return;if(f>1){if(p.loop){f=f%1;}else return;}alive=true;var x=p.a[0]+(p.b[0]-p.a[0])*f,y=p.a[1]+(p.b[1]-p.a[1])*f;var c=svgEl('circle',{cx:x,cy:y,r:11,fill:p.col||'#FF5A1F'});g.appendChild(c);});
  raf=requestAnimationFrame(frame);}
 raf=requestAnimationFrame(frame);}
/* ip helpers */
function toO(x){return [(x>>>24)&255,(x>>>16)&255,(x>>>8)&255,x&255];}
function ipS(x){var o=toO(x);return o[0]+'.'+o[1]+'.'+o[2]+'.'+o[3];}
function maskStr(p){var m=[0,0,0,0];for(var k=0;k<32;k++){if(k<p)m[(k/8)|0]|=(1<<(7-k%8));}return m.join('.');}
/* ---- auto bit-row renderer: <div class="bitauto" data-oct="11000000" data-net="1"></div> ---- */
function renderBits(root){[].forEach.call((root||document).querySelectorAll('.bitauto'),function(el){
  if(el.dataset.done)return;el.dataset.done='1';
  var oct=el.dataset.oct||'00000000';var net=+(el.dataset.net||0);var sm=el.classList.contains('smb');
  var s='<div class="bits'+(sm?' sm':'')+'">';
  for(var k=0;k<8;k++){var on=oct.charAt(k)==='1';var cls=(k<net)?'net':(on?'on':'');
    s+='<div class="bit '+cls+'"><div class="w">'+W[k]+'</div><div class="v">'+(on?1:0)+'</div></div>';}
  s+='</div>';el.innerHTML=s;});}

/* ===================== INTERACTIVES ===================== */

/* storm: broadcast domain with / without router */
inits.storm=function(sl){var svg=document.getElementById('stormSvg');var hasR=true;
 var R=[700,210],SWA=[430,210],SWB=[970,210],A=[[210,120],[210,310]],B=[[1190,120],[1190,310]];
 function draw(){var s='<rect x="70" y="70" width="560" height="290" rx="16" fill="#FF5A1F" opacity="0.07"/><text x="150" y="100" font-family="JetBrains Mono" font-size="16" fill="#9A9A94">сеть A</text>';
  s+='<rect x="770" y="70" width="560" height="290" rx="16" fill="#2563EB" opacity="0.06"/><text x="1250" y="100" font-family="JetBrains Mono" font-size="16" fill="#9A9A94">сеть B</text>';
  s+='<g stroke="#9A9A94" stroke-width="2">';A.forEach(function(p){s+='<line x1="'+SWA[0]+'" y1="'+SWA[1]+'" x2="'+p[0]+'" y2="'+p[1]+'"/>';});B.forEach(function(p){s+='<line x1="'+SWB[0]+'" y1="'+SWB[1]+'" x2="'+p[0]+'" y2="'+p[1]+'"/>';});
  if(hasR){s+='<line x1="'+SWA[0]+'" y1="'+SWA[1]+'" x2="'+R[0]+'" y2="'+R[1]+'"/><line x1="'+R[0]+'" y1="'+R[1]+'" x2="'+SWB[0]+'" y2="'+SWB[1]+'"/>';}
  else{s+='<line x1="'+SWA[0]+'" y1="'+SWA[1]+'" x2="'+SWB[0]+'" y2="'+SWB[1]+'"/>';}s+='</g>';
  if(hasR){s+='<rect x="'+(R[0]-56)+'" y="'+(R[1]-38)+'" width="112" height="76" rx="14" fill="#111"/><text x="'+R[0]+'" y="'+(R[1]+6)+'" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="20" fill="#FF5A1F">R1</text>';}
  else{s+='<circle cx="'+R[0]+'" cy="'+R[1]+'" r="30" fill="#fff" stroke="#9A9A94" stroke-width="2" stroke-dasharray="5 5"/><text x="'+R[0]+'" y="'+(R[1]+42)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="14" fill="#9A9A94">нет роутера</text>';}
  s+='<rect x="'+(SWA[0]-38)+'" y="'+(SWA[1]-26)+'" width="76" height="52" rx="10" fill="#fff" stroke="#111" stroke-width="2"/><text x="'+SWA[0]+'" y="'+(SWA[1]+5)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="13">SW-A</text>';
  s+='<rect x="'+(SWB[0]-38)+'" y="'+(SWB[1]-26)+'" width="76" height="52" rx="10" fill="#fff" stroke="#111" stroke-width="2"/><text x="'+SWB[0]+'" y="'+(SWB[1]+5)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="13">SW-B</text>';
  A.forEach(function(p,k){s+=node(p[0],p[1],'A'+(k+1));});B.forEach(function(p,k){s+=node(p[0],p[1],'B'+(k+1));});s+='<g id="pk"></g>';svg.innerHTML=s;}
 draw();
 document.getElementById('stormR').onclick=function(){hasR=!hasR;this.textContent='Маршрутизатор: '+(hasR?'есть':'убран');this.classList.toggle('acc',hasR);draw();document.getElementById('stormHint').textContent=hasR?'R1 на месте: broadcast упрётся в него и останется в сети A.':'Роутера нет — сети слились в один L2-домен: broadcast зальёт и A, и B.';};
 document.getElementById('stormGo').onclick=function(){draw();var pk=[{a:SWA,b:A[0],sp:.9,col:'#FF5A1F',loop:true},{a:SWA,b:A[1],sp:.9,off:-.15,col:'#FF5A1F',loop:true},{a:SWA,b:R,sp:.9,off:-.3,col:'#FF5A1F',loop:true}];
  if(!hasR){pk.push({a:R,b:SWB,sp:.9,off:-.5,col:'#FF5A1F',loop:true},{a:SWB,b:B[0],sp:.9,off:-.7,col:'#FF5A1F',loop:true},{a:SWB,b:B[1],sp:.9,off:-.85,col:'#FF5A1F',loop:true});}
  animPackets(svg,pk);document.getElementById('stormHint').textContent=hasR?'Broadcast заполнил только сеть A — домен ограничен.':'ШТОРМ: broadcast залил обе сети — единый домен.';};};

/* bsmall: L2 broadcast all receive */
inits.bsmall=function(sl){var svg=document.getElementById('bsmallSvg');var sw=[700,190];
 var d=[[300,80],[300,300],[1100,80],[1100,300]];
 function draw(){var s='<g stroke="#9A9A94" stroke-width="2">';d.forEach(function(p){s+='<line x1="'+sw[0]+'" y1="'+sw[1]+'" x2="'+p[0]+'" y2="'+p[1]+'"/>';});s+='</g>';
  s+='<rect x="'+(sw[0]-70)+'" y="'+(sw[1]-40)+'" width="140" height="80" rx="14" fill="#111"/><text x="'+sw[0]+'" y="'+(sw[1]+6)+'" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="17" fill="#fff">SW L2</text>';
  d.forEach(function(p,k){s+=node(p[0],p[1],'PC'+(k+1),false);});s+='<g id="pk"></g>';svg.innerHTML=s;}
 draw();
 document.getElementById('bsmallBtn').onclick=function(){draw();animPackets(svg,d.map(function(p,k){return {a:sw,b:p,sp:1,off:-k*0.05,col:'#FF5A1F',loop:true};}));};};

/* bgrow: broadcast traffic grows superlinearly */
inits.bgrow=function(sl){var box=document.getElementById('bgrowBars');var r=document.getElementById('bgrowR');
 function upd(){var nn=+r.value;box.innerHTML='';var maxT=40*39;
  for(var k=2;k<=nn;k+=Math.max(1,Math.round(nn/16))){var t=k*(k-1);var h=Math.max(4,t/maxT*260);
   box.innerHTML+='<div style="flex:1;background:'+(k===nn?'#FF5A1F':'#111')+';height:'+h+'px;border-radius:5px 5px 0 0"></div>';}
  document.getElementById('bgrowInfo').innerHTML='узлов <b>'+nn+'</b> → broadcast-обменов ~ <b style="color:#FF5A1F">'+(nn*(nn-1))+'</b><br>трафик ∝ n² — растёт опережающе';}
 r.oninput=upd;upd();};

/* rdom: router limits broadcast */
inits.rdom=function(sl){var svg=document.getElementById('rdomSvg');var R=[700,200],A=[[220,110],[220,300]],B=[[1180,110],[1180,300]],SWA=[460,200],SWB=[940,200];
 function draw(){var s='<rect x="60" y="60" width="600" height="280" rx="16" fill="#FF5A1F" opacity="0.07"/><rect x="740" y="60" width="600" height="280" rx="16" fill="#2563EB" opacity="0.06"/>';
  s+='<g stroke="#9A9A94" stroke-width="2"><line x1="'+SWA[0]+'" y1="'+SWA[1]+'" x2="'+R[0]+'" y2="'+R[1]+'"/><line x1="'+R[0]+'" y1="'+R[1]+'" x2="'+SWB[0]+'" y2="'+SWB[1]+'"/>';
  A.forEach(function(p){s+='<line x1="'+SWA[0]+'" y1="'+SWA[1]+'" x2="'+p[0]+'" y2="'+p[1]+'"/>';});B.forEach(function(p){s+='<line x1="'+SWB[0]+'" y1="'+SWB[1]+'" x2="'+p[0]+'" y2="'+p[1]+'"/>';});s+='</g>';
  s+='<rect x="'+(R[0]-56)+'" y="'+(R[1]-40)+'" width="112" height="80" rx="14" fill="#111"/><text x="'+R[0]+'" y="'+(R[1]+6)+'" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="20" fill="#FF5A1F">R</text>';
  s+='<rect x="'+(SWA[0]-40)+'" y="'+(SWA[1]-28)+'" width="80" height="56" rx="10" fill="#fff" stroke="#111" stroke-width="2"/><text x="'+SWA[0]+'" y="'+(SWA[1]+5)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="14">SW-A</text>';
  s+='<rect x="'+(SWB[0]-40)+'" y="'+(SWB[1]-28)+'" width="80" height="56" rx="10" fill="#fff" stroke="#111" stroke-width="2"/><text x="'+SWB[0]+'" y="'+(SWB[1]+5)+'" text-anchor="middle" font-family="JetBrains Mono" font-size="14">SW-B</text>';
  A.forEach(function(p,k){s+=node(p[0],p[1],'A'+(k+1));});B.forEach(function(p,k){s+=node(p[0],p[1],'B'+(k+1));});s+='<g id="pk"></g>';svg.innerHTML=s;}
 draw();
 document.getElementById('rdomBcast').onclick=function(){draw();animPackets(svg,[{a:SWA,b:A[0],sp:.9,col:'#FF5A1F',loop:true},{a:SWA,b:A[1],sp:.9,off:-.2,col:'#FF5A1F',loop:true},{a:SWA,b:R,sp:.9,off:-.4,col:'#FF5A1F',loop:true}]);
  document.getElementById('rdomHint').textContent='Broadcast упёрся в маршрутизатор — в сеть B не прошёл.';};
 document.getElementById('rdomUni').onclick=function(){draw();animPackets(svg,[{a:A[0],b:SWA,sp:1,col:'#2563EB'},{a:SWA,b:R,sp:1,off:-1,col:'#2563EB'},{a:R,b:SWB,sp:1,off:-2,col:'#2563EB'},{a:SWB,b:B[0],sp:1,off:-3,col:'#2563EB'}]);
  document.getElementById('rdomHint').textContent='Unicast маршрутизатор пропускает — дошёл до сети B.';};};

/* half: 4th-octet stepper for two /25 */
inits.half=function(sl){var step=0;
 var cases=[{o:'00000000',t:'подсеть 1 · адрес сети',ip:'192.168.15.0/25',note:'узловая часть — все нули → первый адрес'},
  {o:'01111111',t:'подсеть 1 · broadcast',ip:'192.168.15.127/25',note:'узловая часть — все единицы → последний адрес'},
  {o:'10000000',t:'подсеть 2 · адрес сети',ip:'192.168.15.128/25',note:'+1 к broadcast → перенос в сетевой бит: родилась новая подсеть'},
  {o:'11111111',t:'подсеть 2 · broadcast',ip:'192.168.15.255/25',note:'узловая часть снова все единицы → конец второй подсети'}];
 function render(){var c=cases[step];var dec=parseInt(c.o,2);
  document.getElementById('halfBits').innerHTML='<div class="bitauto" data-oct="'+c.o+'" data-net="1"></div>';renderBits(document.getElementById('halfBits'));
  document.getElementById('halfCap').innerHTML='<span class="h-d h4">'+c.t+'</span>';
  document.getElementById('halfDec').innerHTML='<span class="mono">'+c.o.slice(0,1)+' '+c.o.slice(1)+'</span> = <span class="dec">'+dec+'</span> → <span class="ip mono">'+c.ip+'</span>';
  document.getElementById('halfNote').textContent=c.note;
  [].forEach.call(sl.querySelectorAll('.steps .st'),function(st,k){st.classList.toggle('on',k===step);});}
 render();
 document.getElementById('halfNext').onclick=function(){step=(step+1)%4;render();};
 document.getElementById('halfPrev').onclick=function(){step=(step+3)%4;render();};};

/* divider / borrow: subnet divider slider */
inits.divider=function(sl){var base=(192<<24)|(168<<16)|(15<<8)|0;var basePref=24,hostBase=8;var r=document.getElementById('divR');
 function upd(){var b=+r.value;var pref=basePref+b;var subs=Math.pow(2,b);var hbits=hostBase-b;var per=Math.pow(2,hbits);var usable=Math.max(per-2,0);
  document.getElementById('divBits').textContent=b;
  document.getElementById('divInfo').innerHTML='маска <b>'+maskStr(pref)+'</b> · /'+pref+'<br>подсетей <b style="color:#FF5A1F">'+subs+'</b> · узлов в каждой <b>'+usable+'</b> · шаг блока '+per;
  var seg='';var show=Math.min(subs,32);for(var k=0;k<show;k++)seg+='<div style="flex:1;background:'+(k%2?'#FF5A1F':'#111')+';border-right:1px solid #fff"></div>';
  document.getElementById('divBar').innerHTML=seg;
  var rows='<tr><th>№</th><th>Адрес сети</th><th>Диапазон узлов</th><th>Broadcast</th></tr>';var lim=Math.min(subs,16);
  for(var k=0;k<lim;k++){var net=(base+k*per)>>>0;var bc=(net+per-1)>>>0;rows+='<tr><td>'+(k+1)+'</td><td>'+ipS(net)+'/'+pref+'</td><td>'+ipS((net+1)>>>0)+' – '+ipS((bc-1)>>>0)+'</td><td>'+ipS(bc)+'</td></tr>';}
  if(subs>lim)rows+='<tr><td>…</td><td colspan="3">ещё '+(subs-lim)+' подсет(и/ей) по тому же принципу</td></tr>';
  document.getElementById('divTbl').innerHTML=rows;}
 r.oninput=upd;upd();};

/* border: 4th octet bit rows for /25 boundaries */
inits.border=function(sl){var mode='net1';
 var cases={net1:{v:0,t:'1-я подсеть · адрес сети',ip:'192.168.15.0/25'},bc1:{v:127,t:'1-я подсеть · broadcast',ip:'192.168.15.127/25'},
  net2:{v:128,t:'2-я подсеть · адрес сети',ip:'192.168.15.128/25'},bc2:{v:255,t:'2-я подсеть · broadcast',ip:'192.168.15.255/25'}};
 function bitsRow(val){var s='';for(var k=0;k<8;k++){var on=(val>>(7-k))&1;var net=k<1;
   s+='<div class="bit '+(net?'net':(on?'on':''))+'"><div class="w">'+W[k]+'</div><div class="v">'+on+'</div></div>';}
   return '<div class="bits" style="max-width:900px;margin:0 auto">'+s+'</div>';}
 function render(){var c=cases[mode];
  document.getElementById('borderBody').innerHTML='<div style="text-align:center;margin-bottom:14px"><span class="h-d h4">'+c.t+'</span> → <span class="mono o" style="font-size:26px">'+c.ip+'</span></div>'
   +'<div class="mono g2c" style="text-align:center;margin-bottom:10px">4-й октет · <span style="color:#111">■</span> сетевой бит /25 · <span style="color:#FF5A1F">■</span> узловые</div>'+bitsRow(c.v)
   +'<p class="body sm g2c" style="text-align:center;margin-top:14px">'+(mode.indexOf('net')===0?'узловая часть — все нули → это адрес сети':'узловая часть — все единицы → это broadcast')+'</p>';}
 [].forEach.call(sl.querySelectorAll('[data-bd]'),function(b){b.onclick=function(){mode=b.dataset.bd;[].forEach.call(sl.querySelectorAll('[data-bd]'),function(x){x.classList.toggle('on',x===b);x.classList.toggle('acc',x===b);});render();};});
 render();};

/* eight: stepper over 8 subnets /27 */
inits.eight=function(sl){var idx=0;var W3=[128,64,32,16,8,4,2,1];
 function three(k){return ('00'+k.toString(2)).slice(-3);}
 function render(){var net=idx*32;var bc=net+31;var oct=('0000000'+net.toString(2)).slice(-8);
  document.getElementById('eightBits').innerHTML='<div class="bitauto" data-oct="'+oct+'" data-net="3"></div>';renderBits(document.getElementById('eightBits'));
  document.getElementById('eightCap').innerHTML='подсеть <b>'+(idx+1)+'</b> из 8 · счётчик <span class="mono o">'+three(idx)+'</span>';
  document.getElementById('eightDec').innerHTML='<span class="mono">'+three(idx)+' '+oct.slice(3)+'</span> = <span class="dec">'+net+'</span> → <span class="ip mono">192.168.15.'+net+'/27</span>';
  document.getElementById('eightRange').innerHTML='узлы .'+(net+1)+' – .'+(bc-1)+' · broadcast .'+bc;}
 render();
 document.getElementById('eightNext').onclick=function(){idx=(idx+1)%8;render();};
 document.getElementById('eightPrev').onclick=function(){idx=(idx+7)%8;render();};};

/* formula calc */
inits.formula=function(sl){var r=document.getElementById('fR');
 function upd(){var b=+r.value;var hbits=8-b;var subs=Math.pow(2,b);var usable=Math.max(Math.pow(2,hbits)-2,0);var pref=24+b;
  document.getElementById('fB').textContent=b;
  document.getElementById('fOut').innerHTML='b = '+b+' → подсетей 2<sup>'+b+'</sup> = <b style="color:#FF5A1F">'+subs+'</b> · осталось узловых бит '+hbits+' → узлов 2<sup>'+hbits+'</sup> − 2 = <b style="color:#FF5A1F">'+usable+'</b> · маска /'+pref;}
 r.oninput=upd;upd();};

/* need: pick mask for N subnets from /16 */
inits.need=function(sl){var inp=document.getElementById('needN');
 function upd(){var need=parseInt(inp.value,10);if(isNaN(need)||need<1)need=1;
  var b=0;while(Math.pow(2,b)<need)b++;var subs=Math.pow(2,b);var pref=16+b;var hbits=32-pref;var usable=Math.pow(2,hbits)-2;
  document.getElementById('needOut').innerHTML='<div class="card inv" style="text-align:center"><div class="mono" style="font-size:24px;color:#e8e6e0">нужно '+need+' → ближайшая степень двойки <b style="color:#FF5A1F">'+subs+'</b> = 2<sup>'+b+'</sup> → заимствуем <b>'+b+'</b> бит → префикс <b style="color:#FF5A1F">/'+pref+'</b> · маска '+maskStr(pref)+' · узлов '+usable.toLocaleString('ru')+'</div></div>';
  var rows='<tr><th>Префикс</th><th>Подсетей</th><th>Узлов</th></tr>';for(var p=17;p<=22;p++){var s=Math.pow(2,p-16);var u=Math.pow(2,32-p)-2;rows+='<tr'+(p===pref?' class="hot"':'')+'><td>/'+p+'</td><td>'+s+'</td><td>'+u.toLocaleString('ru')+'</td></tr>';}
  document.getElementById('needTbl').innerHTML=rows;}
 inp.oninput=upd;upd();};

/* hostn: prefix vs hosts table */
inits.hostn=function(sl){var t=document.getElementById('hostnTbl');
 var rows='<tr><th>Префикс</th><th>Маска</th><th>Подсетей</th><th>Узлов</th></tr>';
 [[25,2,126],[26,4,62],[27,8,30],[28,16,14],[29,32,6],[30,64,2]].forEach(function(x){rows+='<tr data-p="1"><td>/'+x[0]+'</td><td>'+maskStr(x[0])+'</td><td>'+x[1]+'</td><td>'+x[2]+'</td></tr>';});
 t.innerHTML=rows;};

/* vtopo: VLSM topology */
inits.vtopo=function(sl){var svg=document.getElementById('vtopoSvg');
 var s='<g stroke="#9A9A94" stroke-width="2"><line x1="700" y1="200" x2="300" y2="200"/><line x1="700" y1="200" x2="1100" y2="200"/></g>';
 s+='<rect x="640" y="150" width="120" height="100" rx="14" fill="#111"/><text x="700" y="195" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="18" fill="#fff">HQ</text><text x="700" y="222" text-anchor="middle" font-family="JetBrains Mono" font-size="14" fill="#FF5A1F">300</text>';
 s+='<rect x="200" y="150" width="120" height="100" rx="14" fill="#fff" stroke="#111" stroke-width="2"/><text x="260" y="195" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="18">Ф1</text><text x="260" y="222" text-anchor="middle" font-family="JetBrains Mono" font-size="14" fill="#FF5A1F">20</text>';
 s+='<rect x="1040" y="150" width="120" height="100" rx="14" fill="#fff" stroke="#111" stroke-width="2"/><text x="1100" y="195" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="18">Ф2</text><text x="1100" y="222" text-anchor="middle" font-family="JetBrains Mono" font-size="14" fill="#FF5A1F">70</text>';
 s+='<text x="490" y="180" text-anchor="middle" font-family="JetBrains Mono" font-size="15" fill="#9A9A94">канал /30</text>';
 s+='<text x="910" y="180" text-anchor="middle" font-family="JetBrains Mono" font-size="15" fill="#9A9A94">канал /30</text>';
 s+='<text x="700" y="330" text-anchor="middle" font-family="Inter" font-size="20" fill="#111">3 сети + 2 канала = <tspan font-weight="700" fill="#FF5A1F">5 сетей</tspan></text>';
 svg.innerHTML=s;};

/* vlsm stepper */
inits.vlsm=function(sl){var step=0;
 var rows=[['HQ, головной офис','300','510','/23','172.16.0.0/23','172.16.0.1 – 172.16.1.254','172.16.1.255'],
  ['Ф2, филиал №2','70','126','/25','172.16.2.0/25','172.16.2.1 – 172.16.2.126','172.16.2.127'],
  ['Ф1, филиал №1','20','30','/27','172.16.2.128/27','172.16.2.129 – 172.16.2.158','172.16.2.159'],
  ['Канал Ф1–HQ','2','2','/30','172.16.2.160/30','172.16.2.161 – 172.16.2.162','172.16.2.163'],
  ['Канал Ф2–HQ','2','2','/30','172.16.2.164/30','172.16.2.165 – 172.16.2.166','172.16.2.167']];
 function render(){var h='<tr><th>Сеть</th><th>Нужно</th><th>Факт</th><th>Префикс</th><th>Адрес сети</th><th>Диапазон узлов</th><th>Broadcast</th></tr>';
  rows.forEach(function(rw,k){var on=k<step;h+='<tr style="opacity:'+(on?1:.2)+'">'+rw.map(function(c,ci){return '<td'+(ci===3?' style="color:#FF5A1F;font-weight:700"':'')+'>'+(on?c:(ci===0?c:'—'))+'</td>';}).join('')+'</tr>';});
  document.getElementById('vlsmTbl').innerHTML=h;}
 render();
 document.getElementById('vlsmNext').onclick=function(){if(step<rows.length)step++;render();};
 document.getElementById('vlsmReset').onclick=function(){step=0;render();};};

/* vruler: VLSM ruler on /22 */
inits.vruler=function(sl){var withV=true;
 var blocks=[{n:'HQ /23',f:512,c:'#111'},{n:'Ф2 /25',f:128,c:'#FF5A1F'},{n:'Ф1 /27',f:32,c:'#2563EB'},{n:'к1 /30',f:4,c:'#0f9d58'},{n:'к2 /30',f:4,c:'#7c3aed'},{n:'резерв',f:1024-512-128-32-8,c:'#E7E5E0'}];
 var total=1024;
 function render(){var box=document.getElementById('vrulerBar');
  if(withV){box.innerHTML=blocks.map(function(b){return '<div style="width:'+(b.f/total*100)+'%;background:'+b.c+';color:'+(b.c==='#E7E5E0'?'#9A9A94':'#fff')+';font-family:JetBrains Mono;font-size:13px;display:flex;align-items:center;justify-content:center;padding:14px 2px;overflow:hidden;white-space:nowrap">'+b.n+'</div>';}).join('');
   document.getElementById('vrulerCap').innerHTML='<b>С VLSM:</b> всё умещается в один блок <span class="mono o">172.16.0.0/22</span> (1024 адреса), ещё и резерв остаётся.';}
  else{var s='';for(var k=0;k<8;k++){s+='<div style="width:12.5%;background:'+(k<5?'#111':'#E7E5E0')+';color:'+(k<5?'#fff':'#9A9A94')+';font-family:JetBrains Mono;font-size:13px;display:flex;align-items:center;justify-content:center;padding:14px 2px;border-right:1px solid #fff">'+(k<5?'сеть '+(k+1)+' /23':'—')+'</div>';}box.innerHTML=s;
   document.getElementById('vrulerCap').innerHTML='<b>Без VLSM:</b> каждая из 5 сетей = /23 (под максимум 300), округляем до 8×/23 = <span class="mono o">172.16.0.0/20</span> — вчетверо больше.';}}
 render();
 document.getElementById('vrulerTog').onclick=function(){withV=!withV;this.textContent=withV?'Показать без VLSM (/20)':'Показать с VLSM (/22)';render();};};

/* v6sub: IPv6 subnet id slider */
inits.v6sub=function(sl){var r=document.getElementById('v6R');
 function upd(){var nn=+r.value;document.getElementById('v6N').textContent=nn;var s='';
  for(var k=0;k<nn;k++){var id=('000'+k).slice(-4);s+='2001:ABCD:BCDA:<span class="o">'+id+'</span>::/64<br>';}
  document.getElementById('v6list').innerHTML=s;}
 r.oninput=upd;upd();};

/* v6b: toggle subnet-id /64 vs interface-id /68 */
inits.v6b=function(sl){var mode='sub';
 function render(){var s='';
  if(mode==='sub'){for(var k=0;k<5;k++){var id=('000'+k).slice(-4);s+='2001:ABCD:BCDA:<span class="o">'+id+'</span>::/64<br>';}
   document.getElementById('v6bNote').innerHTML='Идентификатор подсети (16 бит) → до <b>2¹⁶ = 65 536</b> подсетей /64. Штатный способ.';}
  else{for(var k=0;k<5;k++){s+='2001:ABCD:BCDA:0000:<span class="o">'+k+'</span>000::/68<br>';}
   document.getElementById('v6bNote').innerHTML='Заимствуем 4 бита интерфейса (кратно 4) → /68. Так почти не делают: ломается автоконфигурация (SLAAC).';}
  document.getElementById('v6bList').innerHTML=s;}
 [].forEach.call(sl.querySelectorAll('[data-v6]'),function(b){b.onclick=function(){mode=b.dataset.v6;[].forEach.call(sl.querySelectorAll('[data-v6]'),function(x){x.classList.toggle('on',x===b);x.classList.toggle('acc',x===b);});render();};});
 render();};

/* quiz */
var QZ=[
{q:'Что ограничивает широковещательный домен?',a:['маршрутизатор','коммутатор L2','хаб'],ok:0,why:'Маршрутизатор не пропускает broadcast.'},
{q:'Чтобы получить 8 подсетей, сколько бит заимствуем?',a:['3','2','8'],ok:0,why:'2³ = 8 подсетей.'},
{q:'Сколько узлов в подсети /26?',a:['62','64','126'],ok:0,why:'2⁶ − 2 = 62.'},
{q:'Маска для /27 — это…',a:['255.255.255.224','255.255.255.192','255.255.255.240'],ok:0,why:'11100000 = 224.'},
{q:'Почему в формуле узлов вычитают 2?',a:['адрес сети и broadcast','шлюз и DNS','запас на рост'],ok:0,why:'Первый адрес — сеть, последний — broadcast.'},
{q:'Разбить сеть ровно на 3 равные подсети…',a:['нельзя, только степень двойки','можно','можно на /26'],ok:0,why:'Число подсетей кратно степени двойки; под 3 берут 4.'},
{q:'Нужно 50 подсетей — на сколько режем?',a:['на 64','на 50','на 56'],ok:0,why:'Ближайшая большая степень двойки — 64 = 2⁶.'},
{q:'Главный плюс VLSM?',a:['адреса под фактический размер','быстрее считать','только для IPv6'],ok:0,why:'Маски переменной длины — блок под реальную потребность.'},
{q:'В VLSM считают…',a:['от большего к меньшему','от меньшего','в любом порядке'],ok:0,why:'Крупный блок последовательно режут на меньшие.'},
{q:'Канал точка-точка между роутерами — это…',a:['отдельная сеть /30','не сеть','часть LAN'],ok:0,why:'2 узла → маска /30, отдельная сеть.'},
{q:'Сколько подсетей даёт идентификатор подсети IPv6?',a:['2¹⁶ = 65 536','256','2⁶⁴'],ok:0,why:'16 бит → 65 536 подсетей /64.'},
{q:'Заимствование бит интерфейса в IPv6…',a:['ломает SLAAC','ускоряет сеть','обязательно'],ok:0,why:'Перестаёт работать автоконфигурация адреса.'},
{q:'Broadcast первой подсети 192.168.15.0/25 — это…',a:['.127','.128','.255'],ok:0,why:'01111111 = 127.'},
{q:'Адрес сети — это адрес, где узловая часть…',a:['все нули','все единицы','127'],ok:0,why:'Первый адрес подсети — узловая часть в нулях.'}];
var qzI=0,qzOk=0,qzAll=0,qzRun=false,qzAns=[];
function qzStart(){qzI=0;qzOk=0;qzAll=0;qzRun=true;qzAns=QZ.map(function(){return -1});document.getElementById('qzOk').textContent='0';document.getElementById('qzAll').textContent='0';document.getElementById('qzStart').textContent='Заново';qzShow();}
function qzShow(){var box=document.getElementById('qzBtns'),it=QZ[qzI],ch=qzAns[qzI];document.getElementById('qzQ').textContent=(qzI+1)+'. '+it.q;box.innerHTML='';
 it.a.forEach(function(t,k){var b=document.createElement('button');b.className='abtn';b.style.cssText+='text-align:left;justify-content:flex-start';if(ch>-1){if(k===it.ok){b.classList.add('acc');}if(k===ch&&ch!==it.ok){b.style.background='#111';b.style.color='#fff';}}b.textContent=t;b.onclick=function(){qzAns2(k);};box.appendChild(b);});
 var m=document.getElementById('qzMsg');if(ch>-1){m.textContent=(ch===it.ok?'Верно. ':'Нет. Правильный: «'+it.a[it.ok]+'». ')+it.why;}else m.textContent='Выбери ответ.';
 var nav=document.getElementById('qzNav');nav.innerHTML='';var p=document.createElement('button');p.className='abtn';p.textContent='‹';p.disabled=qzI===0;p.onclick=function(){if(qzI>0){qzI--;qzShow();}};var c=document.createElement('span');c.className='mono';c.style.color='#9A9A94';c.textContent=(qzI+1)+'/'+QZ.length;var nx=document.createElement('button');nx.className='abtn';nx.textContent='›';nx.disabled=qzI===QZ.length-1;nx.onclick=function(){if(qzI<QZ.length-1){qzI++;qzShow();}};nav.appendChild(p);nav.appendChild(c);nav.appendChild(nx);}
function qzAns2(k){if(!qzRun)return;if(qzAns[qzI]===-1){qzAns[qzI]=k;qzAll++;if(k===QZ[qzI].ok)qzOk++;document.getElementById('qzOk').textContent=qzOk;document.getElementById('qzAll').textContent=qzAll;}else qzAns[qzI]=k;qzShow();}
inits.quiz=function(){var b=document.getElementById('qzStart');b.onclick=qzStart;if(!qzRun){document.getElementById('qzQ').textContent='Нажми «Старт»';document.getElementById('qzBtns').innerHTML='';document.getElementById('qzNav').innerHTML='';}};

renderBits(document);
fit();show(0);
})();
