const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"  if(b._vile&&b._vileSolar)vileSolarWheelTick(b,dt);",
"  if(b._vile&&b._vileSolar)vileSolarWheelTick(b,dt);\n  if(b._vile&&b._vileMissiles)vileMissileSalvoTick(b,dt);",
'missile per-frame tick');
once(
"function vileAttack(b){",
`function vileMissileSalvoPaths(b,V){
  if(!b||!V)return [];const y=b.y+b.h*.28;return V.offsets.map(fx=>({x:b.x+b.w*fx,y:y,a:Math.PI/2,fx:fx}));
}
function vileMissileSalvoStart(b){
  if(!b||b._vileMissiles)return false;b._vileMissiles={t:0,tell:.58,cooldown:.78,id:'stage8-vile-missile-salvo',offsets:[-.30,-.10,.10,.30],released:false,finish:0};
  b.fireCd=.78;combatWarningTick(b,'stage8-vile-missile-salvo',0,.58,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)();
  return true;
}
function vileMissileSalvoTick(b,dt){
  const V=b&&b._vileMissiles;if(!V)return false;V.t+=dt;combatWarningTick(b,V.id,Math.min(V.t,V.tell),V.tell);
  if(!V.released&&V.t>=V.tell){
    V.released=true;V.finish=V.t+Math.max(.14,V.cooldown-V.tell);const paths=vileMissileSalvoPaths(b,V);
    for(let i=0;i<paths.length;i++){const p=paths[i];eMissile(p.x,p.y);vileMuzzle(b,p.fx,.28,'armored_gunship',.82,.14);}
  }
  if(V.released&&V.t>=V.finish){b._vileMissiles=null;return false;}return true;
}
function vileMissileSalvoDraw(b,front){
  const V=b&&b._vileMissiles;if(!V||V.released)return false;const paths=vileMissileSalvoPaths(b,V),k=clamp(V.t/V.tell,0,1);
  if(!front)for(const p of paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH+40,progress:k,width:20,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
function vileAttack(b){`,
'missile salvo controller');
once(
"  if(b._vileSolar){b.fireCd=.22;return;}",
"  if(b._vileSolar){b.fireCd=.22;return;}\n  if(b._vileMissiles){b.fireCd=.22;return;}",
'missile attack guard');
once(
"    } else if((step%3)===0 && typeof eMissile==='function'){\n      for(const fx of [-0.30,-0.10,0.10,0.30]){eMissile(b.x+b.w*fx,y);vileMuzzle(b,fx,.28,'armored_gunship',.82,.14);}\n    } else {vileAimedFanStart(b,'gunship',step);return;}",
"    } else if((step%3)===0 && typeof eMissile==='function'){vileMissileSalvoStart(b);return;} else {vileAimedFanStart(b,'gunship',step);return;}",
'Furious missile salvo');
once(
"  const F=VILE_FORMS[idx];b._vileWall=null;b._vileFan=null;b._vileSolar=null;",
"  const F=VILE_FORMS[idx];b._vileWall=null;b._vileFan=null;b._vileSolar=null;b._vileMissiles=null;",
'clear missile warning on form change');
once(
"  if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,false);",
"  if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,false);\n  if(b._vileMissiles&&typeof vileMissileSalvoDraw==='function')vileMissileSalvoDraw(b,false);",
'missile fields below hull');
once(
"if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,true);return;",
"if(b._vileSolar&&typeof vileSolarWheelDraw==='function')vileSolarWheelDraw(b,true);if(b._vileMissiles&&typeof vileMissileSalvoDraw==='function')vileMissileSalvoDraw(b,true);return;",
'missile alert above hull');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s);console.log('PATCHED_STAGE8_VILE_MISSILE_SALVO_WARNING_0916');
