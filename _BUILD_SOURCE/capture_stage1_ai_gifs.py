#!/usr/bin/env python3
"""Capture real Stage-1 AI behavior from the live Bullets of Fury canvas."""

from __future__ import annotations

import functools
import http.server
import subprocess
import threading
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage1_ai_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


COMMON_SETUP = r"""() => {
  if(window.__s1ProofTimer){ clearInterval(window.__s1ProofTimer); window.__s1ProofTimer=0; }
  if(window.__s1ProofTimeouts){ for(const id of window.__s1ProofTimeouts) clearTimeout(id); }
  window.__s1ProofTimeouts=[];
  beginStage(1); player.reset(); player.invuln=999999; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0;
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  const started=performance.now();
  window.__s1ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;
    player.x=240+Math.sin(t*1.42)*142;
    player.y=438+Math.sin(t*0.84)*12;
    player.invuln=999999;
  },16);
}"""


CASES = [
    {
        "name": "Stage1_Air_Naval_Enemy_AI",
        "duration": 7_500,
        "setup": r"""() => {
          spawnEnemy('s1jetdelta',105,-54,{});
          spawnEnemy('s1jetdelta_b',375,-92,{});
          spawnEnemy('s1jetbomber',235,-138,{});
          spawnEnemy('s1boatpatrol',145,-76,{});
          spawnEnemy('s1boatgun',335,-122,{});
          spawnEnemy('s1rivermine',238,205,{});
          spawnEnemy('s1fuelbarrel',78,275,{});
          window.__s1ProofTimeouts.push(setTimeout(()=>{
            spawnEnemy('s1jetdelta',90,-64,{});
            spawnEnemy('s1jetbomber_b',390,-110,{});
          },3600));
        }""",
    },
    {
        "name": "Stage1_Armored_Enemy_AI",
        "duration": 7_500,
        "setup": r"""() => {
          mapScroll=1250; _prevMapScroll=mapScroll;
          const rows=[
            ['s1tanklight',110,72],['s1tankheavy',225,46],
            ['s1tankapc',345,96],['s1truckmissile',420,32]
          ];
          for(const r of rows){
            const e=spawnEnemy(r[0],r[1],r[2],{});
            e._lvlY=levelSrcY()+r[2]; e._dir8=0; e._gear=1;
            e._phase='drive'; e._phT=1.4; e._shotCd=0; e._burstCd=0.25;
          }
        }""",
    },
    {
        "name": "Stage1_Jungle_Cruiser_Miniboss_AI",
        "duration": 9_500,
        "setup": r"""() => {
          mapScroll=1250; _prevMapScroll=mapScroll;
          spawnSubBoss('junglecruiser');
          subBoss.enter=false; subBoss.x=240; subBoss.y=116; subBoss.ty=116;
          subBoss.fireCd=0.12; subBoss._sbm='hold'; subBoss._sbmT=3.8; subBoss._sbmAge=0;
          window.__s1ProofTimeouts.push(setTimeout(()=>{
            if(subBoss&&!subBoss.dead){ subBoss.hp=subBoss.maxhp*0.38; subBoss.fireCd=0.05; }
          },3900));
        }""",
    },
    {
        "name": "Stage1_OverlordX_Boss_AI",
        "duration": 11_500,
        "setup": r"""() => {
          mapScroll=1250; _prevMapScroll=mapScroll;
          spawnBoss('damkeeper'); boss.enter=false; boss.x=240; boss.y=112; boss.ty=112;
          boss.fireCd=0.08; boss._ovChargeCd=6.4;
          window.__s1ProofTimeouts.push(setTimeout(()=>{
            if(boss&&!boss.dead){ boss.hp=boss.maxhp*0.48; boss._ovChargeCd=0.22; }
          },3300));
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
          window.__s1Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
            rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'})); rec.stop();
          })};
          rec.start(250); return {w:c.width,h:c.height,mime};
        }"""
    )


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(
            """async () => {
              const blob=await window.__s1Capture.stop();
              const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
              a.download='stage1-ai.webm'; document.body.appendChild(a); a.click(); a.remove();
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
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(webm), "-lavfi", vf, "-loop", "0", str(gif)],
        check=True,
    )


def make_contact_sheet(webm: Path, contact: Path) -> None:
    """Eight one-second samples make the animation review reproducible in a still diff."""
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-y", "-i", str(webm),
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
                "() => typeof beginStage==='function' && typeof updateOverlordX==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.evaluate(
                """() => ['nca_s1combatfx','ovbody_intact','ovbody_critical','ovrotor_00']
                  .forEach(k=>XART._touch(k))"""
            )
            page.wait_for_function(
                "() => XART.rdy('s1fx_green_impact_0') && XART.rdy('ovbody_intact') && XART.rdy('ovrotor_00')",
                timeout=60_000,
            )

            for case in CASES:
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
            page.evaluate("() => { if(window.__s1ProofTimer) clearInterval(window.__s1ProofTimer); }")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))


if __name__ == "__main__":
    main()
