#!/usr/bin/env python3
"""probe_bulletshimmer.py — do bullet sprites CRAWL as they travel?

Mike, asked which projectiles look wobbly: "almost all of them do. bullets from the planes,
ships, jets, level 1 boss etc."

Drop 0811p measured the PATHS and found ten of eleven kinds geometrically perfect. That was right
and it answered the wrong question: a bullet can travel a dead-straight line and still shimmer,
because the SPRITE is resampled every frame at a different sub-pixel phase.

This measures the shimmer directly. A bullet sprite is drawn at a series of sub-pixel offsets, and
each render is compared against the FIRST one shifted by the same whole-pixel amount. A sprite that
is merely moving scores near zero; one whose pixels are being re-averaged differently every frame
scores high. That difference is the wobble.

  churn%   share of the sprite's own pixels that disagree with the translated reference.
           Under nearest-neighbour a pixel-art sprite should snap between whole pixels and score
           low; under bilinear smoothing at 12-20px it smears differently at every offset.
"""
import http.server, socketserver, threading, functools, base64, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
()=>{
  /* a representative spread: the per-stage arsenal round, a missile and a shell */
  const keys=[];
  for(const k in (XART._src||{})){
    if(/^nep_1_[0-5]$/.test(k) || /^mfx_pellet/.test(k) || k==='mslB_0_0') keys.push(k);
  }
  for(const k of keys) XART.rdy(k);
  return keys.slice(0,4);
}
"""
MEASURE=r"""
([keys])=>{
  const H=16, ANG=0.35;            // the size and rotation a real round is drawn at
  const out=[];
  const strip=document.createElement('canvas'); strip.width=keys.length*220; strip.height=250;
  const sg=strip.getContext('2d'); sg.imageSmoothingEnabled=false;
  sg.fillStyle='#1b1f28'; sg.fillRect(0,0,strip.width,strip.height);

  keys.forEach((k,i)=>{
    if(!XART.rdy(k)) return;
    const im=XART.get(k);
    const w=H*(im.naturalWidth/im.naturalHeight);
    const P=48;                     // pad so rotation never clips
    const row={k};
    [true,false].forEach((smooth,si)=>{
      /* render the sprite at a run of sub-pixel offsets; compare each against the first,
         shifted by the same WHOLE pixels, so pure translation cancels out */
      const shots=[];
      for(let s=0;s<8;s++){
        const c=document.createElement('canvas'); c.width=P*2; c.height=P*2;
        const g=c.getContext('2d');
        g.imageSmoothingEnabled=smooth; if(smooth) g.imageSmoothingQuality='high';
        g.save(); g.translate(P + s*0.125, P); g.rotate(ANG);
        g.drawImage(im, -w/2, -H/2, w, H); g.restore();
        shots.push(g.getImageData(0,0,P*2,P*2).data);
      }
      const ref=shots[0];
      let churn=0, n=0;
      for(let s=1;s<shots.length;s++){
        const d=shots[s];
        for(let j=0;j<ref.length;j+=4){
          const a0=ref[j+3], a1=d[j+3];
          if(a0<12 && a1<12) continue;      // background on both: not part of the sprite
          n++;
          if(Math.abs(a0-a1)>28 || Math.abs(ref[j]-d[j])>36) churn++;
        }
      }
      row[smooth?'smoothed':'nearest']= n ? +(100*churn/n).toFixed(1) : null;

      /* a visible strip: the sprite drawn big at one offset, both ways */
      const c2=document.createElement('canvas'); c2.width=P*2; c2.height=P*2;
      const g2=c2.getContext('2d');
      g2.imageSmoothingEnabled=smooth; if(smooth) g2.imageSmoothingQuality='high';
      g2.save(); g2.translate(P+0.5,P); g2.rotate(ANG); g2.drawImage(im,-w/2,-H/2,w,H); g2.restore();
      sg.drawImage(c2, i*220+110-P*2, 18+si*116, P*4, P*4);
      sg.fillStyle='#9fd0ff'; sg.font='11px monospace'; sg.textAlign='center';
      sg.fillText(k+(smooth?'  SMOOTHED':'  NEAREST'), i*220+110, 12+si*116);
    });
    out.push(row);
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
    print('sprites:', keys)
    pg.wait_for_timeout(2000)
    r=pg.evaluate(MEASURE,[keys])
    print('%-18s %14s %14s' % ('sprite','SMOOTHED churn','NEAREST churn'))
    for e in r['out']:
        print('%-18s %13s%% %13s%%' % (e['k'], e.get('smoothed'), e.get('nearest')))
    with open(os.path.join(OUT,'bulletshimmer_0811v.png'),'wb') as fh:
        fh.write(base64.b64decode(r['img'].split(',',1)[1]))
    print('-> docs/proofs/bulletshimmer_0811v.png')
    b.close()
