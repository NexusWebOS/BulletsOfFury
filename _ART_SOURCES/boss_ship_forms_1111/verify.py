from pathlib import Path
import sys,json,base64,subprocess,time,hashlib,io
from PIL import Image
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/Boss-ships-and-gun';V=O/'verification';V.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8');errors=[];checks=[];traces=[];requests=[];runtime_hash=hashlib.sha256((R/'assets/boss_ship_forms_1111.js').read_bytes()).hexdigest()
stages=json.loads((W/'verify-settings.json').read_text()).get('stages',[5,8]) if (W/'verify-settings.json').exists() else [5,8]
if stages==[8] and (V/'checks.json').exists():
 previous=json.loads((V/'checks.json').read_text());checks=[c for c in previous['checks']if c['name'].startswith(('Stage5','Chronos','Password','Approved three hammer'))];assert all(c['passed']for c in checks)
def ck(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS 'if value else'FAIL ')+name, ''if value else str(data)[:800],flush=True);(V/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,name):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(V/(name+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  for stage in stages:
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);context=br.new_context(viewport={'width':1280,'height':800});context.on('requestfailed',lambda r:requests.append(dict(url=r.url,failure=r.failure)));p=boot(context,port,stage,errors,'boss')
   p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()&&sf1111Warm(s)}',arg=stage,timeout=180000)
   p.evaluate("()=>{BOFCinematicDirector.cancel();window.B=boss;DBGT.god=true;player.invuln=1e9;B.enter=B._noHit=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+200;}")
   ck('Stage'+str(stage)+' all new lossless sheets load',p.evaluate('sf1111Warm('+str(stage)+')'))
   if stage==5:
    q=p.evaluate("""()=>{const h=B._hammer;h.c25Knock=h.hb20Pickup=h.throw=null;h._td1111Dir=h._td1111From='center';let out=[];for(const mat of ['regular','chrome']){h.frArmor={hp:mat==='regular'?0:900,max:900,activated:true,active:true,t:0,flash:0};for(const [s,t]of [['flyby',0],['unfold',0],['unfold',1],['unfold',2]]){hammerState(B,s);h.t=t;const q=ha21Blue(B);out.push({mat,state:s,t,bank:q?.a.bank,f:q?.a.frame,key:q?.a.key});}}return out;}""")
    ck('Chronos flyby and unfolding use new original ship in both materials',all(a['bank']=='chronus-transform'for a in q),q)
    for age,name in [(0,'closed'),(.85,'unfold'),(2,'ready')]:
     p.evaluate("t=>{B._hammer.frArmor.hp=0;hammerState(B,'unfold');B._hammer.t=t}",age);shot(p,'chronos-'+name)
    q=p.evaluate("""()=>{B._hammerTime={mode:'intro',musicStarted:true,shipFrame:15};const a=ha21Blue(B);B._hammerTime.shipFrame=6;const z=ha21Blue(B);B._hammerTime.mode='dance';const d=ha21Blue(B);delete B._hammerTime;return{start:a?.a.bank,first:a?.a.frame,end:z?.a.frame,dance:d};}""")
    ck('Password intro owns new ship and yields to existing dance',q['start']=='chronus-transform'and q['first']==0 and q['end']==23 and q['dance']is None,q)
    ck('Approved three hammer directions still registered',p.evaluate("['blue-overhead','blue-overhead-left','blue-overhead-right'].every(k=>BA119_ART[k].count===32)"))
    p.evaluate("""()=>{window.seed119=(diff,mat)=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);const b=B,h=b._hammer;b.enter=b._noHit=b.dead=false;b.maxhp=11220;b.hp=b.maxhp;b.x=worldWidth()/2;b.y=viewTopY()+210;b._drawY=b.y;b.flash=0;h.balance0922=true;h.ballSeen=h.whirlSeen=h.hb20PickupDone=true;h.mode='hammer';h.phaseTwo=false;h.hammerDestroyed=false;h.c27RagePending=false;h._hf22Red=false;h._hf22Charge=null;h.frArmor={hp:mat==='regular'?0:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]};h.recovery=h.c25Knock=h.hb20Pickup=h.c26Return=h.c27Combo=h.throw=null;h.c30=null;h.phasePending=false;h._hj22Pair=h._hf22StormPair=null;eBullets=[];pBullets=[];enemies=[];l5Rocks=[];powerups=[];player.x=worldWidth()/2;player.y=VH-110;h.tx=player.x;h.ty=player.y-32;hammerState(b,'warn');BA119.events=[];HF22.events=[];};}""")
    sys.path.insert(0,str(W.parent/'three_way_hammer_1111'));import verify_three_way as hammer_checks;hammer_checks.O=O;(O/'verification-stage5').mkdir(exist_ok=True);hammer_checks.run_three_way(p,5,ck,shot)
   else:
    p.evaluate("""()=>{v18Enter(B,2,8);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;window.Q=hb20State(B);window.seedSF=(chrome=false)=>{Q.rf1110=null;Q.rage=false;Q.chrome=chrome;Q.action=null;Q.cool=999;Q.pendingArsenal=Q.pendingGun=Q.pendingRecall=false;Q.gunHP=Q.parts[2].max||900;Q.gunHP=Math.max(Q.gunHP,900);Q.parts[2].hp=Q.gunHP;Q.parts[2].destroyed=true;Q.parts[2].flash=0;Q.sf1111={acquired:false,held:false,broken:false};B.hp=B.maxhp;B.flash=0;B._noHit=B.enter=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+190;eBullets=[];B._r30.mode='fight';B._r30.v18.donorAge=0;SF1111.events=[];RD74.events=[];};seedSF(false);}""")
    sys.path.insert(0,str(W.parent/'three_way_hammer_1111'));import verify_three_way as hammer_checks;hammer_checks.O=O;(O/'verification-stage8').mkdir(exist_ok=True);hammer_checks.run_three_way(p,8,ck,shot)
    # Observe the actual native boss-draw owner, not only the clip helper.
    q=p.evaluate("""()=>{const save=ctx.drawImage,S=B._r30,N=S.v18;let keys=[];ctx.drawImage=function(im,...args){const k=HA21.tags.get(im);if(k)keys.push(k);return save.call(this,im,...args)};try{for(const from of [0,8]){N.from=from;N.to=from===0?8:0;N.form=from;S.mode='v18formOut';for(const t of [0,1.45]){S.t=t;r30DrawBoss(B);}N.form=N.to;S.mode='v18formIn';for(const t of [0,1.6]){S.t=t;r30DrawBoss(B);}}}finally{ctx.drawImage=save;S.mode='fight';N.form=8;N.from=0;N.to=8;}return{keys,draws:SF1111.draws['draconus-transform']};}""")
    ck('Draconus actual morph in/out paints its distinct ship bank',q['draws']>=8 and len(q['keys'])>=8 and all('sf1111_draconus-transform_'in k for k in q['keys']),q)
    for chrome in [False,True]:
     for mode,age,name in [('v18formOut',0,'closed'),('v18formIn',.3,'unfold'),('v18formIn',1.6,'ready')]:
      p.evaluate("([c,m,t])=>{Q.chrome=c;B._r30.mode=m;B._r30.t=t;B._r30.v18.form=8;B._r30.v18.from=0;B._r30.v18.to=8}",[chrome,mode,age]);shot(p,'draconus-'+('chrome-'if chrome else'')+name)
    p.evaluate("B._r30.mode='fight'")
    for chrome in [False,True]:
     q=p.evaluate("""chrome=>{seedSF(chrome);const hp=B.hp,gunHP=Q.gunHP;hb20Start(B,'arsenal');const A=Q.action;let seen=new Set(),early=0,notes=[];for(let i=0;i<300&&Q.action===A;i++){v19NativeTick(B,1/60);seen.add(hb20Pose(B).a.bank);if(eBullets.length)early++;if(i%15===0)notes.push({t:A.t,bank:hb20Pose(B).a.bank,f:hb20Pose(B).a.frame,gunTarget:v19HammerRig(B).some(v=>v.p.id==='chaingun')});}return{hpSame:B.hp===hp,gunSame:Q.gunHP===gunHP,type:Q.action?.type,seen:[...seen],early,events:SF1111.events,notes};}""",chrome);traces.append(q)
     ck(('Chrome'if chrome else'Normal')+' icon-box strike→eject→catch order', [e['event']for e in q['events']][:5]==['icon-box-approach','icon-box-hit','hammer-release','gun-eject','gun-catch'],q['events'])
     ck(('Chrome'if chrome else'Normal')+' pickup has no shots or HP reset',q['early']==0 and q['hpSame']and q['gunSame']and q['type']=='gun',q)
     ck('Pickup uses empty-hand and complete held-gun drawings '+str(chrome),'draconus-catch-pre'in q['seen']and'draconus-catch-take'in q['seen'],q['seen'])
     q=p.evaluate("""()=>{const A=Q.action,hp=B.hp;let counts=[],mismatch=0,seen=new Set();for(let i=0;i<390&&Q.action===A;i++){const n=eBullets.length;v19NativeTick(B,1/60);const pose=hb20Pose(B);seen.add(pose.a.bank);if(eBullets.length>n){const m=rd74Point(B,pose,'muzzle');for(const bullet of eBullets.slice(n))if(Math.hypot(bullet.x-m.x,bullet.y-m.y)>.01)mismatch++;counts.push({t:A.t,shots:eBullets.length-n});}}return{counts,mismatch,seen:[...seen],hpSame:hp===B.hp,after:Q.action?.type,held:Q.sf1111.held,gunHP:Q.gunHP};}""");traces.append(q)
     ck('Gun fires only from actual muzzle during native active window '+str(chrome),len(q['counts'])>15 and q['mismatch']==0 and min(z['t']for z in q['counts'])>=1.2 and max(z['t']for z in q['counts'])<5.02,q)
     ck('Gun coasts, stows and returns to hammer without healing '+str(chrome),'draconus-gun-stow'in q['seen']and q['after']=='recall'and not q['held']and q['hpSame'],q)
    # Native pixels, not isolated source-sheet renders.
    p.evaluate("seedSF(false);efxClock+=2;GP4.clock+=2;hb20Start(B,'arsenal');Q.action.t=1.78");shot(p,'draconus-box-contact')
    ck('Visible box pixels touch the actual forward cap',p.evaluate("(()=>{const a=hb20Pose(B).a,box=sf1111Box(B),s=SF1111_ART['icon-box'];return a.frame===22&&Math.abs(box.y-s.pivot[1]+s.meta[0].bounds[1]-(B.y+a.tip[1]-256))<1&&Math.abs(box.x-B.x)<8})()"))
    p.evaluate('Q.action.t=3.30');shot(p,'draconus-gun-eject')
    p.evaluate('Q.action.t=3.80;Q.sf1111.acquired=Q.sf1111.held=true');shot(p,'draconus-gun-catch')
    p.evaluate("Q.action=null;hb20Start(B,'gun');Q.action.t=2.3;Q.action.muzzle=.08;Q.parts[2].destroyed=false");shot(p,'draconus-gun-fire')
    p.evaluate('Q.action.t=5.78;Q.action.muzzle=0');shot(p,'draconus-gun-stow')
    p.evaluate("Q.action.t=2.3;Q.chrome=true");shot(p,'draconus-chrome-gun')
    q=p.evaluate("""()=>{seedSF(true);Q.sf1111.acquired=Q.sf1111.held=true;hb20Start(B,'gun');Q.action.t=2;Q.parts[2].destroyed=false;const rig=v19HammerRig(B),gun=rig.find(v=>v.p.id==='chaingun'),a=gun.a;let point;for(let y=a.gunBounds[3]-20;y>a.gunBounds[1];y--){const spans=a.spans[y];if(spans?.length){point={x:B.x+(spans[0]+spans[1])/2-256,y:B.y+y-256};break;}}const contains=v19AtRect(gun,point.x,point.y),hp=B.hp,ghp=Q.gunHP;B._lastPart=Q.parts[2];modularHit(17);return{contains,hpSame:hp===B.hp,gunLost:ghp-Q.gunHP,flash:Q.parts[2].flash,point,rig:rig.map(v=>({id:v.p.id,role:v.spec.role,spans:!!v.a.spans}))};}""")
    ck('Gun has independent native pixel target and HP',q['contains']and q['hpSame']and q['gunLost']==17 and q['flash']>0,q)
    shot(p,'draconus-gun-white-hit')
    q=p.evaluate("""()=>{for(let i=0;i<16;i++)updateBoss(1/60);const expired=Q.parts[2].flash<=0,hp=B.hp,g=Q.gunHP;B._lastPart=Q.parts[0];modularHit(5);return{expired,coreLost:hp-B.hp,gunSame:g===Q.gunHP};}""")
    ck('Gun flash expires and core damage keeps its own pool',q['expired']and q['coreLost']==5 and q['gunSame'],q)
    q=p.evaluate("""()=>{const hp=B.hp;B._lastPart=Q.parts[2];modularHit(Q.gunHP+1);const A=Q.action,n=RD74.events.filter(e=>e.event==='gun-volley').length;for(let i=0;i<70;i++)v19NativeTick(B,1/60);const after=Q.action?.type;hb20Start(B,'gun');return{hpSame:B.hp===hp,broken:Q.sf1111.broken,gHP:Q.gunHP,type:A.type,after,retry:Q.action.type,extra:RD74.events.filter(e=>e.event==='gun-volley').length-n,events:SF1111.events};}""")
    ck('Destroyed gun drops once, stops firing, recalls hammer and never respawns',q['hpSame']and q['broken']and q['gHP']==0 and q['type']=='sf1111_break'and q['after']=='recall'and q['retry']=='side'and q['extra']==0,q)
    q=p.evaluate("""()=>{seedSF(false);Q.sf1111.acquired=Q.sf1111.held=true;Q.gunHP=321;hb20Start(B,'armor');const A=Q.action;let keys=new Set();for(let i=0;i<260&&Q.action===A;i++){v19NativeTick(B,1/60);keys.add(hb20Pose(B).a.key);}Q.cool=0;hb20Start(B);return{gunHP:Q.gunHP,held:Q.sf1111.held,chrome:Q.chrome,type:Q.action.type,box:SF1111.events.some(e=>e.event==='icon-box-approach'),keys:[...keys]};}""")
    ck('Chromium activation retains held gun and damage budget',q['gunHP']==321 and q['held']and q['chrome']and q['type']=='gun'and not q['box'],q)
    ck('Copied hammer directions and rage remain registered',p.evaluate("['corrupt-overhead','corrupt-overhead-left','corrupt-overhead-right'].every(k=>BA119_ART[k].count===32)&&typeof rf1110DracStart==='function'"))
    # Bounded real game-loop capture: normal input, bullets, FX clocks and native
    # action handoffs stay live. No recorder or replacement actor renderer.
    p.evaluate("()=>{const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};DBGT.god=true;player.invuln=1e9;}")
    for chrome in [False,True]:
     p.evaluate("c=>{seedSF(c);Q.opening=true;Q.speech=null;diffKey='normal';DIFF=difficultyForRun(run.mode,diffKey);hb20Start(B,'arsenal')}",chrome);frames=[];seen=set()
     for k in range(144):
      err=p.evaluate(STEP,5)
      if err:raise RuntimeError(err)
      seen.add(p.evaluate('Q.action?.type||"ready"'))
      data=p.screenshot();im=Image.open(io.BytesIO(data)).convert('RGB').crop((265,0,1015,800)).resize((480,512),Image.Resampling.NEAREST);frames.append(im)
      if k%36==0:print('Capturing native gun handoff',chrome,k,flush=True)
     path=O/('draconus-'+('chromium'if chrome else'normal')+'-native.gif');frames[0].save(path,save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=False)
     ck('Real native loop completes pickup/fire/stow/recall '+str(chrome),{'sf1111_arsenal','gun','recall','ready'}.issubset(seen),sorted(seen))
    p.evaluate('v18Clear(B)');ck('Native exit clears temporary gun handoff',p.evaluate('!Q.sf1111'))
   ck('Stage'+str(stage)+' browser has no renderer exceptions',not [e for e in errors if 'Failed to load resource:'not in e],errors);br.close()
finally:stop()
(V/'traces.json').write_text(json.dumps(traces,indent=2));(V/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,requests=requests,runtimeHash=runtime_hash),indent=2));assert runtime_hash==hashlib.sha256((R/'assets/boss_ship_forms_1111.js').read_bytes()).hexdigest();print(json.dumps(dict(total=len(checks),failed=[c['name']for c in checks if not c['passed']],errors=errors,requests=requests)),flush=True)
if any(not c['passed']for c in checks):raise SystemExit(1)
