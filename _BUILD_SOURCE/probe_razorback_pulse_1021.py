"""Native PixelLab sonic-bank playback, damage flashes, tells and safe gaps."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/razorback_arc_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
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
  for color in ['green','red']:
   row=p.evaluate('''color=>{const a=SX21_ART.banks['pulse_'+color],hashes=[];sx21draws=[];let colored=0,gold=0;for(let f=0;f<a.frames;f++){const im=sx21Frame('pulse_'+color,(f+.1)/a.fps),px=im.getContext('2d').getImageData(0,0,128,128).data;let hash=2166136261;for(let j=0;j<px.length;j+=4){hash=Math.imul(hash^px[j]^px[j+1]^px[j+2],16777619);if(px[j+3]>100){if(color==='red'?px[j]>px[j+1]*1.3&&px[j]>px[j+2]*1.3:px[j+1]>px[j]*1.3&&px[j+1]>px[j+2]*1.3)colored++;if(px[j]>px[j+1]*1.15&&px[j+1]>px[j+2]*1.5&&px[j+1]>35)gold++;}}hashes.push(hash);ctx.setTransform(SS,0,0,SS,0,0);ctx.drawImage(im,80,80,128,128);}return{draws:sx21draws.length,unique:new Set(hashes).size,colored,gold};}''',color)
   ck(color+' actual gold-arc replacement has16 animated frames, correct palette and no gold',row['draws']==16 and row['unique']>=12 and row['colored']>1000 and row['gold']==0,row)
  def tick(n):
   for i in range(0,n,12):
    r=p.evaluate(shoot.STEP,min(12,n-i))
    if r:errors.append(r)
    p.wait_for_timeout(10)
  for diff in ['normal','hard','furious']:
   p.evaluate('''diff=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);storySkip();BOFCinematicDirector.cancel();run.sonicT=0;sonicTrail=[];enemies=[];eBullets=[];pBullets=[];stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;boss=null;bossActive=false;subBoss=null;mapScroll=1400;spawnSubBoss('razorback');window.rpActors=subBoss._rzbPair?.actors||[subBoss];subBoss.enter=false;subBoss._noHit=false;for(const b of rpActors){b.enter=false;b._noHit=false;b.y=VH*.25;b._rzb.state='guns';b._rzb.trans=0;b._rzb.tgt={x:b.x,y:b.y};razorbackUpdate(b,0);}player.x=camLeftX()+viewW()/2;player.y=VH*.80;player.invuln=1e9;Input.clearTaps();TARGET17.events=[];window.rpCaught=[];sx21draws=[];}''',diff)
   p.wait_for_function('()=>rpActors.every(b=>XART.rdy(b._rzb.furious?"rzbf_hull_0":"rzb_hull_0"))')
   wanted=2 if diff=='hard' else 1
   for batch in range(90):
    tick(12)
    row=p.evaluate('''()=>{for(const q of eBullets)if(q._target17Art==='sonic'&&!q.dead&&!rpCaught.includes(q))rpCaught.push(q);return{seen:new Set(rpCaught.map(q=>q._target17Port)).size,live:eBullets.some(q=>q._target17Art==='sonic'&&!q.dead)};}''')
    if row['seen']>=wanted and row['live']:break
   tick(12)
   row=p.evaluate('''()=>({events:TARGET17.events.filter(e=>e.type==='weapon-shot'&&e.kind==='sonic').length,actors:rpActors.length,shots:rpCaught.map(q=>({red:q._target17RazorFurious,g:sx21TargetPulseGeometry(q),port:q._target17Port,hp:q.hp,shootable:q._shootable,guide:q._target17Guide?.for})),draws:sx21draws.slice(-600)})''')
   color='red' if diff=='furious' else 'green'
   ck(diff+' naturally releases the specific Retina-targeted sonic attack',row['events']>=wanted and len(row['shots'])>=wanted,row['events'])
   ck(diff+' targeted arcs use '+color+' from their actual firing tank',all(q['red']==(diff=='furious') and q['g']['bank']=='pulse_'+color for q in row['shots']) and any(d['key']=='rp21_pulse_'+color for d in row['draws']),row['shots'])
   ck(diff+' arc faces down toward player and has the requested variant scale',all(abs(q['g']['angle']-3.14159265)<.9 and (117<=q['g']['size']<=168 if diff=='furious' else 78<=q['g']['size']<=112) for q in row['shots']),row['shots'])
   ck(diff+' native guided pulse remains interceptable with its original HP',all(q['shootable'] and q['hp']>=4 and q['guide']==1.35 for q in row['shots']),row['shots'])
   p.screenshot(path=str(O/(diff+'-actual-targeted-pulse.png')))
   if diff=='hard':ck('Both real Hard Razorbacks keep medium green pulses',row['actors']==2 and len(set(q['port'] for q in row['shots']))==2)
   if diff=='furious':
    p.evaluate('''()=>{window.rpDraw=sx21TargetPulseDraw;sx21TargetPulseDraw=undefined;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');p.screenshot(path=str(O/'furious-legacy-exact-gold-control.png'))
    p.evaluate('''()=>{sx21TargetPulseDraw=rpDraw;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');p.screenshot(path=str(O/'furious-corrected-exact-pulse.png'))
  row=p.evaluate('''()=>{const green={_target17Art:'sonic',_target17RazorFurious:false,_target17Age:.8,vx:0,vy:3},red={...green,_target17RazorFurious:true};const a=sx21TargetPulseGeometry(green),b=sx21TargetPulseGeometry(red);return{a,b};}''')
  ck('Furious pulse is1.5x the medium green pulse without using the global difficulty',row['b']['size']/row['a']['size']==1.5,row)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/sonic_effects_1021/index.html?scene=targetPulse&difficulty=furious&revision=razorback-pulse-1021');p.wait_for_function('!document.querySelector("#replay").disabled');g=p.frames[1];g.wait_for_function('eBullets.some(q=>q._target17Art==="sonic")')
  ck('Preview reaches the exact targeted attack',g.evaluate('eBullets.some(q=>q._target17Art==="sonic"&&q._target17RazorFurious)'))
  p.screenshot(path=str(O/'targeted-pulse-preview.png'))
  ck('No page console draw or asset errors',not errors,errors);b.close()

finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
