"""Inspect Stage-clear score/sign-off/password/Continue at common display shapes."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_shots/stageclear_separation_0920"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    port, stop = serve(str(ROOT))
    errors = []
    records = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.on("pageerror", lambda err: errors.append("page " + str(err)))
            page.on("console", lambda msg: errors.append("console " + msg.text) if msg.type == "error" else None)
            page.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load", timeout=120000)
            page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
            page.evaluate(TRAP_RAF)
            page.evaluate("() => XART.rdy('statpanel_full_0916')")
            for _ in range(220):
                if page.evaluate("() => XART.rdy('statpanel_full_0916')"):
                    break
                page.wait_for_timeout(35)
            for name, width, height, stage in [
                ("wide_stage1", 1920, 1080, 1),
                ("square_stage5", 1024, 1024, 5),
                ("portrait_stage9", 900, 1600, 9),
            ]:
                page.set_viewport_size({"width": width, "height": height})
                page.evaluate("""(stage) => {
                    run.stage=stage;curStage=STAGES[stage-1];run.pilot='cole';run.score=41250;
                    run._fpLevel=null;run._fpLevelDone=false;achToasts=[];
                    stageStats.kills=137;stageStats.spawned=152;stageStats.shots=2841;
                    stageStats.hits=1794;stageStats.missiles=46;stageStats.mslHits=39;
                    stageStats.dmgDealt=98420;stageStats.deaths=1;stageStats.livesStart=5;
                    stageStats.scoreStart=0;stageStats.spShots=12;stageStats.spHits=11;
                    stageStats.spDmg=15600;stageTimer=158.2;
                    drawStageClear._init=false;drawStageClear._res=null;
                    setState(GS.STAGECLEAR);
                    achToastPush({title:'STAGE CLEAR',points:200});
                }""", stage)
                page.evaluate("""() => {
                    for(let i=0;i<760;i++){
                        stateT+=1/60;ctx.setTransform(SS,0,0,SS,0,0);
                        drawStageClear(1/60);achToastTick(1/60);
                    }
                }""")
                meta = page.evaluate("""() => {
                    const P=scPanelRect(), S=SC_SLOTS_FULL;
                    const box=f=>({left:P[0]+P[2]*f[0],top:P[1]+P[3]*f[1],
                        right:P[0]+P[2]*(f[0]+f[2]),bottom:P[1]+P[3]*(f[1]+f[3])});
                    return {canvas:[cv.width,cv.height],window:[innerWidth,innerHeight],
                        panel:P,score:box(S.score),signoff:box(S.signoff),footer:box(S.footer),
                        conversion:run._fpLevel,toastCount:achToasts.length,
                        toastTime:achToasts[0]&&achToasts[0].t,
                        password:drawStageClear._pwY,continue:drawStageClear._pfY,
                        stamp:drawStageClear._stamp,typed:drawStageClear._pwChars,
                        ready:drawStageClear._stamp>=1 && (!drawStageClear._res.pw || drawStageClear._pwChars>=drawStageClear._res.pw.length)};
                }""")
                uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                (OUT / (name + ".png")).write_bytes(base64.b64decode(uri.split(",", 1)[1]))
                records.append({"name": name, **meta})
                print(name, {k: meta[k] for k in ["canvas", "conversion", "toastCount", "toastTime", "password", "continue", "ready"]}, flush=True)
            browser.close()
    finally:
        stop()
    (OUT / "results.json").write_text(json.dumps({"records": records, "errors": errors}, indent=2), encoding="utf-8")
    assert not errors, errors
    assert all(r["ready"] and r["toastCount"] > 0 and r["toastTime"] == 0 for r in records)
    assert all(r["score"]["bottom"] < r["signoff"]["top"] < r["signoff"]["bottom"] < r["continue"] < r["password"] for r in records)


if __name__ == "__main__":
    main()
