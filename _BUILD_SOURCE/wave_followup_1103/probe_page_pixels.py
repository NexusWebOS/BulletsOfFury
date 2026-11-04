from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
W=Path(__file__).parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102')
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800})
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.route('**/assets/game/shared/combat/sewer_pages_1103/*',lambda route:route.fulfill(path=str(W/'pages'/route.request.url.rsplit('/',1)[-1]),content_type='image/png'))
 p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
 for f in [R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js',O/'reference_wave_maps.js',O/'wave_observe_1102.js',W/'sewer_pages_art_1103.js',W/'sewer_pages_1103.js']:p.add_script_tag(path=str(f))
 p.evaluate('WO16.start(7)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000)
 keys=['s711_relay_hull','s711_relay_gun0','s711_barge_hull','s711_brood_hull','s711_brood_face','s711_slug','s711_slug_glow','r46_bf_sewerdrone']
 banks=p.evaluate('''keys=>{const all=[...Object.values(S711_ART.banks),...Object.values(R46_ART.models),...Object.values(R46_ORDNANCE.glyphs),...Object.values(R46_FEEDBACK.banks)];return keys.map(k=>all.find(B=>B.key===k)).filter(Boolean)}''',keys)
 checks=[]
 for bank in banks:
  p.wait_for_function('k=>XART.rdy(k)',arg=bank['key'],timeout=90000)
  p.evaluate('async k=>{const im=XART.get(k);if(im.decode)await im.decode();}',bank['key'])
  p.wait_for_timeout(50)
  result=p.evaluate('''B=>{
   const tests=[],paged=B.key.startsWith('s711_'),P=S7P113_ART.banks[B.key],c=ctx.canvas;
   // Exercise the original lazy source once before comparing settled pixels.
   for(let warm=0;warm<8;warm++){
    (paged?S7P113.base.v31:S7P113.base.r46)(B,0,Math.PI/2,240,260,100,null,1);
    (paged?v31Blit:r46Blit)(B,0,Math.PI/2,240,260,100,null,1);
    ctx.getImageData(100,100,280,300);
   }
   window.__pixelExample=null;
   for(const d of [0,Math.floor(B.dirs/2),B.dirs-1])for(const f of [0,Math.max(0,(B.frames||1)-1)])for(const style of ['normal','white','alpha']){
    const a=Math.PI/2+d*TAU/B.dirs,tint=style==='white'?'#ffffff':null,alpha=style==='alpha'?.52:1,size=B.cell*.371;
    function paint(old){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,c.width,c.height);
     if(paged)(old?S7P113.base.v31:v31Blit)(B,f,a,240.25,260.5,size,tint,alpha);else(old?S7P113.base.r46:r46Blit)(B,f,a,240.25,260.5,size,tint,alpha);
     return ctx.getImageData(100,100,280,300).data;}
    const before=paint(true),oldPNG=d===0&&f===0&&style==='normal'&&!window.__pixelExample?c.toDataURL():null,after=paint(false);if(oldPNG)window.__pixelExample={old:oldPNG,new:c.toDataURL()};let different=0,meaningful=0,max=0,premul=0,alphaDiff=0,oldLit=0,newLit=0;for(let i=0;i<before.length;i+=4){let delta=0;for(let j=0;j<4;j++)delta=Math.max(delta,Math.abs(before[i+j]-after[i+j]));if(delta){different++;max=Math.max(max,delta);}if(delta>2)meaningful++;for(let j=0;j<3;j++)premul=Math.max(premul,Math.abs(before[i+j]*before[i+3]/255-after[i+j]*after[i+3]/255));alphaDiff=Math.max(alphaDiff,Math.abs(before[i+3]-after[i+3]));if(before[i+3])oldLit++;if(after[i+3])newLit++;}
    tests.push({key:B.key,d,f,style,different,meaningful,max,premul,alphaDiff,oldLit,newLit});
   }return tests;
  }''',bank)
  checks.extend(result);print('PIXELS',bank['key'],'max changed',max(q['different']for q in result),flush=True)
  images=p.evaluate('window.__pixelExample')
  for style,uri in images.items():(W/(bank['key']+'-'+style+'.png')).write_bytes(base64.b64decode(uri.split(',')[1]))
  if hasattr(p,'wait_for_timeout'):p.wait_for_timeout(10)
 report={'checks':checks,'errors':errors,'bankCount':len(banks),'allExact':not any(q['different']for q in checks),'oldRootsInPreload':p.evaluate('()=>_stageLoads[7].keys.filter(k=>S7P113_ART.banks[k])')}
 (W/'page-pixels.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 assert not errors and max(q['meaningful']for q in checks)<=50 and max(q['alphaDiff']for q in checks)<=1 and not report['oldRootsInPreload'],report
 b.close();print('PASS',len(checks),'native pixel comparisons',flush=True)
