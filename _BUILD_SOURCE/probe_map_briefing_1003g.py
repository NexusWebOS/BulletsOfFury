"""Native campaign layout, live lettering, and fixed-frame Lizzie checks."""
from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/map_briefing_1003g';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
sys.stdout.reconfigure(encoding='utf-8')
errors=[];report={'checks':{}}
def check(name,value):
 report['checks'][name]=bool(value)
def save_data(name,data): (O/name).write_bytes(base64.b64decode(data.split(',')[1]))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate("()=>{run.mode='campaign';run.pilot='lizzie';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.bonusUnlocked=false;campaign.rivalScattered=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();mapgWarm();}")
  p.wait_for_function("()=>Object.keys(MAP30_ART).every(k=>XART.rdy('map30_'+k))&&cmap2Keys().every(k=>XART.rdy(k))&&XART.rdy('comm_lizzie_talk-wide')&&bmfReady('game')&&bmfReady('dialogue')",timeout=60000)
  p.wait_for_timeout(3700);p.screenshot(path=str(O/'desktop.png'))
  p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  report['geometry']=p.evaluate("()=>({panel:MAPG.rect,bandBottom:CM2_BAND_BOT,points:CM2_ISLANDS.map(s=>({s,...cmap2ToScreen(...Object.values(cmap2World(s)))})),font:_msgFace})")
  check('Map islands stay above theater row',all(q['y']<320 for q in report['geometry']['points'] if q['s']!=9))
  check('Briefing restores shared font state',report['geometry']['font'] is None)
  # Instrument actual game context and shared text renderer, without replacing either renderer.
  p.evaluate("""()=>{window.mapgProbe={blits:[],text:[],key:null};const get=XART.get;XART.get=function(k){const r=get.apply(this,arguments);mapgProbe.key=k;return r;};const original=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...args){if(['mapg_briefing','nss_panel_1','nss_panel_2'].includes(mapgProbe.key))mapgProbe.blits.push({key:mapgProbe.key,args});mapgProbe.key=null;return original(im,...args);};const draw=msgTextLeft;window.msgTextLeft=function(text,x,y,h,...args){mapgProbe.text.push({text,x,y,h,face:_msgFace});return draw(text,x,y,h,...args);};}""")
  p.evaluate("()=>{sselCursor=2;cmap2.focus='map';MAPG.typing=null;}");p.evaluate(sh.STEP,1)
  count0=p.evaluate('()=>MAPG.typing.count');p.wait_for_timeout(280);p.evaluate(sh.STEP,1)
  count1=p.evaluate('()=>MAPG.typing.count');p.screenshot(path=str(O/'typing.png'))
  check('Selecting a new stage starts with zero letters',count0==0)
  check('Letters appear progressively',0<count1<30)
  report['lettering']=p.evaluate("()=>{const copy=mapgCopy(2),r=MAPG.rect;mapgProbe.text=[];MAPG.typing.at=performance.now()-220;mapgBriefingDraw(2);const first=mapgProbe.text[0];mapgProbe.text=[];MAPG.typing.at=performance.now()-8000;mapgBriefingDraw(2);return {first,complete:mapgProbe.text,blits:mapgProbe.blits,copy};}")
  q=report['lettering'];check('Partial title keeps the final centered left edge',q['first']['x']==q['complete'][0]['x'])
  check('Generated blank plate renders, baked panels do not',any(x['key']=='mapg_briefing' for x in q['blits']) and not any(x['key'].startswith('nss_panel') for x in q['blits']))
  # All nine full briefs, including the bonus card, go through the same centered layout.
  report['stages']=p.evaluate("""()=>{const out=[];for(let s=1;s<=9;s++){mapgProbe.text=[];mapgBriefingDraw(s);MAPG.typing.at=performance.now()-10000;mapgBriefingDraw(s);out.push({stage:s,copy:mapgCopy(s),rows:mapgProbe.text,complete:MAPG.typing.count});}return out;}""")
  for s in report['stages']:
   check('Stage '+str(s['stage'])+' copy completes inside frame',s['complete']==len(s['copy']['title'])+len(s['copy']['body']) and all(29<=r['x']<449 and 402<=r['y']<476 for r in s['rows']))
  # Arrow navigation uses the real handler and must reset the timer again.
  p.evaluate("()=>{sselCursor=1;MAPG.typing=null;window.sselCommitted=false;_selFlash=null;sselZoom=null;cmap2.focus='map';Input.injectTap('arrowright');}");p.evaluate(sh.STEP,2)
  check('Real arrow selection resets lettering',p.evaluate("()=>sselCursor!==1&&MAPG.typing.key===String(sselCursor)&&MAPG.typing.count<8"))
  # Portrait pixels outside the mouth must be identical, including ALL four frame sides.
  report['portraits']=p.evaluate("""()=>{const names=['idle','talk-small','talk-medium','talk-wide','talk-o'];const out={};for(const comm of [false,true]){const images=names.map(em=>mapgLizzieCell(em,comm)),a=images[0].getContext('2d').getImageData(0,0,256,256).data;let stable=true,moved=0;for(const im of images.slice(1)){const d=im.getContext('2d').getImageData(0,0,256,256).data;for(let y=0;y<256;y++)for(let x=0;x<256;x++){let diff=false;for(let c=0;c<4;c++)if(a[(y*256+x)*4+c]!==d[(y*256+x)*4+c])diff=true;if(diff){moved++;const mx=comm?256-x:x;if(mx<110||mx>147||y<109||y>145)stable=false;}}}out[comm?'comm':'menu']={stable,moved,size:images.map(im=>[im.width,im.height])};}return out;}""")
  for kind,q in report['portraits'].items():
   check(kind+' frame/body never jump between mouth poses',q['stable'])
   check(kind+' mouth is actually animated',q['moved']>40)
  # Draw current logical keys THROUGH the game context for visual review.
  save_data('lizzie_poses.png',p.evaluate("""()=>{cv.width=1350;cv.height=536;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);['idle','talk-small','talk-medium','talk-wide','talk-o'].forEach((em,i)=>{ctx.drawImage(XART.get('port_cf_lizzie_'+em),i*270,0,256,256);ctx.drawImage(XART.get('comm_lizzie_'+em),i*270,280,256,256);});return cv.toDataURL();}"""))
  p.evaluate("()=>{campaign.bonusUnlocked=false;openStageSelect(4,{});sselBoot=0;sselUnlockCine=null;}")
  p.set_viewport_size({'width':1000,'height':900})
  for i in range(30):p.evaluate(sh.STEP,12);p.wait_for_timeout(12)
  p.evaluate('()=>{MAPG.typing.at=performance.now()-12000;}');p.evaluate(sh.STEP,2);p.screenshot(path=str(O/'compact.png'))
  p.set_viewport_size({'width':480,'height':800})
  for i in range(12):p.evaluate(sh.STEP,12);p.wait_for_timeout(12)
  p.evaluate("()=>{Input.clearTaps();Input.mouse.moved=false;cmap2.focus='map';sselCursor=4;mapgBriefingDraw(4);MAPG.typing.at=performance.now()-12000;}");p.evaluate(sh.STEP,1)
  p.screenshot(path=str(O/'narrow.png'))
  check('Narrow view retains theater progression renderer',p.evaluate("()=>typeof drawTheaterProgression1003g==='function'&&MAPG.rect.x>=0&&MAPG.rect.x+MAPG.rect.w<=VW"))
  check('Narrow view hides duplicate control legend',p.evaluate("()=>getComputedStyle(document.getElementById('hint')).display==='none'"))
  check('Narrow view preserves canvas aspect ratio',p.evaluate("()=>{const r=cv.getBoundingClientRect();return Math.abs(r.width/r.height-cv.width/cv.height)<.005;}"))
  p.set_viewport_size({'width':1920,'height':1080})
  p.evaluate("()=>{campaign.rivalScattered=true;campaign.rivalDefeated=[];openStageSelect(6,{});sselBoot=0;sselUnlockCine=null;Input.injectTap('arrowdown');}");p.evaluate(sh.STEP,2)
  check('Stage X uses its own live briefing',p.evaluate("()=>Rival24.mapFocused&&MAPG.typing.key.startsWith('x-')"))
  p.evaluate("()=>{MAPG.typing.at=performance.now()-12000;}");p.evaluate(sh.STEP,2);p.screenshot(path=str(O/'stage_x.png'))
  p.evaluate("()=>{setState(GS.CUTSCENE);XART.rdy('dlg_rect_0914');}");p.evaluate(sh.STEP,1)
  p.wait_for_function("()=>XART.rdy('dlg_rect_0914')",timeout=30000)
  save_data('lizzie_dialogue.png',p.evaluate("""()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#081322';ctx.fillRect(0,0,cutsceneViewWidth(),VH);dlgBox({who:'LIZZIE',full:'Ready when you are. Pick our next target and let us give them something to remember.',shown:'Ready when you are. Pick our next',forceShown:true});return cv.toDataURL();}"""))
  p.evaluate("()=>{setState(GS.PILOT);pilotIndex=PILOTS.findIndex(p=>p.key==='lizzie');}");p.evaluate(sh.STEP,2)
  p.wait_for_timeout(1200);p.screenshot(path=str(O/'lizzie_pilot.png'))
  check('Pilot menu uses the complete Lizzie frame',p.evaluate("()=>XART.rdy(pilotPortrait('lizzie','idle'))&&XART.get(pilotPortrait('lizzie','idle')).width===256"))
  report['errors']=errors;b.close()
finally:
 stop();(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'checks':report['checks'],'errors':errors},indent=2))
assert not errors,errors
assert all(report['checks'].values()),[k for k,v in report['checks'].items() if not v]
