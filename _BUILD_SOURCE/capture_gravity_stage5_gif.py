#!/usr/bin/env python3
"""Capture the real Stage 5 Fury-kit cinematic from the game canvas."""

from __future__ import annotations

import functools
import http.server
import subprocess
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "gravity_mode_stage5_stage9_live"
WEBM = OUT / "Fury_Spaceship_Transformation_Stage5.webm"
GIF = OUT / "Fury_Spaceship_Transformation_Stage5.gif"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function("() => typeof beginStage==='function' && typeof gravityModeStart==='function'", timeout=60_000)
            page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=45_000)
            page.evaluate("""() => {
              ['ngm_space_atlas','bg_stage05_loop','nl6sky_stage06_sky_scroll_640x960']
                .forEach(k=>XART._touch(k));
            }""")
            page.wait_for_function(
                "() => XART.rdy('ngm_space_atlas') && XART.rdy('bg_stage05_loop') && XART.rdy('nl6sky_stage06_sky_scroll_640x960')",
                timeout=60_000,
            )

            # MediaRecorder consumes the actual canvas stream, preserving every live animated frame.
            capture = page.evaluate("""() => {
              const c=document.getElementById('screen');
              const stream=c.captureStream(24);
              const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
                .find(t=>MediaRecorder.isTypeSupported(t)) || '';
              const chunks=[];const rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
              rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
              window.__gravityCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
                rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();
              })};
              rec.start(250);
              return {w:c.width,h:c.height,mime};
            }""")

            page.evaluate("""() => {
              beginStage(5);player.reset();player.invuln=999999;snapCamToPlayer();
              setState(GS.LAUNCH);gravityModeReset();drawLaunch._phase=undefined;
            }""")
            page.wait_for_function(
                "() => gravityMode && gravityMode.phase==='active' && drawLaunch._phase==='cd'",
                timeout=35_000,
            )
            page.wait_for_timeout(900)

            with page.expect_download(timeout=30_000) as info:
                page.evaluate("""async () => {
                  const blob=await window.__gravityCapture.stop();
                  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
                  a.download='Fury_Spaceship_Transformation_Stage5.webm';
                  document.body.appendChild(a);a.click();a.remove();
                }""")
            info.value.save_as(WEBM)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))

    # Detailed star fields are expensive in GIF.  360x540 at 12fps keeps the animation readable
    # while remaining small enough to render directly in the Codex conversation.
    vf = (
        "fps=12,scale=360:-1:flags=lanczos,"
        "split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(WEBM), "-lavfi", vf, "-loop", "0", str(GIF)],
        check=True,
    )
    print(f"capture={capture['w']}x{capture['h']} {capture['mime']}")
    print(f"webm={WEBM} ({WEBM.stat().st_size} bytes)")
    print(f"gif={GIF} ({GIF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
