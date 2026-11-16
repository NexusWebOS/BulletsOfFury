from pathlib import Path
import json,sys,hashlib,base64,io
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_animation_1115';sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL',name,str(data)[:900],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq20qa');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{diffKey='hard';run.mode='campaign';D1110.preview('post-5','cole');}");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 pilots=p.evaluate('HQ19_PILOTS');meta=p.evaluate('HQ20_ART');ck('complete actual nine-pilot animation roster',set(meta['pilots'])==set(pilots))
 for pk in pilots:
  a=meta['pilots'][pk];im=Image.open(ROOT/a['path']).convert('RGBA');alpha=set(im.getchannel('A').getdata());ck(pk+' fixed even cells and clean binary alpha',im.size==(1536,1536)and a['w']==a['h']==384 and alpha=={0,255})
  for kind in ['walk','cheer']:
   hashes=[]
   for f in range(8):
    out=p.evaluate("([pk,kind,f])=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#182a39';ctx.fillRect(0,0,912,512);const a=hq20Performance(pk,kind,(f+.01)/(kind==='walk'?10:6),200,400,300),data=ctx.getImageData(16,80,768,768).data;let h=2166136261;for(const v of data)h=Math.imul(h^v,16777619);return{a,hash:h>>>0,png:f===0?cv.toDataURL('image/png'):null};}",[pk,kind,f]);hashes.append(out['hash'])
    if f==0:
     raw=Image.open(io.BytesIO(base64.b64decode(out['png'].split(',')[1]))).convert('RGB');live=raw.crop((16,80,784,848)).resize((384,384),Image.Resampling.NEAREST)
     k=0 if kind=='walk' else 8;src=im.crop((k%4*384,k//4*384,(k%4+1)*384,(k//4+1)*384));expected=Image.new('RGB',(384,384),'#182a39');expected.paste(src,mask=src.getchannel('A'))
     diff=ImageChops.difference(live,expected);ck(pk+' '+kind+' actual rendered pixels match accepted source',not diff.getbbox(),diff.getbbox())
   ck(pk+' '+kind+' eight distinct actual rendered poses',len(set(hashes))==8,hashes)
  p.evaluate('pk=>{run.pilot=pk;pilotIndex=PILOTS.findIndex(x=>x.key===pk);}',pk)
  for mode,t in [('corridor',2.1),('welcome',3.3)]:
   data=p.evaluate("([mode,t])=>{const b=hq19Rows(run.pilot).find(x=>x.hq19===mode);d1110Visual(b,{t,shown:0,i:0,id:'hq20-native'});return HQ19.last;}",[mode,t]);ck(pk+' '+mode+' uses new generated performance bank',any(x['pilot']==pk and x['key']==a['key']for x in data['cast']))
   p.locator('#screen').screenshot(path=str(OUT/(pk+'-'+mode+'.png')))
 # Check the actual baked door pixels: fixed world, progressively exposed opening.
 a=meta['door'];sheet=Image.open(ROOT/a['path']).convert('RGB');frames=[sheet.crop((i%4*418,i//4*236,i%4*418+418,i//4*236+236))for i in range(16)];hashes=[];outside=[];gaps=[]
 for i,f in enumerate(frames):
  h=f.copy();h.paste((0,0,0),tuple(a['aperture']));outside.append(hashlib.sha256(h.tobytes()).hexdigest());hashes.append(hashlib.sha256(f.tobytes()).hexdigest())
  openrow=list(frames[-1].crop((176,101,242,102)).getdata());row=list(f.crop((176,101,242,102)).getdata());gaps.append(sum(x==y for x,y in zip(row,openrow)))
 ck('all sixteen door frames physically differ',len(set(hashes))==16)
 ck('every exterior pixel outside doorway stays fixed',len(set(outside))==1)
 ck('door exposes the open hangar progressively',all(x<=y for x,y in zip(gaps,gaps[1:]))and gaps[-1]==66 and gaps[0]<8,gaps)
 # Current scene screenshots show opening, counterfire, explosions and individual exits.
 for mode,t,label in [('enter',2.1,'doors-half-open'),('enter',3.2,'doors-open'),('launch',3.2,'departure-southwest'),('launch',6.0,'departure-southeast'),('quiet',3.0,'quiet-base'),('escape-decker',3.8,'guard-counterfire'),('escape-decker',4.3,'guard-takedown'),('escape-decker',8.4,'six-enemies-defeated'),('escape-axel',.5,'decker-southeast-exit'),('escape-axel',3.0,'axel-southwest-exit')]:
  data=p.evaluate("([mode,t])=>{run.pilot='cole';const b=hq19Rows(run.pilot).find(x=>x.hq19===mode);d1110Visual(b,{t,shown:999,i:0,id:'hq20-native'});return HQ19.last;}",[mode,t]);p.locator('#screen').screenshot(path=str(OUT/(label+'.png')))
  if mode=='escape-decker'and t==3.8:ck('native scene visibly includes Decker tracers from his nose',bool(data['friendlyShots'])and any(x['pilot']=='decker'for x in data['friendlyShots']),data['friendlyShots'])
  if mode=='escape-decker'and t==4.3:ck('first enemy removed at the actual blast location',data['kills']and not any(x['id']==0 for x in data['enemies']),data['kills'])
 ck('original five-second empty-base interval retained',next(x for x in p.evaluate('hq19Rows(run.pilot).map(b=>({mode:b.hq19,duration:b.duration}))')if x['mode']=='quiet')['duration']==5)
 ck('no page console or HTTP errors',not errors,errors);b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(x['ok']for x in checks))+'/'+str(len(checks))+' native checks',flush=True);assert all(x['ok']for x in checks)
