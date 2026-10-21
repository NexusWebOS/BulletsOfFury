from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot,probe_tutorial_1015 as old
O=R/'_shots/instructor_fit_1020';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,ok=bool(v),data=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
def step(p,n=1):return p.evaluate(old.STEPN,n)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport=dict(width=390,height=844));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');step(p,60);p.wait_for_function('XART.rdy("ic20_neutral")');step(p,30);p.screenshot(path=str(O/'invitation-390.png'));p.evaluate('Input.injectTap("j")');step(p,5);p.wait_for_function('BOFINSTRUCTOR.artReady');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for i in range(100):
   m=step(p,30)
   if m['state']=='play' and m['lesson']=='move':break
   p.wait_for_timeout(10)
  ck('Real tutorial entered',m['state']=='play' and m['lesson']=='move',m);print(m,flush=True)
  p.evaluate('''()=>{TD=null;TUT.i=TUT_LESSONS.findIndex(d=>d.id==='bob_card')-1;tutNext();TUT.typed=10000;TUT.L.age=5;}''')
  for width,height in [(390,844),(1366,768),(1920,1080),(768,1024)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('__bofFit()');step(p,3)
   for part in range(4):
    p.evaluate('i=>{TUT.L.sel=i;TUT.typed=10000;}',part);step(p,2)
    # Actual card text is drawn by the production fit helper into each authored safe aperture.
    fit=p.evaluate('''()=>{const D=IC20.cardLayout,M=D.model,rs=D.regions,out=[];for(const q of rs){const c=document.createElement('canvas');c.width=Math.ceil(q.rect.w)+8;c.height=Math.ceil(q.rect.h)+8;const g=c.getContext('2d');ui20Text(g,q.text,c.width/2,c.height/2,q.rect.h,q.rect.w,'center','#ffffff');const a=g.getImageData(0,0,c.width,c.height).data;let l=c.width,t=c.height,r=0,b=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(a[(y*c.width+x)*4+3]){l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x+1);b=Math.max(b,y+1);}out.push({text:q.text,w:q.rect.w,h:q.rect.h,ink:[l,t,r,b],fits:r-l<=Math.ceil(q.rect.w)+1&&b-t<=Math.ceil(q.rect.h)+1,centered:Math.abs((l+r)/2-c.width/2)<=1&&Math.abs((t+b)/2-c.height/2)<=1});}return{card:{x:D.x,y:D.y,w:D.w,h:D.h},model:M,rows:out,gap:M.y-(rs[2].rect.y+rs[2].rect.h),bottom:D.y+D.h,hintTop:VH-25};}''')
    ck(f'{width}x{height} part{part} all ten text blocks fit and center',len(fit['rows'])==10 and all(r['fits'] and r['centered'] for r in fit['rows']),fit)
    ck(f'{width}x{height} part{part} model clears title and card clears prompts',fit['gap']>=0 and fit['bottom']<=fit['hintTop'],dict(gap=fit['gap'],bottom=fit['bottom'],hintTop=fit['hintTop']))
    if width in [390,1366]:p.screenshot(path=str(O/f'card-{width}-{part}.png'))
   # All lesson sentences + runtime feedback strings at fully revealed budget.
   result=p.evaluate('''()=>{const texts=TUT_LESSONS.map(d=>({id:d.id,text:typeof d.text==='function'?d.text():d.text||''}));texts.push({id:'feedback',text:'REACTOR EXPOSED! FIRE BEATS ICE. A RETINA MISSILE HITS THIS CORE FOR DOUBLE DAMAGE.'});return texts.map(v=>{ic20Panel(v.text,v.text.length);const q=UI20.dialogue;return{id:v.id,lines:q.layout.lines.length,height:q.layout.height,room:q.text.h,fit:q.layout.height<=q.text.h&&q.layout.lines.every(line=>msgMeasure(line,q.layout.H)<=q.text.w+.1),rect:q.text};});}''')
   ck(f'{width}x{height} every lesson dialogue fits its inset',all(r['fit'] for r in result),result)
  portraits=p.evaluate('''()=>IC20_ART.portraits.map(a=>({key:a.key,path:a.path,ready:XART.rdy(a.key)}))''')
  ck('All four talking portrait states use black/red exports',all(q['ready'] and '-black-red.webp' in q['path'] for q in portraits),portraits)
  p.set_viewport_size(dict(width=390,height=844));p.evaluate('__bofFit()');p.evaluate('''()=>{TUT.i=TUT_LESSONS.findIndex(d=>d.id==='bob_card')-1;tutNext();TUT.L.age=5;TUT.typed=10000;}''');step(p,3);p.screenshot(path=str(O/'card-final-narrow.png'))
  # Real logical controls still select parts and confirm deployment.
  selected=p.evaluate('TUT.L.sel');p.evaluate('Input.injectTap("s")');step(p,2);ck('Part selection still uses native controls',p.evaluate('TUT.L.sel')!=selected)
  p.evaluate('Input.injectTap("j")');step(p,150);ck('Deploy still advances to the graduation fight',p.evaluate('TUT.L.def.id==="exam"'))
  p.evaluate('TUT.typed=10000');step(p,2);p.screenshot(path=str(O/'long-dialogue-390.png'))
  ck('No browser errors',not errors,errors);(O/'verification.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(dict(passed=sum(q['ok'] for q in checks),failed=sum(not q['ok'] for q in checks),errors=errors)),flush=True);raise SystemExit(bool(errors) or any(not q['ok'] for q in checks))
