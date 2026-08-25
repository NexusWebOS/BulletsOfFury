#!/usr/bin/env python3
import re, json, os, sys, time

# ============================================================
# STALE-SOURCE GUARD (drop 0805a)
#
# assets/game.js is what index.html actually loads. On 0801ku it was found to be
# NINE DROPS AHEAD of gamecode.js: every change from 0801kl through 0801ku (the
# crackle strip, sxPackDraw, section_geom, the missile crates, the audio loops,
# the stage-4 crash overlay, the ice-breath fix) had been hand-edited straight
# into the built artifact and never back-ported. 45 diff hunks.
#
# Running this script in that state silently reverts all of it, and because the
# harness reads assets/game.js the loss shows up as dozens of "fixed" things
# breaking again with no obvious cause. That is the most expensive possible
# failure mode, so it is now impossible to hit by accident.
#
# If you have deliberately back-ported and want to rebuild, pass --force.
# ============================================================
def _guard_stale_sources():
    if '--force' in sys.argv:
        print('[guard] --force given; overwriting assets/game.js'); return
    built = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'game.js')
    built = os.path.normpath(built)
    if not os.path.exists(built):
        return
    bt = os.path.getmtime(built)
    for src in ('gamecode.js', 'patches.js'):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), src)
        if os.path.exists(p) and os.path.getmtime(p) < bt:
            print('=' * 68)
            print('REFUSING TO BUILD — assets/game.js is NEWER than ' + src)
            print('  ' + src + ':      ' + time.ctime(os.path.getmtime(p)))
            print('  assets/game.js:  ' + time.ctime(bt))
            print('')
            print('The built artifact contains work the sources do not. Building now')
            print('would destroy it. Diff them first:')
            print('  python3 assemble.py --force   (only after back-porting)')
            print('=' * 68)
            sys.exit(2)
_guard_stale_sources()

BT=chr(96)
# ---- load JS blocks from patches.js ----
pj=open('patches.js').read()
blocks={}
for m in re.finditer(r'const (B_\w+) = String\.raw'+BT+r'(.*?)'+BT+r';', pj, re.S):
    blocks[m.group(1)]=m.group(2)
print("loaded blocks:", list(blocks.keys()))
for need in ['B_XART','B_PILOTS','B_BOOTSEQ','B_TITLE','B_DIFF','B_PW','B_LAUNCH']:
    assert need in blocks, "missing "+need

src=open('gamecode.js').read()
orig_len=len(src)

def span_replace(s, start_anchor, end_anchor, new, label):
    i=s.find(start_anchor); assert i>=0, "start not found: "+label
    j=s.find(end_anchor, i); assert j>i, "end not found: "+label
    return s[:i]+new+s[j:]

def replace(s, old, new, label, n=1):
    c=s.count(old); assert c==n, f"{label}: expected {n} match got {c}"
    return s.replace(old,new)

def insert_before(s, anchor, ins, label):
    i=s.find(anchor); assert i>=0, "anchor not found: "+label
    return s[:i]+ins+"\n"+s[i:]

def insert_after_line(s, anchor, ins, label):
    i=s.find(anchor); assert i>=0, "anchor not found: "+label
    e=s.find("\n", i)+1
    return s[:e]+ins+"\n"+s[e:]

# 1) GS enum
src=replace(src,
"""const GS = { BOOT:'boot', TITLE:'title', DIFF:'diff', PASSWORD:'password',
  OPTIONS:'options', INTRO:'intro', PLAY:'play', GAMEOVER:'gameover',
  VICTORY:'victory', STAGECLEAR:'stageclear', CONTINUE:'continue' };""",
"""const GS = { BOOT:'boot', LOADING:'loading', TITLE:'title', DIFF:'diff', PILOT:'pilot',
  PASSWORD:'password', CREDITS:'credits', OPTIONS:'options', INTRO:'intro', LAUNCH:'launch',
  PLAY:'play', GAMEOVER:'gameover', VICTORY:'victory', STAGECLEAR:'stageclear', CONTINUE:'continue', RIVAL:'rival', FLYOVER:'flyover', STAGESEL:'stagesel', MODESEL:'modesel', OUTBOUND:'outbound', OPENING:'opening' };""",
"GS enum")

# 2) PILOTS + flash globals after DIFF normal line
src=insert_after_line(src, "let DIFF = DIFFS.normal;", blocks['B_PILOTS'], "B_PILOTS")

