"""Verify current Nightwing identity and exact native normal/hit silhouettes.
The old release movie contains the retired Part2 banked planform; live art must
resolve only the source-locked aircraft in every flight and white-hit pose.
"""
from pathlib import Path
import json,hashlib,http.server
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/nightwing_shape_1028';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(name,v,data=None):
 checks.append(dict(name=name,passed=bool(v),data=data));(O/'probe.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));assert v,name
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text());images={k:Image.open(R/a['path']).convert('RGBA')for k,a in M['banks'].items()}
def cell(k,f):
 a=M['banks'][k];x=f%a['cols']*a['cw'];y=f//a['cols']*a['ch'];return images[k].crop((x,y,x+a['cw'],y+a['ch']))
source=Image.open(R/M['identity']['source']).convert('RGBA')
check('Every current flight bank declares the actual canonical aircraft identity',hashlib.sha256(source.tobytes()).hexdigest()==M['identity']['sha256'])
check('Level roll and pitch start from exactly the regular aircraft pixels',cell('whole',0).tobytes()==cell('whole',17).tobytes()==cell('whole',33).tobytes())
for bank in ['whole','clean','heading','flyover','drift_left','drift_right','approach','gun_left','gun_right']:
 check(bank+' normal and white-hit frames have identical alpha and common pivots',M['banks'][bank]['pivot']==M['banks'][bank+'_hit']['pivot']and all(cell(bank,f).getchannel('A').tobytes()==cell(bank+'_hit',f).getchannel('A').tobytes()for f in range(M['banks'][bank]['frames'])))
check('All actual frame canvases are fixed even cells',all(a['cw']%2==a['ch']%2==0 and max(images[k].size)<=4096 for k,a in M['banks'].items()))
check('Legacy whole and directional aliases select only corrected current banks',all(('identity_1028b'in M['banks'][v]['path']or'flight_1028c'in M['banks'][v]['path'])for k,v in M['aliases'].items()))
old=Image.open(R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/whole.png').convert('RGBA');old65=np.asarray(old.crop((272,8*272,544,9*272)))[:,:,3];new65=np.asarray(cell('whole',65))[:,:,3]
yy,xx=np.where((old65>128)&(new65==0));points=list(zip(xx.tolist(),yy.tolist()))[::max(1,len(xx)//40)]
check('Retired banked planform differs from the corrected canonical wing geometry',len(points)>20,dict(removedOpaquePixels=len(xx)))
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(NW30_ART.banks).every(a=>XART.rdy(a.key))}');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss)}")
  for i in range(18):
   err=p.evaluate(shoot.STEP,24);assert not err,err;p.wait_for_timeout(1)
  p.evaluate("""()=>{window.nightwingPixels=(hit)=>{const draw=ctx.drawImage,get=XART.get,keys=new Set(Object.entries(NW30_ART.banks).filter(([k])=>/^(whole|clean|heading|flyover|drift_left|drift_right|approach|death_large|gun_left|gun_right)(_hit)?$/.test(k)).map(([,a])=>a.key));let key='',calls=[];
   const render=bg=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=bg;ctx.fillRect(0,0,cv.width,cv.height);XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...a){if(keys.has(key)){calls.push(key);return draw.call(this,im,...a)}};try{nw28DrawBody(boss)}finally{XART.get=get;ctx.drawImage=draw;ctx.restore()}return ctx.getImageData(0,0,cv.width,cv.height).data;};
   // The native canvas is opaque: recover coverage from two background reads.
   const black=render('#000000'),light=render('#ffffff'),mask=Uint8Array.from({length:black.length/4},(_,i)=>255-(light[i*4]-black[i*4]));let same=true,white=0,lit=0,maxDelta=0;
   for(let i=0;i<mask.length;i++){if(hit){const delta=Math.abs(mask[i]-window.nightwingNormalMask[i]);maxDelta=Math.max(maxDelta,delta);if(delta>2)same=false;}if(mask[i]>250){lit++;if(black[i*4]>245&&black[i*4+1]>245&&black[i*4+2]>245)white++;}}
   if(!hit)window.nightwingNormalMask=mask;return{same,maxDelta,lit,white,calls,pose:nw30Pose(boss).bank};};}""")
  poses=[('cruise',{}),('left-bank',dict(vx=-200)),('right-bank',dict(vx=200)),('roll',dict(roll=dict(t=.10,dir=1))),('somersault',dict(somer=dict(t=.12))),('inverted',dict(inverted=True)),('turn',dict(pose=dict(bank='heading',frame=117,scale=1))),('flyover',dict(pose=dict(bank='flyover',frame=3,scale=1.6))),('drift',dict(pose=dict(bank='drift_right',frame=18,scale=1.3))),('return',dict(pose=dict(bank='approach',frame=14,scale=.98)))]
  for name,config in poses:
   p.evaluate("""c=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A._nw28.mode='fight';A.st='fight';A.dash=A.desp=A.roll=A.somer=A._nf29Pose=null;A.inverted=false;A.vx=A.vy=0;A.x=camLeftX()+viewW()/2;A.y=220;b.x=A.x;b.y=A.y;b.flash=0;b.dead=false;b._noHit=false;Object.assign(A,c);A._nf29Pose=c.pose||null;}""",config)
   normal=p.evaluate('nightwingPixels(false)');p.evaluate('()=>{boss._gp4FlashNext=0;markHit(boss)}');hit=p.evaluate('nightwingPixels(true)')
   check(name+' actual native normal/hit body pixels preserve exactly the same silhouette',hit['same']and hit['lit']>1000 and hit['white']>hit['lit']*.99,dict(normal=normal,hit=hit))
   if name in ['right-bank','roll','cruise']:p.screenshot(path=str(O/(name+'-hit.png')))
  p.evaluate("()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.dash=A.desp=A.roll=A.somer=A._nf29Pose=null;A.inverted=false;A.vx=200;b.flash=0;}")
  q=p.evaluate('pts=>pts.map(([x,y])=>nw28AlphaAt(boss,boss._whv.ace.x+x-136,boss._whv.ace.y+y-136))',points)
  check('Removed legacy fin pixels do not leave phantom damage collision',not any(q),len(q))
  p.evaluate('()=>{boss._whv.ace.vx=0;boss._gp4FlashNext=0;}');before=p.evaluate('boss.hp');p.evaluate('hitBoss(1)');hit=p.evaluate('nightwingPixels(true)');check('A real native hit reduces the single HP pool and whites the current aircraft',p.evaluate('boss.hp')<before and p.evaluate('boss.flash>0')and hit['white']>hit['lit']*.99)
  for i in range(2):
   err=p.evaluate(shoot.STEP,12);assert not err,err;p.wait_for_timeout(1)
  check('Native white hit flash expires with one live Retina target',p.evaluate('boss.flash===0&&!boss.modular&&retinaBossTargets(boss).length===1'))
  check('No game, draw, console or asset errors',not errors,errors);browser.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),passed=all(q['passed']for q in checks))))
