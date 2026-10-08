import sys,json,traceback,time
from pathlib import Path
GAME=Path(__file__).resolve().parents[1];OUT=GAME/'_shots/enemy_hud_1007c';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(GAME/'_BUILD_SOURCE'));import shoot
from playwright.sync_api import sync_playwright
port,stop=shoot.serve(str(GAME));errors=[];checks=[];shots=[];started=time.time()
def check(ok,what,detail=None):
 checks.append({'pass':bool(ok),'check':what,'detail':detail});print(('PASS ' if ok else 'FAIL ')+what,flush=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--no-sandbox','--mute-audio']);page=browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=90000);page.wait_for_function('window.__bofFrames>4',timeout=90000)
  page.evaluate(shoot.TRAP_RAF);page.wait_for_timeout(100);page.add_script_tag(content=(GAME/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  def ready():
   for i in range(1000):
    r=page.evaluate('() => {stageLoadTick();drawWorld(0);return stageLoadInfo(run.stage);}')
    if r['ready']:return r
    page.wait_for_timeout(30)
   return r
  def capture(name):
   page.evaluate(shoot.STEP,1);page.evaluate('()=>{player.invuln=9999;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   page.locator('#game-frame').screenshot(path=str(OUT/(name+'.png')));shots.append(name+'.png')
  for stage in range(1,10):
   kind=page.evaluate('(n)=>debugFightFor(n,"boss").kind',stage)
   c={'stage':stage,'kind':kind,'diff':['easy','normal','hard','furious'][(stage-1)%4],'pilot':'yuri','seconds':10}
   if stage==8:c['form']='host'
   page.evaluate('(c)=>BAL7.setup(c)',c)
   page.evaluate('()=>{player.invuln=9999;B.hp=B.maxhp*.57;if(B._whv){B._whv.cy=190;B._whv.cx=worldWidth()/2;B.x=B._whv.cx;B.y=190;}}')
   r=ready();check(r['ready'] and not r['failed'],f'Stage {stage}: required assets ready',r)
   if stage in (1,7):
    page.evaluate('()=>{for(let i=0;i<1500&&(boss._ovIntro&&!boss._ovIntro.done||!bossHealthVisible(boss));i++)updateBoss(1/60);}')
    ready()
   if stage==9:
    page.evaluate('()=>{for(let i=0;i<120;i++)updateBoss(1/60);const F=B._s9fusion;for(const q of [F.left,F.right]){F.hit=q;s9FusionHit(B,q.hp+1);}for(let i=0;i<160;i++)updateBoss(1/60);}')
    ready()
   capture(f'level_{stage:02d}_boss')
   q=page.evaluate('()=>({bar:EH7.lastBoss,oldRoots:Object.keys(XART.img).filter(k=>k.startsWith("eh7_stage_")&&!k.endsWith(String(run.stage).padStart(2,"0")))})')
   check(q['bar'] and q['bar']['theme']==f'stage_{stage:02d}',f'Stage {stage}: correct live boss palette',q['bar'])
   check(not q['oldRoots'],f'Stage {stage}: preceding stage HUD textures retired',q['oldRoots'])
   # Exercise all authored housings through the game's Canvas2D renderer. Read
   # actual pixels at both sides of a drain; includes empty and refilled bars.
   pix=page.evaluate('''() => {
    const out=[],theme=eh7Theme(boss);ctx.save();ctx.setTransform(1,0,0,1,0,0);
    for(const variant of ['boss','bossShield','mini','miniShield']){
     const f=eh7Frame(theme,variant,436),w=f.hp;
     for(const frac of [0,.25,.5,.75,1]){
      ctx.clearRect(0,0,cv.width,cv.height);eh7Paint(f,20,20,frac,frac);
      const sample=(t,well=w)=>Array.from(ctx.getImageData(Math.round(20+well[0]+well[2]*t),Math.floor(20+well[1]+well[3]*.58),1,1).data);
      out.push({variant,frac,left:sample(.12),right:sample(.88),shield:f.shield?{left:sample(.12,f.shield),right:sample(.88,f.shield)}:null});
     }
    }ctx.restore();return out;
   }''')
   for q in pix:
    light=lambda color:max(color[:3])>60 and max(color[:3])-min(color[:3])>25
    ok=light(q['left'])==(q['frac']>.12) and light(q['right'])==(q['frac']>.88)
    if q['shield']:ok=ok and light(q['shield']['left'])==(q['frac']>.12) and light(q['shield']['right'])==(q['frac']>.88)
    check(ok,f"Stage {stage}: {q['variant']} pixels at {q['frac']:.0%}",q)
   mini=page.evaluate('(n)=>SUBBOSS[n]?.kind',stage)
   if mini:
    page.evaluate('(c)=>BAL7.setup(c)',{**c,'kind':mini,'mini':True,'form':None});ready()
    page.evaluate('()=>{B.hp=B.maxhp*.42;B.enter=false;player.invuln=9999;if(B._s9rift){for(let i=0;i<110;i++)s9VoidHorizonTick(B,1/60);B._s9rift.core.hp=B._s9rift.core.maxhp*.42;}}');ready();capture(f'level_{stage:02d}_mini')
    q=page.evaluate('()=>EH7.lastBoss');check(q and q['theme']==f'stage_{stage:02d}' and q['variant'].startswith('mini'),f'Stage {stage}: live miniboss palette',q)
  # Both routes on every requested difficulty. Independent HP, real cloak flags,
  # and death visibility must not alter any fighter health value.
  for diff in ['easy','normal','hard','furious']:
   for route in [None,'right']:
    page.evaluate('(c)=>BAL7.setup(c)',{'stage':6,'kind':'rebelsquad','diff':diff,'pilot':'yuri','seconds':10});ready()
    page.evaluate('(route)=>{if(route)run._gp4StageX=route;else delete run._gp4StageX;for(const q of B._rebels.ships)q.hp=q.max*(.2+.15*q.i);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}',route)
    q=page.evaluate('()=>({bars:EH7.lastRebels,health:B._rebels.ships.map(q=>q.hp/q.max)})')
    check(len(q['bars'])==5 and all(abs(v['frac']-q['health'][i])<1e-8 for i,v in enumerate(q['bars'])),f'{diff} Rebels {"Stage X" if route else "Stage 6"}: five independent fills',q)
    if diff=='normal':capture('rebels_'+('stage_x' if route else 'stage_06'))
    hidden=page.evaluate('()=>{B._rebels.ships[1].frCloak=1;B._rebels.ships[4].dead=true;drawWorld(0);return EH7.lastRebels.map(q=>q.pilot);}')
    check(hidden==['voss','rook','kaia'],f'{diff} Rebels {route}: hidden on cloak/death',hidden)
  for route in [None,'left']:
   page.evaluate('(c)=>BAL7.setup(c)',{'stage':6,'kind':'warhive','diff':'furious','pilot':'yuri','seconds':10});ready()
   page.evaluate('(r)=>{if(r)run._gp4StageX=r;else delete run._gp4StageX;B._whv.cy=190;B.x=B._whv.cx=worldWidth()/2;B.y=190;B.hp=B.maxhp*.65;player.invuln=9999;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}',route)
   q=page.evaluate('()=>EH7.lastBoss');check(q['theme']==('harrier' if route else 'stage_06'),f'Harrier routing {route}',q)
   capture('harrier_'+('stage_x' if route else 'stage_06'))
  # Current gallery loads one image at a time and every requested tab resolves.
  page.goto(f'http://127.0.0.1:{port}/_ART_SOURCES/hud_themes_1007/review.html#stage_04',wait_until='load')
  for key in [f'stage_{n:02d}' for n in range(1,10)]+['stage_x','rebels']:
   page.locator(f'button[data-theme="{key}"]').click();page.wait_for_function('(k)=>document.body.dataset.ready===k',arg=key)
   q=page.evaluate('()=>({w:art.naturalWidth,h:art.naturalHeight,images:document.images.length})');check(q['w']>1000 and q['images']==1,'Gallery '+key,q)
  page.screenshot(path=str(OUT/'gallery_rebels.png'));browser.close()
except Exception as e:
 errors.append(traceback.format_exc());print(traceback.format_exc(),flush=True)
finally:
 stop();summary={'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'errors':errors,'elapsed':round(time.time()-started,1),'shots':shots,'checks':checks}
 (OUT/'validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='checks'}),flush=True)
 sys.exit(1 if errors or summary['failed'] else 0)
