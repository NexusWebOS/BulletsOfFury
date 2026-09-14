#!/usr/bin/env python3
"""Deterministic live QA for Magma Ward and Inferno Reaver's movement-driven fire kits."""

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
OUT = ROOT / "docs" / "proofs" / "stage2_fire_bosses_0830"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def begin_capture(page):
    page.evaluate(r"""() => {
      const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
        .find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:5200000}:undefined);
      rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__s2FireCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
        rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();
      })};rec.start(250);
    }""")


def stop_capture(page, target: Path):
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(r"""async () => {
          const blob=await window.__s2FireCapture.stop(),a=document.createElement('a');
          a.href=URL.createObjectURL(blob);a.download='stage2-fire-boss.webm';
          document.body.appendChild(a);a.click();a.remove();
        }""")
    info.value.save_as(target)


def derivatives(webm: Path, gif: Path, contact: Path):
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi",
        "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
        "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
        "-loop", "0", str(gif),
    ], check=True)
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
        "fps=.75,scale=240:-1:flags=lanczos,tile=4x3:padding=4:margin=4:color=black",
        "-frames:v", "1", str(contact),
    ], check=True)


SETUP = r"""(kind) => {
  beginStage(2);player.reset();player.invuln=999999;player.x=240;player.y=438;
  snapCamToPlayer();setState(GS.PLAY);stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;
  stageTimer=0;mapScroll=levelScrollRange();enemies.length=0;eBullets.length=0;
  pBullets.length=0;powerups.length=0;particles.length=0;explosions.length=0;
  smokeTrails.length=0;playerLocks.length=0;boss=null;bossActive=false;bossDefeated=false;
  subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=true;
  if(kind==='mini'){spawnSubBoss('magmaward');subBoss.enter=false;subBoss.x=240;subBoss.y=116;subBoss.ty=116;subBoss._sbm=SBM_HOLD;subBoss._sbmT=999;subBoss.fireCd=999;}
  else{spawnBoss('infernoreaver');boss.enter=false;boss.x=240;boss.y=116;boss.ty=116;boss._sbm=SBM_HOLD;boss._sbmT=999;boss.fireCd=999;}
  const born=performance.now();if(window.__s2Pilot)clearInterval(window.__s2Pilot);
  window.__s2Pilot=setInterval(()=>{const t=(performance.now()-born)/1000;
    player.x=240+Math.sin(t*1.05)*154;player.y=438;player.invuln=999999;},16);
}"""


