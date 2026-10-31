from pathlib import Path
import sys,json,http.server,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/order_phoenix_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));checks=[];errors=[];states=[]
def ck(name,v):
 checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
SETUP="""cfg=>{diffKey=cfg.rank||'furious';spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,2);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.arenaPhase=2;B.x=340;B.y=174;B._r30.v18.home={x:340,y:174};window.Q=ph21State(B);Q.cool=0;Q.action=null;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;player.x=340;player.y=VH-65;DBGT.god=true;pBullets=[];eBullets=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;for(const id of ['cannonL','cannonR']){B._lastPart=ph21Part(B,id);modularHit(ph21Part(B,id).hp);}Q.cool=0;ph83State(B).seed=cfg.seed||11;for(const i of V18.forms)if(i!==2)j3State(B).hp[i]=0;PH83.events=[];window.P=ph83Start(B);}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.evaluate(SETUP,{});seen=set();positions=[];last=None
  for i in range(2600):
   p.evaluate(STEP,1)
   s=p.evaluate('({phase:P.phase,x:B.x,y:B.y,t:P.t,depth:P.depth,bank:P.bank,frame:P.frame,hp:B.hp,count:P.count,sent:P.sent,live:P.echoes.length,events:PH83.events.length})')
   positions.append(s)
   if s['phase']not in seen:
    seen.add(s['phase']);print('PHASE',i,s,flush=True);p.screenshot(path=str(W/('native-'+s['phase']+'.png')))
   if s['phase']=='barrage'and s['sent']==4 and s['t']>2.1 and 'bigEcho'not in seen:
    seen.add('bigEcho');p.screenshot(path=str(W/'native-barrage-large.png'))
   if s['phase']=='twist'and s['t']>.38 and 'midTwist'not in seen:
    seen.add('midTwist');p.screenshot(path=str(W/'native-twist-volume.png'))
   if s['phase']=='return'and s['t']>.75 and 'midReturn'not in seen:
    seen.add('midReturn');p.screenshot(path=str(W/'native-return-volume.png'))
   if p.evaluate('PH83.events.some(e=>e.event==="order-complete")'):break
  ev=p.evaluate('PH83.events');states.append({'first':positions,'events':ev});releases=[e for e in ev if e['event']=='corner-release'];charge=[e for e in ev if e['event']=='order-charge'];launches=[e for e in ev if e['event']=='phoenix-launch']
  ck('Four unique committed corner rushes complete before the new cast',len(releases)==4 and len(set(e['corner']for e in releases))==4)
  ck('New background turn and charge complete with eight to twelve launches',len(charge)==1 and 8<=len(launches)<=12 and len(launches)==charge[0]['count'])
  ck('Charge-down, offscreen exit, returning roll and vulnerable recovery complete',all(q in seen for q in ['cooldown','exitTwist','exit','return','recover'])and any(e['event']=='order-complete'for e in ev))
  ck('Post-pod HP stays at native2624 with no healing',all(s['hp']==2624 for s in positions))
  ck('No frame-to-frame teleport anywhere in the full sequence',max(((b['x']-a['x'])**2+(b['y']-a['y'])**2)**.5 for a,b in zip(positions,positions[1:]))<34)
  ck('No more than four giant silhouettes are active together',max(s['live']for s in positions)<=4)
  ck('Background approach and turn use small real-volume source banks',all(s['depth']<=.41 for s in positions if s['phase']in ['approach','twist','charge','barrage']))
  ck('RNG bags visit each corner once and never repeat the previous ending',p.evaluate('()=>{let good=true;for(let seed=1;seed<101;seed++){const s={seed,lastCorner:-1};let last=-1;for(let n=0;n<20;n++){const q=ph83Bag(s);good&&=new Set(q).size===4&&q[0]!==last;last=q[3];}}return good;}'))
  ck('No native page, draw or missing-asset errors',not errors)
  br.close()
finally:stop()
(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
