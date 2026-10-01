"use strict";
/* September 27: Mike's corrected roster. Geometry owns art, weapons and Retina. */
const MR27_CACHE=new Map();
for(const [k,v] of Object.entries(MR27_ART))XART._src['mr27_'+k]=v.path;
function mr27Owns(b){return !!b&&['cryospear','olivewarden','stormsovereign'].includes(b._ship);}
function mr27Cell(skin,cell,form){
  const id=skin+':'+cell+':'+(form||'neutral');if(MR27_CACHE.has(id))return MR27_CACHE.get(id);
  const d=MR27_ART[skin];if(!d||!XART.rdy('mr27_'+skin))return null;
  const r=d.cells[cell],c=document.createElement('canvas');c.width=r[2];c.height=r[3];const g=c.getContext('2d');
  g.drawImage(XART.get('mr27_'+skin),...r,0,0,c.width,c.height);
  // Mike's Furious thermodynamic forms preserve luminance and metallic outlines.
  if(form==='fire'||form==='ice'){g.globalCompositeOperation='color';g.fillStyle=form==='fire'?'#df4825':'#40aaff';g.fillRect(0,0,c.width,c.height);g.globalCompositeOperation='destination-in';g.drawImage(XART.get('mr27_'+skin),...r,0,0,c.width,c.height);}
  if(form==='fury'&&typeof d27TempestPalette==='function')d27TempestPalette(c);
  if(form==='white'||/^#[0-9a-f]{6}$/i.test(form||'')){g.globalCompositeOperation='source-in';g.fillStyle=form==='white'?'#fff':form;g.fillRect(0,0,c.width,c.height);}
  MR27_CACHE.set(id,c);return c;
}
function mr27Blit(skin,cell,p,flash,form,owner){
  const im=mr27Cell(skin,cell,form);if(!im)return false;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(p.x,p.y);ctx.rotate(p.rot||0);
  ctx.drawImage(im,-p.w/2,-p.h/2,p.w,p.h);
  if(flash>0){const white=mr27Cell(skin,cell,hitFlashColor(owner||p));ctx.globalAlpha=Math.min(.82,flash*5);ctx.drawImage(white,-p.w/2,-p.h/2,p.w,p.h);}
  ctx.restore();return true;
}
function mr27Init(b){
  if(!mr27Owns(b)||b._mr27)return;
  const skin=b._ship==='cryospear'?'rime':b._ship==='olivewarden'?'iron':'storm';
  b._mr27={skin,clock:0,stun:0,parts:[],breaks:[],draws:0};XART.rdy('mr27_'+skin);XART.rdy('mr27_corefx');
  if(skin==='rime'){b.w=286;b.h=266;b.name='RIME WALL â€” MODULAR BASTION';}
  if(skin==='iron')b.name='IRON WARDEN';
  for(const [id,f]of [['gunL',.09],['gunR',.09],['rocketL',.055],['rocketR',.055]]){
    const hp=Math.ceil(b.maxhp*f);b._mr27.parts.push({id,hp,maxhp:hp,flash:0,rot:0,recoil:0,dead:false});
  }
  if(b._er26){b._er26.home=Math.max(b._er26.home,b.h*.5+40);b.ty=b._er26.home;}
}
function mr27Part(b,id){return b._mr27?.parts.find(p=>p.id===id);}
function mr27Shape(b,id){
  const M=b._mr27,iron=M.skin==='iron',rime=M.skin==='rime',s=id.endsWith('L')?-1:1,p=mr27Part(b,id);
  const core=id==='core',rocket=id.startsWith('rocket'),cell=core?3:rocket?(iron?2:4):iron?1:s<0?1:2;
  const dx=core?0:rocket?s*(rime?.37:iron?.35:.38):s*(rime?.205:iron?.29:.245);
  const dy=core?(rime?-.04:iron?.06:-.015):rocket?-.20:iron?.11:.16;
  const maxW=b.w*(core?(rime?.24:iron?.19:.16):rocket?.14:iron?.29:.22),maxH=b.h*(core?(rime?.25:iron?.31:.55):rocket?.34:iron?.47:.64);
  const r=MR27_ART[M.skin].cells[cell],scale=Math.min(maxW/r[2],maxH/r[3]);
  return {id,cell,x:b.x+dx*b.w,y:(b._drawY??b.y)+dy*b.h-(p?.recoil||0)*3,w:r[2]*scale,h:r[3]*scale,rot:p?.rot||0};
}
function mr27Mount(b,slot){
  const id=/ROCKET/.test(slot)?(slot.endsWith('L')?'rocketL':'rocketR'):['L','L0','L1','LW','CL','gunL'].includes(slot)?'gunL':['R','R0','R1','RW','CR','gunR'].includes(slot)?'gunR':'core';
  const p=mr27Shape(b,id),a=p.rot+Math.PI/2,offset=/^[LR][01]$/.test(slot)?(slot.endsWith('0')?-1:1)*p.w*.13:0;return {x:p.x+Math.cos(a)*p.h*.48+Math.cos(p.rot)*offset,y:p.y+Math.sin(a)*p.h*.48+Math.sin(p.rot)*offset};
}
function mr27CanFire(b,slot){if(!b?._mr27||typeof slot!=='string')return true;const id=/ROCKET/.test(slot)?(slot.endsWith('L')?'rocketL':'rocketR'):['L','L0','L1','LW','CL','gunL'].includes(slot)?'gunL':['R','R0','R1','RW','CR','gunR'].includes(slot)?'gunR':null;return !id||!mr27Part(b,id)?.dead;}
function mr27Fire(b,slot,a){
  if(!b?._mr27||typeof slot!=='string')return;
  const id=/ROCKET/.test(slot)?(slot.endsWith('L')?'rocketL':'rocketR'):['L','L0','L1','LW','CL'].includes(slot)?'gunL':['R','R0','R1','RW','CR'].includes(slot)?'gunR':null;
  const p=mr27Part(b,id);if(p&&!p.dead){p.rot=a-Math.PI/2;p.recoil=1;}
}
function mr27At(b,x,y){
  if(!b||b.dead||b.enter||b._noHit)return null;
  for(const q of [...b._mr27.parts].reverse())if(!q.dead){const p=mr27Shape(b,q.id),dx=x-p.x,dy=y-p.y,c=Math.cos(p.rot),s=Math.sin(p.rot);
    if(Math.abs(dx*c+dy*s)<p.w*.52&&Math.abs(-dx*s+dy*c)<p.h*.5)return q.id;}
  return Math.abs(x-b.x)<b.w*.37&&Math.abs(y-(b._drawY??b.y))<b.h*.44?'core':null;
}
function mr27Damage(b,dmg,x,y){
  const id=mr27At(b,x??b.x,y??b.y),p=mr27Part(b,id);if(!p)return dmg;
  const actual=Math.min(p.hp,dmg);p.hp-=actual;p.flash=.2;
  if(p.hp<=0){p.dead=true;const q=mr27Shape(b,id);b._mr27.breaks.push(id);if(typeof d27ModuleRupture==='function')d27ModuleRupture(b,p,q,'blue');b._mr27.stun=diffKey==='easy'?1.8:diffKey==='normal'?1.4:1.05;
    unitDeathFX({x:q.x,y:q.y,w:q.w,h:q.h},'turret','blue');explode(q.x,q.y,48,'blue');
    b._l23Beam=null;b._smz=null;polishLanes=polishLanes.filter(w=>w.owner!==b);groundTargetingCancel(b);
    er26Set(b,'recover');b._er26.dur=Math.max(b._er26.dur,b._mr27.stun);b._er26.from={x:b.x,y:b.y};
    er26Sound('combatStun0927','shieldBreak');shake=Math.max(shake,5);
  }
  return actual;
}
function mr27Tick(b,dt){
  mr27Init(b);const M=b._mr27;if(!M)return;M.clock+=dt;M.stun=Math.max(0,M.stun-dt);
  for(const p of M.parts){p.flash=Math.max(0,p.flash-dt);p.recoil=Math.max(0,p.recoil-dt*10);
    const q=mr27Shape(b,p.id),target=b._er26.target||player,a=Math.atan2(target.y-q.y,target.x-q.x)-Math.PI/2;
    const beam=b._ship==='cryospear'&&b._l23Beam,slot=p.id==='gunL'?'L0':'R0',idx=beam?beam.slots.indexOf(slot):-1;const wanted=idx>=0?beam.angles[idx]-Math.PI/2:p.id.startsWith('gun')?clamp(a,-.42,.42):0;p.rot+=(wanted-p.rot)*Math.min(1,dt*4);}
}
function mr27Targets(b,a){
  if(b.enter||b.dead||b._noHit)return;
  const S=b._s4war;
  for(const d of S?(S.mini?S.drones:S.coreTurrets):[]){
    if(d.dead||(S.mini?d.active<.82:d.materialize<.92))continue;
    const g=mr27HelperState(d);if(g.dead)continue;
    const pos=()=>({...mr27HelperGun(b,d),hp:g.hp,dead:g.dead||d.dead||b.dead});
    a.push(retinaDynamicPiece(b,'helper-gun-'+d.side,'helper weapon',pos,damage=>{
      const p=pos();_lastHitX=p.x;_lastHitY=p.y;
      if(S.mini)stage4MiniDroneDamage(b,d,damage);else stage4CoreTurretDamage(b,d,damage);
    },pos().w,pos().h));
  }
  const shield=b._s4war?.shield;if(shield&&(shield.active||shield.rearming))return;
  for(const p of b._mr27.parts)if(!p.dead){const pos=()=>{const q=mr27Shape(b,p.id);return {...q,hp:p.hp,dead:p.dead||b.dead||b.enter};},q=pos();
    a.push(retinaImpactTarget(b,'mr27-'+p.id,p.id,pos,q.w,q.h));}
}
function mr27CoreDraw(b,p){
  const R=b._er26,charge=R.mode!=='recover'&&R.t<(R.warm||0),skin=b._mr27.skin;
  if(skin==='storm'&&MR27_ART.corefx&&XART.rdy('mr27_corefx')){
    const cell=charge?Math.min(4,Math.floor(R.t/Math.max(.1,R.warm)*5)):5+Math.floor(b._mr27.clock*9)%3;
    mr27Blit('corefx',cell,p,b.flash,null,b);return;
  }
  mr27Blit(skin,3,p,b.flash,skin==='rime'&&b._s3Nuclear?R.form:null,b);
}
function mr27HelperState(d){if(!d._mrGun){const hp=Math.ceil(d.maxhp*.4);d._mrGun={hp,maxhp:hp,dead:false,flash:0};}return d._mrGun;}
function mr27HelperGun(b,d){
  const mini=b._s4war.mini,size=mini?(d.size||112):96,a=d.ang??Math.PI/2;
  return {x:d.x+Math.cos(a)*size*.17,y:d.y+Math.sin(a)*size*.17,w:size*.32,h:size*.62,rot:a-Math.PI/2};
}
function mr27HelperDamage(b,d,dmg){
  if(!b._mr27||d.shield>0)return dmg;const g=mr27HelperState(d),p=mr27HelperGun(b,d),dx=(_lastHitX??d.x)-p.x,dy=(_lastHitY??d.y)-p.y;
  if(!g.dead&&Math.hypot(dx,dy)<p.h*.55){g.hp-=dmg;g.flash=.18;if(g.hp<=0){g.hp=0;g.dead=true;if(typeof d27ModuleRupture==='function')d27ModuleRupture(d,g,p,'blue');unitDeathFX({x:p.x,y:p.y,w:p.w,h:p.h},'turret','blue');er26Sound('shieldBreak','expSmall');}}
  return dmg;
}
function mr27HelperDraw(b,d){
  const mini=b._s4war.mini,skin=mini?'iron':'storm',size=mini?(d.size||112):96,g=mr27HelperState(d),p=mr27HelperGun(b,d);
  mr27Blit(skin,mini?4:5,{x:d.x,y:d.y,w:size,h:mini?size*.63:size},d.flash);
  if(!g.dead)mr27Blit(skin,mini?5:1,p,d.flash);
  const core={x:d.x,y:d.y-size*.13,w:size*.16,h:size*.33};if(mini)mr27Blit(skin,3,core,d.flash);else mr27CoreDraw(b,core);
  if(d.shield>0){const k='s4w_lightning_shield_'+Math.floor(b._mr27.clock*12)%12;if(XART.rdy(k)){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.28;ctx.drawImage(XART.get(k),d.x-size*.57,d.y-size*.57,size*1.14,size*1.14);ctx.restore();}}
}
function mr27Over(b){
  const S=b._s4war;if(!S)return;const H=S.shield;
  if(H){
    const key='s4w_lightning_shield_'+Math.floor(b._mr27.clock*12)%12;
    if((H.active||H.breakT>0)&&XART.rdy(key)){const size=b.w*1.25;ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=H.active?.34:Math.min(.34,H.breakT*.3);ctx.drawImage(XART.get(key),b.x-size/2,b.y-size/2,size,size);ctx.restore();}
    for(const n of H.nodes)if(!n.dead){mr27Blit('storm',5,{x:n.x,y:n.y,w:54,h:54},n.flash);mr27CoreDraw(b,{x:n.x,y:n.y,w:15,h:34});}
  }
  const list=S.mini?S.drones:S.coreTurrets;for(const d of list||[])if(!d.dead&&(S.mini?d.active>.1:d.materialize>.1))mr27HelperDraw(b,d);
}
function mr27Draw(b){
  mr27Init(b);const M=b._mr27;if(!XART.rdy('mr27_'+M.skin))return false;
  if(b._l23Beam)l23BossBeamDraw(b);
  const shape=MR27_ART[M.skin].cells[0],scale=Math.min(b.w/shape[2],b.h/shape[3]),form=M.skin==='rime'&&b._s3Nuclear?b._er26.form:null;
  mr27Blit(M.skin,0,{x:b.x,y:b._drawY??b.y,w:shape[2]*scale,h:shape[3]*scale},b.flash,form,b);
  for(const q of M.parts)if(!q.dead){const p=mr27Shape(b,q.id);mr27Blit(M.skin,p.cell,p,Math.max(q.flash,b.flash||0),form,b);}
  mr27CoreDraw(b,mr27Shape(b,'core'));
  if(M.skin==='rime'&&b._l23Beam&&!b._l23Beam.released){const B=b._l23Beam,k=clamp(B.t/B.warm,0,1),key='l23fx_rime_orb_'+(Math.floor(M.clock*16)%8);
    if(XART.rdy(key))for(const slot of B.slots){const p=shipBossMount(b,slot),s=12+k*17;ctx.save();ctx.globalAlpha=.5+k*.5;ctx.drawImage(XART.get(key),p.x-s/2,p.y-s/2,s,s);ctx.restore();}}
  mr27Over(b);er26Draw(b);shipBossMuzzleDraw(b);M.draws++;return true;
}

/* One Earth bomber; two modular Tempest skins for the space pursuit. */
function mr27BomberSetup(b){
  if(!b._bomber)return;const B=b._bomber;B.space=run.stage===5;B.skin=B.space?'space':null;
  B.variant=B.space&&['hard','furious','insanity'].includes(diffKey)?1:0;b.name=B.space?(B.variant?'TEMPEST SILVER ECLIPSE':'TEMPEST VOID ECLIPSE'):'ECLIPSE SIEGE BOMBER';
  if(B.space&&(diffKey==='furious'||diffKey==='insanity'))b.name='TEMPEST CRIMSON ECLIPSE';
  const mul=diffKey==='easy'?.52:diffKey==='normal'?1:diffKey==='hard'?1.18:diffKey==='furious'?1.35:1.5;
  const durability=B.space?1:1.10;B.core=B.coreMax=Math.ceil(1050*mul*durability);for(const p of B.parts)p.hp=p.max=p.maxhp=Math.ceil(250*mul*durability);
  b.hp=b.maxhp=B.core+B.parts.reduce((a,p)=>a+p.hp,0);b.w=VW*.5;b.h=B.space?b.w*.83:b.w*.62;
  if(B.space){XART.rdy('mr27_space');XART.rdy('tlv_beam');for(let i=0;i<8;i++)XART.rdy('l23fx_rime_mg_'+i);}
}
function mr27SpaceParts(b){
  const B=b._bomber,W=b.w,H=b.h,defs=[['core',B.variant,0,0,W,H],['engineL',3,-W*.135,H*.35,W*.18,H*.24],['engineR',3,W*.135,H*.35,W*.18,H*.24],['laserL',2,-W*.215,-H*.02,W*.115,H*.72],['laserR',2,W*.215,-H*.02,W*.115,H*.72]];
  return defs.map(([id,cell,dx,dy,w,h])=>({id,cell,x:b.x+dx,y:b.y+dy,w,h,pool:id==='core'?null:B.parts.find(p=>p.id===id)}));
}
function mr27SpaceDraw(b){
  const B=b._bomber;if(!XART.rdy('mr27_space'))return false;const form=typeof d27FuriousBomber==='function'&&d27FuriousBomber(b)?'fury':null;
  for(const p of mr27SpaceParts(b))if(!p.pool||p.pool.hp>0){mr27Blit('space',p.cell,p,p.pool?p.pool.flash:b.flash,form);
    if(p.id.startsWith('engine')&&typeof d27MuzzleDraw==='function')d27MuzzleDraw(ctx,'exhaust',p.x,p.y+p.h*.37,Math.PI/2,(B.clock*12)%1,30,form?'#ff3922':null);}
  mr27Blit('space',4,{x:b.x,y:b.y+b.h*.03,w:b.w*.1,h:b.h*.31},b.flash,form,b);
  if(B.mode==='bombs')mr27Blit('space',5,{x:b.x,y:b.y+b.h*.27,w:b.w*.17,h:b.h*.22},0,form);
  for(const q of B.bombs)if(q.t>0&&q.t<q.warn&&XART.rdy('lz_bomb')){const u=clamp(q.t/q.warn,0,1);ctx.save();ctx.translate(lerp(q._polishBomb.x,q.x,u),lerp(q._polishBomb.y,q.y,u));ctx.rotate(Math.PI);ctx.drawImage(XART.get('lz_bomb'),-8,-20,16,40);ctx.restore();}
  return true;
}
function mr27TrueRoute(){return diffKey==='furious'||diffKey==='insanity';}
