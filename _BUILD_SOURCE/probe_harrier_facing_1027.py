from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,numpy as np,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/harrier_facing_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];console=[];http=[]
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks-partial.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert v,name
M=json.loads((R/'_ART_SOURCES/harrier_facing_1027/manifest.json').read_text(encoding='utf-8'))
for name,a in M['art'].items():
 if name.startswith('hit_'):continue
 im=np.array(Image.open(R/a['path']).convert('RGBA'));src=np.array(Image.open(R/a['source']).convert('RGBA'));mask=np.zeros(src.shape[:2],dtype=bool)
 for x,y,w,h in M['oldRects']:mask[y:y+h,x:x+w]=True
 for x,y in M['pivots']:mask[y-20:y+20,x-16:x+16]=True
 check(name+' keeps original hull pixels outside the four gun apertures',np.array_equal(im[~mask],src[~mask]))
 check(name+' preserves complete hull alpha and even dimensions',np.array_equal(im[:,:,3],src[:,:,3])and im.shape[:2]==(288,512))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof HF28!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000,polling=100);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';run.ngplus=false;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive',name:'Harrier south-facing start'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];for(const q of boss._carrier17.parts.filter(p=>p.kind==='gun'))q.angle=q.er28Bearing=q.muzzleAngle=.1;}")
  step(125);p.wait_for_timeout(1200);step(1);p.screenshot(path=str(W/'arrival.png'));before=p.evaluate("()=>({depth:boss._carrier17.depth,phase:boss._carrier17.phase,last:HF28.last,hp:boss.hp,max:boss.maxhp,angles:boss._carrier17.parts.filter(p=>p.kind==='gun').map(p=>p.er28Bearing)})")
  check('The real pre-modular arrival uses the south-facing whole hull',before['depth']and before['last']['screenFacing']=='south'and before['last']['art'].endswith('_south'),before)
  check('Pre-modular damage masks use matching full south-facing silhouettes',p.evaluate("[0,1,2,3].every(i=>XART.get('hh21_gun_'+i)===XART.get(HF28_ART['hit_'+i].key))"))
  for i in range(45):
   step(1)
   if p.evaluate('!boss._carrier17.depth&&boss._carrier17.phase==="fight"'):break
  landed=p.evaluate("()=>({handovers:HF28.handovers,phase:boss._carrier17.phase,hp:boss.hp,max:boss.maxhp,parts:boss._carrier17.parts.length,guns:boss._carrier17.parts.filter(p=>p.kind==='gun').map(p=>({angle:p.angle,bearing:p.er28Bearing,muzzle:p.muzzleAngle,age:p.muzzleAge}))})")
  check('All four modular guns begin at the same south-facing handover',landed['handovers']==1 and all(abs(g['bearing']-np.pi/2)<.0001 and g['angle']==g['muzzle']for g in landed['guns']),landed)
  check('Handover keeps the native ten modules and health budget',landed['parts']==10 and landed['max']==before['max']and landed['hp']==before['hp'])
  step(1);p.screenshot(path=str(W/'modular-handover.png'));step(4);check('The handover does not retrigger during ordinary fighting',p.evaluate('HF28.handovers===1'))
  p.evaluate("()=>{const C=boss._carrier17;C.phase='flyover';C.depth=true;C.t=1.95;C.scale=1.1;boss._noHit=true;}");step(1);p.screenshot(path=str(W/'return-flyover.png'));check('Return flyover also selects the south-facing hull',p.evaluate("HF28.last?.art==='hf28_closed_wells_south'||HF28.last?.art==='hf28_open_wells_south'"))
  for i in range(80):
   step(1)
   if p.evaluate('!boss._carrier17.depth&&boss._carrier17.phase==="fight"'):break
  check('A later flyover resets the gun handover south exactly once again',p.evaluate('HF28.handovers===2&&boss._carrier17.parts.filter(p=>p.kind==="gun").every(p=>p.er28Bearing===Math.PI/2)'))
  p.evaluate('''()=>{for(const g of boss._carrier17.parts.filter(p=>p.kind==='gun')){g.cool=99;g.phase='rest';g.angle=g.er28Bearing=g.muzzleAngle=Math.PI/2;} }''');step(1);p.screenshot(path=str(W/'south-facing-modules.png'))
  q=p.evaluate("()=>({targets:retinaBossTargets(boss).filter(q=>String(q._retinaId).includes('hullGun')).length,hit:boss._carrier17.parts.filter(p=>p.kind==='gun').every(g=>{const q=roster17Mount(boss,g);return roster17At(boss,q.x,q.y)===g.id})})");check('Independent live gun targets and actual opaque hits remain',q['targets']==4 and q['hit'],q)
  p.evaluate('''()=>{boss=null;bossActive=false;s6OpeningInit();s6Opening.phase='flyover';s6Opening.t=4;s6Opening.allT=12;s6Opening.carrierJets=[];}''');step(1);p.screenshot(path=str(W/'opening-north-flight.png'));opening=p.evaluate('HF28.last');check('The northbound opening flight uses compensated hull pixels to keep guns facing screen-south',opening['opening']and opening['screenFacing']=='south'and opening['art'].endswith('_north'),opening);check('Opening compensation is scoped and restored after draw',p.evaluate('!HF28.northPass'))
  p.evaluate('run.stage=7');check('Other stages retain their original carrier images',p.evaluate("XART.get('whv_closed_w')===HF28.base.get('whv_closed_w')"));check('No page, draw or HTTP errors',not errors and not console and not http,{'page':errors,'console':console,'http':http});br.close()
finally:
 stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'pageErrors':errors,'consoleErrors':console,'HTTPerrors':http},indent=2),encoding='utf-8')
print(f'{len(checks)} art/native checks passed.')
