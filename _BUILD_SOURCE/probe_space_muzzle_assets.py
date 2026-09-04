#!/usr/bin/env python3
"""Render the live production muzzle families at one comparable scale."""

from __future__ import annotations

import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "space_muzzle_asset_inventory.png"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main() -> None:
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 1100, "height": 1760}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof XART!=='undefined' && (window.__bofFrames|0)>4", timeout=60_000)
            page.evaluate("""() => {
              const rows=[];
              for(let family=1;family<=9;family++) rows.push({name:'JET / NAVAL  nmz_'+family,keys:Array.from({length:4},(_,f)=>'nmz_'+family+'_'+f)});
              for(let level=1;level<=5;level++) rows.push({name:'SPREAD '+level,keys:Array.from({length:4},(_,f)=>'nsf_'+level+'_muzzle_'+f)});
              rows.push({name:'QUAD LASER',keys:Array.from({length:4},(_,f)=>'nql_muzzle_0'+(f+1))});
              rows.push({name:'MAGMA',keys:Array.from({length:4},(_,f)=>'bfx_magma_m_'+f)});
              rows.push({name:'PLAYER MG COLORS',keys:['mgmuz_0','mgmuz_1','mgmuz_2','mgmuz_3','mgmuz_4']});
              for(const row of rows)for(const key of row.keys)XART._touch(key);
              window.__muzzleRows=rows;
            }""")
            page.wait_for_function("() => __muzzleRows.every(r=>r.keys.every(k=>XART.rdy(k)))", timeout=45_000)
            page.evaluate("""() => {
              const old=document.getElementById('muzzle-inventory');if(old)old.remove();
              const rows=window.__muzzleRows,c=document.createElement('canvas');c.id='muzzle-inventory';
              c.width=1080;c.height=100+rows.length*92;c.style.cssText='position:fixed;left:0;top:0;z-index:999999';
              document.body.appendChild(c);const g=c.getContext('2d');g.imageSmoothingEnabled=false;
              g.fillStyle='#080d18';g.fillRect(0,0,c.width,c.height);g.fillStyle='#f0c45b';g.font='bold 25px monospace';
              g.fillText('PRODUCTION MUZZLE OVERLAYS — SAME 58px BOX',24,38);
              g.fillStyle='#8fa6c7';g.font='15px monospace';g.fillText('Rendered through XART from the assets already shipped in the game',24,66);
              rows.forEach((row,i)=>{
                const y=104+i*92;g.fillStyle=i%2?'#0c1424':'#101a2b';g.fillRect(0,y-25,c.width,88);
                g.fillStyle='#d8e4f5';g.font='bold 15px monospace';g.fillText(row.name,18,y+10);
                row.keys.forEach((key,j)=>{
                  const im=XART.get(key),x=360+j*142,w=58,h=58;
                  g.fillStyle='#1b2a40';g.fillRect(x-w/2-3,y-h/2-3,w+6,h+6);
                  g.drawImage(im,x-w/2,y-h/2,w,h);g.fillStyle='#7f97b8';g.font='11px monospace';g.textAlign='center';g.fillText(key,x,y+42);
                });g.textAlign='left';
              });
            }""")
            page.locator("#muzzle-inventory").screenshot(path=str(OUT))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    if errors:
        raise RuntimeError("; ".join(errors))
    print(OUT)


if __name__ == "__main__":
    main()
