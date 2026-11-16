from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cockpit_castB_1115';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL',name,str(data)[:1200],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?castB-qa=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 pilots=p.evaluate('PILOTS.map(p=>p.key)')
 for pk in pilots:
  q=p.evaluate("pk=>{const rows=city16Rows(pk,['axel','freezer','cole','decker','falva','lizzie']);return{dj:city16AlbumPilot(pk,[]),paired:city16AlbumPilot(pk,['decker','cole','axel','freezer']),speaker:rows[4].who,answer:rows[5].who,line:rows[4].text,people:rows[4].people,rows:rows.map(b=>({id:b.id,who:b.who,people:b.people,rooms:b.fpLocations}))}}",pk)
  ck(pk+' album joke belongs to Juggernaut with any allies',q['dj']==q['paired']=='juggernaut'and q['speaker']=='JUGGERNAUT'and q['answer']=='COLE'and q['people']==['juggernaut','cole'],q)
  matrix=p.evaluate("pk=>['post-6','arrival-7','post-7','post-8','arrival-9','post-9','warp-5-9','sting'].map(id=>({id,rows:c16Rows(id,pk).filter(b=>b.people?.length).map(b=>({id:b.id,who:b.who,people:b.people,places:b.fpLocations}))}))",pk)
  ck(pk+' post-evacuation speakers all use current cockpit family',all(all(str(row['places'].get(person,'')).startswith('cockpit-')for person in row['people'])for scene in matrix for row in scene['rows']),matrix)
  for scene in ['city','arrival']:
   p.evaluate("([pk,scene])=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);coopOn=false;D1110.static=false;run.stage=scene==='city'?6:7;const rows=scene==='city'?city16Rows(pk,[]):c16Rows('arrival-7',pk);d1110Play('style-'+scene,rows,()=>{});}",[pk,scene])
   p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
   n=p.evaluate('BOFCinematicDirector.current.beats.length')
   for i in range(n):
    q=p.evaluate("i=>{const s=BOFCinematicDirector.current;s.i=i;s.t=1.8;s.age=90+i;s.shown=20;CP15.history=[];d1110Visual(s.beats[i],s);const row=s.beats[i];return{id:row.id,who:row.who,text:row.text,album:!!row.city16Album,faces:CM3.last?.shot===row.id?CM3.last.faces:[],calls:CP15.history};}",i)
    if not q['album']:ck(pk+' '+scene+' '+q['id']+' rendered only current cockpit portraits',bool(q['faces'])and all(f.get('family')=='talking-cockpit'and f.get('artFamily')=='castB-1115'and f.get('key')=='cp15_'+f['pilot']and not f.get('loading')for f in q['faces']),q)
    if pk=='cole'and (scene=='arrival'or i in [0,1,4,5,6]):
     fn=scene+'-'+q['id']+'.png';p.locator('#screen').screenshot(path=str(O/fn));shots.append({'file':fn,**q})
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.pilot='cole';run.stage=7;d1110Play('mouth-check',city16Rows('cole',[]),()=>{});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 poses=set()
 for i in range(110):
  q=p.evaluate("i=>{const s=BOFCinematicDirector.current;s.i=4;s.t=.7+i/60;s.age=40+i/60;s.shown=Math.floor((s.t-s.beats[4].cm3.readAt)*30);d1110Visual(s.beats[4],s);return CM3.last.faces.filter(f=>f.pilot==='juggernaut').map(f=>f.frame)}",i);poses.update(q)
 ck('Juggernaut album speech animates authored mouth cells',len(poses)>=4,sorted(poses))
 q=p.evaluate("()=>{const rows=c16Rows('arrival-7','cole'),row=rows[0],saved=CP15.base.face,ready=XART.rdy;let called=0;try{CP15.base.face=()=>{called++;return{family:'old'}};XART.rdy=function(k){return k==='cp15_decker'?false:ready.call(this,k)};const result=cm3DrawFace('decker',[0,0,400,300],row,1,{zoom:0});return{called,result}}finally{CP15.base.face=saved;XART.rdy=ready}}")
 ck('loading cockpit cannot fall through to an older portrait',q['called']==0 and q['result'].get('loading')and q['result']['family']=='talking-cockpit',q)
 q=p.evaluate("()=>['post-1','post-2','post-3','post-4'].map(id=>({id,rooms:c16Rows(id,'cole').filter(b=>b.people?.includes('decker')).map(b=>b.fpLocations.decker)}))")
 ck('earlier ground-based technician keeps his real location',all(not str(room).startswith('cockpit-')for scene in q for room in scene['rooms']),q)
 ck('no page/console/HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'shots':shots,'scope':'All9 city/arrival dialogue branches drawn through actual native comic/CP15 renderers. All post-evacuation row locations checked; earlier real HQ locations retained. Loading guard and authored Juggernaut speech tested. Prepared renderer checkpoints, no campaign-win claim.'},indent=2),encoding='utf8')
print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' native speaker/style checks passed',flush=True);assert all(c['ok']for c in checks)
