"""Decode and hear the actual native hammerLaser shared-mixer route."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_frames_1025';port,stop=serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate("()=>{Snd.prepare(['enemyLaser']);}")
  p.wait_for_function("()=>['enemyLaser'].every(k=>Snd.pools[k]?.list.some(a=>a.readyState>=3))",timeout=60000)
  r=p.evaluate("""async()=>{const c=Snd._audioCtx();await c.resume();const a=c.createAnalyser();a.fftSize=1024;let peak=0,route=[],playing=[];const old=Snd.play,play=HTMLMediaElement.prototype.play;
   Snd.play=function(k){route.push(k);return old.apply(this,arguments)};
   HTMLMediaElement.prototype.play=function(){try{if(this._bofNode)this._bofNode.connect(a);else{const n=c.createMediaElementSource(this);n.connect(c.destination);n.connect(a)}}catch(e){}playing.push({el:this,initial:this.readyState,file:this.src.split('/').at(-1)});return play.apply(this,arguments)};
   try{c26BallLaser(340,120,Math.PI/2,5.8,false);for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,15));const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);for(const v of d)peak=Math.max(peak,Math.abs(v))}}
   finally{Snd.play=old;HTMLMediaElement.prototype.play=play}
   playing=playing.map(v=>({initial:v.initial,ready:v.el.readyState,time:v.el.currentTime,file:v.file}));return{route,playing,peak,passed:peak>.001&&route.length>0&&playing.some(v=>v.ready>=3&&v.time>.05&&v.file==='chip_enemyLaser.mp3')};}""")
  r['errors']=errors;r['passed']=r['passed'] and not errors;(O/'laser-audio.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8');print(json.dumps(r),flush=True);b.close()
finally:stop()
raise SystemExit(0 if r['passed'] else 1)
