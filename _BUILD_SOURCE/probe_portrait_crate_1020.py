from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import ast,json,base64,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/portrait_crate_1020';O=R/'_shots/portrait_crate_1020';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def string_in(file,needle):
 return next(n.value for n in ast.walk(ast.parse((R/'_BUILD_SOURCE'/file).read_text(encoding='utf-8'))) if isinstance(n,ast.Constant) and isinstance(n.value,str) and needle in n.value)
SETUP=string_in('probe_feedback_1002.py','c=>{ht27Stop()');BLUE=string_in('probe_source_hammer_1020.py','window.source20=');BOOT=string_in('probe_boss_redesign_1020.py','window.clean20=')
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000);p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate(SETUP,dict(stage=5,kind='chromehammer',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&hm10Ready()&&b20Ready(HB20_ART.banks)&&Object.values(HB20_PICKUP).map(k=>XART.rdy(k)).every(Boolean);}');p.evaluate(BLUE)
  p.evaluate('''()=>{window.pcTags=new WeakMap();window.pcUsed=[];window.pcScrates=0;const get=XART.get,draw=ctx.drawImage,crate=drawScrate;XART.get=function(k){const im=get.apply(this,arguments);if(im)pcTags.set(im,k);return im};ctx.drawImage=function(im){if(pcTags.has(im))pcUsed.push(pcTags.get(im));return draw.apply(this,arguments)};drawScrate=function(){pcScrates++;return crate.apply(this,arguments)};window.pcPaint=()=>{pcUsed=[];pcScrates=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return{keys:[...new Set(pcUsed)],generic:pcScrates};};}''')
  def capture(name):
   p.evaluate('pcPaint()');(O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('diff=>{source20(diff);B._hammer.hb20PickupDone=false;hammerPhaseTwoStart(B);}',diff)
   p.evaluate('()=>{for(let i=0;i<36;i++)hammerBossTick(B,1/60);}');row=p.evaluate('pcPaint()');ck(diff+' Stage5 uses exclusive chaingun box and no player crate','hb20_chaingun_crate_exclusive' in row['keys'] and row['generic']==0,row)
   if diff=='normal':capture('stage5-crate')
   p.evaluate('()=>{while(B._hammer.hb20Pickup&&B._hammer.hb20Pickup.t<1.94)hammerBossTick(B,1/60);}');row=p.evaluate('pcPaint()');ck(diff+' Stage5 struck crate disappears and exclusive numeral-free icon flies to boss','hb20_chaingun_icon_exclusive' in row['keys'] and 'hb20_chaingun_crate_exclusive' not in row['keys'],row)
   if diff=='normal':capture('stage5-icon')
   p.evaluate('()=>{while(B._hammer.hb20Pickup)hammerBossTick(B,1/60);}');row=p.evaluate('pcPaint()');ck(diff+' Stage5 completes pickup and retires both pickup sprites',p.evaluate('B._hammer.hb20PickupDone') and not any(k.startswith('hb20_chaingun_') for k in row['keys']),row)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='yuri'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&XART.rdy(DP20.key);}');p.evaluate(BOOT)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('diff=>{setup20(8,diff);hb20Start(B,"pickup");}',diff)
   p.evaluate('tick20(36)');row=p.evaluate('pcPaint()');ck(diff+' Stage8 corrupted Hammer uses the same exclusive crate independent of pilot','hb20_chaingun_crate_exclusive' in row['keys'] and row['generic']==0,row)
   if diff=='normal':capture('stage8-crate')
   p.evaluate('tick20(80)');row=p.evaluate('pcPaint()');ck(diff+' Stage8 release uses exclusive chaingun icon','hb20_chaingun_icon_exclusive' in row['keys'] and 'hb20_chaingun_crate_exclusive' not in row['keys'],row)
   if diff=='normal':capture('stage8-icon')
   p.evaluate('tick20(65)');ck(diff+' Stage8 transitions into its gun attack',p.evaluate('Q.action?.type==="gun"&&Q.gunSeen'))
  p.evaluate('''()=>{setup20(0);B._r30.mode='dr5Monologue';B._r30.t=2;B._r30.clock=2;B.enter=B._noHit=true;dr5Say(B,'DRACODIA',DR5.intro[0][0],3);dr5State(B).radio.t=1;}''');capture('dracodia-dialogue')
  ck('Actual monologue uses regenerated framed portrait',p.evaluate('()=>{const im=XART.get(DP20.key);return UI20.dialogue.who==="DRACODIA"&&XART.get(UI20.dialogue.portrait)===im&&im.width===512&&/portrait_box/.test(XART._src[DP20.key]);}'))
  ck('Every Dracodia form/talking alias resolves to new framed portrait',p.evaluate('()=>Array.from({length:9},(_,i)=>[0,1,2].every(t=>dr5Portrait(i,t)===XART.get(DP20.key))).every(Boolean)'))
  for key,name in [('dp20_dracodia_portrait','portrait-native'),('hb20_chaingun_crate_exclusive','crate-native'),('hb20_chaingun_icon_exclusive','icon-native')]:
   p.evaluate('k=>{const im=XART.get(k);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,0,0,im.width,im.height)}',key);(O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('No native page, draw, console or asset errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks);(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(not all(c['passed'] for c in checks))
