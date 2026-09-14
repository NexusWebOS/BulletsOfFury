#!/usr/bin/env python3
"""Deterministic live-canvas QA and gameplay capture for the Stage-1 Jungle Cruiser."""

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
OUT = ROOT / "docs" / "proofs" / "stage1_jungle_cruiser_0830"
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
    return page.evaluate(
        """() => {
          const c=document.getElementById('screen'),stream=c.captureStream(30);
          const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
            .find(t=>MediaRecorder.isTypeSupported(t))||'';
          const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:5000000}:undefined);
          rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
          window.__jcCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
            rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();
          })};
          rec.start(250);return {w:c.width,h:c.height,mime};
        }"""
    )


def stop_capture(page, target: Path):
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(
            """async () => {
              const blob=await window.__jcCapture.stop(),a=document.createElement('a');
              a.href=URL.createObjectURL(blob);a.download='jungle-cruiser-gameplay.webm';
              document.body.appendChild(a);a.click();a.remove();
            }"""
        )
    info.value.save_as(target)


def transcode(webm: Path, mp4: Path, gif: Path, contact: Path):
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
        str(mp4),
    ], check=True)
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm),
        "-vf", "fps=10,scale=360:-1:flags=neighbor,split[s0][s1];"
               "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
               "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
        "-loop", "0", str(gif),
    ], check=True)
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-ss", "1.0", "-i", str(webm),
        "-vf", "fps=1/4,scale=240:-1:flags=neighbor,tile=3x3:padding=4:margin=4:color=black",
        "-frames:v", "1", str(contact),
    ], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    errors: list[str] = []
    video = OUT / "Stage1_Jungle_Cruiser_Gameplay.webm"
    mp4 = OUT / "Stage1_Jungle_Cruiser_Gameplay.mp4"
    gif = OUT / "Stage1_Jungle_Cruiser_Gameplay.gif"
    contact = OUT / "Stage1_Jungle_Cruiser_Contact.png"
    report_path = OUT / "Stage1_Jungle_Cruiser_QA.json"
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=[
                "--disable-gpu", "--no-sandbox", "--autoplay-policy=no-user-gesture-required"
            ])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html",
                      wait_until="load", timeout=60_000)
            page.wait_for_function(
                "() => typeof beginStage==='function' && typeof jungleCruiserDirector==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.evaluate("""() => {
              ['nsb_junglecruiser','s1fx_rotary_muzzle_0','bpfx_muzzle_missile_0',
               'bpfx_muzzle_laser_0','nlz_3_b0','nhxsb_g_2','nxp_dense_0']
                .forEach(k=>{try{XART._touch(k)}catch(_e){}});
            }""")
            page.wait_for_timeout(1200)
            page.evaluate("""() => {
              beginStage(1);player.reset();player.invuln=999999;player.y=438;
              snapCamToPlayer();setState(GS.PLAY);
              stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
              enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
              particles.length=0;explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
              boss=null;bossActive=false;bossDefeated=false;
              subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
              mapScroll=1250;_prevMapScroll=mapScroll;
              spawnSubBoss('junglecruiser');subBoss.enter=false;subBoss.x=worldWidth()/2;
              subBoss.y=116;subBoss.ty=116;subBoss._entT=0;

              const A=window.__jcAudit={start:performance.now(),states:[],stateSeen:{},bullets:{rocket:0,loop:0,nose:0,helix:0,other:0},
                flashes:{missile:0,mg:0,laser:0},maxAnchorError:{missile:0,mg:0,laser:0},
                ghostSolidViolations:0,ghostBodyFrames:0,beamFrames:0,beamSeconds:0,chargeFrames:0,
                beamMaxCenterError:0,beamMinAngle:999,beamMaxAngle:-999,
                damagedFrames:0,enragedFrames:0,deathFx:false,removed:false,soundCalls:{}};
              const seen=new WeakSet(),soundNames=['missile','enemyMachineGunLight','enemyMachineGunHeavy',
                'enemyHeavyLaser','laserBeamStart','laserBeamEnd','bossWeaponCharge','expBig','expSmall'];
              if(Audio&&Audio.SFX)for(const n of soundNames){const fn=Audio.SFX[n];if(typeof fn!=='function')continue;
                Audio.SFX[n]=function(){A.soundCalls[n]=(A.soundCalls[n]||0)+1;return fn.apply(this,arguments);};}
              let lastState='';
              window.__jcTimer=setInterval(()=>{
                const sec=(performance.now()-A.start)/1000;
                player.x=worldWidth()/2+Math.sin(sec*1.10)*150;
                player.y=438+Math.sin(sec*.67)*10;player.invuln=999999;
                const b=subBoss;
                if(!b){A.removed=true;return;}
                if(b._jc){const s=b._jc.state;if(s!==lastState){lastState=s;A.states.push({state:s,time:+sec.toFixed(2)});A.stateSeen[s]=1;}
                  if(b._jc.beamActive){A.beamFrames++;A.beamSeconds+=.025;
                    A.beamMaxCenterError=Math.max(A.beamMaxCenterError,Math.abs(b.x-worldWidth()/2));
                    A.beamMinAngle=Math.min(A.beamMinAngle,b._jc.beamAng||0);
                    A.beamMaxAngle=Math.max(A.beamMaxAngle,b._jc.beamAng||0);}
                  if(b._jc.charge>0)A.chargeFrames++;
                  if(b._jc.damaged)A.damagedFrames++;
                  if(b._jc.enraged)A.enragedFrames++;
                  if(b._jcGhost){A.ghostBodyFrames++;if(subBossSolidAt(b.x,b.y)!==false)A.ghostSolidViolations++;}
                }
                if(b._deathFxStarted)A.deathFx=true;
                for(const q of eBullets){if(seen.has(q))continue;seen.add(q);
                  if(q._jcLoop){A.bullets.loop++;A.bullets.rocket++;}
                  else if(q._jcRocket)A.bullets.rocket++;
                  else if(q._jcNose)A.bullets.nose++;
                  else if(q._jcHelix)A.bullets.helix++;
                  else A.bullets.other++;
                }
                if(typeof _navalFlashes!=='undefined')for(const f of _navalFlashes){
                  let bucket=null,slots=[];
                  if(f.fam==='bpfx_muzzle_missile'){bucket='missile';slots=['L','R'];}
                  else if(f.fam==='s1fx_rotary_muzzle'){bucket='mg';slots=['C'];}
                  else if(f.fam==='bpfx_muzzle_laser'){bucket='laser';slots=['C'];}
                  if(!bucket||f._jcCounted)continue;f._jcCounted=true;A.flashes[bucket]++;
                  let best=999;for(const slot of slots){const m=shipBossMount(b,slot);best=Math.min(best,Math.hypot(f.x-m.x,f.y-m.y));}
                  A.maxAnchorError[bucket]=Math.max(A.maxAnchorError[bucket],best);
                }
              },25);
              setTimeout(()=>{if(subBoss&&!subBoss.dead)subBoss.hp=subBoss.maxhp*.48;},8000);
              setTimeout(()=>{if(subBoss&&!subBoss.dead)subBoss.hp=subBoss.maxhp*.24;},23200);
              setTimeout(()=>{if(subBoss&&!subBoss.dead){subBoss.hp=1;hitSubBoss(99999,subBoss.x,subBoss.y);}},32500);
            }""")
            page.wait_for_timeout(300)
            capture = start_capture(page)
            page.wait_for_timeout(36_000)
            page.locator("#screen").screenshot(path=str(OUT / "Stage1_Jungle_Cruiser_Final.png"))
            stop_capture(page, video)
            report = page.evaluate("""() => {
              if(window.__jcTimer)clearInterval(window.__jcTimer);
              const A=window.__jcAudit;A.beamSeconds=+A.beamSeconds.toFixed(2);
              for(const k in A.maxAnchorError)A.maxAnchorError[k]=+A.maxAnchorError[k].toFixed(2);
              A.beamMaxCenterError=+A.beamMaxCenterError.toFixed(3);
              A.beamMinAngle=+A.beamMinAngle.toFixed(3);A.beamMaxAngle=+A.beamMaxAngle.toFixed(3);
              return A;
            }""")
            browser.close()

        report["capture"] = capture
        report["pageErrors"] = errors
        for i, entry in enumerate(report["states"]):
            if entry["state"] == "beamSweep" and i + 1 < len(report["states"]):
                report["beamSeconds"] = round(report["states"][i + 1]["time"] - entry["time"], 2)
                break
        required = {"acquire", "missiles", "edgeGun", "gunSlide", "diveSouth", "riseNorth",
                    "returnTop", "beamCharge", "beamSweep", "rageMissiles", "rageChargeEdge",
                    "rageSlide", "ragePounce", "rageOrbit"}
        report["assertions"] = {
            "allRequiredStates": required.issubset(report["stateSeen"]),
            "allThreeHardpointsFlashed": all(report["flashes"].get(k, 0) > 0 for k in ("missile", "mg", "laser")),
            "flashesRemainAnchored": all(report["maxAnchorError"].get(k, 999) <= 3.0 for k in ("missile", "mg", "laser")),
            "projectilesAuthoredOnly": report["bullets"].get("other", 1) == 0,
            "loopMissilesPresent": report["bullets"].get("loop", 0) >= 4,
            "helixPresent": report["bullets"].get("helix", 0) >= 1,
            "beamHeldEightSeconds": report.get("beamSeconds", 0) >= 8.0,
            "beamCentered": report.get("beamMaxCenterError", 999) <= 0.01,
            "beamSweepsBothSides": report.get("beamMinAngle", 0) <= -0.50 and report.get("beamMaxAngle", 0) >= 0.50,
            "ghostFlybysNonSolid": report.get("ghostSolidViolations", 1) == 0 and report.get("ghostBodyFrames", 0) > 0,
            "damageStatesVisible": report.get("damagedFrames", 0) > 0 and report.get("enragedFrames", 0) > 0,
            "authoredExplosionDeath": bool(report.get("deathFx")),
            "noBrowserErrors": not errors,
        }
        report["passed"] = all(report["assertions"].values())
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        if not report["passed"]:
            raise RuntimeError("Jungle Cruiser QA failed: " + json.dumps(report["assertions"]))
        transcode(video, mp4, gif, contact)
        print(json.dumps({"passed": True, "video": str(mp4), "contact": str(contact), "report": str(report_path)}, indent=2))
    finally:
        server.shutdown();server.server_close()


if __name__ == "__main__":
    main()
