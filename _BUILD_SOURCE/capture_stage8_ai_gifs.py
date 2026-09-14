#!/usr/bin/env python3
"""Capture live Stage-8 Furious Death mega-enemy combat and roll/twist GIFs."""

from __future__ import annotations

import functools
import http.server
import subprocess
import sys
import threading
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage8_ai_live"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


COMMON_SETUP = r"""() => {
  if(window.__s8ProofTimer){clearInterval(window.__s8ProofTimer);window.__s8ProofTimer=0;}
  if(window.__s8ThreatTimer){clearInterval(window.__s8ThreatTimer);window.__s8ThreatTimer=0;}
  beginStage(8);player.reset();player.invuln=999999;player.x=240;player.y=442;
  snapCamToPlayer();setState(GS.PLAY);stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
  enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;
  explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
  boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
  const started=performance.now();window.__s8ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;player.x=240+Math.sin(t*1.18)*138;
    player.y=442+Math.sin(t*.67)*9;player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 128, duration: int = 5600) -> dict:
    return {
        "name": f"Stage8_{kind}_Mega_Enemy_AI",
        "duration": duration,
        "setup": f"""() => {{
          const e=spawnEnemy('{kind}',{x},{y},{{}});if(e){{e.x={x};e.y={y};e.hp=e._maxhp||e.hp;e._fcd=0;e._stagger=0;
          if('{kind}'==='s8bomber'){{e._dir=1;e.x=60;}}
          window.__s8ThreatTimer=setInterval(()=>{{if(e&&!e.dead&&!e._s8Roll){{pBullets.push({{x:e.x,y:e.y+145,vx:0,vy:-8,w:5,h:14,dmg:1,t:0,kind:'mg'}});}}}},1450);}}
        }}""",
    }


CASES = [
    enemy_case("s8leech"), enemy_case("s8interceptor"), enemy_case("s8manta"),
    enemy_case("s8hunter"), enemy_case("s8deathorb", duration=6500),
    enemy_case("s8parasite"), enemy_case("s8razor"), enemy_case("s8skull", duration=6200),
    enemy_case("s8carrier", duration=7200), enemy_case("s8symbiote"),
    enemy_case("s8tentacle", duration=6500), enemy_case("s8bomber", x=60, duration=4700),
    {
        "name": "Stage8_Furious_Death_Annihilation_Boss", "duration": 7200,
        "setup": r"""() => {
          spawnBoss('vileexistence');boss.enter=false;bossActive=true;boss.x=VW/2;boss.y=132;boss.ty=132;
          vileBuildForm(boss,3);boss._be=null;boss.enter=false;boss.fireCd=.04;boss.hp=boss.maxhp*.72;
          vileAnnihilationStart(boss);
        }""",
    },
]


def start_capture(page: Page) -> dict:
    return page.evaluate("""() => {const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__s8Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};
      rec.start(250);return {w:c.width,h:c.height,mime};}""")


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30000) as info:
        page.evaluate("""async()=>{const blob=await window.__s8Capture.stop(),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='stage8-ai.webm';document.body.appendChild(a);a.click();a.remove();}""")
    info.value.save_as(webm)


def make_gif(webm: Path, gif: Path) -> None:
    vf = ("fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
          "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
          "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi", vf,
                    "-loop", "0", str(gif)], check=True)


def make_contact(webm: Path, contact: Path) -> None:
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
                    "fps=2,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black",
                    "-frames:v", "1", str(contact)], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    server, errors = serve(), []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60000)
            page.wait_for_function("() => typeof beginStage==='function'&&typeof s8MegaTick==='function'&&(window.__bofFrames|0)>4", timeout=60000)
            page.evaluate("""() => {for(const k in S8MEGA){const a=S8MEGA[k].art;for(let f=0;f<8;f++){XART._touch('s8atk_'+a+'_'+f);XART._touch('s8roll_'+a+'_'+f);}}for(let f=0;f<16;f++)XART._touch('s8rift_'+f);}""")
            page.wait_for_function("() => XART.rdy('s8atk_armored_leech_0')&&XART.rdy('s8roll_void_bomber_7')&&XART.rdy('s8rift_15')", timeout=60000)
            selected = set(sys.argv[1:])
            for case in CASES:
                if selected and case["name"] not in selected:
                    continue
                page.evaluate(COMMON_SETUP)
                page.evaluate(case["setup"])
                page.wait_for_timeout(350)
                capture = start_capture(page)
                page.wait_for_timeout(case["duration"])
                page.locator("#screen").screenshot(path=str(OUT / f"{case['name']}.png"))
                webm = OUT / f"{case['name']}.webm"
                gif = OUT / f"{case['name']}.gif"
                contact = OUT / f"{case['name']}_contact.png"
                stop_capture(page, webm)
                make_gif(webm, gif)
                make_contact(webm, contact)
                print(f"{case['name']}: {capture['w']}x{capture['h']} gif={gif.stat().st_size}")
            page.evaluate("() => {if(window.__s8ProofTimer)clearInterval(window.__s8ProofTimer);if(window.__s8ThreatTimer)clearInterval(window.__s8ThreatTimer);}")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))


if __name__ == "__main__":
    main()
