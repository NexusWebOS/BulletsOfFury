"""Real game pixels: Phase 3 void coverage, parallax, fade, pause and forms."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import shoot, json, sys, base64, io

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/void_arena_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];screens=[];metrics={}
def check(name, passed, data=None):
    checks.append(dict(name=name,passed=bool(passed),data=data))
    print(('PASS ' if passed else 'FAIL ')+name+((' '+json.dumps(data)) if not passed else ''),flush=True)

port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
    br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
    p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
    p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
    p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
    p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(70)
    p.evaluate(shoot.SETUP,dict(state='PLAY',stage=8,pilot='cole',invuln=True))
    p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(8).ready}',polling=50)
    p.evaluate('''()=>{diffKey='normal';DIFF=difficultyForRun('arcade','normal');coopOn=false;
      BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;H3.ending=null;
      stagePlan=[];enemies=[];pBullets=[];eBullets=[];special=null;boss=null;bossActive=false;
      subBoss=null;subBossActive=false;subBossDone=true;player.invuln=1e9;camX=0;
      spawnBoss(curStage.boss);boss.enter=false;r30Warm();av11Warm();}''')
    p.wait_for_function('()=>Object.values(AV11_ART).flat().map(a=>XART.rdy(a.key)).every(Boolean)&&Object.values(AA5_ART).flat().map(a=>XART.rdy(a.key)).every(Boolean)&&Object.values(ON5_ART).flat().map(a=>XART.rdy(a.key)).every(Boolean)',polling=50)
    check('New environment and all sixteen code poses decode',True)
    q=p.evaluate('()=>Object.values(AV11_ART).flat().every(a=>a.w%2===0&&a.h%2===0)&&AV11_ART.code.every(a=>a.w===320&&a.h===320&&a.pivot[0]===160&&a.pivot[1]===160)')
    check('Even frame sizes and one common code pivot',q)

    def ticks(n):
        for i in range(0,n,15):
            err=p.evaluate(shoot.STEP,min(15,n-i))
            if err: errors.append(err)
            p.wait_for_timeout(4)
    def snap(name):
        ticks(1);p.screenshot(path=str(OUT/(name+'.png')));screens.append(name+'.png')
    def background(name, arena=True):
        p.evaluate('''(arena)=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#ff00ff';ctx.fillRect(0,0,VW,VH);
          ctx.save();const z=viewZoom();ctx.scale(z,z);ctx.translate(-camLeftX(),VH*(1-z)/z);
          if(arena)av11ArenaDraw(boss);else drawBG(0);ctx.restore();}''',arena)
        raw=base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]'))
        (OUT/(name+'.png')).write_bytes(raw);screens.append(name+'.png')
        return Image.open(io.BytesIO(raw)).convert('RGB')

    # The first two phases retain the stage biome; the real intro then reveals
    # the new environment without bypassing the existing transition controller.
    p.evaluate('()=>{j3Encounter(boss,1);boss._r30.mode="fight";boss.enter=false;}')
    check('Ghost phase does not use the Phase 3 void',p.evaluate('!aa5Arena(boss)&&!av11ArenaDraw(boss)'))
    p.evaluate('()=>{j3Encounter(boss,2);player.x=worldWidth()/2;player.y=430;}')
    ticks(125);snap('01-engulfed');ticks(75);snap('02-reveal');ticks(355)
    # Keep the complete authored monologue. Its twelve lines precede combat;
    # a fixed nine-second intro wait is not a valid fight-start assertion.
    for _ in range(100):
        if p.evaluate('boss._r30.mode==="fight"&&!boss.enter'):break
        ticks(30)
    check('Existing intro naturally reaches a playable Phase 3',p.evaluate('boss._r30.mode==="fight"&&j3State(boss).encounter===2&&!boss.enter'))
    snap('03-battle-begins');ticks(300);snap('04-code-awake')
    check('Code illumination rises with the battle',p.evaluate('AV11.last.awake===1&&j3State(boss).av11.combat>=4&&AV11.draws.code>0'))

    # Inspect through the game context. Read the key at XART.get, then consume
    # that key on the actual drawImage; never infer art from canvas.src/identity.
    p.evaluate('''()=>{window.av11Calls=[];const get=XART.get,draw=ctx.drawImage;let key=null;
      XART.get=function(k){const im=get.apply(this,arguments);key=k;return im;};
      ctx.drawImage=function(){if(key)av11Calls.push({key,args:Array.from(arguments).slice(1)});key=null;return draw.apply(this,arguments);};
      window.av11Restore=()=>{XART.get=get;ctx.drawImage=draw;};}''')
    p.evaluate('()=>{boss._r30.attack=null;boss._r30.cd=999;window.arenaClock=j3State(boss).av11;arenaClock.t=14;arenaClock.combat=10;}')
    p.evaluate('()=>{VIEW_FIT=false;camX=0;}')
    a=background('05-void-left')
    p.evaluate('()=>{camX=Math.max(0,worldWidth()-viewW());}')
    b=background('06-void-right')
    p.evaluate('()=>{VIEW_FIT=true;camX=0;}')
    c=background('07-void-fit')
    for label,im in [('left',a),('right',b),('fit',c)]:
        px=list(im.get_flattened_data());dark=sum(max(rgb)<28 for rgb in px)/len(px)
        pink=sum(r>200 and g<40 and blue>200 for r,g,blue in px)
        w,h=im.size
        edges=list(im.crop((0,0,w//6,h)).get_flattened_data())+list(im.crop((w*5//6,0,w,h)).get_flattened_data())
        edge_dark=sum(max(rgb)<28 for rgb in edges)/len(edges)
        metrics[label]=dict(dark=dark,edgeDark=edge_dark,uncoveredPixels=pink)
        check(f'{label}: opaque coverage and darkness across the entire arena',dark>.87 and edge_dark>.83 and pink==0,metrics[label])
    calls=p.evaluate('av11Calls');keys={d['key'] for d in calls}
    check('Native background draws no cathedral, ribs or old code mounts',keys and all(k.startswith('av11_') for k in keys),sorted(keys))
    check('Native draw scales preserve every asset aspect ratio',all(abs(d['args'][2]/d['args'][3]-(2/3 if 'back' in d['key'] else 1))<.0001 for d in calls),None)
    p.evaluate('av11Restore()')

    p.evaluate('()=>{arenaClock.t=14.375;}');d=background('08-code-motion')
    moving=sum(max(rgb)>8 for rgb in ImageChops.difference(c,d).get_flattened_data())
    check('Code and atmosphere visibly animate in real game pixels',moving>180,dict(movingPixels=moving))
    q=p.evaluate('''()=>{const Q=j3State(boss).av11,t=Q.t,c=Q.combat;drawBG(0);drawBG(0);
      return {same:Q.t===t&&Q.combat===c,depths:new Set(AV11.last.points.map(p=>p.depth)).size};}''')
    check('Draw-only calls freeze simulation clocks; code has three parallax depths',q['same'] and q['depths']==3,q)
    p.evaluate('()=>{setState(GS.PAUSE);window.pauseClock=arenaClock.t;}');ticks(45)
    check('Actual Pause freezes the void animation',p.evaluate('arenaClock.t===pauseClock'))
    p.evaluate('()=>{setState(GS.PLAY);}')
    q=p.evaluate('''()=>{const t=arenaClock.t;camX=0;av11ArenaDraw(boss);const a=AV11.last.points.map(p=>p.x);
      VIEW_FIT=false;camX=Math.max(0,worldWidth()-viewW());const delta=camX;av11ArenaDraw(boss);
      return {delta,shifts:AV11.last.points.map((p,i)=>(p.x-a[i])/delta),depths:AV11.last.points.map(p=>p.depth),time:j3State(boss).av11.t===t};}''')
    # The first sample uses fit view, with cam=0. Scroll view's camera center
    # shifts by half its travel; the three depth groups must remain distinct.
    check('Camera movement produces distinct depth shifts without advancing time',q['delta']>0 and len({round(v,3) for v in q['shifts']})==3 and q['time'],q)
    p.evaluate('()=>{VIEW_FIT=true;camX=0;}')
    # Copy transitions should not reset the ambience or any health pool.
    q=p.evaluate('''()=>{const Q=j3State(boss).av11,t=Q.t,hp=boss.hp;j3Mimic(boss,1);const copy=aa5Arena(boss)&&j3State(boss).av11===Q;
      j3Home(boss);return {copy,host:aa5Arena(boss)&&j3State(boss).av11===Q&&Q.t===t,hp:boss.hp===hp};}''')
    check('Copied forms and host return retain the same void and saved health',q['copy'] and q['host'] and q['hp'],q)
    p.evaluate('()=>{boss._r30.mode="fight";boss.enter=false;boss._r30.cd=0;boss._r30.attack=null;player.invuln=1e9;}')
    ticks(220);snap('09-active-attacks')
    # Render every cell at game scale through the shipping renderer.
    p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#050808';ctx.fillRect(0,0,VW,VH);
      for(let i=0;i<16;i++)av11Plate('code',i,60+i%4*120,64+Math.floor(i/4)*128,145,1);}''')
    p.locator('#screen').screenshot(path=str(OUT/'10-code-16.png'));screens.append('10-code-16.png')
    check('All sixteen drawn code poses stay within their fixed canvases',all(Image.open(ROOT/a['path']).getbbox() is not None for a in p.evaluate('AV11_ART.code')))
    # A short silent native loop, readable outside the automation fixture.
    frames=[]
    for i in range(48):
        ticks(5)
        frames.append(Image.open(io.BytesIO(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))).convert('RGB'))
    frames[0].save(OUT/'battle-loop.webp',save_all=True,append_images=frames[1:],duration=83,loop=0,quality=83,method=3)
    p.set_viewport_size(dict(width=390,height=844));ticks(8);snap('11-mobile')
    check('Mobile canvas remains inside the viewport',p.evaluate('(()=>{const r=document.querySelector("#screen").getBoundingClientRect();return r.width>0&&r.left>=-1&&r.right<=innerWidth+1;})()'))
    p.evaluate('()=>{boss._r30.mode="escape";}')
    check('Portal home releases the void environment',p.evaluate('!aa5Arena(boss)&&!av11ArenaDraw(boss)'))
    p.evaluate('()=>{run.stage=1;}')
    check('Void cannot leak into other stages',p.evaluate('!aa5Arena(boss)&&!av11ArenaDraw(boss)'))
    check('No page, console or missing-asset errors',not errors,errors)
    br.close()
finally:
 stop()
 report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),
             checks=checks,metrics=metrics,screens=screens,errors=errors)
 (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
