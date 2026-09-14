#!/usr/bin/env python3
"""Live Stage 9 damage and player-audio regression probe."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage9_combat_audio_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


RESET_WARDENS = """() => {
  beginStage(9);setState(GS.PLAY);player.reset();player.invuln=999999;
  player.x=240;player.y=390;snapCamToPlayer();
  stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;
  enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
  boss=null;bossActive=false;bossDefeated=false;
  subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=true;
  spawnSubBoss('riftwardens');subBoss.enter=false;subBoss._s9rift.t=2;
  for(const w of [subBoss._s9rift.left,subBoss._s9rift.right]){w.hp=200;w.maxhp=200;w._fire=999;}
  subBoss.hp=400;subBoss.maxhp=400;window.__probeWardens=subBoss;
  return true;
}"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    report = {}
    page_errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                args=["--disable-gpu", "--no-sandbox", "--autoplay-policy=no-user-gesture-required"]
            )
            page = browser.new_page(viewport={"width": 760, "height": 820})
            page.add_init_script("""(() => {
              window.__mediaPlayCalls=[];
              const original=HTMLMediaElement.prototype.play;
              HTMLMediaElement.prototype.play=function(){
                const row={src:this.src.split('/').pop(),volume:this.volume,loop:this.loop,
                  ready:this.readyState,paused:this.paused,status:'called'};
                window.__mediaPlayCalls.push(row);
                let p;try{p=original.call(this);}catch(e){row.status='throw:'+e.name;throw e;}
                if(p&&p.then)p.then(()=>row.status='playing').catch(e=>row.status='reject:'+e.name);
                return p;
              };
            })()""")
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof s9RiftWardensInit==='function'&&(window.__bofFrames|0)>4", timeout=60_000)
            page.mouse.click(380, 410)
            page.wait_for_timeout(700)

            damage = {}
            for weapon, setup, frames in (
                ("laser", "run.spaceWeapon=0;run.spaceLevels=[5,5,5];spaceLaserFire();", 70),
                ("shadow", "run.spaceWeapon=1;run.spaceLevels=[5,5,5];spaceShadowRelease(1.55);", 100),
                ("volley", "run.spaceWeapon=2;run.spaceLevels=[5,5,5];spaceVolleyFire();", 150),
            ):
                page.evaluate(RESET_WARDENS)
                damage[weapon] = page.evaluate(
                    """([setup,frames]) => {
                      const F=subBoss._s9rift;player.x=F.left.x;player.y=390;
                      const before=F.left.hp;(0,eval)(setup);const trace=[];
                      for(let i=0;i<frames;i++){
                        if(i<30&&(i%5)===0){const q=pBullets.find(b=>!b.dead);trace.push({i,
                          targets:spaceTargets().map(t=>({x:t.x,y:spaceTargetY(t),w:t.w,h:t.h,sub:!!t._spaceSubOwner})),
                          bullet:q?{kind:q.kind,x:q.x,y:q.y,w:q.w,h:q.h}:null});}
                        updatePlay(1/60);
                      }
                      return {before,after:F.left.hp,right:F.right.hp,dead:subBoss&&subBoss.dead,
                        shots:pBullets.length,space:run.spaceMode,enter:subBoss&&subBoss.enter,trace};
                    }""",
                    [setup, frames],
                )

            page.evaluate(RESET_WARDENS)
            kill = page.evaluate("""() => {
              const B=subBoss,F=B._s9rift;
              for(const w of [F.left,F.right]){w.hp=1;w.maxhp=1;}
              B.hp=B.maxhp=2;
              s9RiftWardensHit(B,2,F.left.x,F.left.y);
              const one={left:F.left.disabled,right:F.right.disabled,dead:B.dead};
              s9RiftWardensHit(B,2,F.right.x,F.right.y);
              const both={left:F.left.disabled,right:F.right.disabled,dead:B.dead,hp:B.hp};
              for(let i=0;i<125;i++)updateSubBoss(1/60);
              return {one,both,cleared:subBoss===null,done:subBossDone,active:subBossActive};
            }""")

            page.evaluate("""() => {
              window.__mediaPlayCalls.length=0;
              Snd._last={};
              run.stage=5;run.spaceMode=true;run.spaceLevels=[3,3,3];player.dead=false;
              run.spaceWeapon=0;spaceLaserFire();
              run.spaceWeapon=1;spaceShadowTick(.72,true);spaceShadowTick(.02,false);
              run.spaceWeapon=2;spaceVolleyFire();
              window.__mavOldInput=Input.down;Input.down=function(){return true;};
              special={pilot:'maverick',mavCharging:false,mavCharge:0,mavOrbs:[]};mavCharge(.72);
              window.__mavProbe=setInterval(()=>{mavCharge(1/60);Snd.loopTick(1/60);},16);
            }""")
            page.wait_for_timeout(1200)
            audio = page.evaluate("""() => ({calls:window.__mediaPlayCalls.slice(),
              pools:['spaceLaserCannon','spaceShadowRelease','spaceVolleyLaunch','helixChargeStart','helixCharge'].map(n=>({
                name:n,exists:!!Snd.pools[n],ready:Snd.pools[n]?Snd.pools[n].list.map(a=>a.readyState):[],
                paused:Snd.pools[n]?Snd.pools[n].list.map(a=>a.paused):[]})),
              loop:Snd.loops.helixCharge?{on:Snd.loops.helixCharge.on,paused:Snd.loops.helixCharge.el.paused,
                ready:Snd.loops.helixCharge.el.readyState,volume:Snd.loops.helixCharge.el.volume}:null
            })""")
            page.evaluate("""() => {clearInterval(window.__mavProbe);Input.down=window.__mavOldInput;
              if(Snd.loops.helixCharge)Snd.loopOff('helixCharge');}""")

            page.evaluate(RESET_WARDENS)
            page.wait_for_timeout(100)
            page.locator("#screen").screenshot(path=str(OUT / "stage9_wardens_damage_probe.png"))
            report = {"damage": damage, "kill": kill, "audio": audio, "pageErrors": page_errors}
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert all(v["after"] < v["before"] for v in report["damage"].values()), report["damage"]
    assert report["kill"]["both"]["dead"] and report["kill"]["done"] and not report["kill"]["active"], report["kill"]
    played = {(c["src"], c["loop"]) for c in report["audio"]["calls"] if c["status"] == "playing"}
    assert ("reviewed_laser_cannon.wav", False) in played
    assert ("reviewed_shadow_orb_launch.wav", False) in played
    assert ("nsp_rocket_launch.mp3", False) in played
    assert ("reviewed_maverick_charge_build.wav", False) in played
    assert ("reviewed_maverick_charge_loop.wav", True) in played
    assert report["audio"]["loop"]["on"] and not report["audio"]["loop"]["paused"], report["audio"]["loop"]
    assert not report["pageErrors"], report["pageErrors"]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
