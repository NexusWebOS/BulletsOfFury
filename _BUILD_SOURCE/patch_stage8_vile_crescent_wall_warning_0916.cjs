const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
function once(old,replacement,label){const n=s.split(old).length-1;if(n!==1)throw new Error(label+' anchor count '+n);s=s.replace(old,replacement);}
once(
"function vileAttack(b){",
`const VILE_CRESCENT_WALL_WARN=.72;
function vileCrescentWallColumns(W,gap){
  const out=[];for(let x=30;x<W-20;x+=46)if(Math.abs(x-gap)>=70)out.push(x);return out;
}
function vileCrescentWallStart(b){
  if(!b||b._vileWall)return false;
  const W=(typeof worldWidth==='function')?worldWidth():VW,gap=W*(.18+.64*(.5+.5*Math.sin((b.t||0)*.8)));
  b._vileWall={t:0,tell:VILE_CRESCENT_WALL_WARN,gap:gap,width:W,columns:vileCrescentWallColumns(W,gap),released:false,finish:0};
  b.fireCd=1.35;combatWarningTick(b,'stage8-vile-crescent-wall',0,VILE_CRESCENT_WALL_WARN,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)();
  return true;
}
function vileCrescentWallTick(b,dt){
  const V=b&&b._vileWall;if(!V)return false;V.t+=dt;
  combatWarningTick(b,'stage8-vile-crescent-wall',Math.min(V.t,V.tell),V.tell);
  if(!V.released&&V.t>=V.tell){
    V.released=true;V.finish=V.t+.32;const y=b.y+b.h*.28;
    for(let i=0;i<V.columns.length;i++)vileAnnihilationShot(V.columns[i],y,Math.PI/2,2.25,'s8nf_crescent',{silent:i>0});
    vileMuzzle(b,0,.33,'stealth_crescent',1.12,.20);shake=Math.max(shake,5);
    if(typeof Audio!=='undefined'&&Audio.SFX&&Audio.SFX.enemyShoot)Audio.SFX.enemyShoot();
  }
  if(V.released&&V.t>=V.finish){b._vileWall=null;return false;}return true;
}
function vileCrescentWallDraw(b,front){
  const V=b&&b._vileWall;if(!V||V.released)return false;
  const y=b.y+b.h*.28,k=clamp(V.t/V.tell,0,1);
  if(!front)for(const x of V.columns)combatWarningDraw(b,{x:x,y:y,ex:x,ey:VH+40,progress:k,width:25,fieldOnly:true});
  else combatWarningDraw(b,{x:b.x,y:y,ex:b.x,ey:VH+40,progress:k,alertOnly:true,alertX:b.x,alertY:54});
  return true;
}
function vileAttack(b){`,
'crescent wall controller');
once(
"  if(b._annihilation){b.fireCd=.22;return;}\n  if(f===3&&!b._annihilationUsed){vileAnnihilationStart(b);return;}\n  if(f===0){\n    const gap=W*(0.18+0.64*(0.5+0.5*Math.sin((b.t||0)*0.8)));\n    for(let x=30;x<W-20;x+=46){\n      if(Math.abs(x-gap)<70) continue;\n      vileAnnihilationShot(x,y,Math.PI/2,2.25,'s8nf_crescent',{silent:x>30});\n    }\n    vileMuzzle(b,0,.33,'stealth_crescent',1.12,.20);\n    b.fireCd=1.35;\n  } else if(f===1){",
"  if(b._annihilation){b.fireCd=.22;return;}\n  if(b._vileWall){b.fireCd=.22;return;}\n  if(f===3&&!b._annihilationUsed){vileAnnihilationStart(b);return;}\n  if(f===0){vileCrescentWallStart(b);return;\n  } else if(f===1){",
'replace instant form-zero wall');
once("  const W=(typeof worldWidth==='function')?worldWidth():VW;\n  const step=(b._vAtk=(b._vAtk|0)+1);","  const step=(b._vAtk=(b._vAtk|0)+1);",'remove obsolete wall width');
once(
"function vileBuildForm(b, idx){\n  const F=VILE_FORMS[idx];",
"function vileBuildForm(b, idx){\n  const F=VILE_FORMS[idx];b._vileWall=null;",
'clear wall on form change');
once(
"  if(b._vile&&b._annihilation)vileAnnihilationTick(b,dt);",
"  if(b._vile&&b._annihilation)vileAnnihilationTick(b,dt);\n  if(b._vile&&b._vileWall)vileCrescentWallTick(b,dt);",
'per-frame wall tick');
once(
"  if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,false);",
"  if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,false);\n  if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,false);",
'wall fields below hull');
once(
"  if(b._vile&&_animK&&_animK.indexOf('s8symboss_form_')===0){if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,true);return;}",
"  if(b._vile&&_animK&&_animK.indexOf('s8symboss_form_')===0){if(b._annihilation&&typeof vileAnnihilationDraw==='function')vileAnnihilationDraw(b,true);if(b._vileWall&&typeof vileCrescentWallDraw==='function')vileCrescentWallDraw(b,true);return;}",
'wall alert over hull');
if(s.includes('\r'))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE8_VILE_CRESCENT_WALL_WARNING_0916');
