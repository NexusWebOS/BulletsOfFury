#!/usr/bin/env python3
"""Live browser QA for Gravity Mode v2 and the Stage 5/9 space armory."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "gravity_mode_v2_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


SETUP = """() => {
  beginStage(5); setState(GS.PLAY); player.reset(); player.invuln=999999;
  player.x=worldWidth()/2; player.y=VH-82; snapCamToPlayer();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  stagePlan=[]; waveIdx=999; subBossTriggered=true; subBossDone=true; bossWarned=true;
  gravityModeStart();
  return {stage:run.stage,spaceMode:run.spaceMode,spaceLevels:run.spaceLevels.slice()};
}"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    errors: list[str] = []
    console_errors: list[str] = []
    report = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
        page = browser.new_page(viewport={"width": 1040, "height": 1120}, device_scale_factor=1)
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
        page.wait_for_function("() => typeof beginStage==='function' && typeof spaceWeaponFire==='function'", timeout=60_000)
        page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=45_000)
        page.evaluate(SETUP)
        page.wait_for_function("() => SPACE_ATLAS_FRAMES && XART.rdy('ngm_space_atlas')", timeout=45_000)

        canvas = page.locator("#screen")
        for name, phase, tick, age in (
            ("01_rise_spin", "rise", 1.38, 1.38),
            ("02_shoot_out", "shoot", 0.19, 2.39),
            ("03_snap_in", "snap", 0.20, 2.74),
            ("04_fuse_shake", "fuse", 0.22, 3.10),
            ("05_white_fusion", "whiteout", 0.20, 3.56),
            ("06_reveal", "reveal", 0.48, 4.04),
            ("07_active_fury", "active", 0.0, 5.0),
        ):
            page.evaluate("([p,t,a])=>{gravityMode.phase=p;gravityMode.t=t;gravityMode.age=a;}", [phase, tick, age])
            page.wait_for_timeout(55)
            canvas.screenshot(path=str(OUT / f"{name}.png"))

        # One visual proof that all nine pilot palettes are real cached sprites, including Cole's
        # black craft and the matching recoloured thrusters.
        page.evaluate("""() => {
          const old=document.getElementById('gravity-palette-proof');if(old)old.remove();
          const c=document.createElement('canvas');c.id='gravity-palette-proof';c.width=720;c.height=700;
          c.style.cssText='position:fixed;left:0;top:0;z-index:999999;background:#080b13';document.body.appendChild(c);
          const g=c.getContext('2d'), pilots=['axel','cole','maverick','decker','yuri','freezer','juggernaut','lizzie','falva'];
          g.fillStyle='#f2b84b';g.font='bold 20px monospace';g.fillText('FURY - BLUE ACCENTS ONLY / STEEL UNCHANGED',24,30);
          pilots.forEach((p,i)=>{const col=i%3,row=(i/3)|0,x=120+col*240,y=135+row*200;
            const s=spaceAtlasCanvas('ship_base',p),t=spaceAtlasCanvas('thruster_2',p);
            if(t)g.drawImage(t,x-31,y+38,62,91);if(s)g.drawImage(s,x-55,y-60,110,119);
            g.fillStyle='#eef4ff';g.font='bold 15px monospace';g.textAlign='center';g.fillText(p.toUpperCase(),x,y-67);});
          g.textAlign='left';
        }""")
        page.locator("#gravity-palette-proof").screenshot(path=str(OUT / "05b_pilot_palette_sheet.png"))
        page.evaluate("()=>document.getElementById('gravity-palette-proof').remove()")

        palette_contract = page.evaluate("""() => {
          const pilots=['cole','maverick','decker','yuri','freezer','juggernaut','lizzie','falva'];
          const ax=spaceAtlasCanvas('ship_base','axel'),mask=spaceAtlasCanvas('ship_base_blue',null);
          const ag=ax.getContext('2d').getImageData(0,0,ax.width,ax.height).data;
          const md=mask.getContext('2d').getImageData(0,0,mask.width,mask.height).data;
          let neutralChanged=0,accentChanged=0,neutralSamples=0,accentSamples=0;
          for(const p of pilots){
            const c=spaceAtlasCanvas('ship_base',p),d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            for(let i=0;i<ag.length;i+=4){
              if(ag[i+3]<220)continue;
              const changed=ag[i]!==d[i]||ag[i+1]!==d[i+1]||ag[i+2]!==d[i+2];
              if(md[i+3]===0){neutralSamples++;if(changed)neutralChanged++;}
              else {accentSamples++;if(changed)accentChanged++;}
            }
          }
          return {neutralChanged,neutralSamples,accentChanged,accentSamples};
        }""")

        # Laser Cannon V: six twin pulses = 12 independent rounds, 2 ms pulse separation.
        laser = page.evaluate("""() => {
          gravityMode.phase='active';run.spaceWeapon=0;run.spaceLevels[0]=5;run.wlevel=5;pBullets.length=0;
          spaceLaserFire();
          return {name:spaceWeaponName(),icon:spaceWeaponIconKey(),count:pBullets.length,
            delays:[...new Set(pBullets.map(b=>b._launchDelay))],kinds:[...new Set(pBullets.map(b=>b.kind))]};
        }""")
        page.wait_for_timeout(65)
        canvas.screenshot(path=str(OUT / "06_laser_cannon_v.png"))

        # Shadow charge and released flight.
        page.evaluate("""() => {pBullets.length=0;run.spaceWeapon=1;run.spaceLevels[1]=4;run.wlevel=4;
          run._spaceShadowHeld=false;run._spaceShadowCharge=0;}""")
        page.keyboard.down("j")
        page.wait_for_timeout(460)
        canvas.screenshot(path=str(OUT / "07_shadow_orb_charge.png"))
        page.keyboard.up("j")
        page.wait_for_timeout(55)
        shadow = page.evaluate("""() => {const b=pBullets.find(x=>x.kind==='shadowOrb');return {
          name:spaceWeaponName(),icon:spaceWeaponIconKey(),kind:b&&b.kind,charge:b&&b.charge};}""")
        page.wait_for_timeout(160)
        canvas.screenshot(path=str(OUT / "08_shadow_orb_flight.png"))

        # Volley seed visibly separates, then each missile gets its own heading and weave phase.
        volley = page.evaluate("""() => {pBullets.length=0;run.spaceWeapon=2;run.spaceLevels[2]=5;run.wlevel=5;
          spaceVolleyFire();return {name:spaceWeaponName(),icon:spaceWeaponIconKey(),seed:pBullets[0].kind};}""")
        page.wait_for_timeout(260)
        canvas.screenshot(path=str(OUT / "09_volley_missiles_split.png"))
        volley_state = page.evaluate("""() => ({count:pBullets.filter(b=>b.kind==='spaceVolley').length,
          phases:pBullets.filter(b=>b.kind==='spaceVolley').map(b=>b._phase),
          headings:pBullets.filter(b=>b.kind==='spaceVolley').map(b=>b.ang)})""")

        # Ground loadout is restored on Stage 6; no normal weapon survives inside Stage 5.
        isolation = page.evaluate("""() => {
          run.spaceMode=false;run._groundLoadout=null;run.weapon=4;run.wlevel=3;
          run.wlevels=[0,0,0,0,3,0];run.wvars=[null,null,null,null,'flamethrower',null];run.missileLevel=4;
          beginStage(5);const locked={space:run.spaceMode,weapon:run.weapon,missiles:run.missileLevel,name:spaceWeaponName()};
          beginStage(6);const restored={space:run.spaceMode,weapon:run.weapon,wlevel:run.wlevel,
            levels:run.wlevels.slice(),variant:run.wvars[4],missiles:run.missileLevel};
          return {locked,restored};
        }""")

        report = {
            "laser": laser,
            "shadow": shadow,
            "volley": {**volley, **volley_state},
            "loadoutIsolation": isolation,
            "paletteContract": palette_contract,
            "pageErrors": errors,
            "consoleErrors": console_errors,
        }
        browser.close()
    server.shutdown()
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(2)
    assert laser["count"] == 12 and laser["kinds"] == ["spaceLaser"]
    assert laser["delays"] == [0, 0.002, 0.004, 0.006, 0.008, 0.01]
    assert shadow["kind"] == "shadowOrb"
    assert volley_state["count"] == 3 and len(set(volley_state["phases"])) == 3
    assert palette_contract["neutralChanged"] == 0 and palette_contract["accentChanged"] > 0
    assert isolation["locked"]["space"] and isolation["locked"]["missiles"] == 0
    assert not isolation["restored"]["space"] and isolation["restored"]["weapon"] == 4


if __name__ == "__main__":
    main()
