"""Inspect five generated HUD concepts and their controls in real Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64, json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot

OUT=ROOT/'_shots/hud_concepts_1011'
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
errors=[]
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)

port,stop=shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        page=browser.new_page(viewport=dict(width=1280,height=1050))
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
        page.goto(f'http://127.0.0.1:{port}/docs/previews/hud_concepts_1011/index.html')
        page.wait_for_function('window.hudConceptReady===true')
        check('Five selectable generated concepts and five comparison cards',page.locator('#conceptTabs button').count()==5 and page.locator('#gallery .card').count()==5)
        for i in range(5):
            page.locator('#conceptTabs button').nth(i).click()
            name=page.locator('#conceptName').inner_text()
            page.locator('#screen').screenshot(path=str(OUT/f'concept-{i+1}-normal.png'))
            # Browser element screenshots can round a fractional CSS edge up
            # by one pixel. Export the even canvas itself for the final assets.
            raw=page.evaluate('document.querySelector("#screen").toDataURL("image/png")')
            (OUT/f'concept-{i+1}-native.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
            check(name+': actual selector updates the labeled canvas and URL',name in page.locator('#screen').get_attribute('aria-label') and 'concept=' in page.url)
        page.locator('#conceptTabs button').nth(1).click()
        page.select_option('#scenario','low')
        check('Low-stock controls show one life and one missile',page.locator('#livesReadout').inner_text()=='01' and page.locator('#missilesReadout').inner_text()=='01')
        page.locator('#screen').screenshot(path=str(OUT/'concept-2-low.png'))
        page.select_option('#scenario','empty')
        check('Empty stocks stay explicit as zero',page.locator('#livesReadout').inner_text()=='00' and page.locator('#missilesReadout').inner_text()=='00')
        page.locator('#screen').screenshot(path=str(OUT/'concept-2-empty.png'))
        page.select_option('#scenario','normal')
        page.select_option('#background','stage1')
        page.locator('#screen').screenshot(path=str(OUT/'concept-2-ocean.png'))
        check('All counters remain large and every measured field remains in its own strip',page.evaluate('window.__hudConceptChecks.counterSizes.every(q=>q.size>=24)&&window.__hudConceptChecks.placements.every(q=>q.inBanner)'))
        with page.expect_download() as dl:
            page.locator('#save').click()
        download=dl.value
        download.save_as(str(OUT/'download-mockup.png'))
        check('The selected mockup exports as an actual PNG',download.suggested_filename=='bold-cabinet-normal-mockup.png' and (OUT/'download-mockup.png').stat().st_size>10000)
        page.select_option('#background','stage6')
        page.locator('#enlarge').click()
        check('Enlargement control increases the on-screen canvas width',page.locator('#screen').bounding_box()['width']>576)
        page.locator('#screen').screenshot(path=str(OUT/'concept-2-enlarged.png'))
        page.locator('#enlarge').click()
        page.screenshot(path=str(OUT/'review-desktop.png'),full_page=True)
        page.locator('#gallery').screenshot(path=str(OUT/'comparison.png'))
        page.set_viewport_size(dict(width=480,height=900))
        page.wait_for_timeout(50)
        check('Review fits the narrow viewport without horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.screenshot(path=str(OUT/'review-mobile.png'),full_page=True)
        page.set_viewport_size(dict(width=360,height=800))
        check('Review also fits 360px screens',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.emulate_media(reduced_motion='reduce')
        check('Reduced-motion mode disables smooth page scrolling',page.evaluate('getComputedStyle(document.documentElement).scrollBehavior==="auto"'))
        check('No page, console or missing-image errors',not errors)
        browser.close()
except Exception as e:
    errors.append(type(e).__name__+': '+str(e))
    print(errors[-1],flush=True)
finally:
    stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
