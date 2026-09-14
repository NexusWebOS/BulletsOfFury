#!/usr/bin/env python3
"""Live Chromium proof for normal impact audio and silhouette-only element flashes."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "element_hit_flashes_live"


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
    console_errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
            page = browser.new_page(viewport={"width": 760, "height": 820})
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on(
                "console",
                lambda msg: console_errors.append(msg.text) if msg.type == "error" else None,
            )
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function(
                "() => typeof spawnEnemy==='function' && typeof opposingElementImpact==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.mouse.click(380, 410)
            page.wait_for_timeout(300)
            page.evaluate("""() => {
              Audio.setVol('master',0);Audio.setVol('sfx',0);
              XART._touch('s2atk_golem_0');XART._touch('s3atk_tank_0');
            }""")
            page.wait_for_function(
                "() => XART.rdy('s2atk_golem_0') && XART.rdy('s3atk_tank_0')",
                timeout=30_000,
            )

            def stage_flash(stage: int, enemy_type: str, projectile_element: str, file_name: str):
                row = page.evaluate(
                    """([stage,type,projectileElement]) => {
                      beginStage(stage);setState(GS.PLAY);player.reset();player.dead=false;
                      player.invuln=99999;player.x=VW/2;player.y=VH-56;snapCamToPlayer();
                      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
                      enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
                      boss=null;bossActive=false;subBoss=null;subBossActive=false;
                      const e=spawnEnemy(type,VW/2,VH*.40,{});
                      e.pattern='proof_hold';e.vx=0;e.vy=0;e.shoots=false;e.hp=e.maxhp=999;
                      const reaction=opposingElementImpact(e,'enemy',{_el:projectileElement});
                      e.flash=99;window.__proofEnemy=e;
                      return {stage,type,projectileElement,reaction,color:e._hitFlashColor,
                        elementalObjects:pImpacts.filter(p=>p.elemental).length};
                    }""",
                    [stage, enemy_type, projectile_element],
                )
                page.wait_for_timeout(220)
                page.locator("#screen").screenshot(path=str(OUT / file_name))
                row["liveColor"] = page.evaluate("() => window.__proofEnemy._hitFlashColor")
                return row

            report["iceOnFire"] = stage_flash(2, "golem", "ice", "01_ice_on_fire_light_blue.png")
            report["fireOnIce"] = stage_flash(3, "s3tank", "fire", "02_fire_on_ice_red.png")

            report["audio"] = page.evaluate("""() => {
              const count={hit:0,special:0};
              Audio.SFX.hit=()=>count.hit++;
              for(const k of ['flameHit','iceBreathHit','laserBeamHit','chainHit','enemyHit'])
                Audio.SFX[k]=()=>count.special++;
              _hitSfxAt={};stateT+=1;
              _dmgBullet={kind:'flame',_el:'fire'};hitEnemy(window.__proofEnemy,1);
              stateT+=1;_dmgBullet={kind:'iceorb',_el:'ice'};hitEnemy(window.__proofEnemy,1);
              stateT+=1;_dmgBullet={kind:'beam'};hitEnemy(window.__proofEnemy,1);
              return count;
            }""")
            report["pageErrors"] = page_errors
            report["consoleErrors"] = console_errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert report["iceOnFire"]["reaction"] == "ice", report
    assert report["iceOnFire"]["color"] == "#83d9ff", report
    assert report["fireOnIce"]["reaction"] == "fire", report
    assert report["fireOnIce"]["color"] == "#ff3b30", report
    assert report["iceOnFire"]["elementalObjects"] == 0, report
    assert report["fireOnIce"]["elementalObjects"] == 0, report
    assert report["audio"] == {"hit": 3, "special": 0}, report
    assert not page_errors, page_errors
    assert not console_errors, console_errors
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
