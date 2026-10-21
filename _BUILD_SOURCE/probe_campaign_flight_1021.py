"""Actual intro exhaust, dialogue alpha, map boot framing and ocean source cells."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_flight_1021';O.mkdir(parents=True,exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=128
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.pilot="yuri";run.mode="campaign";campaignIntroStart();campaignIntroWarm();UI20.warm();cmap2Warm();}')
  p.wait_for_function('()=>campaignIntroKeys().every(k=>XART.rdy(k))&&XART.rdy(S1W20_ART.key)&&bmfReady("dialogue")')
  p.evaluate('''()=>{window.cf21Calls=[];window.cf21Burn=false;const thrust=pf27PlaneThrustDraw,draw=ctx.drawImage;
   pf27PlaneThrustDraw=function(){cf21Burn=true;try{return thrust.apply(this,arguments);}finally{cf21Burn=false;}};
   ctx.drawImage=function(im,...a){if(cf21Burn)cf21Calls.push(a);return draw.call(this,im,...a);};}''')
  for pilot in p.evaluate('PILOTS.map(p=>p.key)'):
   rows=[]
   for time in [.44,.55,.66]:
    row=p.evaluate('''([pilot,t])=>{run.pilot=pilot;campaignIntro.pilot=pilot;const beat=IP21.beats.find(b=>b.comic);cf21Calls=[];
     const previous=player._thrustFrame;ctx.setTransform(SS,0,0,SS,0,0);ip21Visual(beat,campaignIntro,t,cutsceneViewWidth(),VH);
     const q={...PT11_UI.ship};const bytes=ctx.getImageData(Math.floor((q.x-q.w/2)*SS),Math.floor(q.y*SS),Math.ceil(q.w*SS),Math.ceil(q.h*.95*SS)).data;
     let hash=2166136261;for(const v of bytes)hash=Math.imul(hash^v,16777619);
     return{...q,calls:cf21Calls.length,hash,restored:player._thrustFrame===previous};}''',[pilot,time]);rows.append(row)
   ck(pilot+' flight has actual animated exhaust at its authored engine mounts',all(r['plume'] and r['calls']>=2 and r['restored'] and r['key'].startswith('ship_'+pilot) for r in rows) and len({r['hash'] for r in rows})>1,rows)
   p.screenshot(path=str(O/(pilot+'-flight.png')))
  for portrait in [False,True]:
   row=p.evaluate('''portrait=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#ff00ff';ctx.fillRect(0,0,cv.width/SS,cv.height/SS);const x=20,y=100,w=450,h=120;
    ui20Panel('YURI',x,y,w,h,portrait);const d=ctx.getImageData((x+7)*SS,(y+7)*SS,(w-14)*SS,(h-14)*SS).data;let transparent=0,opaque=0;
    for(let i=0;i<d.length;i+=4){if(d[i]>220&&d[i+1]<30&&d[i+2]>220)transparent++;if(d[i]<80&&d[i+2]<80)opaque++;}
    return{transparent,opaque};}''',portrait)
   # The native canvas is alpha:false. These tiny bevel cutouts lie INSIDE
   # the old seven-pixel backing; background pixels here used to turn black.
   ck(('Portrait' if portrait else 'Portrait-free')+' dialogue has transparent outer cutouts and an opaque text plate',row['transparent']>0 and row['opaque']>10000,row)
  p.evaluate('''()=>{ht27Stop();BOFCinematicDirector.cancel();Rival24.reset();run.pilot='cole';run.mode='campaign';campaign.rank={};campaign.unlockedMax=1;
   campaign.bonusUnlocked=false;campaign.stageX1004=null;campaign.rivalScattered=false;CF4.flight=4;campPause=null;s9MapCine=null;riftReturn=null;
   campaignIntro=null;_setCinematicViewport(false);openStageSelect(1,{boot:true});Input.clearTaps();Input.mouse.active=false;map4eWarm();}''')
  p.wait_for_function('()=>MAP4E.keys.every(k=>XART.rdy("map4e_region_"+k))&&XART.rdy("ship_cole")&&MAP4F_FLAG_STATES.every(v=>XART.rdy("map4f_flag1_"+v))')
  rows=[]
  for n in range(20):
   p.evaluate(shoot.STEP,30);p.wait_for_timeout(15)
   row=p.evaluate('''()=>({boot:sselBoot,time:sselBootT,z:cmap2.cam.z,ship:sselShip&&cmap2ToScreen(sselShip.x,sselShip.y),frame:CW21.frame,draws:CW21.draws})''');rows.append(row)
   if n in [4,9,19]:p.screenshot(path=str(O/('map-boot-'+str(n)+'.png')))
  ck('Actual new-campaign boot stays close while the jet approaches Stage1',all(r['z']>=1.5 and (r['time']<1.7 or r['ship'] and 80<=r['ship']['y']<=278) for r in rows),rows)
  ck('Actual map boot completes and the new ocean keeps animating',not rows[-1]['boot'] and len({r['frame'] for r in rows})>8 and rows[-1]['draws']>rows[0]['draws'],rows)
  row=p.evaluate('''()=>{const real=ctx.drawImage;let cells=[],smooth=[];ctx.drawImage=function(im,...args){cells.push(args.slice(0,4));smooth.push(ctx.imageSmoothingEnabled);return real.call(this,im,...args);};
   const frames=[];try{for(let n=0;n<S1W20_ART.frames;n++){cmap2.t=(n+.2)/S1W20_ART.fps;cells=[];cmap2DrawOcean();frames.push({n,cells:cells.slice(0,1),count:cells.length});}}finally{ctx.drawImage=real;}
   return{frames,smooth,expected:S1W20_ART.cells};}''')
  ck('All32 approved ocean poses blit their registered atlas cells through the native game context',all(r['count']>0 and r['cells'][0]==row['expected'][r['n']] for r in row['frames']) and not any(row['smooth']),row['frames'])
  p.screenshot(path=str(O/'map-close-water.png'))
  ck('No page, console, draw or missing-art errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
