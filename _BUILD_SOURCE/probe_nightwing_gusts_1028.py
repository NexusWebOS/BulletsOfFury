from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys,http.server,math,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_gusts_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text());images={k:Image.open(R/M['banks'][k]['path']).convert('RGBA')for k in ['wind_bullet','wind_muzzle']}
def cell(k,i):
 a=M['banks'][k];return images[k].crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],i%a['cols']*a['cw']+a['cw'],i//a['cols']*a['ch']+a['ch']))
ck('Travel gusts have32 directions and16 animated phases',M['banks']['wind_bullet']['frames']==512 and M['banks']['wind_bullet']['directions']==32 and M['banks']['wind_bullet']['phaseFrames']==16)
ck('Barrel gusts have32 directions and8 phases',M['banks']['wind_muzzle']['frames']==256 and M['banks']['wind_muzzle']['phaseFrames']==8)
ck('All768 gust cells retain clear borders, fixed even canvases and bounded textures',all(a['cw']==a['ch']==64 and max(images[k].size)<=4096 and all((lambda b:b and b[0]>0 and b[1]>0 and b[2]<64 and b[3]<64)(cell(k,i).getbbox())for i in range(a['frames']))for k,a in M['banks'].items()if k in images))
ck('All sixteen travel animation phases are distinct',len({cell('wind_bullet',i).tobytes()for i in range(16)})==16)
ck('New source is the selected animated wind design',M['gusts']['keyframeJob']=='b5986218-1399-4445-be0c-cf08ba36f449'and M['gusts']['selectedCandidate']==4 and M['gusts']['animationJob']=='9c1789b8-64ba-4aa4-819d-195ecf675e54')
H=json.loads((R/'_ART_SOURCES/nightwing_wind_1028/source-hashes.json').read_text());stable=[(k,v)for k,v in H.items()if '_identity_1028b.png'in k or any(s in k for s in ['gun_left.png','gun_right.png','wind_ring.png','wind_charge.png','exhaust_'])];ck('Corrected aircraft, guns, exhausts, charge and dash rings remain byte-identical',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in stable),len(stable))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None);p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);}");step(430)
  p.evaluate("()=>{nw30Cancel(boss);const A=boss._whv.ace;A.dash=A.desp=A.roll=A.somer=A._nf29Pose=null;A.inverted=false;A.gunCd=A.dashCd=A.somerCd=A.rollCd=99;boss._nw30.gunCd=boss._nw30.windCd=99;NW30.events=[];eBullets=[];wm26Releases=[];nw30Start(boss,'wind');}");step(70);p.screenshot(path=str(W/'charge.png'));step(63);p.screenshot(path=str(W/'gust-salvo.png'))
  q=p.evaluate("()=>({wind:eBullets.filter(q=>q._nw30Wind).map(q=>({w:q.w,h:q.h,element:enemyOrdnanceElement(q),intercept:enemyOrdnanceCanIntercept(q)})),muzzles:wm26Releases.filter(q=>q.owner===boss).map(q=>({family:q.family,age:q.age})),action:boss._nw30.action.kind})")
  ck('Wind attack releases six real gust rounds in its first dual fan',len(q['wind'])==6,q)
  ck('Real rounds retain Wind classification and cannot be shot down',all(z['element']=='wind'and not z['intercept']for z in q['wind']))
  ck('Both barrels use the dedicated gust release rather than sonic rings',len(q['muzzles'])==2 and all(z['family']=='nw30wind'for z in q['muzzles']),q['muzzles'])
  q=p.evaluate('''()=>{const f=wm26Releases.find(f=>f.owner===boss),a=wm26Point(f),A=boss._whv.ace;A.x+=11;A.y+=7;const c=wm26Point(f);A.x-=11;A.y-=7;return{x:c.x-a.x,y:c.y-a.y};}''');ck('Gust releases stay anchored to the moving barrel',abs(q['x']-11)<.001 and abs(q['y']-7)<.001,q)
  q=p.evaluate('''()=>{let calls=[];const draw=ctx.drawImage,im=XART.get(NW30_ART.banks.wind_muzzle.key);ctx.drawImage=function(q,...args){if(q===im)calls.push(args);return draw.apply(this,[q,...args]);};try{wm26DrawEnemy()}finally{ctx.drawImage=draw}return calls;}''');ck('Native muzzle renderer blits exactly two fixed authored gust cells',len(q)==2 and all(a[-2:]==[64,64]for a in q))
  q=p.evaluate('''()=>{const p=eBullets.find(p=>p._nw30Wind),M=NW30_ART.banks.wind_bullet,im=XART.get(M.key),base=ctx.drawImage,out=[];let current;ctx.drawImage=function(q,...a){if(q===im)current=a;return base.apply(this,[q,...a]);};try{for(let i=0;i<32;i++){const a=Math.PI/2+i*TAU/32;drawCombatFinalProjectile({...p,vx:Math.cos(a),vy:Math.sin(a),t:.2});out.push(Math.floor(current[1]/64)*M.cols+Math.floor(current[0]/64));}}finally{ctx.drawImage=base}return out;}''');ck('Every travel direction selects its own native wind-gust bank',all(f//16==i for i,f in enumerate(q)),q)
  q=p.evaluate('''()=>{const p=eBullets.find(p=>p._nw30Wind),M=NW30_ART.banks.wind_bullet,im=XART.get(M.key),base=ctx.drawImage,out=[];ctx.drawImage=function(q,...a){if(q===im)out.push(Math.floor(a[1]/64)*M.cols+Math.floor(a[0]/64));return base.apply(this,[q,...a]);};try{for(let i=0;i<16;i++)drawCombatFinalProjectile({...p,vx:0,vy:1,t:i/24});}finally{ctx.drawImage=base}return out;}''');ck('Native projectile animation traverses the generated motion',len(set(q))>=14,q)
  step(100);q=p.evaluate("()=>({shots:NW30.events.filter(e=>e.event==='turret-shot'&&e.kind==='wind').length,n:boss._nw30.action?.n,phase:boss._nw30.action?.phase})");ck('The existing five-volley dual-fan firing sequence is preserved',q['shots']==10 and q['n']==5,q)
  step(65);ck('Native muzzle lifetime and attack recovery clear their effects',p.evaluate("!boss._nw30.action&&!wm26Releases.some(f=>f.owner===boss&&f.family==='nw30wind')"))
  q=p.evaluate('''()=>{const old=NW30.base.projectile;let n=0;NW30.base.projectile=()=>{n++;return 'base';};try{return{value:drawCombatFinalProjectile({kind:'mg',x:50,y:50,vx:0,vy:1}),calls:n};}finally{NW30.base.projectile=old;}}''');ck('Other projectiles retain their existing renderer',q['value']=='base'and q['calls']==1)
  q=p.evaluate("""()=>{eBullets=[];nw30Shoot(boss,{kind:'gun',tx:player.x,ty:player.y,n:0,id:99});return eBullets.map(q=>({wind:enemyOrdnanceElement(q),intercept:enemyOrdnanceCanIntercept(q),marker:pw5Impact({...q,x:player.x,y:player.y-100,vx:0,vy:4},player)}));}""")
  ck('Gun rounds are Wind, unshootable, and have no collision marker',len(q)==2 and all(z['wind']=='wind' and not z['intercept'] and z['marker'] is None for z in q),q)
  p.evaluate("()=>{eBullets.forEach((q,i)=>{q.x=player.x+(i?25:-25);q.y=player.y-100;q.vx=0;q.vy=4;});pw5Collect();drawWorld(0);}");p.screenshot(path=str(W/'teal-gun-no-markers.png'))
  ck('Native scene has no game, draw or HTTP errors',not errors and not http,dict(errors=errors,http=http));b.close()
finally:stop()
print(len(checks),'native gust checks passed')
