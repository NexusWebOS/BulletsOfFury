from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import numpy as np,json,hashlib,io,subprocess
R=Path(__file__).resolve().parents[1];O=R/'_shots/pursuit_trace_exact_1115';S=R/'_ART_SOURCES/pursuit_trace_exact_1115'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=json.loads((S/'manifest.json').read_text(encoding='utf8'))
paths=[R/b['path']for b in M['banks'].values()]+[R/'assets/pursuit_trace_art_1115.js']
sources=[R/b['source']for b in M['banks'].values()]
before={str(p.relative_to(R)):digest(p)for p in paths+sources}
subprocess.run(['python',str(R/'_BUILD_SOURCE/pursuit_trace_exact_1115_build.py')],cwd=R,check=True,capture_output=True)
after={str(p.relative_to(R)):digest(p)for p in paths+sources}
assert before==after
repro={'allPagesRegistryAndSourcesByteIdentical':True,'sha256':after,'scope':'Default build exports retained Aseprite-format cels; it does not rewrite authored sources.'}
(O/'reproduction.json').write_text(json.dumps(repro,indent=2),encoding='utf8')
for path in ['assets/game.js','assets/city_rescue_1115.js','assets/pursuit_trace_art_1115.js']:
 subprocess.run(['node','--check',path],cwd=R,check=True)

def decoded(path):
 im=Image.open(path);out=[]
 for i in range(im.n_frames):
  im.seek(i);out.append((im.convert('RGB').copy(),im.info['duration']))
 return out
def timeline(frames):
 out=[]
 for im,ms in frames:out.extend([hashlib.sha256(im.tobytes()).hexdigest()]*(ms//10))
 return out
optimized=[]
for filename,total in [('pursuit-hard-highlight.gif',4000),('pursuit-furious-highlight.gif',4000),('pursuit-highlights.gif',8000)]:
 path=O/filename;originalBytes=path.stat().st_size;frames=decoded(path);colors=set()
 for im,ms in frames:
  a=np.asarray(im,dtype=np.uint32);packed=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];colors.update(np.unique(packed).tolist())
 assert len(colors)<=256
 lut=np.array(sorted(colors),dtype=np.uint32);pal=[]
 for c in lut:pal.extend([int(c>>16)&255,int(c>>8)&255,int(c)&255])
 pal.extend([0]*(768-len(pal)));out=[]
 for im,ms in frames:
  a=np.asarray(im,dtype=np.uint32);packed=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];idx=np.searchsorted(lut,packed);assert np.array_equal(lut[idx],packed)
  pim=Image.fromarray(idx.astype(np.uint8));pim.putpalette(pal);out.append(pim)
 buf=io.BytesIO();out[0].save(buf,format='GIF',save_all=True,append_images=out[1:],duration=[ms for im,ms in frames],optimize=True,disposal=1,loop=0)
 compact=decoded(io.BytesIO(buf.getvalue()));assert timeline(frames)==timeline(compact)
 assert all(im.size==(912,512)for im,ms in compact)and sum(ms for im,ms in compact)==total
 path.write_bytes(buf.getvalue());optimized.append({'file':filename,'beforeBytes':originalBytes,'afterBytes':len(buf.getvalue()),'frames':len(compact),'durationMs':total,'size':[912,512],'decodedTimingTimelineIdentical':True})
(O/'gif-optimization.json').write_text(json.dumps(optimized,indent=2),encoding='utf8')
(O/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF exact card-frame flash</title><style>body{max-width:1000px;margin:24px auto;padding:0 20px;background:#0b1420;color:#f4ecdb;font:17px/1.5 system-ui}img{max-width:100%;height:auto;image-rendering:pixelated}a{color:#9af2c1}section{margin:30px 0}</style><h1>Exact card-frame flash + arrow</h1><p>The original metal frame pixels now carry the pulse: raised top plates, side steps and bottom tabs. Hard first, then Furious. Real in-game left/right input; only the selected frame flashes.</p><section><img id="combined" src="pursuit-highlights.gif" alt="Native pursuit selections with exact frame highlights and existing arrow"></section><section><h2>Hard</h2><img id="hard" src="pursuit-hard-highlight.gif" alt="Hard pursuit exact frame pulse"></section><section><h2>Furious</h2><img id="furious" src="pursuit-furious-highlight.gif" alt="Furious pursuit exact frame pulse"></section><p><a href="../../docs/PURSUIT_TRACE_EXACT_1115.md">Sources and verification</a></p></html>''',encoding='utf8')
errors=[];checks=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1100,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8766/_shots/pursuit_trace_exact_1115/review.html');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth)')
 q=p.evaluate('Array.from(document.images).map(i=>({id:i.id,width:i.naturalWidth,height:i.naturalHeight}))')
 for a in q:checks.append({'name':a['id']+' GIF browser geometry','ok':a['width']==912 and a['height']==512,'data':a})
 hashes=[]
 for i in range(4):
  raw=p.locator('#combined').screenshot(animations='allow');hashes.append(hashlib.sha256(raw).hexdigest());(O/('browser-animation-'+str(i)+'.png')).write_bytes(raw);p.wait_for_timeout(350)
 checks.append({'name':'actual browser composited GIF frames change','ok':len(set(hashes))>=3,'data':hashes})
 p.screenshot(path=str(O/'browser-preview.png'),full_page=True)
 checks.append({'name':'no preview page/console/HTTP errors','ok':not errors,'data':errors});b.close()
assert all(c['ok']for c in checks)
(O/'browser-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Animated image element screenshots, not canvas default-image sampling.'},indent=2),encoding='utf8')
print(json.dumps({'reproduction':True,'syntax':True,'gif':optimized,'browserPassed':len(checks)},indent=2))
