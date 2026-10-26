from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_melee_1024';port,stop=serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate("()=>{Snd.prepare(['hammerImpact','hammerThrow']);}")
  p.wait_for_function("()=>['hammerImpact','hammerThrow'].every(k=>Snd.pools[k]?.list.every(a=>a.readyState>=3))",timeout=60000)
  p.evaluate("""async()=>{window.meleeAudio={playing:[],calls:[],peak:0};Snd.vol.master=1;Snd.vol.sfx=.4;const c=window.meleeAudioContext=new AudioContext();await c.resume();window.meleeAnalyzers=[];for(const k of ['hammerImpact','hammerThrow'])for(const a of Snd.pools[k].list){const src=c.createMediaElementSource(a),an=c.createAnalyser();src.connect(an);an.connect(c.destination);meleeAnalyzers.push(an);a.addEventListener('playing',()=>meleeAudio.playing.push({cue:k,decoded:a.readyState,volume:a.volume}));}window.meleeAudioTimer=setInterval(()=>{for(const a of meleeAnalyzers){const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);for(const v of d)meleeAudio.peak=Math.max(meleeAudio.peak,Math.abs(v));}},10);const play=Snd.play;Snd.play=function(k,...args){const accepted=play.call(this,k,...args);if(['hammerImpact','hammerThrow'].includes(k))meleeAudio.calls.push({cue:k,accepted});return accepted;};b20Cue('hammerImpact');}""")
  p.wait_for_timeout(250);p.evaluate("b20Cue('hammerThrow')");p.wait_for_timeout(350)
  d=p.evaluate("()=>({context:meleeAudioContext.state,...meleeAudio})");d['errors']=errors;d['passed']=not errors and d['peak']>0 and len({v['cue'] for v in d['playing']})==2
  (O/'audio-results.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));b.close()
finally:stop()
raise SystemExit(0 if d['passed'] else 1)
