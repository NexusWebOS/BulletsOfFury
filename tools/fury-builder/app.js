"use strict";

(() => {
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const clone = value => JSON.parse(JSON.stringify(value));
  const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
  const uid = prefix => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
  const storageKey = "bof-fury-forge-project-v2";
  const saved = localStorage.getItem(storageKey);
  let project;
  try { project = saved ? JSON.parse(saved) : clone(window.FURY_DATA); }
  catch { project = clone(window.FURY_DATA); }
  // One-time seed migration: preserve edits while adding newly discovered runtime units.
  if (project.version !== window.FURY_DATA.version) {
    const knownEntities=new Set(project.entities.map(entity=>entity.id));
    window.FURY_DATA.entities.forEach(entity=>{ if(!knownEntities.has(entity.id)) project.entities.push(clone(entity)); });
    const knownPatterns=new Set((project.patterns||[]).map(pattern=>pattern.id));
    window.FURY_DATA.patterns.forEach(pattern=>{ if(!knownPatterns.has(pattern.id)) project.patterns.push(clone(pattern)); });
    project.version=window.FURY_DATA.version;
    project.runtime=clone(window.FURY_DATA.runtime);
    localStorage.setItem(storageKey,JSON.stringify(project));
  }
  // Keep saved seed entities portable when the builder moves into another checkout. User-authored
  // frames remain untouched; only known seed-frame IDs are redirected to the bundled runtime art.
  const seedEntities=new Map(window.FURY_DATA.entities.map(entity=>[entity.id,entity]));
  let portablePathsChanged=false;
  project.entities.forEach(entity=>{
    const seed=seedEntities.get(entity.id);if(!seed)return;
    const seedFrames=new Map(seed.frames.map(frame=>[frame.id,frame]));
    entity.frames.forEach(frame=>{const portable=seedFrames.get(frame.id);if(portable?.image?.startsWith("library/")&&frame.image?.startsWith("../../assets/")){frame.image=portable.image;portablePathsChanged=true;}});
  });
  if(portablePathsChanged)localStorage.setItem(storageKey,JSON.stringify(project));
  // Upgrade legacy/unit-wide marks into frame-owned annotations. Every animation frame can now
  // carry independent muzzles, anchors, hurt regions, and sectional damage geometry.
  project.entities.forEach(entity => {
    entity.frames.forEach((frame, index) => {
      if (!Array.isArray(frame.annotations)) frame.annotations = index === 0 ? clone(entity.annotations || []) : [];
    });
    delete entity.annotations;
  });
  const catalog = window.FURY_CATALOG || { assets: [], frameSets: [] };

  const state = {
    mode: "live", entityId: project.entities[0].id, levelId: project.levels[0].id,
    selectedSpawnId: null, playing: true, previewTime: 0, previewSpeed: 1,
    tool: "select", pointer: null, drawStart: null, dragging: null,
    liveOrigin: { x: 240, y: 160 }, customDraft: [], filter: "all", search: "",
    waveCount: 6, waveSpacing: .22, fps: 60, dirty: false, history: [],
    viewZoom: 1, viewPan: { x: 0, y: 0 },
    lastFrame: performance.now(), frames: 0, fpsClock: performance.now()
  };

  const canvas = $("#preview");
  const ctx = canvas.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  const images = new Map();
  const currentEntity = () => project.entities.find(e => e.id === state.entityId) || project.entities[0];
  const currentLevel = () => project.levels.find(l => l.id === state.levelId) || project.levels[0];
  const currentSpawn = () => currentLevel().spawns.find(s => s.id === state.selectedSpawnId) || null;
  const currentFrame = (entity = currentEntity()) => entity.frames[entity.selectedFrame || 0] || entity.frames[0];
  const annotationsFor = (entity = currentEntity()) => currentFrame(entity).annotations || (currentFrame(entity).annotations = []);
  const patternById = id => project.patterns.find(p => p.id === id) || project.patterns[0];

  function getImage(src) {
    if (!src) return null;
    if (!images.has(src)) {
      const image = new Image();
      const item = { image, ready: false, failed: false };
      image.onload = () => { item.ready = true; renderFrameStrip(); renderEntityList(); };
      image.onerror = () => { item.failed = true; };
      image.src = src;
      images.set(src, item);
    }
    return images.get(src);
  }

  function drawProcedural(target,kind,cx,cy,w,h){
    const px=(x,y,pw,ph,color)=>{target.fillStyle=color;target.fillRect(x,y,pw,ph);};
    const ellipse=(x,y,rx,ry,color)=>{target.fillStyle=color;target.beginPath();target.ellipse(x,y,rx,ry,0,0,Math.PI*2);target.fill();};
    target.save();target.translate(cx,cy);target.scale(w/40,h/44);
    if(kind==="classic-mine"){
      target.strokeStyle="#8a7a44";target.lineWidth=3;for(let i=0;i<8;i++){const a=i*Math.PI/4;target.beginPath();target.moveTo(Math.cos(a)*8,Math.sin(a)*8);target.lineTo(Math.cos(a)*17,Math.sin(a)*17);target.stroke();}
      ellipse(0,0,9,9,"#5a4f2c");ellipse(0,0,3,3,"#ff3030");
    }else if(kind==="classic-octo"){
      target.strokeStyle="#2e2e36";target.lineWidth=4;for(let i=0;i<6;i++){const x=-14+i*5.6;target.beginPath();target.moveTo(x,7);target.quadraticCurveTo(x+(i%2?5:-5),15,x,21);target.stroke();}
      ellipse(0,-3,15,13,"#3a3a42");ellipse(0,-3,11,10,"#4a4a52");px(-3,-7,6,8,"#ff3030");
    }else if(kind==="classic-mech"){
      px(-12,-16,24,20,"#5a5430");px(-12,-16,24,5,"#76703f");px(-4,-12,8,8,"#ff3a1e");
      px(-11,4,6,14,"#46421f");px(5,4,6,14,"#46421f");px(-16,-10,5,18,"#3a3618");px(11,-10,5,18,"#3a3618");
    }else if(kind==="classic-tank"||kind==="classic-heavy-tank"){
      const heavy=kind==="classic-heavy-tank",bw=heavy?36:30,bh=heavy?27:22;
      px(-bw/2,-bh/2,bw,bh,heavy?"#686244":"#5b6038");px(-bw/2,-bh/2,bw,4,"#878256");px(-bw/2-4,-bh/2,5,bh,"#2b2d20");px(bw/2-1,-bh/2,5,bh,"#2b2d20");
      px(-7,-6,14,11,"#474c32");px(-3,-20,6,18,"#303426");ellipse(0,0,3,3,"#ff3a1e");
    }else if(kind==="classic-boss-spider"){
      target.strokeStyle="#4c5360";target.lineWidth=3;for(let side of [-1,1])for(let i=0;i<4;i++){const y=-14+i*9;target.beginPath();target.moveTo(side*10,y);target.lineTo(side*(19+i*2),y-7);target.lineTo(side*(24+i*2),y+5);target.stroke();}
      ellipse(0,0,14,20,"#343944");ellipse(0,-2,9,14,"#555d69");ellipse(0,-5,4,6,"#ff3d42");px(-6,10,12,5,"#20242b");
    }else if(kind==="classic-boss-leviathan"){
      target.fillStyle="#31384a";target.beginPath();target.moveTo(0,-21);target.lineTo(16,-9);target.lineTo(18,12);target.lineTo(0,21);target.lineTo(-18,12);target.lineTo(-16,-9);target.closePath();target.fill();
      px(-25,-8,10,22,"#252a38");px(15,-8,10,22,"#252a38");ellipse(0,0,10,12,"#59677e");ellipse(0,0,5,7,"#ffcf52");ellipse(0,0,2,3,"#ffffff");
    }else{
      px(-12,-14,24,28,"#5e6542");ellipse(0,-4,5,5,"#ff3a1e");
    }
    target.restore();return true;
  }

  function drawRef(ref, x, y, w, h, options = {}) {
    if(ref&&ref.procedural){ctx.save();if(options.rotation){ctx.translate(x,y);ctx.rotate(options.rotation);x=0;y=0;}if(options.alpha!=null)ctx.globalAlpha=options.alpha;if(options.filter)ctx.filter=options.filter;drawProcedural(ctx,ref.procedural,x,y,w,h);ctx.restore();return true;}
    const item = getImage(ref && ref.image);
    if (!item || !item.ready) return false;
    ctx.save();
    ctx.translate(x, y);
    if (options.rotation) ctx.rotate(options.rotation);
    if (options.alpha != null) ctx.globalAlpha = options.alpha;
    if (options.filter) ctx.filter = options.filter;
    const r = ref.sourceRect;
    if (r) ctx.drawImage(item.image, r.x, r.y, r.w, r.h, -w / 2, -h / 2, w, h);
    else ctx.drawImage(item.image, -w / 2, -h / 2, w, h);
    ctx.restore();
    return true;
  }

  function drawRefTo(ref, target, x, y, w, h) {
    if(ref&&ref.procedural){const c=target.getContext("2d");c.clearRect(0,0,target.width,target.height);c.imageSmoothingEnabled=false;return drawProcedural(c,ref.procedural,x+w/2,y+h/2,w,h);}
    const item = getImage(ref && ref.image);
    if (!item) return false;
    if (!item.ready){item.image.addEventListener("load",()=>drawRefTo(ref,target,x,y,w,h),{once:true});return false;}
    const c = target.getContext("2d"); c.clearRect(0, 0, target.width, target.height); c.imageSmoothingEnabled = false;
    const r = ref.sourceRect;
    if (r) c.drawImage(item.image, r.x, r.y, r.w, r.h, x, y, w, h);
    else c.drawImage(item.image, x, y, w, h);
    return true;
  }

  function pushHistory() {
    state.history.push(JSON.stringify(project));
    if (state.history.length > 40) state.history.shift();
  }

  let saveTimer;
  function markDirty(render = true) {
    state.dirty = true;
    $("#dirtyBadge").textContent = "UNSAVED";
    $("#saveState").textContent = "SAVING…";
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveLocal, 450);
    if (render) refreshInspector();
  }

  function saveLocal() {
    localStorage.setItem(storageKey, JSON.stringify(project));
    state.dirty = false;
    $("#dirtyBadge").textContent = "SYNCED";
    $("#saveState").textContent = "LOCAL DRAFT";
  }

  function undo() {
    if (!state.history.length) return;
    project = JSON.parse(state.history.pop());
    if (!project.entities.some(e => e.id === state.entityId)) state.entityId = project.entities[0].id;
    markDirty(false); refreshAll();
  }

  function entityTypeLabel(e) { const source=e.runtimeRef?.startsWith("assets/game.js")?" · CLASSIC RUNTIME":"";return `${e.category.toUpperCase()} · ${e.wired ? "WIRED" : "UNWIRED"}${source}`; }
  function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[c]); }

  function renderEntityList() {
    const list = $("#entityList");
    const search = state.search.toLowerCase();
    const filtered = project.entities.filter(e => {
      const match = !search || `${e.name} ${e.id} ${e.category} ${(e.tags || []).join(" ")}`.toLowerCase().includes(search);
      const combatUnit=!['boss','miniboss','pilot','plane'].includes(e.category);
      const filter = state.filter === "all" || (state.filter === "wired" && e.wired) || (state.filter === "unwired" && !e.wired) || (state.filter === "enemies"&&combatUnit) || e.category === state.filter;
      return match && filter;
    });
    $("#entityCount").textContent = `${project.entities.length} UNITS`;
    const card=e=>`<button class="entity-card ${e.id === state.entityId ? "active" : ""}" data-id="${escapeHtml(e.id)}">
      <span class="thumb"><canvas width="42" height="42" data-thumb="${escapeHtml(e.id)}"></canvas></span>
      <span><strong>${escapeHtml(e.name)}</strong><small>${escapeHtml(e.category)} · ${e.frames.length} FRAME${e.frames.length === 1 ? "" : "S"}</small></span>
      <b class="wire-pill ${e.wired ? "" : "off"}">${e.wired ? (e.runtimeRef?.startsWith("assets/game.js")?"CLASSIC":"LIVE") : "DRAFT"}</b></button>`;
    const groupDefs=[
      ["BOSSES",e=>e.category==="boss"],["MINI-BOSSES",e=>e.category==="miniboss"],
      ["ENEMIES + GROUND UNITS",e=>!['boss','miniboss','pilot','plane'].includes(e.category)&&e.wired],
      ["PILOT SHIPS",e=>['pilot','plane'].includes(e.category)],
      ["UNWIRED DRAFTS",e=>!e.wired&&!['boss','miniboss','pilot','plane'].includes(e.category)]
    ];
    list.innerHTML=groupDefs.map(([name,test])=>{const members=filtered.filter(test);return members.length?`<section class="roster-group"><div class="roster-group-title"><span>${name}</span><b>${members.length}</b></div>${members.map(card).join("")}</section>`:"";}).join("")||`<div class="empty-state">No units match this filter.</div>`;
    const counts={enemies:project.entities.filter(e=>!['boss','miniboss','pilot','plane'].includes(e.category)).length,miniboss:project.entities.filter(e=>e.category==='miniboss').length,boss:project.entities.filter(e=>e.category==='boss').length};
    $("#rosterSummary").innerHTML=`<button data-summary-filter="enemies"><b>${counts.enemies}</b>ENEMIES</button><button data-summary-filter="miniboss"><b>${counts.miniboss}</b>MINI-BOSSES</button><button data-summary-filter="boss"><b>${counts.boss}</b>BOSSES</button>`;
    $$('[data-summary-filter]',$("#rosterSummary")).forEach(button=>button.onclick=()=>{state.filter=button.dataset.summaryFilter;$$("#filters button").forEach(v=>v.classList.toggle("active",v.dataset.filter===state.filter));renderEntityList();});
    $$(".entity-card", list).forEach(btn => btn.onclick = () => selectEntity(btn.dataset.id));
    $$('canvas[data-thumb]', list).forEach(c => {
      const e = project.entities.find(v => v.id === c.dataset.thumb); const f = currentFrame(e); if (!e || !f) return;
      const sr = f.sourceRect; const ratio = sr ? sr.w / sr.h : e.size.width / e.size.height;
      const h = ratio > 1 ? 34 / ratio : 34, w = ratio > 1 ? 34 : 34 * ratio;
      drawRefTo(f, c, (42 - w) / 2, (42 - h) / 2, w, h);
    });
  }

  function renderAssetVault() {
    const refKey = value => `${value.image}|${value.sourceRect ? [value.sourceRect.x,value.sourceRect.y,value.sourceRect.w,value.sourceRect.h].join(",") : "full"}`;
    const used = new Set(project.entities.flatMap(e => e.frames.map(refKey)));
    const wholeImages = (catalog.assets || []).filter(a => /\.(png|jpg|jpeg|webp)$/i.test(a.path)).map(a => ({...a, image:a.path, sourceRect:null, type:"image"}));
    const atlasFrames = (catalog.frameSets || []).flatMap(set => Object.entries(set.frames).map(([name,rect]) => ({
      id:`${set.id}-${name}`, name:`${set.id} · frame ${name}`, path:set.image, image:set.image,
      sourceRect:{x:rect[0],y:rect[1],w:rect[2],h:rect[3]}, wired:set.wired, group:`atlas/${set.id}`, type:"frame"
    })));
    const assets = [...atlasFrames,...wholeImages].filter(a => !used.has(refKey({image:`../../${a.image}`,sourceRect:a.sourceRect})));
    $("#assetCount").textContent = assets.length;
    const search = state.search.toLowerCase();
    const visible = assets.filter(a => !search || a.path.toLowerCase().includes(search)).slice(0, 120);
    $("#assetList").innerHTML = visible.map((a, i) => `<button class="asset-item" data-index="${i}" title="Create a unit draft from ${escapeHtml(a.path)}"><canvas width="72" height="45" data-vault="${i}"></canvas><span>${escapeHtml(a.name || a.path.split("/").pop())}</span></button>`).join("");
    $$('canvas[data-vault]', $("#assetList")).forEach(c => { const a=visible[+c.dataset.vault],r=a.sourceRect,ratio=r?r.w/r.h:1,h=ratio>1?38/ratio:38,w=ratio>1?64:Math.min(64,38*ratio);drawRefTo({image:`../../${a.image}`,sourceRect:r},c,(72-w)/2,(45-h)/2,w,h); });
    $$(".asset-item", $("#assetList")).forEach(btn => btn.onclick = () => createFromAsset(visible[+btn.dataset.index]));
  }

  function createFromAsset(asset) {
    pushHistory();
    const name = (asset.name || asset.path.split("/").pop()).replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ");
    const entity = makeBlankEntity(name, `../../${asset.image || asset.path}`, asset.sourceRect || null);
    project.entities.push(entity); state.entityId = entity.id; markDirty(false); refreshAll();
  }

  function makeBlankEntity(name = "New Unit", image = "library/runtime/ships/ship_axel.png", sourceRect = null) {
    return { id:uid("unit"), name, category:"enemy", wired:false, tags:["draft"], selectedFrame:0,
      frames:[{ id:uid("frame"), label:"base", image, sourceRect, annotations:[{id:uid("anchor"),kind:"anchor",x:.5,y:.5,name:"body-origin"},{id:uid("muzzle"),kind:"muzzle",x:.5,y:.9,name:"primary-muzzle"}] }], size:{width:sourceRect?sourceRect.w:48,height:sourceRect?sourceRect.h:48,displayScale:100,lockAspect:true},
      combat:{hp:4,damage:1,score:200,speed:80,fireRate:1.25}, movement:{pattern:"straight",amplitude:40,frequency:2,customPath:[]},
      aiNotes:"", runtimeRef:null };
  }

  function selectEntity(id) {
    state.entityId = id; state.previewTime = 0; state.liveOrigin = {x:240,y:160}; state.customDraft = [];
    renderEntityList(); refreshInspector(); renderFrameStrip(); updateStatus();
  }

  function refreshInspector() {
    const e = currentEntity(); if (!e) return;
    $("#entityName").value = e.name; $("#entityMeta").textContent = entityTypeLabel(e);
    $("#category").value = e.category;
    $("#statusOrb").className = `status-orb ${e.wired ? "wired" : "unwired"}`;
    $("#hp").value = e.combat.hp; $("#damage").value = e.combat.damage; $("#score").value = e.combat.score;
    $("#speed").value = e.combat.speed; $("#fireRate").value = e.combat.fireRate;
    $("#width").value = e.size.width; $("#height").value = e.size.height; $("#displayScale").value = e.size.displayScale;
    $("#scaleValue").textContent = `${e.size.displayScale}%`; $("#lockAspect").checked = e.size.lockAspect;
    $("#pattern").value = e.movement.pattern; $("#amplitude").value = e.movement.amplitude; $("#frequency").value = e.movement.frequency;
    const p = patternById(e.movement.pattern); $("#patternCard").innerHTML = `<b>${escapeHtml(p.name)}</b><br>${escapeHtml(p.description)}`;
    renderAnnotations(); updateStatus();
  }

  function renderPatternOptions() {
    const html = project.patterns.map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join("");
    $("#pattern").innerHTML = html; $("#spawnPattern").innerHTML = `<option value="inherit">Inherit unit AI</option>${html}`;
  }

  function renderFrameStrip() {
    const e = currentEntity(); const strip = $("#frameStrip");
    strip.innerHTML = e.frames.map((f, i) => `<button class="frame-card ${i === (e.selectedFrame || 0) ? "active" : ""}" data-frame="${i}"><canvas width="58" height="55"></canvas><span>${i+1} · ${escapeHtml(f.label || f.id)}</span></button>`).join("");
    $$(".frame-card", strip).forEach((btn, i) => {
      btn.onclick = () => { e.selectedFrame = i; renderFrameStrip(); refreshInspector(); };
      const f = e.frames[i], sr = f.sourceRect; const ratio = sr ? sr.w/sr.h : e.size.width/e.size.height;
      const h = ratio > 1 ? 46/ratio : 46, w = ratio > 1 ? 46 : 46*ratio;
      drawRefTo(f, $("canvas",btn), (58-w)/2,(55-h)/2,w,h);
    });
  }

  function renderAnnotations() {
    const list = $("#annotationList"), e = currentEntity();
    const annotations = annotationsFor(e);
    list.innerHTML = annotations.map((a,i) => `<div class="annotation-item"><span>${i+1}. ${escapeHtml(a.kind.toUpperCase())} · ${escapeHtml(a.name || "region")}</span><button data-delete="${a.id}">×</button></div>`).join("") || `<div class="empty-state">No points or regions on this frame.</div>`;
    $$('[data-delete]',list).forEach(b => b.onclick = () => { pushHistory(); currentFrame(e).annotations = annotationsFor(e).filter(a=>a.id!==b.dataset.delete); markDirty(); });
  }

  function renderLevelControls() {
    $("#stageSelect").innerHTML = project.levels.map(l=>`<option value="${l.id}">${escapeHtml(l.name)}</option>`).join("");
    $("#stageSelect").value = state.levelId;
    $("#spawnEntity").innerHTML = project.entities.map(e=>`<option value="${e.id}">${escapeHtml(e.name)}${e.wired?"":" [UNWIRED]"}</option>`).join("");
    const level = currentLevel(); $("#stageDuration").value=level.duration; $("#stageScroll").value=level.scroll;
    refreshSpawnInspector(); renderTimeline();
  }

  function refreshSpawnInspector() {
    const s = currentSpawn(); $("#noSpawn").classList.toggle("hidden",!!s); $("#spawnFields").classList.toggle("hidden",!s); $("#deleteSpawn").disabled=!s;
    if (!s) return;
    $("#spawnEntity").value=s.entityId; $("#spawnTime").value=s.time; $("#spawnCount").value=s.count;
    $("#spawnX").value=Math.round(s.x); $("#spawnY").value=Math.round(s.y); $("#spawnInterval").value=s.interval; $("#spawnHp").value=s.hpMultiplier; $("#spawnPattern").value=s.pattern || "inherit";
  }

  function renderTimeline() {
    const l=currentLevel(), events=$("#timelineEvents"), ruler=$("#timelineRuler");
    ruler.innerHTML=Array.from({length:11},(_,i)=>`<span style="left:${i*10}%">${Math.round(l.duration*i/10)}s</span>`).join("");
    events.innerHTML=l.spawns.map(s=>{const e=project.entities.find(v=>v.id===s.entityId);return `<button class="timeline-event ${s.id===state.selectedSpawnId?"selected":""}" data-spawn="${s.id}" style="left:${clamp(s.time/l.duration*100,0,100)}%"><span>${escapeHtml(e?e.name:s.entityId)}</span></button>`}).join("");
    $$(".timeline-event",events).forEach(b=>b.onpointerdown=evt=>{evt.preventDefault();state.selectedSpawnId=b.dataset.spawn;state.dragging={type:"timeline",id:b.dataset.spawn};b.setPointerCapture(evt.pointerId);refreshSpawnInspector();renderTimeline();});
  }

  function updateTimelinePlayhead(){ const l=currentLevel(); $("#playhead").style.left=`${clamp(state.previewTime/l.duration*100,0,100)}%`; $("#timeReadout").textContent=formatTime(state.previewTime); }
  function formatTime(v){const m=Math.floor(v/60),s=v-m*60;return `${String(m).padStart(2,"0")}:${s.toFixed(1).padStart(4,"0")}`;}

  function setMode(mode) {
    state.mode=mode; state.previewTime=0; state.playing=true; state.customDraft=[];
    $$(".mode").forEach(b=>b.classList.toggle("active",b.dataset.mode===mode));
    const info={live:["1:1 RUNTIME REPLICA","LIVE COMBAT LAB","Drag to reposition · Wheel to zoom · 0 resets zoom"],frame:["PIXEL-SPACE AUTHORING","FRAME FORGE","Draw on the frame · Wheel to zoom · 0 resets zoom"],wave:["NORMALIZED PATH AUTHORING","WAVE STUDIO","Draw a flight path · Wheel to zoom · 0 resets zoom"],level:["REAL-TIME SPAWN AUTHORING","LEVEL DIRECTOR","Click to place · drag to move · Wheel to zoom"]}[mode];
    $("#modeEyebrow").textContent=info[0]; $("#stageTitle").textContent=info[1]; $("#canvasHelp").textContent=info[2];
    $("#frameTools").classList.toggle("hidden",mode!=="frame"); $("#waveTools").classList.toggle("hidden",mode!=="wave");
    $("#entityInspector").classList.toggle("hidden",mode==="level"); $("#levelInspector").classList.toggle("hidden",mode!=="level");
    $("#frameStripWrap").classList.toggle("hidden",mode==="level"); $("#timelineWrap").classList.toggle("hidden",mode!=="level");
    $("#canvasBadge").textContent=mode==="frame"?"SOURCE PIXEL SPACE":mode==="level"?"SPAWN MAP · 480 × 720":"480 × 720 GAME SPACE";
    updateCanvasInteractionState(); updatePlayIcon();
    if(mode==="level")renderLevelControls(); else refreshInspector(); updateStatus();
  }

  function updateCanvasInteractionState(){canvas.dataset.mode=state.mode;canvas.dataset.tool=state.tool;}
  function updateStatus(){const e=currentEntity();$("#selectionStatus").textContent=state.mode==="level"?`${currentLevel().name.toUpperCase()} · ${currentLevel().spawns.length} SPAWNS`:`${e.name.toUpperCase()} · FRAME ${(e.selectedFrame||0)+1}/${e.frames.length}`;const unitMetric=$("#unitMetric"),spawnMetric=$("#spawnMetric"),patternMetric=$("#patternMetric");if(unitMetric)unitMetric.textContent=project.entities.length;if(spawnMetric)spawnMetric.textContent=project.levels.reduce((sum,level)=>sum+level.spawns.length,0);if(patternMetric)patternMetric.textContent=project.patterns.length;}

  function bindNumber(id, getter, setter) {
    const el=$(id); el.addEventListener("change",()=>{pushHistory();setter(+el.value);markDirty(false);refreshInspector();if(state.mode==="level"){refreshSpawnInspector();renderTimeline();updateStatus();}});
  }

  function bindUI() {
    $$(".mode").forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
    $("#search").oninput=e=>{state.search=e.target.value;renderEntityList();renderAssetVault();};
    $$("#filters button").forEach(b=>b.onclick=()=>{$$("#filters button").forEach(v=>v.classList.remove("active"));b.classList.add("active");state.filter=b.dataset.filter;renderEntityList();});
    $("#newEntity").onclick=()=>{pushHistory();const e=makeBlankEntity();project.entities.push(e);selectEntity(e.id);markDirty(false);refreshAll();};
    $("#duplicateEntity").onclick=()=>{pushHistory();const e=clone(currentEntity());e.id=uid(e.id);e.name+=` COPY`;e.wired=false;e.runtimeRef=null;project.entities.push(e);state.entityId=e.id;markDirty(false);refreshAll();};
    $("#entityName").onchange=e=>{pushHistory();currentEntity().name=e.target.value.trim()||"Unnamed Unit";markDirty(false);renderEntityList();refreshInspector();};
    $("#category").onchange=e=>{pushHistory();currentEntity().category=e.target.value;currentEntity().tags=[...new Set([...(currentEntity().tags||[]),e.target.value])];markDirty(false);renderEntityList();refreshInspector();};
    bindNumber("#hp",()=>currentEntity().combat.hp,v=>currentEntity().combat.hp=Math.max(0,v));
    bindNumber("#damage",()=>currentEntity().combat.damage,v=>currentEntity().combat.damage=Math.max(0,v));
    bindNumber("#score",()=>currentEntity().combat.score,v=>currentEntity().combat.score=Math.max(0,v));
    bindNumber("#speed",()=>currentEntity().combat.speed,v=>currentEntity().combat.speed=Math.max(0,v));
    bindNumber("#fireRate",()=>currentEntity().combat.fireRate,v=>currentEntity().combat.fireRate=Math.max(.05,v));
    bindNumber("#width",()=>currentEntity().size.width,v=>resizeEntity("width",Math.max(1,v)));
    bindNumber("#height",()=>currentEntity().size.height,v=>resizeEntity("height",Math.max(1,v)));
    $("#displayScale").oninput=e=>{currentEntity().size.displayScale=+e.target.value;$("#scaleValue").textContent=`${e.target.value}%`;markDirty(false);};
    $("#displayScale").onchange=()=>pushHistory(); $("#lockAspect").onchange=e=>{pushHistory();currentEntity().size.lockAspect=e.target.checked;markDirty();};
    $("#pattern").onchange=e=>{pushHistory();const ent=currentEntity(),p=patternById(e.target.value);ent.movement.pattern=p.id;ent.movement.amplitude=p.params.amplitude;ent.movement.frequency=p.params.frequency;markDirty();};
    bindNumber("#amplitude",()=>currentEntity().movement.amplitude,v=>currentEntity().movement.amplitude=Math.max(0,v));
    bindNumber("#frequency",()=>currentEntity().movement.frequency,v=>currentEntity().movement.frequency=Math.max(0,v));
    $("#recommendAI").onclick=recommendAI;
    $$("#toolGrid button").forEach(b=>b.onclick=()=>{$$("#toolGrid button").forEach(v=>v.classList.remove("active"));b.classList.add("active");state.tool=b.dataset.tool;updateCanvasInteractionState();});
    $("#clearPath").onclick=()=>{pushHistory();state.customDraft=[];currentEntity().movement.customPath=[];markDirty(false);};
    $("#useDrawnPath").onclick=()=>{if(state.customDraft.length<2)return;pushHistory();currentEntity().movement.customPath=clone(state.customDraft);currentEntity().movement.pattern="drawn";markDirty();};
    $("#waveCount").oninput=e=>{state.waveCount=+e.target.value;$("#waveCountValue").textContent=e.target.value;};
    $("#waveSpacing").oninput=e=>{state.waveSpacing=+e.target.value;$("#waveSpacingValue").textContent=`${(+e.target.value).toFixed(2)}s`;};
    $("#resetPreview").onclick=resetPreview; $("#playPreview").onclick=()=>{state.playing=!state.playing;updatePlayIcon();}; $("#previewSpeed").onchange=e=>state.previewSpeed=+e.target.value;
    $("#zoomBadge").onclick=resetViewZoom;
    $("#addFrame").onclick=addFrameReference; $("#copyRef").onclick=copyFrameReference;
    $("#exportBtn").onclick=()=>downloadJSON("bullets-of-fury-builder.json",{...project,assetCatalog:{generatedAt:catalog.generatedAt,assetCount:(catalog.assets||[]).length}});
    $("#importBtn").onclick=()=>$("#importFile").click(); $("#importFile").onchange=importJSON;
    $("#stageSelect").onchange=e=>{state.levelId=e.target.value;state.selectedSpawnId=null;state.previewTime=0;renderLevelControls();updateStatus();};
    bindNumber("#stageDuration",()=>currentLevel().duration,v=>currentLevel().duration=Math.max(1,v)); bindNumber("#stageScroll",()=>currentLevel().scroll,v=>currentLevel().scroll=Math.max(0,v));
    $("#addSpawn").onclick=()=>addSpawn(240,-30,state.previewTime); $("#deleteSpawn").onclick=deleteSelectedSpawn;
    $("#spawnEntity").onchange=e=>updateSpawn("entityId",e.target.value); $("#spawnPattern").onchange=e=>updateSpawn("pattern",e.target.value);
    [["#spawnTime","time"],["#spawnCount","count"],["#spawnX","x"],["#spawnY","y"],["#spawnInterval","interval"],["#spawnHp","hpMultiplier"]].forEach(([id,key])=>$(id).onchange=e=>updateSpawn(key,+e.target.value));
    $("#previewLevel").onclick=()=>{state.previewTime=currentSpawn()?.time||0;state.playing=true;updatePlayIcon();}; $("#exportLevel").onclick=()=>downloadJSON(`${currentLevel().id}.level.json`,currentLevel());
    $("#timeline").onpointermove=timelineMove; $("#timeline").onpointerup=timelineUp; $("#timeline").onpointercancel=timelineUp;
    canvas.addEventListener("pointerdown",canvasDown); canvas.addEventListener("pointermove",canvasMove); canvas.addEventListener("pointerup",canvasUp); canvas.addEventListener("pointercancel",canvasUp);
    canvas.addEventListener("wheel",canvasWheel,{passive:false});
    window.addEventListener("keydown",keyDown);
  }

  function resizeEntity(key,value){const e=currentEntity(),f=currentFrame(),old=e.size[key];e.size[key]=value;if(!e.size.lockAspect||!old)return;const ratio=f.sourceRect?f.sourceRect.w/f.sourceRect.h:e.size.width/e.size.height;if(key==="width")e.size.height=Math.max(1,Math.round(value/ratio));else e.size.width=Math.max(1,Math.round(value*ratio));}
  function recommendAI(){const e=currentEntity();const order={pilot:"hoverStrafe",plane:"hoverStrafe",jet:e.combat.speed>115?"dive":"sine",drone:"orbit",boat:"drift",boss:"bossPhases",miniboss:"carrier",tank:"grid",turret:"gate",ice:"pounceRetreat",lava:"pounceRetreat",sludge:"drift",alienoid:"orbit",enemy:e.combat.speed>115?"dive":"sine"};const p=patternById(order[e.category]||"sine");pushHistory();e.movement.pattern=p.id;e.movement.amplitude=p.params.amplitude;e.movement.frequency=p.params.frequency;e.aiNotes=`Recommended for ${e.category}: ${p.name}. ${p.description}`;markDirty();}
  function updatePlayIcon(){const button=$("#playPreview");button.textContent=state.playing?"Ⅱ":"▶";button.dataset.playing=state.playing?"true":"false";button.title=state.playing?"Pause preview":"Play preview";}
  function resetPreview(){state.previewTime=0;state.liveOrigin={x:240,y:160};state.customDraft=[];updateTimelinePlayhead();}
  function updateZoomBadge(){$("#zoomBadge").textContent=`ZOOM ${Math.round(state.viewZoom*100)}% · RESET`;}
  function resetViewZoom(){state.viewZoom=1;state.viewPan={x:0,y:0};updateZoomBadge();}
  function addFrameReference(){const path=prompt("Image path relative to the builder (example: library/runtime/ships/ship_axel.png)");if(!path)return;pushHistory();currentEntity().frames.push({id:uid("frame"),label:`frame-${currentEntity().frames.length+1}`,image:path,sourceRect:null,annotations:[]});currentEntity().selectedFrame=currentEntity().frames.length-1;markDirty(false);renderFrameStrip();refreshInspector();}
  async function copyFrameReference(){const f=currentFrame(),ref={image:f.image,sourceRect:f.sourceRect,size:currentEntity().size,frameId:f.id};try{await navigator.clipboard.writeText(JSON.stringify(ref,null,2));$("#copyRef").textContent="COPIED";setTimeout(()=>$("#copyRef").textContent="COPY REF",1000);}catch{downloadJSON(`${currentEntity().id}.image-ref.json`,ref);}}
  function downloadJSON(name,data){const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"}),a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
  async function importJSON(evt){const file=evt.target.files[0];if(!file)return;try{const data=JSON.parse(await file.text());const incoming=data.entities&&data.levels?data:null;if(!incoming)throw new Error("Expected entities and levels arrays.");pushHistory();project=incoming;if(!project.patterns)project.patterns=clone(window.FURY_DATA.patterns);state.entityId=project.entities[0].id;state.levelId=project.levels[0].id;markDirty(false);renderPatternOptions();refreshAll();}catch(err){alert(`Could not import: ${err.message}`);}evt.target.value="";}

  function addSpawn(x,y,time){const level=currentLevel();pushHistory();const s={id:uid("spawn"),time:+clamp(time,0,level.duration).toFixed(2),entityId:currentEntity().id,x:Math.round(x),y:Math.round(y),count:1,interval:.3,pattern:currentEntity().movement.pattern,hpMultiplier:1};level.spawns.push(s);level.spawns.sort((a,b)=>a.time-b.time);state.selectedSpawnId=s.id;markDirty(false);renderLevelControls();updateStatus();}
  function deleteSelectedSpawn(){const l=currentLevel();if(!state.selectedSpawnId)return;pushHistory();l.spawns=l.spawns.filter(s=>s.id!==state.selectedSpawnId);state.selectedSpawnId=null;markDirty(false);renderLevelControls();updateStatus();}
  function updateSpawn(key,value){const s=currentSpawn();if(!s)return;pushHistory();if(key==="time")value=clamp(value,0,currentLevel().duration);if(key==="count")value=Math.max(1,Math.round(value));s[key]=value;markDirty(false);refreshSpawnInspector();renderTimeline();}
  function timelineMove(evt){if(state.dragging?.type!=="timeline")return;const rect=$("#timeline").getBoundingClientRect(),s=currentSpawn();if(!s)return;s.time=+clamp((evt.clientX-rect.left)/rect.width*currentLevel().duration,0,currentLevel().duration).toFixed(2);refreshSpawnInspector();renderTimeline();}
  function timelineUp(){if(state.dragging?.type==="timeline"){pushHistory();markDirty(false);}state.dragging=null;}

  function rawCanvasPoint(evt){const r=canvas.getBoundingClientRect();return{x:(evt.clientX-r.left)/r.width*canvas.width,y:(evt.clientY-r.top)/r.height*canvas.height};}
  function canvasPoint(evt){const p=rawCanvasPoint(evt);return{x:(p.x-state.viewPan.x)/state.viewZoom,y:(p.y-state.viewPan.y)/state.viewZoom};}
  function canvasWheel(evt){
    evt.preventDefault();
    const cursor=rawCanvasPoint(evt),oldZoom=state.viewZoom;
    const nextZoom=clamp(oldZoom*Math.exp(-evt.deltaY*.0015),1,8);
    if(Math.abs(nextZoom-oldZoom)<.001)return;
    const worldX=(cursor.x-state.viewPan.x)/oldZoom,worldY=(cursor.y-state.viewPan.y)/oldZoom;
    const nextPanX=cursor.x-worldX*nextZoom,nextPanY=cursor.y-worldY*nextZoom;
    state.viewZoom=nextZoom;
    state.viewPan={x:clamp(nextPanX,canvas.width*(1-nextZoom),0),y:clamp(nextPanY,canvas.height*(1-nextZoom),0)};
    updateZoomBadge();
  }
  function frameLayout(){const e=currentEntity(),f=currentFrame(),sr=f.sourceRect;let sw=sr?sr.w:e.size.width,sh=sr?sr.h:e.size.height;const zoom=e.size.displayScale/100;let w=sw*zoom,h=sh*zoom;const maxW=canvas.width-80,maxH=canvas.height-130;if(w>maxW||h>maxH){const fit=Math.min(maxW/w,maxH/h);w*=fit;h*=fit;}return{x:(canvas.width-w)/2,y:(canvas.height-h)/2,w,h,sw,sh};}
  function normalizedOnFrame(p){const r=frameLayout();return{x:clamp((p.x-r.x)/r.w,0,1),y:clamp((p.y-r.y)/r.h,0,1)};}
  function canvasDown(evt){canvas.setPointerCapture(evt.pointerId);canvas.classList.add("is-dragging");const p=canvasPoint(evt);state.pointer=p;
    if(state.mode==="live"){state.dragging={type:"live"};state.liveOrigin=p;return;}
    if(state.mode==="wave"){pushHistory();state.customDraft=[{x:clamp(p.x/480,0,1),y:clamp(p.y/720,0,1)}];state.dragging={type:"path"};return;}
    if(state.mode==="level"){const hit=findSpawnAt(p);if(hit){state.selectedSpawnId=hit.id;state.dragging={type:"spawn"};refreshSpawnInspector();renderTimeline();}else addSpawn(p.x,p.y,state.previewTime);return;}
    if(state.mode!=="frame")return;
    const n=normalizedOnFrame(p),e=currentEntity();
    if(state.tool==="muzzle"||state.tool==="anchor"||state.tool==="x"){const annotations=annotationsFor(e);pushHistory();annotations.push({id:uid(state.tool),kind:state.tool,x:n.x,y:n.y,name:`${state.tool}-${annotations.filter(a=>a.kind===state.tool).length+1}`});markDirty();return;}
    if(state.tool==="erase"){const found=nearestAnnotation(n);if(found){pushHistory();currentFrame(e).annotations=annotationsFor(e).filter(a=>a.id!==found.id);markDirty();}return;}
    if(["box","ellipse","diamond"].includes(state.tool)){state.drawStart=n;state.dragging={type:"shape",kind:state.tool};return;}
  }
  function canvasMove(evt){const p=canvasPoint(evt);state.pointer=p;if(!state.dragging)return;
    if(state.dragging.type==="live")state.liveOrigin=p;
    if(state.dragging.type==="path"){const n={x:clamp(p.x/480,0,1),y:clamp(p.y/720,0,1)},last=state.customDraft.at(-1);if(!last||Math.hypot((n.x-last.x)*480,(n.y-last.y)*720)>6)state.customDraft.push(n);}
    if(state.dragging.type==="spawn"){const s=currentSpawn();if(s){s.x=Math.round(clamp(p.x,0,480));s.y=Math.round(clamp(p.y,-200,720));refreshSpawnInspector();}}
  }
  function canvasUp(evt){if(state.dragging?.type==="shape"&&state.drawStart){const end=normalizedOnFrame(canvasPoint(evt)),x=Math.min(state.drawStart.x,end.x),y=Math.min(state.drawStart.y,end.y),w=Math.abs(end.x-state.drawStart.x),h=Math.abs(end.y-state.drawStart.y);if(w>.005||h>.005){pushHistory();annotationsFor().push({id:uid(state.dragging.kind),kind:state.dragging.kind,x,y,w,h,name:`${state.dragging.kind}-region`});markDirty();}}
    if(state.dragging?.type==="spawn"){pushHistory();markDirty(false);renderTimeline();}if(state.dragging?.type==="path"&&state.customDraft.length>1){currentEntity().movement.customPath=clone(state.customDraft);}
    state.dragging=null;state.drawStart=null;canvas.classList.remove("is-dragging");
  }
  function nearestAnnotation(n){let best=null,d=.08;for(const a of annotationsFor()){const cx=a.w?a.x+a.w/2:a.x,cy=a.h?a.y+a.h/2:a.y,dd=Math.hypot(n.x-cx,n.y-cy);if(dd<d){d=dd;best=a;}}return best;}
  function findSpawnAt(p){let best=null,d=24;for(const s of currentLevel().spawns){const dd=Math.hypot(p.x-s.x,p.y-s.y);if(dd<d){d=dd;best=s;}}return best;}
  function keyDown(evt){if((evt.ctrlKey||evt.metaKey)&&evt.key.toLowerCase()==="s"){evt.preventDefault();saveLocal();return;}if((evt.ctrlKey||evt.metaKey)&&evt.key.toLowerCase()==="z"){evt.preventDefault();undo();return;}if(evt.code==="Space"&&!/INPUT|SELECT/.test(document.activeElement.tagName)){evt.preventDefault();state.playing=!state.playing;updatePlayIcon();}if(evt.key.toLowerCase()==="r"&&!/INPUT|SELECT/.test(document.activeElement.tagName))resetPreview();if(evt.key==="0"&&!/INPUT|SELECT/.test(document.activeElement.tagName))resetViewZoom();if(evt.key==="Delete"){if(state.mode==="level")deleteSelectedSpawn();}}

  function background(level=currentLevel()){
    const grad=ctx.createLinearGradient(0,0,0,720);grad.addColorStop(0,"#101c1a");grad.addColorStop(1,level?.background||"#172a22");ctx.fillStyle=grad;ctx.fillRect(0,0,480,720);
    const scroll=(state.previewTime*(level?.scroll||66))%72;ctx.strokeStyle="rgba(105,170,120,.12)";ctx.lineWidth=1;
    for(let y=-72+scroll;y<760;y+=72){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(480,y);ctx.stroke();}
    for(let x=30;x<480;x+=70){ctx.fillStyle=x%140?"rgba(27,72,44,.35)":"rgba(60,90,50,.25)";for(let y=-100+scroll*1.2;y<760;y+=130)ctx.fillRect(x-17,y+(x%3)*19,34,50);}
    ctx.fillStyle="rgba(0,0,0,.15)";ctx.fillRect(0,0,26,720);ctx.fillRect(454,0,26,720);
  }
  function gridBackground(){ctx.fillStyle="#0a0e11";ctx.fillRect(0,0,480,720);ctx.strokeStyle="#202a31";ctx.lineWidth=1;for(let x=0;x<=480;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,720);ctx.stroke();}for(let y=0;y<=720;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(480,y);ctx.stroke();}ctx.strokeStyle="#394750";ctx.beginPath();ctx.moveTo(240,0);ctx.lineTo(240,720);ctx.moveTo(0,360);ctx.lineTo(480,360);ctx.stroke();}
  function motionAt(e,age,origin={x:240,y:-40},phase=0,patternOverride=null){const p=patternOverride||e.movement.pattern,amp=e.movement.amplitude||40,f=Math.max(.01,e.movement.frequency||2),s=e.combat.speed;let x=origin.x,y=origin.y+s*age;
    if(p==="sine")x=origin.x+Math.sin(age*f+phase)*amp;
    else if(p==="vee")x=origin.x+(phase-3)*10*age;
    else if(p==="side"){x=origin.x+(origin.x<240?1:-1)*Math.max(140,s)*age;y=origin.y+s*.62*age+(amp/f)*(Math.cos(phase)-Math.cos(age*f+phase));}
    else if(p==="dive"){y=origin.y+s*1.15*age+Math.min(90,age*42)*age*.5;const track=Math.max(0,age-.55)*(68+amp*.1);x=origin.x+Math.sign(240-origin.x)*Math.min(Math.abs(240-origin.x),track);}
    else if(p==="snake"){y=origin.y+s*.9*age;x=240+Math.sin(age*f+phase)*amp;}
    else if(p==="carrier"){y=origin.y+s*.64*age;x=origin.x+(amp/f)*(1-Math.cos(age*f));}
    else if(p==="grid"){y=origin.y+s*.72*age;x=origin.x+Math.sin(age*f+phase)*amp;}
    else if(p==="gate"){y=origin.y+s*.65*age;x=origin.x+Math.sin(age*f+phase)*amp;}
    else if(p==="fan"){y=origin.y+s*.95*age;x=origin.x+Math.sin(phase)*amp*age;}
    else if(p==="spiral"){y=origin.y+s*.86*age;x=origin.x+Math.sin(age*f+phase)*(12+age*amp*.22);}
    else if(p==="drift"){y=origin.y+s*.72*age;x=origin.x+(amp/f)*(Math.cos(phase)-Math.cos(age*f+phase));}
    else if(p==="hoverStrafe"){y=origin.y+Math.min(190,s*age);x=origin.x+Math.sin(Math.max(0,age-1.5)*f+phase)*amp;}
    else if(p==="orbit"){x=240+Math.cos(age*f+phase)*amp;y=330+Math.sin(age*f+phase)*amp*.7;}
    else if(p==="pounceRetreat"){const t=age%4;y=t<1.4?origin.y+(t/1.4)*560:560-((t-1.4)/2.6)*600;x=origin.x+Math.sin(t*2+phase)*amp;}
    else if(p==="bossPhases"){const t=age%8;y=115+Math.sin(Math.min(t,2)/2*Math.PI)*35;x=240+Math.sin(age*f+phase)*amp;}
    else if(p==="drawn"){const path=(e.movement.customPath||[]).filter(point=>point&&Number.isFinite(point.x)&&Number.isFinite(point.y));if(path.length>1){const t=((age*f*.22)%1+1)%1,idx=t*(path.length-1),i=clamp(Math.floor(idx),0,path.length-1),q=idx-i,a=path[i],b=path[Math.min(i+1,path.length-1)];x=(a.x+(b.x-a.x)*q)*480;y=(a.y+(b.y-a.y)*q)*720;}}
    return{x,y};}
  function drawUnit(e,pos,alpha=1,rotation=0){const scale=e.size.displayScale/100,w=e.size.width*scale,h=e.size.height*scale;if(!drawRef(currentFrame(e),pos.x,pos.y,w,h,{alpha,rotation})){ctx.fillStyle=e.wired?"#ffb326":"#ff7540";ctx.beginPath();ctx.moveTo(pos.x,pos.y-h/2);ctx.lineTo(pos.x-w/2,pos.y+h/2);ctx.lineTo(pos.x+w/2,pos.y+h/2);ctx.closePath();ctx.fill();}return{w,h};}
  function drawShotsFor(e,pos,age){const rate=Math.max(.08,e.combat.fireRate),phase=(age%rate)/rate;if(phase>.5)return;const muzzles=annotationsFor(e).filter(a=>a.kind==="muzzle");ctx.fillStyle="#ffdc61";ctx.shadowColor="#ff573d";ctx.shadowBlur=9;(muzzles.length?muzzles:[{x:.5,y:.9}]).forEach(m=>{const x=pos.x+(m.x-.5)*e.size.width,y=pos.y+(m.y-.5)*e.size.height+phase*90;ctx.fillRect(x-2,y-6,4,12);});ctx.shadowBlur=0;}
  function renderLive(){background();const e=currentEntity(),origin=state.liveOrigin,cycle=Math.max(4,Math.min(9,(760-origin.y)/Math.max(30,e.combat.speed)+1)),age=state.previewTime%cycle,pos=motionAt(e,age,origin,0);drawUnit(e,pos);drawShotsFor(e,pos,age);ctx.fillStyle="#59d9d0";ctx.fillRect(237,640,6,32);ctx.fillRect(226,658,28,10);label(`${e.name.toUpperCase()} · ${e.combat.hp} HP · ${e.combat.speed} PX/S`,12,20,"#ffcf58");label(patternById(e.movement.pattern).name.toUpperCase(),12,36,"#83a0ad");}
  function renderFrame(){gridBackground();const e=currentEntity(),f=currentFrame(),r=frameLayout();ctx.fillStyle="#07090a";ctx.fillRect(r.x-12,r.y-12,r.w+24,r.h+24);if(f.procedural){drawProcedural(ctx,f.procedural,r.x+r.w/2,r.y+r.h/2,r.w,r.h);}else{const item=getImage(f.image);if(item?.ready){if(f.sourceRect)ctx.drawImage(item.image,f.sourceRect.x,f.sourceRect.y,f.sourceRect.w,f.sourceRect.h,r.x,r.y,r.w,r.h);else ctx.drawImage(item.image,r.x,r.y,r.w,r.h);}}ctx.strokeStyle="#52616b";ctx.strokeRect(r.x-.5,r.y-.5,r.w+1,r.h+1);annotationsFor(e).forEach((a,i)=>drawAnnotation(a,r,i));if(state.dragging?.type==="shape"&&state.drawStart&&state.pointer){const end=normalizedOnFrame(state.pointer);drawAnnotation({kind:state.dragging.kind,x:Math.min(state.drawStart.x,end.x),y:Math.min(state.drawStart.y,end.y),w:Math.abs(end.x-state.drawStart.x),h:Math.abs(end.y-state.drawStart.y)},r,-1);}label(`${f.procedural?"PROCEDURAL":"SOURCE"} ${r.sw}×${r.sh} PX · DISPLAY ${Math.round(r.w)}×${Math.round(r.h)}`,12,20,"#ffcf58");}
  function drawAnnotation(a,r,i){const color=a.kind==="muzzle"?"#ffb326":a.kind==="anchor"?"#43e1d0":a.kind==="x"?"#ff4e3b":"#80e05a";ctx.save();ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=2;ctx.shadowColor=color;ctx.shadowBlur=4;
    if(a.w!=null){const x=r.x+a.x*r.w,y=r.y+a.y*r.h,w=a.w*r.w,h=a.h*r.h;if(a.kind==="ellipse"){ctx.beginPath();ctx.ellipse(x+w/2,y+h/2,w/2,h/2,0,0,Math.PI*2);ctx.stroke();}else if(a.kind==="diamond"){ctx.beginPath();ctx.moveTo(x+w/2,y);ctx.lineTo(x+w,y+h/2);ctx.lineTo(x+w/2,y+h);ctx.lineTo(x,y+h/2);ctx.closePath();ctx.stroke();}else ctx.strokeRect(x,y,w,h);label(String(i+1),x+3,y+8,color);}else{const x=r.x+a.x*r.w,y=r.y+a.y*r.h;ctx.beginPath();ctx.arc(x,y,6,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(x-10,y);ctx.lineTo(x+10,y);ctx.moveTo(x,y-10);ctx.lineTo(x,y+10);ctx.stroke();label(String(i+1),x+8,y-8,color);}ctx.restore();}
  function renderWave(){gridBackground();const e=currentEntity(),path=state.customDraft.length?state.customDraft:e.movement.customPath||[];if(path.length>1){ctx.strokeStyle="#ffb326";ctx.lineWidth=3;ctx.setLineDash([8,5]);ctx.beginPath();path.forEach((p,i)=>(i?ctx.lineTo(p.x*480,p.y*720):ctx.moveTo(p.x*480,p.y*720)));ctx.stroke();ctx.setLineDash([]);path.forEach((p,i)=>{if(i%Math.max(1,Math.floor(path.length/12))===0){ctx.fillStyle="#fff";ctx.fillRect(p.x*480-2,p.y*720-2,4,4);}});}for(let i=0;i<state.waveCount;i++){const age=Math.max(0,state.previewTime-i*state.waveSpacing),phase=i*.7;let pos;if(path.length>1){const ghost={...e,movement:{...e.movement,pattern:"drawn",customPath:path}};pos=motionAt(ghost,age,{x:240,y:-40},phase);}else pos=motionAt(e,age,{x:240,y:-40-i*24},phase);if(age>0)drawUnit(e,pos,i===0?1:.82);}label(`FORMATION ×${state.waveCount} · ${state.waveSpacing.toFixed(2)}S SPACING`,12,20,"#ffcf58");label(path.length>1?`${path.length} NORMALIZED PATH POINTS`:patternById(e.movement.pattern).name.toUpperCase(),12,36,"#83a0ad");}
  function renderLevel(){background(currentLevel());const l=currentLevel();for(const [spawnIndex,s] of l.spawns.entries()){const e=project.entities.find(v=>v.id===s.entityId);if(!e)continue;const selected=s.id===state.selectedSpawnId,markerY=s.y<0?74+(spawnIndex%3)*34:clamp(s.y,18,702);ctx.save();ctx.strokeStyle=selected?"#43e1d0":"#ffb326";ctx.fillStyle=selected?"#43e1d0":"#ffb326";ctx.lineWidth=selected?3:1.5;ctx.setLineDash([5,4]);ctx.beginPath();ctx.arc(s.x,markerY,selected?18:13,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);ctx.beginPath();ctx.moveTo(s.x-7,markerY);ctx.lineTo(s.x+7,markerY);ctx.moveTo(s.x,markerY-7);ctx.lineTo(s.x,markerY+7);ctx.stroke();if(s.y<0){ctx.beginPath();ctx.moveTo(s.x-5,markerY+9);ctx.lineTo(s.x+5,markerY+9);ctx.lineTo(s.x,markerY+15);ctx.closePath();ctx.fill();}ctx.restore();label(selected?`${s.time.toFixed(1)}s · ${e.name} · y${s.y}`:`${s.time.toFixed(1)}s`,s.x+16,markerY+3,selected?"#8ffff2":"#ffd16e");}
    for(const s of l.spawns){const e=project.entities.find(v=>v.id===s.entityId);if(!e)continue;for(let i=0;i<s.count;i++){const age=state.previewTime-(s.time+i*s.interval);if(age<0||age>12)continue;const pos=motionAt(e,age,{x:s.x,y:s.y},i*.55,s.pattern==="inherit"?null:s.pattern);if(pos.y>-100&&pos.y<800&&pos.x>-100&&pos.x<580){drawUnit(e,pos,.92);drawShotsFor(e,pos,age);}}}label(`${l.name.toUpperCase()} · ${l.spawns.length} SPAWN EVENTS`,12,20,"#ffcf58");label(`${formatTime(state.previewTime)} / ${formatTime(l.duration)}`,12,36,"#83a0ad");updateTimelinePlayhead();}
  function label(text,x,y,color="#fff"){ctx.save();ctx.font='10px "Cascadia Mono",monospace';ctx.fillStyle="#000";ctx.fillText(text,x+1,y+1);ctx.fillStyle=color;ctx.fillText(text,x,y);ctx.restore();}
  function render(){ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,480,720);ctx.save();ctx.translate(state.viewPan.x,state.viewPan.y);ctx.scale(state.viewZoom,state.viewZoom);if(state.mode==="frame")renderFrame();else if(state.mode==="wave")renderWave();else if(state.mode==="level")renderLevel();else renderLive();ctx.restore();}
  function tick(now){const raw=Math.min(.05,(now-state.lastFrame)/1000);state.lastFrame=now;if(state.playing){state.previewTime+=raw*state.previewSpeed;const limit=state.mode==="level"?currentLevel().duration:state.mode==="frame"?999:18;if(state.previewTime>limit)state.previewTime=state.mode==="level"?0:0;}state.frames++;if(now-state.fpsClock>500){state.fps=Math.round(state.frames*1000/(now-state.fpsClock));state.frames=0;state.fpsClock=now;$("#fpsBadge").textContent=`${state.fps} FPS`;}render();requestAnimationFrame(tick);}

  function refreshAll(){renderPatternOptions();renderEntityList();renderAssetVault();renderFrameStrip();refreshInspector();if(state.mode==="level")renderLevelControls();updateStatus();}
  bindUI(); refreshAll(); setMode("live"); requestAnimationFrame(tick);
})();
