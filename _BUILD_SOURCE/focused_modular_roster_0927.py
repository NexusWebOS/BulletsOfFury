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
  report['helpers']=p.evaluate("""()=>{diffKey='hard';DIFF=DIFFS.hard;run.stage=4;curStage=STAGES[3];spawnBoss('stormsovereign');const b=boss;b.enter=false;b._noHit=false;stage4CoreTurretSpawnMissing(b,.5);const d=b._s4war.coreTurrets[0];d.materialize=1;d.shield=0;const q=mr27HelperGun(b,d),g=mr27HelperState(d);_lastHitX=q.x;_lastHitY=q.y;stage4CoreTurretDamage(b,d,g.hp+1);return {size:stage4HelperExtent(d),gun:g,hullAlive:!d.dead,targets:retinaBossTargets(b).filter(q=>q.kind==='helper weapon').length};}""")
  report['actualBreaks']=[]
  for stage,kind,mini in [(3,'cryospear',False),(4,'olivewarden',True),(4,'stormsovereign',False)]:
   p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':mini,'diff':'hard'});p.evaluate('()=>{story=null;s6Opening=null;B.enter=false;B._be=null;B._noHit=false;B.x=worldWidth()/2;B.y=B.ty;B._drawY=B.y;if(B._s4war?.shield){B._s4war.shield.active=false;B._s4war.shield.rearming=false;}er26Set(B,\'warden-suppress\');}')
   report['actualBreaks'].append(p.evaluate("""()=>{const p=mr27Part(B,'gunL'),q=mr27Shape(B,'gunL'),trace=[];for(let i=0;i<3;i++){_lastHitX=q.x;_lastHitY=q.y;_dmgBullet=null;const before=p.hp;if(B===boss)hitBoss(p.maxhp+1);else hitSubBoss(p.maxhp+1,q.x,q.y);trace.push({before,after:p.hp,dead:p.dead,hp:B.hp,noHit:B._noHit,at:mr27At(B,q.x,q.y)});}return {kind:B.kind,trace};}"""))
  report['finale']=[]
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','mini':False,'diff':diff})
   report['finale'].append(p.evaluate("""()=>{vileBuildForm(B,2);B.enter=false;B._v24.shield=0;for(const p of [...B.parts])if(p.dmg){p.hp=1;B._lastPart=p;modularHit(99999);if(!p.destroyed){B._lastPart=p;modularHit(99999);}}return {difficulty:diffKey,form:B._vForm,dead:B.dead,trueRoute:mr27TrueRoute()};}"""))
  report['errors']=errors;br.close()
finally:stop()
(OUT/'focused-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'cases':len(report['cases']),'errors':errors}))
assert not errors,errors
assert all(c['finite'] for c in report['cases'])
