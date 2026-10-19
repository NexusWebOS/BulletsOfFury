"""Normal post-Stage6 story, Start skip and the Stage7 entry callback."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_revision_1017/arrival';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof CR17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  row=p.evaluate('''()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(6);BOFCinematicDirector.cancel();run.mode='campaign';run._sewerBriefed17=false;window.arrivalCallbacks=0;window.arrivalStarts=CR17.sewerStarts;
   const ok=BOFCampaignStory.start(6,()=>{arrivalCallbacks++;beginStage(7);setState(GS.LAUNCH);});return{ok,id:BOFCinematicDirector.current.id,beats:BOFCinematicDirector.current.beats.map(b=>({text:b.text,bg:b.bg,flight:b.flight,approach:!!b._sewer17}))};}''')
  check('Normal post-Stage6 continuation starts its existing director',row['ok'] and row['id']=='post-6')
  check('Route recap and upgrades remain before the five flight beats',len(row['beats'])>5 and all(b['approach'] for b in row['beats'][-5:]) and not row['beats'][0]['approach'],row)
  check('Normal continuation includes the river and bridge approach',any(b.get('bg')=='cin_story_river_bridge' for b in row['beats']))
  p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.i=s.beats.length-1;s.t=0;s.shown=0;s.age=.3;}''')
  p.keyboard.press('Enter');p.evaluate('BOFCinematicDirector.tick(1/60)')
  check('Real Start input skips once and invokes the existing Stage7 callback',p.evaluate('arrivalCallbacks===1&&run.stage===7&&state===GS.LAUNCH&&!BOFCinematicDirector.active'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}')
  row=p.evaluate('''()=>{const first=CR17.sewerStarts;drawLaunch(0);drawLaunch(.016);return{callbacks:arrivalCallbacks,starts:CR17.sewerStarts,first,briefed:run._sewerBriefed17,active:BOFCinematicDirector.active,state};}''')
  check('Post-Stage6 launch does not replay an already viewed or skipped approach',row['callbacks']==1 and row['starts']==row['first'] and row['briefed'] and not row['active'],row)
  p.screenshot(path=str(O/'native-entry.png'));br.close()
finally:stop()
check('No page, console or draw errors',not errors,errors)
result=dict(passed=sum(q['passed'] for q in checks),failed=[q for q in checks if not q['passed']],errors=errors,checks=checks)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'failed':len(result['failed']),'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
