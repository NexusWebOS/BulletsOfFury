"""Measure the live Hammer recovery reel and export its exact XART source.

Writes only this key's usage entry and ignored source PNG. Then run
pixel_glow_1015.py --keys=arch_storm_charge_0926 to refresh its companions.
Uses the native reel's physical core/head anchors; no alternate boss forms.
"""
from pathlib import Path
import sys,ast,json,base64
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
(R/'_shots/boss_repairs_1016').mkdir(parents=True,exist_ok=True)
import shoot
from playwright.sync_api import sync_playwright
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=5,kind='chromehammer',pilot='cole',diff='normal'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&XART.rdy("arch_storm_charge_0926")}')
  p.evaluate('''()=>{story=fb2Talk=null;BOFCinematicDirector.cancel();stagePlan=[];VP12.next=CP12.next=EP13.next=9999;player.invuln=1e9;
   B.enter=false;B._be=null;B.hp=B.maxhp*.6;B._phaseInvuln=0;B._noHit=false;fr27BeginArmor(B);B._hammer.frArmor.activated=true;B._noHit=false;fr27Restore(B,.1,false,false);
   window.chargeUsage={n:0,st:[5],scope:['boss'],rects:[],scale:0,tints:{}};window.chargeRectSet=new Set();const draw=ctx.drawImage;
   ctx.drawImage=function(im,...args){const t=PXG.tags.get(im);if(t?.key==='arch_storm_charge_0926'&&!PXG.drawing){
    const a=[im,...args],n=a.length,iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height;
    const sx=n>=9?a[1]:0,sy=n>=9?a[2]:0,sw=n>=9?a[3]:iw,sh=n>=9?a[4]:ih,dw=n>=9?a[7]:n>=5?a[3]:iw;
    const r=[Math.round(t.ax*sx+t.bx),Math.round(t.ay*sy+t.by),Math.round(t.ax*(sx+sw)+t.bx),Math.round(t.ay*(sy+sh)+t.by)];
    chargeRectSet.add(r.join(','));chargeUsage.n++;chargeUsage.scale+=Math.hypot(this.getTransform().a,this.getTransform().b)*dw/(t.ax*sw);}
    return draw.call(this,im,...args);};}''')
  for i in range(18):
   p.evaluate('()=>{for(let j=0;j<30;j++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0)}}');p.wait_for_timeout(10)
  info=p.evaluate('()=>({...chargeUsage,rects:[...chargeRectSet].map(k=>k.split(",").map(Number)),scale:chargeUsage.scale/chargeUsage.n,emitters:HAMMER_CHARGE_REEL.flatMap(r=>[{kind:"core",center:[r[4],r[5]],radius:[32,32]},{kind:"hammer",center:[r[6],r[7]],radius:[66,70]}])})')
  raw=p.evaluate('()=>{const im=XART.get("arch_storm_charge_0926"),c=document.createElement("canvas");c.width=im.width;c.height=im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL().split(",")[1]}')
  assert info['n']>20 and not errors,(info,errors)
  out=R/'_shots/glow_usage_1015/src';out.mkdir(parents=True,exist_ok=True);(out/'arch_storm_charge_0926.png').write_bytes(base64.b64decode(raw))
  f=R/'_BUILD_SOURCE/glow_usage_1015.json';usage=json.loads(f.read_text());usage['keys']['arch_storm_charge_0926']=info;usage['dropped_fx'].pop('arch_storm_charge_0926',None);f.write_bytes((json.dumps(usage,indent=0)+'\n').encode())
  (R/'_shots/boss_repairs_1016/charge_usage.json').write_text(json.dumps(info,indent=2));print(info,flush=True);b.close()
finally:stop()
