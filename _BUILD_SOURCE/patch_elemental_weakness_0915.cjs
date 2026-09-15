const fs=require('fs'),file=require('path').resolve(__dirname,'../assets/game.js');let src=fs.readFileSync(file,'utf8');
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
function rep(a,b,n){const c=src.split(a).length-1;if(c!==1)throw new Error(n+' expected once, found '+c);src=src.replace(a,b);}
const already=src.includes('function elementalAlreadyScaled(');
if(!already){
rep(`function elementalDamageResult(t,role,b,dmg,x,y){
  const reaction=opposingElementImpact(t,role,b);
  if(reaction!=='absorb-fire'&&reaction!=='absorb-ice')return{dmg:dmg,reaction:reaction};
  const now=(typeof stageTimer==='number'?stageTimer:0),next=t._elemAbsorbNext;
  if(next==null||now>=next){
    t._elemAbsorbNext=now+.55;
    if(typeof floatText==='function')floatText(Number.isFinite(x)?x:t.x,(Number.isFinite(y)?y:(t._drawY!=null?t._drawY:t.y))-18,
      reaction==='absorb-fire'?'FIRE DMG ABSORBED!':'ICE DMG ABSORBED!',reaction==='absorb-fire'?'#ffad55':'#b9efff');
  }
  return{dmg:dmg*.5,reaction:reaction};
}`,
`function elementalAlreadyScaled(b,reaction){
  if(!run||typeof _pilotKey!=='function'||_pilotKey()!=='freezer'||!b)return false;
  const kind=String(b.kind||'').toLowerCase();
  return (run.stage===2&&reaction==='ice'&&kind==='flame')||
    (run.stage===3&&reaction==='fire'&&(b._ts||damageProjectileElement(b)==='fireice'));
}
function elementalDamageResult(t,role,b,dmg,x,y){
  const reaction=opposingElementImpact(t,role,b);
  if(reaction==='fire'||reaction==='ice')return{dmg:elementalAlreadyScaled(b,reaction)?dmg:dmg*2,reaction:reaction};
  if(reaction!=='absorb-fire'&&reaction!=='absorb-ice')return{dmg:dmg,reaction:reaction};
  const now=(typeof stageTimer==='number'?stageTimer:0),next=t._elemAbsorbNext;
  if(next==null||now>=next){
    t._elemAbsorbNext=now+.55;
    if(typeof floatText==='function')floatText(Number.isFinite(x)?x:t.x,(Number.isFinite(y)?y:(t._drawY!=null?t._drawY:t.y))-18,
      reaction==='absorb-fire'?'FIRE DMG ABSORBED!':'ICE DMG ABSORBED!',reaction==='absorb-fire'?'#ffad55':'#b9efff');
  }
  return{dmg:dmg*.5,reaction:reaction};
}`,'element result');
rep(`  markHit(e,0.08);   // 0912y: a shield that eats the round still shows the unit was struck
  if(typeof enemyShieldIntercept==='function' && enemyShieldIntercept(e,dmg,_dmgBullet)) return true;
  const _elem=(typeof elementalDamageResult==='function')?elementalDamageResult(e,'enemy',_dmgBullet,dmg,e.x,e.y):{dmg:dmg,reaction:null};
  dmg=_elem.dmg;const _elemHit=_elem.reaction;`,
`  markHit(e,0.08);   // 0912y: a shield that eats the round still shows the unit was struck
  const _elem=(typeof elementalDamageResult==='function')?elementalDamageResult(e,'enemy',_dmgBullet,dmg,e.x,e.y):{dmg:dmg,reaction:null};
  dmg=_elem.dmg;const _elemHit=_elem.reaction;
  if(typeof enemyShieldIntercept==='function' && enemyShieldIntercept(e,dmg,_dmgBullet)) return true;`,'enemy shield order');
}
const oldComment=`   Mike's exact correction overrides the earlier generic opposing-element interpretation:
     - Stage 2: Freezer's ICE BREATH deals x2.
     - Stage 3: Freezer's FIRE-ICE / thermoshock ball deals x2.
     - Cole has no elemental damage addition. His specials are Sonic Boom and nuclear missiles.

   The attack identity is required as well as the element. This prevents a generic ice/fire orb
   carried by Cole (or any other pilot) from silently becoming a special elemental bonus. */`;
const newComment=`   These two multipliers predate the shared fire-versus-ice weakness gate:
     - Stage 2: Freezer's ICE BREATH deals x2.
     - Stage 3: Freezer's FIRE-ICE / thermoshock ball deals x2.
     - Cole has no pilot-specific elemental bonus. His specials are Sonic Boom and nuclear missiles.

   elementalAlreadyScaled recognizes these authored paths so the shared opposing-element rule
   keeps them at x2 instead of stacking a second multiplier and turning them into x4 attacks. */`;
if(src.includes(oldComment))src=src.replace(oldComment,newComment);
else if(!src.includes(newComment))throw new Error('element multiplier comment guard not found');
fs.writeFileSync(file,src,'utf8');console.log(already?'Elemental weakness patch already applied; comments verified.':'Applied shared opposing-element weakness.');
