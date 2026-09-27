"""Native modular roster: real update/render, targeted damage and geometry checks."""
import ast,base64,http.server,json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/modular_roster_0927');OUT.mkdir(exist_ok=True,parents=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={'cases':[]}
def shot(p,name): (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>Object.keys(MR27_ART).forEach(k=>XART.rdy('mr27_'+k))");p.wait_for_function("()=>Object.keys(MR27_ART).every(k=>XART.rdy('mr27_'+k))")
  for stage,kind,mini in [(3,'cryospear',False),(4,'olivewarden',True),(4,'stormsovereign',False),(5,'spacebomber',True),(6,'siegebomber',True)]:
   for diff in ['easy','normal','hard','furious']:
    case={'stage':stage,'kind':kind,'mini':mini,'diff':diff};print(case,flush=True);p.evaluate(SETUP,case);p.evaluate('()=>{story=null;s6Opening=null;s6Wing=null;run._lifeThreat=0;run._threatBuild=0;}')
    p.evaluate('()=>{window.seen=[];window.peak=0;window.forms=[];}')
    for sec in range(42):
     p.evaluate("()=>{for(let i=0;i<60;i++){player.invuln=999;updatePlay(1/60);if(i%4===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/15);}const mode=B._er26?.mode||B._bomber?.mode;if(!seen.includes(mode))seen.push(mode);const form=B._er26?.form;if(form&&!forms.includes(form))forms.push(form);peak=Math.max(peak,eBullets.filter(q=>!q.dead).length);}}")
     p.wait_for_timeout(15)
     if sec in [6,14,24] and diff in ['normal','furious']:shot(p,f'{kind}-{diff}-{sec}')
    sample=p.evaluate("()=>({hp:B.hp,max:B.maxhp,seen,forms,peak,zoom:typeof bossZoom==='undefined'?null:bossZoom,parts:B._mr27?.parts||B._bomber?.parts,draws:B._mr27?.draws,enter:B.enter,finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy))})")
    sample['case']=case
    sample['damage']=p.evaluate("""()=>{const out=[];if(B._mr27){if(B._s4war?.shield){B._s4war.shield.active=false;B._s4war.shield.rearming=false;B._noHit=false;}B._noHit=false;for(const part of B._mr27.parts){const q=mr27Shape(B,part.id);_lastHitX=q.x;_lastHitY=q.y;_dmgBullet=null;const hp=B.hp,at=mr27At(B,q.x,q.y);if(B===boss)hitBoss(part.hp+1);else hitSubBoss(part.hp+1,q.x,q.y);out.push({id:part.id,at,dead:part.dead,delta:hp-B.hp,fire:mr27CanFire(B,part.id==='gunL'?'L':part.id==='gunR'?'R':part.id==='rocketL'?'ROCKET_L':'ROCKET_R')});if(B._s4war?.shield){B._s4war.shield.active=false;B._s4war.shield.rearming=false;B._noHit=false;}}}else for(const part of B._bomber.parts){const q=siegeBomberParts(B).find(p=>p.id===part.id);hitSubBoss(part.hp+1,q.x,q.y);out.push({id:part.id,hp:part.hp});}return out;}""")
    shot(p,f'{kind}-{diff}-broken');report['cases'].append(sample)
  report['route']=p.evaluate("()=>['easy','normal','hard','furious'].map(k=>{diffKey=k;return {difficulty:k,trueRoute:mr27TrueRoute(),mini5:SUBBOSS[5].kind,mini6:SUBBOSS[6].kind};})")
  report['errors']=errors;br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'cases':len(report['cases']),'errors':errors}))
assert not errors,errors
assert all(c['finite'] for c in report['cases'])
