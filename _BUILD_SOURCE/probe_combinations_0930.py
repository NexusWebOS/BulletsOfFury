"""Real renderer / preview isolation checks for all nine element families."""
import sys,json,base64,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
OUT=ROOT/'_shots/combinations_0930';OUT.mkdir(parents=True,exist_ok=True)
rows=[];errors=[]
def ok(v,n,d=None):
 rows.append(dict(ok=bool(v),name=n,detail=d));print(('OK ' if v else 'FAIL ')+n,d or '',flush=True)
port,stop=sh.serve(str(ROOT))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1100})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' or 'draw error' in m.text else None)
 p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>(window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
 p.evaluate("()=>{ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';beginStage(6);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;stagePlan=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];pBullets=[];for(const a of [...Object.values(REPAIR30_ART),...Object.values(MISSION29_ART)])XART.rdy(a.key);}")
 p.wait_for_function('()=>[...Object.values(REPAIR30_ART),...Object.values(MISSION29_ART)].every(a=>XART.rdy(a.key))',timeout=60000)
 for w,label in [(3,'laser'),(4,'cast'),(5,'orb'),(7,'chaingun')]:
  for lv in range(1,6):
   r=p.evaluate(r'''c=>{const els=['kinetic','fire','ice','lightning','chrome','dark','toxic','prism','water'],out=[];
    const before=JSON.stringify({weapon:run.weapon,wlevel:run.wlevel,wvars:run.wvars,forge:run.forge,space:run.spaceMode}),live=pBullets;
    for(const el of els){const P=forgePreviewNew(c.w,el,c.lv);let count=0,kinds=new Set();
     for(let i=0;i<60;i++){forgePreviewTick(P,240,280,1/60);count=Math.max(count,P.bullets.length);P.bullets.forEach(b=>kinds.add(b.kind));if(i===18||i===28)forgePreviewDraw(P,20,20,240,280);}
     out.push({el,err:P.err,fired:P.fired,count,kinds:[...kinds]});}
    return {out,isolated:live===pBullets&&before===JSON.stringify({weapon:run.weapon,wlevel:run.wlevel,wvars:run.wvars,forge:run.forge,space:run.spaceMode})};}''',{'w':w,'lv':lv})
   ok(r['isolated'] and all(not q['err'] and q['fired']>0 and q['count']>0 for q in r['out']),f'{label} tier {lv}: all nine previews fire, draw and preserve live loadout',r if any(q['err'] or not q['count'] for q in r['out']) else None)
  p.evaluate(r'''c=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#030611';ctx.fillRect(0,0,cv.width,cv.height);
   ['kinetic','fire','ice','lightning','chrome','dark','toxic','prism','water'].forEach((el,i)=>{const P=forgePreviewNew(c.w,el,3);for(let j=0;j<24;j++)forgePreviewTick(P,260,275,1/60);
    const x=15+(i%3)*315,y=22+Math.floor(i/3)*335;forgePreviewDraw(P,x,y+25,285,295);campText(el.toUpperCase(),x+142,y+10,14,'#fff');});ctx.restore();}''',{'w':w})
  (OUT/(label+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL()').split(',')[1]))
 r=p.evaluate(r'''()=>{const out=[];for(const el of ['kinetic','fire','ice','lightning','chrome','dark','toxic','prism','water']){
   for(const type of ['beam','orb','cast','chaingun_round']){const a=type==='beam'?MISSION29_ART['beam_'+el]:REPAIR30_ART[type+'_'+el],im=XART.get(a.key),frames=new Set(),di=ctx.drawImage;
    ctx.drawImage=function(src,...r){if(src===im&&r.length===8)frames.add(r.slice(0,4).join(','));return di.call(this,src,...r);};
    try{for(let i=0;i<6;i++){efxClock=i*.1;const q={kind:type==='chaingun_round'?'mg':type,_inf:el,lv:3,x:200,y:350,w:24,h:140,top:100,bot:350,t:i*.1,anim:i*.1,vx:0,vy:-10};
      if(type==='beam')missionBeamDraw(q);else if(type==='orb')repair30OrbDraw(q);else if(type==='cast')repair30Cell('cast_'+el,i*.1,200,200,30,120,true);else chaingunRoundDraw(q);}}
    finally{ctx.drawImage=di;}out.push({el,type,frames:frames.size,expected:Math.min(2,a.frames.length)});}}
   return out;}''')
 ok(all(q['frames']>=q['expected'] for q in r),'27 animated families advance; nine authored chaingun rounds render',[q for q in r if q['frames']<q['expected']])
 r=p.evaluate(r'''()=>{const a=REPAIR30_ART.shield,img=XART.get(a.key);for(let i=0;i<650;i++)glyph30(img,[0,0,8,8],'#'+(i+4096).toString(16),1,true);return {size:GLYPH30.map.size,bytes:GLYPH30.bytes,limit:GLYPH30.limit};}''')
 ok(r['size']<=512 and r['bytes']<=r['limit'],'glyph cache stays bounded through 650 unique masks',r)
 ok(not errors,'no browser errors',errors[:12]);b.close()
stop();(OUT/'results.json').write_text(json.dumps(rows,indent=2));sys.exit(0 if all(x['ok'] for x in rows) else 1)
