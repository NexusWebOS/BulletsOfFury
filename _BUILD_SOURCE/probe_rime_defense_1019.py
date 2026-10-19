"""Rime Wall: real primary core hits, frost charge, beams, mortar warnings and desperation."""
from pathlib import Path
import ast,argparse,json,sys,http.server,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/rime_defense_1019';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--before',action='store_true');args=ap.parse_args();tag='before' if args.before else 'after'
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:650]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.pilot='cole';startRun(3)")
  p.evaluate('''()=>{window.rimeShots=[];window.rimeDamage=[];const shot=eShootT,hit=hitBoss;
   eShootT=function(){const q=shot.apply(this,arguments);rimeShots.push(q);return q;};
   hitBoss=function(d){const b=boss,hp=b?.hp,r=hit.apply(this,arguments);if(b?._ship==='cryospear')rimeDamage.push({kind:_dmgBullet?.kind,loss:hp-b.hp,x:_lastHitX,y:_lastHitY});return r;};
   window.rimeKeys=[];const get=XART.get;XART.get=function(k){rimeKeys.push(k);return get.apply(this,arguments);};
   window.rimeBeamDraws=[];const beam=av3Beam;av3Beam=function(g,x,y,angle,length,width,color){let n=0;const draw=g.drawImage;g.drawImage=function(){n++;return draw.apply(this,arguments);};let result;try{result=beam.apply(this,arguments);}finally{g.drawImage=draw;}rimeBeamDraws.push({x,y,color,draws:n,ready:XART.rdy('av3_laser_beams')});return result;};
   window.rimeTransitions=[];const set=er26Set;er26Set=function(b,mode){if(b?._ship==='cryospear')rimeTransitions.push({mode,time:b._er26?.t,stack:new Error().stack});return set.apply(this,arguments);};
   window.rimePixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return d;};
   window.rimeChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>100&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    if extra:p.evaluate(extra)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(tag+'-'+name+'.png')))
  def setup(diff='normal',disarmed=False):
   p.keyboard.up('j');p.evaluate(SETUP,dict(stage=3,pilot='cole',kind='cryospear',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();er26Warm();return stageLoadReady(3)&&bmfReady("game")&&XART.rdy("mr27_rime")&&(typeof rd19Ready!=="function"||rd19Ready())}',polling=50)
   p.evaluate('''disarmed=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=thaw=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;warnT=0;warnKind=null;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;stageEnding=0;bossDefeated=false;Input.keys={};Input.mouse.down=false;
    run.spaceMode=false;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};weaponFormSelect(7,{kind:'primary1003b',id:'mg'});
    run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.fireCd=0;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;playerHit=()=>{};powerups=[];
    B._be=null;B.enter=B._noHit=false;B._phaseInvuln=0;B.x=worldWidth()/2;B.y=B._er26.home;B._drawY=B.y;mr27Init(B);if(disarmed)B._mr27.parts.forEach(q=>{q.dead=true;q.hp=0;});
    camX=clamp(player.x-VW/2,0,worldWidth()-VW);rimeShots=[];rimeDamage=[];SC12.refresh();__bofFit();}''',disarmed);frames(1)
  if args.before:
   setup();snap('intact')
   row=p.evaluate('''()=>({hull:{x:B.x,y:B.y,w:B.w,h:B.h},core:mr27Shape(B,'core'),book:er26Book(B),at:mr27At(B,B.x,B.y),hp:B.hp})''');(O/'before-state.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row),flush=True)
   p.evaluate('''()=>{er26Set(B,'sa14-ice');B._er26.t=B._er26.warm*.8;B._sa14.glow=.8;rimeKeys=[];}''');snap('charge');print('chargeKeys',p.evaluate('[...new Set(rimeKeys)].filter(k=>/lightning|cryo|ice|rime/.test(k))'),flush=True)
   setup(disarmed=True);p.evaluate('''()=>{B._er26.mode='recover';B._er26.dur=4;B._er26.t=0;window.hpBefore=B.hp;const c=mr27Shape(B,'core');player.x=c.x-(wm26PlayerNose().x-player.x);player.y=c.y+155;player.fireCd=0;}''')
   p.keyboard.down('j');frames(120);p.keyboard.up('j');snap('disarmed-fire');print('gunRouting',p.evaluate('({loss:hpBefore-B.hp,hits:rimeDamage,core:mr27Shape(B,"core"),at:mr27At(B,B.x,B.y)})'),flush=True)
   frames(720);print('disarmedHistory',p.evaluate('({history:B._er26.history,shots:rimeShots.map(q=>({kind:q.kind,source:q._er26Source})),hp:B.hp})'),flush=True)
   # Export the actual core/hull and mid-reel candidate effects through XART.
   p.evaluate('''()=>{for(const k of ['l23fx_cryo_ball_4','l23fx_rime_orb_4','l23fx_rime_laser_6','l23fx_rime_mg_4','polish_ice_ordnance','efx_burst_ice'])XART.rdy(k);}''')
   p.wait_for_function('()=>XART.rdy("l23fx_cryo_ball_4")&&XART.rdy("l23fx_rime_orb_4")&&XART.rdy("l23fx_rime_laser_6")&&XART.rdy("polish_ice_ordnance")',polling=50)
   for name in ['l23fx_cryo_ball_4','l23fx_rime_orb_4','l23fx_rime_laser_6','l23fx_rime_mg_4','polish_ice_ordnance','efx_burst_ice']:
    data=p.evaluate('''k=>{if(!XART.rdy(k))return null;const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1];}''',name)
    if data:(O/(name+'.png')).write_bytes(base64.b64decode(data))
  else:
   for diff in ['normal','hard','furious']:
    setup(diff)
    check(diff+' regular portrait playfield and whole authored hull',p.evaluate('VW===480&&VH===512&&B._mr27.skin==="rime"&&B._mr27.parts.length===4'))
    # The native renderer must fetch and actually blit every delivered pose.
    art=p.evaluate('''()=>{rimeKeys=[];const draws=[],draw=ctx.drawImage;ctx.drawImage=function(...a){draws.push([a[0].width,a[0].height]);return draw.apply(this,a);};try{for(const [name,frames]of Object.entries(RD19_ART.banks))for(let i=0;i<frames.length;i++)rd19Effect(name,B.x,B.y,.5,(i+.01)/18);}finally{ctx.drawImage=draw;}return{keys:[...new Set(rimeKeys.filter(k=>k.startsWith('rd19_')))],draws};}''')
    check(diff+' all 96 PixelLab poses reach the game context drawImage',len(art['keys'])==96 and len(art['draws'])==96,dict(keys=len(art['keys']),draws=len(art['draws'])))
    p.evaluate('''()=>{er26Set(B,'sa14-mg');B._er26.t=B._er26.warm+.02;er26Combat(B,1/60);rimeKeys=[];}''');snap(diff+'-ice-bullets')
    check(diff+' ordinary boss MG bullets use a registered authored ice projectile',p.evaluate('eBullets.some(q=>q._rd19IceSlug)&&rimeKeys.includes(RD19_ART.bullet.key)'))
    # Do not infer native artwork from a filename, canvas .src or identity.
    p.evaluate('''()=>{er26Set(B,'rd19-lasers');B._er26.t=B._er26.warm*.72;er26Combat(B,1/60);rimeKeys=[];}''');snap(diff+'-laser-warning')
    keys=p.evaluate('[...new Set(rimeKeys)]')
    check(diff+' actual FOV plates and icy reactor art render during laser warning',any('bmfx_fov_' in k for k in keys) and any(k.startswith('rd19_swirl_') for k in keys),keys)
    p.evaluate('''()=>{window.warnAngles=B._rd19.beam.angles.slice();B._er26.t=B._er26.warm+.02;er26Combat(B,1/60);rimeKeys=[];rimeBeamDraws=[];}''');snap(diff+'-laser-release')
    laser=p.evaluate('({keys:[...new Set(rimeKeys)].filter(k=>/rime_laser|av3_laser_beams/.test(k)),draws:rimeBeamDraws,beam:B._rd19.beam,mode:B._er26.mode,t:B._er26.t})')
    check(diff+' actual ice laser frame renders from native gun mounts',any(q['color']=='ice' and q['draws']>0 and q['ready'] for q in laser['draws']) and bool(laser.get('beam',{})) and bool(laser['beam'].get('released')),laser)
    p.evaluate('''()=>{const q=mr27Shape(B,'gunL');_lastHitX=q.x;_lastHitY=q.y;hitBoss(4);window.moduleFlash=B._mr27.parts.find(p=>p.id==='gunL').flash;}''')
    flash=p.evaluate('''()=>{const part=mr27Part(B,'gunL'),old=part.flash,owner=B.flash,draw=()=>mr27Draw(B);part.flash=B.flash=0;const before=rimePixels(draw);part.flash=old;B.flash=owner;const after=rimePixels(draw);return {changed:rimeChanged(before,after),timer:part.flash,owner:B.flash};}''')
    check(diff+' actual damaged module pixels flash',flash['changed']>15 and flash['timer']>0,flash)
    p.evaluate('mr27Tick(B,.3)');check(diff+' module flash expires through native clock',p.evaluate('mr27Part(B,"gunL").flash===0'))
    setup(diff)
    p.evaluate('''()=>{er26Set(B,'sa14-ice');B._er26.t=B._er26.warm*.8;B._sa14.glow=.8;rimeKeys=[];}''');snap(diff+'-icy-charge')
    keys=p.evaluate('[...new Set(rimeKeys)]')
    check(diff+' icy charge draws frost banks without Storm lightning art',any(k.startswith('rd19_charge_') for k in keys) and not any('s4w_lightning_ball_' in k or 'chain_lightning' in k for k in keys),keys)
    p.evaluate('''()=>{er26Set(B,'rd19-mortars');B._er26.t=B._er26.warm*.85;er26Combat(B,1/60);}''');snap(diff+'-shoulder-charge')
    check(diff+' shoulder sockets remain outside the destroyable target roster',p.evaluate('retinaBossTargets(B).every(q=>!/SHOULDER|shoulder/.test(q._retinaId||q.kind||""))'))
    sockets=p.evaluate('''()=>{const C=rd19State(B),old=sg19Shoulders,scale=Math.min(B.w/658,B.h/579);SG19.draws=[];old(B,0);const idle=SG19.draws.slice();SG19.draws=[];old(B,1);const hot=SG19.draws.slice();
     const draw=()=>mr27Draw(B);sg19Shoulders=()=>{};const unlit=rimePixels(draw);sg19Shoulders=old;const lit=rimePixels(draw);let changed=0,outside=0;
     for(let i=0;i<lit.length;i+=4){if(Math.max(Math.abs(lit[i]-unlit[i]),Math.abs(lit[i+1]-unlit[i+1]),Math.abs(lit[i+2]-unlit[i+2]))<8)continue;
      changed++;const x=(i/4)%cv.width+camX,y=Math.floor(i/4/cv.width);if(![-1,1].some(s=>{const a=rd19Port(B,s);return ((x-a.x)/(27*scale+2))**2+((y-a.y)/(26*scale+2))**2<1;}))outside++;}
     const a=rd19Port(B,-1);B.x+=19;B.y+=13;B._drawY=B.y;SG19.draws=[];old(B,.8);const moved=SG19.draws[0];B.x-=19;B.y-=13;B._drawY=B.y;
     return{idle,hot,changed,outside,moved:{dx:moved.x-a.x,dy:moved.y-a.y},keys:SG19.draws.map(q=>q.key)};}''')
    check(diff+' shoulder pixel glow is present at idle and rises on charge',len(sockets['idle'])==2 and all(q['intensity']>0 for q in sockets['idle']) and all(q['intensity']>sockets['idle'][i]['intensity'] for i,q in enumerate(sockets['hot'])),sockets)
    check(diff+' actual shoulder-light pixels stay inside authored cavities',sockets['changed']>60 and sockets['outside']==0,sockets)
    check(diff+' shoulder light follows translated hull at one source scale',abs(sockets['moved']['dx']-19)<.01 and abs(sockets['moved']['dy']-13)<.01,sockets['moved'])
    wash=p.evaluate('''()=>{const A=B._sa14,glow=A.glow,flash=B.flash,shape=MR27_ART.rime.cells[0],scale=Math.min(B.w/shape[2],B.h/shape[3]),draw=()=>mr27Blit('rime',0,{x:B.x,y:B.y,w:shape[2]*scale,h:shape[3]*scale},0,null,B);B.flash=0;A.glow=0;const a=rimePixels(draw);A.glow=1;const b=rimePixels(draw);A.glow=glow;B.flash=flash;return rimeChanged(a,b);}''')
    check(diff+' charge retains authored hull palette outside pixel emitters',wash==0,wash)
    p.evaluate('''()=>{B._er26.t=B._er26.warm+.01;er26Combat(B,1/60);window.mortar=groundTargetingFx.find(q=>q._rd19Mortar);window.mortarAim={x:mortar.x,y:mortar.y};mortar.t=mortar.warn-.18;player.x=camRightX()-50;player.y=VH-70;rimeKeys=[];}''');snap(diff+'-mortar-descent')
    check(diff+' mortar descends at a committed ground Retina',p.evaluate('rimeKeys.some(k=>k.startsWith("rd19_mortar_"))&&!mortar.track&&mortar.x===mortarAim.x&&mortar.y===mortarAim.y'))
    p.evaluate('''()=>{mortar.t=mortar.warn+.15;mortar.impact=true;rimeKeys=[];}''');snap(diff+'-mortar-impact')
    check(diff+' mortar impact uses the new frost spiral and beam',p.evaluate('rimeKeys.some(k=>k.startsWith("rd19_mortar_"))&&rimeKeys.some(k=>k.startsWith("rd19_swirl_"))'))
    # Real keyboard primary fire, actual movement/collision/hitBoss pipeline.
    setup(diff,True)
    p.evaluate('''()=>{er26Set(B,'recover');B._er26.dur=15;B._er26.t=0;const c=mr27Shape(B,'core');player.x=c.x-(wm26PlayerNose().x-player.x);player.y=c.y+165;player.fireCd=0;window.gunHP=B.hp;rimeDamage=[];Input.keys={};}''')
    p.keyboard.down('j');frames(110);p.keyboard.up('j');snap(diff+'-critical-primary')
    hit=p.evaluate('''()=>({loss:gunHP-B.hp,hits:rimeDamage,core:mr27Shape(B,'core'),targets:retinaBossTargets(B).map(t=>t._retinaId)})''')
    check(diff+' ordinary primary fire reaches and critically damages exposed core',hit['loss']>0 and any(q['loss']>0 and q.get('kind')=='mg' for q in hit['hits']),hit)
    check(diff+' manual lock target follows the seated critical core',p.evaluate('(()=>{const p=mr27Shape(B,"core"),t=retinaBossTargets(B).find(t=>t._retinaId==="rd19-core");return t&&Math.hypot(t.x-p.x,t.y-p.y)<.01;})()'))
    # Independent final attacks continue with the normal native loop.
    p.evaluate('''()=>{er26Set(B,'rd19-ram');B._er26.t=B._er26.warm*.8;er26Combat(B,1/60);}''');snap(diff+'-ram-warning')
    frames(120);snap(diff+'-final-defense')
    check(diff+' final defense stays finite and actually releases a ram',p.evaluate('Number.isFinite(B.x+B.y+B.hp)&&RD19.events.some(e=>e.event==="ram-release")'))
   # The miniboss shares frost charge artwork without replacing its encounter.
   setup('furious');p.evaluate('''()=>{boss=null;bossActive=false;spawnSubBoss__inner('frostcruiser');B=subBoss;B.enter=B._noHit=false;B._be=null;B.x=worldWidth()/2;B.y=B._er26.home;B._drawY=B.y;er26Set(B,'cryo-missiles');B._er26.t=B._er26.warm*.8;rimeKeys=[];}''');snap('miniboss-icy-charge')
   check('Frost Cruiser keeps ice identity and draws PixelLab cold charge',p.evaluate('B._mr27.skin==="pt11_frost"&&B._er26.form==="ice"&&!B._s3Nuclear&&rimeKeys.some(k=>k.startsWith("rd19_"))'))
   # Exercise the delivered review UI as well as controlled encounter fixtures.
   p.goto(f'http://127.0.0.1:{port}/docs/previews/rime_defense_1019/index.html?scene=mortars&difficulty=furious')
   p.wait_for_function('document.querySelector("#status").textContent.startsWith("Shoulder laser mortars -")')
   f=p.locator('#game').element_handle().content_frame()
   check('Delivered full-FOV review boots the real Furious Stage 3',f.evaluate('run.stage===3&&diffKey==="furious"&&VW===480&&VH===512&&SC12.mode==="sides"&&rd19Ready()'))
   check('Review saves are isolated from campaign storage',f.evaluate('window.__rimeReviewStorage===true'))
   p.screenshot(path=str(O/'review-mortars-furious.png'))
   p.locator('#scene').select_option('critical');p.wait_for_function('document.querySelector("#status").textContent.startsWith("Exposed critical core -")')
   check('Delivered critical-core scene exposes all four original weapons',f.evaluate('boss._rd19.exposed&&rd19Disarmed(boss)&&retinaBossTargets(boss).some(t=>t._retinaId==="rd19-core")'))
   p.screenshot(path=str(O/'review-critical.png'))
   p.locator('#scene').select_option('mini');p.wait_for_function('document.querySelector("#status").textContent.startsWith("Frost Cruiser charge -")')
   check('Review selector loads the actual Frost Cruiser encounter',f.evaluate('subBoss._ship==="frostcruiser"&&subBoss._mr27.skin==="pt11_frost"'))
   p.set_viewport_size(dict(width=600,height=900));p.wait_for_timeout(100)
   check('Compact review retains the same 480x512 playfield',f.evaluate('VW===480&&VH===512&&SC12.mode==="compact"'))
   p.screenshot(path=str(O/'review-compact.png'))
   p.set_viewport_size(dict(width=1600,height=1000));p.goto(f'http://127.0.0.1:{port}/docs/previews/rime_defense_1019/frames.html')
   p.wait_for_function('document.querySelector("#status").textContent.includes("/ 32")');p.locator('#pause').click();p.locator('#frame').fill('17');p.locator('#frame').dispatch_event('input')
   for bank,size in [('swirl',[384,384]),('charge',[384,384]),('mortar',[192,576])]:
    p.locator('#bank').select_option(bank)
    check('Delivered '+bank+' frame player and onions use fixed bank geometry',p.evaluate('s=>{const c=document.querySelector("#view");return c.width===s[0]&&c.height===s[1]&&document.querySelector("#onion").checked;}',size))
    p.screenshot(path=str(O/('frames-'+bank+'.png')))
  br.close()
finally:stop()
if not args.before:
 check('No page, console, draw or asset errors',not errors,errors)
 report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
 (O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
 sys.exit(1 if report['failed'] else 0)
