"""Chromium pixel proof for the Stage-3 Furious ice beams."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_shots/frost_furious_beams_0920"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    port, stop = serve(str(ROOT))
    errors = []
    checks = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 1100, "height": 1200})
            page.on("pageerror", lambda err: errors.append("page " + str(err)))
            page.on("console", lambda msg: errors.append("console " + msg.text) if msg.type == "error" else None)
            page.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load", timeout=120000)
            page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
            page.evaluate(TRAP_RAF)
            page.evaluate("""() => {
                stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];
                story=null;dlgBox=function(){};run.stage=3;curStage=STAGES[2];
                diffKey='furious';DIFF=DIFFS.furious;player.reset();player.x=120;player.y=610;
                player.invuln=1e9;player.dead=false;subBoss=null;subBossActive=false;
                boss=null;bossActive=false;bossTriggered=true;bossDone=false;
                state=GS.PLAY;stateT=1;spawnBoss('cryospear');
                boss.enter=false;boss.x=worldWidth()/2;boss.y=shipBossStationY(boss);
                boss._drawY=boss.y;boss.fireCd=999;bossActive=true;
                stage3WallLaserAttack(boss,'s3wallcannons',0);
                for(const k of ['nsb_rimewall_intact','frost_furious_beam_0920','l23fx_rime_laser_3'])XART.rdy(k);
            }""")
            ready = False
            for _ in range(220):
                ready = page.evaluate("() => ['nsb_rimewall_intact','frost_furious_beam_0920','l23fx_rime_laser_3'].every(k=>XART.rdy(k))")
                if ready:
                    break
                page.wait_for_timeout(35)
            checks.append((ready, "authored Rime Wall and blue beam plates decode"))

            def step(count):
                page.evaluate("n => {for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}", count)

            def capture(name):
                page.evaluate("() => {shake=0;drawWorld(0);}")
                uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                path = OUT / (name + ".png")
                path.write_bytes(base64.b64decode(uri.split(",", 1)[1]))
                return page.evaluate("""() => ({role:boss._s3boss.role,feint:!!boss._s3boss.furyFeint,
                    beam:boss._l23Beam&&{released:boss._l23Beam.released,width:boss._l23Beam.width,
                    slots:boss._l23Beam.slots,simon:boss._l23Beam._furySimon},
                    plate:XART.rdy('frost_furious_beam_0920'),state})""")

            step(70)
            warning = capture("rime_furious_simon_warning")
            step(47)
            release = capture("rime_furious_giant_blue_beam")
            checks.append((warning["role"] == "wall" and warning["feint"], "Furious Rime Wall keeps Simon-Says FOV warning"))
            checks.append((release["beam"] and release["beam"]["released"] and release["beam"]["simon"] and release["beam"]["width"] == 62 and len(release["beam"]["slots"]) == 1, "one enlarged blue beam follows the selected cannon"))
            page.evaluate("""() => {
                boss=null;bossActive=false;subBoss=null;subBossActive=false;
                subBossTriggered=true;subBossDone=false;spawnSubBoss('frostcruiser');
                subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=shipBossStationY(subBoss);
                subBoss._drawY=subBoss.y;subBossActive=true;
                subBoss._jc.state='beamSweep';subBoss._jc.beamActive=true;
                subBoss._jc.beamAng=0;subBoss._jc.charge=1;
            }""")
            for _ in range(220):
                if page.evaluate("() => XART.rdy('nsb_frost_cruiser')"):
                    break
                page.wait_for_timeout(35)
            mini = page.evaluate("""() => {
                shake=0;drawWorld(0);
                return {ship:subBoss._ship,beam:subBoss._jc.beamActive,
                    plate:XART.rdy('frost_furious_beam_0920'),
                    hull:XART.rdy('nsb_frost_cruiser')};
            }""")
            uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (OUT / "frost_cruiser_furious_blue_sweep.png").write_bytes(base64.b64decode(uri.split(",", 1)[1]))
            checks.append((mini["ship"] == "frostcruiser" and mini["beam"] and mini["plate"] and mini["hull"], "Furious Frost Cruiser uses decoded hull and blue plate at its nose"))
            checks.append((not errors, "no Chromium page or console errors"))
            browser.close()
    finally:
        stop()
    result = {"checks": [{"pass": bool(value), "label": label} for value, label in checks],
              "warning": warning, "release": release, "mini": mini, "errors": errors}
    (OUT / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    for value, label in checks:
        print(("ok " if value else "FAIL ") + label, flush=True)
    if not all(value for value, _ in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
