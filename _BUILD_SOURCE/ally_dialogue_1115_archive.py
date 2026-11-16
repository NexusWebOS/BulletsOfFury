from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,json,sys,base64,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/ally_dialogue_1115/archive';F=O/'films';F.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
source=(R/'_BUILD_SOURCE/ally_dialogue_1115_record.py').read_text(encoding='utf8')
RECORD=next(ast.literal_eval(n.value)for n in ast.parse(source).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RECORD'for t in n.targets))
original=json.loads((O.parent/'dialogue-inventory.json').read_text(encoding='utf8'));legacy={p:v for p,v in original['legacy'].items()if len(v['cast'])>1};errors=[]
files=['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html','assets/opening_fury_1114.js','assets/cockpit_talk_art_1114.js','assets/cockpit_talk_1114.js']
report={'clips':[],'errors':[],'scope':'Review-only native comic rehearsals of six inactive PILOT_OPENINGS duo scripts. Exact retained words and casts, current castB talking cockpit portraits and native letter audio. The old flight staging is not reproduced. No campaign routing or shipping scripts are changed.','before':{n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in files}}
with sync_playwright()as pw:
 browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?archive-duo-rehearsal=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 for lead,v in legacy.items():
  plan={'key':'archive-'+lead,'title':lead.title()+' lead — '+' & '.join(c.title()for c in v['cast']),'pilot':lead,'scene':'inactive pilot opener','cast':v['cast'],'original':[b for b in v['beats']if b.get('text')]}
  selected=p.evaluate('''plan=>{BOFCinematicDirector.cancel();story=null;campPause=null;run.mode='campaign';diffKey='furious';run.pilot=plan.pilot;pilotIndex=PILOTS.findIndex(p=>p.key===plan.pilot);coopOn=false;run._gp4StageX=null;D1110.paused=false;D1110.static=false;window.__allyReviewDone=false;Input.clearTaps();Input.mouse.down=false;
  const source=PILOT_OPENINGS[plan.pilot];let i=0;const rows=source.beats.filter(b=>b.text).map(raw=>{const text=raw.text,readAt=i===0?.42:.26,duration=Math.max(3.2,text.length/30+2.2),id='ARCHIVE-'+plan.pilot.toUpperCase()+'-'+String(++i).padStart(2,'0');return {id,who:raw.who.toUpperCase(),text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people:[...source.cast],fpScene:'archive-rehearsal',fpPilot:plan.pilot,fpLocations:Object.fromEntries(source.cast.map(pk=>[pk,'cockpit-sky'])),duration,speechEnd:readAt+text.length/30+.12,readings:[],_cueSet:new Set(),cm3:{group:'archive:'+plan.pilot,readAt,newStrip:i===1,baseDuration:duration}}});
  window.__allyReviewRows=rows;window.__allyReviewKeys=d1110Keys(rows,plan.pilot);d1110Ready(__allyReviewKeys);return rows.map(b=>({id:b.id,who:b.who,text:b.text,people:b.people,duration:b.duration,locations:b.fpLocations,kind:b.kind}));}''',plan)
  assert [r['text']for r in selected]==[r['text']for r in plan['original']]
  p.wait_for_function('()=>d1110Ready(__allyReviewKeys)',polling=50)
  p.evaluate('''plan=>{CP15.history=[];CM3.last=null;CP15.last=null;d1110Play('archive-dialogue-'+plan.pilot,__allyReviewRows,()=>{window.__allyReviewDone=true;});Input.clearTaps();last=performance.now();Audio.startMusic('hq');}''',plan)
  print('REHEARSING '+lead+' '+str(len(selected))+' lines',flush=True);r=p.evaluate(RECORD,plan);(F/(plan['key']+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));shots=[]
  for i,s in enumerate(r.pop('samples')):
   fn=plan['key']+'-%02d.png'%i;(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':fn})
  r.update({'plan':plan,'rows':selected,'shots':shots,'errors':list(errors)});report['clips'].append(r);report['errors']=list(errors);(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');assert r['completed']and r['peak']>.001 and not errors
  faces=[f for line in r['receipts']for f in line['faces']];assert faces and all(f.get('artFamily')=='castB-1115'and not f.get('loading')for f in faces),(lead,faces)
  print(json.dumps({'archive':lead,'seconds':r['seconds'],'currentFaceReceipts':len(faces)}),flush=True)
 browser.close()
report['after']={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in files};assert report['after']==report['before'];(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('Six exact archived duo scripts rehearsed with current talking cockpit art.',flush=True)
