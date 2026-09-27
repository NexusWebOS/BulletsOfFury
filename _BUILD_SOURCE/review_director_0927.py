"""Real-time Chromium + SFX recordings. Controlled inspection fixtures, not wins."""
import ast,base64,json,http.server,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/director_0927');OUT.mkdir(parents=True,exist_ok=True)
def constant(file,key):
 t=ast.parse(Path(file).read_text(encoding='utf-8'));return next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id==key)
SETUP=constant('_BUILD_SOURCE/probe_polish_0927b.py','SETUP');CAPTURE=constant('_BUILD_SOURCE/review_overnight_0927.py','CAPTURE')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report=[];selected=set(sys.argv[1:])
if selected and (OUT/'videos.json').exists():report=[c for c in json.loads((OUT/'videos.json').read_text(encoding='utf-8'))['clips'] if c['name'] not in selected]
CASES=[{'name':'tempest-hard','stage':5,'kind':'spacebomber','mini':True,'diff':'hard','seconds':24},
 {'name':'tempest-furious','stage':5,'kind':'spacebomber','mini':True,'diff':'furious','seconds':30},
 {'name':'module-cascades','stage':4,'kind':'stormsovereign','mini':False,'diff':'normal','seconds':22},
 {'name':'player-weapons','stage':1,'kind':'junglecruiser','mini':False,'diff':'normal','seconds':30},
 {'name':'muzzle-reels','stage':1,'kind':'junglecruiser','mini':False,'diff':'normal','seconds':8},
 {'name':'pilot-thrusters','stage':1,'kind':'junglecruiser','mini':False,'diff':'normal','seconds':8}]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF);p.evaluate(CAPTURE)
  p.evaluate("()=>{wm26Warm();Object.keys(MR27_ART).forEach(k=>XART.rdy('mr27_'+k));PILOTS.forEach(p=>['','_g1','_g2'].forEach(s=>XART.rdy('ship_'+p.key+s)));}")
  p.wait_for_function("()=>Object.keys(DIRECTOR_ART.sheets).every(k=>XART.rdy('d27_'+k))&&PILOTS.every(p=>['','_g1','_g2'].every(s=>XART.rdy('ship_'+p.key+s)))")
  for c in CASES:
   if selected and c['name'] not in selected:continue
   print('RECORD',c['name'],flush=True);p.evaluate(SETUP,c)
   p.evaluate("()=>{story=null;s6Opening=null;s6Wing=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Snd.stopMusic();Snd.setVol('music',0);Snd.loopStopAll();capturePeak=0;captureCues=[];run.forge={};run.forgeForms={};run.wvars=[];special=null;}")
   if c['name']=='module-cascades':p.evaluate("()=>{B.enter=false;B._noHit=false;B._be=null;B.y=B.ty;B._drawY=B.y;B._s4war.shield.active=false;B._s4war.shield.rearming=false;for(const n of B._s4war.shield.nodes)n.dead=true;}")
   if c['name']=='player-weapons':p.evaluate("()=>{boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];stagePlan=[];spawnClock=99999;run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.wlevel=3;run.wlevels=[3,3,3,3,3,3,3,3,3];}")
   r=p.evaluate("""async c=>{const stream=ctx.canvas.captureStream(30);for(const a of captureAudio.stream.getAudioTracks())stream.addTrack(a.clone());const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1700000,audioBitsPerSecond:96000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    const start=performance.now(),snaps=[],families=new Set();let broke=0,lastWeapon=-1,finite=true,zoomMin=1,zoomMax=1;rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=c.name==='player-weapons'?0:1002;powerups=[];story=null;
      if(c.name==='muzzle-reels'||c.name==='pilot-thrusters'){
       ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#101c28';ctx.fillRect(0,0,VW,VH);
       if(c.name==='muzzle-reels'){let i=0;for(const k of Object.keys(DIRECTOR_ART.reels)){const x=60+i%4*120,y=109+Math.floor(i/4)*126;d27MuzzleDraw(ctx,k,x,y,-Math.PI/2,(t*2)%1,90);ctx.fillStyle='#d5eaff';ctx.font='10px monospace';ctx.textAlign='center';ctx.fillText(k,x,y+12);i++;}}
       else PILOTS.forEach((p,i)=>{const im=XART.get('ship_'+p.key),h=136,w=h*im.width/im.height,x=80+i%3*160,y=74+Math.floor(i/3)*169;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.fillStyle='#d5eaff';ctx.font='11px monospace';ctx.textAlign='center';ctx.fillText(p.key,x,y+81);});
      }else{
       const fire=c.name==='player-weapons';for(const [a,on]of [['left',!fire&&t%8<4],['right',!fire&&t%8>=4],['fire',fire]])for(const k of keybindFor(1)[a]||[])if(!k.startsWith('pad_'))Input.keys[k]=on;
       if(fire){const w=Math.min(8,Math.floor(t/3.3));if(w!==lastWeapon){pBullets=[];wm26Releases=[];Snd.loopStopAll();run.weapon=w;run.wlevel=3;lastWeapon=w;player.fireCD=0;}}
       if(c.name==='module-cascades'&&broke<4&&t>3+broke*4){const part=B._mr27.parts[broke],q=mr27Shape(B,part.id);_lastHitX=q.x;_lastHitY=q.y;_dmgBullet=null;hitBoss(part.hp+1);broke++;}
       loop(now);zoomMin=Math.min(zoomMin,viewZoom());zoomMax=Math.max(zoomMax,viewZoom());for(const f of wm26Releases)families.add(f.family);finite=finite&&eBullets.every(q=>Number.isFinite(q.x+q.y));
      }
      captureAnalyser.getFloatTimeDomainData(captureBins);for(const x of captureBins)capturePeak=Math.max(capturePeak,Math.abs(x));
      if(snaps.length<4&&t>(snaps.length+1)*c.seconds/5)snaps.push(ctx.canvas.toDataURL());if(t>=c.seconds){clearInterval(timer);resolve();}
    },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());for(const k of Object.keys(Input.keys))Input.keys[k]=false;return {video,snaps,finite,zoomMin,zoomMax,families:[...families],audioPeak:capturePeak,breaks:broke};}""",c)
   (OUT/(c['name']+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
   for i,img in enumerate(r.pop('snaps')):(OUT/f"{c['name']}-video-{i}.png").write_bytes(base64.b64decode(img.split(',')[1]))
   report.append({**c,**r});(OUT/'videos.json').write_text(json.dumps({'clips':report,'errors':errors},indent=2),encoding='utf-8')
  br.close()
finally:stop()
assert not errors,errors
assert all(c['finite'] and c['zoomMin']==c['zoomMax']==1 for c in report)
print(json.dumps({'clips':report,'errors':errors},indent=2))
