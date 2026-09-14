#!/usr/bin/env python3
"""Live Chromium proof for Freezer and Decker weapon-audio dispatch."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "freezer_decker_audio_0830"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    report: dict = {}
    errors: list[str] = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                args=["--disable-gpu", "--no-sandbox", "--autoplay-policy=no-user-gesture-required"]
            )
            page = browser.new_page(viewport={"width": 760, "height": 820})
            page.add_init_script(
                """(() => {
                  window.__mediaPlayCalls=[];
                  const original=HTMLMediaElement.prototype.play;
                  HTMLMediaElement.prototype.play=function(){
                    const row={src:this.src.split('/').pop(),volume:this.volume,loop:this.loop,
                      ready:this.readyState,status:'called',at:performance.now()};
                    window.__mediaPlayCalls.push(row);
                    let p;try{p=original.call(this);}catch(e){row.status='throw:'+e.name;throw e;}
                    if(p&&p.then)p.then(()=>row.status='playing').catch(e=>row.status='reject:'+e.name);
                    return p;
                  };
                })()"""
            )
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(
                f"http://127.0.0.1:{server.server_address[1]}/index.html",
                wait_until="load",
                timeout=60_000,
            )
            page.wait_for_function(
                "() => typeof flameFire==='function' && typeof freezerOrbCharge==='function' && "
                "typeof dkFire==='function' && typeof Snd!=='undefined' && (window.__bofFrames|0)>4",
                timeout=60_000,
            )
            page.mouse.click(380, 410)
            page.evaluate(
                """() => {
                  beginStage(3);setState(GS.PLAY);player.reset();player.dead=false;player.invuln=99999;
                  player.x=240;player.y=410;snapCamToPlayer();stagePlan=[{t:9999,fn:function(){}}];
                  waveIdx=0;stageTimer=0;enemies.length=0;eBullets.length=0;pBullets.length=0;
                  powerups.length=0;boss=null;bossActive=false;subBoss=null;subBossActive=false;
                  run.spaceMode=false;run.wlevels=[5,5,5,5,5,5];run.wvars=[null,null,null,null,null,null];
                  run.wlevel=5;run.missileLevel=0;
                  Audio.setVol('master',1);Audio.setVol('sfx',1);Snd._last={};
                  Snd.prepare(['iceBreathStart','iceBreathLoop','iceBreathEnd','fireIceChargeStart',
                    'fireIceChargeLoop','fireIceOrbLaunch','dkBuck','dkShell','dkReload']);
                  Snd.loopPrepare('iceBreathLoop');Snd.loopPrepare('fireIceChargeLoop');
                  window.__probeFire=false;window.__probeOldDown=Input.down;
                  Input.down=function(k){return keybind.fire.indexOf(k)>=0?window.__probeFire:window.__probeOldDown(k);};
                }"""
            )
            page.wait_for_function(
                "() => ['iceBreathStart','fireIceOrbLaunch','dkBuck','dkReload'].every(n=>"
                "Snd.pools[n]&&Snd.pools[n].list.some(a=>a.readyState>=3))",
                timeout=20_000,
            )
            page.wait_for_function(
                "() => Snd.loops.iceBreathLoop&&Snd.loops.iceBreathLoop.el.readyState>=3&&"
                "Snd.loops.fireIceChargeLoop&&Snd.loops.fireIceChargeLoop.el.readyState>=3",
                timeout=20_000,
            )

            # Freezer Ice Breath: the actual held-fire input path owns start, loop and release.
            page.evaluate(
                """() => {window.__mediaPlayCalls.length=0;Snd._last={};Snd.loopStopAll();
                  run.pilot='freezer';run.weapon=4;run.wlevel=5;run.wvars[4]='icebreath';
                  player.fireCd=0;window.__probeFire=true;}"""
            )
            page.wait_for_timeout(800)
            page.screenshot(path=str(OUT / "01_freezer_ice_breath.png"))
            ice_live = page.evaluate(
                """() => {const L=Snd.loops.iceBreathLoop;return {calls:window.__mediaPlayCalls.slice(),
                  loop:{on:L.on,paused:L.el.paused,ready:L.el.readyState,currentTime:L.el.currentTime,
                    volume:L.el.volume}};}"""
            )
            page.evaluate("() => {window.__probeFire=false;}")
            page.wait_for_timeout(450)
            ice_live["releaseCalls"] = page.evaluate("() => window.__mediaPlayCalls.slice()")
            report["iceBreath"] = ice_live

            # Freezer Thermoshock: hold past the 45% threshold, then release one charged orb.
            page.evaluate(
                """() => {window.__mediaPlayCalls.length=0;Snd._last={};Snd.loopStopAll();pBullets.length=0;
                  run.pilot='freezer';run.weapon=5;run.wlevel=5;run.wvars[5]='fireice';
                  special={pilot:'freezer',t:15,dur:15};_frzOrb=null;player.fireCd=0;window.__probeFire=true;}"""
            )
            page.wait_for_timeout(1050)
            page.screenshot(path=str(OUT / "02_freezer_thermoshock_charge.png"))
            page.evaluate("() => {window.__probeFire=false;}")
            page.wait_for_timeout(350)
            page.screenshot(path=str(OUT / "03_freezer_thermoshock_release.png"))
            report["thermoshock"] = page.evaluate(
                """() => ({calls:window.__mediaPlayCalls.slice(),
                  projectiles:pBullets.filter(b=>b.kind==='fireball').map(b=>({kind:b.kind,ts:b._ts,tier:b.tier}))})"""
            )

            # Decker: one real blast, one casing event and exactly one delayed reload cue.
            page.evaluate(
                """() => {window.__probeFire=false;window.__mediaPlayCalls.length=0;Snd._last={};
                  special=null;pBullets.length=0;run.pilot='decker';dkGrant();run._dkCd=0;dkFire();}"""
            )
            page.wait_for_timeout(260)
            page.screenshot(path=str(OUT / "04_decker_incendiary_shotgun.png"))
            report["decker"] = page.evaluate(
                """() => ({calls:window.__mediaPlayCalls.slice(),pellets:pBullets.filter(b=>b.kind==='dkshot').length,
                  reloadCue:run._dkReloadCue,reloadCooldown:run._dkCd})"""
            )

            page.evaluate("() => {Input.down=window.__probeOldDown;window.__probeFire=false;Snd.loopStopAll();}")
            report["pageErrors"] = errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    def sources(row):
        return [call["src"] for call in row["calls"]]

    ice_sources = sources(report["iceBreath"])
    ice_release_sources = [c["src"] for c in report["iceBreath"]["releaseCalls"]]
    assert "ice_breath_start.wav" in ice_sources, report["iceBreath"]
    assert "ice_breath_loop.wav" in ice_sources, report["iceBreath"]
    assert "ice_breath_release.wav" in ice_release_sources, report["iceBreath"]
    assert report["iceBreath"]["loop"]["currentTime"] > 0.20, report["iceBreath"]
    assert report["iceBreath"]["loop"]["volume"] >= 0.70, report["iceBreath"]

    thermo_sources = sources(report["thermoshock"])
    assert "ice_breath_start.wav" in thermo_sources, report["thermoshock"]
    assert "nsp_bof2_charge_shot.mp3" in thermo_sources, report["thermoshock"]
    assert "nsp_charge_release.mp3" in thermo_sources, report["thermoshock"]
    assert thermo_sources.count("nsp_charge_release.mp3") == 1, report["thermoshock"]
    assert any(p["ts"] == 1 for p in report["thermoshock"]["projectiles"]), report["thermoshock"]

    decker_sources = sources(report["decker"])
    assert decker_sources.count("reviewed_decker_shotgun.wav") == 1, report["decker"]
    assert decker_sources.count("reviewed_decker_shell_eject.wav") == 1, report["decker"]
    assert decker_sources.count("reviewed_decker_reload.wav") == 1, report["decker"]
    assert report["decker"]["pellets"] == 7, report["decker"]
    assert not errors, errors

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
