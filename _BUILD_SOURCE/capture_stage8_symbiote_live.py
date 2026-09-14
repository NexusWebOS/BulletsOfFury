#!/usr/bin/env python3
"""Live Chromium proofs for the Stage-8 symbiote entrance and reinforcement fleet."""

from __future__ import annotations

import functools
import http.server
import subprocess
import threading
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage8_symbiote_live"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def start_capture(page):
    return page.evaluate("""() => {const c=document.getElementById('screen'),s=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(s,mime?{mimeType:mime}:undefined);
      rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__symcap={rec,chunks,mime,stop:()=>new Promise(ok=>{rec.onstop=()=>ok(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};
      rec.start(200);return {w:c.width,h:c.height};}""")


def stop_capture(page, target):
    with page.expect_download(timeout=30000) as info:
        page.evaluate("""async()=>{const b=await window.__symcap.stop(),a=document.createElement('a');
          a.href=URL.createObjectURL(b);a.download='symbiote.webm';document.body.appendChild(a);a.click();a.remove();}""")
    info.value.save_as(target)


def gif_and_contact(webm, gif, contact, seconds):
    palette = ("fps=10,scale=360:-1:flags=lanczos,split[s0][s1];"
               "[s0]palettegen=max_colors=160:stats_mode=diff[p];"
               "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
                    "-lavfi", palette, "-loop", "0", str(gif)], check=True)
    frames = max(4, int(seconds * 2))
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
                    f"fps=2,scale=240:-1:flags=lanczos,tile=4x{(frames+3)//4}:padding=4:margin=4:color=black",
                    "-frames:v", "1", str(contact)], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server, errors = serve(), []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60000)
            page.wait_for_function("() => typeof beginStage==='function'&&typeof symbioteEntryTick==='function'&&(window.__bofFrames|0)>4", timeout=60000)
            page.evaluate("""() => {
              for(let f=0;f<4;f++)XART._touch('s8symboss_form_'+f);
              for(let f=0;f<16;f++)XART._touch('s8symboss_entrance_'+f);
              for(const u of ['armored_gunship','needle_interceptor','scout_drone','solar_corvette','spread_wing_fighter','stealth_crescent']){
                XART._touch('s8nf_'+u+'_idle');
                for(let f=0;f<4;f++){XART._touch('s8nf_'+u+'_muzzle_'+f);XART._touch('s8nf_'+u+'_projectile_'+f);}
              }
            }""")
            page.wait_for_function("() => XART.rdy('s8symboss_form_3')&&XART.rdy('s8symboss_entrance_15')&&XART.rdy('s8nf_stealth_crescent_projectile_3')", timeout=60000)

            setup = """() => {beginStage(8);player.reset();player.invuln=999999;player.x=240;player.y=442;
              snapCamToPlayer();setState(GS.PLAY);stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;
              explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
              boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;
              subBossDone=false;subBossTriggered=false;}"""

            # Entrance proof: the real spawn path, including invulnerability and handoff.
            page.evaluate(setup)
            hp_contract = page.evaluate("""() => {spawnBoss('vileexistence');const bars=[];
              for(let i=0;i<4;i++){vileBuildForm(boss,i);bars.push({form:boss._vForm,hp:boss.hp,max:boss.maxhp,art:VILE_FORMS[i].art});}
              vileBuildForm(boss,0);boss.enter=true;
              return {total:boss._vBase,phase:boss._vPhaseHp,max:boss.maxhp,form:boss._vForm,
                      entry:!!boss._symEntry,enter:boss.enter,bars};}""")
            if (hp_contract["phase"] * 4 != hp_contract["total"] or
                    hp_contract["max"] != hp_contract["phase"] or
                    any(b["hp"] != hp_contract["phase"] or b["max"] != hp_contract["phase"]
                        for b in hp_contract["bars"])):
                raise RuntimeError(f"invalid 25% boss HP contract: {hp_contract}")
            start_capture(page)
            page.wait_for_timeout(3400)
            page.locator("#screen").screenshot(path=str(OUT / "stage8_symbiote_entrance_final.png"))
            entrance_webm = OUT / "stage8_symbiote_entrance.webm"
            stop_capture(page, entrance_webm)
            gif_and_contact(entrance_webm, OUT / "stage8_symbiote_entrance.gif",
                            OUT / "stage8_symbiote_entrance_contact.png", 3.4)

            # Six live AIs at once: their fixed hulls, anchored flashes, and distinct ammunition.
            page.evaluate(setup)
            page.evaluate("""() => {
              const rows=[['s8gunship',130,118],['s8solar',350,112],['s8needlejet',555,126],
                          ['s8scout',130,250],['s8crescent',350,245],['s8spread',555,272]];
              for(const [k,x,y] of rows){const e=spawnEnemy(k,x,y,{});if(e){e.x=x;e.y=y;e._fcd=.06;e._stagger=0;}}
              const start=performance.now();window.__symPlayer=setInterval(()=>{const t=(performance.now()-start)/1000;
                player.x=340+Math.sin(t*1.1)*180;player.y=450;player.invuln=999999;},16);
            }""")
            start_capture(page)
            page.wait_for_timeout(6200)
            page.locator("#screen").screenshot(path=str(OUT / "stage8_symbiote_fleet_final.png"))
            fleet_webm = OUT / "stage8_symbiote_fleet.webm"
            stop_capture(page, fleet_webm)
            gif_and_contact(fleet_webm, OUT / "stage8_symbiote_fleet.gif",
                            OUT / "stage8_symbiote_fleet_contact.png", 6.2)
            page.evaluate("() => {if(window.__symPlayer)clearInterval(window.__symPlayer);}")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    if errors:
        raise RuntimeError("browser errors: " + " | ".join(errors))
    print(f"HP contract: {hp_contract}")
    print(f"proofs: {OUT}")


if __name__ == "__main__":
    main()
