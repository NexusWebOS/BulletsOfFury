"""Visual proof for fixed weapon categories, form selection and wide menu/map."""
import base64, json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, STEP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots'/'fixed_loadout_menu_0920'
OUT.mkdir(parents=True,exist_ok=True)

def main():
    port,stop=serve(str(ROOT)); errors=[]; result={}
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
            page=browser.new_page(viewport={'width':1920,'height':1080})
            page.on('pageerror',lambda e:errors.append('page '+str(e)))
            page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
            page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
            page.wait_for_function('() => (window.__bofFrames|0)>4',timeout=120000)
            page.evaluate("() => {document.body.classList.add('fs');__bofFit();setState(GS.TITLE);}")
            page.wait_for_timeout(350)
            page.screenshot(path=str(OUT/'menu.png'))
            page.evaluate("() => {run.mode='campaign';run.pilot='freezer';run.stage=4;campaign.unlockedMax=5;openStageSelect(4,{});}")
            page.wait_for_timeout(1600)
            page.screenshot(path=str(OUT/'map.png'))
            page.evaluate(TRAP_RAF)
            page.evaluate("""() => {run.mode='arcade';run.pilot='freezer';run.stage=4;
              run.forge={};run.forgeElems={fire:true,ice:true};
              run.forgeForms={4:{fire:{elem:'fire',lv:1},ice:{elem:'ice',lv:1}}};
              loadoutStart(null);loadoutScr.sel=run.loadout.indexOf(4);}""")
            page.wait_for_function("() => XART.rdy('forge_loadout_0918')",timeout=30000)
            for _ in range(40): page.evaluate(STEP,1)
            load_before=page.evaluate('() => run.loadout.slice()')
            def shot(name):
                page.evaluate(STEP,3)
                uri=page.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                (OUT/(name+'.png')).write_bytes(base64.b64decode(uri.split(',',1)[1]))
            def tap(k):
                page.evaluate('k => BOSSMODE.hold(k,true)',k);page.evaluate(STEP,1)
                page.evaluate('k => BOSSMODE.hold(k,false)',k);page.evaluate(STEP,8)
            shot('loadout_bays')
            tap('s');shot('loadout_forms')
            tap('d');shot('loadout_ice_form')
            tap('s');shot('loadout_forge_form')
            tap('j');shot('loadout_equipped')
            result={'before':load_before,'after':page.evaluate('() => run.loadout.slice()'),
                    'form':page.evaluate('() => run.forge[4]&&run.forge[4].elem'),'errors':errors}
            assert result['before']==result['after'],result
            assert result['form'] in ('fire','ice'),result
            assert not errors,errors
            browser.close()
    finally: stop()
    (OUT/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))

if __name__=='__main__': main()
