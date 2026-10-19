/* Read display strings from the current full-index encounter owners.
   This is label metadata, not a native-render or combat assertion. */
const fs=require('fs'),path=require('path');
const {read,ROOT}=require('./test_rime_defense_1019.cjs');
const roster={1:[['razorback',true],['damkeeper',false]],2:[['magmaward',true],['infernoreaver',false]],3:[['frostcruiser',true],['cryospear',false]],4:[['olivewarden',true],['stormsovereign',false]],5:[['siegebomber',true],['chromehammer',false]],6:[['siegefortress17',true],['warhive',false],['rebelsquad',false]],7:[['dualscoopdredger',true],['sludgeemperor',false]],8:[['heralddeath',true],['vileexistence',false]],9:[['voidhorizon',true],['tidalfusion',false]]};
const out={};
for(const [stage,rows] of Object.entries(roster))for(const [kind,mini] of rows){
 try{const q=read(`coopOn=false;run.mode='arcade';run.stage=${stage};run.pilot='cole';curStage=STAGES[${stage}-1];diffKey='normal';DIFF=DIFFS.normal;boss=null;subBoss=null;bossActive=subBossActive=false;enemies=[];eBullets=[];pBullets=[];player.dead=player.out=false;groundTargetingReset();
 ${mini?'spawnSubBoss__inner':'spawnBoss'}('${kind}');const b=${mini?'subBoss':'boss'};if(run.stage===7&&b?._s7mod)s7mInit(b);return {name:b?.name||null,kind:b?.kind,ship:b?._ship};`);out[kind]={...q,stage:+stage,role:mini?'miniboss':'boss'};
 }catch(e){out[kind]={name:null,stage:+stage,error:String(e.message)};}
}
fs.writeFileSync(path.join(ROOT,'docs/previews/overnight_1019/names.json'),JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out));
