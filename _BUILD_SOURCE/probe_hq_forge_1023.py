from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(__file__).resolve().parents[1];W=R/'_shots/hq_forge_1023';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1100,'height':900});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]+' '+str(m.location))if m.type=='error'and'ERR_ABORTED'not in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{window.__step='+shoot.STEP+';}')
  def ev(js,a=None):return p.evaluate(js,a)if a is not None else p.evaluate(js)
  def step(n=60):ev('(n)=>{for(let i=0;i<n;i++)__step(1)}',n)
  def press(k):p.keyboard.down(k);step(1);p.keyboard.up(k);step(24)
  def click_virtual(x,y):
   q=ev('''p=>{const r=cv.getBoundingClientRect(),f=sm22Field();return{x:r.x+(f.ox+p.x*f.k)/cv.width*r.width,y:r.y+(f.oy+p.y*f.k)/cv.height*r.height};}''',{'x':x,'y':y})
   p.mouse.move(q['x'],q['y']);step(1);p.mouse.down();step(1);p.mouse.up();step(24)
  def shot(name):
   (W/(name+'.png')).write_bytes(base64.b64decode(ev('cv.toDataURL().split(",")[1]')))
  def setup(stage=6):
   ev('''stage=>{HF23.modal=null;UC22.open=false;UC22.focus=false;UC22.pending=false;SM22.open=false;coopOn=false;run.mode='campaign';run.pilot='cole';run.stage=stage;run.ngplus=false;run._respecBase23=false;delete run._forgeBudget23;run.forge={0:{elem:'fire',lv:1},3:{elem:'fire',lv:1}};run.forgeForms={0:{fire:{elem:'fire',lv:1}},3:{fire:{elem:'fire',lv:1}}};run.forgeElems={fire:1,ice:1};run.wvars=[];run.wvars[3]='firewhip';run.infusion={elem:'fire',lv:1,_forgeW:0};run.weapon=0;run.loadout=[0,1,2,3];run._earnedUnlocks={chaingun:true};campaign.rank={};for(let n=1;n<stage;n++)campaign.rank[n]='A';campaign.unlockedMax=stage;campaign.bonusUnlocked=false;achievementState.fp={carry:0,levels:[{stage:1,score:5000000,fp:5000,at:Date.now()}],supplies:[]};achievementState.owned={};achievementSave();hf23Budget();}''',stage)
  setup();row=ev('hf23Info()');ck('Stage6 before clear earns10, with2 spent and8 available',row['earned']==10 and row['left']==8,row)
  row=ev('''()=>{setState(GS.STAGECLEAR);const a=run.forgeCombos,e=hf23Earned();setState(GS.STAGECLEAR);hf23Grant(6);return{a,e,after:run.forgeCombos};}''');ck('Stage6 clear earns12; duplicate clear awards nothing',row=={'a':10,'e':12,'after':10},row)
  row=ev('''()=>{hf23Grant(7);return{earned:hf23Earned(),left:run.forgeCombos};}''');ck('Stage7 clear earns14',row=={'earned':14,'left':12},row)
  setup();row=ev('''()=>{const before=furiousBalance(),score=run.score,unlocks=JSON.stringify(run._earnedUnlocks),elements=JSON.stringify(run.forgeElems),r=hf23PayReset();return{r,spent:before-furiousBalance(),points:run.forgeCombos,empty:!Object.keys(run.forge).length&&!Object.keys(run.forgeForms).length,vars:Object.keys(run.wvars).length,infusion:run.infusion,score:score===run.score,unlocks:unlocks===JSON.stringify(run._earnedUnlocks),elements:elements===JSON.stringify(run.forgeElems)};}''')
  ck('Fullreset costs300FP and restores10 points/basic forms, preserves progress and weapons',row['r']=='ok'and row['spent']==300 and row['points']==10 and row['empty']and row['vars']==0 and row['infusion']is None and row['score']and row['unlocks']and row['elements'],row)
  row=ev('''()=>{const b=furiousBalance(),n=run.forgeCombos,r=hf23PayReset();return{r,same:b===furiousBalance()&&n===run.forgeCombos};}''');ck('No repeat charge on already basic build',row=={'r':'bare','same':True},row)
  row=ev('''()=>{const b=run.forgeCombos;forgeStart(()=>{});forgeStart(()=>{});return{before:b,after:run.forgeCombos};}''');ck('Repeated Forge visits do not refill or spend points',row['before']==row['after']==10,row)
  row=ev('''()=>{run.ngplus=true;achievementState.owned.forge_fire_0_C={at:1};ensureForgeForms();const s=campSnapshot();run._respecBase23=false;run.forge={0:{elem:'ice',lv:1}};run.forgeForms={};campApply(s);ensureForgeForms();return{empty:!Object.keys(run.forgeForms).length,points:run.forgeCombos,earned:hf23Earned(),base:run._respecBase23,profile:!!achievementState.owned.forge_fire_0_C,paid:achievementNormalize(JSON.parse(localStorage.getItem(ACHIEVEMENT_STORE_KEY))).fp.supplies.some(q=>q.kind==='respec'&&q.cost===300)};}''')
  ck('Campaign and profile save retain paid reset; NG+ recipes do not reappear',row['empty']and row['points']==10 and row['earned']==10 and row['base']and row['profile']and row['paid'],row)
  setup();row=ev('''()=>{achievementState.fp.levels=[];achievementState.unlocked={};const old=JSON.stringify(run.forgeForms),before=furiousBalance(),r=hf23PayReset();return{r,same:old===JSON.stringify(run.forgeForms)&&furiousBalance()===before};}''');ck('InsufficientFP cannot charge or reset',row=={'r':'poor','same':True},row)
  setup();row=ev('''()=>{const get=()=>{const s=campSnapshot();delete s.t;return JSON.stringify(s);},old=get(),balance=furiousBalance(),save=achievementSave;achievementSave=()=>false;const r=hf23PayReset();achievementSave=save;return{r,same:old===get(),balance:furiousBalance()===balance};}''');ck('Failed profile save rolls back fee, forms and points',row['r']=='save'and row['same']and row['balance'],row)
  setup();row=ev('''()=>{const old=JSON.stringify(run.forgeForms),b=furiousBalance(),set=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===CAMP_AUTO_KEY)throw Error('test full disk');return set.apply(this,arguments);};const r=hf23PayReset();Storage.prototype.setItem=set;return{r,same:old===JSON.stringify(run.forgeForms)&&b===furiousBalance()};}''');ck('Failed campaign save rolls back transaction',row=={'r':'save','same':True},row)
  setup();ev('''()=>{campaign.rank={};campaign.unlockedMax=1;delete run._forgeBudget23;run.stage=6;run.forge={};run.forgeForms={};}''');ck('Merely choosing Stage6 cannot award10 points',ev('hf23Earned()')==0)
  setup();ev('''()=>{const s=campSnapshot();delete s.forgeBudget23;delete s.forgeCombos;campApply(s);}''');ck('Legacy Stage6 save migrates to10 earned',ev('hf23Earned()')==10)
  # Real map, movement and menus.
  setup();ev('''()=>{campaign._booted=true;campaign._introSeen=true;window.sselCommitted=false;openStageSelect(1,{});}''')
  for _ in range(45):
   step(60)
   if ev('state===GS.STAGESEL&&campPauseIsCampaignScreen()&&!sselUnlockCine&&sselBoot===0'):break
  p.wait_for_function('Object.keys(HF23_ART.assets).every(k=>XART.rdy(k))')
  p.wait_for_function('()=>{map4eWarm();return MAP4E.keys.every(k=>XART.rdy("map4e_region_"+k))&&XART.rdy("map4e_landscape");}')
  ev('sselCursor=1');press('w');step(600);shot('map')
  row=ev('''()=>({focus:UC22.focus,ship:Math.hypot(sselShip.x-uc22Point().x,sselShip.y-uc22Point().y),hq:cmap2ToScreen(...MAP4E.hq),forge:cmap2ToScreen(UC22.pos.x,UC22.pos.y)})''')
  ck('UP flies actual map ship to new Forge landmark',row['focus']and row['ship']<12,row)
  press('j');step(60);shot('workshop');ck('FIRE enters generated map service',ev('UC22.open&&state===GS.STAGESEL'))
  ev('UC22.sel=2');press('j');step(30);shot('respec');ck('Re-Spec row opens generated fullreset menu',ev('!!HF23.modal'))
  ck('Re-Spec opens with safe Cancel selected',ev('HF23.modal.sel')==1)
  row=ev('''()=>({fp:furiousBalance(),forms:JSON.stringify(run.forgeForms),points:run.forgeCombos})''');press('Escape');ck('B cancels reset without a fee or changing forms',ev('!HF23.modal')and ev('furiousBalance()')==row['fp']and ev('JSON.stringify(run.forgeForms)')==row['forms'])
  ev('uc22Choose(0)');step(100);shot('forge');ck('THE FORGE opens existing Forge',ev('state===GS.FORGE'))
  press('h');step(30);ck('Charge shortcut opens Re-Spec from Forge',ev('!!HF23.modal'))
  if ev('!!HF23.modal'):
   press('Escape');ck('Forge Re-Spec B cancels without leaving Forge',ev('!HF23.modal&&state===GS.FORGE'))
  # Native layout at desktop and narrow window; no label exceeds measured bitmap apertures.
  ev('hf23Open()');step(30);shot('respec_desktop')
  for width,height in [(1100,900),(390,844),(1920,1080)]:
   p.set_viewport_size({'width':width,'height':height});step(60)
   row=ev('''()=>({layout:HF23.layout.map(q=>({text:q.text,size:q.size,rows:q.rows,rect:q.rect,fit:q.rows.every(s=>bmfMeasure(window.BOF_UI_FACE||'game',s,q.size)<=q.rect.w+.1)})),modal:!!HF23.modal})''');ck(f'All Re-Spec labels fit at{width}x{height}',row['modal']and all(q['fit']for q in row['layout']),row if not all(q['fit']for q in row['layout'])else None)
   if width==390:shot('respec_mobile')
  # Pay using real mouse input in the generated confirmation, then reassign a point.
  before=ev('furiousBalance()');click_virtual(150,374);ck('Generated PAY button performs one confirmed reset',ev('!hf23HasForms()&&run.forgeCombos===10')and before-ev('furiousBalance()')==300)
  click_virtual(150,374);ck('Repeated PAY click does not charge twice',before-ev('furiousBalance()')==300)
  click_virtual(365,374);ck('Generated CANCEL closes confirmation',ev('!HF23.modal'))
  row=ev('''()=>{const before=run.forgeCombos,r=forgeCombine(3,'ice');return{r,before,after:run.forgeCombos,elem:run.forge[3]?.elem};}''');ck('Basic build can choose a new element for one point',row['r']=='ok'and row['before']==10 and row['after']==9 and row['elem']=='ice',row)
  row=ev('''()=>{const s=campSnapshot();campApply(s);return{left:run.forgeCombos,elem:run.forge[3]?.elem,stage:run.stage};}''');ck('Reassigned form and9 remaining points survive load; resumeStage6',row=={'left':9,'elem':'ice','stage':6},row)
  ev('''()=>{HF23.modal=null;loadoutStart(()=>{});}''');step(90);press('h');ck('Loadout charge shortcut also opens fullreset menu',ev('!!HF23.modal'));press('Escape');ck('Loadout modal B returns to Loadout',ev('!HF23.modal&&state===GS.LOADOUT'))
  # Start-menu route opens the same map service and doesn't alter the point bank.
  ev('''()=>{UC22.open=false;UC22.focus=false;UC22.pending=false;openStageSelect(6,{});}''');step(400);press('p');step(60);shot('start_menu');ck('Start opens Claude menu with authored button states',ev('SM22.open'))
  ev('SM22.sel=4');press('j');step(120);ck('Start menu Forge/Loadout enters the same service with9 points',ev('UC22.open&&state===GS.STAGESEL&&run.forgeCombos===9'))
  # Controller edges use the game's real gamepad poller and logical A/B actions.
  ev('''()=>{window.__hfPad=Array.from({length:16},()=>({pressed:false,value:0}));navigator.getGamepads=()=>[{id:'BOF QA controller',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:window.__hfPad}];UC22.sel=2;}''')
  def btn(i):ev('i=>{__hfPad[i]={pressed:true,value:1}}',i);step(1);ev('i=>{__hfPad[i]={pressed:false,value:0}}',i);step(30)
  btn(0);ck('Controller A enters Re-Spec',ev('!!HF23.modal'));btn(1);ck('Controller B cancels without leaving workshop',ev('!HF23.modal&&UC22.open'))
  # Save while parked at the Forge must retain the campaign destination, not its Stage1 navigation flag.
  ck('Saving in map service keepsStage6 destination',ev('campSnapshot().stage')==6)
  br.close()
finally:stop()
ck('No native page or console errors',not errors,errors)
out={'checks':checks,'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'errors':errors};(W/'report.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k]for k in ['passed','failed','errors']}));sys.exit(bool(out['failed']))
