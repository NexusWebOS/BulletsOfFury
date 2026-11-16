from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from io import BytesIO
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/('_shots/cinema_overnight_1116/'+(sys.argv[1]if len(sys.argv)>1 else'render-before'));O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[];tiles=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-render=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate("()=>{BOFOnline.submitScore=()=>{};run.mode='campaign';run.pilot='cole';pilotIndex=8;coopOn=false;diffKey='hard';Input.clearTaps();Input.mouse.down=false;}")
 p.evaluate("""()=>{window.NightAudit={badSourceRects:[],styleLeaks:[],smoothing:[],draws:0,conferenceDraws:0,blocks:[],skipped:[]};const draw=ctx.drawImage;ctx.drawImage=function(...a){NightAudit.draws++;const im=a[0],w=im?.naturalWidth||im?.width,h=im?.naturalHeight||im?.height;if(a.length===9&&w&&h&&(a[1]<0||a[2]<0||a[1]+a[3]>w+.01||a[2]+a[4]>h+.01)&&NightAudit.badSourceRects.length<400)NightAudit.badSourceRects.push({tag:window.NightTag,source:im.src?.split('/').at(-1),rect:a.slice(1,5),size:[w,h]});if(ctx.imageSmoothingEnabled&&NightAudit.smoothing.length<100)NightAudit.smoothing.push(window.NightTag);if(im?.src?.includes('/cinema_overnight_1116/hq-conference-comic.webp')&&a.length===9&&a[3]===754&&a[4]===270)NightAudit.conferenceDraws++;return draw.apply(this,a);};const block=msgDrawBlock;msgDrawBlock=function(o){const L=block.apply(this,arguments);if(NightAudit.blocks.length<10)NightAudit.blocks.push({text:o.text,budget:o.budget,box:[o.x,o.y,o.w,o.h],layout:L});return L;};window.nightStyle=()=>({transform:Array.from([ctx.getTransform().a,ctx.getTransform().b,ctx.getTransform().c,ctx.getTransform().d,ctx.getTransform().e,ctx.getTransform().f]),alpha:ctx.globalAlpha,blend:ctx.globalCompositeOperation,filter:ctx.filter,shadow:ctx.shadowBlur,smoothing:ctx.imageSmoothingEnabled});}""")
 ids=p.evaluate("Object.keys(C16_STORY.scenes).filter(id=>id!=='opening')")
 for scene in ids:
  stage=2 if scene=='post-2'else 7 if scene in ['arrival-7','post-7']else 6 if scene in ['post-6']else 5 if scene in ['post-5','warp-5-9']else 9 if '9'in scene else 3 if scene=='post-3'else 4 if scene in ['post-4','arrival-4']else 1
  p.evaluate("q=>{BOFCinematicDirector.cancel();delete run._gp4StageX;campaign.cityRescue16=null;campaign.stageX1004=null;beginStage(q.stage);BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;run.mode='campaign';mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;window.NightRows=c16Rows(q.scene,'cole','left');d1110Play('night-'+q.scene,NightRows,()=>{});}",{'scene':scene,'stage':stage})
  p.wait_for_function('()=>{stageLoadTick();return d1110Ready(BOFCinematicDirector.current.d1110Keys||[])}',polling=50)
  n=p.evaluate('NightRows.length');e0=len(errors)
  for i in range(n):
   for tag in ['reading','end']:
    q=p.evaluate("([i,tag])=>{const s=BOFCinematicDirector.current,b=s.beats[i];s.i=i;s.t=tag==='reading'?Math.min(1.8,b.duration*.55):Math.max(.2,b.duration-.35);s.age=s.beats.slice(0,i).reduce((n,v)=>n+v.duration,0)+s.t;s.shown=tag==='end'?b.text.length:Math.min(b.text.length,Math.floor(Math.max(0,s.t-(b.cm3?.readAt||0))*30));window.NightTag={scene:s.id,shot:b.id,tag};NightAudit.blocks=[];const before=nightStyle(),skips=window.__skippedDraws?.().skipped||0;d1110Visual(b,s);const after=nightStyle(),delta=(window.__skippedDraws?.().skipped||0)-skips;if(JSON.stringify(before)!==JSON.stringify(after))NightAudit.styleLeaks.push({tag:NightTag,before,after});if(delta)NightAudit.skipped.push({tag:NightTag,delta,details:window.__skippedDraws()});return{shot:b.id,who:b.who,text:b.text,kind:b.kind,time:s.t,shown:s.shown,mode:b.hq19||b.service14||b.cw16||b.kit17,last:D1110.last,cp:CP15.last,blocks:NightAudit.blocks,errors:window.__lastError||null}}",[i,tag])
    raw=p.locator('#screen').screenshot();im=Image.open(BytesIO(raw)).convert('RGB');small=im.resize((456,256),Image.Resampling.NEAREST);tile=Image.new('RGB',(456,288),'#0b1420');tile.paste(small,(0,28));ImageDraw.Draw(tile).text((7,7),scene+' / '+q['shot']+' / '+tag,fill='#e9f1ff');tiles.append(tile)
    if tag=='end'and (q.get('mode')or scene in ['post-3','ending','arrival-4']):
     fn=scene+'-'+q['shot']+'.png';(O/fn).write_bytes(raw);q['screenshot']=fn
    rows.append({'scene':scene,'tag':tag,**q})
   if len(tiles)>=12:
    sheet=Image.new('RGB',(456*3,288*4),'#050810')
    for j,im in enumerate(tiles[:12]):sheet.paste(im,((j%3)*456,(j//3)*288))
    sheet.save(O/f'contact-{len(list(O.glob("contact-*.jpg"))):02}.jpg',quality=91);tiles=tiles[12:]
  print(scene+': '+str(n)+' native shots, '+str(len(errors)-e0)+' errors',flush=True)
 if tiles:
  sheet=Image.new('RGB',(456*3,288*((len(tiles)+2)//3)),'#050810')
  for j,im in enumerate(tiles):sheet.paste(im,((j%3)*456,(j//3)*288))
  sheet.save(O/f'contact-{len(list(O.glob("contact-*.jpg"))):02}.jpg',quality=91)
 audit=p.evaluate('NightAudit');b.close()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'audit':audit,'scope':'Cole/Hard native scene rows rendered at two animation times. Native production draw path and decoded assets; source rectangles, sampling, draw skips and context restoration inspected. Direct render checkpoints, not naturally played campaign transitions.'},indent=2),encoding='utf8');print(json.dumps({'renders':len(rows),'errors':errors,'audit':{k:v for k,v in audit.items()if k!='blocks'}}),flush=True)
