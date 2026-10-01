from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
from PIL import Image

repo=Path(__file__).resolve().parents[1]
out=repo/'_shots'/'east_coast_datawall_0930'
out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'_BUILD_SOURCE'))
import shoot
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=shoot.serve(str(repo))
errors=[]
report={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e: errors.append(str(e)))
  p.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate("()=>{run.mode='campaign';run.pilot='yuri';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.bonusUnlocked=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();}")
  p.wait_for_function("()=>Object.keys(MAP30_ART).every(k=>XART.rdy('map30_'+k))",timeout=60000)
  p.wait_for_timeout(2600)
  p.screenshot(path=str(out/'overview.png'))
  report['sheet']=p.evaluate("""()=>{
   const im=XART.get('map30_datawall'),c=document.createElement('canvas');
   c.width=512;c.height=1024;const g=c.getContext('2d'),frames=[];
   for(let i=0;i<4;i++){
    g.clearRect(0,0,512,1024);g.drawImage(im,i*512,0,512,1024,0,0,512,1024);
    const d=g.getImageData(0,0,256,512).data,edges=[];let clear=0,solid=0;
    for(let k=3;k<d.length;k+=4){if(d[k]===0)clear++;if(d[k]>=250)solid++;}
    for(let y=8;y<1016;y+=16){let density=0;for(let x=256;x<512;x++)if(d[(y*512+x)*4+3]>200)density++;edges.push(density);}
    frames.push({clear,solid,edgeVariation:Math.max(...edges)-Math.min(...edges),hash:d.reduce((a,b)=>(a*31+b)>>>0,0)});
   }
   return {size:[im.width,im.height],frames,source:MAP30_ART.datawall,fps:MAP30_DATA.fps};
  }""")
  report['animation']=p.evaluate("""()=>{
   const get=XART.get,draw=ctx.drawImage,t=cmap2.t;let key='',calls=[];
   XART.get=function(k){key=k;return get.call(this,k);};
   ctx.drawImage=function(...a){if(key==='map30_datawall')calls.push({source:a.slice(1,5),dest:a.slice(5)});return draw.apply(this,a);};
   try{for(let i=0;i<5;i++){cmap2.t=(i+.25)/MAP30_DATA.fps;map30DataWall();}}
   finally{ctx.drawImage=draw;XART.get=get;cmap2.t=t;}
   return {sources:calls.map(c=>c.source),fixedDest:calls.every(c=>JSON.stringify(c.dest)===JSON.stringify(calls[0].dest))};
  }""")
  report['locked']=p.evaluate("()=>({label:map30Labels.toString().includes('EAST COAST USA'),west:MAP30.westX,bonus:campaign.bonusUnlocked})")
  p.wait_for_timeout(700)
  p.screenshot(path=str(out/'second_frame.png'))
  report['errors']=errors
  b.close()
finally:
 stop()
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not errors,errors
assert report['sheet']['size']==[2048,1024]
assert len({f['hash'] for f in report['sheet']['frames']})==4
assert all(f['clear']>1000 and f['solid']>1000 and f['edgeVariation']>20 for f in report['sheet']['frames'])
assert len({tuple(s) for s in report['animation']['sources']})==4
assert report['animation']['fixedDest'] and report['locked']['label'] and not report['locked']['bonus']
