from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');C=ROOT/'_shots/hq_turns_1115';OUT=ROOT/'_shots/hq_turns_1115';sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:800],flush=True)
meta=json.loads((C/'art-manifest.json').read_text(encoding='utf8'))
for pk,a in meta['pilots'].items():
 im=Image.open(ROOT/a['path']).convert('RGBA');hashes=[];exact=True;minMargin=256
 for f in range(20):
  cell=im.crop((f%5*256,f//5*256,f%5*256+256,f//5*256+256));src=Image.open(ROOT/'_ART_SOURCES/hq_turns_1115'/pk/('%02d.png'%f)).convert('RGBA');exact=exact and not ImageChops.difference(cell,src).getbbox();hashes.append(hashlib.sha256(cell.tobytes()).hexdigest());b=cell.getbbox();minMargin=min(minMargin,b[0],b[1],256-b[2],256-b[3])
 ck(pk+' twenty distinct actual banked heading/exhaust cells',len(set(hashes))==20 and len({x['sourceKey']for x in a['poses']})>=2)
 ck(pk+' native exports exact, even and unclipped',exact and im.size==(1280,1024)and minMargin>=4,{'margin':minMargin})
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq21qa');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate("()=>{diffKey='hard';D1110.preview('post-5','cole');}");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 data=p.evaluate('''()=>{const k=Math.max(888/418,488/236),r={x:12,y:12+(488-236*k)/2,w:418*k,h:236*k},order=[...HQ19_SQUAD,'decker','axel'],out=[];
 const oldRotate=ctx.rotate,oldDraw=ctx.drawImage,oldGet=XART.get,tags=new WeakMap();let rotations=0,blits=[];
 XART.get=function(key){const im=oldGet.apply(this,arguments);if(im)tags.set(im,key);return im;};ctx.rotate=function(a){rotations++;return oldRotate.apply(this,arguments);};ctx.drawImage=function(im,...args){blits.push({key:tags.get(im),args});return oldDraw.call(this,im,...args);};
 try{for(let index=0;index<order.length;index++){const pk=order[index],last=HQ20_KILLS.filter(q=>q.pilot===pk).at(-1),side=pk==='decker'?-1:1;let origin=null;
  if(last){const x=r.x+r.w*.5+side*r.w*.13,y=r.y+r.h*.727+18,e=hq20EnemyPose(last.id,3.4+last.at,r);origin={x,y,h:96,heading:Math.atan2(e.y-y,e.x-x)+Math.PI/2};}
  const poses=[];for(let f=0;f<20;f++){rotations=0;blits=[];const q=hq19Launch(pk,(f+.01)/20*1.3,0,index,r,origin);poses.push({q,rotations,blits});}out.push({pk,poses});}
 }finally{ctx.rotate=oldRotate;ctx.drawImage=oldDraw;XART.get=oldGet;}return out;}''')
 for row in data:
  a=meta['pilots'][row['pk']];ck(row['pk']+' native playback advances all twenty atlas cells without rotating a static hull',all(q['q']['turnFrame']==f and q['rotations']==0 and len(q['blits'])==1 and q['blits'][0]['key']==a['key'] and q['blits'][0]['args'][:2]==[f%5*256,f//5*256]for f,q in enumerate(row['poses'])))
  ck(row['pk']+' actual takeoff time halved',all(q['q']['duration']==1.3 for q in row['poses']))
 for mode,t,name in [('launch',2.35,'cole-turn'),('launch',3.85,'maverick-turn'),('launch',6.85,'juggernaut-turn'),('escape-decker',2.75,'guard-bank'),('escape-decker',9.35,'decker-fast-exit'),('escape-axel',1.25,'axel-fast-exit')]:
  p.evaluate("([mode,t])=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.hq19===mode);s.t=t;s.shown=999;d1110Visual(s.beats[s.i],s);}",[mode,t]);p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
 variant=p.evaluate("()=>{applyLizzieSkin(true);const r={x:12,y:5,w:888,h:501};return hq19Launch('lizzie',.55,0,5,r);}");ck('Lizzie alternate uses its actual B42 turn bank',variant['key']=='hq21_turn_lizzie_b42');p.evaluate('applyLizzieSkin(false)')
 ck('first launch sequence shortened to12.6 seconds',p.evaluate("hq19Rows(run.pilot).find(b=>b.hq19==='launch').duration===12.6"))
 ck('five-second pause and six counterattack kills retained',p.evaluate("hq19Rows(run.pilot).find(b=>b.hq19==='quiet').duration===5&&HQ20_KILLS.length===6"))
 ck('no native browser errors',not errors,errors);b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'nativeTurnSamples':data},indent=2),encoding='utf8');print(sum(c['ok']for c in checks),'/',len(checks),'native turn checks');assert all(c['ok']for c in checks)
