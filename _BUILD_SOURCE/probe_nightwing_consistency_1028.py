from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys,math,numpy as np,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_consistency_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,n
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text());images={k:Image.open(R/a['path']).convert('RGBA')for k,a in M['banks'].items()}
def cell(k,f):
 a=M['banks'][k];return images[k].crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],f%a['cols']*a['cw']+a['cw'],f//a['cols']*a['ch']+a['ch']))
old=Image.open(R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/whole.png').convert('RGBA');canonical=cell('whole',0)
ck('Regular teal aircraft and royal cockpit are pixel-identical to the existing design',canonical.tobytes()==old.crop((0,0,272,272)).tobytes())
ck('Bank, roll and pitch now use the canonical aircraft rather than Part2 art','part2_art_1010'not in (R/'_ART_SOURCES/nightwing_wind_1028/build.py').read_text() and cell('whole',17).tobytes()==canonical.tobytes()and cell('whole',33).tobytes()==canonical.tobytes())
ck('The inverted view retains exactly the canonical wing planform',cell('whole',16).getchannel('A').tobytes()==canonical.getchannel('A').tobytes())
body=[k for k,a in M['banks'].items()if '_identity_1028b' in a['path']]
ck('All rebuilt textures have even fixed cells and fit4096px',all(a['cw']%2==a['ch']%2==0 and max(images[k].size)<=4096 for k,a in M['banks'].items()))
ck('Every rebuilt body, hit and shadow frame has transparent safety borders',all((lambda b,a:b is not None and b[0]>0 and b[1]>0 and b[2]<a['cw']and b[3]<a['ch'])(cell(k,f).getbbox(),M['banks'][k])for k in body for f in range(M['banks'][k]['frames'])))
for k in ['whole','heading','flyover','drift_left','drift_right','approach','clean']:
 ck(k+' white-hit masks match every actual pose silhouette',all(cell(k,f).getchannel('A').tobytes()==cell(k+'_hit',f).getchannel('A').tobytes()and np.all(np.array(cell(k+'_hit',f))[:,:,:3][np.array(cell(k+'_hit',f))[:,:,3]>0]==255)for f in range(M['banks'][k]['frames'])))
for k in ['flyover','drift_left','drift_right','approach']:
 ck(k+' shadow uses the same new planform and source alias',all(np.array_equal(np.rint(np.asarray(cell(k,f).getchannel('A'))*.32),np.asarray(cell(k+'_shadow',f).getchannel('A')))for f in range(M['banks'][k]['frames']))and M['aliases']['nf29_'+k+'_shadow']==k+'_shadow')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None);p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF);p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);}");p.evaluate(STEP,430)
  for name,config in [('cruise',{}),('bank',dict(vx=200)),('roll',dict(roll=dict(t=.055,dir=1))),('somer',dict(somer=dict(t=.08))),('inverted',dict(inverted=True)),('flyover',dict(pose=dict(bank='flyover',frame=3,scale=1.6))),('drift',dict(pose=dict(bank='drift_right',frame=8,scale=1.3))),('return',dict(pose=dict(bank='approach',frame=15,scale=1)))]:
   q=p.evaluate('''c=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A._nw28.mode='fight';A.st='fight';A.dash=A.desp=A.roll=A.somer=A._nf29Pose=null;A.inverted=false;A.vx=0;A.x=camLeftX()+viewW()/2;A.y=220;b._noHit=false;b.dead=false;b.flash=0;Object.assign(A,c);A._nf29Pose=c.pose||null;A.x=camLeftX()+viewW()/2;A.y=220;let calls=[];const draw=ctx.drawImage;ctx.drawImage=function(im,...a){for(const [k,v]of Object.entries(NW30_ART.banks))if(im===XART.get(v.key)){calls.push({bank:k,frame:Math.floor(a[1]/v.ch)*v.cols+Math.floor(a[0]/v.cw)});break;}return draw.apply(this,[im,...a]);};try{nw28DrawBody(b)}finally{ctx.drawImage=draw}return {calls,pose:nw30Pose(b)};}''',config)
   main=[c for c in q['calls']if c['bank']in ['whole','clean','heading','flyover','drift_right','approach']];ck(name+' native renderer uses exactly one source-locked hull',len(main)==1,q)
   p.evaluate('()=>{boss.x=boss._whv.ace.x;boss.y=boss._whv.ace.y;drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(name+'.png')))
   q=p.evaluate('''()=>{boss._gp4FlashNext=0;markHit(boss);let calls=[];const draw=ctx.drawImage;ctx.drawImage=function(im,...a){for(const [k,v]of Object.entries(NW30_ART.banks))if(im===XART.get(v.key)){calls.push(k);break;}return draw.apply(this,[im,...a]);};try{nw28DrawBody(boss)}finally{ctx.drawImage=draw}return {flash:boss.flash,calls};}''');ck(name+' native flash selects matching authored hit art',q['flash']>0 and any(k.endswith('_hit')for k in q['calls']),q)
  # The discarded bank's extra fins must no longer receive body collision.
  oldBank=np.asarray(old.crop((272,8*272,544,9*272)))[:,:,3];newBank=np.asarray(cell('whole',65))[:,:,3];ys,xs=np.where((oldBank>128)&(newBank==0)&(np.indices(newBank.shape)[0]>145));pts=list(zip(xs.tolist(),ys.tolist()))[::max(1,len(xs)//25)]
  q=p.evaluate('''pts=>{const b=boss,A=b._whv.ace;A._nf29Pose=A.roll=A.somer=A.dash=A.desp=null;A.inverted=false;A.vx=200;b.flash=0;return pts.map(([x,y])=>nw28AlphaAt(b,A.x+x-136,A.y+y-136));}''',pts);ck('Removed extra-wing pixels no longer create phantom hull hits',len(q)>2 and not any(q),len(q))
  ck('Nightwing still has one health pool and one live target',p.evaluate('!boss.modular&&boss.hp>0&&retinaBossTargets(boss).length===1'))
  ck('Native rendering has no game, draw or HTTP errors',not errors and not http,dict(errors=errors,http=http));b.close()
finally:stop()
print(len(checks),'identity and native-render checks passed')
