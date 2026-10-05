"""Every selected mutant/alien uses the original warning pixels, without a boss.
Controlled Chromium rendering fixtures; not full campaign or balance certification.
"""
from pathlib import Path
import base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/enemy_warnings_1003f';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'scenes':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.add_init_script('(()=>{for(const k of ["fillRect","drawImage"]){const f=CanvasRenderingContext2D.prototype[k];CanvasRenderingContext2D.prototype[k]=function(){if(window.ewKey&&typeof ctx!=="undefined"&&this===ctx)ewDraws.push(ewKey);return f.apply(this,arguments);};}})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate('''()=>{
   window.ewDraws=[];window.ewKey=null;window.ewCalls=[];window.ewWarm=[];
   const ready=XART.rdy;XART.rdy=function(k){ewWarm.push(k);return ready.apply(this,arguments);};
   const warn=combatWarningDraw;combatWarningDraw=function(owner,q){ewCalls.push({enemy:enemies.includes(owner),owner:owner?.type,q});return warn.apply(this,arguments);};
   const band=s67LaneBand;s67LaneBand=function(x,y,ex,ey,w,k){ewKey='band-'+s67LanePhase(k);try{return band.apply(this,arguments);}finally{ewKey=null;}};
   const ret=groundTargetReticleDraw;groundTargetReticleDraw=function(x,y,w,k){ewKey='retina-'+(k<.5?'green':k<.78?'yellow':'red');try{return ret.apply(this,arguments);}finally{ewKey=null;}};
   const fov=l23FovDraw;l23FovDraw=function(){ewKey='boss-fov';try{return fov.apply(this,arguments);}finally{ewKey=null;}};
   const alert=l23WarnSymbolDraw;l23WarnSymbolDraw=function(){ewKey='boss-alert';try{return alert.apply(this,arguments);}finally{ewKey=null;}};
   const cell=s81003Cell;s81003Cell=function(name,frame){if(name==='fov'&&frame<8)ewDraws.push('retired-warning');return cell.apply(this,arguments);};
  }''')
  p.evaluate(SETUP,{'stage':7})
  ck(p.evaluate('()=>!boss&&["hammer_reticle","fx_ground_target_reticle","bmfx_fov_green_tall","bmfx_fov_yellow_tall","bmfx_fov_red_tall"].every(k=>ewWarm.includes(k))'),'Stage 7 entry warms original warning/Retina assets without spawning a boss')
  p.wait_for_function('()=>["hammer_reticle","fx_ground_target_reticle",...Object.values(MM1003_ART).map(a=>a.key),...Object.values(S81003_ART).map(a=>a.key)].every(k=>XART.rdy(k))',timeout=120000,polling=60)
  kinds=p.evaluate('()=>Object.keys(MM1003_DEF)')
  for diff in ['normal','furious']:
   for kind in kinds:
    stage=7 if kind in ['hellram','riflelocust','hellhugger','hexpyre','impharrow'] else 8
    p.evaluate(SETUP,{'stage':stage,'diff':diff})
    p.evaluate('(kind)=>{window.E=spawnEnemy("mm1003_"+kind,player.x,145,{});mm1003Warning(E);window.ewLane=JSON.stringify(E._mm1003.lane);}',kind)
    states=[]
    for progress,color in [(.2,'green'),(.6,'yellow'),(.9,'red')]:
     p.evaluate('(k)=>{const A=E._mm1003;A.age=A.warm*k;for(const q of groundTargetingFx)q.t=q.warn*k;ewDraws=[];ewCalls=[];}',progress)
     if diff=='normal':shot(p,kind+'-'+color)
     else:p.evaluate('()=>drawWorld(0)')
     states.append(p.evaluate('()=>({keys:[...new Set(ewDraws)],owners:ewCalls.filter(q=>q.owner===E.type),stable:JSON.stringify(E._mm1003.lane)===ewLane})'))
    report['scenes'].append({'kind':kind,'diff':diff,'stage':stage,'states':states})
    clean=all(not any(k in s['keys'] for k in ['retired-warning','boss-alert','boss-fov']) and s['stable'] for s in states)
    expected=['green','yellow','red']
    if kind=='hexpyre':valid=all('retina-'+c in s['keys'] for s,c in zip(states,expected))
    else:valid=all('band-'+c in s['keys'] and s['owners'] and all(q['enemy'] for q in s['owners']) for s,c in zip(states,expected))
    if kind in ['hellram','hellhugger']:valid=valid and all('retina-'+c in s['keys'] for s,c in zip(states,expected))
    ck(clean and valid,diff+' '+kind+' draws all original warning phases with committed geometry')
   for role in ['stalker','prism','gravity']:
    p.evaluate(SETUP,{'stage':8,'diff':diff})
    p.evaluate('(role)=>{window.E=spawnEnemy("s8"+role+"1003",player.x,140,{});const A=E._orbit1003;A.phase="tell";A.warm=1;A.lanes=s81003EnemyLanes(E,A);}',role)
    valid=True
    for progress,color in [(.2,'green'),(.6,'yellow'),(.9,'red')]:
     p.evaluate('(k)=>{E._orbit1003.age=k;ewDraws=[];ewCalls=[];}',progress)
     if diff=='normal':shot(p,role+'-'+color)
     else:p.evaluate('()=>drawWorld(0)')
     valid=valid and p.evaluate('(c)=>ewDraws.includes("band-"+c)&&!ewDraws.some(k=>["boss-fov","boss-alert","retired-warning"].includes(k))&&ewCalls.length>0&&ewCalls.every(q=>q.enemy)',color)
    ck(valid,diff+' '+role+' alien uses original enemy lanes in all three phases')
  # Owner routing must remain correct even if a boss is on screen at the same time.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{window.E=spawnEnemy("mm1003_hellram",player.x,180,{});mm1003Warning(E);E._mm1003.age=E._mm1003.warm*.9;ewDraws=[];ewCalls=[];drawEnemy(E);}')
  ck(p.evaluate('()=>ewCalls.length===1&&ewCalls[0].enemy&&ewDraws.includes("band-red")&&!ewDraws.includes("boss-fov")'),'mutant warning belongs to its emitter when the finale boss is also alive')
  for stage in [7,8]:
   p.evaluate(SETUP,{'stage':stage})
   q=p.evaluate('(stage)=>{enemies=[];for(const w of buildStagePlan(stage))w.fn();return {mutants:[...new Set(enemies.map(e=>e._mutator1003).filter(Boolean))],aliens:[...new Set(enemies.map(e=>e._alien1003).filter(Boolean))]};}',stage)
   report['roster'+str(stage)]=q;ck(len(q['mutants'])==(5 if stage==7 else 4) and (stage==7 or len(q['aliens'])==3),'actual Stage '+str(stage)+' spawn plan retains the corrected enemy roster')
  report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
