"""Palette-specific native pixel, hit-flash, emitter and owner verification."""
from pathlib import Path
import json,sys,copy
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from stage9_cases_1101 import CASES,SETUP
O=R/'_shots/stage9_palettes_1101';checks=[];errors=[]
old=json.loads((O/'before.json').read_text());new=json.loads((R/'assets/game/levels/stage_09/enemies/amplify_1101/manifest.json').read_text());names=set(new['palettes']['models'])
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',n,flush=True)
def geometry(x):
 if isinstance(x,dict):return{k:geometry(v)for k,v in x.items()if k!='sha256'}
 if isinstance(x,list):return[geometry(v)for v in x]
 return x
ck('All19 live shapes, banks, pivots and weapon sockets unchanged',geometry(old['models'])==geometry(new['models']))
ck('Nine retained models and all ordnance/exhaust keep exact source banks',all(old['models'][n]==new['models'][n]for n in old['models']if n not in names)and all(old['banks'][n]==b for n,b in new['banks'].items()if n.split('_')[0]not in names))
ck('Every palette export preserves exact frame alpha',len(new['paletteProof'])>40 and all(p['alphaPreserved']for p in new['paletteProof'].values()),len(new['paletteProof']))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(9,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s911Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){return window.allowS911?spawn.apply(this,arguments):null;};window.platePixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,blue=0,pink=0,lit=0;for(let i=0;i<a.length;i+=4){if(a[i+3]<100)continue;const r=a[i],g=a[i+1],b=a[i+2];if(r>235&&g>235&&b>235)white++;if(b>100&&b>r*1.3&&b>g*1.15)blue++;if(r>100&&r>g*1.3&&b>g*1.3)pink++;if(r+g+b>80)lit++;}return{white,blue,pink,lit};};}')
 for cid,typ,model,role,title,seconds in CASES:
  if model not in names:continue
  init=p.evaluate(SETUP,dict(type=typ,model=model,role=role))
  for j in range(28):
   q=p.evaluate('()=>{for(let i=0;i<24;i++)updatePlay(1/60);drawWorld(0);return{phase:E._s911.phase,hp:E.hp,events:S911.events.length};}');p.wait_for_timeout(2)
   if q['events']>4 and q['phase']in['fire','beam','pass','recover']:break
  p.screenshot(path=str(O/(model+'-native.png')))
  q=p.evaluate('()=>{const events=S911.events.filter(v=>["shot","beam-release"].includes(v.event)).length;E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;E.flash=0;const clean=platePixels(),hp=E.hp,shield=E._esh?.energy||0;hitEnemy(E,1);const damaged=platePixels();for(let i=0;i<32;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;const expired=platePixels();return{clean,damaged,expired,hp,after:E.hp,shield,afterShield:E._esh?.energy||0,flash:E.flash,events};}')
  family=new['palettes']['models'][model];ck(model+' real native palette pixels',q['clean']['lit']>150 and q['clean']['blue'if family=='black-blue'else'pink']>12,q['clean'])
  ck(model+' native damage flashes and expires',q['damaged']['white']>q['clean']['white']+10 and q['expired']['white']<q['damaged']['white']and q['flash']<=0 and(q['after']<q['hp']or q['afterShield']<q['shield']),q)
  ck(model+' native attack owner still fires',q['events']>0,q['events'])
 q=p.evaluate('()=>{const out=[];for(const name of Object.keys(S911_ART.palettes.models)){const M=S911_ART.models[name];for(const m of M.modules){const B=m.bank,f=m.bores?8:0,v=m.bores?.[f]||m.muzzle,a=s811Alpha({B,f,angle:Math.PI/2}),x=Math.round(B.cell/2+v[0]),y=Math.round(B.cell/2+v[1]);let alpha=0;for(let yy=y-3;yy<=y+3;yy++)for(let xx=x-3;xx<=x+3;xx++)if(xx>=0&&xx<B.cell&&yy>=0&&yy<B.cell)alpha=Math.max(alpha,a[(yy*B.cell+xx)*4+3]);out.push({name,alpha});}}return out;}');ck('Recolored modular gun mouths retain real source pixels',all(v['alpha']>80 for v in q),q)
 ck('No game, console or asset errors',not errors,errors);b.close()
print('SUMMARY',sum(v['passed']for v in checks),'/',len(checks));sys.exit(0 if all(v['passed']for v in checks)else 1)
