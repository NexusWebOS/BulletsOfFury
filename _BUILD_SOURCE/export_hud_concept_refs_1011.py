"""Export the real HUD icons/font for Mike's five review-only HUD concepts.

Uses the game's own icon renderer and existing Chromium harness. Never edits
the shipping HUD, atlas, combat state files or source sprites.
"""
from pathlib import Path
import base64, json, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
import shoot

OUT = ROOT / 'docs/previews/hud_concepts_1011'
SCRATCH = ROOT / '_shots/hud_concepts_1011'
OUT.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)
errors = []
port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport=dict(width=1100, height=950))
        page.set_default_timeout(120000)
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text[:800]) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html')
        page.wait_for_function('window.__bofFrames>4')
        page.evaluate(shoot.TRAP_RAF)
        page.evaluate(shoot.SETUP, dict(state='PLAY', stage=1, pilot='cole', invuln=True))
        page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&bmfReady("game")&&fs11ArtReady("cole")}', polling=50)
        page.evaluate('()=>{window.__hudRefs=[{id:"lives",key:"nli_2"},{id:"missiles",key:"nmi_2"},{id:"weapon",key:weaponIconKey(0,1)},{id:"special",key:fs11IconKey("cole")},{id:"lock",key:"retm_0"}];}')
        # Poll the native blit, rather than relying on aliases having XART entries.
        page.wait_for_function('()=>window.__hudRefs.every(q=>{const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d");iconBlit(g,q.key,64,64,100,true);return g.getImageData(0,0,128,128).data.some((v,i)=>i%4===3&&v>0);})', polling=50)
        refs = page.evaluate('()=>window.__hudRefs.map(q=>{const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d");g.imageSmoothingEnabled=false;iconBlit(g,q.key,64,64,104,true);const pixels=g.getImageData(0,0,128,128).data;return {...q,data:c.toDataURL("image/png"),ink:pixels.filter((v,i)=>i%4===3&&v>0).length};})')
        for ref in refs:
            (OUT / (ref['id'] + '.png')).write_bytes(base64.b64decode(ref.pop('data').split(',', 1)[1]))
        font = page.evaluate('()=>({path:BMF_FACES.game+"-alpha.png",map:BMF.game.map,name:"Command Alloy"})')
        shutil.copyfile(ROOT / font['path'], OUT / 'command-alloy.png')
        (OUT / 'command-alloy.json').write_text(json.dumps(font['map']), encoding='utf-8')
        browser.close()
    for source, name in [('cole-enhanced.png', 'gameplay-stage1.png'), ('rebel-voss-fusion.png', 'gameplay-stage6.png')]:
        shutil.copyfile(ROOT / '_shots/signature_specials_1011' / source, OUT / name)
    report = dict(icons=refs, font=dict(name=font['name'], source=font['path']),
                  screenshotSource='_shots/signature_specials_1011',
                  playfieldCrop=[212, 59, 676, 724], errors=errors)
    (OUT / 'references.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (SCRATCH / 'reference-export.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)
finally:
    stop()
sys.exit(1 if errors else 0)
