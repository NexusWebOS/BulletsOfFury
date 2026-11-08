from pathlib import Path
import json,sys,time,subprocess
from PIL import Image
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');Q=R/'_shots/locked_pilot_1106';Q.mkdir(parents=True,exist_ok=True);checks=[];m=json.loads((W/'manifest.json').read_text())
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:120]if d is not None else'',flush=True)
for name,a in m['banks'].items():
 im=Image.open(W/'exports'/Path(a['path']).name).convert('RGBA');left=im.crop((0,0,a['w'],a['h']));right=im.crop((a['w'],0,a['w']*2,a['h']));colors={p[:3]for p in im.getdata()if p[3]};alphas={p[3]for p in im.getdata()}
 ck(name+' has exact black/gray opaque pixels and identical fixed alpha',colors=={(0,0,0),(96,96,96)}and alphas<={0,255}and left.getchannel('A').tobytes()==right.getchannel('A').tobytes()and not a['w']%2 and not a['h']%2)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R));errors=[];missing=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:missing.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high');p.wait_for_function('window.__bofFrames>3',timeout=180000);p.evaluate(TRAP_RAF)
  p.wait_for_function('()=>Object.values(LP116.banks).every(a=>XART.rdy(a.key))&&pm27Live()',polling=100,timeout=90000)
  p.evaluate("()=>{coleUnlocked=coleSessionUnlocked=false;run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');pilotFrom=pilotIndex;pilotPending=null;pilotRot=0;Input.mouse.down=false;setState(GS.PILOT);_setPilotViewport();ctx.setTransform(SS,0,0,SS,0,0);}")
  def frame(t,name):
   d=p.evaluate('''t=>{stateT=t;ctx.setTransform(SS,0,0,SS,0,0);drawPilot(1/60);return {card:LP116.lastCard,mini:LP116.lastMini,locked:isPilotLocked(PILOTS[pilotIndex]),width:cv.width,height:cv.height,ss:SS};}''',t);p.screenshot(path=str(Q/(name+'.png')));return d
  gray=frame(.1,'locked-gray');black=frame(.55,'locked-black');again=frame(1,'locked-gray-return')
  neutral=p.evaluate('''()=>{const out=[];for(const t of [.1,.55]){stateT=t;ctx.setTransform(SS,0,0,SS,0,0);drawPilot(0);const samples=[[4,4],[30,180]].map(([x,y])=>Array.from(ctx.getImageData(x*SS,y*SS,1,1).data));out.push({t,background:lp116Background(),panel:lp116Panel(),samples});}return out;}''')
  ck('Locked Cole background and card use contrasting black/gray phases',all(v[0]==v[1]==v[2]for r in neutral for v in r['samples'])and neutral[0]['background']=='#000000'and neutral[1]['background']=='#484848',neutral)
  ck('Native card and roster switch gray-black-gray together',gray['card']['phase']==gray['mini']['phase']==0 and black['card']['phase']==black['mini']['phase']==1 and again['card']['phase']==again['mini']['phase']==0)
  ck('Main card draws both Cole and actual jet plus a lock',all(gray['card'][k]is not None for k in ['body','ship','lock']))
  def inside(q,box):return q['x']>=box[0]and q['y']>=box[1]and q['x']+q['w']<=box[0]+box[2]and q['y']+q['h']<=box[1]+box[3]
  ck('All large silhouettes remain inside the wide card',all(inside(gray['card'][k],gray['card']['box'])for k in ['body','ship','lock']))
  blocked=p.evaluate('()=>{const was=state;confirmPilot();return state===was&&pilotPending===null&&isPilotLocked(PILOTS[pilotIndex]);}');ck('Locked Cole still refuses deployment',blocked)
  p.set_viewport_size({'width':480,'height':512});p.evaluate('()=>{_setPilotViewport();ctx.setTransform(SS,0,0,SS,0,0)}');small=frame(.1,'locked-native-480')
  ck('Native 480 layout uses the small jet without clipping',small['card']['ship']['id']=='ship_small'and all(inside(small['card'][k],small['card']['box'])for k in ['body','ship','lock']))
  p.set_viewport_size({'width':390,'height':844});p.evaluate('()=>{_setPilotViewport();ctx.setTransform(SS,0,0,SS,0,0)}');phone=frame(.55,'locked-portrait')
  ck('Portrait layout retains both silhouettes and lock',all(inside(phone['card'][k],phone['card']['box'])for k in ['body','ship','lock']))
  p.set_viewport_size({'width':1280,'height':800});p.evaluate('()=>{_setPilotViewport();ctx.setTransform(SS,0,0,SS,0,0);pwInput="COLE4U";submitPassword();setState(GS.PILOT);pilotRot=0;pilotPending=null;}')
  p.wait_for_function('()=>XART.rdy(psBodyKey("cole"))&&XART.rdy(psShipKey("cole",null))',polling=100,timeout=90000)
  result=p.evaluate('''()=>{stateT=.2;const before=LP116.draws;for(let i=0;i<8;i++)drawPilot(.6);return {unlocked:!isPilotLocked(PILOTS[pilotIndex]),session:coleSessionUnlocked,shadowDraws:LP116.draws-before};}''');p.screenshot(path=str(Q/'cole-unlocked.png'))
  ck('Real COLE4U password restores full-color artwork and stops silhouette rendering',result['unlocked']and result['session']and result['shadowDraws']==0,result)
  other=p.evaluate('''()=>{coleUnlocked=coleSessionUnlocked=false;pilotIndex=0;pilotRot=0;stateT=1;const before=LP116.draws;drawPilot(.5);return {pilot:PT11_UI.card.pilot,locked:!!PT11_UI.card.locked,delta:LP116.draws-before};}''')
  ck('Other selected pilots keep their original card',other['pilot']=='axel'and not other['locked'])
  ck('No runtime errors or missing game assets',not errors and not missing,{'errors':errors,'missing':missing});b.close()
finally:
 stop();(Q/'checks.json').write_text(json.dumps(checks,indent=2));(W/'verification.json').write_text(json.dumps({'directory':str(Q),'checks':checks},indent=2))
if any(not x['passed']for x in checks):raise SystemExit(1)
