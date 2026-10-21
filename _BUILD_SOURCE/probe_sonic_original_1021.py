"""Native PixelLab sonic-bank playback, damage flashes, tells and safe gaps."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/sonic_original_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&window.BOF_SONIC_EFFECTS');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.mode="arcade";run.pilot="cole";pilotIndex=PILOTS.findIndex(q=>q.key==="cole");startRun(1);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);player.invuln=1e9;storySkip();BOFCinematicDirector.cancel();}')
  p.evaluate('''()=>{sx21Warm();window.sx21draws=[];const draw=ctx.drawImage;
   ctx.drawImage=function(im,...args){if(im?._so21)sx21draws.push({...im._so21,args});return draw.call(this,im,...args);};}''')
  p.wait_for_function('()=>Object.values(SX21_ART.banks).every(a=>XART.rdy(a.key)&&XART.rdy(a.sourceKey))')
  for bank in p.evaluate('Object.keys(SX21_ART.banks)'):
   row=p.evaluate('''bank=>{const a=SX21_ART.banks[bank];sx21draws=[];let exact=true,mask=true,alpha=true;const source=SX21.base.get(a.sourceKey),ref=document.createElement('canvas');ref.width=256;ref.height=256;ref.getContext('2d').drawImage(source,0,0);const orig=ref.getContext('2d').getImageData(0,0,256,256).data;const hashes=[];
    for(let f=0;f<a.frames;f++){const im=sx21Frame(bank,(f+.1)/a.fps),px=im.getContext('2d').getImageData(0,0,256,256).data;let hash=2166136261;
     for(let j=0;j<px.length;j+=4){if(orig[j+3]>0){mask&&=px[j+3]>0;const tol=Math.ceil(255/px[j+3])+Math.ceil(255/orig[j+3]);exact&&=[0,1,2].every(k=>Math.abs(px[j+k]-orig[j+k])<=tol);}else mask&&=px[j+3]===0;
      alpha&&=px[j+3]<=orig[j+3]&&px[j+3]>=Math.floor(orig[j+3]*.72);hash=Math.imul(hash^px[j+3],16777619);
      if(f===0||f===a.frames-1)exact&&=px[j+3]===orig[j+3];}
     ctx.setTransform(SS,0,0,SS,0,0);ctx.drawImage(im,100,100,256,256);hashes.push(hash);}
    return{a,exact,mask,alpha,unique:new Set(hashes).size,draws:sx21draws};}''',bank)
   ck(bank+' original palette and silhouette survive native canvas rounding',row['exact'] and row['mask'] and row['alpha'],dict(source=row['a']['sourceKey']))
   ck(bank+' all9 original-based animation frames blit natively',len(row['draws'])==9 and row['unique']>=3 and all(d['frame']==i for i,d in enumerate(row['draws'])),dict(unique=row['unique']))
   p.wait_for_timeout(15)
  def tick(n):
   for i in range(0,n,12):
    result=p.evaluate(shoot.STEP,min(12,n-i))
    if result:errors.append(result)
    p.wait_for_timeout(10)
  for variant in ['green','red']:
   row=p.evaluate('''variant=>{const a=SX21_ART.banks['ring_'+variant],clock=efxClock,counts=[];ctx.setTransform(SS,0,0,SS,0,0);
    try{for(let i=0;i<a.frames;i++){efxClock=(i+.1)/a.fps;ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width/SS,cv.height/SS);
     razorbackWaveDraw({x:240,y:140,r:75,a:0,arc:.65,width:8,fade:1,furious:variant==='red'});
     const px=ctx.getImageData(130*SS,170*SS,220*SS,100*SS).data;let n=0;for(let j=0;j<px.length;j+=4)if(Math.max(px[j],px[j+1],px[j+2])>40)n++;counts.push(n);}
    }finally{efxClock=clock;}return counts;}''',variant)
   ck(variant+' ring remains visibly present in every animated danger-arc frame',min(row)>70,row)
  for diff in ['normal','hard','furious']:
   p.evaluate('''diff=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);enemies=[];eBullets=[];pBullets=[];stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;
    boss=null;bossActive=false;subBoss=null;spawnSubBoss('razorback');window.sx21actors=subBoss._rzbPair?subBoss._rzbPair.actors:[subBoss];
    for(const a of sx21actors){a.x=camLeftX()+viewW()*(sx21actors.length>1?(a._rzb.pairSide<0?.28:.72):.5);a.y=VH*.28;a.enter=false;a.dead=false;const r=a._rzb;r.state='guns';r.attack='sonic';r.at=.6;r.charge=.5;r.turret=0;r.a=0;r.tgt={x:a.x,y:a.y};razorbackUpdate(a,0);}
    player.x=camLeftX()+viewW()*.5;player.y=VH*.8;player.invuln=1e6;Input.clearTaps();sx21draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''',diff)
   p.wait_for_function('()=>["rzb_hull_0","rzb_turret","rzbf_hull_0","rzbf_turret","rzb_machinegun","rzbf_machinegun"].every(k=>XART.rdy(k))')
   p.evaluate('()=>{sx21draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   row=p.evaluate('''()=>({actors:sx21actors.length,red:sx21actors[0]._rzb.furious||false,draws:sx21draws})''')
   color='red' if diff=='furious' else 'green'
   ck(diff+' native tank charge uses the new '+color+' spiral and retains the duo',any(d['key']=='so21_charge_'+color for d in row['draws']) and row['actors']==(2 if diff=='hard' else 1),row['actors'])
   p.screenshot(path=str(O/(diff+'-tank-charge.png')))
   hit=p.evaluate('''()=>{const a=sx21actors[0],before=ctx.getImageData(0,0,cv.width,cv.height).data;
    const dealt=razorbackHit(a,1);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let pixels=0;
    for(let i=0;i<after.length;i+=4)if(after[i]>150&&after[i+1]>150&&after[i+2]>150&&after[i]-before[i]>30&&after[i+1]-before[i+1]>30&&after[i+2]-before[i+2]>30)pixels++;
    return{dealt,pixels,partFlash:a._rzb.flash.left};}''');p.screenshot(path=str(O/(diff+'-tank-hit.png')))
   ck(diff+' native tank damage still visibly flashes actual authored pixels',hit['dealt']>0 and hit['partFlash']>0 and hit['pixels']>10,hit)
   tick(55)
   row=p.evaluate('''()=>({count:eBullets.filter(q=>q.kind==='rzbSonic').length,draws:sx21draws.slice(-500),flash:sx21actors[0]._rzb.flash.left})''')
   ck(diff+' real tank releases use animated waves and hit flash expires',row['count']>0 and any(d['key']=='so21_bullet_'+color for d in row['draws']) and row['flash']==0,dict(count=row['count']))
   p.screenshot(path=str(O/(diff+'-tank-release.png')))
   # Exercise the exact native segmented ring, including its safe angular gaps.
   row=p.evaluate('''()=>{const red=diffKey==='furious',segments=rzbFuriousSegments(1.05,5),w={x:camLeftX()+viewW()/2,y:VH*.18,r:120,a:0,arc:1.05,width:10,fade:1,furious:red,segments:red?segments:null};
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);sx21draws=[];razorbackWaveDraw(w);return{calls:sx21draws.filter(d=>d.key==='so21_ring_'+(red?'red':'green')).length,segments:segments.length,safe:!rzbWaveAngleHit({...w,segments},(segments[0][1]+segments[1][0])/2),danger:rzbWaveAngleHit({...w,segments},(segments[0][0]+segments[0][1])/2)};}''')
   ck(diff+' animated ring keeps the native safe-gap geometry',row['calls']==(5 if diff=='furious' else 1) and row['safe'] and row['danger'],row)
   p.screenshot(path=str(O/(diff+'-tank-ring.png')))
   p.evaluate('''()=>{subBoss=null;subBossActive=false;eBullets=[];pBullets=[];spawnBoss('damkeeper');updateOverlordX(boss,0);boss.enter=false;boss.dead=false;boss._ovIntro=null;boss._ovAirborne=false;boss._noHit=false;
    boss.x=camLeftX()+viewW()/2;boss.y=VH*.24;boss._pivot=0;boss.t=1;ovSonicStart(boss);boss._ovSonic.t=1.05;sx21draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''')
   p.wait_for_function('()=>XART.rdy("ovbody_intact")&&XART.rdy("ovrotor_00")')
   p.evaluate('()=>{sx21draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   color='fury' if diff=='furious' else 'normal'
   row=p.evaluate('''()=>({phase:boss._ovSonic.phase,t:boss._ovSonic.t,draws:sx21draws})''')
   ck(diff+' helicopter native2.1s warning charges at its actual sonic mount',any(d['key']=='so21_charge_green' for d in row['draws']) and row['phase']=='waveTell',dict(phase=row['phase'],time=row['t']))
   p.screenshot(path=str(O/(diff+'-helicopter-charge.png')))
   tick(70)
   row=p.evaluate('''()=>({waves:eBullets.filter(q=>q._ovSonicWave).map(q=>({w:q.w,h:q.h,vertical:q.vertical,proof:q._weaponProof,shootable:q._shootable})),draws:sx21draws.slice(-500)})''')
   ck(diff+' native helicopter pressure fronts use the new bank and remain unshootable',len(row['waves'])>0 and all(q['proof'] and not q['shootable'] for q in row['waves']) and any(d['key']=='so21_wave_green' for d in row['draws']),row['waves'])
   p.screenshot(path=str(O/(diff+'-helicopter-wave.png')))
   tick(40);p.screenshot(path=str(O/(diff+'-helicopter-blades.png')))
   row=p.evaluate('''()=>{const q={x:240,y:240,ang:Math.PI/2,_waveW:190,_waveH:46};return{center:ovSonicWaveHit(q,{x:240,y:240},9,10),edge:ovSonicWaveHit(q,{x:360,y:240},9,10),corner:ovSonicWaveHit(q,{x:322,y:267},9,10)};}''')
   ck(diff+' original pressure-front collision remains precise',row==dict(center=True,edge=False,corner=False),row)
  ck('Original sonic keys stay unchanged outside enemy rendering',p.evaluate('!SX21.active&&!["rzb_sonic_bullet","rzb_sonic_wave","rzb_sonic_ring","rzb_sonic_charge"].some(k=>XART.get(k)._so21)'))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/sonic_effects_1021/index.html?scene=heli&difficulty=furious&revision=sonic-original-1021')
  p.wait_for_function('!document.querySelector("#replay").disabled');game=p.frames[1]
  game.wait_for_function('window.BOF_SONIC_EFFECTS&&boss?._ovSonic')
  ck('Native review starts the selected Furious helicopter combo',game.evaluate('diffKey==="furious"&&boss.kind==="damkeeper"&&!!boss._ovSonic'))
  for scene in ['tank','nova','charge']:
   p.select_option('#scene',scene);p.wait_for_timeout(300)
   ck('Native review replays '+scene,game.evaluate('scene=>scene==="charge"?boss?._ovState==="chargeTell":!!(subBoss?._rzb||subBoss?._rzbPair)',scene))
  p.select_option('#difficulty','hard');p.select_option('#scene','tank');p.wait_for_timeout(500)
  ck('Native review retains both Hard-mode tank actors',game.evaluate('subBoss?._rzbPair?.actors.length===2'))
  p.screenshot(path=str(O/'native-review-hard-duo.png'))
  ck('No page, console, draw or missing-asset errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