def run_mini(page):
    page.evaluate(SETUP, "mini")
    page.evaluate(r"""() => {
      const A=window.__mw0830={kinds:{},holdSlots:{},minHoldX:999,maxHoldX:-999,maxHoldY:0,
        maxSpin:0,shieldFrames:0,laserFrames:0,fireballs:0,embers:0,minHomeError:999,recovered:false,
        slideMinX:999,slideMaxX:-999,slideMaxAngleError:0,slideFrames:0,
        douseMaxCenterError:0,douseMinPose:999,douseMaxPose:-999,douseFrames:0};
      const seen=new WeakSet();window.__mw0830Timer=setInterval(()=>{
        const b=subBoss;if(!b)return;const q=b._mwAttack;
        if(q){A.kinds[q.kind]=1;A.maxSpin=Math.max(A.maxSpin,Math.abs(q.poseRot||0));
          if(q.kind==='magmaflamelaser'&&q.t>=q.tell&&q.t<q.tell+q.active){
            A.minHoldX=Math.min(A.minHoldX,b.x);A.maxHoldX=Math.max(A.maxHoldX,b.x);A.maxHoldY=Math.max(A.maxHoldY,b.y);
            if(q.holdSlot)A.holdSlots[q.holdSlot]=1;
            if(q.mode==='slide'){
              A.slideMinX=Math.min(A.slideMinX,b.x);A.slideMaxX=Math.max(A.slideMaxX,b.x);A.slideFrames++;
              if(q.flameOn)A.slideMaxAngleError=Math.max(A.slideMaxAngleError,Math.abs(q.flameAng-Math.PI/2));
            }else if(q.mode==='douse'){
              A.douseMaxCenterError=Math.max(A.douseMaxCenterError,Math.abs(b.x-worldWidth()/2));
              A.douseMinPose=Math.min(A.douseMinPose,q.poseRot);A.douseMaxPose=Math.max(A.douseMaxPose,q.poseRot);A.douseFrames++;
            }}
          if(b._mwShieldActive)A.shieldFrames++;
          if(q.laserLive)A.laserFrames++;
        }else if(Object.keys(A.kinds).length>=4){
          A.minHomeError=Math.min(A.minHomeError,Math.hypot(b.x-worldWidth()/2,b.y-shipBossStationY(b)));
          if(Math.abs(b.x-worldWidth()/2)<140&&Math.abs(b.y-shipBossStationY(b))<18)A.recovered=true;
        }
        for(const p of eBullets){if(seen.has(p))continue;seen.add(p);if(p._mwKind==='fireball')A.fireballs++;else if(p._mwKind==='ember')A.embers++;}
      },16);
    }""")
    begin_capture(page)
    steps = [
        ("magmaflame", 1, 3500),
        ("magmaflamelaser", 2, 7950),
        ("magmafireball", 3, 2500),
        ("magmafireshield", 4, 4300),
    ]
    for index, (pattern, beat, wait_ms) in enumerate(steps, start=1):
        page.evaluate(f"() => {{subBoss.fireCd=999;magmaWardStartAttack(subBoss,'{pattern}',{beat},1);}}")
        page.wait_for_timeout(wait_ms)
        page.locator("#screen").screenshot(path=str(OUT / f"magma_ward_phase{index}.png"))
    webm = OUT / "Magma_Ward_Fire_Dance.webm"
    gif = OUT / "Magma_Ward_Fire_Dance.gif"
    contact = OUT / "Magma_Ward_Fire_Dance_Contact.png"
    stop_capture(page, webm); derivatives(webm, gif, contact)
    report = page.evaluate(r"""() => {clearInterval(window.__mw0830Timer);const A=window.__mw0830,b=subBoss;
      A.holdSpan=A.maxHoldX-A.minHoldX;A.slideSpan=A.slideMaxX-A.slideMinX;A.douseArc=A.douseMaxPose-A.douseMinPose;return A;}""")
    assertions = {
        "allFourPatterns": all(name in report["kinds"] for name in ("magmaflame", "magmaflamelaser", "magmafireball", "magmafireshield")),
        "fullFlameSpin": report["maxSpin"] > 6.0,
        "alternatesLeftRight": all(side in report["holdSlots"] for side in ("L", "R")),
        "slidesLeftToRight": report["slideSpan"] > 250 and report["slideFrames"] > 80,
        "slideFlameIsVertical": report["slideMaxAngleError"] < 1e-9,
        "centredDouseMode": report["douseMaxCenterError"] < 1e-9 and report["douseFrames"] > 100,
        "douseUsesFortyFiveDegrees": report["douseMinPose"] < -0.72 and report["douseMaxPose"] > 0.72 and report["douseArc"] <= 1.58,
        "fireRoundsPresent": report["embers"] >= 20 and report["fireballs"] >= 3,
        "shieldThenLaser": report["shieldFrames"] > 20 and report["laserFrames"] > 20,
        "restoresToStation": report["recovered"],
    }
    report["assertions"] = assertions; report["passed"] = all(assertions.values())
    if not report["passed"]:
        raise RuntimeError("Magma Ward QA failed: " + json.dumps(report, indent=2))
    return report


