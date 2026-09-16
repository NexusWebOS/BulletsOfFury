const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(file,'utf8');
function once(from,to,label){const n=s.split(from).length-1;if(n!==1)throw new Error(`${label}: expected one match, got ${n}`);s=s.replace(from,to);}
once(
  "  else{h.chainDestroyed=true;if(hammerHard()){h.mode='enraged';hammerState(b,'enrage');}else{h.mode='core';h.coreAngle=0;hammerState(b,'core_orbit');const cue=Audio.SFX.bossWeaponCharge||Audio.SFX.crackle||Audio.SFX.bossPhase;if(cue)cue();}}",
  "  else{h.chainDestroyed=true;h.hammerDestroyed=true;h.throw=null;if(hammerHard()){h.mode='enraged';hammerState(b,'enrage');}else{h.mode='core';h.coreAngle=0;hammerState(b,'core_orbit');const cue=Audio.SFX.bossWeaponCharge||Audio.SFX.crackle||Audio.SFX.bossPhase;if(cue)cue();}}",
  'retire obsolete modules on final-form entry'
);
once(
  "    for(let i=0;i<3;i++){const q=a+i*TAU/3;archEffectBlit((Math.floor(h.t*12)+i)%4,b.x+Math.cos(q)*r,b.y+Math.sin(q)*r*.48,sz,q,.72+.2*k);}\n    archEffectBlit(2,b.x,b.y-9,lerp(32,68,k),a,.55+.35*k);",
  "    const cells=[0,3,4];for(let i=0;i<3;i++){const q=a+i*TAU/3;archEffectBlit(cells[i],b.x+Math.cos(q)*r,b.y+Math.sin(q)*r*.48,sz,q,.72+.2*k);}\n    archEffectBlit(6,b.x,b.y-9,lerp(32,68,k),a,.55+.35*k);",
  'use authored energy cells without the hammer icon'
);
fs.writeFileSync(file,s,'utf8');console.log('PATCHED_ARCHMAGE_CORE_CLEANUP_0916');
