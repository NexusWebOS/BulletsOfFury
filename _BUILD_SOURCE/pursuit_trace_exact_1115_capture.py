from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import json,sys,base64,io,hashlib,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/pursuit_trace_exact_1115';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];dialogues=[];allFrames=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL',name,str(data)[:1400],flush=True)
def step(p,n=4):
 e=p.evaluate(shoot.STEP,n)
 if e:raise RuntimeError(e)
 p.wait_for_timeout(1)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?pursuit-card-exact-trace=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 # The final and legacy row providers must all use the current squad name.
 samples=p.evaluate("""()=>{const out=[];run.mode='campaign';for(const d of ['normal','hard','furious'])for(const pilot of PILOTS){run.pilot=pilot.key;diffKey=d;for(const defeated of (d==='furious'?['harrier','rebels','storm']:['harrier','rebels'])){run._stage6FateDefeat={defeated,difficulty:d};for(const side of ['left','right']){const groups=[['post6',c16Rows('post-6',pilot.key,side)],['native-route',BOFCinematicDirector.routeScript(side,pilot.key)],['fallback-post6',BOFCinematicDirector.script(6,pilot.key,side)],['bridge',br1110Post6(pilot.key,side)]];for(const [source,rows]of groups)for(const row of rows)if(row.text)out.push({source,d,pilot:pilot.key,defeated,side,text:row.text});}for(const key of [undefined,'voss','nyx','rook','kaia','jace'])for(const row of BOFCinematicDirector.rebelScript(pilot.key,key))if(row.text)out.push({source:'rider-contact',d,pilot:pilot.key,key:key||'squad',text:row.text});}}return out;}""")
 dialogues=samples;legacy=[v for v in samples if re.search(r'\brebels?\b',v['text'],re.I)]
 ck('all nine pilots and three difficulties use Rough Riders across current/fallback dialogue',not legacy,{'sampledLines':len(samples),'stale':legacy[:12]})
 q=p.evaluate("()=>({name:FATE15_NAMES.rebels,rebelReport:fate15SkyReport(fate15Outcome('rebels','hard')),harrierReport:fate15SkyReport(fate15Outcome('harrier','hard')),award:achievementDefinition('road_not_taken').desc,ids:[...REBEL_KEYS].sort(),storm:fate15Outcome('storm','furious'),rebels:fate15Outcome('rebels','furious')})")
 ck('current squad name and plural reports',q['name']=='Rough Riders'and q['rebelReport'].startswith('The Rough Riders are down.')and'The Rough Riders are still heading'in q['harrierReport'],q)
 ck('achievement calls the squad Rough Riders',q['award']=='Defeated the Rough Riders on Furious Difficulty',q['award'])
 ck('all five pilot and saved encounter identifiers stay stable',q['ids']==sorted(['voss','nyx','rook','kaia','jace'])and q['storm']['target']=='rebels'and q['rebels']['target']=='harrier',q['ids'])
 p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 for diff in ['hard','furious']:
  p.evaluate("d=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'warhive',pilot:'cole',diff:d,mode:'campaign',fire:false});BOFCinematicDirector.cancel();story=null;AP10_X.intro=null;s6Opening=null;fb2Talk=null;CA111.active=null;CA111.completed=new Set(['pair-top','pair-bottom','nuclear','laser']);boss=null;bossActive=false;bossDefeated=false;debugFight=null;stagePlan=[];spawnClock=9999;stageTimer=80;run._mission29OpeningDone=true;s6WingInit();s6Wing.fakeDone=true;s6Wing._fb2Talked=true;s6Wing.beats=3;s6Wing.all=true;s6Wing.postMiniT=99;s6Wing.supplyIndex=3;s6Wing.choice=true;setState(GS.PLAY);Input.clearTaps();}",diff)
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&city16Warm()&&fate15Warm();}',polling=50)
  for i in range(600):
   step(p,6)
   if p.evaluate('(s6Wing.frChoice?.t||0)>.3'):break
  p.evaluate("()=>{s6Wing.frChoice.side='left';s6Wing.frChoice.t=1/120;}")
  frames=[];states=[]
  for i in range(64):
   side='left'if i//16%2==0 else'right';n=[4,4,4,3][i%4]
   if i%16==0:
    key='ArrowLeft'if side=='left'else'ArrowRight';p.keyboard.down(key);step(p,1);p.keyboard.up(key);step(p,n-1)
   else:step(p,n)
   q=p.evaluate("()=>{const c=document.getElementById('screen'),r=city16MenuRect();return{image:c.toDataURL('image/png'),rect:[Math.round(r.x*SS),Math.round(r.y*SS),Math.round(r.w*SS),Math.round(r.h*SS)],choice:FATE15.lastChoice,arrow:CITY16.lastSelection,trace:CITY16.lastTrace,canvas:[c.width,c.height],ss:SS};}")
   ck(diff+' frame'+str(i)+' native input and authored phase',q['choice']['selected']==side and q['arrow']['key']=='pm27_arrow_g'and 0<=q['arrow']['frame']<16 and q['trace']['side']==side and q['trace']['difficulty']==diff and q['trace']['frame']==q['arrow']['frame'])
   im=Image.open(io.BytesIO(base64.b64decode(q['image'].split(',')[1]))).convert('RGB');x,y,ww,hh=q['rect'];im=im.crop((x,y,x+ww,y+hh));assert im.size==(912,512),im.size
   frames.append(im);states.append({'selected':side,'frame':q['arrow']['frame'],'key':q['arrow']['key'],'trace':q['trace']})
   if i in [0,16]:im.save(O/(diff+'-'+side+'.png'))
  ck(diff+' contains all16 native highlight phases',set(v['frame']for v in states)==set(range(16)),sorted(set(v['frame']for v in states)))
  ck(diff+' actual title matches difficulty',q['choice']['left']==('HARRIER'if diff=='hard'else'STORM CANNON')and q['choice']['right']=='ROUGH RIDERS',q['choice'])
  (O/(diff+'-frames.json')).write_text(json.dumps(states,indent=2),encoding='utf8');allFrames+=frames
  # GIF uses one shared palette, no blur or interpolated image frames.
  strip=Image.new('RGB',(912*8,512*8))
  for i,im in enumerate(frames):strip.paste(im,(i%8*912,i//8*512))
  palette=strip.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  gif=[im.quantize(palette=palette,dither=Image.Dither.NONE)for im in frames]
  gif[0].save(O/('pursuit-'+diff+'-highlight.gif'),save_all=True,append_images=gif[1:],duration=[60,60,60,70]*16,loop=0,optimize=False,disposal=1)
  # Render both native card states against the same scene with just the new
  # trace disabled. Every changed pixel must remain on the selected perimeter.
  for selected in ['left','right']:
   sample=p.evaluate("""side=>{s6Wing.frChoice.side=side;s6Wing.frChoice.t=7.5/16;const draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);s6WingChoiceDraw();return document.getElementById('screen').toDataURL('image/png');};const actual=draw(),saved=city16Trace;let plain;try{city16Trace=()=>false;plain=draw();}finally{city16Trace=saved;}const r=city16MenuRect(),B=CITY16_TRACE_ART.banks[diffKey+'-'+side];return{actual,plain,bank:B,phase:7,ss:SS,rect:[Math.round(r.x*SS),Math.round(r.y*SS),Math.round(r.w*SS),Math.round(r.h*SS)]};}""",selected)
   def crop(uri):
    im=Image.open(io.BytesIO(base64.b64decode(uri.split(',')[1]))).convert('RGB');x,y,ww,hh=sample['rect'];return im.crop((x,y,x+ww,y+hh))
   actual=crop(sample['actual']);plain=crop(sample['plain']);B=sample['bank'];ss=sample['ss'];d=B.get('density',1);f=sample['phase'];page=Image.open(R/B['path']);maskCell=page.crop((f%B['cols']*B['w'],f//B['cols']*B['h'],(f%B['cols']+1)*B['w'],(f//B['cols']+1)*B['h'])).getchannel('A');mask=Image.new('L',actual.size);mask.paste(maskCell.resize((B['w']*ss//d,B['h']*ss//d),Image.Resampling.NEAREST),(B['origin'][0]*ss//d,B['origin'][1]*ss//d));delta=ImageChops.difference(actual,plain);bands=delta.split();changed=ImageChops.lighter(ImageChops.lighter(bands[0],bands[1]),bands[2]);outside=ImageChops.multiply(changed,ImageChops.invert(mask));count=sum(v>0 for v in changed.getdata())
   ck(diff+' '+selected+' actual border visibly flashes',count>500,{'changedPixels':count,'bank':B['key']})
   ck(diff+' '+selected+' unselected card, aircraft, text and footer remain byte-identical',outside.getbbox()is None)
   actual.save(O/(diff+'-'+selected+'-trace-native.png'));plain.save(O/(diff+'-'+selected+'-without-trace.png'))
 # Confirm the new right-card name still reaches the real native briefing/boss.
 box=p.locator('#screen').bounding_box();p.mouse.move(box['x']+box['width']*.72,box['y']+box['height']*.49);p.mouse.down()
 for i in range(60):
  step(p,1)
  if p.evaluate('!!BOFCinematicDirector.current'):break
 p.mouse.up();q=p.evaluate('({id:BOFCinematicDirector.current?.id,lines:BOFCinematicDirector.current?.beats.map(b=>b.text)})')
 ck('real right-card pointer opens Rough Riders campaign briefing',q.get('id')=='route-right'and any('Rough Riders'in t for t in q['lines'])and not any(re.search(r'\brebels?\b',t,re.I)for t in q['lines']),q)
 for i in range(1200):
  step(p,6)
  if p.evaluate('!!boss'):break
 q=p.evaluate('({name:boss?.name,kind:boss?.kind,ships:boss?._rebels?.ships.map(q=>q.key),route:s6Wing.route})')
 ck('native route still spawns the actual five Rough Riders',q.get('kind')=='rebelsquad'and q.get('name')=='THE ROUGH RIDERS'and len(q.get('ships')or[])==5 and q.get('route')=='right',q)
 ck('no page/console/HTTP errors',not errors,errors);b.close()
strip=Image.new('RGB',(912*16,512*8))
for i,im in enumerate(allFrames):strip.paste(im,(i%16*912,i//16*512))
palette=strip.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE)for im in allFrames]
gif[0].save(O/'pursuit-highlights.gif',save_all=True,append_images=gif[1:],duration=[60,60,60,70]*32,loop=0,optimize=False,disposal=1)
for filename,total in [('pursuit-hard-highlight.gif',4000),('pursuit-furious-highlight.gif',4000),('pursuit-highlights.gif',8000)]:
 im=Image.open(O/filename);dur=0
 for f in range(im.n_frames):im.seek(f);dur+=im.info['duration']
 ck(filename+' actual GIF geometry and timing',im.size==(912,512)and dur==total,{'frames':im.n_frames,'durationMs':dur,'size':im.size})
(O/'dialogue-samples.json').write_text(json.dumps(dialogues,indent=2),encoding='utf8')
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Real native rendered menus captured with actual keyboard left/right input; real right-card pointer commits the campaign briefing and five-ship encounter. Prepared checkpoint, no campaign win.','dialogueSamples':len(dialogues)},indent=2),encoding='utf8')
print(str(sum(v['ok']for v in checks))+'/'+str(len(checks))+' native/GIF/name checks passed; '+str(len(dialogues))+' dialogue lines sampled.',flush=True)
assert all(v['ok']for v in checks)
