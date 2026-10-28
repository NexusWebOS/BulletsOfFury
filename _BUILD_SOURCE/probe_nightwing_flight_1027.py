from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,numpy as np,base64,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/nightwing_flight_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];console=[];http=[]
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors,'console':console,'http':http},indent=2),encoding='utf-8');assert v,name
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof NF29!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  def setup(diff):
   p.evaluate("d=>{diffKey=d;run.ngplus=false;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];}",diff)
  for diff,count in [('easy',0),('normal',0),('hard',2),('furious',5)]:
   setup(diff);step(620);p.wait_for_timeout(600);step(1)
   q=p.evaluate("()=>({cap:boss._whv.jetN,alive:whvJetsAlive(boss._whv),slots:boss._whv.jets.map(e=>e._hwSlot),bay:s6r18State(boss).bay.mode,model:boss._whv.jets.map(e=>bf22Model(e).id)})")
   check(diff+' native bay launches exactly '+str(count)+' royal helpers',q['alive']==count and q['cap']==count and all(v=='royal_harrier_escort'for v in q['model']),q)
   p.evaluate('()=>{for(let i=0;i<12;i++)whvLaunchJet(boss)}');check(diff+' repeated spawn calls cannot exceed the cap',p.evaluate('whvJetsAlive(boss._whv)')==count)
   if count:
    p.screenshot(path=str(W/(diff+'-escorts.png')))
    p.evaluate('()=>{const e=boss._whv.jets[0];e.dead=true;e.hp=0;e._dyingT=0;whvLaunchJet(boss)}');check(diff+' replacement fills a vacant slot without exceeding cap',p.evaluate('whvJetsAlive(boss._whv)')==count)
   else:check(diff+' bay stays closed without announcing incoming helpers',q['bay']=='wait')
  check('Shared Stage6 sky enemies keep their original model',p.evaluate("bf22Model({type:'s6bomber'}).id==='sky_stratus'"))
  p.evaluate('()=>{delete boss._carrier17;boss._whv.mode="ace";boss._whv.jets=[];enemies=[];whvAceSpawn(boss);s6Wing.ships=[];}')
  entries=[]
  for i in range(440):
   step(1)
   if i%8==0:entries.append(p.evaluate('()=>({mode:boss._whv.ace._nw28.mode,x:boss.x,y:boss.y,pose:boss._whv.ace._nf29Pose,protected:whvAceInvuln(boss._whv.ace)})'))
   if p.evaluate('boss._whv.ace._nw28.mode==="fight"'):break
  north=[x for x in entries if x['mode']=='north'];ret=[x for x in entries if x['mode']=='return']
  check('Corner entrance bends laterally and changes authored headings',len({q['pose']['frame']for q in north if q.get('pose')})>=3 and max(q['x']for q in north)-min(q['x']for q in north)>60,entries)
  check('Intro remains protected until the whole ship settles',all(q['protected']for q in entries if q['mode']!='fight'))
  check('Curved entrance returns to native fight with one HP pool',p.evaluate('boss._whv.ace.st==="fight"&&!boss.modular&&!boss._noHit'))
  # Controlled fixture starts the native charge decision; subsequent phases are
  # stepped through the production owner, not authored video or HP manipulation.
  p.evaluate("()=>{const A=boss._whv.ace;A._ra7Gate=A._pw5Gun=A.desp=A.roll=A.somer=null;A.inverted=false;A.dash={st:'warn',t:0,x0:A.x,y0:A.y};boss.hp=boss.maxhp*.8;player.x=camLeftX()+viewW()*.4;player.y=VH-70;NF29.events=[];}")
  stages={};timeline=[]
  for i in range(600):
   step(1)
   q=p.evaluate('()=>{const A=boss._whv.ace;return{phase:A.dash?.st||"done",x:A.x,y:A.y,w:boss.w,h:boss.h,pose:A._nf29Pose,hidden:nf29Hidden(A),hp:boss.hp}}')
   timeline.append(q)
   if q['phase']not in stages and q['phase']!='done':stages[q['phase']]=q
   if q['phase']in ['flyover','drift','approach']and i%10==0:p.screenshot(path=str(W/(q['phase']+'.png')))
   if q['phase']=='done':break
  (W/'flight-timeline.json').write_text(json.dumps(timeline,indent=2),encoding='utf-8')
  check('Charge actually leaves the screen before its large northbound pass',set(['warn','go','offscreen','flyover_warn','flyover','drift','approach','done']).issubset(set(q['phase']for q in timeline)),list(stages))
  fly=[q for q in timeline if q['phase']=='flyover'and q.get('pose')and q['pose']['bank']=='flyover'];drift=[q for q in timeline if q['phase']=='drift'and q.get('pose')and q['pose']['bank'].startswith('drift_')]
  check('Flyover is large, moves north and has a paired authored shadow',fly[0]['y']>fly[-1]['y']and fly[0]['pose']['scale']==1.6 and p.evaluate('!!NF29_ART.banks.flyover_shadow'))
  check('Drift uses many rotated frames while shrinking continuously',len({q['pose']['frame']for q in drift})>=20 and drift[0]['pose']['scale']>1.5 and drift[-1]['pose']['scale']<.7)
  check('Flight restores original body dimensions and foreground vulnerability',p.evaluate('boss.w===184&&boss.h===192&&!boss._noHit&&!whvAceInvuln(boss._whv.ace)'))
  # Native whole-ship renderer pixel proof for regular bank, large flyover,
  # shrinking bank and foreground return. Actual hitBoss must consume HP first.
  pixels=[]
  for name,pose in [('idle',None),('bank',{'bank':'heading','frame':71,'scale':1}),('flyover',{'bank':'flyover','frame':3,'scale':1.6}),('drift',{'bank':'drift_right','frame':8,'scale':1.3}),('return',{'bank':'approach','frame':15,'scale':1})]:
   q=p.evaluate('''([name,pose])=>{const b=boss,A=b._whv.ace;A.dash=A.roll=A.somer=A.desp=A._ra7Gate=A._pw5Gun=null;A.inverted=false;A.vx=name==='bank'?200:0;A.x=camLeftX()+viewW()/2;A.y=viewTopY()+viewH()/2;A._nf29Pose=pose;b._noHit=false;b.flash=0;b._gp4FlashNext=0;nf29Sync(b);const hp=b.hp;hitBoss(1,'bullet');const after=b.hp,flash=b.flash;
    function draw(){ctx.clearRect(0,0,cv.width,cv.height);nw28DrawBody(b);return Array.from(ctx.getImageData(Math.round(A.x)-220,Math.round(A.y)-220,440,440).data)}
    const hit=draw();b.flash=0;const normal=draw();let opaque=0,white=0,changed=0;for(let i=0;i<hit.length;i+=4)if(Math.max(hit[i],hit[i+1],hit[i+2])>25){opaque++;if(Math.max(hit[i],hit[i+1],hit[i+2])-Math.min(hit[i],hit[i+1],hit[i+2])<2)white++;if(hit[i]!==normal[i]||hit[i+1]!==normal[i+1]||hit[i+2]!==normal[i+2])changed++;}return{name,hp,after,flash,opaque,white,changed,key:NF29.last?.key||NW28.last?.key};}''',[name,pose]);pixels.append(q)
   check(name+' accepted damage visibly whites the complete current pose and expires',q['after']<q['hp']and q['flash']>0 and q['white']>q['opaque']*.95 and q['changed']>q['opaque']*.8,q)
  p.evaluate('()=>{boss.flash=.16;}');step(16);check('Native hit-flash timer expires during movement',p.evaluate('boss.flash<=0'))
  q=p.evaluate('''()=>{const A=boss._whv.ace;A.roll=A.somer=A.dash=A.desp=null;A._nf29Pose={bank:'flyover',frame:3,scale:1.6};let inside=0;for(let y=-140;y<=140;y+=20)for(let x=-140;x<=140;x+=20)if(warhiveHitTest(boss,A.x+x,A.y+y))inside++;return{inside,outside:warhiveHitTest(boss,A.x+210,A.y+210)};}''');check('Large flyover collision uses its actual whole silhouette',q['inside']>40 and not q['outside'],q)
  p.evaluate("()=>{const A=boss._whv.ace;A.dash={_nf29:true,st:'approach'};A._nf29Pose={bank:'approach',frame:0,scale:.65};}");q=p.evaluate('()=>{const hp=boss.hp;hitBoss(50,"bullet");return{same:boss.hp===hp,targets:retinaBossTargets(boss).length}}');check('Background scale rejects bullets and Retina until foreground return',q['same']and q['targets']==0,q)
  for furious in [True,False]:
   p.evaluate('''fur=>{boss._whv.fur=fur;boss.hp=boss.maxhp*.45;const A=boss._whv.ace;A.dash={_nf29:true,st:'approach',t:.719,from:{x:A.x,y:A.y},second:false};A.desp=A.roll=A.somer=null;A._nf29Pose={bank:'approach',frame:15,scale:1};}''',furious);step(1)
   check(('Furious preserves the second fully warned charge below half HP'if furious else'Hard completes one charge without an extra pass'),p.evaluate('!!boss._whv.ace.dash?.second&&boss._whv.ace.dash.st==="warn"')if furious else p.evaluate('!boss._whv.ace.dash'))
  check('No page, draw or HTTP errors',not errors and not console and not http,{'page':errors,'console':console,'http':http});br.close()
finally:stop()
print(f'{len(checks)} native checks passed')
