"""Actual game-context revival pixels and threshold timing; protected fixtures."""
from pathlib import Path
import ast,json,base64
import shoot as sh
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/s4_core_revival_1006';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
report={'checks':[],'captures':{},'scope':'Protected native threshold/visual fixtures; not campaign clears.'};errors=[]
def ck(value,name):report['checks'].append({'ok':bool(value),'name':name});print(('OK ' if value else 'FAIL ')+name,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{fb1002Warm();er26Warm();missionWarm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);XART.rdy(S4REV1006_ART.key);}')
  p.wait_for_function('()=>Object.values(FB1002_ART).every(a=>XART.rdy(a.key))&&XART.rdy("mr27_storm")&&XART.rdy(S4REV1006_ART.key)',timeout=120000)
  p.evaluate('''()=>{
   window.reviveDraws=[];window.reviveLabel=null;window.reviveChargeCues=0;
   const image=ctx.drawImage;ctx.drawImage=function(...a){if(reviveLabel)reviveDraws.push({...reviveLabel,source:a.slice(1,5)});return image.apply(this,a);};
   const clip=s4RevivalClip1006;s4RevivalClip1006=function(name,u,x,y,sx,sy,alpha){const old=reviveLabel;reviveLabel={name,u,x,y,sx,sy,alpha};try{return clip.apply(this,arguments);}finally{reviveLabel=old;}};
   const sound=stage4WarfareSound;stage4WarfareSound=function(name){if(name==='warshipCoreCharge')reviveChargeCues++;return sound.apply(this,arguments);};
  }''')
  def setup(diff):
   p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','diff':diff});p.evaluate('()=>{B._phaseInvuln=0;B._noHit=false;B._drawY=B.y;stage4ShieldSyncNodes(B);B._er26.neutralOpening=false;}')
  def cap(name):
   q=p.evaluate('()=>{reviveDraws=[];shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {draws:reviveDraws,revival:B._s4war.shield.revival1006,rearming:B._s4war.shield.rearming,active:B._s4war.shield.active,nodes:B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y,dead:n.dead,mat:n.materialize})),hp:B.hp};}')
   report['captures'][name]=q;(O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));return q
  def frames(n):
   for i in range(0,n,15):p.evaluate('(n)=>{for(let i=0;i<n;i++)updatePlay(1/60);}',min(15,n-i));p.wait_for_timeout(8)
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   for threshold in [.75,.5,.25]:
    q=p.evaluate('''threshold=>{const H=B._s4war.shield;H.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));B._phaseInvuln=0;B._noHit=false;
     _lastHitX=B.x;_lastHitY=B.y+B.h*.39;_dmgBullet={kind:'mg',x:_lastHitX,y:_lastHitY};try{hitBoss(B.maxhp*.35);}finally{_dmgBullet=null;}
     return {hp:B.hp,max:B.maxhp,revival:H.revival1006,cycle:H.cycle};}''',threshold)
    ck(abs(q['hp']/q['max']-threshold)<.0001 and q['revival'] and q['revival']['cycle']==q['cycle'],diff+' '+str(threshold)+' real threshold starts ship revival')
    frames(6);early=cap(diff+'-'+str(threshold)+'-charge')
    ck(any(d['name']=='charge' for d in early['draws']) and not any(d['name']=='conduit' for d in early['draws']),diff+' '+str(threshold)+' ship charges before conduit release')
    frames(20);feed=cap(diff+'-'+str(threshold)+'-conduits')
    ck(sum(d['name']=='conduit' for d in feed['draws'])==4 and sum(d['name']=='socket' for d in feed['draws'])==4,diff+' '+str(threshold)+' four generated feeds and socket reels draw on actual game context')
    ck(all(any(d['name']=='socket' and abs(d['x']-n['x'])<.001 and abs(d['y']-n['y'])<.001 for d in feed['draws']) for n in feed['nodes']),diff+' '+str(threshold)+' revival pulses use moving generator sockets')
    frames(22);cap(diff+'-'+str(threshold)+'-reconstruct')
    frames(18);complete=cap(diff+'-'+str(threshold)+'-restored')
    ck(complete['active'] and not complete['rearming'] and sum(d['name']=='socket' for d in complete['draws'])==4 and all(not n['dead'] and n['mat']==1 for n in complete['nodes']) and complete['hp']==q['hp'],diff+' '+str(threshold)+' four cores return at existing timing with harmless afterglow')
    frames(28);done=cap(diff+'-'+str(threshold)+'-finished')
    ck(not done['draws'] and not done['revival'],diff+' '+str(threshold)+' revival ends without lingering or looping')
  setup('furious');p.evaluate('()=>{B._s4war.shield.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));stage4ShieldBeginRearm(B,.75);}');frames(26)
  p.evaluate('()=>B.dead=true');q=cap('death-cancels-revival');ck(not q['draws'],'death immediately suppresses charge/conduits/socket effects')
  setup('furious');p.evaluate('()=>{B._s4war.shield.nodes.forEach(n=>stage4ShieldDestroyNode(B,n));stage4ShieldBeginRearm(B,.75);}');frames(26)
  p.evaluate('()=>{B._s4war.shield.active=false;B._s4war.shield.rearming=false;}');q=cap('inactive-cancels-revival');ck(not q['draws'],'inactive field immediately suppresses revival pixels')
  setup('normal');q=cap('fresh-stage-no-revival');ck(not q['draws'] and not q['revival'],'fresh encounter has no leftover revival')
  ck(p.evaluate('()=>reviveChargeCues>=12'),'native revival charge sound cue dispatches')
  ck(not errors,'zero page or console errors');report['errors']=errors;br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');bad=[c['name'] for c in report['checks'] if not c['ok']];print(json.dumps({'checks':len(report['checks']),'failed':bad,'errors':errors}));assert not bad and not errors
