const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierNodeFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.nodeFan;if(!F||F.released)return false;const paths=carrierNodeFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});\n  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;\n}\n",
`function carrierNodeFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.nodeFan;if(!F||F.released)return false;const paths=carrierNodeFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
/* Once all four storm nodes are gone, the Carrier's four authored upper barrels alternate two
   crossing prism geometries. Commit all four angles before the shared warning; hardpoint origins
   keep following the sliding hull, but player movement cannot bend this fixed crossfire. */
function carrierPrismFanPaths(b,F){
  if(!b||!F)return [];const len=Math.max(VH,worldWidth())*1.35;return F.lanes.map(q=>{const p=carrierHP(b,q.slot);return{x:p.x,y:p.y,a:q.a,slot:q.slot,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len};});
}
function carrierPrismFanStart(b){
  const M=b&&b._mega;if(!M||M.prismFan)return false;const step=M.step|0,tell=.62,cooldown=1.25,slots=['upper_left_outer','upper_left_inner','upper_right_inner','upper_right_outer'],degrees=(step&2)?[-22,-8,8,22]:[22,8,-8,-22];
  const lanes=slots.map((slot,i)=>({slot:slot,a:Math.PI/2+degrees[i]*Math.PI/180}));M.prismFan={t:0,tell:tell,cooldown:cooldown,id:'stage6-carrier-prism-crossfire',step:step,lanes:lanes,released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-prism-crossfire',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierPrismFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.prismFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierPrismFanPaths(b,F);for(let i=0;i<paths.length;i++){const p=paths[i];carrierMegaShot(b,p,p.a,4.3,'s6prism',{silent:i>0});}
    for(const slot of ['L','C','R'])carrierMegaMuzzle(b,slot,'s6mb_prismmuzzle',1.08);if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();}
  if(F.released&&F.t>=F.finish){M.prismFan=null;M.cd=.02;return false;}return true;
}
function carrierPrismFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.prismFan;if(!F||F.released)return false;const paths=carrierPrismFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:24,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`,
'prism fan controller');
once("    for(const q of [M.cycloneFan,M.nodeFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;","    for(const q of [M.cycloneFan,M.nodeFan,M.prismFan])if(q)combatWarningTick(b,q.id,q.tell,q.tell,true);M.cycloneFan=null;M.nodeFan=null;M.prismFan=null;",'phase cleanup');
once("  if(carrierNodeFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierNodeFanTick(b,dt))return;\n  if(carrierPrismFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'prism per-frame tick');
once(
`      const _ub=['upper_left_outer','upper_left_inner','upper_right_inner','upper_right_outer'];
      const _ua=(M.step&2)?[-22,-8,8,22]:[22,8,-8,-22];
      for(let _i=0;_i<4;_i++){
        const pt=carrierHP(b,_ub[_i]);
        carrierMegaShot(b,pt,Math.PI/2+_ua[_i]*Math.PI/180,4.3,'s6prism',{silent:_i>0});
      }
      for(const slot of ['L','C','R'])carrierMegaMuzzle(b,slot,'s6mb_prismmuzzle',1.08);M.cd=1.25;`,
"      carrierPrismFanStart(b);return;",
'replace immediate prism crossfire');
once("  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);if(M.phase<1)return;","  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);carrierPrismFanDraw(b,false);if(M.phase<1)return;",'prism fields below hull');
once("  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);","  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);carrierPrismFanDraw(b,true);",'prism alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_node_fan_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_node_fan_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_prism_crossfire_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_PRISM_CROSSFIRE_WARNING_0916');
