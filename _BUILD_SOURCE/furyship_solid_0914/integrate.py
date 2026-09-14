from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/furyship_solid_0914';p=R/'assets/game.js'
b=(O/'game.before.js').read_bytes();assert hashlib.sha256(b).hexdigest()=='3d55604968cc2af62926ed8ef7ed296a03cf051c57d87686ad6434d9405e2978'
s=b.decode('utf-8')
def edit(a,z):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,z)
def function_block(start,end,source):
 global s
 a=s.index(start);z=s.index(end,a);s=s[:a]+source+'\n'+s[z:]
function_block('function furyShipDrawPhase(', 'function furyShipVeil(', (H/'parts.js').read_text(encoding='utf-8'))
function_block('function furyIntroClouds(', 'function furyIntroDialogue(', (H/'clouds.js').read_text(encoding='utf-8'))
edit('const FURY_INTRO_SPEED=420,FURY_INTRO_SKY_SECONDS=12;', 'const FURY_INTRO_SPEED=1000,FURY_INTRO_SKY_SECONDS=12;')
edit("    gravityScatter(){", """    furyPartArrival(index){
      const n=(index|0)%4;
      noise(.30,.13,850+n*120,+2400);tone(150+n*28,.24,'triangle',.10,+390);
      tone(680+n*70,.075,'square',.045,-120);
    },
    gravityScatter(){""")
edit("  gravityModeTick(dt);\n  if(S.t>=FURY_INTRO_SKY_SECONDS&&gravityMode.dialogueDone&&furyShipReady()", "  gravityModeTick(dt);furyPartsTick(gravityMode);\n  if(S.t>=FURY_INTRO_SKY_SECONDS&&gravityMode.dialogueDone&&furyPartsReadyToFuse(gravityMode)&&furyShipReady()")
edit(" if(S.build&&S.phase==='sky'&&S.t<6){", " if(S.build&&S.phase==='sky'&&gravityMode.partStartAge==null){")
edit(" furyIntroClouds(S);\n furyIntroDialogue(G);", " if(!(furyShipReady()&&G.partStartAge!=null&&['drift','charge','scatter','snap','pixelglow'].includes(G.phase)))furyIntroClouds(S);\n furyIntroDialogue(G);")
expected=s.encode('utf-8');assert b'\r\n'not in expected
assert p.read_bytes()in[b,expected,(O/'game.expected.js').read_bytes()if(O/'game.expected.js').exists()else b],'Concurrent runtime changes'
p.write_bytes(expected);(O/'game.expected.js').write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
