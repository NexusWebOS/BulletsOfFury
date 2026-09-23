"""Verify the authored fire muzzle at the moving whip pivot in play and Forge."""
import base64,json,sys,http.server,io
from PIL import Image
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/firewhip_sweep_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];results={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1500,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(TRAP_RAF)
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':False})
  pg.evaluate("""()=>{story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
    run.weapon=3;run.wlevel=1;run.wlevels=WEAPONS.map(()=>1);run.spaceMode=false;run.forge={3:{elem:'fire',lv:1}};run.forgeForms={3:{fire:{elem:'fire',lv:1}}};run.wvars=WEAPONS.map(()=>null);run.wvars[3]='firewhip';
    player.x=240;player.y=400;player.dead=false;player.invuln=0;player.roll=0;shake=0;camX=0;pShoot();
    window.muzzleCalls=[];let active=null;const muzzle=roundLaserMuzzleDraw,draw=ctx.drawImage;
    roundLaserMuzzleDraw=function(g,x,y,size,col,frame){active={x,y,size,col,frame};try{return muzzle(...arguments)}finally{active=null}};
    ctx.drawImage=function(im,...a){if(active)muzzleCalls.push({...active,source:[im.width,im.height]});return draw.call(this,im,...a)};
    for(let i=0;i<8;i++)XART.rdy('laser_round_muzzle_'+i);XART.rdy('forge_fire_laser_0918');
  }""")
  pg.wait_for_function("()=>Array.from({length:24},(_,i)=>i).every(i=>XART.rdy('fire_whip_pose_'+i))&&Array.from({length:8},(_,i)=>i).every(i=>XART.rdy('fire_whip_muzzle_'+i))")
  def capture(name):
   (OUT/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")))
  results['moving']=[]
  for x,y in [(240,400),(290,350),(170,430)]:
   result=pg.evaluate("p=>{player.x=p[0];player.y=p[1];const b=pBullets.find(b=>b.kind==='firewhip');b.life=1;b.t=b.duration*.48;fireWhipTick(b,.016);muzzleCalls=[];drawWorld(0);return {calls:muzzleCalls,pivot:[b.x,b.y]};}",[x,y])
   assert len(result['calls'])==1 and abs(result['calls'][0]['x']-result['pivot'][0])<.01 and result['calls'][0]['y']==y-18 and result['calls'][0]['col']=='#ff6924',result
   assert result['calls'][0]['source']==[128,128],result
   results['moving'].append(result)
  capture('live_firewhip')
  results['stopped']=pg.evaluate("()=>{pBullets=[];player._mgMuzT=0;muzzleCalls=[];drawWorld(0);return muzzleCalls.length}");assert results['stopped']==0
  pg.evaluate("()=>{run.stage=3;run.loadout=[3,0,1,2,4,5];run.forgeElems=Object.fromEntries(Object.keys(INFUSIONS).map(e=>[e,1]));forgeStart();forge.row=1;forge.sel=run.loadout.indexOf(3);forge.esel=forgeElemsFor(3).indexOf('fire');}")
  for _ in range(8):
   pg.evaluate("()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);for(let i=0;i<15;i++)drawForge(1/60);ctx.restore()}");pg.wait_for_timeout(80)
  results['preview']=pg.evaluate("()=>{const b=forge.preview.bullets.find(b=>b.kind==='firewhip');b.t=b.duration*.48;muzzleCalls=[];ctx.save();ctx.setTransform(2,0,0,2,0,0);drawForge(0);ctx.restore();return {calls:muzzleCalls,pivot:[b.x,b.y],error:forge.preview.err};}")
  q=results['preview'];assert len(q['calls'])==1 and abs(q['calls'][0]['x']-q['pivot'][0])<.01 and q['calls'][0]['y']==q['pivot'][1] and q['error'] is None,q
  capture('forge_firewhip')
  # Real complete-pose animation: one unsliced draw per frame, palette-matched muzzle.
  pg.wait_for_function("()=>Array.from({length:24},(_,i)=>i).every(i=>XART.rdy('fire_whip_pose_'+i))")
  frames=[];results['poses']=[]
  for f in range(24):
   data=pg.evaluate("""f=>{const b=forge.preview.bullets.find(b=>b.kind==='firewhip');b.dir=f<12?1:-1;b.t=b.duration*((f%12+.1)/12);forge.preview.t=f*(1.4/24);
     const get=XART.get,draw=ctx.drawImage,blits=[];let active=null;
     XART.get=function(k){active=k.startsWith('fire_whip_pose_')?k:null;return get.call(this,k)};
     ctx.drawImage=function(im,...args){if(active)blits.push({key:active,args:args.length});active=null;return draw.call(this,im,...args)};
     muzzleCalls=[];try{ctx.save();ctx.setTransform(2,0,0,2,0,0);drawForge(0);ctx.restore()}finally{XART.get=get;ctx.drawImage=draw}
     const rootX=b.x;
     const v=frc(FORGE_CHAMBER.view,cutsceneViewWidth(),VH);return {blits,muzzles:muzzleCalls,rootX,view:v.map(n=>Math.round(n*2)),png:document.getElementById('screen').toDataURL().split(',')[1]};}""",f)
   assert data['blits']==[{'key':f'fire_whip_pose_{f}','args':4}],data['blits']
   assert len(data['muzzles'])==1 and abs(data['muzzles'][0]['x']-data['rootX'])<.01,data['muzzles']
   results['poses'].append({'blits':data['blits'],'muzzleX':data['muzzles'][0]['x'],'rootX':data['rootX']})
   x,y,w,h=data['view'];frames.append(Image.open(io.BytesIO(base64.b64decode(data['png']))).crop((x,y,x+w,y+h)))
  frames[0].save(OUT/'wide_whip.gif',save_all=True,append_images=frames[1:],duration=58,loop=0,disposal=2)
  frames[5].save(OUT/'wide_whip_detail.png')
  contact=Image.new('RGB',(frames[0].width*4,frames[0].height*2))
  for i,f in enumerate([0,3,6,11,12,15,18,23]):contact.paste(frames[f],((i%4)*frames[f].width,(i//4)*frames[f].height))
  contact.save(OUT/'wide_whip_contact.png')
  results['collision']=pg.evaluate("""()=>{const b={x:240,y:400,reach:122,dir:1,dmg:5,_hit:[]};let checked=0;
    for(let f=0;f<24;f++){b.dir=f<12?1:-1;const progress=(f%12+.1)/12,scale=b.reach/FIRE_WHIP_POSES.reach;
      for(const r of FIRE_WHIP_POSES.frames[f]){const e={x:b.x+(r[0]+r[2]/2-192)*scale,y:b.y+(r[1]+r[3]/2-224)*scale,w:0,h:0};if(!fireWhipTouches(b,e,progress,progress))throw Error('missed authored cell '+f);checked++;}
      if(fireWhipTouches(b,{x:240,y:450,w:2,h:2},progress,progress))throw Error('hit behind root');
    }
    const saved={enemies,hitEnemy,powerups,bossActive,subBossActive};let once,twice;
    try{enemies=[{x:240,y:392,w:4,h:4,received:0}];powerups=[];bossActive=false;subBossActive=false;hitEnemy=(e,d)=>e.received+=d;
      b.dir=1;fireWhipStrike(b,0,1);fireWhipStrike(b,0,1);once=enemies[0].received;b.dir=-1;b._hit=[];fireWhipStrike(b,0,1);twice=enemies[0].received;
    }finally{enemies=saved.enemies;hitEnemy=saved.hitEnemy;powerups=saved.powerups;bossActive=saved.bossActive;subBossActive=saved.subBossActive}
    return {checked,once,twice};}""")
  results['sideReach']=pg.evaluate("""()=>{const m=FIRE_WHIP_POSES,scale=122/m.reach;return [0,11,12,23].map(f=>{const xs=m.frames[f].flatMap(r=>[r[0]-192,r[0]+r[2]-192]);return [Math.min(...xs)*scale,Math.max(...xs)*scale]})}""")
  assert results['sideReach'][0][0]<-100 and results['sideReach'][1][1]>100 and results['sideReach'][2][1]>100 and results['sideReach'][3][0]<-100,results['sideReach']
  # The flame's lower shaft must bend both directions while the source and flash stay on the nose.
  def ink_x(frame,lo,hi):
   import numpy as np
   a=np.asarray(Image.open(ROOT/f'assets/game/player_weapons/fire_whip_sweep_0923/pose_{frame}.png'))[:,:,3]
   yy,xx=np.where(a[lo:hi]>96)
   return float(xx.mean()-192)
  results['hinge']={'baseLeft':ink_x(0,204,220),'baseRight':ink_x(11,204,220),'shaftLeft':ink_x(0,160,184),'shaftRight':ink_x(11,160,184)}
  assert abs(results['hinge']['baseLeft'])<5 and abs(results['hinge']['baseRight'])<5 and results['hinge']['shaftLeft']<-40 and results['hinge']['shaftRight']>40,results['hinge']
  assert results['collision']['checked']>700 and results['collision']['once']==5 and results['collision']['twice']==10,results['collision']
  assert not errors,errors
  results['errors']=errors;(OUT/'results.json').write_text(json.dumps(results,indent=2));print('PASS: 24 authored poses, fixed muzzle, lower flame bends both ways, matching baked collision, one hit per stroke; no browser errors.');br.close()
finally:stop()
