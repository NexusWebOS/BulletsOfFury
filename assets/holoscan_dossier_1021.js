'use strict';
/* The selected BOF Holoscan dossier. Native tutorial clocks/input/combat own the
   lesson; DOM text and authored turntables use that same render tick, no new RAF. */
const HS21={root:null,L:null,visible:false,dirty:true,lastFrame:'',lastInfo:'',rotating:true,draws:0,fontReady:false,fontStarted:false,targets:[],
 base:{card:ic20CardDraw,tick:ic20CardTick,next:tutNext,cleanup:tutCleanup,set:setState,warm:sg20Warm,keys:sg20Keys,ready:sg20LayersReady},
 art:{frame:{key:'hs21_frame',path:'assets/game/shared/ui/holoscan_1021/frame.webp'},floor:{key:'hs21_floor',path:'assets/game/shared/ui/holoscan_1021/floor.webp'},grid:{key:'hs21_grid',path:'assets/game/shared/ui/holoscan_1021/grid.webp'},dais:{key:'hs21_dais',path:'assets/game/shared/ui/holoscan_1021/dais.webp'}},
 order:['whole','missile','cannon','core'],reduced:typeof matchMedia==='function'?matchMedia('(prefers-reduced-motion: reduce)'):null};
for(const a of Object.values(HS21.art))XART._src[a.key]=a.path;
// Retain the old source record for reproducibility, remove it from live decoding.
const hs21Retired=IC20_KEYS.indexOf(IC20_ART.card.key);if(hs21Retired>=0)IC20_KEYS.splice(hs21Retired,1);
function hs21Warm(){for(const a of Object.values(HS21.art))XART.rdy(a.key);for(const k of ['pad_dpad','pad_a','pad_b','pad_start'])XART.rdy(k);
 if(!HS21.fontStarted&&typeof document!=='undefined'&&document.fonts){HS21.fontStarted=true;document.fonts.load('16px Holoscan').then(()=>{HS21.fontReady=true;HS21.dirty=true;}).catch(()=>{HS21.fontFailed=true;HS21.fontReady=true;});}}
