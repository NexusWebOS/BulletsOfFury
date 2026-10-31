from pathlib import Path
import sys,json,http.server,numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_storm_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));assert v,(n,d)
D=R/'assets/game/levels/stage_08/miniboss/herald_storm_1030';M=json.loads((D/'manifest.json').read_text());baseM=json.loads((R/'assets/game/levels/stage_08/miniboss/herald_chaos_1029/manifest.json').read_text())['tornado'];base=Image.open(R/baseM['path']).convert('RGBA')
def cell(im,a,f):return im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],f%a['cols']*a['cw']+a['cw'],f//a['cols']*a['ch']+a['ch']))
ims={n:Image.open(R/a['path']).convert('RGBA')for n,a in M.items()}
ck('All new art has even fixed cells and shared source pivots',all(a['cw']%2==a['ch']%2==0 and max(ims[n].size)<=4096 for n,a in M.items())and all(M[n]['pivot']==baseM['pivot']for n in ['arrive','depart','flash']))
arr=[np.asarray(cell(ims['arrive'],M['arrive'],i))for i in range(8)];out=[np.asarray(cell(ims['depart'],M['depart'],i))for i in range(8)]
ck('Eight incoming frames gain stored alpha and outgoing frames finish completely clear',arr[0][:,:,3].max()<40 and arr[-1][:,:,3].max()==255 and out[-1][:,:,3].max()==0)
ck('Every1015 lightning frame preserves the exact original tornado alpha',all(np.array_equal(np.asarray(cell(ims['flash'],M['flash'],level*16+f))[:,:,3],np.asarray(cell(base,baseM,f))[:,:,3])for level in range(3)for f in range(16)))
bright=0
for f in range(16):
 a=np.asarray(cell(base,baseM,f)).astype('int16');b=np.asarray(cell(ims['flash'],M['flash'],32+f)).astype('int16');bright+=int(np.sum((b[:,:,1]>220)&(b[:,:,2]>220)&(a[:,:,1]<150)&(a[:,:,3]>0)))
ck('Flash bank adds white-core lightning inside actual red funnel pixels',bright>100,bright)
ck('Warning graphic is the approved metal sign, not the plain impact star',ims['warning'].tobytes()==Image.open(R/'assets/game/levels/stage_09/boss/tidal_sovereign_1029/wall_warning.png').convert('RGBA').tobytes())
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;HH52.events=[];pBullets=[];eBullets=[];hr28Start(B,'storm');}")
  ck('Native entry finishes before the storm fixture',advance(p,'!B.enter',240,1))
  p.evaluate("()=>{HH52.events=[];hr28Start(B,'storm')}")
  ck('Storm art preloads before summoning',p.evaluate('Object.values(HH69_ART).every(a=>XART.rdy(a.key))'))
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  def draws():return p.evaluate('''()=>{const f=combatWarningDraw,h=hh69Blit,o=hh52Blit,fields=[],art=[];combatWarningDraw=function(o,a){fields.push(a)};hh69Blit=function(...a){art.push(a);return h.apply(this,a)};hh52Blit=function(...a){art.push(a);return o.apply(this,a)};try{heraldDeathDraw(B)}finally{combatWarningDraw=f;hh69Blit=h;hh52Blit=o}return{fields,art};}''')
  step(30);q=draws();ck('Charge uses a real metal warning and forming red bolt, with no storm FOV',not q['fields']and any(a[0]=='warning'and a[1]==0 for a in q['art'])and any(a[0]=='summon'for a in q['art'])and not any(a[0]=='star'for a in q['art']),q)
  p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'storm-summon.png'))
  step(78);q=draws();ck('Tornadoes materialize through actual incoming frames before they can attack',len([a for a in q['art']if a[0]=='arrive'])==2 and not p.evaluate('eBullets.some(q=>q._hh69Storm)'),q)
  p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/'storm-fade-in.png'))
  ck('Native first orb volley releases',advance(p,"HH52.events.some(e=>e.event==='tornado-volley')",60,1))
  q=draws();shots=p.evaluate('eBullets.filter(q=>q._hh69Storm).map(q=>({lightning:q._hh52Lightning,intercept:enemyOrdnanceCanIntercept(q),w:q.w,h:q.h}))')
  ck('Storm volleys are actual red lightning orbs with native ordinary-energy rules',len(shots)==12 and all(v['lightning']and not v['intercept']and v['w']==12 and v['h']==12 for v in shots),shots[:2])
  ck('Emitting funnel selects an internal-lightning1015 flash on that exact beat',any(a[0]=='flash'and a[1]>=32 for a in q['art'])and p.evaluate('HH52.events.filter(e=>e.event==="tornado-volley").at(-1).flash'),q)
  p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/'storm-orb-flash.png'))
  orb=p.evaluate('''()=>{const q=eBullets.find(q=>q._hh69Storm),n=ctx.drawImage;let calls=[];ctx.drawImage=function(im,...a){if(im===XART.get(HH52_ART.lightning_ball.key))calls.push(a);return n.apply(this,[im,...a])};try{drawCombatFinalProjectile(q)}finally{ctx.drawImage=n}return calls;}''')
  ck('Native projectile renderer uses the44px animated lightning-ball bank',len(orb)==1 and orb[0][-2:]==[44,44],orb)
  e=p.evaluate('HH52.events.filter(e=>e.event==="storm-summon-bolt")');ck('Summoning lightning cadence accelerates before release',len(e)>=6 and e[0]['gap']>e[-1]['gap']*2,dict(beats=len(e),first=e[0]['gap'],last=e[-1]['gap']))
  step(14);q=draws();ck('Volley flash returns to the normal funnel between releases',not any(a[0]=='flash'for a in q['art'])and len([a for a in q['art']if a[0]=='tornado'])==2,q)
  ck('Native storm reaches recovery',advance(p,"hh52Special(B)?.kind==='storm'&&hh52Special(B).phase==='recover'",450,1));step(6);q=draws();ck('Both funnels fade out through authored departing frames',len([a for a in q['art']if a[0]=='depart'])==2 and not any(a[0]in ['flash','tornado']for a in q['art']),q)
  p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/'storm-fade-out.png'));step(20);q=draws();ck('Tornado art ends before the finite native recovery completes',not any(a[0]in ['arrive','depart','flash','tornado','summon']for a in q['art']))
  step(65);ck('Native attack book resumes after the storm',p.evaluate('!hh52Special(B)||hh52Special(B).kind!=="storm"'))
  ck('Native pressure cap remains bounded',p.evaluate('eBullets.filter(q=>q._heraldOwner1003===B&&!q.dead).length<=128'))
  p.evaluate("()=>{hr28Start(B,'storm');B.dead=true}");q=draws();ck('Boss death cancels pending summon and tornado graphics',not any(a[0]in ['arrive','depart','flash','tornado','summon','warning']for a in q['art']))
  ck('Dual red lasers and animated bottom Retinas stay registered',p.evaluate('typeof HL67!=="undefined"&&XART.rdy(HL51_ART.key)'))
  ck('No native game/draw/console errors',not errors,errors);(W/'storm-events.json').write_text(json.dumps(e,indent=2));br.close()
finally:stop()
print(len(checks),'Herald storm checks passed')
