"""Native portal lifecycle, loop joins, Stage 8 continuity and review controls."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import shoot,json,hashlib,io,base64,sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/portal_lifecycle_1011'
M=json.loads((ROOT/'assets/game/shared/fx/portal_lifecycle_1011/manifest.json').read_text(encoding='utf-8'))
checks=[];errors=[];metrics={}
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
def decode(url):return Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGBA')
for bank,entry in M['art'].items():
 ims={p:[Image.open(ROOT/f['path']).convert('RGBA') for f in entry[p]['frames']] for p in ['form','loop','close']}
 dimensions={im.size for clip in ims.values() for im in clip};pivots={tuple(f['pivot']) for p in ims for f in entry[p]['frames']}
 check(bank+': three 32-cell banks on one fixed even canvas/pivot',len(dimensions)==len(pivots)==1 and all(w%2==h%2==0 for w,h in dimensions) and all(len(v)==32 for v in ims.values()))
 check(bank+': all 96 PNG checksums match the owner manifest',all(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'] for p in ims for f in entry[p]['frames']))
 check(bank+': formation and closure share the exact approved join pose',ims['form'][-1].tobytes()==ims['loop'][0].tobytes()==ims['close'][0].tobytes())
 check(bank+': new close is separately drawn, not the opening reversed',sum(a.tobytes()!=b.tobytes() for a,b in zip(ims['form'],reversed(ims['close'])))>=28)
 for phase in ['form','close']:
  check(bank+'/'+phase+': all 32 authored cells differ',len({im.tobytes() for im in ims[phase]})==32)
  check(bank+'/'+phase+': no exterior edge clipping',all(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])[:,3].max()==0 for a in map(np.asarray,ims[phase])))
 if bank!='amethyst_gate':
  check(bank+': close ends fully transparent',ims['close'][-1].getchannel('A').getextrema()==(0,0))
  check(bank+': original loop pixels preserved inside padding',all(ImageChops.difference(im.crop((32,32,352,352)),Image.open(ROOT/f['source']).convert('RGBA')).getbbox() is None for im,f in zip(ims['loop'],entry['loop']['frames'])))
 else:
  shell=Image.open(ROOT/'assets/game/shared/fx/portals_bof_1011/gate-shell.png').convert('RGBA');mask=np.array(Image.open(ROOT/'assets/game/shared/fx/portals_bof_1011/gate-aperture-mask.png'))
  a=np.array(shell);fixed=(mask==0)&(a[:,:,3]>0)
  check('Gate armor stays fixed throughout all three phases',all(np.array_equal(np.array(im)[fixed],a[fixed]) for clip in ims.values() for im in clip))
  check('Gate closure leaves only its original stationary shell',ims['close'][-1].tobytes()==shell.tobytes())

port,stop=shoot.serve(str(ROOT));base=f'http://127.0.0.1:{port}/'
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  def watch(p):
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
   p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p=br.new_page(viewport=dict(width=1280,height=1080));p.set_default_timeout(120000);watch(p)
  p.goto(base+'index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
  p.wait_for_function('()=>Object.keys(PL11_ART).map(bank=>PL11.ready(bank,XART)).every(Boolean)',polling=50)
  check('All 576 frames and fixed gate layers load through native XART',True)
  p.evaluate('''()=>{window.plCalls=[];const draw=ctx.drawImage,get=XART.get;let key=null;
    XART.get=function(k){key=k;return get.apply(this,arguments);};
    ctx.drawImage=function(){const m=ctx.getTransform();plCalls.push({key,args:Array.from(arguments).slice(1),matrix:[m.a,m.b,m.c,m.d,m.e,m.f]});key=null;return draw.apply(this,arguments);};
    window.plRestore=()=>{ctx.drawImage=draw;XART.get=get;};
    window.plFixture=(bank,phase,t,blend=true,rotate=true)=>{
      ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#0d1720';ctx.fillRect(0,0,VW,VH);
      const pose=phase==='sequence'?PL11.sequence(bank,t,{loop:64/PL11_ART[bank].fps,blend}):PL11.sample(bank,phase,t,{blend});
      if(!rotate)pose.rotation=0;
      PL11.draw(ctx,pose,VW/2,VH/2,bank==='amethyst_gate'?340:420,k=>XART.get(k));return cv.toDataURL();
    };}''')
  for bank in M['art']:
   for phase in ['form','loop','close']:
    renders=[];fps=M['art'][bank]['fps']
    for i in range(32):
     t=i/fps if phase=='loop' else i/31*(32/fps)
     renders.append(decode(p.evaluate('([b,ph,t])=>plFixture(b,ph,t,false,false)',[bank,phase,t])))
     if i%8==7:p.wait_for_timeout(10)
    check(bank+'/'+phase+': all authored keys render through the game context',True)
    if bank in M['main']:
     w,h=renders[0].size;sheet=Image.new('RGB',(1600,round(h/w*320)),'#0d1720')
     for col,i in enumerate([0,8,16,24,31]):sheet.paste(renders[i].resize((320,sheet.height),Image.Resampling.NEAREST),(col*320,0))
     sheet.save(OUT/f'{bank}_{phase}-native.png')
   fps=M['art'][bank]['fps'];cycle=32/fps
   before=decode(p.evaluate('([b,t])=>plFixture(b,"loop",t)',[bank,cycle-.001]));after=decode(p.evaluate('([b,t])=>plFixture(b,"loop",t)',[bank,cycle+.001]))
   old_a=decode(p.evaluate('([b,t])=>plFixture(b,"loop",t,false)',[bank,31/fps]));old_b=decode(p.evaluate('b=>plFixture(b,"loop",0,false)',bank))
   gap=float(np.abs(np.array(before).astype(float)-np.array(after).astype(float)).mean());rawgap=float(np.abs(np.array(old_a).astype(float)-np.array(old_b).astype(float)).mean())
   check(bank+': rendered last-to-first boundary has no image reset',gap<rawgap*.18,dict(continuous=gap,hardSwitch=rawgap));metrics[bank]={'continuousSeam':gap,'unblendedSeam':rawgap}
   check(bank+': one-shots clamp, and long idle clocks stay in the loop',p.evaluate('b=>{const a=PL11.sample(b,"form",999),c=PL11.sample(b,"close",999),l=PL11.sample(b,"loop",999);return a.done&&c.done&&a.from===31&&c.from===31&&!l.done&&l.from>=0&&l.from<32;}',bank))
   if bank in M['main']:
    turned=[];changes=[]
    for progress in [.125,.25,.5,.75,.875]:
     rotating=decode(p.evaluate('([b,t])=>plFixture(b,"form",t,true,true)',[bank,cycle*progress]))
     still=decode(p.evaluate('([b,t])=>plFixture(b,"form",t,true,false)',[bank,cycle*progress]))
     changes.append(float(np.abs(np.array(rotating).astype(float)-np.array(still).astype(float)).mean()));turned.append(rotating)
    check(bank+': circular formation is visible in rendered pixels',min(changes)>.05,changes)
    q=p.evaluate('b=>{const d=32/PL11_ART[b].fps,poses=Array.from({length:65},(_,i)=>PL11.sample(b,"form",i*d/64));return {angles:poses.map(p=>p.rotation),loop:PL11.sample(b,"loop",0).rotation,close:PL11.sample(b,"close",0).rotation};}',bank)
    check(bank+': one forward turn settles at the original loop orientation',q['angles'][0]==q['angles'][-1]==q['loop']==q['close']==0 and all(a<b for a,b in zip(q['angles'][:-2],q['angles'][1:-1])) and q['angles'][-2]>6.28,q)
    endpoint=decode(p.evaluate('([b,t])=>plFixture(b,"form",t)',[bank,cycle]));first=decode(p.evaluate('b=>plFixture(b,"loop",0)',bank))
    before=decode(p.evaluate('([b,t])=>plFixture(b,"form",t)',[bank,cycle-.001]))
    join=float(np.abs(np.array(before).astype(float)-np.array(first).astype(float)).mean());metrics[bank]['formationJoin']=join
    check(bank+': forming rotation meets the loop without a visible reset',endpoint.tobytes()==first.tobytes() and join<.6,join)
    q=p.evaluate('([b,t])=>{plFixture(b,"form",t,false);const q=plCalls[plCalls.length-1],f=PL11_ART[b].form.frames[0],a=q.args,m=q.matrix,lx=a[0]+f.pivot[0]*a[2]/f.w,ly=a[1]+f.pivot[1]*a[3]/f.h;return {center:[m[0]*lx+m[2]*ly+m[4],m[1]*lx+m[3]*ly+m[5]],expected:[VW/2*SS,VH/2*SS],restored:ctx.getTransform().a===SS&&ctx.getTransform().b===0};}',[bank,cycle*.25])
    check(bank+': native transform keeps the aperture fixed and restores the context',q['restored'] and all(abs(a-b)<.001 for a,b in zip(q['center'],q['expected'])),q)
    sheet=Image.new('RGB',(1600,round(turned[0].height/turned[0].width*320)),'#0d1720')
    for i,im in enumerate(turned):sheet.paste(im.resize((320,sheet.height),Image.Resampling.NEAREST),(i*320,0))
    sheet.save(OUT/f'{bank}_forming-turn-native.png')
    if bank=='amethyst_gate':
     mask=decode(p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#000";ctx.fillRect(0,0,VW,VH);const k=340/512;ctx.drawImage(XART.get("pl11_gate_mask"),VW/2-256*k,VH/2-352*k,512*k,640*k);return cv.toDataURL();}'))
     fixed=np.array(mask)[:,:,0]==0;base_pixels=np.array(turned[0])[fixed]
     check('Gate shell and exterior remain pixel-stationary during the entire turn',all(np.array_equal(np.array(im)[fixed],base_pixels) for im in turned))
    frames=[]
    for i in range(129):
     im=decode(p.evaluate('([b,t])=>plFixture(b,"sequence",t)',[bank,i/fps]));frames.append(im.resize((480,512),Image.Resampling.NEAREST))
     if i%12==11:p.wait_for_timeout(10)
    frames[0].save(OUT/f'{bank}-sequence-native.webp',save_all=True,append_images=frames[1:],duration=round(1000/fps),loop=1,lossless=True,method=2)
  called={q['key'] for q in p.evaluate('plCalls') if q['key']};expected={f['key'] for b in M['art'].values() for ph in ['form','loop','close'] for f in b[ph]['frames']}
  check('All 576 registered keys reach the game context drawImage',expected.issubset(called),{'missing':list(expected-called)[:8]})
  p.evaluate('plRestore()')
  # Actual encounter owners: preserve the clock/anchor over the phase switch,
  # pause-safe simulation, and exercise forming + loop + close in the finale.
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=8,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(8).ready}',polling=50)
  p.evaluate('''()=>{diffKey='furious';DIFF=difficultyForRun('arcade','furious');coopOn=false;BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;H3.ending=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];special=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.invuln=1e9;camX=0;spawnBoss(curStage.boss);boss.enter=false;j3Encounter(boss,1);boss._r30.mode='dr5Reform';boss._r30.t=5.5;j3State(boss).pt11Portal={x:240,y:200,t:5.5,size:340};}''')
  p.wait_for_function('()=>{r30Warm();return PL11_GAME.banks.map(b=>PL11.ready(b,XART)).every(Boolean)}',polling=50)
  def snap(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();window.__bofFit();}')
   p.wait_for_timeout(30);p.screenshot(path=str(OUT/(name+'.png')))
  p.evaluate('()=>{j3State(boss).pt11Portal.t=.4;}');snap('stage8-forming-turn')
  check('Stage 8 reformation uses the circular formation in-game',p.evaluate('PL11_GAME.last.phase==="form"&&PL11_GAME.last.rotation>0'))
  p.evaluate('()=>{j3State(boss).pt11Portal.t=5.5;}')
  snap('stage8-reformation')
  q=p.evaluate('''()=>{pt11ReformDraw(boss);const before={...PL11_GAME.last},Q=j3State(boss).pt11Portal;
    j3Encounter(boss,2);boss._r30.mode='voidIntro1005';boss._r30.t=0;on5IntroDraw(boss);
    return {before,after:PL11_GAME.last,clock:j3State(boss).pt11Portal.t,kept:j3State(boss).pt11Portal.x===Q.x&&j3State(boss).pt11Portal.y===Q.y};}''')
  check('Stage 8 phase handoff retains exact animation frame, fractional phase and anchor',q['kept'] and q['clock']==5.5 and all(q['before'][k]==q['after'][k] for k in ['from','to','mix','rotation','x','y']),q)
  p.evaluate('()=>{boss._r30.t=.7;j3State(boss).pt11Portal.t=6.2;}');snap('stage8-expanding-portal')
  q=p.evaluate('''()=>{const Q=j3State(boss).pt11Portal;window.plPauseClock=Q.t;window.plPauseState=state;setState('paused');return true;}''')
  step_error=p.evaluate(shoot.STEP,30)
  q=p.evaluate('()=>{const stopped=j3State(boss).pt11Portal.t===plPauseClock;state=plPauseState;return stopped;}') and not step_error
  check('Pause does not advance the portal simulation clock',q)
  for t,label in [(.8,'forming'),(3.6,'loop'),(6.9,'closing'),(7.7,'closed')]:
   p.evaluate('t=>{boss._r30.mode="dr5Portal";boss._r30.t=t;PL11_GAME.last=null;r30DrawBoss(boss);}',t)
   q=p.evaluate('PL11_GAME.last');check('Homeward portal '+label+' uses the new authored phase',q is not None and q['phase']==('form' if t<2 else 'loop' if t<6.2 else 'close'),q)
   if label=='forming':check('Homeward portal forms with a circular turn in-game',q is not None and q['rotation']>0,q)
   snap('homeward-'+label)
  p.close()
  p=br.new_page(viewport=dict(width=1440,height=1080),reduced_motion='reduce');p.set_default_timeout(120000);watch(p)
  p.goto(base+'docs/previews/portals_1011/index.html?effect=green_rift&revision=lifecycle');p.wait_for_function('PORTAL_REVIEW.state.ready')
  check('Review loads all 480 frames and respects reduced motion',p.evaluate('!PORTAL_REVIEW.state.playing&&Object.values(PORTAL_REVIEW.images).every(b=>Object.values(b).every(a=>a.length===32&&a.every(im=>im.complete)))'))
  for bank in M['main']:
   p.locator(f'[data-bank="{bank}"]').click()
   for phase in ['form','loop','close']:
    p.locator('#mode').select_option(phase);p.locator('#frame').fill('16');p.locator('#frame').dispatch_event('input')
    check(bank+'/'+phase+': selector and frame scrub display the requested pose',p.evaluate('PORTAL_REVIEW.state.bank')==bank and p.evaluate('PORTAL_REVIEW.state.phase')==phase and p.evaluate('PORTAL_REVIEW.state.frame')==16)
   p.locator('#mode').select_option('sequence');p.locator('#frame').fill('16');p.locator('#frame').dispatch_event('input');p.screenshot(path=str(OUT/(bank+'-preview.png')))
  p.locator('[data-bank="blue_rift"]').click();p.locator('#mode').select_option('close');p.locator('#frame').fill('0');p.locator('#frame').dispatch_event('input');p.locator('#next').click()
  check('One-shot frame step advances one authored drawing',p.evaluate('PORTAL_REVIEW.state.frame===1&&!PORTAL_REVIEW.state.playing'))
  p.locator('#mode').select_option('sequence');p.evaluate('()=>{PORTAL_REVIEW.state.playing=true;for(let i=0;i<80;i++)PORTAL_REVIEW.advance(.1);}');done=p.evaluate('({playing:PORTAL_REVIEW.state.playing,phase:PORTAL_REVIEW.state.phase,frame:PORTAL_REVIEW.state.frame})')
  check('Full sequence finishes closed without starting again',not done['playing'] and done['phase']=='close' and done['frame']==31,done)
  p.locator('#play').click();check('Replay restarts formation',p.evaluate('PORTAL_REVIEW.state.phase==="form"&&PORTAL_REVIEW.state.playing'));p.locator('#play').click()
  p.locator('#mode').select_option('loop');p.locator('#seam').check();p.locator('#onion').check();p.locator('#anchor').check();p.screenshot(path=str(OUT/'preview-onion-seam.png'))
  check('Onion and seam controls select the loop boundary',p.evaluate('PORTAL_REVIEW.state.onion&&PORTAL_REVIEW.state.anchor&&PORTAL_REVIEW.state.seam'))
  p.locator('#onion').uncheck();p.locator('#anchor').uncheck();p.locator('#blend').uncheck();check('Raw-frame comparison can disable continuous blending',p.evaluate('PORTAL_REVIEW.current().mix===0'));p.locator('#blend').check()
  p.set_viewport_size(dict(width=390,height=844));p.screenshot(path=str(OUT/'preview-mobile.png'),full_page=True)
  check('Mobile controls and canvas fit the viewport',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  check('No page, console or missing-asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors,metrics=metrics)
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(ROOT/'docs/qa/portal_lifecycle_1011.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
