"""Real Chromium: dialogue bounds, generated wall frames, elemental damage and pixels."""
from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/feedback_1001';OUT.mkdir(parents=True,exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
errors=[];report={'dialogue':[],'combat':[]}
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL()').split(',')[1]))
def step(p,n=1):
 r=p.evaluate(sh.STEP,n)
 assert r is None,r
 p.wait_for_timeout(30)
SETUP="""st=>{BOFCinematicDirector.cancel();ht27Stop();debugFight=null;diffKey='normal';DIFF=DIFFS.normal;run.mode='arcade';run.pilot='cole';beginStage(st);setState(GS.PLAY);player.reset();player.invuln=9999;story=null;special=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;floaters=[];stageTimer=10;_dmgSrc=null;_dmgBullet=null;player.x=worldWidth()/2;player.y=420;camX=player.x-VW/2;}"""
AUDIT="""()=>{
 const df=dialogueFrameDraw,mb=msgDrawBlock,get=XART.get,di=ctx.drawImage;let active=false,key='',row=null;
 window.feedbackRows=[];
 dialogueFrameDraw=function(who,tint,x,y,w,h){key='';row={who,frame:{x,y,w,h},ports:[]};feedbackRows.push(row);active=true;return df.apply(this,arguments);};
 XART.get=function(k){key=k;return get.call(this,k);};
 ctx.drawImage=function(...a){if(active&&row&&key.startsWith('comm_')&&a.length===5)row.ports.push({key,x:a[1],y:a[2],w:a[3],h:a[4]});key='';return di.apply(this,a);};
 msgDrawBlock=function(o){const r=mb.call(this,o);if(active&&row){row.text={...o,layout:r,widths:r.lines.map(l=>msgMeasure(l,r.H))};active=false;}return r;};
 window.endFeedbackAudit=()=>{dialogueFrameDraw=df;msgDrawBlock=mb;XART.get=get;ctx.drawImage=di;};
}"""
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  p=b.new_page(viewport={'width':1920,'height':1080})
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);step(p)
  # Warm actual authored backgrounds, mouth poses and dialogue font, not substitute images.
  p.evaluate("""()=>{const keys=new Set(['dlg_window']);for(const pilot of PILOTS){for(const e of ['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'])keys.add('comm_'+pilot.key+'_'+e);for(let st=1;st<=9;st++)for(const row of BOFCinematicDirector.script(st,pilot.key)){keys.add(row.bg||'cin_story_lab_empty');const k=BOFCinematicDirector.artFor(row);if(k)keys.add(k);}}window.feedbackKeys=[...keys];bmfReady('dialogue');for(const k of feedbackKeys)XART.rdy(k);}""")
  p.wait_for_function("()=>feedbackKeys.every(k=>XART.rdy(k))&&bmfReady('dialogue')",timeout=120000)
  for width,height in [(1920,1080),(1280,800),(720,900)]:
   p.set_viewport_size({'width':width,'height':height});p.wait_for_timeout(80)
   p.evaluate("()=>{BOFCinematicDirector.preview('post-1','axel');const S=BOFCinematicDirector.current;S.i=Math.max(0,S.beats.findIndex(b=>/filled the uplink/i.test(b.text)));S.shown=999;S.t=4;}");step(p)
   p.evaluate(AUDIT)
   # Every authored mission bridge, all pilots, measured by the actual bitmap renderer.
   for st in range(1,10):
    p.evaluate("""st=>{for(const pilot of PILOTS)for(const row of BOFCinematicDirector.script(st,pilot.key)){const W=cutsceneViewWidth(),pw=Math.min(W*.92,1020);dlgBox({who:row.who,portrait:pilot.key,full:row.text,shown:row.text,forceShown:true,pw,ph:VH*.245,x:(W-pw)/2,y:VH*.70,maxBottom:VH*.94,screenSpace:false});}}""",st)
    p.wait_for_timeout(5)
   audit=p.evaluate("()=>{endFeedbackAudit();return {width:cutsceneViewWidth(),rows:feedbackRows};}")
   bad=[]
   for row in audit['rows']:
    f,t=row['frame'],row['text'];ports=row['ports']
    fits=t['layout']['height']<=t['h']+.01 and all(v<=t['w']+.01 for v in t['widths']) and f['y']+f['h']<=512*.94+.1
    if ports:
     q=ports[0];fits=fits and abs(q['y']+q['h']/2-f['y']-f['h']/2)<=1 and q['x']>=f['x']+18 and q['x']+q['w']<t['x']
    else:fits=False
    if not fits:bad.append(row)
   report['dialogue'].append({'viewport':[width,height],'canvasWidth':audit['width'],'count':len(audit['rows']),'bad':bad})
   step(p);shot(p,f'dialogue_{width}')
   print('Dialogue',width,len(audit['rows']),'bad',len(bad),flush=True)
  # New wall: all eight frames rendered from explicit XART rects at a fixed destination.
  p.set_viewport_size({'width':1920,'height':1080});p.wait_for_timeout(80)
  p.evaluate("()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='yuri';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.bonusUnlocked=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();}")
  p.wait_for_function("()=>Object.keys(MAP30_ART).every(k=>XART.rdy('map30_'+k))",timeout=120000)
  for i in range(10):step(p,20)
  shot(p,'map_overview')
  report['wall']=p.evaluate("""()=>{const get=XART.get,draw=ctx.drawImage,t=cmap2.t;let key='',calls=[];XART.get=function(k){key=k;return get.call(this,k);};ctx.drawImage=function(...a){if(key==='map30_datawall'&&a.length===9)calls.push({source:a.slice(1,5),dest:a.slice(5)});return draw.apply(this,a);};try{for(let i=0;i<8;i++){cmap2.t=(i+.25)/MAP30_DATA.fps;map30DataWall();}}finally{ctx.drawImage=draw;XART.get=get;cmap2.t=t;}const im=XART.get('map30_datawall'),c=document.createElement('canvas');c.width=314;c.height=627;const g=c.getContext('2d'),hashes=[];for(const f of MAP30_DATA.frames){g.clearRect(0,0,c.width,c.height);g.drawImage(im,...f.rect,0,0,314,627);hashes.push(g.getImageData(0,0,314,627).data.reduce((a,b)=>(a*31+b)>>>0,0));}return {size:[im.width,im.height],path:XART._src.map30_datawall,calls,hashes};}""")
  # Native canvas recording of the map, using the real engine clock at 60Hz.
  p.evaluate("""()=>{window.wallChunks=[];window.wallStream=cv.captureStream(30);window.wallRecorder=new MediaRecorder(wallStream,{mimeType:'video/webm;codecs=vp9'});wallRecorder.ondataavailable=e=>wallChunks.push(e.data);wallRecorder.start();window.wallTimer=setInterval(()=>{window.__bofStepNow+=1000/60;loop(window.__bofStepNow);},1000/60);}""")
  p.wait_for_timeout(4500)
  data=p.evaluate("""()=>new Promise(resolve=>{clearInterval(wallTimer);wallRecorder.onstop=()=>{wallStream.getTracks().forEach(t=>t.stop());const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.readAsDataURL(new Blob(wallChunks,{type:'video/webm'}));};wallRecorder.stop();})""")
  (OUT/'data_wall.webm').write_bytes(base64.b64decode(data))
  # Registered enemy hits, not a substituted effect. Freeze only the scene between comparisons.
  p.set_viewport_size({'width':1100,'height':1000});p.wait_for_timeout(80)
  for stage,attack,name in [(2,'ice','ice_vs_fire'),(3,'fire','fire_vs_ice')]:
   p.evaluate(SETUP,stage);step(p)
   r=p.evaluate("""({stage,attack})=>{const e=spawnEnemy(stage===2?'skim':'s3interceptor',worldWidth()/2,200,{});window.testEnemy=e;Object.assign(e,{hp:200,maxhp:200,dead:false,enter:false,x:worldWidth()/2,y:200});e._esh=null;_dmgBullet={kind:attack==='ice'?'iceorb':'flame',_el:attack};return {type:e.type,art:e.art,src:e._enc30};}""",{'stage':stage,'attack':attack})
   for i in range(8):p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.wait_for_timeout(80)
   before=p.evaluate("()=>testEnemy.hp")
   p.evaluate("()=>{hitEnemy(testEnemy,20);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
   shot(p,name)
   r.update(p.evaluate("()=>({hp:testEnemy.hp,color:hitFlashColor(testEnemy),flash:testEnemy.flash,crit:floaters.filter(f=>f.elementCrit).map(f=>({text:f.txt,color:f.color}))})"));r['before']=before;r['name']=name
   report['combat'].append(r);print(name,r,flush=True)
  # Modular Stage 3 boss: inspect actual silhouettes and independently damaged module pool.
  p.evaluate(SETUP,3);step(p)
  p.evaluate("""()=>{spawnBoss('cryospear');bossActive=true;Object.assign(boss,{enter:false,_be:null,_noHit:false,x:worldWidth()/2,y:160});boss._drawY=boss.y;boss._er26.neutralOpening=false;boss._er26.mode='recover';boss._er26.from={x:boss.x,y:boss.y};boss._er26.to={x:boss.x,y:boss.y};mr27Init(boss);XART.rdy('mr27_rime');}""")
  p.wait_for_function("()=>XART.rdy('mr27_rime')",timeout=60000)
  for i in range(5):p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.wait_for_timeout(80)
  report['module']=p.evaluate("""()=>{const part=boss._mr27.parts[0],q=mr27Shape(boss,part.id),hp=part.hp;_lastHitX=q.x;_lastHitY=q.y;_dmgBullet={_el:'fire'};hitBoss(20);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {before:hp,after:part.hp,color:hitFlashColor(boss),floaters:floaters.filter(f=>f.elementCrit).length,cache:[...MR27_CACHE.keys()].filter(k=>k.endsWith('#ff3b30'))};}""")
  shot(p,'modular_critical')
  report['errors']=errors;b.close()
finally:
 stop();(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
assert not errors,errors
assert all(not r['bad'] for r in report['dialogue'])
assert len(set(report['wall']['hashes']))==8
assert len({tuple(r['source']) for r in report['wall']['calls']})==8
assert len({tuple(r['dest']) for r in report['wall']['calls']})==1
assert all(r['before']-r['hp']==30 and r['crit'] for r in report['combat'])
assert report['module']['before']-report['module']['after']==30 and report['module']['cache']
