/* ============================================================
   BOSS MODE — the editor (drop 0910a)

   Layout of this file:
     1. UI   — the pack's atlases become CSS (buttons, icons, window frames, loading bars) and a
               bitmap text helper for the three glyph faces
     2. HOST — the engine iframe (index.html?bossmode=1) and window.BOSSMODE behind it
     3. DOC  — one fight as a document: identity, art states, size, hp, movement, anchors,
               actions, phases, hitboxes, parts, notes. toPatch() is the subset the engine reads.
     4. VIEWS — boss list, inspector, plate editor, graphics browser, json, stage overlay, clips
     5. FILE — new / open / save / save as / import / export

   ⚠ WHAT IS LIVE AND WHAT IS DATA. The engine draws ONE plate per boss (CLAUDE.md: "NO BOSS
   SPLITS"), fires from the anchors in SHIPBOSS[kind].mounts, and phases its pats list evenly
   across the HP bar (shipBossPhase). So name / art states / size / hp / movement / anchors /
   pat+cd+proj / pats are LIVE the moment you APPLY. Extra hitboxes, parts, orientation and notes
   are saved in the .json for design and shown in the editor, but the shipping engine does not
   read them yet — the inspector says so on each such field rather than pretending.
   ============================================================ */
(function(){
'use strict';
const $=(s,el)=>(el||document).querySelector(s), $$=(s,el)=>Array.from((el||document).querySelectorAll(s));
const UI='assets/bossmode/ui/';
const SCHEMA='bof-bossmode/1';
const BTN_SCALE=0.36, BTN_SM=0.30, ICO_SCALE=0.1;

/* ================================================================== 1. UI ================= */
const A={};   // name -> {img, map}
function loadImg(src){ return new Promise((res,rej)=>{ const im=new Image(); im.onload=()=>res(im); im.onerror=()=>rej(new Error('img '+src)); im.src=src; }); }
async function loadAtlas(name){ const [img,map]=await Promise.all([loadImg(UI+name+'.png'), fetch(UI+name+'.json').then(r=>r.json())]); A[name]={img,map}; return A[name]; }
function rectOf(name, itemName){ const M=A[name].map; const i=M.items.findIndex(it=>it.name===itemName); if(i<0) return null; return M.atlas.rects[i]; }
function cellRule(sel, name, itemName, S){
  const r=rectOf(name,itemName); if(!r) return '';
  const im=A[name].img;
  return sel+'{width:'+Math.round(r.w*S)+'px;height:'+Math.round(r.h*S)+'px;background-image:url('+UI+name+'.png);'+
    'background-size:'+Math.round(im.width*S)+'px '+Math.round(im.height*S)+'px;background-position:-'+Math.round(r.x*S)+'px -'+Math.round(r.y*S)+'px}\n';
}
function crop(name, idx){ const M=A[name].map, r=M.atlas.rects[idx-1], it=M.items[idx-1];
  const c=document.createElement('canvas'); c.width=it.visible_size[0]; c.height=it.visible_size[1];
  c.getContext('2d').drawImage(A[name].img, r.x+it.placement[0], r.y+it.placement[1], c.width, c.height, 0,0,c.width,c.height); return c; }
function buildCSS(){
  let css='';
  for(const set of [['files','buttonsfiles'],['editor','buttonseditor']]){
    const M=A[set[1]].map;
    for(const it of M.items){
      const m=it.name.match(/^(.*)-(normal|hover|pressed)$/); if(!m) continue;
      const base='.pb[data-set='+set[0]+'][data-name='+m[1]+']';
      const sel = m[2]==='normal' ? base : (m[2]==='hover' ? base+':hover' : base+':active');
      css+=cellRule(sel, set[1], it.name, BTN_SCALE);
      css+=cellRule(sel.replace('.pb','.pb.sm'), set[1], it.name, BTN_SM);
    }
  }
  for(const it of A.icons.map.items) css+=cellRule('.ico[data-icon='+it.name+']','icons',it.name,ICO_SCALE);
  // window frame: frame 1 as a 9-slice. Title bar 72px, sides 24, bottom 32 (measured on the plate)
  const f1=crop('windows',1).toDataURL();
  css+='.win{border-image-source:url('+f1+');border-image-slice:72 24 32 24 fill;border-width:36px 12px 16px 12px;border-image-width:36px 12px 16px 12px}\n';
  const bar=crop('loading',1).toDataURL(), fillO=crop('loading',3).toDataURL(), fillR=crop('loading',4).toDataURL(), fillG=crop('loading',6).toDataURL();
  css+='#boot-bar,#tele-hp{background-image:url('+bar+')}\n#boot-bar-fill{background-image:url('+fillO+')}\n#tele-hp-fill{background-image:url('+fillG+')}\n#tele-hp-fill.low{background-image:url('+fillR+')}\n';
  const st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
}
/* bitmap text from the three glyph faces. Upper carries A-Z 0-9, lower a-z, symbols the rest. */
const bmCache={};
function bmGlyph(ch){
  let face=null;
  if(/[A-Z0-9]/.test(ch)) face='fontupper'; else if(/[a-z]/.test(ch)) face='fontlower'; else face='fontsymbols';
  const M=A[face]; if(!M) return null;
  const i=M.map.items.findIndex(it=>it.name===ch); if(i<0) return null;
  return {img:M.img, r:M.map.atlas.rects[i], it:M.map.items[i]};
}
function bm(text, h, color){
  const key=text+'|'+h+'|'+(color||''); if(bmCache[key]) return bmCache[key];
  const gs=[]; let w=0; const sp=Math.round(h*0.12);
  for(const ch of String(text)){
    if(ch===' '){ gs.push(null); w+=Math.round(h*0.42); continue; }
    const g=bmGlyph(ch); if(!g){ gs.push(null); w+=Math.round(h*0.3); continue; }
    const cellH=g.r.h, s=h/cellH*0.92; gs.push({g,s}); w+=Math.round(g.it.visible_size[0]*s)+sp;
  }
  const c=document.createElement('canvas'); c.width=Math.max(1,w); c.height=h;
  const x2=c.getContext('2d'); x2.imageSmoothingEnabled=true; let x=0;
  for(let i=0,ch=0;i<gs.length;i++){
    const e=gs[i]; const t=String(text)[i];
    if(!e){ x+= t===' '?Math.round(h*0.42):Math.round(h*0.3); continue; }
    const {g,s}=e, vw=g.it.visible_size[0], vh=g.it.visible_size[1];
    x2.drawImage(g.img, g.r.x+g.it.placement[0], g.r.y+g.it.placement[1], vw, vh, x, Math.round(h*0.06), Math.round(vw*s), Math.round(vh*s));
    x+=Math.round(vw*s)+sp;
  }
  if(color){ x2.globalCompositeOperation='source-atop'; x2.fillStyle=color; x2.fillRect(0,0,c.width,c.height); }
  bmCache[key]=c; return c;
}
function bmInto(el, text, h){ el.innerHTML=''; const c=bm(text,h||40); c.style.height=(h?h/2.5:16)+'px'; c.style.width='auto'; el.appendChild(c); }

/* ================================================================== 2. HOST =============== */
const host={ win:null, api:null, ready:false, err:'' };
function hostTick(){
  try{
    const f=$('#host'); host.win=f.contentWindow; host.api=host.win&&host.win.BOSSMODE||null;
    host.ready=!!(host.api&&host.api.ready&&host.api.state!=='boot'&&host.api.state!=='loading');
    if(host.api&&!host._hooked){ host._hooked=true; host.win.BOSSMODE_ONREC=onClip; }
  }catch(e){ host.err=String(e.message||e); host.ready=false; }
  return host.ready;
}
function api(){ return host.api; }
function hostFullscreenChrome(){
  try{ const d=host.win.document; if(d&&d.body&&!d.body.classList.contains('fs')){ d.body.classList.add('fs'); if(host.win.__bofFit) host.win.__bofFit(); } }catch(e){}
}

/* ================================================================== 3. DOC ================ */
const state={ doc:null, docs:{}, undo:[], sel:{stage:0,role:'',kind:''}, tab:'stage', plateState:0, dragging:null, snap:null, clips:[], gfxSel:null, inv:false, paused:false };
const hooks={ onDoc:null, onTab:null, overlay:null, scene:null };   // scene.js hangs off these
function clone(o){ return JSON.parse(JSON.stringify(o)); }
function loadDocs(){ try{ state.docs=JSON.parse(localStorage.getItem('bof_bossmode_docs')||'{}'); }catch(e){ state.docs={}; } }
function saveDocs(){ try{ localStorage.setItem('bof_bossmode_docs', JSON.stringify(state.docs)); }catch(e){} }
function fights(){ return host.api?host.api.fights():[]; }
function tables(){ return host.api?host.api.tables():null; }
function slotOf(kind){ return fights().find(f=>f.kind===kind)||null; }
/* a document from the engine's own row (stock + any saved override), or from the saved doc */
function docFor(kind, role, stage){
  const T=tables(); if(!T) return null;
  const stock=host.api.override.stock(kind); if(!stock) return null;
  const ov=host.api.override.get(kind)||{};
  const D=Object.assign({}, stock, ov);
  const saved=state.docs[kind];
  const slot=slotOf(kind);
  const d={
    schema:SCHEMA, kind, base:kind, role:role||(slot?slot.role:(D.mini?'mini':'boss')), stage:stage||(slot?slot.stage:0),
    name:D.name||kind.toUpperCase(),
    states:[{name:'intact', key:D.key||'', at:1.0}, {name:'damaged', key:(D.dmg&&D.dmg[0])||'', at:0.66}, {name:'critical', key:(D.dmg&&D.dmg[1])||'', at:0.33}],
    size:{w:D.w||160, h:D.h||120, ty:(D.ty!=null?D.ty:null), drawW:(D.drawW!=null?D.drawW:null), drawH:(D.drawH!=null?D.drawH:null)},
    hp:{hp:(D.hp!=null?D.hp:null), hpMul:(D.hpMul!=null?D.hpMul:null)},
    move:Object.assign({ampX:0,ampY:0,period:0,orbit:false}, D.move||{}),
    anchors:clone(D.mounts||{C:[0,0.4]}),
    orientation:{facing:'south', rotation:0},
    actions:{pat:D.pat||'', cd:(D.cd!=null?D.cd:1.2), proj:D.proj||'', pats:clone(D.pats||(D.pat?[D.pat]:[]))},
    hitboxes:[{name:'hull', x:0, y:0, w:D.w||160, h:D.h||120, live:true}],
    parts:[], notes:'', scene:(ov.scene?clone(ov.scene):null)
  };
  if(saved && saved.schema===SCHEMA){
    if(!d.scene && saved.scene) d.scene=clone(saved.scene);
    // the saved doc carries the data-only fields; the live fields come from the engine row so a
    // change made through the game's own tables is never hidden by a stale document
    d.orientation=saved.orientation||d.orientation; d.parts=saved.parts||[]; d.notes=saved.notes||'';
    if(saved.hitboxes) d.hitboxes=[d.hitboxes[0]].concat(saved.hitboxes.filter(h=>!h.live));
    if(saved.states) for(let i=0;i<3;i++) if(saved.states[i]&&saved.states[i].at!=null) d.states[i].at=saved.states[i].at;
    if(saved.name && !ov.name) d.name=saved.name;
  }
  return d;
}
/* the subset the engine reads. Everything else is design data that rides in the .json only. */
function toPatch(d){
  const p={ name:d.name, w:+d.size.w, h:+d.size.h, pat:d.actions.pat, cd:+d.actions.cd, proj:d.actions.proj,
    pats:d.actions.pats.filter(Boolean), move:{ampX:+d.move.ampX||0, ampY:+d.move.ampY||0, period:+d.move.period||0}, mounts:{} };
  if(d.move.orbit) p.move.orbit=true;
  for(const k in d.anchors){ const a=d.anchors[k]; p.mounts[k]=[+a[0]||0, +a[1]||0]; }
  if(d.states[0].key) p.key=d.states[0].key;
  const dmg=[d.states[1].key, d.states[2].key].filter(Boolean); if(dmg.length) p.dmg=dmg;
  if(d.size.ty!=null && d.size.ty!=='') p.ty=+d.size.ty;
  if(d.size.drawW!=null && d.size.drawW!=='') p.drawW=+d.size.drawW;
  if(d.size.drawH!=null && d.size.drawH!=='') p.drawH=+d.size.drawH;
  if(d.hp.hp!=null && d.hp.hp!=='') p.hp=+d.hp.hp; else if(d.hp.hpMul!=null && d.hp.hpMul!=='') p.hpMul=+d.hp.hpMul;
  const hull=d.hitboxes.find(h=>h.live); if(hull){ p.w=+hull.w; p.h=+hull.h; }
  if(d.scene && ((d.scene.tracks&&d.scene.tracks.length)||(d.scene.zones&&d.scene.zones.length))) p.scene=clone(d.scene);   // the scene director's data (0911a)
  return p;
}
function pushUndo(){ if(!state.doc) return; state.undo.push(JSON.stringify(state.doc)); if(state.undo.length>60) state.undo.shift(); }
function setDoc(d, keepUndo){ if(!keepUndo) state.undo=[]; state.doc=d; state.sel={stage:d.stage, role:d.role, kind:d.kind}; renderAll(); if(hooks.onDoc) try{ hooks.onDoc(d); }catch(e){} }
function msg(t, bad){ const e=$('#tf-msg'); e.textContent=t; e.style.color=bad?'var(--bad)':'var(--hot2)'; clearTimeout(msg._t); msg._t=setTimeout(()=>{ e.textContent=''; }, 7000); }
function applyDoc(opts){
  const d=state.doc; if(!d||!host.api) return false;
  const p=toPatch(d);
  const ok=host.api.override.apply(d.base, p, Object.assign({hp:true}, opts||{}));
  state.docs[d.kind]=clone(d); saveDocs();
  if(ok) msg('APPLIED to '+d.base+(host.api.override.armed?' (live)':' (saved; host arms overrides itself)')); else msg('engine has no row for '+d.base, true);
  renderList(); return ok;
}

/* ================================================================== 4. VIEWS ============== */
function renderAll(){ renderList(); renderInspector(); renderPlate(); renderJSON(); renderGraphics(); syncTitle(); }
function syncTitle(){ const d=state.doc; const T={stage:'STAGE',plate:'PLATE',scene:'SCENE',graphics:'ART',json:'JSON',clips:'CLIPS'}; $('#vt-tab').textContent=T[state.tab]||state.tab.toUpperCase(); $('#vt-name').textContent=d?d.name:''; const ds=$('#dock-sub'); if(ds) ds.textContent=d?(d.role.toUpperCase()+' · S'+d.stage):''; }
/* ---- boss list ---- */
function renderList(){
  const el=$('#list-groups'); el.innerHTML='';
  if(!host.ready){ el.innerHTML='<div class="hint">engine booting…</div>'; return; }
  const T=tables(), F=fights(), ov=host.api.override.all();
  const byStage={}; for(const f of F){ (byStage[f.stage]=byStage[f.stage]||[]).push(f); }
  for(const s of Object.keys(byStage).sort((a,b)=>a-b)){
    const g=document.createElement('div'); g.className='lg';
    const S=T.STAGES.find(x=>x.n==s); g.innerHTML='<h4>STAGE '+s+(S?' · '+S.sub:'')+'</h4>';
    for(const f of byStage[s]){
      const li=document.createElement('div'); li.className='li'+(state.doc&&state.doc.kind===f.kind?' on':'');
      const live=!!T.SHIPBOSS[f.kind];
      li.innerHTML='<span class="role '+f.role+'">'+(f.role==='boss'?'BOSS':'MINI')+'</span><span class="name">'+f.name+'</span>'+(ov[f.kind]?'<span class="ov">EDITED</span>':'')+(live?'':'<span class="ov" title="not on the SHIPBOSS table: playable, but its stats live in code">CODE</span>');
      li.onclick=()=>openFight(f.kind, f.role, f.stage);
      g.appendChild(li);
    }
    el.appendChild(g);
  }
  // rows on the table that no stage fields
  const spare=Object.keys(T.SHIPBOSS).filter(k=>!F.some(f=>f.kind===k));
  if(spare.length){
    const g=document.createElement('div'); g.className='lg'; g.innerHTML='<h4>UNSLOTTED ROWS</h4>';
    for(const k of spare){ const li=document.createElement('div'); li.className='li'+(state.doc&&state.doc.kind===k?' on':'');
      li.innerHTML='<span class="role">ROW</span><span class="name">'+(T.SHIPBOSS[k].name||k)+'</span>'+(ov[k]?'<span class="ov">EDITED</span>':'');
      li.onclick=()=>openFight(k, T.SHIPBOSS[k].mini?'mini':'boss', 0); g.appendChild(li); }
    el.appendChild(g);
  }
}
function openFight(kind, role, stage){
  const T=tables(); if(!T) return;
  if(layout.drawer) toggleDrawer(false);
  if(!T.SHIPBOSS[kind]){
    // a code-driven fight (e.g. the stage-1 helicopter): playable, not editable as a row
    const d={schema:SCHEMA, kind, base:kind, role, stage, name:host.api.name(kind), codeOnly:true, states:[{name:'intact',key:'',at:1},{name:'damaged',key:'',at:.66},{name:'critical',key:'',at:.33}],
      size:{w:0,h:0,ty:null,drawW:null,drawH:null}, hp:{hp:null,hpMul:null}, move:{ampX:0,ampY:0,period:0,orbit:false}, anchors:{}, orientation:{facing:'south',rotation:0},
      actions:{pat:'',cd:0,proj:'',pats:[]}, hitboxes:[], parts:[], notes:'this fight is built in code (spawnBoss / spawnSubBoss), not on the SHIPBOSS table - PLAY TEST works, the row editor does not apply'};
    setDoc(d); msg(d.name+' is code-driven: play test only', true); return;
  }
  setDoc(docFor(kind, role, stage)); msg('opened '+state.doc.name);
}
/* ---- inspector ---- */
const SEC_OPEN={identity:1, art:1, size:1, hp:1, weapons:1, patterns:1, phases:0, anchors:1, move:0, hitboxes:0, parts:0, notes:0};
function sec(id, icon, title, right, body){
  return '<div class="sec'+(SEC_OPEN[id]?'':' closed')+'" data-sec="'+id+'"><h3><span class="ico" data-icon="'+icon+'"></span>'+title+'<span class="r">'+(right||'')+'</span></h3><div class="sb">'+body+'</div></div>';
}
function fld(label, id, val, type, extra){ return '<div class="f"><label>'+label+'</label><input data-f="'+id+'" type="'+(type||'text')+'" value="'+(val==null?'':String(val).replace(/"/g,'&quot;'))+'" '+(extra||'')+'></div>'; }
function sel(label, id, val, opts, allowBlank){ return '<div class="f"><label>'+label+'</label><select data-f="'+id+'">'+(allowBlank?'<option value="">(none)</option>':'')+opts.map(o=>'<option value="'+o+'"'+(o===val?' selected':'')+'>'+o+'</option>').join('')+'</select></div>'; }
function allPatterns(){ const T=tables(); const s=new Set(); for(const k in T.SHIPBOSS){ const D=T.SHIPBOSS[k]; if(D.pat) s.add(D.pat); (D.pats||[]).forEach(p=>s.add(p)); } if(T.SHIP_ACTION_PROFILE) Object.keys(T.SHIP_ACTION_PROFILE).forEach(p=>s.add(p)); return [...s].sort(); }
function allProj(){ const s=new Set(['cryo','cyclone','glacier','legion','magma','mirv','obsid','rampart','sludge','storm','toxic','warhawk']); const T=tables(); for(const k in T.SHIPBOSS) if(T.SHIPBOSS[k].proj) s.add(T.SHIPBOSS[k].proj); return [...s].sort(); }
function renderInspector(){
  const el=$('#insp'), d=state.doc;
  if(!d){ el.innerHTML='<div class="hint">open a fight from the BOSS LIST, or OPEN BOSS above</div>'; return; }
  const T=tables(); const stock=host.api.override.stock(d.base)||{};
  let h='';
  h+=sec('identity','boss','IDENTITY', d.role.toUpperCase()+' · STAGE '+(d.stage||'-'),
    fld('NAME','name',d.name)+fld('KIND','kind',d.kind,'text','readonly class="ro"')+fld('BASE ROW','base',d.base,'text','readonly class="ro"')+
    sel('ROLE','role',d.role,['boss','mini'])+fld('STAGE','stage',d.stage,'number','min="0" max="9"')+
    (d.codeOnly?'<div class="hint bad">code-driven fight: the fields below are not read by the engine</div>':''));
  // states as data
  let st='<table class="t"><tr><th>STATE</th><th>ART KEY</th><th>AT HP</th><th></th></tr>';
  d.states.forEach((s,i)=>{ const rdy=s.key&&host.api.art.rdy(s.key); st+='<tr><td>'+s.name.toUpperCase()+'</td><td><input data-f="states.'+i+'.key" value="'+s.key+'"></td><td><input class="n" type="number" step="0.01" min="0" max="1" data-f="states.'+i+'.at" value="'+s.at+'"></td><td>'+(s.key?(rdy?'<span class="tag">ok</span>':'<span class="tag miss" title="not decoded yet, or not registered">?</span>'):'')+'</td></tr>'; });
  st+='</table><div class="hint">the engine swaps damaged at 66% and critical at 33% (drawn whole, never split). AT HP is design data.</div>';
  h+=sec('art','part','ART STATES', d.states.filter(s=>s.key).length+' plates', st);
  h+=sec('size','hitbox','SIZE & PLACEMENT', d.size.w+'×'+d.size.h,
    fld('W (hull box)','size.w',d.size.w,'number')+fld('H (hull box)','size.h',d.size.h,'number')+fld('TY (hover y)','size.ty',d.size.ty,'number','placeholder="engine default"')+
    fld('DRAW W','size.drawW',d.size.drawW,'number','placeholder="= W"')+fld('DRAW H','size.drawH',d.size.drawH,'number','placeholder="= H"')+
    '<div class="hint">W×H is the hit box AND the plate\'s drawn size unless DRAW W/H override it. Stock: '+(stock.w||'-')+'×'+(stock.h||'-')+'</div>');
  const hpNote=(d.hp.hp!=null&&d.hp.hp!=='')?('absolute '+d.hp.hp+' × eHp '+(T.DIFF&&T.DIFF.eHp||1)+' = '+Math.ceil((+d.hp.hp)*((T.DIFF&&T.DIFF.eHp)||1))):('multiplier of the stage seed'+(d.role==='mini'?' (100)':' (220+120·stage, floored)'));
  h+=sec('hp','damage','HP', '', fld('HP (absolute)','hp.hp',d.hp.hp,'number','placeholder="use multiplier"')+fld('HP MUL','hp.hpMul',d.hp.hpMul,'number','step="0.01" placeholder="use absolute"')+'<div class="hint">'+hpNote+'. Stock: '+(stock.hp!=null?('hp '+stock.hp):('hpMul '+stock.hpMul))+'</div>');
  h+=sec('weapons','cannon','WEAPONS', d.actions.pat||'-',
    sel('PATTERN','actions.pat',d.actions.pat,allPatterns(),true)+fld('COOLDOWN s','actions.cd',d.actions.cd,'number','step="0.01"')+sel('PROJECTILE','actions.proj',d.actions.proj,allProj(),true)+
    '<div class="hint">PATTERN is the fallback when PATTERNS below is empty; PROJECTILE picks the bfx_&lt;proj&gt; muzzle + round family.</div>');
  // patterns
  let pt='<table class="t"><tr><th>#</th><th>PATTERN</th><th>FIRES FROM</th><th></th></tr>';
  d.actions.pats.forEach((p,i)=>{ const slots=host.api.patternSlots(p,1)||[]; const miss=slots.filter(s=>!d.anchors[s]);
    pt+='<tr><td>'+(i+1)+'</td><td><select data-f="actions.pats.'+i+'">'+allPatterns().map(o=>'<option'+(o===p?' selected':'')+'>'+o+'</option>').join('')+'</select></td><td>'+slots.map(s=>'<span class="tag'+(d.anchors[s]?'':' miss')+'">'+s+'</span>').join('')+'</td><td><span class="up" data-up="'+i+'">▲</span><span class="dn" data-dn="'+i+'">▼</span><span class="x" data-delpat="'+i+'">✕</span></td></tr>'; });
  pt+='</table><div class="row"><button class="tb" id="i-addpat"><span class="ico" data-icon="new"></span>ADD PATTERN</button></div><div class="hint">each pattern is a phase; the fight moves down the list as the bar drains. A red slot is an anchor this pattern fires from that the boss does not have.</div>';
  h+=sec('patterns','pattern','PATTERNS / ACTIONS', d.actions.pats.length+' phases', pt);
  // phases (derived)
  const n=d.actions.pats.length; let ph='<table class="t"><tr><th>PHASE</th><th>FROM HP</th><th>TO HP</th><th>PATTERN</th><th>TELL / RECOVER</th></tr>';
  for(let i=0;i<n;i++){ const pr=T.SHIP_ACTION_PROFILE&&T.SHIP_ACTION_PROFILE[d.actions.pats[i]]; ph+='<tr><td>'+(i+1)+'</td><td>'+Math.round(100*(1-i/n))+'%</td><td>'+Math.round(100*(1-(i+1)/n))+'%</td><td>'+d.actions.pats[i]+'</td><td>'+(pr?(pr.tell+' / '+pr.recover+'s'):'default')+'</td></tr>'; }
  if(!n) ph+='<tr><td colspan=5>single phase: '+(d.actions.pat||'-')+'</td></tr>';
  ph+='</table><div class="hint">phases are even across the bar by engine rule (shipBossPhase) - reorder PATTERNS to change them.</div>';
  h+=sec('phases','phases','PHASES', n+' · even split', ph);
  // anchors
  let an='<table class="t"><tr><th>NAME</th><th>FX</th><th>FY</th><th></th></tr>';
  for(const k of Object.keys(d.anchors)){ const a=d.anchors[k]; an+='<tr><td><input class="n" data-anch-name="'+k+'" value="'+k+'"></td><td><input class="n" type="number" step="0.005" data-f="anchors.'+k+'.0" value="'+a[0]+'"></td><td><input class="n" type="number" step="0.005" data-f="anchors.'+k+'.1" value="'+a[1]+'"></td><td><span class="x" data-delanch="'+k+'">✕</span></td></tr>'; }
  an+='</table><div class="row"><button class="tb" id="i-addanch"><span class="ico" data-icon="path"></span>ADD ANCHOR</button><span class="hint">drag them on the PLATE tab</span></div>'+
    '<div class="hint">hull fractions from the plate\'s centre: +X right, +Y toward the nose (south). C:[0,0.42] is the nose gun.</div>'+
    '<div class="f"><label>FACING</label><select data-f="orientation.facing"><option'+(d.orientation.facing==='south'?' selected':'')+'>south</option><option'+(d.orientation.facing==='north'?' selected':'')+'>north</option></select></div>'+
    fld('ROTATION °','orientation.rotation',d.orientation.rotation,'number')+'<div class="hint warn">FACING / ROTATION are saved as data; the engine draws every ship boss nose-south.</div>';
  h+=sec('anchors','path','ANCHORS & ORIENTATION', Object.keys(d.anchors).length+' mounts', an);
  h+=sec('move','path','MOVEMENT', (d.move.ampX||0)+'/'+(d.move.ampY||0)+' · '+(d.move.period||0)+'s',
    fld('AMP X px','move.ampX',d.move.ampX,'number')+fld('AMP Y px','move.ampY',d.move.ampY,'number')+fld('PERIOD s','move.period',d.move.period,'number','step="0.05"')+
    '<div class="f"><label>ORBIT</label><input type="checkbox" data-f="move.orbit" '+(d.move.orbit?'checked':'')+'></div><div class="hint">a slow patrol: ampX 116 / period 5.8 reads as a boss; 150 / 2.7 with ORBIT is the void bat.</div>');
  // hitboxes
  let hb='<table class="t"><tr><th>NAME</th><th>X</th><th>Y</th><th>W</th><th>H</th><th></th></tr>';
  d.hitboxes.forEach((b,i)=>{ hb+='<tr><td><input class="n" data-f="hitboxes.'+i+'.name" value="'+b.name+'" '+(b.live?'readonly':'')+'></td><td><input class="n" type="number" data-f="hitboxes.'+i+'.x" value="'+b.x+'" '+(b.live?'readonly':'')+'></td><td><input class="n" type="number" data-f="hitboxes.'+i+'.y" value="'+b.y+'" '+(b.live?'readonly':'')+'></td><td><input class="n" type="number" data-f="hitboxes.'+i+'.w" value="'+b.w+'"></td><td><input class="n" type="number" data-f="hitboxes.'+i+'.h" value="'+b.h+'"></td><td>'+(b.live?'<span class="tag">LIVE</span>':'<span class="x" data-delhit="'+i+'">✕</span>')+'</td></tr>'; });
  hb+='</table><div class="row"><button class="tb" id="i-addhit"><span class="ico" data-icon="hitbox"></span>ADD HITBOX</button></div><div class="hint warn">HULL is the engine\'s one collision box (= SIZE W×H). Extra boxes are design data until the engine grows sub-hit zones.</div>';
  h+=sec('hitboxes','hitbox','HITBOXES', d.hitboxes.length+' boxes', hb);
  // parts
  let pa='<table class="t"><tr><th>PART</th><th>ART KEY</th><th>FX</th><th>FY</th><th>HP</th><th></th></tr>';
  d.parts.forEach((p,i)=>{ pa+='<tr><td><input class="n" data-f="parts.'+i+'.name" value="'+p.name+'"></td><td><input data-f="parts.'+i+'.key" value="'+(p.key||'')+'"></td><td><input class="n" type="number" step="0.005" data-f="parts.'+i+'.fx" value="'+p.fx+'"></td><td><input class="n" type="number" step="0.005" data-f="parts.'+i+'.fy" value="'+p.fy+'"></td><td><input class="n" type="number" data-f="parts.'+i+'.hp" value="'+(p.hp||0)+'"></td><td><span class="x" data-delpart="'+i+'">✕</span></td></tr>'; });
  pa+='</table><div class="hint warn">parts are saved as data. The shipping engine draws a boss as ONE plate with damage STATES (Mike\'s no-splits rule) - use ADD PART to plan turrets / pods for a future rig.</div>';
  h+=sec('parts','missiles','PARTS', d.parts.length+' parts', pa);
  h+=sec('notes','settings','NOTES', '', '<textarea data-f="notes" style="width:100%;height:70px">'+String(d.notes||'').replace(/</g,'&lt;')+'</textarea>');
  el.innerHTML=h;
  // wire
  $$('.sec>h3',el).forEach(hd=>hd.onclick=()=>{ const s=hd.parentElement; s.classList.toggle('closed'); SEC_OPEN[s.dataset.sec]=!s.classList.contains('closed'); });
  $$('[data-f]',el).forEach(inp=>{ inp.onchange=()=>{ pushUndo(); setPath(d, inp.dataset.f, inp.type==='checkbox'?inp.checked:(inp.type==='number'?(inp.value===''?null:+inp.value):inp.value)); afterEdit(); }; });
  $$('[data-anch-name]',el).forEach(inp=>{ inp.onchange=()=>{ const old=inp.dataset.anchName, nu=inp.value.trim(); if(!nu||nu===old||d.anchors[nu]) { inp.value=old; return; } pushUndo(); d.anchors[nu]=d.anchors[old]; delete d.anchors[old]; afterEdit(); }; });
  $$('[data-delanch]',el).forEach(x=>x.onclick=()=>{ pushUndo(); delete d.anchors[x.dataset.delanch]; afterEdit(); });
  $$('[data-delpat]',el).forEach(x=>x.onclick=()=>{ pushUndo(); d.actions.pats.splice(+x.dataset.delpat,1); afterEdit(); });
  $$('[data-up]',el).forEach(x=>x.onclick=()=>{ const i=+x.dataset.up; if(i<1) return; pushUndo(); const a=d.actions.pats; [a[i-1],a[i]]=[a[i],a[i-1]]; afterEdit(); });
  $$('[data-dn]',el).forEach(x=>x.onclick=()=>{ const i=+x.dataset.dn; const a=d.actions.pats; if(i>=a.length-1) return; pushUndo(); [a[i+1],a[i]]=[a[i],a[i+1]]; afterEdit(); });
  $$('[data-delhit]',el).forEach(x=>x.onclick=()=>{ pushUndo(); d.hitboxes.splice(+x.dataset.delhit,1); afterEdit(); });
  $$('[data-delpart]',el).forEach(x=>x.onclick=()=>{ pushUndo(); d.parts.splice(+x.dataset.delpart,1); afterEdit(); });
  const ap=$('#i-addpat',el); if(ap) ap.onclick=()=>{ pushUndo(); d.actions.pats.push(d.actions.pat||allPatterns()[0]); afterEdit(); };
  const aa=$('#i-addanch',el); if(aa) aa.onclick=addAnchor;
  const ah=$('#i-addhit',el); if(ah) ah.onclick=addHitbox;
}
function setPath(o, path, v){ const ks=path.split('.'); let t=o; for(let i=0;i<ks.length-1;i++){ if(t[ks[i]]==null) t[ks[i]]={}; t=t[ks[i]]; } t[ks[ks.length-1]]=v; }
function afterEdit(){
  const d=state.doc;
  // the hull hitbox mirrors SIZE both ways
  const hull=d.hitboxes.find(h=>h.live); if(hull){ if(hull.w!==d.size.w||hull.h!==d.size.h){ if(afterEdit._from==='hull'){ d.size.w=hull.w; d.size.h=hull.h; } else { hull.w=d.size.w; hull.h=d.size.h; } } }
  renderInspector(); renderPlate(); renderJSON(); syncTitle();
  if($('#p-live').checked && !d.codeOnly) applyDoc({});
}
function addAnchor(){ const d=state.doc; if(!d) return; pushUndo(); let i=1; while(d.anchors['A'+i]) i++; d.anchors['A'+i]=[0,0.3]; afterEdit(); }
function addHitbox(){ const d=state.doc; if(!d) return; pushUndo(); d.hitboxes.push({name:'zone'+d.hitboxes.length, x:0, y:0, w:Math.round(d.size.w/3), h:Math.round(d.size.h/3), live:false}); afterEdit(); }
function addPart(){ const d=state.doc; if(!d) return; pushUndo(); d.parts.push({name:'part'+(d.parts.length+1), key:'', fx:0, fy:0, hp:0}); SEC_OPEN.parts=1; afterEdit(); }

/* ---- plate editor ---- */
const P={ z:1.5, off:[0,0], img:null, key:'' };
function plateKey(){ const d=state.doc; if(!d) return ''; const s=d.states[state.plateState]; return (s&&s.key)||d.states[0].key||''; }
function renderPlate(){
  const cv=$('#plate'), d=state.doc; if(!d) return;
  const key=plateKey(); let im=null;
  try{ if(key&&host.api&&host.api.art.rdy(key)) im=host.api.art.raw(key); }catch(e){}
  if(!im){ if(key){ try{ host.api.art.rdy(key); }catch(e){} } }
  const W=$('#plate-wrap').clientWidth-2, H=$('#plate-wrap').clientHeight-2;
  const z=P.z; const bw=(d.size.drawW||d.size.w||160), bh=(d.size.drawH||d.size.h||120);
  cv.width=Math.max(W, Math.round(bw*z+160)); cv.height=Math.max(H, Math.round(bh*z+160));
  const x=cv.getContext('2d'); x.clearRect(0,0,cv.width,cv.height); x.imageSmoothingEnabled=false;
  const cx=cv.width/2, cy=cv.height/2; P.c=[cx,cy]; P.bw=bw; P.bh=bh;
  if(im){ x.drawImage(im, cx-bw*z/2, cy-bh*z/2, bw*z, bh*z); }
  else { x.fillStyle='rgba(255,138,30,.15)'; x.fillRect(cx-bw*z/2, cy-bh*z/2, bw*z, bh*z); x.fillStyle='#ff8a1e'; x.font='12px monospace'; x.textAlign='center'; x.fillText(key?('decoding '+key+' …'):'no plate key', cx, cy); if(key) setTimeout(renderPlate, 400); }
  // hull box (live) + extra hitboxes (data)
  const hw=d.size.w*z, hh=d.size.h*z;
  x.strokeStyle='#8de23a'; x.lineWidth=1.5; x.setLineDash([6,4]); x.strokeRect(cx-hw/2, cy-hh/2, hw, hh); x.setLineDash([]);
  for(const b of d.hitboxes){ if(b.live) continue; x.strokeStyle='#4aa8ff'; x.strokeRect(cx+(b.x-b.w/2)*z, cy+(b.y-b.h/2)*z, b.w*z, b.h*z); x.fillStyle='#4aa8ff'; x.font='10px monospace'; x.textAlign='left'; x.fillText(b.name, cx+(b.x-b.w/2)*z+2, cy+(b.y-b.h/2)*z+10); }
  // facing arrow
  x.strokeStyle='rgba(255,194,26,.7)'; x.lineWidth=2; x.beginPath(); const ay=d.orientation.facing==='north'?-1:1; x.moveTo(cx, cy-ay*hh*0.1); x.lineTo(cx, cy+ay*hh*0.62); x.lineTo(cx-6, cy+ay*hh*0.62-ay*10); x.moveTo(cx, cy+ay*hh*0.62); x.lineTo(cx+6, cy+ay*hh*0.62-ay*10); x.stroke();
  // parts
  for(const p of d.parts){ const px=cx+(+p.fx||0)*hw, py=cy+(+p.fy||0)*hh; x.strokeStyle='#ff8a7a'; x.strokeRect(px-8,py-8,16,16); x.fillStyle='#ff8a7a'; x.font='10px monospace'; x.textAlign='left'; x.fillText(p.name, px+10, py+4); }
  // anchors
  const need=new Set(); for(const p of d.actions.pats.concat(d.actions.pat?[d.actions.pat]:[])) (host.api.patternSlots(p,1)||[]).forEach(s=>need.add(s));
  for(const k in d.anchors){ const a=d.anchors[k]; const px=cx+(+a[0]||0)*hw, py=cy+(+a[1]||0)*hh; const used=need.has(k);
    x.strokeStyle=used?'#ffc21a':'#8a919c'; x.lineWidth=2; x.beginPath(); x.moveTo(px-9,py); x.lineTo(px+9,py); x.moveTo(px,py-9); x.lineTo(px,py+9); x.stroke();
    x.beginPath(); x.arc(px,py,5,0,Math.PI*2); x.stroke(); x.fillStyle=used?'#ffc21a':'#8a919c'; x.font='bold 11px monospace'; x.textAlign='left'; x.fillText(k, px+8, py-6); }
  for(const s of need) if(!d.anchors[s]){ x.fillStyle='#ff4a4a'; x.font='bold 11px monospace'; x.textAlign='center'; x.fillText('MISSING ANCHOR: '+s, cx, cy-hh/2-14-(Array.from(need).indexOf(s))*0); }
  $('#plate-readout').textContent=(key||'(no key)')+'   '+bw+'×'+bh+' @ '+z.toFixed(2)+'x   hull '+d.size.w+'×'+d.size.h+'\n'+(P.hover||'');
  $$('#plate-tools .st').forEach(b=>b.classList.toggle('on', +b.dataset.state===state.plateState));
}
function plateHit(mx,my){ const d=state.doc; if(!d) return null; const [cx,cy]=P.c; const hw=d.size.w*P.z, hh=d.size.h*P.z; let best=null, bd=14;
  for(const k in d.anchors){ const a=d.anchors[k]; const px=cx+(+a[0])*hw, py=cy+(+a[1])*hh; const dd=Math.hypot(mx-px,my-py); if(dd<bd){ bd=dd; best=k; } } return best; }
function plateMouse(){
  const cv=$('#plate');
  const pos=e=>{ const r=cv.getBoundingClientRect(); return [e.clientX-r.left, e.clientY-r.top]; };
  cv.onmousedown=e=>{ const [mx,my]=pos(e); const k=plateHit(mx,my); if(k){ pushUndo(); state.dragging=k; cv.classList.add('drag'); } };
  cv.onmousemove=e=>{ const d=state.doc; if(!d) return; const [mx,my]=pos(e); const [cx,cy]=P.c; const fx=((mx-cx)/(d.size.w*P.z)), fy=((my-cy)/(d.size.h*P.z));
    P.hover='cursor  fx '+fx.toFixed(3)+'  fy '+fy.toFixed(3)+'   px '+Math.round(fx*d.size.w)+','+Math.round(fy*d.size.h);
    if(state.dragging){ const snap=e.shiftKey?0.05:0.005; d.anchors[state.dragging]=[Math.round(fx/snap)*snap, Math.round(fy/snap)*snap]; renderPlate(); } else { $('#plate-readout').textContent=$('#plate-readout').textContent.split('\n')[0]+'\n'+P.hover; } };
  window.addEventListener('mouseup',()=>{ if(state.dragging){ state.dragging=null; cv.classList.remove('drag'); afterEdit(); } });
  cv.ondblclick=e=>{ const d=state.doc; if(!d) return; const [mx,my]=pos(e); const [cx,cy]=P.c; pushUndo(); let i=1; while(d.anchors['A'+i]) i++; d.anchors['A'+i]=[+((mx-cx)/(d.size.w*P.z)).toFixed(3), +((my-cy)/(d.size.h*P.z)).toFixed(3)]; afterEdit(); };
}
/* ---- graphics browser ---- */
const G={keys:[], thumbs:{}};
function renderGraphics(){
  const d=state.doc, grid=$('#gfx-grid'); if(!d||!host.ready){ grid.innerHTML=''; return; }
  const keys=host.api.art.keysFor(d.base); G.keys=keys;
  const f=$('#gfx-filter').value.trim().toLowerCase(); const shown=keys.filter(k=>!f||k.indexOf(f)>=0);
  $('#gfx-count').textContent=shown.length+' / '+keys.length+' keys for '+d.base;
  grid.innerHTML='';
  for(const k of shown.slice(0,400)){
    const e=document.createElement('div'); e.className='gk'+(state.gfxSel===k?' on':''); const c=document.createElement('canvas'); c.width=88; c.height=64; e.appendChild(c);
    const t=document.createElement('div'); t.textContent=k; t.title=k; e.appendChild(t); e.onclick=()=>{ state.gfxSel=k; $$('.gk',grid).forEach(x=>x.classList.toggle('on', x.firstChild===c)); bigGfx(k); };
    grid.appendChild(e); thumb(k, c, 0);
  }
}
function thumb(k, c, tries){
  let im=null; try{ if(host.api.art.rdy(k)) im=host.api.art.raw(k); }catch(e){}
  if(!im){ if(tries<40) setTimeout(()=>thumb(k,c,tries+1), 250+tries*50); return; }
  const x=c.getContext('2d'); x.clearRect(0,0,c.width,c.height); x.imageSmoothingEnabled=false; const s=Math.min(c.width/im.width, c.height/im.height, 1); const w=im.width*s, h=im.height*s; x.drawImage(im,(c.width-w)/2,(c.height-h)/2,w,h);
}
function bigGfx(k){
  const c=$('#gfx-big-cv'); let im=null; try{ if(host.api.art.rdy(k)) im=host.api.art.raw(k); }catch(e){}
  if(!im){ $('#gfx-big-txt').textContent=k+'\n(decoding)'; setTimeout(()=>bigGfx(k),300); return; }
  c.width=im.width; c.height=im.height; c.getContext('2d').drawImage(im,0,0);
  const cell=host.api.art.cell(k), img=host.api.art.img(k);
  $('#gfx-big-txt').textContent=k+'\n'+im.width+'×'+im.height+'\n'+(cell?('cell on sheet '+cell[0]+' @ '+cell[1]+','+cell[2]):('file '+(img||'?')));
}
/* ---- json ---- */
function renderJSON(){ const d=state.doc; $('#json').value=d?JSON.stringify(d,null,2):''; $('#j-err').textContent=''; }
function applyJSONText(){
  try{ const j=JSON.parse($('#json').value); if(j.schema!==SCHEMA) throw new Error('schema must be '+SCHEMA); pushUndo(); state.doc=j; state.undo=state.undo; renderAll(); applyDoc({}); }
  catch(e){ $('#j-err').textContent=String(e.message||e); }
}
/* ---- stage overlay + telemetry ---- */
function tick(){
  const was=host.ready; hostTick();
  const led=$('#host-led'), txt=$('#host-txt');
  if(!host.api){ led.className='led bad'; txt.textContent=host.err?('ENGINE ERROR: '+host.err.slice(0,40)):'ENGINE LOADING'; }
  else if(!host.ready){ led.className='led busy'; txt.textContent='ENGINE BOOTING ('+host.api.state+')'; }
  else { led.className='led on'; txt.textContent='ENGINE '+String(host.api.state).toUpperCase(); }
  if(host.ready && !was){ onHostReady(); }
  if(!host.ready) return;
  let s=null; try{ s=host.api.snapshot(); }catch(e){}
  state.snap=s; if(!s) return;
  const b=s.boss; const f=$('#tele-hp-fill');
  if(b&&b.maxhp){ const fr=Math.max(0,Math.min(1,b.hp/b.maxhp)); f.style.width=(fr*97)+'%'; f.classList.toggle('low', fr<0.33); $('#tele-hp-txt').textContent=Math.ceil(b.hp)+' / '+Math.ceil(b.maxhp)+'  '+Math.round(fr*100)+'%'; }
  else { f.style.width='0'; $('#tele-hp-txt').textContent='—'; }
  $('#tf-state').textContent=s.state+(s.fight?('  S'+s.fight.stage+' '+s.fight.role):'')+(s.warnT>0?('  WARNING '+s.warnT.toFixed(1)):'');
  $('#tf-boss').textContent=b?(b.name+(b.dead?' (DEAD '+b.dying.toFixed(1)+'s)':(b.enter?' (entering)':''))):'no boss';
  $('#tf-pat').textContent=b&&b.ship?('phase '+phaseOf(b)+(b.step!=null?'  step '+b.step:'')+'  cd '+(b.fireCd!=null?b.fireCd.toFixed(2):'-')):'';
  $('#tf-pos').textContent=b?('x '+Math.round(b.x)+'  y '+Math.round(b.y)+'  bullets '+s.eBullets):'';
  const rec=$('#tf-rec'); rec.textContent=s.recording?'● REC':''; rec.classList.toggle('on',!!s.recording);
  $('#t-rec').classList.toggle('on', !!s.recording); $('#t-pause').classList.toggle('on', s.state==='paused');
  $('#b-stop').classList.toggle('dis', !s.fight);
  drawOverlay(s);
}
function phaseOf(b){ const d=state.doc; const n=d&&d.actions.pats.length||1; const fr=b.maxhp?b.hp/b.maxhp:1; let i=Math.floor((1-fr)*n); if(i<0)i=0; if(i>n-1)i=n-1; return (i+1)+'/'+n+(d&&d.actions.pats[i]?(' '+d.actions.pats[i]):''); }
function drawOverlay(s){
  const ov=$('#stage-overlay'); const on=$('#t-overlay').checked && state.tab==='stage';
  let r=null; try{ const sc=host.win.document.getElementById('screen'); if(sc) r=sc.getBoundingClientRect(); }catch(e){}
  if(!on||!r||!s.boss||!s.fight){ ov.width=1; ov.height=1; return; }
  ov.style.left=r.left+'px'; ov.style.top=r.top+'px'; ov.width=Math.round(r.width); ov.height=Math.round(r.height);
  const x=ov.getContext('2d'); x.clearRect(0,0,ov.width,ov.height);
  const k=r.width/s.VW, b=s.boss, d=state.doc; const vz=s.vz||1;
  const sx=v=>(v-s.camX)*vz*k, sy=v=>(v*vz+s.VH*(1-vz))*k;
  const bx=sx(b.x), by=sy(b.y), bw=b.w*vz*k, bh=b.h*vz*k;
  x.strokeStyle='rgba(141,226,58,.8)'; x.lineWidth=1; x.setLineDash([4,3]); x.strokeRect(bx-bw/2, by-bh/2, bw, bh); x.setLineDash([]);
  if(d && d.base===(b.ship||b.kind)){
    for(const nm in d.anchors){ const a=d.anchors[nm]; const px=bx+(+a[0])*bw, py=by+(+a[1])*bh; x.strokeStyle='#ffc21a'; x.beginPath(); x.moveTo(px-6,py); x.lineTo(px+6,py); x.moveTo(px,py-6); x.lineTo(px,py+6); x.stroke(); x.fillStyle='#ffc21a'; x.font='10px monospace'; x.fillText(nm, px+5, py-4); }
  }
  x.fillStyle='rgba(0,0,0,.5)'; x.fillRect(4,4,150,14); x.fillStyle='#8de23a'; x.font='10px monospace'; x.fillText('hull '+Math.round(b.w)+'×'+Math.round(b.h)+'  hp '+Math.round(100*(b.hp/(b.maxhp||1)))+'%', 8, 14);
  if(hooks.overlay) try{ hooks.overlay(x, s, k); }catch(e){}
}
function onHostReady(){
  hostFullscreenChrome();
  const T=tables(); const ps=$('#t-pilot'); ps.innerHTML=T.PILOTS.map(p=>'<option value="'+p.key+'"'+(p.key==='cole'?' selected':'')+'>'+p.name+'</option>').join('');
  renderList();
  const b=$('#boot'); $('#boot-bar-fill').style.width='97%'; $('#boot-bar-txt').textContent='READY'; setTimeout(()=>b.classList.add('gone'), 500);
  msg('engine ready · '+fights().length+' fights on the table');
  if(!state.doc){ const f=fights().find(x=>x.role==='boss'&&x.stage===2)||fights()[0]; if(f) openFight(f.kind,f.role,f.stage); }
}
/* ---- clips ---- */
function onClip(rec){ state.clips.unshift({name:rec.name, url:rec.url, size:rec.size, dur:rec.dur, t:Date.now()}); $('#clip-n').textContent='('+state.clips.length+')'; renderClips(); msg('clip saved: '+rec.name); }
function renderClips(){
  const el=$('#clips-list'); el.innerHTML=state.clips.length?'':'<div class="hint">press REC (or R in the fight) - the clip lands here and in your Downloads as a .webm</div>';
  state.clips.forEach((c,i)=>{ const e=document.createElement('div'); e.className='clip'+(state.clipSel===i?' on':''); e.innerHTML='<b>'+c.name+'</b><span>'+(c.size/1e6).toFixed(1)+' MB · '+c.dur.toFixed(0)+'s</span>'; e.onclick=()=>{ state.clipSel=i; $('#clip-video').src=c.url; $('#clip-video').play().catch(()=>{}); renderClips(); }; el.appendChild(e); });
}

/* ================================================================== 5. FILE =============== */
function download(name, text){ const blob=new Blob([text],{type:'application/json'}); const u=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=u; a.download=name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(u), 2000); }
function fileNew(){ const d=state.doc; if(!d) return msg('open a fight first', true); const nm=prompt('New variant name (kind id, letters/digits):', d.kind+'_v2'); if(!nm) return; const nd=clone(d); nd.kind=nm.replace(/[^a-z0-9_]/gi,'').toLowerCase(); nd.base=d.base; nd.name=(d.name+' V2').toUpperCase(); state.docs[nd.kind]=nd; saveDocs(); setDoc(nd); msg('new variant '+nd.kind+' of '+nd.base+' - PLAY TEST runs it on the base slot'); }
function fileOpen(){ const el=$('#open-list'); el.innerHTML=''; for(const f of fights()){ const e=document.createElement('div'); e.className='li'; e.innerHTML='<span class="role '+f.role+'">S'+f.stage+' '+(f.role==='boss'?'BOSS':'MINI')+'</span><span class="name">'+f.name+'</span>'; e.onclick=()=>{ $('#modal').classList.add('hidden'); openFight(f.kind,f.role,f.stage); }; el.appendChild(e); }
  for(const k in state.docs){ if(fights().some(f=>f.kind===k)) continue; const e=document.createElement('div'); e.className='li'; e.innerHTML='<span class="role">DOC</span><span class="name">'+(state.docs[k].name||k)+'</span>'; e.onclick=()=>{ $('#modal').classList.add('hidden'); setDoc(clone(state.docs[k])); }; el.appendChild(e); }
  $('#modal').classList.remove('hidden'); }
function fileSave(){ if(!state.doc) return; if(state.doc.codeOnly){ state.docs[state.doc.kind]=clone(state.doc); saveDocs(); return msg('saved doc (code-driven fight: nothing to apply)'); } applyDoc({}); msg('SAVED - '+state.doc.name+' is in the game\'s override store; F4 in the debug menu arms it for normal play'); }
function fileSaveAs(){ if(!state.doc) return; const nm=prompt('File name:', state.doc.kind+'.json'); if(!nm) return; download(nm.endsWith('.json')?nm:nm+'.json', JSON.stringify(state.doc,null,2)); }
function fileExport(){ if(!state.doc) return; download('bossmode_'+state.doc.kind+'.json', JSON.stringify(state.doc,null,2)); msg('exported bossmode_'+state.doc.kind+'.json'); }
function fileBundle(){ if(!host.ready) return; const all=host.api.override.all(); download('bossmode_overrides_'+new Date().toISOString().slice(0,10)+'.json', JSON.stringify({schema:'bof-bossmode-overrides/1', overrides:all, docs:state.docs},null,2)); msg(Object.keys(all).length+' overrides exported'); }
function fileImport(){ $('#file-in').value=''; $('#file-in').click(); }
function onImportFile(ev){
  const f=ev.target.files[0]; if(!f) return; const rd=new FileReader();
  rd.onload=()=>{ try{ const j=JSON.parse(rd.result);
    if(j.schema===SCHEMA){ if(!tables().SHIPBOSS[j.base]) throw new Error('base row '+j.base+' is not on this build'); state.docs[j.kind]=j; saveDocs(); setDoc(clone(j)); applyDoc({}); msg('imported '+j.name); }
    else if(j.schema==='bof-bossmode-overrides/1'){ let n=0; for(const k in j.overrides){ if(host.api.override.apply(k, j.overrides[k], {noSave:true})) n++; } host.api.override.arm(host.api.override.armed); for(const k in (j.docs||{})) state.docs[k]=j.docs[k]; saveDocs(); try{ host.win.localStorage.setItem('bof_bossmode', JSON.stringify(host.api.override.all())); }catch(e){} renderAll(); msg(n+' overrides imported'); }
    else throw new Error('not a Boss Mode file');
  }catch(e){ msg('import failed: '+(e.message||e), true); } };
  rd.readAsText(f);
}
function playTest(){ if(!host.ready) return msg('engine not ready', true); const d=state.doc; if(!d) return msg('open a fight first', true);
  const slot=slotOf(d.base); if(!slot) return msg(d.base+' has no stage slot to run in', true);
  if(!d.codeOnly) applyDoc({});
  const rec=$('#t-rec').classList.contains('arm');
  host.api.start(slot.stage, slot.role, $('#t-pilot').value, rec); state.inv=false; selectTab('stage'); msg('PLAY TEST · S'+slot.stage+' '+slot.role+' · '+d.name); setTimeout(()=>{ try{ $('#host').contentWindow.focus(); }catch(e){} }, 200); }
function stopTest(){ if(!host.ready) return; host.api.stop(); msg('stopped'); }

/* ---- wiring ---- */
function selectTab(t){ state.tab=t; document.body.dataset.tab=t; $$('#tabs .tab').forEach(b=>b.classList.toggle('on', b.dataset.tab===t)); $$('.pane').forEach(p=>p.classList.toggle('on', p.id==='pane-'+t)); syncTitle(); if(t==='plate') renderPlate(); if(t==='graphics') renderGraphics(); if(t==='json') renderJSON(); if(t==='clips') renderClips(); if(hooks.onTab) try{ hooks.onTab(t); }catch(e){} }
/* ---- the theater layout: drawer (L), dock (Tab), theater (T / F11); remembered per browser ---- */
const layout={ dock:true, theater:false, drawer:false };
function layoutLoad(){ try{ Object.assign(layout, JSON.parse(localStorage.getItem('bof_bm_layout')||'{}')); }catch(e){} layout.drawer=false; layoutApply(); }
function layoutApply(){ const b=document.body; b.classList.toggle('nodock', !layout.dock); b.classList.toggle('theater', !!layout.theater); b.classList.toggle('drawer', !!layout.drawer);
  $('#v-insp').classList.toggle('on', !!layout.dock && !layout.theater); $('#v-theater').classList.toggle('on', !!layout.theater); $('#v-list').classList.toggle('on', !!layout.drawer); $('#rail-list').classList.toggle('on', !!layout.drawer);
  try{ localStorage.setItem('bof_bm_layout', JSON.stringify({dock:layout.dock, theater:layout.theater})); }catch(e){}
  setTimeout(()=>{ try{ window.dispatchEvent(new Event('resize')); }catch(e){} }, 220); }
function toggleDrawer(on){ layout.drawer=(on==null)?!layout.drawer:!!on; layoutApply(); }
function toggleDock(on){ layout.dock=(on==null)?!layout.dock:!!on; if(layout.dock) layout.theater=false; layoutApply(); }
function toggleTheater(on){ layout.theater=(on==null)?!layout.theater:!!on; layoutApply(); }
function wire(){
  $$('#tabs .tab').forEach(b=>b.onclick=()=>selectTab(b.dataset.tab));
  $('#v-list').onclick=()=>toggleDrawer(); $('#rail-list').onclick=()=>toggleDrawer(); $('#drawer-close').onclick=()=>toggleDrawer(false);
  $('#v-insp').onclick=()=>toggleDock(); $('#dock-close').onclick=()=>toggleDock(false); $('#dock-open').onclick=()=>toggleDock(true);
  $('#v-theater').onclick=()=>toggleTheater();
  $('#w-view').addEventListener('mousedown', ()=>{ if(layout.drawer) toggleDrawer(false); });
  layoutLoad();
  $('#b-new').onclick=fileNew; $('#b-open').onclick=fileOpen; $('#b-save').onclick=fileSave; $('#b-saveas').onclick=fileSaveAs;
  $('#b-import').onclick=fileImport; $('#b-export').onclick=fileExport; $('#b-play').onclick=playTest; $('#b-stop').onclick=stopTest;
  $('#file-in').onchange=onImportFile; $('#open-cancel').onclick=()=>$('#modal').classList.add('hidden'); $('#modal').onclick=e=>{ if(e.target.id==='modal') $('#modal').classList.add('hidden'); };
  $('#e-apply').onclick=()=>{ if(state.doc&&!state.doc.codeOnly) applyDoc({}); };
  $('#e-undo').onclick=()=>{ if(!state.undo.length) return msg('nothing to undo'); state.doc=JSON.parse(state.undo.pop()); renderAll(); if(hooks.onDoc) try{ hooks.onDoc(state.doc); }catch(e){} if($('#p-live').checked) applyDoc({}); msg('undo'); };
  $('#e-cancel').onclick=()=>{ if(!state.doc) return; const d=state.doc; if(host.api.override.get(d.base)) host.api.override.reset(d.base); delete state.docs[d.kind]; saveDocs(); setDoc(docFor(d.base, d.role, d.stage)); msg('reverted '+d.base+' to the shipped row'); };
  $('#e-addpart').onclick=addPart;
  $$('#editbar [data-sec]').forEach(b=>b.onclick=()=>{ const s=$('#insp .sec[data-sec='+b.dataset.sec+']'); if(s){ s.classList.remove('closed'); SEC_OPEN[b.dataset.sec]=1; s.scrollIntoView({behavior:'smooth',block:'start'}); } });
  $$('#plate-tools .st').forEach(b=>b.onclick=()=>{ state.plateState=+b.dataset.state; renderPlate(); });
  $('#p-zoom').oninput=e=>{ P.z=+e.target.value; $('#p-zoom-v').textContent=P.z.toFixed(2); renderPlate(); };
  $('#p-addanchor').onclick=addAnchor; $('#p-addhit').onclick=addHitbox;
  $('#gfx-filter').oninput=renderGraphics;
  $('#gfx-plate').onclick=()=>{ if(!state.gfxSel||!state.doc) return; pushUndo(); state.doc.states[0].key=state.gfxSel; afterEdit(); };
  $('#gfx-dmg').onclick=()=>{ if(!state.gfxSel||!state.doc) return; pushUndo(); state.doc.states[1].key=state.gfxSel; afterEdit(); };
  $('#gfx-crit').onclick=()=>{ if(!state.gfxSel||!state.doc) return; pushUndo(); state.doc.states[2].key=state.gfxSel; afterEdit(); };
  $('#j-apply').onclick=applyJSONText; $('#j-copy').onclick=()=>{ navigator.clipboard&&navigator.clipboard.writeText($('#json').value); msg('copied'); }; $('#j-bundle').onclick=fileBundle;
  $('#t-rec').onclick=()=>{ if(!host.ready) return; const s=state.snap; if(s&&s.fight){ if(s.recording) host.api.rec.stop(); else host.api.rec.start(); } else { $('#t-rec').classList.toggle('arm'); msg($('#t-rec').classList.contains('arm')?'REC armed: the next PLAY TEST records from its first frame':'REC disarmed'); } };
  $('#t-invuln').onclick=()=>{ if(!host.ready) return; state.inv=!state.inv; host.api.setInvuln(state.inv); $('#t-invuln').classList.toggle('on', state.inv); };
  $('#t-speed').oninput=e=>{ $('#t-speed-v').textContent=(+e.target.value).toFixed(2); if(host.ready) host.api.setTimeScale(+e.target.value); };
  $('#t-pause').onclick=()=>{ if(!host.ready) return; host.api.pause(host.api.state!=='paused'); };
  $('#t-kill').onclick=()=>{ if(host.ready) host.api.kill(); };
  $('#t-sethp').onclick=()=>{ if(!host.ready||!state.snap||!state.snap.boss) return; host.api.setBossHp(state.snap.boss.maxhp*Math.max(1,Math.min(100,+$('#t-hp').value))/100); };
  window.addEventListener('keydown', e=>{ if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA'||e.target.tagName==='SELECT') return;
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){ e.preventDefault(); fileSave(); }
    else if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){ e.preventDefault(); $('#e-undo').click(); }
    else if(e.key==='F5'){ e.preventDefault(); playTest(); }
    else if(e.key==='F11'||e.key==='t'||e.key==='T'){ e.preventDefault(); toggleTheater(); }
    else if(e.key==='Tab'){ e.preventDefault(); toggleDock(); }
    else if(e.key==='l'||e.key==='L'){ toggleDrawer(); }
    else if(e.key==='F6'){ e.preventDefault(); stopTest(); } });
  window.addEventListener('resize', ()=>{ if(state.tab==='plate') renderPlate(); });
  plateMouse();
}

/* ---- boot ---- */
async function boot(){
  const bar=$('#boot-bar-fill'), txt=$('#boot-bar-txt');
  const names=['buttonsfiles','buttonseditor','icons','windows','loading','fontupper','fontlower','fontsymbols'];
  let n=0; txt.textContent='LOADING UI';
  await Promise.all(names.map(async nm=>{ await loadAtlas(nm); n++; bar.style.width=Math.round(50*n/names.length)+'%'; }));
  buildCSS();
  $$('.win-title[data-bm], .bm[data-bm]').forEach(el=>bmInto(el, el.dataset.bm, 40));
  txt.textContent='BOOTING ENGINE'; bar.style.width='60%';
  loadDocs(); wire(); syncTitle();
  setInterval(tick, 120);
  setTimeout(()=>{ if(!host.ready){ bar.style.width='80%'; } }, 3000);
  setTimeout(()=>{ if(!host.ready){ txt.textContent='ENGINE SLOW TO BOOT - is index.html beside this page?'; } }, 25000);
}
window.BM={ state, host, A, hooks, loadAtlas, rectOf, cellRule, applyDoc, pushUndo, renderJSON, renderAll, msg, selectTab, get api(){ return host.api; } };
boot().catch(e=>{ $('#boot-bar-txt').textContent='UI FAILED: '+(e.message||e); });
})();
