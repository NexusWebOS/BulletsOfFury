"""Native Sovereign generator, camera and electrical-art fixtures, not full clears."""
from pathlib import Path
import sys,ast,json,base64,argparse
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot as sh
ap=argparse.ArgumentParser();ap.add_argument('--browser',default='msedge');args=ap.parse_args()
O=R/'_shots/s4_core_access_1013'/args.browser;O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
report={'checks':[],'cameraSamples':[],'attacks':[],'browser':args.browser,'scope':'Protected native fixtures across four difficulties, not complete human fight clears.'};errors=[]
def check(value,name):
 report['checks'].append({'ok':bool(value),'name':name});print(('OK ' if value else 'FAIL ')+name,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel=args.browser,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.wait_for_function('()=>typeof S4AC13!=="undefined"',timeout=10000)
  p.evaluate('()=>{fb1002Warm();er26Warm();missionWarm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);for(let i=0;i<16;i++)XART.rdy("s4w_lightning_ball_"+i);XART.rdy("efx_burst_lightning");}')
  p.wait_for_function('()=>Object.values(FB1002_ART).every(a=>XART.rdy(a.key))&&XART.rdy("mr27_storm")&&Array.from({length:16},(_,i)=>XART.rdy("s4w_lightning_ball_"+i)).every(Boolean)',timeout=120000)
  p.evaluate('''()=>{window.s4DrawKeys=[];window.s4DrawRecord=false;window.s4LastKey=null;
   const get=XART.get;XART.get=function(k){const out=get.apply(this,arguments);if(s4DrawRecord)s4LastKey=k;return out;};
   const draw=ctx.drawImage;ctx.drawImage=function(){if(s4DrawRecord)s4DrawKeys.push(s4LastKey);return draw.apply(this,arguments);};
  }''')
  def setup(diff):
   p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','diff':diff})
   p.evaluate('()=>{B._phaseInvuln=0;B._drawY=B.y;B._er26.engaged=false;B._er26.neutralOpening=false;B.flash=0;B._s4war.shield.nodes.forEach(n=>n.materialize=1);er26Tick(B,0);stage4ShieldSyncNodes(B);player.invuln=1e9+2;story=fb2Talk=null;}')
  def frames(n):
   for start in range(0,n,30):
    p.evaluate('(n)=>{for(let j=0;j<n;j++){story=fb2Talk=null;BOFCinematicDirector.cancel();updatePlay(1/60);}}',min(30,n-start));p.wait_for_timeout(8)
  def shot(name):
   p.evaluate('()=>{shake=0;flashScreen=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   for x in [80,340,600]:
    data=p.evaluate('''x=>{player.x=x;for(let i=0;i<240;i++){updateCamX();er26Tick(B,1/60);}stage4ShieldSyncNodes(B);
     const H=B._s4war.shield,ts=retinaBossTargets(B);return {x,view:[camLeftX(),camRightX()],boss:[B.x,B.y],nodes:H.nodes.map(n=>({x:n.x,y:n.y,dx:Math.abs(n.x-B.x),valid:ts.some(t=>t.part===n&&retinaTargetValid(t)),point:bossHitTest(n.x,n.y)&&B._s4ShieldHit===n})),shieldR:B.w*.67};}''',x)
    report['cameraSamples'].append({'difficulty':diff,**data})
    check(all(n['dx']>=data['shieldR']+25 for n in data['nodes']),f'{diff} pan{x}: every core outside hull and field approach')
    check(all(n['valid'] and n['point'] for n in data['nodes']),f'{diff} pan{x}: all four native Retina/point targets resolve to their core')
    check(all(n['x']-27>=data['view'][0] and n['x']+27<=data['view'][1] for n in data['nodes']),f'{diff} pan{x}: settled formation fully visible')
    result=p.evaluate('''()=>{eBullets=[];const H=B._s4war.shield;let ok=true;for(const n of H.nodes){
     const hp=n.hp,hull=B.hp,light=mr27Part(B,'lightning').hp;B._phaseInvuln=0;B.flash=0;
     pBullets.push({kind:'mg',x:n.x,y:n.y+14,vx:0,vy:-4,w:5,h:12,dmg:2,t:0});updatePlay(1/60);pBullets=[];
     ok=ok&&n.hp<hp&&B.hp===hull&&mr27Part(B,'lightning').hp===light&&!(mr27Part(B,'lightning').flash>0);
    }return ok;}''')
    check(result,f'{diff} pan{x}: real bullets damage each core, never hull/middle weapon')
    if x in [80,600]:shot(diff+'-pan-'+str(x))
   setup(diff)
   motion=p.evaluate('''()=>{let minimum=Infinity,valid=true,point=true,maxStep=0;const H=B._s4war.shield;let old=H.nodes.map(n=>({x:n.x,y:n.y}));
    for(let i=0;i<720;i++){player.x=340+Math.sin(i/100)*225;updatePlay(1/60);const ts=retinaBossTargets(B);
     for(let j=0;j<H.nodes.length;j++){const n=H.nodes[j];minimum=Math.min(minimum,Math.abs(n.x-B.x)-B.w*.67);
      valid=valid&&ts.some(t=>t.part===n&&retinaTargetValid(t));point=point&&bossHitTest(n.x,n.y)&&B._s4ShieldHit===n;
      maxStep=Math.max(maxStep,Math.hypot(n.x-old[j].x,n.y-old[j].y));}old=H.nodes.map(n=>({x:n.x,y:n.y}));
    }return {minimum,valid,point,maxStep};}''')
   report.setdefault('continuousMotion',[]).append({'difficulty':diff,**motion})
   check(motion['minimum']>=25 and motion['valid'] and motion['point'],diff+' continuous native 12-second camera sweep preserves every core lane and target')
   check(motion['maxStep']<8,diff+' live generator motion remains smooth without target teleports')
   setup(diff)
   p.evaluate('''()=>{window.missileNode=B._s4war.shield.nodes[1];window.missileTarget=retinaBossTargets(B).find(t=>t.part===missileNode);window.beforeMissile=missileNode.hp;
    run.bombs=20;run.missileTier='standard';player.x=worldWidth()/2;window.realLaunched=useBomb(missileTarget);}''')
   frames(180)
   check(p.evaluate('()=>realLaunched&&missileNode.hp<beforeMissile'),diff+' launched curved Retina missile reaches an upper core')
   setup(diff)
   p.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.5);B._s4war.coreTurrets.forEach(d=>{d._mrOwner=B;d.materialize=1;Object.assign(d,stage4CoreTurretTarget(B,d.side));});}')
   check(p.evaluate('()=>B._s4war.shield.nodes.every(n=>!stage4CoreTurretAt(B,n.x,n.y,2)&&bossHitTest(n.x,n.y)&&B._s4ShieldHit===n)'),diff+' helpers cannot mask a core collider')
   check(p.evaluate('()=>B._s4war.shield.nodes.every(n=>B._s4war.coreTurrets.every(d=>Math.abs(n.y-d.y)>=27+48))'),diff+' helper hulls sit in the gap between core images')
   shot(diff+'-helpers-clear-cores')
   setup(diff)
   beam=p.evaluate('''()=>{const H=B._s4war.shield;window.oldTarget=retinaBossTargets(B).find(t=>t.part===H.nodes[0]);
    const h=B.hp,light=mr27Part(B,'lightning').hp;player.x=H.nodes[0].x;player.y=VH-80;
    pBullets.push({kind:'beam',x:player.x,y:player.y,w:26,h:600,dmg:Math.max(...H.nodes.map(n=>n.hp))+1,life:.2,_hit:[],_bt:0});updatePlay(1/60);pBullets=[];
    return {ok:H.nodes.filter(n=>n.side<0).every(n=>n.dead)&&H.nodes.filter(n=>n.side>0).every(n=>!n.dead)&&B.hp===h&&mr27Part(B,'lightning').hp===light,nodes:H.nodes.map(n=>({hp:n.hp,dead:n.dead,x:n.x,y:n.y})),bx:B.x,px:player.x,boss:B.hp,h,light:mr27Part(B,'lightning').hp,beforeLight:light};}''')
   report.setdefault('beam',[]).append({'diff':diff,**beam});print(json.dumps(beam),flush=True);check(beam['ok'],diff+' native beam destroys both selected-column cores only')
   check(p.evaluate('()=>!retinaTargetValid(oldTarget)&&retinaMissileDamage(oldTarget,999,{kind:"gmiss"})===false'),diff+' destroyed core rejects stale locks and damage')
   for threshold in [.75,.5]:
    p.evaluate('()=>{B._s4war.shield.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));}')
    check(p.evaluate('''v=>{const yes=stage4ShieldBeginRearm(B,v);return yes&&B._s4war.shield.rearming&&!retinaBossTargets(B).some(t=>t.kind==='electrical node');}''',threshold),diff+f' {threshold} rearm has no premature core targets')
    p.evaluate('()=>{stage4ShieldTick(B,1.1);stage4ShieldSyncNodes(B);}')
    check(p.evaluate('()=>B._s4war.shield.nodes.every(n=>!n.dead&&n.materialize===1)&&retinaBossTargets(B).filter(t=>t.kind==="electrical node").length===4'),diff+f' {threshold} rearm restores four real visible targets')
   setup(diff)
   for mode in ['p2-core-balls','ap10-stormburst','pt11-chase']:
    setup(diff)
    p.evaluate('''mode=>{if(mode==='pt11-chase'){B._s4war.shield.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));B.hp=B.maxhp*.25;stage4ShieldBeginRearm(B,.25);}else er26Set(B,mode);window.nativeElectric=[];window.artRead=[];}''',mode)
    # Native controllers run, real native draw dispatch samples every frame.
    p.evaluate('''()=>{for(let i=0;i<390;i++){er26Tick(B,1/60);for(const q of eBullets){if(s4ac13Electric(q)&&!nativeElectric.includes(q))nativeElectric.push(q);q.t=(q.t||0)+1/60;}
     s4DrawRecord=true;s4DrawKeys=[];drawBullets();s4DrawRecord=false;artRead.push(...s4DrawKeys.filter(k=>k&&(/fireball|lightning_ball/.test(k))));}}''')
    attack=p.evaluate('()=>({count:nativeElectric.length,kinds:[...new Set(nativeElectric.map(q=>q.kind))],elements:[...new Set(nativeElectric.map(enemyOrdnanceElement))],keys:[...new Set(artRead)],finite:nativeElectric.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy)),shootable:nativeElectric.every(q=>{s3kOrdnanceRules(q);return q._shootable&&!q._weaponProof;})})')
    report['attacks'].append({'difficulty':diff,'mode':mode,**attack})
    check(attack['count']>0 and attack['finite'] and attack['shootable'],diff+' '+mode+': actual electrical balls finite and interceptable')
    check(attack['elements']==['lightning'] and attack['keys'] and all(k.startswith('s4w_lightning_ball_') for k in attack['keys']),diff+' '+mode+': native draw uses electric reel, never magma')
    p.evaluate('()=>{eBullets=nativeElectric.slice(0,5);eBullets.forEach((q,i)=>{q.x=B.x-100+i*50;q.y=330;q.t=.16+i*.12;});}')
    if mode=='p2-core-balls':shot(diff+'-electric-balls')
   check(p.evaluate('''()=>{const q=nativeElectric[0];q._fbImpact1002=false;const before=efxBursts.length;ordnanceBreak1002(q);return q._intercepted&&efxBursts.length===before+1&&efxBursts.at(-1).elem==='lightning';}'''),diff+' intercepted ball uses authored lightning impact')
  check(not errors,'zero browser errors');report['errors']=errors;br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
bad=[c['name'] for c in report['checks'] if not c['ok']];print(json.dumps({'checks':len(report['checks']),'failed':bad,'errors':errors}),flush=True)
assert not bad and not errors
