#!/usr/bin/env python3
"""Live Chromium proof for Stage 1/2 miniboss durability and Maverick's encounter cap."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "helix_hp_live_0830"


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
    errors: list[str] = []
    report: dict = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820})
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function(
                "() => typeof spawnSubBoss==='function' && typeof helixFlurrySpawn==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.mouse.click(380, 410)

            report["minibosses"] = page.evaluate("""() => {
              const out={};
              for(const [stage,kind] of [[1,'junglecruiser'],[2,'magmaward']]){
                beginStage(stage);setState(GS.PLAY);player.reset();player.invuln=999999;
                enemies.length=0;eBullets.length=0;pBullets.length=0;boss=null;bossActive=false;
                subBoss=null;subBossActive=false;spawnSubBoss(kind);
                out[kind]={hp:subBoss.hp,maxhp:subBoss.maxhp,ship:subBoss._ship};
              }
              return out;
            }""")

            page.evaluate("""() => {
              beginStage(2);setState(GS.PLAY);player.reset();player.invuln=999999;
              player.x=240;player.y=438;snapCamToPlayer();
              stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
              subBoss=null;subBossActive=false;boss=null;bossActive=false;
              spawnBoss('infernoreaver');boss.enter=false;boss.x=240;boss.y=116;boss.ty=116;
              boss.fireCd=999;boss._sba={pat:'proof',t:0,tell:999,recover:999,kick:0,shake:0,fired:true};
              window.__helixBefore={hp:boss.hp,maxhp:boss.maxhp};
              /* Match real play: the charged ball bursts from the player's approach lane.
                 Bursting inside a hull sends the five radial fans outward before acquisition. */
              helixFlurrySpawn(player.x,player.y-34,5,true);
              /* Run the real gameplay update deterministically. Stage-entry UI timers can briefly
                 own the browser RAF even after a forced PLAY state; direct fixed ticks keep this
                 an encounter test instead of a transition-timing test. */
              for(let i=0;i<240;i++)updatePlay(1/60);
            }""")
            page.wait_for_timeout(120)
            report["helix"] = page.evaluate("""() => ({
              before:window.__helixBefore,
              after:{hp:boss.hp,maxhp:boss.maxhp},
              dealt:window.__helixBefore.hp-boss.hp,
              ratio:(window.__helixBefore.hp-boss.hp)/window.__helixBefore.maxhp,
              survivingLances:pBullets.filter(b=>b.kind==='mavlaser'&&!b.dead).length
            })""")
            page.locator("#screen").screenshot(path=str(OUT / "helix_stage2_boss_cap.png"))
            report["pageErrors"] = errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    report["assertions"] = {
        "jungleCruiserAtLeast900": report["minibosses"]["junglecruiser"]["maxhp"] >= 900,
        "magmaWardAtLeast1100": report["minibosses"]["magmaward"]["maxhp"] >= 1100,
        "helixExactlyQuarterGauge": abs(report["helix"]["ratio"] - 0.25) < 1e-9,
        "noPageErrors": not errors,
    }
    report["passed"] = all(report["assertions"].values())
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not report["passed"]:
        raise AssertionError(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
