#!/usr/bin/env python3
"""Capture the real Stage-4 Blacksite highway controllers from the live game canvas."""

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
OUT = ROOT / "docs" / "proofs" / "stage4_ai_live"
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
  if(window.__s4ProofTimer){ clearInterval(window.__s4ProofTimer); window.__s4ProofTimer=0; }
  if(window.__s4ProofTimeouts){ for(const id of window.__s4ProofTimeouts) clearTimeout(id); }
  window.__s4ProofTimeouts=[];
  beginStage(4); player.reset(); player.invuln=999999; player.x=240; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0;
  mapScroll=levelScrollRange();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  const started=performance.now();
  window.__s4ProofTimer=setInterval(()=>{
    const t=(performance.now()-started)/1000;
    player.x=240+Math.sin(t*1.09)*132;
    player.y=438+Math.sin(t*.57)*10;
    player.invuln=999999;
  },16);
}"""


def enemy_case(kind: str, x: int = 240, y: int = 140, duration: int = 4_400) -> dict:
    prep = "e._fcd=0;e._stagger=0;"
    if kind in {"s4interceptor", "s4rocket"}:
        prep += "e._side=1;e._dir=1;"
    return {
        "name": f"Stage4_{kind}_Enemy_AI",
        "duration": duration,
        "setup": f"""() => {{
          const e=spawnEnemy('{kind}',{x},{y},{{}});
          if(e){{ e.x={x}; e.y={y}; e.hp=e._maxhp||e.hp; {prep} }}
        }}""",
    }


CASES = [
    enemy_case("s4airfield"),
    enemy_case("s4tractor"),
    enemy_case("s4interceptor", x=80, y=108, duration=4_100),
    enemy_case("s4command", y=106, duration=4_600),
    enemy_case("s4barrel", duration=3_800),
    enemy_case("s4tanker", duration=4_500),
    enemy_case("s4bomber", duration=4_700),
    enemy_case("s4heavyjet", duration=4_500),
    enemy_case("s4missile", duration=4_700),
    enemy_case("s4rocket", x=90, duration=4_300),
    enemy_case("s4minitank", duration=4_200),
    enemy_case("s4sam", duration=5_000),
    {
        "name": "Stage4_Dambreaker_Arsenal_Mini_AI",
        "duration": 9_000,
        "setup": r"""() => {
          const e=spawnArsenalMini('dambreaker');
          if(e){ e.y=112; e.vy=0; e._dr.entry=0; e._dr.cd=.06; }
        }""",
    },
    {
        "name": "Stage4_Olive_Warden_Miniboss_AI",
        "duration": 9_500,
        "setup": r"""() => {
          spawnSubBoss('olivewarden');
          subBoss.enter=false; subBoss.x=240; subBoss.y=132; subBoss.ty=132;
          subBoss.fireCd=.05; subBoss._sbStep=0; subBoss._sbPhase=0;
          window.__s4ProofTimeouts.push(setTimeout(()=>{
            if(subBoss&&!subBoss.dead){ subBoss.hp=subBoss.maxhp*.40; subBoss.fireCd=.04; }
          },4500));
        }""",
    },
    {
        "name": "Stage4_Storm_Sovereign_Boss_AI",
        "duration": 11_500,
        "setup": r"""() => {
          spawnBoss('stormsovereign');
          boss.enter=false; boss.x=240; boss.y=150; boss.ty=150; boss.fireCd=.04;
          const thresholds=[[3900,.62],[7600,.26]];
          for(const [delay,ratio] of thresholds){
            window.__s4ProofTimeouts.push(setTimeout(()=>{
              if(boss&&!boss.dead){ boss.hp=boss.maxhp*ratio; boss.fireCd=.04; }
            },delay));
          }
        }""",
    },
    {
        "name": "Stage4_Storm_Sovereign_ShieldBreak_AI",
        "duration": 13_000,
        "setup": r"""() => {
          spawnBoss('stormsovereign');
          boss.enter=false; boss.x=240; boss.y=150; boss.ty=150; boss.fireCd=.04;
          const hp0=boss.hp;
          const id=setInterval(()=>{
            if(!boss||boss.dead){clearInterval(id);return;}
            const H=boss._s4war&&boss._s4war.shield;
            if(!H||!H.active){
              window.__s4ShieldProof={hp0:hp0,hpAfter:boss.hp,allDead:H&&H.nodes.every(n=>n.dead)};
              clearInterval(id);return;
            }
            const n=H.nodes.find(q=>!q.dead);
            if(n){
              const routed=bossHitTest(n.x,n.y);
              if(routed){_lastHitX=n.x;_lastHitY=n.y;hitBoss(Math.ceil(n.maxhp*.34));}
            }
          },360);
          window.__s4ProofTimeouts.push(id);
        }""",
    },
    {
        "name": "Stage4_Storm_Sovereign_Rearm_Chainguns_AI",
        "duration": 20_000,
        "setup": r"""() => {
          spawnBoss('stormsovereign');
          boss.enter=false; boss.x=240; boss.y=150; boss.ty=150; boss.fireCd=.04;
          const fake={x:boss.x,y:boss.y+boss.w*.64,vx:0,vy:-8,dmg:1};
          const deflected=stage4ShieldDeflectBullet(boss,fake);
          let halfSpawn=0,leftDestroyed=false,leftRouted=false,bossHpBeforeCore=0,bossHpAfterCore=0,
              blockedDuringFire=false,blockedHpBefore=0,blockedHpAfter=0,destroyedDuringOverheat=false,
              spreadShifted=false;
          const id=setInterval(()=>{
            if(!boss||boss.dead){clearInterval(id);return;}
            const S=boss._s4war,H=S&&S.shield;
            if(!H)return;
            if(H.rearming)return;
            if(H.active){
              /* At 25%, leave the restored shield intact and prove that only the helper killed
                 during the 50% cycle was replaced. */
              if(S.shieldThresholdIndex===3){
                const left=S.coreTurrets.find(t=>t.side<0),right=S.coreTurrets.find(t=>t.side>0);
                if(left&&right&&!left.dead&&!right.dead&&left.materialize>=.92&&right.materialize>=.92){
                  window.__s4RearmProof={cycles:H.cycle,thresholds:S.shieldThresholdIndex,
                    shieldActive:H.active,halfSpawn:halfSpawn,leftDestroyed:leftDestroyed,leftRouted:leftRouted,
                    blockedDuringFire:blockedDuringFire,blockedHpBefore:blockedHpBefore,
                    blockedHpAfter:blockedHpAfter,destroyedDuringOverheat:destroyedDuringOverheat,
                    spreadShifted:spreadShifted,cycleSeen:Object.assign({},S.coreCycleSeen),
                    leftGeneration:left.generation,rightGeneration:right.generation,
                    bossHpBeforeCore:bossHpBeforeCore,bossHpAfterCore:bossHpAfterCore,
                    coreShots:S.coreShots,coreSpreadShots:S.coreSpreadShots,
                    coreBlockedHits:S.coreBlockedHits,coreVulnerableHits:S.coreVulnerableHits,
                    spreadLast:S.coreSpreadLast,fullSpread:stage4CoreSpreadOffsets(false,false),
                    deflected:deflected,deflectVy:fake.vy,
                    leftAngle:left.ang,rightAngle:right.ang,
                    barrelLeftShots:S.coreBarrelShots['-1'],barrelRightShots:S.coreBarrelShots['1'],
                    helperSpan:right.x-left.x,leftHp:left.hp,rightHp:right.hp,
                    hp:boss.hp,maxhp:boss.maxhp,finalGuns:S.finalGuns};
                  clearInterval(id);return;
                }
              }
              /* Hold the 50% shield long enough to see both helpers traverse and fire. Then
                 destroy only the left helper, proving that it owns independent HP. */
              if(S.shieldThresholdIndex===2){
                const living=S.coreTurrets.filter(t=>!t.dead&&t.materialize>=.92);
                halfSpawn=Math.max(halfSpawn,living.length);
                const left=S.coreTurrets.find(t=>t.side<0),right=S.coreTurrets.find(t=>t.side>0);
                if(left&&!left.dead&&left.state==='fire'&&!blockedDuringFire){
                  blockedHpBefore=left.hp;const routed=bossHitTest(left.x,left.y);
                  if(routed){_lastHitX=left.x;_lastHitY=left.y;hitBoss(31);}
                  blockedHpAfter=left.hp;blockedDuringFire=routed&&blockedHpAfter===blockedHpBefore;return;
                }
                if(left&&!left.dead&&left.state==='overheat'&&blockedDuringFire&&!leftDestroyed){
                  bossHpBeforeCore=boss.hp;leftRouted=bossHitTest(left.x,left.y);
                  if(leftRouted){_lastHitX=left.x;_lastHitY=left.y;hitBoss(left.maxhp+1);}
                  bossHpAfterCore=boss.hp;leftDestroyed=left.dead;
                  destroyedDuringOverheat=leftDestroyed;return;
                }
                if(leftDestroyed&&right&&!right.dead){
                  const D=S.coreSpreadLast;
                  spreadShifted=!!(D&&!D.leftAlive&&D.rightAlive&&D.min===0&&D.max>=.49);
                  if(!spreadShifted)return;
                }else return;
              }
              const n=H.nodes.find(q=>!q.dead);
              if(n){
                boss._s4ShieldHit=n;_lastHitX=n.x;_lastHitY=n.y;hitBoss(n.maxhp+1);
                return;
              }
            }
            if(!H.active&&S.shieldThresholdIndex<3){
              const threshold=S.shieldThresholds[S.shieldThresholdIndex];
              _lastHitX=boss.x;_lastHitY=boss.y;hitBoss(Math.max(1,boss.hp-boss.maxhp*threshold+9));return;
            }
          },145);
          window.__s4ProofTimeouts.push(id);
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
          window.__s4Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
            rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'})); rec.stop();
          })};
          rec.start(250); return {w:c.width,h:c.height,mime};
        }"""
    )


def stop_capture(page: Page, webm: Path) -> None:
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(
            """async () => {
              const blob=await window.__s4Capture.stop();
              const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
              a.download='stage4-ai.webm'; document.body.appendChild(a); a.click(); a.remove();
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
            "-vf", "fps=.75,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black",
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
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function(
                "() => typeof beginStage==='function' && typeof s4ChaseTick==='function' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.evaluate(
                """() => {
                  const units=['airfield_tank','armored_tractor','blacksite_interceptor','command_plane',
                    'explosive_barrel','fuel_tanker','gunship_bomber','heavy_attack_jet',
                    'missile_vehicle','rocket_plane','runway_mini_tank','sam_carrier'];
                  const keys=['nsb_olivewarden_intact','mbs6_master'];
                  for(let f=0;f<12;f++) keys.push('s4w_node_teleport_'+f);
                  for(let f=0;f<8;f++){
                    keys.push('s4w_final_chaingun_'+f,'s4w_helper_core_left_'+f,
                      's4w_helper_core_right_'+f,'s4w_helper_dual_'+f,
                      's4w_helper_dual_hot_'+f,'s4w_lightning_mg_round_'+f);
                  }
                  for(const u of units) for(let f=0;f<8;f++) keys.push('s4atk_'+u+'_'+f);
                  keys.forEach(k=>XART._touch(k));
                }"""
            )
            page.wait_for_function(
                "() => XART.rdy('s4atk_airfield_tank_0') && XART.rdy('s4atk_sam_carrier_7') && "
                "XART.rdy('nsb_olivewarden_intact') && XART.rdy('mbs6_master')",
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
                shield_note = ""
                if case["name"] == "Stage4_Storm_Sovereign_ShieldBreak_AI":
                    proof = page.evaluate("() => window.__s4ShieldProof || null")
                    if not proof or not proof.get("allDead") or proof.get("hpAfter") != proof.get("hp0"):
                        raise RuntimeError(f"Stage-4 shield routing failed: {proof}")
                    shield_note = f" shield_nodes=4/4 hull_hp={proof['hpAfter']}/{proof['hp0']}"
                if case["name"] == "Stage4_Storm_Sovereign_Rearm_Chainguns_AI":
                    proof = page.evaluate("() => window.__s4RearmProof || null")
                    if (not proof or proof.get("cycles") != 3 or proof.get("thresholds") != 3
                            or not proof.get("shieldActive") or proof.get("halfSpawn") != 2
                            or not proof.get("leftDestroyed") or not proof.get("leftRouted")
                            or not proof.get("blockedDuringFire")
                            or proof.get("blockedHpAfter") != proof.get("blockedHpBefore")
                            or not proof.get("destroyedDuringOverheat") or not proof.get("spreadShifted")
                            or not all(proof.get("cycleSeen", {}).get(k) for k in ("windup", "fire", "overheat"))
                            or proof.get("leftGeneration") != 2 or proof.get("rightGeneration") != 1
                            or proof.get("bossHpAfterCore") != proof.get("bossHpBeforeCore")
                            or proof.get("coreShots", 0) < 30 or proof.get("coreSpreadShots", 0) < 5
                            or proof.get("coreBlockedHits", 0) < 1 or proof.get("coreVulnerableHits", 0) < 1
                            or len(proof.get("fullSpread", [])) != 10
                            or proof.get("finalGuns") != "off"
                            or abs(proof.get("leftAngle", 0) - 1.57079632679) > .001
                            or abs(proof.get("rightAngle", 0) - 1.57079632679) > .001
                            or proof.get("barrelLeftShots", 0) < 1 or proof.get("barrelRightShots", 0) < 1
                            or not proof.get("deflected") or proof.get("deflectVy", 0) <= 0
                            or proof.get("helperSpan", 0) < 240):
                        raise RuntimeError(f"Stage-4 rearm/side-helper routing failed: {proof}")
                    shield_note = (f" rearm_cycles={proof['cycles']} thresholds={proof['thresholds']}"
                                   f" half_helpers={proof['halfSpawn']} left_gen={proof['leftGeneration']}"
                                   f" right_gen={proof['rightGeneration']} core_shots={proof['coreShots']}"
                                   f" spread_shots={proof['coreSpreadShots']} shifted={proof['spreadShifted']}"
                                   f" dual_reels={proof['barrelLeftShots']}/{proof['barrelRightShots']}"
                                   f" blocked={proof['coreBlockedHits']} vulnerable={proof['coreVulnerableHits']}"
                                   f" deflect_vy={proof['deflectVy']:.2f} span={proof['helperSpan']:.1f}px"
                                   f" hull_hp={proof['hp']:.0f}/{proof['maxhp']:.0f}")
                print(
                    f"{case['name']}: {capture['w']}x{capture['h']} {capture['mime']} "
                    f"gif={gif.stat().st_size} png={png.stat().st_size}{shield_note}"
                )
            page.evaluate("() => { if(window.__s4ProofTimer) clearInterval(window.__s4ProofTimer); }")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))


if __name__ == "__main__":
    main()
