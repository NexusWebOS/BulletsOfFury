#!/usr/bin/env python3
"""Live visual QA for Stage 6's continuous sky, weather, and independent scroll clock."""

from __future__ import annotations

import functools
import http.server
import json
import math
import threading
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage6_weather_0830"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def rgb_mean(path: Path) -> list[float]:
    image = Image.open(path).convert("RGB")
    # Ignore the HUD band and outer letterbox; measure the playfield atmosphere.
    crop = image.crop((image.width // 6, 20, image.width * 5 // 6, image.height * 3 // 4))
    sample = crop.resize((80, 80), Image.Resampling.BOX)
    pixels = list(sample.getdata())
    return [round(sum(p[c] for p in pixels) / len(pixels), 2) for c in range(3)]


def image_delta(a: Path, b: Path) -> float:
    ia = Image.open(a).convert("RGB").resize((160, 160), Image.Resampling.BOX)
    ib = Image.open(b).convert("RGB").resize((160, 160), Image.Resampling.BOX)
    pa, pb = list(ia.getdata()), list(ib.getdata())
    return round(sum(abs(x - y) for p, q in zip(pa, pb) for x, y in zip(p, q)) / (len(pa) * 3), 3)


def make_contact(paths: list[tuple[str, Path]]) -> Path:
    thumbs = []
    for label, path in paths:
        im = Image.open(path).convert("RGB")
        im.thumbnail((300, 320), Image.Resampling.LANCZOS)
        card = Image.new("RGB", (320, 370), "#050913")
        card.paste(im, ((320 - im.width) // 2, 38))
        ImageDraw.Draw(card).text((12, 10), label, fill="white")
        thumbs.append(card)
    contact = Image.new("RGB", (320 * len(thumbs), 370), "black")
    for i, im in enumerate(thumbs):
        contact.paste(im, (i * 320, 0))
    path = OUT / "stage6_weather_phase_contact.png"
    contact.save(path, optimize=True)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    errors: list[str] = []
    report: dict = {"phases": {}, "pageErrors": errors}
    captures: list[tuple[str, Path]] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60000)
            page.wait_for_function("() => typeof beginStage==='function' && (window.__bofFrames|0)>4", timeout=60000)
            page.evaluate("""() => {
              XART._touch('stage6_blue_master');
              for(let i=0;i<8;i++)XART._touch('bg6_bolt_'+i);
              for(let i=0;i<4;i++)XART._touch('bg6_flash_'+i);
            }""")
            page.wait_for_function(
                "() => XART.rdy('stage6_blue_master') && XART.rdy('bg6_bolt_7') && XART.rdy('bg6_flash_3')",
                timeout=60000,
            )
            page.evaluate("""() => {
              beginStage(6); player.reset(); player.invuln=999999;
              snapCamToPlayer(); setState(GS.PLAY);
              stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0;
              enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
              boss=null; bossActive=false; bossDefeated=false;
              subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
            }""")
            page.wait_for_timeout(300)

            phases = [
                ("01_blue_night", 0.02, False),
                ("02_black_squall_rain", 0.28, False),
                ("03_lightning_strike", 0.30, True),
                ("04_purple_dusk", 0.56, False),
                ("05_fire_dawn", 0.76, False),
                ("06_sunlight", 0.98, False),
            ]
            for name, phase, bolt in phases:
                page.evaluate(
                    """([phase,bolt]) => {
                      stageTimer=curStage.length*phase;
                      _stage6SkyScroll=phase*1700;
                      if(!wfx)wfxReset();
                      wfx.bolt=bolt?{key:'nwf_ltF',x:worldWidth()*.52,y:10,sc:2,t:.055}:null;
                      wfx.boltCd=bolt?99:4;
                    }""",
                    [phase, bolt],
                )
                page.wait_for_timeout(90 if bolt else 180)
                path = OUT / f"{name}.png"
                page.locator("#screen").screenshot(path=str(path))
                mean = rgb_mean(path)
                report["phases"][name] = {"phase": phase, "meanRGB": mean, "storm": phase < 0.48 and phase > 0.08}
                captures.append((name.replace("_", " ").upper(), path))

            # Prove the rain field is moving, rather than a static overlay.
            page.evaluate("""() => {stageTimer=curStage.length*.30;if(!wfx)wfxReset();wfx.bolt=null;wfx.boltCd=99;}""")
            rain_a = OUT / "rain_motion_a.png"
            rain_b = OUT / "rain_motion_b.png"
            page.locator("#screen").screenshot(path=str(rain_a))
            page.wait_for_timeout(220)
            page.locator("#screen").screenshot(path=str(rain_b))
            report["rainMotionMeanDelta"] = image_delta(rain_a, rain_b)

            # Visual sky speed must be decisively stronger than the encounter/map clock.
            page.evaluate("""() => {stageTimer=curStage.length*.62;mapScroll=500;_stage6SkyScroll=500;}""")
            before = page.evaluate("() => ({map:mapScroll,sky:_stage6SkyScroll})")
            page.wait_for_timeout(1000)
            after = page.evaluate("() => ({map:mapScroll,sky:_stage6SkyScroll})")
            report["scroll"] = {
                "mapPxPerSec": round(after["map"] - before["map"], 2),
                "skyPxPerSec": round(after["sky"] - before["sky"], 2),
                "ratio": round((after["sky"] - before["sky"]) / max(1, after["map"] - before["map"]), 2),
            }
            report["contact"] = str(make_contact(captures))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    means = [row["meanRGB"] for row in report["phases"].values()]
    separations = [math.dist(means[i], means[i + 1]) for i in range(len(means) - 1)]
    report["adjacentMoodDistances"] = [round(v, 2) for v in separations]
    (OUT / "qa_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")

    assert not errors, errors
    assert report["scroll"]["skyPxPerSec"] >= 95, report["scroll"]
    assert report["scroll"]["ratio"] >= 2.2, report["scroll"]
    assert report["rainMotionMeanDelta"] >= 1.0, report["rainMotionMeanDelta"]
    assert min(separations) >= 3.0, report["adjacentMoodDistances"]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
