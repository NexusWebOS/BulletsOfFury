from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF, STEP
R=Path(__file__).resolve().parents[1]
O=R/'_shots/citylife_1025'; O.mkdir(exist_ok=True)
port,stop=serve(str(R)); errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1280,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html')
  p.wait_for_function('window.__bofFrames>5',timeout=180000)
  p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("""()=>{debugStartFight({stage:1,role:'boss',kind:'helicopter'},{pilot:'cole'});setState(GS.STAGECLEAR);drawStageClear._init=false;}""")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000,polling=100)
  p.evaluate('()=>{setState(GS.STAGECLEAR);drawStageClear._init=false;drawStageClear(1/60);} ')
  p.evaluate(STEP,5)
  p.wait_for_function('Snd.cur===Snd.music.stageclear&&Snd.cur.currentTime>.2',timeout=60000,polling=100)
  result=p.evaluate("""async()=>{const m=Snd.music.stageclear,c=new AudioContext();await c.resume();const bytes=await(await fetch(m.src)).arrayBuffer(),a=await c.decodeAudioData(bytes);let peak=0;for(const v of a.getChannelData(0))peak=Math.max(peak,Math.abs(v));return {state:gameState,src:m.src,duration:m.duration,decodedDuration:a.duration,peak,loop:m.loop,playing:!m.paused,time:m.currentTime,password:Snd.music.password.src};}""".replace('state:gameState,',''))
  p.screenshot(path=str(O/'stats.png'))
  p.wait_for_timeout(1200)
  result['advanced']=p.evaluate('Snd.cur.currentTime')>result['time']+.5
  p.evaluate("Audio.startMusic('title')")
  result['stopsOnExit']=p.evaluate('Snd.music.stageclear.paused&&Snd.cur===Snd.music.title')
  result['errors']=errors
  result['passed']=result['decodedDuration']>59.7 and result['peak']>.01 and result['advanced'] and result['stopsOnExit'] and not errors
  (O/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
  print(json.dumps(result));b.close()
finally:stop()
raise SystemExit(0 if result['passed'] else 1)
