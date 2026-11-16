from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,hashlib,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/ally_dialogue_1115';F=O/'films';F.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
PLAN=[
 {'key':'roundtable','title':'Allied pairs — Stage 3 briefing','scene':'post-3','pilot':'cole','ids':['CW3-'+str(i).zfill(2)for i in range(9,17)]},
 {'key':'workshop','title':'Cole & Decker — Photon Cannon and workshop','scene':'post-3','pilot':'cole','tag':'prototypes'},
 {'key':'brotherhood','title':'Axel & Freezer — homecoming','scene':'ending','pilot':'axel','ids':['ENDING-07','ENDING-08']},
 {'key':'sisters','title':'Falva & Lizzie — calling Mom','scene':'ending','pilot':'falva','ids':['ENDING-11','ENDING-12']},
 {'key':'yuri','title':'Yuri & Cole — calling home','scene':'ending','pilot':'yuri','ids':['ENDING-09','ENDING-10']},
 {'key':'maverick','title':'Maverick & Cole — stop worrying','scene':'ending','pilot':'maverick','ids':['ENDING-13']},
 {'key':'coffee','title':'Decker & Cole — cold coffee','scene':'ending','pilot':'decker','ids':['ENDING-14','ENDING-15']},
 {'key':'heavy-metal','title':'Juggernaut & Freezer — the volume knob','scene':'ending','pilot':'juggernaut','ids':['ENDING-16','ENDING-17','ENDING-18']},
 {'key':'album','title':'Juggernaut & Cole — Bulletalica','scene':'city','pilot':'cole','ids':['CITY16-03','CITY16-04','CITY16-05','CITY16-06','CITY16-ALBUM']}
]
RECORD=r'''async plan=>{
 const ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),anal=ac.createAnalyser();aq112Bus().output.connect(dest);aq112Bus().output.connect(anal);anal.fftSize=2048;const bins=new Float32Array(2048);
 const out=document.createElement('canvas');out.width=1824;out.height=1024;const g=out.getContext('2d');g.imageSmoothingEnabled=false;const stream=out.captureStream(30);for(const t of dest.stream.getAudioTracks())stream.addTrack(t);
 const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:3600000,audioBitsPerSecond:96000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
 let start=performance.now(),frames=0,peak=0,prior='',tagAt=0,endAt=null,stages=[],samples=[],receipts=[],seen=new Set(),gotFaces=new Set();
 rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();loop(now);frames++;
 const c=document.getElementById('screen');g.globalAlpha=1;g.fillStyle='#000';g.fillRect(0,0,1824,1024);g.drawImage(c,0,0,1824,1024);
 anal.getFloatTimeDomainData(bins);for(const v of bins)peak=Math.max(peak,Math.abs(v));
 const s=BOFCinematicDirector.current,b=s?.beats[s.i],tag=b?.id||'end';
 if(tag!==prior){stages.push({tag,at:(now-start)/1000});prior=tag;tagAt=now;}
 if(b&&s.t>(b.cm3?.readAt||0)+.85&&!seen.has(tag)){seen.add(tag);samples.push({tag,who:b.who,text:b.text,at:(now-start)/1000,image:out.toDataURL('image/png')});}
 if(b&&s.t>(b.cm3?.readAt||0)+.9&&!gotFaces.has(tag)){gotFaces.add(tag);receipts.push({tag,who:b.who,text:b.text,people:b.people,locations:b.fpLocations,kind:b.kind,bank:b.bank,cw16:b.cw16,faces:CM3.last?.shot===tag?CM3.last.faces:[],direct:CP15.last?.pilot===b.who.toLowerCase()?CP15.last:null});}
 if(window.__allyReviewDone&&endAt===null)endAt=now;
 if(endAt!==null&&now-endAt>100||now-start>180000){clearInterval(timer);resolve();}
 },1000/60);});rec.stop();const video=await done;aq112Bus().output.disconnect(dest);aq112Bus().output.disconnect(anal);stream.getTracks().forEach(t=>t.stop());return{video,seconds:(performance.now()-start)/1000,frames,peak,stages,samples,receipts,completed:!!window.__allyReviewDone};
}'''
files=['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html','assets/cinematic_rework_1114.js','assets/comic_story_1111.js','assets/comic_motion_1111.js','assets/front_pilots_1111.js','assets/cockpit_talk_1114.js','assets/cockpit_talk_art_1114.js','assets/city_rescue_1115.js','assets/stage_frame_1115.js']
report={'clips':[],'errors':[],'scope':'Native directed excerpts selected verbatim from current scene builders, with ordinary dialogue clocks, artwork and native mixer. This review does not represent ally-gated unlocks or a campaign win; historical opening transcripts are inactive. No shipping story/art edits.','before':{n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in files}}
with sync_playwright()as pw:
 browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 p=browser.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?ally-dialogue-review=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 inventory=p.evaluate('''()=>{run.mode='campaign';diffKey='furious';run.pilot='cole';coopOn=false;campaign.stageX1004=null;run._gp4StageX=null;const out={};for(const id of ['post-3','post-4','ending'])out[id]=c16Rows(id,'cole','left').map(b=>({id:b.id,who:b.who,text:b.text,people:b.people,tag:b.tag,kind:b.kind,bank:b.bank,cw16:b.cw16}));out.city=city16Rows('cole').map(b=>({id:b.id,who:b.who,text:b.text,people:b.people,kind:b.kind,bank:b.bank}));out.legacy=PILOT_OPENINGS;return out}''')
 (O/'dialogue-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf8')
 for plan in PLAN:
  print('PREPARING '+plan['key'],flush=True)
  selected=p.evaluate('''plan=>{BOFCinematicDirector.cancel();story=null;campPause=null;run.mode='campaign';run.pilot=plan.pilot;pilotIndex=PILOTS.findIndex(p=>p.key===plan.pilot);coopOn=false;run._gp4StageX=null;D1110.paused=false;D1110.static=false;window.__allyReviewDone=false;Input.clearTaps();Input.mouse.down=false;
   let rows=plan.scene==='city'?city16Rows(plan.pilot):c16Rows(plan.scene,plan.pilot,'left');rows=rows.filter(b=>plan.tag?b.tag===plan.tag:plan.ids.includes(b.id));if(!rows.length)throw Error('No review rows for '+plan.key);window.__allyReviewRows=rows;window.__allyReviewKeys=d1110Keys(rows,plan.pilot);d1110Ready(__allyReviewKeys);return rows.map(b=>({id:b.id,who:b.who,text:b.text,people:b.people,duration:b.duration,locations:b.fpLocations,kind:b.kind,cw16:b.cw16,bank:b.bank}));}''',plan)
  p.wait_for_function('()=>d1110Ready(__allyReviewKeys)',polling=50)
  p.evaluate('''plan=>{CP15.history=[];CM3.last=null;CP15.last=null;d1110Play('ally-review-'+plan.key,__allyReviewRows,()=>{window.__allyReviewDone=true;});Input.clearTaps();last=performance.now();Audio.startMusic('hq');}''',plan)
  print('RECORDING '+plan['key']+' '+str(len(selected))+' rows',flush=True);r=p.evaluate(RECORD,plan)
  (F/(plan['key']+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));shots=[]
  for i,s in enumerate(r.pop('samples')):
   fn=plan['key']+'-%02d.png'%i;(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':fn})
  r.update({'plan':plan,'rows':selected,'shots':shots,'errors':list(errors)});report['clips'].append(r);report['errors']=list(errors)
  (O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');assert r['completed']and r['peak']>.001 and not errors,(plan['key'],r['completed'],errors)
  print(json.dumps({'clip':plan['key'],'seconds':r['seconds'],'peak':r['peak'],'errors':len(errors)}),flush=True)
 browser.close()
report['after']={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in files};assert report['before']==report['after'];(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('Nine native pair-dialogue chapters recorded.',flush=True)
