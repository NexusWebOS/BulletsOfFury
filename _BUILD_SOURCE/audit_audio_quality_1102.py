"""Actual Chromium decoding and post-mix audible playback of every unique SFX.
Inventory aliases/variants separately; honour source files and native mix gates.
"""
from pathlib import Path
import json,sys,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/furious_encounters_1102/audio';O.mkdir(parents=True,exist_ok=True)
state=dict(registry={},decoded=[],playback=[],errors=[],checks=[])
def save(): (O/'quality.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000);p.on('pageerror',lambda e:state['errors'].append(str(e)));p.on('console',lambda m:state['errors'].append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF)
 inventory=p.evaluate('''async()=>{Audio.init();Audio.resume();Audio.stopMusic();Snd.loopStopAll();const c=Snd._audioCtx();await c.resume();window.aqFiles=[];const seen=new Map();for(const [cue,raw]of Object.entries(BOFA.sfx))for(const value of(Array.isArray(raw)?raw:[raw])){const uri=typeof value==='string'&&value.startsWith('assets/')?value:'data:audio/mpeg;base64,'+value;if(!seen.has(uri)){seen.set(uri,aqFiles.length);aqFiles.push({uri,cues:[],file:uri.startsWith('assets/')?uri:'embedded-'+aqFiles.length});}aqFiles[seen.get(uri)].cues.push(cue);}window.aqAnalyser=c.createAnalyser();aqAnalyser.fftSize=2048;BOF_AUDIO_QUALITY_1102.tap().connect(aqAnalyser);return{cues:Object.keys(BOFA.sfx).length,unique:aqFiles.length,functions:Object.keys(Audio.SFX).length,entries:aqFiles.map((f,i)=>({i,file:f.file,cues:f.cues}))};}''')
 state['registry']=inventory;save();print('REGISTRY',inventory['cues'],'cues;',inventory['unique'],'unique sources',flush=True)
 for i in range(0,inventory['unique'],8):
  rows=p.evaluate('''async from=>Promise.all(aqFiles.slice(from,from+8).map(async(f,n)=>{try{const r=await fetch(f.uri);if(!r.ok)throw Error('HTTP '+r.status);const ab=await r.arrayBuffer(),audio=await Snd._audioCtx().decodeAudioData(ab);let peak=0,sum=0,count=0,clipped=0;for(let ch=0;ch<audio.numberOfChannels;ch++){const a=audio.getChannelData(ch);for(let j=0;j<a.length;j+=8){const v=a[j];peak=Math.max(peak,Math.abs(v));sum+=v*v;count++;if(Math.abs(v)>=.9999)clipped++;}}return{i:from+n,file:f.file,cues:f.cues,seconds:audio.duration,rate:audio.sampleRate,peak,rms:Math.sqrt(sum/Math.max(1,count)),clipRatio:clipped/Math.max(1,count),ok:audio.duration>0&&peak>.000001};}catch(e){return{i:from+n,file:f.file,cues:f.cues,ok:false,error:String(e)};}}))''',i)
  state['decoded']+=rows;save()
  if i%40==0:print('DECODE',min(i+8,inventory['unique']),'/',inventory['unique'],flush=True)
 for i,f in enumerate(inventory['entries']):
  cue=f['cues'][0]
  try:
   row=p.evaluate('''async arg=>{
    for(const s of Snd._sfxVoices)try{s.el.pause();}catch(e){}
    const name=arg.cue,uri=aqFiles[arg.i].uri;Snd.prepare(name);const bank=Snd.pools[name];let selected=-1;
    for(let j=0;j<bank.list.length;j++){bank.list[j];if(bank.slots[j].uri===uri){selected=j;break;}}
    if(selected<0)throw Error('Exact registered source missing from native pool');
    const el=bank.list[selected];el.preload='auto';el.load();const until=performance.now()+10000;
    while(el.readyState<3&&performance.now()<until)await new Promise(r=>setTimeout(r,20));
    delete Snd._last[name];bank.i=selected;const accepted=Snd.play(name);let peak=0,sum=0,count=0;
    for(let j=0;j<12;j++){await new Promise(r=>setTimeout(r,25));const a=new Float32Array(aqAnalyser.fftSize);aqAnalyser.getFloatTimeDomainData(a);for(const x of a){peak=Math.max(peak,Math.abs(x));sum+=x*x;count++;}}
    return{cue:name,source:aqFiles[arg.i].file,selectedSource:bank.slots[selected].uri===uri,accepted,advanced:el.currentTime>0,peak,rms:Math.sqrt(sum/Math.max(1,count)),routeErrors:AQ112.errors.slice()};
   }''',dict(cue=cue,i=i))
   row['ok']=bool(row['accepted']and row['advanced']and row['peak']>.000001 and not row['routeErrors'])
  except Exception as e:row=dict(cue=cue,ok=False,error=str(e))
  state['playback'].append(row);save()
  if i%30==0:print('PLAYBACK',i+1,'/',inventory['unique'],'failed',sum(not r['ok']for r in state['playback']),flush=True)
 # Real default-cabinet stress: layered native launches, charge, beams and
 # explosions go through the same output heard by the player and the recorder.
 row=p.evaluate('''async()=>{for(const s of Snd._sfxVoices)try{s.el.pause();}catch(e){}const keys=['enemyMachineGunHeavy','combatEnergy0927','combatBeam0927','bossWeaponCharge','expBig','missile','machineGun','enemyHeavyLaser'];Snd.prepare(keys);await new Promise(r=>setTimeout(r,400));let peak=0,sum=0,count=0,lo=0;for(let j=0;j<45;j++){if(j%4===0)for(const k of keys)Snd.play(k);await new Promise(r=>setTimeout(r,25));const a=new Float32Array(aqAnalyser.fftSize);aqAnalyser.getFloatTimeDomainData(a);for(const x of a){peak=Math.max(peak,Math.abs(x));sum+=x*x;count++;}lo=Math.min(lo,AQ112.bus.compressor.reduction);}return{peak,rms:Math.sqrt(sum/count),reduction:lo,routed:AQ112.routed,errors:AQ112.errors};}''')
 state['stress']=row;state['checks']=[dict(name='Every unique registered SFX source decodes',passed=all(r['ok']for r in state['decoded'])),dict(name='Every unique source has audible real mixer playback',passed=all(r['ok']for r in state['playback'])),dict(name='Default cabinet stress stays audible and below clipping',passed=.001<row['peak']<.9999 and row['rms']>.00001 and not row['errors']),dict(name='No browser or audio routing errors',passed=not state['errors']and not row['errors'])];save();b.close()
print('DONE',len(state['decoded']),'decoded;',len(state['playback']),'played;',sum(c['passed']for c in state['checks']),'/',len(state['checks']),flush=True)
sys.exit(0 if all(c['passed']for c in state['checks'])else 1)
