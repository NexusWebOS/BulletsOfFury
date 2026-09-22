"""Campaign slot and autosave round-trip for discovered/selected Forge forms."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/forge_campaign_save_0920'
OUT.mkdir(parents=True, exist_ok=True)


def main():
    port, stop = serve(str(ROOT))
    errors, records = [], {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
            context = browser.new_context()
            page = context.new_page()
            page.on('pageerror', lambda e: errors.append('page ' + str(e)))
            page.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
            url = f'http://127.0.0.1:{port}/index.html'

            def boot():
                page.goto(url, wait_until='load', timeout=120000)
                page.wait_for_function('() => (window.__bofFrames|0)>4', timeout=120000)
                page.evaluate(TRAP_RAF)

            boot()
            assert page.evaluate(SETUP, {'state':'PLAY','stage':2,'pilot':'cole','invuln':True})['ok']
            records['write'] = page.evaluate("""() => {
                run.mode='campaign';run.pilot='cole';run.stage=2;run.weapon=0;
                run.forgeElems={kinetic:1,fire:1};
                run.forgeForms={0:{kinetic:{elem:'kinetic',lv:2},fire:{elem:'fire',lv:1}},
                  4:{fire:{elem:'fire',lv:2}},5:{kinetic:{elem:'kinetic',lv:1}}};
                run.forge={0:run.forgeForms[0].kinetic,4:run.forgeForms[4].fire};
                run.loadout=[0,1,2,3,4,5];run.wvars=Array.isArray(run.wvars)?run.wvars:WEAPONS.map(()=>null);run.wvars[4]='icebreath';
                run.infusion=null;forgeApply();
                const ok=campWriteSlot(0),snap=campReadSlot(0);
                return {ok,slot:campSlotUsed(0),elements:Object.keys(snap.forgeElems),
                  selected:snap.forge[0],stored:snap.forgeForms[0],variant:snap.wvars[4]};
            }""")
            assert records['write']['ok'] and records['write']['slot']
            assert records['write']['selected']['elem'] == 'kinetic'
            assert sorted(records['write']['elements']) == ['fire','kinetic']

            boot()
            records['slot_load'] = page.evaluate("""() => {
                const ok=campApply(campReadSlot(0));run.infusion=null;forgeApply();
                return {ok,stage:run.stage,mode:run.mode,elements:Object.keys(run.forgeElems),
                  selected:run.forge[0],stored:run.forgeForms[0],infusion:run.infusion,
                  variant:run.wvars[4],loadout:run.loadout};
            }""")
            assert records['slot_load']['ok'] and records['slot_load']['mode'] == 'campaign'
            assert records['slot_load']['selected']['lv'] == 2
            assert sorted(records['slot_load']['stored']) == ['fire','kinetic']
            assert records['slot_load']['infusion']['elem'] == 'kinetic'
            assert records['slot_load']['variant'] == 'icebreath'

            records['auto_write'] = page.evaluate("""() => {
                campaign.unlockedMax=3;const ok=campAutoAfterClear(2,3,'A'),snap=campReadAuto();
                return {ok,stage:snap&&snap.stage,mode:snap&&snap.mode,
                  elements:snap&&Object.keys(snap.forgeElems),selected:snap&&snap.forge[0]};
            }""")
            assert records['auto_write']['ok'] and records['auto_write']['stage'] == 3
            boot()
            records['auto_load'] = page.evaluate("""() => {
                const ok=campApply(campReadAuto());run.infusion=null;forgeApply();
                return {ok,stage:run.stage,unlocked:campaign.unlockedMax,
                  elements:Object.keys(run.forgeElems),selected:run.forge[0],infusion:run.infusion};
            }""")
            assert records['auto_load']['ok'] and records['auto_load']['stage'] == 3
            assert records['auto_load']['selected']['elem'] == 'kinetic'
            assert records['auto_load']['infusion']['elem'] == 'kinetic'
            records['stage_entry'] = page.evaluate("""() => {
                run.infusion=null;beginStage(3);
                return {stage:run.stage,elements:Object.keys(run.forgeElems),
                  selected:run.forge[0],infusion:run.infusion,variant:run.wvars[4]};
            }""")
            assert records['stage_entry']['infusion']['elem'] == 'kinetic'
            assert records['stage_entry']['variant'] == 'icebreath'
            assert not errors, errors
            context.close()
            browser.close()
    finally:
        stop()
    (OUT / 'results.json').write_text(json.dumps({'records':records,'errors':errors}, indent=2), encoding='utf-8')
    print('PASS campaign slot/autosave round-trips preserve elements, forms, loadout and infusion; no browser errors')


if __name__ == '__main__':
    main()
