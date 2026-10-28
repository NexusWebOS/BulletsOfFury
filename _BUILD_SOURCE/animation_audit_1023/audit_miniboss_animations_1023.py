from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,base64,io,numpy as np,time
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'miniboss-native';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
report={'cases':[],'errors':[]};port,stop=shoot.serve(str(R))
def img(s):return Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')
def bright(a,b):
 a=np.array(a).astype(int);b=np.array(b).astype(int);return int(((a.max(2)>12)&(b.mean(2)-a.mean(2)>20)).sum())
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  kinds=['razorback','magmaward','frostcruiser','olivewarden','siegebomber','siegefortress17','dualscoopdredger','heralddeath','voidhorizon'];p.evaluate('''()=>{window.MQ23={keys:new Set(),bad:[],drawBase:ctx.drawImage};ctx.drawImage=function(im,...a){const k=AQ23.tags.get(im)||HA21.tags.get(im)||'cached';if(MQ23.active){MQ23.keys.add(k);const w=im?.naturalWidth||im?.width,h=im?.naturalHeight||im?.height;if(!w||!h||a.some(v=>!Number.isFinite(v))||a.length===8&&(a[0]+a[2]>w+.1||a[1]+a[3]>h+.1))if(MQ23.bad.length<12)MQ23.bad.push({k,a,w,h});}return MQ23.drawBase.call(this,im,...a);};MQ23.draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);drawSubBoss(B);ctx.restore();return cv.toDataURL().split(',')[1];};}''')
  for diff in ['normal','hard','furious','easy']:
   for st,kind in enumerate(kinds,1):
    row={'stage':st,'kind':kind,'difficulty':diff};p.evaluate('c=>BAL7.setup(c)',{'stage':st,'kind':kind,'mini':True,'diff':diff,'fire':False});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
    p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;B.enter=B._noHit=false;player.invuln=40002;camX=B.x-viewW()/2;MQ23.active=true;MQ23.keys.clear();MQ23.bad=[];AQ23.current={mini:true};AQ23.cue.clear();window.MQ23states=new Set();window.MQ23peak=0;}''')
    normal=None;flash=None
    for batch in range(36):
     m=p.evaluate('''()=>{for(let i=0;i<60;i++){player.invuln=40002;player.fireCd=9999;pBullets=[];updatePlay(1/60);if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}MQ23states.add(B.phase??B._state??B._er26?.mode??B.pattern??'native');MQ23peak=Math.max(MQ23peak,eBullets.length);}return{y:B.y,x:B.x,dead:B.dead,state,finite:Number.isFinite(B.x+B.y)};}''')
     if batch in [2,10,20,32] and diff=='normal':
      p.screenshot(path=str(O/f's{st}-{batch:02}.png'))
     if batch==4:
      p.wait_for_timeout(150);data=p.evaluate('()=>{B.flash=0;return MQ23.draw();}');normal=img(data);native=p.evaluate('''()=>{const before=B.hp;const old=_dmgBullet;_dmgBullet={kind:'mg',lv:1,x:B.x,y:B.y};hitSubBoss(.1,B.x,B.y);_dmgBullet=old;const timer=B.flash;return{before,after:B.hp,timer,image:MQ23.draw()};}''');flash=bright(normal,img(native['image']));row['nativeHit']={k:v for k,v in native.items()if k!='image'};row['nativeHit']['brightPixels']=flash;p.evaluate('()=>markHit(B,.12)');p.wait_for_timeout(120);marked=img(p.evaluate('()=>MQ23.draw()'));row['markedBrightPixels']=bright(normal,marked)
     if not m['finite']or m['dead']:break
    row.update(p.evaluate('''()=>({states:[...MQ23states],keys:[...MQ23.keys],geometry:MQ23.bad,peakProjectiles:MQ23peak,cues:Object.fromEntries(AQ23.cue),flashExpired:B.flash<=0,finite:Number.isFinite(B.x+B.y),hp:B.hp})'''));MQ=False;report['cases'].append(row);(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:row[k]for k in ['stage','kind','difficulty','peakProjectiles','flashExpired','finite']}|{'geometry':len(row['geometry']),'nativeWhite':flash}),flush=True)
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps(report,indent=2))

