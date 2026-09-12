#!/usr/bin/env python3
"""
probe_art_menu_jugg.py - WHAT THE HELP BUTTON AND THE WRECKING BALL HAVE TO MATCH.

    python3 _BUILD_SOURCE/probe_art_menu_jugg.py --out /tmp/mj

Renders the five title buttons (the plate a HELP button must be cut from), every special icon
(is the Juggernaut wrecking ball already good?), and Juggernaut's hull, at real scale.
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

DRAW = r"""
(spec) => {
  const [rows, cw, ch] = spec;
  const pad=6, lw=140;
  const cvw = lw + Math.max(...rows.map(r=>r[1].length))*(cw+pad) + pad;
  const cvh = rows.length*(ch+pad) + pad;
  const c=document.createElement('canvas'); c.width=cvw; c.height=cvh;
  const x=c.getContext('2d');
  x.fillStyle='#0d1016'; x.fillRect(0,0,cvw,cvh);
  x.font='10px monospace'; x.textBaseline='middle'; x.imageSmoothingEnabled=false;
  rows.forEach((r,ri)=>{
    const [label, keys, how]=r;
    const cy=pad+ri*(ch+pad);
    x.fillStyle='#ffc21a'; x.fillText(label, 4, cy+ch/2);
    keys.forEach((k,ki)=>{
      if(!k) return;
      const cx=lw+ki*(cw+pad);
      x.fillStyle='#05070a'; x.fillRect(cx,cy,cw,ch);
      let drew=false;
      try{
        if(how==='icon' && typeof iconBlit==='function'){ iconBlit(x,k,cx+(cw-ch)/2,cy,ch,true); drew=true; }
        else if(typeof XART!=='undefined' && XART.rdy(k)){
          const im=XART.get(k);
          const s=Math.min(cw/im.naturalWidth, ch/im.naturalHeight);
          x.drawImage(im, cx+(cw-im.naturalWidth*s)/2, cy+(ch-im.naturalHeight*s)/2, im.naturalWidth*s, im.naturalHeight*s);
          drew=true;
        }
      }catch(e){}
      x.fillStyle=drew?'#7f9':'#f88'; x.font='9px monospace';
      x.fillText(k.replace('special_icon_','').slice(0,24), cx+2, cy+ch-7);
      x.font='10px monospace';
    });
  });
  return c.toDataURL('image/png');
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/mj'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    BTN=['btn_newgame','btn_password','btn_options','btn_credits','btn_exit']
    SPI=['spicon_axel','spicon_cole','spicon_decker','spicon_falva','spicon_freezer',
         'spicon_juggernaut','spicon_lizzie','spicon_maverick','spicon_yuri']
    HULL=['ship_juggernaut_nf','ship_juggernaut_l','ship_juggernaut_r']
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1400,'height':900})
        pg.goto(f'http://127.0.0.1:{port}/index.html?debug=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof XART!=='undefined'", timeout=60000)
        pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", BTN+HULL)
        pg.wait_for_timeout(5000)
        pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", BTN+HULL)
        pg.wait_for_timeout(3000)
        d=pg.evaluate(DRAW, [[['TITLE BUTTONS', BTN, 'art']], 240, 56])
        open(os.path.join(a.out,'01_buttons.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))
        d=pg.evaluate(DRAW, [[['SPECIAL ICONS', SPI, 'icon'], ['JUGGERNAUT', HULL, 'art']], 96, 96])
        open(os.path.join(a.out,'02_icons_hull.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))
        b.close()
    stop(); print('wrote', a.out)

if __name__=='__main__':
    main()
