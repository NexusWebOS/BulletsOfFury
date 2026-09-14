#!/usr/bin/env python3
"""Live Chromium regression probe for the shared laser beam and flamethrower audio."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "ground_held_weapon_audio_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    report: dict = {}
    page_errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                args=["--disable-gpu", "--no-sandbox", "--autoplay-policy=no-user-gesture-required"]
            )
            page = browser.new_page(viewport={"width": 760, "height": 820})
            page.add_init_script("""(() => {
              window.__mediaPlayCalls=[];
              const original=HTMLMediaElement.prototype.play;
              HTMLMediaElement.prototype.play=function(){
                const row={src:this.src.split('/').pop(),volume:this.volume,loop:this.loop,
                  ready:this.readyState,paused:this.paused,currentTime:this.currentTime,
                  status:'called',at:performance.now()};
                window.__mediaPlayCalls.push(row);
                let p;try{p=original.call(this);}catch(e){row.status='throw:'+e.name;throw e;}
                if(p&&p.then)p.then(()=>row.status='playing').catch(e=>row.status='reject:'+e.name);
                return p;
              };
            })()""")
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function(
                "() => typeof flameFire==='function' && typeof pShoot==='function' && typeof Snd!=='undefined' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.mouse.click(380, 410)
            page.wait_for_timeout(500)
            page.evaluate("""() => {
              beginStage(1);setState(GS.PLAY);player.reset();player.dead=false;player.invuln=99999;
              player.x=240;player.y=410;snapCamToPlayer();
              stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
              boss=null;bossActive=false;subBoss=null;subBossActive=false;
              run.spaceMode=false;run.pilot='axel';run.wlevels=[5,5,5,5,5,5];run.wlevel=5;
              Audio.setVol('master',1);Audio.setVol('sfx',1);Snd._last={};
              Snd.prepare(['laserBeamStart','laserBeamLoop','laserBeamEnd',
                'flameThrowerStart','flameThrowerLoop','flameThrowerEnd','flameHit']);
              Snd.loopPrepare('laserBeamLoop');Snd.loopPrepare('flameThrowerLoop');
            }""")
            page.wait_for_function(
                "() => ['laserBeamStart','flameThrowerStart'].every(n=>Snd.pools[n].list.some(a=>a.readyState>=3))",
                timeout=20_000,
            )

            for name, weapon in (("flamethrower", 4), ("laser", 3)):
                page.evaluate("""w => {
                  pBullets.length=0;window.__mediaPlayCalls.length=0;Snd._last={};
                  Snd.loopStopAll();run.weapon=w;run.wlevel=5;
                  if(!run.wvars)run.wvars=[null,null,null,null,null,null];
                  if(w===4)run.wvars[4]='flamethrower';
                  player.fireCd=0;window.__heldOldDown=Input.down;
                  Input.down=function(k){return keybind.fire.indexOf(k)>=0?true:window.__heldOldDown(k);};
                }""", weapon)
                page.wait_for_timeout(650)
                suspended = page.evaluate("""async () => {
                  if(!Snd._ctx||!Snd._ctx.suspend)return 'none';
                  await Snd._ctx.suspend();return Snd._ctx.state;
                }""")
                page.wait_for_timeout(450)
                report[name] = page.evaluate("""([loopName,startName]) => {
                  const L=Snd.loops[loopName];const P=Snd.pools[startName];
                  return {
                    calls:window.__mediaPlayCalls.slice(),
                    context:Snd._ctx?Snd._ctx.state:'none',
                    loop:L?{on:L.on,hold:L.hold,lvl:L.lvl,paused:L.el.paused,
                      ready:L.el.readyState,currentTime:L.el.currentTime,volume:L.el.volume,
                      nativeOutput:!L.el._bofNode,
                      ended:L.el.ended,error:L.el.error?{code:L.el.error.code,message:L.el.error.message}:null}:null,
                    start:P?P.list.map(a=>({ready:a.readyState,paused:a.paused,
                      currentTime:a.currentTime,volume:a.volume,error:a.error?{code:a.error.code,message:a.error.message}:null})):[]
                  };
                }""", ["flameThrowerLoop" if weapon == 4 else "laserBeamLoop",
                         "flameThrowerStart" if weapon == 4 else "laserBeamStart"])
                report[name]["suspendIssuedState"] = suspended
                page.evaluate("""() => {Input.down=window.__heldOldDown;window.__heldOldDown=null;}""")
                page.wait_for_timeout(700)

            report["pageErrors"] = page_errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for weapon in ("flamethrower", "laser"):
        row = report[weapon]
        assert row["loop"]["on"] and not row["loop"]["paused"], row
        assert row["loop"]["currentTime"] > 0.25, row
        assert row["loop"]["volume"] >= 0.60, row
        if weapon == "laser":
            assert row["context"] == "running", row
        assert any(c["status"] == "playing" for c in row["calls"]), row
    assert report["flamethrower"]["loop"]["nativeOutput"], report["flamethrower"]
    assert not page_errors, page_errors
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
