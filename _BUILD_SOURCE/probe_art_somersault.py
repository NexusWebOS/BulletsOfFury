#!/usr/bin/env python3
"""
probe_art_somersault.py - LOOK AT THE SOMERSAULT REELS BEFORE BUILDING LIZZIE'S.

    python3 _BUILD_SOURCE/probe_art_somersault.py --out /tmp/somer

CLAUDE.md: render the art, never trust the key list. Contact sheets of every pilot's so0..so7
(eight of nine exist) plus every plate Lizzie actually has, so the missing reel is built from
what is really on the sheet rather than from what the manifest names.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SHEET = r"""
(spec) => {
  const [rows, cell] = spec;
  const pad=4, lw=92;
  const cvw = lw + rows[0][1].length*(cell+pad) + pad;
  const cvh = rows.length*(cell+pad) + pad + 18;
  const c=document.createElement('canvas'); c.width=cvw; c.height=cvh;
  const x=c.getContext('2d');
  x.fillStyle='#101319'; x.fillRect(0,0,cvw,cvh);
  x.font='9px monospace'; x.textBaseline='middle';
  rows.forEach((r,ri)=>{
    const [label, keys]=r;
    const cy=pad+ri*(cell+pad);
    x.fillStyle='#ffc21a'; x.fillText(label, 3, cy+cell/2);
    keys.forEach((k,ki)=>{
      const cx=lw+ki*(cell+pad);
      const ok = (typeof XART!=='undefined') && XART.rdy(k);
      x.fillStyle = ok ? '#05070a' : '#3a1414'; x.fillRect(cx,cy,cell,cell);
      if(ok){
        const im=XART.get(k);
        const s=Math.min(cell/im.naturalWidth, cell/im.naturalHeight);
        const w=im.naturalWidth*s, h=im.naturalHeight*s;
        x.imageSmoothingEnabled=false;
        x.drawImage(im, cx+(cell-w)/2, cy+(cell-h)/2, w, h);
        x.fillStyle='#6f8'; x.font='8px monospace';
        x.fillText(im.naturalWidth+'x'+im.naturalHeight, cx+2, cy+cell-6);
        x.font='9px monospace';
      } else { x.fillStyle='#ff8a7a'; x.font='8px monospace'; x.fillText('MISSING', cx+4, cy+cell/2); x.font='9px monospace'; }
    });
  });
  return c.toDataURL('image/png');
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/somer'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    import base64
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    PILOTS=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1280,'height':900})
        pg.goto(f'http://127.0.0.1:{port}/index.html?debug=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof XART!=='undefined'", timeout=60000)
        # XART.rdy() is false on its FIRST call - that call starts the load. Ask twice, with a wait.
        keys=[]
        for pk in PILOTS: keys += ['ship_%s_so%d'%(pk,i) for i in range(8)]
        keys += ['ship_lizzie_'+s for s in ['nf','l','r','b42','pv0','pv1','pv2','pv3','pv4']]
        keys += ['ship_lizzie_br%d'%i for i in range(8)]
        keys += ['ship_lizzie_sp%d'%i for i in range(8)]
        pg.evaluate("(ks) => ks.forEach(k=>{ try{ XART.rdy(k); }catch(e){} })", keys)
        pg.wait_for_timeout(4000)
        pg.evaluate("(ks) => ks.forEach(k=>{ try{ XART.rdy(k); }catch(e){} })", keys)
        pg.wait_for_timeout(2500)

        rdy=pg.evaluate("(ks) => ks.filter(k=>XART.rdy(k)).length", keys)
        print('%d / %d keys decoded' % (rdy, len(keys)))

        rows=[[pk.upper(), ['ship_%s_so%d'%(pk,i) for i in range(8)]] for pk in PILOTS]
        d=pg.evaluate(SHEET, [rows, 96])
        open(os.path.join(a.out,'01_somersault_all.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))

        rows2=[['LZ IDLE/LR', ['ship_lizzie_nf','ship_lizzie_l','ship_lizzie_r','ship_lizzie_b42','ship_lizzie_pv0','ship_lizzie_pv2','ship_lizzie_pv4','']],
               ['LZ ROLL',   ['ship_lizzie_br%d'%i for i in range(8)]],
               ['LZ SPIN',   ['ship_lizzie_sp%d'%i for i in range(8)]],
               ['MAV SOMER', ['ship_maverick_so%d'%i for i in range(8)]],
               ['MAV ROLL',  ['ship_maverick_br%d'%i for i in range(8)]]]
        d=pg.evaluate(SHEET, [rows2, 110])
        open(os.path.join(a.out,'02_lizzie_vs_maverick.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))

        # is a pilot's so reel the same art as their br reel? measure, do not eyeball
        same=pg.evaluate("""() => {
          const out={};
          for(const pk of ['maverick','axel','juggernaut','yuri']){
            const a=XART.rdy('ship_'+pk+'_so2')?XART.get('ship_'+pk+'_so2'):null;
            const b=XART.rdy('ship_'+pk+'_br2')?XART.get('ship_'+pk+'_br2'):null;
            out[pk]= a&&b ? [a.naturalWidth+'x'+a.naturalHeight, b.naturalWidth+'x'+b.naturalHeight, a.src===b.src] : null;
          }
          return out; }""")
        print('so2 vs br2 (size, size, same src):', same)
        b.close()
    stop()
    print('sheets in', a.out)

if __name__=='__main__':
    main()
