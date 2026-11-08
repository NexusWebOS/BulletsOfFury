from pathlib import Path
import json,re,sys,random
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=R/'_shots/furious_perf_1104';W.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
art=json.loads((R/'assets/game/levels/stage_06/boss/performance_1104/manifest.json').read_text());bits=(R/'assets/game/levels/stage_06/boss/performance_1104/opaque_masks.bin').read_bytes();cases=[];rng=random.Random(1104)
for name,B in art['masks'].items():
 for n,m in enumerate(B['cells']):
  points=[(-1,0),(0,0),(B['cell']//2,B['cell']//2),(B['cell']-1,B['cell']-1)]
  if m:
   x,y,w,h,offset=m;points.extend([(x,y),(x+w-1,y+h-1),(x+w//2,y+h//2)])
   points.extend((rng.randrange(x,x+w),rng.randrange(y,y+h))for _ in range(8))
  for x,y in points:
   expected=False
   if m and m[0]<=x<m[0]+m[2]and m[1]<=y<m[1]+m[3]:
    index=(y-m[1])*m[2]+x-m[0];expected=bool(bits[m[4]+index//8]&(1<<(index%8)))
   cases.append([name,n//B['dirs'],n%B['dirs'],x,y,expected])
port,stop=serve(str(R));errors=[];checks=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("()=>{EA11.setup(6,'furious');spawnSubBoss('razorwake');}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000)
  result=p.evaluate('''rows=>{const failed=[];for(const [name,f,d,x,y,expected]of rows){const B=FB112_ART.banks[name],k=name==='razor_roll'?.6510416667:.48828125,a=Math.PI/2+d*TAU/B.dirs,px=240+(x+.5-B.cell/2)*k,py=250+(y+.5-B.cell/2)*k;const actual=fb112Opaque(name,f,a,k,240,250,px,py);if(actual!==expected&&failed.length<20)failed.push({name,f,d,x,y,actual,expected});}return{tested:rows.length,failed};}''',cases)
  checks.append(dict(name='Exact native opaque mask queries across every original pose',passed=not result['failed'],data=result))
  old=(R/'_BUILD_SOURCE/furious_perf_1104/before_controller.js').read_text();fn=re.search(r'function fb112Shadow\([\s\S]+?\nfunction fb112Draw\(',old)[0].rsplit('\nfunction fb112Draw(',1)[0]
  p.evaluate('()=>{window.qaOldShadow='+fn+';}')
  p.evaluate("()=>{XART.rdy('fb112_razor_body');XART.rdy('fb112_razor_roll');}");p.wait_for_function("()=>XART.rdy('fb112_razor_body')&&XART.rdy('fb112_razor_roll')",timeout=180000)
  parity=p.evaluate('''()=>{const results=[];for(const [name,f,d]of [['razor_body',0,0],['razor_body',2,4],['razor_body',0,16],['razor_roll',0,0],['razor_roll',4,3],['razor_roll',9,8],['razor_roll',17,11],['razor_roll',30,15]]){const B=FB112_ART.banks[name],a=Math.PI/2+d*TAU/B.dirs,k=225/B.cell;function draw(fn){FB112.shadows.clear();ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);fn(name,f,VW/2,VH/2,k,a);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}const before=draw(qaOldShadow),after=draw(fb112Shadow);let maxAlpha=0,maxPremult=0;for(let i=0;i<before.length;i+=4){maxAlpha=Math.max(maxAlpha,Math.abs(before[i+3]-after[i+3]));for(let c=0;c<3;c++)maxPremult=Math.max(maxPremult,Math.abs(before[i+c]*before[i+3]/255-after[i+c]*after[i+3]/255));}results.push({name,f,d,maxAlpha,maxPremult});}return results;}''')
  checks.append(dict(name='Authored shadows retain silhouette and displayed source colours',passed=all(r['maxAlpha']<=1 and r['maxPremult']<=1.01 for r in parity),data=parity));p.screenshot(path=str(W/'shadow-native.png'));b.close()
finally:stop()
checks.append(dict(name='No browser errors',passed=not errors,data=errors));(W/'pixel-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
