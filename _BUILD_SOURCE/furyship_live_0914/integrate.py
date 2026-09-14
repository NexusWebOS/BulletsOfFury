from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/furyship_live_0914'
p=R/'assets/game.js';before=(O/'game.before.js').read_bytes()
assert hashlib.sha256(before).hexdigest()=='41a0790603c5e4d8320839e1083b19a6e123e9075fce334a744825dea888d7d5'
s=before.decode('utf-8')
def edit(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a))
 s=s.replace(a,b)
edit('const GRAVITY_PIECES=[',(H/'runtime.js').read_text(encoding='utf-8')+'\nconst GRAVITY_PIECES=[')
edit('function gravityModeStart(){','function gravityModeStart(){\n  if(!furyLegacyShip)furyShipWarm();')
edit('function gravityModeRetain(earned){','function gravityModeRetain(earned){\n  if(!furyLegacyShip)furyShipWarm();')
edit('function updatePlay(dt){\n  _lastDt=dt;','function updatePlay(dt){\n  _lastDt=dt;\n  if(spaceShipActive())furyFlightTime+=dt;')
start=s.index('function gravityModeDrawShip(');end=s.index('\nfunction drawPlayer()',start)
old=s[start:end];new=old
new=new.replace("  if(!spaceAtlasCanvas('ship_base',pilot))return false;", "  const newFury=furyShipReady();\n  if(!newFury&&!spaceAtlasCanvas('ship_base',pilot))return false;")
a=new.index("  if(phase==='drift'");z=new.index("  if(phase==='pixelglow'){",a)
new=new[:a]+"  if(newFury)furyShipDrawPhase(G,x,y,size,planeH,pilot);\n  else {\n"+new[a:z]+"  }\n"+new[z:]
new=new.replace("  if(phase==='pixelglow'){", "  if(!newFury&&phase==='pixelglow'){")
new=new.replace("  if(phase==='pixelglow')gravityWhite", "  if(newFury)furyShipVeil(G);\n  else if(phase==='pixelglow')gravityWhite")
new=new.replace("  if(newFury)furyShipVeil(G);\n  else if(phase==='pixelglow')gravityWhite", "  if(!newFury&&phase==='pixelglow')gravityWhite")
new=new.replace("  else if(phase==='whiteout') gravityWhite", "  else if(!newFury&&phase==='whiteout') gravityWhite").replace("  else if(phase==='reveal') gravityWhite", "  else if(!newFury&&phase==='reveal') gravityWhite")
new=new.replace("  if(phase!=='active'){", "  if(newFury)furyShipVeil(G);\n  if(phase!=='active'){")
edit(old,new)
edit('function gravityDeathSpinDraw(s){', '''function gravityDeathSpinDraw(s){
  if(s&&furyShipReady()){
    const k=clamp(s.t/s.dur,0,1),a=Math.round(k*s.turns*s.dir/45)*Math.PI/4;
    ctx.save();ctx.globalAlpha=1-.35*k;ctx.translate(player.x,player.y);ctx.rotate(a);
    furyShipDrawFlight(0,0,SPACE_SHIP_SIZE,_pilotKey(),{key:'base'},furyFlightTime);ctx.restore();return true;
  }''')
edit('function spaceShipHardpoints(x,y,size){\n  const s=size||SPACE_SHIP_SIZE;', '''function spaceShipHardpoints(x,y,size){
  const s=size||SPACE_SHIP_SIZE;
  if(!furyLegacyShip)return {laser:[{x:x-s*26/128,y:y-s*21/128,side:-1},{x:x+s*26/128,y:y-s*21/128,side:1}],nose:{x:x,y:y-s*57/128}};''')
edit('function submitPassword(){', '''function submitPassword(){
  if(String(pwInput).toUpperCase()==='SPCBOY'){
    furyLegacyShip=!furyLegacyShip;if(!furyLegacyShip)furyShipWarm();
    Audio.SFX.select();drawPassword.unlockMsg=1.8;drawPassword.unlockWho=furyLegacyShip?'spaceLegacy':'spaceNew';pwInput='';return;
  }''')
edit("    const _um=(_uw==='bomber')?'B-42 BOMBER UNLOCKED!':'COLE UNLOCKED!';", "    const _um=_uw==='spaceLegacy'?'CLASSIC FURYSHIP SELECTED!':(_uw==='spaceNew'?'NEW FURYSHIP SELECTED!':((_uw==='bomber')?'B-42 BOMBER UNLOCKED!':'COLE UNLOCKED!'));")
edit('unlocks:{bomber:!!lizzieSkinUnlocked, cole:!!coleUnlocked}', 'unlocks:{bomber:!!lizzieSkinUnlocked, cole:!!coleUnlocked, legacySpaceShip:!!furyLegacyShip}')
edit('  coleUnlocked=!!(s.unlocks && s.unlocks.cole);', '  coleUnlocked=!!(s.unlocks && s.unlocks.cole);\n  furyLegacyShip=!!(s.unlocks && s.unlocks.legacySpaceShip);')
edit("    if(typeof entryConnectorDraw==='function') entryConnectorDraw(5,launchConnDy());\n    ctx.restore();}", """    if(typeof entryConnectorDraw==='function') entryConnectorDraw(5,launchConnDy());
    ctx.restore();}
  // Authored energy rides the travelling sky/space join and covers its hard edge.
  // The biomes still attach and scroll; neither background is cross-faded.
  if(yb>0&&yb<VH&&furyShipReady()){
    ctx.save();ctx.translate(VW/2,yb);ctx.rotate(Math.PI/2);
    furyShipBlit('veil_04',0,0,112,VW+48,null,.95);ctx.restore();
  }""")
expected=s.encode('utf-8');assert b'\r\n' not in expected
assert p.read_bytes() in [before,expected,(O/'game.expected.js').read_bytes() if (O/'game.expected.js').exists() else before],'Runtime changed since this batch began'
p.write_bytes(expected);(O/'game.expected.js').write_bytes(expected)
print('Integrated Furyship:',hashlib.sha256(expected).hexdigest())
