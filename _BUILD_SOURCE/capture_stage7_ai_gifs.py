#!/usr/bin/env python3
"""Capture live Stage-7 toxic-fleet, miniboss and Sludge Emperor gameplay GIFs."""

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
OUT = ROOT / "docs" / "proofs" / "stage7_ai_live"
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
  if(window.__s7ProofTimer){clearInterval(window.__s7ProofTimer);window.__s7ProofTimer=0;}
  if(window.__s7ProofTimeouts)for(const id of window.__s7ProofTimeouts)clearTimeout(id);
  window.__s7ProofTimeouts=[];
  beginStage(7);player.reset();player.invuln=999999;player.x=240;player.y=438;
  snapCamToPlayer();setState(GS.PLAY);stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
  enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;
  explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
  boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
  const started=performance.now();window.__s7ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;player.x=240+Math.sin(t*1.03)*132;
    player.y=438+Math.sin(t*.57)*10;player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 132, duration: int = 4400) -> dict:
    prep = "e._fcd=0;e._stagger=0;"
    if kind in {"s7sampler", "s7skimmer"}:
        prep += "e._side=1;e._dir=1;"
    return {
        "name": f"Stage7_{kind}_Enemy_AI", "duration": duration,
        "setup": f"""() => {{const e=spawnEnemy('{kind}',{x},{y},{{}});if(e){{e.x={x};e.y={y};e.hp=e._maxhp||e.hp;{prep}}}}}""",
    }


CASES = [
    enemy_case("s7lamprey"), enemy_case("s7barge", duration=5200),
    enemy_case("s7pipe"), enemy_case("s7walker", duration=5000),
    enemy_case("s7sampler", x=90), enemy_case("s7serpent", duration=5000),
    enemy_case("s7mine"), enemy_case("s7canister"), enemy_case("s7tank"),
    enemy_case("s7skimmer", x=80), enemy_case("s7valve"),
    {
        "name": "Stage7_Dual_Scoop_Dredger_Miniboss_AI", "duration": 9600,
        "setup": r"""() => {
          spawnSubBoss('dualscoopdredger');subBoss.enter=false;subBoss.x=240;subBoss.y=116;subBoss.ty=116;subBoss.fireCd=.04;
          window.__s7ProofTimeouts.push(setTimeout(()=>{if(subBoss&&!subBoss.dead){subBoss.hp=subBoss.maxhp*.2;subBoss.fireCd=.04;}},4300));
        }""",
    },
    {
        "name": "Stage7_Sludge_Emperor_Four_Phase_Boss", "duration": 15000,
        "setup": r"""() => {
          spawnBoss('sludgeemperor');boss.enter=false;boss.x=VW/2;boss.y=118;boss.ty=118;boss.fireCd=.04;
          for(const row of [[3600,.68],[7200,.43],[10800,.18]])window.__s7ProofTimeouts.push(setTimeout(()=>{
            if(boss&&!boss.dead){boss.hp=boss.maxhp*row[1];boss.fireCd=.04;boss._sba=null;}
          },row[0]));
        }""",
    },
]


def start_capture(page: Page) -> dict:
    return page.evaluate("""() => {const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__s7Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};
      rec.start(250);return {w:c.width,h:c.height,mime};}""")


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30000) as info:
        page.evaluate("""async()=>{const blob=await window.__s7Capture.stop(),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='stage7-ai.webm';document.body.appendChild(a);a.click();a.remove();}""")
    info.value.save_as(webm)


def make_gif(webm: Path, gif: Path) -> None:
    vf = ("fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
          "[s0]palettegen=max_colors=112:stats_mode=diff[p];"
          "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi", vf, "-loop", "0", str(gif)], check=True)


def make_contact(webm: Path, contact: Path) -> None:
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
                    "fps=2,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black", "-frames:v", "1", str(contact)], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True);server=serve();errors=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(args=["--disable-gpu","--no-sandbox","--mute-audio"])
            page=browser.new_page(viewport={"width":760,"height":820},device_scale_factor=1)
            page.on("pageerror",lambda err:errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html",wait_until="load",timeout=60000)
            page.wait_for_function("() => typeof beginStage==='function'&&typeof s7ToxicTick==='function'&&(window.__bofFrames|0)>4",timeout=60000)
            page.evaluate("""() => {const units=['armored_lamprey','armored_sludge_barge','dual_scoop_dredger','pipe_crawler','piston_pump_walker','sampling_drone','sewer_serpent','sludge_mine','toxic_canister','toxic_mini_tank','toxic_skimmer','valve_turret'];for(const u of units)for(let f=0;f<8;f++)XART._touch('s7atk_'+u+'_'+f);for(let f=0;f<12;f++)XART._touch('s7spore_'+f);['nsb_sludgeemperor_intact','nsb_sludgeemperor_damaged','nsb_sludgeemperor_critical'].forEach(k=>XART._touch(k));}""")
            page.wait_for_function("() => XART.rdy('s7atk_armored_lamprey_0')&&XART.rdy('s7atk_valve_turret_7')&&XART.rdy('s7atk_dual_scoop_dredger_7')&&XART.rdy('s7spore_11')&&XART.rdy('nsb_sludgeemperor_intact')",timeout=60000)
            selected=set(sys.argv[1:])
            for case in CASES:
                if selected and case['name'] not in selected: continue
                page.evaluate(COMMON_SETUP);page.evaluate(case['setup']);page.wait_for_timeout(350)
                capture=start_capture(page);page.wait_for_timeout(case['duration'])
                page.locator('#screen').screenshot(path=str(OUT/f"{case['name']}.png"))
                webm=OUT/f"{case['name']}.webm";gif=OUT/f"{case['name']}.gif";contact=OUT/f"{case['name']}_contact.png"
                stop_capture(page,webm);make_gif(webm,gif);make_contact(webm,contact)
                print(f"{case['name']}: {capture['w']}x{capture['h']} gif={gif.stat().st_size}")
            page.evaluate("() => {if(window.__s7ProofTimer)clearInterval(window.__s7ProofTimer);}");browser.close()
    finally:
        server.shutdown();server.server_close()
    if errors:raise RuntimeError('Browser errors: '+' | '.join(errors))


if __name__ == '__main__':
    main()
