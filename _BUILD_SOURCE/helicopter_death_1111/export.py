from pathlib import Path
import sys,json,base64,hashlib
W=Path(__file__).parent;sys.path.insert(0,str(W.parent/'helicopter-1111'));from native import R,serve,STEP,TRAP_RAF,sync_playwright
O=W.parents[1]/'outputs/helicopter-death';O.mkdir(parents=True,exist_ok=True);(W/'sources').mkdir(exist_ok=True);port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>4');p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugUnlocked=true;diffKey='normal';debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss('damkeeper');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);player.invuln=1e9;window.B=boss;}")
  p.wait_for_function("()=>{stageLoadTick();return stageLoadReady(1)&&['ovbody_intact','ovbody_critical',...Array.from({length:16},(_,i)=>'ovrotor_'+String(Math.floor(i*72/16)).padStart(2,'0'))].every(k=>XART.rdy(k))}")
  sizes=p.evaluate('({w:B.w,h:B.h,source:[XART.get("ovbody_critical").width,XART.get("ovbody_critical").height],worldW:worldWidth()})')
  for key in ['ovbody_intact','ovbody_critical']+['ovrotor_'+str(i*72//16).zfill(2)for i in range(16)]:
   data=p.evaluate("(key)=>{const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}",key);(W/'sources'/(key+'.png')).write_bytes(base64.b64decode(data))
  for key in ['ovbody_intact','ovbody_critical']:
   data=p.evaluate("(key)=>{const im=ovFuryPlate(key);return im.toDataURL('image/png').split(',')[1];}",key);(W/'sources'/(key+'-furious.png')).write_bytes(base64.b64decode(data))
  br.close()
finally:stop()
files=['game.js','stage1_repair_1021.js','dracodia_helicopter_1030.js','helicopter_effects_1111.js','dracodia_energy_1110.js','stage8_identity_1018.js','dracodia_return_1030.js'];before={n:hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()for n in files};before['index.html']=hashlib.sha256((R/'index.html').read_bytes()).hexdigest();(W/'before.json').write_text(json.dumps(before,indent=2));(W/'reference.json').write_text(json.dumps({'stage1':sizes,'errors':errors},indent=2));print(json.dumps({'stage1':sizes,'errors':errors}),flush=True);assert not errors
