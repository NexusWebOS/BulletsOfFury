"""Real Chromium: Furnace arm ownership, committed eye sweep and hit pixels."""
from pathlib import Path
import argparse,base64,io,json,math,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/furnace_pixellab_1017/native';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--logic-only',action='store_true');args=parser.parse_args()
checks=[];errors=[];measures=[]
def check(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  index=(ROOT/'index.html').read_bytes()
  if b'assets/furnace_assault_1017.js' not in index:
   tags=(b'<script src="assets/furnace_head_art_1017.js?v=furnace-1017"></script>\n' if (ROOT/'assets/furnace_head_art_1017.js').exists() else b'')+b'<script src="assets/furnace_assault_1017.js?v=furnace-1017"></script>\n'
   needle=b'<!-- Campaign world now renders once, on the full-width game canvas. -->';assert index.count(needle)==1;index=index.replace(needle,tags+needle)
   p.route('**/index.html*',lambda route:route.fulfill(body=index,content_type='text/html'));(OUT/'candidate-index.html').write_bytes(index)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof FURNACE17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  audio=p.evaluate('''()=>{window.f17Audio={};const original=fztSfx;fztSfx=function(name){f17Audio[name]=(f17Audio[name]||0)+1;return original.apply(this,arguments);};return ['furnaceLaserCharge','furnaceReactorHum','furnaceLaserBurst','furnaceFlameRelease'].map(name=>({name,registered:typeof Audio.SFX[name]==='function'}));}''')
  check('Head charge, rumble, laser release and flame cues have native sound owners',all(a['registered'] for a in audio),audio)
  def ticks(n):
   for i in range(0,n,12):
    error=p.evaluate(shoot.STEP,min(12,n-i))
    if error:errors.append(error)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}');p.screenshot(path=str(OUT/(name+'.png')))
  def head_pixels(name):
   raw=p.evaluate('''()=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,worldWidth(),viewH());f17PaintHead(boss);ctx.restore();return ctx.canvas.toDataURL('image/png');}''')
   data=base64.b64decode(raw.split(',',1)[1]);(OUT/(name+'.png')).write_bytes(data);return np.asarray(Image.open(io.BytesIO(data)).convert('RGBA'))
  def setup(diff,phase):
   r=p.evaluate(shoot.SETUP,{'state':'PLAY','stage':2,'pilot':'cole','invuln':True});assert r.get('ok'),r
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(2).ready;}')
   p.evaluate('''([diff,phase])=>{diffKey=diff;DIFF=DIFFS[diff];BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;subBossDone=true;boss=null;bossActive=false;spawnBoss('infernoreaver');furnaceSync(boss);furnaceEnter(boss,phase);boss._fz.trans=0;boss._mwStun=0;if(boss._mwBarrier){boss._mwBarrier.active=false;boss._mwBarrier.breakT=0;}player.invuln=9999;player.x=worldWidth()*.65;player.y=VH*.8;FURNACE17.events=[];window.f17Seen=new WeakSet();window.f17Stats={flameFrames:0,laserFrames:0,both:0,originError:0,fullTurn:0,shake:0,headKeys:[]};
    window.__qaTick=()=>{const F=boss?._fz,Q=F?._f17;if(!F)return;const S=f17Stats;S.flameFrames+=F.beams.some(q=>q._f17Flame)?1:0;const beams=F.beams.filter(q=>q._f17Laser);S.laserFrames+=beams.length?1:0;S.both+=beams.length===2?1:0;S.shake=Math.max(S.shake,shake||0);if(Q)S.fullTurn=Math.max(S.fullTurn,Math.abs(Q.roll));
     if(FURNACE17.last?.bank==='spin'&&!S.headKeys.includes(FURNACE17.last.key))S.headKeys.push(FURNACE17.last.key);
     if(beams.length){const sockets=f17Sockets(boss);for(let i=0;i<beams.length;i++)S.originError=Math.max(S.originError,Math.hypot(beams[i].x-sockets[i].x,beams[i].y-sockets[i].y));}
    };}''',[diff,phase])
   p.wait_for_function('()=>PT11_ART.furnace_head.map(a=>XART.rdy(a.key)).every(Boolean)')
   if not args.logic_only:p.evaluate('f17Warm()');p.wait_for_function('()=>f17Keys().map(k=>XART.rdy(k)).every(Boolean)')
  for diff in ['easy','normal','hard','furious']:
   setup(diff,'arms');ticks(720);snap(diff+'-arms')
   q=p.evaluate('''()=>({stats:f17Stats,flameDraws:FURNACE17.draws.flame,magma:FURNACE17.events.filter(e=>e.event==='cannon-magma').length,waves:FURNACE17.events.filter(e=>e.event==='cannon-wave').length,arms:boss._fz.phase})''')
   measures.append({'difficulty':diff,'arms':q})
   check(diff+' restores actual continuous flamethrower frames',q['stats']['flameFrames']>15 and q['flameDraws']>0,q)
   check(diff+' cannon retains magma balls and also releases fire waves',q['magma']>0 and q['waves']>0,q)
   check(diff+' remains in its native armor phase',q['arms']=='arms',q)
   setup(diff,'head');C=p.evaluate('f17Tune()');ticks(round(C['warm']*60*.70));snap(diff+'-head-windup')
   check(diff+' warns and rumbles before the laser sweep',p.evaluate('f17Stats.shake>1&&boss._fz.tells.length===2&&boss._fz.beams.length===0'))
   ticks(round(C['warm']*60*.30)+round(C['active']*60*.35));snap(diff+'-head-spin')
   check(diff+' twin eye lasers are active together',p.evaluate('f17Stats.both>8&&boss._fz.beams.filter(q=>q._f17Laser).length===2'))
   ticks(round(C['active']*60*.65)+round(C['recover']*60*.35));snap(diff+'-head-recover')
   q=p.evaluate('()=>({stats:f17Stats,events:FURNACE17.events,beams:boss._fz.beams.length,headPhase:boss._fz.phase,pool:boss._fz.pools.head})');measures.append({'difficulty':diff,'head':q})
   check(diff+' completes a committed 360-degree turn',q['stats']['fullTurn']>=math.pi*2-1e-6,q)
   check(diff+' eye-laser roots remain mounted to their visible sockets',q['stats']['originError']<1e-5,q)
   check(diff+' has a beam-free recovery and a shootable head',q['beams']==0 and q['headPhase']=='head' and q['pool']>0,q)
   if not args.logic_only:check(diff+' draws the actual generated rotation bank',len(q['stats']['headKeys'])>=26,{'uniqueHeadKeys':len(q['stats']['headKeys'])})
  setup('normal','head');ticks(40);before_hit=head_pixels('head-pixels-before-hit')
  damage=p.evaluate('''()=>{const F=boss._fz,out=[];for(const kind of ['bullet','missile','iceorb','beam']){const before=F.pools.head;_dmgBullet={kind,x:boss.x,y:boss.y,_el:kind==='iceorb'?'ice':null};_lastHitX=boss.x;_lastHitY=boss.y;hitBoss(5);out.push({kind,damage:before-F.pools.head,flash:boss.flash,partFlash:F.flash.head});}return out;}''')
  after_hit=head_pixels('head-pixels-real-hit');changed=int(np.count_nonzero((before_hit[:,:,3]>128)&(np.max(np.abs(after_hit[:,:,:3].astype(int)-before_hit[:,:,:3].astype(int)),2)>8)))
  check('The actual damaged head pixels visibly flash in the native renderer',changed>250,{'changedOpaquePixels':changed})
  snap('head-real-hit');check('Precision rounds, missiles, ice orb and beam all damage the head and flash',all(q['damage']>0 and (q['flash']>0 or q['partFlash']>0) for q in damage),damage)
  check('Ice orb keeps the authored fire-boss damage advantage',next(q['damage'] for q in damage if q['kind']=='iceorb')>next(q['damage'] for q in damage if q['kind']=='bullet'),damage)
  ticks(40);head_pixels('head-pixels-expired');check('Native owner and head hit-flash timers expire normally',p.evaluate('boss.flash<=0&&boss._fz.flash.head<=0&&FURNACE17.last.flash===0'))
  for weapon,w,variant,missile in [('precision',0,None,False),('missile',0,None,True),('ice-orb',5,'iceorb',False)]:
   setup('normal','head');ticks(round((p.evaluate('f17Tune().warm')+.25)*60))
   baseline=p.evaluate('''([w,variant,missile])=>{run.weapon=w;run.wlevels??={};run.wvars??={};run.wlevels[w]=3;run.wlevel=3;run.wvars[w]=variant;run.bombs=10;player.fireCd=0;player.x=boss.x;player.y=boss.y+165;Input.keys.j=!missile;retina.target=null;retina.phase=null;if(missile)useBomb(null);return boss._fz.pools.head;}''',[w,variant,missile])
   ticks(120);q=p.evaluate('''()=>{Input.keys.j=false;return {pool:boss._fz.pools.head,dead:boss.dead,kind:run.weapon,projectiles:pBullets.length,beams:boss._fz.beams.filter(q=>q._f17Laser).length};}''')
   check('Real '+weapon+' projectiles can hit the rotating head',q['pool']<baseline or q['dead'],dict(before=baseline,after=q))
   check(weapon+' damage does not cancel or shoot down the eye lasers',q['beams']==2 or q['dead'],q)
  setup('normal','head');p.evaluate('''()=>{window.f17ContactCalls=0;const native=playerHit;playerHit=function(){f17ContactCalls++;return native.apply(this,arguments);};}''')
  ticks(75);check('Eye-laser windup is a warning, not a damaging beam',p.evaluate('f17ContactCalls===0&&boss._fz.beams.length===0'))
  ticks(55);p.evaluate('''()=>{const q=boss._fz.beams.find(q=>q._f17Laser);if(!q)throw Error('No live beam');const k=180/q.len;player.x=q.x+(q.ex-q.x)*k;player.y=q.y+(q.ey-q.y)*k;}''');ticks(1)
  check('The actual continuous eye beam reaches native player collision',p.evaluate('f17ContactCalls>0'))
  if not args.logic_only:
   check('PixelLab spin, charge and laser banks are installed',p.evaluate('!!FURNACE17.art&&F17_ART.spin.frames.length>=30&&F17_ART.charge.frames.length>=16&&F17_ART.laser.frames.length>=16&&FURNACE17.draws.laser>0'))
  check('Native charge, rumble and release sound cues actually fire',p.evaluate("['furnaceLaserCharge','furnaceReactorHum','furnaceLaserBurst','furnaceFlameRelease'].every(k=>f17Audio[k]>0)"))
  if not args.logic_only:
   p.goto(f'http://127.0.0.1:{port}/docs/previews/furnace_1017/index.html');p.wait_for_function('loaded&&game.contentWindow.eval("boss?._fz?.phase===\'head\'&&boss._fz.beams.length===2")');p.screenshot(path=str(OUT/'review-head.png'))
   check('Review opens the actual head encounter at the regular field of view',p.evaluate('game.contentWindow.eval("run.stage===2&&!!FURNACE17.art&&boss._fz.phase===\'head\'")'))
   p.click('[data-phase="arms"]');p.wait_for_function('game.contentWindow.eval("boss?._fz?.phase===\'arms\'&&boss._fz.beams.some(q=>q._f17Flame)")');p.screenshot(path=str(OUT/'review-arms.png'))
   check('Review can restart the actual flamethrower and cannon encounter',True)
  check('No page, console or asset errors',not errors,errors);browser.close()
finally:stop()
report={'checks':checks,'errors':errors,'measurements':measures,'logicOnly':args.logic_only,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks)}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed',len(errors),'browser errors');sys.exit(1 if report['failed'] else 0)
