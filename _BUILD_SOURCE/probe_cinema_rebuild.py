from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,hashlib
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=Path(__file__).parent/'BOF-Cinema-Rebuild/verification';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,v,detail=None):
 checks.append(dict(name=name,ok=bool(v),detail=detail));print(('PASS ' if v else 'FAIL ')+name,flush=True)
 if not v:raise AssertionError(name)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof C22!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.wait_for_function('c22Warm()',polling=50)
  ck('all authored cinematic art decodes',p.evaluate('c22Keys().every(k=>!!XART.get(k))'))
  data=p.evaluate('''()=>{const out={};for(const pk of CE20.pilots){out[pk]={};for(const stage of [1,2,3,4,5,6])out[pk][stage]=c22Script(stage,pk,'right');}return out;}''')
  (O/'story-scripts.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
  for pk,stages in data.items():
   s3=stages['3'];s4=stages['4'];s5=stages['5'];s6=stages['6'];text=lambda rows:' '.join(r['text'] for r in rows)
   ck(pk+' restored comms and HQ regroup before airbase', 'All squad channels are back' in text(s3) and 'launch-pad generator' in text(s3))
   ck(pk+' power cell restores launch and reveals satellite takeover', 'Launch-pad power restored' in text(s4) and "Earth's entire infrastructure" in text(s4))
   ck(pk+' .50 upgrade precedes alarm and selected-pilot boarding',text(s5).index('.50 caliber')<text(s5).index('RED ALERT') and any(r.get('c22Flight')=='board' and r['who']==pk.upper() for r in s5))
   guard=next(r['text'] for r in s5 if 'Two of you' in r['text']);ck(pk+' player never assigned base defense',pk.upper() not in guard.split('base!')[1].split(', hold HQ')[0])
   ck(pk+' returns to HQ before tracing river sewer',s6[0].get('c22Flight')=='land' and 'underground, by the river' in text(s6))
   ck(pk+' private prototype story remains Cole-only',any(r.get('c22Private') for r in s3)==(pk=='cole'))
  ck('Maverick homing lasers remain a separate circuit','homing lasers stay on their own circuit' in ' '.join(r['text'] for r in data['maverick']['5']))
  ck('intro wordless run is 1.65 seconds',p.evaluate('IP21.beats.find(b=>b.dispatch==="run").duration===1.65'))
  for pk,stage,shot in [('yuri',3,'hq_regroup'),('cole',3,'forge_upgrade'),('yuri',4,'launch_generator'),('cole',5,'hq_alarm'),('decker',5,'hq_hangar'),('yuri',6,'hq_river')]:
   p.evaluate('''({pk,stage,shot})=>{BOFCinematicDirector.cancel();run.pilot=pk;run.mode='campaign';BOFCinematicDirector.start(stage,()=>{});const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.c22===shot);s.t=1.3;s.shown=s.beats[s.i].text.length;drawCutsceneState(0);}''',dict(pk=pk,stage=stage,shot=shot))
   p.screenshot(path=str(O/f'{pk}-{stage}-{shot}.png'));ck('native '+pk+' '+shot+' actually renders',p.evaluate('C22.last.shot')==shot)
  p.evaluate('BOFCinematicDirector.cancel();setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._sfx={};drawVictory._t=62')
  for t,name in [(63,'air_invasion'),(74,'coast_invasion'),(84,'earth_invasion'),(98,'solar')]:
   p.evaluate('t=>{ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(t,cutsceneViewWidth(),VH,drawVictory._sfx);}',t);p.screenshot(path=str(O/f'ending-{name}.png'));ck('native ending uses dimensional '+name,p.evaluate('C22.draws["'+name+'"]>0'))
  for name,a in p.evaluate('C22_ART.banks').items():
   for f in range(a['frames']):p.evaluate('({name,f,fps})=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#172230";ctx.fillRect(0,0,cutsceneViewWidth(),VH);c22Bank(name,f/fps+.001,cutsceneViewWidth()/2,VH*.45,400,true);}',dict(name=name,f=f,fps=a['fps']))
   p.screenshot(path=str(O/f'bank-{name}-last.png'));ck(name+' all native source cells render',p.evaluate('C22.lastBank.f')==a['frames']-1)
  ck('no page / console errors',not errors,errors);br.close()
finally:
 stop();(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
print('ALL',len(checks),'CHECKS PASSED',flush=True)
