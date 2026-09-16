const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p);
function once(old,replacement,label){
  const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');
  if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);
}
once(
"  if(b._vile&&b._vileFan)vileAimedFanTick(b,dt);",
"  if(b._vile&&b._vileFan)vileAimedFanTick(b,dt);\n  if(b._vile&&b._vileSolar)vileSolarWheelTick(b,dt);",
'solar per-frame tick');
once(
"function vileAttack(b){",
`function vileSolarWheelPaths(b,V){
  if(!b||!V)return [];const p=vileHardpoint(b,0,.30);return V.angles.map(a=>({x:p.x,y:p.y,a:a}));
}
function vileSolarWheelStart(b){
  if(!b||b._vileSolar)return false;const base=(b._vRot=(b._vRot||0)+.19),angles=[];for(let k=0;k<9;k++)angles.push(base+k*TAU/9);
  b._vileSolar={t:0,tell:.62,cooldown:.95,id:'stage8-vile-solar-wheel',angles:angles,released:false,finish:0};
  b.fireCd=.95;combatWarningTick(b,'stage8-vile-solar-wheel',0,.62,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)();
  return true;
}
function vileSolarWheelTick(b,dt){
  const V=b&&b._vileSolar;if(!V)return false;V.t+=dt;combatWarningTick(b,V.id,Math.min(V.t,V.tell),V.tell);
  if(!V.released&&V.t>=V.tell){
    V.released=true;V.finish=V.t+Math.max(.14,V.cooldown-V.tell);const paths=vileSolarWheelPaths(b,V);
    for(let i=0;i<paths.length;i++){const p=paths[i];vileAnnihilationShot(p.x,p.y,p.a,2.45,'s8nf_solar',{silent:i>0});}
    vileMuzzle(b,0,.30,'solar_corvette',1.22,.22);if(typeof Audio!=='undefined'&&Audio.SFX&&Audio.SFX.enemyShoot)Audio.SFX.enemyShoot();
  }
  if(V.released&&V.t>=V.finish){b._vileSolar=null;return false;}return true;
}
function vileSolarWheelDraw(b,front){
  const V=b&&b._vileSolar;if(!V||V.released)return false;const paths=vileSolarWheelPaths(b,V),k=clamp(V.t/V.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(p.a)*700,ey:p.y+Math.sin(p.a)*700,progress:k,width:17,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
function vileAttack(b){`,
'solar wheel controller');
once(
"  if(b._vileFan){b.fireCd=.22;return;}",
"  if(b._vileFan){b.fireCd=.22;return;}\n  if(b._vileSolar){b.fireCd=.22;return;}",
'solar attack guard');
once(
"    } else {\n      const p=vileHardpoint(b,0,.30),base=(b._vRot=(b._vRot||0)+.19);\n      for(let k=0;k<9;k++)vileAnnihilationShot(p.x,p.y,base+k*TAU/9,2.45,'s8nf_solar',{silent:k>0});\n      vileMuzzle(b,0,.30,'solar_corvette',1.22,.22);\n    }",
"    } else {vileSolarWheelStart(b);return;}",
'Leviathan solar wheel');
once(
"  const F=VILE_FORMS[idx];b._vileWall=null;b._vileFan=null;",
"  const F=VILE_FORMS[idx];b._vileWall=null;b._vileFan=null;b._vileSolar=null;",
'clear solar warning on form change');
once(
"  if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,false);",
"  if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,false);\n  if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,false);",
'solar fields below hull');
once(
"if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,true);return;",
"if(b._vileFan&&typeof vileAimedFanDraw==='function')vileAimedFanDraw(b,true);if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,true);return;",
'solar alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s);console.log('PATCHED_STAGE8_VILE_SOLAR_WHEEL_WARNING_0916');
