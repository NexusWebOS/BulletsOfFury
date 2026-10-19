"""Native Chromium proof: fixed armor, shot order, fragments and Earth approach."""
from pathlib import Path
import argparse,base64,io,json,math,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/hammer_finish_1017/native';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--review-only',action='store_true');args=parser.parse_args()
checks=[];errors=[];measurements=[]
def check(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport={'width':1920,'height':1080});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  if not args.review_only:
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof HF17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
   p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
   p.evaluate('''()=>{window.hf17Stats={body:[],retina:[],fx:[],sound:{},legacy:0,fragments:[]};
    for(const key of ['missile','retinaCharge','retinaLockBeep','bossWeaponCharge','expBig','bossShieldStatic']){const fn=Audio.SFX[key];Audio.SFX[key]=function(){hf17Stats.sound[key]=(hf17Stats.sound[key]||0)+1;return fn?.apply(this,arguments);};}
    const cell=hf17Cell,ret=drawBossRetina,old=hammerBossDraw,di=ctx.drawImage;let owner=null;
    hf17Cell=function(name,index,x,y,k,alpha,flash,rot){owner={name,index,x,y,k,alpha,flash,rot,phase:H3.ending?.hf17?.phase,age:H3.ending?.hf17?.age};try{return cell.apply(this,arguments);}finally{owner=null;}};
    ctx.drawImage=function(im,...a){if(owner){const m=ctx.getTransform(),q={...owner,m:[m.a,m.b,m.c,m.d,m.e,m.f],rect:a.slice(-4),key:HF17_ART[owner.name][Math.min(HF17_ART[owner.name].length-1,owner.index|0)].key};if(owner.name==='stunned')hf17Stats.body.push(q);else if(owner.name==='fragments')hf17Stats.fragments.push(q);else hf17Stats.fx.push(q);}return di.call(this,im,...a);};
    drawBossRetina=function(b,x,y){if(H3.ending?.hf17)hf17Stats.retina.push({x,y,core:H3.ending.hf17.core,ready:XART.rdy('nbret_'+_pilotKey())});return ret.apply(this,arguments);};
    hammerBossDraw=function(){if(H3.ending?.hf17&&H3.ending.hf17.phase!=='after')hf17Stats.legacy++;return old.apply(this,arguments);};}''')
   p.evaluate('''()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(5);BAL7.setup({stage:5,kind:'chromehammer',pilot:'cole',diff:'normal',seconds:120,fire:false});hf17Warm();h3Warm();furyShipWarm();}''')
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hf17Warm()&&furyShipReady()&&XART.rdy("h3_earth");}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];B.x=worldWidth()/2;B.y=VH*.31;B.enter=B.dead=B._noHit=false;B._hammer.state='storm_raise';B._hammer.t=2;player.x=B.x;player.y=VH*.81;player.dead=player.out=false;player.invuln=99999;camX=clamp(player.x-VW/2,0,worldWidth()-VW);eBullets=[];pBullets=[];enemies=[];l5Rocks=[];l5RockT=999;stagePlan=[];B.hp=0;bossDie();if(window.__bofFit)__bofFit();SC12.refresh();}''')
   check('Native boss defeat enters the new stationary ending',p.evaluate('B.dead&&!!H3.ending?.hf17&&H3.ending.hf17.phase==="drain"&&B.dying===0'))
   geometry=p.evaluate('Object.fromEntries(Object.entries(HF17_ART).map(([n,a])=>[n,{count:a.length,dimensions:[...new Set(a.map(v=>v.w+"x"+v.h))],pivots:[...new Set(a.map(v=>v.pivot.join(",")))],even:a.every(v=>v.w%2===0&&v.h%2===0)}]))');measurements.append({'geometry':geometry})
   check('All four PixelLab banks have32 even frames and fixed pivots',all(geometry[n]['count']==32 and geometry[n]['even'] and len(geometry[n]['dimensions'])==len(geometry[n]['pivots'])==1 for n in ['drain','pulse','engulf','rupture']),geometry)
   check('The exact authored stun and18 armor cuts are loaded',geometry['stunned']['count']==1 and geometry['fragments']['count']==18 and p.evaluate('hf17Warm()'))
   def ticks(n):
    for i in range(0,n,12):
     err=p.evaluate(shoot.STEP,min(12,n-i))
     if err:errors.append(err)
     p.wait_for_timeout(7)
   def snap(name):p.screenshot(path=str(OUT/(name+'.png')))
   def actor_pixels(flash):
    data=p.evaluate('''flash=>{const e=H3.ending,F=e.hf17,save={phase:F.phase,t:F.t,age:F.age,flash:e.boss.flash};F.phase='pulse';F.t=0;F.age=0;e.boss.flash=flash;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);hf17Actor(e);const png=cv.toDataURL().split(',')[1];ctx.restore();Object.assign(F,{phase:save.phase,t:save.t,age:save.age});e.boss.flash=save.flash;return png;}''',flash)
    return np.array(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGBA'))
   before=actor_pixels(0);after=actor_pixels(.14);changed=np.count_nonzero((before[:,:,3]>128)&(np.max(np.abs(before[:,:,:3].astype(int)-after[:,:,:3].astype(int)),2)>15))
   check('The actual authored stunned armor visibly flashes on impact',int(changed)>1000,{'changedOpaquePixels':int(changed)})
   p.evaluate('hf17Stats.body=[]')
   seen=[];body_anchor=p.evaluate('({...H3.ending.hf17.anchor})');initial_score=p.evaluate('run.score');impact_age=None
   for _ in range(320):
    ticks(4);q=p.evaluate('''()=>{const e=H3.ending,F=e?.hf17;return{phase:F?.phase,age:F?.age,t:F?.t,impacts:F?.impacts,dying:B.dying,x:B.x,y:B.y,legacy:hf17Stats.legacy};}''')
    if q['phase'] not in seen:
     seen.append(q['phase']);snap('phase-'+str(q['phase']))
     if q['phase']=='engulf':impact_age=q['age']
    if q['phase']=='burst' and .7<q['t']<.8:snap('burst-fragments')
    if q['phase']=='burst' and 3<q['t']<3.1:snap('late-armor-drift')
    if q['phase']=='after':break
   check('Drain, core pulse, lock, missile, engulf, burst and aftermath occur in order',seen==['drain','pulse','lock','missile','engulf','burst','after'],seen)
   state=p.evaluate('({events:HF17.events,stats:hf17Stats,anchor:H3.ending.hf17.anchor,core:H3.ending.hf17.core,flash:B.flash,phase:H3.ending.phase})');measurements.append({'finale':{'events':state['events'],'sound':state['stats']['sound'],'seen':seen}})
   check('Exactly one committed missile impact triggers destruction',len([q for q in state['events'] if q['event']=='shot-fired'])==len([q for q in state['events'] if q['event']=='core-impact'])==1)
   check('No combat pose renderer runs after defeat',state['stats']['legacy']==0)
   check('Armor root remains fixed through every drawn intact frame',bool(state['stats']['body']) and all(abs(q['x']-body_anchor['x'])<1e-7 and abs(q['y']-body_anchor['y'])<1e-7 and q['k']==240/208 for q in state['stats']['body']),{'intactDraws':len(state['stats']['body']),'anchor':body_anchor})
   check('No engulf or rupture pixels render before the core impact',all(q['age']>=impact_age-.07 for q in state['stats']['fx'] if q['name'] in ['engulf','rupture']))
   check('Retina draws the real pilot reticle at the measured core',len(state['stats']['retina'])>20 and all(q['ready'] and abs(q['x']-q['core']['x'])<1e-7 and abs(q['y']-q['core']['y'])<1e-7 for q in state['stats']['retina']))
   check('Charge, lock beeps, missile and chromium crackle all fire',all(state['stats']['sound'].get(k,0)>0 for k in ['bossWeaponCharge','retinaCharge','retinaLockBeep','missile','bossShieldStatic']),state['stats']['sound'])
   check('The real impact flash expires normally',state['flash']==0)
   fragments=state['stats']['fragments'];ages={round(q['age']-impact_age,1) for q in fragments}
   check('Every authored armor fragment leaves once the reactor ruptures',len({q['index'] for q in fragments})==18 and all(q['phase']=='burst' for q in fragments))
   check('Armor stays opaque at one scale until each fragment exits the playfield',all(q['alpha']==1 and abs(q['k']-240/208)<1e-8 for q in fragments),{'draws':len(fragments)})
   check('Armor continues scattering beyond the first reactor explosion',any(q['phase']=='burst' and q['age']>impact_age+3.2 for q in fragments))
   check('Many authored explosions follow the scattering armor',p.evaluate('(HF17.explosions||0)>45&&(HF17.draws.breakupExplosion||0)>200'),p.evaluate('({bursts:HF17.explosions,draws:HF17.draws.breakupExplosion})'))
   check('Every fragment physically leaves the screen before the cutaway',p.evaluate('''()=>{const F=H3.ending.hf17;return HF17_ART.fragments.every((a,i)=>{const q=hf17Fragment(F,i,5.1),r=Math.hypot(a.w,a.h)*q.k/2;return q.x+r<F.camX||q.x-r>F.camX+VW||q.y+r<0||q.y-r>VH;});}'''))
   check('Rewards and score are not applied again by the cinematic',p.evaluate('run.score')==initial_score)
   # Escape clocks are intentionally scrambled: only stars may move with them.
   earth=[]
   p.evaluate('''()=>{const e=H3.ending;e.hf17.phase='after';e.sm10.phase='death';delete e.engineDeath;e.t=24;e.phase='descent';e.cheer=H3_CHEERS.length;e.homeAge=3;}''')
   for t in [0,2,4,6,7.9]:
    q=p.evaluate('''t=>{const e=H3.ending;e.descent=t;mapScroll=90000+t*700;_stage5SpaceScroll=60000+t*900;camX=21+t*13;ctx.setTransform(SS,0,0,SS,0,0);h3EndingDraw();SC12.refresh();return HF17.earth;}''',t);earth.append(q);snap('earth-'+str(t).replace('.','-'))
   measurements.append({'earth':earth})
   check('Earth keeps one center despite map, sky and horizontal camera scroll',all(q['center']==earth[0]['center'] for q in earth),earth)
   check('We close on Earth: planet grows while the northbound ship recedes',all(earth[i+1]['size']>earth[i]['size'] and earth[i+1]['ship']['y']<earth[i]['ship']['y'] and earth[i+1]['ship']['size']<earth[i]['ship']['size'] for i in range(4)))
   check('The flight reaches Earth with a smooth scene fade',earth[-1]['ship']['size']<4 and abs(earth[-1]['ship']['y']-earth[-1]['center']['y'])<1)
   p.evaluate('''()=>{const e=H3.ending;e.descent=8.8;e.homeAge=14;e.cheer=H3_CHEERS.length;e.phase='descent';e.t=28;h3EndingDraw();}''');snap('earth-fade')
   check('The end of the Earth approach visibly fades out',p.evaluate('HF17.earth.fade')>.45)
   for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
    p.evaluate('''pk=>{run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);furyShipWarm();H3.ending.descent=3;h3EndingDraw();}''',pk)
    check(pk+' retains the actual native Furyship during reentry',p.evaluate('furyShipReady()&&HF17.earth.ship.size>0'))
   p.evaluate('''()=>{run.pilot='cole';H3.ending.descent=9.79;h3EndingTick(1/30);}''');check('Native ending reaches Stage Clear once',p.evaluate('H3.ending===null&&state===GS.STAGECLEAR'))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/hammer_finale_1017/index.html');p.wait_for_function('ready&&game.contentWindow.eval("!!H3.ending?.hf17")');p.wait_for_timeout(1300);p.screenshot(path=str(OUT/'review-finish.png'))
  check('Review boots the actual finale and normal playfield',p.evaluate('game.contentWindow.eval("run.stage===5&&!!H3.ending.hf17&&SC12.active()")'))
  check('Review isolates saves before the game boots',p.evaluate('game.contentWindow.__hammerFinaleReviewStorage===true'))
  p.click('#earth');p.wait_for_function('game.contentWindow.eval("H3.ending?.phase===\'descent\'")');p.wait_for_timeout(1800);p.screenshot(path=str(OUT/'review-earth.png'))
  check('Review can replay the native anchored Earth approach',p.evaluate('game.contentWindow.eval("HF17.earth?.phase===\'descent\'")'))
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(q['passed'] for q in checks),'failed':[q for q in checks if not q['passed']],'errors':errors,'checks':checks,'measurements':measurements}
(OUT/('review-verification.json' if args.review_only else 'verification.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
