from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,hashlib
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=Path(__file__).resolve().parents[1]/'_ART_SOURCES/cinema_story_1021' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Cinema-Rebuild'
D=W/'consistency_1021';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,value):
 checks.append({'name':name,'ok':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
 assert value,name
shots={'hq_regroup':3,'forge_upgrade':3,'hq_alarm':5,'hq_river':6,'launch_generator':4,'power_cell':4}
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof C22!=="undefined"');p.wait_for_function('c22Warm()',polling=50)
  # Export the identity-bearing native assets still used outside C22 plates.
  keys=p.evaluate('''()=>[...new Set(['cole','maverick','freezer'].flatMap(pk=>[campaignIntroPortraitKey(pk),INV20_ART.images[pk]?.key,INV20_ART.images[pk+'_horror']?.key,'comm_'+pk+'_idle',...(pk==='cole'?Object.values(PF20_ART).filter(a=>a&&/cole/.test(a.key||'')).map(a=>a.key):[])]).filter(Boolean))]''')
  for key in keys:
   p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
   data=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}''',key)
   (D/('audit-native-'+key+'.png')).write_bytes(base64.b64decode(data))
  (D/'native-identity-assets.json').write_text(json.dumps(keys,indent=2),encoding='utf-8')
  p.evaluate(shoot.TRAP_RAF)
  for name,stage in shots.items():
   ck(name+' path has current art hash',p.evaluate('n=>C22_ART.images[n].path.includes("?v=")',name))
   data=p.evaluate('''n=>{const a=C22_ART.images[n],im=XART.get(a.key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}''',name)
   decoded=D/(name+'-native-source.png');decoded.write_bytes(base64.b64decode(data))
   ck(name+' actual decoded native pixels match revised art',Image.open(decoded).convert('RGBA').tobytes()==Image.open(W/'shipping'/(name+'.webp')).convert('RGBA').tobytes())
   for pk in ['cole','maverick']:
    p.evaluate('''({name,stage,pk})=>{BOFCinematicDirector.cancel();run.pilot=pk;run.mode='campaign';BOFCinematicDirector.start(stage,()=>{});const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.c22===name);s.t=1.3;s.shown=s.beats[s.i].text.length;window.__consistencyDraws=0;const orig=ctx.drawImage;ctx.drawImage=function(im,...args){if(im===XART.get(C22_ART.images[name].key))window.__consistencyDraws++;return orig.call(this,im,...args);};try{drawCutsceneState(0);}finally{ctx.drawImage=orig;}}''',{'name':name,'stage':stage,'pk':pk})
    ck(pk+' native '+name+' drawImage',p.evaluate('n=>window.__consistencyDraws>0&&C22.last.shot===n',name))
    if pk=='cole':p.screenshot(path=str(D/(name+'-native.png')))
  for t,name in [(28,'report'),(40,'alarm')]:
   p.evaluate('''t=>{BOFCinematicDirector.cancel();setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._sfx={};drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(t,cutsceneViewWidth(),VH,drawVictory._sfx);}''',t)
   p.screenshot(path=str(D/('ending-'+name+'-native.png')))
   ck('native ending '+name+' uses revised plate',p.evaluate('C22.draws.'+('hq_regroup' if name=='report' else 'hq_alarm')+'>0'))
  ck('native opening uses revised regroup / alarm plates',p.evaluate('''()=>{const W=cutsceneViewWidth(),H=VH;ip21Visual({dispatch:'dispatch'},{pilot:'cole'},1,W,H);const a=IP21.last.name;ip21Visual({dispatch:'turn'},{pilot:'cole'},1,W,H);return a==='hq_regroup'&&IP21.last.name==='hq_alarm';}'''))
  ck('Maverick arrival uses identity variant',p.evaluate('campaignIntroPortraitKey("maverick")===C22_ART.images.maverick_standing_pose.key'))
  for kind in ['report','horror','standing']:
   q=p.evaluate('''kind=>{const W=cutsceneViewWidth(),H=VH,name='maverick_'+kind+'_pose',key=C22_ART.images[name].key;BOFCinematicDirector.cancel();INV20.active=false;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0a0e15';ctx.fillRect(0,0,W,H);let calls=0;const old=ctx.drawImage;ctx.drawImage=function(im,...a){if(im===XART.get(key))calls++;return old.call(this,im,...a);};try{if(kind==='standing')ce20Pilot('maverick',W*.5,H*.88,H*.75,0);else inv20Pose('maverick',W*.5,H*.88,H*.75,0,kind==='horror');}finally{ctx.drawImage=old;}return {calls,key};}''',kind)
   ck('Maverick '+kind+' actual native variant draws',q['calls']>0)
   p.screenshot(path=str(D/('maverick-'+kind+'-native.png')))
  ck('no page / console errors',not errors);b.close()
finally:
 stop();(D/'native-report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
print('ALL',len(checks),'CHECKS PASSED',flush=True)
