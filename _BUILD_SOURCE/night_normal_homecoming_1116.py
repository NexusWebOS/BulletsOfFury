from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/normal-homecoming';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];runs=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-normal=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 for diff in ['easy','normal']:
  for pk in p.evaluate('PILOTS.map(p=>p.key)'):
   p.evaluate("q=>{BOFCinematicDirector.cancel();debugFight=null;story=null;S113.guard=null;NF100.current=null;NF100.resume=null;run._normalComplete100=null;P2M.active=null;coopOn=false;run.mode='campaign';run.stage=5;curStage=STAGES[4];run.pilot=q.pk;pilotIndex=PILOTS.findIndex(p=>p.key===q.pk);diffKey=q.diff;DIFF=difficultyForRun('campaign',q.diff);campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=5;Input.clearTaps();Input.mouse.down=false;nf100Open(true,false);}",{'pk':pk,'diff':diff})
   p.wait_for_function('()=>{nf100Warm();const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys)&&nf100Warm()}',polling=50)
   q=p.evaluate('''async()=>{const visited=[];let n=0;while(BOFCinematicDirector.current&&n<6000){const s=BOFCinematicDirector.current,b=s.beats[s.i];if(!visited.includes(b.id))visited.push(b.id);BOFCinematicDirector.tick(1/60);if(n%15===0&&BOFCinematicDirector.current)BOFCinematicDirector.draw();if(n%120===0)await new Promise(r=>setTimeout(r,0));n++}drawScene(1/60);return{state,phase:NF100.current?.phase,from:NF100.current?.from,saved:NF100.current?.saved,viewport:[cv.width,cv.height],logical:[cv.width/SS,cv.height/SS],visited,options:nf100Options(NF100.current).map(o=>o.key),copy:NF100.current?.copy,detail:NF100.current?.detail};}''')
   q.update(pilot=pk,difficulty=diff);runs.append(q);checks.append({'name':diff+' '+pk+' homecoming reaches its correctly framed completion choice','ok':q['state']=='normal-finale-1031'and q['phase']=='menu'and q['saved']and q['logical']==[480,512]and q['visited']==['HQ19-LAND','HQ19-EXIT','HQ19-ENTER','HQ19-CORRIDOR','HQ19-WELCOME']and q['options']==(['normal','hard','furious']if diff=='easy'else['hard','furious']),'data':q})
   if pk in['cole','decker','juggernaut']:p.locator('#screen').screenshot(path=str(O/(diff+'-'+pk+'.png')))
 # Use real menu edges from the current Normal choice to a new Furious pilot selection.
 p.evaluate("()=>{NF100.current.t=1;NF100.current.sel=0;Input.clearTaps();Input.injectTap('s')}");p.evaluate(shoot.STEP,1);q=p.evaluate('({state,sel:NF100.current?.sel})');checks.append({'name':'Normal completion D-pad moves to Furious','ok':q['state']=='normal-finale-1031'and q['sel']==1,'data':q})
 p.evaluate("()=>Input.injectTap('j')")
 for i in range(12):p.evaluate(shoot.STEP,6)
 q=p.evaluate('({state,diff:diffKey,mode:run.mode,stage:run.stage,archived:!!JSON.parse(localStorage.getItem(NF100.key)||"null")?.normalComplete100})');checks.append({'name':'Native confirm starts a fresh Furious pilot selection and retains the completed archive','ok':q['state']=='pilot'and q['diff']=='furious'and q['stage']==1 and q['archived'],'data':q})
 checks.append({'name':'No page console or HTTP errors','ok':not errors,'data':errors});b.close()
(O/'report.json').write_text(json.dumps({'checks':checks,'runs':runs,'errors':errors,'scope':'All9 pilots on Easy/Normal prepared completion profiles: actual native HQ19 director into NF100 difficulty-choice callback, viewport and menu-input/archive checks. No earned Chronos clear or complete campaign-win claim.'},indent=2),encoding='utf8');print(json.dumps({'pass':sum(q['ok']for q in checks),'fail':[q['name']for q in checks if not q['ok']]},indent=2));assert all(q['ok']for q in checks)
