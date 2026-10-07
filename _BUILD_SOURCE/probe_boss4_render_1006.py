"""Native Boss 4 component ownership fixtures; not campaign clears."""
from pathlib import Path
import sys,json,base64,ast
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
ap=__import__('argparse').ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
O=R/'_shots/boss4_render_1006';O.mkdir(parents=True,exist_ok=True)
report={'checks':[],'traces':{},'scope':'Protected native component fixtures; not an unassisted fight or balance proof.'};errors=[]
def check(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{fb1002Warm();er26Warm();missionWarm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);}')
  p.wait_for_function('()=>Object.values(FB1002_ART).every(a=>XART.rdy(a.key))&&XART.rdy("mr27_storm")',timeout=120000)
  p.evaluate('''()=>{
   window.drawTrace=[];window.drawLabel=null;
   const draw=ctx.drawImage;ctx.drawImage=function(...a){if(drawLabel)drawTrace.push({...drawLabel});return draw.apply(this,a);};
   const cell=fb1002Cell;fb1002Cell=function(name,frame,x,y,w,h,tint,...rest){const old=drawLabel;drawLabel={kind:name,x,y,w,h,tint:!!tint};try{return cell.call(this,name,frame,x,y,w,h,tint,...rest);}finally{drawLabel=old;}};
   const blit=mr27Blit;mr27Blit=function(skin,cell,q,flash,...rest){const old=drawLabel;drawLabel={kind:skin+'-'+cell,x:q.x,y:q.y,w:q.w,h:q.h,flash:flash||0};try{return blit.call(this,skin,cell,q,flash,...rest);}finally{drawLabel=old;}};
  }''')
  def setup(diff='normal'):
   p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','diff':diff});p.evaluate('()=>{B._phaseInvuln=0;B._drawY=B.y;stage4ShieldSyncNodes(B);B.flash=0;B._er26.t=2;B._er26.warm=1;B._s4war.shield.nodes.forEach(n=>n.materialize=1);}')
  def draw(name):
   q=p.evaluate('()=>{drawTrace=[];shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {trace:drawTrace,nodes:B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y,hp:n.hp,dead:n.dead})),lightning:mr27Shape(B,"lightning")};}')
   report['traces'][name]=q
   (O/(('before-' if args.baseline else '')+name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   return q
  for diff in ['easy','normal','hard','furious']:
   setup(diff);q=draw(diff+'-intact');guns=[t for t in q['trace'] if t['kind']=='lightning_gun']
   check(len(guns)==1,diff+' middle lightning weapon draws once, not once per generator')
   nodes=q['nodes'];locals=[t for t in q['trace'] if t['kind']=='storm-3' and any(abs(t['x']-n['x'])<.01 and abs(t['y']-n['y'])<.01 for n in nodes)]
   check(len(locals)==4,diff+' four generator centres draw at their own sockets')
   p.evaluate('()=>{B.flash=.18;B._s4war.shield.nodes[0].flash=.16;}');q=draw(diff+'-local-flash')
   check(all(not t['tint'] for t in q['trace'] if t['kind']=='lightning_gun'),diff+' unrelated hull/generator flash does not whiten the middle weapon')
   p.evaluate('()=>{B.flash=0;B._mr27.parts.find(p=>p.id==="lightning").flash=.18;}');q=draw(diff+'-middle-hit')
   check(any(t['tint'] for t in q['trace'] if t['kind']=='lightning_gun'),diff+' direct middle weapon damage still has its own hit flash')
  setup();p.evaluate('''()=>{const n=B._s4war.shield.nodes[0];window.hpBefore={node:n.hp,boss:B.hp,gun:B._mr27.parts.find(p=>p.id==='lightning').hp};pBullets.push({kind:'mg',x:n.x,y:n.y+14,vx:0,vy:-4,w:5,h:12,dmg:2,t:0});updatePlay(1/60);}''')
  check(p.evaluate('()=>{const n=B._s4war.shield.nodes[0];return n.hp<hpBefore.node&&B.hp===hpBefore.boss&&B._mr27.parts.find(p=>p.id==="lightning").hp===hpBefore.gun;}'),'real ordinary bullet damages only its generator')
  q=draw('ordinary-generator-hit')
  check(not any(t.get('tint') for t in q['trace'] if t['kind']=='lightning_gun'),'actual generator bullet hit does not flash the middle weapon')
  p.evaluate('()=>stage4ShieldDestroyNode(B,B._s4war.shield.nodes[0])');q=draw('one-generator-broken');dead=q['nodes'][0]
  check(not any(t['kind'] in ['storm-3','storm-5'] and abs(t['x']-dead['x'])<.01 and abs(t['y']-dead['y'])<.01 for t in q['trace']),'broken generator body and centre disappear immediately')
  check(len([t for t in q['trace'] if t['kind']=='storm-5' and t['w']==54])==3,'three surviving generators remain visible')
  for i in range(4):
   p.evaluate('()=>{for(let i=0;i<30;i++)updatePlay(1/60);}');p.wait_for_timeout(8)
  q=draw('broken-generator-after-two-seconds');dead=q['nodes'][0]
  check(dead['dead'] and not any(t['kind'] in ['storm-3','storm-5'] and abs(t['x']-dead['x'])<.01 and abs(t['y']-dead['y'])<.01 for t in q['trace']),'broken generator stays absent through two seconds of real combat updates')
  p.evaluate('()=>{B._mr27.parts.find(p=>p.id==="lightning").dead=true;B.flash=0;}');q=draw('middle-weapon-broken')
  check(not any(t['kind']=='lightning_gun' for t in q['trace']),'destroyed middle weapon disappears without removing live generator centres')
  check(len([t for t in q['trace'] if t['kind']=='storm-3' and t['w']==15])==3,'local generator centres survive middle weapon destruction')
  p.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.5);B._s4war.coreTurrets.forEach(d=>{d.materialize=1;d.shield=0;});}')
  q=draw('helpers-with-middle-broken');check(len([t for t in q['trace'] if t['kind']=='storm-3' and t['w']!=15])>=2,'helper centres retain their own position after middle weapon destruction')
  p.evaluate('()=>{B._s4war.shield.active=false;B._s4war.shield.rearming=false;B._s4war.shield.breakT=0;}');q=draw('shield-inactive')
  check(not any(t['kind']=='storm-5' and t['w']==54 for t in q['trace']),'inactive field never leaves ghost generators')
  setup();p.evaluate('()=>{const H=B._s4war.shield;H.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));stage4ShieldBeginRearm(B,.75);stage4ShieldTick(B,.1);}');q=draw('rearm-before-materialization')
  check(not any(t['kind']=='storm-5' and t['w']==54 for t in q['trace']),'rearming generators wait for their visible materialization')
  p.evaluate('()=>stage4ShieldTick(B,1.1)');q=draw('rearm-complete');check(len([t for t in q['trace'] if t['kind']=='storm-5' and t['w']==54])==4,'intentional threshold rearm restores four real generators')
  p.evaluate('()=>{B._s4war.shield.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));}');q=draw('all-generators-broken');check(not any(t['kind']=='storm-5' and t['w']==54 for t in q['trace']),'last generator break removes all four node renders')
  # Extended double-check: use native projectile updates and actual HP thresholds.
  report['extendedAudit']={'damageRoutes':[],'cycles':[]}
  def frames(n):
   for i in range(0,n,30):
    p.evaluate('(n)=>{for(let i=0;i<n;i++)updatePlay(1/60);}',min(30,n-i));p.wait_for_timeout(8)
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   result=p.evaluate('''()=>{const H=B._s4war.shield;window.auditOldTarget=retinaBossTargets(B).find(t=>t.part===H.nodes[0]);
    const hp=B.hp,light=B._mr27.parts.find(p=>p.id==='lightning').hp,right=H.nodes.filter(n=>n.side>0).map(n=>n.hp);
    player.x=H.nodes[0].x;player.y=VH-100;
    pBullets.push({kind:'beam',x:player.x,y:player.y,w:26,h:600,dmg:Math.max(...H.nodes.map(n=>n.hp))+1,life:.2,_hit:[],_bt:0});updatePlay(1/60);pBullets=[];
    return {leftGone:H.nodes.filter(n=>n.side<0).every(n=>n.dead),rightUntouched:H.nodes.filter(n=>n.side>0).every((n,i)=>n.hp===right[i]),hullUntouched:B.hp===hp,middleUntouched:B._mr27.parts.find(p=>p.id==='lightning').hp===light};}''')
   report['extendedAudit']['damageRoutes'].append({'difficulty':diff,'beam':result})
   check(all(result.values()),diff+' real held beam destroys both column cores without damaging the other column or middle')
   q=draw(diff+'-beam-column-break')
   check(len([t for t in q['trace'] if t['kind']=='storm-5' and t['w']==54])==2 and not any(t.get('tint') for t in q['trace'] if t['kind']=='lightning_gun'),diff+' paired beam break leaves only two visible cores and no middle flash')
   check(p.evaluate('()=>{const hp=B.hp;return !retinaTargetValid(auditOldTarget)&&retinaMissileDamage(auditOldTarget,999,{kind:"gmiss"})===false&&B.hp===hp;}'),diff+' destroyed core loses its old Retina lock and rejects late damage')
   p.evaluate('''()=>{window.auditNode=B._s4war.shield.nodes.find(n=>!n.dead);window.auditTarget=retinaBossTargets(B).find(t=>t.part===auditNode);window.auditHP=auditNode.hp;run.bombs=20;run.missileTier='standard';player.x=worldWidth()/2;window.auditLaunched=useBomb(auditTarget);}''')
   frames(150)
   check(p.evaluate('()=>auditLaunched&&auditNode.hp<auditHP'),diff+' actual curved Retina missile damages a surviving generator')
   q=draw(diff+'-retina-generator-hit');check(not any(t.get('tint') for t in q['trace'] if t['kind']=='lightning_gun'),diff+' missile damage leaves the middle weapon untinted')
   setup(diff)
   for threshold in [.75,.50,.25]:
    for side in [-1,1]:
     p.evaluate('''side=>{const H=B._s4war.shield,n=H.nodes.find(n=>n.side===side);player.x=n.x;player.y=VH-100;
      pBullets.push({kind:'beam',x:player.x,y:player.y,w:26,h:600,dmg:Math.max(...H.nodes.map(n=>n.hp))+1,life:.2,_hit:[],_bt:0});updatePlay(1/60);pBullets=[];}''',side)
    check(p.evaluate('()=>!B._s4war.shield.active&&B._s4war.shield.nodes.every(n=>n.dead)&&!retinaBossTargets(B).some(t=>t.kind==="electrical node")'),diff+' all cores broken before '+str(threshold)+' threshold: art owners and Retina targets are dead')
    event=p.evaluate('''threshold=>{B._phaseInvuln=0;B._noHit=false;B._er26.neutralOpening=false;
     _lastHitX=B.x;_lastHitY=B.y+B.h*.39;_dmgBullet={kind:'mg',x:_lastHitX,y:_lastHitY};
     try{hitBoss(B.maxhp*.35);}finally{_dmgBullet=null;}
     return {ratio:B.hp/B.maxhp,thresholdIndex:B._s4war.shieldThresholdIndex,rearming:B._s4war.shield.rearming,cycle:B._s4war.shield.cycle,targets:retinaBossTargets(B).filter(t=>t.kind==='electrical node').length};}''',threshold)
    report['extendedAudit']['cycles'].append({'difficulty':diff,'threshold':threshold,'begin':event})
    check(abs(event['ratio']-threshold)<.0001 and event['rearming'] and event['targets']==0,diff+' real hull damage triggers '+str(threshold)+' rearm with no premature locks')
    q=draw(diff+'-threshold-'+str(threshold)+'-start')
    check(not any(t['kind']=='storm-5' and t['w']==54 for t in q['trace']),diff+' '+str(threshold)+' rearm begins with no ghost core art')
    frames(75);q=draw(diff+'-threshold-'+str(threshold)+'-complete')
    check(p.evaluate('()=>B._s4war.shield.active&&!B._s4war.shield.rearming&&retinaBossTargets(B).filter(t=>t.kind==="electrical node").length===4') and len([t for t in q['trace'] if t['kind']=='storm-5' and t['w']==54])==4,diff+' '+str(threshold)+' complete rearm restores exactly four visible/targetable cores')
   # Exercise the real no-weapons ram branch that disables the field.
   p.evaluate('()=>{B._mr27.parts.forEach(p=>p.dead=true);B._phaseInvuln=0;}');frames(180);q=draw(diff+'-weaponless-ram')
   check(p.evaluate('()=>!B._s4war.shield.active&&!retinaBossTargets(B).some(t=>t.kind==="electrical node")') and not any(t['kind']=='storm-5' and t['w']==54 for t in q['trace']),diff+' real weaponless ram removes generator art and locks together')
  check(not errors,'zero page or console errors');report['errors']=errors;br.close()
finally:stop()
(O/('baseline.json' if args.baseline else 'verification.json')).write_text(json.dumps(report,indent=2)+'\n')
failed=[c['name'] for c in report['checks'] if not c['ok']];print(json.dumps({'checks':len(report['checks']),'failed':failed,'errors':errors}))
if not args.baseline: assert not failed and not errors
