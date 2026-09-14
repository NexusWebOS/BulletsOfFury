from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parents[2];O=R/'_shots/supply_audit_0914';p=R/'assets/game.js';current=p.read_bytes();b=(O/'game.before.js').read_bytes()if(O/'game.before.js').exists()else current
assert hashlib.sha256(b).hexdigest()=='e2e95dfbd9e0d65bfe55ac40d4989f3be1aba6d3ad4f33c9c89efe5f57674533'
if not(O/'game.before.js').exists():
 (O/'game.before.js').write_bytes(b);(O/'test.before.js').write_bytes((R/'_BUILD_SOURCE/test_fl.js').read_bytes())
s=b.decode('utf-8')
def edit(a,z):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,z)
edit("   Decker keeps his pilot name until Mike supplies the ninth model. */", "   Mike named Decker's model Draven on 0914. */")
edit("axel:'Aristotle',freezer:'Falcon'};", "axel:'Aristotle',freezer:'Falcon',decker:'Draven'};")
edit("""    // Original death drops: 6.2% ammo, 2.8% shield, 1% life. Add the life
    // bonus in a separate interval so extra lives do not steal ammo/shield rolls.
    const roll=Math.random(),extraLife=lifeDropChance(.01)-.01;
    if(roll>.10+extraLife)return;
    if(roll>.10)kind='life';
    else {const r=Math.random();kind=r<.62?'bomb':(r<.9?'shield':'life');}""", """    // Original death drops: 6.2% ammo, 2.8% shield, 1% life. Independent
    // bonus intervals preserve the original grants and each other's probability.
    const roll=Math.random(),extraLife=lifeDropChance(.01)-.01,extraAmmo=.062*(missileSupplyRate()-1);
    if(roll>.10+extraLife+extraAmmo)return;
    if(roll>.10+extraLife)kind='bomb';
    else if(roll>.10)kind='life';
    else {const r=Math.random();kind=r<.62?'bomb':(r<.9?'shield':'life');}""")
edit("  else if(type==='mcrate') powerups.push({x,y:-30,vy:0.85,t:0,kind:'mcrate',hp:6,flash:0,w:48,h:44,bob:rnd(0,TAU)});", "  else if(type==='mcrate'){\n    powerups.push({x:rnd(camLeftX()+40,camRightX()-40),y:-30,vy:0.85,t:0,kind:'mcrate',hp:6,flash:0,w:48,h:44,bob:rnd(0,TAU)});\n    missileSupplyBonusRoll();\n  }")
edit("  run.contUsed=0;   // continue counter resets per RUN, not per stage (drop 0805b)", "  run.contUsed=0;   // continue counter resets per RUN, not per stage (drop 0805b)\n  run._missileBonus=null;")
edit("  run.mode='campaign';\n  run.pilot=s.pilot||run.pilot;", "  run.mode='campaign';run._missileBonus=null;\n  run.pilot=s.pilot||run.pilot;")
edit('  bossMissileSupplyTick(dt);','  missileSupplyBonusTick(dt);\n  bossMissileSupplyTick(dt);')
edit('function bossMissileSupplyTick(dt){',"""function missileSupplyRate(){return diffKey==='hard'||diffKey==='furious'?1.25:1;}
function missileSupplyOnScreen(){return powerups.some(p=>!p.dead&&(p.kind==='mcrate'||/^missilepack/.test(p.kind)));}
/* Scheduled and guaranteed phase crates have finite authored events, not a
   repeating clock. Each gets one 25% bonus-crate roll on Hard/Furious. Earned
   extras wait two active seconds and for existing missile boxes to clear.
   Boss clock supplies and bonus supplies never roll again (no double bonus). */
function missileSupplyBonusRoll(){
  if(missileSupplyRate()===1||Math.random()>=.25)return false;
  const B=run._missileBonus||(run._missileBonus={pending:0,delay:0});
  B.pending++;B.delay=Math.max(B.delay,2);return true;
}
function scriptedMissileSupply(x,pack){
  const p={x:clamp(x,camLeftX()+40,camRightX()-40),y:-30,vy:.85,t:0,kind:'mcrate',
    hp:6,flash:0,w:48,h:44,bob:rnd(0,TAU),_pack:pack};
  powerups.push(p);missileSupplyBonusRoll();return p;
}
function missileSupplyBonusTick(dt){
  const B=run._missileBonus;if(!B)return;
  if(missileSupplyRate()===1){run._missileBonus=null;return;}
  if(player.dead||B.pending<=0)return;
  B.delay=Math.max(0,B.delay-dt);
  if(B.delay>1e-9||missileSupplyOnScreen())return;
  B.pending--;B.delay=2;
  powerups.push({x:clamp(player.x,camLeftX()+40,camRightX()-40),y:-30,vy:.85,t:0,kind:'mcrate',
    hp:6,flash:0,w:48,h:44,bob:0,_pack:mslPackRoll(),_bonusSupply:true});
  if(typeof stageStats!=='undefined')stageStats.pickupsSeen++;
}
function bossMissileSupplyTick(dt){""")
edit("const B=b._missileSupply||(b._missileSupply={t:0,due:7});", "const B=b._missileSupply||(b._missileSupply={t:0,due:7/missileSupplyRate()});")
edit("if(B.t<B.due||powerups.some(p=>!p.dead&&(p.kind==='mcrate'||/^missilepack/.test(p.kind))))continue;", "if(B.t<B.due||missileSupplyOnScreen())continue;")
# Both existing rate sites use the same shared rule.
a="const bonus=diffKey==='hard'||diffKey==='furious'?1.25:1;";assert s.count(a)==2;s=s.replace(a,"const bonus=missileSupplyRate();")
edit("""        powerups.push({x:clamp(b.x, 60, VW-60), y:-30, vy:0.85, t:0, kind:'mcrate',
                       hp:6, flash:0, w:48, h:44, bob:rnd(0,TAU), _pack:'missilepack10'});""", """        scriptedMissileSupply(b.x,'missilepack10');""")
x=s.encode('utf-8');assert b'\r\n'not in x;assert current in[b,x]
if '--dry-run'not in sys.argv:p.write_bytes(x)
(O/'game.expected.js').write_bytes(x);print(hashlib.sha256(x).hexdigest())
