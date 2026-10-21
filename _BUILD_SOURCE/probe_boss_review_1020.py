from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';errors=[];checks=[];text=(O/'review.html').read_text();refs=re.findall(r'(?:src|href)="([^"]+)"',text)
missing=[ref for ref in refs if not ref.startswith(('http:','https:','#')) and not (O/ref).resolve().exists()];checks.append({'name':'All local review links and visible image paths exist','passed':not missing,'data':missing})
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1400,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None);p.goto('http://127.0.0.1:8794/_shots/boss_redesign_1020/review.html');p.wait_for_function('document.querySelector("#frame").naturalWidth>0');p.screenshot(path=str(O/'review-desktop.png'))
 p.locator('#toggle').click();p.locator('#bank').select_option('corrupt_break');p.wait_for_function('document.querySelector("#frame").complete&&document.querySelector("#frame").naturalWidth===256');p.locator('#next').click();checks.append({'name':'Real PNG frame selector and single-step controls work','passed':'2 / 33' in p.locator('#position').inner_text()});p.locator('#frame').scroll_into_view_if_needed();p.screenshot(path=str(O/'review-frames.png'))
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'review-narrow.png'));checks.append({'name':'Narrow preview has no horizontal overflow','passed':p.evaluate('document.documentElement.scrollWidth<=innerWidth')});checks.append({'name':'Review has no browser or asset errors','passed':not errors,'data':errors});b.close()
(O/'review-qa.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks));raise SystemExit(not all(q['passed'] for q in checks))
