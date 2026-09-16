const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
function once(old,replacement,label){const n=s.split(old).length-1;if(n!==1)throw new Error(label+' anchor count '+n);s=s.replace(old,replacement);}
once(
"function vileAttack(b){",
`function vileAimedFanPaths(b,V){
  if(!b||!V)return [];const left=vileHardpoint(b,V.left,V.oy),right=vileHardpoint(b,V.right,V.oy);
  return V.entries.map(e=>({x:e.side==='R'?right.x:left.x,y:e.side==='R'?right.y:left.y,a:e.a}));
}
function vileAimedFanStart(b,kind,step){
  if(!b||b._vileFan)return false;const gun=kind==='gunship',y=b.y+b.h*.28,a0=aimPlayer(b.x,y),from=gun?-3:-2,to=gun?3:2,spread=gun?.085:.10;
  const entries=[];for(let k=from;k<=to;k++)entries.push({side:(k&1)?'R':'L',a:a0+k*spread});
  const tell=gun?.58:.62,cooldown=gun?.78:1.05,id=gun?'stage8-vile-gunship-fan':'stage8-vile-needle-fan';
  b._vileFan={t:0,tell:tell,cooldown:cooldown,kind:kind,id:id,left:gun?-.34:-.27,right:gun?.34:.27,oy:gun?.25:.27,entries:entries,released:false,finish:0,homing:!gun&&(step%2)===0,missileOy:y-b.y};
  b.fireCd=cooldown;combatWarningTick(b,id,0,tell,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)();
  return true;
}
function vileAimedFanTick(b,dt){
  const V=b&&b._vileFan;if(!V)return false;V.t+=dt;combatWarningTick(b,V.id,Math.min(V.t,V.tell),V.tell);
  if(!V.released&&V.t>=V.tell){
    V.released=true;V.finish=V.t+Math.max(.14,V.cooldown-V.tell);const paths=vileAimedFanPaths(b,V),gun=V.kind==='gunship';
    for(let i=0;i<paths.length;i++){const p=paths[i];vileAnnihilationShot(p.x,p.y,p.a,gun?4.25:3.65,gun?'s8nf_gunship':'s8nf_needle',{silent:i>0});}
    if(gun){vileMuzzle(b,-.34,.25,'armored_gunship',1.02,.15);vileMuzzle(b,.34,.25,'armored_gunship',1.02,.15);}
    else{vileMuzzle(b,-.27,.27,'needle_interceptor',.92,.15);vileMuzzle(b,.27,.27,'needle_interceptor',.92,.15);}
    if(V.homing&&typeof eMissileHoming==='function')enemyLockOn(b,.55,{fire:function(){eMissileHoming(b.x-b.w*.26,b.y+V.missileOy,-1);eMissileHoming(b.x+b.w*.26,b.y+V.missileOy,1);}});
    if(typeof Audio!=='undefined'&&Audio.SFX&&Audio.SFX.enemyShoot)Audio.SFX.enemyShoot();
  }
  if(V.released&&V.t>=V.finish){b._vileFan=null;return false;}return true;
}
function vileAimedFanDraw(b,front){
  const V=b&&b._vileFan;if(!V||V.released)return false;const paths=vileAimedFanPaths(b,V),k=clamp(V.t/V.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(p.a)*700,ey:p.y+Math.sin(p.a)*700,progress:k,width:V.kind==='gunship'?18:16,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
function vileAttack(b){`,
'aimed fan controller');
once(
"  if(b._annihilation){b.fireCd=.22;return;}\n  if(b._vileWall){b.fireCd=.22;return;}",
"  if(b._annihilation){b.fireCd=.22;return;}\n  if(b._vileWall){b.fireCd=.22;return;}\n  if(b._vileFan){b.fireCd=.22;return;}",
'fan attack guard');
once(
"  } else if(f===1){\n    const a0=aimPlayer(b.x,y);\n    const lp=vileHardpoint(b,-.27,.27),rp=vileHardpoint(b,.27,.27);\n    for(let k=-2;k<=2;k++)vileAnnihilationShot(k&1?rp.x:lp.x,k&1?rp.y:lp.y,a0+k*.10,3.65,'s8nf_needle',{silent:k!==-2});\n    vileMuzzle(b,-.27,.27,'needle_interceptor',.92,.15);vileMuzzle(b,.27,.27,'needle_interceptor',.92,.15);\n    if((step%2)===0 && typeof eMissileHoming==='function'){\n      const _oy=y-b.y;   // THE RETINA LOCK (0912)\n      enemyLockOn(b, 0.55, {fire:function(){\n        eMissileHoming(b.x-b.w*0.26, b.y+_oy, -1);\n        eMissileHoming(b.x+b.w*0.26, b.y+_oy,  1);\n      }});\n    }\n    b.fireCd=1.05;",
"  } else if(f===1){vileAimedFanStart(b,'needle',step);return;",
'second form fan');
once(
"    } else {\n      const a0=aimPlayer(b.x,y);\n      const lp=vileHardpoint(b,-.34,.25),rp=vileHardpoint(b,.34,.25);\n      for(let k=-3;k<=3;k++)vileAnnihilationShot(k&1?rp.x:lp.x,k&1?rp.y:lp.y,a0+k*.085,4.25,'s8nf_gunship',{silent:k!==-3});\n      vileMuzzle(b,-.34,.25,'armored_gunship',1.02,.15);vileMuzzle(b,.34,.25,'armored_gunship',1.02,.15);\n    }\n    b.fireCd=0.78;",
"    } else {vileAimedFanStart(b,'gunship',step);return;}\n    b.fireCd=0.78;",
'final form fan');
once(
"  const F=VILE_FORMS[idx];b._vileWall=null;",
"  const F=VILE_FORMS[idx];b._vileWall=null;b._vileFan=null;",
'clear fan on form change');
once(
"  if(b._vile&&b._vileWall)vileCrescentWallTick(b,dt);",
"  if(b._vile&&b._vileWall)vileCrescentWallTick(b,dt);\n  if(b._vile&&b._vileFan)vileAimedFanTick(b,dt);",
'per-frame fan tick');
once(
"  if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,false);",
"  if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,false);\n  if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,false);",
'fan fields below hull');
once(
"if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,true);if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,true);return;",
"if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,true);if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,true);if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,true);return;",
'fan alert over hull');
if(s.includes('\r'))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE8_VILE_AIMED_FAN_WARNING_0916');