# 3) run object: add pilot field
src=replace(src,
"  speed:0, speedT:0, speedLevel:0, shield:0, power:0, distance:0,\n};",
"  speed:0, speedT:0, speedLevel:0, shield:0, power:0, distance:0, pilot:'axel',\n};",
"run pilot field")

# 4) playerBaseSpeed pilot mod
src=replace(src,
"function playerBaseSpeed(){ return 2.6 + run.speed*0.55; }",
"function playerBaseSpeed(){ return (2.6 + run.speed*0.55)*(1+(PILOTMOD?PILOTMOD.spd:0)); }",
"playerBaseSpeed")

# 5) fire cd pilot mod (applies only to the normal weapon cd, not the constant special rates)
src=replace(src,
"      else cd = _weaponCadence();\n      player.fireCd=(cd!=null?cd:0.2); pShoot();",
"      else cd = _weaponCadence();\n      player.fireCd=(cd!=null?cd:0.2)*(specialActive('maverick')||specialActive('yuri')?1:(1-(PILOTMOD?PILOTMOD.fire:0))); pShoot();",
"fire cd", 1)   # was 2: the free-flight dogfight carried its own copy of the player
                # fire path. That whole function was deleted in drop 0724m (the rival RACE replaced
                # it), so exactly one copy — the real one in updatePlay — remains.

# 6) startRun: apply pilot
src=replace(src,
"""function startRun(fromStage=1){
  DIFF=DIFFS[diffKey];
  run.stage=fromStage; run.score=0;""",
"""function startRun(fromStage=1){
  DIFF=DIFFS[diffKey]||DIFFS.normal;
  const _P=PILOTS[pilotIndex]||PILOTS[0]; run.pilot=_P.key;
  PILOTMOD={spd:_P.spd||0, fire:_P.fire||0, range:_P.range||0, tint:_P.tint};
  run.stage=fromStage; run.score=0;""",
"startRun pilot")

# 7) XART block before drawBossSprite
src=insert_before(src, "function drawBossSprite(b){", blocks['B_XART'], "B_XART")

# 8) Audio SFX: add launch + thruster after shatter
src=replace(src,
"    shatter(){ noise(0.18,0.6,5200,-2400); for(let k=0;k<7;k++){ setTimeout(()=>tone(1400+Math.random()*1600,0.10,'triangle',0.10),k*22); } },",
"""    shatter(){ noise(0.18,0.6,5200,-2400); for(let k=0;k<7;k++){ setTimeout(()=>tone(1400+Math.random()*1600,0.10,'triangle',0.10),k*22); } },
    launch(){ noise(0.9,0.5,2200,500); tone(110,0.9,'sawtooth',0.24,420); tone(170,0.7,'triangle',0.14,260); },
    thruster(){ noise(1.2,0.55,2000,-1500); tone(70,1.05,'sawtooth',0.26,-30); tone(140,0.7,'triangle',0.18,-90); },
    brake(){ noise(0.7,0.42,1700,-1350); tone(300,0.6,'sawtooth',0.2,-230); tone(120,0.45,'triangle',0.14,-80); },""",
"SFX launch/thruster")

