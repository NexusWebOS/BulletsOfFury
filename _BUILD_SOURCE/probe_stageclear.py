#!/usr/bin/env python3
"""probe_stageclear.py - the tester's stage-clear complaint, rendered instead of reasoned about.

  "Stage-clear text centring - the label column and the value column disagree; the rank letter
   and portrait collide with the first rows."

Renders the screen at three points in its own timeline (rows still filling, rows done, fully
settled) because the layout is animated: a single late screenshot cannot show a collision that
only exists while a row is sliding in, and a single early one cannot show the score block.

It also reads the LAYOUT CONSTANTS out of the running game and prints the derived column edges,
so a disagreement between the label column and the value column can be stated as two numbers
rather than argued from a screenshot.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SETUP = r"""
(frames)=>{
  ASSETS.ready=true;
  run.stage=1; run.pilot='cole'; run.score=41250;
  /* REAL STATS, NOT ZEROES. Every row read 0 / 0% / 0:00 on an unplayed run - the shortest
     possible string in the value column, which is exactly the case that CANNOT show a column
     disagreement. Seeded to plausible end-of-stage numbers so the widest values (a fraction, a
     percent, a clock) are the ones being measured. */
  stageStats.kills=137; stageStats.spawned=152; stageStats.shots=2841; stageStats.hits=1794;
  stageStats.missiles=46; stageStats.mslHits=39; stageStats.dmgDealt=98420;
  stageStats.deaths=1; stageStats.livesStart=3; stageStats.scoreStart=0;
  stageStats.spShots=12; stageStats.spHits=11; stageStats.spDmg=15600;
  drawStageClear._init=false; drawStageClear._row=0; drawStageClear._segT=0;
  drawStageClear._scoreShown=run.score|0;
  setState(GS.STAGECLEAR);
  /* stateT IS ADVANCED BY THE GAME LOOP, NOT BY THE DRAW CALL. Pumping drawStageClear alone left
     t at 0.00 for every frame, so all three "timeline points" rendered the same 0.18s early-out
     and the screen was just the empty panel. */
  for(let i=0;i<frames;i++){ stateT+=1/60; try{ drawStageClear(1/60); }catch(e){} }
  const r=drawStageClear._rect||[0,0,0,0], px=r[0],py=r[1],pw=r[2],ph=r[3];
  const R=drawStageClear._res||{rows:[]};
  return {
    VW:VW, VH:VH, rect:r, t:stateT, row:drawStageClear._row, nrows:R.rows.length,
    labels:R.rows.map(x=>x.label+' = '+x.text),
    /* the same expressions the draw code uses, so these ARE the drawn positions */
    portrait:{ x:px+pw*0.046, r:px+pw*0.268, y:py+ph*0.215, w:(px+pw*0.268-(px+pw*0.046))*0.86 },
    rowsX:px+pw*0.290, rowsW:pw*0.610, rowY0:py+ph*0.170, rowH:ph*0.062,
    headerY:py+ph*0.118, scoreY:py+ph*0.744,
    img:document.getElementById('screen').toDataURL('image/png') };
}
"""

LONGPW = r"""
()=>{
  drawStageClear._res.pw='THUNDERX';        // 8 chars: the case the 0.52 centre cannot fit
  drawStageClear._pwChars=99;
  for(let i=0;i<40;i++){ stateT+=1/60; try{ drawStageClear(1/60); }catch(e){} }
  const r=drawStageClear._rect, px=r[0],py=r[1],pw=r[2],ph=r[3];
  return {VW:VW,VH:VH,rect:r,t:stateT,row:drawStageClear._row,nrows:drawStageClear._res.rows.length,
          img:document.getElementById('screen').toDataURL('image/png')};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)

    for tag, frames in (('mid', 70), ('rows', 260), ('settled', 700), ('longpw', 700)):
        r = pg.evaluate(SETUP, frames)
        if tag == 'longpw':
            # the password is typed and LEFT-anchored, so the failure case is a long one running
            # back into its own label - IRON is four characters and can never show it.
            r = pg.evaluate(LONGPW)
        name = 'stageclear_%s_0812b.png' % tag
        with open(os.path.join(OUT, name), 'wb') as f:
            f.write(base64.b64decode(r['img'].split(',', 1)[1]))
        if tag == 'mid':
            px, py, pw, ph = r['rect']
            print('viewport %dx%d   panel x=%.1f y=%.1f w=%.1f h=%.1f' % (r['VW'], r['VH'], px, py, pw, ph))
            print('portrait column   x %.1f .. %.1f   top %.1f   w %.1f'
                  % (r['portrait']['x'], r['portrait']['r'], r['portrait']['y'], r['portrait']['w']))
            print('rows              x %.1f .. %.1f   y0 %.1f   pitch %.1f'
                  % (r['rowsX'], r['rowsX'] + r['rowsW'], r['rowY0'], r['rowH']))
            gap = r['rowsX'] - r['portrait']['r']
            print('gap portrait->rows %.1f px %s' % (gap, '' if gap >= 0 else '  *** COLUMNS OVERLAP ***'))
            print('header y %.1f, first row y %.1f, score y %.1f' % (r['headerY'], r['rowY0'], r['scoreY']))
            print('rows (%d):' % r['nrows'])
            for s in r['labels']:
                print('   %s' % s)
        print('  wrote docs/proofs/%s   (t=%.2f, row %d/%d)' % (name, r['t'], r['row'], r['nrows']))
    b.close()
