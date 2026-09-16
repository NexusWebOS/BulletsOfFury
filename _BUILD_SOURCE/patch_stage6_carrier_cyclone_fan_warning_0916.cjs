const fs=require('fs'),path=require('path');
const gamePath=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierMegaShot(b,p,a,sp,kind,opts){\n  opts=opts||{};const q=eShootT(p.x,p.y,a,sp,kind,opts);q._boss=true;\n  if(opts.accel){q._s6Accel=opts.accel;q._s6Max=opts.max||sp*1.8;}return q;\n}\n",
`function carrierMegaShot(b,p,a,sp,kind,opts){
  opts=opts||{};const q=eShootT(p.x,p.y,a,sp,kind,opts);q._boss=true;
  if(opts.accel){q._s6Accel=opts.accel;q._s6Max=opts.max||sp*1.8;}return q;
}
/* The carrier's opening twin rotary rake used to aim and release six 4.1-speed cyclone tracers in
   the same frame.  Keep the exact two batteries, mirrored offsets and cooldown, but commit the six
   angles at the start of a short shared warning so a late dodge is useful and cannot bend the fan. */
function carrierCycloneFanPaths(b,F){
  if(!b||!F)return [];const len=Math.max(VH,worldWidth())*1.35;
  return F.lanes.map(q=>{const p=shipBossMount(b,q.slot);return{x:p.x,y:p.y,a:q.a,slot:q.slot,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len};});
}
function carrierCycloneFanStart(b){
  const M=b&&b._mega;if(!M||M.cycloneFan)return false;const phase=M.phase|0,tell=.62,cooldown=phase===2?1.12:1.35,lanes=[];
  for(const row of [['MG_L',-1],['MG_R',1]]){const p=shipBossMount(b,row[0]),a=aimPlayer(p.x,p.y);for(const o of [-.15,0,.15])lanes.push({slot:row[0],a:a+o*row[1]});}
  M.cycloneFan={t:0,tell:tell,cooldown:cooldown,id:'stage6-carrier-cyclone-fan',lanes:lanes,released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-cyclone-fan',0,tell,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();
  return true;
}
function carrierCycloneFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.cycloneFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierCycloneFanPaths(b,F);
    for(let i=0;i<paths.length;i++){const p=paths[i];carrierMegaShot(b,p,p.a,4.1,'s6cyclone',{silent:(i%3)!==1});}
    carrierMegaMuzzle(b,'MG_L','s6mb_cyclonemuzzle',.92);carrierMegaMuzzle(b,'MG_R','s6mb_cyclonemuzzle',.92);
    if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();
  }
  if(F.released&&F.t>=F.finish){M.cycloneFan=null;M.cd=.02;return false;}return true;
}
function carrierCycloneFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.cycloneFan;if(!F||F.released)return false;const paths=carrierCycloneFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:25,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
`,
'cyclone fan controller');
once(
"  if(carrierThunderheadTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",
"  if(carrierThunderheadTick(b,dt))return;\n  if(carrierCycloneFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",
'cyclone per-frame tick');
once(
"    const ML=shipBossMount(b,'MG_L'),MR=shipBossMount(b,'MG_R');\n    for(const row of [[ML,-1],[MR,1]]){const a=aimPlayer(row[0].x,row[0].y);for(const o of [-.15,0,.15])carrierMegaShot(b,row[0],a+o*row[1],4.1,'s6cyclone',{silent:o!==0});}\n    carrierMegaMuzzle(b,'MG_L','s6mb_cyclonemuzzle',.92);carrierMegaMuzzle(b,'MG_R','s6mb_cyclonemuzzle',.92);M.cd=(M.phase===2?1.12:1.35);",
"    carrierCycloneFanStart(b);return;",
'replace immediate cyclone fan');
once(
"function carrierMegaDrawUnder(b){\n  const M=b&&b._mega;if(!M||M.phase<1||typeof XART==='undefined')return;\n  carrierThunderheadDraw(b,false);",
"function carrierMegaDrawUnder(b){\n  const M=b&&b._mega;if(!M||typeof XART==='undefined')return;\n  carrierCycloneFanDraw(b,false);if(M.phase<1)return;\n  carrierThunderheadDraw(b,false);",
'cyclone fields below hull');
once(
"function carrierMegaDrawOver(b){\n  const M=b&&b._mega;if(!M||M.phase<1||typeof XART==='undefined')return;const fi=Math.floor(M.t*11)%8,key='s6mb_stormnode_'+fi;",
"function carrierMegaDrawOver(b){\n  const M=b&&b._mega;if(!M||typeof XART==='undefined')return;\n  if(M.phase<1){carrierCycloneFanDraw(b,true);return;}const fi=Math.floor(M.t*11)%8,key='s6mb_stormnode_'+fi;",
'cyclone alert in phase zero');
once(
"  carrierThunderheadDraw(b,true);\n}",
"  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);\n}",
'cyclone alert after nodes');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath);const old=Buffer.from("require('./test_stage8_vile_missile_salvo_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage8_vile_missile_salvo_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_cyclone_fan_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);
console.log('PATCHED_STAGE6_CARRIER_CYCLONE_FAN_WARNING_0916');