# 9) drawScene dispatch
src=replace(src,
"""function drawScene(dt){
  switch(state){
    case GS.BOOT:    return drawBoot(dt);
    case GS.TITLE:   return drawTitle(dt);
    case GS.DIFF:    return drawDiff(dt);
    case GS.PASSWORD:return drawPassword(dt);
    case GS.OPTIONS: return drawOptions(dt);
    case GS.INTRO:   return drawIntro(dt);
    case GS.PLAY:    return drawWorld(dt);
    case 'paused':   drawWorld(0); return drawPaused();
    case GS.STAGECLEAR: return drawStageClear(dt);
    case GS.GAMEOVER:return drawGameOver(dt);
    case GS.CONTINUE: return drawContinue(dt);
    case GS.VICTORY: return drawVictory(dt);
  }
}""",
"""function drawScene(dt){
  if(typeof window!=='undefined') window.__bofFrames=(window.__bofFrames|0)+1;
  if(typeof window!=='undefined') window.__bofFrames=(window.__bofFrames|0)+1;   // watchdog: proves the loop is running
  switch(state){
    case GS.OPENING: return drawOpening(dt);
    case GS.BOOT:    return drawBoot(dt);
    case GS.LOADING: return drawLoading(dt);
    case GS.TITLE:   return drawTitle(dt);
    case GS.DIFF:    return drawDiff(dt);
    case GS.PILOT:   return drawPilot(dt);
    case GS.PASSWORD:return drawPassword(dt);
    case GS.CREDITS: return drawCredits(dt);
    case GS.OPTIONS: return drawOptions(dt);
    case GS.INTRO:   return drawIntro(dt);
    case GS.LAUNCH:  return drawLaunch(dt);
    case GS.OUTBOUND: return drawOutbound(dt);
    case GS.PLAY:    return drawWorld(dt);
    case 'paused':   drawWorld(0); return drawPaused();
    case GS.STAGECLEAR: return drawStageClear(dt);
    case GS.GAMEOVER:return drawGameOver(dt);
    case GS.CONTINUE: return drawContinue(dt);
    case GS.VICTORY: return drawVictory(dt);
    case GS.RIVAL:   return drawRivalSeq(dt);
    case GS.FLYOVER: return drawFlyover(dt);
    case GS.STAGESEL: return drawStageSelect(dt);
    case GS.MODESEL: return drawModeSelect(dt);
  }
}""",
"drawScene")

# 10) drawBoot block -> B_BOOTSEQ  (replace boot comment..goTitle)
src=span_replace(src,
  "/* BOOT \u2014 ColeForge studio screen + boot chime */",
  "function goTitle(){ Audio.init();",
  blocks['B_BOOTSEQ']+"\n", "drawBoot block")

# 11) TITLE block -> B_TITLE (TITLE_ITEMS..tryExit)
src=span_replace(src,
  "const TITLE_ITEMS=['NEW GAME','PASSWORD','OPTIONS','EXIT GAME'];",
  "function tryExit(){",
  blocks['B_TITLE']+"\n", "TITLE block")

# 12) DIFF block -> B_DIFF (DIFF_KEYS..drawTitleBackdrop)
src=span_replace(src,
  "const DIFF_KEYS=['easy','normal','hard'];",
  "function drawTitleBackdrop(dt){",
  blocks['B_DIFF']+"\n", "DIFF block")

# 13) drawPassword -> B_PW (drawPassword..submitPassword)
src=span_replace(src,
  "function drawPassword(dt){",
  "function submitPassword(){",
  blocks['B_PW']+"\n", "drawPassword block")

# 14) proceedIntro -> launch
src=replace(src,
"function proceedIntro(){ resetIntro(); drawIntro._snd=false; setState(GS.PLAY); Audio.startMusic((curStage&&curStage.music)||'stage'); }",
"function proceedIntro(){ resetIntro(); drawIntro._snd=false; setState(GS.LAUNCH); }",
"proceedIntro")

# 15) legacy intro proceed -> launch
src=replace(src,
"  const proceed=()=>{ drawIntro._snd=false; drawIntro._mus=false; setState(GS.PLAY); Audio.startMusic((curStage&&curStage.music)||'stage'); };",
"  const proceed=()=>{ drawIntro._snd=false; drawIntro._mus=false; setState(GS.LAUNCH); };",
"legacy intro proceed")

# 16) drawLaunch block before metalBanner
src=insert_before(src, "function metalBanner(){", blocks['B_LAUNCH'], "B_LAUNCH")

# 17) stage start -> INTRO card first (then card hands off to LAUNCH transition)
src=replace(src,
"  setState(GS.INTRO);\n  Audio.stopMusic();",
"  setState(GS.INTRO);\n  Audio.stopMusic();/*card-first*/",
"beginStage->INTRO")

# 18) drawPlayer pilot ship pivot is handled directly in gamecode.js now (pv/br twist frames).
#     The old _t/_l/_r select-screen banking injection was REMOVED: it intercepted _drawPlayerCore
#     and returned before the new pv->twist pivot block could run, so turning only showed the mild
#     _t/_l/_r bank and never the edge-on twist.

