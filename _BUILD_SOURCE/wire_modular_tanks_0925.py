"""Wire authored Stage 1/4/7 tank hull/turret pairs without repacking atlases."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()

def replace_once(old, new):
    global data
    before = old.encode("utf-8")
    assert data.count(before) == 1, (old[:100], data.count(before))
    data = data.replace(before, new.encode("utf-8"), 1)

replace_once(
    "  BOFX.img.frost_furious_beam_0920='assets/game/bosses/frost/frost_furious_beam_0920.png';",
    "  BOFX.img.frost_furious_beam_0920='assets/game/bosses/frost/frost_furious_beam_0920.png';\n"
    "  for(const _tankStage of [1,4,7])for(const _part of ['hull','turret'])\n"
    "    BOFX.img['overhaul_tank_'+_tankStage+'_'+_part]='assets/game/enemy_overhaul_0925/sprites/stage'+_tankStage+'_tank_'+_part+'.png';"
)
replace_once(
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);",
    "  /* Author-approved independently rotating jungle, desert and toxic armour. */\n"
    "  if(run.stage===1 && /^s1tank/.test(type)) c._modTank=1;\n"
    "  else if(run.stage===4 && (type==='sandtank'||type==='roadtank')) c._modTank=4;\n"
    "  else if(run.stage===7 && type==='s7tank') c._modTank=7;\n"
    "  if(c._modTank){c._modAngle=Math.PI/2;for(const _p of ['hull','turret'])XART.rdy('overhaul_tank_'+c._modTank+'_'+_p);}\n"
    "  if(typeof enemyShieldAutoEquip==='function')enemyShieldAutoEquip(c);"
)
replace_once(
    "    if(e.flash>0) e.flash-=dt;",
    "    if(e.flash>0) e.flash-=dt;\n"
    "    if(e._modTank) modularTankTick(e,dt);"
)
replace_once(
    "function tankMuzzle(e){ // fixed south-facing barrel: the art has no independently rotating turret\n  const aim=Math.PI/2;",
    "function tankMuzzle(e){ // authored modular tanks use the visible turret pivot\n"
    "  if(e._modTank)return modularTankMuzzle(e);\n"
    "  const aim=Math.PI/2;"
)
replace_once(
    "  if(e && e.type==='sandtank'){ try{ if(sandTankDraw(e)) return; }catch(_sde){} }",
    "  if(e && e._modTank && drawModularTank(e)) return;\n"
    "  if(e && e.type==='sandtank'){ try{ if(sandTankDraw(e)) return; }catch(_sde){} }"
)
replace_once(
    "function drawEnemy(e){",
    "function modularTankMuzzle(e){\n"
    "  const aim=Number.isFinite(e._modAngle)?e._modAngle:Math.PI/2;\n"
    "  const reach=e.w*.70;\n"
    "  return {x:e.x+Math.cos(aim)*reach,y:e.y+Math.sin(aim)*reach,aim};\n"
    "}\n"
    "function modularTankTick(e,dt){\n"
    "  if(e.dead)return;\n"
    "  const m=modularTankMuzzle(e),target=targetShip(m.x,m.y);\n"
    "  const want=Math.atan2(target.y-e.y,target.x-e.x);\n"
    "  const have=Number.isFinite(e._modAngle)?e._modAngle:Math.PI/2;\n"
    "  const delta=Math.atan2(Math.sin(want-have),Math.cos(want-have));\n"
    "  e._modAngle=have+clamp(delta,-dt*3.6,dt*3.6);\n"
    "}\n"
    "function drawModularTank(e){\n"
    "  if(!e._modTank||e.dead||e._dyingT!=null)return false;\n"
    "  const root='overhaul_tank_'+e._modTank+'_',hk=root+'hull',tk=root+'turret';\n"
    "  if(!XART.rdy(hk)||!XART.rdy(tk))return false;\n"
    "  const size=e.w*1.62,back=(e._kick||e._recoil||0)*3.0;\n"
    "  e._drawW=e.w;e._drawH=e.h;\n"
    "  ctx.save();ctx.imageSmoothingEnabled=false;\n"
    "  ctx.drawImage(XART.get(hk),e.x-size/2,e.y-size/2,size,size);\n"
    "  ctx.save();ctx.translate(e.x,e.y);ctx.rotate((e._modAngle||Math.PI/2)-Math.PI/2);\n"
    "  ctx.drawImage(XART.get(tk),-size/2,-size/2-back,size,size);\n"
    "  ctx.restore();\n"
    "  if(e.flash>0&&typeof xartTint==='function'){\n"
    "    const color=hitFlashColor(e,'#ffffff');\n"
    "    const h=xartTint(hk,color,.77),t=xartTint(tk,color,.77);\n"
    "    if(h)ctx.drawImage(h,e.x-size/2,e.y-size/2,size,size);\n"
    "    if(t){ctx.save();ctx.translate(e.x,e.y);ctx.rotate((e._modAngle||Math.PI/2)-Math.PI/2);ctx.drawImage(t,-size/2,-size/2-back,size,size);ctx.restore();}\n"
    "  }\n"
    "  ctx.restore();return true;\n"
    "}\n"
    "function drawEnemy(e){"
)
replace_once(
    "        eShoot(e.x, e.y+e.h*0.42, aimAt(e), 2.6, 'eshot');",
    "        {const m=e._modTank?modularTankMuzzle(e):{x:e.x,y:e.y+e.h*.42,aim:aimAt(e)};\n"
    "         eShoot(m.x,m.y,m.aim,2.6,'eshot');e._muz=.16;}"
)
replace_once(
    "        const mz={x:e.x, y:e.y+(e._bodyH||e.h||60)*0.46};\n        eShootT(mz.x, mz.y, Math.PI/2, 4.5, 's1bullet', {});",
    "        const mz=e._modTank?modularTankMuzzle(e):{x:e.x,y:e.y+(e._bodyH||e.h||60)*.46,aim:Math.PI/2};\n"
    "        eShootT(mz.x,mz.y,mz.aim,4.5,'s1bullet',{});"
)
replace_once(
    "          follow:()=>combatHardpoint(e,0,0.46)});",
    "          follow:()=>e._modTank?modularTankMuzzle(e):combatHardpoint(e,0,0.46)});"
)
replace_once(
    "      const mz={x:e.x, y:e.y+(e._bodyH||e.h||60)*0.46};\n      const cannon=e._atk==='cannon';\n      eShootT(mz.x, mz.y, Math.PI/2, cannon?3.8:3.05,",
    "      const mz=e._modTank?modularTankMuzzle(e):{x:e.x,y:e.y+(e._bodyH||e.h||60)*.46,aim:Math.PI/2};\n"
    "      const cannon=e._atk==='cannon';\n"
    "      eShootT(mz.x,mz.y,mz.aim,cannon?3.8:3.05,"
)
replace_once(
    "        follow:()=>combatHardpoint(e,0,0.46)});",
    "        follow:()=>e._modTank?modularTankMuzzle(e):combatHardpoint(e,0,0.46)});"
)
replace_once(
    "queue(()=>{const p=s7Hardpoint(e,0,.40),a=aim(p);for(const o of [-.08,-.04,0,.04,.08])fire(p,a+o,4.65,'s7shard',{silent:o>-.08});stage7Muzzle(e,0,.40,.62,.10);}",
    "queue(()=>{const p=e._modTank?modularTankMuzzle(e):s7Hardpoint(e,0,.40),a=e._modTank?p.aim:aim(p);for(const o of [-.08,-.04,0,.04,.08])fire(p,a+o,4.65,'s7shard',{silent:o>-.08});if(e._modTank)navalFlash(null,p,.62,BPFX_MUZZLE_VOID,{n:8,hpx:48,life:.10,follow:()=>modularTankMuzzle(e)});else stage7Muzzle(e,0,.40,.62,.10);}"
)
assert b"\r\n" not in data, "game.js must remain LF-only"
path.write_bytes(data)
print("Wired Stage 1/4/7 modular tank art, tracking, and actual muzzle origins")
