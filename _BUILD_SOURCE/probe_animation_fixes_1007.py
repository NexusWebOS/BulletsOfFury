"""Final focused regression of discovered failures and native comparison frames."""
from pathlib import Path
import json,sys,base64,http.server,subprocess,io
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/projectiles_1007/final';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));report={'errors':[],'cases':[],'checks':{},'frames':{}}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(120000)
  p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p.on('pageerror',lambda e:report['errors'].append(str(e)))
  def boot():
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
   for f in ['balance_lab_1007.js','projectile_lab_1007.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/f))
  boot()
  for diff in ['easy','normal','hard','furious']:
   for args in [dict(stage=3,kind='cryospear'),dict(stage=3,kind='frostcruiser',mini=True),dict(stage=6,kind='warhive',ace=True),dict(stage=6,kind='warhive',slice=True),dict(stage=8,kind='heralddeath',mini=True)]:
    boot();case={**args,'diff':diff,'pilot':'yuri','level':3,'id':f'{diff}-s{args["stage"]}-{args["kind"]}'+('-ace' if args.get('ace') else '')+('-stage' if args.get('slice') else '')}
    p.evaluate('c=>AP7.begin(c)',case)
    for i in range(72 if args.get('slice') else 48):
     row=p.evaluate('()=>AP7.step(30)')
     if i%10==0:p.wait_for_timeout(20)
    row['case']=case;report['cases'].append(row)
    if args['stage']==8:
     # Wait for a real shot; record 30 full native frames at 30fps while flying.
     for i in range(120):
      if p.evaluate("()=>eBullets.some(b=>b._heraldProjectile&&b.y>180&&b.y<430)"):break
      p.evaluate('()=>AP7.step(10)')
     if diff=='normal':
      frames=[]
      for f in range(30):
       p.evaluate('()=>{player.invuln=99999;updatePlay(1/60);updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/30);}')
       frames.append(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
      report['frames']['heraldLive']=frames
      (O/'herald-live.png').write_bytes(base64.b64decode(frames[15]))
    print('RECHECK',case['id'],'invalid draws',len(row['geometry']),flush=True)
    (O/'audit.json').write_text(json.dumps({k:v for k,v in report.items() if k!='frames'},indent=2)+'\n',encoding='utf-8')
  # Isolate the projectile renderer from any live cross/beam still owned by
  # the previous encounter before measuring opacity and source-frame bounds.
  p.evaluate("()=>{AP7.begin({stage:8,kind:'heralddeath',mini:true,diff:'normal',pilot:'yuri',id:'isolated'});boss=null;subBoss=null;bossActive=subBossActive=false;enemies=[];}")
  p.evaluate("""()=>{window.specialCatalog=()=>{
   const variants=[];
   for(const role of ['machine','mg','rocket','lightning','lightningmg','spread','orb','lance'])variants.push({kind:'eshot',_s4wKind:role});
   for(const family of ['inferno_mg','inferno_shotgun','cryo_ball','rime_orb'])variants.push({kind:'eshot',_l23fx:family});
   for(const kind of ['pellet','laser','missile','orb'])variants.push({kind,_boss:true});
   for(const role of [6,7,8])variants.push({kind:'s8pair',_r30Shot:role,_r30Age:0});
   variants.push({kind:'eshot',_s7modOrb:true},{kind:'eshot',_s7modGun:true},{kind:'eshot',_s3DroneShot:true},{kind:'eglaser',_hammerLaser:true},{kind:'frostNoseLaser',_frostNoseLaser:true},{kind:'s8pair',_alienOrb1003:true});
   return variants.map(v=>{const b={x:240,y:256,vx:3,vy:0,w:12,h:24,ang:0,t:0,life:4,_noArsenal:true,...v},frames=[];
    for(let f=0;f<16;f++){b.t=b._visualAge=f/24;frames.push(AP7.frame(b));}return{variant:v,frames};});
  };specialCatalog();}""");p.wait_for_timeout(600)
  report['specialized']=[]
  for diff in ['easy','normal','hard','furious']:
   p.evaluate("d=>{diffKey=d;DIFF=difficultyForRun('arcade',d);AP7.geometry=[];}",diff)
   report['specialized'].append({'diff':diff,'rows':p.evaluate('()=>specialCatalog()'),'geometry':p.evaluate('()=>AP7.geometry')})
  # Render old and new CFX implementations against the same actual assets.
  raw=subprocess.run(['git','-C',str(R),'--work-tree='+str(R),'show','HEAD:assets/game.js'],capture_output=True,check=True).stdout.decode('utf-8')
  old=raw[raw.index('function drawCfxStageProjectile(b){'):raw.index('\nfunction drawCombatFinalProjectile(b){',raw.index('function drawCfxStageProjectile(b){'))]
  p.evaluate('src=>{window.CFX_CURRENT=drawCfxStageProjectile;window.CFX_OLD=(0,eval)("("+src+")");}',old)
  p.evaluate("()=>{for(const S of Object.values(CFX_STAGE_PROJECTILE))XART.rdy(S[0]);}");p.wait_for_timeout(200)
  for kind in ['s8pair','s8blade','s8rift','s7bio']:
   row={}
   for before in [True,False]:
    row['before' if before else 'after']=p.evaluate("""q=>{
     drawCfxStageProjectile=q.before?CFX_OLD:CFX_CURRENT;
     const frames=[],c=document.createElement('canvas');c.width=160;c.height=160;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
     for(let f=0;f<90;f++){const b={kind:q.kind,x:240,y:256,w:16,h:16,vx:0,vy:3,t:f/30,_visualAge:f/30,_noArsenal:true};AP7.frame(b);
      g.clearRect(0,0,160,160);g.drawImage(cv,160*SS,176*SS,160*SS,160*SS,0,0,160,160);frames.push(c.toDataURL());}
     drawCfxStageProjectile=CFX_CURRENT;return frames;
    }""",{'before':before,'kind':kind})
   report['frames'][kind]=row
  # Native opacity, source-pivot and frame-rate contracts, with final code.
  report['checks']=p.evaluate("""()=>{
   const out={};let vals=[];for(const hz of [30,60,120]){let b={_visualAge:0};for(let n=0;n<hz;n++)b._visualAge+=1/hz;vals.push(projectileVisualFrame(b,12,8));}
   out.sameFrameAtAllRates=vals.every(f=>f===4);
   const old=ctx.globalAlpha;ctx.globalAlpha=0;const f=AP7.frame({kind:'s8pair',x:240,y:256,t:.4,vx:0,vy:3,_noArsenal:true});ctx.globalAlpha=old;out.hiddenShotsDoNotLeakHighlights=f.n===0;
   const alpha=CFX_CURRENT({kind:'s8pair',x:240,y:256,t:.4,vx:0,vy:3});out.originalSpriteDraws=alpha;
   const ps=[];for(const hz of [30,60,120]){const p={x:0,y:0,vx:100,vy:50,t:0,life:2};for(let n=0;n<hz;n++)deathDebrisTick(p,1/hz);ps.push(p);}
   out.debrisDistance=ps.every(p=>p.x>50&&p.x<65);out.debrisRateIndependent=ps.every(p=>Math.abs(p.x-ps[0].x)<1e-8);
   return out;
  }""")
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps({k:v for k,v in report.items() if k!='frames'},indent=2)+'\n',encoding='utf-8')
for kind,row in report['frames'].items():
 if kind=='heraldLive':pairs=[('herald-live',row)]
 else:pairs=[(kind+'-'+state,frames) for state,frames in row.items()]
 for name,frames in pairs:
  images=[Image.open(io.BytesIO(base64.b64decode(f.split(',')[-1]))).convert('RGBA') for f in frames]
  images[0].save(O/(name+'.webp'),save_all=True,append_images=images[1:],duration=[33,33,34]*(len(images)//3),loop=0,lossless=True,method=4)
  for im in images:im.close()
print('DONE',json.dumps({'errors':report['errors'],'checks':report['checks']}),flush=True)
