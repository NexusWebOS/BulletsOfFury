/* ============================================================
   BOSS MODE — THE SCENE EDITOR (drop 0911a)

   Mike: "a boss editor section where it's a scene editor essentially, but with a grid/tile based
   system ... drag my boss across horizontally, vertically, diagonally, spin, rotate etc. ... zones
   where the boss would go, attack zones, safe zones for the player, and a list of the in-game
   projectiles to key to the boss, the flashes, the effects, etc."

   Loads after bossmode.js and hangs off window.BM. The document it edits is doc.scene, which is
   exactly what the engine's SCENE DIRECTOR consumes (assets/game.js, "THE SCENE DIRECTOR"), so
   APPLY puts it on the row and PLAY TEST runs it. Everything drawn on the canvas here is what the
   engine will do with the same numbers; nothing is a mock.

   Coordinates are TILES. The field is VW x VH (480 x 512) or the stage's world width on the wide
   stages; the cell size is the scene's own. The boss's position is its CENTRE, as in play.
   ============================================================ */
(function(){
'use strict';
const $=(s,el)=>(el||document).querySelector(s), $$=(s,el)=>Array.from((el||document).querySelectorAll(s));
const SCHEMA='bof-bossscene/1';
const TOOLS=[
  {id:'select',  icon:['pointmarkers','anchor-normal'],     tip:'SELECT / DRAG  (drag the boss, a waypoint or a zone; shift = free, no snap)'},
  {id:'waypoint',icon:['pointmarkers','waypoint-normal'],   tip:'WAYPOINT  (click to add a key at the end of the track; drag to place)'},
  {id:'zboss',   icon:['firinghitboxguides','hitbox-rectangle'], tip:'BOSS ZONE  (drag a rectangle the boss is fenced to between tracks)'},
  {id:'zattack', icon:['markers','fire-cone-wide'],         tip:'ATTACK ZONE  (drag a rectangle; telegraphed on the field; a fire action can aim at it)'},
  {id:'zsafe',   icon:['shields','shield-circle'],          tip:'SAFE ZONE  (drag a rectangle; enemy rounds entering it are removed)'},
  {id:'delete',  icon:['icons','delete'],                   tip:'DELETE  (click a waypoint or zone)'},
];
const PATHS=[ // the pack's pathing guides, as key generators relative to the selected key
  ['straight-right',(k,c)=>[{dx:6,dy:0}]], ['straight-down',(k,c)=>[{dx:0,dy:4}]], ['diagonal-down-right',(k,c)=>[{dx:5,dy:4}]],
  ['elbow',(k,c)=>[{dx:5,dy:0},{dx:5,dy:4}]], ['curve-quarter',(k,c)=>arc(0,4,4,-90,0,5)], ['u-turn',(k,c)=>arc(3,0,3,180,360,7)],
  ['s-curve',(k,c)=>[{dx:2,dy:1.5,e:'inout'},{dx:5,dy:2,e:'inout'},{dx:8,dy:3.5,e:'inout'}]],
  ['zigzag',(k,c)=>[{dx:2,dy:1},{dx:4,dy:-1},{dx:6,dy:1},{dx:8,dy:-1}].map(p=>({dx:p.dx,dy:p.dy+0}))],
  ['orbit-clockwise',(k,c)=>arc(0,3,3,-90,270,9)], ['orbit-counterclockwise',(k,c)=>arc(0,3,3,-90,-450,9)],
  ['figure-eight',(k,c)=>arc(0,2.5,2.5,-90,270,9).concat(arc(0,-2.5,2.5,90,-270,9))],
  ['patrol',(k,c)=>[{dx:-4,dy:0,hold:0.4},{dx:4,dy:0,hold:0.4},{dx:0,dy:0}]],
  ['bezier',(k,c)=>[{dx:2,dy:-2,e:'in'},{dx:5,dy:2,e:'out'},{dx:8,dy:-1,e:'inout'}]],
];
const MANEUVERS=[
  ['spin-clockwise',k=>[{rot:(k.rot||0)+180,t:0.5,e:'linear'},{rot:(k.rot||0)+360,t:0.5,e:'linear'}]],
  ['spin-counterclockwise',k=>[{rot:(k.rot||0)-180,t:0.5,e:'linear'},{rot:(k.rot||0)-360,t:0.5,e:'linear'}]],
  ['bank-left',k=>[{rot:(k.rot||0)-25,t:0.35,e:'inout'},{rot:(k.rot||0),t:0.35,e:'inout'}]],
  ['bank-right',k=>[{rot:(k.rot||0)+25,t:0.35,e:'inout'},{rot:(k.rot||0),t:0.35,e:'inout'}]],
  ['boost',k=>[{dy:5,t:0.35,e:'in'},{dy:0,t:0.9,e:'out'}]],
  ['strafe',k=>[{dx:4,t:0.4,e:'inout'},{dx:-4,t:0.8,e:'inout'},{dx:0,t:0.4,e:'inout'}]],
  ['evasive-zigzag',k=>[{dx:2,dy:1,t:0.25},{dx:-2,dy:2,t:0.25},{dx:2,dy:3,t:0.25},{dx:0,dy:4,t:0.25}]],
  ['orbit-target',k=>arc(0,3,3,-90,270,9).map(p=>Object.assign(p,{t:0.3}))],
];
function arc(cx,cy,r,a0,a1,n){ const out=[]; for(let i=1;i<=n;i++){ const a=(a0+(a1-a0)*i/n)*Math.PI/180; out.push({dx:cx+Math.cos(a)*r, dy:cy+Math.sin(a)*r}); } return out; }
const ZCOL={boss:'255,210,48', attack:'255,64,64', safe:'90,255,130'};
const S={ tool:'select', selKey:-1, selZone:-1, track:0, drag:null, hover:null, scale:1, cell:32, grid:true, snap:true,
          preview:{on:false,t:0,last:0}, showGuides:true, art:{}, pal:null };

function BM(){ return window.BM; }
function doc(){ return BM().state.doc; }
function api(){ return BM().host.api; }
function scene(){
  const d=doc(); if(!d) return null;
  if(!d.scene){ d.scene={schema:SCHEMA, grid:{cell:32, w:480, h:512}, ownFire:true, tracks:[], zones:[]}; }
  if(!d.scene.grid) d.scene.grid={cell:32,w:480,h:512};
  if(!d.scene.tracks) d.scene.tracks=[]; if(!d.scene.zones) d.scene.zones=[];
  return d.scene;
}
function track(){ const sc=scene(); if(!sc) return null; if(!sc.tracks.length) return null; S.track=Math.max(0,Math.min(sc.tracks.length-1,S.track)); return sc.tracks[S.track]; }
function keys(){ const t=track(); return t?t.keys:[]; }
function fieldW(){ const sc=scene(); return (sc&&sc.grid.w)||480; }
function fieldH(){ const sc=scene(); return (sc&&sc.grid.h)||512; }
function cell(){ const sc=scene(); return (sc&&sc.grid.cell)||32; }

/* ---- pack icons as CSS, on top of what bossmode.js already generated ---- */
const EXTRA_ATLASES=['pointmarkers','pathingguides','bulletpatterns','phaseemittertools','firinghitboxguides','markers','shields','maneuvericons','alerts-neonred','alerts-yellow','alerts-lightgreen','lines'];
async function loadExtra(){
  const B=BM();
  await Promise.all(EXTRA_ATLASES.map(n=>B.loadAtlas(n)));
  let css='';
  for(const n of EXTRA_ATLASES){
    const M=B.A[n].map; const cw=M.atlas.cell[0], ch=M.atlas.cell[1]; const sc=34/Math.max(cw,ch);
    for(const it of M.items) css+=B.cellRule('.pk[data-set="'+n+'"][data-name="'+it.name+'"]', n, it.name, sc);
    const sc2=64/Math.max(cw,ch);
    for(const it of M.items) css+=B.cellRule('.pk.lg[data-set="'+n+'"][data-name="'+it.name+'"]', n, it.name, sc2);
  }
  const st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
}
function packImg(n, name){ const B=BM(); const r=B.rectOf(n,name); if(!r) return null; const M=B.A[n]; const it=M.map.items.find(i=>i.name===name);
  const c=document.createElement('canvas'); const px=(it&&it.placement)?it.placement:[0,0], vs=(it&&it.visible_size)?it.visible_size:[r.w,r.h];
  c.width=vs[0]; c.height=vs[1]; c.getContext('2d').drawImage(M.img, r.x+px[0], r.y+px[1], vs[0], vs[1], 0,0,vs[0],vs[1]); return c; }
const MK={};
function marker(kind, state){ const k=kind+'-'+state; if(!MK[k]) MK[k]=packImg('pointmarkers',k)||packImg('pointmarkers',kind+'-normal'); return MK[k]; }
function alertImg(col, name){ const k='al-'+col+'-'+name; if(!MK[k]) MK[k]=packImg('alerts-'+col, name); return MK[k]; }

/* ---- the pane ---- */
function build(){
  const pane=$('#pane-scene');
  pane.innerHTML=
   '<div id="sc-tools">'+
     '<div class="sc-group" id="sc-toolbtns">'+TOOLS.map(t=>'<button class="scb" data-tool="'+t.id+'" title="'+t.tip+'"><span class="pk" data-set="'+t.icon[0]+'" data-name="'+t.icon[1]+'"></span></button>').join('')+'</div>'+
     '<div class="sc-group"><label>TRACK <select id="sc-track"></select></label><button class="tb" id="sc-newtrack">+ TRACK</button><button class="tb" id="sc-deltrack">✕</button>'+
       '<label>MODE <select id="sc-mode"><option>once</option><option>loop</option><option>pingpong</option></select></label>'+
       '<label>SPEED <input type="number" id="sc-speed" step="0.1" min="0.1" value="1" style="width:52px"></label>'+
       '<label>REPEAT <input type="number" id="sc-repeat" min="0" value="0" style="width:46px" title="0 = forever (loop/pingpong)"></label>'+
       '<label>TRIGGER <select id="sc-trig"><option value="start">start</option><option value="time">time</option><option value="phase">phase</option><option value="hp">hp below</option><option value="proximity">proximity</option></select><input type="number" id="sc-trigv" step="0.05" style="width:56px"></label></div>'+
     '<div class="sc-group"><label>CELL <select id="sc-cell"><option>16</option><option>24</option><option selected>32</option><option>48</option><option>64</option></select></label>'+
       '<label class="chk"><input type="checkbox" id="sc-grid" checked> GRID</label><label class="chk"><input type="checkbox" id="sc-snap" checked> SNAP</label>'+
       '<label class="chk"><input type="checkbox" id="sc-ownfire" checked> ENGINE PATTERNS TOO</label>'+
       '<button class="tb" id="sc-play"><span class="ico" data-icon="play"></span>PREVIEW</button><button class="tb" id="sc-stop"><span class="ico" data-icon="stop"></span></button>'+
       '<button class="tb on" id="sc-attach" title="Send the scene to the running boss without saving"><span class="ico" data-icon="boss"></span>ATTACH LIVE</button>'+
       '<button class="tb" id="sc-clear">CLEAR SCENE</button></div>'+
     '<div class="sc-group" id="sc-paths"><span class="sc-lbl">PATH</span>'+PATHS.map(p=>'<button class="scb" data-path="'+p[0]+'" title="'+p[0]+'"><span class="pk" data-set="pathingguides" data-name="'+p[0]+'"></span></button>').join('')+
       '<span class="sc-lbl">MOVE</span>'+MANEUVERS.map(p=>'<button class="scb" data-man="'+p[0]+'" title="'+p[0]+'"><span class="pk" data-set="maneuvericons" data-name="'+p[0]+'"></span></button>').join('')+'</div>'+
   '</div>'+
   '<div id="sc-main"><div id="sc-wrap"><canvas id="sc-cv"></canvas><div id="sc-readout"></div></div></div>'+
   '<div id="sc-time"><canvas id="sc-tl"></canvas></div>';
  // the scene inspector lives in the DOCK, so the field has the whole theater
  const dock=$('#dock-scene'); dock.innerHTML='<div id="sc-insp"></div>';
  $$('#sc-toolbtns .scb').forEach(b=>b.onclick=()=>{ S.tool=b.dataset.tool; $$('#sc-toolbtns .scb').forEach(x=>x.classList.toggle('on',x===b)); draw(); });
  $('#sc-toolbtns .scb').classList.add('on');
  $('#sc-track').onchange=e=>{ S.track=+e.target.value; S.selKey=-1; renderAll(); };
  $('#sc-newtrack').onclick=()=>{ const sc=scene(); if(!sc) return; BM().pushUndo(); sc.tracks.push({name:'track '+(sc.tracks.length+1), trigger:{type:'start'}, mode:'once', speed:1, repeat:0, keys:[]}); S.track=sc.tracks.length-1; S.selKey=-1; renderAll(); };
  $('#sc-deltrack').onclick=()=>{ const sc=scene(); if(!sc||!sc.tracks.length) return; BM().pushUndo(); sc.tracks.splice(S.track,1); S.track=0; S.selKey=-1; renderAll(); after(); };
  $('#sc-mode').onchange=e=>{ const t=track(); if(!t) return; BM().pushUndo(); t.mode=e.target.value; after(); };
  $('#sc-speed').onchange=e=>{ const t=track(); if(!t) return; BM().pushUndo(); t.speed=+e.target.value||1; after(); };
  $('#sc-repeat').onchange=e=>{ const t=track(); if(!t) return; BM().pushUndo(); t.repeat=+e.target.value||0; after(); };
  $('#sc-trig').onchange=e=>{ const t=track(); if(!t) return; BM().pushUndo(); t.trigger=t.trigger||{}; t.trigger.type=e.target.value; after(); renderTop(); };
  $('#sc-trigv').onchange=e=>{ const t=track(); if(!t) return; BM().pushUndo(); t.trigger=t.trigger||{type:'start'}; const v=+e.target.value; if(t.trigger.type==='time') t.trigger.t=v; else if(t.trigger.type==='phase') t.trigger.phase=v|0; else if(t.trigger.type==='hp') t.trigger.hp=v; else if(t.trigger.type==='proximity') t.trigger.dist=v; after(); };
  $('#sc-cell').onchange=e=>{ const sc=scene(); if(!sc) return; BM().pushUndo(); rescale(sc, +e.target.value); after(); };
  $('#sc-grid').onchange=e=>{ S.grid=e.target.checked; draw(); };
  $('#sc-snap').onchange=e=>{ S.snap=e.target.checked; };
  $('#sc-ownfire').onchange=e=>{ const sc=scene(); if(!sc) return; BM().pushUndo(); sc.ownFire=e.target.checked; after(); };
  $('#sc-play').onclick=()=>{ S.preview.on=!S.preview.on; S.preview.t=0; S.preview.last=performance.now(); $('#sc-play').classList.toggle('on',S.preview.on); };
  $('#sc-stop').onclick=()=>{ S.preview.on=false; S.preview.t=0; $('#sc-play').classList.remove('on'); draw(); };
  $('#sc-attach').onclick=()=>{ const sc=scene(); if(!sc||!api()) return; const r=api().scene.attach(JSON.parse(JSON.stringify(sc))); BM().msg(r?'scene attached to the live boss':'no live boss to attach to - PLAY TEST first', !r); };
  $('#sc-clear').onclick=()=>{ const d=doc(); if(!d) return; if(!confirm('Clear every track and zone of this scene?')) return; BM().pushUndo(); d.scene={schema:SCHEMA, grid:{cell:cell(), w:fieldW(), h:fieldH()}, ownFire:true, tracks:[], zones:[]}; S.selKey=-1; S.selZone=-1; renderAll(); after(); };
  $$('#sc-paths [data-path]').forEach(b=>b.onclick=()=>addPath(b.dataset.path));
  $$('#sc-paths [data-man]').forEach(b=>b.onclick=()=>addManeuver(b.dataset.man));
  const cv=$('#sc-cv');
  cv.onmousedown=onDown; cv.onmousemove=onMove; window.addEventListener('mouseup', onUp); cv.oncontextmenu=e=>e.preventDefault();
  cv.onwheel=e=>{ if(!e.ctrlKey) return; e.preventDefault(); };
  $('#sc-tl').onmousedown=onTimeline;
  window.addEventListener('keydown', e=>{ if(!$('#pane-scene').classList.contains('on')) return; if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT'||e.target.tagName==='TEXTAREA') return;
    if(e.key==='Delete'||e.key==='Backspace'){ delSelected(); e.preventDefault(); }
    else if(e.key==='r'||e.key==='R'){ rotSel(e.shiftKey?-15:15); }
    else if(e.key==='g'){ S.grid=!S.grid; $('#sc-grid').checked=S.grid; draw(); }
    else if(e.key===' '){ $('#sc-play').click(); e.preventDefault(); }
    else if(e.key==='ArrowLeft'||e.key==='ArrowRight'||e.key==='ArrowUp'||e.key==='ArrowDown'){ nudge(e.key, e.shiftKey?1:0.25); e.preventDefault(); }
    else if(e.key==='1'){ S.tool='select'; syncTool(); } else if(e.key==='2'){ S.tool='waypoint'; syncTool(); }
  });
  requestAnimationFrame(tickPreview);
}
function syncTool(){ $$('#sc-toolbtns .scb').forEach(x=>x.classList.toggle('on',x.dataset.tool===S.tool)); draw(); }
function after(){ renderInsp(); draw(); drawTimeline(); if($('#p-live').checked) BM().applyDoc({}); BM().renderJSON(); }
function rescale(sc, newCell){ const old=sc.grid.cell||32, f=old/newCell; for(const t of sc.tracks) for(const k of t.keys){ k.x=+(k.x*f).toFixed(3); k.y=+(k.y*f).toFixed(3); } for(const z of sc.zones){ z.x=+(z.x*f).toFixed(3); z.y=+(z.y*f).toFixed(3); z.w=+(z.w*f).toFixed(3); z.h=+(z.h*f).toFixed(3); } sc.grid.cell=newCell; }

/* ---- geometry ---- */
function fit(){ const wrap=$('#sc-wrap'); const W=wrap.clientWidth-4, H=wrap.clientHeight-4; const fw=fieldW(), fh=fieldH(); S.scale=Math.max(0.5, Math.min(W/fw, H/fh)); const cv=$('#sc-cv'); cv.width=Math.round(fw*S.scale); cv.height=Math.round(fh*S.scale); }
function toPx(tx,ty){ return [tx*cell()*S.scale, ty*cell()*S.scale]; }
function toTile(px,py){ return [px/(cell()*S.scale), py/(cell()*S.scale)]; }
function snapT(v){ return S.snap? Math.round(v*2)/2 : +v.toFixed(3); }
function bossSize(){ const d=doc(); return [(d&&d.size.w)||160, (d&&d.size.h)||120]; }
function bossPose(){ // where the boss sits in the editor: the selected key, else the preview pose, else the first key, else stage centre
  const ks=keys();
  if(S.preview.on && ks.length) return previewPose(S.preview.t);
  if(S.selKey>=0 && ks[S.selKey]) { const k=ks[S.selKey]; return {x:+k.x, y:+k.y, rot:+k.rot||0, sx:(k.sx!=null&&k.sx!=='')?+k.sx:1, sy:(k.sy!=null&&k.sy!=='')?+k.sy:1}; }
  if(ks.length){ const k=ks[0]; return {x:+k.x, y:+k.y, rot:+k.rot||0, sx:1, sy:1}; }
  const d=doc(); const ty=(d&&d.size.ty!=null&&d.size.ty!=='')?+d.size.ty:fieldH()*0.24; return {x:fieldW()/2/cell(), y:ty/cell(), rot:0, sx:1, sy:1};
}
/* the editor's own interpolator, the same rules as sceneDirectorTick, for scrubbing without the engine */
function previewPose(t){
  const tr=track(); const ks=tr?tr.keys:[]; if(!ks.length) return bossPoseStatic();
  const spd=Math.max(0.05,+tr.speed||1); let from={x:+ks[0].x,y:+ks[0].y,rot:0,sx:1,sy:1}; let clock=0;
  const d=doc(); const start={x:fieldW()/2/cell(), y:((d&&d.size.ty!=null&&d.size.ty!=='')?+d.size.ty:fieldH()*0.24)/cell(), rot:0,sx:1,sy:1};
  from=start;
  let i=0, dir=1, loops=0;
  for(let guard=0; guard<400; guard++){
    const k=ks[i]; if(!k) break;
    const dur=Math.max(0.0001,(k.t!=null?+k.t:1)/spd), hold=(+k.hold||0)/spd;
    const tgt={x:+k.x,y:+k.y,rot:+k.rot||0,sx:(k.sx!=null&&k.sx!=='')?+k.sx:1,sy:(k.sy!=null&&k.sy!=='')?+k.sy:1};
    if(t<clock+dur){ const p=(t-clock)/dur, e=ease(k.ease,p); return {x:from.x+(tgt.x-from.x)*e, y:from.y+(tgt.y-from.y)*e, rot:from.rot+(tgt.rot-from.rot)*e, sx:from.sx+(tgt.sx-from.sx)*e, sy:from.sy+(tgt.sy-from.sy)*e, key:i, p:p}; }
    clock+=dur; if(t<clock+hold) return Object.assign({key:i,p:1},tgt);
    clock+=hold; from=tgt;
    let n=i+dir;
    if(n>=ks.length||n<0){ loops++; const rep=+tr.repeat||0; if(tr.mode==='loop'&&!(rep&&loops>=rep)) n=0; else if(tr.mode==='pingpong'&&!(rep&&loops>=rep)){ dir=-dir; n=i+dir; if(n<0||n>=ks.length) n=i; } else return Object.assign({key:i,p:1,end:true},tgt); }
    i=n;
  }
  return Object.assign({key:i,p:1},from);
}
function bossPoseStatic(){ const d=doc(); const ty=(d&&d.size.ty!=null&&d.size.ty!=='')?+d.size.ty:fieldH()*0.24; return {x:fieldW()/2/cell(), y:ty/cell(), rot:0, sx:1, sy:1}; }
function ease(kind,p){ if(kind==='in') return p*p; if(kind==='out') return 1-(1-p)*(1-p); if(kind==='inout') return p<0.5?2*p*p:1-Math.pow(-2*p+2,2)/2; return p; }
function trackLength(){ const tr=track(); if(!tr) return 0; const spd=Math.max(0.05,+tr.speed||1); return tr.keys.reduce((s,k)=>s+((k.t!=null?+k.t:1)+(+k.hold||0))/spd,0); }

/* ---- drawing ---- */
function draw(){
  const cv=$('#sc-cv'); if(!cv||!$('#pane-scene').classList.contains('on')) return;
  fit(); const x=cv.getContext('2d'); const W=cv.width, H=cv.height, c=cell()*S.scale;
  x.clearRect(0,0,W,H); x.fillStyle='#0c0e13'; x.fillRect(0,0,W,H);
  // a faint stage plate: the play field band
  x.fillStyle='rgba(30,34,44,0.6)'; x.fillRect(0,0,W,H);
  if(S.grid){ x.strokeStyle='rgba(74,168,255,0.16)'; x.lineWidth=1; x.beginPath(); for(let gx=0;gx<=W+0.5;gx+=c){ x.moveTo(Math.round(gx)+0.5,0); x.lineTo(Math.round(gx)+0.5,H); } for(let gy=0;gy<=H+0.5;gy+=c){ x.moveTo(0,Math.round(gy)+0.5); x.lineTo(W,Math.round(gy)+0.5); } x.stroke();
    x.strokeStyle='rgba(74,168,255,0.34)'; x.beginPath(); for(let gx=0;gx<=W+0.5;gx+=c*4){ x.moveTo(Math.round(gx)+0.5,0); x.lineTo(Math.round(gx)+0.5,H); } for(let gy=0;gy<=H+0.5;gy+=c*4){ x.moveTo(0,Math.round(gy)+0.5); x.lineTo(W,Math.round(gy)+0.5); } x.stroke(); }
  // the player's lane, for scale
  x.fillStyle='rgba(141,226,58,0.08)'; x.fillRect(0, H*0.72, W, H*0.28);
  x.fillStyle='rgba(141,226,58,0.5)'; x.font='10px monospace'; x.fillText('player lane', 6, H*0.72+12);
  const sc=scene(); if(!sc) return;
  // zones
  sc.zones.forEach((z,i)=>{ const [zx,zy]=toPx(z.x,z.y), zw=z.w*c, zh=z.h*c; const rgb=ZCOL[z.type]||ZCOL.boss; const sel=(i===S.selZone);
    x.fillStyle='rgba('+rgb+','+(sel?0.28:0.14)+')'; x.fillRect(zx,zy,zw,zh); x.strokeStyle='rgba('+rgb+','+(sel?1:0.75)+')'; x.lineWidth=sel?2:1.5; x.setLineDash([6,4]); x.strokeRect(zx+0.5,zy+0.5,zw-1,zh-1); x.setLineDash([]);
    x.fillStyle='rgba('+rgb+',0.95)'; x.font='bold 10px monospace'; x.fillText(z.type.toUpperCase()+' · '+z.name, zx+4, zy+12);
    const col=z.type==='safe'?'lightgreen':(z.type==='attack'?'neonred':'yellow'); const sym=z.type==='attack'?(z.symbol||'danger'):null;
    if(sym){ const im=alertImg(col,sym); if(im){ const s=Math.max(14,Math.min(40,zw*0.4,zh*0.4)); x.globalAlpha=0.8; x.drawImage(im, zx+zw/2-s/2, zy+zh/2-s/2, s, s); x.globalAlpha=1; } }
    if(z.type==='attack' && (z.telegraph==='fov'||z.telegraph==='fovtall')){ // the cone, from the boss anchor to the zone, as the engine draws it
      const P=bossPose(); const [bx,by]=toPx(P.x,P.y); const [bw,bh]=bossSize(); const d=doc(); const a=(d&&d.anchors&&d.anchors[z.anchor||'C'])||[0,0.4];
      const ax=bx+a[0]*bw*S.scale, ay=by+a[1]*bh*S.scale; const h=Math.max(30,(zy+zh)-ay), w=h*(z.telegraph==='fovtall'?0.5:1)*1.25;
      x.fillStyle='rgba(255,64,64,0.18)'; x.beginPath(); x.moveTo(ax,ay); x.lineTo(ax-w/2,ay+h); x.lineTo(ax+w/2,ay+h); x.closePath(); x.fill(); }
  });
  // the path
  const ks=keys(); const tr=track();
  if(ks.length){ x.strokeStyle='rgba(74,168,255,0.85)'; x.lineWidth=2; x.beginPath(); const p0=bossPoseStatic(); const [sx0,sy0]=toPx(p0.x,p0.y); x.moveTo(sx0,sy0);
    ks.forEach(k=>{ const [px,py]=toPx(+k.x,+k.y); x.lineTo(px,py); }); x.stroke();
    // direction ticks
    for(let i=0;i<ks.length;i++){ const a=i?toPx(+ks[i-1].x,+ks[i-1].y):[sx0,sy0], b=toPx(+ks[i].x,+ks[i].y); const ang=Math.atan2(b[1]-a[1],b[0]-a[0]); const mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2; x.save(); x.translate(mx,my); x.rotate(ang); x.fillStyle='rgba(74,168,255,0.9)'; x.beginPath(); x.moveTo(6,0); x.lineTo(-4,-4); x.lineTo(-4,4); x.closePath(); x.fill(); x.restore(); }
  }
  // the boss
  const P=bossPose(); const [bx,by]=toPx(P.x,P.y); const [bw,bh]=bossSize();
  x.save(); x.translate(bx,by); x.rotate((P.rot||0)*Math.PI/180); x.scale(P.sx||1,P.sy||1);
  const im=plateImg(); const dw=bw*S.scale, dh=bh*S.scale;
  if(im){ x.imageSmoothingEnabled=false; x.drawImage(im,-dw/2,-dh/2,dw,dh); } else { x.fillStyle='rgba(255,138,30,0.25)'; x.fillRect(-dw/2,-dh/2,dw,dh); }
  x.strokeStyle='rgba(141,226,58,0.8)'; x.setLineDash([5,3]); x.strokeRect(-dw/2,-dh/2,dw,dh); x.setLineDash([]);
  // anchors on the hull
  const d=doc(); if(d&&d.anchors){ for(const nm in d.anchors){ const a=d.anchors[nm]; const mx=a[0]*dw, my=a[1]*dh; const mk=marker('muzzle','normal'); if(mk) x.drawImage(mk, mx-9, my-9, 18, 18); x.fillStyle='#ffc21a'; x.font='9px monospace'; x.fillText(nm, mx+8, my-6); } }
  x.restore();
  // rotation handle above the hull
  const hr=Math.max(dw,dh)*0.62; const hx=bx+Math.sin((P.rot||0)*Math.PI/180)*hr, hy=by-Math.cos((P.rot||0)*Math.PI/180)*hr;
  x.strokeStyle='rgba(255,194,26,0.6)'; x.beginPath(); x.moveTo(bx,by); x.lineTo(hx,hy); x.stroke(); x.fillStyle='#ffc21a'; x.beginPath(); x.arc(hx,hy,6,0,Math.PI*2); x.fill(); x.fillStyle='#000'; x.font='bold 8px monospace'; x.textAlign='center'; x.fillText('R',hx,hy+3); x.textAlign='left';
  // waypoints
  ks.forEach((k,i)=>{ const [px,py]=toPx(+k.x,+k.y); const st=(i===S.selKey)?'selected':((S.hover&&S.hover.type==='key'&&S.hover.i===i)?'hover':'normal'); const mk=marker('waypoint',st); if(mk) x.drawImage(mk,px-11,py-11,22,22); else { x.fillStyle='#4aa8ff'; x.beginPath(); x.arc(px,py,6,0,Math.PI*2); x.fill(); }
    x.fillStyle='#e8eef8'; x.font='bold 10px monospace'; x.fillText(String(i+1), px+12, py-10);
    if(k.actions&&k.actions.length){ const mk2=marker('muzzle','selected'); if(mk2) x.drawImage(mk2,px+8,py+4,14,14); }
    if(k.rot){ x.fillStyle='#ffc21a'; x.font='9px monospace'; x.fillText((+k.rot).toFixed(0)+'°', px+12, py+24); } });
  // drag rubber band for zones
  if(S.drag&&S.drag.type==='zone-new'){ const a=S.drag.a, b=S.drag.b; if(b){ const rgb=ZCOL[S.drag.ztype]; x.fillStyle='rgba('+rgb+',0.2)'; x.strokeStyle='rgba('+rgb+',0.9)'; const [ax,ay]=toPx(Math.min(a[0],b[0]),Math.min(a[1],b[1])), [bx2,by2]=toPx(Math.max(a[0],b[0]),Math.max(a[1],b[1])); x.fillRect(ax,ay,bx2-ax,by2-ay); x.strokeRect(ax,ay,bx2-ax,by2-ay); } }
  // readout
  const ro=$('#sc-readout'); const tl=trackLength();
  ro.textContent=(tr?('track "'+tr.name+'" · '+ks.length+' keys · '+tl.toFixed(2)+'s · '+tr.mode):'no track')+'   ·   boss ('+P.x.toFixed(2)+', '+P.y.toFixed(2)+') tiles  rot '+(P.rot||0).toFixed(0)+'°'+(S.preview.on?('   ·   PREVIEW '+S.preview.t.toFixed(2)+'s'):'')+(S.hover&&S.hover.tile?('   ·   cursor '+S.hover.tile[0].toFixed(2)+', '+S.hover.tile[1].toFixed(2)):'');
}
function plateImg(){ const d=doc(); if(!d||!api()) return null; const k=d.states[0].key; if(!k) return null; try{ if(api().art.rdy(k)) return api().art.raw(k); }catch(e){} setTimeout(draw,300); return null; }
function drawTimeline(){
  const cv=$('#sc-tl'); if(!cv) return; const wrap=$('#sc-time'); cv.width=wrap.clientWidth-4; cv.height=44; const x=cv.getContext('2d'); x.fillStyle='#0c0e13'; x.fillRect(0,0,cv.width,cv.height);
  const tr=track(); if(!tr){ x.fillStyle='#6f7f8f'; x.font='10px monospace'; x.fillText('no track - add one with + TRACK, then click WAYPOINTS on the field', 8, 26); return; }
  const L=Math.max(0.001,trackLength()), spd=Math.max(0.05,+tr.speed||1); const px=t=>10+(cv.width-20)*(t/L);
  x.strokeStyle='#2a2d35'; x.beginPath(); x.moveTo(10,30); x.lineTo(cv.width-10,30); x.stroke();
  let clock=0; tr.keys.forEach((k,i)=>{ const dur=((k.t!=null?+k.t:1))/spd, hold=(+k.hold||0)/spd; const a=px(clock), b=px(clock+dur), c2=px(clock+dur+hold);
    x.fillStyle='rgba(74,168,255,0.55)'; x.fillRect(a,24,Math.max(2,b-a),12); if(hold>0){ x.fillStyle='rgba(255,194,26,0.5)'; x.fillRect(b,24,c2-b,12); }
    const mk=marker('waypoint', i===S.selKey?'selected':'normal'); if(mk) x.drawImage(mk, b-9, 4, 18, 18); x.fillStyle='#cfd6e0'; x.font='9px monospace'; x.fillText(String(i+1), b+10, 12); if(k.actions&&k.actions.length){ x.fillStyle='#ff8a1e'; x.fillText('▲'+k.actions.length, b+10, 22); }
    clock+=dur+hold; });
  x.fillStyle='#6f7f8f'; x.font='9px monospace'; x.fillText('0s', 4, 42); x.textAlign='right'; x.fillText(L.toFixed(2)+'s', cv.width-4, 42); x.textAlign='left';
  if(S.preview.on){ const p=px(Math.min(S.preview.t,L)); x.strokeStyle='#8de23a'; x.lineWidth=2; x.beginPath(); x.moveTo(p,2); x.lineTo(p,42); x.stroke(); }
}
function onTimeline(e){ const cv=$('#sc-tl'); const r=cv.getBoundingClientRect(); const L=Math.max(0.001,trackLength()); const t=((e.clientX-r.left)-10)/(cv.width-20)*L; const P=previewPose(Math.max(0,t)); if(P&&P.key!=null){ S.selKey=P.key; } S.preview.t=Math.max(0,Math.min(L,t)); S.preview.on=false; $('#sc-play').classList.remove('on'); renderInsp(); draw(); drawTimeline(); }
function tickPreview(){ if(S.preview.on){ const now=performance.now(); S.preview.t+=(now-S.preview.last)/1000; S.preview.last=now; const L=trackLength(); const tr=track(); if(tr&&tr.mode==='once'&&S.preview.t>L+0.5){ S.preview.t=0; } draw(); drawTimeline(); } requestAnimationFrame(tickPreview); }

/* ---- mouse ---- */
function pos(e){ const cv=$('#sc-cv'); const r=cv.getBoundingClientRect(); return [e.clientX-r.left, e.clientY-r.top]; }
function hitTest(px,py){
  const ks=keys(); for(let i=ks.length-1;i>=0;i--){ const [kx,ky]=toPx(+ks[i].x,+ks[i].y); if(Math.hypot(px-kx,py-ky)<12) return {type:'key',i:i}; }
  const P=bossPose(); const [bx,by]=toPx(P.x,P.y); const [bw,bh]=bossSize(); const hr=Math.max(bw,bh)*S.scale*0.62; const hx=bx+Math.sin((P.rot||0)*Math.PI/180)*hr, hy=by-Math.cos((P.rot||0)*Math.PI/180)*hr;
  if(Math.hypot(px-hx,py-hy)<10) return {type:'rot'};
  if(Math.abs(px-bx)<bw*S.scale/2 && Math.abs(py-by)<bh*S.scale/2) return {type:'boss'};
  const sc=scene(); for(let i=sc.zones.length-1;i>=0;i--){ const z=sc.zones[i]; const [zx,zy]=toPx(z.x,z.y); const zw=z.w*cell()*S.scale, zh=z.h*cell()*S.scale; if(px>=zx&&px<=zx+zw&&py>=zy&&py<=zy+zh){ const edge=(px>zx+zw-10&&py>zy+zh-10); return {type:'zone',i:i,resize:edge}; } }
  return null;
}
function onDown(e){
  const sc=scene(); if(!sc) return; const [px,py]=pos(e); const [tx,ty]=toTile(px,py); const h=hitTest(px,py);
  if(S.tool==='delete'){ if(h&&h.type==='key'){ BM().pushUndo(); keys().splice(h.i,1); S.selKey=-1; after(); } else if(h&&h.type==='zone'){ BM().pushUndo(); sc.zones.splice(h.i,1); S.selZone=-1; after(); } return; }
  if(S.tool==='waypoint'){ let tr=track(); if(!tr){ sc.tracks.push({name:'track 1',trigger:{type:'start'},mode:'once',speed:1,repeat:0,keys:[]}); S.track=0; tr=sc.tracks[0]; renderTop(); }
    BM().pushUndo(); const last=tr.keys[tr.keys.length-1]; const k={x:snapT(tx), y:snapT(ty), rot:last?+last.rot||0:0, t:1, hold:0, ease:'inout', actions:[]}; tr.keys.push(k); S.selKey=tr.keys.length-1; S.selZone=-1; S.drag={type:'key',i:S.selKey,shift:e.shiftKey}; after(); return; }
  if(S.tool==='zboss'||S.tool==='zattack'||S.tool==='zsafe'){ S.drag={type:'zone-new', ztype:S.tool.slice(1), a:[snapT(tx),snapT(ty)], b:null}; return; }
  // select
  if(h&&h.type==='key'){ S.selKey=h.i; S.selZone=-1; S.drag={type:'key',i:h.i,shift:e.shiftKey}; BM().pushUndo(); }
  else if(h&&h.type==='rot'){ S.drag={type:'rot'}; BM().pushUndo(); if(S.selKey<0&&keys().length) S.selKey=0; }
  else if(h&&h.type==='boss'){ // dragging the boss moves the selected key, or creates the first one
    if(S.selKey<0){ let tr=track(); if(!tr){ sc.tracks.push({name:'track 1',trigger:{type:'start'},mode:'once',speed:1,repeat:0,keys:[]}); S.track=0; tr=sc.tracks[0]; renderTop(); } if(!tr.keys.length){ const P=bossPose(); tr.keys.push({x:snapT(P.x),y:snapT(P.y),rot:0,t:1,hold:0,ease:'inout',actions:[]}); } S.selKey=tr.keys.length-1; }
    BM().pushUndo(); S.drag={type:'key',i:S.selKey,shift:e.shiftKey}; }
  else if(h&&h.type==='zone'){ S.selZone=h.i; S.selKey=-1; BM().pushUndo(); const z=sc.zones[h.i]; S.drag={type:h.resize?'zone-size':'zone-move', i:h.i, off:[tx-z.x, ty-z.y], shift:e.shiftKey}; }
  else { S.selKey=-1; S.selZone=-1; }
  renderInsp(); draw(); drawTimeline();
}
function onMove(e){
  const [px,py]=pos(e); const [tx,ty]=toTile(px,py); S.hover=hitTest(px,py)||{}; S.hover.tile=[tx,ty];
  const cv=$('#sc-cv'); cv.className = S.drag ? 'c-grabbing' : ((S.hover.type==='key'||S.hover.type==='boss')?'c-move':(S.hover.type==='rot'?'c-precision':(S.tool==='select'?'c-pointer':'c-precision')));
  if(!S.drag){ draw(); return; }
  const sc=scene(); const D=S.drag; const free=(e.shiftKey||D.shift);
  if(D.type==='key'){ const k=keys()[D.i]; if(!k) return; k.x=free?+tx.toFixed(3):snapT(tx); k.y=free?+ty.toFixed(3):snapT(ty); }
  else if(D.type==='rot'){ const k=keys()[S.selKey]; if(!k) return; const P=bossPose(); const [bx,by]=toPx(P.x,P.y); let ang=Math.atan2(px-bx, -(py-by))*180/Math.PI; if(!free) ang=Math.round(ang/15)*15; k.rot=+ang.toFixed(1); }
  else if(D.type==='zone-new'){ D.b=[free?+tx.toFixed(3):snapT(tx), free?+ty.toFixed(3):snapT(ty)]; }
  else if(D.type==='zone-move'){ const z=sc.zones[D.i]; z.x=free?+(tx-D.off[0]).toFixed(3):snapT(tx-D.off[0]); z.y=free?+(ty-D.off[1]).toFixed(3):snapT(ty-D.off[1]); }
  else if(D.type==='zone-size'){ const z=sc.zones[D.i]; z.w=Math.max(0.5, free?+(tx-z.x).toFixed(3):snapT(tx-z.x)); z.h=Math.max(0.5, free?+(ty-z.y).toFixed(3):snapT(ty-z.y)); }
  draw(); renderInsp(true);
}
function onUp(e){
  if(!S.drag) return; const D=S.drag; S.drag=null; const sc=scene(); if(!sc) return;
  if(D.type==='zone-new'){ if(D.b){ const x0=Math.min(D.a[0],D.b[0]), y0=Math.min(D.a[1],D.b[1]); const w=Math.abs(D.b[0]-D.a[0]), h=Math.abs(D.b[1]-D.a[1]); if(w>=0.5&&h>=0.5){ BM().pushUndo(); let n=1; while(sc.zones.some(z=>z.name===D.ztype+n)) n++; const z={name:D.ztype+n, type:D.ztype, x:x0, y:y0, w:w, h:h}; if(D.ztype==='attack'){ z.telegraph='rect'; z.symbol='danger'; z.anchor='C'; } if(D.ztype==='safe'){ z.enforce=true; } sc.zones.push(z); S.selZone=sc.zones.length-1; S.selKey=-1; } } }
  after();
}
function nudge(key, amt){ const k=keys()[S.selKey]; const z=scene().zones[S.selZone]; const t=k||z; if(!t) return; BM().pushUndo(); if(key==='ArrowLeft') t.x=+(t.x-amt).toFixed(3); if(key==='ArrowRight') t.x=+(t.x+amt).toFixed(3); if(key==='ArrowUp') t.y=+(t.y-amt).toFixed(3); if(key==='ArrowDown') t.y=+(t.y+amt).toFixed(3); after(); }
function rotSel(d){ const k=keys()[S.selKey]; if(!k) return; BM().pushUndo(); k.rot=+((+k.rot||0)+d).toFixed(1); after(); }
function delSelected(){ const sc=scene(); if(S.selKey>=0){ BM().pushUndo(); keys().splice(S.selKey,1); S.selKey=-1; after(); } else if(S.selZone>=0){ BM().pushUndo(); sc.zones.splice(S.selZone,1); S.selZone=-1; after(); } }
function addPath(name){ const sc=scene(); if(!sc) return; let tr=track(); if(!tr){ sc.tracks.push({name:'track 1',trigger:{type:'start'},mode:'once',speed:1,repeat:0,keys:[]}); S.track=0; tr=sc.tracks[0]; renderTop(); }
  BM().pushUndo(); const P=(S.selKey>=0&&tr.keys[S.selKey])?tr.keys[S.selKey]:(tr.keys.length?tr.keys[tr.keys.length-1]:bossPoseStatic()); const gen=PATHS.find(p=>p[0]===name)[1](P, cell());
  const at=(S.selKey>=0)?S.selKey+1:tr.keys.length;
  const ks=gen.map(g=>({x:+(+P.x+g.dx).toFixed(3), y:+(+P.y+g.dy).toFixed(3), rot:+P.rot||0, t:+(g.t!=null?g.t:0.5).toFixed(2), hold:g.hold||0, ease:g.e||'inout', actions:[]}));
  tr.keys.splice(at,0,...ks); S.selKey=at+ks.length-1; after(); }
function addManeuver(name){ const sc=scene(); if(!sc) return; let tr=track(); if(!tr){ sc.tracks.push({name:'track 1',trigger:{type:'start'},mode:'once',speed:1,repeat:0,keys:[]}); S.track=0; tr=sc.tracks[0]; renderTop(); }
  BM().pushUndo(); const P=(S.selKey>=0&&tr.keys[S.selKey])?tr.keys[S.selKey]:(tr.keys.length?tr.keys[tr.keys.length-1]:bossPoseStatic()); const gen=MANEUVERS.find(p=>p[0]===name)[1](P);
  const at=(S.selKey>=0)?S.selKey+1:tr.keys.length;
  const ks=gen.map(g=>({x:+(+P.x+(g.dx||0)).toFixed(3), y:+(+P.y+(g.dy||0)).toFixed(3), rot:(g.rot!=null)?+g.rot:(+P.rot||0), t:+(g.t!=null?g.t:0.5), hold:g.hold||0, ease:g.e||'inout', actions:[]}));
  tr.keys.splice(at,0,...ks); S.selKey=at+ks.length-1; after(); }

/* ---- the scene inspector (right of the field) ---- */
function fld(label,id,val,type,extra){ return '<div class="f"><label>'+label+'</label><input data-s="'+id+'" type="'+(type||'text')+'" value="'+(val==null?'':String(val).replace(/"/g,'&quot;'))+'" '+(extra||'')+'></div>'; }
function sel(label,id,val,opts,blank){ return '<div class="f"><label>'+label+'</label><select data-s="'+id+'">'+(blank?'<option value="">'+blank+'</option>':'')+opts.map(o=>{ const v=Array.isArray(o)?o[0]:o, t=Array.isArray(o)?o[1]:o; return '<option value="'+v+'"'+(String(v)===String(val)?' selected':'')+'>'+t+'</option>'; }).join('')+'</select></div>'; }
function palette(){ if(S.pal) return S.pal; if(!api()) return {muzzle:[],explode:[],round:[],kinds:[],sfx:[]}; try{ const fx=api().scene.fx(); S.pal={muzzle:fx.muzzle, explode:fx.explode, round:fx.round, kinds:api().scene.kinds(), sfx:api().scene.sfx()}; }catch(e){ S.pal={muzzle:[],explode:[],round:[],kinds:[],sfx:[]}; } return S.pal; }
function renderTop(){
  const sc=scene(); const ts=$('#sc-track'); if(!ts) return; ts.innerHTML=(sc?sc.tracks:[]).map((t,i)=>'<option value="'+i+'"'+(i===S.track?' selected':'')+'>'+(t.name||('track '+(i+1)))+'</option>').join('')||'<option value="0">(none)</option>';
  const tr=track(); $('#sc-mode').value=tr?(tr.mode||'once'):'once'; $('#sc-speed').value=tr?(tr.speed||1):1; $('#sc-repeat').value=tr?(tr.repeat||0):0;
  const T=(tr&&tr.trigger)||{type:'start'}; $('#sc-trig').value=T.type||'start'; $('#sc-trigv').value=(T.type==='time')?(T.t||0):(T.type==='phase')?(T.phase||0):(T.type==='hp')?(T.hp!=null?T.hp:0.5):(T.type==='proximity')?(T.dist||160):''; $('#sc-trigv').disabled=(T.type==='start'||!T.type);
  $('#sc-cell').value=String(cell()); $('#sc-ownfire').checked=!(sc&&sc.ownFire===false);
}
function renderInsp(quiet){
  const el=$('#sc-insp'); if(!el) return; const sc=scene(); const d=doc(); if(!sc||!d){ el.innerHTML='<div class="hint">open a fight first</div>'; return; }
  if(quiet && S.drag){ // live numbers only while dragging
    const k=keys()[S.selKey], z=sc.zones[S.selZone]; const t=k||z; if(!t) return; $$('[data-s]',el).forEach(i=>{ const p=i.dataset.s.split('.'); if(p.length===1 && t[p[0]]!=null && document.activeElement!==i) i.value=t[p[0]]; }); return; }
  const P=palette(); const anchors=Object.keys(d.anchors||{}); const zoneAims=sc.zones.map(z=>['zone:'+z.name,'zone '+z.name]);
  let h='';
  const k=keys()[S.selKey];
  if(k){
    h+='<div class="sec"><h3><span class="ico" data-icon="path"></span>WAYPOINT '+(S.selKey+1)+' / '+keys().length+'<span class="r">'+(track().name||'')+'</span></h3><div class="sb">'+
      fld('X (tiles)','x',k.x,'number','step="0.25"')+fld('Y (tiles)','y',k.y,'number','step="0.25"')+fld('ROT °','rot',k.rot||0,'number','step="5"')+
      fld('SCALE X','sx',k.sx==null?'':k.sx,'number','step="0.05" placeholder="1"')+fld('SCALE Y','sy',k.sy==null?'':k.sy,'number','step="0.05" placeholder="1"')+
      fld('TRAVEL s','t',k.t!=null?k.t:1,'number','step="0.05" min="0"')+fld('HOLD s','hold',k.hold||0,'number','step="0.05" min="0"')+sel('EASE','ease',k.ease||'inout',['linear','in','out','inout'])+
      '<div class="row"><button class="tb" data-act="dup">DUPLICATE</button><button class="tb" data-act="up">◀ EARLIER</button><button class="tb" data-act="dn">LATER ▶</button><button class="tb" data-act="del"><span class="ico" data-icon="delete"></span></button></div>'+
      '<div class="hint">drag the yellow R handle to rotate (15° steps; shift free) · arrows nudge ¼ tile · R / shift-R rotate ±15°</div></div></div>';
    h+='<div class="sec"><h3><span class="ico" data-icon="cannon"></span>ACTIONS ON THIS KEY<span class="r">'+((k.actions||[]).length)+'</span></h3><div class="sb">';
    (k.actions||[]).forEach((a,ai)=>{
      const p='a'+ai+'.';
      h+='<div class="sc-act"><div class="row"><b>'+(ai+1)+' · '+a.type.toUpperCase()+'</b><span class="x" data-delact="'+ai+'">✕</span><button class="tb" data-testact="'+ai+'" title="fire this action on the live boss now"><span class="ico" data-icon="play"></span>TEST</button></div>';
      if(a.type==='fire'){
        h+='<div class="sc-shapes">'+['straight-stream','spread-three','fan-five','radial-burst','spiral-clockwise','spiral-counterclockwise','aimed-burst','sweep-fan','mirrored-streams','sine-wave','bullet-wall','bullet-rain'].map(n=>{ const sh=shapeOf(n); return '<button class="scb'+(a.shape===sh.shape&&(!!a.ccw===!!sh.ccw)?' on':'')+'" data-shape="'+n+'" data-ai="'+ai+'" title="'+n+'"><span class="pk" data-set="bulletpatterns" data-name="'+n+'"></span></button>'; }).join('')+'</div>'+
          sel('ROUND',p+'kind',a.kind||'boss',[['boss','boss\'s own round ('+(d.actions.proj||'stage')+')']].concat(P.kinds.map(x=>[x,x])))+
          sel('FROM ANCHOR',p+'anchor',a.anchor||'C',anchors.length?anchors:['C'])+
          sel('AIM',p+'aim',a.aim||'',[['','straight (angle below)'],['player','at the player']].concat(zoneAims))+fld('ANGLE °',p+'angle',a.angle!=null?a.angle:90,'number','step="5" title="90 = straight down"')+
          fld('ROUNDS n',p+'n',a.n||1,'number','min="1"')+fld('SPREAD °',p+'spread',a.spread!=null?a.spread:40,'number','step="5"')+fld('SPEED',p+'speed',a.speed||3,'number','step="0.25"')+
          fld('BURST ×',p+'burst',a.burst||1,'number','min="1"')+fld('INTERVAL s',p+'interval',a.interval!=null?a.interval:0.1,'number','step="0.02"')+fld('STEP °',p+'step',a.step!=null?a.step:20,'number','step="5" title="spiral / sweep turn per beat"')+
          (a.shape==='wall'?fld('GAP (index)',p+'gap',a.gap!=null?a.gap:'','number','placeholder="none"'):'')+
          sel('FLASH',p+'flash',a.flash||'',[['','boss\'s own muzzle'],['none','none']].concat(P.muzzle.map(x=>[x,x])))+sel('SOUND',p+'sfx',a.sfx||'',P.sfx,'(pattern default)');
      } else if(a.type==='fx'){
        h+=sel('FAMILY',p+'fam',a.fam||'',P.explode,'(by size)')+fld('SIZE',p+'size',a.size||40,'number')+sel('PALETTE',p+'palette',a.palette||'red',['red','blue','green'])+sel('AT ANCHOR',p+'anchor',a.anchor||'',anchors,'(hull centre)')+fld('DX',p+'dx',a.dx||0,'number')+fld('DY',p+'dy',a.dy||0,'number');
      } else if(a.type==='flash'){
        h+=sel('FAMILY',p+'fam',a.fam||'bpfx_muzzle_kinetic',P.muzzle)+sel('AT ANCHOR',p+'anchor',a.anchor||'C',anchors.length?anchors:['C'])+fld('SCALE',p+'scale',a.scale||1,'number','step="0.1"');
      } else if(a.type==='sfx'){ h+=sel('SOUND',p+'name',a.name||'',P.sfx); }
      else if(a.type==='shake'){ h+=fld('AMOUNT',p+'amount',a.amount||6,'number'); }
      else if(a.type==='zone'){ h+=sel('ZONE',p+'name',a.name||'',sc.zones.map(z=>z.name))+sel('SET',p+'on',a.on===false?'off':'on',[['on','ON'],['off','OFF']]); }
      h+='</div>';
    });
    h+='<div class="row"><button class="tb" data-add="fire"><span class="ico" data-icon="cannon"></span>FIRE</button><button class="tb" data-add="fx"><span class="ico" data-icon="damage"></span>EFFECT</button><button class="tb" data-add="flash"><span class="pk" data-set="markers" data-name="muzzle"></span>FLASH</button><button class="tb" data-add="sfx">SOUND</button><button class="tb" data-add="shake">SHAKE</button><button class="tb" data-add="zone">ZONE ON/OFF</button></div>'+
      '<div class="hint">actions run when the key is reached. ROUND "boss\'s own" fires exactly what the fight fires (family, hit box, skin); any other kind is a FIRETYPES round.</div></div></div>';
  }
  const z=sc.zones[S.selZone];
  if(z){
    const col=z.type;
    h+='<div class="sec"><h3><span class="pk" data-set="'+(z.type==='safe'?'shields':(z.type==='attack'?'markers':'firinghitboxguides'))+'" data-name="'+(z.type==='safe'?'shield-circle':(z.type==='attack'?'fire-cone-wide':'hitbox-rectangle'))+'"></span>'+z.type.toUpperCase()+' ZONE<span class="r">'+z.name+'</span></h3><div class="sb">'+
      fld('NAME','name',z.name)+sel('TYPE','type',z.type,[['boss','boss - fences the manoeuvre'],['attack','attack - telegraphed danger'],['safe','safe - rounds removed']])+
      fld('X','x',z.x,'number','step="0.5"')+fld('Y','y',z.y,'number','step="0.5"')+fld('W','w',z.w,'number','step="0.5" min="0.5"')+fld('H','h',z.h,'number','step="0.5" min="0.5"')+
      fld('FROM s','from',z.from==null?'':z.from,'number','step="0.1" placeholder="always"')+fld('TO s','to',z.to==null?'':z.to,'number','step="0.1" placeholder="always"')+fld('PHASE','phase',z.phase==null?'':z.phase,'number','min="0" placeholder="any"')+
      (z.type==='attack'?(sel('TELEGRAPH','telegraph',z.telegraph||'rect',[['rect','rect + symbol'],['badge','armoured badge'],['fov','FOV cone (wide)'],['fovtall','FOV cone (tall)'],['','none (data only)']])+sel('SYMBOL','symbol',z.symbol||'danger',['danger','impact-imminent','incoming-projectile'])+sel('CONE FROM','anchor',z.anchor||'C',anchors.length?anchors:['C'])):'')+
      (z.type==='safe'?('<div class="f"><label>ENFORCE</label><input type="checkbox" data-s="enforce" '+(z.enforce!==false?'checked':'')+'></div><div class="f"><label>FIZZLE FX</label><input type="checkbox" data-s="fizzle" '+(z.fizzle!==false?'checked':'')+'></div>'):'')+
      (z.type==='boss'?'<div class="hint">while no track is moving the boss, its own manoeuvre is clamped inside this box</div>':'')+
      '<div class="row"><button class="tb" data-act="delzone"><span class="ico" data-icon="delete"></span>DELETE ZONE</button></div></div></div>';
  }
  if(!k&&!z){
    h+='<div class="sec"><h3><span class="ico" data-icon="boss"></span>SCENE<span class="r">'+sc.tracks.length+' tracks · '+sc.zones.length+' zones</span></h3><div class="sb">'+
      '<div class="hint">1 · pick WAYPOINT and click the field to lay the boss\'s path - or press a PATH / MOVE preset<br>2 · drag a BOSS / ATTACK / SAFE zone<br>3 · select a waypoint and add FIRE / EFFECT / FLASH actions from the engine\'s own families<br>4 · PREVIEW scrubs here; ATTACH LIVE or APPLY + PLAY TEST runs it in the real engine</div>'+
      '<div class="hint">grid cell '+cell()+'px · field '+fieldW()+'×'+fieldH()+' · positions are the hull CENTRE in tiles</div>'+
      fld('FIELD W','grid.w',fieldW(),'number')+fld('FIELD H','grid.h',fieldH(),'number')+'<div class="hint">wide stages (1-4 are 680 wide since 0822d) - set the field width to the stage\'s world so the tiles line up</div></div></div>';
  }
  el.innerHTML=h;
  $$('[data-s]',el).forEach(inp=>{ inp.onchange=()=>{ BM().pushUndo(); const key=inp.dataset.s; let v=inp.type==='checkbox'?inp.checked:(inp.type==='number'?(inp.value===''?null:+inp.value):inp.value);
    if(key.indexOf('grid.')===0){ sc.grid[key.slice(5)]=v||480; }
    else if(key.indexOf('a')===0 && /^a\d+\./.test(key)){ const m=key.match(/^a(\d+)\.(.+)$/); const a=k.actions[+m[1]]; if(m[2]==='on') a.on=(v!=='off'); else if(v===null) delete a[m[2]]; else a[m[2]]=v; }
    else { const t=k||z; if(!t) return; if(v===null) delete t[key]; else t[key]=v; if(key==='type'&&z){ if(v==='attack'&&!z.telegraph){ z.telegraph='rect'; z.symbol='danger'; } } }
    after(); }; });
  $$('[data-shape]',el).forEach(b=>b.onclick=()=>{ BM().pushUndo(); const a=k.actions[+b.dataset.ai]; const sh=shapeOf(b.dataset.shape); a.shape=sh.shape; if(sh.ccw) a.ccw=true; else delete a.ccw; if(sh.n) a.n=sh.n; if(sh.spread!=null) a.spread=sh.spread; if(sh.burst) a.burst=sh.burst; if(sh.aim) a.aim=sh.aim; after(); });
  $$('[data-add]',el).forEach(b=>b.onclick=()=>{ BM().pushUndo(); k.actions=k.actions||[]; const t=b.dataset.add; const a={type:t}; if(t==='fire'){ Object.assign(a,{shape:'fan',kind:'boss',anchor:anchors[0]||'C',n:5,spread:50,speed:3,burst:1,interval:0.1}); } if(t==='fx'){ Object.assign(a,{size:40,palette:'red'}); } if(t==='flash'){ Object.assign(a,{fam:P.muzzle[0]||'bpfx_muzzle_kinetic',anchor:anchors[0]||'C',scale:1}); } if(t==='sfx'){ a.name=P.sfx[0]||''; } if(t==='shake'){ a.amount=6; } if(t==='zone'){ a.name=(sc.zones[0]||{}).name||''; a.on=true; } k.actions.push(a); after(); });
  $$('[data-delact]',el).forEach(x=>x.onclick=()=>{ BM().pushUndo(); k.actions.splice(+x.dataset.delact,1); after(); });
  $$('[data-testact]',el).forEach(b=>b.onclick=()=>{ if(!api()) return; const r=api().scene.action(JSON.parse(JSON.stringify(k.actions[+b.dataset.testact]))); BM().msg(r?'action fired on the live boss':'no live boss - PLAY TEST first', !r); });
  $$('[data-act]',el).forEach(b=>b.onclick=()=>{ const ks=keys(); BM().pushUndo(); const act=b.dataset.act;
    if(act==='dup'){ ks.splice(S.selKey+1,0,JSON.parse(JSON.stringify(k))); S.selKey++; } else if(act==='up'&&S.selKey>0){ [ks[S.selKey-1],ks[S.selKey]]=[ks[S.selKey],ks[S.selKey-1]]; S.selKey--; } else if(act==='dn'&&S.selKey<ks.length-1){ [ks[S.selKey+1],ks[S.selKey]]=[ks[S.selKey],ks[S.selKey+1]]; S.selKey++; } else if(act==='del'){ ks.splice(S.selKey,1); S.selKey=-1; } else if(act==='delzone'){ sc.zones.splice(S.selZone,1); S.selZone=-1; }
    after(); });
}
function shapeOf(n){ return {'straight-stream':{shape:'stream',n:1,burst:6},'spread-three':{shape:'spread',n:3,spread:36},'fan-five':{shape:'fan',n:5,spread:60},'radial-burst':{shape:'radial',n:12},'spiral-clockwise':{shape:'spiral',burst:16},'spiral-counterclockwise':{shape:'spiral',ccw:true,burst:16},'aimed-burst':{shape:'aimed',n:1,burst:3,aim:'player'},'sweep-fan':{shape:'sweep',n:3,spread:24,burst:6},'mirrored-streams':{shape:'mirrored',spread:50,burst:5},'sine-wave':{shape:'sine',burst:8},'bullet-wall':{shape:'wall',n:9},'bullet-rain':{shape:'rain',n:6,burst:4}}[n]||{shape:'stream'}; }

/* ---- live overlay on the STAGE tab: the path + zones on the real fight ---- */
function overlay(x, s, k){ // x: overlay ctx, s: snapshot, k: px per world unit (already camera-adjusted by the caller's sx/sy)
  const sc=scene(); if(!sc||!s||!s.boss) return;
  const c=cell(); const vz=s.vz||1; const sx=v=>(v-s.camX)*vz*k, sy=v=>(v*vz+s.VH*(1-vz))*k;
  for(const z of sc.zones){ const rgb=ZCOL[z.type]||ZCOL.boss; const live=s.scene&&s.scene.zones&&s.scene.zones.find(q=>q.name===z.name); const on=!live||live.active; x.globalAlpha=on?1:0.35; x.strokeStyle='rgba('+rgb+',0.9)'; x.setLineDash([4,3]); x.strokeRect(sx(z.x*c), sy(z.y*c), z.w*c*vz*k, z.h*c*vz*k); x.setLineDash([]); x.fillStyle='rgba('+rgb+',0.9)'; x.font='9px monospace'; x.fillText(z.name, sx(z.x*c)+3, sy(z.y*c)+10); x.globalAlpha=1; }
  const tr=(s.scene&&s.scene.track>=0)?sc.tracks[s.scene.track]:track(); if(!tr||!tr.keys.length) return;
  x.strokeStyle='rgba(74,168,255,0.8)'; x.lineWidth=1.5; x.beginPath(); tr.keys.forEach((kk,i)=>{ const px=sx(kk.x*c), py=sy(kk.y*c); if(i) x.lineTo(px,py); else x.moveTo(px,py); }); x.stroke();
  tr.keys.forEach((kk,i)=>{ const px=sx(kk.x*c), py=sy(kk.y*c); const cur=(s.scene&&s.scene.kf===i); x.fillStyle=cur?'#8de23a':'#4aa8ff'; x.beginPath(); x.arc(px,py,cur?5:3.5,0,Math.PI*2); x.fill(); });
  if(s.scene){ x.fillStyle='rgba(0,0,0,.5)'; x.fillRect(4,20,190,12); x.fillStyle='#4aa8ff'; x.font='9px monospace'; x.fillText('scene '+(s.scene.trackName||'(idle)')+'  key '+(s.scene.kf+1)+'  t '+s.scene.t.toFixed(1)+'s  rot '+s.scene.rotDeg.toFixed(0)+'°', 8, 29); }
}

/* ---- wire into the editor ---- */
function renderAll(){ renderTop(); renderInsp(); draw(); drawTimeline(); }
function init(){
  const B=BM(); if(!B){ setTimeout(init,100); return; }
  build();
  loadExtra().then(()=>{ draw(); });
  B.hooks.onDoc=function(){ S.selKey=-1; S.selZone=-1; S.track=0; S.pal=null; renderAll(); };
  B.hooks.onTab=function(t){ if(t==='scene'){ fit(); renderAll(); } };
  B.hooks.overlay=overlay;
  B.hooks.scene={draw:draw, state:S, scene:scene};
  window.addEventListener('resize', ()=>{ if($('#pane-scene').classList.contains('on')){ fit(); draw(); drawTimeline(); } });
}
init();
})();
