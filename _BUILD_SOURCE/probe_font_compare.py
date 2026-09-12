#!/usr/bin/env python3
"""
probe_font_compare.py - WHICH FACE, AND AT WHAT SIZE.

    python3 _BUILD_SOURCE/probe_font_compare.py --out /tmp/fonts

Mike, on the HELP controls page: "whatever font is being used here is bad. please use stage fonts
only the proper ones."

Draws the exact strings that page draws, in both candidates, at every size the page uses, so the
choice is made off the pixels rather than off the function names:

    uiFontArt()   ASSETS.stageArt['1']     the stage-1 CARD alphabet (what the page used)
    curFontArt()  ASSETS.stageFontV4[n]    CF_BOFStageFonts Vol.2, the authored per-stage face
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SHEET = r"""
() => {
  const S=['FIRE','MISSILE','RETINA / C','J  /  L-CLICK','CHARGE','PAUSE','MOVE'];
  const SZ=[8,9,10,11,13,16];
  const c=document.createElement('canvas'); c.width=980; c.height=760;
  const g=c.getContext('2d');
  g.fillStyle='#0d1016'; g.fillRect(0,0,c.width,c.height);
  // draw onto the real game canvas then copy back, because stageText writes to `ctx`
  const cv=document.getElementById('screen');
  const real=cv.getContext('2d');
  const faces=[['uiFontArt  (card alphabet)', uiFontArt()], ['curFontArt (stage font V4)', curFontArt()]];
  let y=28;
  g.font='12px monospace'; g.textBaseline='middle';
  for(const [label, art] of faces){
    g.fillStyle='#ffc21a'; g.fillText(label, 8, y-12);
    for(const sz of SZ){
      real.save();
      real.setTransform(1,0,0,1,0,0);
      real.clearRect(0,0,cv.width,cv.height);
      let x=6;
      for(const s of S){
        if(art && typeof stageText==='function') stageText(art, s, x+60, 24, sz, '#ffd36b', 0.9, 1, 0.10);
        x += 128;
      }
      real.restore();
      g.drawImage(cv, 0, 0, cv.width, 46, 96, y, 880, 46*(880/cv.width)*1.6);
      g.fillStyle='#9fb4c8'; g.font='11px monospace';
      g.fillText(sz+'px', 12, y+16);
      y += 52;
    }
    y += 26;
  }
  return c.toDataURL('image/png');
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/fonts'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1000})
        pg.goto(f'http://127.0.0.1:{port}/index.html?debug=1', wait_until='load', timeout=60000)
        pg.wait_for_timeout(1200); pg.keyboard.press('Enter')
        pg.wait_for_function("() => window.__BOFSTATE && window.__BOFSTATE()==='opener'", timeout=60000)
        pg.wait_for_timeout(400); pg.keyboard.press('Space')
        pg.wait_for_function("() => window.__BOFSTATE()==='title'", timeout=20000)
        # both faces are lazy sheets - touch them and let them decode
        pg.evaluate("() => { try{ void uiFontArt().img; void curFontArt().img; warmStageSheets(1); }catch(e){} }")
        pg.wait_for_timeout(3500)
        print('uiFontArt ready :', pg.evaluate("() => artReady(uiFontArt())"))
        print('curFontArt ready:', pg.evaluate("() => artReady(curFontArt())"))
        d=pg.evaluate(SHEET)
        open(os.path.join(a.out,'faces.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))
        b.close()
    stop(); print('wrote', os.path.join(a.out,'faces.png'))

if __name__=='__main__':
    main()
