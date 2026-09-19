/* THUMBMENU: меню с мини-слайдами (кнопка «Слайды» или клавиша M) */
(function(){
  if(window.__thumbMenu) return; window.__thumbMenu=true;
  var slides=[].slice.call(document.querySelectorAll('section.slide'));
  if(slides.length<2) return;
  var css='#tm-btn{position:fixed;left:16px;bottom:16px;z-index:9998;display:flex;gap:8px;align-items:center;padding:9px 14px;border-radius:12px;border:1px solid rgba(128,128,160,.45);background:rgba(20,20,34,.78);color:#fff;font:600 14px/1 system-ui,Segoe UI,sans-serif;cursor:pointer;backdrop-filter:blur(6px)}'+
  '#tm-btn:hover{background:rgba(40,40,70,.92)}#tm-btn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2}'+
  '#tm-ov{position:fixed;inset:0;z-index:9999;background:rgba(12,12,22,.94);overflow:auto;padding:28px 36px;font-family:system-ui,Segoe UI,sans-serif}'+
  '#tm-ov[hidden]{display:none}#tm-hd{display:flex;justify-content:space-between;align-items:center;color:#fff;margin-bottom:18px}#tm-hd b{font-size:22px}'+
  '#tm-x{border:1px solid rgba(255,255,255,.3);background:none;color:#fff;border-radius:10px;padding:7px 12px;font:inherit;cursor:pointer}'+
  '#tm-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}'+
  '.tm-i{all:unset;box-sizing:border-box;cursor:pointer;display:flex;flex-direction:column;gap:6px;padding:6px;border-radius:12px;border:2px solid transparent;background:rgba(255,255,255,.05)}'+
  '.tm-i:hover{border-color:rgba(160,140,255,.7)}.tm-i:focus-visible{outline:3px solid #a78bfa}.tm-i.cur{border-color:#a78bfa}'+
  '.tm-t{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:8px;background:#fff;pointer-events:none}'+
  '.tm-t section{position:absolute!important;left:0!important;top:0!important;right:auto!important;bottom:auto!important;margin:0!important;display:flex!important;visibility:visible!important;opacity:1!important;transform-origin:0 0!important;pointer-events:none}'+
  '.tm-t *{animation-play-state:paused!important;transition:none!important}'+
  '.tm-n{color:#ddd;font-size:13px;display:flex;gap:8px}.tm-n span:first-child{color:#a78bfa;font-weight:700;min-width:22px}'+
  '@media print{#tm-btn,#tm-ov{display:none!important}}';
  var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
  var btn=document.createElement('button'); btn.id='tm-btn'; btn.type='button'; btn.title='Все слайды (M)';
  btn.innerHTML='<svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg>Слайды';
  var ov=document.createElement('div'); ov.id='tm-ov'; ov.hidden=true; ov.setAttribute('role','dialog'); ov.setAttribute('aria-label','Все слайды');
  ov.innerHTML='<div id="tm-hd"><b>Все слайды</b><button id="tm-x" type="button">Закрыть (Esc)</button></div><div id="tm-g"></div>';
  document.body.appendChild(btn); document.body.appendChild(ov);
  var grid=ov.querySelector('#tm-g');
  function title(s,k){
    var t=s.getAttribute('data-label')||s.getAttribute('data-title');
    if(!t){ var h=s.querySelector('h1,h2,h3,.h-d,.title'); t=h?h.textContent:''; }
    t=(t||'').replace(/\s+/g,' ').trim(); return t.length>60?t.slice(0,58)+'…':t||('Слайд '+(k+1));
  }
  function active(){
    for(var j=0;j<slides.length;j++){ if(slides[j].classList.contains('on')||slides[j].classList.contains('active')) return j; }
    var best=-1,ba=0;
    slides.forEach(function(s,i){var r=s.getBoundingClientRect(),cs=getComputedStyle(s);
      if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<.05) return;
      var a=Math.max(0,Math.min(r.right,innerWidth)-Math.max(r.left,0))*Math.max(0,Math.min(r.bottom,innerHeight)-Math.max(r.top,0));
      if(a>ba){ba=a;best=i;}});
    return best;
  }
  function key(k){ var e=new KeyboardEvent('keydown',{key:k,code:k,bubbles:true,cancelable:true}); (document.activeElement&&document.activeElement!==document.body?document.body:document.body).dispatchEvent(e); }
  function goTo(t){
    var guard=0, c=active();
    if(c<0) return;
    while(c!==t && guard++<400){ key(t>c?'ArrowRight':'ArrowLeft'); var n=active(); if(n===c){ /* шаги внутри слайда */ } c=n; }
  }
  var built=false, dims=[1920,1080];
  function build(){
    var a=slides[active()]||slides[0];
    var W=a.offsetWidth||innerWidth, H=a.offsetHeight||innerHeight; dims=[W,H];
    var bg='#fff',bgi='none',e=a.parentElement;
    while(e){ var cs=getComputedStyle(e); if(cs.backgroundImage!=='none'&&bgi==='none') bgi=cs.backgroundImage; if(cs.backgroundColor!=='rgba(0, 0, 0, 0)'&&cs.backgroundColor!=='transparent'){ bg=cs.backgroundColor; break; } e=e.parentElement; }
    grid.innerHTML='';
    slides.forEach(function(s,k){
      var b=document.createElement('button'); b.className='tm-i'; b.type='button';
      b.innerHTML='<span class="tm-t"></span><span class="tm-n"><span>'+(k+1)+'</span><span></span></span>';
      b.querySelector('.tm-n span:last-child').textContent=title(s,k);
      var box=b.querySelector('.tm-t'), c=s.cloneNode(true);
      box.style.backgroundColor=bg; box.style.backgroundImage=bgi; box.style.backgroundSize='cover';
      c.removeAttribute('id'); [].forEach.call(c.querySelectorAll('[id]'),function(e){e.removeAttribute('id')});
      [].forEach.call(c.querySelectorAll('input,button,select,textarea,a'),function(e){e.tabIndex=-1});
      [].forEach.call(c.querySelectorAll('video,audio,iframe'),function(e){e.remove()});
      c.classList.add('on','active','in','visible','show','is-active','current');
      c.setAttribute('aria-hidden','true');
      c.style.width=W+'px'; c.style.height=H+'px';
      var host=box, chain=[], pe=s.parentElement;
      while(pe&&pe!==document.body&&pe!==document.documentElement){ chain.unshift(pe); pe=pe.parentElement; }
      chain.forEach(function(anc){ var w=document.createElement(anc.tagName); if(anc.id) w.id=anc.id; w.className=anc.className;
        ['position','transform','width','height','inset','margin','padding','overflow','display','scale','translate','left','top'].forEach(function(pr){});
        w.style.cssText='position:absolute!important;inset:0!important;transform:none!important;scale:none!important;translate:none!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;overflow:visible!important;display:block!important;background:none!important;border:0!important;box-shadow:none!important';
        host.appendChild(w); host=w; });
      host.appendChild(c); c.__tmRoot=box.firstChild;
      b.onclick=function(){ close(); setTimeout(function(){ goTo(k); },30); };
      grid.appendChild(b);
    });
    requestAnimationFrame(function(){
      [].forEach.call(grid.querySelectorAll('.tm-t'),function(box){ var c=box.querySelector('section'); c.style.setProperty('transform','scale('+(box.clientWidth/dims[0])+')','important'); });
    });
    built=true;
  }
  function open(){ if(!built) build(); ov.hidden=false; var c=active();
    [].forEach.call(grid.children,function(b,k){b.classList.toggle('cur',k===c)});
    var cur=grid.children[c]; if(cur){ cur.focus({preventScroll:true}); cur.scrollIntoView({block:'center'}); } }
  function close(){ ov.hidden=true; }
  btn.onclick=open; ov.querySelector('#tm-x').onclick=close;
  addEventListener('resize',function(){ built=false; if(!ov.hidden){ build(); } });
  document.addEventListener('keydown',function(e){
    if(!ov.hidden){ if(e.key==='Escape'){ e.preventDefault(); e.stopImmediatePropagation(); close(); } else if(e.key==='ArrowRight'||e.key==='ArrowLeft'||e.key===' '){ e.stopImmediatePropagation(); } return; }
    var t=e.target.tagName; if(t==='INPUT'||t==='TEXTAREA'||e.ctrlKey||e.metaKey||e.altKey) return;
    if(e.key==='m'||e.key==='M'||e.key==='ь'||e.key==='Ь'){ e.preventDefault(); open(); }
  },true);
})();