# 19) SUPERSAMPLE backing (2x) + smooth scaling for crisp detailed art
src=replace(src,
"""ctx.imageSmoothingEnabled = false;

/* ---- responsive integer scaling, letterboxed ---- */
function fitCanvas(){
  const ww = window.innerWidth, wh = window.innerHeight;
  let s = Math.min(ww/VW, wh/VH);
  s = Math.max(0.5, s);
  cv.style.width = Math.floor(VW*s)+'px';
  cv.style.height = Math.floor(VH*s)+'px';
}
window.addEventListener('resize', fitCanvas); fitCanvas();""",
"""const SS = 2;                       /* supersample backing for crisp detailed art */
cv.width = VW*SS; cv.height = VH*SS;
ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
function fitCanvas(){
  const ww = window.innerWidth, wh = window.innerHeight;
  let s = Math.min(ww/VW, wh/VH); s = Math.max(0.5, s);
  cv.style.width = Math.round(VW*s)+'px';
  cv.style.height = Math.round(VH*s)+'px';
}
window.addEventListener('resize', fitCanvas); fitCanvas();""",
"supersample setup")

src=replace(src,
"  dt=Math.min(dt,0.05); stateT+=dt;\n  ctx.imageSmoothingEnabled=false;",
"""  /* CLAMP BOTH ENDS (drop 0724df). This was Math.min(dt,0.05) with NO lower bound, so a single
     negative frame permanently poisoned stateT — and stateT never recovers, because it accumulates.
     Every state gate that waits on `t >= X` then fails FOREVER: the loading screen never calls
     goTitle, the game sits there, no input is processed, and the loop's own try/catch keeps
     running so nothing looks like it crashed. Measured in a browser simulation: stateT reached
     -1,785,288,103 and the game was stuck on 'loading' after 1,001 frames.
     dt can go negative from a backgrounded tab, a clock adjustment, or a rAF timestamp that does
     not share an origin with performance.now(). Clamping to [0, 0.05] costs nothing and removes
     the whole class. */
  dt=Math.max(0, Math.min(dt,0.05)); stateT+=dt;
  if(!(stateT>=0)) stateT=0;                 // belt and braces: never let it go bad at all
  ctx.setTransform(SS,0,0,SS,0,0); ctx.imageSmoothingEnabled=true;""",
"loop supersample transform")

# 20) skinned options menu
src=span_replace(src,
  "function drawOptions(dt){",
  "/* ===== STAGE INTRO + STAGE FONT",
  blocks['B_OPTIONS']+"\n/* ===== STAGE INTRO + STAGE FONT", "drawOptions skin")

# 21) AUDIO: add 'stageend' synth track + stat/rank sounds + synth fallback for missing sample tracks
src=replace(src,
"    boss:   {bass:[41,41,49,55],   arp:[247,330,415,330, 220,294,370,294], tempo:185},\n  };",
"    boss:   {bass:[41,41,49,55],   arp:[247,330,415,330, 220,294,370,294], tempo:185},\n    stageend:{bass:[65,65,73,82],   arp:[523,659,784,659, 587,784,988,784], tempo:128},\n  };",
"stageend music pattern")

src=replace(src,
"    shatter(){ noise(0.18,0.6,5200,-2400); for(let k=0;k<7;k++){ setTimeout(()=>tone(1400+Math.random()*1600,0.10,'triangle',0.10),k*22); } },",
"""    shatter(){ noise(0.18,0.6,5200,-2400); for(let k=0;k<7;k++){ setTimeout(()=>tone(1400+Math.random()*1600,0.10,'triangle',0.10),k*22); } },
    statTick(){ tone(880,0.05,'square',0.16,-200); },
    statCount(){ tone(1280,0.016,'square',0.06); },
    rankStamp(g){ const base=g==='S'?1568:g==='A'?1318:g==='B'?1046:g==='C'?880:g==='D'?660:392;
      tone(base,0.32,'square',0.30); tone(base*1.5,0.30,'square',0.15); noise(0.2,0.32,3200,-2000);
      setTimeout(()=>tone(base*2,0.4,'square',0.20),90); },""",
"stat/rank synth sfx")

src=replace(src,
"  Audio.startMusic=function(n){ Snd.startMusic(n); };",
"  const _synthMusic=Audio.startMusic;\n  Audio.startMusic=function(n){ if(Snd.music[n]){ Snd.startMusic(n); } else { try{Snd.stopMusic();}catch(e){} if(_synthMusic)_synthMusic(n); } };",
"synth music fallback")

# 22) STATS tracking (kills / shots / hits / lives) for the arcade stage-end
src=replace(src,
"const WEAPONS=['MACHINE GUN','SPREAD FIRE','MISSILES','LASER','FLAMETHROWER','ICE ORB'];",
"const WEAPONS=['MACHINE GUN','SPREAD FIRE','MISSILES','LASER','FLAMETHROWER','ICE ORB'];\nlet stageStats={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0};",
"stageStats global")

