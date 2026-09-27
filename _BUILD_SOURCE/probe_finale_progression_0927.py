"""Natural damage progression through all four Stage 8 shells in real Chromium.
Diagnostic aiming bot; damage immunity except authored grab kills, 99 reserve lives.
Cole Space Laser III, auto missiles II. No HP/form changes, elements or specials.
This verifies reachable phases and damage routing, not campaign balance or wins.
"""
import ast, base64, http.server, json, sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright

OUT=Path('_shots/overnight_0927/finale-progression'); OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
STEP="""()=>{for(let f=0;f<60;f++){
 if(B.dead||bossDefeated||state!==GS.PLAY)break;
 T.frames++;powerups=[];special=null;run.sonicT=run.dkT=0;player.invuln=2;
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 let targets=_lockTargets().filter(t=>!t.dead&&!t._noHit&&t.y>PLAY.y&&t.y<VH-70&&t.x>24&&t.x<worldWidth()-24);
 const old=targets.find(t=>t===T.target);if(!old||T.frames%180===1){targets.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x));T.target=targets[0]||null;}
 const target=T.target, P=B._v24?.pattern;let tx=target?target.x:worldWidth()/2,ty=target?clamp(target.y+145,VH*.6,VH*.82):VH*.8;
 if(P?.type==='phantom'||P?.type==='knight'){tx=clamp(P.tx+(P.tx<worldWidth()/2?100:-100),32,worldWidth()-32);ty=VH*.8;}
 if(P?.type==='box'&&P.fired.lock&&!P.fired.strike){tx=P.strikeX+(P.strikeX<worldWidth()/2?85:-85);ty=VH*.58;}
 const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
 if(player.x<tx-4)hold('right');else if(player.x>tx+4)hold('left');if(player.y<ty-5)hold('down');else if(player.y>ty+5)hold('up');hold('fire');
 const oldForm=B._vForm, oldHp=B.hp, dead=player.dead;updatePlay(1/60);
 if(!dead&&player.dead)T.deaths++;
 if(B._vForm===oldForm)T.damage+=Math.max(0,oldHp-B.hp);
 const phase=B._vForm+':'+(B.enter?'entry':B._v24?.pattern?.type||'recovery');
 if(phase!==T.last){T.phases.push({at:T.frames/60,phase,hp:B.hp,shield:B._v24?.shield,targets:targets.map(q=>({id:q._retinaId,x:q.x,y:q.y}))});T.last=phase;}
 T.forms.add(B._vForm);T.maxBullets=Math.max(T.maxBullets,eBullets.length);
 if(f%15===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.25);}
 }return {seconds:T.frames/60,form:B._vForm,phase:T.last,hp:B.hp,done:!!B.dead||bossDefeated||state!==GS.PLAY};}"""
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];runs=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=browser.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for diff in (sys.argv[1:] or ['normal','hard','furious']):
   c={'stage':8,'kind':'vileexistence','mini':False,'diff':diff};p.evaluate(SETUP,c)
   p.evaluate("""()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.lives=99;run.spaceWeapon=0;run.spaceLevels=[3,3,3];run.missileLevel=2;run.forge={};run.forgeForms={};run.wvars=[];run.infusion=null;run.bombs=0;run.shield=0;special=null;timeScale=1;window.T={frames:0,damage:0,deaths:0,phases:[],forms:new Set([B._vForm]),maxBullets:0};window.audioCues=[];const original=combatAudio0927;combatAudio0927=function(o,c,i){const r=original(o,c,i);if(r)audioCues.push({at:T.frames/60,cue:c,form:B._vForm});return r;};}""")
   last=None
   for sec in range(480):
    r=p.evaluate(STEP);p.wait_for_timeout(10)
    if r['phase']!=last or r['done'] or sec%30==29:
     name=f'{diff}-{sec+1:03d}-{r["phase"].replace(":","-")}.png';(OUT/name).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]));last=r['phase']
    if sec%30==29 or r['done']:print(diff,r,flush=True)
    if r['done']:break
   result=p.evaluate("""d=>({diff:d,seconds:T.frames/60,damage:T.damage,deaths:T.deaths,forms:[...T.forms],maxBullets:T.maxBullets,endHp:B.hp,ended:!!B.dead||bossDefeated,state,phases:T.phases,audioCues,parts:B.parts.map(p=>({id:p.rc,hp:p.hp,dead:p.destroyed})),finite:[...eBullets,...pBullets].every(q=>Number.isFinite(q.x+q.y))})""",diff)
   runs.append(result);(OUT/'report.json').write_text(json.dumps({'runs':runs,'errors':errors,'limits':__doc__},indent=2),encoding='utf-8')
  browser.close()
finally:stop()
assert not errors,errors
assert all(r['finite'] for r in runs)
