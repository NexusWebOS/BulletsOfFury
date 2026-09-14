#!/usr/bin/env node
'use strict';

const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets','game.js'),'utf8');

function block(start,end){
  const a=src.indexOf(start), b=src.indexOf(end,a+start.length);
  if(a<0||b<0) throw new Error(`Missing block: ${start}`);
  return src.slice(a,b);
}
function ok(value,message){ if(!value) throw new Error(message); }

const hit=block('function weaponHitSfx(el){','function flameHit(');
ok(hit.includes("el='normal'"),'impact limiter is not shared across all weapons');
ok(hit.includes('if(S.hit) S.hit()'),'normal impact cue is not the sole impact route');
for(const forbidden of ['iceBreathHit','flameHit||','laserBeamHit','S.shatter','S.crackle'])
  ok(!hit.includes(forbidden),`specialized impact cue remains in weaponHitSfx: ${forbidden}`);

const elemental=block('function opposingElementImpact(','const ORB_FIRE_ON_L3');
ok(elemental.includes("'#ff3b30'"),'fire-on-ice red flash is missing');
ok(elemental.includes("'#83d9ff'"),'ice-on-fire light-blue flash is missing');
ok(elemental.includes("role==='boss'&&run&&run.stage===8"),'Stage 8 final-boss exemption is missing');
ok(!elemental.includes('pImpacts.push'),'elemental impact still creates a separate effect object');

const impactDraw=block('/* PLAYER IMPACTS','function metalPanel(');
for(const forbidden of ['ctx.ellipse','nx_ice_','nx_fire0_','quadraticCurveTo','nwp_kin_hit_spark'])
  ok(!impactDraw.includes(forbidden),`ornamental elemental drawing remains: ${forbidden}`);

ok(src.includes("e.hp-=dmg; e.flash=0.12; weaponHitSfx('normal');"),'enemy damage does not use normal impact');
ok(src.includes("b.hp-=dmg; b.flash=0.18;\n  weaponHitSfx('normal');"),'miniboss damage does not use normal impact');
ok(src.includes("boss.hp-=dmg; boss.flash=0.08;"),'boss elemental flash timer is not active');
ok((src.match(/hitFlashColor\(/g)||[]).length>=24,'element flash color is not wired through enemy/boss renderers');

console.log(JSON.stringify({
  normalImpactOnly:true,
  elementalFlashes:{fireOnIce:'#ff3b30',iceOnFire:'#83d9ff'},
  ornamentalElementFxRemoved:true,
  stage8BossExempt:true,
  rendererRoutes:(src.match(/hitFlashColor\(/g)||[]).length
},null,2));
