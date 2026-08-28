#!/usr/bin/env python3
"""Live browser proof for the reconciled Stage 6, Gravity ship, icons and container fixes."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "reconciled_repairs_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    page_errors: list[str] = []
    console_errors: list[str] = []
    report: dict = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 1040, "height": 1120}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof beginStage==='function' && (window.__bofFrames|0)>4", timeout=60_000)
            canvas = page.locator("#screen")

            # Stage 6: force the live director into its storm interval. drawWorld must be the caller.
            page.evaluate("""() => {
              beginStage(6);setState(GS.PLAY);player.reset();player.invuln=999999;
              player.x=worldWidth()/2;player.y=VH-72;snapCamToPlayer();stagePlan=[];waveIdx=999;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
              stageTimer=curStage.length*0.31;_bg6T=8;_bg6BoltGap=0;_bg6BoltT=0.04;
              window.__repairUpdate=updatePlay;updatePlay=function(){};
              ['nsky6_sky','bg6_cloud_day_0','bg6_rain_heavy','bg6_rain_turbulent','bg6_moon_full',
               ...Array.from({length:8},(_,i)=>'bg6_bolt_'+i),...Array.from({length:4},(_,i)=>'bg6_flash_'+i)]
                .forEach(k=>XART._touch(k));
            }""")
            page.wait_for_function("() => XART.rdy('nsky6_sky') && XART.rdy('bg6_cloud_day_0') && XART.rdy('bg6_rain_heavy')", timeout=45_000)
            page.wait_for_timeout(120)
            canvas.screenshot(path=str(OUT / "01_stage6_live_storm_overlay.png"))
            stage6 = page.evaluate("""() => ({stage:run.stage,phase:bg6Phase(),wet:bg6StormStrength(),
              liveCall:drawWorld.toString().includes('if(run.stage===6) bg6Draw(dt)'),bolt:_bg6BoltT})""")

            # Stage 5: active recovered ship at normal player scale, then fire from both real pods.
            page.evaluate("""() => {
              beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999999;
              player.x=worldWidth()/2;player.y=VH-82;snapCamToPlayer();stagePlan=[];waveIdx=999;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
              gravityModeRetain();gravityMode.phase='active';run.gravityShipReady=true;
              run.spaceWeapon=0;run.spaceLevels=[5,0,0];spaceLaserFire();
              for(let f=0;f<9;f++)for(const b of pBullets)spaceBulletTick(b,1/60);
              player._spaceMuzzle=0.08;
            }""")
            page.wait_for_function("() => SPACE_ATLAS_FRAMES && XART.rdy('ngm_space_atlas')", timeout=45_000)
            page.wait_for_timeout(100)
            canvas.screenshot(path=str(OUT / "02_stage5_60px_ship_turret_lasers.png"))
            gravity = page.evaluate("""() => {const h=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE);
              return {size:SPACE_SHIP_SIZE,player:{x:player.x,y:player.y},hardpoints:h,
                rounds:pBullets.filter(b=>b.kind==='spaceLaser').map(b=>({x:b._muzzleX,y:b._muzzleY})).slice(0,2)};}""")

            # The dedicated space collision path must open a capsule and create its reward.
            container = page.evaluate("""() => {
              pBullets.length=0;powerups.length=0;const h=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).laser[0];
              const c={kind:'capsule',x:h.x,y:h.y-72,w:22,h:32,hp:1,flash:0,dead:false};powerups.push(c);
              spaceLaserFire();for(let f=0;f<18;f++)for(const b of pBullets)if(!b.dead)spaceBulletTick(b,1/60);
              return {broken:c.dead,rewards:powerups.filter(p=>p!==c&&!p.dead).map(p=>p.kind)};
            }""")

            # Render the exact nine production special icons through the live shared blitter.
            page.evaluate("""() => {
              const old=document.getElementById('repair-icon-proof');if(old)old.remove();
              const c=document.createElement('canvas');c.id='repair-icon-proof';c.width=920;c.height=360;
              c.style.cssText='position:fixed;left:0;top:0;z-index:999999;background:#070b13';document.body.appendChild(c);
              const g=c.getContext('2d'),pilots=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'];
              g.imageSmoothingEnabled=false;g.fillStyle='#f1bd4e';g.font='bold 24px monospace';g.fillText('FURY SPECIAL ABILITY ICONS - LIVE ROUTE',24,38);
              pilots.forEach((p,i)=>{const x=58+(i%5)*176,y=115+Math.floor(i/5)*145;iconBlit(g,'spicon_'+p,x,y,72,true);
                g.fillStyle='#dce8ff';g.font='bold 14px monospace';g.textAlign='center';g.fillText(p.toUpperCase(),x,y+58);});
            }""")
            page.locator("#repair-icon-proof").screenshot(path=str(OUT / "03_all_nine_special_icons.png"))
            icons = page.evaluate("""() => ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
              .map(p=>({pilot:p,width:iconBlit(document.createElement('canvas').getContext('2d'),'spicon_'+p,0,0,64,false)}))""")

            report = {"stage6": stage6, "gravity": gravity, "container": container, "icons": icons,
                      "pageErrors": page_errors, "consoleErrors": console_errors}
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert not page_errors and not console_errors
    assert stage6["liveCall"] and 0.25 < stage6["phase"] < 0.4 and stage6["wet"] > 0.5
    assert gravity["size"] == 60 and len(gravity["rounds"]) == 2
    assert gravity["rounds"][0]["x"] == gravity["hardpoints"]["laser"][0]["x"]
    assert gravity["rounds"][1]["x"] == gravity["hardpoints"]["laser"][1]["x"]
    assert container["broken"] and container["rewards"]
    assert len(icons) == 9 and all(i["width"] for i in icons)


if __name__ == "__main__":
    main()
