"""Real Chromium integration fixtures. Inspect native art, motion, locks and damage.
Not a campaign completion or final difficulty certification.
"""
from pathlib import Path
import json,sys,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/mutator_gameplay_1003';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];report={'checks':[],'scenes':[],'scope':'Controlled real game fixtures; not campaign wins or final balance.'}
def ck(value,name):
 report['checks'].append({'ok':bool(value),'name':name});print(('OK ' if value else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,20):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1100,'height':950});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50);p.mouse.click(500,500)
  p.evaluate('()=>{mm1003Warm();window.realMutatorHit1003=playerHit;window.probeMutatorSound={};window.realMutatorSound1003=r30Sound;r30Sound=function(k){probeMutatorSound[k]=(probeMutatorSound[k]||0)+1;return realMutatorSound1003.apply(this,arguments);};}')
  p.wait_for_function('()=>Object.values(MM1003_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))',timeout=120000,polling=60)
  ck(p.evaluate('()=>Object.values(MM1003_ART).every(a=>{const im=XART.get(a.key);return im.width===a.size[0]&&im.height===a.size[1];})'),'all ten authored sheets resolve through registered XART keys')
  kinds=p.evaluate('()=>Object.keys(MM1003_DEF)')
  for diff in ['normal','hard','furious']:
   for kind in kinds:
    stage=7 if kind in ['hellram','riflelocust','hellhugger'] else 8
    p.evaluate(SETUP,{'stage':stage,'diff':diff})
    p.evaluate('(kind)=>{playerHit=function(){};player.invuln=0;window.E=spawnEnemy("mm1003_"+kind,player.x,120,{});E._mm1003.homeY=130;window.mmShotPeak=0;window.mmGroundPeak=0;window.mmAngles=[];window.mmPhases=[];window.mmMoves=[];window.mmLast={x:E.x,y:E.y};}',kind)
    captured=[]
    for j in range(100):
     frames(p,6)
     q=p.evaluate('()=>{mmShotPeak=Math.max(mmShotPeak,eBullets.filter(q=>q._mutatorShot1003).length);mmGroundPeak=Math.max(mmGroundPeak,groundTargetingFx.filter(q=>q.owner===E).length);mmAngles.push(E.spin);mmMoves.push(Math.hypot(E.x-mmLast.x,E.y-mmLast.y));mmLast={x:E.x,y:E.y};return {phase:E._mm1003.phase,dead:E.dead};}')
     if q['phase'] not in captured:
      captured.append(q['phase'])
      if diff=='hard' and q['phase'] in ['rest','tell','fire','dash','recover']:shot(p,kind+'-'+q['phase'])
     if q.get('dead'):break
    q=p.evaluate('()=>({kind:E._mutator1003,shots:mmShotPeak,ground:mmGroundPeak,straight:mmAngles.every(a=>a===0),finite:Number.isFinite(E.x+E.y),phases:[...new Set(E._mm1003.history.map(q=>q.phase))],maxStep:Math.max(...mmMoves)})')
    report['scenes'].append({'diff':diff,**q})
    ck(q['straight'] and q['finite'],diff+' '+kind+' stays upright in native movement')
    ck('tell' in q['phases'] and 'recover' in q['phases'],diff+' '+kind+' completes warning and recovery')
    ck(q['ground']>0 if kind=='hexpyre' else 'dash' in q['phases'] if kind=='hellhugger' else q['shots']>0,diff+' '+kind+' releases a native attack')
  # Real authored wave callbacks must contain every selected candidate and retain aliens.
  for stage in [7,8]:
   p.evaluate(SETUP,{'stage':stage});q=p.evaluate('(stage)=>{enemies=[];for(const w of buildStagePlan(stage))w.fn();return {selected:[...new Set(enemies.map(e=>e._mutator1003).filter(Boolean))],aliens:[...new Set(enemies.map(e=>e._alien1003).filter(Boolean))]};}',stage)
   ck(len(q['selected'])==(5 if stage==7 else 4),'actual Stage '+str(stage)+' wave plan contains its selected enemies')
   if stage==8:ck(len(q['aliens'])==3,'existing gravity, Retina and code laser aliens remain in Stage8')
  # Native drawImage calls on the game context are the evidence, never Image.src or identity.
  p.evaluate(SETUP,{'stage':7});p.evaluate('()=>{window.E=spawnEnemy("mm1003_riflelocust",player.x,140,{});E._mm1003.phase="rest";window.mmKeys=[];const blit=mm1003Blit,draw=ctx.drawImage;window.mmProbeKey=null;mm1003Blit=function(k){mmProbeKey=k;try{return blit.apply(this,arguments);}finally{mmProbeKey=null;}};ctx.drawImage=function(){if(mmProbeKey)mmKeys.push(mmProbeKey);return draw.apply(this,arguments);};drawWorld(0);ctx.drawImage=draw;mm1003Blit=blit;}')
  ck(p.evaluate('()=>mmKeys.filter(k=>k==="mm1003_riflelocust_parts").length===5'),'game draws five independent Rifle Locust components')
  p.evaluate('()=>{const gun=E._mm1003.parts.find(p=>p.kind==="gun");window.mt=mm1003Target(E,gun);window.partHP=gun.hp;window.bodyHP=E.hp;run.bombs=20;run.missileTier="standard";window.launched=useBomb(mt);}')
  frames(p,180);q=p.evaluate('()=>({launched,part:mt.hp,old:partHP,hull:E.hp,oldHull:bodyHP,dead:mt.dead,valid:_lockTargets().includes(mt)})');report['missile']=q
  ck(q['launched'] and q['part']<q['old'],'actual curved Retina missile hits the rifle module')
  p.evaluate('()=>{for(let i=0;i<3&&!mt.dead;i++)retinaMissileDamage(mt,99,{kind:"gmiss"});}')
  shot(p,'riflelocust-module-break');ck(p.evaluate('()=>mt.dead&&!_lockTargets().includes(mt)&&E.hp===bodyHP'),'rifle detaches without silently damaging the hull')
  # Ordinary forward shot reaches core through native collision/update loop.
  p.evaluate('()=>{E._mm1003.phase="tell";E._mm1003.warm=10;E._mm1003.age=0;E._mm1003.lane=s81003Lane(E.x,E.y,player.x,player.y);window.beforeCore=E.hp;pBullets.push({kind:"mg",x:E.x,y:E.y+1,vx:0,vy:0,w:5,h:12,dmg:3,t:0});}')
  frames(p,2);ck(p.evaluate('()=>E.hp<beforeCore'),'ordinary weapon shots damage the real hull');shot(p,'riflelocust-hit-flash')
  # Live Hammer arrival from incoming build, with local choreography and no second scene.
  p.evaluate(SETUP,{'stage':5,'kind':'chromehammer'});p.evaluate('()=>{B._hammer.state="unfold";B._hammer.t=1.95;fb2IntroStart(B);window.introScroll=mapScroll;playerHit=realMutatorHit1003;player.invuln=999;}');frames(p,15)
  ck(p.evaluate('()=>fb2IntroActive()&&!BOFCinematicDirector.live&&B._hammer.intro1002'),'incoming live Hammer dialogue suppresses the duplicate paused scene')
  shot(p,'integrated-hammer-intro');p.evaluate('()=>fb2IntroEnd()');frames(p,1)
  ck(p.evaluate('()=>!B._noHit&&B._hammer.state==="warn"&&!BOFCinematicDirector.live'),'live dialogue releases into the requested opening jump')
  ck(p.evaluate('()=>typeof fb2Flights!=="undefined"&&FB2_BEAM.key==="fb2_fusion_beam"&&typeof FB1002_ART!=="undefined"&&typeof hamaRecordedVocals1001==="function"'),'incoming stealth/fusion layers coexist with local encounter assets and recorded HAMA')
  report['sounds']=p.evaluate('()=>probeMutatorSound');ck(report['sounds'].get('bossWeaponCharge',0)>0 and report['sounds'].get('combatOrb0927',0)>0,'warnings and projectile releases invoke native sound cues')
  report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}),flush=True);b.close()
finally:stop()
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
