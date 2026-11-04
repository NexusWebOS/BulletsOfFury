from pathlib import Path
import sys,json,base64,hashlib,time,math
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';O=D/'verification';O.mkdir(exist_ok=True)
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(D));import review_server
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];missing=[];shots=[];failed=[]
def ck(name,passed,data=None):
 checks.append({'name':name,'passed':bool(passed),'data':data});print(('PASS 'if passed else 'FAIL ')+name,flush=True)
def shot(p,name):
 f=O/(name+'.png');f.write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));shots.append(f)
if '--installed' in sys.argv:
 review_server.INJECT='';review_server.OVERLAY=D/'_no_overlay_in_installed_verification'
port,stop=review_server.serve()
if '--ui' in sys.argv:
 try:
  with sync_playwright()as pw:
   br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(90000)
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(f'http://127.0.0.1:{port}/review.html');p.wait_for_function('document.getElementById("status").textContent.startsWith("Ready")')
   ck('Review lists all nine pilots',p.locator('#pilot option').count()==9)
   p.select_option('#pilot','falva');p.select_option('#scene','post-4');p.click('#play')
   p.wait_for_function('document.getElementById("status").textContent.startsWith("Playing")')
   ck('Review starts the selected pilot and scene',p.frame_locator('#game').locator('canvas').count()>0 and p.evaluate('game.contentWindow.run.pilot')=='falva')
   i=p.evaluate('game.contentWindow.BOFCinematicDirector.current.i');p.click('#next')
   ck('Review Next shot advances the native director',p.evaluate('game.contentWindow.BOFCinematicDirector.current.i')==i+1)
   p.select_option('#scene','post-6');p.select_option('#route','right');p.click('#play');p.wait_for_function('game.contentWindow.BOFCinematicDirector.current?.id==="review-post-6"')
   ck('Review route selector keeps the correct surviving threat',p.evaluate('game.contentWindow.BOFCinematicDirector.current.beats.some(b=>b.text.includes("Harrier is heading"))'))
   p.set_viewport_size({'width':390,'height':844});p.wait_for_timeout(300)
   ck('Mobile review has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   p.screenshot(path=str(O/'review-mobile.png'),full_page=True)
   ck('Review has no page errors',not errors,errors);br.close()
 finally:stop()
 (O/'review-controls.json').write_text(json.dumps({'passed':sum(a['passed']for a in checks),'total':len(checks),'checks':checks},indent=2))
 raise SystemExit(not all(a['passed']for a in checks))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append({'text':m.text[:600],'location':m.location})if m.type=='error' or 'draw error' in m.text else None)
  p.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}))
  p.on('response',lambda r:missing.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.BOF_STORY_1103&&window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  ck('Native game loads additive story owner',p.evaluate('typeof S113.script===\'undefined\'&&typeof s113Script===\'function\''))
  matrix=p.evaluate('''()=>S113.casts.flatMap(p=>[2,3,4,5,6].map(n=>{const rows=s113Script(n,p,'left');return{p,n,count:rows.length,valid:rows.every(b=>b.s113&&S113_ART.banks[b.s113]&&typeof b.text==='string')}}))''')
  ck('All nine pilots have all five event-bound stories',len(matrix)==45 and all(a['valid']and a['count']>5 for a in matrix),matrix)
  ck('Both route reports identify the surviving threat',p.evaluate("s113Script(6,'cole','left').some(b=>b.text.includes('Rebel Fighters have reached'))&&s113Script(6,'cole','right').some(b=>b.text.includes('Harrier is heading'))"))
  ck('All playable pilots stay out of the HQ guard assignment',p.evaluate("S113.casts.every(p=>{const a=s113Crew(p);return !a.guards.includes(p)&&a.guards.length===2&&a.flying.length===5})"))
  for pilot in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']:
   p.evaluate('p=>S113.preview("post-2",p)',pilot)
   for name,t in [('cockpit-'+pilot,1),('cable-'+pilot,5.5)]:
    p.evaluate('''o=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.s113===o.name);s.t=o.t;s.shown=s.beats[s.i].text.length;ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw()}''',{'name':name,'t':t})
    ck(pilot+' '+name+' draws native pixels',p.evaluate('S113.last.shot')==name)
    if name.startswith('cable'):shot(p,name)
   p.evaluate('p=>S113.preview("post-4",p)',pilot)
   p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);s.t=1;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.draw()}''')
   shot(p,'headsets-'+pilot)
  for stage in [3,4,5,6]:
   p.evaluate('n=>S113.preview("post-"+n,"cole")',stage)
   rows=p.evaluate('BOFCinematicDirector.current.beats.map((b,i)=>({i,shot:b.s113,actor:b.actor,radar:b.radar,flight:b.flight,battle:b.battle}))')
   for row in rows:
    p.evaluate('''o=>{const s=BOFCinematicDirector.current;s.i=o.i;s.t=o.t;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.draw()}''',{'i':row['i'],'t':4 if row.get('radar')else 2.5})
    ck('post-'+str(stage)+' beat '+str(row['i'])+' renders',p.evaluate('S113.last.shot')==row['shot'])
    if row.get('actor')in ['shock','recover','typing','ecstatic','panic','duck']or row.get('flight')or row.get('battle')or row.get('radar'):shot(p,f'stage-{stage}-beat-{row["i"]:02d}')
   # Exercise automatic wordless playback through the director's actual clock.
   data=p.evaluate('''()=>{const s=BOFCinematicDirector.current;const i=s.beats.findIndex(b=>b.s113Action);s.i=i;s.t=0;s.shown=0;for(let j=0;j<1000&&BOFCinematicDirector.current===s&&s.i===i;j++)BOFCinematicDirector.tick(1/60);return{before:i,after:s.i}}''')
   ck('Stage '+str(stage)+' action beat advances on game time',data['after']>data['before'],data)
  for kind in ['x-harrier','x-rebels']:
   p.evaluate('id=>S113.preview(id,"cole")',kind)
   for t in [0,1.5,3.5,5.5]:
    p.evaluate('t=>{BOFCinematicDirector.current.t=t;BOFCinematicDirector.draw()}',t);shot(p,kind+'-'+str(t))
   ck(kind+' uses native route art',p.evaluate('S113.last.battle')==kind[2:])
  # Real ending-state entry and stats handoff; combat HP is irrelevant to this isolated exit check.
  for stage in [2,4]:
   p.evaluate('''n=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';beginStage(n);run.stage=n;setState(GS.FLYOVER);S113.exit=null;player.x=340;player.y=380;flyoverStartX=340;flyoverStartY=380;for(const k of ['s113_'+(n===2?'dish-exit':'pad-exit'),'s113_landing-cole','s113_fade'])XART.rdy(k)}''',stage)
   p.wait_for_function('n=>["s113_"+(n===2?"dish-exit":"pad-exit"),"s113_landing-cole","s113_fade"].every(k=>XART.rdy(k))',arg=stage)
   for t in [0,2,5,8.5,10.3,11]:
    p.evaluate('t=>{S113.exit??={t:0,wait:0,startX:340,startY:380,cam:0,done:false};S113.exit.t=t;ctx.setTransform(SS,0,0,SS,0,0);drawFlyover(0)}',t);shot(p,f'exit-{stage}-{t}')
   result=p.evaluate('''()=>{S113.exit.t=11.35;drawFlyover(.1);return{state,stats:GS.STAGECLEAR,count:S113.events.filter(e=>e.event==='landed-to-stats'&&e.stage===run.stage).length}}''')
   ck('Stage '+str(stage)+' lands and reaches native stats exactly once',result['state']==result['stats']and result['count']==1,result)
  external=[e for e in errors if isinstance(e,dict)and e.get('location',{}).get('url','').startswith('https://oobdbhdsvcsjnwpvjuyg.supabase.co/auth/v1/signup')]
  runtime=[e for e in errors if e not in external]
  ck('No cutscene page, render or console errors',not runtime,runtime)
  data=p.evaluate('''()=>{BOFCinematicDirector.cancel();const score=run.score;S113.probeDone=0;s113Play('probe-once',[s113Line('COLE','Check.','command-bay')],()=>S113.probeDone++);BOFCinematicDirector.finish();BOFCinematicDirector.finish();return{count:S113.probeDone,scoreBefore:score,scoreAfter:run.score}}''')
  ck('Finish/skip callback runs once and does not award score',data['count']==1 and data['scoreBefore']==data['scoreAfter'],data)
  ck('No missing requested art',not missing,missing)
  br.close()
finally:stop()
# Review contact sheet uses actual browser captures, never a replacement renderer.
selected=[f for f in shots if f.name.startswith('stage-')][:16]
board=Image.new('RGB',(1824,math.ceil(len(selected)/3)*360),'#142333')
draw=ImageDraw.Draw(board)
for i,f in enumerate(selected):
 im=Image.open(f).convert('RGB');im.thumbnail((608,340));x=i%3*608;y=i//3*360;board.paste(im,(x,y));draw.text((x+10,y+340),f.stem,fill='white')
board.save(D/'Cutscene-review.jpg',quality=94)
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'errors':runtime,'externalServiceErrors':external,'missing':missing,'failedRequests':failed,'checks':checks}
(O/('installed-report.json'if '--installed' in sys.argv else 'report.json')).write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k not in ['checks','failedRequests']}));raise SystemExit(not all(c['passed']for c in checks))
