const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierGravityFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.gravityFan;if(!F||F.released)return false;const paths=carrierGravityFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:32,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n",
`function carrierGravityFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.gravityFan;if(!F||F.released)return false;const paths=carrierGravityFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:32,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
/* Last Run omega bombs accelerate sharply down a fixed centre corridor. Commit that corridor
   before either authored speed variant leaves the live centre mount. */
function carrierOmegaPath(b,F){
  if(!b||!F)return null;const p=shipBossMount(b,'C'),len=Math.max(VH,worldWidth())*1.35;return{x:p.x,y:p.y,a:F.a,ex:p.x+Math.cos(F.a)*len,ey:p.y+Math.sin(F.a)*len};
}
function carrierOmegaStart(b,sp,cooldown){
  const M=b&&b._mega;if(!M||M.omegaBomb)return false;const tell=.66;M.omegaBomb={t:0,tell:tell,cooldown:cooldown,sp:sp,a:Math.PI/2,id:'stage6-carrier-omega-bomb',released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-omega-bomb',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierOmegaTick(b,dt){
  const M=b&&b._mega,F=M&&M.omegaBomb;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const p=carrierOmegaPath(b,F);carrierMegaShot(b,p,p.a,F.sp,'s6omega',{accel:1.05,max:5.2,szMul:1.15});carrierMegaMuzzle(b,'C','s6mb_prismmuzzle',1.30);if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();}
  if(F.released&&F.t>=F.finish){M.omegaBomb=null;M.cd=.02;return false;}return true;
}
function carrierOmegaDraw(b,front){
  const M=b&&b._mega,F=M&&M.omegaBomb;if(!F||F.released)return false;const p=carrierOmegaPath(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:38,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`,
'omega warning controller');
once("    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;","    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan,M.gravityFan,M.omegaBomb])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;M.gravityFan=null;M.omegaBomb=null;",'phase cleanup');
once("  if(carrierGravityFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierGravityFanTick(b,dt))return;\n  if(carrierOmegaTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'omega per-frame tick');
once("      carrierMegaShot(b,C,Math.PI/2,1.1,'s6omega',{accel:1.05,max:5.2,szMul:1.15});carrierMegaMuzzle(b,'C','s6mb_prismmuzzle',1.30);M.cd=1.45;","      carrierOmegaStart(b,1.1,1.45);return;",'primary omega launch');
once("        carrierMegaShot(b,C,Math.PI/2,1.25,'s6omega',{accel:1.05,max:5.2,szMul:1.15});\n        carrierMegaMuzzle(b,'C','s6mb_prismmuzzle',1.30); M.cd=1.20;","        carrierOmegaStart(b,1.25,1.20);return;",'alternate omega launch');
once("  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);carrierGravityFanDraw(b,false);if(M.phase<1)return;","  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);carrierGravityFanDraw(b,false);carrierOmegaDraw(b,false);if(M.phase<1)return;",'omega field below hull');
once("  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);carrierGravityFanDraw(b,true);","  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);carrierGravityFanDraw(b,true);carrierOmegaDraw(b,true);",'omega alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_last_run_slide_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_last_run_slide_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_omega_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_OMEGA_WARNING_0916');
