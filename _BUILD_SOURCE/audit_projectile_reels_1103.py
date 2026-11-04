"""Source-level audit of every animation reel the projectiles draw.

    python _BUILD_SOURCE/audit_projectile_reels_1103.py

For each art family recorded in the gallery catalogs (`art` per clip), every frame key
(<family>_0.._N, as XART resolves it: loose PNG or atlas cell) is decoded in the real game and measured:
  cell      the drawable's own width/height (a reel whose cells differ in size pumps when drawn by height)
  bbox      opaque-content bounds inside the cell
  frags     detached flat slivers (baked artefacts / neighbour bleed) and border-touching slivers
Output: _shots/projectiles_1103/audit/reels.json
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
G = R / '_shots/projectiles_1103'; http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
fams = set()
for t in ['before', 'after']:
    for it in json.load(open(G / t / 'catalog.json'))['items']:
        for k in it.get('art') or []:
            if k not in ('ap10_wind', 'av3_laser_beams', 's81003_beams'): fams.add(k)
JS = r"""async fams=>{
  const out={};
  const keysOf=f=>{const ks=[];for(const k of Object.keys(XART._src).concat(Object.keys((window.BOFX&&BOFX.cells)||{}),Object.keys((window.BOFX&&BOFX.playercells)||{}))){
      if(k===f||(k.startsWith(f+'_')&&/^\d+$/.test(k.slice(f.length+1))))ks.push(k);}
    return [...new Set(ks)].sort((a,b)=>(+a.slice(f.length+1)||0)-(+b.slice(f.length+1)||0)).slice(0,48);};
  const all=[];for(const f of fams){const ks=keysOf(f);out[f]={keys:ks,frames:[]};for(const k of ks){XART._touch(k);all.push(k);}}
  for(let i=0;i<120;i++){if(all.every(k=>XART.rdy(k)))break;const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());await new Promise(r=>setTimeout(r,50));}
  for(const f of fams){for(const k of out[f].keys){
    const im=XART.raw(k);if(!im||!XART.rdy(k)){out[f].frames.push({k,missing:true});continue;}
    const w=im.naturalWidth||im.width,h=im.naturalHeight||im.height,c=document.createElement('canvas');c.width=w;c.height=h;
    const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);let d;try{d=g.getImageData(0,0,w,h).data;}catch(e){out[f].frames.push({k,w,h,tainted:true});continue;}
    const A=new Uint8Array(w*h);for(let i=0;i<w*h;i++)A[i]=d[i*4+3]>24?1:0;
    const lab=new Int32Array(w*h),comps=[];let n=0;
    for(let i=0;i<w*h;i++){if(!A[i]||lab[i])continue;n++;const st=[i];lab[i]=n;let a=0,x0=w,x1=0,y0=h,y1=0;
      while(st.length){const p=st.pop(),x=p%w,y=(p/w)|0;a++;if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
        for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const X=x+dx,Y=y+dy;if(X<0||Y<0||X>=w||Y>=h)continue;const q=Y*w+X;if(A[q]&&!lab[q]){lab[q]=n;st.push(q);}}}
      comps.push({a,x0,x1,y0,y1});}
    comps.sort((p,q)=>q.a-p.a);const m=comps[0];
    const frags=[];for(const c2 of comps.slice(1)){if(c2.a<6||!m)continue;const cw=c2.x1-c2.x0+1,ch=c2.y1-c2.y0+1;
      const flat=(ch<=Math.max(4,h*.12)&&cw>=2.2*ch)||(cw<=Math.max(4,w*.12)&&ch>=2.2*cw);
      const edge=c2.x0===0||c2.y0===0||c2.x1===w-1||c2.y1===h-1;
      if((flat||edge)&&c2.a<m.a*.5)frags.push({...c2,flat,edge});}
    let bb=null;if(comps.length){bb=[w,h,0,0];for(const c2 of comps){if(c2.a<6)continue;bb=[Math.min(bb[0],c2.x0),Math.min(bb[1],c2.y0),Math.max(bb[2],c2.x1),Math.max(bb[3],c2.y1)];}}
    /* cut: opaque pixels running along a cell edge (art sliced by its own cell) */
    let cut=0;const run=(get,len)=>{let best=0,cur=0;for(let i=0;i<len;i++){if(get(i)){cur++;if(cur>best)best=cur;}else cur=0;}return best;};
    const edges=[run(i=>A[i],w),run(i=>A[(h-1)*w+i],w),run(i=>A[i*w],h),run(i=>A[i*w+w-1],h)];
    for(const e of edges)if(e>=8&&m&&e>=.35*Math.max(m.x1-m.x0,m.y1-m.y0))cut++;
    out[f].frames.push({k,w,h,bb,main:m?[m.x0,m.y0,m.x1,m.y1,m.a]:null,frags,cut,edges});
  }}
  return out;
}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(); p.set_default_timeout(300000)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        res = p.evaluate(JS, sorted(fams))
        br.close()
finally:
    stop()
(G / 'audit').mkdir(exist_ok=True)
(G / 'audit' / 'reels.json').write_text(json.dumps(res, indent=1))
pump, frag, missing = [], [], []
for f, r in res.items():
    fr = [x for x in r['frames'] if not x.get('missing') and not x.get('tainted') and x.get('main')]
    if any(x.get('missing') for x in r['frames']): missing.append(f)
    if len(fr) >= 2:
        hs = [x['main'][3] - x['main'][1] + 1 for x in fr]; ws = [x['main'][2] - x['main'][0] + 1 for x in fr]
        cells = {(x['w'], x['h']) for x in fr}
        if len(cells) > 1 or max(hs) / max(1, min(hs)) > 1.25: pump.append((f, sorted(cells), min(hs), max(hs)))
    fc = sum(1 for x in fr if x['frags'])
    if fc: frag.append((f, fc, len(fr), [(g['flat'], g['edge'], g['a']) for x in fr for g in x['frags']][:3]))
drop, cuts = [], []
for f, r in res.items():
    fr = [x for x in r['frames'] if x.get('main')]
    if len(fr) >= 3:
        import statistics
        med = statistics.median(x['main'][4] for x in fr)
        lows = [x['k'] for x in fr if x['main'][4] < .3 * med]
        if lows: drop.append((f, lows))
    cs = [x['k'] for x in fr if x.get('cut')]
    if cs and len(fr) > 1: cuts.append((f, len(cs), len(fr)))
print('DROPOUT', *drop, sep=chr(10)+'  '); print('CUT (multi-frame reels only)', *cuts, sep=chr(10)+'  ')
print('families', len(res)); print('PUMP', *pump, sep='\n  '); print('FRAG', *frag, sep='\n  '); print('MISSING', missing)
