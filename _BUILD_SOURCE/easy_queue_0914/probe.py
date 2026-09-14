"""Native proof for the first easy-to-hard queue entries."""
import base64,json,sys,threading,http.server
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'_shots/easy_queue_0914';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
checks=[];errors=[];shots=[];details={}
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  'if v else'FAIL ')+label,flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate("()=>{__auto=function(){};window.__labels=[];const f=ctx.fillText;ctx.fillText=function(t,x,y){if(String(t).startsWith('SPACE FIGHTER')||String(t).includes('GRAVITY MODE'))__labels.push({text:t,x,y,width:ctx.measureText(t).width});return f.apply(this,arguments);};window.__blits=0;const d=ctx.drawImage;ctx.drawImage=function(){__blits++;return d.apply(this,arguments);};}")
 def step(n):
  for i in range(0,n,30):pg.evaluate('n=>__step(n)',min(30,n-i));pg.wait_for_timeout(12)
 def shot(name,frame=False):
  path=O/(name+'.png')
  if frame:pg.locator('#game-frame').screenshot(path=str(path))
  else:path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
  shots.append(path)
 pilots=[('yuri','YAMADO'),('maverick','MOONRAKER'),('lizzie','LAVENDER'),('falva','FOXTROUT'),('cole','COLLISTO'),('juggernaut','JANIS'),('axel','ARISTOTLE'),('freezer','FALCON'),('decker','DECKER')]
 pg.evaluate("()=>{run.mode='arcade';run.stage=5;beginStage(5);run.gravityShipReady=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch(0);gravityModeStart();drawLaunch._phase='gravity';drawLaunch._dist=SEG_B3+SEG_B1+240;gravityMode.phase='reveal';gravityMode.t=.3;gravityMode.dialogueT=0;}")
 details['models']=[]
 for pilot,model in pilots:
  pg.evaluate("k=>{run.pilot=k;pilotIndex=PILOTS.findIndex(p=>p.key===k);__labels=[];}",pilot)
  for _ in range(180):
   if pg.evaluate('()=>!!spaceAtlasCanvas("ship_base",_pilotKey())'):break
   pg.wait_for_timeout(35)
  pg.evaluate('()=>{drawLaunch(0);}')
  labels=pg.evaluate('()=>__labels');details['models'].append({'pilot':pilot,'labels':labels})
  ok(any(q['text']=='SPACE FIGHTER '+model and q['x']-q['width']/2>=0 and q['x']+q['width']/2<=480 and 0<=q['y']<512 for q in labels),pilot+' native reveal shows its model name within the screen')
  shot('model_'+pilot)
 pg.evaluate("()=>{gravityMode.phase='charge';gravityMode.t=.5;__labels=[];drawLaunch(0);}")
 ok(pg.evaluate("()=>__labels.some(q=>q.text==='SPACE FIGHTER DECKER')&&!__labels.some(q=>q.text.includes('GRAVITY MODE'))"),'assembly and reveal use Space Fighter wording; Decker preserves his name pending a model')
 def prep(mode,key):
  pg.evaluate("a=>{run.mode=a[0];diffKey=a[1];DIFF=difficultyForRun(run.mode,diffKey);run.stage=1;curStage=STAGES[0];beginStage(1);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;bossWarned=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];special=null;__auto=function(){};lifeUpRolled=false;stageTimer=curStage.length*.5+.1;}",[mode,key])
 for mode in ['campaign','arcade']:
  for key in ['easy','normal','hard','furious']:
   prep(mode,key)
   pg.evaluate('()=>{window.__savedRandom=Math.random;Math.random=()=>.022;}');step(1);pg.evaluate('()=>{Math.random=__savedRandom;}')
   n=pg.evaluate("()=>powerups.filter(p=>p.kind==='life').length");expected=key in ['hard','furious']
   ok((n==1)==expected and pg.evaluate('()=>lifeUpRolled'),mode+' '+key+' native midpoint uses the correct probability at a 2.2% roll')
   if expected:
    ok(pg.evaluate("()=>powerups.some(p=>p.kind==='life'&&p.x>=camLeftX()+40&&p.x<=camRightX()-40)"),mode+' '+key+' extra Life Up spawns inside the visible camera')
 # Current scene is Arcade/Furious, with one actual midpoint pickup. Let it enter the view.
 step(65);shot('lifeup_midpoint',True)
 pg.evaluate("()=>{run.lives=3;const p=powerups.find(p=>p.kind==='life');p.x=player.x;p.y=player.y;p.vy=0;}");step(1)
 ok(pg.evaluate("()=>run.lives===4&&!powerups.some(p=>p.kind==='life')"),'native pickup collision grants exactly one life')
 shot('lifeup_collected',True)
 # Extra death-drop interval produces life without replacing the original ammo/shield outcomes.
 details['deathRolls']=pg.evaluate("()=>{const saved=Math.random;const out=[];try{for(const key of ['normal','hard','furious']){diffKey=key;powerups=[];Math.random=()=>.101;dropPowerup(player.x,player.y-70);out.push({key,kinds:powerups.map(p=>p.kind)});}}finally{Math.random=saved;}return out;}")
 ok(details['deathRolls']==[{'key':'normal','kinds':[]},{'key':'hard','kinds':['life']},{'key':'furious','kinds':['life']}],'native ordinary-death supply route adds the Hard/Furious life interval')
 details['loopError']=pg.evaluate('()=>window.__err||null');details['blits']=pg.evaluate('()=>__blits')
 ok(details['blits']>0 and not errors and not details['loopError'],'zero page, console or controlled-loop errors while rendering native art')
 b.close()
srv.shutdown()
(O/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'screenshots':[str(s)for s in shots]},indent=2),encoding='utf-8')
board=Image.new('RGB',(960,1080),'#101218');d=ImageDraw.Draw(board)
for i,(pilot,model)in enumerate(pilots):
 im=Image.open(O/('model_'+pilot+'.png')).convert('RGB');im.thumbnail((320,340));x=i%3*320;y=i//3*360;board.paste(im,(x,y+18));d.text((x+6,y+3),pilot+' / '+model,fill='white')
board.save(O/'models_contact.png')
n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)
