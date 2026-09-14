#!/usr/bin/env python3
"""Browser/decode smoke test for the approved 2026-08-29 sound routing."""

from __future__ import annotations

import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
KEYS = [
    "enemyMachineGunHeavy", "heavyMachineGun", "dkReload", "enemyPulseLaserBlue",
    "laserCannon", "spaceLaserCannon", "atomicLaunch", "atomicDetonate",
    "flameThrowerStart", "flameThrowerLoop", "flameThrowerEnd", "amb_storm",
    "spaceShadowRelease", "laserBeamStart", "laserBeamLoop", "laserBeamEnd",
    "helixChargeStart", "helixCharge", "maverickHelixRelease", "gravityTransform",
    "gravityFuse", "megaShieldPickup", "specialAbilityPickup", "sonicChargeStart",
    "sonicChargeLoop", "coleSonicBoom",
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main() -> None:
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    errors: list[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(f"http://127.0.0.1:{server.server_port}/minimal.html", wait_until="load")
            page.wait_for_function("typeof Snd==='object' && Snd && Snd.pools", timeout=15000)
            result = page.evaluate(
                """async (keys) => {
                  const rows=[];
                  for(const key of keys){
                    const pool=Snd.pools[key], a=pool&&pool.list&&pool.list[0];
                    if(!a){rows.push({key,ok:false,why:'missing pool'});continue;}
                    a.load();
                    if(!(a.readyState>=1 && Number.isFinite(a.duration))){
                      await new Promise(resolve=>{
                        const done=()=>resolve();
                        a.addEventListener('loadedmetadata',done,{once:true});
                        a.addEventListener('error',done,{once:true});
                        setTimeout(done,3000);
                      });
                    }
                    rows.push({key,ok:a.readyState>=1&&Number.isFinite(a.duration)&&a.duration>0,
                               duration:Number.isFinite(a.duration)?a.duration:0,
                               file:(a.src.split('/').pop()||'')});
                  }
                  beginStage(6);
                  return {rows,stage6Ambience:_ambStage===6&&!!_ambEl};
                }""",
                KEYS,
            )
            browser.close()
    finally:
        server.shutdown()

    bad = [row for row in result["rows"] if not row["ok"]]
    if errors or bad or not result["stage6Ambience"]:
        raise SystemExit(
            f"FAIL page_errors={errors} decode_failures={bad} "
            f"stage6_ambience={result['stage6Ambience']}"
        )
    print(f"PASS: {len(result['rows'])} routed samples decoded; Stage 6 atmosphere started")
    for row in result["rows"]:
        print(f"  {row['key']:<26} {row['duration']:.3f}s  {row['file']}")


if __name__ == "__main__":
    main()
