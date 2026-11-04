from pathlib import Path
import sys,json,base64,hashlib
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';O=D/'verification/revision8';O.mkdir(parents=True,exist_ok=True)
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(D));import review_server
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
if '--installed' in sys.argv:review_server.INJECT='';review_server.OVERLAY=D/'_no_overlay'
checks=[];errors=[];missing=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else 'FAIL ')+name,flush=True)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('nativeCapture().toDataURL().split(",")[1]')))
port,stop=review_server.serve()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(e.stack))
  p.on('response',lambda r:missing.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.BOF_STORY_1103&&window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  # Read logical pixels even when the player's stored display setting is 2x.
  # Only the evidence canvas is resized; game rendering stays untouched.
  p.evaluate('''()=>{window.nativeCapture=()=>{const c=document.createElement('canvas');c.width=Math.round(cv.width/SS);c.height=Math.round(cv.height/SS);const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(cv,0,0,c.width,c.height);return c};window.nativePixels=(x,y,w,h)=>nativeCapture().getContext('2d').getImageData(x,y,w,h)}''')
  ck('Pixel divider and scrolling-panel revision loaded',p.evaluate('S113.revision')==8)
  for pilot in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']:
   p.evaluate('p=>S113.preview("post-4",p)',pilot)
   data=p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);s.t=1;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.draw();const a=nativePixels(0,388,912,16).data;let left=0,right=0,gray=0;for(let x=0;x<912;x++){const i=x*4,m=Math.max(a[i],a[i+1],a[i+2]);if(m>25){if(x<414)left++;if(x>498)right++;}const j=(12*912+x)*4;if(a[j]>45&&Math.abs(a[j]-a[j+1])<10&&Math.abs(a[j+1]-a[j+2])<10)gray++;}return{left,right,gray,comic:S113.last.comic,actor:S113.last.actor}}''')
   ck(pilot+' comic portraits reach gray footer without floating chest edge',data['left']>25 and data['right']>25 and data['gray']>800 and data['comic'] and data['actor']is None,data)
   shot(p,'comic-'+pilot)
  p.evaluate('S113.preview("post-4","cole")')
  for pose in ['typing','ecstatic','shock','recover','panic','duck']:
   data=p.evaluate('''pose=>{s113Viewport();ctx.setTransform(SS,0,0,SS,0,0);s113Bank('command-bay',0);const holo=nativePixels(310,210,350,150).data.slice(),seat=nativePixels(86,206,208,208).data.slice();s113Visual({s113:'command-bay',frame:0,actor:pose},1);const B=nativePixels(310,210,350,150).data,C=nativePixels(86,206,208,208).data;let holoChanges=0,seatChanges=0;for(let i=0;i<B.length;i+=4)if(B[i]!==holo[i]||B[i+1]!==holo[i+1]||B[i+2]!==holo[i+2])holoChanges++;for(let i=0;i<C.length;i+=4)if(C[i]!==seat[i]||C[i+1]!==seat[i+1]||C[i+2]!==seat[i+2])seatChanges++;return{holoChanges,seatChanges}}''',pose)
   ck('Decker '+pose+' occupies left workstation and leaves holo table untouched',data['holoChanges']==0 and data['seatChanges']>1000,data)
   shot(p,'decker-'+pose)
  p.evaluate('S113.preview("post-5","cole")')
  ck('Squad takeoff and alien descent are separate shots',p.evaluate("(()=>{const b=s113Script(5,'cole');return b.at(-2).s113==='hangar'&&b.at(-2).flight==='squad'&&b.at(-1).s113==='alien-descent'&&!b.at(-1).flight})()"))
  hashes=[]
  for frame in range(4):
   p.evaluate('f=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.s113==="alien-descent");s.t=f*1.6+.1;BOFCinematicDirector.draw()}',frame)
   shot(p,'alien-descent-'+str(frame));hashes.append(p.evaluate('cv.toDataURL()'))
  ck('Drone descent has four distinct native frames and no allied overlay',len(set(hashes))==4 and p.evaluate('S113.last.flight===undefined'))
  # Compare actual rendered pad pixels with and without the aircraft. Empty
  # sprite pixels must leave the pad unchanged, even inside the 128px cell.
  p.evaluate('''()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';beginStage(2);run.stage=2;setState(GS.FLYOVER);for(const p of S113.casts)XART.rdy('s113_landing-'+p);XART.rdy('s113_dish-exit');XART.rdy('s113_fade')}''')
  p.wait_for_function('S113.casts.map(p=>XART.rdy("s113_landing-"+p)).every(Boolean)&&XART.rdy("s113_dish-exit")&&XART.rdy("s113_fade")')
  for pilot in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']:
   data=p.evaluate('''pilot=>{run.pilot=pilot;S113.exit={t:10.3,wait:0,startX:340,startY:380,cam:0,done:false};ctx.setTransform(SS,0,0,SS,0,0);drawFlyover(0);const x=Math.round(S113.last.ship[0]-camX)-64,y=Math.round(S113.last.ship[1])-64;const A=nativePixels(x,y,128,128).data.slice(),saved=s113Bank;try{s113Bank=function(n,...args){if(n.startsWith('landing-'))return true;return saved(n,...args)};drawFlyover(0)}finally{s113Bank=saved}const B=nativePixels(x,y,128,128).data;const a=S113_ART.banks['landing-'+pilot],c=document.createElement('canvas');c.width=c.height=128;c.getContext('2d').drawImage(XART.get(a.key),31%a.cols*128,Math.floor(31/a.cols)*128,128,128,0,0,128,128);const mask=c.getContext('2d').getImageData(0,0,128,128).data;let changed=0,outside=0,opaque=0;for(let i=0;i<A.length;i+=4){if(mask[i+3])opaque++;if(A[i]!==B[i]||A[i+1]!==B[i+1]||A[i+2]!==B[i+2]){changed++;if(!mask[i+3])outside++;}}drawFlyover(0);return{changed,outside,opaque,cornerAlpha:mask[3]}}''',pilot)
   ck(pilot+' actual landing pad remains visible through empty ship pixels',data['outside']==0 and data['changed']>30 and data['opaque']<1000 and data['cornerAlpha']==0,data)
   shot(p,'landing-'+pilot)
  ck('No page or render exceptions',not errors,errors);ck('No missing scene assets',not missing,missing);br.close()
finally:stop()
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'errors':errors,'missing':missing,'checks':checks}
(O/('installed-report.json'if '--installed'in sys.argv else 'report.json')).write_text(json.dumps(report,indent=2))
selected=['comic-falva','decker-shock','alien-descent-3','landing-cole'];board=Image.new('RGB',(1824,1024),'#000')
for i,n in enumerate(selected):
 im=Image.open(O/(n+'.png')).convert('RGB');im.thumbnail((912,512));board.paste(im,(i%2*912+(912-im.width)//2,i//2*512+(512-im.height)//2))
board.save(D/'Four-shot-corrections.jpg',quality=96)
print(json.dumps({k:v for k,v in report.items()if k!='checks'}));raise SystemExit(not all(c['passed']for c in checks))
