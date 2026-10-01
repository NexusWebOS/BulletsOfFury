from pathlib import Path
import sys,json,http.server,io
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/campaign_0930';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(R));errors=[];frames=[];report={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append('console: '+m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate("()=>{run.mode='campaign';run.pilot='yuri';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.bonusUnlocked=false;campaign.rivalScattered=false;Rival24.mapAvailable=false;Rival24.flying=false;Rival24.mapFocused=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();}")
  p.wait_for_function("()=>Object.keys(MAP30_ART).every(k=>XART.rdy('map30_'+k))&&cmap2Keys().every(k=>XART.rdy(k))",timeout=60000)
  p.wait_for_timeout(2800);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(80)
  p.evaluate("()=>{window.fireProofKeys=[];const g=XART.get;XART.get=function(k){fireProofKeys.push(k);return g.call(this,k);};}")
  for i in range(32):
   p.evaluate(sh.STEP,5);p.wait_for_timeout(10)
   frames.append(Image.open(io.BytesIO(p.screenshot())).convert('RGB').resize((960,540),Image.Resampling.NEAREST))
  report=p.evaluate("()=>({flameDraws:fireProofKeys.filter(k=>k==='map30_flames').length,retiredDraws:fireProofKeys.filter(k=>['map30_west','map30_sun','map30_curtain'].includes(k)).length,noWesternGeography:!MAP30.land.some(q=>q.key==='west'),time:cmap2.t})")
  report['animation']=p.evaluate("""()=>{
   const get=XART.get,draw=ctx.drawImage,t=cmap2.t;let key='',calls=[];
   XART.get=function(k){key=k;return get.call(this,k);};
   ctx.drawImage=function(...a){if(key==='map30_flames'){const m=ctx.getTransform();calls.push({source:a.slice(1,5),dest:a.slice(5),transform:[m.a,m.b,m.c,m.d,m.e,m.f],alpha:ctx.globalAlpha});}return draw.apply(this,a);};
   ctx.save();ctx.setTransform(1,0,0,1,0,0);
   try{for(let i=0;i<9;i++){cmap2.t=(i+.25)/MAP30_FIRE.fps;map30SolarCurtain();}}
   finally{ctx.restore();ctx.drawImage=draw;XART.get=get;cmap2.t=t;}
   const first=calls[0],same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
   return {samples:calls.length,uniqueFrames:new Set(calls.map(q=>q.source.join(','))).size,
    fixedDestination:calls.every(q=>same(q.dest,first.dest)),
    fixedTransform:calls.every(q=>same(q.transform,first.transform)),
    fullDrawOpacity:calls.every(q=>q.alpha===1),loops:same(calls[0].source,calls[8].source),
    sourceRects:calls.map(q=>q.source),label:map30Labels.toString().includes('EAST COAST USA')};
  }""")
  report['organicEdge']=p.evaluate("""()=>{
   const c=document.createElement('canvas');c.width=256;c.height=512;
   const g=c.getContext('2d'),im=XART.get('map30_flames'),frames=[];
   for(let i=0;i<8;i++){
    g.clearRect(0,0,256,512);g.drawImage(im,(i%4)*256,Math.floor(i/4)*512,256,512,0,0,256,512);
    const data=g.getImageData(0,0,256,512).data,edges=[];let clear=0,solid=0;
    for(let j=3;j<data.length;j+=4){if(data[j]===0)clear++;if(data[j]>=250)solid++;}
    for(let y=8;y<504;y+=8){let last=-1;for(let x=0;x<256;x++)if(data[(y*256+x)*4+3]>128)last=x;if(last>=0)edges.push(last);}
    frames.push({transparentPixels:clear,densePixels:solid,edgeVariation:Math.max(...edges)-Math.min(...edges)});
   }
   const oldClip=ctx.clip;let clips=0;ctx.clip=function(...a){clips++;return oldClip.apply(this,a);};
   try{map30SolarCurtain();}finally{ctx.clip=oldClip;}
   const B=map30LockedBounds(),P=map30FireLayout(B);
   return {frames,noHardEdgeClip:clips===0,perimeterOverlapsOcean:P.x+P.w>B.right};
  }""")
  report['fallback']=p.evaluate("""()=>{
   const rdy=XART.rdy,fill=ctx.fillRect,draw=ctx.drawImage;let fills=[],draws=0;
   const B=map30LockedBounds();XART.rdy=function(k){return k==='map30_flames'?false:rdy.call(this,k);};
   ctx.fillRect=function(...a){fills.push({rect:a,alpha:ctx.globalAlpha});return fill.apply(this,a);};
   ctx.drawImage=function(...a){draws++;return draw.apply(this,a);};
   try{map30SolarCurtain();}finally{XART.rdy=rdy;ctx.fillRect=fill;ctx.drawImage=draw;}
   return {noImageDraw:draws===0,opaque:fills.length===1&&fills[0].alpha===1,
    coversRegion:JSON.stringify(fills[0].rect)===JSON.stringify([B.left,B.top,B.right-B.left,B.height])};
  }""")
  # Ignore text, ocean and other animated scenery; compare the fire itself.
  report['animatedPixelsChanged']=frames[0].crop((25,60,140,200)).tobytes()!=frames[1].crop((25,60,140,200)).tobytes()
  p.evaluate(sh.STEP,1);p.screenshot(path=str(O/'east_coast_usa.png'));b.close()
finally:stop()
frames[0].save(O/'east_coast_usa.webp',save_all=True,append_images=frames[1:],duration=83,loop=0,quality=85,method=4)
report['errors']=errors;(R/'docs/qa/east_coast_0930.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
assert not errors and report['retiredDraws']==0 and report['flameDraws']>0 and report['noWesternGeography'] and report['animatedPixelsChanged']
a=report['animation'];assert a['samples']==9 and a['uniqueFrames']==8 and all(a[k] for k in ['fixedDestination','fixedTransform','fullDrawOpacity','loops','label']),a
assert all(report['fallback'].values()),report['fallback']

e=report['organicEdge'];assert e['noHardEdgeClip'] and e['perimeterOverlapsOcean'] and all(f['transparentPixels']>1000 and f['densePixels']>1000 and f['edgeVariation']>20 for f in e['frames']),e
