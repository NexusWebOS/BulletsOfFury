"""Native articulated volcano attacks, ten damage owners, sockets and breaks."""
from pathlib import Path
from PIL import Image,ImageDraw
from io import BytesIO
import ast,base64,http.server,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_volcano_1019';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&vp23Warm();}',polling=80)
  p.evaluate('''()=>{window.VK={keys:new Set()};window.volcanoSetup=(diff,phase,attack)=>{B=boss;v18Clear(B);GP4.clock+=1;diffKey=diff;DIFF=DIFFS[diff];v18Budget(B);(j3State(B).gp4Donors??=[])[2]=null;v18Enter(B,2,2);v18Fight(B);window.P=gd4Create(B,2).p;window.F=P._fz;B._r30.v18.arenaPhase=2;B._r30.v18.nextClawAt=9999;B._r30.cd=999;B.enter=B._noHit=false;B.x=P.x=worldWidth()/2;B.y=P.y=viewTopY()+viewH()*.46;B._r30.v18.home={x:B.x,y:B.y};B._drawY=B.y;
    for(const q of B.parts)if(phase==='core'&&['left','right'].includes(vp23Group(q.id))||phase==='head'&&q.id!=='head'){q.hp=0;q.destroyed=true;}vp23Sync(B);furnaceEnter(P,phase);F.trans=0;F.attack=attack;F.at=0;F.idx=0;F.serial++;F.a=0;F.shotBeat=F.burstBeat=-1;F.startX=B.x;F.endX=worldWidth()*.70;B.hp=P.hp=Object.values(F.pools).reduce((s,h)=>s+h,0);
    H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;dr5State(B).radio=null;
    zoneCols=[];enemies=[];eBullets=[];pBullets=[];explosions=[];particles=[];floaters=[];smokeTrails=[];sprAnims=[];fadeOuts=[];pilotFx=[];powerups=[];player.dead=player.out=false;player._dr21Death=null;player._spin=null;player.invuln=999;player.roll=player.somer=null;player.x=worldWidth()/2;player.y=viewTopY()+viewH()-72;run.shield=0;shake=whiteBlast=0;Input.keys={};Input.mouse.down=false;window.VK={maxError:0,rays:0,shots:0,rotation:new Set(),keys:new Set(),warningBoxes:0};SC12.refresh();__bofFit();};
    const baseGet=XART.get,baseDraw=ctx.drawImage,tags=new WeakMap();XART.get=function(key){const im=baseGet.apply(this,arguments);if(im)tags.set(im,key);return im;};ctx.drawImage=function(im){const key=tags.get(im);if(key?.startsWith('vp23_')||key?.startsWith('vh19_'))VK?.keys.add(key);return baseDraw.apply(this,arguments);};
    const warning=combatWarningDraw;combatWarningDraw=function(owner,q){if(owner===B&&q?.alertOnly)VK.warningBoxes++;return warning.apply(this,arguments);};
    window.volcanoTick=n=>{for(let i=0;i<n;i++){const before=eBullets.length;GP4.clock+=1/60;r30Tick(B,1/60);for(const q of [...F.beams,...F.tells])if(q._vp23Emitter){const at=vp23Socket(P,q._vp23Emitter);if(at){VK.maxError=Math.max(VK.maxError,Math.hypot(q.x-at.x,q.y-at.y));VK.rays++;}}for(const q of eBullets.slice(before))if(q._vp23Emitter){const at=vp23Socket(P,q._vp23Emitter);if(at){VK.maxError=Math.max(VK.maxError,Math.hypot(q.x-at.x,q.y-at.y));VK.shots++;}}const v=v18Rig(B).find(v=>v.layer==='left');if(v)VK.rotation.add(v.rot.toFixed(3));}};
    window.volcanoPaintPart=id=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);for(const v of v18Rig(B))if(v.p.id===id)v19Paint(v,B);ctx.restore();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};
   }''')
  def setup(diff='normal',phase='arms',attack='cannon'):p.evaluate('([a,b,c])=>volcanoSetup(a,b,c)',[diff,phase,attack])
  def tick(n):p.evaluate('volcanoTick',n)
  def shot(name=None):
   p.evaluate('()=>{shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   raw=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
   if name:(O/(name+'.png')).write_bytes(raw)
   im=Image.open(BytesIO(raw)).convert('RGB');im.thumbnail((840,1000));return im
  setup();row=p.evaluate('({parts:B.parts.length,max:B.maxhp,sum:B.parts.reduce((s,q)=>s+q.maxhp,0),hp:B.hp,remaining:B.parts.reduce((s,q)=>s+q.hp,0)})');ck('Ten independently damageable modules preserve original total HP',row['parts']==10 and row['max']==row['sum'] and row['hp']==row['remaining'],row)
  film=[];gallery=[]
  for diff in ['easy','normal','hard','furious']:
   for phase,attack in [('arms','cannon'),('arms','sweep'),('arms','spin900'),('core','ring'),('core','coreLaser'),('core','rotor'),('core','rollerball'),('head','eyeSweep')]:
    setup(diff,phase,attack);start=p.evaluate('F.serial')
    for i in range(72):
     tick(6)
     if diff=='normal':
      im=shot(attack+'-'+str(i) if i in [9,19,29,39,49,59] else None)
      if i%2==0:film.append(im)
      if i in [9,29,49]:gallery.append((attack+' '+str(i),im.copy()))
     elif i%10==0:shot()
    row=p.evaluate('({error:VK.maxError,rays:VK.rays,shots:VK.shots,keys:VK.keys.size,finite:Number.isFinite(B.x+B.y+B.hp),rotations:VK.rotation.size,boxes:VK.warningBoxes})');ck(diff+' '+attack+' actual sockets and damage rays stay registered',row['finite'] and row['error']<.02,row)
    ck(diff+' '+attack+' actual art paints without anchored warning boxes',row['keys']>0 and row['boxes']==0,row)
  film[0].save(O/'attack-reel.webp',save_all=True,append_images=film[1:],duration=200,loop=0,quality=87)
  # Every real target receives real damage, flashes actual pixels, expires,
  # then breaks into its authored modules and stays absent.
  for id in ['shoulderL','left','shoulderR','right','ventL','ventR','legL','legR','core','head']:
   phase='arms' if id in ['shoulderL','left','shoulderR','right'] else 'head' if id=='head' else 'core';setup(phase=phase);tick(1)
   row=p.evaluate('''id=>{const part=B.parts.find(q=>q.id===id),hp=part.hp,before=volcanoPaintPart(id);B._lastPart=part;modularHit(1);const after=volcanoPaintPart(id);let changed=0;for(let i=0;i<after.length;i+=4)if(after[i]!==before[i]||after[i+1]!==before[i+1]||after[i+2]!==before[i+2])changed++;return{loss:hp-part.hp,owner:B.flash,part:part.flash,changed};}''',id);ck(id+' actual damage flashes its own rendered pixels',row['loss']==1 and row['owner']>0 and row['part']>0 and row['changed']>10,row)
   tick(15);ck(id+' native hit flash expires',p.evaluate('id=>B.parts.find(q=>q.id===id).flash<=0&&B.flash<=0',id))
   row=p.evaluate('''id=>{const part=B.parts.find(q=>q.id===id);B._noHit=false;B._lastPart=part;modularHit(part.hp+1);return{dead:part.destroyed,hp:part.hp,gone:!v18Rig(B).some(v=>v.p===part),budget:B.hp===B.parts.reduce((s,q)=>s+q.hp,0)};}''',id);ck(id+' breaks independently and leaves no lingering piece',row['dead'] and row['hp']==0 and row['gone'] and row['budget'],row)
   if id!='head':tick(45);ck(id+' stays broken after native attack updates',p.evaluate('id=>B.parts.find(q=>q.id===id).destroyed&&!v18Rig(B).some(v=>v.p.id===id)',id))
  setup(attack='sweep');tick(95);row=p.evaluate('''()=>{const before=F.beams.filter(q=>q._vp23Emitter==='left').length;B._lastPart=B.parts.find(q=>q.id==='left');modularHit(B._lastPart.hp+1);return{before,beams:F.beams.filter(q=>q._vp23Emitter==='left').length,tells:F.tells.filter(q=>q._vp23Emitter==='left').length};}''');ck('Breaking a firing nozzle removes its live beam immediately',row['before']>0 and row['beams']==0 and row['tells']==0,row)
  setup();p.evaluate('()=>{B._lastPart=B.parts.find(q=>q.id==="right");modularHit(B._lastPart.hp+1);eBullets=[];F.beams=[];F.tells=[];}');tick(210);row=p.evaluate('({shots:eBullets.filter(q=>q._vp23Emitter==="right").length,shoulder:B.parts.find(q=>q.id==="shoulderR").hp,phase:F.phase})');ck('Destroyed cannon stops firing while shoulder armor remains targetable',row['shots']==0 and row['shoulder']>0 and row['phase']=='arms',row)
  setup(phase='core',attack='rotor');p.evaluate('()=>{B._lastPart=B.parts.find(q=>q.id==="ventL");modularHit(B._lastPart.hp+1);}');tick(180);row=p.evaluate('F.beams.map(q=>q._vp23Emitter)');ck('Destroyed vent cannot emit its rotor flame',not any(q=='ventL' for q in row),row)
  setup(phase='core',attack='ring');p.evaluate('()=>{B._lastPart=B.parts.find(q=>q.id==="core");modularHit(B._lastPart.hp+1);eBullets=[];furnaceNext(P);}');tick(150);row=p.evaluate('({attack:F.attack,shots:eBullets.filter(q=>q._vp23Emitter==="reactor").length})');ck('Destroyed reactor removes its ring and laser attacks',row['attack'] not in ['ring','coreLaser'] and row['shots']==0,row)
  setup();p.evaluate('()=>{v19BeginSwipe(B,"volcanoRake");}');rake=[]
  for i in range(48):tick(6);rake.append(shot('rake-'+str(i) if i in [9,19,29] else None))
  rake[0].save(O/'rake.webp',save_all=True,append_images=rake[1:],duration=100,loop=0,quality=87);row=p.evaluate('({boxes:VK.warningBoxes,done:!B._r30.v18.swipe,rotations:VK.rotation.size})');ck('Articulated rake has real windup, swing and recovery with FOV only',row['boxes']==0 and row['done'] and row['rotations']>15,row)
  setup();p.evaluate('()=>{B._lastPart=B.parts.find(q=>q.id==="left");modularHit(7);window.saved=JSON.stringify(B.parts.map(q=>[q.id,q.hp,q.destroyed]));j3Save(B);v18Enter(B,2,0);v18Enter(B,2,2);}');ck('Copy morph preserves all ten module HP values and breaks',p.evaluate('saved===JSON.stringify(B.parts.map(q=>[q.id,q.hp,q.destroyed]))'))
  setup(phase='core');p.evaluate('()=>{B._lastPart=B.parts.find(q=>q.id==="core");modularHit(B._lastPart.hp+1);window.savedBroken=JSON.stringify(B.parts.map(q=>[q.id,q.hp,q.destroyed]));j3Save(B);v18Enter(B,2,0);v18Enter(B,2,2);}');ck('Destroyed reactor stays absent and disabled after morphing away and back',p.evaluate('savedBroken===JSON.stringify(B.parts.map(q=>[q.id,q.hp,q.destroyed]))&&vp23Missing(B,"core")&&!v18Rig(B).some(v=>v.layer==="reactor")'))
  setup();row=p.evaluate('''()=>{const before=ctx.getTransform(),alpha=ctx.globalAlpha,composite=ctx.globalCompositeOperation;for(let i=0;i<16;i++){F.t=i*.06;v19Body(B);}const after=ctx.getTransform();return{same:['a','b','c','d','e','f'].every(k=>before[k]===after[k]),alpha:alpha===ctx.globalAlpha,composite:composite===ctx.globalCompositeOperation};}''');ck('All articulated layers and sixteen vent frames restore canvas state',all(row.values()),row)
  ck('Native renderer blits every component and PixelLab vent frame',p.evaluate('Object.keys(VP23.draws).length>=15'),p.evaluate('VP23.draws'))
  ck('No page, console, draw or asset errors',not errors,errors);br.close()
finally:stop()
sheet=Image.new('RGB',(3*320,8*370),'#0c1018');d=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(gallery):
 im.thumbnail((320,340));x=i%3*320;y=i//3*370;sheet.paste(im,(x,y));d.text((x+8,y+342),label,fill='white')
sheet.save(O/'native-sheet.png');report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True);raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
