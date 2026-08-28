#!/usr/bin/env python3
"""Live browser proof for the Stage 5 Fury-kit cinematic and Stage 9 retention."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "gravity_mode_stage5_stage9_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


STAGE5_SETUP = """() => {
  beginStage(5); player.reset(); player.invuln=999999; snapCamToPlayer();
  setState(GS.LAUNCH); gravityModeReset(); gravityModeStart();
  drawLaunch._phase='settle'; drawLaunch._pt=0.12; drawLaunch._lastT=stateT;
  drawLaunch._dist=SEG_B3+1750; drawLaunch._spd=LAUNCH_COUNTDOWN_SCROLL;
  drawLaunch._bgScroll=SEG_B3+1750; drawLaunch._mus=true; drawLaunch._go=false; drawLaunch._num=99;
  return {stage:run.stage,pilot:run.pilot,line:gravityMode.line,phase:gravityMode.phase};
}"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    page_errors: list[str] = []
    console_errors: list[str] = []
    report: dict = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 1040, "height": 1120}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function("() => typeof beginStage==='function' && typeof gravityModeStart==='function'", timeout=60_000)
            page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=45_000)
            page.evaluate("""() => {
              ['ngm_space_atlas','bg_stage05_loop','nl6sky_stage06_sky_scroll_640x960',
               'nst9_voidwater_master',...Array.from({length:8},(_,i)=>'nfx_wportal_'+i)].forEach(k=>XART._touch(k));
            }""")
            page.wait_for_function(
                "() => XART.rdy('ngm_space_atlas') && XART.rdy('bg_stage05_loop') && XART.rdy('nfx_wportal_0')",
                timeout=60_000,
            )

            stage5 = page.evaluate(STAGE5_SETUP)
            canvas = page.locator("#screen")

            # The intro is one continuous sky-to-space climb, not a cut to the space plate.
            page.evaluate("""() => {
              drawLaunch._phase='run';drawLaunch._pt=0;drawLaunch._lastT=stateT;
              drawLaunch._dist=SEG_B1*0.10+SEG_B3*0.72*0.42;drawLaunch._spd=220;
              drawLaunch._bgScroll=drawLaunch._dist;gravityMode.dialogueT=gravityMode.dialogueDelay+0.72;
              gravityMode.dialogueDone=false;
            }""")
            page.wait_for_timeout(45)
            canvas.screenshot(path=str(OUT / "00_stage5_sky_to_space_ascent.png"))

            # Kit parts are already travelling with the aircraft while Fury HQ types the warning.
            page.evaluate("""() => {
              drawLaunch._phase='settle';drawLaunch._pt=0.12;drawLaunch._lastT=stateT;
              drawLaunch._dist=SEG_B3+1750;drawLaunch._spd=LAUNCH_COUNTDOWN_SCROLL;
              drawLaunch._bgScroll=SEG_B3+1750;
              gravityMode.dialogueT=gravityMode.dialogueDelay+(gravityMode.line.length/44)+0.10;
              gravityMode.dialogueDone=false;
            }""")
            page.wait_for_timeout(55)
            canvas.screenshot(path=str(OUT / "01_stage5_ascent_hq_dispatch.png"))

            # Five authored charge speeds: the first and fifth frames make the acceleration visible.
            for name, tick, band, age in (
                ("02_stage5_spiral_slow", 0.44, 0, 1.10),
                ("03_stage5_spiral_turbo", 3.72, 4, 4.38),
                ("04_stage5_gravity_scatter", 0.46, 4, 4.72),
                ("05_stage5_fast_snap", 0.40, 4, 5.34),
                ("06_stage5_pixel_glow", 0.61, 4, 5.93),
                ("07_stage5_white_fusion", 0.27, 4, 6.44),
                ("08_stage5_reveal", 0.50, 4, 7.05),
                ("09_stage5_fury_ship_online", 0.0, 4, 8.0),
            ):
                phase = {
                    "02_stage5_spiral_slow": "charge",
                    "03_stage5_spiral_turbo": "charge",
                    "04_stage5_gravity_scatter": "scatter",
                    "05_stage5_fast_snap": "snap",
                    "06_stage5_pixel_glow": "pixelglow",
                    "07_stage5_white_fusion": "whiteout",
                    "08_stage5_reveal": "reveal",
                    "09_stage5_fury_ship_online": "active",
                }[name]
                page.evaluate(
                    "([p,t,b,a])=>{drawLaunch._phase=(p==='active'?'cd':'gravity');drawLaunch._pt=0.12;gravityMode.phase=p;gravityMode.t=t;gravityMode.chargeBand=b;gravityMode.age=a;}",
                    [phase, tick, band, age],
                )
                page.wait_for_timeout(45)
                canvas.screenshot(path=str(OUT / f"{name}.png"))

            # Exercise the phase machine separately so direct proof poses cannot hide a broken handoff.
            phase_machine = page.evaluate("""() => {
              beginStage(5); gravityModeStart(); gravityMode.dialogueDone=true; gravityModeBeginCharge();
              const seen=[gravityMode.phase]; let guard=0;
              while(gravityMode.phase!=='active' && guard++<300){
                const before=gravityMode.phase; gravityModeTick(0.05);
                if(gravityMode.phase!==before)seen.push(gravityMode.phase);
              }
              return {seen,ready:run.gravityShipReady,guard};
            }""")

            # Stage 9 begins on the far side of the secret portal with the Fury ship already active.
            page.evaluate("""() => {
              beginStage(9); player.reset(); player.invuln=999999; snapCamToPlayer();
              setState(GS.LAUNCH); drawLaunch._phase=undefined;
            }""")
            page.wait_for_timeout(80)
            page.evaluate("""() => {
              drawLaunch._phase='run';drawLaunch._pt=0;drawLaunch._lastT=stateT;
              drawLaunch._dist=360;drawLaunch._spd=110;drawLaunch._bgScroll=360;drawLaunch._mus=true;
            }""")
            page.wait_for_timeout(45)
            canvas.screenshot(path=str(OUT / "10_stage9_retained_ship_portal_escape.png"))
            stage9_entry = page.evaluate("""() => ({stage:run.stage,space:run.spaceMode,
              gravityPhase:gravityMode&&gravityMode.phase,retained:gravityMode&&gravityMode.retained,
              ready:run.gravityShipReady,launchPhase:drawLaunch._phase})""")

            # A settled Stage 9 launch must go straight to GET READY, never back to assembly.
            page.evaluate("""() => {drawLaunch._phase='settle';drawLaunch._pt=0.44;drawLaunch._lastT=stateT;}""")
            page.wait_for_timeout(90)
            stage9_handoff = page.evaluate("""() => ({launchPhase:drawLaunch._phase,
              gravityPhase:gravityMode&&gravityMode.phase,ready:run.gravityShipReady})""")

            report = {
                "stage5": stage5,
                "phaseMachine": phase_machine,
                "stage9Entry": stage9_entry,
                "stage9Handoff": stage9_handoff,
                "pageErrors": page_errors,
                "consoleErrors": console_errors,
            }
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert not page_errors and not console_errors
    assert "TOO DANGEROUS TO TRAVEL TO SPACE" in stage5["line"]
    assert "FURY HQ IS DISPATCHING A SPACESHIP KIT YOUR WAY, STAT!" in stage5["line"]
    assert phase_machine["seen"] == ["charge", "scatter", "snap", "pixelglow", "whiteout", "reveal", "active"]
    assert phase_machine["ready"] is True
    assert stage9_entry["gravityPhase"] == "active" and stage9_entry["retained"] is True
    assert stage9_entry["ready"] is True and stage9_entry["space"] is True
    assert stage9_handoff["launchPhase"] == "cd" and stage9_handoff["gravityPhase"] == "active"


if __name__ == "__main__":
    main()
