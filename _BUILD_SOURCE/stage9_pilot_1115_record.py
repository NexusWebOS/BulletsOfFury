from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_pilot_1115/final-recording';F=O/'films';F.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
RECORD=r'''async mode=>{
 const ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),anal=ac.createAnalyser();aq112Bus().output.connect(dest);aq112Bus().output.connect(anal);anal.fftSize=2048;const bins=new Float32Array(2048),out=document.createElement('canvas');out.width=1824;out.height=1024;const g=out.getContext('2d');g.imageSmoothingEnabled=false;
 const stream=out.captureStream(30);for(const t of dest.stream.getAudioTracks())stream.addTrack(t);const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:3500000,audioBitsPerSecond:96000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
 let start=performance.now(),frames=0,peak=0,endAt=null,hit=false,ended=false,prior='',tagAt=0,seen=new Set(),samples=[],stages=[],scroll=[],music=[],hud=[];
 function layers(){return ['screen','hud-top','hud-bot','equipcv','wide-left','wide-right','wide-clock','siege-left','siege-right','siege-compact'].map(id=>document.getElementById(id)).filter(Boolean).map(c=>{let opacity=1;for(let p=c;p;p=p.parentElement){const s=getComputedStyle(p);if(s.display==='none'||s.visibility==='hidden')opacity=0;opacity*=Number(s.opacity);}return{c,r:c.getBoundingClientRect(),opacity};}).filter(v=>v.opacity>0&&v.r.width>0&&v.r.height>0);}
 rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;
 if(mode==='fight'){
  const B=boss,G=B?._w9p15;if(G?.phase==='ship'&&t>2.5&&!hit){hit=true;B._ts58.half=true;B._ts58.protected=false;B.enter=false;let n=0;while(G.phase==='ship'&&n++<1000)hitBoss(5000);}
  if(G?.phase==='pilot'){const fire=keybindFor(1).fire.find(k=>!k.startsWith('mouse'));if(fire)Input.keys[fire]=G.t>1.3&&G.t<2.4;
   const aim=worldWidth()/2+Math.sin(G.t*.8)*95;Input.keys.a=player.x>aim+6;Input.keys.d=player.x<aim-6;
   if(G.cycles>0&&G.actor._cb112.phase==='grenades'&&G.actor._cb112.t>1.3&&!ended){ended=true;Input.keys.a=Input.keys.d=false;if(fire)Input.keys[fire]=false;let n=0;while(!B.dead&&n++<1000)hitBoss(5000);}
  }
 }
 loop(now);if(mode==='fight')SC12.refresh();frames++;const ls=layers();g.globalAlpha=1;g.fillStyle='#000';g.fillRect(0,0,1824,1024);if(ls.length){const x=Math.min(...ls.map(v=>v.r.left)),y=Math.min(...ls.map(v=>v.r.top)),w=Math.max(...ls.map(v=>v.r.right))-x,h=Math.max(...ls.map(v=>v.r.bottom))-y,k=Math.min(1824/w,1024/h),ox=(1824-w*k)/2,oy=(1024-h*k)/2;for(const v of ls){g.globalAlpha=v.opacity;g.drawImage(v.c,ox+(v.r.left-x)*k,oy+(v.r.top-y)*k,v.r.width*k,v.r.height*k);}g.globalAlpha=1;}
 anal.getFloatTimeDomainData(bins);for(const v of bins)peak=Math.max(peak,Math.abs(v));const G=boss?._w9p15;if(mode==='fight'&&frames%120===0){const m=Snd.music.boss9;music.push({t,src:m?.currentSrc,time:m?.currentTime,paused:m?.paused});hud.push({t,phase:G?.phase,visible:bossHealthVisible(boss),painted:!!EH7.lastBoss,hp:boss?.hp,max:boss?.maxhp,layers:ls.map(v=>v.c.id)});}
 const tag=mode==='fight'?(state+':'+(G?.phase||'')+':'+(G?.actor?._cb112.phase||'')+(boss?.dead?':dead':'')):('freezer:'+(DS15.last?.offset||0));
 if(tag!==prior){stages.push({tag,at:t});prior=tag;tagAt=now;}
 const shot=mode==='fight'?tag:Math.floor(t/2).toString();if((mode==='freezer'||now-tagAt>500)&&!seen.has(shot)){seen.add(shot);samples.push({tag,at:t,image:out.toDataURL('image/png')});}
 if(mode==='freezer'&&DS15.last)scroll.push({t,offset:DS15.last.offset,budget:DS15.last.budget,visible:DS15.last.visible});
 const finished=mode==='fight'?state===GS.STAGECLEAR:window.__freezerDone;if(finished&&endAt===null)endAt=now;
 if(endAt!==null&&now-endAt>650||t>(mode==='fight'?100:18)){clearInterval(timer);resolve();}
 },1000/60);});rec.stop();const video=await done;aq112Bus().output.disconnect(dest);aq112Bus().output.disconnect(anal);stream.getTracks().forEach(t=>t.stop());return {video,seconds:(performance.now()-start)/1000,frames,peak,stages,samples,scroll,music,hud,completed:endAt!==null};
}'''
files=['assets/game.js','_BUILD_SOURCE/test_fl.js','assets/current_breaker_1102.js','assets/stage9_pilot_1115.js','assets/dialogue_scroll_1115.js','index.html'];report={'clips':[],'errors':[],'sourceBefore':{f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in files},'scope':'Prepared terminal ship-health checkpoint, scripted native terminal damage on the two forms, untouched pilot AI clocks, brief real primary input and native full death/flyover/stage-clear. Player invulnerable. Not a campaign win or full balance certification. Freezer uses exact inactive retained dialogue as a current native comic rehearsal.'}
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for mode in ['fight','freezer']:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?water-pilot-record='+mode);p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  if mode=='fight':
   p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'));p.evaluate("()=>{BAL7.setup({stage:9,kind:'tidalfusion',pilot:'cole',diff:'normal',mode:'campaign',fire:false});DBGT.god=true;player.invuln=999;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;}")
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(9).ready&&Object.values(CB112_ART.banks).every(a=>XART.rdy(a.key))}',polling=50)
   for i in range(25):p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
   p.evaluate("()=>{boss._ts58.half=true;boss._ts58.protected=false;boss.enter=false;let n=0;while(boss.hp>boss.maxhp*.08&&n++<1000)hitBoss(40);Audio.startMusic('boss9');Input.clearTaps();last=performance.now();}")
  else:
   p.evaluate("()=>{run.mode='campaign';run.stage=1;run.pilot='freezer';coopOn=false;D1110.static=false;D1110.paused=false;const raw=PILOT_OPENINGS.axel.beats.find(b=>b.who==='freezer'),text=raw.text;window.__freezerDone=false;window.FROW={id:'FREEZER-SCROLL',who:'FREEZER',text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people:['freezer','axel'],fpLocations:{freezer:'cockpit-sky',axel:'cockpit-sky'},duration:text.length/30+3.5,readings:[],_cueSet:new Set(),cm3:{group:'freezer-scroll',readAt:.42,newStrip:true,baseDuration:text.length/30+3.5}};window.FKEYS=d1110Keys([FROW]);d1110Ready(FKEYS);}")
   p.wait_for_function('()=>d1110Ready(FKEYS)',polling=50);p.evaluate("()=>{d1110Play('freezer-scroll-review',[FROW],()=>window.__freezerDone=true);Input.clearTaps();last=performance.now();Audio.startMusic('cinematics');}")
  print('RECORDING '+mode,flush=True);r=p.evaluate(RECORD,mode);(F/(mode+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));shots=[]
  for i,s in enumerate(r.pop('samples')):fn=mode+'-'+str(i).zfill(2)+'.png';(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':fn})
  r.update({'mode':mode,'errors':errors,'shots':shots,'events':p.evaluate('mode=>mode==="fight"?W9P15.events:[]',mode)});report['clips'].append(r);report['errors']+=errors;(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');assert not errors and r['peak']>.001 and r['completed'],(mode,r['completed'],errors);print(json.dumps({'mode':mode,'seconds':r['seconds'],'peak':r['peak'],'completed':r['completed']}),flush=True);p.close()
 b.close()
report['sourceAfter']={f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in files};assert report['sourceAfter']==report['sourceBefore'];(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
