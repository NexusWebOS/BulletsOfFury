"""Native-rendered isolated contact closeups. Direct native damage calls and
updateEffects, not a campaign fight. Real travel/collision is checked separately.
The earlier noisy real-RAF recording remains QA scratch, not presented as proof.
"""
from pathlib import Path
import sys,json,base64,subprocess,io
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/weapon_contacts_1031';W.mkdir(exist_ok=True);errors=[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe()
cases=[('Machine gun / metal contact + bullet marks',dict(kind='mg',lv=1)),('Laser cannon / blue contact + cooling scorch',dict(kind='spaceLaser',lv=2)),('Laser / red singe',dict(kind='beam',lv=5)),('Orb / toxic splash + elemental residue',dict(kind='orb',_el='toxic',lv=2)),('Maverick Helix / green energy contact',dict(kind='venomx',_charged=True,_full=False,lv=2)),('Maverick Helix ball / purple-blue energy',dict(kind='venomx',_charged=True,_full=True,lv=2))]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WC1031!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate('()=>{run.stage=1;stageLoadBegin(1)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(WC1031_ART).every(a=>XART.rdy(a.key))}',timeout=180000);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies.length=0;eBullets.length=0;pBullets.length=0;camX=0;player.x=VW/2;player.y=VH-70;window.E=spawnEnemy('s1tankheavy',player.x,player.y-190,{});Object.assign(E,{x:player.x,y:player.y-190,hp:1e7,maxhp:1e7,pattern:'__dummy',shoots:false,fk:null,vx:0,vy:0,_noSep:true,t:0});E._esh=null;window.home={x:E.x,y:E.y};drawWorld(0);}");p.wait_for_timeout(300)
  log=[]
  out=(W/'contacts-closeups-1031.mp4');enc=subprocess.Popen([ff,'-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x800','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=(W/'closeups-encode.log').open('w'))
  font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
  for n,(label,opt)in enumerate(cases):
   p.evaluate("()=>{pImpacts.length=0;particles.length=0;explosions.length=0;efxBursts.length=0;WC1031.gates=new WeakMap();E.x=home.x;E.y=home.y;E.flash=0;run.pilot='cole';run.weapon=0;run.wlevel=1;}")
   for f in range(72):
    data=p.evaluate("([b,fire])=>{const dt=1/30;efxClock+=dt;stateT+=dt;E.flash=Math.max(0,(E.flash||0)-dt);if(fire){const old=_dmgBullet;_dmgBullet={...b,x:E.x,y:E.y+10,vx:0,vy:-8,w:8,h:20};hitEnemy(E,1);_dmgBullet=old;}updateEffects(dt);drawWorld(0);return{png:cv.toDataURL().split(',')[1],x:E.x,y:E.y,w:cv.width,h:cv.height,draws:{...WC1031.draws}};}",[opt,f in (0,30)])
    native=Image.open(io.BytesIO(base64.b64decode(data['png']))).convert('RGB');frame=Image.new('RGB',(1280,800),(4,12,20));d=ImageDraw.Draw(frame)
    # The entire left view and the enlarged right crop are actual native pixels.
    view=native.copy();view.thumbnail((750,690),Image.Resampling.NEAREST);frame.paste(view,(5,70))
    x,y=data['x'],data['y'];detail=native.crop((round(x-64),round(y-64),round(x+64),round(y+64))).resize((460,460),Image.Resampling.NEAREST);frame.paste(detail,(790,125))
    d.text((22,24),label,font=font,fill='#e9faff');d.text((790,600),'Native contact detail / 3.6x',font=small,fill='#8deaff');d.text((22,765),'ISOLATED NATIVE EFFECT PREVIEW / actual authored hull, damage and drawImage / not a campaign fight',font=small,fill='#a9b9ca')
    enc.stdin.write(frame.tobytes())
    if f==5:frame.save(W/(f'closeup-{n}.jpg'),quality=94)
    if f%12==0:p.wait_for_timeout(1)
   log.append(dict(label=label,weapon=opt,draws=data['draws'],actor={k:data[k]for k in ['x','y','w','h']}))
  enc.stdin.close();assert enc.wait()==0;report=dict(frames=432,seconds=14.4,errors=errors,cases=log,method=__doc__);(W/'closeups-report.json').write_text(json.dumps(report,indent=2));br.close();print('NATIVE PREVIEW',out,'errors',errors,flush=True)
finally:stop()
