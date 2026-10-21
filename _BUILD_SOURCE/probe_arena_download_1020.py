from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import ast,base64,hashlib,http.server,io,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot,probe_tutorial_1015 as tut
Q=R/'_shots/arena_download_1020';Q.mkdir(exist_ok=True)
def literal(file,name):return next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE'/file).read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
SETUP=literal('probe_feedback_1002.py','SETUP');BOOT=literal('probe_boss_redesign_1020.py','BOOT').replace('drawWorld(0);drawHUD();','const inv=player.invuln;player.invuln=0;drawWorld(0);player.invuln=inv;SC12.invalidate();SC12.refresh();')
checks=[];errors=[];requests=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+n+(' '+json.dumps(data)[:1000] if not ok else ''),flush=True)
def shot(p,name):
 data=base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]'));(Q/(name+'.png')).write_bytes(data);return Image.open(io.BytesIO(data)).convert('RGB')
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda c:errors.append(c.text[:600]) if c.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('request',lambda r:requests.append(r.url) if 'arena_download_1020/' in r.url or 'lava_pixellab_1020/' in r.url else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(600,400)
  ck('New lava and arena textures stay outside title/boot loading',not requests,requests[:])
  p.evaluate(SETUP,dict(stage=2,pilot='cole',diff='normal'))
  p.wait_for_function('()=>{ASSETS.ready=true;stageLoadTick();UI20.warm();return stageLoadReady(2)&&BOFSTAGE2LAVA.ready&&XART.rdy(_levelCfg().master)&&XART.rdy("nsa_ship_cole")&&XART.rdy("nbret_cole")}')
  cfg=p.evaluate('_levelCfg(2)');ref=json.loads((R/'_ART_SOURCES/arena_download_1020/references/native.json').read_text(encoding='utf-8'))[1]
  ck('Level2 native terrain, route dimensions and combat configuration remain intact',cfg==ref['cfg'] and p.evaluate('worldWidth()')==ref['world'],cfg)
  ck('Level2 loading includes lava and excludes Dracodia arena art',p.evaluate('_stageLoads[2].keys.includes(S2L20_ART.key)&&!_stageLoads[2].keys.includes("ad20_jungle_terrain")'))
  rows=[];lava=[]
  for i in range(32):
   row=p.evaluate('''i=>{efxClock=(i+.001)/12;mapScroll=1500;shake=0;player.invuln=0;
    const im=XART.get(S2L20_ART.key),draw=ctx.drawImage,calls=[];ctx.drawImage=function(image,...a){if(image===im)calls.push(a);return draw.call(this,image,...a);};
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);ctx.drawImage=draw;return{phase:S2L20.frame,calls};}''',i)
   rows.append(row);lava.append(shot(p,'lava-frame-'+str(i)))
  ck('All32 lava phases draw at their real fixed224-square cells',all(r['phase']==i and r['calls'] and all(c[:4]==[2+i%8*228,2+i//8*228,224,224] and c[6:]==[224,224] for c in r['calls']) for i,r in enumerate(rows)))
  lava[0].save(Q/'native-lava.gif',save_all=True,append_images=lava[1:],duration=83,loop=0,optimize=True)
  p.screenshot(path=str(Q/'level2-desktop.png'))
  lavaDiff=[]
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=2,pilot='cole',diff=diff));lavaDiff.append(p.evaluate('()=>{const n=S2L20.draws;drawBG(0);return S2L20.draws>n}'))
  ck('Level2 molten water palette applies on all4 difficulties',all(lavaDiff))
  # The original cracked lava reels remain untouched and are used only by the Phoenix arena.
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole',diff='normal'))
  p.wait_for_function('()=>{ASSETS.ready=true;stageLoadTick();return stageLoadReady(8)&&v18Warm()&&ad20Warm()}')
  p.evaluate(BOOT)
  p.evaluate('setup20(0)')
  curtain=json.loads((R/'assets/game/levels/stage_08/boss/arena_download_1020/manifest.json').read_text(encoding='utf-8'))['curtain']
  cell_checks=[]
  atlas=Image.open(R/curtain['path']).convert('RGBA')
  for i,c in enumerate(curtain['cells']):
   sample=p.evaluate('''i=>{const a=AD20_ART.curtain,im=XART.get(a.key),base=ctx.drawImage,calls=[];ctx.drawImage=function(image,...args){if(image===im)calls.push(args);return base.call(this,image,...args);};
    ad20Curtain((i+.001)/a.fps,viewTopY()+viewH()/2);ctx.drawImage=base;
    const out=document.createElement('canvas');out.width=out.height=256;out.getContext('2d').drawImage(im,...a.cells[AD20.curtainFrame],0,0,256,256);
    return{phase:AD20.curtainFrame,calls,png:out.toDataURL().split(',')[1]};}''',i)
   native=Image.open(io.BytesIO(base64.b64decode(sample.pop('png')))).convert('RGBA');x,y,w,h=c
   cell_checks.append(sample['phase']==i and bool(sample['calls']) and all(a[:4]==c for a in sample['calls']) and native.tobytes()==atlas.crop((x,y,x+w,y+h)).tobytes())
  ck('All32 authored PixelLab curtain phases select exact lossless native cells',curtain['frames']==32 and all(cell_checks),{'frames':curtain['frames'],'checks':cell_checks})
  ck('Stage8 gate warms all arena, wireframe, curtain and original lava keys',p.evaluate('ad20Keys().every(k=>_stageLoads[8].keys.includes(XART.root(k)))'))
  # Warm native actor/mixer caches before measuring arena-only work.
  for form,theme in [(1,'jungle'),(2,'lava'),(6,'sky'),(8,'space')]:
   p.evaluate('f=>setup20(f)',form);p.evaluate('paint20');shot(p,'fight-'+theme);p.screenshot(path=str(Q/('fight-'+theme+'-desktop.png')))
   ck('Correct live '+theme+' terrain selected for form'+str(form),p.evaluate('AD20.last?.theme')==theme)
  ck('Phoenix draws original animated cracked lava through its new transparent land',p.evaluate('AD20.draws.originalLava>0') and p.evaluate('AD20_ART.arenas.lava.terrain.key')=='ad20_lava_terrain')
  allocation=p.evaluate('''()=>{const base=document.createElement;let n=0;document.createElement=function(tag,...a){if(tag==='canvas')n++;return base.call(this,tag,...a);};
   const size=[];try{for(let i=0;i<60;i++){B._r30.clock+=1/60;ad20Scene(B,'sky');size.push(AD20.plate);}}finally{document.createElement=base;}return{allocations:n,plateStable:size.every(a=>JSON.stringify(a)===JSON.stringify(size[0]))};}''')
  ck('Arena rendering allocates no canvas per frame and holds terrain scale/pivot',allocation['allocations']==0 and allocation['plateStable'],allocation)
  anchors=p.evaluate('''()=>{const out=[];for(const x of [250,340,430]){player.x=x;updateCamX();ad20Scene(B,'sky');out.push({...AD20.plate,cam:camX});}return out;}''')
  ck('Solid arena architecture remains world anchored as the pilot moves laterally',all(all(a[k]==anchors[0][k] for k in ['x','y','k','w','h']) for a in anchors),anchors)
  transitions=[];movies={}
  for diff in ['easy','normal','hard','furious']:
   for form,theme in [(1,'jungle'),(2,'lava'),(6,'sky'),(8,'space')]:
    p.evaluate('d=>setup20(0,d)',diff);p.evaluate('f=>{j3State(B).attacks=D20.book.length;j3Morph(B,f)}',form)
    frames=[];states=[]
    # Natural form timers, not manually assigned transition modes.
    for tick in range(0,193,3):
     if tick:p.evaluate('tick20',3)
     if diff=='normal' or tick in [30,120,192]:
      p.evaluate('paint20');states.append(p.evaluate('({mode:B._r30.mode,arena:AD20.last,parts:B.parts.map(p=>p.id),hp:B.hp,protected:B.enter||B._noHit})'))
      if diff=='normal':frames.append(shot(p,'transition-'+theme+'-'+str(tick)))
    end=p.evaluate('({mode:B._r30.mode,theme:AD20.last?.theme,form:B._r30.v18.form,hp:B.hp,lives:run.lives})')
    ok=end['mode']=='fight' and end['form']==form and end['theme']==theme and any(s['arena'] and s['arena']['mode']=='erase' for s in states) and any(s['arena'] and s['arena']['mode']=='build' for s in states)
    transitions.append(dict(diff=diff,form=form,theme=theme,passed=ok,end=end,states=states))
    if diff=='normal':
     frames[0].save(Q/('download-'+theme+'.gif'),save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=True);movies[theme]=len(frames)
  ck('All4 arenas download through native erase/build/fight transitions on all4 difficulties',all(t['passed'] for t in transitions),[{'diff':t['diff'],'form':t['form'],'end':t['end']} for t in transitions if not t['passed']])
  p.evaluate('()=>{setup20(2);const p=ph21Part(B,"cannonL");p.destroyed=true;p.hp=0;j3Save(B);j3Morph(B,"home");}');p.evaluate('tick20',192);p.evaluate('paint20')
  ck('Returning to main Dracodia restores the native void arena',p.evaluate('B._r30.v18.form===0&&B._r30.mode==="fight"&&!B._r30.v18.arenaDownload'))
  p.evaluate('()=>{j3State(B).attacks=D20.book.length;j3Morph(B,2)}');p.evaluate('tick20',192);p.evaluate('paint20')
  ck('Arena downloads cannot revive a destroyed Phoenix cannon',p.evaluate('B._r30.v18.form===2&&ph21Part(B,"cannonL").destroyed&&ph21Part(B,"cannonL").hp===0'))
  # Deliberate hit on an intact actor: scene renderer must not suppress its flash path.
  p.evaluate('()=>{setup20(1);B.flash=0;paint20();}');before=shot(p,'hit-before')
  p.evaluate('()=>{markHit(B,.2);paint20();}');after=shot(p,'hit-after')
  ck('Native boss hit flash remains visibly different above downloaded terrain',before.tobytes()!=after.tobytes())
  p.evaluate('()=>{setup20(1);setState(GS.PLAY);Input.injectTap("p")}');p.evaluate(tut.STEPN,65)
  paused=p.evaluate('({state,clock:B._r30.clock})');p.evaluate(tut.STEPN,90);again=p.evaluate('({state,clock:B._r30.clock})')
  ck('Pausing freezes arena, cloud and download animation clocks',paused==again and again['state']=='paused',[paused,again])
  # Audio is already assigned to the native transformation; our erase uses its mixer charge cue.
  ck('Download charge and native materialization cues have decoded mixer voices',p.evaluate('["bossWeaponCharge","teleportIn","bossPhase"].every(k=>Snd.pools[k]?.slots.some(s=>s?.attached&&s.el.readyState>=3))'))
  p.evaluate('()=>{setState(GS.PLAY);setup20(1);Snd.audioOn=true;Audio.SFX.bossWeaponCharge();Audio.SFX.teleportIn();}')
  ck('No browser page, console, drawing or failed asset errors',not errors,errors)
  b.close()
finally:stop()
report={'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'checks':checks,'transitions':transitions,'movie_frames':movies,'curtain_frames':json.loads((R/'assets/game/levels/stage_08/boss/arena_download_1020/manifest.json').read_text(encoding='utf-8'))['curtain']['frames']}
(Q/'native-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:report[k] for k in ['passed','total','errors','curtain_frames']}));raise SystemExit(not all(c['passed'] for c in checks))
