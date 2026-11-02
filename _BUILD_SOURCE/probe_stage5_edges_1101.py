"""Native orbital roles, current pixels, birth interception and cleanup."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage5_amplify_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'edge-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
SETUP='''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;S511.events=[];S511.fx=[];S511.mines.clear();player.invuln=40002;playerLocks=[];return {type:E.type,hp:E.hp,x:E.x,y:E.y,shield:E._esh?.max||0};}'''
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(5,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&Object.values(S511_ART.banks).every(B=>XART.rdy(B.key))&&Object.values(S511_ART.models).every(m=>XART.rdy(m.bank.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 specs=json.loads((R/'_shots/enemy_flight_1031/before/stage5-specs.json').read_text());types=['s5frigate','s5rammer','s5skimmer','s5gravity','s5minelayer','s5satellite','s5portalmine','s5repair','s5station','s5leech']
 p.evaluate('''()=>{window.orbitalPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return {white,color};};}''')
 # All weapon mouth samples must meet the visible source alpha, every direction.
 for typ in types:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ))
  q=p.evaluate('''()=>{for(let i=0;i<70;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const before=E.hp,s=E._esh;let shield=false;if(s){const en=s.energy;hitEnemy(E,1);shield=E.hp===before&&s.energy<en;hitEnemy(E,s.max+5);for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;}const clean=orbitalPixels();const hp=E.hp;hitEnemy(E,.02);const hit=orbitalPixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return {before,hp,after:E.hp,clean,hit,expired:orbitalPixels(),flash:E.flash,shield};}''')
  ck(typ+' actual native damage pixels expire',q['after']<q['hp']and q['hit']['white']>q['clean']['white']+15 and q['expired']['white']<q['hit']['white']and q['flash']<=0,q)
  if typ in['s5station','s5frigate','s5leech']:ck(typ+' native shield absorbs before hull',q['shield'],q)
 # Exact warning/beam sharing and source-alpha calibration, real renderer pixels.
 for typ in['s5frigate','s5repair','s5station']:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ))
  q=p.evaluate('''()=>{for(let i=0;i<1200;i++){updatePlay(1/60);if(E._s511.beams.length)break;}const A=E._s511,b=A.beams[0],p=b?.p;const src=S511_ART.banks.laser,im=XART.get(src.key),c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d');g.drawImage(im,0,0,64,64,0,0,64,64);const z=g.getImageData(0,0,64,64).data;let min=64,max=-1;for(let y=0;y<64;y++)for(let x=0;x<64;x++)if(z[(y*64+x)*4+3]>0){min=Math.min(min,x);max=Math.max(max,x);}const event=S511.events.find(e=>e.event==='beam-release');return {p,sourceAlphaWidth:max-min+1,same:event?.lanes.some(q=>Math.abs(q.x-p.x)<.1&&Math.abs(q.width-p.width)<.1),on:p&&ep13BeamTouches({x:p.x,y:p.y,a:p.angle,width:p.width,len:1200,active:true},{x:p.x,y:p.y+100}),off:p&&ep13BeamTouches({x:p.x,y:p.y,a:p.angle,width:p.width,len:1200,active:true},{x:p.x+p.width,y:p.y+100})};}''')
  ck(typ+' beam starts at warned socket and contact fits alpha',q['sourceAlphaWidth']==18 and q['same']and q['on']and not q['off'],q)
  p.screenshot(path=str(O/(typ+'-current-beam.png')))
 # A dropped mine is genuinely destroyed by the pilot's ordinary primary fire.
 p.evaluate(SETUP,next(s for s in specs if s['type']=='s5minelayer'))
 q=p.evaluate('''()=>{for(let i=0;i<240;i++){updatePlay(1/60);if(S511.mines.size)break;}const b=[...S511.mines][0];E._s511.cd=999;const before=b?.hp;player.x=b.x;player.y=b.y+120;Input.keys.j=true;for(let i=0;i<180&&!b.dead;i++)updatePlay(1/60);Input.keys.j=false;return {before,dead:b.dead,hp:b.hp,t:b.t,events:S511.events.filter(e=>e.event==='mine-intercepted')};}''')
 ck('Mine can be destroyed by actual player gunfire',q['dead']and q['t']<7.8 and len(q['events'])==1,q)
 # Real contact detonates a mine and reaches the native player hit owner.
 p.evaluate(SETUP,next(s for s in specs if s['type']=='s5minelayer'))
 q=p.evaluate('''()=>{for(let i=0;i<240;i++){updatePlay(1/60);if(S511.mines.size)break;}const b=[...S511.mines][0];while(b.t<.7)updatePlay(1/60);player.x=b.x+30;player.y=b.y;player.invuln=0;DBGT.god=false;const before=run.lives;for(let i=0;i<6;i++)updatePlay(1/60);return {dead:player.dead,invuln:player.invuln,before,after:run.lives,events:S511.events.filter(e=>e.event==='mine-detonated')};}''')
 ck('Mine proximity has explosion and native player damage',len(q['events'])==1 and(q['dead']or q['invuln']>0 or q['after']<q['before']),q)
 # True defeat cancels pending lock callbacks and beams, preserving native death.
 for typ in['s5satellite','s5frigate']:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ))
  q=p.evaluate('''()=>{for(let i=0;i<600;i++){updatePlay(1/60);if(playerLocks.some(L=>L.src===E)||E._s511.beams.length)break;}for(let k=0;k<4&&!E.dead&&E._dyingT==null;k++)hitEnemy(E,99999);const n=S511.events.filter(e=>e.event==='shot').length;for(let i=0;i<150;i++)updatePlay(1/60);return {before:n,after:S511.events.filter(e=>e.event==='shot').length,beams:E._s511.beams.length,locks:playerLocks.filter(L=>L.src===E).length,death:!!E._deathFxStarted};}''')
  ck(typ+' death cancels attacks and retains native effects',q['before']==q['after']and not q['beams']and not q['locks']and q['death'],q)
 ck('No native page/console errors',not errors,errors);b.close()
(O/'edge-errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