sg20Keys=function(){return [...HS21.base.keys(),...Object.values(HS21.art).map(a=>a.key),'pad_dpad','pad_a','pad_b','pad_start'];};
sg20Warm=function(){const r=HS21.base.warm.apply(this,arguments);hs21Warm();return r;};
sg20LayersReady=function(){hs21Warm();return HS21.base.ready()&&HS21.fontReady&&Object.values(HS21.art).every(a=>XART.rdy(a.key));};
function hs21Active(){return state===GS.PLAY&&tutLive()&&TUT.L?.def.id==='bob_card';}
function hs21Data(){const S=BOB20_SPEC;return {total:Object.values(S).reduce((n,s)=>n+s.hp,0),missile:S.missile.hp,cannon:S.cannon.hp,core:S.core.hp,coreMissile:S.core.missileMultiplier};}
function hs21Select(i){if(!hs21Active()||TUT.done)return;const L=TUT.L;L.sel=clamp(i,0,3);L.seen[L.sel]=true;HS21.dirty=true;Audio.SFX.blip();}
function hs21Turn(d){if(!hs21Active())return;TUT.L.yaw=(TUT.L.yaw+d+32)%32;HS21.dirty=true;}
function hs21Canvas(c){const r=c.getBoundingClientRect(),k=Math.min(window.devicePixelRatio||1,1.5),even=n=>Math.max(2,Math.ceil(n/2)*2),w=even(r.width*k),h=even(r.height*k);if(c.width!==w||c.height!==h){c.width=w;c.height=h;}const g=c.getContext('2d');g.setTransform(w/Math.max(1,r.width),0,0,h/Math.max(1,r.height),0,0);g.clearRect(0,0,r.width,r.height);g.imageSmoothingEnabled=false;return{g,w:r.width,h:r.height};}
function hs21Part(g,key,f,x,y,size,glow=false){const a=IC20_ART.views[key];if(!a||!XART.rdy(a.key))return;const c=a.cells[(f%a.frames+a.frames)%a.frames];g.save();if(glow){g.shadowColor='#48dfff';g.shadowBlur=12;}g.drawImage(XART.get(a.key),...c,x-size/2,y-size/2,size,size);g.restore();}
function hs21Glyph(canvas,key){if(!XART.rdy(key))return;const im=XART.get(key),g=canvas.getContext('2d'),iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height,k=28/Math.max(iw,ih);g.clearRect(0,0,32,32);g.imageSmoothingEnabled=false;g.drawImage(im,(32-iw*k)/2,(32-ih*k)/2,iw*k,ih*k);}
function hs21Draw(L){const main=HS21.root.querySelector('.hs-model'),{g,w,h}=hs21Canvas(main),compact=innerWidth<=900,f=Math.floor(L.yaw)%32,selected=HS21.order[L.sel],small=w<530;
 const specs=[['missile',.205,small?.59:.54,small?.60:.88,'01'],['core',.50,small?.50:.48,small?.78:1.12,'02'],['cannon',.805,small?.59:.54,small?.60:.88,'03']];HS21.targets=[];
 for(const[key,fx,fy,fs,id]of specs){const size=Math.min(h*fs,w*(key==='core'?.43:.28)),x=w*fx,y=h*fy,active=selected==='whole'||selected===key;
  if(XART.rdy('hs21_dais')){const im=XART.get('hs21_dais'),rw=size*.96,rh=rw*im.height/im.width;g.globalAlpha=active?.8:.35;g.drawImage(im,x-rw/2,h*.82-rh/2,rw,rh);g.globalAlpha=1;}
  hs21Part(g,key,f,x,y,size,active);HS21.targets.push({i:HS21.order.indexOf(key),x:x-size*.32,y:y-size*.39,w:size*.64,h:size*.78});
  const tx=x+size*.34,ty=Math.max(small?25:30,y-size*.38);g.strokeStyle=active?'#bceeff':'#397b9a';g.lineWidth=1.2;g.beginPath();g.moveTo(x+size*.19,y-size*.14);g.lineTo(tx,ty);g.lineTo(tx+20,ty);g.stroke();g.fillStyle=active?'#efffff':'#76afc7';g.fillRect(x+size*.19-2,y-size*.14-2,4,4);ui20Text(g,id,tx+11,ty-10,small?12:18,38,'center',active?'#edfbff':'#6999ae');
  if(!compact)ui20Text(g,key==='core'?'CRYO REACTOR':key==='missile'?'MISSILE POD':'CANNON POD',x,h*.95,Math.min(16,w/52),w*.28,'center',active?'#bdf4ff':'#6791a5');
 }
 for(const c of HS21.root.querySelectorAll('[data-model]')){const q=hs21Canvas(c);hs21Part(q.g,c.dataset.model,f,q.w/2,q.h/2,Math.min(q.w,q.h)*(c.classList.contains('hs-detail-model')?1.05:1.2),false);}
 for(const c of HS21.root.querySelectorAll('[data-glyph]'))hs21Glyph(c,c.dataset.glyph);
 IC20.cardFrame={part:selected,frame:f};HS21.draws++;HS21.modelFrame=f;
}
function hs21Hide(release=false){if(!HS21.root)return;HS21.root.hidden=true;HS21.visible=false;HS21.drag=null;if(release){HS21.L=null;HS21.lastFrame='';HS21.dirty=true;for(const c of HS21.root.querySelectorAll('canvas')){c.width=2;c.height=2;}}document.body.classList.remove('holoscan-open');}
function hs21Sync(){if(!hs21Active())hs21Hide(!tutLive()||TUT.L?.def.id!=='bob_card');}
function hs21Build(){if(HS21.root||typeof HTMLElement!=='function')return;const root=HS21.root=document.createElement('section');root.id='bof-holoscan';root.hidden=true;root.setAttribute('role','dialog');root.setAttribute('aria-modal','true');root.setAttribute('aria-labelledby','hs21-name');root.tabIndex=-1;
 const glyph=(key)=>'<canvas class="hs-glyph" width="32" height="32" data-glyph="'+key+'" aria-hidden="true"></canvas>';
 const names={whole:['FULL UNIT','FULL UNIT'],missile:['MISSILE POD','MISSILE'],cannon:['CANNON POD','CANNON'],core:['CRYO REACTOR','REACTOR']};
 const tiny={whole:'ALL',missile:'MSSL',cannon:'GUN',core:'CORE'};
 const tabs=HS21.order.map((k,i)=>'<button type="button" class="hs-part" data-part="'+i+'" aria-pressed="'+(i===0)+'" aria-label="Inspect '+names[k][0]+'"><canvas class="hs-thumb" data-model="'+k+'" aria-hidden="true"></canvas><span class="hs-wide">'+names[k][0]+'</span><span class="hs-short">'+names[k][1]+'</span><span class="hs-tiny">'+tiny[k]+'</span></button>').join('');
 root.innerHTML='<div class="hs-shell"><header class="hs-header"><div class="hs-title"><h1 id="hs21-name">B.O.B.</h1><p class="hs-subtitle">BALLISTICS<br>ORIENTATION BOT</p></div><div class="hs-mode"><span class="hs-mode-label">02 / HOLOSCAN<br><span class="hs-scan-label">UNIT ANALYSIS MODE</span></span><button type="button" class="hs-pause" aria-label="Pause tutorial">'+glyph('pad_start')+'<span class="hs-glyph-label">PAUSE</span></button><div class="hs-progress" aria-hidden="true"><span></span></div></div></header><div class="hs-workspace"><div class="hs-stage"><div class="hs-classification"><strong>CLASS : TRAINING MECH</strong><br>HP : <span data-stat="total"></span> / ICE REACTOR<br><span class="hs-class-extra">ARMAMENT : CANNON / MISSILES<br>MODULES : 2 PODS + REACTOR</span></div><canvas class="hs-model" role="img" aria-label="Rotating exploded view of the missile pod, ice reactor and cannon; drag to turn"></canvas><div class="hs-model-note">'+(innerWidth>900?'DRAG TO TURN / SELECT A MODULE':'DRAG TO TURN / CHOOSE A PART')+'</div></div><nav class="hs-tabs" aria-label="B.O.B. modules">'+tabs+'</nav></div><div class="hs-details"><section class="hs-detail" data-detail="missile"><h2>01 / MISSILE POD</h2><canvas class="hs-detail-model" data-model="missile" aria-hidden="true"></canvas><dl><div class="hs-pair"><dt>ARMOR</dt><dd><span data-stat="missile"></span> HP / STEEL</dd></div><div><dt>ATTACK</dt><dd>GROUND MISSILES</dd></div><div><dt>COUNTER</dt><dd>LEAVE THE IMPACT RETINA</dd></div><div><dt>BREAK POD</dt><dd>STOPS GROUND STRIKES</dd></div></dl></section><section class="hs-detail is-selected" data-detail="core"><h2>02 / CRYO REACTOR</h2><canvas class="hs-detail-model" data-model="core" aria-hidden="true"></canvas><dl><div class="hs-pair"><dt>CORE</dt><dd><span data-stat="core"></span> HP / ICE</dd></div><div class="hs-pair"><dt>WEAK</dt><dd class="hs-advantage">FIRE X1.5</dd></div><div class="hs-pair"><dt>RESISTS</dt><dd class="hs-resistance">ICE X0.5</dd></div><div class="hs-pair"><dt>EXPOSED CORE</dt><dd class="hs-advantage">MISSILE X<span data-stat="coreMissile"></span></dd></div><div><dt>REACTOR ARMOR</dt><dd>BREAK BOTH PODS FIRST</dd></div></dl></section><section class="hs-detail" data-detail="cannon"><h2>03 / CANNON POD</h2><canvas class="hs-detail-model" data-model="cannon" aria-hidden="true"></canvas><dl><div class="hs-pair"><dt>ARMOR</dt><dd><span data-stat="cannon"></span> HP / STEEL</dd></div><div><dt>ATTACK</dt><dd>FOV CANNON VOLLEYS</dd></div><div><dt>COUNTER</dt><dd>GREEN AIM / YELLOW SET<br>RED: LEAVE THE LANE</dd></div><div><dt>BREAK POD</dt><dd>STOPS GUN VOLLEYS</dd></div></dl></section></div><div class="hs-objective">BREAK BOTH ARM PODS FIRST.</div><footer class="hs-footer"><div class="hs-tools"><button type="button" data-turn="-2" aria-label="Turn left">←</button><button type="button" class="hs-auto" aria-pressed="true">AUTO</button><button type="button" data-turn="2" aria-label="Turn right">→</button></div><div class="hs-hints">'+glyph('pad_dpad')+'<span class="hs-dpad-label">PART / TURN</span><button type="button" class="hs-full">'+glyph('pad_b')+'FULL UNIT</button></div><button type="button" class="hs-deploy" disabled>'+glyph('pad_a')+'<span>SCANNING</span></button></footer></div>';
 document.body.appendChild(root);
 root.addEventListener('mousedown',e=>{e.stopPropagation();Audio.init();});root.addEventListener('click',e=>e.stopPropagation());
 for(const b of root.querySelectorAll('[data-part]'))b.onclick=()=>hs21Select(+b.dataset.part);
 for(const b of root.querySelectorAll('[data-turn]'))b.onclick=()=>hs21Turn(+b.dataset.turn);
 root.querySelector('.hs-auto').onclick=()=>{HS21.rotating=HS21.reduced?.matches?false:!HS21.rotating;HS21.dirty=true;};
 root.querySelector('.hs-full').onclick=()=>hs21Select(0);
 root.querySelector('.hs-deploy').onclick=()=>{if(hs21Active()&&TUT.L.age>3.8)TUT.L._hsConfirm=true;};
 root.querySelector('.hs-pause').onclick=()=>{if(hs21Active()){const k=(keybindFor(1).start||[]).find(k=>!k.startsWith('mouse'));if(k)Input.injectTap(k);}};
 root.addEventListener('keydown',e=>{if(e.key==='Tab'){const buttons=[...root.querySelectorAll('button:not(:disabled)')],i=buttons.indexOf(document.activeElement);if(e.shiftKey&&i<=0){buttons[buttons.length-1].focus();e.preventDefault();}else if(!e.shiftKey&&i===buttons.length-1){buttons[0].focus();e.preventDefault();}}if(e.target.tagName==='BUTTON'&&(e.key==='Enter'||e.key===' '))e.stopPropagation();});
 const model=root.querySelector('.hs-model');model.addEventListener('pointerdown',e=>{if(!hs21Active())return;HS21.drag={id:e.pointerId,x:e.clientX,y:e.clientY,yaw:TUT.L.yaw};model.setPointerCapture(e.pointerId);e.preventDefault();});
 model.addEventListener('pointermove',e=>{const d=HS21.drag;if(!d||d.id!==e.pointerId||!hs21Active())return;TUT.L.yaw=(d.yaw+(e.clientX-d.x)/8+320)%32;HS21.dirty=true;});
 model.addEventListener('pointerup',e=>{const d=HS21.drag;HS21.drag=null;if(!d||!hs21Active())return;if(Math.hypot(e.clientX-d.x,e.clientY-d.y)<5){const r=model.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,q=HS21.targets.find(q=>x>=q.x&&x<=q.x+q.w&&y>=q.y&&y<=q.y+q.h);if(q)hs21Select(q.i);}if(model.hasPointerCapture(e.pointerId))model.releasePointerCapture(e.pointerId);});
 model.addEventListener('pointercancel',()=>HS21.drag=null);
 new ResizeObserver(()=>HS21.dirty=true).observe(root.querySelector('.hs-stage'));
}
function hs21Show(L){hs21Build();if(!HS21.root)return;hs21Warm();const newLesson=HS21.L!==L;if(newLesson){HS21.L=L;HS21.rotating=!HS21.reduced?.matches;HS21.lastInfo='';HS21.lastFrame='';HS21.dirty=true;}
 const opening=HS21.root.hidden;HS21.root.hidden=false;HS21.visible=true;document.body.classList.add('holoscan-open');if(opening){HS21.root.focus({preventScroll:true});HS21.dirty=true;}
 const selected=HS21.order[L.sel],ready=L.age>3.8&&!TUT.done,data=hs21Data(),auto=HS21.rotating&&!HS21.reduced?.matches,sig=JSON.stringify([L.sel,ready,!!TUT.done,auto,data]);
 if(HS21.lastInfo!==sig){HS21.lastInfo=sig;for(const e of HS21.root.querySelectorAll('[data-stat]'))e.textContent=data[e.dataset.stat];for(const b of HS21.root.querySelectorAll('[data-part]'))b.setAttribute('aria-pressed',+b.dataset.part===L.sel);
  for(const e of HS21.root.querySelectorAll('[data-detail]'))e.classList.toggle('is-selected',e.dataset.detail===(selected==='whole'?'core':selected));
  const deploy=HS21.root.querySelector('.hs-deploy');deploy.disabled=!ready;deploy.querySelector('span').textContent=TUT.done?'DEPLOYING':ready?'DEPLOY':'SCANNING';HS21.root.querySelector('.hs-scan-label').textContent=ready?'SCAN COMPLETE':'UNIT ANALYSIS MODE';HS21.root.querySelector('.hs-auto').setAttribute('aria-pressed',auto);HS21.dirty=true;
 }
 HS21.root.querySelector('.hs-progress span').style.transform='scaleX('+clamp(L.age/3.8,0,1)+')';
 const frame=[Math.floor(L.yaw)%32,L.sel].join('|');if(!document.hidden&&(HS21.dirty||HS21.lastFrame!==frame)){HS21.lastFrame=frame;HS21.dirty=false;hs21Draw(L);}
}
ic20CardDraw=function(L){if(typeof HTMLElement!=='function')return HS21.base.card.apply(this,arguments);hs21Show(L);};
ic20CardTick=function(L,dt){const stopped=!HS21.rotating||HS21.reduced?.matches||!!HS21.drag,r=HS21.base.tick.apply(this,arguments);if(stopped)L.yaw=(L.yaw-dt*10+32)%32;return r;};
tutNext=function(){hs21Hide(true);return HS21.base.next.apply(this,arguments);};
tutCleanup=function(){hs21Hide(true);return HS21.base.cleanup.apply(this,arguments);};
setState=function(s){const r=HS21.base.set.apply(this,arguments);hs21Sync();return r;};
if(typeof window!=='undefined')window.BOFHOLOSCAN={get visible(){return HS21.visible;},get frame(){return IC20.cardFrame;},get stats(){return hs21Data();},get ready(){return HS21.fontReady&&Object.values(HS21.art).every(a=>XART.rdy(a.key));}};
