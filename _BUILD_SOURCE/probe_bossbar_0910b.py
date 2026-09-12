#!/usr/bin/env python3
"""
probe_bossbar_0910b.py - THE PACK'S GAUGES, RENDERED (drop 0910b).

    python3 _BUILD_SOURCE/probe_bossbar_0910b.py --out /tmp/bars

Real Chromium via the boss-mode host. Draws the boss bar and the miniboss bar for all nine stages
with a damage-lag ghost and a critical pulse into one contact sheet, proves the ART path (not the
drawn fallback) is what blits, then shoots three live fights at 62% HP.
"""
import sys, os, base64, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot
from PIL import Image

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bars'); a=ap.parse_args()
    OUT=a.out; os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]
    def ok(c,m):
        print(('  ok   ' if c else '  FAIL ')+m)
        if not c: fails.append(m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1200}); pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && BOSSMODE.state==='bmhost'", timeout=60000)
        pg.evaluate("() => bossBarWarm(1)")
        pg.wait_for_function("() => XART.rdy('bmbar_frame_boss') && XART.rdy('bmbar_frame_mini') && XART.rdy('bmbar_fill_seg') && XART.rdy('bmbar_fill_grey') && XART.rdy('bmbar_fill_orange')", timeout=10000)
        tiles=[]
        for st in range(1,10):
            d=pg.evaluate("""(st) => { run.stage=st; _gaugeLag.boss=0.9; _gaugeLag.mini=0.8;
              ctx.setTransform(SS,0,0,SS,0,0); ctx.fillStyle='#101318'; ctx.fillRect(0,0,VW,110);
              const ok1=drawHealthBarV2('boss',0.72,VW/2,22,VW*0.72); const ok2=drawHealthBarV2('mini',0.55,VW/2,50,VW*0.62,false);
              const ok3=drawHealthBarV2('boss',0.18,VW/2,80,VW*0.72);
              ctx.fillStyle='#cfd6e0'; ctx.font='bold 10px monospace'; ctx.textAlign='left'; ctx.fillText('STAGE '+st+'  boss 72% (ghost 90%) / mini 55% (ghost 80%) / boss 18% critical', 8, 104);
              return [ok1&&ok2&&ok3, document.getElementById('screen').toDataURL('image/png')]; }""", st)
            ok(d[0], 'stage %d: both gauges draw' % st)
            im=Image.open(io.BytesIO(base64.b64decode(d[1].split(',',1)[1]))); tiles.append(im.crop((0,0,im.width,220)))
        sheet=Image.new('RGB',(tiles[0].width, sum(t.height for t in tiles)),(0,0,0)); y=0
        for t in tiles: sheet.paste(t,(0,y)); y+=t.height
        sheet.save(os.path.join(OUT,'bars_all_stages.png'))
        n=pg.evaluate("""() => { let n=0; const o=ctx.drawImage; ctx.drawImage=function(im){ if(im&&im.width===700&&im.height===33) n++; return o.apply(ctx,arguments); }; run.stage=4; drawHealthBarV2('boss',0.5,240,20,346); drawHealthBarV2('mini',0.5,240,50,298,false); ctx.drawImage=o; return n; }""")
        ok(n==2, 'the ART path blits the frame cell for a boss and a mini draw (%d frame blits)' % n)
        # the fill never draws narrower than the opening: trap the fill blit's destination width at two fractions
        w=pg.evaluate("""() => { const ws=[]; const o=ctx.drawImage; ctx.drawImage=function(im,a,b,c,d,e,f,g,h){ if(im&&im.height<30&&im.width>500) ws.push(arguments.length>=5?arguments[3]:im.width); return o.apply(ctx,arguments); }; run.stage=2; _gaugeLag.boss=0.3; drawHealthBarV2('boss',0.3,240,20,346); _gaugeLag.boss=0.9; drawHealthBarV2('boss',0.9,240,20,346); ctx.drawImage=o; return ws; }""")
        ok(len(w)>=2 and max(w)-min(w)<0.5, 'the fill is blitted at ONE width whatever the fraction - clipped, not shrunk (%s)' % [round(x,1) for x in w])
        for st,role,name in [(2,'boss','live_s2_boss.png'),(3,'mini','live_s3_mini.png'),(6,'boss','live_s6_boss.png')]:
            pg.evaluate(f"() => BOSSMODE.start({st},'{role}','cole')")
            pg.wait_for_function("() => { const s=BOSSMODE.snapshot(); return (s.bossActive||s.subBossActive) && s.boss && !s.boss.enter; }", timeout=20000)
            pg.wait_for_timeout(1200)
            pg.evaluate("() => { const s=BOSSMODE.snapshot(); BOSSMODE.setBossHp(s.boss.maxhp*0.62); }"); pg.wait_for_timeout(700)
            d=pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(OUT,name),'wb').write(base64.b64decode(d.split(',',1)[1]))
            ok(True, 'shot '+name+': '+pg.evaluate("() => { const s=BOSSMODE.snapshot(); return s.boss.name+' '+Math.round(100*s.boss.hp/s.boss.maxhp)+'%'; }"))
            pg.evaluate("() => BOSSMODE.stop()"); pg.wait_for_function("() => BOSSMODE.state==='bmhost'", timeout=15000)
        b.close()
    stop()
    print('%d fail; page errors: %s' % (len(fails), errs[:4]))
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
