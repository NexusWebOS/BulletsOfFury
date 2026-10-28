"""Real Chromium coverage through shoot.py. Explicit fixtures are recorded as such.
Actual canvas differences verify connected arms, liquid motion and hit flashes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_lunge_1028/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];trails=[]
def ck(name,value,data=None):
 checks.append({'name':name,'passed':bool(value),'data':data});print(('PASS 'if value else'FAIL ')+name,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  def page(stage):
   p=bc.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WT25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("n=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(n,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(n,'boss').kind);debugFight.spawned=true;bossActive=true;warnT=0;BOFCinematicDirector.cancel();DBGT.god=true;run.lives=3;player.dead=false;player.invuln=1e9;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",stage)
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   return p
  def shot(p,name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p=page(7)
  p.evaluate("()=>{s7mWarm();r25Warm(7);bm9Warm(bm9StageNames(7));window.wt7Setup=(mode,x,y)=>{const b=boss,M=s7mInit(b);b.enter=false;b.x=x;b.y=y;b._drawY=y;M.height=M.drop=M.lean=0;M._mission29IntroDone=true;M.r25Gait=null;M.counterTell=null;M.frExit=null;s7mSet(b,mode);for(const q of M.parts)q.hp=q.max;player.x=worldWidth()/2;player.y=VH-55;};wt7Setup('recover',worldWidth()/2,175);}")
  p.wait_for_function('r25Warm(7)&&bm9StageNames(7).every(n=>BM9_ART[n].every(a=>XART.rdy(a.key)))',timeout=180000)
  p.wait_for_function("()=>Object.values(WL39_ART).every(a=>XART.rdy(a.key))")
  ck('Native body and health budget retained',p.evaluate("()=>{const b=boss,M=b._s7mod;return b.hp===M.core+M.shield+M.parts.reduce((n,q)=>n+q.hp,0);}"))
  q=p.evaluate("""()=>{wt7Setup('swipeX',worldWidth()/2,235);const b=boss,M=b._s7mod,start=b.y,rows=[];eBullets=[];window.wlBeforeBlocks=DBGT.stats.godBlocks;for(let i=0;i<105;i++){s7mTick(b,1/60);const pose=s7mPose(b);rows.push({t:M.t,mode:M.mode,y:b.y,legs:pose.filter(p=>p.wl39).map(p=>({id:p.id,f:p.frame,stance:p.stance,world:s7mWorld(b,p.toe)})),claws:pose.filter(p=>p.id.startsWith('front')).map(p=>({id:p.id,...s7mWorld(b,p.toe)}))});}window.wlRows=rows;return {start,max:Math.max(...rows.map(q=>q.y)),hit:DBGT.stats.godBlocks-wlBeforeBlocks,rows};}""")
  ck('Rear drive moves the chassis into real melee range',q['max']-q['start']>100,q['max']-q['start']);ck('Native swept claw contact actually reaches the stationary player',q['hit']>0,q['hit'])
  ck('Rear source frames visibly brace and extend',len(set(x['f'] for row in q['rows'] for x in row['legs']))>=20)
  pins=[]
  for a,z in zip(q['rows'],q['rows'][1:]):
   for x in a['legs']:
    y=next((y for y in z['legs'] if y['id']==x['id']),None)
    if y and x['stance'] and y['stance']:pins.append(abs(y['world']['y']-x['world']['y']))
  ck('Rear feet plant through the main push',pins and max(pins)<6,dict(samples=len(pins),max=max(pins,default=999)))
  ck('Swat emits no bullets and does not scroll the floor',p.evaluate('eBullets.length===0&&s7WardenReverseScroll()===0'))
  for t,name in [(0.65,'brace'),(1.18,'rear-push'),(1.38,'claw-contact'),(1.9,'recovery')]:
   p.evaluate("t=>{wt7Setup('swipeX',worldWidth()/2,235);for(let i=0;i<Math.ceil(t*60);i++)s7mTick(boss,1/60);}",t);shot(p,name)
  ck('Strike has finite recovery to the original ground position',p.evaluate("()=>{wt7Setup('swipeX',worldWidth()/2,235);for(let i=0;i<145;i++)s7mTick(boss,1/60);return boss._s7mod.mode==='recover'&&Math.abs(boss.y-235)<1;}"))
  ck('Escaping after commitment avoids the real claw path',p.evaluate("()=>{wt7Setup('swipeX',worldWidth()/2,235);for(let i=0;i<48;i++)s7mTick(boss,1/60);player.x=camRightX()-15;const n=DBGT.stats.godBlocks;for(let i=0;i<65;i++)s7mTick(boss,1/60);return DBGT.stats.godBlocks===n;}"))
  q=p.evaluate("""()=>{wt7Setup('swipeX',worldWidth()/2,235);for(let i=0;i<68;i++)s7mTick(boss,1/60);const out=[];for(const v of s7mPose(boss).filter(p=>p.wl39)){const a=s7mWorld(boss,v.target);out.push({id:v.id,at:s7mAt(boss,a.x,a.y)});}return out;}""")
  ck('Rear Retina target overlaps the rendered alpha in the push pose',all(x['at']==x['id'] for x in q),q)
  q=p.evaluate("""()=>{const b=boss,M=b._s7mod;wt7Setup('swipeX',worldWidth()/2,235);s7mTick(b,.3);const part=M.parts.find(p=>p.id==='frontL');function whites(){drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]>240&&a[i+1]>240&&a[i+2]>240&&a[i+3]>80)n++;return n;}const base=whites(),hp=part.hp;s7mHit(b,1,0,0,'frontL');const hit=whites();for(let i=0;i<18;i++)s7mTick(b,1/60);return{base,hit,end:whites(),hp:part.hp,before:hp,flash:part.flash};}""")
  ck('Actual claw damage flashes native white pixels then expires',q['hp']<q['before']and q['hit']>q['base']+50 and q['end']<q['hit']and q['flash']<=0,q)
  q=p.evaluate("""()=>{wt7Setup('recover',worldWidth()/2,235);eBullets=[];s7mVolley(boss,9,Math.PI/2,.2,3);s7mWaves(boss,1);s7mShot(boss,boss.x,boss.y+26,Math.PI/2,3,'acid');const suppressed=eBullets.length===0;s7mSet(boss,'er28-core-burst');const mapped=boss._s7mod.mode;sw28Slug(boss,'gunL');sw28Slug(boss,'gunR');const guns=eBullets.filter(q=>q._er28Slug).length;const A=boss._s7mod.er28;A.target={x:player.x,y:player.y};sw28Mortars(boss);return{suppressed,mapped,guns,mortars:SW28.mortars.length,barrage:bh25Start(boss,'warden',()=>{})};}""")
  ck('Face volleys, acid rounds and face bullet hell are retired',q['suppressed'] and q['mapped']=='er28-mortar'and q['barrage']is False,q)
  ck('Both native turrets and dorsal mortars still launch',q['guns']==2 and q['mortars']>=3,q)
  q=p.evaluate("""()=>{explosions=[];WL39.base.toxic(100,100,120,0);const original=explosions[0].dur;explosions=[];fr27ToxicExplosion(100,100,120,0);return{original,now:explosions[0].dur};}""")
  ck('Toxic explosion frames play faster',abs(q['now']/q['original']-.62)<.001,q)
  q=p.evaluate("""()=>{wt7Setup('dead',worldWidth()/2,235);window.wlExitBoss=boss;for(let i=0;i<175;i++)fr27Exit(boss,1/60);const E=boss._s7mod.frExit,serial=E.serial;explosions=[];for(let i=0;i<30;i++)fr27Exit(boss,1/60);window.wlPortalE=E;return{serial:E.serial-serial,live:explosions.filter(e=>e._wl39Toxic).length,t:E.t,finite:explosions.every(e=>Number.isFinite(e.x+e.y))};}""")
  ck('Portal approach has a rapid dense explosion cadence',q['serial']>=20 and q['live']<=66 and q['finite'],q);shot(p,'portal-explosions')
  q=p.evaluate("()=>{const E=wlPortalE,b=wlExitBoss;for(let i=0;i<650;i++)if(!b.dead)fr27Exit(b,1/60);return {t:E.t,end:E.entry.goneAt+7.6,finished:b._s7warden.final.finished,dead:b.dead};}")
  ck('Native portal and finale clocks remain unchanged',q['finished']and q['dead']and abs(q['t']-q['end'])<.03,q)
  ck('No page or console errors',not errors,errors)
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,events=p.evaluate('WL39.events')),indent=2),encoding='utf8')
  br.close()
finally:stop()
assert all(c['passed']for c in checks)
