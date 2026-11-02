"""Verify all twelve current local guide clips in real Chromium, with seek/play."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage1_followup_1031';checks=[];errors=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print('PASS'if passed else'FAIL',name,flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':980})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage1-physical-1031#enemy=stage1-s1boatpatrol',wait_until='networkidle',timeout=120000)
  p.wait_for_function('data?.items?.length===163')
  ck('Complete163-card inventory retained',p.evaluate('data.items.length===163'))
  ck('Current-pass banner and original archive are identified',p.get_by_text('October31 weapon alignment:',exact=False).count()>0 and 'remains an archive'in p.locator('body').inner_text())
  receipt=json.loads((W/'guide-update.json').read_text());updates={q['id']:q for q in receipt['cards']}
  for id,q in updates.items():
   p.evaluate('id=>select(id,false)',id);p.wait_for_function('v.readyState>=2&&v.duration>0',timeout=30000)
   meta=p.evaluate('()=>({url:v.currentSrc,duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error?.message})')
   ck(id+' loads current MP4',('/current/stage1-physical-'+q['type']+'.mp4')in meta['url']and abs(meta['duration']-q['duration'])<.2 and meta['width']==1280 and not meta['error'],meta)
   p.evaluate('()=>{v.currentTime=v.duration*.55;}');p.wait_for_function('!v.seeking&&v.readyState>=2',timeout=30000)
   before=p.evaluate('v.currentTime');p.evaluate('v.play()');p.wait_for_timeout(450);after=p.evaluate('v.currentTime');p.evaluate('v.pause()')
   ck(id+' seeks and plays with audio track',after>before+.2 and p.evaluate('v.webkitAudioDecodedByteCount>0'),dict(before=before,after=after))
   if id in ['stage1-s1boatpatrol','stage1-s1tanklight','stage1-modturret-2']:p.screenshot(path=str(W/('guide-'+q['type']+'.png')))
  old=json.loads((R/'_shots/stage1_amplify_1031/guide-manifest-current.json').read_text(encoding='utf-8'))
  live=p.evaluate('data.items');ck('Other151 cards preserve original clip names',all(next(i for i in live if i['id']==o['id'])['video'].split('/')[-1]==o['video'].split('/')[-1]for o in old['items']if o['id']not in updates))
  ck('No page,console or asset errors',not errors,errors);b.close()
finally:(W/'guide-checks.json').write_text(json.dumps(checks,indent=2))
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
