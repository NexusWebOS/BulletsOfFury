"""Native projectiles aimed at Stage3 miniboss core, before/after the repair."""
from pathlib import Path
import argparse,base64,hashlib,io,json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/frost_core_1017';OUT.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--before',action='store_true');args=ap.parse_args();tag='before' if args.before else 'after'
checks=[];rows=[];errors=[]
def check(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport={'width':1920,'height':1080});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('''()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(3);
   const tick=er26Tick;er26Tick=function(b,dt){const r=tick.apply(this,arguments);if(b===window.B&&window.frostPin){b.x=frostPin.x;b.y=frostPin.y;b._drawY=b.y;}return r;};
   window.frostHits=[];const hit=hitSubBoss;hitSubBoss=function(d,x,y){const b=subBoss,before=b?.hp,fl=b?.flash;const r=hit.apply(this,arguments);if(b?._ship==='frostcruiser')frostHits.push({kind:_dmgBullet?.kind,damage:before-b.hp,x,y,flash:b.flash});return r;};
  }''')
  def setup(diff='normal',broken=True):
   p.evaluate('''([diff,broken])=>{window.frostPin=null;BAL7.setup({stage:3,kind:'frostcruiser',mini:true,pilot:'cole',diff,seconds:60,fire:false});BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;B.enter=B.dead=B._noHit=B._jcGhost=false;B.x=worldWidth()/2;B.y=190;B._drawY=B.y;B._phaseInvuln=0;B._er26.engaged=true;B._er26.phaseInvuln=0;B._er26.mode='recover';B._er26.t=0;B._er26.warm=0;B._er26.dur=999;B._er26.from={x:B.x,y:B.y};if(broken)for(const q of B._mr27.parts){q.dead=true;q.hp=0;}enemies=[];eBullets=[];pBullets=[];powerups=[];stagePlan=[];player.invuln=99999;player.dead=player.out=false;run.shield=0;retina.target=null;retina.phase=null;window.frostPin={x:B.x,y:B.y};window.frostHits=[];pt11Ready('ice_parts');}''',[diff,broken])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(3).ready&&pt11Ready("ice_parts");}',polling=50)
   return p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);const c=pt11Part(B,'core');player.x=c.x;player.y=c.y+130;camX=clamp(player.x-VW/2,0,worldWidth()-VW);if(window.__bofFit)__bofFit();SC12.refresh();return{hp:B.hp,skin:B._mr27.skin,core:c,at:mr27At(B,c.pivotX,c.pivotY),solid:subBossSolidAt(c.pivotX,c.pivotY)};}''')
  def tick(n):
   for i in range(0,n,8):
    err=p.evaluate(shoot.STEP,min(8,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(5)
  cases=[('machine-gun',0,None,'hold'),('spread',1,None,'hold'),('laser',3,None,'hold'),('flamethrower',4,None,'hold'),('ice-orb',5,'iceorb','hold'),('fire-orb',5,'fireorb','hold'),('chaingun',7,None,'hold'),('missile',0,None,'missile')]
  for diff in (['normal'] if args.before else ['easy','normal','hard','furious']):
   for name,weapon,variant,mode in cases:
    q=setup(diff)
    p.evaluate('''q=>{const [weapon,variant,mode]=q;run.weapon=weapon;run.wlevels??=[];run.wvars??=[];run.wlevels[weapon]=3;run.wlevel=3;run.wvars[weapon]=variant;run.bombs=20;player.fireCd=0;Input.keys.j=mode==='hold';if(mode==='missile'){retina.target=B;retina.phase='locked';retina.lockT=5;useBomb();}}''',[weapon,variant,mode])
    tick(100)
    out=p.evaluate('''()=>{Input.keys.j=false;return{hp:B.hp,damage:frostHits.filter(q=>q.damage>0).reduce((s,q)=>s+q.damage,0),hits:frostHits.filter(q=>q.damage>0).length,seen:[...new Set(frostHits.map(q=>q.kind))],at:mr27At(B,B.x,B._drawY),form:B._er26.form,skin:B._mr27.skin,flash:B.flash};}''');out.update({'diff':diff,'weapon':name,'before':q});rows.append(out)
    print(json.dumps({'tag':tag,'difficulty':diff,'weapon':name,'damage':out['damage'],'solid':q['solid'],'route':q['at']}),flush=True)
    if not args.before:check(diff+' core takes real '+name+' projectiles after all modules break',out['damage']>0,out)
    if name in ['machine-gun','laser','missile'] and diff=='normal':p.screenshot(path=str(OUT/(tag+'-'+name+'.png')))
   if not args.before:check(diff+' remains an ice encounter',all(q['form']=='ice' for q in rows if q['diff']==diff))
  if not args.before:
   setup('normal',False)
   q=p.evaluate('''()=>{const c=pt11Part(B,'core');return{at:mr27At(B,c.pivotX,c.pivotY),solid:subBossSolidAt(c.pivotX,c.pivotY),guns:B._mr27.parts.filter(p=>!p.dead).map(q=>{const p=mr27Shape(B,q.id);return{id:q.id,actual:mr27At(B,p.x,p.y)}})};}''')
   check('The core is reachable while intact modular weapons keep their own routing',q['at']=='core' and q['solid'] and all(p['id']==p['actual'] for p in q['guns']),q)
   p.screenshot(path=str(OUT/'after-intact-core.png'))
   def pixels():
    raw=p.evaluate('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);mr27Draw(B);const s=cv.toDataURL().split(',')[1];ctx.restore();return s;}''')
    return np.array(Image.open(io.BytesIO(base64.b64decode(raw))).convert('RGBA'))
   before=pixels();p.evaluate('''()=>{const c=pt11Part(B,'core');_dmgBullet={kind:'bullet',x:c.pivotX,y:c.pivotY};hitSubBoss(3,c.pivotX,c.pivotY);}''');after=pixels()
   changed=int(np.count_nonzero((before[:,:,3]>128)&(np.max(np.abs(before[:,:,:3].astype(int)-after[:,:,:3].astype(int)),2)>10)))
   check('A real core impact visibly flashes the native damaged pixels',changed>100,{'changedOpaquePixels':changed})
   tick(35);check('Core and module hit-flash timers expire normally',p.evaluate('B.flash<=0&&B._mr27.parts.every(q=>q.flash<=0)'))
   q=p.evaluate('''()=>{const core=()=>{const c=pt11Part(B,'core');return mr27At(B,c.pivotX,c.pivotY);},at=core();B._drawY=B.y+35;const moved=core();B._drawY=B.y;const air=mr27At(B,B.x-140,B.y+110);B.enter=true;const entry=core();B.enter=false;B._noHit=true;const noHit=core();B._noHit=false;B.dead=true;const dead=core();B.dead=false;return{at,moved,air,entry,noHit,dead};}''')
   check('The painted core follows its actual draw position while bare air stays clear',q['at']==q['moved']=='core' and q['air'] is None,q)
   check('Entry, invulnerability and dead-body collision gates remain intact',q['entry'] is None and q['noHit'] is None and q['dead'] is None,q)
   setup('normal',True);p.evaluate('''()=>{B.hp=24;run.weapon=0;run.wlevel=1;run.wlevels[0]=1;player.fireCd=0;Input.keys.j=true;}''');tick(180)
   check('Ordinary machine-gun rounds can deliver the final core kill without missiles',p.evaluate('B.dead&&subBossDone&&!subBossActive'))
   p.evaluate('Input.keys.j=false');p.screenshot(path=str(OUT/'after-gun-finishes-core.png'))
  br.close()
finally:stop()
check('No page, console or missing asset errors',not errors,errors)
report={'passed':sum(q['passed'] for q in checks),'failed':[q for q in checks if not q['passed']],'errors':errors,'cases':rows,'checks':checks}
(OUT/(tag+'-verification.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}),flush=True)
if report['failed'] or errors:sys.exit(1)
