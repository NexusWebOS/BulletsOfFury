const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"function carrierCycloneFanDraw(b,front){\n  const M=b&&b._mega,F=M&&M.cycloneFan;if(!F||F.released)return false;const paths=carrierCycloneFanPaths(b,F),k=clamp(F.t/F.tell,0,1);\n  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:25,fieldOnly:true});\n  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});\n  return true;\n}\n",
`function carrierCycloneFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.cycloneFan;if(!F||F.released)return false;const paths=carrierCycloneFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:25,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
/* Shield-down phases alternate the four storm nodes and widen each surviving node from three to
   five cyclone lanes.  Commit node identity, parity and aim here; destroying a warned node still
   disarms its own lanes, but moving after green cannot turn any surviving lane. */
function carrierNodeFanPaths(b,F){
  const M=b&&b._mega;if(!M||!F)return [];const len=Math.max(VH,worldWidth())*1.35,out=[];
  for(const q of F.lanes){const n=M.nodes.find(v=>v.id===q.node);if(!n||n.dead)continue;const p=carrierMegaNodePos(b,n);out.push({x:p.x,y:p.y,a:q.a,node:q.node,sp:q.sp,ex:p.x+Math.cos(q.a)*len,ey:p.y+Math.sin(q.a)*len});}return out;
}
function carrierNodeFanStart(b){
  const M=b&&b._mega;if(!M||M.nodeFan)return false;const phase=M.phase|0,step=M.step|0,tell=.62,cooldown=phase>=3?1.12:1.55,lanes=[],alive=M.nodes.filter(n=>!n.dead),parity=step&1;
  for(let i=0;i<M.nodes.length;i++){const n=M.nodes[i];if(n.dead||(i&1)!==parity)continue;const p=carrierMegaNodePos(b,n),a=aimPlayer(p.x,p.y);for(const o of (phase>=3?[-.34,-.17,0,.17,.34]:[-.16,0,.16]))lanes.push({node:n.id,a:a+o,sp:3.15});}
  if(!lanes.length&&alive.length){const n=alive[step%alive.length],p=carrierMegaNodePos(b,n);lanes.push({node:n.id,a:aimPlayer(p.x,p.y),sp:3.35});}
  if(!lanes.length)return false;M.nodeFan={t:0,tell:tell,cooldown:cooldown,id:'stage6-carrier-node-fan',phase:phase,step:step,lanes:lanes,released:false,finish:0};M.cd=cooldown;
  combatWarningTick(b,'stage6-carrier-node-fan',0,tell,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function carrierNodeFanTick(b,dt){
  const M=b&&b._mega,F=M&&M.nodeFan;if(!F)return false;F.t+=dt;combatWarningTick(b,F.id,Math.min(F.t,F.tell),F.tell);
  if(!F.released&&F.t>=F.tell){F.released=true;F.finish=F.t+Math.max(.14,F.cooldown-F.tell);const paths=carrierNodeFanPaths(b,F);
    for(let i=0;i<paths.length;i++){const p=paths[i];carrierMegaShot(b,p,p.a,p.sp,'s6cyclone',{silent:i>0});}
    if(!b._s9Beam){const charged=(F.step%4)===3,tap=(F.phase>=3)||((F.step%2)===1);if(charged)s9aBeamStart(b,{charge:.62,off:1.70,end:2.05,w:64});else if(tap)s9aBeamStart(b,{charge:.24,off:.58,end:.74,w:30});if(b._s9Beam)carrierMegaMuzzle(b,'C','s6mb_prismmuzzle',charged?1.30:.90);}
    if(Audio.SFX&&(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch))(Audio.SFX.enemyBossCannon||Audio.SFX.spaceVolleyLaunch)();
  }
  if(F.released&&F.t>=F.finish){M.nodeFan=null;M.cd=.02;return false;}return true;
}
function carrierNodeFanDraw(b,front){
  const M=b&&b._mega,F=M&&M.nodeFan;if(!F||F.released)return false;const paths=carrierNodeFanPaths(b,F),k=clamp(F.t/F.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:23,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});return true;
}
`,
'node fan controller');
once("  if(carrierCycloneFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.","  if(carrierCycloneFanTick(b,dt))return;\n  if(carrierNodeFanTick(b,dt))return;\n  /* The launch/cannon reels own their beat.",'node fan per-frame tick');
once(
`    const alive=M.nodes.filter(n=>!n.dead),parity=M.step&1;let fired=0;
    for(let i=0;i<M.nodes.length;i++){const n=M.nodes[i];if(n.dead||(i&1)!==parity)continue;const p=carrierMegaNodePos(b,n),a=aimPlayer(p.x,p.y);
      for(const o of (M.phase>=3?[-.34,-.17,0,.17,.34]:[-.16,0,.16]))
        carrierMegaShot(b,p,a+o,3.15,'s6cyclone',{silent:fired++>0});}
    if(!fired&&alive.length){const n=alive[M.step%alive.length],p=carrierMegaNodePos(b,n),a=aimPlayer(p.x,p.y);carrierMegaShot(b,p,a,3.35,'s6cyclone',{});}
    /* THE LANCE: short TAPS between volleys, a long CHARGED burn to punctuate. Phase 4 taps every
       volley instead of every other one. Never stacked on a live beam. */
    if(!b._s9Beam){
      const _chg=(M.step%4)===3, _tap=(M.phase>=3)||((M.step%2)===1);
      if(_chg)      s9aBeamStart(b,{charge:.62,off:1.70,end:2.05,w:64});
      else if(_tap) s9aBeamStart(b,{charge:.24,off:.58,end:.74,w:30});
      if(b._s9Beam) carrierMegaMuzzle(b,'C','s6mb_prismmuzzle',_chg?1.30:.90);
    }
    M.cd=(M.phase>=3?1.12:1.55);`,
"    carrierNodeFanStart(b);return;",
'replace immediate node fan');
once("  carrierCycloneFanDraw(b,false);if(M.phase<1)return;","  carrierCycloneFanDraw(b,false);carrierNodeFanDraw(b,false);if(M.phase<1)return;",'node fields below hull');
once("  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);","  carrierThunderheadDraw(b,true);carrierCycloneFanDraw(b,true);carrierNodeFanDraw(b,true);",'node alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_cyclone_fan_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_cyclone_fan_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_node_fan_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_NODE_FAN_WARNING_0916');
