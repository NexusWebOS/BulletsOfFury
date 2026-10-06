"""Native protected form/animation fixtures. Not an unassisted Furious clear."""
from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import sys,json,base64,io
sys.path.insert(0,str(Path(__file__).resolve().parent));import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_ai_1006';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
checks=[];errors=[];scenes=[];port,stop=sh.serve(str(R))
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n):
 for i in range(0,n,15):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}',min(n-i,15));p.wait_for_timeout(4)
def snap(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 data=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));(O/(name+'.png')).write_bytes(data);return Image.open(io.BytesIO(data)).convert('RGB')
def setup(p,form,diff='furious',outer=2):
 p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':diff})
 p.evaluate('(c)=>{j3Encounter(B,c.outer);if(c.outer===2&&c.form)j3Mimic(B,c.form);on5FightStart(B);window.S=B._r30;window.J=j3State(B);window.D=c.form?gd4Create(B,c.form):null;dr5State(B).introWanted=false;dr5State(B).introSeen=true;fb2Talk=null;BOFCinematicDirector.cancel();story=null;player.y=hammerWarningFloorY();F6.events=[];}',{'form':form,'outer':outer})
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate('()=>r30Warm()');p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&F6_MOTION.every(a=>XART.rdy(a.key))',timeout=120000)
  ck(True,'all original modular cells plus 16 new native motion cells decode')
  setup(p,8);p.evaluate('()=>{B.x=D.p.x=worldWidth()/2;B.y=D.p.y=220;}');ims=[]
  poses=[('curl',0),('curl',.6),('ball',0),('uncurl',1),('giant_windup',0),('giant_dive',.40),('giant_sweep',.2),('giant_recover',.65),('whirlwind',0),('whirlwind',.12),('whirlwind',.24),('whirlwind',.36),('hammer_stun',0),('hammer_stun',.4),('storm_rebuild',0),('throw',0)]
  for i,(state,t) in enumerate(poses):
   p.evaluate('(c)=>{const h=D.p._hammer;h.gp4Emergency=null;h.state=c.state;h.t=c.t;h.angle=0;h.throw=null;h.frArmor=null;}',{'state':state,'t':t})
   ims.append(snap(p,'motion-'+str(i)).resize((480,512)))
  contact=Image.new('RGB',(480*4,540*4));dr=ImageDraw.Draw(contact)
  for i,im in enumerate(ims):x=(i%4)*480;y=(i//4)*540;contact.paste(im,(x,y));dr.text((x+5,y+514),F'Pose {i}: {poses[i][0]}',fill='white')
  contact.save(O/'motion-contact.jpg',quality=88)
  ck(p.evaluate('()=>Object.keys(F6.draws).length===16'),'all 16 additional poses actually pass through native game renderer')
  for diff in ['normal','furious']:
   for form in [1,2,3,4,6,7]:
    setup(p,form,diff);ticks(p,350);snap(p,f'copy-{form}-{diff}')
    r=p.evaluate('()=>({form:J.mimic,mode:S.mode,hp:B.hp,max:B.maxhp,history:D.history,events:F6.events,keys:fmcRig(B).map(v=>v.key),finite:fmcRig(B).every(v=>[v.x,v.y,v.w,v.h,v.rot].every(Number.isFinite)),ready:fmcRig(B).every(v=>XART.rdy(v.key))})')
    scenes.append({'form':form,'diff':diff,**r});ck(r['finite'] and r['ready'] and r['mode']=='fight',f'copy {form} renders live finite authored rig on {diff}')
    # Read the live plan just after it is selected; never invent proof by stubbing source AI.
    for _ in range(8):
     if p.evaluate('()=>F6.events.some(q=>q.event==="donorPlan")'):break
     ticks(p,60)
    plans=p.evaluate('()=>F6.events.filter(q=>q.event==="donorPlan")');ck(bool(plans) and plans[0]['count']==(3 if diff=='furious' else 1),f'copy {form} selects {"three" if diff=="furious" else "one"} separately warned followup bursts')
  setup(p,5);p.evaluate('()=>hk5AttackStart(B,"shieldCode")');frames=[]
  for i in range(32):ticks(p,12);frames.append(snap(p,'knight-code-'+str(i)).resize((480,512)))
  frames[0].save(O/'knight-code.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
  ck(p.evaluate('()=>F6.events.filter(q=>q.event==="knightCodeBurst").length===3'),'actual Furious shield fires three independently warned code bursts')
  setup(p,5);p.evaluate('()=>hk5AttackStart(B,"leapSlash")');ticks(p,210);snap(p,'knight-followup')
  ck(p.evaluate('()=>F6.events.some(q=>q.event==="knightFollowup")'),'Furious native downward/rising slash leads into newly warned smite')
  p.evaluate('()=>{hk5AttackStart(B,"armageddon");window.K=S.hkKnight;B.parts.find(q=>q.id==="sword").destroyed=true;}');ticks(p,1)
  ck(p.evaluate('()=>K.phase==="recover"&&K.rows.length===0'),'destroyed sword cancels real native Armageddon')
  setup(p,8);p.evaluate('()=>{B.x=D.p.x=worldWidth()/2;B.y=D.p.y=220;D.p._hammer.hkSide=-1;hammerState(D.p,"hkSideTell");D.p._hammer.f6Sides=0;}');frames=[]
  for i in range(18):ticks(p,12);frames.append(snap(p,'hammer-chain-'+str(i)).resize((480,512)))
  frames[0].save(O/'hammer-chain.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
  ck(p.evaluate('()=>D.history.filter(q=>q==="hkSideTell").length>=2'),'actual Furious copied Hammer warns both sideways strikes')
  setup(p,0,outer=1);p.evaluate('()=>{S.cd=0;}');ticks(p,480);snap(p,'ghost-furious');ck(p.evaluate('()=>F6.events.some(q=>q.event==="outerPlan"&&q.type==="ghostWarp")'),'actual Furious ghost uses warp early in its upgraded pattern book')
  setup(p,0);p.evaluate('()=>S.cd=0');ticks(p,195);snap(p,'colossus-furious');ck(p.evaluate('()=>F6.events.some(q=>q.event==="colossusEcho")'),'actual Furious colossus fires its newly warned followup')
  p.evaluate('()=>{const before=J.hp.slice();j3Mimic(B,3);on5FightStart(B);window.saved=before;}');ticks(p,100);p.evaluate('()=>j3Clear(B)')
  ck(p.evaluate('()=>J.hp.length===9&&J.max.length===9&&!eBullets.some(q=>q._f6Owner===B)&&J.gp4Donors.every(d=>!d||!d.aa5Salvo)'),'nine pools and full cleanup remain intact')
  ck(not errors,'zero native browser or renderer errors');br.close()
finally:
 stop();(R/'docs/qa/finale_ai_1006.json').write_text(json.dumps({'checks':checks,'scenes':scenes,'errors':errors,'limitations':'Protected native encounter fixtures. No unassisted Furious clear or human balance approval claimed.'},indent=2),encoding='utf-8')
if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