def run_boss(page):
    page.evaluate(SETUP, "boss")
    page.evaluate(r"""() => {
      const A=window.__ir0830={fx:{},beamSamples:[],rollPhases:{},minRollX:999,maxRollX:-999,
        maxRollY:0,maxPoseRot:0,rollFlameFrames:0,minHomeError:999,recovered:false};const seen=new WeakSet();
      window.__ir0830Timer=setInterval(()=>{const b=boss;if(!b)return;
        if(b._l23Beam)A.beamSamples.push(b._l23Beam.angles.slice());
        if(b._irRoll){const r=b._irRoll;A.rollPhases[r.phase]=1;A.maxPoseRot=Math.max(A.maxPoseRot,Math.abs(r.poseRot||0));
          if(r.phase==='roll'){A.minRollX=Math.min(A.minRollX,b.x);A.maxRollX=Math.max(A.maxRollX,b.x);A.maxRollY=Math.max(A.maxRollY,b.y);A.rollFlameFrames++;}}
        else if(A.rollPhases.recover){
          A.minHomeError=Math.min(A.minHomeError,Math.hypot(b.x-worldWidth()/2,b.y-shipBossStationY(b)));
          if(Math.abs(b.x-worldWidth()/2)<140&&Math.abs(b.y-shipBossStationY(b))<18)A.recovered=true;
        }
        for(const p of eBullets){if(seen.has(p))continue;seen.add(p);if(p._l23fx)A.fx[p._l23fx]=1;}
      },16);
    }""")
    begin_capture(page)
    steps = [(.95, 800), (.55, 950), (.35, 3500), (.15, 5600)]
    for index, (ratio, wait_ms) in enumerate(steps, start=1):
        page.evaluate(f"""() => {{boss.hp=boss.maxhp*{ratio};boss.fireCd=999;boss._sba=null;shipBossAttack(boss);boss.fireCd=999;}}""")
        page.wait_for_timeout(wait_ms)
        page.locator("#screen").screenshot(path=str(OUT / f"inferno_reaver_phase{index}.png"))
    webm = OUT / "Inferno_Reaver_Fire_Roll.webm"
    gif = OUT / "Inferno_Reaver_Fire_Roll.gif"
    contact = OUT / "Inferno_Reaver_Fire_Roll_Contact.png"
    stop_capture(page, webm); derivatives(webm, gif, contact)
    report = page.evaluate(r"""() => {clearInterval(window.__ir0830Timer);const A=window.__ir0830,b=boss;
      A.rollSpan=A.maxRollX-A.minRollX;A.beamMin=999;A.beamMax=-999;A.beamMaxSouthOffset=0;
      for(const sample of A.beamSamples)for(const ang of sample){A.beamMin=Math.min(A.beamMin,ang);A.beamMax=Math.max(A.beamMax,ang);A.beamMaxSouthOffset=Math.max(A.beamMaxSouthOffset,Math.abs(ang-Math.PI/2));}
      A.beamAngularTravel=A.beamMax-A.beamMin;
      return A;}""")
    assertions = {
        "fireAmmoPresent": all(name in report["fx"] for name in ("inferno_mg", "inferno_shotgun")),
        "laserDousesFortyFiveDegrees": report["beamAngularTravel"] > 1.40 and report["beamAngularTravel"] <= 1.58 and report["beamMaxSouthOffset"] <= .80,
        "rollHasAllPhases": all(name in report["rollPhases"] for name in ("tell", "roll", "recover")),
        "rollCrossesArena": report["rollSpan"] > 245,
        "rollComesClose": report["maxRollY"] > 220,
        "hullSpinsContinuously": report["maxPoseRot"] > 18,
        "heldFlameVisible": report["rollFlameFrames"] > 100,
        "restoresToStation": report["recovered"],
    }
    report["assertions"] = assertions; report["passed"] = all(assertions.values())
    if not report["passed"]:
        raise RuntimeError("Inferno Reaver QA failed: " + json.dumps(report, indent=2))
    return report


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve(); page_errors = []; console_errors = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof infernoReaverRollStart==='function' && (window.__bofFrames|0)>4", timeout=60_000)
            page.evaluate(r"""() => {
              const keys=['nsb_magmaward_intact','nsb_magmaward_damaged','nsb_magmaward_critical','nsb_inferno_reaver'];
              for(let i=0;i<12;i++)keys.push('mwfx_flamethrower_'+i,'mwfx_flame_laser_'+i,'l23fx_inferno_laser_'+i);
              for(let i=0;i<8;i++)keys.push('mwfx_fireball_charge_'+i,'mwfx_fireball_'+i,'mwfx_fire_shield_'+i,'l23fx_inferno_mg_'+i,'l23fx_inferno_shotgun_'+i);
              keys.forEach(k=>XART._touch(k));
            }""")
            page.wait_for_function("() => XART.rdy('nsb_magmaward_intact') && XART.rdy('nsb_inferno_reaver') && XART.rdy('mwfx_flamethrower_11') && XART.rdy('mwfx_flame_laser_11') && XART.rdy('l23fx_inferno_laser_11')", timeout=60_000)
            mini = run_mini(page); boss = run_boss(page)
            page.evaluate("() => {if(window.__s2Pilot)clearInterval(window.__s2Pilot);}")
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    report = {"magmaWard": mini, "infernoReaver": boss, "pageErrors": page_errors, "consoleErrors": console_errors}
    report["passed"] = bool(mini["passed"] and boss["passed"] and not page_errors and not console_errors)
    (OUT / "Stage2_Fire_Bosses_QA.json").write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    if not report["passed"]:
        raise RuntimeError(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
