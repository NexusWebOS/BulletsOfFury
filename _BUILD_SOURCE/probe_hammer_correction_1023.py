from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,io
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';O=R/'_shots/hammer_correction_1023';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(45000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for path in ['balance_lab_1007.js','animation_audit_1023/hammer_review_lab_1023.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/path))
  ev=p.evaluate
  ev('BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ht23Warm()&&ha21Ready();}');ev('''()=>{window.reset23=()=>{HR23.blue();HT23.speech=[];HT23.speechOwner=null;HR23.active=true;B._hammer.cp12State='hammer';B._hammer.cp12Caption=null;};reset23();window.redraw23=()=>{HR23.keys.clear();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return [...HR23.keys];};}''')
  def snap(name):
   (O/(name+'.png')).write_bytes(base64.b64decode(ev('cv.toDataURL().split(",")[1]')))
  # Exact approved box, not a new chest: compare the real registered cell pixels.
  row=ev('''()=>{const a=HT23_ART.banks.crate[0],c=document.createElement('canvas');c.width=c.height=80;const g=c.getContext('2d');g.drawImage(XART.get(a.key),0,0);return{png:c.toDataURL().split(',')[1]};}''')
  native=Image.open(io.BytesIO(base64.b64decode(row['png']))).convert('RGBA');ref=Image.open(R/'assets/game/shared/pickups/hammer_chaingun_1020/crate.webp').convert('RGBA').resize((80,80),Image.Resampling.NEAREST);ref.putalpha(ref.getchannel('A').point(lambda v:255 if v>127 else 0))
  import numpy as np
  a=np.array(native).astype(int);b=np.array(ref).astype(int);solid=b[:,:,3]>0
  # Canvas premultiplication may discard hidden RGB; compare displayed pixels.
  error=np.abs(a[:,:,:3]*a[:,:,3:4]/255-b[:,:,:3]*b[:,:,3:4]/255)
  ck('Pickup icon cell matches the original exclusive chaingun box pixels',bool(np.array_equal(a[:,:,3],b[:,:,3]))and float(error.max())<=1.1,{'maxPremultipliedError':float(error.max())})
  ev('''()=>{reset23();HR23.start('pickup','normal');B._hammer.hb20Pickup.t=1.7;redraw23();}''');snap('chaingun-box')
  for diff in ['normal','hard','furious']:
   row=ev('''d=>{reset23();diffKey=d;DIFF=difficultyForRun(run.mode,d);fr27BeginArmor(B);HT23.speech=[];const keys=[],bad=[];for(let i=0;i<16;i++){B._hammer.t=(i+.25)/16*FR27_ACT.end;const q=ha21Blue(B);keys.push(q.a.key);const drawn=redraw23();if(!drawn.includes(q.a.key)||drawn.some(k=>/^ha21_blue_chromium_/.test(k)))bad.push(i);}return{keys,bad};}''',diff)
   ck(diff+' all 16 actual activation poses draw the cleaned authored plates',len(set(row['keys']))==16 and not row['bad'],row)
  for i in [0,5,10,15]:
   ev('''i=>{B._hammer.t=(i+.25)/16*FR27_ACT.end;redraw23();}''',i);snap('activation-'+str(i))
  row=ev('''()=>{B._hammer.t=1.8;B._hammer.cp12State='fr_activation';HT23.speech=[];B.flash=0;B._gp4FlashNext=0;GP4.clock+=1;const keys=redraw23();const before=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(B,.12);const hit=redraw23();const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<before.length;i+=4)if(before[i]+before[i+1]+before[i+2]<650&&after[i]>240&&after[i+1]>240&&after[i+2]>240)white++;for(let i=0;i<14;i++)HR23.step();return{white,hit:hit.some(k=>k.startsWith('ht23_activation_hit')),expired:B.flash<=0,after:redraw23()};}''')
  ck('Clean activation has actual white hit pixels and natural flash expiry',row['white']>100 and row['hit']and row['expired'],row)
  audit=json.loads((W/'armor/manifest.json').read_text())['activationAudit']
  ck('Every exported activation preserves source outline pixels, dark seams and alpha',len(audit)==16 and all(q['darkSeamsPreserved']and q['edgeRGBPreserved']and q['sameAlpha']for q in audit))
  sheets=json.loads((W/'armor/manifest.json').read_text())['audit']
  ck('All 20 live/legacy armor sheets preserve dark outlines, seams and alpha',len(sheets)==20 and all(q['edgeDarkKept']and q['darkSeamsPreserved']and q['sameAlpha']for q in sheets))
  # Announcements: native trigger, actual portrait blit, protected clocks, real Start.
  for kind,text in [('armor','Chromium Armor, Activated!'),('shield','Chromium Shield, Activate!'),('recharge','Gotta Recharge!'),('taunt',"Is that the best you've got, mortal?")]:
   ev('''q=>{reset23();if(q.kind==='armor')fr27BeginArmor(B);else{B._hammer.state=q.kind==='shield'?'shield':'hammer';cp12Caption(B,q.text);}updatePlay(1/60);}''',{'kind':kind,'text':text})
   p.wait_for_function('XART.rdy("fb1002_hammer_portrait")&&XART.rdy("ui20_dialogue-a")')
   row=ev('''()=>{for(let i=0;i<75;i++)HR23.step();const t=B._hammer.t,keys=redraw23();for(let i=0;i<10;i++)HR23.step();return{live:BOFCinematicDirector.live,text:BOFCinematicDirector.current?.beats[0]?.text,portrait:UI20.dialogue?.portrait,keys,paused:B._hammer.t===t,legacy:B._hammer.cp12Caption?.t>0,layout:UI20.dialogue};}''')
   ck(kind+' opens the real Hammer portrait dialogue and freezes unsafe combat',row['live']and row['text']==text and row['portrait']=='fb1002_hammer_portrait'and 'fb1002_hammer_portrait'in row['keys']and row['paused']and not row['legacy'],row)
   snap('dialogue-'+kind)
   p.keyboard.press('Enter');ev('HR23.step()')
   row=ev('''()=>{const active=BOFCinematicDirector.active,t=B._hammer.t;HR23.step();return{active,resumed:B._hammer.t>t,queued:HT23.speech.length};}''')
   ck(kind+' real Start skips once and native combat resumes without duplicate dialogue',not row['active']and row['resumed']and row['queued']==0,row)
  # Queue while another conversation owns the dialogue; do not interrupt it.
  row=ev('''()=>{reset23();BOFCinematicDirector.play('unrelated-test',[{who:'COLE',text:'Hold the line.'}],()=>{},true);fr27BeginArmor(B);updatePlay(0);const held=BOFCinematicDirector.current.id==='unrelated-test'&&HT23.speech.length===1;BOFCinematicDirector.finish();updatePlay(0);const next=BOFCinematicDirector.current?.beats[0]?.text;return{held,next};}''')
  ck('Armor line waits for an existing conversation instead of replacing it',row['held']and row['next']=='Chromium Armor, Activated!',row)
  row=ev('''()=>{B.flash=0;B._gp4FlashNext=0;GP4.clock+=1;markHit(B,.12);const hit=redraw23().some(k=>k.includes('activation_hit')),t=B._hammer.t;for(let i=0;i<18;i++)HR23.step();return{hit,expired:B.flash<=0,stillSpeaking:BOFCinematicDirector.live,combatPaused:B._hammer.t===t};}''')
  ck('A pre-announcement hit flash expires while dialogue keeps combat paused',row['hit']and row['expired']and row['stillSpeaking']and row['combatPaused'],row)
  row=ev('''()=>{B.dead=true;updatePlay(0);return{active:BOFCinematicDirector.active,pending:HT23.speech.length};}''');ck('Defeated boss cannot leave a stuck or queued announcement',not row['active']and row['pending']==0,row)
  # Native visible armor attack banks across raised, throw and jump states.
  row=ev('''()=>{reset23();const out=[];for(const [state,t]of[['storm_raise',1],['warn',.5],['spin',.4],['throw',.2],['recover',.2]]){B._hammer.state=state;B._hammer.t=t;const q=ha21Blue(B),keys=redraw23();out.push({state,key:q?.a?.key,corrected:!!HT23_ARMOR.sheets[q?.a?.sheet],drawn:keys.includes(q?.a?.key)});}return out;}''');ck('Raised-hammer, jump, throw and recovery use corrected dark-edged armor sheets',all(q['corrected']and q['drawn']for q in row),row)
  ev('''()=>{reset23();fr27BeginArmor(B);}''')
  video=ev('''async()=>{const cs=cv.captureStream(30),as=await HR23.audio(),stream=new MediaStream([...cs.getVideoTracks(),...as.getAudioTracks()]),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1800000}),chunks=[];rec.ondataavailable=e=>e.data.size&&chunks.push(e.data);const end=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});rec.start();let last=performance.now(),start=last,transition=false;await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();if(now-start>8000&&!transition){transition=true;HR23.start('pickup','normal');HT23.speech=[];}HR23.step(Math.min(.035,(now-last)/1000));last=now;if(now-start>15500){clearInterval(timer);resolve();}},1000/60);});rec.stop();const data=await end;HR23.audioRestore();cs.getTracks().forEach(t=>t.stop());return data;}''');(O/'corrected-native.webm').write_bytes(base64.b64decode(video.split(',')[1]));ck('Corrected armor, portrait announcement and icon-box handoff recorded in native game',(O/'corrected-native.webm').stat().st_size>50000)
  br.close()
finally:stop()
ck('No page or asset errors',not errors,errors);report={'checks':checks,'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'errors':errors};(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k]for k in ['passed','failed','errors']}));sys.exit(bool(report['failed']))
