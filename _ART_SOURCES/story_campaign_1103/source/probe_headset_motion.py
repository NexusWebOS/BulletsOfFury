from pathlib import Path
import sys,json,base64,hashlib
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';V=D/'verification/revision8';V.mkdir(exist_ok=True)
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(D));import review_server
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
if '--installed'in sys.argv:review_server.INJECT='';review_server.OVERLAY=D/'_no_overlay'
checks=[];errors=[];missing=[]
def ck(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else 'FAIL ')+name,flush=True)
port,stop=review_server.serve()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(e.stack));p.on('response',lambda r:missing.append(r.url)if r.status>=400 else None)
  if '--controls'in sys.argv:
   p.goto(f'http://127.0.0.1:{port}/review.html');p.wait_for_function('document.getElementById("game").contentWindow.BOF_STORY_1103?.revision===8')
   p.select_option('#pilot','falva');p.select_option('#motion','angry');p.click('#headsets')
   p.wait_for_function('document.getElementById("status").textContent.includes("Pilot animation")')
   ck('Review pilot and emotion controls select Falva angry frames',p.evaluate('game.contentWindow.BOFCinematicDirector.current.beats[0].portraitClip==="angry"&&game.contentWindow.BOF_STORY_1103.casts.includes("falva")&&game.contentWindow.BOF_STORY_1103.last.pilot==="falva"'))
   prior=p.evaluate('game.contentWindow.BOF_STORY_1103.last.scrollFrame');p.wait_for_function('f=>game.contentWindow.BOF_STORY_1103.last.scrollFrame!==f',arg=prior)
   ck('Native elapsed-time playback advances the scrolling background',True)
   p.select_option('#motion','all');p.click('#headsets');p.wait_for_function('game.contentWindow.BOFCinematicDirector.current.beats.length===13')
   ck('All animations queues every talking, turn and emotional clip',p.evaluate('game.contentWindow.BOFCinematicDirector.current.beats.length===13'))
   p.evaluate('game.contentWindow.BOFCinematicDirector.current.t=4.99');p.wait_for_function('game.contentWindow.BOFCinematicDirector.current.i===1')
   ck('Animation preview advances automatically after clip duration',p.evaluate('game.contentWindow.BOFCinematicDirector.current.beats[1].portraitClip==="turn-left"'))
   p.click('#next');p.wait_for_function('game.contentWindow.BOFCinematicDirector.current.i===2')
   ck('Next shot advances to the next authored turn',p.evaluate('game.contentWindow.BOFCinematicDirector.current.beats[2].portraitClip==="turn-right"'))
   p.set_viewport_size({'width':640,'height':900});ck('Review controls fit a narrow display',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   ck('Review controls have no script errors or missing assets',not errors and not missing,{'errors':errors,'missing':missing})
   br.close();(V/'review-controls.json').write_text(json.dumps({'passed':sum(c['passed']for c in checks),'total':len(checks),'checks':checks},indent=2));raise SystemExit(not all(c['passed']for c in checks))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.BOF_STORY_1103&&window.__bofFrames>4')
  # BOF advances its lazy image queue inside the native RAF loop. Warm all
  # diagnostic scene assets before freezing time for exact pixel reads.
  p.evaluate('''()=>{const saved=run.pilot,keys=new Set();for(const pilot of S113.casts){run.pilot=pilot;for(const key of s113Keys(s113Script(4,pilot)))keys.add(key);keys.add('s113_headset-'+pilot);keys.add('s113_headset-panel-'+pilot);keys.add('s113_comic-scroll-'+pilot);}run.pilot=saved;window.__motionProbeKeys=[...keys];for(const key of keys)XART.rdy(key)}''')
  p.wait_for_function('window.__motionProbeKeys.every(k=>XART.rdy(k))',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.nativeCapture=()=>{const c=document.createElement('canvas');c.width=912;c.height=512;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(cv,0,0,912,512);return c};window.pixelProbe=()=>{const a=nativeCapture().getContext('2d').getImageData(506,26,384,366).data;let h=2166136261;for(let i=0;i<a.length;i++)h=Math.imul(h^a[i],16777619);return h>>>0}}''')
  ck('Current pixel divider and scrolling-panel revision loaded',p.evaluate('S113.revision===8&&S113_ART.headsetMotion.poses.length===24&&S113_ART.comicScroll.phases===24'))
  for pilot in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']:
   p.evaluate('p=>S113.previewHeadsets(p,"all")',pilot)
   p.evaluate('p=>XART.rdy("s113_headset-"+p)',pilot);p.wait_for_function('p=>XART.rdy("s113_headset-"+p)',arg=pilot)
   scroll=p.evaluate('''pilot=>{const s=BOFCinematicDirector.current,b=s.beats[0],a=S113_ART.banks['comic-scroll-'+pilot],c=document.createElement('canvas');c.width=912;c.height=392;const g=c.getContext('2d'),rows=[];g.imageSmoothingEnabled=false;ctx.imageSmoothingEnabled=false;for(let f=0;f<S113_ART.comicScroll.phases;f++){s.age=(f+.01)/S113_ART.comicScroll.fps;s113Visual(b,.5);const rendered=nativeCapture().getContext('2d').getImageData(0,0,912,392).data;g.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,a.w,a.h);const expected=g.getImageData(0,0,912,392).data;let wrong=0;for(let y=0;y<388;y++)for(const x of[4,908]){const i=(y*912+x)*4;for(let k=0;k<3;k++)if(rendered[i+k]!==expected[i+k])wrong++;}rows.push({frame:f,selected:S113.last.scrollFrame,wrong,left:S113.last.leftColor,right:S113.last.rightColor});}s.age=.75;s113Visual(b,.6);const prior=S113.last.scrollFrame;s113Visual(b,0);return{rows,continuous:prior===S113.last.scrollFrame}}''',pilot)
   ck(pilot+' both scrolling fields display all 24 shaded color phases correctly',all(a['frame']==a['selected']and a['wrong']==0 for a in scroll['rows']),scroll['rows'])
   ck(pilot+' background scroll stays continuous between dialogue beats',scroll['continuous'])
   if pilot=='cole':
    p.evaluate('S113.preview("post-4","cole")')
    for phase in range(24):
     p.evaluate('''f=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);s.t=.5+f/S113_ART.comicScroll.fps;s.age=(f+.01)/S113_ART.comicScroll.fps;s.shown=40;BOFCinematicDirector.draw()}''',phase)
     (V/('scroll-'+str(phase).zfill(2)+'.png')).write_bytes(base64.b64decode(p.evaluate('nativeCapture().toDataURL().split(",")[1]')))
    p.evaluate('p=>S113.previewHeadsets(p,"all")',pilot)
   frames=p.evaluate('''pilot=>{const slots=[['front-talk',0],['front-talk',.1],['front-talk',.2],['front-talk',.4],['left-talk',0],['left-talk',.13],['left-profile-talk',0],['left-profile-talk',.13],['right-talk',0],['right-talk',.13],['right-profile-talk',0],['right-profile-talk',.13],...['happy','sad','angry','scared','surprised','determined'].flatMap(n=>[[n,0],[n,.18]])];const a=S113_ART.banks['headset-'+pilot],image=XART.get(a.key),c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const rows=[];for(let f=0;f<24;f++){const [clip,t]=slots[f],b={who:pilot.toUpperCase(),text:'Preview',s113:'comic-backdrop',comic:true,portraitClip:clip};s113Viewport();s113Visual(b,t);const rendered=nativeCapture().getContext('2d').getImageData(506,26,384,366).data;g.clearRect(0,0,128,128);g.drawImage(image,f%4*128,Math.floor(f/4)*128,128,128,0,0,128,128);const src=g.getImageData(0,0,128,128).data;let compared=0,wrong=0;for(let y=8;y<116;y++)for(let x=8;x<120;x++){let q=(y*128+x)*4;if(!src[q+3])continue;const j=(y*3*384+x*3)*4;compared++;if(rendered[j]!==src[q]||rendered[j+1]!==src[q+1]||rendered[j+2]!==src[q+2])wrong++;}rows.push({frame:f,selected:S113.last.rightFrame,compared,wrong,hash:pixelProbe()});}return rows}''',pilot)
   ck(pilot+' all 24 frames render exact authored native pixels',all(a['frame']==a['selected']and a['compared']>3000 and a['wrong']==0 for a in frames),frames)
   ck(pilot+' six emotional displays remain visually distinct',len({frames[f]['hash']for f in [12,14,16,18,20,22]})==6)
   turn=p.evaluate('''pilot=>[0,.15,.3,.45,.6].map(t=>{s113Visual({who:pilot.toUpperCase(),text:'Turn',s113:'comic-backdrop',comic:true,portraitClip:'turn-right'},t);return{frame:S113.last.rightFrame,hash:pixelProbe()}})''',pilot)
   ck(pilot+' turn crosses left profile, left quarter, front, right quarter, right profile',[r['frame']for r in turn]==[6,4,0,8,10]and len({r['hash']for r in turn})==5,turn)
   data=p.evaluate('''pilot=>{const b=s113Script(4,pilot).find(b=>b.comic&&b.who===pilot.toUpperCase()&&!b.portraitEmotion),s=BOFCinematicDirector.current;s.shown=0;s113Visual(b,.45);const a={...S113.last},ha=pixelProbe();s113Visual(b,.6);const hb=pixelProbe();s.shown=b.text.length;s113Visual(b,.6);return{a,b:{...S113.last},mouthChanges:ha!==hb}}''',pilot)
   ck(pilot+' only active speaker talks and mouth stops after text completes',data['a']['speaker']=='right'and data['a']['leftFrame']==8 and data['a']['rightFrame']in [1,2,3]and data['b']['rightFrame']==0 and not data['b']['talking']and data['mouthChanges'],data)
   # Save actual native game renders of the six emotion variants.
   for emotion in ['happy','sad','angry','scared','surprised','determined']:
    p.evaluate('''e=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.portraitClip===e);s.t=.18;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.draw()}''',emotion)
    (V/(pilot+'-'+emotion+'.png')).write_bytes(base64.b64decode(p.evaluate('nativeCapture().toDataURL().split(",")[1]')))
  p.evaluate('S113.preview("post-4","cole")')
  for phase in range(24):
   p.evaluate('''f=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.comic);s.t=.5+f/S113_ART.comicScroll.fps;s.age=(f+.01)/S113_ART.comicScroll.fps;s.shown=40;BOFCinematicDirector.draw()}''',phase)
   (V/('scroll-'+str(phase).zfill(2)+'.png')).write_bytes(base64.b64decode(p.evaluate('nativeCapture().toDataURL().split(",")[1]')))
  ck('No page or rendering exceptions',not errors,errors);ck('No missing frames or scene assets',not missing,missing);br.close()
finally:stop()
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'errors':errors,'missing':missing,'checks':checks}
(V/('motion-installed-report.json'if '--installed'in sys.argv else 'motion-report.json')).write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='checks'}));raise SystemExit(not all(c['passed']for c in checks))
