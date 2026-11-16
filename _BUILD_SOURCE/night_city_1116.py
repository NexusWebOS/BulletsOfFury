from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/city';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];checks=[];shots=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-city=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  p.evaluate("pk=>{BOFCinematicDirector.cancel();D1110.paused=false;run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);run.mode='campaign';diffKey='hard';coopOn=false;Input.clearTaps();Input.mouse.down=false;window.NightDone=0;d1110Play('post-city16',city16Rows(pk,['decker','axel']),()=>{NightDone++;setState(GS.TITLE)});}",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  q=p.evaluate('''()=>{let n=0,shots=[],holds={},seen=[];while(BOFCinematicDirector.current&&n<7000){const s=BOFCinematicDirector.current,b=s.beats[s.i];BOFCinematicDirector.tick(1/60);if(!seen.includes(b.id))seen.push(b.id);if(s.shown>=b.text.length&&b.text)holds[b.id]=(holds[b.id]||0)+1/60;if(n%15===0&&BOFCinematicDirector.current)BOFCinematicDirector.draw();if(s.t>2.2&&!shots.some(q=>q.id===b.id)){BOFCinematicDirector.draw();shots.push({id:b.id,who:b.who,text:b.text,locations:b.fpLocations,image:cv.toDataURL('image/png')})}n++}return{done:NightDone,n,holds,shots,seen};}''')
  checks.append({'name':pk+' city debrief, album owner, reading hold and callback','ok':q['done']==1 and len(q['seen'])==7 and min(q['holds'].values())>=2.25 and next(s for s in q['shots']if s['id']=='CITY16-05')['who']=='JUGGERNAUT','data':{k:q[k]for k in['done','n','holds','seen']}})
  for s in q['shots']:
   fn=pk+'-'+s['id']+'.png';(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({'pilot':pk,'file':fn,**s})
 # Prepared verified city-clear receipt: exercise its actual native continuation.
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';diffKey='hard';campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=6;campaign.stageX1004={route:'left',done:true};campaign.cityRescue16=city16Receipt({version:1,completed:true,verified:true,pilot:'cole',target:'harrier',allies:['axel','decker']});CITY16.travel=null;Input.clearTaps();city16StartDebrief();}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 q=p.evaluate('''async()=>{let n=0;while(BOFCinematicDirector.current&&n<7000){BOFCinematicDirector.tick(1/60);if(n%15===0&&BOFCinematicDirector.current)BOFCinematicDirector.draw();n++;if(n%120===0)await new Promise(r=>setTimeout(r,0))}return{state,unlocked:campaign.unlockedMax,debrief:campaign.cityRescue16.debriefSeen,travel:!!CITY16.travel,stage:run.stage};}''')
 checks.append({'name':'Native city debrief unlocks the map and begins chibi travel without deploying Stage7','ok':q['state']=='stagesel'and q['unlocked']>=7 and q['debrief']and q['travel'],'data':q})
 checks.append({'name':'No page console or HTTP errors','ok':not errors,'data':errors});b.close()
files=[s for s in shots if s['pilot']in['cole','decker','juggernaut']and s['id']in['CITY16-01','CITY16-05','CITY16-ALBUM']]
sheet=Image.new('RGB',(1368,((len(files)+2)//3)*279),(6,10,17));d=ImageDraw.Draw(sheet)
for i,s in enumerate(files):im=Image.open(O/s['file']).convert('RGB').resize((456,256));x=i%3*456;y=i//3*279;sheet.paste(im,(x,y));d.text((x+5,y+258),s['file'],fill='white')
sheet.save(O/'contact.jpg');(O/'report.json').write_text(json.dumps({'checks':checks,'shots':shots,'errors':errors,'scope':'All9 pilot debriefs on native director clocks; prepared verified clear receipt tests actual map continuation. No city combat win or naturally earned achievement claim.'},indent=2),encoding='utf8');print(json.dumps(checks,indent=2));assert all(c['ok']for c in checks)
