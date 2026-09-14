from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parents[2];O=R/'_shots/easy_queue_0914';p=R/'assets/game.js';current=p.read_bytes();b=(O/'game.before.js').read_bytes()if(O/'game.before.js').exists()else current
assert hashlib.sha256(b).hexdigest()=='41ee9c77220592dc818374cd5a1fba54d870ac22036c113c38284d48c9b15835'
if not(O/'game.before.js').exists():
 (O/'game.before.js').write_bytes(b);(O/'test.before.js').write_bytes((R/'_BUILD_SOURCE/test_fl.js').read_bytes())
s=b.decode('utf-8')
def edit(a,z):
 global s
 assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,z)
edit('let gravityMode=null;',"""/* Mike 0914: display the pilot's Space Fighter model during assembly/reveal.
   Decker keeps his pilot name until Mike supplies the ninth model. */
const SPACE_FIGHTER_MODELS={yuri:'Yamado',maverick:'Moonraker',lizzie:'Lavender',falva:'Foxtrout',cole:'Collisto',juggernaut:'Janis',axel:'Aristotle',freezer:'Falcon'};
function spaceFighterName(pilot){
  const key=pilot||_pilotKey(),p=PILOTS.find(p=>p.key===key);
  return 'SPACE FIGHTER '+String(SPACE_FIGHTER_MODELS[key]||(p&&p.name)||'').toUpperCase();
}
let gravityMode=null;""")
edit("ctx.fillText(phase==='reveal'?'GRAVITY MODE ONLINE':'GRAVITY MODE',x,y-size*0.72);", "ctx.fillText(spaceFighterName(pilot),x,y-size*0.72);")
edit('function dropPowerup(x,y,forceKind){',"""// Shared Life Up probability boost for Hard/Furious in every run mode.
function lifeDropChance(base){return clamp(base*((diffKey==='hard'||diffKey==='furious')?1.25:1),0,1);}
function dropPowerup(x,y,forceKind){""")
edit("""    if(Math.random()>0.10) return;
    const r=Math.random();
    kind = r<0.62?'bomb' : (r<0.9?'shield':'life');""", """    // Original death drops: 6.2% ammo, 2.8% shield, 1% life. Add the life
    // bonus in a separate interval so extra lives do not steal ammo/shield rolls.
    const roll=Math.random(),extraLife=lifeDropChance(.01)-.01;
    if(roll>.10+extraLife)return;
    if(roll>.10)kind='life';
    else {const r=Math.random();kind=r<.62?'bomb':(r<.9?'shield':'life');}""")
edit('// life-up rare roll once per stage (1/50)', '// Life Up once per stage: 2% normally, 2.5% on Hard/Furious.')
edit("if(rint(1,50)===1){ dropPowerup(rnd(60,VW-60), -10, 'life'); }", "if(chance(lifeDropChance(.02))){ dropPowerup(rnd(camLeftX()+40,camRightX()-40), -10, 'life'); }")
x=s.encode('utf-8');assert b'\r\n'not in x;assert current in[b,x]
if '--dry-run'not in sys.argv:p.write_bytes(x)
(O/'game.expected.js').write_bytes(x);print(hashlib.sha256(x).hexdigest())
