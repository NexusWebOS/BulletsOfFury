#!/usr/bin/env python3
"""measure_chaingun_mounts_0928.py - where each pilot's wing roots are, for the chaingun pods (Mike 0928:
"anchored chaingun attachments to all our pilots ships ... and spin the barrels").

For each pilot, draws one real PLAY frame on Stage 6, records the hull blit (XART.get key + the destination
rect under the live transform), then reads that plate's alpha to find the widest ink row in the front
two-thirds of the hull (the wings) and the ink span on it. Prints anchors as offsets from (player.x,player.y)
in world px - the numbers CHAINGUN_MOUNTS carries.
"""
import os, sys, json, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
MEASURE = r"""
(pk) => {
  run.pilot=pk;player.reset();player.x=camLeftX()+viewW()/2;player.y=VH*.7;player.invuln=0;
  const rec=[];const xg=XART.get.bind(XART);let last=null;XART.get=function(k){last=k;return xg(k);};
  const di=ctx.drawImage;ctx.drawImage=function(im){const a=arguments;
    if(last&&/^ship_/.test(last)&&a.length>=5){const m=ctx.getTransform();const dx=a.length>=9?a[5]:a[1],dy=a.length>=9?a[6]:a[2],dw=a.length>=9?a[7]:a[3],dh=a.length>=9?a[8]:a[4];
      rec.push({k:last,x:(m.a*dx+m.c*dy+m.e)/SS,y:(m.b*dx+m.d*dy+m.f)/SS,w:dw*m.a/SS,h:dh*m.d/SS,iw:im.width||im.naturalWidth,ih:im.height||im.naturalHeight,camX:camX});}
    last=null;return di.apply(this,a);};
  try{drawWorld(1/60);}finally{ctx.drawImage=di;XART.get=xg;}
  const r=rec.find(q=>q.k==='ship_'+pk)||rec[0];if(!r)return {pk,err:'no hull blit'};
  const im=XART.get(r.k),c=document.createElement('canvas');c.width=r.iw;c.height=r.ih;const g=c.getContext('2d');g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data;let best=null,top=c.height,bot=0;
  const span=[];for(let y=0;y<c.height;y++){let l=-1,rr=-1;for(let x=0;x<c.width;x++)if(d[(y*c.width+x)*4+3]>40){if(l<0)l=x;rr=x;}span.push([l,rr]);if(l>=0){top=Math.min(top,y);bot=Math.max(bot,y);}}
  for(let y=top;y<=top+(bot-top)*.75;y++){const [l,rr]=span[y];if(l<0)continue;if(!best||rr-l>best.w)best={y,l,r:rr,w:rr-l};}
  const sx=r.w/r.iw,sy=r.h/r.ih,cx=(best.l+best.r)/2;
  // pods sit a quarter of the span in from each wingtip, on the widest row
  const wx=(best.w*.5-best.w*.22)*sx, wy=r.y+best.y*sy-player.y, worldShipX=r.x+cx*sx+ (r.camX||0);
  return {pk,key:r.k,blit:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.w.toFixed(1),h:+r.h.toFixed(1)},ink:{top,bot,row:best.y,span:best.w},
    player:{x:+player.x.toFixed(1),y:+player.y.toFixed(1)},mount:{dx:+wx.toFixed(1),dy:+wy.toFixed(1),hull:+((bot-top)*sy).toFixed(1),centerOff:+(r.x+cx*sx-(player.x-(r.camX||0))).toFixed(1)}};
}
"""
def main():
    port, stop = sh.serve(sh.GAME); out = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("""() => { diffKey='normal';DIFF=DIFFS.normal;run.mode='arcade';run.stage=6;curStage=STAGES[5];beginStage(6);setState(GS.PLAY);
          story=null;special=null;s6Opening=null;s6Wing=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];
          for(const p of %s)XART.rdy('ship_'+p); }""" % json.dumps(PILOTS))
        pg.wait_for_timeout(2500)
        for pk in PILOTS:
            pg.evaluate("(pk)=>XART.rdy('ship_'+pk)", pk); pg.wait_for_timeout(300)
            r = pg.evaluate(MEASURE, pk); out.append(r); print(json.dumps(r), flush=True)
        br.close()
    stop()
    json.dump(out, open(os.path.join(sh.GAME, '_shots', 'opus0928', 'chaingun_mounts.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