src=replace(src,
"  run.stage=num; mapScroll=0; damBroken=false;",
"  run.stage=num; mapScroll=0; damBroken=false;\n  stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score};\n  if(typeof drawStageClear!=='undefined'){ drawStageClear._init=false; drawStageClear._rsnd=false; for(const _k in drawStageClear){ if(/^_(l|c)\\d/.test(_k)) delete drawStageClear[_k]; } }",
"stageStats reset")

src=replace(src,
"function pShoot(){\n  const w=run.weapon, lv=run.wlevel;",
"function pShoot(){\n  const w=run.weapon, lv=run.wlevel; const _sn0=pBullets.length;",
"pShoot shot count start")

# FLAMETHROWER (drop 0730a): the old anchor was the firewall projectile's sound call, which no
# longer exists — weapon 4 is a held emitter now. Anchored on the new tail instead. The shot
# counter still works: flameFire pushes exactly one 'flame' entity the first time it is called
# and refreshes it thereafter, so a held jet counts as one shot rather than ten a second.
src=replace(src,
"    flameFire(lv);\n  }\n}",
"    flameFire(lv);\n  }\n  stageStats.shots+=(pBullets.length-_sn0);\n}",
"pShoot shot count end")

src=replace(src,
"          hitEnemy(e,b.dmg);\n          if(b.kind==='nade'){ nadeBlast(b); }",
"          hitEnemy(e,b.dmg); stageStats.hits++;\n          if(b.kind==='nade'){ nadeBlast(b); }",
"hit count")

src=replace(src,
"function killEnemy(e){\n  if(e.dead) return;",
"function killEnemy(e){\n  if(e.dead) return;\n  if(e._dyingT==null && typeof stageStats!==\'undefined\') stageStats.kills++;",
"kill count")

# 23) arcade stage-end (stats + rank), replaces drawStageClear
src=span_replace(src,
  "/* STAGE CLEAR */\nfunction drawStageClear(dt){",
  "/* GAME OVER */",
  blocks['B_STAGEEND']+"\n\n/* GAME OVER */", "drawStageClear arcade")

# 24) URL-aware loaders (externalised asset build): mk() + sample audio accept relative URLs
src=replace(src,
"  function mk(d,m){ if(!d)return null; const im=new Image(); im.src='data:'+m+';base64,'+d; return im; }",
"  function mk(d,m){ if(!d)return null; const im=new Image(); im.src=(typeof d==='string'&&d.lastIndexOf('assets/',0)===0)?d:('data:'+m+';base64,'+d); return im; }",
"ASSETS mk url-aware")
src=replace(src,
"  for(const name in BOFA.sfx){ const uri='data:audio/mpeg;base64,'+BOFA.sfx[name];",
"  function _au(v){ return (typeof v==='string'&&v.lastIndexOf('assets/',0)===0)?v:('data:audio/mpeg;base64,'+v); }\n  for(const name in BOFA.sfx){ const uri=_au(BOFA.sfx[name]);",
"Snd sfx url-aware")
src=replace(src,
"  for(const name in BOFA.music){ const m=new window.Audio(); m.src='data:audio/mpeg;base64,'+BOFA.music[name]; m.loop=true; m.preload='auto'; A.music[name]=m; }",
"  for(const name in BOFA.music){ const m=new window.Audio(); m.src=_au(BOFA.music[name]); m.loop=true; m.preload='auto'; A.music[name]=m; }",
"Snd music url-aware")

# 25) new image HUD bar
src=span_replace(src,
  "function drawHUDCustom(){",
  "/* ---- framed HUD ---- */",
  blocks['B_HUD']+"\n/* ---- framed HUD ---- */", "image HUD bar")

