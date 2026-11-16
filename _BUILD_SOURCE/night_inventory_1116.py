from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-inventory=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 result=p.evaluate(r'''()=>{
  BOFOnline.submitScore=()=>{};BOFCinematicDirector.cancel();run.mode='campaign';delete run._gp4StageX;
  const pilots=PILOTS.map(q=>q.key),ids=Object.keys(C16_STORY.scenes),cases=[],issues=[],seen=new Set(),canonical={};
  for(const diff of ['normal','hard','furious'])for(const pk of pilots)for(const partner of [null,...pilots.filter(v=>v!==pk)])for(const route of ['left','right']){
   diffKey=diff;run.pilot=pk;pilotIndex=pilots.indexOf(pk);coopOn=!!partner;if(partner){p2Index=pilots.indexOf(partner);run2.pilot=partner;}
   for(const id of ids){
    // The active opener uses FURY14; old retained C16 opening rows are archive data.
    if(id==='opening')continue;
    let rows;try{rows=c16Rows(id,pk,route);}catch(e){issues.push({type:'exception',id,pk,partner,diff,route,error:String(e)});continue;}
    const list=rows.map(v=>({id:v.id,who:v.who,text:v.text,duration:v.duration,kind:v.kind,bank:v.bank,people:v.people,locations:v.fpLocations,page:v.page,cm3:v.cm3,service:v.service14,cw:v.cw16,hq:v.hq19,kit:v.kit17,readHold:v.text?v.duration-(v.cm3?.readAt||0)-v.text.length/30-(v.cm3?.readAt!=null?.18:0):null}));
    cases.push({id,pk,partner,diff,route,count:list.length,duration:list.reduce((n,v)=>n+v.duration,0)});
    if(pk==='cole'&&!partner&&route==='left')canonical[diff+':'+id]=list;
    for(const row of list){const bad=[];if(!Number.isFinite(row.duration)||row.duration<=0)bad.push('invalid-duration');if(/\$\w+|\[Guard names\]/.test(row.text||''))bad.push('unresolved-text');if(row.cm3&&row.text&&row.readHold<2.2)bad.push('short-complete-text-hold');if(new Set(rows.map(v=>v.id)).size!==rows.length)bad.push('duplicate-shot-id');for(const type of bad){const k=[type,id,row.id,pk,partner,diff,route].join('|');if(!seen.has(k)){seen.add(k);issues.push({type,scene:id,pk,partner,diff,route,...row});}}}
   }
  }
  coopOn=false;run.pilot='cole';pilotIndex=pilots.indexOf('cole');return{pilots,sceneIds:ids,canonical,cases,issues};
 }''')
 result.update({'errors':errors,'scope':'Current runtime C16 row generators for all9 pilots, all ordered two-pilot combinations, Normal/Hard/Furious, left/right routes. Metadata/continuity/read-time inventory, not rendered-scene or campaign certification. Retained C16 opening is excluded; current FURY14 opener is reviewed separately.'});b.close()
(O/('inventory-'+(sys.argv[1]if len(sys.argv)>1 else'before')+'.json')).write_text(json.dumps(result,indent=2),encoding='utf8');counts={k:sum(q['type']==k for q in result['issues'])for k in set(q['type']for q in result['issues'])};print(json.dumps({'cases':len(result['cases']),'scenes':result['sceneIds'],'issues':counts,'errors':errors}));print(json.dumps([q for q in result['issues']if not q.get('partner')and q.get('pk')=='cole'and q.get('diff')=='hard'and q.get('route')=='left'][:14],indent=2))
