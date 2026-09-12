/* ============================================================
   BULLETS OF DEBUG! (drop 0912g)

   The editor for everything that is not a boss. Host/guest, same as Boss Mode: the shipping game
   runs in the iframe and is driven through window.BOFDEBUG, which lives in assets/game.js.

   ⚠ THE ENGINE IS REACHED DIRECTLY, NOT THROUGH postMessage. Same-origin iframe, exactly as
   bossmode.js does it (there is zero postMessage on either side of that editor). Every column-0
   function in game.js is a property of the guest window, so `host.win.spawnEnemy` works; the
   BOFDEBUG object exists only for the DATA, which lives in lexical consts nothing outside the file
   can see.

   ⚠ AND ARRAYS ARE READ THROUGH THE GETTER EVERY TIME. `enemies` is reassigned once per frame by
   the cull, so a cached reference is a corpse on the next frame. Never hold one.
   ============================================================ */
(function(){
'use strict';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const UI='assets/bulletsofdebug/ui/';

/* ---------------- the pack ---------------- */
const A={};
function loadImg(src){ return new Promise((ok,no)=>{ const i=new Image(); i.onload=()=>ok(i); i.onerror=no; i.src=src; }); }
async function loadAtlas(name){
  const [img,map]=await Promise.all([loadImg(UI+name+'.png'), fetch(UI+name+'.json').then(r=>r.json())]);
  A[name]={img,map}; return A[name];
}
/* rectOf pairs items[i] with atlas.rects[i] - the same contract the Boss Mode loader uses, which is
   why the generated maps were written in that shape rather than a new one. */
function rectOf(name,item){ const M=A[name].map; const i=M.items.findIndex(x=>x.name===item); return i<0?null:M.atlas.rects[i]; }
function cellRule(sel,name,item,S){
  const r=rectOf(name,item); if(!r) return '';
  const im=A[name].img;
  return sel+'{width:'+Math.round(r.w*S)+'px;height:'+Math.round(r.h*S)+'px;'+
    'background-image:url('+UI+name+'.png);background-size:'+Math.round(im.width*S)+'px '+Math.round(im.height*S)+'px;'+
    'background-position:-'+Math.round(r.x*S)+'px -'+Math.round(r.y*S)+'px}\n';
}
function buildCSS(){
  let css='';
  const BS=0.30;                                  // the button plates are ~330px wide at 1:1
  for(const it of A.buttons.map.items){
    const base=it.name.replace(/-(hover|down)$/,'');
    if(/-hover$/.test(it.name))      css+=cellRule('.pb[data-btn='+base+']:hover','buttons',it.name,BS);
    else if(/-down$/.test(it.name))  css+=cellRule('.pb[data-btn='+base+']:active','buttons',it.name,BS);
    else                             css+=cellRule('.pb[data-btn='+base+']','buttons',it.name,BS);
  }
  const IS=0.145;                                 // icon tiles are ~190px at 1:1
  for(const it of A.icons.map.items) css+=cellRule('.ico[data-icon='+it.name+']','icons',it.name,IS);
  const s=document.createElement('style'); s.textContent=css; document.head.appendChild(s);
}

/* ---------------- host ---------------- */
const host={win:null, api:null, ok:false};
function api(){ return host.api; }
function hostTick(){
  const f=$('#host');
  try{
    const w=f.contentWindow;
    const d=w&&w.BOFDEBUG;
    host.win=w; host.api=d||null;
    const ready=!!(d&&d.ready);
    if(ready!==host.ok){
      host.ok=ready;
      $('#host-led').className='led '+(ready?'on':'busy');
      $('#host-txt').textContent=ready?'ENGINE READY':'ENGINE BOOTING';
      if(ready) onReady();
    }
  }catch(e){ host.ok=false; $('#host-led').className='led bad'; $('#host-txt').textContent='ENGINE UNREACHABLE'; }
}

/* ---------------- state ---------------- */
const FIRE_SHAPE0='fan';
const S={ roster:[], sel:null, unit:null, tab:'enemy', filter:'', booted:false,
          fov:true, anchors:true, hull:false, paused:false,
          bustCam:false, _mark:null };
const layout={dock:true, theater:false, drawer:false};

function msg(t){ $('#tf-msg').textContent=t||''; }

/* ---------------- roster ---------------- */
function onReady(){
  if(S.booted) return; S.booted=true;
  const d=api();
  S.roster=d.roster();
  $('#roster-n').textContent=S.roster.length+' TYPES';
  $('#roster-filter').placeholder='filter '+S.roster.length+' types…';
  const sel=$('#t-stage'); sel.innerHTML='';
  for(let i=1;i<=9;i++){ const o=document.createElement('option'); o.value=i; o.textContent='STAGE '+i; sel.appendChild(o); }
  renderRoster();
  msg('roster: '+S.roster.length+' types across '+new Set(S.roster.map(r=>r.table)).size+' tables');
}
function renderRoster(){
  const box=$('#roster'); box.innerHTML='';
  const f=S.filter.toLowerCase();
  const rows=S.roster.filter(r=>!f || r.type.toLowerCase().includes(f) || r.table.toLowerCase().includes(f));
  const byTable={};
  for(const r of rows){ (byTable[r.table]=byTable[r.table]||[]).push(r); }
  for(const t of Object.keys(byTable).sort()){
    const g=document.createElement('div'); g.className='rg';
    g.innerHTML='<h4>'+t+' · '+byTable[t].length+'</h4>';
    for(const r of byTable[t]){
      const el=document.createElement('div');
      el.className='ri'+(r.row?'':' norow')+((S.sel&&S.sel.type===r.type&&S.sel.table===r.table)?' on':'');
      el.innerHTML='<span class="nm">'+r.type+'</span>'+(r.row?'':'<span class="tg">CODE</span>');
      el.onclick=()=>pick(r);
      g.appendChild(el);
    }
    box.appendChild(g);
  }
}
function pick(r){
  /* ⚠ HAND FOCUS BACK OFF THE FILTER. The shortcut handler deliberately ignores keys while an
     INPUT has focus - you do not want S spawning a unit while someone types "s6" into the filter -
     but that meant picking a unit from a filtered list left S/C dead until the user clicked
     somewhere else. Measured: the key never reached the handler. Picking is the moment the user is
     done typing, so it is the right place to release focus. */
  try{ if(document.activeElement && document.activeElement.blur) document.activeElement.blur(); }catch(e){}
  S.sel=r;
  $('#vt-name').textContent=r.type+'  ·  '+r.table;
  $('#dock-sub').textContent=r.table;
  renderRoster(); renderInspector();
  if(layout.drawer) toggleDrawer(false);
}

/* ---------------- the lab ---------------- */
function labOpen(){
  const d=api(); if(!d) return;
  const st=+$('#t-stage').value||1;
  const ok=d.lab.on(st);
  msg(ok?('lab open on stage '+st+' — wave script spent, nothing will arrive'):'lab failed to open');
}
function spawn(){
  const d=api(); if(!d||!S.sel) return msg('pick a unit first');
  if(!d.lab.active) labOpen();
  const snap=d.snapshot();
  const e=d.spawn(S.sel.type, snap.VW/2, snap.VH*0.28, {});
  if(e && e.err){ msg(e.err); S.unit=null; return; }
  S.unit=true;
  msg('spawned '+S.sel.type);
  renderInspector();
}
function clearField(){ const d=api(); if(d){ d.clear(); S.unit=null; msg('field cleared'); renderInspector(); } }

/* the live unit, fetched through the getter every time (never cached) */
function unit(){
  const d=api(); if(!d) return null;
  const es=d.enemies;
  return (es&&es.length)?es[es.length-1]:null;
}

/* ---------------- inspector ---------------- */
const FIELDS=[
  {k:'hp',    label:'HP',        min:1,   max:400, step:1},
  {k:'w',     label:'WIDTH',     min:4,   max:220, step:1},
  {k:'h',     label:'HEIGHT',    min:4,   max:220, step:1},
  {k:'vy',    label:'FALL SPD',  min:-4,  max:8,   step:0.02},
  {k:'vx',    label:'DRIFT',     min:-6,  max:6,   step:0.02},
  {k:'fireRate', label:'FIRE RATE', min:0.05, max:4, step:0.01},
  {k:'score', label:'SCORE',     min:0,   max:5000, step:10},
];
function sec(id,title,right,body,open){
  return '<div class="sec'+(open===false?' closed':'')+'" data-sec="'+id+'"><h3>'+title+
         '<span class="r">'+(right||'')+'</span></h3><div class="sb">'+body+'</div></div>';
}
function renderInspector(){
  /* the dock shows ONE panel, chosen by the active tab - the same body[data-tab] switch Boss Mode
     uses for its fight/scene inspectors, rather than two docks fighting over the same column. */
  if(S.tab==='fire'){ return renderFire(); }
  if(S.tab==='stage'){ return renderStage(); }
  const box=$('#insp'); const d=api();
  if(!d){ box.innerHTML='<div class="hint">waiting for the engine…</div>'; return; }
  if(!S.sel){ box.innerHTML='<div class="hint">Pick a unit from the ROSTER drawer (L).</div>'; return; }
  const u=unit();
  let h='';

  /* the roster row - the authored numbers, which are NOT what the unit gets */
  const row=S.sel.row;
  h+=sec('row','ROSTER ROW', S.sel.table,
      row? '<div class="hint">The authored values. Spawning re-derives some of them — see below.</div>'+
           Object.keys(row).slice(0,14).map(k=>
             '<div class="f wide"><label>'+k+'</label><span class="v mono">'+
             String(typeof row[k]==='object'?JSON.stringify(row[k]):row[k]).slice(0,26)+'</span></div>').join('')
        : '<div class="hint warn">This type has no data row — it is one of the hand-written switch bodies inside spawnEnemy. Its numbers are literals in code, so they can be tuned on the LIVE unit below but not read back from a table.</div>');

  if(!u){
    h+='<div class="hint">No live unit. Press <b>S</b> or SPAWN to put one in the lab.</div>';
    box.innerHTML=h; wireSections(); return;
  }

  /* the live unit */
  let f='';
  for(const F of FIELDS){
    const v=(u[F.k]==null?0:u[F.k]);
    f+='<div class="f"><label>'+F.label+'</label>'+
       '<input type="range" data-k="'+F.k+'" min="'+F.min+'" max="'+F.max+'" step="'+F.step+'" value="'+v+'">'+
       '<span class="v" data-v="'+F.k+'">'+(Math.round(v*100)/100)+'</span></div>';
  }
  h+=sec('live','LIVE UNIT', u.type||'', f+
     '<div class="hint">⚠ HP here is the SPAWNED value. The roster row\'s hp is re-projected through EHP() against the stage\'s shots-to-kill band, so the two rarely match — this slider is the truth.</div>'+
     '<div class="hint">⚠ WIDTH/HEIGHT are the collision hull AND the draw size at once.</div>');

  /* behaviour */
  const pats=d.patterns();
  h+=sec('beh','BEHAVIOUR', u.pattern||'—',
     '<div class="f wide"><label>PATTERN</label><select id="i-pattern">'+
       pats.map(p=>'<option'+(p===u.pattern?' selected':'')+'>'+p+'</option>').join('')+'</select></div>'+
     '<div class="row"><label class="chk"><input type="checkbox" id="i-shadow"'+(u._bodShadow?' checked':'')+'> SHADOW UNDER UNIT</label></div>'+
     '<div class="hint">Shadows were removed game-wide in 0724bd for not matching the art. This is a per-unit opt-in for the lab only — the shipping game is unchanged.</div>');

  /* firing */
  h+=sec('fire','FIRING', (u.shoots?'armed':'silent'),
     '<div class="row"><label class="chk"><input type="checkbox" id="i-shoots"'+(u.shoots?' checked':'')+'> SHOOTS</label></div>'+
     /* ⚠ DEFAULT TO `fan`, NOT TO shapes()[0]. The vocabulary happens to start with `stream`,
        which fires ONE round - so the first FIRE ONCE a user ever clicks looked like a broken
        button ("1 rounds") while the pattern system underneath it was working perfectly. */
     '<div class="f wide"><label>SHAPE</label><select id="i-shape">'+
       d.shapes().map(s=>'<option'+(s===FIRE_SHAPE0?' selected':'')+'>'+s+'</option>').join('')+'</select></div>'+
     '<div class="f"><label>COUNT</label><input type="range" id="i-n" min="1" max="24" step="1" value="7"><span class="v" id="v-n">7</span></div>'+
     '<div class="f"><label>SPREAD°</label><input type="range" id="i-spread" min="5" max="360" step="5" value="70"><span class="v" id="v-spread">70</span></div>'+
     '<div class="f"><label>SPEED</label><input type="range" id="i-speed" min="0.5" max="9" step="0.1" value="3"><span class="v" id="v-speed">3</span></div>'+
     '<div class="row"><button class="tb" id="i-fire"><span class="ico" data-icon="projectile"></span>FIRE ONCE</button>'+
     '<button class="tb" id="i-fire-loop">LOOP</button></div>'+
     '<div class="hint">These are the SCENE DIRECTOR shapes the bosses use, fired off an ordinary enemy — measured working with no boss present.</div>');

  box.innerHTML=h;
  wireSections(); wireInspector();
}
function wireSections(){
  $$('#insp .sec>h3').forEach(hh=>hh.onclick=()=>hh.parentNode.classList.toggle('closed'));
}
function wireInspector(){
  const d=api();
  $$('#insp input[type=range][data-k]').forEach(r=>{
    r.oninput=()=>{
      const u=unit(); if(!u) return;
      const v=parseFloat(r.value);
      u[r.dataset.k]=v;
      /* hp has a twin: some families keep maxhp, some _maxhp, and the damage-state art reads
         whichever its family expects. Write both so the bar and the plate agree. */
      if(r.dataset.k==='hp'){ if(u.maxhp!=null) u.maxhp=Math.max(u.maxhp,v); if(u._maxhp!=null) u._maxhp=Math.max(u._maxhp,v); }
      const out=$('#insp [data-v="'+r.dataset.k+'"]'); if(out) out.textContent=Math.round(v*100)/100;
    };
  });
  const p=$('#i-pattern'); if(p) p.onchange=()=>{ const u=unit(); if(u){ u.pattern=p.value; msg('pattern → '+p.value); } };
  const sh=$('#i-shadow'); if(sh) sh.onchange=()=>{ const u=unit(); if(u) d.shadow(u, sh.checked); };
  const ss=$('#i-shoots'); if(ss) ss.onchange=()=>{ const u=unit(); if(u) u.shoots=ss.checked; };
  ['n','spread','speed'].forEach(k=>{
    const el=$('#i-'+k); if(!el) return;
    el.oninput=()=>{ $('#v-'+k).textContent=el.value; };
  });
  const fire=$('#i-fire'); if(fire) fire.onclick=()=>fireOnce();
  const loop=$('#i-fire-loop'); if(loop) loop.onclick=()=>{ S.loop=!S.loop; loop.classList.toggle('on',S.loop); msg(S.loop?'looping':'loop off'); };
}
let _beat=0;
function fireOnce(){
  const d=api(), u=unit(); if(!d||!u) return;
  const act={shape:$('#i-shape').value, n:+$('#i-n').value, spread:+$('#i-spread').value,
             speed:+$('#i-speed').value, kind:'e', anchor:'C'};
  const r=d.emit(u, act, _beat++);
  if(r!==true) msg('emit: '+r);
}

/* ============================================================
   THE FIRE TAB (drop 0912h)

   Mike: "projectiles ... muzzle flashes, firing speed, damage or damage per second, projectile
   patterning ... anchor points".

   ⚠⚠ THIS PANEL IS DELIBERATELY NARROWER THAN THAT LIST, AND THE INERT SECTION SAYS WHY.
   Seven subsystems were read before a control was drawn, and the finding that shaped the whole tab
   is that a straightforward reading of the ask produces a wall of sliders that READ BACK THE VALUE
   YOU WROTE AND CHANGE NOTHING. Enemy-to-player damage is the headline: playerHit() takes zero
   arguments, there is no player.hp in the file, and the collision never looks at the bullet - every
   enemy round costs exactly one shield pip. A "damage" slider here would be a lie with a readout.

   So every dial below was confirmed to move something in the engine, and the twelve that do not
   are listed, greyed, with the measurement that condemned them.
   ============================================================ */

/* the shapes that emit exactly ONE round per beat, so `n` is meaningless for them. Measured off
   sceneEmitBeat's switch: spiral / sine / the default (stream, aimed) all call fire() once, and
   mirrored always calls it exactly twice. */
const ONE_SHOT_SHAPES={spiral:1, sine:1, stream:1, aimed:1};
const FIXED_N={mirrored:2};
/* shapes that ignore the anchor and the aim entirely */
const NO_ANCHOR={wall:1, rain:1};

const F={kind:'pellet', shape:'fan', n:7, spread:70, step:24, speed:3, angle:90, gap:-1,
         burstN:10, interval:0.12, flash:'bpfx_muzzle_kinetic', flashScale:1, flashN:6, flashPx:40,
         slot:'C', mx:0, my:0.30, curveAmt:0.5};

function fireKindOptions(){
  const d=api(); if(!d||!d.fireKinds) return '';
  const ks=d.fireKinds();
  S.fireKinds=ks;
  /* ⚠ `shadowed` IS COMPUTED IN THE BRIDGE, NOT HERE. The rule is the engine's, so the editor
     reading PROJ/FIRETYPES and re-deriving it is the same mistake as recomputing the camera - and
     the first cut got it wrong on screen, labelling `blast` shadowed when PROJ.blast.type IS
     'blast', i.e. it resolves to itself. Exactly 8 rows are genuinely unreachable, and naming them
     is useful: that is authored projectile art nothing in the game can draw. */
  return ks.map(k=>
    '<option value="'+k.kind+'"'+(k.kind===F.kind?' selected':'')+'>'+
      k.kind + (k.cls&&k.cls!==k.kind?('  ['+k.cls+']'):'') +
      (k.shadowed?('  — shadowed, draws as '+k.resolves):'') + '</option>').join('');
}

function renderFire(){
  const box=$('#insp'), d=api();
  if(!d){ box.innerHTML='<div class="hint">waiting for the engine…</div>'; return; }
  const u=unit();
  let h='';

  if(!u){
    h+='<div class="hint warn">The FIRE tab drives a LIVE unit. Pick one from the ROSTER drawer (L) and press <b>S</b> to put it in the lab — every control here fires off that unit.</div>';
  }

  /* ---- the round ---- */
  h+=sec('fk','PROJECTILE', F.kind,
    '<div class="f wide"><label>KIND</label><select id="f-kind">'+fireKindOptions()+'</select></div>'+
    '<div class="f"><label>SPEED</label><input type="range" id="f-speed" min="0.5" max="9" step="0.1" value="'+F.speed+'"><span class="v" id="fv-speed">'+F.speed+'</span></div>'+
    '<div class="hint">⚠ <b>kind</b> decides the muzzle as well as the art. A blank kind or <code>boss</code> routes to <code>_shipShot</code>, which derives its family from <code>owner._ship</code> — on an ordinary enemy that returns <code>eshot</code>, the hull collapses to a square and the authored boss family never appears. Name a real kind.</div>'+
    '<div class="hint">⚠ <b>speed</b> is live for most kinds and a placebo for <code>emissile</code>, <code>s1jungleMissile</code> and anything <code>_shootable</code> — the steering block rewrites vx/vy from <code>spd*DIFF.ebSpeed</code> every frame.</div>');

  /* ---- the pattern ---- */
  const shapes=d.shapes();
  const oneShot=!!ONE_SHOT_SHAPES[F.shape], fixedN=FIXED_N[F.shape];
  h+=sec('fp','PATTERN', F.shape,
    '<div class="f wide"><label>SHAPE</label><select id="f-shape">'+
      shapes.map(s=>'<option'+(s===F.shape?' selected':'')+'>'+s+'</option>').join('')+'</select></div>'+
    '<div class="f"><label>ROUNDS</label><input type="range" id="f-n" min="1" max="24" step="1" value="'+F.n+'"'+
      ((oneShot||fixedN)?' disabled':'')+'><span class="v" id="fv-n">'+(fixedN?fixedN:(oneShot?1:F.n))+'</span></div>'+
    '<div class="f"><label>SPREAD°</label><input type="range" id="f-spread" min="5" max="360" step="5" value="'+F.spread+'"><span class="v" id="fv-spread">'+F.spread+'</span></div>'+
    '<div class="f"><label>STEP°</label><input type="range" id="f-step" min="1" max="90" step="1" value="'+F.step+'"><span class="v" id="fv-step">'+F.step+'</span></div>'+
    '<div class="f"><label>ANGLE°</label><input type="range" id="f-angle" min="0" max="360" step="5" value="'+F.angle+'"><span class="v" id="fv-angle">'+F.angle+'</span></div>'+
    (F.shape==='wall'
      ? '<div class="f"><label>GAP</label><input type="range" id="f-gap" min="-1" max="23" step="1" value="'+F.gap+'"><span class="v" id="fv-gap">'+F.gap+'</span></div>'+
        '<div class="hint">The gap is the column that is NOT fired — move it and the wall gets a lane. <code>-1</code> closes it entirely.</div>'
      : '')+
    (oneShot
      ? '<div class="hint warn">⚠ <b>'+F.shape+'</b> emits exactly ONE round per beat — that is the design, not a fault. It only becomes a pattern through a BURST below: <code>spiral</code> and <code>sweep</code> read the beat index, and <code>sine</code> gets its curve from the burst alternating it.</div>'
      : '')+
    (fixedN ? '<div class="hint warn">⚠ <b>mirrored</b> always fires exactly two rounds, one each side of the aim.</div>' : '')+
    (NO_ANCHOR[F.shape]
      ? '<div class="hint warn">⚠ <b>'+F.shape+'</b> ignores the anchor and the aim. <code>wall</code> lays columns across the whole world width at 90°, using only the anchor\'s Y; <code>rain</code> randomises x across the world and starts above the top edge.</div>'
      : ''));

  /* ---- cadence ---- */
  h+=sec('fb','BURST', F.burstN+' × '+F.interval+'s',
    '<div class="f"><label>BEATS</label><input type="range" id="f-burstn" min="1" max="48" step="1" value="'+F.burstN+'"><span class="v" id="fv-burstn">'+F.burstN+'</span></div>'+
    '<div class="f"><label>INTERVAL</label><input type="range" id="f-interval" min="0.02" max="1" step="0.01" value="'+F.interval+'"><span class="v" id="fv-interval">'+F.interval+'</span></div>'+
    '<div class="f"><label>CURVE AMT</label><input type="range" id="f-curveamt" min="0" max="2" step="0.05" value="'+F.curveAmt+'"><span class="v" id="fv-curveamt">'+F.curveAmt+'</span></div>'+
    '<div class="row"><button class="tb" id="f-once"><span class="ico" data-icon="projectile"></span>FIRE ONCE</button>'+
    '<button class="tb" id="f-burst">FIRE BURST</button>'+
    '<button class="tb" id="f-clearb">CLEAR ROUNDS</button></div>'+
    '<div class="hint">Beats run on the engine\'s own clock (<code>updateEffects</code>), so a burst inherits pause and time scale and looks exactly like a real fight. Rounds per second = <b>'+
      (Math.round(10/Math.max(0.02,F.interval))/10)+'</b> × the shape\'s round count.</div>');

  /* ---- the muzzle ---- */
  const fams=(d.flashFams?d.flashFams():[]);
  h+=sec('fm','MUZZLE FLASH', F.flash==='none'?'off':F.flash,
    '<div class="f wide"><label>FAMILY</label><select id="f-flash">'+
      '<option value="none"'+(F.flash==='none'?' selected':'')+'>none</option>'+
      fams.map(f=>'<option value="'+f.fam+'"'+(f.fam===F.flash?' selected':'')+'>'+f.fam+'  ('+f.frames+' frames)</option>').join('')+
      '</select></div>'+
    '<div class="f"><label>SCALE</label><input type="range" id="f-fscale" min="0.2" max="4" step="0.1" value="'+F.flashScale+'"><span class="v" id="fv-fscale">'+F.flashScale+'</span></div>'+
    '<div class="f"><label>PUFFS</label><input type="range" id="f-fn" min="1" max="16" step="1" value="'+F.flashN+'"><span class="v" id="fv-fn">'+F.flashN+'</span></div>'+
    '<div class="f"><label>REACH px</label><input type="range" id="f-fpx" min="4" max="120" step="2" value="'+F.flashPx+'"><span class="v" id="fv-fpx">'+F.flashPx+'</span></div>'+
    '<div class="hint warn">⚠ There is no usable <b>default</b>. Leaving the family unset routes to <code>shipBossMuzzleStart</code>, which returns immediately unless the unit has <code>_ship</code> AND that SHIPBOSS row has both <code>.proj</code> and <code>.mounts</code> — so firing off an ordinary enemy with the default produces <b>zero</b> flashes, silently. Naming a family routes to <code>navalFlash</code>, which works on anything.</div>');

  /* ---- the anchor ---- */
  const mp=u?d.mountPoint(u,F.slot):null;
  h+=sec('fa','ANCHOR', F.slot+(mp?('  '+Math.round(mp.x)+','+Math.round(mp.y)):''),
    '<div class="f wide"><label>SLOT</label><select id="f-slot">'+
      ['C','L','R','LW','RW','nose','tail','bay'].map(s=>'<option'+(s===F.slot?' selected':'')+'>'+s+'</option>').join('')+
      '</select></div>'+
    '<div class="f"><label>X (of w)</label><input type="range" id="f-mx" min="-0.6" max="0.6" step="0.01" value="'+F.mx+'"><span class="v" id="fv-mx">'+F.mx+'</span></div>'+
    '<div class="f"><label>Y (of h)</label><input type="range" id="f-my" min="-0.6" max="0.8" step="0.01" value="'+F.my+'"><span class="v" id="fv-my">'+F.my+'</span></div>'+
    '<div class="row"><button class="tb" id="f-mclear">RESET MOUNTS</button></div>'+
    '<div class="hint">⚠ This was inert until 0912h. Measured on a stage-1 delta jet, <b>all twelve slot names returned one point</b> — <code>(x, y + h×0.30)</code> — because <code>shipBossMount</code> reads <code>SHIPBOSS[b._ship].mounts</code> and an ordinary enemy has no <code>_ship</code>. It now also honours a per-unit <code>_mounts</code> in the same normalised form, so these sliders write real anchors and the rounds leave from them.</div>');

  /* ---- the unit's own volley ---- */
  const vf=(u&&d.volleyFor)?d.volleyFor(u.type):null;
  const vpats=(d.volleyPatterns?d.volleyPatterns():[]);
  h+=sec('fv','VOLLEY  (the unit\'s own)', vf&&vf.row?vf.key:'none',
    (vf&&vf.row
      ? '<div class="f wide"><label>ROW</label><span class="v mono">'+JSON.stringify(vf.row).slice(0,44)+'</span></div>'+
        '<div class="f"><label>EVERY</label><input type="range" id="f-vevery" min="1" max="12" step="1" value="'+(vf.row.every||3)+'"><span class="v" id="fv-vevery">'+(vf.row.every||3)+'</span></div>'+
        '<div class="row"><button class="tb" id="f-vfire">FIRE VOLLEY</button></div>'+
        '<div class="hint warn">⚠ This edits the TABLE, not the unit — every live '+u.type+' changes with it. The row is keyed in both spellings on purpose, and both are written.</div>'+
        '<div class="hint">⚠ <code>every</code> is not "fire every Nth cycle" despite the name. On the live path it is a seconds multiplier on the in-burst gap, and the fixed 1.5s pause dominates — dragging it 2→9 changes the period by only about 1.7×.</div>'
      : '<div class="hint">This type has no <code>ENEMY_VOLLEY</code> row, so it has no volley. '+
        vpats.length+' patterns exist across the 52 rows that do: '+vpats.map(p=>p.pat+'×'+p.uses).join(', ')+'.</div>'), false);

  /* ---- the honesty section ---- */
  const inert=(d.inert?d.inert():[]);
  h+=sec('fi','DIALS THAT DO NOTHING', inert.length+' measured',
    '<div class="hint">Every one of these would read back the value you wrote and change nothing — which is worse than being absent, so they are named rather than shipped.</div>'+
    inert.map(x=>'<div class="f wide"><label style="color:var(--bad)">'+x.dial+'</label>'+
      '<span class="hint" style="margin:0">'+x.why+'</span></div>').join(''), false);

  box.innerHTML=h;
  wireSections(); wireFire();
}

function fireAction(){
  return {shape:F.shape, n:F.n, spread:F.spread, step:F.step, angle:F.angle,
          speed:F.speed, kind:F.kind, anchor:F.slot,
          gap:(F.shape==='wall'?F.gap:undefined),
          curveAmt:F.curveAmt,
          flash:(F.flash==='none'?'none':F.flash),
          flashScale:F.flashScale, flashN:F.flashN, flashPx:F.flashPx};
}
function wireFire(){
  const d=api();
  const num=(id,key,after)=>{ const el=$('#f-'+id); if(!el) return;
    el.oninput=()=>{ F[key]=parseFloat(el.value); const o=$('#fv-'+id); if(o) o.textContent=el.value; if(after) after(); }; };
  num('speed','speed'); num('n','n'); num('spread','spread'); num('step','step');
  num('angle','angle'); num('gap','gap'); num('burstn','burstN'); num('interval','interval');
  num('curveamt','curveAmt'); num('fscale','flashScale'); num('fn','flashN'); num('fpx','flashPx');
  num('mx','mx',()=>applyMount()); num('my','my',()=>applyMount());

  const k=$('#f-kind'); if(k) k.onchange=()=>{ F.kind=k.value; renderFire(); };
  const sh=$('#f-shape'); if(sh) sh.onchange=()=>{ F.shape=sh.value; renderFire(); };
  const fl=$('#f-flash'); if(fl) fl.onchange=()=>{ F.flash=fl.value; msg('muzzle → '+fl.value); };
  const sl=$('#f-slot'); if(sl) sl.onchange=()=>{ F.slot=sl.value; renderFire(); };

  const once=$('#f-once'); if(once) once.onclick=()=>{
    const u=unit(); if(!u) return msg('no live unit — press S to spawn one');
    const n0=d.eBullets.length; const r=d.emit(u, fireAction(), 0);
    msg(r===true ? ('fired '+(d.eBullets.length-n0)+' round(s)') : ('emit: '+r));
  };
  const bu=$('#f-burst'); if(bu) bu.onclick=()=>{
    const u=unit(); if(!u) return msg('no live unit — press S to spawn one');
    const r=d.burst(u, fireAction(), F.burstN, F.interval);
    msg(r===true ? ('burst: '+F.burstN+' beats at '+F.interval+'s') : ('burst: '+r));
  };
  const cb=$('#f-clearb'); if(cb) cb.onclick=()=>{ try{ d.eBullets.length=0; msg('rounds cleared'); }catch(e){} };
  const mc=$('#f-mclear'); if(mc) mc.onclick=()=>{ const u=unit(); if(u){ d.clearMounts(u); renderFire(); msg('mounts reset'); } };
  const vfire=$('#f-vfire'); if(vfire) vfire.onclick=()=>{
    const u=unit(); if(!u) return msg('no live unit');
    const r=d.volleyFire(u); msg(r===true?'volley fired':('volley: '+r));
  };
  const ve=$('#f-vevery'); if(ve) ve.oninput=()=>{
    const u=unit(); if(!u) return; $('#fv-vevery').textContent=ve.value;
    d.setVolley(u.type, {every:+ve.value});
  };
}
function applyMount(){
  const d=api(), u=unit(); if(!d||!u) return;
  d.setMount(u, F.slot, F.mx, F.my);
  const mp=d.mountPoint(u, F.slot);
  const hh=$('#insp .sec[data-sec=fa] > h3 .r');
  if(hh&&mp) hh.textContent=F.slot+'  '+Math.round(mp.x)+','+Math.round(mp.y);
}

/* ============================================================
   THE STAGE TAB (drop 0912L)

   Mike's Bullets of Debug brief opens with "level backgrounds, waves".

   ⚠ ONE OF THOSE TWO IS EDITABLE AND THE OTHER IS NOT, AND THE PANEL SAYS SO RATHER THAN
   PRETENDING. `_levelCfg()` returns a FRESH OBJECT LITERAL on every call, so what the bridge hands
   back is a SNAPSHOT - writing to it changes nothing, and a background panel full of live-looking
   inputs would be exactly the placebo the FIRE tab's inert list exists to prevent. The background
   is shown read-only with the reason attached.

   What IS live: STAGE_AI_PROFILE (read every frame by the wave pump), the scroll position, and the
   wave plan, which can be dry-run to see what it contains and fired one wave at a time.
   ============================================================ */

const SA = {stage: 1, plan: null, scrollF: 0};

function stageOpts() {
  const d = api(); if (!d || !d.stages) return '';
  return d.stages().map(s =>
    '<option value="' + s.idx + '"' + (s.idx === SA.stage ? ' selected' : '') + '>' +
    s.idx + ' — ' + s.name + '</option>').join('');
}

function renderStage() {
  const box = $('#insp'), d = api();
  if (!d) { box.innerHTML = '<div class="hint">waiting for the engine…</div>'; return; }
  let h = '';

  const st = d.stages().find(s => s.idx === SA.stage) || {};
  h += sec('sg', 'STAGE', st.name || '',
    '<div class="f wide"><label>STAGE</label><select id="s-stage">' + stageOpts() + '</select></div>' +
    '<div class="f wide"><label>SUBTITLE</label><span class="v mono">' + (st.sub || '—') + '</span></div>' +
    '<div class="f wide"><label>BOSS</label><span class="v mono">' + (st.boss || '—') + '</span></div>' +
    '<div class="f wide"><label>LENGTH</label><span class="v mono">' + (st.length || '—') + 's</span></div>' +
    '<div class="f wide"><label>MUSIC</label><span class="v mono">' + (st.music || '—') + '</span></div>' +
    '<div class="row"><button class="tb" id="s-open"><span class="ico" data-icon="play"></span>OPEN THIS STAGE</button></div>');

  /* the background - READ ONLY, and the reason is the point */
  const cfg = d.levelCfg(SA.stage) || {};
  h += sec('sb', 'BACKGROUND', cfg.master || '—',
    Object.keys(cfg).map(k =>
      '<div class="f wide"><label>' + k + '</label><span class="v mono">' +
      String(cfg[k]).slice(0, 30) + '</span></div>').join('') +
    '<div class="hint warn">⚠ READ ONLY, and not as a limitation - <code>_levelCfg()</code> builds a ' +
    'FRESH OBJECT LITERAL on every call, so this is a snapshot and writing to it changes nothing. ' +
    'A panel of live-looking inputs here would be a placebo. Changing a stage\'s plate means ' +
    'changing the table in game.js.</div>');

  /* the scroll - genuinely scrubbable, which is how you look at the whole plate */
  const sc = d.scroll || {at: 0, range: 0};
  h += sec('ss', 'SCROLL', sc.range ? (sc.at + ' / ' + sc.range) : '—',
    '<div class="f"><label>POSITION</label><input type="range" id="s-scroll" min="0" max="1" step="0.005" value="' +
      (sc.range ? (sc.at / sc.range) : 0) + '"><span class="v" id="sv-scroll">' +
      Math.round((sc.range ? sc.at / sc.range : 0) * 100) + '%</span></div>' +
    '<div class="hint">Scrub the level to inspect any part of the plate. ⚠ <code>mapScroll</code> is ' +
    'advanced inside <code>drawLevelMaster</code>, not in the update - so this writes it and the ' +
    'next DRAW picks it up. Play will move it again the moment the stage is running.</div>');

  /* the AI profile - live, every frame */
  const ai = d.aiProfile(SA.stage);
  h += sec('sa', 'AI PROFILE', ai ? ('cap ' + ai.cap) : '—',
    ai ? [
      ['move', 0.5, 2.0, 0.01, 'movement speed multiplier'],
      ['formation', 0.5, 2.0, 0.01, 'formation tightness'],
      ['waveGap', 0.3, 2.0, 0.01, 'seconds between waves'],
      ['cap', 1, 24, 1, 'how many units may be on screen at once'],
      ['spawn', 0.02, 0.6, 0.01, 'spawn cadence']
    ].map(F =>
      '<div class="f"><label>' + F[0].toUpperCase() + '</label><input type="range" data-ai="' + F[0] +
      '" min="' + F[1] + '" max="' + F[2] + '" step="' + F[3] + '" value="' + ai[F[0]] +
      '"><span class="v" data-aiv="' + F[0] + '">' + ai[F[0]] + '</span></div>').join('') +
      '<div class="hint">These ARE live - <code>STAGE_AI_PROFILE</code> is read every frame by the ' +
      'wave pump, so a change lands immediately. ⚠ <code>cap</code> is the on-screen limit the pump ' +
      'gates on: set it low and the wave index stops advancing, which reads as a broken wave script ' +
      'and is not. That is what froze the L6 fleet probe at wave 9 with 10 units alive.</div>'
      : '<div class="hint">no profile row for this stage</div>');

  /* the wave plan */
  h += sec('sw', 'WAVE PLAN', SA.plan ? (SA.plan.length + ' waves') : '—',
    '<div class="row"><button class="tb" id="s-plan">READ THE PLAN</button>' +
    '<button class="tb" id="s-clear2">CLEAR FIELD</button></div>' +
    (SA.plan ? planHtml() : '<div class="hint">Reading the plan DRY-RUNS every wave to see what it ' +
      'contains - that is the only way to know, because a wave is a function that spawns rather ' +
      'than a list. The field and the current stage are saved and put back.</div>'));

  box.innerHTML = h;
  wireSections(); wireStage();
}

function planHtml() {
  const tot = SA.plan.reduce((a, w) => a + (w.n || 0), 0);
  const bad = SA.plan.filter(w => w.err);
  return '<div class="hint">' + SA.plan.length + ' waves, ' + tot + ' units' +
    (bad.length ? (' — ⚠ ' + bad.length + ' threw') : '') + '. Click a row to fire that wave now.</div>' +
    SA.plan.map(w =>
      '<div class="f wide wv" data-wave="' + w.i + '" style="cursor:var(--cur-pointer)">' +
      '<label>' + (w.t) + 's</label><span class="v mono">' +
      (w.err ? ('⚠ ' + w.err) : (w.n + '× ' + (w.types || []).slice(0, 3).join(', ') +
        ((w.types || []).length > 3 ? '…' : ''))) + '</span></div>').join('');
}

function wireStage() {
  const d = api();
  const sel = $('#s-stage');
  if (sel) sel.onchange = () => { SA.stage = +sel.value; SA.plan = null; renderStage(); };
  const op = $('#s-open');
  if (op) op.onclick = () => {
    const t = $('#t-stage'); if (t) { t.value = SA.stage; }
    labOpen(); msg('stage ' + SA.stage + ' open');
  };
  const scr = $('#s-scroll');
  if (scr) scr.oninput = () => {
    const r = d.scrollTo(parseFloat(scr.value));
    $('#sv-scroll').textContent = Math.round(scr.value * 100) + '%';
    if (r === false) msg('no scroll range - open a stage first');
  };
  $$('#insp input[data-ai]').forEach(r => {
    r.oninput = () => {
      const k = r.dataset.ai, v = parseFloat(r.value);
      const out = $('#insp [data-aiv="' + k + '"]'); if (out) out.textContent = v;
      const p = {}; p[k] = v;
      d.setAiProfile(SA.stage, p);
    };
  });
  const pl = $('#s-plan');
  if (pl) pl.onclick = () => {
    msg('dry-running every wave on stage ' + SA.stage + '…');
    SA.plan = d.stagePlan(SA.stage);
    renderStage();
    msg(SA.plan.length + ' waves read');
  };
  const cl = $('#s-clear2'); if (cl) cl.onclick = () => clearField();
  $$('#insp .wv').forEach(el => {
    el.onclick = () => {
      const r = d.runWave(SA.stage, +el.dataset.wave);
      msg(typeof r === 'object' ? ('wave ' + el.dataset.wave + ': ' + r.spawned + ' spawned') : ('wave: ' + r));
    };
  });
}

/* ---------------- the overlay: FOV, anchors, hull ---------------- */
function drawOverlay(){
  const cv=$('#overlay'), wrap=$('#stage-wrap');
  const d=api();
  const g0=cv.getContext('2d'); g0.clearRect(0,0,cv.width,cv.height);
  if(!d||!host.ok) return;
  const u=unit(); if(!u) return;
  const s=d.snapshot();

  /* ============================================================
     PIN THE OVERLAY TO THE GUEST CANVAS, MEASURED - DO NOT COMPUTE A LETTERBOX.

     The first cut sized this canvas to #stage-wrap and derived the letterbox itself
     (`sc=min(W/VW,H/VH)`, `ox=(W-VW*sc)/2`). Measured against the engine's own CTM that was
     **19.3px out horizontally and 19.8px vertically** - index.html places its canvas inside the
     iframe with its own layout, which no amount of arithmetic out here can know about. bossmode.js
     has always read `#screen`'s getBoundingClientRect and put its overlay exactly there; doing the
     same makes the letterbox a MEASUREMENT rather than an assumption, and the editor then only has
     to map world -> canvas.
     ⚠ Offsets are taken relative to the overlay's own positioned parent, not the viewport: #overlay
     is absolute inside #stage-wrap, so raw clientRect coords would re-introduce the dock's width.
     ============================================================ */
  let r=null;
  try{ const gc=host.win.document.getElementById('screen'); if(gc) r=gc.getBoundingClientRect(); }catch(e){}
  if(!r||!r.width){ if(cv.width!==1){ cv.width=1; cv.height=1; } return; }
  /* ⚠ THE GUEST RECT IS IN THE IFRAME'S COORDINATE SYSTEM, NOT THE PAGE'S. `r.left` is measured
     inside the guest document, so it has to be carried into page space by the IFRAME's own rect
     before being made relative to the overlay's positioned parent. Skipping that middle term put
     the overlay out by exactly the iframe's page offset - measured -51px across and -106px down,
     which is the rail's width and the header+toolbar's height. It only looks right when the iframe
     sits at the page origin, which it never does here. */
  const fr=$('#host').getBoundingClientRect(), pr=wrap.getBoundingClientRect();
  cv.style.left=Math.round(fr.left+r.left-pr.left)+'px';
  cv.style.top =Math.round(fr.top +r.top -pr.top )+'px';
  const W=Math.round(r.width), H=Math.round(r.height);
  if(cv.width!==W||cv.height!==H){ cv.width=W; cv.height=H; }
  const g=cv.getContext('2d'); g.clearRect(0,0,W,H);

  /* ⚠ WORLD -> CANVAS, AND BOTH TERMS MATTER. drawWorld scales by viewZoom() and then anchors the
     BOTTOM edge (`translate(0, VH*(1-vz)/vz)`), and applies translate(-camX) only while the world
     is wider than the view. So x is `(x-cam)*vz` and y is `y*vz + VH*(1-vz)` - NOT `y*vz`, which is
     right only at vz=1. CLAUDE.md records this world-vs-screen class five times; the cone sat ~190px
     right of the ship on a scrolled stage while every number printed looked correct.
     `bustCam` exists so the probe can prove the mapping is load-bearing: with it set this goes back
     to reading world coords as screen coords and the alignment check must FAIL. */
  const k=W/s.VW;
  const vz=S.bustCam?1:(s.vz||1), cam=S.bustCam?0:(s.camX||0);
  const sc=k;
  const X=x=>(x-cam)*vz*k, Y=y=>(y*vz+s.VH*(1-vz))*k;

  /* where the overlay PUT the unit, in overlay-canvas px. Recorded rather than recomputed, so the
     probe reads what was drawn instead of re-deriving the formula under test. */
  S._mark={x:X(u.x), y:Y(u.y), sc:sc, vz:vz, cam:cam, k:k};

  if(S.hull){
    g.strokeStyle='#ff5a6e'; g.lineWidth=1.5;
    g.strokeRect(X(u.x-u.w/2), Y(u.y-u.h/2), u.w*sc*vz, u.h*sc*vz);
  }
  if(S.fov){
    /* the firing reach, as a cone. Range is not a field on an enemy - it is implied by bullet
       speed and life - so this draws the SHAPE the current inspector settings would produce. */
    const n=+($('#i-n')||{value:7}).value, sp=(+($('#i-spread')||{value:70}).value)*Math.PI/180;
    const R=Math.min(s.VH*0.9, 260)*sc*vz;
    const base=Math.PI/2;                          // enemies fire down-screen
    g.save();
    g.translate(X(u.x), Y(u.y));
    const grad=g.createRadialGradient(0,0,4,0,0,R);
    grad.addColorStop(0,'rgba(0,217,255,0.30)'); grad.addColorStop(1,'rgba(0,217,255,0.02)');
    g.fillStyle=grad;
    g.beginPath(); g.moveTo(0,0); g.arc(0,0,R, base-sp/2, base+sp/2); g.closePath(); g.fill();
    g.strokeStyle='rgba(124,245,255,0.75)'; g.lineWidth=1;
    g.beginPath(); g.moveTo(0,0); g.arc(0,0,R, base-sp/2, base+sp/2); g.closePath(); g.stroke();
    /* one ray per round, so COUNT is visible as well as SPREAD */
    g.strokeStyle='rgba(124,245,255,0.5)';
    for(let k=0;k<n;k++){ const t=(n===1)?0:(k/(n-1)-0.5); const a2=base+t*sp;
      g.beginPath(); g.moveTo(0,0); g.lineTo(Math.cos(a2)*R, Math.sin(a2)*R); g.stroke(); }
    g.restore();
  }
  if(S.anchors){
    g.fillStyle='#7cf5ff';
    g.beginPath(); g.arc(X(u.x), Y(u.y), 3.5, 0, Math.PI*2); g.fill();
    g.strokeStyle='rgba(124,245,255,.5)'; g.lineWidth=1;
    g.beginPath(); g.moveTo(X(u.x)-9,Y(u.y)); g.lineTo(X(u.x)+9,Y(u.y));
    g.moveTo(X(u.x),Y(u.y)-9); g.lineTo(X(u.x),Y(u.y)+9); g.stroke();

    /* ⚠ THE MOUNT IS DRAWN FROM shipBossMount, NOT FROM (mx,my) RE-APPLIED OUT HERE. The engine
       composes the mount with the unit's pose rotation and scale, so recomputing `x + w*mx` in the
       editor would agree at rest and drift the moment anything banked - and it would be the editor
       checking its own arithmetic again, which is the whole lesson of the camera fix above. */
    if(S.tab==='fire' && d.mountPoint){
      const mp=d.mountPoint(u, F.slot);
      if(mp){
        const px=X(mp.x), py=Y(mp.y);
        g.strokeStyle='#ffc21a'; g.lineWidth=1.5;
        g.beginPath(); g.moveTo(px-7,py); g.lineTo(px+7,py);
        g.moveTo(px,py-7); g.lineTo(px,py+7); g.stroke();
        g.beginPath(); g.arc(px,py,4.5,0,Math.PI*2); g.stroke();
        /* the line from hull centre to the mount, so an offset reads as an offset */
        g.strokeStyle='rgba(255,194,26,.45)';
        g.beginPath(); g.moveTo(X(u.x),Y(u.y)); g.lineTo(px,py); g.stroke();
        g.fillStyle='#ffc21a'; g.font='10px Consolas,monospace';
        g.fillText(F.slot, px+7, py-6);
      }
    }
  }
}

/* ---------------- layout ---------------- */
function layoutApply(){
  const b=document.body;
  b.classList.toggle('nodock',!layout.dock);
  b.classList.toggle('theater',!!layout.theater);
  b.classList.toggle('drawer',!!layout.drawer);
  $('#v-insp').classList.toggle('on', layout.dock && !layout.theater);
  $('#v-theater').classList.toggle('on', !!layout.theater);
  $('#v-list').classList.toggle('on', !!layout.drawer);
  try{ localStorage.setItem('bof_bod_layout', JSON.stringify({dock:layout.dock,theater:layout.theater})); }catch(e){}
}
function toggleDrawer(on){ layout.drawer=(on==null)?!layout.drawer:!!on; layoutApply(); }
function toggleDock(on){ layout.dock=(on==null)?!layout.dock:!!on; if(layout.dock) layout.theater=false; layoutApply(); }
function toggleTheater(on){ layout.theater=(on==null)?!layout.theater:!!on; layoutApply(); }

function selectTab(t){
  S.tab=t; document.body.dataset.tab=t;
  $$('#tabs .tab').forEach(b=>b.classList.toggle('on', b.dataset.tab===t));
  $('#vt-tab').textContent={enemy:'ENEMY LAB',fire:'PROJECTILES',stage:'STAGE',art:'ART',json:'JSON'}[t]||t.toUpperCase();
  if(t==='enemy'||t==='fire'||t==='stage') renderInspector();
  else msg(t.toUpperCase()+' tab lands in a later increment — ENEMY LAB, FIRE and STAGE are live now.');
}

/* ---------------- boot ---------------- */
function wire(){
  $$('#tabs .tab').forEach(b=>b.onclick=()=>selectTab(b.dataset.tab));
  $('#v-list').onclick=()=>toggleDrawer(); $('#rail-list').onclick=()=>toggleDrawer();
  $('#drawer-close').onclick=()=>toggleDrawer(false);
  $('#v-insp').onclick=()=>toggleDock(); $('#dock-close').onclick=()=>toggleDock(false);
  $('#dock-open').onclick=()=>toggleDock(true);
  $('#v-theater').onclick=()=>toggleTheater();
  $('#roster-filter').oninput=e=>{ S.filter=e.target.value; renderRoster(); };
  $('#t-lab').onclick=labOpen;
  $('#b-spawn').onclick=spawn; $('#b-clear').onclick=clearField;
  $('#b-apply').onclick=()=>renderInspector();
  $('#e-apply').onclick=()=>renderInspector();
  $('#e-respawn').onclick=()=>{ clearField(); spawn(); };
  $('#t-fov').onchange=e=>S.fov=e.target.checked;
  $('#t-anchor').onchange=e=>S.anchors=e.target.checked;
  $('#t-hull').onchange=e=>S.hull=e.target.checked;
  $('#t-pause').onclick=()=>{
    const d=api(); if(!d||!d.lab.active) return;
    S.paused=!S.paused;
    try{ host.win.setState ? null : null; }catch(e){}
    $('#t-pause').classList.toggle('on',S.paused);
    msg(S.paused?'paused':'running');
  };
  document.addEventListener('keydown',e=>{
    if(/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) return;
    if(e.key==='l'||e.key==='L') toggleDrawer();
    else if(e.key==='Tab'){ e.preventDefault(); toggleDock(); }
    else if(e.key==='t'||e.key==='T'||e.key==='F11'){ e.preventDefault(); toggleTheater(); }
    else if(e.key==='s'||e.key==='S') spawn();
    else if(e.key==='c'||e.key==='C') clearField();
  });
  try{ Object.assign(layout, JSON.parse(localStorage.getItem('bof_bod_layout')||'{}')); }catch(e){}
  layout.drawer=false; layoutApply();
}

function frame(){
  hostTick();
  if(S.loop && (performance.now()%200)<17) fireOnce();
  const d=api();
  if(d&&host.ok){
    const s=d.snapshot(); const u=unit();
    $('#t-count').textContent=s.enemies+' units · '+s.eBullets+' rounds';
    $('#tf-state').textContent=s.lab?('lab s'+s.labStage):s.state;
    $('#tf-unit').textContent=u?(u.type+' hp '+Math.round(u.hp)):'no unit';
    $('#tf-pos').textContent=u?('x '+Math.round(u.x)+' y '+Math.round(u.y)):'';
  }
  drawOverlay();
  requestAnimationFrame(frame);
}

(async function boot(){
  try{
    await Promise.all([loadAtlas('buttons'), loadAtlas('icons')]);
    buildCSS();
  }catch(e){ console.error('pack failed to load', e); }
  wire();
  selectTab('enemy');
  requestAnimationFrame(frame);
})();

window.BOD={S, api, unit, spawn, clearField, labOpen, selectTab, toggleDrawer, toggleDock, toggleTheater, fireOnce};
})();
