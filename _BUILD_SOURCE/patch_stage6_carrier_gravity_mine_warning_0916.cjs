const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierPrismFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.prismFan;if(!F||F.released)return false;const paths=carrierPrismFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:24,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n",
`function carrierPrismFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.prismFan;if(!F||F.released)return false;const paths=carrierPrismFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:24,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
/* The Phase-5 gravity pair is deliberately slow, but the two accelerating mines still occupied
   large committed corridors with no advance read. Preserve their mounts, angles and acceleration
   while showing both paths before the authored mine reels leave the hull. */
function carrierGravityFanPaths(b,F){
  if(!b||!F)return [];const len=Math.max(VH,worldWidth())*1.35;return F.lanes.map(q=>{const p=shipBossMount(b,q.slot);return{x:p.x,y:p.y,a:q.a,slot:q.slot,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len};});
}
function carrierGravityFanStart(b){
  const M=b&&b._mega;if(!M||M.gravityFan)return false;const tell=.72,cooldown=1.72,lanes=[{slot:'L',a:Math.PI/2-.20},{slot:'R',a:Math.PI/2+.20}];M.gravityFan={t:0,tell:tell,cooldown:cooldown,id:'stage6-carrier-gravity-mines',lanes:lanes,released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-gravity-mines',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierGravityFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.gravityFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierGravityFanPaths(b,F);for(let i=0;i<paths.length;i++){const p=paths[i];carrierMegaShot(b,p,p.a,1.35,'s6gravity',{silent:i>0,accel:.16,max:2.15,szMul:1.05});}
    carrierMegaMuzzle(b,'L','s6mb_prismmuzzle',.92);carrierMegaMuzzle(b,'R','s6mb_prismmuzzle',.92);if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();}
  if(F.released&&F.t>=F.finish){M.gravityFan=null;M.cd=.02;return false;}return true;
}
function carrierGravityFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.gravityFan;if(!F||F.released)return false;const paths=carrierGravityFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:32,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`,
'gravity mine controller');
once("    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;","    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;",'phase cleanup');
once("  if(carrierPrismFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierPrismFanTick(b,dt))return;\n  if(carrierGravityFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'gravity per-frame tick');
once(
"      for(const row of [[L,-.20],[R,.20]])carrierMegaShot(b,row[0],Math.PI/2+row[1],1.35,'s6gravity',{silent:row[0]!==L,accel:.16,max:2.15,szMul:1.05});\n      carrierMegaMuzzle(b,'L','s6mb_prismmuzzle',.92);carrierMegaMuzzle(b,'R','s6mb_prismmuzzle',.92);M.cd=1.72;",
"      carrierGravityFanStart(b);return;",
'replace immediate gravity pair');
once("  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);if(M.phase<1)return;","  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);carrierGravityFanDraw(b,false);if(M.phase<1)return;",'gravity fields below hull');
once("  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);","  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);carrierGravityFanDraw(b,true);",'gravity alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_prism_crossfire_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_prism_crossfire_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_gravity_mine_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_GRAVITY_MINE_WARNING_0916');
