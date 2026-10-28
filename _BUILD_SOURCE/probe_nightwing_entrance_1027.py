from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/nightwing_entrance_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];http=[];console=[];checks=[];points=[];seen=set()
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks-partial.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert v,name
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None);p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof NW28!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{run.ngplus=false;diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,kind:'warhive',role:'boss',name:'Whole Nightwing route'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;}")
  for i in range(50):
   step(30)
   if p.evaluate('boss?._carrier17?.phase==="fight"&&!boss._carrier17.depth'):break
  check('Harrier retains all ten native modular components',p.evaluate('boss._carrier17.parts.length===10'))
  p.evaluate('''()=>{const b=boss;NW28.events=[];s6Wing.ships=[];for(const g of b._carrier17.parts.slice()){if(g.dead)continue;b._carrier17.direct=g.id;_dmgBullet=null;hitBoss(g.hp+1);}window.nwGuns=0;window.nwMissiles=0;window.nwOldGuns=whvAceGuns;window.nwOldMissiles=whvAceFireMissiles;whvAceGuns=function(){nwGuns++;return nwOldGuns.apply(this,arguments)};whvAceFireMissiles=function(){nwMissiles++;return nwOldMissiles.apply(this,arguments)};}''')
  for i in range(160):
   step(5);q=p.evaluate('''()=>{const b=boss,A=b?._whv?.ace,M=A?._nw28;return M?{mode:M.mode,t:M.t,heading:M.heading,x:A.x,y:A.y,bx:b.x,by:b.y,hp:b.hp,maxhp:b.maxhp,stored:b._whv.aceMax,st:A.st,targets:retinaBossTargets(b).length,invuln:whvAceInvuln(A),hit:warhiveHitTest(b,A.x,A.y),modular:b.modular,hasPartFl:!!A.fl,guns:nwGuns,missiles:nwMissiles,whole:NW28.last}:null}''')
   if not q:continue
   points.append(q)
   if q['mode']=='south'and q['t']<.5 and'pause'not in seen:
    old=q['t'];p.evaluate("setState('paused')");step(20);check('Pause holds the entrance simulation clock',p.evaluate('boss._whv.ace._nw28.t')==old);p.evaluate('setState(GS.PLAY)');seen.add('pause')
    hp=q['hp'];p.evaluate('()=>{_dmgBullet=null;hitBoss(900)}');check('Direct locked damage cannot hurt the protected entrance',p.evaluate('boss.hp')==hp)
   if q['mode']in ['south','north','return','settle','fight']and q['t']>(.45 if q['mode']!='settle'else .15)and q['mode']not in seen:
    p.wait_for_timeout(350);step(1);p.screenshot(path=str(W/('route-'+q['mode']+'.png')));seen.add(q['mode'])
   if q['mode']=='fight':break
  modes=[]
  for q in points:
   if not modes or modes[-1]!=q['mode']:modes.append(q['mode'])
  check('The complete south exit, corner north pass and south-facing return occur in order',modes==['south','south_wait','north','north_wait','return','settle','fight'],modes)
  north=[q for q in points if q['mode']=='north'];check('The north pass is vertical at one corner and exits north',len(north)>8 and max(q['x']for q in north)-min(q['x']for q in north)<.01 and north[-1]['y']<0 and all(b['y']<a['y']for a,b in zip(north,north[1:])))
  returns=[q for q in points if q['mode']=='return'];check('The returning ship faces south and advances down from the top',len(returns)>6 and all(q['heading']=='south'for q in returns)and all(b['y']>=a['y']for a,b in zip(returns,returns[1:])))
  intro=[q for q in points if q['mode']!='fight'];check('Every entrance beat protects the whole hull and hides Retina targets',all(q['invuln']and not q['hit']and q['targets']==0 for q in intro))
  check('No Nightwing guns or missiles fire before the return completes',all(q['guns']==q['missiles']==0 for q in intro))
  check('The complete original Nightwing life survives the entrance unchanged',all(q['hp']==q['maxhp']==q['stored']for q in points))
  fight=points[-1];check('Combat begins in the upper half with one live whole-hull target',fight['targets']==1 and fight['hit']and not fight['modular']and not fight['hasPartFl']and fight['y']<256,fight)
  step(80);p.screenshot(path=str(W/'whole-fighting.png'))
  # The whole body draw is exactly one sprite blit even during movement and hit.
  draws=p.evaluate('''()=>{const b=boss,A=b._whv.ace,save={roll:A.roll,somer:A.somer,inverted:A.inverted,vx:A.vx};A.dash=A.desp=A._pw5Gun=A._ra7Gate=null;const out=[];for(const pose of['idle','roll','somer','inverted']){A.roll=pose==='roll'?{t:.2,dir:1}:null;A.somer=pose==='somer'?{t:.22}:null;A.inverted=pose==='inverted';A.vx=0;let n=0;const old=ctx.drawImage;ctx.drawImage=function(im){if(im===XART.get(NW28_ART.whole.key)||im===XART.get(NW28_ART.whole_hit.key))n++;return old.apply(this,arguments)};whvDrawAce(b);ctx.drawImage=old;out.push({pose,blits:n,frame:NW28.last.frame});}Object.assign(A,save);return out}''');check('Idle, roll, somersault and inverted poses each draw one complete ship',all(q['blits']==1 for q in draws),draws)
  p.evaluate('''()=>{const A=boss._whv.ace;A.roll=A.somer=A.dash=A.desp=A._pw5Gun=A._ra7Gate=null;A.inverted=false;A.vx=0;A.gunCd=A.mslCd=A.rollCd=A.somerCd=A.dashCd=A._ra7Cd=99;boss.flash=0;}''');step(1)
  sample='''()=>{const A=boss._whv.ace,d=ctx.getImageData(Math.floor(A.x-camLeftX()-90),Math.floor(A.y-85),180,170).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>245&&d[i+1]>245&&d[i+2]>245)white++;return{white,hp:boss.hp,flash:boss.flash}}'''
  before=p.evaluate(sample);p.evaluate('()=>{_dmgBullet=null;hitBoss(9)}');step(1);after=p.evaluate(sample);check('A real body hit damages one pool and flashes the full ship',after['hp']<before['hp']and after['white']>before['white']+1500,{'before':before,'after':after});p.screenshot(path=str(W/'whole-hit.png'));step(22);expired=p.evaluate(sample);check('Whole-ship flash expires without split wing/body remnants',expired['flash']==0 and expired['white']<after['white']and p.evaluate('!boss._whv.ace.fl'),expired)
  p.evaluate('()=>{const A=boss._whv.ace;A.gunCd=.1;A.mslCd=1;A._ra7Cd=.5;}');step(300);check('Native patterns resume after the new entrance',p.evaluate('nwGuns+nwMissiles>0||RA7.events.some(q=>q.event==="aceGateVolley")'),p.evaluate('({guns:nwGuns,missiles:nwMissiles,volleys:RA7.events.filter(q=>q.event==="aceGateVolley").length})'))
  p.evaluate('()=>{_dmgBullet=null;hitBoss(boss.hp+1)}');step(30);check('Native death uses the whole authored spin bank',p.evaluate('boss.dead&&NW28.last.frame>=NW28_ART.groups.death.start'));p.screenshot(path=str(W/'whole-death.png'));step(400);check('Normal final defeat still exits the encounter',p.evaluate('bossDefeated'))
  check('No page, draw or HTTP errors',not errors and not console and not http,{'page':errors,'console':console,'http':http});br.close()
finally:
 stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'route':points,'pageErrors':errors,'HTTPerrors':http,'consoleErrors':console},indent=2),encoding='utf-8')
print(f'{len(checks)} native checks passed.')
