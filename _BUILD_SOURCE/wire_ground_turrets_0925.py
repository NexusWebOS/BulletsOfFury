"""Install authored biome bases and four independent rotating turret heads."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()

def replace_once(old, new):
    global data
    before = old.encode("utf-8")
    assert data.count(before) == 1, (old[:95], data.count(before))
    data = data.replace(before, new.encode("utf-8"), 1)

replace_once(
    "  BOFX.img.overhaul_toxic_jet='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_jet_01.png';",
    "  for(const _gs of [1,2,3,4,6,7,8])\n"
    "    BOFX.img['overhaul_ground_base_'+_gs]='assets/game/enemy_overhaul_0925/sprites/ground_base_stage'+_gs+'_'+({1:'jungle',2:'volcano',3:'ice',4:'desert',6:'city',7:'toxic',8:'alien'}[_gs])+'.png';\n"
    "  for(const _gh of ['mg','missile','laser','sonic'])\n"
    "    BOFX.img['overhaul_ground_head_'+_gh]='assets/game/enemy_overhaul_0925/sprites/ground_head_'+_gh+'.png';\n"
    "  BOFX.img.overhaul_toxic_jet='assets/game/enemy_overhaul_0925/sprites/stage7_toxic_jet_01.png';"
)
replace_once(
    "function _planSorted(P,stageNum){\n  if(Number.isFinite(stageNum)) difficultyElitePlan(P,stageNum);",
    "function modularGroundTurretPlan(P,stageNum){\n"
    "  if(![1,2,3,4,6,7,8].includes(stageNum)||!Array.isArray(P))return;\n"
    "  const rank=diffKey==='furious'?2:diffKey==='hard'?1:diffKey==='normal'?0:-1;\n"
    "  if(rank<0)return;\n"
    "  const count=rank===2?7:rank===1?4:2;\n"
    "  const roster={1:['mg','missile'],2:['missile','laser'],3:['laser','sonic'],\n"
    "    4:['mg','missile','laser'],6:['mg','laser','sonic'],7:['mg','laser','sonic'],\n"
    "    8:['missile','laser','sonic']}[stageNum];\n"
    "  const ts=P.map(w=>Number(w&&w.t)).filter(Number.isFinite);\n"
    "  const last=ts.length?Math.max(...ts):45;\n"
    "  const end=Math.max(20,Math.min(last*.78,(curStage&&curStage.length||last)*.70));\n"
    "  const start=stageNum===6?end*.45:Math.max(7,end*.21);\n"
    "  for(let i=0;i<count;i++){\n"
    "    const t=start+(end-start)*(i+.35)/(count+.2),weapon=roster[i%roster.length];\n"
    "    const fn=()=>modularGroundTurretSpawn(stageNum,weapon,i);\n"
    "    fn._modGroundTurret=true;fn._modGroundStage=stageNum;fn._modGroundWeapon=weapon;\n"
    "    P.push({t,fn});\n"
    "  }\n"
    "}\n"
    "function modularGroundTurretSpawn(stageNum,weapon,index){\n"
    "  if(!run||run.stage!==stageNum||bossActive||subBossActive)return null;\n"
    "  const W=worldWidth(),left=camLeftX(),right=camRightX();\n"
    "  const target=left+(index%2?.76:.24)*(right-left),mapY=levelSrcY()+42;\n"
    "  let x=null;\n"
    "  for(let d=0;d<=210;d+=14){\n"
    "    for(const s of d?[1,-1]:[1]){const q=clamp(target+s*d,left+26,right-26);\n"
    "      if(tankDrivable(q,mapY,false)){x=q;break;}}\n"
    "    if(x!=null)break;\n"
    "  }\n"
    "  /* Stages with continuous paved or built-up ground may not publish a tank mask.\n"
    "     Their flanking emplacement art is a visible stationary platform. */\n"
    "  if(x==null&&[4,6,7,8].includes(stageNum))x=target;\n"
    "  if(x==null)return null;\n"
    "  return spawnEnemy('modturret',x,-45,{_modStage:stageNum,_modWeapon:weapon,_modIndex:index});\n"
    "}\n"
    "function _planSorted(P,stageNum){\n"
    "  if(Number.isFinite(stageNum)){modularGroundTurretPlan(P,stageNum);difficultyElitePlan(P,stageNum);}"
)
replace_once(
    "    case 'turret':\n      c.w=26;c.h=26;c.hp=EHP(5);c.fireRate=1.3;c.score=400;c.color='#6b6b40';\n      c.vy=0.7; c.pattern='straight'; break;",
    "    case 'turret':\n"
    "      c.w=26;c.h=26;c.hp=EHP(5);c.fireRate=1.3;c.score=400;c.color='#6b6b40';\n"
    "      c.vy=0.7; c.pattern='straight'; break;\n"
    "    case 'modturret':\n"
    "      c.w=42;c.h=42;c.hp=c.maxhp=EHP(opt._modWeapon==='missile'?14:10);\n"
    "      c.score=opt._modWeapon==='sonic'?850:600;c.vy=0;c.pattern='ground';\n"
    "      c.ground=true;c.shoots=false;c.dropOk=true;c.art=null;\n"
    "      c._modTurret={stage:opt._modStage||run.stage,weapon:opt._modWeapon||'mg',\n"
    "        angle:Math.PI/2,mode:'wait',timer:.65+(opt._modIndex||0)*.08,shots:0};\n"
    "      break;"
)
replace_once(
    "                  racer:1,strafer:1,stationship:1,jungletank:1,roadtank:1,microturret:1,topgun:1,sideswirl:1,jetflyby:1,gunboat:1,",
    "                  racer:1,strafer:1,stationship:1,jungletank:1,roadtank:1,microturret:1,modturret:1,topgun:1,sideswirl:1,jetflyby:1,gunboat:1,"
)
replace_once(
    "if(!_vis && (c._dr||c._l6x||c._bcar||c._el8||c._volc||c._s3ice||c._s4chase||c._s6storm||c._sew||c._orb||c._el||",
    "if(!_vis && (c._modTurret||c._dr||c._l6x||c._bcar||c._el8||c._volc||c._s3ice||c._s4chase||c._s6storm||c._sew||c._orb||c._el||"
)
replace_once(
    "  if(run.stage===7&&type==='s7skimmer'){c._toxicJet=true;XART.rdy('overhaul_toxic_jet');XART.rdy('overhaul_toxic_core_0');XART.rdy('overhaul_toxic_exhaust_0');}",
    "  if(run.stage===7&&type==='s7skimmer'){c._toxicJet=true;XART.rdy('overhaul_toxic_jet');XART.rdy('overhaul_toxic_core_0');XART.rdy('overhaul_toxic_exhaust_0');}\n"
    "  if(c._modTurret){XART.rdy('overhaul_ground_base_'+c._modTurret.stage);XART.rdy('overhaul_ground_head_'+c._modTurret.weapon);}"
)
replace_once(
    "    if(e._modJet) modularJetTick(e,dt);",
    "    if(e._modJet) modularJetTick(e,dt);\n"
    "    if(e._modTurret) modularGroundTurretTick(e,dt);"
)
replace_once(
    "function drawEnemy(e){",
    "function modularGroundTurretMuzzle(e){\n"
    "  const T=e._modTurret,a=T.angle,r=e.w*.43;\n"
    "  return {x:e.x+Math.cos(a)*r,y:e.y+Math.sin(a)*r,aim:a};\n"
    "}\n"
    "function modularGroundTurretTick(e,dt){\n"
    "  const T=e._modTurret;if(!T||e.dead)return;\n"
    "  const p=modularGroundTurretMuzzle(e),target=targetShip(p.x,p.y);\n"
    "  const want=Math.atan2(target.y-e.y,target.x-e.x);\n"
    "  const delta=Math.atan2(Math.sin(want-T.angle),Math.cos(want-T.angle));\n"
    "  T.angle+=clamp(delta,-dt*2.8,dt*2.8);\n"
    "  if(e.y<32||e.y>VH-44||bossActive||subBossActive)return;\n"
    "  T.timer-=dt;if(T.timer>0)return;\n"
    "  if(T.mode==='wait'){T.mode='tell';T.timer=T.weapon==='sonic'?.93:T.weapon==='laser'?.75:.58;return;}\n"
    "  if(T.mode==='tell'){T.mode='burst';T.shots=T.weapon==='mg'?4:T.weapon==='missile'?2:1;T.timer=0;}\n"
    "  if(T.mode!=='burst')return;\n"
    "  const m=modularGroundTurretMuzzle(e),w=T.weapon,kind=w==='mg'?'mg':w==='missile'?'s4missile':\n"
    "    w==='sonic'?'rzbSonic':T.stage===3?'s3lance':T.stage===7?'s7laser':'s4rail';\n"
    "  const gap=w==='mg'?.11:w==='missile'?.20:.20;\n"
    "  const offsets=w==='sonic'?[-.16,0,.16]:[0];\n"
    "  for(const off of offsets)eShootT(m.x,m.y,m.aim+off,w==='mg'?4.2:w==='missile'?2.45:w==='sonic'?3.0:5.0,kind,\n"
    "    {w:w==='sonic'?15:w==='mg'?6:10,h:w==='sonic'?15:w==='mg'?15:26,silent:off!==0});\n"
    "  const family='weapon_muzzle_'+(w==='mg'?'rotary':w==='missile'?'missile':T.stage===7?'toxic':'laser');\n"
    "  navalFlash(null,m,.70,family,{n:4,hpx:32,life:.14,follow:()=>e&&!e.dead?modularGroundTurretMuzzle(e):null});\n"
    "  e._muz=.15;T.shots--;\n"
    "  if(T.shots>0)T.timer=gap;\n"
    "  else {T.mode='wait';T.timer=(w==='mg'?2.0:w==='missile'?3.2:w==='sonic'?3.6:2.8)/\n"
    "      (diffKey==='furious'?1.25:diffKey==='hard'?1.1:1);}\n"
    "}\n"
    "function drawModularGroundTurret(e){\n"
    "  const T=e._modTurret;if(!T||e.dead||e._dyingT!=null)return false;\n"
    "  const bk='overhaul_ground_base_'+T.stage,hk='overhaul_ground_head_'+T.weapon;\n"
    "  if(!XART.rdy(bk)||!XART.rdy(hk))return false;\n"
    "  const bs=e.w*1.27,hs=e.w*.96;\n"
    "  ctx.save();ctx.imageSmoothingEnabled=false;\n"
    "  ctx.drawImage(XART.get(bk),e.x-bs/2,e.y-bs/2,bs,bs);\n"
    "  ctx.translate(e.x,e.y);ctx.rotate(T.angle-Math.PI/2);\n"
    "  ctx.drawImage(XART.get(hk),-hs/2,-hs/2,hs,hs);\n"
    "  if(T.mode==='tell'){const p=clamp(1-T.timer/(T.weapon==='sonic'?.93:T.weapon==='laser'?.75:.58),0,1);\n"
    "    const ck='weapon_muzzle_'+(T.weapon==='missile'?'missile':T.stage===7?'toxic':'laser')+'_0';\n"
    "    if(XART.rdy(ck)){ctx.globalAlpha=.22+p*.46;ctx.drawImage(XART.get(ck),-hs*.20,hs*.25,hs*.40,hs*.40);ctx.globalAlpha=1;}}\n"
    "  ctx.restore();\n"
    "  if(e.flash>0&&typeof xartTint==='function'){const f=xartTint(bk,hitFlashColor(e,'#ffffff'),.76);\n"
    "    if(f)ctx.drawImage(f,e.x-bs/2,e.y-bs/2,bs,bs);}\n"
    "  ctx.restore();return true;\n"
    "}\n"
    "function drawEnemy(e){"
)
replace_once(
    "  if(e && e._toxicJet && drawToxicJet(e)) return;",
    "  if(e && e._toxicJet && drawToxicJet(e)) return;\n"
    "  if(e && e._modTurret && drawModularGroundTurret(e)) return;"
)
replace_once(
    "const SCORCH_GROUND={tank:1,htank:1,jungletank:1,mgturret:1,rockturret:1,turret:1,microturret:1,",
    "const SCORCH_GROUND={tank:1,htank:1,jungletank:1,mgturret:1,rockturret:1,turret:1,microturret:1,modturret:1,"
)
replace_once(
    "const _GROUND={tank:1,htank:1,jungletank:1,mgturret:1,rockturret:1,turret:1,microturret:1,turdrone:1};",
    "const _GROUND={tank:1,htank:1,jungletank:1,mgturret:1,rockturret:1,turret:1,microturret:1,modturret:1,turdrone:1};"
)
assert b"\r\n" not in data
path.write_bytes(data)
print("Wired ground turret art, attack state machines and stage-frequency plan")
