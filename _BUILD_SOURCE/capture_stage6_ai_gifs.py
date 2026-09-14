#!/usr/bin/env python3
"""Capture the live Stage-6 Heavy Turbulence controllers and Doomsday mega boss."""

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
OUT = ROOT / "docs" / "proofs" / "stage6_ai_live"
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
  if(window.__s6ProofTimer){clearInterval(window.__s6ProofTimer);window.__s6ProofTimer=0;}
  if(window.__s6ProofTimeouts)for(const id of window.__s6ProofTimeouts)clearTimeout(id);
  window.__s6ProofTimeouts=[];
  beginStage(6);player.reset();player.invuln=999999;player.x=240;player.y=438;
  snapCamToPlayer();setState(GS.PLAY);stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
  enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;
  explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
  boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
  const started=performance.now();window.__s6ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;player.x=240+Math.sin(t*1.07)*132;
    player.y=438+Math.sin(t*.53)*10;player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 132, duration: int = 4400) -> dict:
    prep = "e._fcd=0;e._stagger=0;"
    if kind in {"s6cyclone", "s6bomber", "s6skimmer", "s6dart"}:
        prep += "e._side=1;e._dir=1;"
    return {
        "name": f"Stage6_{kind}_Enemy_AI",
        "duration": duration,
        "setup": f"""() => {{const e=spawnEnemy('{kind}',{x},{y},{{}});if(e){{e.x={x};e.y={y};e.hp=e._maxhp||e.hp;{prep}}}}}""",
    }


CASES = [
    enemy_case("s6lancer"), enemy_case("s6cyclone", duration=5000),
    enemy_case("s6bomber", x=90), enemy_case("s6mine"),
    enemy_case("s6skimmer", x=80), enemy_case("s6carrier", duration=5600),
    enemy_case("s6reactor", duration=5800), enemy_case("s6buoy"),
    enemy_case("s6dart", x=80), enemy_case("s6thunder"),
    enemy_case("s6turbine", duration=5000), enemy_case("s6probe", duration=5200),
    {
        "name": "Stage6_Blacksteel_Raptor_Miniboss_AI", "duration": 9000,
        "setup": r"""() => {
          spawnSubBoss('blacksteel');subBoss.enter=false;subBoss.x=240;subBoss.y=116;subBoss.ty=116;subBoss.fireCd=.04;
          window.__s6ProofTimeouts.push(setTimeout(()=>{if(subBoss&&!subBoss.dead){subBoss.hp=subBoss.maxhp*.2;subBoss.fireCd=.04;}},4300));
        }""",
    },
    {
        "name": "Stage6_Doomsday_Carrier_MkII_Mega_Boss", "duration": 14500,
        "setup": r"""() => {
          spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=VW/2;boss.y=172;boss.ty=172;boss.fireCd=.04;
          carrierInit(boss);carrierMegaInit(boss);boss._lc.cd=.35;
          for(const row of [[3500,.69],[7000,.44],[10400,.19]])window.__s6ProofTimeouts.push(setTimeout(()=>{
            if(boss&&!boss.dead){boss.hp=boss.maxhp*row[1];boss._cn=null;boss._lc.playing=false;boss._lc.cd=2.1;boss._mega.cd=.05;}
          },row[0]));
        }""",
    },
    {
        "name": "Stage6_Carrier_Bay_Giant_Warhead_Handoff", "duration": 6800,
        "setup": r"""() => {
          spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=VW/2;boss.y=172;boss.ty=172;boss.fireCd=99;
          carrierInit(boss);carrierMegaInit(boss);boss._mega.cd=999;boss._lc.cd=.04;
          let reflected=false;const rid=setInterval(()=>{const q=eBullets.find(x=>x._carrierWarhead&&!x._ref&&!x.dead);
            if(q&&!reflected&&q.y>340){reflected=true;pBullets.push({x:q.x,y:q.y,vx:0,vy:0,w:8,h:18,dmg:1,t:0,kind:'mg'});}},16);
          window.__s6ProofTimeouts.push(rid);
        }""",
    },
]


def start_capture(page: Page) -> dict:
    return page.evaluate("""() => {
      const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
      rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__s6Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};
      rec.start(250);return {w:c.width,h:c.height,mime};
    }""")


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30000) as info:
        page.evaluate("""async()=>{const blob=await window.__s6Capture.stop(),a=document.createElement('a');
          a.href=URL.createObjectURL(blob);a.download='stage6-ai.webm';document.body.appendChild(a);a.click();a.remove();}""")
    info.value.save_as(webm)


def make_gif(webm: Path, gif: Path) -> None:
    vf = ("fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
          "[s0]palettegen=max_colors=112:stats_mode=diff[p];"
          "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi", vf,
                    "-loop", "0", str(gif)], check=True)


def make_contact(webm: Path, contact: Path) -> None:
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
                    "fps=2,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black",
                    "-frames:v", "1", str(contact)], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True);server=serve();errors=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(args=["--disable-gpu","--no-sandbox","--mute-audio"])
            page=browser.new_page(viewport={"width":760,"height":820},device_scale_factor=1)
            page.on("pageerror",lambda err:errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html",wait_until="load",timeout=60000)
            page.wait_for_function("() => typeof beginStage==='function'&&typeof s6StormTick==='function'&&(window.__bofFrames|0)>4",timeout=60000)
            page.evaluate("""() => {
              const units=['cloud_lancer','cyclone_interceptor','four_engine_bomber','lightning_mine','lightning_skimmer','nuclear_carrier','reactor_storm_bomber','storm_buoy','storm_dart','thunder_fighter','turbine_drone','weather_probe'];
              const mega={stormnode:8,stormlink:6,prismmuzzle:8,prismbolt:8,cyclonemuzzle:8,cyclonetracer:8,flakshell:8,gravitymine:8,'omegabomb-hostile':8,clusterbomblet:8};
              for(const u of units)for(let f=0;f<8;f++)XART._touch('s6atk_'+u+'_'+f);
              for(const g in mega)for(let f=0;f<mega[g];f++)XART._touch('s6mb_'+g+'_'+f);
              ['nsb_blacksteel','nsb_dcarrmk2_closed'].forEach(k=>XART._touch(k));
            }""")
            page.wait_for_function("() => XART.rdy('s6atk_cloud_lancer_0')&&XART.rdy('s6atk_weather_probe_7')&&XART.rdy('s6mb_stormnode_7')&&XART.rdy('nsb_blacksteel')&&XART.rdy('nsb_dcarrmk2_closed')",timeout=60000)
            selected=set(sys.argv[1:])
            for case in CASES:
                if selected and case['name'] not in selected:continue
                page.evaluate(COMMON_SETUP);page.evaluate(case['setup']);page.wait_for_timeout(350)
                capture=start_capture(page);page.wait_for_timeout(case['duration'])
                page.locator('#screen').screenshot(path=str(OUT/f"{case['name']}.png"))
                webm=OUT/f"{case['name']}.webm";gif=OUT/f"{case['name']}.gif";contact=OUT/f"{case['name']}_contact.png"
                stop_capture(page,webm);make_gif(webm,gif);make_contact(webm,contact)
                print(f"{case['name']}: {capture['w']}x{capture['h']} gif={gif.stat().st_size}")
            page.evaluate("() => {if(window.__s6ProofTimer)clearInterval(window.__s6ProofTimer);}");browser.close()
    finally:
        server.shutdown();server.server_close()
    if errors:raise RuntimeError('Browser errors: '+' | '.join(errors))


if __name__ == '__main__':
    main()
