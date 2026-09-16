const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierOmegaDraw(b,front){\n  const M=b&&b._mega,F=M&&M.omegaBomb;if(!F||F.released)return false;const p=carrierOmegaPath(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:38,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n",
`function carrierOmegaDraw(b,front){
  const M=b&&b._mega,F=M&&M.omegaBomb;if(!F||F.released)return false;const p=carrierOmegaPath(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:38,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
/* The Last Run cluster fan fires three mirrored paths from each side mount. Preserve the open
   middle wedge, but commit all six paths before the fast authored bomblets leave the hull. */
function carrierClusterFanPaths(b,F){
  if(!b||!F)return [];const len=Math.max(VH,worldWidth())*1.35;return F.lanes.map(q=>{const p=shipBossMount(b,q.slot);return{x:p.x,y:p.y,a:q.a,slot:q.slot,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len};});
}
function carrierClusterFanStart(b){
  const M=b&&b._mega;if(!M||M.clusterFan)return false;const tell=.62,cooldown=1.18,lanes=[];for(const row of [['L',-1],['R',1]])for(const o of [.22,.38,.54])lanes.push({slot:row[0],a:Math.PI/2+row[1]*o});
  M.clusterFan={t:0,tell:tell,cooldown:cooldown,id:'stage6-carrier-cluster-fan',lanes:lanes,released:false,finish:0};M.cd=cooldown;combatWarningTick(b,'stage6-carrier-cluster-fan',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierClusterFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.clusterFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierClusterFanPaths(b,F);for(const p of paths)carrierMegaShot(b,p,p.a,3.35,'s6cluster',{silent:true});carrierMegaMuzzle(b,'L','s6mb_cyclonemuzzle',1.0);carrierMegaMuzzle(b,'R','s6mb_cyclonemuzzle',1.0);if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();}
  if(F.released&&F.t>=F.finish){M.clusterFan=null;M.cd=.02;return false;}return true;
}
function carrierClusterFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.clusterFan;if(!F||F.released)return false;const paths=carrierClusterFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`,
'cluster warning controller');
once("    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan,M.omegaBomb])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;M.omegaBomb=null;","    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan,M.omegaBomb,M.clusterFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;M.omegaBomb=null;M.clusterFan=null;",'phase cleanup');
once("  if(carrierOmegaTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierOmegaTick(b,dt))return;\n  if(carrierClusterFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'cluster per-frame tick');
once("      for(const row of [[L,-1],[R,1]])for(const o of [.22,.38,.54])carrierMegaShot(b,row[0],Math.PI/2+row[1]*o,3.35,'s6cluster',{silent:true});\n      carrierMegaMuzzle(b,'L','s6mb_cyclonemuzzle',1.0);carrierMegaMuzzle(b,'R','s6mb_cyclonemuzzle',1.0);M.cd=1.18;","      carrierClusterFanStart(b);return;",'replace immediate cluster fan');
once("  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);carrierGravityFanDraw(b,false);carrierOmegaDraw(b,false);if(M.phase<1)return;","  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);carrierGravityFanDraw(b,false);carrierOmegaDraw(b,false);carrierClusterFanDraw(b,false);if(M.phase<1)return;",'cluster fields below hull');
once("  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);carrierGravityFanDraw(b,true);carrierOmegaDraw(b,true);","  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);carrierGravityFanDraw(b,true);carrierOmegaDraw(b,true);carrierClusterFanDraw(b,true);",'cluster alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_omega_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_omega_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_cluster_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_CLUSTER_WARNING_0916');
