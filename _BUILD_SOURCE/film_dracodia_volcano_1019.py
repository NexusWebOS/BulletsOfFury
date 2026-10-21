"""Full native loop footage, moving ordnance, ordinary fire and audio."""
from pathlib import Path
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright
import ast,base64,http.server,json
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_volcano_1019';checks=[];errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
BOOT=next(n.args[0].value for n in ast.walk(ast.parse((R/'_BUILD_SOURCE/probe_dracodia_volcano_1019.py').read_text(encoding='utf-8'))) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.volcanoSetup=' in n.args[0].value)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&vp23Warm();}',polling=80);p.evaluate(BOOT)
  def setup(phase='arms',attack='cannon'):
   p.evaluate('([phase,attack])=>{volcanoSetup("normal",phase,attack);VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;player.fireCd=999999;}',[phase,attack])
  def step(n):
   result=p.evaluate(shoot.STEP,n)
   if result:errors.append(result)
  def frame():
   raw=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));return Image.open(BytesIO(raw)).convert('RGB')
  def movie(name,film):film[0].save(O/(name+'.webp'),save_all=True,append_images=film[1:],duration=100,loop=0,quality=87)
  whole=[]
  for phase,attack in [('arms','cannon'),('arms','sweep'),('arms','spin900'),('core','ring'),('core','coreLaser'),('core','rotor'),('core','rollerball'),('head','eyeSweep')]:
   setup(phase,attack);film=[]
   for i in range(46):step(6);im=frame();film.append(im);whole.append(im)
   movie('live-'+attack,film);row=p.evaluate('({phase:F.phase,attack:F.attack,alive:!B.dead,finite:Number.isFinite(B.x+B.y+B.hp),bullets:eBullets.length,poses:Object.keys(VP23.draws).length})');ck(attack+' full native loop animates boss, ordnance and effects',row['alive'] and row['finite'],row)
  movie('live-attack-reel',whole)
  for phase in ['arms','core']:
   setup(phase,'cannon' if phase=='arms' else 'ring');p.evaluate('''()=>{run.spaceMode=false;run.wlevels=Array(8).fill(0);run.wvars=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});run.weapon=0;run.wlevel=0;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];const at=F.phase==='arms'?vp23Socket(P,'left'):vp23Socket(P,'reactor');player.x=at.x-(wm26PlayerNose().x-player.x);player.y=viewTopY()+viewH()-60;player.fireCd=0;window.beforeHP=B.hp;}''');p.keyboard.down('j');step(105);p.keyboard.up('j');row=p.evaluate('({loss:beforeHP-B.hp,last:B._lastPart?.id,budget:Math.abs(B.hp-B.parts.reduce((s,q)=>s+q.hp,0))})');ck(phase+' actual ordinary primary hits real module and budget',row['loss']>0 and row['budget']<.01,row);frame().save(O/('ordinary-fire-'+phase+'.png'))
  setup();p.evaluate('()=>{Audio.resume();Snd.prepare("shieldBreakCombat");}')
  for cue in ['enemyBossCannon','furnaceFlameIgnite','furnaceLaserCharge','furnaceLaserBurst','shieldBreakCombat']:
   row=p.evaluate('''async key=>{await Snd._audioCtx().resume();let seen=[];const prior=Snd.play;Snd.play=function(k){seen.push(k);return prior.apply(this,arguments);};try{fztSfx(key);}finally{Snd.play=prior;}const a=seen.at(-1)||key,b=CA15.aliases[a]||a,k=window.BOF_CHIP_PASS?.aliases[b]||b;Snd.prepare(k);await new Promise(r=>setTimeout(r,900));Snd.stopCue(k);Snd._last[k]=0;AV3.last.clear();Snd.play(k);let el;for(let i=0;i<200;i++){el=Snd.pools[k]?.slots.find(s=>s?.attached&&!s.el.paused&&s.el.currentTime>0)?.el;if(el)break;await new Promise(r=>setTimeout(r,10));}return{key:k,playing:!!el,ready:el?.readyState,volume:el?.volume};}''',cue);ck(cue+' recorded native sound decodes and plays',row['playing'] and row.get('ready',0)>=2 and row.get('volume',0)>0,row)
  ck('No full-loop browser, asset, draw or update errors',not errors,errors);br.close()
finally:stop()
(O/'live-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors)),flush=True);raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
