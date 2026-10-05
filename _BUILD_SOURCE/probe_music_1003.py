"""Native encounter music routing, file decoding, and organized catalog verification."""
from pathlib import Path
import json, base64
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/music_1003';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];report={'minibosses':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required','--mute-audio'])
 p=b.new_page(viewport={'width':1100,'height':950});p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.goto('http://127.0.0.1:8794/index.html');p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
 p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50);p.mouse.click(500,500)
 p.evaluate('()=>{window.musicCalls1003=[];const start=Audio.startMusic;Audio.startMusic=function(k){musicCalls1003.push(k);return start.apply(this,arguments);};}')
 report['files']=p.evaluate('''async()=>{const c=await(await fetch('assets/game/music/catalog.json')).json();for(const t of c.tracks){const r=await fetch(t.file,{method:'HEAD'});if(!r.ok)throw Error(t.file);}return c.tracks.length;}''')
 for stage in [4,6,7,9]:
  p.evaluate(SETUP,{'stage':stage});p.evaluate('()=>{warnKind="sub";warnT=.001;updatePlay(.01);}')
  p.wait_for_function('()=>Snd.cur&&Snd.cur.readyState>=2&&!Snd.cur.paused',timeout=30000)
  q=p.evaluate('()=>({stage:run.stage,kind:subBoss.kind,path:Snd.cur.getAttribute("src"),key:musicCalls1003.at(-1),duration:Snd.cur.duration})')
  assert q['key']=='mini'+str(stage) and q['path']==f'assets/game/music/Level{stage}mb.mp3';report['minibosses'].append(q)
 p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
 p.evaluate('()=>{r30Warm();r30Form(B,0);B._r30.mode="morph1003b";B._r30.t=1.64;r30Tick(B,.02);}')
 p.wait_for_function('()=>Snd.cur&&Snd.cur.readyState>=2&&!Snd.cur.paused',timeout=30000)
 report['secondForm']=p.evaluate('()=>({name:B.name,form:B._r30.form,key:musicCalls1003.at(-1),path:Snd.cur.getAttribute("src"),duration:Snd.cur.duration})')
 assert report['secondForm']['form']==1 and report['secondForm']['key']=='boss8p2' and report['secondForm']['path'].endswith('/Level8b2.mp3')
 p.evaluate('()=>{B._r30.mode="morph1003b";B._r30.t=1.64;r30Tick(B,.02);}')
 report['thirdForm']=p.evaluate('()=>({form:B._r30.form,key:musicCalls1003.at(-1)})')
 assert report['thirdForm']=={'form':2,'key':'boss8p3'}
 report['decoded']=p.evaluate('''async()=>{const a=new AudioContext(),out=[];for(const k of ['mini4','mini6','mini7','mini9','boss8p2']){const d=await a.decodeAudioData(await(await fetch(BOFA.music[k])).arrayBuffer());out.push({key:k,seconds:d.duration,channels:d.numberOfChannels});}await a.close();return out;}''')
 assert all(q['seconds']>30 and q['channels']>0 for q in report['decoded'])
 report['unused']=p.evaluate('()=>Object.entries(BOFA.music).filter(([k])=>k.startsWith("unused"))')
 assert not any('/Level' in path for _,path in report['unused'])
 report['errors']=errors
 (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 b.close()
assert not errors,errors
print(json.dumps(report,indent=2))
