import json,base64,http.server
from pathlib import Path
import shoot as sh
from probe_stage7_modular_0927 import SETUP
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
OUT=Path('_shots/toxic_modular_0927');port,stop=sh.serve(sh.GAME);errors=[];report={}
def canvas(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(70)
  for mini in [True,False]:
   p.evaluate(SETUP,{'mini':mini});p.wait_for_function("()=>Object.keys(S7M_ART).map(k=>XART.rdy('s7m_'+k)).every(Boolean)",timeout=60000)
   report['tank' if mini else 'warden']=p.evaluate(r'''()=>{
    const out={};s7mSet(B,'recover');B.y=175;const M=B._s7mod,id=M.tank?'gunL':'frontL',part=M.parts.find(p=>p.id===id),pose=s7mPose(B).find(p=>p.id===id),q=s7mWorld(B,pose);
    const hp=part.hp;pBullets.push({x:q.x,y:q.y,vx:0,vy:0,w:4,h:8,dmg:17,t:0});updatePlay(1/60);out.bulletDamage=hp-part.hp;out.bulletHitPart=part.flash>0;
    const target=s7mTargets(B).find(t=>t._retinaId===id),h=part.hp;out.missileRouted=retinaMissileDamage(target,29,{kind:'missile',x:target.x,y:target.y});out.missileDamage=h-part.hp;
    const beam=s7mBeamImpact(B,{x:q.x,w:6,bot:450,top:0});out.beamPart=beam?.id;
    const x=part.hp;player.x=q.x;pBullets=[{kind:'beam',x:q.x,y:450,w:6,dmg:11,life:1,_hit:[],_ht:0,t:0}];updatePlay(1/60);out.nativeBeamDamage=x-part.hp;
    out.generated=Object.keys(S7M_ART).map(k=>({key:'s7m_'+k,ready:XART.rdy('s7m_'+k),width:XART.get('s7m_'+k).width}));
    return out;
   }''')
  p.evaluate("()=>{setState(GS.PASSWORD);drawPassword.sel=36;drawPassword.typing=false;Input.mouse.x=-999;Input.mouse.y=-999;}");p.evaluate(sh.STEP,2)
  sels=[]
  for key in ['ArrowRight','ArrowRight','ArrowRight','ArrowLeft','ArrowLeft','ArrowLeft']:
   p.keyboard.down(key);p.evaluate(sh.STEP,1);p.keyboard.up(key);p.evaluate(sh.STEP,1);sels.append(p.evaluate('()=>drawPassword.sel'))
  report['passwordSelections']=sels;canvas(p,'password_verified')
  p.evaluate("()=>{XART.rdy('bof_cover_b');XART.rdy('nbl_logo_0916');setState(GS.OPENER);opnI=OPN.length-1;opnT=4;}")
  p.wait_for_function("()=>XART.rdy('bof_cover_b')&&XART.rdy('nbl_logo_0916')");p.evaluate(sh.STEP,4);canvas(p,'cover_verified')
  p.evaluate('()=>setState(GS.TITLE)');p.evaluate(sh.STEP,3);canvas(p,'title_verified')
  report['cover']=p.evaluate("()=>({source:[XART.get('bof_cover_b').width,XART.get('bof_cover_b').height],canvas:[ctx.canvas.width,ctx.canvas.height],beats:OPN})")
  report['errors']=errors;(OUT/'contracts.json').write_text(json.dumps(report,indent=2));br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert report['passwordSelections']==[37,38,38,37,36,36],report['passwordSelections']
for k in ['tank','warden']:
 assert report[k]['bulletDamage']==17,report[k]
 assert report[k]['missileDamage']==29 and report[k]['missileRouted'],report[k]
 assert report[k]['nativeBeamDamage']==11,report[k]
