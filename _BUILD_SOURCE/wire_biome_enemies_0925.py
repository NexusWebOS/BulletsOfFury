"""Use the approved generated biome plates on existing, fully authored enemy AI."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()


def replace_once(before: str, after: str) -> None:
    global data
    source = before.encode("utf-8")
    assert data.count(source) == 1, (before[:80], data.count(source))
    data = data.replace(source, after.encode("utf-8"), 1)


replace_once(
    "  BOFX.img.overhaul_toxic_jet='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_jet_01.png';",
    "  for(const _plate of ['stage2_fire_jet_01','stage2_fire_jet_02','stage3_ice_jet_01',"
    "'stage3_ice_jet_02','stage3_ice_drone_01','stage4_war_drone_01',"
    "'stage5_space_drone_01','stage6_storm_drone_01','stage7_slime_01',"
    "'stage8_alien_jet_01','stage8_alien_drone_01','stage9_water_jet_01',"
    "'stage9_water_alien_01','stage9_water_drone_01'])\n"
    "    BOFX.img['overhaul_'+_plate]='assets/game/enemy_overhaul_0925/sprites/'+_plate+'.png';\n"
    "  BOFX.img.overhaul_toxic_jet='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_jet_01.png';",
)

replace_once(
    "  if(c._modTurret){XART.rdy('overhaul_ground_base_'+c._modTurret.stage);XART.rdy('overhaul_ground_head_'+c._modTurret.weapon);}\n"
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);",
    "  if(c._modTurret){XART.rdy('overhaul_ground_base_'+c._modTurret.stage);XART.rdy('overhaul_ground_head_'+c._modTurret.weapon);}\n"
    "  /* Keep native movement, collision and attack logic; the new plate is visual only. */\n"
    "  const _biomeArtByStage={\n"
    "    2:{skim:'stage2_fire_jet_01',ash:'stage2_fire_jet_02'},\n"
    "    3:{s3interceptor:'stage3_ice_jet_01',s3barge:'stage3_ice_jet_02',s3mine:'stage3_ice_drone_01'},\n"
    "    4:{s4bomber:'stage4_war_drone_01'},\n"
    "    5:{s5repair:'stage5_space_drone_01'},\n"
    "    6:{s6probe:'stage6_storm_drone_01'},\n"
    "    7:{s7mine:'stage7_slime_01'},\n"
    "    8:{s8interceptor:'stage8_alien_jet_01',s8scout:'stage8_alien_drone_01'},\n"
    "    9:{s9interceptor:'stage9_water_jet_01',s9gunship:'stage9_water_alien_01',s9ring:'stage9_water_drone_01'}\n"
    "  };\n"
    "  const _biomePlate=_biomeArtByStage[run.stage]&&_biomeArtByStage[run.stage][type];\n"
    "  if(_biomePlate){c._biomePlate='overhaul_'+_biomePlate;XART.rdy(c._biomePlate);}\n"
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);",
)

replace_once(
    "function drawEnemy(e){",
    "function drawBiomeEnemyPlate(e){\n"
    "  if(!e._biomePlate||e.dead||e._dyingT!=null)return false;\n"
    "  const key=e._biomePlate;if(!XART.rdy(key))return false;\n"
    "  const image=XART.get(key);if(!image)return false;\n"
    "  const size=Math.max(e.w,e.h)*1.67,t=e.t||0;\n"
    "  e._drawW=size*.72;e._drawH=size*.72;\n"
    "  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(e.x,e.y);\n"
    "  if(key==='overhaul_stage7_slime_01'){\n"
    "    const pulse=1+Math.sin(t*5.2)*.045;ctx.scale(pulse,2-pulse);\n"
    "  }else ctx.rotate(e.spin||0);\n"
    "  ctx.drawImage(image,-size/2,-size/2,size,size);\n"
    "  if(e.flash>0&&typeof xartTint==='function'){\n"
    "    const tint=xartTint(key,hitFlashColor(e,'#ffffff'),.76);\n"
    "    if(tint)ctx.drawImage(tint,-size/2,-size/2,size,size);\n"
    "  }\n"
    "  ctx.restore();return true;\n"
    "}\n"
    "function drawEnemy(e){",
)
replace_once(
    "  if(e && e._modTurret && drawModularGroundTurret(e)) return;",
    "  if(e && e._modTurret && drawModularGroundTurret(e)) return;\n"
    "  if(e && e._biomePlate && drawBiomeEnemyPlate(e)) return;",
)
assert b"\r\n" not in data
path.write_bytes(data)
print("Wired fourteen generated biome plates to existing enemy AI")
