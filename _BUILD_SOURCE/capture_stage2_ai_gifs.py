#!/usr/bin/env python3
"""Capture real Stage-2 volcanic AI and boss behavior from the live game canvas."""

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
OUT = ROOT / "docs" / "proofs" / "stage2_ai_live"
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
  if(window.__s2ProofTimer){ clearInterval(window.__s2ProofTimer); window.__s2ProofTimer=0; }
  if(window.__s2ProofTimeouts){ for(const id of window.__s2ProofTimeouts) clearTimeout(id); }
  window.__s2ProofTimeouts=[];
  beginStage(2); player.reset(); player.invuln=999999; player.x=240; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0;
  mapScroll=levelScrollRange();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  const started=performance.now();
  window.__s2ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;
    player.x=240+Math.sin(t*1.24)*138;
    player.y=438+Math.sin(t*0.71)*10;
    player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 150, duration: int = 4_400) -> dict:
    prep = "e._fcd=0;"
    if kind == "skim":
        prep += "e._dir=1;e._ty=190;"
    elif kind == "lance":
        prep += "e._vt=.2;"
    return {
        "name": f"Stage2_{kind}_Enemy_AI",
        "duration": duration,
        "setup": f"""() => {{
          const e=spawnEnemy('{kind}',{x},{y},{{}});
          if(e){{ e.y={y}; e.hp=e._maxhp||e.hp; {prep} }}
        }}""",
    }


CASES = [
    enemy_case("ash", duration=3_600),
    enemy_case("skim", x=72, y=180, duration=3_400),
    enemy_case("eye"),
    enemy_case("disc"),
    enemy_case("lance", duration=2_800),
    enemy_case("cruc"),
    enemy_case("carrier", duration=3_500),
    enemy_case("miner"),
    enemy_case("lavamaw"),
    enemy_case("crawl"),
    enemy_case("pod"),
    enemy_case("golem", duration=4_800),
    {
        "name": "Stage2_Magma_Ward_Miniboss_AI",
        "duration": 10_000,
        "setup": r"""() => {
          spawnSubBoss('magmaward');
          subBoss.enter=false; subBoss.x=240; subBoss.y=116; subBoss.ty=116;
          subBoss.fireCd=0.08; subBoss.phase=0; subBoss._phase=0;
          window.__s2ProofTimeouts.push(setTimeout(()=>{
            if(subBoss&&!subBoss.dead){ subBoss.hp=subBoss.maxhp*0.38; subBoss.fireCd=0.05; }
          },4300));
        }""",
    },
    {
        "name": "Stage2_Inferno_Reaver_Boss_AI",
        "duration": 13_000,
        "setup": r"""() => {
          spawnBoss('infernoreaver');
          boss.enter=false; boss.x=240; boss.y=116; boss.ty=116; boss.fireCd=0.05;
          const thresholds=[[2400,0.74],[4700,0.54],[7000,0.34],[9300,0.14]];
          for(const [delay,ratio] of thresholds){
            window.__s2ProofTimeouts.push(setTimeout(()=>{
              if(boss&&!boss.dead){ boss.hp=boss.maxhp*ratio; boss.fireCd=0.04; }
            },delay));
          }
        }""",
    },
]


def start_capture(page: Page) -> dict:
    return page.evaluate(
        """() => {
          const c=document.getElementById('screen');
          const stream=c.captureStream(24);
          const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
            .find(t=>MediaRecorder.isTypeSupported(t)) || '';
          const chunks=[]; const rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
          rec.ondataavailable=e=>{if(e.data&&e.data.size) chunks.push(e.data);};
          window.__s2Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
            rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'})); rec.stop();
          })};
          rec.start(250); return {w:c.width,h:c.height,mime};
        }"""
    )


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(
            """async () => {
              const blob=await window.__s2Capture.stop();
              const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
              a.download='stage2-ai.webm'; document.body.appendChild(a); a.click(); a.remove();
            }"""
        )
    info.value.save_as(webm)


def make_gif(webm: Path, gif: Path) -> None:
    vf = (
        "fps=10,scale=320:-1:flags=lanczos,"
        "split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle"
    )
    subprocess.run(
        [FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi", vf, "-loop", "0", str(gif)],
        check=True,
    )


def make_contact_sheet(webm: Path, contact: Path) -> None:
    subprocess.run(
        [
            FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
            "-vf", "fps=1,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black",
            "-frames:v", "1", str(contact),
        ],
        check=True,
    )


def main() -> None:
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
            page.wait_for_function(
                "() => typeof beginStage==='function' && typeof volcTick==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.evaluate(
                """() => {
                  const units=['ash','skim','eye','disc','lance','cruc','carrier','miner','maw','crawl','pod','golem'];
                  const keys=['nst2_master','nsb_magmaward_intact','nsb_inferno_reaver','bfx_magma_m_0'];
                  for(const u of units){ keys.push('nvl_'+u+'_0'); for(let f=0;f<8;f++)keys.push('s2atk_'+u+'_'+f); }
                  keys.forEach(k=>XART._touch(k));
                }"""
            )
            page.wait_for_function(
                "() => XART.rdy('nvl_ash_0') && XART.rdy('s2atk_golem_7') && XART.rdy('bfx_magma_m_0') && "
                "XART.rdy('nsb_magmaward_intact') && XART.rdy('nsb_inferno_reaver')",
                timeout=60_000,
            )

            selected = set(sys.argv[1:])
            for case in CASES:
                if selected and case["name"] not in selected:
                    continue
                page.evaluate(COMMON_SETUP)
                page.evaluate(case["setup"])
                page.wait_for_timeout(450)
                capture = start_capture(page)
                page.wait_for_timeout(case["duration"])
                png = OUT / f"{case['name']}.png"
                page.locator("#screen").screenshot(path=str(png))
                webm = OUT / f"{case['name']}.webm"
                gif = OUT / f"{case['name']}.gif"
                contact = OUT / f"{case['name']}_contact.png"
                stop_capture(page, webm)
                make_gif(webm, gif)
                make_contact_sheet(webm, contact)
                print(
                    f"{case['name']}: {capture['w']}x{capture['h']} {capture['mime']} "
                    f"gif={gif.stat().st_size} png={png.stat().st_size}"
                )
            page.evaluate("() => { if(window.__s2ProofTimer) clearInterval(window.__s2ProofTimer); }")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))


if __name__ == "__main__":
    main()
