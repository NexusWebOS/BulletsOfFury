import sys,json,base64
from pathlib import Path
sys.path.insert(0,'D:/BOF-Downloads/2026-11-14/RevG-source/_BUILD_SOURCE')
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[1]/'_shots/opening_1114';errors=[];report={}
def shot(p,n):
 (OUT/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL()').split(',')[1]))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(90000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.goto('http://127.0.0.1:8765/index.html?opening-review=1114',wait_until='load');p.wait_for_function('()=>window.__bofFrames>6');p.evaluate(sh.TRAP_RAF)
 report['boot']=p.evaluate('()=>({module:!!window.BOF_FURY_OPENING_1114,lastErrors:window.__bofLastError||null})');print('BOOT',report['boot'],flush=True)
 p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;FURY14.preview('opening','cole');}")
 p.wait_for_function('()=>fury14Ready(FURY14.openKeys)');p.evaluate(sh.STEP,120);shot(p,'logo')
 report['crawl']=[]
 for t in [15,38,58,79,100]:
  p.evaluate('(t)=>{campaignIntro.t=t;drawCampaignIntro(0);}',t);shot(p,'crawl-'+str(t));report['crawl'].append(p.evaluate('()=>FURY14.last'))
 report['total']=p.evaluate('()=>FURY14.total')
 p.evaluate('()=>{campaignIntro.t=FURY14.total-.05;drawCampaignIntro(.1);}')
 p.wait_for_function('()=>fury14MapReady()');report['map']=[]
 for sec in range(13):
  for _ in range(4):p.evaluate(sh.STEP,15);p.wait_for_timeout(5)
  report['map'].append(p.evaluate('()=>({state,t:FURY14.map?.t,done:FURY14.map?.done,cam:{...cmap2.cam},ship:sselShip&&{x:sselShip.x,y:sselShip.y}})'))
  if sec in [0,3,6,9,12]:shot(p,'map-'+str(sec))
 print('MAP',report['map'][-1],flush=True)
 report['pilots']=[]
 for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
  p.evaluate("p=>{BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';Input.clearTaps();d1110Play('stage1-lost-comms',fury14Rows(p),()=>beginStage(1));}",pk)
  p.wait_for_function('()=>fury14Ready(BOFCinematicDirector.current.d1110Keys)');p.evaluate(sh.STEP,90);shot(p,'pilot-'+pk+'-left')
  p.evaluate("()=>{const s=BOFCinematicDirector.current;s.i=3;s.t=2;s.shown=s.beats[3].text.length;d1110Visual(s.beats[3],s);}");shot(p,'pilot-'+pk+'-right')
  report['pilots'].append(p.evaluate('()=>({...FURY14.last,keysReady:fury14Ready(BOFCinematicDirector.current.d1110Keys)})'))
 # One complete stage1 cinematic through its normal owner and native card callback.
 p.evaluate("()=>{BOFCinematicDirector.cancel();FURY14.preview('stage1','cole');window.reviewSounds=[];const old=Snd.play;Snd.play=function(n,...v){reviewSounds.push(n);return old.call(this,n,...v)}}")
 p.wait_for_function('()=>fury14Ready(BOFCinematicDirector.current.d1110Keys)')
 report['sequence']=[]
 for sec in range(39):
  for _ in range(4):p.evaluate(sh.STEP,15);p.wait_for_timeout(5)
  report['sequence'].append(p.evaluate('()=>({state,last:FURY14.last,scene:BOFCinematicDirector.current?.id})'))
  if sec in [10,12,14,17,25,31,33,34,35,37]:shot(p,'sequence-'+str(sec))
 report['sound']=p.evaluate("()=>({booms:reviewSounds.filter(n=>n==='expBig').length,last:reviewSounds.slice(-8)})")
 # Actual map selection must enter the comic before the native stage card.
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';campaign.rank={};campaign.unlockedMax=1;openStageSelect(1,{});Input.clearTaps();}")
 p.evaluate(sh.STEP,90);p.keyboard.press('Enter');p.evaluate(sh.STEP,100);p.wait_for_timeout(100)
 report['actualDeploy']=p.evaluate("()=>({state,scene:BOFCinematicDirector.current?.id,pending:FURY14.pending,card:!!FURY14.card})")
 shot(p,'actual-deploy')
 # Skip comic uses the same launch continuation once.
 p.evaluate(sh.STEP,30);p.keyboard.press('Enter');p.evaluate(sh.STEP,2)
 report['skip']=p.evaluate("()=>({state,scene:BOFCinematicDirector.current?.id,stage:run.stage})")
 report['errors']=errors;b.close()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'errors':errors,'sounds':report['sound'],'total':report['total'],'last':report['sequence'][-1]},indent=2),flush=True)
assert not errors,errors
assert report['actualDeploy'].get('scene')=='stage1-lost-comms',report['actualDeploy']
assert report['sound']['booms']==1
assert report['skip']['state']=='intro',report['skip']
assert all(r['keysReady'] and r['pilot']==pk for r,pk in zip(report['pilots'],['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']))
