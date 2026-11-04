"""Native campaign continuations, using real settlement/route/save owners, no preview entry."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';V=D/'verification/revision9';V.mkdir(exist_ok=True)
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(D));import review_server
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
if '--installed'in sys.argv:review_server.INJECT='';review_server.OVERLAY=D/'_no_overlay'
checks=[];errors=[];missing=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else 'FAIL ')+name,flush=True)
def shot(p,name):
 (V/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
port,stop=review_server.serve()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(e.stack));p.on('response',lambda r:missing.append(r.url)if r.status>=400 else None)
  p.on('console',lambda m:errors.append(m.text[:600])if 'draw error'in m.text.lower()else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.BOF_STORY_1103?.revision===9&&window.__bofFrames>4')
  p.evaluate('''()=>{const saved=run.pilot,keys=new Set();for(const pilot of S113.casts){run.pilot=pilot;for(const n of[2,3,4,5,6])for(const k of s113Keys(s113Script(n,pilot)))keys.add(k);for(const n of['landing-'+pilot,'dish-exit','pad-exit'])keys.add('s113_'+n);}run.pilot=saved;nf100Warm();window.__campaignKeys=[...keys];for(const k of keys)XART.rdy(k)}''')
  p.wait_for_function('__campaignKeys.every(k=>XART.rdy(k))&&nf100Warm()',timeout=120000)
  p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{
   window.wireSetup=(stage,difficulty='hard',pilot='cole')=>{
    BOFCinematicDirector.cancel();storySkip();NF100.current=NF100.resume=null;P2M.active=null;
    debugFight=null;coopOn=false;AP10_X.intro=null;run.mode='campaign';run.pilot=pilot;run._normalComplete100=null;
    delete run._gp4StageX;delete run._cf4Return;campaign.stageX1004=null;campaign.unlockedMax=stage;
    diffKey=difficulty;DIFF=difficultyForRun('campaign',difficulty);GP4.route=null;
    beginStage(stage);BOFCinematicDirector.cancel();storySkip();run.stage=stage;run.score=10000;run.lives=3;
    bossDefeated=true;setState(GS.STAGECLEAR);drawStageClear._init=false;drawStageClear._res=null;
    return {bonus:1234,rank:'A'};
   };
   window.wireFinish=()=>{let i=0;while(BOFCinematicDirector.current&&i++<100){const s=BOFCinematicDirector.current;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.advance();}return i;};
   window.wireDraw=()=>{const s=BOFCinematicDirector.current;if(s){s.t=.65;s.age=1;s.shown=Math.min(35,s.beats[s.i].text.length);ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw();}};
  }''')
  ck('Installed campaign owner is revision 9',p.evaluate('S113.revision===9'))
  # The normal tally continuation calls scLeaveStage only after native unlock/Forge pages.
  for stage in [2,3,4]:
   data=p.evaluate('''n=>{const R=wireSetup(n);scLeaveStage(R);const s=BOFCinematicDirector.current,score=run.score;scLeaveStage(R);const stable=BOFCinematicDirector.current===s;wireDraw();return{stage:n,id:s?.id,first:s?.beats[0].s113,score,stable,scoreAfter:run.score,loading:_stageLoads[n]?.keys.filter(k=>k.startsWith('s113_')).length}}''',stage)
   ck(f'Native Stage {stage} results enter the new story once',data['id']==f'post-{stage}'and data['score']==11234 and data['scoreAfter']==11234 and data['stable'],data)
   ck(f'Stage {stage} loads its cutscene assets with the mission',data['loading']>5,data['loading'])
   shot(p,f'native-post-{stage}')
   data=p.evaluate('''()=>{wireFinish();BOFCinematicDirector.finish();const a=campReadAuto();return{state,map:GS.STAGESEL,score:run.score,rank:campaign.rank[run.stage],savedStage:a?.stage,width:cv.width/SS,stage:run.stage}}''')
   ck(f'Post-{stage} returns to the native campaign map and autosave',data['state']==data['map']and data['score']==11234 and data['savedStage']==stage+1 and data['rank']=='A',data)
  # All pilots enter through the real HQ continuation, with identity-specific keys.
  for pilot in p.evaluate('S113.casts'):
   data=p.evaluate('''pilot=>{const R=wireSetup(4,'hard',pilot);scLeaveStage(R);const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);wireDraw();return{id:s.id,pilot:S113.last.pilot,contact:S113.last.contact,comic:S113.last.comic,leftColor:S113.last.leftColor,rightColor:S113.last.rightColor}}''',pilot)
   ck(pilot+' native campaign headset uses the correct identity and scrolling theme',data['id']=='post-4'and data['pilot']==pilot and data['contact']==('cole'if pilot=='decker'else'decker')and data['comic'],data)
   if pilot=='cole':shot(p,'native-comic-cole')
  for difficulty in ['hard','furious']:
   data=p.evaluate('''d=>{const R=wireSetup(5,d);scLeaveStage(R);const s=BOFCinematicDirector.current,entry={id:s?.id,score:run.score};scLeaveStage(R);const stable=s===BOFCinematicDirector.current;wireFinish();return{...entry,stable,stage:run.stage,state,scoreAfter:run.score,normal:!!NF100.current,active:!!BOFCinematicDirector.current}}''',difficulty)
   ck(difficulty+' Chronos homecoming continues into Stage 6 once',data['id']=='post-5'and data['stable']and data['stage']==6 and data['scoreAfter']==11234 and not data['normal'],data)
  for difficulty in ['easy','normal']:
   data=p.evaluate('''d=>{const R=wireSetup(5,d);scLeaveStage(R);const s=BOFCinematicDirector.current,entry={id:s?.id,score:run.score,normalSettled:R._normalSettled100};scLeaveStage(R);const stable=s===BOFCinematicDirector.current;wireDraw();return{...entry,stable,events:S113.events.filter(e=>e.event==='start'&&e.id==='post-5').length}}''',difficulty)
   ck(difficulty+' native Chronos settlement plays homecoming without duplicate rewards',data['id']=='post-5'and data['normalSettled']and data['score']==11234 and data['stable'],data)
   shot(p,'native-'+difficulty+'-homecoming')
   data=p.evaluate('''()=>{wireFinish();BOFCinematicDirector.finish();const a=campReadAuto();return{state,expected:NF100.state,phase:NF100.current?.phase,stage:run.stage,score:run.score,saved:a?.normalComplete100?.phase,difficulty:a?.diff,options:nf100Options(NF100.current).map(o=>o.key),width:cv.width/SS}}''')
   ck(difficulty+' retains its completion menu and archived clear after the new story',data['state']==data['expected']and data['phase']=='menu'and data['stage']==5 and data['score']==11234 and data['saved']=='settled'and data['difficulty']==difficulty,data)
   p.evaluate('nf100Draw(0)');shot(p,'native-'+difficulty+'-completion')
   data=p.evaluate('''()=>{const a=campReadAuto();BOFCinematicDirector.cancel();NF100.current=null;const ok=campApply(a);openStageSelect(5,{});return{ok,state,expected:NF100.state,phase:NF100.current?.phase,active:!!BOFCinematicDirector.current,score:run.score}}''')
   ck(difficulty+' saved clear resumes the completion menu without replay or reward',data['ok']and data['state']==data['expected']and data['phase']=='menu'and not data['active']and data['score']==11234,data)
  for route,kind,remaining in [('left','harrier','Rebel Fighters'),('right','rebels','Harrier')]:
   data=p.evaluate('''route=>{const R=wireSetup(6);s6WingInit();s6Wing.route=route;scLeaveStage(R);const s=BOFCinematicDirector.current;wireDraw();return{id:s?.id,battle:s?.beats[0].battle,remaining:s?.beats.find(b=>b.text.includes('casualties'))?.text,pending:campaign.stageX1004?.route,score:run.score}}''',route)
   ck('Stage 6 '+route+' reports the correct surviving threat',data['id']=='post-6'and data['battle']==kind and remaining in data['remaining']and data['pending']!=route and data['score']==11234,data)
   data=p.evaluate('''()=>{wireFinish();return{state,map:GS.STAGESEL,available:!!Rival24.mapAvailable,focus:!!CF4.focus,score:run.score,saved:campReadAuto()?.stage}}''')
   ck('Stage 6 '+route+' preserves the earned Stage X map offer',data['state']==data['map']and data['available']and data['focus']and data['saved']==7 and data['score']==11234,data)
   # Launch the earned pursuit via the actual map owner, not a manually set Stage X flag.
   data=p.evaluate('''()=>{cf4LaunchX();if(AP10_X.intro){AP10_X.intro.t=4.19;CC21.card=3;CC21.owner=run._gp4StageX;updatePlay(.02);}return{stage:run.stage,route:run._gp4StageX,mode:run.mode,state,play:GS.PLAY,boss:boss?.kind,intro:!!AP10_X.intro}}''')
   ck('Stage X '+route+' launches through the native pursuit owner',data['stage']==6 and data['route']==('right'if route=='left'else'left')and data['mode']=='campaign'and data['state']==data['play']and not data['intro']and data['boss']in ['warhive','rebelsquad'],data)
   actual_kind='rebels'if route=='left'else'harrier'
   data=p.evaluate('''()=>{window.__xResult={bonus:789,rank:'A'};const before=run.score;setState(GS.STAGECLEAR);scLeaveStage(__xResult);const s=BOFCinematicDirector.current;scLeaveStage(__xResult);wireDraw();return{before,id:s?.id,battle:s?.beats[0].battle,score:run.score,stable:s===BOFCinematicDirector.current}}''')
   ck('Stage X '+actual_kind+' plays its destruction before settling once',data['id']=='stage-x-'+actual_kind and data['battle']==actual_kind and data['score']==data['before']and data['stable'],data)
   shot(p,'native-stage-x-'+actual_kind)
   data=p.evaluate('''()=>{const before=run.score;wireFinish();BOFCinematicDirector.finish();scLeaveStage(__xResult);return{before,after:run.score,state,map:GS.STAGESEL,done:campaign.stageX1004?.done,stageX:run._gp4StageX,saved:campReadAuto()?.rivalState?.stageX1004}}''')
   ck('Stage X '+actual_kind+' returns to the map and settles a single bonus',data['after']==data['before']+789 and data['state']==data['map']and data['done']and not data.get('stageX'),data)
  for stage in [2,4]:
   data=p.evaluate('''n=>{wireSetup(n);setState(GS.FLYOVER);S113.exit=null;player.x=340;player.y=380;drawFlyover(.1);S113.exit.t=10.2;drawFlyover(0);return{shot:S113.last.shot,landed:S113.last.landed}}''',stage)
   ck(f'Stage {stage} native ending reaches the connected landing pad',data['landed']and data['shot']==('dish-exit'if stage==2 else'pad-exit'),data)
   shot(p,f'native-stage-{stage}-landed')
   data=p.evaluate('''()=>{S113.exit.t=11.35;drawFlyover(.1);return{state,stats:GS.STAGECLEAR,exit:S113.exit}}''')
   ck(f'Stage {stage} landing and fade hand off to native stats',data['state']==data['stats']and data['exit']is None,data)
  # Real keyboard taps: reveal, advance, and Start invoke the existing input layer.
  p.evaluate('''()=>{const R=wireSetup(4);scLeaveStage(R);const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);s.t=1;s.age=2;s.shown=0;}''')
  p.keyboard.press('Space');data=p.evaluate('''()=>{const s=BOFCinematicDirector.current,i=s.i;BOFCinematicDirector.tick(1/60);return{before:i,after:s.i,revealed:s.shown===s.beats[s.i].text.length}}''')
  ck('Native confirm reveals a line before advancing',data['before']==data['after']and data['revealed'],data)
  p.keyboard.press('Space');data=p.evaluate('''()=>{const s=BOFCinematicDirector.current,i=s.i;BOFCinematicDirector.tick(1/60);return{before:i,after:s.i}}''')
  ck('Native confirm advances the revealed line',data['after']==data['before']+1,data)
  p.keyboard.press('Enter');data=p.evaluate('''()=>{BOFCinematicDirector.tick(1/60);BOFCinematicDirector.finish();return{active:!!BOFCinematicDirector.current,state,map:GS.STAGESEL,score:run.score}}''')
  ck('Native Start skips to the supplied continuation without extra rewards',not data['active']and data['state']==data['map']and data['score']==11234,data)
  ck('No page or renderer exceptions',not errors,errors);ck('No missing requested assets',not missing,missing)
  br.close()
finally:stop()
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'checks':checks,'errors':errors,'missing':missing,'scope':'Native continuation fixtures; not a full combat campaign playthrough.'}
(V/('campaign-installed.json'if '--installed'in sys.argv else'campaign.json')).write_text(json.dumps(report,indent=2))
print(json.dumps({'passed':report['passed'],'total':report['total']}));raise SystemExit(not all(c['passed']for c in checks))
