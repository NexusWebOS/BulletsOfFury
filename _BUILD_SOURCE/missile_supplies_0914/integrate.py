from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/missile_supplies_0914/game.before.js';path=ROOT/'assets/game.js'
s=before.read_bytes().decode('utf-8')
def replace(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:100])
 s=s.replace(a,b,1)
def fn(name,body):
 global s
 a=s.index('\nfunction '+name+'(');b=s.index('\n}',a)+2
 s=s[:a]+'\n'+body+s[b:]
replace('const COMBAT_WARNING_SECONDS=3.0;',(HERE/'engine.js').read_text(encoding='utf-8')+'\nconst COMBAT_WARNING_SECONDS=3.0;')
a=s.index('const MSL_STAGE_TIERS = {');b=s.index('\n};',a)+3
s=s[:a]+"const MSL_STAGE_TIERS = {1:['missilepack20'],2:['missilepack20'],3:['missilepack20'],4:['missilepack20'],5:['missilepack20'],6:['missilepack20'],7:['missilepack20'],8:['missilepack50','missilepack100']};"+s[b:]
fn('mslPackRoll',"function mslPackRoll(){\n const stage=run.stage|0,r=Math.random();\n if(stage===8)return r<.5?'missilepack50':'missilepack100';\n if(stage>=1&&stage<=7)return r<.50?'missilepack':r<.80?'missilepack10':'missilepack20';\n return r<.65?'missilepack':'missilepack10';\n}")
replace('function applyPowerup(p){',"function applyPowerup(p){\n  if(p.kind==='missilepack2')p=Object.assign({},p,{kind:'missilepack'});")
replace('special.strikes+=3; run.bombs=special.strikes;', 'special.strikes+=5; run.bombs=special.strikes;')
replace("'NUKES +3'","'NUKES +5'")
replace('run.bombs=clamp(run.bombs+3,0,MSL_CAP);','run.bombs=clamp(run.bombs+5,0,MSL_CAP);')
replace("'MISSILES +3'","'MISSILES +5'")
replace('const _pk = p._pack || mslPackRoll();',"const _pk = p._pack==='missilepack2'?'missilepack':p._pack||mslPackRoll();")
replace('  // ---- powerup containers ----','  bossMissileSupplyTick(dt);\n  // ---- powerup containers ----')
replace('function killEnemy(e){\n  if(e.dead) return;', 'function killEnemy(e){\n  if(e.dead) return;\n  enemyMissileDrop(e);')
replace('    p.t+=dt; p.y+=p.vy; p.x+=Math.sin(p.t*3+p.bob)*0.4;',
  '    p.t+=dt; p.y+=p.vy; p.x+=Math.sin(p.t*3+p.bob)*0.4;\n    if(p._looseMissile&&p.t<.55){p.x+=p._scatterVx*dt*Math.max(0,1-p.t/.55);p.x=clamp(p.x,camLeftX()+12,camRightX()-12);}')
replace('function drawPowerups(){\n  for(const p of powerups){','function drawPowerups(){\n  for(const p of powerups){\n    if(p.kind===\'missilepack2\')p.kind=\'missilepack\';\n    if(looseMissilePickupDraw(p))continue;')
expected=s.encode('utf-8')
out=ROOT/'_shots/missile_supplies_0914/game.expected.js'if '--dry-run'in sys.argv else path
if out==path and path.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent edits present')
out.write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
