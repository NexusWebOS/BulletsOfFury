"""Native orbital roles, current pixels, birth interception and cleanup."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage5_amplify_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'final-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
SETUP='''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;S511.events=[];S511.fx=[];S511.mines.clear();player.invuln=40002;playerLocks=[];return {type:E.type,hp:E.hp,x:E.x,y:E.y,shield:E._esh?.max||0};}'''
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(5,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&Object.values(S511_ART.banks).every(B=>XART.rdy(B.key))&&Object.values(S511_ART.models).every(m=>XART.rdy(m.bank.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 specs=json.loads((R/'_shots/enemy_flight_1031/before/stage5-specs.json').read_text());types=['s5frigate','s5rammer','s5skimmer','s5gravity','s5minelayer','s5satellite','s5portalmine','s5repair','s5station','s5leech']
 p.evaluate('''()=>{window.orbitalPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return {white,color};};}''')
 # New1015 companion is read by the native projectile renderer at six steps.
 q=p.evaluate('''()=>{const samples=[];for(const t of[.02,.02+4/22,.02+8/22]){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);s511Projectile({_s511Kind:'orb',t,x:300,y:200,vx:0,vy:1});ctx.restore();const a=ctx.getImageData(250,150,100,100).data;let light=0;for(let i=0;i<a.length;i+=4)light+=a[i]+a[i+1]+a[i+2];samples.push({frame:Math.floor(t*22)%4,step:pxgStep(.5+.5*Math.sin(t*9)),light});}return samples;}''')
 ck('Same plasma frame has source-pixel1015 brightness steps',len({x['frame']for x in q})==1 and len({x['step']for x in q})==3 and len({x['light']for x in q})==3,q)
 # Freeze only the sampler camera for evidence; attack clocks remain native.
 for typ in['s5frigate','s5repair','s5station']:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ));q=p.evaluate('''()=>{for(let i=0;i<1000;i++){updatePlay(1/60);if(E._s511.beams.length)break;}drawWorld(0);return {phase:E._s511.phase,beams:E._s511.beams.length,key:E._s511Rendered?.key};}''');ck(typ+' current beam pixels captured',q['beams']>0 and q['key'],q);p.screenshot(path=str(O/(typ+'-current-beam.png')))
 # Leech's actual connected claw contact reaches the native playerHit path.
 p.evaluate(SETUP,next(s for s in specs if s['type']=='s5leech'))
 q=p.evaluate('''()=>{for(let i=0;i<900;i++){updatePlay(1/60);if(E._s511.phase==='pounce')break;}const p=s511Point(E,'centre');player.x=p.x;player.y=p.y;player.invuln=0;player.roll=player.somer=0;DBGT.god=false;const lives=run.lives;updatePlay(1/60);return {lives,after:run.lives,dead:player.dead,invuln:player.invuln,events:S511.events.filter(e=>e.event==='claw-contact'),shots:S511.events.filter(e=>e.event==='shot').length};}''')
 ck('Connected Leech claws cause native player damage without shots',not q['shots']and(q['dead']or q['invuln']>0 or q['after']<q['lives']),q)
 # All campaign routes suppress the retired type, direct and difficulty factories.
 q=p.evaluate('''()=>{window.fixtureSpawn=true;const results=[];for(const stage of[4,5,7,9]){run.stage=stage;results.push(spawnEnemy('xelite_voidreaver',worldWidth()/2,-80));}run.stage=5;window.fixtureSpawn=false;return {suppressed:results.every(e=>e==null),aceTables:Object.values(DIFFICULTY_ELITE_STAGE).every(a=>!a.includes('voidreaver'))};}''');ck('Voidreaver absent from every active stage/factory',q['suppressed']and q['aceTables'],q)
 ck('No native page/console errors',not errors,errors);b.close()
(O/'final-errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
