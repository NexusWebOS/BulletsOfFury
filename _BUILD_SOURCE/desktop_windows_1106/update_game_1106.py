from pathlib import Path
import json,hashlib,shutil
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
B=W/'qa/before-1106b';B.mkdir(exist_ok=True)
def edit(name,fn):
 p=R/name;raw=p.read_bytes();dst=B/name;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():dst.write_bytes(raw)
 s=raw.decode('utf8');new=fn(s);assert new!=s,name
 p.write_bytes(new.encode('utf8'))
def core(s):
 needle='function eMG(x,y,ang,spd,col)'
 helper='''// Physical hostile bullets and sonic pressure fronts are hazards, never targets.
// Keep the original ammunition identity when a later palette/art pass recolors it.
function enemyProjectileIsBulletOrSonic(q){
  if(!q)return false;
  if(q._ordinaryHostile)return true;
  if(q._physicalMissile||/missile|rocket|warhead/i.test(q.kind||''))return false;
  return !!(q.mg||q._s1aSlug||q._ovSonicWave||q._fb9RzbProof||
    /bullet|slug|pellet|tracer|sonic|^sg10pressure$|^(?:mg|minigunT|chaingunT|s1cannon)$/i.test(q.kind||''));
}
'''
 assert s.count(needle)==1;s=s.replace(needle,helper+needle)
 s=s.replace("kind:'mg', _ph:","kind:'mg', _ordinaryHostile:true, _weaponProof:true, _shootable:false, _ph:",1)
 s=s.replace("w:6,h:6, kind,\n    t:0,", "w:6,h:6, kind, _ordinaryHostile:enemyProjectileIsBulletOrSonic({kind}), _weaponProof:enemyProjectileIsBulletOrSonic({kind}),\n    t:0,",1)
 needle='hp:_shootable?1:undefined,_shootable,\n    _curve:'
 assert needle in s;s=s.replace(needle,'hp:_shootable?1:undefined,_shootable,\n    _ordinaryHostile:enemyProjectileIsBulletOrSonic({kind}),_weaponProof:enemyProjectileIsBulletOrSonic({kind}),\n    _curve:',1)
 start=s.index('function drawPilotBG(tint){');end=s.index('\n/* Passwords and stage-labelled UI',start)
 s=s[:start]+'''const PILOT_SOLID_PALETTES_1106={
  axel:'#102850',decker:'#483810',maverick:'#104838',freezer:'#382048',
  juggernaut:'#483020',yuri:'#501820',lizzie:'#504018',falva:'#501038',cole:'#284018'
};
function drawPilotBG(tint){
  const v=pilotViewSize(),p=PILOTS.find(p=>p.tint===tint)||PILOTS[pilotIndex]||PILOTS[0];
  // Mike explicitly requested a flat 16-bit color field with no scenery/gradient.
  ctx.fillStyle=PILOT_SOLID_PALETTES_1106[p.key];ctx.fillRect(0,0,v.w,v.h);
}
'''+s[end:]
 return s
edit('assets/game.js',core)
edit('assets/stage3_combat_1004k.js',lambda s:s.replace("if(!q||/bullet/i.test(q.kind||'')", "if(!q||enemyProjectileIsBulletOrSonic(q)||/bullet/i.test(q.kind||'')",1).replace("return !!q&&(!!enemyOrdnanceElement(q)","return !!q&&!enemyProjectileIsBulletOrSonic(q)&&(!!enemyOrdnanceElement(q)",1))
edit('assets/menu_sceneries_1103.js',lambda s:s.replace("pilot:'hangar',cooproster:'hangar',",'').replace("drawPilotBG=function(){const v={w:Math.round(cv.width/SS),h:Math.round(cv.height/SS)};if(menuScenery113('hangar',v.w,v.h))return true;return MS113.base.pilot.apply(this,arguments);};","drawPilotBG=function(){return MS113.base.pilot.apply(this,arguments);};"))
mod='''"use strict";
/* Final interception invariant: cosmetic elemental art cannot make an ordinary
   gun round or sonic pressure wave into shootable ordnance. Physical missiles
   and deliberately authored boss energy-ball mechanics keep their native rules. */
const ORD1106_INTERCEPT=enemyOrdnanceCanIntercept;
enemyOrdnanceCanIntercept=function(q){
  return !enemyProjectileIsBulletOrSonic(q)&&ORD1106_INTERCEPT.apply(this,arguments);
};
'''
(R/'assets/projectile_contract_1106.js').write_text(mod,encoding='utf8')
edit('index.html',lambda s:s.replace('assets/game.js?v=official-mouse-1105','assets/game.js?v=desktop-controls-1106b').replace('assets/menu_sceneries_1103.js?v=parallax-menus-1','assets/menu_sceneries_1103.js?v=solid-pilot-1106b').replace('</body>','<script src="assets/projectile_contract_1106.js?v=bullets-sonic-proof-1"></script>\n</body>'))
print(json.dumps({n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','index.html','assets/stage3_combat_1004k.js','assets/menu_sceneries_1103.js','assets/projectile_contract_1106.js']},indent=2))
