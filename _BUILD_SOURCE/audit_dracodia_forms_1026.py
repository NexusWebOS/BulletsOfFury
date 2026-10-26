from barrage_review_common_1025 import ROOT,boot
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
import json
O=ROOT/'_shots/dracodia_forms_1026/current';O.mkdir(parents=True,exist_ok=True)
errors=[];port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&rd29Ready()&&bi24Warm()}',timeout=180000)
  catalog=p.evaluate("""()=>({models:Object.fromEntries(Object.entries(V18_ART.models).map(([k,v])=>[k,{fps:v.fps,frames:v.frames.length,first:v.frames[0]}])),clips:Object.fromEntries(Object.entries(V19_ART.clips).map(([k,v])=>[k,{frames:v.frames.length,first:v.frames[0]}])),fx:Object.keys(D20_ART.fx),drfx:Object.keys(DR21_ART.banks),forms:V18.forms,glow:typeof PXG_STEPS!=='undefined'?PXG_STEPS:null})""")
  (O/'catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf8')
  details=[]
  for f in [0,8,1,6,2]:
   p.evaluate('(f)=>{v18Clear(boss);v18Enter(boss,2,f);boss._r30.v18.arenaPhase=2;v18Fight(boss);}',f)
   p.evaluate(STEP,1);p.screenshot(path=str(O/f'form-{f}-idle.png'))
   for i in range(24):p.evaluate(STEP,12);p.wait_for_timeout(1)
   p.screenshot(path=str(O/f'form-{f}-attack.png'))
   details.append(p.evaluate('({form:boss._r30.v18.form,mode:boss._r30.mode,hp:boss.hp,parts:boss.parts.map(p=>({id:p.id,hp:p.hp})),attack:boss._r30.v18.attack?.type,rig:v18Rig(boss).map(v=>({id:v.p.id,x:v.x,y:v.y,w:v.w,h:v.h,anchor:v.anchor,ax:v.ax,ay:v.ay,k:v.k,key:v.key,rot:v.rot}))})'))
  (O/'report.json').write_text(json.dumps({'details':details,'errors':errors},indent=2),encoding='utf8');br.close()
finally:stop()
print(json.dumps({'errors':errors[:2],'errorCount':len(errors),'forms':len(details)}))
