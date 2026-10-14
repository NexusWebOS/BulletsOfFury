from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];P=R/'_shots/air_motion_1013';P.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));report=[]
RASTER='''async()=>{const rows=[];for(const d of Object.values(AM13_ART)){for(const kind of ['heading','roll']){const m=d[kind],paths=m.kind==='strip'?[m.path]:m.refs.map(f=>f.path),images=await Promise.all(paths.map(path=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>ok(im);im.onerror=()=>no(new Error(path));im.src='../../'+path})));const c=document.createElement('canvas');c.width=c.height=m.cell;const ctx=c.getContext('2d',{willReadFrequently:true});for(let f=0;f<m.frames;f++){ctx.clearRect(0,0,c.width,c.height);const im=images[m.kind==='strip'?0:f];if(im.height!==m.cell||im.width!==(m.kind==='strip'?m.frames*m.cell:m.cell))throw new Error('dimensions '+d.id);ctx.drawImage(im,m.kind==='strip'?f*m.cell:0,0,m.cell,m.cell,0,0,m.cell,m.cell);const a=ctx.getImageData(0,0,m.cell,m.cell).data;let count=0,edge=0;for(let y=0;y<m.cell;y++)for(let x=0;x<m.cell;x++)if(a[(y*m.cell+x)*4+3]>0){count++;if(x<2||y<2||x>=m.cell-2||y>=m.cell-2)edge++}if(count<20||edge>0)throw new Error('alpha '+d.id+' '+kind+' '+f+' '+edge);rows.push([d.id,kind,f,count])}}}return{frames:rows.length,designs:Object.keys(AM13_ART).length}}'''
try:
 with sync_playwright() as pw:
  for name in ['edge','chrome','firefox']:
   b=(pw.firefox.launch() if name=='firefox' else pw.chromium.launch(channel='msedge' if name=='edge' else 'chrome',args=['--mute-audio']));p=b.new_page(viewport={'width':1380,'height':1050});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(f'http://localhost:{port}/_shots/air_motion_1013/review.html');p.wait_for_function("document.getElementById('status').textContent.startsWith('All 24')",timeout=60000)
   raster=p.evaluate(RASTER);assert raster['frames']==2088,raster
   p.screenshot(path=str(P/f'hangar-{name}.png'));print(name,'raster',raster,flush=True)
   p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF);live=[]
   for stage in [1,4,6,8,9]:
    p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True});p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=120000)
    p.evaluate('()=>{story=null;s6Opening=null;s6Wing=null;debugFight=null;bossActive=subBossActive=false;warnT=0;stageTimer=1;waveIdx=999;spawnClock=9999;subBossDone=true;VP12.next=CP12.next=9999;player.dead=false;player.invuln=1e9;if(wfx)wfx.fseq=null;enemies=[];}')
    for difficulty in ['easy','normal','hard','furious']:
     p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d];enemies=[];VP12.groups=[];eBullets=[];}',difficulty)
     if stage in [1,4,6,8]:
      p.wait_for_function('s=>XART.rdy(VP12_ART[s].key)&&XART.rdy(AM13_ART["flight_variant_"+s].heading.key)&&XART.rdy(AM13_ART["flight_variant_"+s].roll.key)',arg=stage,timeout=60000)
      p.evaluate('()=>vp12Spawn("barrel")');p.evaluate(shoot.STEP,50)
      r=p.evaluate('()=>({count:VP12.groups[0].live,keys:enemies.filter(e=>e._vp12).map(e=>e._air13RenderedKey),frames:enemies.filter(e=>e._vp12).map(e=>e._air13Frame)})');assert r['count']=={'easy':3,'normal':5,'hard':7,'furious':9}[difficulty],r;assert all(r['keys']),r
     else:
      p.evaluate('()=>{window.E=spawnEnemy("wskim",240,240);E.hp=E.maxhp=900;E._barrelT=.4;E.spin=.2;}');p.wait_for_function('()=>XART.rdy(AM13_ART.wskim.roll.key)&&XART.rdy(AM13_ART.wskim.sourceKeys.wskim)',timeout=60000);r=p.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);drawEnemy(E);return{key:E._air13RenderedKey,frame:E._air13Frame}}')
      assert r['key'] and '_roll' in r['key'],r
     live.append({'stage':stage,'difficulty':difficulty,**r})
    if name=='edge':p.screenshot(path=str(P/f'live-stage-{stage}.png'))
   # Rebel direct renderer: every heading and every roll, cloak and masked modules.
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True});p.wait_for_function('()=>Object.values(AM13_ART).filter(d=>d.rebel).every(d=>XART.rdy(d.heading.key)&&XART.rdy(d.roll.key))',timeout=60000)
   rebel=p.evaluate('''()=>{const out=[];window.B={x:240,y:200,hp:5000,maxhp:5000,dead:false};rebelSquadInit(B,5000);const qs=B._rebels.ships;for(const q of qs){q.x=240;q.y=220;q.mode='fight';q.t=0;q.frCloak=0;q.flash=0;q.frSomersault=false;for(let i=0;i<24;i++){q.evadeT=i<8?0:.38*(1-(i-8)/16);q.rfHeading=i<8?Math.PI/2+i*TAU/8:null;ctx.setTransform(1,0,0,1,0,0);if(!air13DrawRebel(q))throw new Error('rebel frame '+q.key+' '+i);out.push(q._air13Frame)}const m=fr27RebelModules(q);m.find(p=>p.id==='left').hp=0;q.evadeT=.19;air13DrawRebel(q);q.dead=true;air13DrawRebel(q,{allowDead:true,forceRoll:.5,alpha:1});}return{frames:out.length,tints:AIR13.tints.size}}''');assert rebel['frames']==120 and rebel['tints']<=64,rebel
   assert not errors,errors
   report.append({'browser':name,'raster':raster,'live':live,'rebels':rebel,'errors':errors});b.close();print(name,'PASS',len(live),'live difficulty/stage fixtures + 120 rebel poses',flush=True)
finally:
 stop();(P/'native_qa.json').write_text(json.dumps(report,indent=2))
