from pathlib import Path
from PIL import Image
import json,sys,ast,hashlib,numpy as np
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Recovered-boss-animations';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
sys.stdout.reconfigure(encoding='utf-8');checks=[];errors=[];trace=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name,str(data)[:350]if not ok else'',flush=True)
 (O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,name):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
old=ast.parse((W.parent/'solid_hammer_1111/verify_stage5.py').read_text())
seed=next(n.args[0].value for n in ast.walk(old)if isinstance(n,ast.Call)and n.args and isinstance(n.args[0],ast.Constant)and isinstance(n.args[0].value,str)and'window.seed119='in n.args[0].value)
(W/'seed5.js').write_text(seed)
M=json.loads((W/'manifest.json').read_text())['banks']
for n,a in M.items():
 p=R/f'assets/game/shared/combat/{a["folder"]}/{n}_regular.webp';im=np.array(Image.open(p));cw,ch=a['cell'];ok=True
 for f,m in enumerate(a['meta']):
  x,y=m['tip'];ok&=bool(im[f//4*ch+y,f%4*cw+x,3]>96)
 ck(n+': all16 recovered weapon contacts lie on real opaque pixels',ok)
for mat in ['regular','chrome','red','hit','red_hit']:
 a=np.array(Image.open(R/f'assets/game/shared/combat/boss_strike_1109b/corrupt-sides_{mat}.webp'))
 def same_visible(name,f,m):
  b=np.array(Image.open(W/f'exports/{name}_{mat}.webp'));src=m['sourceFrame'];u=a[src//4*576:(src//4+1)*576,src%4*576:(src%4+1)*576];v=b[f//4*576:(f//4+1)*576,f%4*576:(f%4+1)*576];mask=u[:,:,3]>0
  return np.array_equal(u[:,:,3],v[:,:,3])and np.array_equal(u[mask],v[mask])
 ck('Exact original whole-frame Draconus directional sequences / '+mat,all(same_visible(name,f,m)for name in ['corrupt-sides','corrupt-right']for f,m in enumerate(M[name]['meta'])))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  for stage in [5,8]:
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--js-flags=--expose-gc']);context=br.new_context(viewport={'width':1280,'height':800});p=boot(context,port,stage,errors,'boss');p.on('console',lambda m:errors.append(m.text)if'update error'in m.text or'draw error'in m.text else None)
   p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()&&ba119Warm(s)}',arg=stage,timeout=180000)
   if stage==5:p.evaluate(seed)
   else:p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=B._noHit=B.dead=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);Q.rf1110=null;Q.rage=false;Q.action=null;Q.cool=999;}")
   for mat in ['regular','chrome']:
    for right in [False,True]:
     q=p.evaluate('''({stage,mat,right})=>{
      const name=(stage===5?'blue':'corrupt')+(right?'-right':'-sides');
      if(stage===5){seed119('furious',mat);hammerState(B,'recover');const h=B._hammer;h._hj22Pair=hj22Pair(B,'blue',{x:player.x,y:player.y});h._hj22Pair.clock=(right?BA119_REPEAT.right:BA119_REPEAT.left)+.5;h.t=h._hj22Pair.clock;}
      else{Q.action=null;Q.chrome=mat==='chrome';Q.rf1110=null;Q.rage=false;hb20Start(B,'side');Q.action.t=Q.action.tell+(right?.7:0)+.35;}
      const pose=stage===5?ha21Blue(B):hb20Pose(B),a=pose.a,tip=stage===5?ba119At(B,a):rd74Point(B,pose);
      const old=ctx.drawImage,keys=[];ctx.drawImage=function(im,...args){const k=HA21.tags.get(im);if(k)keys.push(k);return old.call(this,im,...args)};
      try{drawWorld(0)}finally{ctx.drawImage=old}
      return{bank:a.bank,key:a.key,frame:a.frame,sourceFrame:a.sourceFrame,cell:[a.w,a.h],tip,keys,root:{x:B.x,y:B.y},hp:B.hp};}''',dict(stage=stage,mat=mat,right=right))
     expected=('blue'if stage==5 else'corrupt')+('-right'if right else'-sides');source_ok=stage==5 or q['sourceFrame']==(12 if right else 5)
     ck(f'Stage{stage} {mat}/{"right"if right else"left"}: actual extended strike source pose at native contact',source_ok and expected in q['bank']and q['frame']==8 and q['cell']==[576,576]and any(expected+'_'+mat in k for k in q['keys']),q)
     shot(p,f'stage{stage}-{mat}-'+('right'if right else'left'))
    q=p.evaluate('''([stage,mat])=>{const frames=new Set(),source=new Set(),xs=[];for(let i=0;i<64;i++){const f=i/64*16,q=stage===5?ba119Pose('blue-sides',f,mat):ba119Corrupt(Q,f,'corrupt-sides');frames.add(q.a.frame);source.add(q.a.sourceFrame??q.a.frame);xs.push(q.a.tip[0]);}return{frames:frames.size,source:source.size,travel:Math.max(...xs)-Math.min(...xs)};}''',[stage,mat])
    ck(f'Stage{stage} {mat}: authored directional cycle and broad physical head travel',q['frames']==16 and q['source']==(16 if stage==5 else 8)and q['travel']>120,q)
   sys.path.insert(0,str(W.parent/'three_way_hammer_1111'));import verify_three_way as h;h.O=O;(O/f'verification-stage{stage}').mkdir(exist_ok=True);h.run_three_way(p,stage,ck,shot)
   if stage==5:
    p.evaluate("()=>{seed119('furious','chrome');const h=B._hammer;h._hf22Red=false;h._hf22Charge=null;h.c29Break=null;h.hb20Pickup=null;h.c27RagePending=true;B.hp=B.maxhp*.15;C45.events=[];C46.events=[];RF1110.events=[];hf22BeginBlueRage(B);window.restoredTrace={phases:new Set(),actualKeys:new Set(),chargeShots:0,finalShots:0};const old=b20Image;b20Image=function(a,...args){if(a?.key)restoredTrace.actualKeys.add(a.key);return old.call(this,a,...args)};}")
    q=p.evaluate('()=>{const hp=B.hp;hammerBossDamage(B,100);return{charge:!!B._hammer._hf22Charge,hpSame:hp===B.hp,protected:B._noHit,hit:bossHitTest(B.x,B.y)};}')
    ck('Restored formation retains native damage protection',q['charge']and q['hpSame']and not q['hit'],q)
    saved=set()
    for batch in range(125):
     rows=p.evaluate('''()=>{const rows=[];for(let i=0;i<15;i++){efxClock+=1/60;updateBoss(1/60);drawWorld(0);const h=B._hammer,C=h._hf22Charge,R=h.c30,phase=C?'charge':R?.phase||h.state;restoredTrace.phases.add(phase);rows.push({phase,u:C?cgChargeU(B):null,t:R?.t,x:B.x,y:B.y,hp:B.hp,scale:R?.scale,key:ha21Blue(B)?.a?.key,final:C45.last});}return rows;}''');trace.extend(rows)
     last=rows[-1];phase=last['phase'];u=last.get('u')
     label='formation-stop'if u is not None and .18<u<.3 else'formation-charge'if u is not None and .55<u<.7 else'formation-release'if u is not None and u>.84 else phase if phase in ['kame_charge','kame_thrust','kame_fire','kame_return','volley_fire']else None
     if label and label not in saved:shot(p,'restored-'+label);saved.add(label)
     if batch%8==0:p.wait_for_timeout(1)
     if phase=='volley_fire'and'kame_fire'in saved:break
    q=p.evaluate('''()=>({phases:[...restoredTrace.phases],keys:[...restoredTrace.actualKeys],strikes:C45.events.filter(e=>e.type==='strike').length,final:C45.events.filter(e=>e.type==='final').length,opener:C46.events.filter(e=>e.type==='fire').length,done:!!B._hammer._c46Done,rf:RF1110.events.filter(e=>e.color==='red').length,cues:CF49.events.map(e=>e.role)})''')
    ck('Original throw/recoup/charge/arms-out release executes once with26 native strikes',q['strikes']==26 and q['final']==1 and q['rf']==0,q)
    ck('Actual rage-body draws use original source frames instead of replacement artwork',any('c29_'in k for k in q['keys'])and not any(k.startswith('rf1110_')for k in q['keys']),q['keys'][:30])
    ck('Original Kamehameha gathers, thrusts, fires, recovers and returns through real native clocks',all(k in q['phases']for k in ['kame_up','kame_strafe','kame_charge','kame_thrust','kame_fire','kame_recover','kame_return'])and q['opener']==1 and q['done'],q)
    ck('Original charge, transformation release and wave audio owners remain active',all(k in q['cues']for k in ['rage_charge','rage_release','wave_charge','wave_full']),q['cues'])
   else:
    q=p.evaluate("()=>{Q.action=null;Q.rf1110=null;Q.rage=false;Q.gunHP=321;Q.sf1111={acquired:true,held:true,broken:false};hb20Start(B,'gun');Q.action.t=2;return{modular:!!hb20Pose(B).a._dgm1111,hp:Q.gunHP};}")
    ck('Draconus modular gun remains selected with its native remaining HP',q['modular']and q['hp']==321,q)
   br.close()
  ck('No native page, update or draw errors',not errors,errors)
finally:stop()
(O/'native-trace.json').write_text(json.dumps(trace,separators=(',',':')));report=dict(checks=checks,errors=errors,runtimeHash=hashlib.sha256((R/'assets/boss_restore_1112.js').read_bytes()).hexdigest());(O/'checks.json').write_text(json.dumps(report,indent=2));assert all(c['passed']for c in checks)and not errors
