from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,json,sys,base64
R=Path(__file__).resolve().parents[1];S=Path(__file__).parent;O=R/'_shots/dialogue_fit_1020';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=1,pilot='cole'))
  p.wait_for_function('()=>{SC12.refresh();UI20.warm();return UI20_KEYS.every(k=>XART.rdy(k))&&bmfReady("dialogue")}')
  p.evaluate('''()=>{window.df20Paint=(o)=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.invalidate();SC12.refresh();dlgBox({...o,forceShown:true});return UI20.dialogue;};window.df20Fits=d=>{const inside=(a,b)=>a.x>=b.x-.01&&a.y>=b.y-.01&&a.x+a.w<=b.x+b.w+.01&&a.y+a.h<=b.y+b.h+.01;return inside(d.name,d)&&inside(d.text,d)&&(!d.portraitDraw||(inside(d.portraitDraw,d.portraitRect)&&Math.abs(d.portraitDraw.w/d.portraitDraw.h-XART.get(d.portrait).width/XART.get(d.portrait).height)<.01&&Math.abs(d.portraitDraw.x+d.portraitDraw.w/2-d.portraitRect.x-d.portraitRect.w/2)<.01&&Math.abs(d.portraitDraw.y+d.portraitDraw.h/2-d.portraitRect.y-d.portraitRect.h/2)<.01))&&d.layout.height<=d.text.h+.01&&d.layout.lines.every(s=>{msgFaceUse('dialogue');const fit=msgMeasure(s,d.layout.H)<=d.text.w+.01;msgFaceUse(null);return fit});};}''')
  pilots=p.evaluate('PILOTS.map(p=>p.key)')+['dracodia']
  text='We got him! Dracodia is down. Tell everyone it is finally over!'
  for pk in pilots:
   who=pk.upper();p.evaluate('pk=>{run.pilot=pk==="dracodia"?"cole":pk;commPortrait(run.pilot,"idle");commPortrait(run.pilot,"talk");XART.rdy(DP20.key)}',pk)
   p.wait_for_function('()=>XART.rdy(commPortrait(run.pilot,"idle"))&&XART.rdy(commPortrait(run.pilot,"talk"))&&XART.rdy(DP20.key)')
   o=dict(who=who,full=text,shown=text,pw=460,ph=130,x=10,y=360)
   if pk=='dracodia':o['portraitKey']=p.evaluate('DP20.key')
   d=p.evaluate('o=>df20Paint(o)',o)
   ck(who+' name, full dialogue and proportional portrait fit apertures',p.evaluate('df20Fits(UI20.dialogue)'),d)
   ck(who+' pilot color actually reaches centered nameplate glyphs',p.evaluate('''()=>{const d=UI20.dialogue,n=d.name,rgb=[1,3,5].map(i=>parseInt(d.color.slice(i,i+2),16)),box=ctx.getImageData(Math.floor(n.x*SS),Math.floor(n.y*SS),Math.ceil(n.w*SS),Math.ceil(n.h*SS));let l=box.width,r=0,t=box.height,b=0,count=0;for(let y=0;y<box.height;y++)for(let x=0;x<box.width;x++){const i=(y*box.width+x)*4;if(box.data[i+3]>220&&rgb.every((v,k)=>Math.abs(box.data[i+k]-v)<5)){l=Math.min(l,x);r=Math.max(r,x+1);t=Math.min(t,y);b=Math.max(b,y+1);count++;}}return count>2&&Math.abs((l+r)/2-box.width/2)<3&&Math.abs((t+b)/2-box.height/2)<3;}'''))
   (O/(pk+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for size in [(390,844),(1366,768),(1920,1080)]:
   p.set_viewport_size(dict(width=size[0],height=size[1]));p.evaluate('()=>{run.pilot="cole";window.__bofFit();}')
   for label,who,full,portrait in [('short','COLE',text,True),('long','JUGGERNAUT','Stay clear of the incoming ships! Roll through the first wave, save your somersault for the second volley, then focus your fire on the exposed central core. We can finish this together!',True),('hq','SPACE FEDERATION','All pilots, return to base. Digital black holes are opening above Earth. Enemy drones are hacking our systems!',False)]:
    o=dict(who=who,full=full,shown=full,pw=460,ph=130,x=10,y=360,portrait=portrait if portrait is False else who.lower())
    d=p.evaluate('o=>df20Paint(o)',o);ck(str(size)+' '+label+' no clipped rows or stretched portrait',p.evaluate('df20Fits(UI20.dialogue)'),d)
    if label=='short':p.screenshot(path=str(O/('native-'+str(size[0])+'.png')))
    if size[0]==390:(O/('narrow-'+label+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
   o=dict(who='COLE',full=text,shown=text[:12],pw=460,ph=130,x=10,y=360)
   before=p.evaluate('o=>df20Paint(o)',o);o['shown']=text;after=p.evaluate('o=>df20Paint(o)',o)
   ck(str(size)+' typing keeps the full sentence layout fixed',before['text']==after['text'] and before['layout']==after['layout'])
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);inv20Text("DRACODIA","YOUR VICTORY IS AN ILLUSION. I WILL RETURN.",VW,VH);}');d=p.evaluate('INV20.caption');ck(str(size)+' ending shares centered fitting geometry',p.evaluate('df20Fits(INV20.caption)'),d)
   p.screenshot(path=str(O/('ending-'+str(size[0])+'.png')))
  # A blank panel records the tint independently of text/portraits: compare native pixels
  # against the exact authored frame, and reject any tint outside the inset tab polygon.
  color=p.evaluate("""()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);const draw=ctx.drawImage,rect=ctx.fillRect;ctx.drawImage=ctx.fillRect=function(){};const r=ui20Panel('COLE',10,360,460,130,true);ctx.drawImage=draw;ctx.fillRect=rect;const a=ctx.getImageData(0,0,cv.width,cv.height),mask=document.createElement('canvas');mask.width=cv.width;mask.height=cv.height;const mg=mask.getContext('2d');mg.setTransform(SS,0,0,SS,0,0);ui20Polygon(mg,r.namePolygon);mg.fill();const pixels=mg.getImageData(0,0,mask.width,mask.height).data;let changed=0,outside=0;for(let i=0;i<a.data.length;i+=4)if(a.data[i+1]>20&&a.data[i+1]>a.data[i]+10){changed++;if(!pixels[i+3])outside++;}return{changed,outside};}""")
  ck('Native pilot tint stays within authored nameplate polygon',color['changed']>0 and color['outside']==0,color)
  edge=p.evaluate("""()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);const draw=ctx.drawImage,rect=ctx.fillRect;ctx.drawImage=ctx.fillRect=function(){};const r=ui20Panel('COLE',10,360,460,130,true);ctx.drawImage=draw;ctx.fillRect=rect;return [[495,47],[700,46],[700,109],[856,71],[869,82],[851,99],[477,92]].map(p=>{const q=p[0]<470?r.bay.point(...p):r.body.point(...p),d=ctx.getImageData(Math.round(q[0]*SS),Math.round(q[1]*SS),1,1).data;return {source:p,colored:d[1]>20&&d[1]>d[0]+10};});}""")
  ck('Tint reaches the top, bottom, left shoulder and entire angled nose',all(q['colored'] for q in edge),edge)
  ck('No native page, draw, console or missing-asset errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks);(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(not all(c['passed'] for c in checks))
