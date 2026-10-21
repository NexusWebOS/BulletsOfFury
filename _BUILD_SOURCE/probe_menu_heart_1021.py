from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import sys,ast,json,base64,http.server,time
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/menu_heart_1021';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));checks=[];errors=[]
def ck(n,v,data=None):checks.append({'name':n,'ok':bool(v),'data':data});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def paint(p,code):p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);shake=0;'+code+';}')
def shot(p,name,code=None):
 data=p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);shake=0;'+(code or '')+';return cv.toDataURL().split(",")[1];}')
 (O/(name+'.png')).write_bytes(base64.b64decode(data))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1000});p.add_init_script(shoot.TRAP_RAF)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m: errors.append(m.text[:300]) if m.type=='error' else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('typeof CH21!=="undefined" && ASSETS.ready',timeout=180000)
  p.evaluate('()=>{Audio.init();for(const a of Object.values(MW21_ART))XART.rdy(a.key);for(const k of ch21Keys())XART.rdy(k);UI20.warm();}');p.wait_for_function('()=>Object.values(MW21_ART).every(a=>XART.rdy(a.key))&&ch21Keys().every(k=>XART.rdy(k))&&UI20_KEYS.every(k=>XART.rdy(k))',timeout=120000)
  p.evaluate('()=>{setState(GS.PILOT);run.mode="campaign";tutAskOpen(1);tutAsk.t=2;}');shot(p,'tutorial-native','tutAskDraw(0)');p.screenshot(path=str(O/'tutorial-desktop.png'))
  row=p.evaluate('()=>({layout:MW21.last,prompt:MW21.prompt,portrait:UI20.dialogue?.portrait})');ck('Neutral menu prompt uses avatar-free L frame and fitted text',row['layout']['avatar']==False and row['prompt']['size']>=11,row)
  p.set_viewport_size({'width':390,'height':844});p.evaluate('window.dispatchEvent(new Event("resize"))');paint(p,'tutAskDraw(0)');p.screenshot(path=str(O/'tutorial-mobile.png'));p.set_viewport_size({'width':1440,'height':1000})
  for n,(w,h) in {'s':(384,132),'m':(456,196),'l':(456,286),'xl':(456,366)}.items():
   shot(p,'menu-'+n,f'ctx.fillStyle="#090c14";ctx.fillRect(0,0,VW,VH);const q=mw21Window("{n}",(VW-{w})/2,(VH-{h})/2,{w},{h});mw21Text("{n.upper()} MENU WINDOW",q.header,14);mw21Text("AVATAR-FREE WINDOW. ALL TEXT CENTERS AND FITS INSIDE ITS OWN APERTURE.",q.body,15);')
  row=p.evaluate('()=>{CH21.unlocked=false;pwInput="BARBIE";submitPassword();return{state,locked:CH21.result.locked,pending:CH21.pending};}');ck('Locked BARBIE cannot launch encounter',row['state']=='chromeheart_result' and row['locked'] and not row['pending'],row)
  shot(p,'password-locked','drawScene(1)')
  # Exercise real victory gate, persist/reload same origin, and protect unrelated pilots/debug.
  rows=p.evaluate('''()=>{const out=[];for(const pilot of ['cole','falva','lizzie']){CH21.unlocked=false;run.pilot=pilot;run.stage=8;run.mode='campaign';run._heartMode=false;bossDefeated=true;debugFight=null;_bmHost=false;out.push({pilot,earned:ch21Earn()});}CH21.unlocked=false;debugFight={stage:8};run.pilot='falva';out.push({pilot:'debug',earned:ch21Earn()});debugFight=null;bossDefeated=false;out.push({pilot:'not-cleared',earned:ch21Earn()});bossDefeated=true;ch21Earn();return out;}''');ck('Only Falva/Lizzie actual final wins unlock password',all(x['earned']==(x['pilot'] in ['falva','lizzie']) for x in rows),rows)
  p.reload();p.wait_for_function('typeof CH21!=="undefined" && ASSETS.ready',timeout=180000);ck('Unlock survives browser reload',p.evaluate('CH21.unlocked'))
  row=p.evaluate('()=>{pwInput="barbie";submitPassword();return{state,pending:CH21.pending,stage:PENDING_STAGE};}');ck('Case-insensitive password opens native difficulty selection',row['state']=='diff' and row['pending'] and row['stage']==5,row)
  p.evaluate('()=>{diffKey="normal";menuIndex=1;pickDiff();pilotIndex=PILOTS.findIndex(p=>p.key==="lizzie");startRun(5);BOFCinematicDirector.cancel();story=null;warnT=0;spawnBoss("chromehammer");}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ch21Keys().every(k=>XART.rdy(k));}',timeout=180000)
  row=p.evaluate('()=>({active:!!boss?._heart,heartMode:run._heartMode,pilot:run.pilot,state,name:boss?.name,hp:boss?.hp,debug:debugFight})');ck('Password route launches only secret Hammer arena',row['active'] and row['heartMode'] and row['state']=='play' and row['pilot']=='lizzie' and row['debug']==None,row)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':5,'pilot':'lizzie','diff':diff,'kind':'chromehammer'});p.evaluate('()=>{run._heartMode=true;ch21Init(boss);window.B=boss;B._be=null;B._ovIntro=null;player.invuln=1e9;warnT=0;warnKind=null;_bossCard=null;stageLoadTick();}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ch21Keys().every(k=>XART.rdy(k));}',timeout=180000)
   for action in ['dance','slam','shield','waltz','bouquet']:
    row=p.evaluate('''a=>{eBullets=[];B._heart.action=null;B.x=worldWidth()/2;B.y=PLAY.y+130;const A=ch21Start(B,a);let min=99,max=0;for(let i=0;i<600&&B._heart.action;i++){updateBoss(1/60);min=Math.min(min,B.x);max=Math.max(max,B.x);if(i%30===0)drawBoss();}return{finished:!B._heart.action,finite:Number.isFinite(B.x+B.y),shots:eBullets.length,heart:eBullets.every(q=>q._chromeHeart),tell:A.tell,width:max-min,cool:B._heart.cool};}''',action);ck(diff+' '+action+' completes with warning, real heart shots and recovery',row['finished'] and row['finite'] and row['shots']>0 and row['heart'] and row['tell']>=.9 and row['cool']>.5,row)
    if diff=='normal':
     p.evaluate('''a=>{B.x=worldWidth()/2;B.y=PLAY.y+130;B._heart.action=null;eBullets=[];const A=ch21Start(B,a);A.t=A.tell+.4;updateBoss(0);}''',action);shot(p,'heart-'+action,'drawWorld(0)')
   row=p.evaluate('''()=>{B._heart.action=null;B._heart.shield=100;const hp=B.hp,n=eBullets.length;hitBoss(35);const r={hp:B.hp,shield:B._heart.shield,flash:B.flash,deflected:eBullets.length-n};B._heart.shield=0;hitBoss(25);r.hurt=hp-B.hp;r.target=retinaBossTargets(B).length;return r;}''');ck(diff+' shield absorbs, never deflects; unshielded hits flash and damage',row['shield']==65 and row['flash']>0 and row['hurt']==25 and row['deflected']==0 and row['target']==1,row)
  # Pixel proof of hit flash and expiry on the actual selected bank.
  p.evaluate('()=>{B._heart.action=null;B._heart.shield=0;B.flash=0;B._heart.age=0;}');shot(p,'heart-normal','drawWorld(0)');p.evaluate('hitBoss(2)');shot(p,'heart-hit','drawWorld(0)');p.evaluate('()=>{updateBoss(.4);B._heart.age=0;}');shot(p,'heart-expired','drawWorld(0)')
  box=(110,65,370,330);before=Image.open(O/'heart-normal.png').convert('RGB').crop(box);after=Image.open(O/'heart-hit.png').convert('RGB').crop(box);pixels=sum(max(v)>24 for v in ImageChops.difference(before,after).getdata());ck('Actual hull pixels visibly flash on damage',pixels>100,{'pixels':pixels});ck('Hit flash expires',p.evaluate('B.flash<=0'))
  row=p.evaluate('''()=>{run._heartMode=true;beginStage(5);warnT=0;spawnBoss('chromehammer');window.B=boss;player.invuln=1e9;stagePlan=[];let fail='';for(let i=0;i<720;i++){updatePlay(1/60);if(!boss?._heart){fail='lost secret boss';break;}}return{fail,state,heart:!!boss?._heart,age:boss?._heart?.age,enemies:enemies.filter(e=>!e.dead).map(e=>e.type)};}''');ck('Restart remains in secret arena and twelve seconds of real play retain ownership',not row['fail'] and row['heart'] and row['age']>10 and len(row['enemies'])==0,row)
  # Decode and play the actual routed mixer cues; do not replace them with stubs.
  p.evaluate('()=>{Audio.init();Snd.prepare(["bossWeaponCharge","hammerImpact","shieldBossAbsorb","enemyBossCannon"]);}');p.wait_for_timeout(1500)
  for cue in ['bossWeaponCharge','hammerImpact','shieldBossAbsorb','enemyBossCannon']:
   p.evaluate('c=>b20Cue(c)',cue);p.wait_for_timeout(180);row=p.evaluate('''c=>{const P=Snd.pools[c];return{slots:P?.slots?.filter(Boolean).map(v=>({ready:v.el.readyState,time:v.el.currentTime,error:v.el.error?.code||null,attached:v.attached}))||[]};}''',cue);ck('Decoded mixer playback: '+cue,any(s['ready']>=2 and s['time']>0 and not s['error'] for s in row['slots']),row)
  row=p.evaluate('()=>{const b=boss;hitBoss(1e8);hitBoss(1e8);for(let i=0;i<120;i++)updateBoss(1/60);return{dead:b.dead,dying:b.dying,hp:b.hp,projectiles:eBullets.filter(q=>!q.dead&&q._heartOwner===b).length};}');ck('Secret defeat uses native death clock and cancels heart ordnance',row['dead'] and row['dying']>1.9 and row['projectiles']==0,row)
  p.evaluate(shoot.STEP,1500);row=p.evaluate('()=>({state,secret:run._heartMode,result:CH21.result,dead:boss?.dead,dying:boss?.dying,ending:stageEnding})');ck('Complete native death and fly-off exit to secret result without Forge',row['state']=='chromeheart_result' and not row['secret'],row)
  # Confirm normal Hammer still selects its established blue owner.
  p.evaluate(SETUP,{'stage':5,'pilot':'cole','diff':'normal','kind':'chromehammer'});ck('Ordinary Hammer remains ordinary blue fight',p.evaluate('!boss._heart && !!boss._hammer'))
  ck('No page exceptions',not errors,errors);br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2));print(json.dumps({'checks':len(checks),'passed':sum(c['ok'] for c in checks),'errors':errors}),flush=True)
sys.exit(0 if not errors and all(c['ok'] for c in checks) else 1)
