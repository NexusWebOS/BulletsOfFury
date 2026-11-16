from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,hashlib,base64,io
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage_frame_1115';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1400],flush=True)
def step(p,n=6):
 err=p.evaluate(shoot.STEP,n)
 if err:raise RuntimeError(err)
 p.wait_for_timeout(1)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?stage-frame-qa=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');diffKey='furious';DIFF=difficultyForRun('campaign','furious');campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A',7:'A',8:'A',9:'A'};campaign.unlockedMax=9;campaign.bonusUnlocked=true;campaign.stage6Fate=null;campaign.stageX1004=null;campaign.cityRescue16=null;CITY16.travel=null;FS11.reward=null;AP10_X.reward=null;UC22.focus=false;CF4.focus=false;MAP4E.xPreview=false;openStageSelect(7,{});Input.clearTaps();Input.mouse.down=false;}")
 p.wait_for_function('()=>{map4eWarm();return fury14MapReady()&&mb15Warm()&&pm27Live();}',polling=50)
 for i in range(400):
  step(p)
  if p.evaluate('sselBoot<=0&&!!MBR15.last'):break
 ck('new panel reached through native map renderer',p.evaluate('state===GS.STAGESEL&&!!MBR15.last'))
 q=p.evaluate("()=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const before=document.getElementById('screen').toDataURL(),out=drawTheaterProgression1003g(ctx,{x:12,y:320,w:456},7),after=document.getElementById('screen').toDataURL();ctx.restore();return{out,same:before===after}}")
 ck('removed theater renderer draws zero pixels',q['out']is False and q['same'],q)
 corpus=p.evaluate("()=>[...Array.from({length:9},(_,i)=>mapgCopy(i+1)),{key:'cf4-x-left',title:'STAGE X - CITY RESCUE',body:'THE HARRIER IS ATTACKING THE CITY. SAVE THE PEOPLE BEFORE HEADING TO THE RIVERBANK.'},{key:'fs11-mk2',title:'STAGE X CLEAR - SIGNATURE MK II',body:'ALL NINE PILOT SPECIALS ENHANCED. 20 SECOND WINDOWS. YOUR NEXT SPECIAL PICKUP USES MK II. AIR SUPERIORITY SUPPLIES ALSO AWARDED.'},{key:'uc22',title:\"DECKER'S UPGRADE CENTER\",body:'FORGOT AN UPGRADE, OR WANT A RE-SPEC? THE FORGE AND YOUR LOADOUT ARE HERE.'}]")
 for copy in corpus:
  q=p.evaluate("copy=>{MBR15.typing=null;mb15BriefingDraw(copy);stateT+=10;for(let i=0;i<40;i++){stateT+=.25;mb15BriefingDraw(copy)}return MBR15.last}",copy)
  ck(copy['key']+' full copy and PixelMap layout fit',q['count']==q['total']and q['font']=='PixelMap'and q['titleLayout']['used']<=q['titleLayout']['available']and q['bodyLayout']['used']<=q['bodyLayout']['available']and all(len(row['full'])>0 for row in q['bodyLayout']['rows']),q)
 # Real wrappers still choose special reward and mandatory-city messages.
 q=p.evaluate("()=>{FS11.reward={pilot:'cole'};AP10_X.reward={};MBR15.typing=null;mapgBriefingDraw(7);return MBR15.last}")
 ck('actual earned reward wrapper reaches clear frame',q['key']=='fs11-mk2'and q['variant']=='clear'and 'AIR SUPERIORITY'in q['body'],q)
 for i in range(120):step(p)
 p.locator('#screen').screenshot(path=str(O/'clear-map.png'))
 # Capture the actual reward reveal from a new native state-clock start.
 p.evaluate("()=>{MBR15.typing=null;PM27.events=[];}");step(p,1);start=p.evaluate('MBR15.last');frames=[];states=[]
 for i in range(144):
  step(p,[4,4,4,3][i%4]);q=p.evaluate("()=>({image:document.getElementById('screen').toDataURL('image/png'),last:MBR15.last,ss:SS,offset:campaignViewOffset(),canvas:[document.getElementById('screen').width,document.getElementById('screen').height]})")
  im=Image.open(io.BytesIO(base64.b64decode(q['image'].split(',')[1]))).convert('RGB');ss=q['ss'];x=round(q['offset']*ss);im=im.crop((x,300*ss,x+480*ss,512*ss));frames.append(im);states.append({k:q['last'][k]for k in ['key','count','total','visibleTitle','visibleBody']})
 ck('native reveal starts blank and advances to full text',start['count']<3 and states[0]['count']<states[-1]['count']==states[-1]['total'],{'start':start['count'],'first':states[0],'last':states[-1]})
 ck('native reveal is monotonic with readable fixed layout',all(a['count']<=c['count']for a,c in zip(states,states[1:])))
 ck('native PixelMap calls contain no theater label',p.evaluate("!PM27.events.some(e=>e.text.includes('THEATER PROGRESSION'))"))
 strip=Image.new('RGB',(frames[0].width*12,frames[0].height*12))
 for i,im in enumerate(frames):strip.paste(im,(i%12*im.width,i//12*im.height))
 palette=strip.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE)for im in frames];gif[0].save(O/'stage-briefing-typewriter.gif',save_all=True,append_images=gif[1:],duration=[60,60,60,70]*36,loop=0,optimize=True,disposal=1)
 (O/'reveal-states.json').write_text(json.dumps(states,indent=2),encoding='utf8')
 p.evaluate("()=>{FS11.reward=null;AP10_X.reward=null;campaign.rank[7]=undefined;campaign.unlockedMax=6;campaign.stageX1004={route:'left',target:'harrier',done:false};cmap2.focus='map';MBR15.typing=null;mapgBriefingDraw(7);}");q=p.evaluate('MBR15.last')
 ck('actual city gate wrapper uses priority frame without unlocking7',q['variant']=='priority'and q['key'].startswith('city16-required')and p.evaluate('campaign.unlockedMax===6&&city16Gate()'),q)
 for i in range(90):step(p)
 p.locator('#screen').screenshot(path=str(O/'priority-map.png'))
 p.evaluate("()=>{campaign.stageX1004=null;campaign.rank[7]='A';campaign.unlockedMax=8;campaign.bonusUnlocked=false;CF4.focus=false;MAP4E.xPreview=false;cmap2.focus='map';sselMax=8;sselCursor=1;sselNext=1;MBR15.typing=null;}")
 for i in range(100):step(p)
 q=p.evaluate('MBR15.last');ck('standard stage uses mission frame',q['variant']=='mission',q);p.locator('#screen').screenshot(path=str(O/'mission-map.png'))
 prior=q['key'];p.keyboard.down('ArrowRight');step(p,1);p.keyboard.up('ArrowRight');step(p,3);q=p.evaluate('MBR15.last');ck('actual map input changes stage and restarts reveal',q['key']!=prior and q['count']<=4,q)
 count=p.evaluate('MBR15.last.count');p.evaluate('campPauseOpen()');step(p,120);paused=p.evaluate('MBR15.last.count');p.evaluate('campPauseClose()');ck('native map pause freezes reveal',count==paused,{'before':count,'paused':paused})
 ck('no page/console/HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Real native map rendering and keyboard selection, original reward/city briefing wrappers, actual glyph reveal, pause and generated panels. Prepared UI checkpoints, no campaign-win claim.'},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' map UI checks passed',flush=True);assert all(c['ok']for c in checks)
