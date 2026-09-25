"""Mount authored fluid/exhaust reels and green laser FX on the sewer skimmer."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()

def replace_once(old, new):
    global data
    before = old.encode("utf-8")
    assert data.count(before) == 1, (old[:90], data.count(before))
    data = data.replace(before, new.encode("utf-8"), 1)

replace_once(
    "  for(const _jv of ['desert','black','snow'])",
    "  BOFX.img.overhaul_toxic_jet='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_jet_01.png';\n"
    "  for(let _tc=0;_tc<8;_tc++)BOFX.img['overhaul_toxic_core_'+_tc]='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_core_'+_tc+'.png';\n"
    "  for(let _te=0;_te<6;_te++)BOFX.img['overhaul_toxic_exhaust_'+_te]='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_exhaust_'+_te+'.png';\n"
    "  for(const _jv of ['desert','black','snow'])"
)
replace_once(
    "    if(c._modJet){c._modJetAngles={left:Math.PI/2,right:Math.PI/2};c._modJetFireSide=-1;",
    "    if(c._modJet){c._modJetAngles={left:Math.PI/2,right:Math.PI/2};c._modJetFireSide=-1;"
)
replace_once(
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);",
    "  if(run.stage===7&&type==='s7skimmer'){c._toxicJet=true;XART.rdy('overhaul_toxic_jet');XART.rdy('overhaul_toxic_core_0');XART.rdy('overhaul_toxic_exhaust_0');}\n"
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);"
)
replace_once(
    "function drawEnemy(e){",
    "function drawToxicJet(e){\n"
    "  if(!e._toxicJet||e.dead||e._dyingT!=null||!XART.rdy('overhaul_toxic_jet'))return false;\n"
    "  const hull='overhaul_toxic_jet',size=e.w*1.70,t=e._s7t||e.t||0;\n"
    "  const core='overhaul_toxic_core_'+(Math.floor(t*10)%8);\n"
    "  const exhaust='overhaul_toxic_exhaust_'+(Math.floor(t*13)%6);\n"
    "  e._drawW=e.w;e._drawH=e.h;ctx.save();ctx.imageSmoothingEnabled=false;\n"
    "  ctx.translate(e.x,e.y);ctx.rotate(e.spin||0);\n"
    "  for(const side of [-1,1])if(XART.rdy(exhaust)){\n"
    "    ctx.save();ctx.translate(side*size*.083,-size*.29);ctx.rotate(Math.PI);\n"
    "    ctx.drawImage(XART.get(exhaust),-size*.055,-size*.105,size*.11,size*.21);ctx.restore();\n"
    "  }\n"
    "  ctx.drawImage(XART.get(hull),-size/2,-size/2,size,size);\n"
    "  if(XART.rdy(core))ctx.drawImage(XART.get(core),-size*.066,-size*.214,size*.132,size*.178);\n"
    "  if(e.flash>0&&typeof xartTint==='function'){const f=xartTint(hull,hitFlashColor(e,'#ffffff'),.78);\n"
    "    if(f)ctx.drawImage(f,-size/2,-size/2,size,size);}\n"
    "  ctx.restore();return true;\n"
    "}\n"
    "function drawEnemy(e){"
)
replace_once(
    "  if(e && e._modJet && drawModularJet(e)) return;",
    "  if(e && e._modJet && drawModularJet(e)) return;\n"
    "  if(e && e._toxicJet && drawToxicJet(e)) return;"
)
replace_once(
    "function stage7Muzzle(e,ox,oy,scale,life){const p=s7Hardpoint(e,ox,oy);if(!p)return;\n  navalFlash(null,p,scale||.78,BPFX_MUZZLE_VOID,{n:8,hpx:48,life:life||.16,follow:()=>e&&!e.dead?s7Hardpoint(e,ox,oy):null});}",
    "function stage7Muzzle(e,ox,oy,scale,life){const p=s7Hardpoint(e,ox,oy);if(!p)return;\n"
    "  navalFlash(null,p,scale||.78,e._toxicJet?'weapon_muzzle_toxic':BPFX_MUZZLE_VOID,\n"
    "    {n:e._toxicJet?4:8,hpx:e._toxicJet?29:48,life:life||.16,follow:()=>e&&!e.dead?s7Hardpoint(e,ox,oy):null});}"
)
replace_once(
    "fire(p,Math.PI/2,2.45,'s7acid',{silent:x!==-.22});stage7Muzzle(e,x,.28,.60,.10);",
    "fire(p,Math.PI/2,x===0?4.15:2.45,x===0?'s7laser':'s7acid',{silent:x!==-.22});stage7Muzzle(e,x,.28,.60,.10);"
)
assert b"\r\n" not in data
path.write_bytes(data)
print("Wired Stage 7 toxic jet fluid, twin thrusters, green laser and muzzle")
