const fs=require('fs'),path=require('path');
const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
const controller=`/* Chrome flak alternates the authored outer and inner angle pairs. Commit each shell corridor
   before launch; the 0.64-second visible fuse remains the readable cue for its five-way airburst. */
function carrierFlakFanPaths(b,F){
  if(!b||!F)return [];const len=Math.max(VH,worldWidth())*1.35;return F.lanes.map(q=>{const p=carrierHP(b,q.slot);return{x:p.x,y:p.y,a:q.a,slot:q.slot,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len};});
}
function carrierFlakFanStart(b){
  const M=b&&b._mega;if(!M||M.flakFan)return false;const tell=.62,cooldown=1.08,pair=M.flakPair|0;
  const specs=pair?[{deg:10,slot:'lower_left_inner'},{deg:-10,slot:'lower_right_inner'}]:[{deg:-18,slot:'lower_left_inner'},{deg:18,slot:'lower_right_inner'}];
  M.flakPair=pair?0:1;M.flakFan={t:0,tell:tell,cooldown:cooldown,pair:pair,id:'stage6-carrier-chrome-flak',lanes:specs.map(q=>({slot:q.slot,a:Math.PI/2+q.deg*Math.PI/180})),released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-chrome-flak',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierFlakFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.flakFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierFlakFanPaths(b,F);for(let i=0;i<paths.length;i++){const p=paths[i],q=carrierMegaShot(b,p,p.a,3.75,'s6flak',{silent:i>0});if(q)q._flakFuse=CARRIER_FLAK_FUSE;}
    carrierMegaMuzzle(b,'MG_L','s6mb_cyclonemuzzle',.90);carrierMegaMuzzle(b,'MG_R','s6mb_cyclonemuzzle',.90);if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();}
  if(F.released&&F.t>=F.finish){M.flakFan=null;M.cd=.02;return false;}return true;
}
function carrierFlakFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.flakFan;if(!F||F.released)return false;const paths=carrierFlakFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:25,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`;
once("function carrierClusterFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.clusterFan;if(!F||F.released)return false;const paths=carrierClusterFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n","function carrierClusterFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.clusterFan;if(!F||F.released)return false;const paths=carrierClusterFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n"+controller,'flak controller');
once("    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan,M.omegaBomb,M.clusterFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;M.omegaBomb=null;M.clusterFan=null;","    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan,M.omegaBomb,M.clusterFan,M.flakFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;M.omegaBomb=null;M.clusterFan=null;M.flakFan=null;",'phase cleanup');
once("  if(carrierClusterFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierClusterFanTick(b,dt))return;\n  if(carrierFlakFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'flak tick');
once("      const _fa=[[-18,'lower_left_inner'],[18,'lower_right_inner'],[10,'lower_left_inner'],[-10,'lower_right_inner']];\n      for(let _i=0;_i<2;_i++){\n        const row=_fa[(M.step+_i)%4], pt=carrierHP(b,row[1]);\n        const q=carrierMegaShot(b,pt,Math.PI/2+row[0]*Math.PI/180,3.75,'s6flak',{silent:_i>0});\n        if(q) q._flakFuse=CARRIER_FLAK_FUSE;\n      }\n      carrierMegaMuzzle(b,'MG_L','s6mb_cyclonemuzzle',.90);carrierMegaMuzzle(b,'MG_R','s6mb_cyclonemuzzle',.90);M.cd=1.08;","      carrierFlakFanStart(b);return;",'replace immediate flak fan');
once("carrierOmegaDraw(b,false);carrierClusterFanDraw(b,false);if(M.phase<1)return;","carrierOmegaDraw(b,false);carrierClusterFanDraw(b,false);carrierFlakFanDraw(b,false);if(M.phase<1)return;",'flak fields under hull');
once("carrierOmegaDraw(b,true);carrierClusterFanDraw(b,true);","carrierOmegaDraw(b,true);carrierClusterFanDraw(b,true);carrierFlakFanDraw(b,true);",'flak alert over hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);console.log('PATCHED_STAGE6_CARRIER_FLAK_WARNING_0916');
