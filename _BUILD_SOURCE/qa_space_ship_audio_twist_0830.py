#!/usr/bin/env python3
"""Focused live QA for the Stage 5/9 Gravity ship audio, turn poses and alpha edge."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "space_ship_audio_twist_0830"
ATLAS_JSON = ROOT / "assets" / "game" / "atlas" / "bof_gravity_mode_space_weapons.json"
ATLAS_PNG = ROOT / "assets" / "game" / "atlas" / "bof_gravity_mode_space_weapons.png"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def edge_purple_count(image: Image.Image) -> int:
    a = np.asarray(image.convert("RGBA"))
    opaque = a[..., 3] > 0
    near_clear = ~opaque
    for _ in range(8):
        expanded = near_clear.copy()
        expanded[1:] |= near_clear[:-1]
        expanded[:-1] |= near_clear[1:]
        expanded[:, 1:] |= near_clear[:, :-1]
        expanded[:, :-1] |= near_clear[:, 1:]
        near_clear = expanded
    rgb = a[..., :3].astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    purple = (r > g + 10) & (b > g + 18) & (r > 35) & (b > 35)
    return int((opaque & near_clear & purple).sum())


def alpha_report() -> dict[str, int]:
    meta = json.loads(ATLAS_JSON.read_text(encoding="utf-8"))["frames"]
    atlas = Image.open(ATLAS_PNG).convert("RGBA")
    keys = ["ship_base"]
    keys += [f"ship_bank_{side}{step}" for side in ("l", "r") for step in range(1, 4)]
    keys += [f"ship_roll_{i:02d}" for i in range(17)]
    result = {}
    for key in keys:
        r = meta[key]
        cell = atlas.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
        result[key] = edge_purple_count(cell)
    return result


def make_contact(paths: list[Path], target: Path):
    shots = [Image.open(p).convert("RGB") for p in paths]
    width = sum(im.width for im in shots)
    height = max(im.height for im in shots) + 34
    out = Image.new("RGB", (width, height), "#080b12")
    draw = ImageDraw.Draw(out)
    labels = ("LEFT / HARD TURN", "LEVEL FLIGHT", "RIGHT / HARD TURN")
    x = 0
    for image, label in zip(shots, labels):
        out.paste(image, (x, 34))
        draw.text((x + 12, 11), label, fill="#f5f8ff")
        x += image.width
    out.save(target, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    page_errors: list[str] = []
    report: dict = {"edgePurple": alpha_report(), "stages": {}}
    screenshots: list[Path] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                args=["--disable-gpu", "--no-sandbox", "--autoplay-policy=no-user-gesture-required"]
            )
            page = browser.new_page(viewport={"width": 480, "height": 720})
            page.add_init_script("""(() => {
              window.__mediaPlayCalls=[];
              const original=HTMLMediaElement.prototype.play;
              HTMLMediaElement.prototype.play=function(){
                const row={src:this.src.split('/').pop(),volume:this.volume,loop:this.loop,
                  ready:this.readyState,status:'called',at:performance.now()};
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
                "() => typeof gravityModeDrawShip==='function' && typeof Snd!=='undefined' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.mouse.click(240, 360)
            page.wait_for_timeout(500)

            page.evaluate("""() => {
              window.__spacePoseKeys=[];
              window.__spaceAtlasDrawOriginal=spaceAtlasDraw;
              spaceAtlasDraw=function(g,key,x,y,w,h,centred,pilot){
                if(/^ship_(base|bank_|roll_)/.test(key))window.__spacePoseKeys.push(key);
                return window.__spaceAtlasDrawOriginal(g,key,x,y,w,h,centred,pilot);
              };
            }""")

            for stage in (5, 9):
                page.evaluate(
                    """stage => {
                      beginStage(stage);setState(GS.PLAY);player.reset();player.dead=false;player.invuln=99999;
                      player.x=240;player.y=500;snapCamToPlayer();
                      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
                      enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
                      boss=null;bossActive=false;subBoss=null;subBossActive=false;
                      spaceModeStage(stage);run.gravityShipReady=true;gravityMode={phase:'active',t:0,age:0,retained:stage===9};
                      run.spaceLevels=[5,5,5];run.spaceWeapon=0;
                      Audio.setVol('master',1);Audio.setVol('sfx',1);
                      Snd._last={};Snd.prepare(['spaceLaserCannon','spaceShadowCharge','spaceShadowRelease','spaceVolleyLaunch']);
                    }""",
                    stage,
                )
                page.wait_for_function(
                    "() => ['spaceLaserCannon','spaceShadowRelease','spaceVolleyLaunch'].every(n=>Snd.pools[n].list.some(a=>a.readyState>=3))",
                    timeout=20_000,
                )
                page.evaluate("window.__mediaPlayCalls.length=0")
                page.evaluate("run.spaceWeapon=0;spaceLaserFire()")
                page.wait_for_timeout(180)
                page.evaluate("run.spaceWeapon=1;spaceShadowTick(.55,true);spaceShadowTick(.02,false)")
                page.wait_for_timeout(180)
                page.evaluate("run.spaceWeapon=2;spaceVolleyFire()")
                page.wait_for_timeout(320)
                audio = page.evaluate("""() => ({
                  calls:window.__mediaPlayCalls.filter(c=>[
                    'reviewed_laser_cannon.wav','reviewed_shadow_orb_launch.wav','nsp_rocket_launch.mp3'
                  ].includes(c.src)),
                  context:Snd._ctx?Snd._ctx.state:'none',
                  ready:['spaceLaserCannon','spaceShadowRelease','spaceVolleyLaunch'].map(n=>({
                    name:n,states:Snd.pools[n].list.map(a=>a.readyState),times:Snd.pools[n].list.map(a=>a.currentTime)
                  }))
                })""")
                report["stages"][str(stage)] = {"audio": audio}

                if stage == 5:
                    page.evaluate("""() => {
                      pBullets.length=0;eBullets.length=0;player.x=VW/2;player.y=VH*0.72;
                    }""")
                    for bank, name in ((-1, "left"), (0, "level"), (1, "right")):
                        page.evaluate("""b => {
                          for(const k of keybind.left.concat(keybind.right))Input.keys[k]=false;
                          if(b<0)for(const k of keybind.left)Input.keys[k]=true;
                          if(b>0)for(const k of keybind.right)Input.keys[k]=true;
                          player._bank=b;window.__spacePoseKeys.length=0;
                        }""", bank)
                        page.wait_for_timeout(180)
                        shot = OUT / f"stage5_ship_{name}.png"
                        page.locator("#screen").screenshot(path=str(shot))
                        screenshots.append(shot)
                        report["stages"]["5"].setdefault("poses", {})[name] = page.evaluate(
                            "window.__spacePoseKeys.slice(-3)"
                        )
                    page.evaluate("""() => {
                      for(const k of keybind.left.concat(keybind.right))Input.keys[k]=false;
                    }""")
            report["pageErrors"] = page_errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    make_contact(screenshots, OUT / "stage5_gravity_ship_turn_contact.png")
    (OUT / "qa_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    assert max(report["edgePurple"].values()) == 0, report["edgePurple"]
    poses = report["stages"]["5"]["poses"]
    assert any("ship_bank_l3" == k for k in poses["left"]), poses
    assert any("ship_base" == k for k in poses["level"]), poses
    assert any("ship_bank_r3" == k for k in poses["right"]), poses
    expected = {"reviewed_laser_cannon.wav", "reviewed_shadow_orb_launch.wav", "nsp_rocket_launch.mp3"}
    for stage in ("5", "9"):
        audio = report["stages"][stage]["audio"]
        played = {c["src"] for c in audio["calls"] if c["status"] == "playing"}
        assert expected.issubset(played), (stage, audio)
        assert audio["context"] in ("running", "none"), (stage, audio["context"])
    assert not page_errors, page_errors
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
