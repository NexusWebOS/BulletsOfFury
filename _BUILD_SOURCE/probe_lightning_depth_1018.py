"""Actual Chromium pixels: all generated poses, occlusion, mounts and native hits."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot

R=Path(__file__).resolve().parents[1];O=R/'_shots/lightning_depth_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128

def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)

port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof L21!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.ltNativeHit=playerHit;window.ltHits=[];window.ltTrack=reason=>ltHits.push(reason);playerHit=ltTrack;
   window.ltPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return a;};
   window.ltDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>18)n++;return n;};
   window.ltHash=a=>{let h=2166136261,n=0;for(let i=0;i<a.length;i+=4){h=Math.imul(h^a[i],16777619);h=Math.imul(h^a[i+1],16777619);h=Math.imul(h^a[i+2],16777619);if(Math.max(a[i],a[i+1],a[i+2])>22)n++;}return{hash:h>>>0,pixels:n};};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(stage=8,diff='normal'):
   p.evaluate(SETUP,dict(stage=stage,diff=diff,kind='vileexistence' if stage==8 else 'stormsovereign',pilot='cole'))
   p.wait_for_function('(stage)=>{stageLoadTick();return stageLoadReady(stage)&&l21Warm()&&bmfReady("game")&&(stage!==8||v18Warm()&&d20Warm())}',arg=stage)
   p.evaluate('''stage=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];groundTargetingReset();tb28Reset();polishLanes=[];
    VP12.next=CP12.next=EP13.next=HM17.next=TARGET17.nextTank=99999;playerHit=ltTrack;ltHits=[];run.shield=0;run.spaceMode=false;player.dead=player.out=false;player.invuln=0;player.x=worldWidth()/2;player.y=VH-70;for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;
    if(stage===8){D20.sparks=[];D20.blasts=[];D20.events=[];v18Budget(B);v18Enter(B,2,0);B._r30.v18.arenaPhase=2;v18Fight(B);B._r30.cd=999;bossWarned=true;}
    else{B._be=null;B._noHit=false;B._phaseInvuln=0;B.enter=false;B.x=worldWidth()/2;B.y=B._drawY=180;B._er26.engaged=false;er26Tick(B,0);}
    SC12.refresh();__bofFit();}''',stage)
  setup()
  for name in p.evaluate('Object.keys(L21_ART.banks)'):
   fmt=p.evaluate('''name=>{const b=L21_ART.banks[name];return{n:b.frames.length,w:b.w,h:b.h,pivot:b.pivot,valid:b.frames.every(a=>a.w===b.w&&a.h===b.h&&a.w%2===0&&a.h%2===0&&a.pivot[0]===b.pivot[0]&&a.pivot[1]===b.pivot[1])};}''',name)
   check(name+' keeps even fixed canvases and a shared pivot',fmt['valid'] and 16<=fmt['n']<=32,fmt)
   poses=[]
   for i in range(fmt['n']):
    poses.append(p.evaluate('''([name,i])=>{const b=L21_ART.banks[name];return ltHash(ltPixels(()=>l21Draw(name,i/b.fps+.00001,worldWidth()/2,256,b.h)));}''',[name,i]))
    if i%8==0:p.wait_for_timeout(5)
   check(name+' renders every actual XART pose through the native game context',all(q['pixels']>12 for q in poses),poses)
   check(name+' genuinely changes pixels across its generated animation',len({q['hash'] for q in poses})>=fmt['n']-2,poses)
  # Native black-composited source and native two-layer reassembly must agree.
  p.evaluate('''async()=>{window.ltRefs=await Promise.all(Array.from({length:32},(_,i)=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='_shots/lightning_depth_1018/art/wrap-reference-'+String(i).padStart(2,'0')+'.png';})));}''')
  recomposed=[]
  for i in range(32):
   recomposed.append(p.evaluate('''i=>{const x=worldWidth()/2,y=256,expected=ltPixels(()=>ctx.drawImage(ltRefs[i],x-160,y-160)),actual=ltPixels(()=>{l21Draw('wrap_back',i/16+.00001,x,y,320);l21Draw('wrap_front',i/16+.00001,x,y,320);});return ltDiff(expected,actual);}''',i))
   if i%8==0:p.wait_for_timeout(5)
  check('all32 front/back plates recompose the actual full generated poses exactly',max(recomposed)==0,recomposed)
  # Prove both occlusion directions with real damaged/undamaged authored body pixels.
  p.evaluate('''()=>{d20Start(B,'spiralLightning');window.ltComposite=mode=>{const P=B._r30.v18.attack,size=v18Size(B)*1.15*L21_ART.banks.wrap_front.renderScale,t=P.t,alpha=(.18+.82*clamp(t/P.tell,0,1))*clamp((P.tell+P.active-t)/.22,0,1);
   if(mode==='actual')return ltPixels(()=>d20MainBody(B));return ltPixels(()=>{if(mode==='all-front')L21.base.body(B);l21Wrap('wrap_back',t,B,size,0,alpha*.56);l21Wrap('wrap_front',t,B,size,0,alpha);if(mode==='all-back')L21.base.body(B);});};}''')
  depth=[]
  for i in range(32):
   depth.append(p.evaluate('''i=>{B._r30.v18.attack.t=2+i/16+.00001;const a=ltComposite('actual');return{frame:i,behind:ltDiff(a,ltComposite('all-front')),over:ltDiff(a,ltComposite('all-back'))};}''',i))
   if i%8==0:p.wait_for_timeout(5)
  rows.append(dict(depth=depth))
  check('electricity is visibly hidden by the actual boss body in multiple poses',sum(q['behind']>20 for q in depth)>=8,depth)
  check('electricity also crosses visibly over the actual boss body',sum(q['over']>20 for q in depth)>=8,depth)
  check('near and far animation plates share the exact body pivot and phase',p.evaluate('L21.last.wrap_back.frame===L21.last.wrap_front.frame&&L21.last.wrap_back.x===B.x&&L21.last.wrap_back.y===B.y&&L21.last.wrap_front.x===B.x&&L21.last.wrap_front.y===B.y'))
  p.evaluate('B._r30.v18.attack.t=2.8');snap('dracodia-over-under')
  flash=p.evaluate('''()=>{const a=ltPixels(()=>r30DrawBoss(B)),hp=B.hp;B._lastPart=B.parts[0];hitBoss(1);return{damage:hp-B.hp,owner:B.flash,part:B.parts[0].flash,pixels:ltDiff(a,ltPixels(()=>r30DrawBoss(B)))};}''')
  check('wrapped main form retains actual damaged pixels and native hit flashes',flash['damage']>0 and flash['owner']>0 and flash['part']>0 and flash['pixels']>50,flash)
  frames(18);check('main hit flash expires under the new lightning',p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
  for diff in ['normal','hard','furious']:
   setup(8,diff);p.evaluate('window.ltOldCrescents=Object.entries(D20.draws).filter(([k])=>k.startsWith("d20_lightning_loop_")).reduce((s,[,v])=>s+v,0);d20Start(B,"spiralLightning")')
   frames(40);check(diff+' actual lightning storm still warns before its projectile release',p.evaluate('D20.sparks.length===0&&!ltHits.includes("spiraling code lightning")'))
   frames(128);snap(diff+'-dracodia-storm')
   check(diff+' live combat uses the animated wrap and forked bolt banks',p.evaluate('D20.sparks.length>=8&&L21.draws.wrap_front>0&&L21.draws.wrap_back>0&&L21.draws.bolt>0&&Object.entries(D20.draws).filter(([k])=>k.startsWith("d20_lightning_loop_")).reduce((s,[,v])=>s+v,0)===ltOldCrescents'))
   p.evaluate('''()=>{const q=D20.sparks[0],t=q.t+1/60,r=28+t*q.speed,a=q.angle+t*q.spin;player.x=q.origin.x+Math.cos(a)*r;player.y=q.origin.y+Math.sin(a)*r;run.shield=0;player.invuln=0;window.ltDeaths=stageStats.deaths;playerHit=ltNativeHit;}''');frames(1)
   check(diff+' new visible lightning still uses native player damage',p.evaluate('stageStats.deaths>ltDeaths'))
   p.evaluate('v18Clear(B);window.ltAfter=L21.draws.dracodia;drawWorld(0)')
   check(diff+' phase cleanup leaves no lightning ghost or hostile projectiles',p.evaluate('D20.sparks.length===0&&L21.draws.dracodia===ltAfter'))
  setup(4)
  p.evaluate('''()=>{window.ltLinks=[];const native=l21Link;l21Link=function(g,x,y,a,len){if(L21.links===B)ltLinks.push({x,y,ex:x+Math.cos(a)*len,ey:y+Math.sin(a)*len});return native.apply(this,arguments);};}''');frames(50);snap('stage4-generators-links')
  link=p.evaluate('''()=>({links:ltLinks.slice(-4),nodes:B._s4war.shield.nodes.filter(n=>!n.dead).map(n=>({x:n.x,y:n.y})),boss:{x:B.x,y:B.y},pixels:L21.draws.links})''')
  check('all four live generator connections use native animated lightning',len(link['links'])==4 and link['pixels']>0,link)
  check('lightning connections terminate at the actual moving hull',all(abs(q['ex']-link['boss']['x'])<.01 and abs(q['ey']-link['boss']['y'])<.01 for q in link['links']),link)
  for diff in ['normal','hard','furious']:
   setup(4,diff)
   p.evaluate('''()=>{B._s4war.shield.active=B._s4war.shield.rearming=false;B._s4war.shield.nodes.forEach(n=>{n.dead=true;n.hp=0;});B._s4war.shieldThresholdIndex=2;B.hp=B.maxhp*.60;er26Set(B,'sa14-storm');}''')
   frames(40);snap(diff+'-stage4-charge')
   check(diff+' Stage4 charge is surrounded by the new near/far lightning',p.evaluate('L21.draws.storm>0&&L21.draws.charge>0&&L21.last.wrap_back.x===B.x&&L21.last.wrap_back.y===B.y&&L21.last.wrap_front.x===B.x&&L21.last.wrap_front.y===B.y'))
   frames(170);snap(diff+'-stage4-volley')
   check(diff+' real Stage4 volleys use the animated plasma-ball bank',p.evaluate('L21.draws.stormOrbs>0'))
   proof=p.evaluate('''()=>{const q=stage4WarfareShot(B,shipBossMount(B,'C'),Math.PI/2,2.5,'orb'),before=q.dead;ordnanceBreak1002(q);s3kOrdnanceRules(q);return{flag:q._sg17Lightning,shootable:q._shootable,proof:q._weaponProof,alive:!q.dead};}''')
   check(diff+' lightning balls remain immune to interception',proof.get('flag') and not proof['shootable'] and proof['proof'] and proof['alive'],proof)
  check('both real encounters keep their source timing and attack ownership',p.evaluate('typeof ST18!=="undefined"&&typeof D20!=="undefined"&&V18.forms.join(",")==="0,8,1,6,2"'))
  # Delivered Level4 selector must really enter and repeat the lightning attack.
  p.goto(f'http://127.0.0.1:{port}/docs/previews/storm_assault_1018/index.html?scene=charge&difficulty=furious')
  p.wait_for_function('()=>ready&&!busy&&document.querySelector("#status").textContent.includes("PixelLab")')
  f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  check('Level4 lightning review uses the real full playfield and isolated saves',f.evaluate('typeof L21!=="undefined"&&window.__stormReviewStorage&&window.l21ReviewCharge&&SC12.layout.field.h>600'))
  f.evaluate('window.ltReviewTimes=[]')
  for _ in range(70):
   f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);ltReviewTimes.push(boss._er26.t);}}');p.wait_for_timeout(5)
  data=f.evaluate('({loops:ltReviewTimes.slice(1).filter((t,i)=>t<ltReviewTimes[i]-.3).length,body:L21.draws.storm||0,balls:L21.draws.stormOrbs||0,mode:boss._er26.mode})')
  check('Level4 selected lightning scene repeats native charges and real volleys',data['loops']>=1 and data['body']>0 and data['balls']>0,data)
  p.screenshot(path=str(O/'review-stage4-lightning.png'))
  check('no page, console, draw or asset errors',not errors,errors[:30]);br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors)
(O/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:report[k] for k in ['passed','failed','errors']}));sys.exit(bool(report['failed']))
