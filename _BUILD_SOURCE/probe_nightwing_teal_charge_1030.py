from pathlib import Path
from PIL import Image
import json,sys,http.server,math,numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_teal_charge_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_stability_1028/original-metadata.json').read_text());D=R/'assets/game/levels/stage_06/boss/nightwing_stability_1028'
def cell(im,cw,ch,cols,f):return im.crop((f%cols*cw,f//cols*ch,f%cols*cw+cw,f//cols*ch+ch))
old=Image.open(R/M['banks']['clean']['path']).convert('RGBA');glow=Image.open(D/'clean_charge.png').convert('RGBA')
ck('Every six-step glow frame preserves the exact approved hull silhouette',all(cell(old,272,272,8,f).getchannel('A').tobytes()==cell(glow,272,272,6,l*3+(2 if f==16 else 1 if f>=8 else 0)).getchannel('A').tobytes()for l in range(6)for f in range(17)))
a=np.asarray(cell(old,272,272,8,0));b=np.asarray(cell(glow,272,272,6,15));mask=a[:,:,3]>0;ck('Charge brightens actual teal armor pixels without adding halo pixels',int(np.sum(np.any(a[:,:,:3]!=b[:,:,:3],axis=2)&mask))>1500)
oldg=Image.open(R/M['banks']['wind_bullet']['path']).convert('RGBA');newg=Image.open(D/'wind_gust.png').convert('RGBA');counts=[]
for f in range(16):
 a=np.asarray(cell(oldg,64,64,16,f));b=np.asarray(cell(newg,96,96,16,f));counts.append([int(np.sum(a[:,:,3]>100)),int(np.sum(b[:,:,3]>100)),int(np.sum((a[:,:,:3].max(2)>220)&(a[:,:,3]>100))),int(np.sum((b[:,:,:3].max(2)>220)&(b[:,:,3]>100)))])
ck('All16 wind frames have more visible area and brighter highlights',all(b>a*1.8 and d>c for a,b,c,d in counts),counts)
N=R/'assets/game/levels/stage_06/boss/nightwing_teal_charge_1030'
for name in ['wind_rear','wind_front']:
 new=Image.open(N/(name+'.png')).convert('RGBA');ck(name+' has24 fixed336px cells at87.5percent size',new.size==(2688,1008))
 for f in range(24):
  source=cell(Image.open(D/(name+'.png')).convert('RGBA'),384,384,8,f).getbbox();target=cell(new,336,336,8,f).getbbox()
  assert source and target and max(abs(target[i]-source[i]*.875)for i in range(4))<2
 ck(name+' retains the exact24-phase vortex proportions and center',True)
aura=Image.open(N/'wind_aura.png').convert('RGBA');areas=[]
for level in range(6):
 for pose,f in enumerate([0,8,16]):
  aa=np.asarray(cell(aura,272,272,6,level*3+pose));base=np.asarray(cell(old,272,272,8,f));mask=aa[:,:,3]>0
  assert not np.any(mask&(base[:,:,3]>0))
  if level==0:assert not np.any(mask)
  else:assert np.sum(mask)>400 and np.all(aa[:,:,1][mask]>aa[:,:,0][mask]) and np.all(aa[:,:,1][mask]>aa[:,:,2][mask])
 areas.append(int(np.sum(np.asarray(cell(aura,272,272,6,level*3))[:,:,3]>0)))
ck('Teal outline preserves all real hit/body pixels across every damage pose',True)
ck('Six authored aura levels progress from off to a stronger energy silhouette',areas[0]==0 and all(b>a for a,b in zip(areas,areas[1:])),areas)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None);p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);}")
  rows=[]
  for i in range(480):
   step(1);rows.append(p.evaluate('''()=>{const A=boss._whv.ace,p=nw30Pose(boss);return{x:A.x,y:A.y,mode:A._nw28.mode,frame:p.frame,bank:p.bank,angle:p.meta.angle,scale:p.meta.scale,inv:whvAceInvuln(A)};}'''))
  (W/'entry-trace.json').write_text(json.dumps(rows,indent=2));active=[q for q in rows if q['mode']in ['north','return']and q['bank']=='heading'];ck('Both arrival curves select one stable64-heading family',len(active)>180 and all(q['frame']<64 for q in active))
  jumps=[]
  for a,b in zip(rows,rows[1:]):
   if a['mode']==b['mode']and a['mode']in ['north','return']and -100<a['y']<780 and -100<b['y']<780:
    jumps.append((math.hypot(b['x']-a['x'],b['y']-a['y']),abs(math.atan2(math.sin(b['angle']-a['angle']),math.cos(b['angle']-a['angle'])))))
  ck('Arrival has bounded per-frame translation and no direction flipping',max(d for d,a in jumps)<18 and max(a for d,a in jumps)<.21,dict(maxPixels=max(d for d,a in jumps),maxDegrees=math.degrees(max(a for d,a in jumps))))
  ck('Arrival finishes with one native target and intact HP',p.evaluate('boss._whv.ace._nw28.mode==="fight"&&retinaBossTargets(boss).length===1&&!boss.modular&&boss.hp>0'))
  # Controlled dash warning must rotate gradually, ending on its committed lane.
  p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.roll=A.somer=A.desp=null;A.inverted=false;A.x=camLeftX()+viewW()/2;A.y=180;A._nw32Yaw=Math.PI/2;player.x=camLeftX()+viewW()*.8;player.y=VH-70;A.dash={st:'warn',t:0};nf29Begin(b);}''');head=[]
  for i in range(55):step(1);head.append(p.evaluate('nw30Pose(boss).meta.angle'))
  ck('Dash windup turns through sequential authored headings',max(abs(math.atan2(math.sin(b-a),math.cos(b-a)))for a,b in zip(head,head[1:]))<.21 and len(set(head))>=2)
  step(350);ck('Flyover, banked drift and approach still complete',p.evaluate('NF29.events.some(e=>e.event==="charge-drift")&&NF29.events.some(e=>e.event==="charge-approach")&&NF29.events.some(e=>e.event==="charge-complete")'))
  p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A._nw28.mode='fight';A.st='fight';A.roll=A.somer=A.dash=A.desp=null;A.inverted=false;A.vx=A.vy=0;A.x=camLeftX()+viewW()/2;A.y=190;nf29Sync(b);nw30Start(b,'wind');b._nw30.action.t=1.65;b.flash=0;window.calls=[];window.nativeBlit=ctx.drawImage;ctx.drawImage=function(im,...a){for(const[k,b]of Object.entries(NW32_ART))if(im===XART.get(b.key))calls.push({bank:k,a});return nativeBlit.call(this,im,...a);};drawWorld(0);SC12.refresh();__bofFit();}''')
  q=p.evaluate('({calls,level:nw32Glow(boss),dim:NW30.dim})');ck('Native charge draws smaller centered vortex with armor and teal outline',{'wind_rear','wind_front','clean_charge','wind_aura'}.issubset({c['bank']for c in q['calls']})and q['level']>=4 and q['dim']>0,q)
  ck('Vortex uses fixed336px native blits while hull aura uses272px',all(c['a'][-2:]==[336,336]for c in q['calls']if c['bank']in ['wind_rear','wind_front'])and all(c['a'][-2:]==[272,272]for c in q['calls']if c['bank']=='wind_aura'));p.screenshot(path=str(W/'wind-charge-native.png'))
  p.evaluate('''()=>{calls=[];boss._gp4FlashNext=0;markHit(boss);nw28DrawBody(boss);}''');ck('Real accepted hit flash takes precedence over charge color',p.evaluate('boss.flash>0&&!calls.some(c=>c.bank==="clean_charge")'))
  ck('Teal wind energy remains visible around the actual white hit flash',p.evaluate('boss.flash>0&&calls.some(c=>c.bank==="wind_aura")'));p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/'wind-hit-native.png'));step(24);ck('Hit timer still expires during charge/fire',p.evaluate('boss.flash===0'))
  p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.dash=A.roll=A.somer=A.desp=null;A._nw28.mode='fight';A.st='fight';nw30Start(b,'gun');b._nw30.action.t=.7;b.flash=0;calls=[];nw28DrawBody(b);}''');ck('Retina machine-gun warning also lights the actual armor',p.evaluate('calls.some(c=>c.bank==="clean_charge")&&nw32Glow(boss)>0'))
  p.evaluate('''()=>{const b=boss;nw30Cancel(b);nw30Start(b,'wind');const C=b._nw30.action;C.tx=player.x;C.ty=player.y;nw30Shoot(b,C);calls=[];for(const q of eBullets.filter(q=>q._nw30Wind&&!q.dead))drawCombatFinalProjectile(q);drawWorld(0);SC12.refresh();__bofFit();}''');q=p.evaluate('''()=>({n:eBullets.filter(q=>q._nw30Wind&&!q.dead).length,draws:calls.filter(c=>c.bank==='wind_gust'),safe:eBullets.filter(q=>q._nw30Wind&&!q.dead).every(q=>!enemyOrdnanceCanIntercept(q)),ports:NW30.events.filter(e=>e.event==='turret-shot').slice(-2)})''');ck('Six wind rounds leave the real dual barrels with unchanged collision policy',q['n']>=6 and q['safe']and len(q['ports'])==2,q)
  ck('Wind rounds use96px fixed directional frames',len(q['draws'])>=6 and all(c['a'][-2:]==[96,96]for c in q['draws']),q['draws'][:1]);step(25);p.screenshot(path=str(W/'wind-rounds-native.png'))
  p.evaluate('''()=>{nw30Cancel(boss);calls=[];nw28DrawBody(boss);}''');ck('Charge effects and armor glow stop with their attack',p.evaluate('!calls.some(c=>["clean_charge","wind_front","wind_rear","wind_aura"].includes(c.bank))'))
  p.evaluate('ctx.drawImage=nativeBlit');ck('No native game, draw or asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(len(checks),'Nightwing visibility and flight checks passed')
