"""Real-time Stage5 encounter capture, including the native external HUD."""
from pathlib import Path
import json, subprocess, time, sys
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve

R=Path(__file__).resolve().parents[1]
ordered='--ordered' in sys.argv
melee=next((s.split('=',1)[1] for s in sys.argv if s.startswith('--melee=')),None)
O=R/('_shots/chronos_melee_1024/'+melee if melee else '_shots/chronos_intro_order_1024' if ordered else '_shots/chronos_radio_1024')
O.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(R))
errors=[];timeline=[];last=''
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  context=br.new_context(viewport={'width':1280,'height':800},record_video_dir=str(O/'raw'),record_video_size={'width':1280,'height':800})
  p=context.new_page()
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1&revision=chronos-radio-recording-1024')
  p.wait_for_function('window.__bofFrames>5',timeout=180000)
  p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
  print('Stage5 assets decoded; starting native encounter recording.',flush=True)
  p.evaluate("""()=>{window.recordFieldDialogue={count:0,lines:[]};const draw=dlgBox;dlgBox=function(o){if(state===GS.PLAY&&run.stage===5){recordFieldDialogue.count++;if(!recordFieldDialogue.lines.some(l=>l.who===o.who&&l.text===o.full))recordFieldDialogue.lines.push({who:o.who,text:o.full});}return draw.apply(this,arguments);};}""")
  if melee:
   p.evaluate("""()=>{window.meleeTrace=[];const hit=b20HitSegment;b20HitSegment=function(b,from,to,r,label,seen){if(b===boss&&/Hammer/.test(label)){meleeTrace.push({time:efxClock,label,from:{...from},to:{...to},r,player:{x:player.x,y:player.y},distance:s81003Distance(player.x,player.y,{x:from.x,y:from.y,ex:to.x,ey:to.y})});}return hit.apply(this,arguments);};}""")
  # Enter through the normal debug encounter route, retaining the native alert,
  # ship entrance, transformation, dialogue and attack sequence. No forced poses.
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});player.invuln=999;}")
  began=time.monotonic();next_move=0;moving=None;firing=False;speech_shots=0
  while time.monotonic()-began<(100 if melee else 65):
   elapsed=time.monotonic()-began
   p.evaluate('player.invuln=999')
   if elapsed>=next_move:
    if moving:p.keyboard.up(moving)
    moving='a' if moving=='d' else 'd';p.keyboard.down(moving);next_move=elapsed+2.0
   if elapsed>12 and not firing:p.keyboard.down('j');firing=True
   row=p.evaluate("""()=>{const s=BOFCinematicDirector.current,q=ui20Radio(),f=cv.getBoundingClientRect(),h=SC12.panels[0].getBoundingClientRect();return {time:efxClock,state,stage:run.stage,scroll:_stage5SpaceScroll,actor:boss?._hammer?.state,hp:boss?.hp,intro:fb2IntroActive(),armor:!!fr27Armor(boss)?.activated,speech:s?.id||(fb2IntroActive()?'arrival-conversation':null),beat:s?.i??fb2Intro?.i,radio:q,fieldDialogue:recordFieldDialogue.count,mode:SC12.mode,hudOutside:h.right<=f.left||h.left>=f.right||h.top>=f.bottom||h.bottom<=f.top};}""")
   row['videoSeconds']=round(elapsed,3);timeline.append(row)
   key=json.dumps([row.get('actor'),row.get('speech'),row.get('beat'),row.get('radio',{}).get('who') if row.get('radio') else None])
   if key!=last:
    print(json.dumps(row),flush=True);last=key
    if row.get('radio'):
     speech_shots+=1;p.screenshot(path=str(O/f'recording-speech-{speech_shots:02}.png'))
   p.wait_for_timeout(500)
  p.keyboard.up('j')
  if moving:p.keyboard.up(moving)
  p.screenshot(path=str(O/'recording-end.png'))
  duration=time.monotonic()-began
  trace=p.evaluate('window.meleeTrace||[]')
  video=p.video
  await_path=O/'stage5-chronos-raw.webm'
  p.close();video.save_as(str(await_path));context.close();br.close()
finally:
 stop()

reader=imageio_ffmpeg.read_frames(str(await_path));meta=next(reader);reader.close()
trim=max(0,meta['duration']-duration)
mp4=O/'stage5-chronos-speaking.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-ss',str(trim),'-i',str(await_path),'-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
spoken=[q for q in timeline if q.get('radio')]
pairs=[(a,b) for a,b in zip(timeline,timeline[1:]) if a.get('speech') and b.get('speech') and a['speech']==b['speech']]
checks={
 'native Stage5 encounter':all(q['stage']==5 and q['state']=='play' for q in timeline),
 'Chronos speaks in recording':len(spoken)>=4,
 'radio outside playfield for all speech samples':bool(spoken) and all(q['hudOutside'] for q in spoken),
 'no dialogue box drawn over the field in any recorded frame':all(q['fieldDialogue']==0 for q in timeline),
 'native arrival conversation also recorded':any(q.get('speech')=='arrival-conversation' for q in timeline),
 'scroll advances throughout speech':bool(pairs) and all(b['scroll']>a['scroll'] for a,b in pairs),
 'no page or console errors':not errors,
}
if ordered:
 intro=[q for q in timeline if q['intro']]
 charge=[q for q in timeline if q.get('actor')=='fr_activation']
 attacks=[q for q in timeline if q.get('actor') not in [None,'flyby','return','unfold','hammer','fr_activation']]
 checks['Chronos waits throughout the beginning dialogue']=bool(intro) and all(q.get('actor')=='unfold' and not q['armor'] for q in intro)
 checks['visible armor charge follows dialogue and precedes first attack']=bool(charge) and bool(attacks) and charge[0]['time']>intro[-1]['time'] and attacks[0]['time']>charge[-1]['time'] and attacks[0]['armor']
report={'duration':duration,'rawDuration':meta['duration'],'trimStart':trim,'video':str(mp4.relative_to(R)),'audio':'Video only; native browser recorder does not capture audio.','difficulty':'furious','pilot':'cole','invulnerability':True,'route':'Native debug Stage5 boss encounter; no pose/attack/dialogue injections.','checks':checks,'errors':errors,'timeline':timeline}
if melee:report['meleeTrace']=trace
(O/'recording.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps({'checks':checks,'duration':duration,'video':str(mp4)}),flush=True)
raise SystemExit(0 if all(checks.values()) else 1)
