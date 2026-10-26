"""Native Chronos radio placement, scrolling, input and continuation regression."""
from pathlib import Path
import base64, json
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF, STEP

R = Path(__file__).resolve().parents[1]
O = R / '_shots/chronos_radio_1024'
O.mkdir(exist_ok=True)
checks, errors = [], []

def ck(name, passed, data=None):
    checks.append(dict(name=name, passed=bool(passed), data=data))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)
    if not passed: print(json.dumps(data), flush=True)

port, stop = serve(str(R))
try:
 with sync_playwright() as pw:
  br = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
  p = br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror', lambda e: errors.append(str(e)))
  p.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?revision=chronos-radio-1024')
  p.wait_for_function('window.__bofFrames>5', timeout=180000)
  p.mouse.click(2,2)
  p.evaluate(TRAP_RAF)
  p.wait_for_timeout(30)
  p.evaluate("""()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;boss.enter=boss._noHit=false;boss.x=worldWidth()/2;boss.y=245;boss._hammer.state='chain_cool';boss._hammer.t=0;boss._cin30Spoke=true;boss._hammer.intro1002=true;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;HT23.speech.length=0;player.invuln=999;setState(GS.PLAY);bi24Warm();}""")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}', timeout=180000)
  p.evaluate(STEP,6)
  # This is the native trap-introduction entry point, with its real done callback.
  p.evaluate('()=>{BOFCinematicDirector.cancel();HT23.speech.length=0;HT23.speechOwner=null;boss._hammer.intro1002=false;fb1002HammerDialogue(boss);}')
  p.evaluate(STEP,60)
  r=p.evaluate("""()=>{const s=BOFCinematicDirector.current,q=ui20Radio();return {id:s?.id,live:s?.combatLive,radio:q,clock:_stage5SpaceScroll,pose:ha21Blue(boss)?.kind,mode:SC12.mode};}""")
  ck('Actual trap introduction reaches external radio',r['id']=='hammer-trap1002' and r['live'] and r['radio']['who']=='CHRONOS',r)
  # Prove the director itself cannot put a portrait/frame over the live actor.
  r=p.evaluate("""()=>{const before=ctx.getImageData(0,0,cv.width,cv.height).data;BOFCinematicDirector.draw();const after=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<after.length;i++)if(after[i]!==before[i])changed++;return changed;}""")
  ck('Live dialogue changes zero playfield pixels',r==0,r)
  before=p.evaluate('()=>({scroll:_stage5SpaceScroll,t:BOFCinematicDirector.current.t,efx:efxClock,x:player.x})')
  p.screenshot(path=str(O/'desktop-intro.png'))
  (O/'scroll-before.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
  p.keyboard.down('d');p.evaluate(STEP,30);p.keyboard.up('d')
  after=p.evaluate('()=>({scroll:_stage5SpaceScroll,t:BOFCinematicDirector.current.t,efx:efxClock,x:player.x})')
  (O/'scroll-after.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
  ck('Starfield scroll and combat clocks continue during speech',after['scroll']>before['scroll']+100 and after['t']>before['t']+.4 and after['efx']>before['efx']+.4,dict(before=before,after=after))
  ck('Native movement input works during speech',after['x']>before['x']+10,dict(before=before['x'],after=after['x']))
  for i in range(180):
   p.evaluate(STEP,6)
   if i%10==0:p.wait_for_timeout(5)
   if not p.evaluate('BOFCinematicDirector.active'):break
  r=p.evaluate('()=>({active:BOFCinematicDirector.active,radio:ui20Radio(),noHit:boss._noHit,state:state,hammer:boss._hammer.state})')
  ck('Trap intro finishes into native fight and clears radio',not r['active'] and r['radio'] is None and not r['noHit'] and r['state']=='play',r)
  for width,height,label in [(1280,800,'desktop'),(480,800,'compact')]:
   p.set_viewport_size({'width':width,'height':height})
   for scene in ['cronos','ht23-announcement-review']:
    p.evaluate("""id=>{BOFCinematicDirector.cancel();HT23.speech.length=0;HT23.speechOwner=boss;window.radioDone=0;BOFCinematicDirector.play(id,[{who:'CHRONOS',art:'fb1002_hammer_portrait',text:'Fury flight. You will never break my chromium armor.'},{who:'COLE',text:'Then we will find another way through.'}],()=>radioDone++,true);player.invuln=999;}""",scene)
    p.evaluate(STEP,30)
    r=p.evaluate("""()=>{SC12.fit();SC12.render();const f=cv.getBoundingClientRect(),hud=(SC12.mode==='compact'?SC12.compact:SC12.panels[0]),h=hud.getBoundingClientRect(),outside=h.right<=f.left||h.left>=f.right||h.top>=f.bottom||h.bottom<=f.top;return{mode:SC12.mode,outside,radio:UI20.radio,field:{x:f.x,y:f.y,w:f.width,h:f.height},hud:{x:h.x,y:h.y,w:h.width,h:h.height}};}""")
    ck(label+' '+scene+' radio is outside the entire playfield',r['outside'] and r['radio'] and r['radio']['who']=='CHRONOS',r)
    p.screenshot(path=str(O/(label+'-'+scene+'.png')))
    # Advance through both speakers with native clocks; callback fires once.
    seen=set()
    for i in range(160):
     q=p.evaluate('ui20Radio()')
     if q:seen.add(q['who'])
     p.evaluate(STEP,6)
     if i%10==0:p.wait_for_timeout(5)
     if not p.evaluate('BOFCinematicDirector.active'):break
    p.evaluate(STEP,12)
    r=p.evaluate('()=>({active:BOFCinematicDirector.active,radio:ui20Radio(),done:radioDone})')
    ck(label+' '+scene+' both speakers finish once without stale radio',seen=={'CHRONOS','COLE'} and not r['active'] and r['radio'] is None and r['done']==1,r)
  # Tactical announcements must still launch through their real queue owner.
  p.evaluate("()=>{HT23.speech.length=0;ht23Say(boss,'Chromium armor, activated!');}")
  p.evaluate(STEP,12)
  r=p.evaluate('()=>({id:BOFCinematicDirector.current?.id,radio:ui20Radio()})')
  ck('Native tactical queue uses the same HUD radio',r.get('id','').startswith('ht23-announcement-') and bool(r['radio']),r)
  # The arrival has a separate historical owner; exercise it without deleting
  # fb2Intro as the earlier isolated director checkpoints did.
  for width,height,label in [(1280,800,'desktop'),(480,800,'compact')]:
   p.set_viewport_size({'width':width,'height':height})
   r=p.evaluate("""()=>{BOFCinematicDirector.cancel();HT23.speech.length=0;fb2IntroStart(boss);SC12.fit();SC12.render();const f=cv.getBoundingClientRect(),h=(SC12.mode==='compact'?SC12.compact:SC12.panels[0]).getBoundingClientRect(),before=ctx.getImageData(0,0,cv.width,cv.height).data;fb2IntroDraw();const after=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<after.length;i++)if(after[i]!==before[i])changed++;return{changed,radio:UI20.radio,outside:h.right<=f.left||h.left>=f.right||h.top>=f.bottom||h.bottom<=f.top};}""")
   ck(label+' historical arrival owner also leaves playfield pixels untouched',r['changed']==0 and r['outside'] and r['radio']['who']=='COLE',r)
   p.screenshot(path=str(O/(label+'-arrival-owner.png')))
  p.evaluate("()=>{HT23.speech.length=0;ht23Say(boss,'Chromium armor, activated!');}")
  p.evaluate(STEP,6)
  before=p.evaluate('()=>({text:fb2Intro.t,scroll:_stage5SpaceScroll})')
  p.evaluate(STEP,30)
  after=p.evaluate('()=>({text:fb2Intro.t,scroll:_stage5SpaceScroll})')
  ck('Tactical interruption preserves arrival reading time while scrolling continues',after['text']==before['text'] and after['scroll']>before['scroll']+100,dict(before=before,after=after))
  ck('No page or console errors',not errors,errors)
  br.close()
finally:
 stop()

# Independent real-frame comparison at the far edge, away from either actor.
from PIL import Image, ImageChops
a=Image.open(O/'scroll-before.png').convert('RGB');b=Image.open(O/'scroll-after.png').convert('RGB')
region=(0,120,min(65,a.width),min(a.height,420))
changed=sum(1 for px in ImageChops.difference(a.crop(region),b.crop(region)).getdata() if max(px)>12)
ck('Captured starfield pixels visibly move during speech',changed>500,changed)
result=dict(checks=checks,errors=errors,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))
(O/'results.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(dict(passed=result['passed'],failed=result['failed'])),flush=True)
raise SystemExit(0 if not result['failed'] else 1)
