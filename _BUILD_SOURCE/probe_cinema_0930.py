import sys,json,base64,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
OUT=ROOT/'_shots/cinema_0930';OUT.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
def ok(v,n,d=None):
 results.append(dict(ok=bool(v),name=n,detail=d));print(('OK ' if v else 'FAIL ')+n, d or '',flush=True)
def grab(p,n):
 p.evaluate(sh.STEP,1)
 (OUT/(n+'.png')).write_bytes(base64.b64decode(p.evaluate("()=>cv.toDataURL('image/png')").split(',')[1]))
SETUP="""c=>{BOFCinematicDirector.cancel();ht27Stop();debugFight=null;diffKey='furious';DIFF=DIFFS.furious;run.mode='campaign';run.pilot=c.pilot||'yuri';beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;s6Wing=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;if(gravityMode)gravityMode.phase='active';return true;}"""
port,stop=sh.serve(str(ROOT))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1280,'height':800})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
 p.goto('http://127.0.0.1:%s/index.html'%port,timeout=120000);p.wait_for_function('()=>(window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
 p.evaluate(SETUP,{'stage':5})
 r=p.evaluate("""()=>{const keys=new Set();const D=BOFCinematicDirector;for(const pk of PILOTS.map(p=>p.key))for(let s=1;s<=9;s++)for(const b of D.script(s,pk)){keys.add(b.bg||'cin_story_lab_empty');const k=D.artFor(b);if(k)keys.add(k);}for(const k of ['cin30_cronos','cin30_decker','cin30_yuri','dlg_window','pad_a','pad_start'])keys.add(k);window.cin30Keys=[...keys];return {missing:[...keys].filter(k=>!XART._src[k]&&!BOFX.cells[k]),count:keys.size};}""")
 ok(not r['missing'],'all story scene keys are registered',r)
 p.wait_for_function("()=>cin30Keys.every(k=>XART.rdy(k))",timeout=120000)
 for pk in ['axel','freezer','lizzie','falva','yuri','maverick','cole','decker','juggernaut']:
  p.evaluate("""pk=>{BOFCinematicDirector.cancel();run.pilot=pk;BOFCinematicDirector.start(5,()=>{window.cinDone=(window.cinDone||0)+1;setState(GS.STAGESEL)});const D=BOFCinematicDirector,S=D.current;S.i=S.beats.findIndex(b=>b.who===pk.toUpperCase()&&b.location==='lab');S.t=4;S.shown=S.beats[S.i].text.length;drawCutsceneState(0);}""",pk)
  grab(p,'upgrade_'+pk)
  ok(p.evaluate("pk=>BOFCinematicDirector.current.beats.some(b=>b.who===pk.toUpperCase()&&b.location==='lab')",pk),pk+' has an individual upgrade conversation')
 p.evaluate("""()=>{const D=BOFCinematicDirector,S=D.current;S.i=S.beats.findIndex(b=>b.art==='cin30_decker');S.t=4;S.shown=S.beats[S.i].text.length;drawCutsceneState(0);}""");grab(p,'decker_chaingun')
 # Use real keyboard input through the engine's frame loop.
 p.evaluate("()=>{const S=BOFCinematicDirector.current;S.i=0;S.t=0;S.age=1;S.shown=0;window.cinDone=0;Input.clearTaps();}")
 fire=p.evaluate("()=>keybind.fire.find(k=>!k.startsWith('mouse')&&!k.startsWith('pad'))||' '")
 def tap(k):
  key='Space' if k==' ' else 'Enter' if k=='enter' else k
  p.keyboard.down(key);p.evaluate(sh.STEP,1);p.keyboard.up(key);p.evaluate(sh.STEP,1)
 tap(fire);r=p.evaluate("()=>({i:BOFCinematicDirector.current?.i,shown:BOFCinematicDirector.current?.shown,n:BOFCinematicDirector.current?.beats[0].text.length})")
 ok(r['i']==0 and r['shown']==r['n'],'A/fire reveals entire current line',r)
 tap(fire);ok(p.evaluate('()=>BOFCinematicDirector.current?.i===1'),'second A advances exactly one dialogue beat')
 tap('enter');ok(p.evaluate('()=>!BOFCinematicDirector.active&&window.cinDone===1'),'Start skips the scene and runs continuation exactly once')
 # Cronos triggers at the actual unfold state, not HAMMER/HAMA.
 p.evaluate(SETUP,{'stage':5})
 p.evaluate("()=>{spawnBoss('chromehammer');bossActive=true;boss._hammer.state='unfold';boss._hammer.t=.7;boss.x=VW/2;boss.y=VH*.32;hammerBossTick(boss,.016);}")
 ok(p.evaluate("()=>BOFCinematicDirector.current?.id==='cronos'&&boss.name==='CRONOS'"),'campaign robot reveal opens Cronos transmission')
 p.evaluate("()=>{BOFCinematicDirector.current.t=4;BOFCinematicDirector.current.age=1;BOFCinematicDirector.current.shown=999;drawWorld(0);}");grab(p,'cronos_live')
 tap('enter');ok(p.evaluate('()=>!BOFCinematicDirector.active&&state===GS.PLAY'),'Start returns directly to Cronos fight, not pause menu')
 for route in ['hammer','hama']:
  p.evaluate(SETUP,{'stage':5});r=p.evaluate("r=>{ht27Pending=true;hamaPending=r==='hama';startRun(5);setState(GS.PLAY);boss._hammer.state='unfold';boss._hammer.t=.7;hammerBossTick(boss,.016);return !BOFCinematicDirector.active;}",route)
  ok(r,route+' music mode never interrupted by campaign speech')
 # Branch choice is deferred until its conversation completes; sky keeps scrolling.
 p.evaluate(SETUP,{'stage':6});p.evaluate("()=>{s6WingInit();s6Wing.choice=true;fr27ChooseRoute(s6Wing,'left');BOFCinematicDirector.current.age=1;}")
 p.wait_for_function("()=>XART.rdy(stageMasterKey(_levelCfg()))",timeout=120000)
 ok(p.evaluate("()=>BOFCinematicDirector.current?.id==='route-left'&&!s6Wing.autoRoute"),'Harrier briefing precedes route commit')
 p.evaluate("()=>{BOFCinematicDirector.current.t=4;BOFCinematicDirector.current.shown=999;drawWorld(0);}");grab(p,'harrier_route')
 before=p.evaluate('()=>mapScroll');p.evaluate(sh.STEP,30);after=p.evaluate('()=>mapScroll')
 ok(after!=before,'Stage 6 terrain continues during route dialogue',{'before':before,'after':after})
 tap('enter');ok(p.evaluate("()=>!BOFCinematicDirector.active&&s6Wing.autoRoute==='left'&&state===GS.PLAY"),'Start commits selected Harrier route once')
 # Stage X introduction uses the selected rival, not all five ships.
 p.evaluate(SETUP,{'stage':6});p.evaluate("()=>{spawnBoss('rebelsquad');bossActive=true;const R=boss._rebels;R.frStageX=true;for(const q of R.ships)q.dead=q.key!=='nyx';rebelSquadTick(boss,2.6);BOFCinematicDirector.current.age=1;BOFCinematicDirector.current.i=1;BOFCinematicDirector.current.t=4;BOFCinematicDirector.current.shown=999;drawWorld(0);}");p.wait_for_function("()=>XART.rdy('rr_portrait_nyx')");grab(p,'stage_x_nyx')
 ok(p.evaluate("()=>BOFCinematicDirector.current?.id==='stage-x-nyx'"),'Stage X briefing identifies the actual rival')
 tap('enter');p.evaluate("()=>rebelSquadTick(boss,.016)")
 ok(p.evaluate('()=>!BOFCinematicDirector.active&&boss._rebels.frIntro.done&&!boss._noHit'),'Stage X skip releases real combat')
 # Use the actual post-stat exits, including the two exits which bypass HQ.
 for st in [5,7,9]:
  p.evaluate(SETUP,{'stage':st})
  r=p.evaluate("st=>{campaign.unlockedMax=st===9?7:st;run.score=100;scLeaveStage({bonus:25,rank:'A'});return {id:BOFCinematicDirector.current?.id,score:run.score};}",st)
  ok(r['id']=='post-'+str(st),'Stage '+str(st)+' real exit enters the mission bridge',r)
  p.evaluate('()=>BOFCinematicDirector.current.age=1');tap('enter')
  r=p.evaluate("()=>({state,score:run.score,next:campaign.unlockedMax,pending:campaign._l78Pending})")
  ok(r['state']=='stagesel' and r['score']==125 and (st!=7 or r['pending']==1),'Stage '+str(st)+' skip returns to map with bonus awarded once',r)
 # Start can exit the original opening before slow art decodes; A only moves a talk beat.
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.pilot='axel';campaignIntroStart(()=>setState(GS.STAGESEL));campaignIntro.ready=true;campaignIntro.t=1;stateT=1;}")
 before=p.evaluate('()=>campaignIntro.t');tap(fire)
 ok(p.evaluate('()=>!!campaignIntro&&state===GS.CAMPAIGNINTRO&&campaignIntro.t>1'),'opening A reveals/advances dialogue without skipping the prologue')
 tap('enter');ok(p.evaluate('()=>!campaignIntro&&state===GS.STAGESEL'),'opening Start skips to its continuation')
 # The review UI uses the same engine without completing a mission or granting rewards.
 p.goto('http://127.0.0.1:%s/cinematic-review.html'%port,timeout=120000)
 p.wait_for_function("()=>!document.querySelector('#play').disabled",timeout=120000)
 p.select_option('#pilot','decker');p.select_option('#scene','post-5');p.click('#play')
 p.wait_for_function("()=>document.querySelector('#game').contentWindow.BOFCinematicDirector.current?.id==='preview-post-5'")
 ok(True,'review screen starts chosen scene in the shared engine')
 p.click('#next');p.click('#next');p.click('#skip')
 ok(p.evaluate("()=>!document.querySelector('#game').contentWindow.BOFCinematicDirector.active"),'review Next/Skip controls operate the same director')
 ok(not errors,'no page/console errors',errors[:15]);b.close()
stop();(OUT/'results.json').write_text(json.dumps(results,indent=2));sys.exit(0 if all(r['ok'] for r in results) else 1)
