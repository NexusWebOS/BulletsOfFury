"""Native baseline/repair proof for Hammer burst damage, aircraft and Stage7 arrival."""
from pathlib import Path
import ast,argparse,base64,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_revision_1017';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--before',action='store_true');args=ap.parse_args();tag='before' if args.before else 'after'
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
errors=[];checks=[];data={}
def check(name,ok,d=None):checks.append(dict(name=name,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(d)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(5);}")
  def setup(stage,kind=None,diff='normal'):
   p.keyboard.up('j');p.evaluate(SETUP,dict(stage=stage,kind=kind,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    VP12.next=CP12.next=EP13.next=99999;TARGET17.nextTank=HM17.next=99999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=true;aminiTriggered=true;
    player.invuln=999999;player.dead=player.out=false;run.shield=0;run.speed=0;l5Rocks=[];l5RockT=99999;furyLegacyShip=false;
    if(window.B){B._be=null;B._noHit=false;B.enter=false;B.x=worldWidth()/2;B.y=170;B._drawY=B.y;}
    player.x=worldWidth()/2;player.y=VH-100;camX=clamp(player.x-VW/2,0,worldWidth()-VW);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}''')
  def frames(n):
   for i in range(0,n,8):
    err=p.evaluate(shoot.STEP,min(8,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
   p.screenshot(path=str(O/(tag+'-'+name+'.png')))
  data['damage']=[]
  for level in ([5] if args.before else [1,3,5]):
   setup(5,'chromehammer');p.evaluate('''lv=>{B._cin30Spoke=B._fb2IntroSeen=true;B._hammer.intro1002=true;B._hammer.mode='hammer';hammerState(B,'hammer');run.spaceMode=true;run.gravityShipReady=true;run.spaceWeapon=0;run.spaceLevels=[lv,lv,lv];run._spaceVolleyCd=0;player.fireCd=0;window.damageRows=[];window.hammerTransitions=[];window.nativeKinds={};
    const fn=spaceBulletHit;spaceBulletHit=function(q){nativeKinds[q.kind]=(nativeKinds[q.kind]||0)+1;return fn.apply(this,arguments);};
    window.__qaTick=function(){if(boss&&!boss.dead){player.x=clamp(boss.x,camLeftX()+50,camRightX()-50);player.y=VH-65;}const h=boss?._hammer;
     if(h&&hammerTransitions.at(-1)?.state!==h.state)hammerTransitions.push({t:stageTimer,state:h.state,hp:boss.hp,armor:fr27Armor(boss)?.hp,heal:h.recovery?.status,counter:h.recovery?._hc17?.hits});};}''',level)
   p.keyboard.down('j')
   for sec in range(26):
    frames(60)
    row=p.evaluate('''()=>({time:stageTimer,hp:B.hp,max:B.maxhp,armor:fr27Armor(B)?.hp,dead:B.dead,state:B._hammer.state,heal:B._hammer.recovery?.status,counter:B._hammer.recovery?._hc17?.hits,guard:B._guard17,restored:B._hammer.restorationSeen})''')
    data['damage'].append(dict(level=level,**row))
    if sec in [4,12,24]:snap('hammer-level'+str(level)+'-'+str(sec))
    if row['dead']:break
   p.keyboard.up('j');data['transitions'+str(level)]=p.evaluate('hammerTransitions');data['nativeKinds'+str(level)]=p.evaluate('nativeKinds');p.evaluate('window.__qaTick=null')
   print(json.dumps({'level':level,'timeline':[q for q in data['damage'] if q['level']==level],'transitions':data['transitions'+str(level)]}),flush=True)
  setup(5,'chromehammer');p.evaluate('''()=>{fr27BeginArmor(B);B._hammer.frArmor.activated=true;B._noHit=false;fr27Restore(B,.1,false,false);window.passiveBefore=hc17Counter(B).hits;for(let i=0;i<6;i++){_dmgBullet={kind:'spaceVolley',x:B.x,y:B.y};B._hammerModuleHit='hammer';hammerBossDamage(B,100);} _dmgBullet=null;}''')
  data['passiveCounter']=p.evaluate('({before:passiveBefore,status:B._hammer.recovery.status,hits:B._hammer.recovery._hc17?.hits})');print('PASSIVE '+json.dumps(data['passiveCounter']),flush=True)
  setup(4);p.wait_for_function('()=>{a17Warm();return XART.rdy("overhaul_jet_desert_hull")&&!!air13Pose("s4interceptor","heading",Math.PI/2)}',polling=50)
  data['camo']=p.evaluate('''()=>{const e=spawnEnemy('s4interceptor',worldWidth()/2,210,{});e.spin=.2;e._air13Motion={kind:'heading',angle:Math.PI/2};window.camo=e;
   const rows=[];for(const ratio of [1,.49,.2]){e.hp=e.maxhp*ratio;e.flash=0;const get=XART.get,keys=[];XART.get=function(k){keys.push(k);return get.apply(this,arguments);};ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);try{drawEnemy(e);}finally{XART.get=get;}let green=0,gray=0;const d=ctx.getImageData(0,0,cv.width,cv.height).data;for(let i=0;i<d.length;i+=4){if(d[i]+d[i+1]+d[i+2]<40)continue;if(d[i+1]>d[i]*1.08&&d[i+1]>d[i+2]*1.15)green++;if(Math.max(d[i],d[i+1],d[i+2])-Math.min(d[i],d[i+1],d[i+2])<20)gray++;}rows.push({ratio,green,gray,keys:[...new Set(keys)]});ctx.restore();}return rows;}''');print('CAMO '+json.dumps(data['camo']),flush=True)
  snap('camo-low-hp')
  data['intro']=p.evaluate('({gate:typeof BOFCampaignStory.drawGateLaunch,post6:BOFCampaignStory.script(6).length})');print('INTRO '+json.dumps(data['intro']),flush=True)
  br.close()
finally:stop()
check('No page, console, draw or asset errors',not errors,errors)
(O/(tag+'.json')).write_text(json.dumps(dict(data=data,checks=checks,errors=errors),indent=2)+'\n',encoding='utf-8')
if errors:sys.exit(1)
