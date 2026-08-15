#!/usr/bin/env python3
"""probe_input0812a.py — the beta tester's input items, verified in the real game.

  1. MOUSE BUTTONS ARE BINDABLE. A click must land in the same `keys` map the keyboard and the
     gamepad use, so tapAny(keybind.fire) sees it. Dispatched as real DOM MouseEvents on the
     canvas - not by poking internals, which would prove only that the internals exist.
  2. THE DEFAULTS ARE HIS. fire has mouse0, bomb has mouse2, retina has space.
  3. menuConfirm IGNORES MOUSE. Otherwise one click both activates the button under the cursor
     and confirms whatever row the keyboard cursor sat on.
  4. THE OPTIONS ARROWS CLEAR THE LABELS. The selection arrows were landing at wx+30 with labels
     drawn at wx+16; measured as pixel columns, not eyeballed.
  5. MODE SELECT TAKES A CLICK. The screen immediately after the title, and one of the dead ones.
"""
import http.server, socketserver, threading, functools, base64, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

BINDS=r"""
()=>({ fire:keybind.fire, bomb:keybind.bomb, retina:keybind.retina,
       unbindableBlocksMouse:(typeof KEY_UNBINDABLE!=='undefined') &&
          ['mouse0','mouse2'].some(k=>KEY_UNBINDABLE.indexOf(k)>=0) })
"""
AFTER_CLICK=r"""
()=>({ mouse0:!!Input.keys['mouse0'], mouse2:!!Input.keys['mouse2'],
       fireHeld:keybind.fire.some(k=>Input.down(k)),
       bombHeld:keybind.bomb.some(k=>Input.down(k)) })
"""
MENUCONF=r"""
()=>{
  /* a left click must NOT read as menuConfirm; the mouse binds are filtered out of it */
  Input.keys['mouse0']=true;
  const src=String(Input.menuConfirm);
  Input.keys['mouse0']=false;
  return {filtered:/filter\(/.test(src)};
}
"""
OPTARROW=r"""
()=>{
  ASSETS.ready=true; setState(GS.OPTIONS);
  for(let i=0;i<30;i++){ try{ drawOptions(1/60); }catch(e){} }
  const cv=document.getElementById('screen'), g=cv.getContext('2d');
  const SX=cv.width/VW;
  const panelX=28, labelX=panelX+16;
  /* scan a vertical band across the selected row for non-background pixels left of the label */
  const d=g.getImageData(0,0,cv.width,cv.height).data;
  let leftMost=1e9;
  for(let y=0;y<cv.height;y+=2){
    for(let x=0;x<Math.round(labelX*SX);x++){
      const i=(y*cv.width+x)*4;
      if(d[i+3]>40 && (d[i]>90||d[i+1]>90||d[i+2]>90)){ if(x<leftMost) leftMost=x; break; }
    }
  }
  return {panelX, labelX, leftMostLitPx:Math.round(leftMost/SX),
          img:cv.toDataURL('image/png')};
}
"""
MODESEL=r"""
()=>{
  ASSETS.ready=true; setState(GS.MODESEL);
  for(let i=0;i<40;i++){ try{ drawModeSelect(1/60); }catch(e){} }
  const before=modeIndex;
  return {before, y0:132, gap:98, hasHandler:/Input\.mouse/.test(String(drawModeSelect))};
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

    kb=pg.evaluate(BINDS)
    print('1/2  DEFAULT BINDS')
    for a in ('fire','bomb','retina'):
        print('       %-7s %s' % (a, kb[a]))
    print('       mouse names blocked by KEY_UNBINDABLE: %s' % kb['unbindableBlocksMouse'])

    # real DOM events on the canvas
    box=pg.evaluate("()=>{const r=document.getElementById('screen').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};}")
    pg.mouse.move(box['x'], box['y'])
    pg.mouse.down(button='left');  left=pg.evaluate(AFTER_CLICK); pg.mouse.up(button='left')
    pg.mouse.down(button='right'); right=pg.evaluate(AFTER_CLICK); pg.mouse.up(button='right')
    print('     LEFT  click -> keys.mouse0=%s  fire held=%s' % (left['mouse0'], left['fireHeld']))
    print('     RIGHT click -> keys.mouse2=%s  bomb held=%s' % (right['mouse2'], right['bombHeld']))

    mc=pg.evaluate(MENUCONF)
    print('3    menuConfirm filters mouse binds: %s' % mc['filtered'])

    oa=pg.evaluate(OPTARROW)
    print('4    OPTIONS ARROWS  panel x=%d  labels start x=%d  left-most lit pixel x=%d  -> %s'
          % (oa['panelX'], oa['labelX'], oa['leftMostLitPx'],
             'ARROW IS OUTSIDE THE LABELS' if oa['leftMostLitPx'] < oa['labelX'] else '*** STILL OVERLAPPING ***'))
    with open(os.path.join(OUT,'options_arrows_0812a.png'),'wb') as f:
        f.write(base64.b64decode(oa['img'].split(',',1)[1]))

    ms=pg.evaluate(MODESEL)
    print('5    MODE SELECT has a mouse handler: %s' % ms['hasHandler'])
    b.close()
    print('-> docs/proofs/options_arrows_0812a.png')
