const fs=require('fs'),path=require('path');const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once("function s7WardenPhase(b,phase){\n  const S=b._s7warden,F=S.final;F.phase=phase;F.t=0;F.beat=0;S.mt=0;S.shot=0;S.event=0;\n  S.noHit=['portalClose','teleportIn','walkIn','roar','hyper','legBurst','defeat','escape'].indexOf(phase)>=0;\n}","function s7WardenPhase(b,phase){\n  const S=b._s7warden,F=S.final;if(F.crippleRail&&!F.crippleRail.released)combatWarningTick(b,F.crippleRail.id,F.crippleRail.warn,F.crippleRail.warn,true);if(phase!=='cripple')F.crippleRail=null;\n  F.phase=phase;F.t=0;F.beat=0;S.mt=0;S.shot=0;S.event=0;\n  S.noHit=['portalClose','teleportIn','walkIn','roar','hyper','legBurst','defeat','escape'].indexOf(phase)>=0;\n}",'phase warning cleanup');
const controller=`const S7_WARDEN_CRIPPLE_WARN=.58;
function s7WardenCrippleRailPaths(b,C){
  if(!b||!C)return [];const len=Math.max(VH,worldWidth())*1.25,spec=[['L',C.aim],['R',C.aim],['L',C.aim-.07],['R',C.aim+.07]];
  return spec.map(q=>{const p=shipBossMount(b,q[0]),a=q[1];return{slot:q[0],x:p.x,y:p.y,a:a,ex:p.x+Math.cos(a)*len,ey:p.y+Math.sin(a)*len};});
}
function s7WardenCrippleRailArm(b){
  const S=b&&b._s7warden,F=S&&S.final;if(!F||F.crippleRail)return false;const aim=aimPlayer(b.x,b.y+b.h*.14);
  F.crippleRail={t:0,warn:S7_WARDEN_CRIPPLE_WARN,aim:aim,shot:0,fire:0,id:'stage7-warden-cripple-rail',released:false};
  combatWarningTick(b,'stage7-warden-cripple-rail',0,S7_WARDEN_CRIPPLE_WARN,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();return true;
}
function s7WardenCrippleRailTick(b,dt){
  const S=b&&b._s7warden,F=S&&S.final;if(!F)return false;let C=F.crippleRail;
  if(!C){F.fire=(F.fire||0)-dt;if(F.fire<=0)s7WardenCrippleRailArm(b);return true;}
  if(!C.released){C.t+=dt;combatWarningTick(b,C.id,Math.min(C.t,C.warn),C.warn);if(C.t<C.warn)return true;dt=Math.max(0,C.t-C.warn);C.released=true;C.fire=0;}
  C.fire-=dt;while(C.shot<4&&C.fire<=0){C.shot++;if(C.shot===4){s7WardenShot(b,'L',C.aim-.07,4.65,'rail',{});s7WardenShot(b,'R',C.aim+.07,4.65,'rail',{silent:true});s7WardenMuzzle(b,'L',true);s7WardenMuzzle(b,'R',true);C.fire+=.54;}else{const slot=(C.shot&1)?'L':'R';s7WardenShot(b,slot,C.aim,5.25,'rail',{});s7WardenMuzzle(b,slot,false);C.fire+=.19;}}
  if(C.shot>=4&&C.fire<=0){F.crippleRail=null;F.fire=.01;}return true;
}
function s7WardenCrippleRailWarningDraw(b,front){
  const S=b&&b._s7warden,F=S&&S.final,C=F&&F.crippleRail;if(!C||C.released||F.phase!=='cripple')return false;const paths=s7WardenCrippleRailPaths(b,C),k=clamp(C.t/C.warn,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:20,fieldOnly:true});else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:52});return true;
}
`;
once("function s7WardenMuzzle(b,slot,large){\n  const p=shipBossMount(b,slot);navalFlash(null,p,large?1.18:.82,BPFX_MUZZLE_LASER,{n:8,hpx:large?72:48,life:large?.22:.14,\n    anchor:.42,follow:()=>b&&!b.dead?shipBossMount(b,slot):null});\n}\n","function s7WardenMuzzle(b,slot,large){\n  const p=shipBossMount(b,slot);navalFlash(null,p,large?1.18:.82,BPFX_MUZZLE_LASER,{n:8,hpx:large?72:48,life:large?.22:.14,\n    anchor:.42,follow:()=>b&&!b.dead?shipBossMount(b,slot):null});\n}\n"+controller,'cripple rail controller');
once("if(F.t>=1.28){b.hp=Math.max(1,Math.min(b.hp,b.maxhp*.24));S.noHit=false;s7WardenPhase(b,'cripple');F.fire=.16;F.volley=0;}","if(F.t>=1.28){b.hp=Math.max(1,Math.min(b.hp,b.maxhp*.24));S.noHit=false;s7WardenPhase(b,'cripple');F.fire=.16;F.volley=0;F.crippleRail=null;}",'cripple entry');
once("    F.fire-=dt;if(F.fire<=0){F.volley++;const aim=aimPlayer(b.x,b.y+b.h*.14);\n      if(F.volley%4===0){s7WardenShot(b,'L',aim-.07,4.65,'rail',{});s7WardenShot(b,'R',aim+.07,4.65,'rail',{silent:true});s7WardenMuzzle(b,'L',true);s7WardenMuzzle(b,'R',true);F.fire=.54;}\n      else{s7WardenShot(b,(F.volley&1)?'L':'R',aim,5.25,'rail',{});s7WardenMuzzle(b,(F.volley&1)?'L':'R',false);F.fire=.19;}}\n    return true;","    s7WardenCrippleRailTick(b,dt);return true;",'replace untelegraphed cripple rails');
once("  s7WardenBurstWarningDraw(b,false);s7WardenRailWarningDraw(b,false);s7WardenMineWarningDraw(b,false);","  s7WardenBurstWarningDraw(b,false);s7WardenRailWarningDraw(b,false);s7WardenMineWarningDraw(b,false);s7WardenCrippleRailWarningDraw(b,false);",'cripple fields under hull');
once("  s7WardenBurstWarningDraw(b,true);s7WardenRailWarningDraw(b,true);s7WardenMineWarningDraw(b,true);","  s7WardenBurstWarningDraw(b,true);s7WardenRailWarningDraw(b,true);s7WardenMineWarningDraw(b,true);s7WardenCrippleRailWarningDraw(b,true);",'cripple alert over hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);console.log('PATCHED_STAGE7_WARDEN_CRIPPLE_RAIL_WARNING_0916');