# 26) per-stage + per-boss music (real tracks)
src=replace(src, "bg:'jungle', music:'jungle'", "bg:'jungle', music:'lvl1'", "stage1 music")
src=replace(src, "bg:'volcano',music:'bullets'", "bg:'volcano',music:'bullets'", "stage2 music")
src=replace(src, "bg:'ice',    music:'stage'", "bg:'ice',    music:'lvl3'", "stage3 music")
# 'stage4 music' was MISLABELLED and matched STAGE 6, because both stages are bg:'sky' and the
# anchor's padded spacing only lined up with stage 6's row. Net effect: stage 6 played level 4's
# track and stage 4 was left on the generic 'stage' fallback. Both now set explicitly in
# gamecode.js (stage 4 -> lvl4, stage 6 -> deathtrap), so this step is gone rather than re-aimed.
# MUSIC REASSIGNMENT (drop 0724cg). Set here, not in gamecode.js, because these anchors already
# own the stage rows — editing gamecode directly consumed the anchors and broke the build twice.
src=replace(src, "music:'stage5mus'", "music:'lvl3-alt'", "stage5 music -> lvl3-alt")
src=replace(src, "bg:'sewer',  music:'stage'", "bg:'sewer',  music:'stage7mus'", "stage7 music -> Fierce Planes")
# stage5 sub uses the pack's canonical name "ALL FOR ONE, NONE FOR ALL" (no override)
src=replace(src, "Audio.startMusic('boss');", "Audio.startMusic('boss'+run.stage);", "per-stage boss music")

# 27) cabinet-aware canvas fit: fill #screen-area if present, else window
src=span_replace(src,
"function fitCanvas(){",
"window.addEventListener('resize', fitCanvas); fitCanvas();",
r"""function fitCanvas(){
  /* ASPECT-LOCKED + CENTRED.
     This used to stretch the canvas to EXACTLY #screen-area's box (width=clientWidth,
     height=clientHeight) and return. Whenever that box's aspect did not match the game's
     480x512 the picture was stretched, and in FULLSCREEN it also sat off-centre because
     nothing re-centred it inside the box. Fit the largest 480x512-proportioned rectangle that
     fits the host, then centre it on both axes. Falls back to the window if the host is absent. */
  const host=document.getElementById('screen-area');
  let ww, wh;
  if(host && host.clientWidth>2 && host.clientHeight>2){ ww=host.clientWidth; wh=host.clientHeight; }
  else { ww=window.innerWidth; wh=window.innerHeight; }
  let s = Math.min(ww/VW, wh/VH);
  if(!isFinite(s) || s<=0) s = 1;
  s = Math.max(0.5, s);
  const dw=Math.round(VW*s), dh=Math.round(VH*s);
  cv.style.width  = dw+'px';
  cv.style.height = dh+'px';
  /* Centring is done in CSS (#screen-area canvas is absolutely positioned and transform-centred),
     so fitCanvas only owns SIZE. Setting margins here as well fought the transform. */
  cv.style.display='block';
}
window.addEventListener('resize', fitCanvas);
window.addEventListener('orientationchange', fitCanvas);
document.addEventListener('fullscreenchange', fitCanvas);
document.addEventListener('webkitfullscreenchange', fitCanvas);
fitCanvas();""",
"cabinet-aware fitCanvas")

# 28) extended stageStats fields (rival/stats system)
src=replace(src,
"let stageStats={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0};",
"let stageStats={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0};",
"stageStats decl")
src=replace(src,
"stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score};",
"stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0};",
"stageStats reset")

open('gamecode_patched.js','w').write(src)
print(f"patched game code: {orig_len} -> {len(src)} chars (+{len(src)-orig_len})")

# ---- build BOFX script ----
OUT=json.load(open('bofx.json'))
imgs={k:v for k,v in OUT.items() if k!='__chime__'}
bofx={'img':imgs, 'chime':OUT['__chime__']}
bofx_script='<script>/*xart*/window.BOFX='+json.dumps(bofx,separators=(',',':'))+';</script>\n'

# ---- reassemble HTML ----
html=open('bofbuild/BulletsOfFury.html',encoding='utf-8',errors='replace').read()
# smooth (non-pixelated) upscale so high-res cards/ships/logos stay crisp
html=html.replace('image-rendering:pixelated;image-rendering:crisp-edges;','image-rendering:auto;')
idx=html.rfind('"use strict"')
sopen=html.rfind('<script', 0, idx)
sbody=html.find('>', sopen)+1
sclose=html.find('</script>', idx)
new_html = html[:sopen] + bofx_script + html[sopen:sbody] + src + html[sclose:]
os.makedirs('/mnt/user-data/outputs', exist_ok=True)
open('out.html','w').write(new_html)
print("HTML:", len(html), "->", len(new_html), "(+%.2f MB)"%((len(new_html)-len(html))/1024/1024))
print("OK")
