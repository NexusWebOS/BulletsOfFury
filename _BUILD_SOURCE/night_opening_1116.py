from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,ast,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/opening';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];checks=[];shots=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-opening=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 if len(sys.argv)>1 and sys.argv[1]=='record':
  tree=ast.parse((R/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf8'));record=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(getattr(t,'id','')=='RECORD'for t in n.targets))
  p.evaluate("()=>FURY14.preview('opening','cole')");p.wait_for_function('()=>fury14Ready(FURY14.openKeys)');p.evaluate('()=>{campaignIntro.t=0;last=performance.now()}')
  q=p.evaluate(record,'opening');(O/'opening.webm').write_bytes(base64.b64decode(q.pop('video').split(',')[1]));q['errors']=errors;(O/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf8');print(json.dumps(q,indent=2));b.close();sys.exit(0 if not errors and q['peak']>.001 else 1)
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  p.evaluate("pk=>{BOFCinematicDirector.cancel();run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);run.mode='campaign';window.NightDone=0;d1110Play('night-first-comic',fury14Rows(pk),()=>{NightDone++;setState(GS.TITLE)});}",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  q=p.evaluate('''()=>{let n=0,shots=[],holds={};while(BOFCinematicDirector.current&&n<4000){const s=BOFCinematicDirector.current,b=s.beats[s.i];BOFCinematicDirector.tick(1/60);if(s.shown>=b.text.length&&b.text)holds[b.id]=(holds[b.id]||0)+1/60;if(n%15===0&&BOFCinematicDirector.current)BOFCinematicDirector.draw();if(s.t>2.1&&!shots.some(q=>q.id===b.id)&&b.shot!=='fade'){BOFCinematicDirector.draw();shots.push({id:b.id,shot:b.shot,layout:FIXC14.last,image:cv.toDataURL('image/png')})}n++;}return{done:NightDone,n,holds,shots};}''')
  checks.append({'name':pk+' six-panel native director traversal','ok':q['done']==1 and len(q['shots'])==5 and min(q['holds'].values())>2.25,'data':{k:q[k]for k in['done','n','holds']}})
  for s in q['shots']:
   fn=pk+'-'+s['shot']+'.png';(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({'pilot':pk,'file':fn,**s})
 # Check the actual opening's full clock and all transition backgrounds.
 p.evaluate("()=>{NightDone=0;FURY14.preview('opening','cole');campaignIntro.onDone=()=>{NightDone++;setState(GS.TITLE)}}");p.wait_for_function('()=>fury14Ready(FURY14.openKeys)')
 q=p.evaluate('''()=>{const phases=[],seen=new Set(),frames=[];let n=0;while(state===GS.CAMPAIGNINTRO&&n<18000){drawCampaignIntro(1/60);const d=FURY14.last;if(d?.kind==='crawl'&&!seen.has(d.background)){seen.add(d.background);phases.push(d)}if(d?.kind==='crawl'&&(Math.abs(d.t-3)<.008||Math.abs(d.t-35)<.008||Math.abs(d.t-60)<.008||Math.abs(d.t-85)<.008||Math.abs(d.t-(FURY14.total-6))<.008))frames.push({t:d.t,image:cv.toDataURL('image/png'),meta:d});n++}return{phases,n,total:FURY14.total,done:NightDone,frames};}''')
 checks.append({'name':'Full opening reaches its callback once with all five backgrounds','ok':q['done']==1 and len(q['phases'])==5,'data':{k:q[k]for k in['phases','n','total','done']}})
 for i,s in enumerate(q['frames']):fn='crawl-'+str(i)+'.png';(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({'file':fn,**s})
 checks.append({'name':'No page console or HTTP errors','ok':not errors,'data':errors});b.close()
for group,files in [('comic',[s for s in shots if s.get('shot')in['pilot','orders']]),('crawl',[s for s in shots if s['file'].startswith('crawl')])]:
 sheet=Image.new('RGB',(1368,((len(files)+2)//3)*279),(6,10,17));d=ImageDraw.Draw(sheet)
 for i,s in enumerate(files):im=Image.open(O/s['file']).convert('RGB').resize((456,256));x=i%3*456;y=i//3*279;sheet.paste(im,(x,y));d.text((x+5,y+258),s['file'],fill='white')
 sheet.save(O/(group+'-contact.jpg'))
(O/'checks.json').write_text(json.dumps({'checks':checks,'shots':shots,'errors':errors,'scope':'All9 selected-pilot Stage1 comics through their native director clocks, direct native crawl owner through all transitions. Checkpoints and shortened drawing cadence for comics, not nine campaign starts.'},indent=2),encoding='utf8');print(json.dumps(checks,indent=2));assert all(c['ok']for c in checks)
