#!/usr/bin/env python3
"""Capture the real Stage-3 native ice-fleet controllers from the live game canvas."""

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
OUT = ROOT / "docs" / "proofs" / "stage3_ai_live"
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
  if(window.__s3ProofTimer){ clearInterval(window.__s3ProofTimer); window.__s3ProofTimer=0; }
  if(window.__s3ProofTimeouts){ for(const id of window.__s3ProofTimeouts) clearTimeout(id); }
  window.__s3ProofTimeouts=[];
  beginStage(3); player.reset(); player.invuln=999999; player.x=240; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0;
  mapScroll=levelScrollRange();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  thaw=null; _frzNarr=null;
  boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  const started=performance.now();
  window.__s3ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;
    player.x=240+Math.sin(t*1.17)*135;
    player.y=438+Math.sin(t*.63)*9;
    player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 145, duration: int = 4_200) -> dict:
    prep = "e._fcd=0;"
    if kind == "s3snowmobile":
        prep += "e._dir=1;e._side=1;"
    return {
        "name": f"Stage3_{kind}_Enemy_AI",
        "duration": duration,
        "setup": f"""() => {{
          const e=spawnEnemy('{kind}',{x},{y},{{}});
          if(e){{ e.x={x}; e.y={y}; e.hp=e._maxhp||e.hp; {prep} }}
        }}""",
    }


CASES = [
    enemy_case("s3mine", duration=3_700),
    enemy_case("s3interceptor", y=105, duration=4_100),
    enemy_case("s3sled", duration=3_700),
    enemy_case("s3snowmobile", x=62, y=155, duration=3_500),
    enemy_case("s3crawler", duration=4_000),
    enemy_case("s3tank", duration=4_300),
    enemy_case("s3barge", duration=4_500),
    enemy_case("s3artillery", duration=4_600),
    {
        "name": "Stage3_Frostbite_Arsenal_Mini_AI",
        "duration": 8_500,
        "setup": r"""() => {
          const e=spawnArsenalMini('frostbite');
          if(e){ e.y=112; e.vy=0; e._dr.entry=0; e._dr.cd=.08; }
        }""",
    },
    {
        "name": "Stage3_Rime_Wall_Miniboss_AI",
        "duration": 9_000,
        "setup": r"""() => {
          spawnSubBoss('rimewall');
          subBoss.enter=false; subBoss.x=240; subBoss.y=116; subBoss.ty=116;
          subBoss.fireCd=.06; subBoss._sbStep=0; subBoss._sbPhase=0;
          window.__s3ProofTimeouts.push(setTimeout(()=>{
            if(subBoss&&!subBoss.dead){ subBoss.hp=subBoss.maxhp*.34; subBoss.fireCd=.04; }
          },4200));
        }""",
    },
    {
        "name": "Stage3_Cryo_Spear_Boss_AI",
        "duration": 11_500,
        "setup": r"""() => {
          spawnBoss('cryospear');
          boss.enter=false; boss.x=240; boss.y=116; boss.ty=116; boss.fireCd=.05;
          const thresholds=[[2500,.72],[5000,.48],[7600,.22]];
          for(const [delay,ratio] of thresholds){
            window.__s3ProofTimeouts.push(setTimeout(()=>{
              if(boss&&!boss.dead){ boss.hp=boss.maxhp*ratio; boss.fireCd=.04; }
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
          window.__s3Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
            rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'})); rec.stop();
          })};
          rec.start(250); return {w:c.width,h:c.height,mime};
        }"""
    )


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(
            """async () => {
              const blob=await window.__s3Capture.stop();
              const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
              a.download='stage3-ai.webm'; document.body.appendChild(a); a.click(); a.remove();
            }"""
        )
    info.value.save_as(webm)


def make_gif(webm: Path, gif: Path) -> None:
    vf = (
        "fps=10,scale=320:-1:flags=lanczos,"
        "split[s0][s1];[s0]palettegen=max_colors=112:stats_mode=diff[p];"
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
            "-vf", "fps=2,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black",
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
                "() => typeof beginStage==='function' && typeof s3IceTick==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.evaluate(
                """() => {
                  const units=['mine','interceptor','sled','snowmobile','crawler','tank','barge','artillery'];
                  const keys=['nst3_master','ndr_frostbite_idle_0','nsb_rimewall_intact','nsb_cryo_spear'];
                  for(const u of units){
                    for(let f=0;f<8;f++){
                      keys.push('s3atk_'+u+'_'+f);
                      keys.push('s3dmg_'+u+'_damaged_'+f);
                      keys.push('s3dmg_'+u+'_critical_'+f);
                    }
                  }
                  keys.forEach(k=>XART._touch(k));
                }"""
            )
            page.wait_for_function(
                "() => XART.rdy('nst3_master') && XART.rdy('s3atk_mine_0') && "
                "XART.rdy('s3atk_artillery_7') && XART.rdy('s3dmg_tank_critical_7') && "
                "XART.rdy('ndr_frostbite_idle_0') && XART.rdy('nsb_rimewall_intact') && XART.rdy('nsb_cryo_spear')",
                timeout=60_000,
            )

            selected = set(sys.argv[1:])
            for case in CASES:
                if selected and case["name"] not in selected:
                    continue
                page.evaluate(COMMON_SETUP)
                page.evaluate(case["setup"])
                page.wait_for_timeout(400)
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
            page.evaluate("() => { if(window.__s3ProofTimer) clearInterval(window.__s3ProofTimer); }")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))


if __name__ == "__main__":
    main()
