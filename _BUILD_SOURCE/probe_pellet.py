#!/usr/bin/env python3
"""probe_pellet.py — what the machine gun pellet actually is.

Mike, clarifying which projectiles look wobbly: "I meant the machine gun pellets".

The pellet FIRETYPE animates by alternating TWO frames every 70ms:

    art:(b)=>['mfx_mg_2_0','mfx_mg_2_2'][(floor(now/70)+b._ph)%2]

Two things worth measuring about that. It skips frame _1 of the reel, so it is not playing an
animation — it is toggling between two non-adjacent poses about seven times a second. And if those
two poses differ in width, brightness or centre of mass, the round will appear to shudder in flight
even though its path is exact.

So: render every frame of the reel side by side, and measure how far apart the two the game
actually uses are — ink, luminance, width, and the horizontal centre of mass. A big gap between
frame 0 and frame 2 IS the wobble.
"""
import http.server, socketserver, threading, functools, base64, os, io
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
()=>{
  const keys=[];
  for(const k in (XART._src||{})) if(/^mfx_mg_/.test(k)) keys.push(k);
  keys.sort();
  for(const k of keys) XART.rdy(k);
  return keys;
}
"""
MEASURE=r"""
([keys])=>{
  const out=[];
  const CW=110;
  const strip=document.createElement('canvas');
  strip.width=Math.max(1,keys.length)*CW; strip.height=150;
  const sg=strip.getContext('2d'); sg.imageSmoothingEnabled=false;
  sg.fillStyle='#141821'; sg.fillRect(0,0,strip.width,strip.height);
  keys.forEach((k,i)=>{
    if(!XART.rdy(k)) return;
    const im=XART.get(k);
    const c=document.createElement('canvas'); c.width=im.naturalWidth; c.height=im.naturalHeight;
    const g=c.getContext('2d'); g.drawImage(im,0,0);
    const d=g.getImageData(0,0,c.width,c.height).data;
    let ink=0, lum=0, sx=0, minX=1e9, maxX=-1;
    for(let y=0;y<c.height;y++) for(let x=0;x<c.width;x++){
      const i4=(y*c.width+x)*4; if(d[i4+3]<30) continue;
      ink++; lum+=0.30*d[i4]+0.59*d[i4+1]+0.11*d[i4+2]; sx+=x;
      if(x<minX)minX=x; if(x>maxX)maxX=x;
    }
    out.push({k, w:c.width, h:c.height, ink,
              meanLum: ink?+(lum/ink).toFixed(0):0,
              inkW: (maxX<0)?0:(maxX-minX+1),
              cx: ink?+((sx/ink)-c.width/2).toFixed(2):0});
    const s=Math.min(90/c.width, 90/c.height);
    sg.drawImage(im, i*CW+55-c.width*s/2, 30-0+ (100-c.height*s)/2, c.width*s, c.height*s);
    sg.fillStyle='#9fd0ff'; sg.font='11px monospace'; sg.textAlign='center';
    sg.fillText(k.replace('mfx_mg_',''), i*CW+55, 140);
  });
  return {out, img:strip.toDataURL('image/png')};
}
"""
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    keys=pg.evaluate(RUN)
    print('mfx_mg_ keys registered: %d  ->  %s' % (len(keys), ', '.join(k.replace('mfx_mg_','') for k in keys)))
    pg.wait_for_timeout(2000)
    r=pg.evaluate(MEASURE,[keys])
    print('%-14s %-9s %7s %9s %8s %9s' % ('frame','size','ink','meanLum','inkWidth','centre-x'))
    used={}
    for e in r['out']:
        mark='  <= USED' if e['k'] in ('mfx_mg_2_0','mfx_mg_2_2') else ''
        if mark: used[e['k']]=e
        print('%-14s %-9s %7s %9s %8s %9s%s' % (e['k'].replace('mfx_mg_',''),
              '%dx%d'%(e['w'],e['h']), e['ink'], e['meanLum'], e['inkW'], e['cx'], mark))
    if len(used)==2:
        a,c=used['mfx_mg_2_0'],used['mfx_mg_2_2']
        print('\nthe two frames the game alternates, 7x a second:')
        print('   ink        %d vs %d   (%+.0f%%)' % (a['ink'],c['ink'],100.0*(c['ink']-a['ink'])/max(1,a['ink'])))
        print('   ink width  %d vs %d px' % (a['inkW'],c['inkW']))
        print('   centre-x   %+.2f vs %+.2f px  -> the round shifts %.2fpx sideways every toggle'
              % (a['cx'],c['cx'],abs(c['cx']-a['cx'])))
    with open(os.path.join(OUT,'pellet_reel_0811y.png'),'wb') as fh:
        fh.write(base64.b64decode(r['img'].split(',',1)[1]))
    print('-> docs/proofs/pellet_reel_0811y.png')
    b.close()
