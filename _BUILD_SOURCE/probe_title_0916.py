#!/usr/bin/env python3
"""
probe_title_0916.py - THE TITLE MENU, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_title_0916.py

Mike, 0916: "Regenerate all my other buttons here to match the current style of Bullets of Fury and
proper reference of ships and pilots please. The help button also is too large compared to the rest."

"Too large" was an ASPECT problem - titleMenuLayout fixes ONE width and takes each row's height from
its own plate, so btn_help at 3.98:1 drew ~23% taller than the 4.7-4.9:1 bars beside it. This probe
measures the quantity that actually was wrong: the spread of the DRAWN heights at a common width.

Blits are identified by KEY (XART.get is wrapped), never by size - every bar on this sheet is within
a pixel of every other, so a size match cannot say whose art a blit is (0906e).

Two faults in its own first run, both kept in the code as comments:
  - it stepped TWO frames and measured row pitch across both, so the wrap from the last row of one
    frame to the first row of the next read as a -288px gap on a menu that is fine;
  - it asserted "every row draws at one measured box", which the layout does not claim.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'awards_0916')
os.makedirs(OUT, exist_ok=True)
N = {'ok': 0, 'fail': 0}
def ok(c, m):
    N['ok' if c else 'fail'] += 1
    print(('  ok   ' if c else '  FAIL ') + m)

port, stop = sh.serve(ROOT)
srv = 'http://127.0.0.1:%d' % port
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': 1000, 'height': 1100})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
    pg.goto(srv + '/index.html')
    pg.wait_for_timeout(2500)
    pg.evaluate(sh.TRAP_RAF)

    # get to the title, then let the plates decode for real
    pg.evaluate("() => { try{ setState(GS.TITLE); }catch(e){} }")
    for _ in range(6):
        pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(500)

    keys = pg.evaluate("() => MENU_KEYS.slice()")
    MENU_KEYS_ORDER = keys
    items = pg.evaluate("() => TITLE_ITEMS.slice()")
    icons = pg.evaluate("() => TITLE_ICONS.slice()")
    print('  MENU_KEYS:', keys)
    ok(len(keys) == len(items) == len(icons) == 7, 'seven rows, seven keys, seven fallback icons')
    ok(all(k.endswith('_0916') for k in keys), 'every row points at the 0916 sheet')

    rdy = pg.evaluate("() => MENU_KEYS.map(k => XART.rdy(k))")
    ok(all(rdy), 'all seven plates decoded: %s' % rdy)
    dims = pg.evaluate("() => MENU_KEYS.map(k => { const i=XART.get(k); return [i.naturalWidth,i.naturalHeight]; })")
    asp = [round(w / float(h), 3) for w, h in dims]
    print('  aspects:', asp)
    ok(max(asp) - min(asp) < 0.30,
       'and they SHARE an aspect (spread %.3f) - the whole of "the help button is too large"' % (max(asp) - min(asp)))

    # what the title actually DRAWS: trap the instance's drawImage and record key + rect
    pg.evaluate("""() => {
      window.__blits=[]; const c=ctx; const o=c.drawImage.bind(c);
      const byKey=new Map();
      for(const k of MENU_KEYS){ const im=XART.get(k); if(im) byKey.set(im.width+'x'+im.height+'#'+k, k); }
      window.__gk=XART.get; const seen=new Map();
      XART.get=function(k){ const im=window.__gk.call(XART,k); if(im) seen.set(im,k); return im; };
      c.drawImage=function(im){ const a=arguments;
        let dx=0,dy=0,dw=0,dh=0;
        if(a.length>=9){ dx=a[5];dy=a[6];dw=a[7];dh=a[8]; } else if(a.length>=5){ dx=a[1];dy=a[2];dw=a[3];dh=a[4]; }
        const k=seen.get(im)||null;
        if(k && k.indexOf('btn_')===0) window.__blits.push({k:k,x:dx,y:dy,w:dw,h:dh});
        return o.apply(c,a); };
    }""")
    # ONE frame. Two frames of blits put a -288px "gap" between the last row of one frame and the
    # first row of the next, which reads as a row flying off the top of a menu that is fine.
    pg.evaluate("() => { window.__blits=[]; }")
    pg.evaluate(sh.STEP, [1])
    bl = pg.evaluate("() => window.__blits.slice()")
    drawn = [b for b in bl if b['k'].endswith('_0916')]
    got = []
    for b in drawn:
        if b['k'] not in got: got.append(b['k'])
    print('  drawn:', json.dumps(got))
    ok(len(got) == 7, 'all seven plates are BLITTED on the title, identified by KEY (%d)' % len(got))
    ok(got == keys, 'in MENU_KEYS order, top to bottom')

    # titleMenuLayout fixes the WIDTH and takes each row's height from its OWN plate, so identical
    # heights are not the claim - "not stretched" is. btn_help at 3.98:1 drew 23% taller than the
    # 4.9:1 bars beside it at this same common width; that is what Mike was looking at.
    hs = sorted(round(b['h'], 2) for b in drawn if abs(b['w'] - min(q['w'] for q in drawn)) < 0.01)
    print('  drawn heights (unselected):', hs)
    ok(hs and max(hs) - min(hs) <= 2.0,
       'no row is stretched: the tallest unselected row is within %.2fpx of the shortest' % (max(hs) - min(hs)))

    ys = [b['y'] + b['h'] / 2 for b in drawn]
    gaps = [round(ys[i + 1] - ys[i], 2) for i in range(len(ys) - 1)]
    print('  row pitch:', gaps)
    ok(gaps and max(gaps) - min(gaps) < 0.5, 'evenly pitched, no row inside its neighbour')

    tops = [b['y'] for b in drawn]; bots = [b['y'] + b['h'] for b in drawn]
    overlap = sum(1 for i in range(len(drawn) - 1) if bots[i] > tops[i + 1] + 0.5)
    ok(overlap == 0, 'and NO row overlaps the one under it (%d overlaps)' % overlap)

    # the fallback row count is the bug this replaces: seven icons for seven rows
    ok(pg.evaluate("() => TITLE_ICONS.length===TITLE_ITEMS.length && TITLE_ICONS.every(i=>!!i)"),
       'the pre-decode fallback has an icon for every row, EXIT GAME included')

    pg.screenshot(path=os.path.join(OUT, '15_title_seven.png'))

    # ---- MIKE'S COLOURS, READ BACK OFF THE LIVE CANVAS ----------------------------------------
    # \u26a0 THE PLATE ON DISK IS NOT EVIDENCE. A builder can write a perfect PNG and the game can
    # still serve the old one - cells are checked before the loose-file cache (0912m), and this
    # family ships under keys chosen precisely to dodge that. So this measures the canvas XART
    # actually hands the title.
    #
    # \u26a0 AND IT MEASURES THE PIXELS THAT CHANGED, NOT THE PIXELS THAT LOOK LIT. The first cut
    # sampled "saturated bright pixels in the bezel" for the lamp and "saturated pixels in the text
    # band" for the lettering, and it FAILED four assertions on a build that is correct:
    #   - CREDITS is "Neon Black" and EXIT GAME is "White Light", so neither lamp HAS saturation -
    #     the sample came back EMPTY and the probe reported value -1.000, which reads as "the lamp
    #     is gone" rather than "I asked the wrong question".
    #   - the 431 and 553 "letter" pixels it did find on those two were the CITY LIGHTS and the
    #     RUNWAY FIRE, which sit in the same band and were never meant to change.
    # Diffing the live plate against the un-recoloured source on disk gives the exact mask the
    # builder touched, so the scene cannot contaminate it and a colourless lamp is still findable.
    WANT = {'btn_newgame_0916':      ('Neon Green',  0.312),
            'btn_password_0916':     ('Neon Orange', 0.055),
            'btn_options_0916':      ('Neon Blue',   0.578),
            'btn_help_0916':         ('Neon Pink',   0.905),
            'btn_achievements_0916': ('Neon Red',    0.985)}
    meas = pg.evaluate("""async () => {
      function hsv(r,g,b){ r/=255;g/=255;b/=255;
        const mx=Math.max(r,g,b), mn=Math.min(r,g,b), d=mx-mn; let h=0;
        if(d){ if(mx===r) h=((g-b)/d+(g<b?6:0))/6; else if(mx===g) h=((b-r)/d+2)/6; else h=((r-g)/d+4)/6; }
        return [h, mx?d/mx:0, mx]; }
      function grab(img){ const c=document.createElement('canvas'); c.width=img.width||img.naturalWidth;
        c.height=img.height||img.naturalHeight; const g=c.getContext('2d'); g.drawImage(img,0,0);
        return {d:g.getImageData(0,0,c.width,c.height).data, w:c.width, h:c.height}; }
      function load(u){ return new Promise((res,rej)=>{ const i=new Image();
        i.onload=()=>res(i); i.onerror=rej; i.src=u; }); }
      const out={};
      for(const k of MENU_KEYS){
        const live=XART.get(k); if(!live) continue;
        const name=k.slice(4,-5);
        let src; try{ src=await load('assets/game/ui/title_0916/btn_'+name+'.png'); }catch(e){ continue; }
        const A=grab(live), B=grab(src);
        if(A.w!==B.w||A.h!==B.h){ out[k]={sizeMismatch:[A.w,A.h,B.w,B.h]}; continue; }
        const lamp=[], text=[], was=[], wasT=[];
        for(let y=0;y<A.h;y++) for(let x=0;x<A.w;x++){
          const i=(y*A.w+x)*4;
          if(A.d[i+3]<200) continue;
          const dr=Math.abs(A.d[i]-B.d[i]), dg=Math.abs(A.d[i+1]-B.d[i+1]), db=Math.abs(A.d[i+2]-B.d[i+2]);
          if(dr+dg+db < 24) continue;                       // unchanged: the scene
          const q=hsv(A.d[i],A.d[i+1],A.d[i+2]);
          if(x<26 || x>=A.w-26){ lamp.push(q); was.push(hsv(B.d[i],B.d[i+1],B.d[i+2])); }
          else { text.push(q); wasT.push(hsv(B.d[i],B.d[i+1],B.d[i+2])); }
        }
        function med(v,j){ if(!v.length) return null; const t=v.map(q=>q[j]).sort((a,b)=>a-b); return t[t.length>>1]; }
        function hi(v,j){ if(!v.length) return null; const t=v.map(q=>q[j]).sort((a,b)=>a-b); return t[Math.floor(t.length*0.9)]; }
        out[k]={lampN:lamp.length, textN:text.length,
                lampH:med(lamp,0), lampS:med(lamp,1), lampV:med(lamp,2), lampVhi:hi(lamp,2),
                textH:med(text,0), textS:med(text,1), textV:med(text,2),
                wasVhi:hi(was,2), wasS:med(was,1), wasV:med(was,2),
                wasTV:med(wasT,2), wasTH:med(wasT,0)};
      }
      return out; }""")
    def dh(a, b):
        d = abs(a - b) % 1.0
        return min(d, 1.0 - d)
    for k in MENU_KEYS_ORDER:
        m = meas.get(k) or {}
        ok(m.get('lampN', 0) > 300 and m.get('textN', 0) > 200,
           '%-13s the swap touched its lamps AND its lettering (%s / %s px changed)'
           % (k[4:-5], m.get('lampN'), m.get('textN')))
    for k, (label, want) in WANT.items():
        m = meas.get(k) or {}
        got = m.get('lampH'); gt = m.get('textH')
        ok(got is not None and dh(got, want) < 0.055,
           '%-13s lamps are %s (hue %s)' % (k[4:-5], label, ('%.3f' % got) if got is not None else None))
        ok(gt is not None and dh(gt, want) < 0.075,
           '%-13s lettering matches its lamps (hue %s)' % (k[4:-5], ('%.3f' % gt) if gt is not None else None))
    # \u26a0 CREDITS IS "NEON BROWN", AND A HUE ASSERTION ALONE WOULD BE VACUOUS HERE. Brown is not
    # its own hue - it is DARK ORANGE - and these plates' lamps are already amber at 0.100 against a
    # brown target of 0.072. Measured ABSOLUTELY - which is how this probe's first cut worked - a
    # check of |hue - 0.072| < 0.055 passes on the UNTOUCHED plate, i.e. it cannot fail. The diff
    # mask already stops that (an untouched plate contributes no pixels at all), but the hue still
    # says almost nothing here, so the LUMINANCE carries the assertion: that is what actually makes
    # brown look like brown, and it is measured against what those same pixels used to be.
    cr = meas.get('btn_credits_0916') or {}
    ok(cr.get('lampH') is not None and 0.02 <= cr['lampH'] <= 0.13,
       'credits       lamps are in the brown/amber band (hue %s)'
       % (('%.3f' % cr['lampH']) if cr.get('lampH') is not None else None))
    ok(cr.get('lampVhi') is not None and cr.get('wasVhi') is not None
       and cr['lampVhi'] < cr['wasVhi'] * 0.72,
       'credits       and BROWN, not amber - the tube came down: brightest lamp pixel %.2f, was %.2f'
       % (cr.get('lampVhi') or -1, cr.get('wasVhi') or -1))
    ok(cr.get('textH') is not None and 0.02 <= cr['textH'] <= 0.13,
       'credits       lettering is in the same band (hue %s)'
       % (('%.3f' % cr['textH']) if cr.get('textH') is not None else None))
    ok(cr.get('textV') is not None and cr.get('wasTV') is not None
       and cr['textV'] < cr['wasTV'] * 0.80,
       'credits       and darker than the gold it replaced (value %.2f, was %.2f)'
       % (cr.get('textV') or -1, cr.get('wasTV') or -1))
    ex = meas.get('btn_exit_0916') or {}
    ok(ex.get('lampS') is not None and ex.get('wasS') is not None and ex['lampS'] < 0.20 < ex['wasS'],
       'exit          lamps went WHITE: lamp saturation %.2f, was %.2f'
       % (ex.get('lampS') or -1, ex.get('wasS') or -1))
    ok((ex.get('textS') or 1) < 0.25 and (ex.get('textV') or 0) > 0.70,
       'exit          and so did the lettering (saturation %.2f, value %.2f)'
       % (ex.get('textS') or -1, ex.get('textV') or -1))
    ok(max(asp) - min(asp) < 0.30,
       'and the recolour did not move a single plate size (spread %.3f)' % (max(asp) - min(asp)))

    # ---- THE BUSTED ARM. The pre-decode fallback only runs before the art lands, so it has never
    # once been exercised by a green run - and it is where the seventh row drew with no icon.
    # MENU_KEYS[0] is repointed at a key nothing registers, which is exactly what a failed decode
    # looks like to the gate, and drawMenuButton is wrapped to record the icon each row asked for.
    pg.evaluate("""() => {
      window.__icons=[]; window.__k0=MENU_KEYS[0];
      window.__dmb=drawMenuButton;
      drawMenuButton=function(cx,cy,w,h,label,sel,icon){
        window.__icons.push({label:label, icon:(icon===undefined?'<undefined>':icon)});
        return window.__dmb.apply(null, arguments); };
      MENU_KEYS[0]='btn_no_such_plate_0916';
    }""")
    pg.evaluate("() => { window.__icons=[]; }")
    pg.evaluate(sh.STEP, [1])
    fb = pg.evaluate("() => window.__icons.slice()")
    pg.evaluate("() => { MENU_KEYS[0]=window.__k0; drawMenuButton=window.__dmb; }")
    print('  fallback rows:', json.dumps(fb))
    ok(len(fb) == 7, 'BUSTED: with the gate failing, the fallback draws all seven rows (%d)' % len(fb))
    ok(fb and all(r['icon'] != '<undefined>' for r in fb),
       'and every one of them carries an icon - EXIT GAME included (this is the bug it replaces)')
    ok(fb and [r['label'] for r in fb] == items, 'in TITLE_ITEMS order')

    # and the real art comes back once the gate is restored
    pg.evaluate("() => { window.__blits=[]; }")
    pg.evaluate(sh.STEP, [1])
    back = pg.evaluate("() => window.__blits.filter(b=>b.k.slice(-5)==='_0916').length")
    ok(back >= 7, 'CONTROL: restoring the key puts the seven plates straight back (%d blits)' % back)

    # ACHIEVEMENTS still opens its gallery from the new plate
    pg.evaluate("() => { menuIndex=TITLE_ITEMS.indexOf('ACHIEVEMENTS'); chooseTitle(); }")
    pg.evaluate(sh.STEP, [40])
    st = pg.evaluate("() => state")
    ok(st == 'achievements', 'choosing the ACHIEVEMENTS row still opens the gallery (state %s)' % st)
    pg.screenshot(path=os.path.join(OUT, '16_awards_from_title.png'))

    ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
    for e in errs[:5]: print('    !', e)
    br.close()

print('\n%d ok / %d fail' % (N['ok'], N['fail']))
sys.exit(1 if N['fail'] else 0)
