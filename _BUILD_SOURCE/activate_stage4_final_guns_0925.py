"""Arm and render the Sovereign's existing authored 25% twin-chaingun phase."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data

old = b"  if(threshold<=.501)stage4CoreTurretSpawnMissing(b,threshold);\n  b._phaseInvuln=Math.max(b._phaseInvuln||0,1.05);"
new = b"  if(threshold<=.501)stage4CoreTurretSpawnMissing(b,threshold);\n  if(threshold<=.251&&S.finalGuns==='off'){\n    S.finalGuns='deploying';S.finalGunT=0;S.finalGunShot=.30;\n    stage4WarfareSound('bossWeaponCharge','enemyBossCannon');\n  }\n  b._phaseInvuln=Math.max(b._phaseInvuln||0,1.05);"
assert data.count(old) == 1
data = data.replace(old, new)

old = b"  if(S.finalGuns!=='active')return;\n  /* Once calibrated, both sockets have unrestricted traverse."
new = b"  if(S.finalGuns!=='active'||S.shield&&S.shield.rearming)return;\n  /* Once calibrated, both sockets have unrestricted traverse."
assert data.count(old) == 1
data = data.replace(old, new)

old = b"  stage4GiantStrikeDraw(b);\n  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;"
new = b"""  stage4GiantStrikeDraw(b);
  if(!S.mini&&S.finalGuns!=='off'){
    /* The existing twin-socket core and rotating barrels share their hit/muzzle anchors.
       The gun's 150px length puts its drawn muzzle at the 76px firing reach. */
    const p=stage4FinalGunMount(b,-1),cy=p.y,
          alpha=S.finalGuns==='deploying'?clamp(S.finalGunT/.36,0,1):1,
          frame=Math.floor(S.finalGunSpin)%8,
          core='s4w_final_chaingun_core_'+frame,gun='s4w_final_chaingun_'+frame;
    ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha;
    if(XART.rdy(core))ctx.drawImage(XART.get(core),b.x-55,cy-55,110,110);
    if(XART.rdy(gun))for(const side of [-1,1]){
      const mount=stage4FinalGunMount(b,side);
      ctx.save();ctx.translate(mount.x,mount.y);
      ctx.rotate(stage4FinalGunAngle(b,side)-Math.PI/2);
      ctx.drawImage(XART.get(gun),-50,-75,100,150);ctx.restore();
    }
    ctx.restore();
  }
  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;"""
assert data.count(old) == 1
path.write_bytes(data.replace(old, new))
