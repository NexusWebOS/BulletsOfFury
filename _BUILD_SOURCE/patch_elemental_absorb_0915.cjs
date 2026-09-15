const fs=require('fs'),path=require('path');
const file=path.resolve(__dirname,'../assets/game.js');
let src=fs.readFileSync(file,'utf8');
if(src.includes('function elementalDamageResult(')){console.log('Elemental absorption patch already applied.');process.exit(0);}
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
function rep(from,to,label){const n=src.split(from).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);src=src.replace(from,to);}
rep(`function opposingElementImpact(t,role,b){
  if(!t) return null;
  /* Stage 8's final boss is intentionally exempt from the opposing-element response. */
  if(role==='boss'&&run&&run.stage===8){ t._hitFlashColor=null; return null; }
  const atk=damageProjectileElement(b||_dmgBullet), def=damageTargetElement(t,role);
  let reaction=null;
  if(def==='ice' && (atk==='fire'||atk==='fireice')) reaction='fire';
  else if(def==='fire' && (atk==='ice'||atk==='fireice')) reaction='ice';
  t._hitFlashColor=reaction==='fire'?'#ff3b30':reaction==='ice'?'#83d9ff':null;
  return reaction;
}`,
`function opposingElementImpact(t,role,b){
  if(!t) return null;
  /* Stage 8's final boss is intentionally exempt from the elemental response. */
  if(role==='boss'&&run&&run.stage===8){ t._hitFlashColor=null; return null; }
  const atk=damageProjectileElement(b||_dmgBullet), def=damageTargetElement(t,role);
  let reaction=null;
  if(def==='ice' && (atk==='fire'||atk==='fireice')) reaction='fire';
  else if(def==='fire' && (atk==='ice'||atk==='fireice')) reaction='ice';
  else if(def==='fire' && atk==='fire') reaction='absorb-fire';
  else if(def==='ice' && atk==='ice') reaction='absorb-ice';
  t._hitFlashColor=reaction==='fire'?'#ff3b30':reaction==='ice'?'#83d9ff':
    reaction==='absorb-fire'?'#ff9b42':reaction==='absorb-ice'?'#b9efff':null;
  return reaction;
}
/* Same-element rounds retain half damage. One shared gate keeps held weapons readable instead of
   printing a new label on every burn tick; stageTimer freezes with the game. */
function elementalDamageResult(t,role,b,dmg,x,y){
  const reaction=opposingElementImpact(t,role,b);
  if(reaction!=='absorb-fire'&&reaction!=='absorb-ice')return{dmg:dmg,reaction:reaction};
  const now=(typeof stageTimer==='number'?stageTimer:0),next=t._elemAbsorbNext;
  if(next==null||now>=next){
    t._elemAbsorbNext=now+.55;
    if(typeof floatText==='function')floatText(Number.isFinite(x)?x:t.x,(Number.isFinite(y)?y:(t._drawY!=null?t._drawY:t.y))-18,
      reaction==='absorb-fire'?'FIRE DMG ABSORBED!':'ICE DMG ABSORBED!',reaction==='absorb-fire'?'#ffad55':'#b9efff');
  }
  return{dmg:dmg*.5,reaction:reaction};
}`,'element response');
rep(`  const _elemHit=(typeof opposingElementImpact==='function')?opposingElementImpact(e,'enemy',_dmgBullet):null;
  e.hp-=dmg; e.flash=0.12; weaponHitSfx('normal');`,
`  const _elem=(typeof elementalDamageResult==='function')?elementalDamageResult(e,'enemy',_dmgBullet,dmg,e.x,e.y):{dmg:dmg,reaction:null};
  dmg=_elem.dmg;const _elemHit=_elem.reaction;
  e.hp-=dmg; e.flash=0.12; weaponHitSfx('normal');`,'enemy boundary');
rep(`  if(hx!=null && hy!=null){ _lastHitX=hx; _lastHitY=hy; }
  /* ⚠ THE RAPTOR'S WINGS`,
`  if(hx!=null && hy!=null){ _lastHitX=hx; _lastHitY=hy; }
  const b=subBoss;if(!b||b.dead)return;
  const _elem=(typeof elementalDamageResult==='function')?elementalDamageResult(b,'subboss',_dmgBullet,dmg,hx,hy):{dmg:dmg,reaction:null};
  dmg=_elem.dmg;const _elemHit=_elem.reaction;
  /* ⚠ THE RAPTOR'S WINGS`,'subboss entry');
rep(`  const b=subBoss; if(!b||b.dead) return;
  if(b._tempestDuo)`,
`  if(b._tempestDuo)`,'subboss duplicate binding');
rep(`  const _elemHit=(typeof opposingElementImpact==='function')?opposingElementImpact(b,'subboss',_dmgBullet):null;
  b.hp-=dmg; b.flash=0.18;`,
`  b.hp-=dmg; b.flash=0.18;`,'subboss old response');
rep(`  if(!boss||boss.dead) return;
  if(boss._hammer)`,
`  if(!boss||boss.dead) return;
  const _elem=(typeof elementalDamageResult==='function')?elementalDamageResult(boss,'boss',_dmgBullet,dmg,_lastHitX,_lastHitY):{dmg:dmg,reaction:null};
  dmg=_elem.dmg;const _elemHit=_elem.reaction;
  if(boss._hammer)`,'boss boundary');
rep(`  const _elemHit=(typeof opposingElementImpact==='function')?opposingElementImpact(boss,'boss',_dmgBullet):null;
  weaponHitSfx('normal');`,
`  weaponHitSfx('normal');`,'boss old response');
rep(`  const src=_isIce?XART.get(key):(xartPalette(key,'#ff6924')||XART.get(key));`,
`  const _isIce = key.indexOf('nib_')===0 || key.indexOf('nibr_')===0;
  const src=_isIce?XART.get(key):(xartPalette(key,'#ff6924')||XART.get(key));`,'flame element before source');
rep(`  const _isIce = key.indexOf('nib_')===0 || key.indexOf('nibr_')===0;
  /* ⚠ ICE_ALPHA`,
`  /* ⚠ ICE_ALPHA`,'late flame element declaration');
if(src.includes('\r'))throw new Error('patch introduced CR');
fs.writeFileSync(file,src,'utf8');console.log('Applied shared same-element absorption.');
