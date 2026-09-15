const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const game=path.join(root,'assets','game.js');
let s=fs.readFileSync(game,'utf8');
if(s.includes('\r'))throw new Error('assets/game.js must remain LF-only');
const backup=path.join(root,'_shots','backups','game_pre_difficulty_elite_aces_0915.js');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.writeFileSync(backup,s,'utf8');
function one(oldText,newText,label){
  const n=s.split(oldText).length-1;
  if(n!==1)throw new Error(label+' expected once, found '+n);
  s=s.replace(oldText,newText);
}
const oldSorter=`function _planSorted(P){
  return P.map(function(w,i){ return [w,i]; })
          .sort(function(a,b){ return (a[0].t-b[0].t) || (a[1]-b[1]); })
          .map(function(p){ return p[0]; });
}`;
const newSorter=`function _planSorted(P,stageNum){
  if(Number.isFinite(stageNum)) difficultyElitePlan(P,stageNum);
  return P.map(function(w,i){ return [w,i]; })
          .sort(function(a,b){ return (a[0].t-b[0].t) || (a[1]-b[1]); })
          .map(function(p){ return p[0]; });
}
/* Hard and Furious add authored Expansion aces instead of tinting ordinary hulls at draw time.
   Each stage receives a distinct finished palette that suits its biome, while its shields,
   predictive strafe, incoming-fire roll and aimed volleys come from the existing ELITEX engine.
   The flag is also the single future reward boundary for Continue Up eligibility. */
const DIFFICULTY_ELITE_STAGE={
  1:['razorback','furytalon'],2:['emberwing','furytalon'],3:['glacierlance','tempest'],
  4:['furytalon','razorback'],5:['voidreaver','nighthammer'],6:['tempest','glacierlance'],
  7:['ironserpent','voidreaver'],8:['nighthammer','solarwarden'],9:['solarwarden','voidreaver']
};
function spawnDifficultyElite(stage,index){
  const row=DIFFICULTY_ELITE_STAGE[stage|0];if(!row)return null;
  const furious=typeof diffKey!=='undefined'&&diffKey==='furious',kind=row[index%row.length],W=worldWidth(),
        x=W*(furious?(index&1?.72:.28):.50),e=spawnEnemy('xelite_'+kind,x,-82,{_difficultyElite:true});
  if(!e)return null;e._difficultyElite=furious?'furious':'hard';e._difficultyEliteStage=stage|0;
  e._continueEligible=true;e._eliteAuthoredVariant=kind;e.dropOk=true;
  if(typeof XART!=='undefined'){try{XART.rdy('xelite_'+kind);if(XART._touch)XART._touch('xelite_'+kind);}catch(_eliteWarm){}}
  return e;
}
function difficultyElitePlan(P,stageNum){
  const hard=typeof diffKey!=='undefined'&&(diffKey==='hard'||diffKey==='furious');
  if(!hard||!DIFFICULTY_ELITE_STAGE[stageNum]||!Array.isArray(P))return P;
  const times=P.map(w=>Number(w&&w.t)).filter(Number.isFinite),last=times.length?Math.max.apply(Math,times):30,
        first=clamp(last*.43,12,Math.max(12,last-8));
  const add=(t,index)=>{const fn=function _difficultyEliteWave(){spawnDifficultyElite(stageNum,index);};
    fn._difficultyElite=true;fn._difficultyEliteStage=stageNum;fn._difficultyEliteIndex=index;P.push({t:t,fn:fn});};
  add(first,0);
  if(diffKey==='furious')add(clamp(last*.71,first+9,Math.max(first+9,last-3)),1);
  return P;
}`;
one(oldSorter,newSorter,'difficulty-aware stable plan sorter');
const oldCalls=(s.match(/_planSorted\(P\)/g)||[]).length;
if(oldCalls!==11)throw new Error('expected 11 plan sorter calls, found '+oldCalls);
s=s.replace(/_planSorted\(P\)/g,'_planSorted(P,stageNum)');
if(s.includes('\r'))throw new Error('patch introduced CR characters');
fs.writeFileSync(game,s,'utf8');
console.log('PATCHED_DIFFICULTY_ELITE_ACES_0915');
