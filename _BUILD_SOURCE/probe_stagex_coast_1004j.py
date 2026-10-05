"""Native terrain/water pixels and real Stage X route ownership."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import base64, json, sys
import shoot as sh

R=Path(__file__).resolve().parents[1];O=R/'_shots/stagex_coast_1004j';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(v,n):
    checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def shot(p,n):
    (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1400,'height':980})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{map4hPreviewStorage();ht27Stop();debugFight=null;coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");diffKey="furious";DIFF=DIFFS.furious;stageXArenaReady();}')
  p.wait_for_function('()=>stageXArenaReady()',timeout=120000)
  for code in ['XHARR','XREBEL','HARR6','REBEL6']:
   p.evaluate('(code)=>{setState(GS.PASSWORD);pwInput=code;submitPassword();startRun(PENDING_STAGE);}',code)
   for i in range(6):
    p.evaluate('()=>{for(let i=0;i<20;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}');p.wait_for_timeout(10)
   info=p.evaluate('()=>({x:stageXArenaActive(),kind:boss.kind})')
   ck(info['x']==code.startswith('X'),code+' retains correct arena')
   ck(info['kind']==('rebelsquad' if 'REBEL' in code else 'warhive'),code+' retains encounter')
   shot(p,'arena-'+code)
  p.evaluate('()=>{run.stage=6;run._gp4StageX="left";window.__camera=stageXArenaSrcY;stageXArenaSrcY=()=>215;window.__get=XART.get;window.__keys=[];XART.get=function(k){__keys.push(k);return __get.call(this,k);};}')
  # Draw both samples through the game context, including its own cached XART canvases.
  info=p.evaluate('''()=>{
    ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);
    const img=XART.get('sx1001_arena'),W=worldWidth(),top=viewTopY(),h=viewH();
    ctx.drawImage(img,0,215,img.width||img.naturalWidth,h,0,top,W,h);
    const alpha=ctx.getImageData(0,0,cv.width,cv.height).data;
    const samples=[];
    for(let f=0;f<4;f++){
      sx1001T=10+f/6;ctx.clearRect(0,0,VW,VH);stageXArenaDraw(0);
      samples.push(ctx.getImageData(0,0,cv.width,cv.height).data);
    }
    let water=0,moving=0,land=0,stable=0,maxLandDelta=0;
    for(let i=0;i<alpha.length;i+=4){
      if(alpha[i+3]<3){water++;if(Math.max(...[0,1,2].map(c=>Math.abs(samples[0][i+c]-samples[1][i+c])))>8)moving++;}
      if(alpha[i+3]>=248){land++;const d=Math.max(...[0,1,2].map(c=>Math.abs(samples[0][i+c]-samples[1][i+c])));if(d<=5)stable++;maxLandDelta=Math.max(maxLandDelta,d);}
    }
    return {water,moving,land,stable,maxLandDelta,keys:[...new Set(__keys.filter(k=>k.startsWith('nwl_water')))],src:_masterSrcY,top,sy:stageXArenaSrcY(img)};
  }''')
  ck(info['water']>1000 and info['moving']/info['water']>.4,'transparent lagoon exposes visibly animated authored water')
  ck(info['land']>1000 and info['stable']/info['land']>.995,'mountain and city remain stable at fixed camera while water animates')
  ck(len(info['keys'])==4,'all four native water frames are drawn through XART and game context')
  ck(abs(info['src']-(info['sy']-info['top']))<.01,'arena preserves world/camera source alignment')
  for f in range(4):
   p.evaluate('(f)=>{sx1001T=10+f/6;ctx.setTransform(SS,0,0,SS,0,0);stageXArenaDraw(0);}',f);shot(p,'water-'+str(f))
  p.evaluate('()=>{stageXArenaSrcY=__camera;XART.get=__get;}')
  ims=[]
  for f in range(4):
   im=Image.open(O/('water-'+str(f)+'.png')).convert('RGB');im.thumbnail((480,720));ims.append(im)
  ims[0].save(O/'water-animation.gif',save_all=True,append_images=ims[1:],duration=166,loop=0)
  p.goto(f'http://127.0.0.1:{port}/_shots/stagex_coast_1004j/review.html',timeout=120000)
  frame=p.frame(url=lambda u:'stagex-coast-1004j-review' in u)
  frame.wait_for_function('()=>window.__bofFrames>4&&bossActive&&stageXArenaReady()',timeout=120000)
  for code in ['XREBEL','XHARR']:
   p.locator('[data-code="'+code+'"]').click();p.wait_for_timeout(150)
   ck(frame.evaluate('(code)=>stageXArenaActive()&&boss.kind===(code==="XREBEL"?"rebelsquad":"warhive")',code),'live review '+code+' button')
  ck(not errors,'zero page and console errors');b.close()
finally:stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors,'pixels':info},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks))
sys.exit(bool(errors) or any(not c['ok'] for c in checks))
