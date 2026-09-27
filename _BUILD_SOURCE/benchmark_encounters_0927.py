"""Native sustained-fire damage-window measurements, NOT player balance or victory claims.
Cole/MG III (space laser III in space), auto missiles II, no manual ammo/elements/specials.
An aiming bot uses normal movement. Immunity removes deaths from this damage-routing sample.
"""
import ast, base64, http.server, json, sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/damage-windows');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
CASES=[(1,'razorback',True),(2,'magmaward',True),(3,'frostcruiser',True),(3,'cryospear',False),(4,'stormsovereign',False),(5,'siegebomber',True),(5,'chromehammer',False),(6,'tempestbrothers',True),(7,'sludgeemperor',False),(9,'voidhorizon',True),(9,'tidalfusion',False)]
if len(sys.argv)>1:CASES=[c for c in CASES if c[1] in sys.argv[1:]]
STEP="""()=>{for(let f=0;f<60;f++){
 if(B.dead||bossDefeated||state!==GS.PLAY)break;
 T.frames++;powerups=[];special=null;run.sonicT=run.dkT=0;player.invuln=2;
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 let targets=_lockTargets().filter(t=>!t.dead&&!t._noHit&&t.y>PLAY.y&&t.y<VH-70&&t.x>24&&t.x<worldWidth()-24);
 const old=targets.find(t=>t===T.target);if(!old||T.frames%180===1){targets.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x));T.target=targets[0]||null;}
 const target=T.target,tx=target?target.x:worldWidth()/2,ty=target?clamp(target.y+135,VH*.58,VH*.82):VH*.8;
 const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
 if(player.x<tx-4)hold('right');else if(player.x>tx+4)hold('left');if(player.y<ty-5)hold('down');else if(player.y>ty+5)hold('up');hold('fire');
 const before=B.hp;updatePlay(1/60);T.max=Math.max(T.max,B.maxhp);T.damage+=Math.max(0,before-B.hp);T.healed+=Math.max(0,B.hp-before);
 T.exposed+=!B.enter&&!B._noHit;T.targetFrames+=!!target;
 const phase=B._hammer?.state||B._s7mod?.mode||B._bomber?.mode||B._er26?.mode||B._late27?.mode||B._s9fusion?.phase||B._tempestDuo?.ai.black.phase;
 if(phase!==T.last){T.phases.push({at:T.frames/60,phase,hp:B.hp});T.last=phase;}
 if(f%15===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.25);}
 }return {seconds:T.frames/60,done:!!B.dead||bossDefeated||state!==GS.PLAY};}"""
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];runs=[]
if len(sys.argv)>1 and (OUT/'report.json').exists():
 prior=json.loads((OUT/'report.json').read_text(encoding='utf-8'));runs=[r for r in prior['runs'] if r['kind'] not in sys.argv[1:]]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for diff in ['normal','hard','furious']:
   for stage,kind,mini in CASES:
    c={'stage':stage,'kind':kind,'mini':mini,'diff':diff};print('RUN',c,flush=True);p.evaluate(SETUP,c)
    p.evaluate("""()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.spaceWeapon=0;run.spaceLevels=[3,3,3];run.missileLevel=2;run.forge={};run.forgeForms={};run.wvars=[];run.infusion=null;run.bombs=0;run.shield=0;special=null;run.sonicT=run.dkT=0;s6Opening=null;timeScale=1;if(s6Wing){s6Wing.ships=[];s6Wing.beats=1;s6Wing.boxes=[];s6Wing.supplyIndex=3;}window.T={frames:0,damage:0,healed:0,exposed:0,targetFrames:0,phases:[],max:B.maxhp};}""")
    for sec in range(180):
     r=p.evaluate(STEP);p.wait_for_timeout(5)
     if sec in [29,89,179] or r['done']:
      (OUT/f'{kind}-{diff}-{sec+1}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
     if r['done']:break
    result=p.evaluate("""c=>({...c,seconds:T.frames/60,damage:T.damage,healed:T.healed,exposed:T.exposed/Math.max(1,T.frames),targetable:T.targetFrames/Math.max(1,T.frames),initialHp:T.max,endHp:B.hp,ended:!!B.dead||bossDefeated,state,phases:T.phases,finite:[...eBullets,...pBullets].every(q=>Number.isFinite(q.x+q.y))})""",c)
    runs.append(result);(OUT/'report.json').write_text(json.dumps({'runs':runs,'errors':errors,'limits':__doc__},indent=2),encoding='utf-8')
    print({k:result[k] for k in ['kind','diff','seconds','damage','endHp','ended']},flush=True)
  br.close()
finally:stop()
assert not errors,errors
assert all(r['finite'] for r in runs)
