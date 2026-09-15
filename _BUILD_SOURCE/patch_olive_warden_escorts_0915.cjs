const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
let src=fs.readFileSync(file,'utf8');
if(src.includes('\r\n'))throw new Error('assets/game.js line endings drifted from LF');
fs.mkdirSync(path.join(root,'_shots','backups'),{recursive:true});
fs.copyFileSync(file,path.join(root,'_shots','backups','game_pre_olive_warden_escorts_0915.js'));
function once(oldText,newText,label){
  const n=src.split(oldText).length-1;
  if(n!==1)throw new Error(label+' expected once, found '+n);
  src=src.replace(oldText,newText);
}
const rocket=`function stage4MiniRocket(b,slot,a){
  const q=stage4WarfareShot(b,slot,a,1.7,'rocket',{accel:1.05,max:5.1,shootable:true,hp:2,szMul:.72});
  q._s4Mini=true;q._s4Slot=slot;
  stage4WarfareMuzzle(b,slot,'rocket',.85,.15);return q;
}`;
const helpers=`${rocket}
/* Hard/Furious Olive Warden escorts are difficulty units, not a restoration of the removed
   Normal helpers. Both roles use the authored south-facing Olive Carrier plate so they share
   the Warden's military palette without a runtime recolor. The gunner holds a flank with a
   separately animated rotary barrel; the protector flies bounded player-like pursuit lines and
   launches shootable missiles on the heading promised at release. */
function stage4MiniEscortEnsure(b){
  const S=b&&b._s4war;if(!S||!S.mini)return [];
  const hard=typeof diffKey!=='undefined'&&(diffKey==='hard'||diffKey==='furious');
  if(!hard){S.summoned=false;if(S.drones.length)S.drones.length=0;return S.drones;}
  const furious=diffKey==='furious',want=furious?3:2,W=worldWidth();
  if(S.drones.length!==want){
    S.drones.length=0;
    const roles=furious?['gunner','protector','protector']:['gunner','protector'];
    for(let i=0;i<roles.length;i++){
      const role=roles[i],side=i===0?-1:(i===1?1:0),hp=Math.ceil((role==='gunner'?145:120)*((DIFF&&DIFF.eHp)||1)),shield=Math.ceil(hp*(role==='gunner'?.48:.38));
      S.drones.push({role:role,side:side,index:i,art:'nsb_olive_carrier',size:role==='gunner'?88:80,
        x:side<0?W*.17:(side>0?W*.83:W*.5),y:214+i*12,stationX:side<0?W*.17:(side>0?W*.83:W*.5),stationY:214+i*12,
        hp:hp,maxhp:hp,shield:shield,maxShield:shield,dead:false,active:0,t:-i*.24,ang:Math.PI/2,
        fireCd:.28+i*.16,burstLeft:role==='gunner'?5:0,movePhase:i*Math.PI,flash:0,shieldFlash:0,shots:0});
    }
    if(typeof XART!=='undefined'&&XART._touch){XART._touch('nsb_olive_carrier');for(let i=0;i<8;i++)XART._touch('s4w_drone_barrel_'+i);}
    stage4WarfareSound('bossWeaponCharge','enemyBossCannon');
  }
  S.summoned=S.drones.some(d=>!d.dead);return S.drones;
}
function stage4MiniEscortTick(b,dt,phase){
  const S=b&&b._s4war,list=stage4MiniEscortEnsure(b);if(!S||!list.length)return false;
  const W=worldWidth(),furious=diffKey==='furious',target=(typeof targetShip==='function')?targetShip(b.x,b.y):player;
  for(const d of list){
    if(d.dead)continue;d.t+=dt;d.flash=Math.max(0,(d.flash||0)-dt);d.shieldFlash=Math.max(0,(d.shieldFlash||0)-dt);
    if(d.t<0)continue;d.active=Math.min(1,d.active+dt*3.4);
    let tx=d.stationX,ty=d.stationY;
    if(d.role==='gunner'){
      ty=d.stationY+Math.sin(d.t*2.1+d.index)*5;
    }else{
      const leg=(d.t+1.05*d.index)%3.2,guardSide=d.side||((Math.floor(d.t/3.2)&1)?1:-1);
      tx=clamp(target.x+guardSide*(leg<1.6?112:72),72,W-72);
      ty=leg<.72?244:(leg<1.6?204:224+Math.sin((leg-1.6)/1.6*Math.PI)*18);
    }
    const speed=(d.role==='gunner'?85:(furious?285:230))*dt;
    d.x+=clamp(tx-d.x,-speed,speed);d.y+=clamp(ty-d.y,-speed,speed);
    const a=Math.atan2(target.y-d.y,target.x-d.x);d.ang+=stage4AngleDelta(d.ang,a)*Math.min(1,dt*(d.role==='gunner'?7:9));
    if(d.active<.82)continue;d.fireCd-=dt;
    if(d.role==='gunner'&&d.fireCd<=0){
      const tip={x:d.x+Math.cos(d.ang)*38,y:d.y+Math.sin(d.ang)*38};
      const q=stage4MiniMachine(b,tip,d.ang,5.45+phase*.18);q._s4EscortRole='gunner';d.shots++;d.burstLeft--;
      d.fireCd=d.burstLeft>0?.105:(furious?.52:.72);if(d.burstLeft<=0)d.burstLeft=furious?7:5;
      stage4WarfareDroneMuzzle(b,d);if((d.shots%5)===1)stageRevisionCue(b,'wardenGun',.10,.82);
    }else if(d.role==='protector'&&d.fireCd<=0){
      const tip={x:d.x+Math.cos(d.ang)*34,y:d.y+Math.sin(d.ang)*34},q=stage4WarfareShot(b,tip,d.ang,1.85,'rocket',{accel:.92,max:5.25,shootable:true,hp:2,szMul:.74});
      q._s4Mini=true;q._s4EscortRole='protector';q._s4EscortIndex=d.index;d.shots++;d.fireCd=(furious?.92:1.24)+d.index*.08;
      stage4WarfareDroneMuzzle(b,d);stageRevisionCue(b,'wardenRocket',.18,.84);
    }
  }
  S.summoned=list.some(d=>!d.dead);return true;
}`;
once(rocket,helpers,'insert escort controller');
once("  S.t+=dt*(1+phase*.10);b.fireCd=999;S.poseRot=0;S.scale=1;b._animKey=null;S.summoned=false;S.drones.length=0;",
     "  S.t+=dt*(1+phase*.10);b.fireCd=999;S.poseRot=0;S.scale=1;b._animKey=null;stage4MiniEscortTick(b,dt,phase);",
     'connect escort controller');
