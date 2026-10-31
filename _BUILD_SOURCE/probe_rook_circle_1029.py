from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=999;G.rd21.fleet=null;G.rd21.next=999;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;q.x=70+q.i*60;q.y=100;}window.n=R.ships.find(q=>q.key==='nyx');n.x=400;n.y=170;ny46Cloak(n);player.x=400;player.y=440;run.bombs=40;}""")
  p.evaluate("()=>{window.k=R.ships.find(q=>q.key==='rook');for(const q of R.ships){q.mode='fight';q.x=camLeftX()+70+q.i*75;q.y=110;q.rg4.act=null;q.rg4.cd=999;}k.x=camLeftX()+80;k.y=150;pBullets=[];G.ord=[];G.rr26.wall=null;rg4Attack(k,R,G,'rk38spin');}")
  p.wait_for_function("()=>['field','symbol'].every(r=>['green','yellow','red'].every(c=>XART.rdy('rk50_'+r+'_'+c)))")
  ck('Stored squad dispatcher initializes the same filled center attack',p.evaluate("(()=>{k.rg4.act=null;RD42.attack(k,R,G,'rk38spin');return k.rg4.act._rk50&&k.rg4.act.center.x===camLeftX()+viewW()/2})()"))
  ck('Spin destination is viewport center rather than the current player lane',p.evaluate('k.rg4.act.center.x===camLeftX()+viewW()/2&&k.rg4.act.center.y===VH/2'))
  p.evaluate('()=>{for(let i=0;i<28;i++)rg4AttackTick(k,R,G,.05)}')
  ck('Rook reaches the center before starting his warning',p.evaluate("k.rg4.act.phase==='charge'&&Math.abs(k.x-camLeftX()-viewW()/2)<.001&&k.y===VH/2"))
  results=[]
  for pan in [0,120,240,60]:
   results.append(p.evaluate("""pan=>{camX=pan;const A=k.rg4.act;A.t=.5;rg4AttackTick(k,R,G,1/60);for(const q of R.ships)if(q!==k){q.x=k.x+(q.i-2)*4;q.y=k.y+(q.i-2)*3;}rr45Separate(boss);return{x:k.x,y:k.y,cx:camLeftX()+viewW()/2,overlap:R.ships.filter(q=>q!==k).some(q=>{const a=rr45Bounds(k),b=rr45Bounds(q);return Math.abs(q.x-k.x)<a.w+b.w+6&&Math.abs(q.y-k.y)<a.h+b.h+8})};}""",pan))
  ck('Center reservation survives camera changes and crowded squad spacing',all(abs(q['x']-q['cx'])<.01 and q['y']==256 and not q['overlap']for q in results),results)
  p.evaluate("()=>{rr26Deploy(G);G.rr26.wall.t=3.1;rk50Hold(k,k.rg4.act);rr26BlockShips(G);rr45Separate(boss)}")
  ck('Golden Aegis and squad spacing do not push him out of center',p.evaluate('Math.abs(k.x-camLeftX()-viewW()/2)<.01&&k.y===VH/2'))
  art=p.evaluate("""()=>{const out=[];for(const c of['green','yellow','red']){const im=XART.get('rk50_field_'+c),s=document.createElement('canvas');s.width=s.height=404;s.getContext('2d').drawImage(im,0,0);let holes=0;for(let a=0;a<360;a+=5)for(const r of[0,50,100,150,190]){const x=Math.round(202+Math.cos(a*Math.PI/180)*r),y=Math.round(202+Math.sin(a*Math.PI/180)*r);if(s.getContext('2d').getImageData(x,y,1,1).data[3]!==128)holes++;}out.push({colour:c,holes,w:im.width,h:im.height});}return out;}""")
  ck('Every colour fills the center and complete 360-degree radius',all(q['holes']==0 and q['w']==404 and q['h']==404 for q in art),art)
  draws=p.evaluate("""()=>{const A=k.rg4.act,rows=[],get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(key){const im=get.apply(this,arguments);if(im)tags.set(im,key);return im};ctx.drawImage=function(im,...a){rows.push({key:tags.get(im)||'',a});return draw.call(this,im,...a)};const old=rr26Effect;window.oldRings=0;rr26Effect=function(key){if(key==='ngm_shock_7')oldRings++;return old.apply(this,arguments)};try{for(const t of[.1,1.3,2]){A.t=t;fr27RebelDrawShip(k)}}finally{ctx.drawImage=draw;XART.get=get;rr26Effect=old;}return rows;}""")
  ck('Native renderer blits all three filled warning states',all(any(q['key']=='rk50_field_'+c for q in draws)for c in ['green','yellow','red']))
  ck('Rotate symbols remain above Rook in matching colours',all(any(q['key']=='rk50_symbol_'+c and abs(q['a'][1]-(256-78-24))<1 for q in draws)for c in ['green','yellow','red']))
  ck('Old outer shock-ring warning is absent',p.evaluate('oldRings===0'))
  ck('Warning field is drawn before the whole Rook hull',next(i for i,q in enumerate(draws)if q['key'].startswith('rk50_field_'))<next(i for i,q in enumerate(draws)if q['key']==p.evaluate('RR33_ART.banks.flight_rook.key')))
  p.evaluate("()=>{for(const q of R.ships)if(q!==k){q.x=2000;q.y=-1000;}camX=0;rk50Hold(k,k.rg4.act);k.rg4.act.t=.3;drawWorld(0)}");p.screenshot(path=str(W/'green-warning.png'))
  p.evaluate("()=>{k.rg4.act.t=1.3;drawWorld(0)}");p.screenshot(path=str(W/'yellow-warning.png'))
  p.evaluate("()=>{k.rg4.act.t=2;drawWorld(0)}");p.screenshot(path=str(W/'red-warning.png'))
  p.evaluate("()=>{eBullets=[];k.rg4.act.t=2.19;rg4AttackTick(k,R,G,.02);window.fireCount=eBullets.length;window.fieldBefore=RK50.fields;drawWorld(0)}")
  ck('Native radial attack starts after the complete windup',p.evaluate("k.rg4.act.phase==='fire'&&eBullets.length===2&&eBullets.every(p=>p._rk38Round)"))
  ck('FOV clears for gunfire while rotate badge remains',p.evaluate('RK50.fields===fieldBefore'))
  p.evaluate("()=>{for(let i=0;i<40;i++)rg4AttackTick(k,R,G,.05)}")
  ck('Real spinning hull remains at center while firing',p.evaluate('Math.abs(k.x-camLeftX()-viewW()/2)<.001&&k.y===VH/2&&k.rfHeading>Math.PI*2'))
  p.evaluate("()=>{window.hpBefore=k.hp;window.srcOld=_dmgSrc;_dmgSrc='missile';boss._rebels.hit=k.i;rebelSquadDamage(boss,10);_dmgSrc=srcOld;}")
  ck('Real missile damage and knockback remain active',p.evaluate('k.hp<hpBefore&&k.y===234&&k.rg4.act._rk50Y===234'))
  pixel=p.evaluate("""()=>{const tint=xartTint,draw=ctx.drawImage,tag=new WeakSet(),B=RR33_ART.banks.flight_rook;let white=0,ink=0,blits=0;xartTint=function(key){const im=tint.apply(this,arguments);if(key===B.key)tag.add(im);return im};ctx.drawImage=function(im,...a){if(tag.has(im)&&a.length===8){blits++;const c=document.createElement('canvas');c.width=a[2];c.height=a[3];const g=c.getContext('2d');g.drawImage(im,a[0],a[1],a[2],a[3],0,0,a[2],a[3]);const d=g.getImageData(0,0,c.width,c.height).data;for(let i=0;i<d.length;i+=4)if(d[i+3]>200){ink++;if(Math.min(d[i],d[i+1],d[i+2])>245)white++;}}return draw.call(this,im,...a)};try{drawWorld(0)}finally{xartTint=tint;ctx.drawImage=draw}return{blits,ink,white,flash:k.flash};}""")
  ck('Real damaged hull pixels render white above the FOV',pixel['blits']>0 and pixel['ink']>200 and pixel['white']/pixel['ink']>.8,pixel)
  p.screenshot(path=str(W/'missile-hit.png'))
  p.evaluate("()=>{for(let i=0;i<4;i++){G.age+=.1;_dmgSrc='missile';boss._rebels.hit=k.i;rebelSquadDamage(boss,10);} _dmgSrc=srcOld;}")
  ck('Five real missile hits still interrupt and stun the spin',p.evaluate('!!k._rk38Stun&&!k.rg4.act&&!rk50Fixed(k)'))
  p.evaluate('()=>{pBullets=[];for(let i=0;i<8;i++)rebelSquadTick(boss,.05)}')
  ck('Native hit flash expires after real missile impacts',p.evaluate('k.flash===0'))
  p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'flash-expired.png'))
  p.evaluate("()=>{run._gp4StageX=true}")
  ck('Stage X keeps its existing attack owner',p.evaluate('!rk50Own(k,{kind:"rk38spin",_rk50:true})'))
  ck('No native errors',not errors,errors);b.close()
finally:stop()
