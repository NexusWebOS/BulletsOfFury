from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import re,json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/registry-bounds';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
html=(R/'index.html').read_text(encoding='utf8');names=set()
for url in re.findall(r'<script[^>]+src=["\x27]([^"\x27]+)',html):
 f=R/url.split('?')[0]
 if f.exists():names.update(re.findall(r'\b(?:const|let|var)\s+([A-Z][A-Z0-9_]*_ART)\s*=',f.read_text(encoding='utf8',errors='replace')))
errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://127.0.0.1:8765/index.html?night-registry-bounds=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 data=p.evaluate('''names=>{const banks=[],seenNames=[],missing=[];function path(key){const root=XART.root?XART.root(key):key;return{key,root,path:XART._src[root]||BOFX.img?.[root]||XART._src[key]||BOFX.img?.[key]||null,cell:BOFX.cells?.[key]||BOFX.playercells?.[key]||null};}for(const name of names){let root;try{root=eval(name)}catch(e){missing.push(name);continue}seenNames.push(name);const seen=new WeakSet();function visit(a,label,depth){if(!a||typeof a!=='object'||depth>7||seen.has(a))return;seen.add(a);const W=a.cw||a.w||(Array.isArray(a.cell)?a.cell[0]:a.cell),H=a.ch||a.h||(Array.isArray(a.cell)?a.cell[1]:a.cell);if(Number.isFinite(W)&&Number.isFinite(H)&&W>0&&H>0){if(Array.isArray(a.cells)&&a.cells.length&&a.cells.every(c=>Array.isArray(c)&&typeof c[0]==='string'&&Number.isFinite(c[1])&&Number.isFinite(c[2]))){banks.push({label,type:'paged',W,H,rects:a.cells.map((c,i)=>({i,...path(c[0]),rect:[c[1],c[2],Number.isFinite(c[3])?c[3]:W,Number.isFinite(c[4])?c[4]:H]}))});return;}const count=Number.isFinite(a.frames)?a.frames:a.count,cols=a.cols||a.columns;if(typeof a.key==='string'&&Number.isFinite(count)&&count>0&&count<=4096&&Number.isFinite(cols)&&cols>0){banks.push({label,type:'grid',W,H,count,cols,rects:Array.from({length:count},(_,i)=>{const page=Array.isArray(a.pages)?a.pages.find(p=>typeof p.key==='string'&&Number.isFinite(p.start)&&Number.isFinite(p.frames)&&i>=p.start&&i<p.start+p.frames):null;const j=page?i-page.start:i;return {i,...path(page?page.key:a.key),rect:[j%cols*W,Math.floor(j/cols)*H,W,H]};})});return;}if(typeof a.key==='string'&&Array.isArray(a.frames)&&a.frames.length&&a.frames.every(f=>Array.isArray(f)&&f.length===4&&f.every(Number.isFinite))){banks.push({label,type:'explicit',W,H,rects:a.frames.map((r,i)=>({i,...path(a.key),rect:r}))});return;}}for(const[k,v]of Object.entries(a)){if(v&&typeof v==='object'&&(!Array.isArray(v)||v.some(q=>q&&typeof q==='object')))visit(v,label+'.'+k,depth+1);}}visit(root,name,0);}return{banks,seenNames,missing};}''',sorted(names));b.close()
sizes={};bad=[];unresolved=[];checked=0;odd=[];Image.MAX_IMAGE_PIXELS=None
for bank in data['banks']:
 if bank['W']%2 or bank['H']%2:odd.append({'bank':bank['label'],'size':[bank['W'],bank['H']]})
 for c in bank['rects']:
  rel=c['path']
  if not isinstance(rel,str)or not rel.startswith('assets/'):
   unresolved.append({'bank':bank['label'],'key':c['key'],'reason':'nonlocal or dynamic source'});continue
  rel=rel.split('?')[0];f=(R/rel).resolve()
  if not f.is_relative_to(R)or not f.exists():unresolved.append({'bank':bank['label'],'key':c['key'],'reason':'path absent','path':rel});continue
  if rel not in sizes:
   try:
    with Image.open(f)as im:sizes[rel]=list(im.size)
   except Exception as e:sizes[rel]=None
  size=sizes[rel]
  if not size:continue
  # A logical cell is already cropped by XART; its intrinsic surface is that
  # registered crop, not the full source sheet. Retain both for review.
  alias=c.get('cell');intrinsic=[alias[3],alias[4]]if isinstance(alias,list)and len(alias)>=5 and isinstance(alias[0],str)else size
  x,y,w,h=c['rect'];checked+=1
  if x<0 or y<0 or x+w>intrinsic[0]or y+h>intrinsic[1]:bad.append({'bank':bank['label'],'frame':c['i'],'key':c['key'],'path':rel,'rect':c['rect'],'intrinsic':intrinsic,'sheet':size})
report={'registries':len(data['seenNames']),'banks':len(data['banks']),'checkedCells':checked,'images':len(sizes),'bad':bad,'odd':odd,'unresolved':unresolved,'missingGlobals':data['missing'],'pageErrors':errors,'scope':'Static metadata candidates from current runtime *_ART globals. Includes retained legacy registries; a candidate is not an active rendering defect until its live draw owner is confirmed. Handles local image grids, explicit rectangles and paged cells; not every custom renderer format.'};(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');(O/'metadata.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf8');print(json.dumps({k:report[k]for k in['registries','banks','checkedCells','images','missingGlobals','pageErrors']}));print('candidate rects',len(bad),'odd banks',len(odd),'unresolved',len(unresolved));print(json.dumps(bad[:12],indent=2))