once("  if(!S.mini||!S.summoned||!XART.rdy('s4w_drone_body'))return;\n  const body=XART.get('s4w_drone_body');\n  for(const d of S.drones){\n    if(d.dead||d.active<=0)continue;const sz=92*d.active;\n    ctx.save();ctx.globalAlpha=d.active;ctx.drawImage(body,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();\n    if(XART.rdy(bk)){",
     "  if(!S.mini||!S.summoned)return;\n  for(const d of S.drones){\n    const bodyKey=d.art||'s4w_drone_body';if(d.dead||d.active<=0||!XART.rdy(bodyKey))continue;\n    const body=XART.get(bodyKey),sz=(d.size||92)*d.active;\n    ctx.save();ctx.globalAlpha=d.active;ctx.drawImage(body,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();\n    if(d.role==='gunner'&&XART.rdy(bk)){",
     'draw authored escort hulls');
once("      const tint=xartTint('s4w_drone_body','#4adfff',1);if(tint){ctx.save();ctx.globalAlpha=clamp(d.shieldFlash/.14,0,1)*.78;ctx.drawImage(tint,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();}",
     "      const tint=xartTint(bodyKey,'#4adfff',1);if(tint){ctx.save();ctx.globalAlpha=clamp(d.shieldFlash/.14,0,1)*.78;ctx.drawImage(tint,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();}",
     'shield contact follows authored hull');
once("      const tint=xartTint('s4w_drone_body','#ffffff',1);if(tint){ctx.save();ctx.globalAlpha=clamp(d.flash/.15,0,1);ctx.drawImage(tint,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();}",
     "      const tint=xartTint(bodyKey,'#ffffff',1);if(tint){ctx.save();ctx.globalAlpha=clamp(d.flash/.15,0,1);ctx.drawImage(tint,d.x-sz/2,d.y-sz/2,sz,sz);ctx.restore();}",
     'hull hit flash follows authored hull');
fs.writeFileSync(file,src,'utf8');
if(fs.readFileSync(file,'utf8').includes('\r\n'))throw new Error('write introduced CRLF');
console.log('patched Olive Warden Hard/Furious escorts');
