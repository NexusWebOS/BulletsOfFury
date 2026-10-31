from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;E=W/'source';E.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800})
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF)
  p.evaluate("()=>{for(const k of ['whv_closed_w','whv_open_w','s6cargo13_turrets',...Array.from({length:4},(_,i)=>CHAINGUN_POD_KEY+i)])XART.rdy(k);s7mWarm();r25Warm(7);}")
  p.wait_for_function("()=>['whv_closed_w','whv_open_w','s6cargo13_turrets',...Array.from({length:4},(_,i)=>CHAINGUN_POD_KEY+i)].every(k=>XART.rdy(k))&&Object.keys(S7M_ART).every(k=>XART.rdy('s7m_'+k))&&r25Warm(7)",timeout=180000)
  exports=p.evaluate("""()=>{
   const out={};function save(name,im){if(!im)return;const c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);out[name]=c.toDataURL().split(',')[1];}
   for(const k of ['whv_closed_w','whv_open_w','s6cargo13_turrets',...Array.from({length:4},(_,i)=>CHAINGUN_POD_KEY+i)])save(k,XART.get(k));
   for(const [name,indexes]of Object.entries({tank:[0,1,2],warden:[5,6,7],body:[0]}))for(const i of indexes)save(name+'_'+i,s7mCell(name,i,true));
   for(const name of Object.keys(R25_ART.legs))for(const f of R25_ART.legs[name].frames)save(f.key,XART.get(f.key));
   return{out,legs:R25_ART.legs,hh:typeof HH21_ART==='undefined'?null:HH21_ART};
  }""")
  for k,v in exports.pop('out').items():(E/(k+'.png')).write_bytes(base64.b64decode(v))
  (E/'metadata.json').write_text(json.dumps(exports,indent=2));b.close();print('Exported native component references',flush=True)
finally:stop()
