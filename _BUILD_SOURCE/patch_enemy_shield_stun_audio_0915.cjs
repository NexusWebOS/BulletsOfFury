const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'../assets/game.js');let src=fs.readFileSync(file,'utf8');
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
const old=`function enemyFrenzyBegin(e){
  if(!e || e._frenzy) return;
  e._frenzy=1; e._frenzyT=0; e._frenzyDiveCd=0.55;
  if(typeof Audio!=='undefined' && Audio.SFX && Audio.SFX.shieldBreakCombat) Audio.SFX.shieldBreakCombat();
}`;
const next=`function enemyFrenzyBegin(e,silent){
  if(!e || e._frenzy) return;
  e._frenzy=1; e._frenzyT=0; e._frenzyDiveCd=0.55;
  if(!silent&&typeof Audio!=='undefined' && Audio.SFX && Audio.SFX.shieldBreakCombat) Audio.SFX.shieldBreakCombat();
}`;
if(src.includes(old))src=src.replace(old,next);else if(!src.includes(next))throw new Error('frenzy guard not found');
const a=`if(frenzy&&typeof enemyFrenzyBegin==='function')enemyFrenzyBegin(e);return false;`;
const b=`if(frenzy&&typeof enemyFrenzyBegin==='function')enemyFrenzyBegin(e,true);return false;`;
if(src.includes(a))src=src.replace(a,b);else if(!src.includes(b))throw new Error('stun frenzy handoff guard not found');
fs.writeFileSync(file,src,'utf8');console.log('Verified silent stun-to-frenzy handoff.');
