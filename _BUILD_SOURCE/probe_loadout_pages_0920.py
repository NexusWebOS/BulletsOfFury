"""Real Chromium proof of readable Loadout pages and D-pad form selection."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, STEP, TRAP_RAF


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_shots/loadout_pages_0920"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    port, stop = serve(str(ROOT))
    errors = []
    records = {}
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
                run.stage=4;run.mode='arcade';run.pilot='cole';
                run.forge={};run.forgeElems={fire:true,kinetic:true};
                run.forgeForms={0:{fire:{elem:'fire',lv:1},kinetic:{elem:'kinetic',lv:1}}};
                run._forgeShown=true;loadoutStart(null);
            }""")
            for _ in range(220):
                if page.evaluate("() => XART.rdy('forge_loadout_0918')"):
                    break
                page.wait_for_timeout(35)
            assert page.evaluate("() => XART.rdy('forge_loadout_0918')")
            assert page.evaluate(STEP, 40) is None

            def tap(key):
                page.evaluate("k => BOSSMODE.hold(k,true)", key)
                assert page.evaluate(STEP, 1) is None
                page.evaluate("k => BOSSMODE.hold(k,false)", key)
                assert page.evaluate(STEP, 8) is None

            def capture(name):
                assert page.evaluate(STEP, 4) is None
                uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                (OUT / (name + ".png")).write_bytes(base64.b64decode(uri.split(",", 1)[1]))
                records[name] = page.evaluate("""() => ({state,row:loadoutScr.row,weapon:loadoutScr.catSel,
                    column:loadoutScr.catCol,page:Math.floor(Math.max(0,loadoutScr.catCol-1)/5)+1,
                    rectangles:loadoutScr.catalogRects.length,
                    selected:loadoutScr.catalogRects.filter(x=>x.ri===loadoutScr.catSel&&x.col===loadoutScr.catCol)
                        .map(x=>({name:x.cell.name,elem:x.cell.elem,ok:x.cell.ok,price:x.cell.price})),
                    form:run.forge[0]&&run.forge[0].elem})""")

            tap("s")
            tap("s")
            capture("page1_fire_owned")
            for _ in range(5):
                tap("s")
            capture("page2_kinetic_owned")
            tap("d")
            capture("page2_other_weapon_locked")
            tap("a")
            tap("j")
            capture("equipped_kinetic")
            assert records["page1_fire_owned"]["selected"][0]["elem"] == "fire"
            assert records["page2_kinetic_owned"]["page"] == 2
            assert records["page2_kinetic_owned"]["selected"][0]["elem"] == "kinetic"
            assert not records["page2_other_weapon_locked"]["selected"][0]["ok"]
            assert records["equipped_kinetic"]["form"] == "kinetic"
            assert not errors, errors
            browser.close()
    finally:
        stop()
    (OUT / "results.json").write_text(json.dumps({"records": records, "errors": errors}, indent=2), encoding="utf-8")
    print("PASS D-pad changes weapon/element page, shows owned/locked state, equips Kinetic; no browser errors")


if __name__ == "__main__":
    main()
