"""Native Harrier: clear bay, existing hull guns, warned rain and muzzle/hit pixels."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/harrier_hull_1021';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n+((' '+json.dumps(d)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(6)")
  p.evaluate('''()=>{window.HH={clock:0,shots:[],flashes:[],warnings:[],plates:[],blits:0,hits:[]};const draw=ctx.drawImage;ctx.drawImage=function(){HH.blits++;return draw.apply(this,arguments);};const fire=eShootT,muzzle=wm26Draw,warn=combatWarningDraw,plate=pf20TurretDraw,test=warhiveHitTest;
   eShootT=function(x,y,a,s,k){const q=fire.apply(this,arguments);HH.shots.push({q,x,y,a,t:HH.clock});return q;};
   wm26Draw=function(g,f,x,y,a){const before=HH.blits,out=muzzle.apply(this,arguments);if(f==='mg'&&HH.blits>before)HH.flashes.push({x,y,a,t:HH.clock});return out;};
   warhiveHitTest=function(b,x,y){const out=test.apply(this,arguments);if(out&&b._carrier17)HH.hits.push({x,y,id:b._carrier17.hit});return out;};
   combatWarningDraw=function(owner,q){if(B?._carrier17?.parts.includes(owner)&&owner.kind==='gun')HH.warnings.push({id:owner.id,t:HH.clock,...q});return warn.apply(this,arguments);};
   pf20TurretDraw=function(part){HH.plates.push(part.id);return plate.apply(this,arguments);};
   window.hhPixels=()=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width/SS,cv.height/SS);ctx.translate(-camX,0);warhiveDraw(B);ctx.restore();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};
   window.hhChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};}''')
  def frames(n,aim=False):
   for i in range(0,n,12):
    p.evaluate('''({n,aim})=>{for(let i=0;i<n;i++){if(aim){const m=roster17Mount(B,G);player.x=m.x;player.y=m.y+160;}HH.clock+=1/60;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}''',dict(n=min(12,n-i),aim=aim));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=6,kind='warhive',diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&bmfReady("game")}')
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    VP12.next=CP12.next=EP13.next=HM17.next=TARGET17.nextTank=SEWER17.next=999999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;s6Wing=null;
    B._be=null;B.enter=false;B._phaseInvuln=0;player.x=worldWidth()/2;player.y=VH-60;player.invuln=1e9;run.shield=0;run.spaceMode=false;special=thunderStorm=null;run.sonicT=run.dkT=0;Input.keys={};Input.mouse.down=false;
    HH.clock=0;HH.shots=[];HH.flashes=[];HH.warnings=[];HH.plates=[];SC12.refresh();__bofFit();}''');frames(180)
   p.evaluate('B._carrier17.flight=999;HH.clock=0;HH.shots=[];HH.flashes=[];HH.warnings=[];HH.plates=[];for(const p of B._carrier17.parts){p.phase="rest";p.t=0;p.cool=.2+(p.hullGun||0)*.20;}')
   row=p.evaluate('''()=>{const C=B._carrier17,rank=target17Rank(),targets=retinaBossTargets(B);return{ids:C.parts.map(p=>p.id),lasers:C.parts.filter(p=>p.kind==='laser').map(p=>p.id),guns:C.parts.filter(p=>p.kind==='gun').length,hp:B.hp,expected:2*(140+rank*22)+4*(105+rank*20)+2*(125+rank*20),targets:targets.length,bayHit:roster17At(B,B.x,B.y+65*WHV_S*roster17HullScale(B))};}''')
   ck(diff+' two fan-side batteries stay, bay batteries are removed and native hull guns replace their HP',row['lasers']==['laser0','laser3'] and 'laser1' not in row['ids'] and 'laser2' not in row['ids'] and row['guns']==4 and row['hp']==row['expected'] and row['targets']==10 and row['bayHit']=='armor',row)
   frames(60);snap(diff+'-fov');frames(90);snap(diff+'-warned-rain');frames(400)
   row=p.evaluate('''()=>{const shots=HH.shots.filter(s=>s.q._carrierHullGun),ids=[...new Set(shots.map(s=>s.q._carrierHullGun))],matches=shots.filter(s=>HH.flashes.some(f=>Math.abs(f.t-s.t)<.0001&&Math.hypot(f.x-s.x,f.y-s.y)<.1));
    return{ids,shots:shots.length,matchingFlashes:matches.length,missing:shots.filter(s=>!matches.includes(s)).map(s=>({id:s.q._carrierHullGun,t:s.t,nearest:HH.flashes.filter(f=>Math.abs(f.t-s.t)<.0001).map(f=>Math.hypot(f.x-s.x,f.y-s.y))})),overlayIDs:[...new Set(HH.plates)],warnings:[...new Set(HH.warnings.map(w=>w.id))],first:ids.map(id=>({id,shot:shots.find(s=>s.q._carrierHullGun===id).t,tell:HH.warnings.find(w=>w.id===id)?.t})),warm:roster17GunConfig().warm};}''')
   ck(diff+' only the two outer added turret plates draw',set(row['overlayIDs'])=={'laser0','laser3'},row['overlayIDs'])
   ck(diff+' every native gun warns and fires actual bullet rain with a same-frame socket flash',len(row['ids'])==4 and len(row['warnings'])==4 and row['shots']>=20 and row['matchingFlashes']==row['shots'] and all(s.get('tell') is not None and s['shot']-s['tell']>=row['warm']-.04 for s in row['first']),row)
   # Isolate a single native hull gun and inspect its actual damaged pixels.
   row=p.evaluate('''()=>{enemies=[];eBullets=[];pBullets=[];for(const p of B._carrier17.parts){p.phase='rest';p.cool=999;p.flash=p.fl=0;p.muzzleAge=99;}window.G=B._carrier17.parts.find(p=>p.id==='hullGun1');const a=hhPixels(),hp=G.hp;B._carrier17.direct=G.id;_dmgBullet={kind:'mg'};hitBoss(1);_dmgBullet=null;const b=hhPixels();return{loss:hp-G.hp,pixels:hhChanged(a,b),flash:G.flash};}''')
   ck(diff+' native gun housing visibly flashes from actual modular damage',row['loss']>0 and row['pixels']>20 and row['flash']>0,row)
   frames(20);ck(diff+' native gun hit flash expires normally',p.evaluate('G.flash<=0&&G.fl<=0'))
   p.evaluate('''()=>{enemies=[];B._whv.jets=[];s6r18State(B).bay.mode='cool';s6r18State(B).bay.t=0;weaponFormSelect(7,{kind:'primary1003b',id:'mg'});chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];const m=roster17Mount(B,G);player.x=m.x;player.y=m.y+160;player._bank=0;player.fireCd=0;window.gunBefore=G.hp;}''')
   p.keyboard.down('j');frames(60,True);p.keyboard.up('j');ck(diff+' real J machine-gun rounds reach the native hull gun',p.evaluate('G.hp<gunBefore'),p.evaluate('({before:gunBefore,hp:G.hp,shots:pBullets.length,weapon:run.weapon,held:Input.keys.j,player:{x:player.x,y:player.y},gun:roster17Mount(B,G),hits:HH.hits.slice(-5),opening:!!s6Opening,story:!!story})'))
   p.evaluate('''()=>{B._carrier17.direct=G.id;warhiveDamage(B,1e6);HH.shots=[];for(const p of B._carrier17.parts.filter(p=>p.kind==='gun')){p.phase='rest';p.cool=.1;} }''');frames(240)
   row=p.evaluate('''()=>({dead:G.dead,stopped:!HH.shots.some(s=>s.q._carrierHullGun===G.id),other:HH.shots.some(s=>s.q._carrierHullGun&&s.q._carrierHullGun!==G.id),removed:!retinaBossTargets(B).some(t=>t.name==='harrier '+G.id)})''')
   ck(diff+' destroyed native gun stops firing and leaves other guns active',all(row.values()),row)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True);sys.exit(bool(report['failed']))
