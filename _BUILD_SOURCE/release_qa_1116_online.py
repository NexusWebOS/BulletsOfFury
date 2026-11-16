from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/online';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];checks=[]
def ck(n,v,data=None):checks.append({'name':n,'ok':bool(v),'data':data});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 c1=b.new_context(viewport={'width':1440,'height':1000});c2=b.new_context(viewport={'width':1440,'height':1000})
 host=c1.new_page();guest=c2.new_page()
 try:
  for label,p in [('host',host),('guest',guest)]:
   p.set_default_timeout(60000);p.on('pageerror',lambda e,label=label:errors.append(label+': '+str(e)))
   p.on('console',lambda m,label=label:errors.append(label+': '+m.text)if m.type=='error'else None)
   p.goto('http://127.0.0.1:8765/index.html?release-net=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate('()=>{BOFOnline.submitScore=()=>{};return BOFOnline.open();}')
   p.wait_for_function('BOFOnline.connected');ck(label+' native anonymous online connection',True)
  for label in ['LEADERBOARD','ANNOUNCEMENTS']:
   host.get_by_role('button',name=label,exact=True).click();host.wait_for_function("!document.querySelector('#bof-online .shell').textContent.includes('LOADING...')")
   text=host.locator('#bof-online .shell').inner_text();ck(label.lower()+' native service read succeeds', 'UNAVAILABLE'not in text)
   host.get_by_role('button',name='BACK',exact=True).click()
  host.get_by_role('button',name='HOST ONLINE',exact=True).click()
  host.wait_for_function("/ROOM READY|ROOM ERROR/.test(document.querySelector('#bof-online .shell').textContent)")
  status=host.locator('#bof-online .shell').inner_text();ck('host UI reaches a room', 'ROOM READY' in status,status)
  host.evaluate("()=>{window.releaseRoomCleanup=[...document.querySelectorAll('#bof-online button')].find(b=>b.textContent==='CLOSE ROOM')?.onclick;}")
  code=host.locator('#bof-online h2').last.inner_text();ck('private room created',len(code)==12)
  guest.get_by_role('button',name='JOIN ONLINE',exact=True).click();guest.get_by_placeholder('12-CHARACTER ROOM CODE').fill(code)
  guest.get_by_role('button',name='JOIN',exact=True).click();guest.wait_for_function("document.querySelector('#bof-online video')?.videoWidth>0")
  host.get_by_role('button',name='START TWO-PILOT RUN',exact=True).click()
  host.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False})
  host.evaluate("()=>{coopOn=true;for(const k of SEAT_RUN_FIELDS)run2[k]=run[k];run2.pilot='decker';p2Index=PILOTS.findIndex(p=>p.key==='decker');PILOTMOD2={...PILOTS[p2Index]};player2.reset();player2.x=worldWidth()/2+45;player2.y=VH-100;player2.dead=player2.out=false;player2.invuln=1e8;player.invuln=1e8;player._spawnClearT=player2._spawnClearT=1e8;stagePlan=[];enemies=[];eBullets=[];spawnClock=1e9;}")
  guest.bring_to_front();guest.evaluate("()=>window.dispatchEvent(new Event('focus'))")
  guest.wait_for_timeout(1000)
  at=host.evaluate('player2.x');guest.keyboard.down('ArrowRight');guest.wait_for_timeout(550);guest.keyboard.up('ArrowRight');guest.wait_for_timeout(350)
  after=host.evaluate('player2.x');ck('remote seat two actually moves over live WebRTC',after>at+15,{'before':at,'after':after})
  guest.keyboard.down('j');guest.wait_for_timeout(180);v=host.evaluate("({held:BOFOnline.remoteHold('fire'),shots:pBullets.filter(b=>b._seat===2||b.seat===2).length})");guest.keyboard.up('j');guest.wait_for_timeout(400)
  ck('remote fire arrives and releases',v['held']and not host.evaluate("BOFOnline.remoteHold('fire')"),v)
  guest.evaluate("async()=>{window.netAudio=new AudioContext();await netAudio.resume();window.netAnal=netAudio.createAnalyser();netAudio.createMediaStreamSource(document.querySelector('#bof-online video').srcObject).connect(netAnal);window.netPeak=0;window.netTimer=setInterval(()=>{const a=new Float32Array(netAnal.fftSize);netAnal.getFloatTimeDomainData(a);for(const v of a)netPeak=Math.max(netPeak,Math.abs(v));},20);}")
  for i in range(4):host.evaluate('()=>Audio.SFX.blip()');guest.wait_for_timeout(240)
  peak=guest.evaluate('()=>{clearInterval(netTimer);return netPeak;}');ck('native mixer sound decodes at the remote client',peak>.0001,{'peak':peak})
  guest.wait_for_timeout(2500)
  m=guest.evaluate("()=>{const v=document.querySelector('#bof-online video'),s=v.srcObject;return{w:v.videoWidth,h:v.videoHeight,muted:v.muted,paused:v.paused,tracks:s.getTracks().map(t=>({kind:t.kind,ready:t.readyState})),frames:v.getVideoPlaybackQuality().totalVideoFrames};}")
  ck('remote video decodes real frames',m['frames']>5 and not m['paused'],m)
  ck('guest receives current full HUD composition',m['w']/m['h']>1.3,m)
  ck('guest receives audible game audio',not m['muted']and any(t['kind']=='audio'and t['ready']=='live'for t in m['tracks']),m)
  host.evaluate('()=>BOFOnline.open()');ck('active room can be reopened and closed without creating another room',host.get_by_role('button',name='CLOSE ROOM',exact=True).count()==1)
  host.get_by_role('button',name='RESUME GAME',exact=True).click();ck('resuming preserves live game state',host.evaluate('state===GS.PLAY'))
  guest.bring_to_front();guest.evaluate("()=>window.dispatchEvent(new Event('focus'))");guest.keyboard.down('ArrowLeft');guest.wait_for_timeout(200);held=host.evaluate("BOFOnline.remoteHold('left')")
  guest.evaluate("()=>window.dispatchEvent(new Event('blur'))");guest.wait_for_timeout(180);ck('focus loss releases remote held keys',held and not host.evaluate("BOFOnline.remoteHold('left')"));guest.keyboard.up('ArrowLeft')
  guest.evaluate("()=>window.dispatchEvent(new Event('focus'))")
  guest.evaluate("()=>{keybind.fire=['pad_b5'];keybind.retina=keybind.retina.filter(k=>k!=='pad_b5');window.netPad={index:2,connected:true,id:'QA raw controller',mapping:'',axes:[0,0],buttons:Array.from({length:18},(_,i)=>({pressed:i===5,value:i===5?1:0}))};Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[null,null,netPad]});}")
  guest.wait_for_timeout(250);v=host.evaluate("({fire:BOFOnline.remoteHold('fire'),retina:BOFOnline.remoteHold('retina')})");ck('online guest honors its native raw controller fire binding',v['fire']and not v['retina'],v)
  guest.evaluate("()=>window.dispatchEvent(new Event('blur'))");guest.wait_for_timeout(200);ck('focus loss releases a held raw controller too',not host.evaluate("BOFOnline.remoteHold('fire')"))
  guest.evaluate("()=>window.dispatchEvent(new Event('focus'))")
  guest.evaluate('()=>{netPad.buttons[5]={pressed:false,value:0};}');guest.wait_for_timeout(200)
  host.screenshot(path=str(O/'host.png'));guest.screenshot(path=str(O/'guest.png'))
  guest.get_by_role('button',name='LEAVE ROOM',exact=True).click()
 except Exception as e:
  errors.append(str(e));print(str(e),flush=True)
  for label,p in [('host',host),('guest',guest)]:
   try:
    print(label+': '+p.locator('#bof-online .shell').inner_text(),flush=True);p.screenshot(path=str(O/(label+'-failure.png')))
   except Exception:pass
 finally:
  # Close this test's room through the native UI/RPC, including failure cleanup.
  try:
   host.evaluate('async()=>{if(window.releaseRoomCleanup)await releaseRoomCleanup();}')
  except Exception:pass
  c1.close();c2.close();b.close()
ck('no page or console errors',not errors,errors)
(O/'report.json').write_text(json.dumps({'scope':'Two independent Chromium contexts, real Supabase anonymous auth/private-room/WebRTC and native seat2 input. Prepared empty Stage1 fixture; not full online campaign, NAT, reconnect or hardware certification.','checks':checks,'errors':errors},indent=2),encoding='utf8')
sys.exit(any(not q['ok']for q in checks)or bool(errors))
