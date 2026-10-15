"""Observe all nine Wind weapons through real Forge simulation and Chromium pixels."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,base64
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/wind_projectiles_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,yes,data=None):
    checks.append(dict(name=name,passed=bool(yes),data=data));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready}')
  p.wait_for_function('()=>WP11_KEYS.map(a=>XART.rdy(a.key)).every(Boolean)',polling=50)
  check('All144 registered Wind poses decode in the running game',p.evaluate('WP11_KEYS.length===144'))
  # The real context uses alpha:false. A cleared pixel is opaque black, so inspect
  # visible RGB ink here; alpha padding is separately verified by the owning builder.
  q=p.evaluate('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);const out=[];for(const a of WP11_KEYS){ctx.clearRect(0,0,256,256);ctx.drawImage(XART.get(a.key),0,0);const d=ctx.getImageData(0,0,256,256).data;let ink=0,edge=0,green=0;for(let y=0;y<256;y++)for(let x=0;x<256;x++){const i=(y*256+x)*4;if(d[i]+d[i+1]+d[i+2]>12){ink++;if(x<6||x>=250||y<6||y>=250)edge++;if(d[i+1]>d[i]*1.3&&d[i+1]>d[i+2]*1.08)green++;}}out.push({key:a.key,ink,edge,green});}ctx.restore();return out;}''')
  check('Native canvas confirms clear outer borders on every pose',all(a['ink']>50 and a['edge']==0 for a in q),dict(frames=len(q)))
  check('Every combat pose contains visible emerald Wind energy',all(a['green']>30 for a in q))
  for slot in range(9):
   family=['bullets','spread','missile','laser','gust','tornado','mist','heavy','electric'][slot]
   for level in [1,5]:
    p.evaluate('''cfg=>{window.__windPreview=forgePreviewNew(cfg.slot,'wind',cfg.level);__windPreview.audition=false;}''',dict(slot=slot,level=level))
    # Yield between batches while the owning simulation advances ordinary shots.
    for _ in range(5):
     p.evaluate('()=>{for(let i=0;i<12;i++)forgePreviewTick(__windPreview,400,500,1/60);}');p.wait_for_timeout(20)
    q=p.evaluate('''()=>{const get=XART.get,draw=ctx.drawImage;let key,seen=[];try{XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){if(key?.startsWith('wp11_'))seen.push(key);return draw.call(this,im,...args)};ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);forgePreviewDraw(__windPreview,20,20,400,500);ctx.restore();return {error:__windPreview.err,keys:[...new Set(seen)],kinds:[...new Set(__windPreview.bullets.map(b=>b.kind))],draws:{...WP11.draws}};}finally{XART.get=get;ctx.drawImage=draw;}}''')
    check(f'{family} level{level}: real weapon preview draws its own Wind reel',not q['error'] and any(k.startswith('wp11_'+family+'_') for k in q['keys']),q)
    if level==5:
     shot=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=400;c.height=500;c.getContext('2d').putImageData(ctx.getImageData(20,20,400,500),0,0);return c.toDataURL('image/png');}''')
     (OUT/(family+'-native.png')).write_bytes(base64.b64decode(shot.split(',',1)[1]))
  q=p.evaluate('''()=>{
   startRun(6);ht27Stop();BOFCinematicDirector.cancel();H3.ending=null;H3.release=false;
   AP10_X.intro=null;story=fb2Talk=s6Opening=null;_cinematicHidePlayer=false;
   state=GS.PLAY;Object.assign(run,{mode:'campaign',stage:6,pilot:'cole',spaceMode:false,sonicT:0,dkT:0,
    _spaceShadowHeld:false,_spaceShadowCharge:0,weapon:3,wlevel:5,wlevels:WEAPONS.map(()=>5),
    forge:{3:{elem:'wind',lv:5}},forgeForms:{3:{wind:{elem:'wind',lv:5}}},forgeElems:{wind:1},
    infusion:{elem:'wind',lv:5,hits:0,_forgeW:3}});
   player.reset();player.x=worldWidth()/2;player.y=VH-86;player.invuln=40002;player._fuse=0;player._chgOn=false;
   stagePlan=[];spawnClock=9999;pBullets=[];eBullets=[];enemies=[];powerups=[];special=null;const before=WP11.draws.laser||0;
   pShoot();updatePlay(1/60);story=fb2Talk=s6Opening=null;drawWorld(0);drawHUD();
   return {live:(WP11.draws.laser||0)>before,carriers:pBullets.map(b=>({kind:b.kind,element:b._inf})),state};
  }''')
  check('The Stage6 world renderer paints the actual equipped Wind laser',q['live'],q)
  p.screenshot(path=str(OUT/'stage6-live-native.png'))
  # Inspect the 16-frame loop at a stable world position using the same game context.
  q=p.evaluate('''()=>{const out={};ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const f of WP11_FAMILIES){const bank=AP10_FX_ART['wind_'+f],frames=[];for(let i=0;i<16;i++){const a=bank[i];ctx.clearRect(0,0,256,256);ctx.drawImage(XART.get(a.key),0,0);const d=ctx.getImageData(0,0,256,256).data;let hash=2166136261;for(let n=0;n<d.length;n+=4)hash=Math.imul(hash^d[n]^d[n+1]^d[n+2]^d[n+3],16777619);frames.push(hash>>>0);}out[f]=new Set(frames).size;}ctx.restore();return out;}''')
  check('Chromium sees16 distinct drawn poses in each family',all(n==16 for n in q.values()),q)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/wind_projectiles_1011/index.html');p.wait_for_function('window.windReviewReady===true')
  p.screenshot(path=str(OUT/'review.png'))
  check('Animated review loads all9 reels and45 green tier badges',p.locator('.badge').count()==45 and p.locator('.reel-card').count()==9)
  p.locator('#onion').check();p.locator('#pause').click();p.locator('#frame').fill('15');p.screenshot(path=str(OUT/'review-onion.png'))
  p.set_viewport_size(dict(width=480,height=900));p.wait_for_timeout(80)
  check('Wind review fits a narrow viewport',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  check('No page, console, renderer or missing-asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(a['passed'] for a in checks),failed=sum(not a['passed'] for a in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
