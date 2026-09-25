"""Wire three Stage-4 modular jet variants and their authored weapon FX."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()

def replace_once(old, new):
    global data
    before = old.encode("utf-8")
    assert data.count(before) == 1, (old[:100], data.count(before))
    data = data.replace(before, new.encode("utf-8"), 1)

replace_once(
    "  for(const _tankStage of [1,4,7])for(const _part of ['hull','turret'])",
    "  for(const _jv of ['desert','black','snow'])\n"
    "    BOFX.img['overhaul_jet_'+_jv+'_hull']='assets/game/enemy_overhaul_0925/sprites/stage4_jet_'+_jv+'_hull.png';\n"
    "  for(const _jm of ['missile','laser'])\n"
    "    BOFX.img['overhaul_jet_'+_jm+'_module']='assets/game/enemy_overhaul_0925/sprites/stage4_jet_'+_jm+'_module.png';\n"
    "  for(let _jf=0;_jf<4;_jf++){\n"
    "    BOFX.img['overhaul_jet_rotary_module_'+_jf]='assets/game/enemy_overhaul_0925/sprites/stage4_jet_rotary_module_'+_jf+'.png';\n"
    "    for(const _fam of ['rotary','missile','laser','toxic'])\n"
    "      BOFX.img['weapon_muzzle_'+_fam+'_'+_jf]='assets/game/enemy_overhaul_0925/sprites/weapon_muzzle_'+_fam+'_'+_jf+'.png';\n"
    "  }\n"
    "  for(const _tankStage of [1,4,7])for(const _part of ['hull','turret'])"
)
replace_once(
    "  if(c._modTank){c._modAngle=Math.PI/2;for(const _p of ['hull','turret'])XART.rdy('overhaul_tank_'+c._modTank+'_'+_p);}",
    "  if(c._modTank){c._modAngle=Math.PI/2;for(const _p of ['hull','turret'])XART.rdy('overhaul_tank_'+c._modTank+'_'+_p);}\n"
    "  if(run.stage===4){\n"
    "    c._modJet=type==='s4interceptor'?'desert':type==='s4heavyjet'?'black':type==='s4command'?'snow':null;\n"
    "    if(c._modJet){c._modJetAngles={left:Math.PI/2,right:Math.PI/2};c._modJetFireSide=-1;\n"
    "      XART.rdy('overhaul_jet_'+c._modJet+'_hull');\n"
    "      XART.rdy(c._modJet==='desert'?'overhaul_jet_rotary_module_0':'overhaul_jet_'+(c._modJet==='black'?'missile':'laser')+'_module');}\n"
    "  }"
)
replace_once(
    "    if(e._modTank) modularTankTick(e,dt);",
    "    if(e._modTank) modularTankTick(e,dt);\n"
    "    if(e._modJet) modularJetTick(e,dt);"
)
replace_once(
    "function drawEnemy(e){",
    "function modularJetMount(e,side){\n"
    "  const s=e.spin||0,ox=side*e.w*.33,oy=e.h*.12;\n"
    "  return {x:e.x+ox*Math.cos(s)-oy*Math.sin(s),y:e.y+ox*Math.sin(s)+oy*Math.cos(s)};\n"
    "}\n"
    "function modularJetPoint(e,side){\n"
    "  const p=modularJetMount(e,side),key=side<0?'left':'right';\n"
    "  const aim=e._modJetAngles?e._modJetAngles[key]:Math.PI/2;\n"
    "  const reach=e.w*.18;return {x:p.x+Math.cos(aim)*reach,y:p.y+Math.sin(aim)*reach,aim};\n"
    "}\n"
    "function modularJetTick(e,dt){\n"
    "  if(e.dead)return;\n"
    "  for(const side of [-1,1]){\n"
    "    const key=side<0?'left':'right',p=modularJetMount(e,side),target=targetShip(p.x,p.y);\n"
    "    const want=Math.atan2(target.y-p.y,target.x-p.x),have=e._modJetAngles[key];\n"
    "    const delta=Math.atan2(Math.sin(want-have),Math.cos(want-have));\n"
    "    e._modJetAngles[key]=have+clamp(delta,-dt*4.4,dt*4.4);\n"
    "  }\n"
    "}\n"
    "function drawModularJet(e){\n"
    "  if(!e._modJet||e.dead||e._dyingT!=null)return false;\n"
    "  const hull='overhaul_jet_'+e._modJet+'_hull';\n"
    "  const module=e._modJet==='desert'?'overhaul_jet_rotary_module_'+((e._muz>0)?Math.floor((e.t||0)*18)%4:0):\n"
    "    'overhaul_jet_'+(e._modJet==='black'?'missile':'laser')+'_module';\n"
    "  if(!XART.rdy(hull)||!XART.rdy(module))return false;\n"
    "  const size=Math.max(e.w,e.h)*1.30,ms=Math.max(19,e.w*.38);\n"
    "  e._drawW=size;e._drawH=size;\n"
    "  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(e.x,e.y);ctx.rotate(e.spin||0);\n"
    "  ctx.drawImage(XART.get(hull),-size/2,-size/2,size,size);ctx.restore();\n"
    "  for(const side of [-1,1]){const p=modularJetMount(e,side),a=e._modJetAngles[side<0?'left':'right'];\n"
    "    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);\n"
    "    ctx.drawImage(XART.get(module),-ms/2,-ms/2,ms,ms);ctx.restore();}\n"
    "  if(e.flash>0&&typeof xartTint==='function'){const h=xartTint(hull,hitFlashColor(e,'#ffffff'),.74);\n"
    "    if(h){ctx.save();ctx.translate(e.x,e.y);ctx.rotate(e.spin||0);ctx.drawImage(h,-size/2,-size/2,size,size);ctx.restore();}}\n"
    "  ctx.restore();return true;\n"
    "}\n"
    "function drawEnemy(e){"
)
replace_once(
    "  if(e && e._modTank && drawModularTank(e)) return;",
    "  if(e && e._modTank && drawModularTank(e)) return;\n"
    "  if(e && e._modJet && drawModularJet(e)) return;"
)
replace_once(
    "function s4Hardpoint(e,ox,oy){return combatHardpoint(e,ox,oy);}",
    "function s4Hardpoint(e,ox,oy){\n"
    "  if(e._modJet)return modularJetPoint(e,ox<0?-1:ox>0?1:e._modJetFireSide||-1);\n"
    "  return combatHardpoint(e,ox,oy);\n"
    "}"
)
replace_once(
    "  const _fam=fam===MUZZLE_MG?BPFX_MUZZLE_KINETIC:BPFX_MUZZLE_MISSILE;\n  navalFlash(null,p,scale||.82,_fam,{n:8,hpx:46,life:life||.15,",
    "  const _fam=e._modJet?'weapon_muzzle_'+(e._modJet==='desert'?'rotary':e._modJet==='black'?'missile':'laser'):\n"
    "    fam===MUZZLE_MG?BPFX_MUZZLE_KINETIC:BPFX_MUZZLE_MISSILE;\n"
    "  navalFlash(null,p,scale||.82,_fam,{n:e._modJet?4:8,hpx:e._modJet?30:46,life:life||.15,"
)
replace_once(
    "queue(()=>{const p=s4Hardpoint(e,0,.36),a=aim(p);for(const o of [-.07,0,.07])fire(p,a+o,4.8,'s4brass'",
    "queue(()=>{e._modJetFireSide=-(e._modJetFireSide||1);const p=s4Hardpoint(e,0,.36),a=e._modJet?p.aim:aim(p);for(const o of [-.07,0,.07])fire(p,a+o,4.8,'s4brass'"
)
replace_once(
    "const p=s4Hardpoint(e,side*.30,.21);for(const o of [-.26,-.13,0,.13,.26])if(Math.sign(o||side)===side||o===0)fire(p,Math.PI/2+o*e._fan,3.0,'s4rail'",
    "const p=s4Hardpoint(e,side*.30,.21);for(const o of [-.26,-.13,0,.13,.26])if(Math.sign(o||side)===side||o===0)fire(p,(e._modJet?p.aim:Math.PI/2)+o*e._fan,3.0,'s4rail'"
)
replace_once(
    "const p=s4Hardpoint(e,side*.31,.20),a=aim(p);fire(p,a+side*.10,2.15,'s4missile'",
    "const p=s4Hardpoint(e,side*.31,.20),a=e._modJet?p.aim:aim(p);fire(p,a+side*.10,2.15,'s4missile'"
)
assert b"\r\n" not in data
path.write_bytes(data)
print("Wired desert rotary, black missile and snow laser modular jets")
