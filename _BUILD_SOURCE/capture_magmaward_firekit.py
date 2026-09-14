#!/usr/bin/env python3
"""Capture and verify MAGMA WARD's four-phase Stage-2 fire kit in the live game."""

from __future__ import annotations

import functools
import http.server
import json
import subprocess
import threading
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage2_magmaward_live"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


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
    page_errors = []
    console_errors = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function("() => typeof beginStage==='function' && (window.__bofFrames|0)>4", timeout=60_000)
            page.evaluate(
                """() => {
                  const keys=['nsb_magmaward_intact','nsb_magmaward_damaged','nsb_magmaward_critical'];
                  for(let i=0;i<12;i++)keys.push('mwfx_flamethrower_'+i,'mwfx_flame_laser_'+i);
                  for(let i=0;i<8;i++)keys.push('mwfx_fireball_charge_'+i,'mwfx_fireball_'+i,'mwfx_fire_shield_'+i);
                  keys.forEach(k=>XART._touch(k));
                }"""
            )
            page.wait_for_function(
                "() => XART.rdy('nsb_magmaward_intact') && XART.rdy('mwfx_flamethrower_11') && "
                "XART.rdy('mwfx_flame_laser_11') && XART.rdy('mwfx_fireball_7') && XART.rdy('mwfx_fire_shield_7')",
                timeout=60_000,
            )
            page.evaluate(
                """() => {
                  beginStage(2); player.reset(); player.invuln=999999; player.x=240; player.y=438;
                  snapCamToPlayer(); setState(GS.PLAY);
                  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0; mapScroll=levelScrollRange();
                  enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
                  particles.length=0;explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
                  boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;
                  subBossDone=false;subBossTriggered=true;
                  window.__mwEvents=[];window.__mwShieldProbe=null;
                  if(!window.__mwOriginalStart)window.__mwOriginalStart=magmaWardStartAttack;
                  magmaWardStartAttack=function(b,pat,step,cd){window.__mwEvents.push({pat,t:performance.now()});return window.__mwOriginalStart(b,pat,step,cd);};
                  spawnSubBoss('magmaward');subBoss.enter=false;subBoss.x=240;subBoss.y=116;subBoss.ty=116;subBoss.fireCd=.04;
                  const ratios=[[3200,.74],[6400,.49],[9600,.24]];
                  window.__mwTimeouts=ratios.map(([delay,ratio])=>setTimeout(()=>{
                    if(subBoss&&!subBoss.dead){subBoss.hp=subBoss.maxhp*ratio;subBoss.fireCd=.03;subBoss._mwAttack=null;subBoss._sba=null;}
                  },delay));
                  const started=performance.now();
                  window.__mwMove=setInterval(()=>{
                    const t=(performance.now()-started)/1000;
                    player.x=240+Math.sin(t*1.14)*148;player.y=438;player.invuln=999999;
                    if(subBoss&&subBoss._mwShieldActive&&!window.__mwShieldProbe){
                      const before=subBoss.hp;hitSubBoss(25,subBoss.x,subBoss.y);
                      window.__mwShieldProbe={before,after:subBoss.hp,blocked:before===subBoss.hp};
                    }
                  },16);
                }"""
            )
            page.wait_for_timeout(350)
            page.evaluate(
                """() => {
                  const c=document.getElementById('screen'),stream=c.captureStream(24);
                  const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'';
                  const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
                  rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
                  window.__mwCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};
                  rec.start(250);
                }"""
            )
            page.wait_for_timeout(13_600)
            page.locator("#screen").screenshot(path=str(OUT / "magmaward_firekit_final.png"))
            report = page.evaluate(
                """() => ({
                  patterns:window.__mwEvents.map(e=>e.pat),
                  shield:window.__mwShieldProbe,
                  liveProjectiles:eBullets.filter(b=>b._mwKind).map(b=>b._mwKind),
                  active:subBoss&&subBoss._mwAttack?subBoss._mwAttack.kind:null,
                  hp:subBoss?subBoss.hp:null,
                  maxhp:subBoss?subBoss.maxhp:null
                })"""
            )
            with page.expect_download(timeout=30_000) as info:
                page.evaluate(
                    """async () => {
                      const blob=await window.__mwCapture.stop(),a=document.createElement('a');
                      a.href=URL.createObjectURL(blob);a.download='magmaward-firekit.webm';document.body.appendChild(a);a.click();a.remove();
                    }"""
                )
            webm = OUT / "magmaward_firekit.webm"
            info.value.save_as(webm)
            page.evaluate("() => {clearInterval(window.__mwMove);for(const id of window.__mwTimeouts||[])clearTimeout(id);}")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    gif = OUT / "magmaward_firekit.gif"
    subprocess.run(
        [
            FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
            "-lavfi",
            "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
            "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
            "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
            "-loop", "0", str(gif),
        ],
        check=True,
    )
    contact = OUT / "magmaward_firekit_contact.png"
    subprocess.run(
        [
            FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
            "-vf", "fps=0.8,scale=240:-1:flags=lanczos,tile=4x3:padding=4:margin=4:color=black",
            "-frames:v", "1", str(contact),
        ],
        check=True,
    )
    report["pageErrors"] = page_errors
    report["consoleErrors"] = console_errors
    report["allFourPatterns"] = all(
        p in report["patterns"]
        for p in ("magmaflame", "magmaflamelaser", "magmafireball", "magmafireshield")
    )
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if page_errors or console_errors or not report["allFourPatterns"] or not (report["shield"] or {}).get("blocked"):
        raise RuntimeError(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(gif)


if __name__ == "__main__":
    main()
