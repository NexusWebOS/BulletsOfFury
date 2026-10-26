"""Native Chromium frame pixels, physical landmarks and complete depth chronology."""
from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_motion_1025/probe';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000)
  p.evaluate("""()=>{window.seedMotion=(chrome=true)=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=260;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h._hf22Charge=h._hj22Pair=h._hf22StormPair=null;h.hammerDestroyed=false;h._hf22Red=false;h.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]}:null;debugUnlocked=true;DBGT.god=true;player.invuln=0;player.x=320;player.y=430;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedMotion();}""")
  # Every delivered frame must decode and paint actual nonempty native pixels.
  banks=p.evaluate('Object.keys(C27_ART.banks)');stats=[]
  for bank in banks:
   p.wait_for_function("bank=>C27_ART.banks[bank]&&Array.from({length:C27_ART.banks[bank].count},(_,f)=>{const a=c27Row(bank,f);return XART.rdy(a.key)&&XART.rdy(a.white)}).every(Boolean)",arg=bank,timeout=90000)
   s=p.evaluate("""bank=>{const a=C27_ART.banks[bank],out=[];for(let f=0;f<a.count;f++){const row=c27Row(bank,f);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);b20Image(row,cv.width/2,cv.height/2,.7,0,0);let n=0;const data=ctx.getImageData(0,0,cv.width,cv.height).data;for(let i=3;i<data.length;i+=4)if(data[i]>32)n++;ctx.restore();out.push(n)}return{bank,frames:a.count,minPixels:Math.min(...out),even:a.cell.every(v=>v%2===0),bounds:a.frames.map(f=>f.bounds)}}""",bank);stats.append(s);p.wait_for_timeout(5)
  ck('All 445 complete PixelLab-derived frames decode and paint real pixels on even cells',sum(s['frames'] for s in stats)==445 and all(s['minPixels']>700 and s['even'] for s in stats),[{k:s[k] for k in ['bank','frames','minPixels']} for s in stats])
  ck('Every hammer and aura remains within the common padded canvas',all(all(v>=2 for v in b[:2]) and all(v<=C for v in b[2:]) for s in stats for b in s['bounds'] for C in [448*512/342-2]),None)
  contact=Image.new('RGB',(1280,340*4),'#091320');d=ImageDraw.Draw(contact)
  for lane,chrome in enumerate([False,True]):
   mat='chrome' if chrome else 'regular';p.evaluate('v=>seedMotion(v)',chrome)
   for i,(bank,u)in enumerate([('takeoff',0),('left',1),('right',1),('aura',.75)]):
    p.evaluate("([bank,u])=>{boss._hammer.state=bank==='left'||bank==='right'?'hammer':'hammer';const q=c27Pose(boss,bank,u);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ha21Body(boss,q);}",[bank,u])
    data=p.evaluate("cv.toDataURL('image/png').split(',')[1]");f=O/(mat+'-'+bank+'.png');f.write_bytes(base64.b64decode(data));im=Image.open(f).convert('RGBA');small=Image.new('RGBA',im.size,'#091320');small.alpha_composite(im);contact.paste(small.convert('RGB').resize((640,320)),(lane*640,i*340));d.text((lane*640+8,i*340+322),mat+' '+bank,fill='white')
   r=p.evaluate("""()=>{const mat=c26Material(boss),g=c27Row('takeoff_'+mat,0),l=c27Row('left_'+mat,16),r=c27Row('right_'+mat,16);return{guard:g.tip,grip:g.grip,pivot:g.pivot,left:l.tip,right:r.tip,reach:Math.hypot(g.tip[0]-g.grip[0],g.tip[1]-g.grip[1])}}""")
   ck(mat+' side guard keeps one hand low with the unchanged hammer extended outward',r['guard'][0]<r['grip'][0]-100 and r['grip'][1]>r['pivot'][1] and 120<r['reach']<130,r)
   ck(mat+' opposite whole-body twists produce opposite physical hammer strikes',r['left'][0]<r['right'][0]-100,r)
  contact.save(O/'native-motion-contact.png')
  # One checkpoint starts the native sequence; every later state is reached by actual ticks.
  p.evaluate("()=>{seedMotion();boss._hammer.giantLeft=1;hammerState(boss,'giant_idle');C27.events.length=0;window.depthSamples=[];window.depthWarnings=0;const w=combatWarningDraw;combatWarningDraw=function(o,q){if(c25Depth(boss))depthWarnings++;return w.apply(this,arguments)};}")
  states=[];shots=set()
  for i in range(430):
   p.evaluate(STEP,1);r=p.evaluate("()=>{const b=boss,q=ha21Blue(b);return{state:b._hammer.state,t:b._hammer.t,x:b.x,y:b.y,k:q?.k,key:q?.a.key,top:q?b.y+(q.a.bounds[1]-q.a.pivot[1])*q.k:null,bottom:q?b.y+(q.a.bounds[3]-q.a.pivot[1])*q.k:null}}")
   states.append(r)
   if r['state'] not in shots:
    shots.add(r['state']);p.screenshot(path=str(O/('depth-'+r['state']+'.png')))
   if i>60 and r['state']=='hammer':break
   if i%15==0:p.wait_for_timeout(3)
  order=[]
  for s in states:
   if not order or order[-1]!=s['state']:order.append(s['state'])
  required=['giant_idle','giant_windup','giant_rise','giant_bg_drop','giant_bg_land','giant_bg_jump','giant_warn','giant_dive','giant_sweep','giant_recover','hammer']
  ck('Native jump route exits, drops into background, lands, jumps again, winds up and strikes in order',order==required,order)
  rise=[s for s in states if s['state']=='giant_rise'];drop=[s for s in states if s['state']=='giant_bg_drop'];jump=[s for s in states if s['state']=='giant_bg_jump']
  ck('Full-size actor exits completely before small top-of-screen background reentry',rise and drop and all(s['k']==1 for s in rise) and rise[-1]['bottom']<0 and drop[0]['bottom']<0 and all(s['k']==.36 for s in drop) and drop[-1]['y']>drop[0]['y']+250,dict(riseEnd=rise[-1] if rise else None,dropStart=drop[0] if drop else None))
  ck('Second background jump has real windup frames and upward travel',len(set(s['key'] for s in jump))>=12 and jump[0]['y']-jump[-1]['y']>50,dict(keys=len(set(s['key'] for s in jump))))
  ck('Depth attack reaches the committed ship with its displayed head',p.evaluate("C27.events.some(q=>q.state==='giant_sweep')"))
  # Explicit shield/counter checkpoint verifies foreground ownership and native white damaged pixels.
  p.evaluate("()=>{seedMotion();fr27Restore(boss,.1,false,true);boss.y=boss._hammer.c25ChargeY;boss._drawY=boss.y;boss._hammer.t=1.6;drawWorld(0);}")
  p.screenshot(path=str(O/'shield-charge.png'));r=p.evaluate('()=>({key:ha21Blue(boss).a.key,objective:C26.objective,head:hammerHeadPoint(boss),open:c25Counter(boss)})')
  ck('Counter head and SHOOT stay visible above the unchanged side-held hammer',r['open'] and r['key']=='c27_palm_chrome_16' and r['objective']['bottom']<=r['objective']['hammerTop']-8,r)
  n=p.evaluate("""()=>{boss.flash=0;boss._gp4FlashNext=0;drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(boss);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)n++;return n;}""");ck('New complete material plate visibly flashes on real damaged pixels',n>100,n)
  p.evaluate(STEP,20);ck('New material hit flash expires',p.evaluate('boss.flash<=0'))
  ck('No Chromium page or console errors',not errors,errors);br.close()
finally:stop()
result=dict(checks=checks,errors=errors,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks));(O/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(passed=result['passed'],failed=result['failed'])),flush=True);raise SystemExit(0 if not result['failed'] else 1)
