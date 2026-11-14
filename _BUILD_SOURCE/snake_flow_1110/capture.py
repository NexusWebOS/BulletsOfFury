from pathlib import Path
import sys,json,base64,io
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-flow';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];checks={};frames=[];rows=[]
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
def gif(frames,path,ms):
 contact=Image.new('RGB',(1920,2048))
 for i in range(16):contact.paste(frames[round(i*(len(frames)-1)/15)],(i%4*480,i//4*512))
 pal=contact.quantize(colors=192,method=Image.Quantize.MEDIANCUT);out=[f.quantize(palette=pal,dither=Image.Dither.NONE)for f in frames];out[0].save(path,save_all=True,append_images=out[1:],duration=ms,loop=0,optimize=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("()=>{EA11.setup(7,'furious');stagePlan=[];waveIdx=0;enemies=[];powerups=[];CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=false;player.invuln=99999;for(const k in Input.keys)Input.keys[k]=false;spawnSubBoss('dualscoopdredger');window.B=subBoss;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&sj98Ready()}')
  p.evaluate('''()=>{window.P={last:new Map(),still:new Map(),air:new Map(),headHold:0,bodyHold:0,airHold:0,maxJump:0,maxStep:0,lands:[0,0],groundedRow:[0,0],modes:new Set(),samples:0};window.origMotion122=sj120Motion;sj120Motion=function(b,a,dt){const oldH=a.height,oldX=a.x,oldY=a.y;origMotion122(b,a,dt);const q=P;q.modes.add(b._sj120.mode);if(oldH>0&&a.height===0)q.lands[a.i]++;if(['row-charge','row-fire'].includes(a.phase)&&a.segments.every(s=>s.h<.5))q.groundedRow[a.i]++;if(!sj98Foreground(a))return;q.samples++;q.maxStep=Math.max(q.maxStep,Math.hypot(a.x-oldX,a.y-oldY));const points=[{x:a.x,y:a.y,h:a.height},...a.segments.map(s=>({x:s.x,y:s.y-s.h,h:s.h}))];for(let i=0;i<points.length;i++){const r=points[i],id=a.i+':'+i,last=q.last.get(id);if(last&&r.x>camLeftX()&&r.x<camRightX()&&r.y>80&&r.y<VH){const d=Math.hypot(r.x-last.x,r.y-last.y);const still=d<.04?(q.still.get(id)||0)+dt:0,air=r.h>5&&d<.04?(q.air.get(id)||0)+dt:0;q.still.set(id,still);q.air.set(id,air);if(i===0)q.headHold=Math.max(q.headHold,still);else q.bodyHold=Math.max(q.bodyHold,still);q.airHold=Math.max(q.airHold,air);}q.last.set(id,r);}};}''')
  for i in range(420):
   err=p.evaluate(STEP,4);assert err is None,err
   r=p.evaluate('({t:B.t,mode:B._sj120.mode,actors:B._sj98.actors.map(a=>({x:a.x,y:a.y,h:a.height,tail:a.segments?.at(-1).h,lands:a.lands})),hp:B.hp})');rows.append(r)
   if i<360:frames.append(shot(p))
   if i in [60,160,230,300]:shot(p).save(O/f'pair-{i}.png')
  proof=p.evaluate('({headHold:P.headHold,bodyHold:P.bodyHold,airHold:P.airHold,lands:P.lands,groundedRow:P.groundedRow,modes:[...P.modes],maxStep:P.maxStep,samples:P.samples})');print(json.dumps({'pair':proof}),flush=True)
  checks['heads_keep_moving']=proof['headHold']<.12;checks['all_visible_body_sections_keep_slithering']=proof['bodyHold']<.2;checks['no_visible_section_hangs_in_air']=proof['airHold']<.12;checks['each_snake_repeatedly_lands']=min(proof['lands'])>=8;checks['the_entire_body_lands_during_row_jumps']=min(proof['groundedRow'])>0;checks['all_native_movement_phases']={'hop-warn','hop','row-form','row-charge','row-fire','split','north','cross','return'}<=set(proof['modes']);checks['fixed_twenty_section_body']=p.evaluate('B._sj98.actors.every(a=>a.segments.length===20)');checks['both_health_halves_preserved']=p.evaluate('SR110.hud.snake.values.length===2&&B.maxhp===14000&&B.hp===14000');checks['native_southward_orbs']=p.evaluate('SJ120.events.filter(e=>e.event==="large-orb").length>30&&SJ120.events.filter(e=>e.event==="large-orb").every(e=>e.angle===Math.PI/2)')
  expr='({clock:B.t,t:B._sj120.t,actors:B._sj98.actors.map(a=>[a.x,a.y,a.height,a.segments])})';frozen=p.evaluate(expr);p.evaluate("setState('paused')");p.evaluate(STEP,60);checks['pause_freezes_all_motion']=frozen==p.evaluate(expr);p.evaluate('setState(GS.PLAY)')
  p.evaluate('()=>{const a=B._sj98.actors[0];for(const q of a.pools)for(let i=0;i<8&&q.hp>0;i++)sj98Damage(B,q.hp+50,null,null,{a,p:q});P.headHold=P.bodyHold=P.airHold=0;P.last.clear();P.still.clear();P.air.clear();P.lands=[0,0];P.groundedRow=[0,0];}')
  soloFrames=[]
  for i in range(330):
   err=p.evaluate(STEP,4);assert err is None,err
   if i<180:soloFrames.append(shot(p))
  solo=p.evaluate('({headHold:P.headHold,bodyHold:P.bodyHold,airHold:P.airHold,lands:P.lands[1],groundedRow:P.groundedRow[1],alive:B._sj98.actors.filter(a=>!a.dead).length,hp:B.hp})');checks['solo_snake_keeps_slithering_and_jumping']=solo['alive']==1 and solo['headHold']<.12 and solo['bodyHold']<.2 and solo['airHold']<.12 and solo['lands']>=6;checks['independent_half_health']=p.evaluate('SR110.hud.snake.values[0]===0&&SR110.hud.snake.values[1]===1');checks['dead_snake_cannot_fire']=p.evaluate('!eBullets.some(q=>q._sj120&&!q.dead&&q._sj98Actor.dead)');checks['no_unsafe_round_growth']=p.evaluate('eBullets.filter(q=>q._sj120&&!q.dead).length<=44')
  p.evaluate('()=>{const a=B._sj98.actors[1];for(const q of a.pools)for(let i=0;i<8&&q.hp>0;i++)sj98Damage(B,q.hp+50,null,null,{a,p:q});}');p.evaluate(STEP,180);checks['once_only_native_pair_defeat']=p.evaluate('B._sj98.rewarded&&subBoss===null&&subBossDone&&SJ98.events.filter(e=>e.event==="pair-defeat").length===1');br.close()
 gif(frames,O/'pair-slithering-and-jumps.gif',67);gif(soloFrames,O/'solo-slithering-and-jumps.gif',67)
finally:stop()
checks['no_page_or_console_errors']=not errors;report={'checks':checks,'pair':proof,'solo':solo,'errors':errors,'rows':rows};(O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({'checks':checks,'pair':proof,'solo':solo,'errors':errors}));assert all(checks.values()),checks
