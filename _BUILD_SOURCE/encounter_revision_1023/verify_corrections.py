from pathlib import Path
from playwright.sync_api import sync_playwright
import json
W=Path(__file__).resolve().parent;O=W/'review/media';rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page();p.goto('http://127.0.0.1:62566/corrections/index.html');p.evaluate('document.querySelectorAll("video").forEach(v=>v.remove())')
 for f in sorted(O.glob('*.mp4')):
  row=p.evaluate('''async name=>{
   const v=document.createElement('video');v.muted=true;v.preload='auto';document.body.append(v);let errors=[];v.addEventListener('error',()=>errors.push(v.error?.message));
   const wait=event=>Promise.race([new Promise((resolve,reject)=>{v.addEventListener(event,resolve,{once:true});v.addEventListener('error',()=>reject(new Error(v.error?.message||'media error')),{once:true});}),new Promise((_,reject)=>setTimeout(()=>reject(new Error('media timeout '+event)),12000))]);
   try{v.src=name;await wait('loadedmetadata');const duration=v.duration;await v.play();await wait('timeupdate');v.pause();const first=v.currentTime;v.currentTime=Math.max(0,duration-1.3);await wait('seeked');await v.play();await wait('timeupdate');v.pause();const end=v.currentTime;return {file:name,duration,first,end,decoded:v.webkitDecodedFrameCount,pass:first>0&&end>duration-2&&v.webkitDecodedFrameCount>0,errors};}
   catch(e){return {file:name,pass:false,error:String(e),errors};}finally{v.removeAttribute('src');v.load();v.remove();}
  }''','media/'+f.name)
  rows.append(row);print(('PASS ' if row.get('pass')else 'FAIL ')+f.name,flush=True)
  (W/'corrections-playback.json').write_text(json.dumps({'pass':len(rows)==12 and all(r['pass']for r in rows),'videos':rows},indent=2))
 b.close()
