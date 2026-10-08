"""Native top-HUD state, pixel, ownership and encounter integration verification."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,traceback,sys
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/player_hud_1008';O.mkdir(exist_ok=True)
errors=[];checks=[];shots=[];start=time.time()
def check(ok,name,data=None):
 checks.append({'pass':bool(ok),'name':name,'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=browser.new_page(viewport={'width':1200,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000)
  p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  def ready():
   for _ in range(1200):
    q=p.evaluate('()=>{stageLoadTick();drawWorld(0);return stageLoadInfo(run.stage);}')
    if q['ready']:return q
    p.wait_for_timeout(30)
   raise RuntimeError('Assets failed readiness: '+str(q))
  def draw():p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);hudctx.setTransform(1,0,0,1,0,0);drawHUDStrip(hudctx);}')
  def shot(name):draw();p.locator('#game-frame').screenshot(path=str(O/(name+'.png')));shots.append(name+'.png')
  for n in ([4] if '--quick' in sys.argv else range(1,10)):
   kind=p.evaluate('(n)=>debugFightFor(n,"boss").kind',n)
   p.evaluate('(c)=>BAL7.setup(c)',{'stage':n,'kind':kind,'pilot':'yuri','diff':'furious','seconds':10,**({'form':'host'} if n==8 else {})});ready()
   p.evaluate('()=>{run.score=123456;run.lives=7;run.bombs=12;run.speedLevel=3;run.shield=4;player._rollCool=BR_COOL*.65;player._somerCool=SS_COOL*.25;special={pilot:"yuri",t:9,dur:15};player.invuln=9999;}')
   if n in (1,7):
    p.evaluate('()=>{for(let i=0;i<1500&&(boss._ovIntro&&!boss._ovIntro.done||!bossHealthVisible(boss));i++)updateBoss(1/60);}')
    ready()
   if n==9:
    p.evaluate('()=>{for(let i=0;i<120;i++)updateBoss(1/60);const F=B._s9fusion;for(const q of [F.left,F.right]){F.hit=q;s9FusionHit(B,q.hp+1);}for(let i=0;i<160;i++)updateBoss(1/60);}')
    ready()
   if n==6:
    p.evaluate('()=>{B.y=B._whv.cy=190;B.x=B._whv.cx=worldWidth()/2;}')
   p.evaluate('()=>{player._rollCool=BR_COOL*.65;player._somerCool=SS_COOL*.25;special={pilot:"yuri",t:9,dur:15};}')
   draw();shot(f'stage_{n:02d}_boss')
   q=p.evaluate('()=>({visible:bossHealthVisible(B),bar:EH7.lastBoss,frac:bossHealthFraction(B)})')
   check(q['visible'] and q['bar'] and q['bar']['theme']==f'stage_{n:02d}' and abs(q['bar']['frac']-q['frac'])<1e-8,f'Stage {n}: complete live boss lane with actual encounter HP',q)
   q=p.evaluate('()=>({hud:PH8.last[0],theme:ph8Theme(),height:hudcv.height,rows:PH8.rows,ready:XART.rdy(PH8_ART[ph8Theme()].key),old:Object.keys(XART.img).filter(k=>k.startsWith("ph8_stage_")&&!ph8Keys(run.stage).includes(k))})')
   check(q['ready'] and q['theme']==f'stage_{n:02d}' and q['height']==80 and q['rows']==1,f'Stage {n}: authored top row, reserved geometry',q)
   v=q['hud'];check(v['lives']==7 and v['missiles']==12 and v['speed']==3 and v['shield']==4 and abs(v['roll']-.35)<1e-6 and abs(v['resource']-.6)<1e-6,f'Stage {n}: actual stocks/equipment/cooldowns/special',v)
   check(not q['old'],f'Stage {n}: preceding HUD roots retired',q['old'])
   # Fraction sampling is through the actual hud context and authored source strip.
   pixels=p.evaluate('''()=>{const f=ph8Frame(ph8Theme()),out=[];for(const well of ['roll','somer','special'])for(const frac of [0,.25,.5,1]){
    hudctx.clearRect(0,0,VW,80);hudctx.drawImage(f.canvas,0,0);ph8Fill(hudctx,f,well,frac,well==='special'?'red':'green');const r=f.rect[well];
    const at=t=>Array.from(hudctx.getImageData(Math.round(r[0]+r[2]*t),Math.floor(r[1]+r[3]*.5),1,1).data);
    let stale=0;if(frac===0)for(let y=Math.ceil(r[1]);y<r[1]+r[3]-1;y++){const c=hudctx.getImageData(Math.round(r[0]+r[2]*.3),y,1,1).data;if(Math.max(...c.slice(0,3))>110&&Math.max(...c.slice(0,3))-Math.min(...c.slice(0,3))>55)stale++;}
    out.push({well,frac,left:at(.12),right:at(.87),stale});
   }return out;}''')
   for z in pixels:
    lit=lambda a:max(a[:3])>110 and max(a[:3])-min(a[:3])>55
    check(lit(z['left'])==(z['frac']>.12) and lit(z['right'])==(z['frac']>.87) and z['stale']==0,f'Stage {n}: {z["well"]} continuous live pixels at {z["frac"]}',z)
   mini=p.evaluate('(n)=>SUBBOSS[n]?.kind',n)
   if mini:
    p.evaluate('(c)=>BAL7.setup(c)',{'stage':n,'kind':mini,'mini':True,'pilot':'yuri','diff':'normal','seconds':10});ready()
    p.evaluate('()=>{B.enter=false;B.hp=B.maxhp*.4;player.invuln=9999;if(B._s9rift){for(let i=0;i<110;i++)s9VoidHorizonTick(B,1/60);B._s9rift.core.hp=B._s9rift.core.maxhp*.4;}}');ready();shot(f'stage_{n:02d}_mini')
    q=p.evaluate('()=>EH7.lastBoss');check(q and q['variant'].startswith('mini') and q['y']>=0 and q['y']<5,f'Stage {n}: miniboss complete and directly below player row',q)
  if '--quick' not in sys.argv:
   # Stage X must use its own player theme while respecting the existing
   # custom Harrier housing and all five independent Rebel HP values.
   for kind,route in [('warhive','left'),('rebelsquad','right')]:
    p.evaluate('(c)=>BAL7.setup(c)',{'stage':6,'kind':kind,'pilot':'cole','diff':'furious','seconds':10});ready()
    p.evaluate('(route)=>{run._gp4StageX=route;player.invuln=9999;if(B._whv){B.y=B._whv.cy=190;B.x=B._whv.cx=worldWidth()/2;}}',route);draw();shot('stage_x_'+kind)
    check(p.evaluate('ph8Theme()')=='stage_x','Stage X player theme '+kind)
    if kind=='rebelsquad':
     check(p.evaluate('EH7.lastRebels.length')==5,'Five Rebel bars retained with new player HUD')
     p.evaluate('()=>{B._rebels.ships[1].frCloak=2;B._rebels.ships[4].dead=true;}');draw();check(p.evaluate('EH7.lastRebels.map(q=>q.pilot)')==['voss','rook','kaia'],'Rebel cloak/death bar suppression retained')
   # All pilot native names/icons, including earned Cole tiers and space weapons.
   p.evaluate('(c)=>BAL7.setup(c)',{'stage':6,'kind':'warhive','pilot':'yuri','diff':'normal','seconds':10});ready()
   for pilot in ['yuri','falva','cole','maverick','axel','juggernaut','lizzie','decker','freezer']:
    p.evaluate('(k)=>{run.pilot=k;pilotIndex=PILOTS.findIndex(q=>q.key===k);special={pilot:k,t:8,dur:15,strikes:3,charge:FALVA_FULL*.5};player._chgT=CHG_FULL*.4;}',pilot);draw();shot('pilot_'+pilot)
    q=p.evaluate('()=>PH8.last[0]');check(q['pilot']==pilot and abs(q['resource']-8/15)<1e-6,'Pilot owns named live special '+pilot,q)
   p.evaluate('()=>{run.pilot="yuri";pilotIndex=0;run.wvars=[];run.forge={};}')
   for weapon in range(9):
    p.evaluate('(w)=>{run.weapon=w;run.wlevel=3;}',weapon);draw();shot('weapon_'+str(weapon))
    q=p.evaluate('()=>{const w=ph8Weapon();return{key:w.key,drawn:iconBlit(hudctx,w.key,30,30,24,true),cell:BOFX.icons[w.key]};}')
    check(q['drawn'] and q['drawn']>0,'Native weapon icon actually blits '+str(weapon),q)
   p.evaluate('()=>{run.pilot="cole";pilotIndex=PILOTS.findIndex(p=>p.key==="cole");run.weapon=0;run.wlevel=8;run._cfUnlocked=8;}');draw();shot('cole_fusion_equipped');check(p.evaluate('PH8.last[0].weapon.label')=='FUSION','Cole VIII displays Fusion equipment')
   p.evaluate('()=>{run.wlevel=7;}');draw();check(p.evaluate('PH8.last[0].weapon.label')=='BLACK/HOMING','Cole VII equipment updates')
   p.evaluate('()=>{run.wlevel=6;}');draw();check(p.evaluate('PH8.last[0].weapon.label')=='YELLOW LASER','Cole VI equipment updates')
   p.evaluate('()=>{enemyLockOn(B,.8,{fire:()=>{}});}');draw();shot('incoming_lock');check(p.evaluate('PH8.last[0].lock'),'Existing enemy lock state reaches top warning capsule')
   p.evaluate('()=>{playerLocks=[];}');draw();check(p.evaluate('!PH8.last[0].lock'),'Released enemy lock clears top warning capsule')
   p.evaluate('()=>{run.pilot="lizzie";pilotIndex=PILOTS.findIndex(p=>p.key==="lizzie");special=null;lzMountGrant();lzMountTick(LZM_DOCK_T);lzMount.life=LZ_LIFE*.4;}');draw();shot('borrowed_heavy_mg')
   check(p.evaluate('PH8.last[0].rollAvailable===false&&Math.abs(PH8.last[0].resource-.4)<1e-8&&PH8.last[0].loans.length===1'),'Borrowed Heavy MG displays remaining resource and locks roll')
   p.evaluate('()=>{run.pilot="yuri";pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");}');draw();check(p.evaluate('PH8.last[0].loans.length===0&&PH8.last[0].resource===0'),'Other pilot does not inherit Lizzie mount readout')
   p.evaluate('()=>{lzMount=null;run.pilot="cole";}')
   p.evaluate('()=>{special=null;run.lives=0;run.bombs=0;run.speedLevel=0;run.shield=0;player.dead=true;}');draw();shot('empty_dead');check(p.evaluate('PH8.last[0].resource===0&&PH8.last[0].missiles===0&&PH8.last[0].detail==="NO SPECIAL"'),'Empty/dead values are not concept sample values')
   # Use the real co-op creation path, not fake DOM canvases or copied renderer logic.
   p.evaluate('(c)=>BAL7.setup(c)',{'stage':6,'kind':'warhive','pilot':'cole','diff':'normal','seconds':10,'coop':True});ready()
   p.evaluate('()=>{run2.pilot="maverick";p2Index=PILOTS.findIndex(p=>p.key===run2.pilot);PILOTMOD2={...PILOTS[p2Index]};run2.lives=2;run2.bombs=4;run2.weapon=1;run2.wlevel=3;run.lives=6;run.bombs=11;player2._rollCool=BR_COOL*.8;player._rollCool=0;}');draw();shot('coop')
   q=p.evaluate('()=>({rows:PH8.last,h:hudcv.height,geometry:window.__bofHudHeight,seat:_seat,main:run.pilot})');check(len(q['rows'])==2 and q['h']==160 and q['geometry']==160,'Co-op reserves two complete independent rows',q)
   check(q['rows'][0]['lives']==6 and q['rows'][1]['lives']==2 and q['rows'][0]['missiles']==11 and q['rows'][1]['missiles']==4 and q['seat']==1,'Co-op reads both stocks and restores original seat',q)
   p.evaluate('()=>{coopOn=false;}');draw();check(p.evaluate('hudcv.height===80&&window.__bofHudHeight===80'),'Solo row size restored on co-op exit')
   # Narrow and fullscreen geometry: only genuine resize/seat-count changes
   # may resize the shell; async ready and drains cannot move it.
   for width,height in [(480,760),(390,844),(1600,1000)]:
    p.set_viewport_size({'width':width,'height':height});p.evaluate('()=>window.__bofFit()');draw();shot('viewport_'+str(width))
    q=p.evaluate('()=>{const a=document.getElementById("game-frame").getBoundingClientRect(),b=document.getElementById("hud").getBoundingClientRect();return{left:a.left,right:a.right,w:innerWidth,hud:b.height,ratio:b.width/b.height};}')
    check(q['left']>=-1 and q['right']<=width+1 and abs(q['ratio']-6)<.15,'Complete fixed native HUD at viewport '+str(width),q)
   p.set_viewport_size({'width':1600,'height':1000});p.evaluate('()=>{document.body.classList.add("fs","wide-playing");window.__bofFit();}');draw();shot('fullscreen')
   check(p.evaluate('getComputedStyle(document.getElementById("hud-row")).display')!='none','Fullscreen keeps top HUD')
   before=p.evaluate('JSON.stringify(ph8Values())');p.evaluate('()=>{for(let i=0;i<100;i++)drawHUDStrip(hudctx);}');check(p.evaluate('JSON.stringify(ph8Values())')==before,'Repeated render calls do not advance clocks or mutate combat')
   timings=p.evaluate('()=>{const n=PH8.cache.size,start=performance.now();for(let i=0;i<300;i++)drawHUDStrip(hudctx);return{msPerDraw:(performance.now()-start)/300,before:n,after:PH8.cache.size};}')
   check(timings['before']==timings['after'],'Stable HUD rendering reuses cached frame',timings)
   p.evaluate('()=>{document.body.classList.remove("fs","wide-playing");window.__bofFit();}')
   # Actual three outer fights and all persistent copied pools. Rendering must
   # neither refill a pool nor replace the coronation's eight colored fills.
   final_kind=p.evaluate('debugFightFor(8,"boss").kind')
   for form in ['host','ghost','home',1,2,3,4,5,6,7,8]:
    p.evaluate('(c)=>BAL7.setup(c)',{'stage':8,'kind':final_kind,'pilot':'cole','diff':'furious','form':form,'seconds':10});ready()
    p.evaluate('()=>{B._r30.mode="fight";B.hp=B.maxhp*.375;player.invuln=9999;}');draw();shot('finale_'+str(form))
    q=p.evaluate('()=>({bar:EH7.lastBoss,hp:B.hp,max:B.maxhp,gauge:fmcGauge(B),pools:j3State(B).hp.slice()})')
    p.evaluate('()=>{for(let i=0;i<20;i++){drawHUDOverlay();drawHUDStrip(hudctx);}}')
    check(q['bar'] and abs(q['bar']['frac']-.375)<1e-8 and p.evaluate('()=>({hp:B.hp,max:B.maxhp,pools:j3State(B).hp.slice()})')=={k:q[k] for k in ['hp','max','pools']},'Finale '+str(form)+': live pool and unchanged HP across rendering',q)
   colors=p.evaluate('''()=>{B._r30.mode='coronation1003j';const out=[];for(let i=0;i<8;i++){B._r30.t=.3+i*.5+.2;drawHUDOverlay();const a=EH7.lastBoss,f=eh7Frame(a.theme,a.variant,a.w),r=f.hp;
    out.push({gauge:fmcGauge(B),pixel:Array.from(ctx.getImageData(Math.floor((a.x+r[0]+r[2]*.2)*SS),Math.floor((a.y+r[1]+r[3]*.5)*SS),1,1).data)});}return out;}''')
   check(len({tuple(q['pixel'][:3]) for q in colors})==8 and all(q['gauge']['charge']==i for i,q in enumerate(colors)),'Coronation preserves eight successive visibly different fills',colors)
   shot('finale_coronation')
  check(not errors,'No page/console errors',errors);browser.close()
except Exception:
 errors.append(traceback.format_exc());print(errors[-1],flush=True)
finally:
 stop();result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'errors':errors,'checks':checks,'shots':shots,'elapsed':round(time.time()-start,1)}
 (O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','shots']}),flush=True)
 options=''.join('<option value="'+name+'"'+(' selected' if name=='stage_04_boss.png' else '')+'>'+name.removesuffix('.png').replace('_',' ').upper()+'</option>' for name in shots)
 (O/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bullets of Fury — Live HUD</title>
 <style>body{margin:0;background:#090d16;color:#e5eefc;font:16px system-ui}header{max-width:900px;margin:auto;padding:20px}h1{font-size:22px}select,a{font:inherit;padding:8px;color:#ecf4ff;background:#182436;border:1px solid #415570;border-radius:5px}a{display:inline-block;text-decoration:none;margin:8px}main{text-align:center}img{max-width:100%;width:756px;height:auto;image-rendering:auto}p{line-height:1.5}</style>
 <header><h1>Live HUD and encounter bars</h1><p>Stage themes, native weapons, pilot specials, co-op and final boss forms. Captures show the live game renderer.</p><select id="shots">'''+options+'''</select><a href="../../index.html?build=hud-1008">Open game</a></header><main><img id="capture" src="stage_04_boss.png" alt="Stage 4 live HUD"></main><script>shots.onchange=()=>{capture.src=shots.value;capture.alt=shots.selectedOptions[0].textContent;};</script></html>''',encoding='utf-8')
 if result['failed'] or errors:sys.exit(1)
