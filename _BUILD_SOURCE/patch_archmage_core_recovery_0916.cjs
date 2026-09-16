const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
let s=fs.readFileSync(file,'utf8');
function once(from,to,label){
  const n=s.split(from).length-1;
  if(n!==1)throw new Error(`${label}: expected one match, got ${n}`);
  s=s.replace(from,to);
}

once(
  "function archBlit(key,frame,x,y,h,tint,rot,alpha){const q=hammerArchFrame(key,frame,tint);if(!q)return false;const w=h*q.sw/q.sh;ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,-w/2,-h/2,w,h);ctx.restore();return true;}\n",
  "function archBlit(key,frame,x,y,h,tint,rot,alpha){const q=hammerArchFrame(key,frame,tint);if(!q)return false;const w=h*q.sw/q.sh;ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,-w/2,-h/2,w,h);ctx.restore();return true;}\n"+
  "function archEffectBlit(cell,x,y,size,rot,alpha){\n"+
  "  if(!XART.rdy('arch_effects'))return false;const im=XART.get('arch_effects'),cols=4,rows=4,cw=im.width/cols,ch=im.height/rows,c=clamp(cell|0,0,cols*rows-1),sx=(c%cols)*cw,sy=((c/cols)|0)*ch;\n"+
  "  ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.globalCompositeOperation='lighter';ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,sx,sy,cw,ch,-size/2,-size/2,size,size);ctx.restore();return true;\n"+
  "}\n",
  'authored Archmage effects helper'
);

once(
  "  else{h.chainDestroyed=true;if(hammerHard()){h.mode='enraged';hammerState(b,'enrage');}else{h.mode='core';hammerState(b,'core_orbit');}}\n",
  "  else{h.chainDestroyed=true;if(hammerHard()){h.mode='enraged';hammerState(b,'enrage');}else{h.mode='core';h.coreAngle=0;hammerState(b,'core_orbit');const cue=Audio.SFX.bossWeaponCharge||Audio.SFX.crackle||Audio.SFX.bossPhase;if(cue)cue();}}\n",
  'normal chaingun break routing'
);

once(
  "  else if(h.state==='chain_cool'){h.chainHeat=Math.max(0,1-h.t/2.3);if(h.t>2.3){if(fur&&Math.random()<.5)hammerSpellStart(b);else hammerState(b,'chaingun');}}\n  else if(h.state==='enrage')",
  "  else if(h.state==='chain_cool'){h.chainHeat=Math.max(0,1-h.t/2.3);if(h.t>2.3){if(fur&&Math.random()<.5)hammerSpellStart(b);else hammerState(b,'chaingun');}}\n"+
  "  else if(h.state==='core_orbit'){\n"+
  "    const k=clamp(h.t/2.15,0,1);b.x+=clamp(homeX-b.x,-150*dt,150*dt);b.y+=clamp(homeY-b.y,-150*dt,150*dt);h.coreAngle=(h.coreAngle||0)+dt*(4+8*k);\n"+
  "    if(h.t>=2.15){h.shotCd=.18;hammerState(b,'uzi');const cue=Audio.SFX.bossPhase||Audio.SFX.enemyShoot;if(cue)cue();}\n"+
  "  }\n"+
  "  else if(h.state==='enrage')",
  'active core-orbit state'
);

once(
  "function hammerBossAtmosphereDraw(b){const h=b._hammer,s=h.state,charged=['mega_charge','mega_beam','spell','spell_blast','enrage'].includes(s);",
  "function hammerBossAtmosphereDraw(b){const h=b._hammer,s=h.state,charged=['core_orbit','mega_charge','mega_beam','spell','spell_blast','enrage'].includes(s);",
  'core atmosphere'
);

once(
  "  else if(['chaingun_draw','chaingun','chain_cool'].includes(h.state)){key='chaingun_detach_fire';f=h.state==='chaingun_draw'?Math.min(15,Math.floor(h.t/2*16)):8+(Math.floor(h.t*(4+12*(h.chainHeat||0)))%8);}\n  else if(h.state==='enrage')",
  "  else if(['chaingun_draw','chaingun','chain_cool'].includes(h.state)){key='chaingun_detach_fire';f=h.state==='chaingun_draw'?Math.min(15,Math.floor(h.t/2*16)):8+(Math.floor(h.t*(4+12*(h.chainHeat||0)))%8);}\n"+
  "  else if(h.state==='core_orbit'){const k=clamp(h.t/2.15,0,1);key='chaingun_break_enrage';f=Math.min(11,Math.floor(k*12));tint='blue';}\n"+
  "  else if(h.state==='enrage')",
  'core authored body reel'
);

once(
  "  archBlit(key,f,b.x,b.y,z,tint,rot);\n  if(h.state==='warn')",
  "  archBlit(key,f,b.x,b.y,z,tint,rot);\n"+
  "  if(h.state==='core_orbit'){\n"+
  "    const k=clamp(h.t/2.15,0,1),a=h.coreAngle||0,r=lerp(78,34,k),sz=lerp(34,54,k);\n"+
  "    for(let i=0;i<3;i++){const q=a+i*TAU/3;archEffectBlit((Math.floor(h.t*12)+i)%4,b.x+Math.cos(q)*r,b.y+Math.sin(q)*r*.48,sz,q,.72+.2*k);}\n"+
  "    archEffectBlit(2,b.x,b.y-9,lerp(32,68,k),a,.55+.35*k);\n"+
  "  }\n"+
  "  if(h.state==='warn')",
  'core authored effects draw'
);

fs.writeFileSync(file,s,'utf8');
console.log('PATCHED_ARCHMAGE_CORE_RECOVERY_0916');
