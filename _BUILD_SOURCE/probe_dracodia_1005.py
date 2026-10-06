"""Native cinematic progression, exact dialogue, audio, all seats and sole reward."""
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import json,base64,io,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[],'clips':[]};errors=[];port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n,render=True):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(6)
def raw(p):return base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 d=raw(p);(O/(n+'.png')).write_bytes(d);report['screens'].append(n);return Image.open(io.BytesIO(d)).convert('RGB')
def reel(p,n,seconds,fps=5):
 ims=[]
 for i in range(seconds*fps):
  ticks(p,60//fps);ims.append(Image.open(io.BytesIO(raw(p))).convert('RGB').resize((480,512)))
  if n=='dracodia-destruction' and i in [8,13,21,24,27,30,34,38,44,53,67]:shot(p,'death-pose-'+str(i))
 ims[0].save(O/(n+'.gif'),save_all=True,append_images=ims[1:],duration=1000//fps,loop=0,optimize=False);report['clips'].append({'name':n,'seconds':seconds,'fps':fps,'audio':False})
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate('()=>{dr5Warm();aa5Warm();on5Log("dr5-probe");r30Warm();}')
  p.wait_for_function('()=>Object.values(DR5_ART).every(a=>a.every(c=>XART.rdy(c.key)))',timeout=120000,polling=50)
  ck(True,'all 55 alpha component portrait effect and portal cells decode')
  # Keep native aliases at their actual XART/canvas entry points for draw evidence.
  p.evaluate('()=>{window.calls=[];const get=XART.get,draw=ctx.drawImage,map=new Map();XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)calls.push(k);return draw.apply(this,arguments);};}')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.S=B._r30;window.J=j3State(B);on5FightStart(B);window.shipStart=player.y;window.scoreStart=run.score;player.invuln=0;B._lastPart=B.parts[0];modularHit(B.hp+1);}')
  ck(p.evaluate('()=>S.mode==="encounterFall1003j"&&J.encounter===0&&!S.rewarded'),'actual first life damage starts destruction without stage rewards')
  reel(p,'first-destruction-reform',11);shot(p,'first-reform')
  ck(p.evaluate('()=>player.y<shipStart&&DR5.events.some(q=>q.event==="reformBegins")'),'player flies ahead while opaque destruction and organic reform continue')
  ck(p.evaluate('()=>DR5.events.some(q=>q.text==="What in the world is that..")&&DR5.events.some(q=>q.text==="It\'s...Reforming?!")'),'first reform retains both exact requested radio lines')
  ticks(p,240);ck(p.evaluate('()=>J.encounter===1&&S.mode==="fight"'),'first reform hands off to the actual ghost encounter')
  p.evaluate('()=>{player.invuln=0;B._lastPart=B.parts[0];modularHit(B.hp+1);}')
  reel(p,'ghost-destruction-reform',13);shot(p,'second-reform')
  ck(p.evaluate('()=>DR5.events.some(q=>q.text===".......")&&DR5.events.some(q=>q.text==="No amount of training could ever have prepared me for this.")'),'second reform retains exact disbelief lines')
  ticks(p,500);shot(p,'dracodia-monologue')
  ck(p.evaluate('()=>J.encounter===2&&S.mode==="dr5Monologue"&&j3State(B).dr5.introWanted&&AA5.draws.code>0'),'third encounter reveals Dracodia in animated black and green arena')
  # Held shoot/retina/special input cannot skip radio, move a seat, create shots or hurt either pilot.
  p.evaluate('()=>{window.D=dr5State(B);window.lineBefore=D.line;window.xy=[player.x,player.y];window.livesBefore=run.lives;player.invuln=0;for(const k of ["a","enter","z","c","u","k","w"])Input.keys[k]=true;pShoot();playerHit("fusionOvercharge");}')
  ticks(p,35)
  ck(p.evaluate('()=>run.lives===livesBefore&&pBullets.length===0&&eBullets.length===0&&player.x===xy[0]&&D.line===lineBefore'),'held action keys cannot skip attack or damage protected dialogue')
  p.evaluate('()=>{for(const k in Input.keys)Input.keys[k]=false;}')
  # Compare fixed expression with alternating speech: any changed pixels must be in the mouth rectangle.
  for f in range(9):
   result=p.evaluate('(f)=>{const a=dr5Portrait(f,1),b=dr5Portrait(f,2),d=dr5Portrait(f,0);const A=a.getContext("2d").getImageData(0,0,a.width,a.height).data,B=b.getContext("2d").getImageData(0,0,b.width,b.height).data;let changed=0,outside=0;for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++){const i=(y*a.width+x)*4;if(A.slice(i,i+4).some((q,j)=>q!==B[i+j])){changed++;if(x<165||x>=261||y<241||y>=329)outside++;}}return{changed,outside,w:a.width,h:a.height,base:!!d};}',f)
   ck(result['changed']>0 and result['outside']==0 and result['base'],'expression '+str(f)+' speaks only inside stable mouth and complete frame')
  reel(p,'dracodia-speech',18);shot(p,'split-maw-speech')
  # Dedicated sample: check the actual voice progresses after the native play call, no generic fallback.
  p.evaluate('()=>{Snd._last.dracodiaShriek=0;Audio.SFX.dracodiaShriek();}');p.wait_for_timeout(500)
  audio=p.evaluate('()=>({uri:BOFA.sfx.dracodiaShriek,voices:Snd.pools.dracodiaShriek.slots.filter(Boolean).map(v=>({time:v.el.currentTime,ready:v.el.readyState,paused:v.el.paused,error:v.el.error?.code||null}))})');report['audio']=audio
  ck(any(v['time']>.05 and v['ready']>=3 and not v['error'] for v in audio['voices']),'dedicated processed shriek advances in a real HTMLAudio voice')
  for i in range(240):
   ticks(p,10)
   if p.evaluate('()=>S.mode==="fight"'):break
  ck(p.evaluate('()=>S.mode==="fight"&&D.introSeen&&!player.dead&&DR5.events.filter(q=>q.event==="dracodiaSpeechBegin").length===1'),'twelve timed speech beats return to live combat exactly once')
  # No false extra outer life. All copied pools are depleted through their damage owner for final kill.
  p.evaluate('()=>{for(let i=1;i<J.hp.length;i++)J.hp[i]=0;J.active=0;J.mimic=null;S.finale1003b=false;S.mode="fight";B.enter=false;B.hp=J.hp[0]=1;B._lastPart=B.parts[0];modularHit(10);}')
  ck(p.evaluate('()=>S.mode==="dr5Death"&&DR5.events.some(q=>q.text==="You. Are. Terminated!")'),'actual last-pool hit begins Dracodia death and exact final line')
  shot(p,'death-shriek');reel(p,'dracodia-destruction',16);shot(p,'portal-open')
  events=p.evaluate('()=>DR5.events.map(q=>q.event)');report['events']=p.evaluate('()=>DR5.events');
  ck(all(n in events for n in ['death-arms-up','death-arms-down','death-thrash','death-head-left','death-head-right','death-head-up','death-head-down','death-head-shocked','death-head-rupture','death-twin-sunbeams','death-disintegrate','death-terminal-flash']),'death performs full arm head sun rupture disintegration and terminal sequence')
  ck(p.evaluate('()=>DR5.draws.sunbeam>0&&DR5.draws.charred>0&&DR5.draws.effects>0&&D.bodyGone'),'native sun beams charred decals and explosive reels render before body is removed')
  reel(p,'portal-home',10);shot(p,'sewer-reunion')
  ck(p.evaluate('()=>S.mode==="reunion"&&run._realmReturned&&DR5.draws.portal>0&&!S.rewarded'),'portal closes and hands off to original unawarded sewer reunion')
  for i in range(33):
   ticks(p,10)
   if p.evaluate('()=>state===GS.STAGECLEAR'):break
  report['rewardState']=p.evaluate('()=>({state,clear:GS.STAGECLEAR,mode:S.mode,t:S.t,rewarded:S.rewarded,history:S.history.slice(-8)})')
  ck(p.evaluate('()=>state===GS.STAGECLEAR&&S.rewarded&&run._trueFinaleCleared&&S.history.filter(q=>q.event==="complete").length===1'),'original reunion awards the finale exactly once')
  ticks(p,400);ck(p.evaluate('()=>S.rewarded&&S.history.filter(q=>q.event==="complete").length===1'),'later flyover never repeats finale rewards')
  # Copy practice never repeats the monologue when coming back to Dracula.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'decker','diff':'hard'});p.evaluate('()=>{j3Encounter(B,2);j3Mimic(B,5);window.S=B._r30;window.J=j3State(B);j3Home(B);}')
  ticks(p,170);ck(p.evaluate('()=>S.mode!=="dr5Monologue"&&dr5State(B).introSeen'),'copied-form practice skips full introduction on return')
  # Every seat gets its own coordinates and protection; no teleport to P1.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':'normal'});p.evaluate('()=>{coopOn=true;withSeat(2,()=>{player.reset();player.x=worldWidth()/2+95;player.y=VH-135;});on5FightStart(B);B._lastPart=B.parts[0];modularHit(B.hp+1);window.S=B._r30;window.D=dr5State(B);}')
  ticks(p,220);ck(p.evaluate('()=>D.ships.length===2&&D.ships.every(q=>withSeat(q.seat,()=>player.x===q.x&&player.y<q.y&&!player.dead))'),'co-op reform travel preserves and protects two independent ships')
  p.evaluate(SETUP,{'stage':1,'pilot':'cole'});ck(p.evaluate('()=>!dr5Locked()&&DR5.events.length===0&&whiteBlast===0'),'new mission clears cinematic radio flags and terminal flash')
  ck(not errors,'zero page or draw errors');br.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(q['ok'] for q in report['checks']) and not errors else 1)
