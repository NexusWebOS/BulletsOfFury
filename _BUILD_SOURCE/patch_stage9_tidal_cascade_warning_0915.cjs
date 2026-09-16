const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
`function tidalCascadeStart(b,step){
  if(!b||b._s9Cascade)return false;const cols=8,left=(typeof camLeftX==='function'?camLeftX():0),right=(typeof camRightX==='function'?camRightX():worldWidth()),cw=(right-left)/cols;
  const gap=clamp(Math.floor(((player?player.x:(left+right)/2)-left)/cw)-1,0,cols-2);
  b._s9Cascade={t:0,tell:.70,wave:0,waves:4,next:.70,gap:gap,dir:(step&1)?1:-1,cols:cols,left:left,right:right};
  b.fireCd=Math.max(b.fireCd||0,2.65);b.flash=Math.max(b.flash||0,.38);
  if(typeof floatText==='function')floatText(b.x,(b._drawY!=null?b._drawY:b.y)+b.h*.39,'TIDAL CASCADE!','#79eaff');
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyHeavyLaser))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyHeavyLaser)();
  return true;
}
function tidalCascadeTick(b,dt){
  const T=b&&b._s9Cascade;if(!T)return false;T.t+=dt;
  if(T.t>=T.next&&T.wave<T.waves){
    const cw=(T.right-T.left)/T.cols,y=(b._drawY!=null?b._drawY:b.y)+b.h*.34;
    for(let i=0;i<T.cols;i++){
      if(i===T.gap||i===T.gap+1)continue;const x=T.left+(i+.5)*cw;
      spaceBossShot(x,y-(i&1)*18,Math.PI/2,1.42+T.wave*.15,'s9pair',{silent:i>0,w:34,h:34,szMul:1.22,accel:.24,max:2.48+T.wave*.18,noArsenal:true,forceStageArt:true});
    }
    shipBossMuzzleStart(b,['L','C','R'],{fam:'bfx_cyclone_m',n:6,life:.18,hpx:66});
    shake=Math.max(shake,5+T.wave);T.wave++;
    let ng=T.gap+T.dir;if(ng<0||ng>T.cols-2){T.dir*=-1;ng=T.gap+T.dir;}T.gap=clamp(ng,0,T.cols-2);T.next+=.42;
  }
  if(T.wave>=T.waves&&T.t>T.next+.62){b._s9Cascade=null;b.fireCd=.68;return false;}return true;
}
function tidalCascadeDraw(b){
  const T=b&&b._s9Cascade;if(!T||T.t>=T.tell)return;const cw=(T.right-T.left)/T.cols,pulse=.25+.18*Math.sin(T.t*21);
  ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<T.cols;i++){
    if(i===T.gap||i===T.gap+1)continue;ctx.globalAlpha=pulse;ctx.fillStyle='#39caff';ctx.fillRect(T.left+i*cw+5,PLAY.y,cw-10,VH-PLAY.y);
    ctx.globalAlpha=.76;ctx.fillStyle='#d4ffff';ctx.fillRect(T.left+i*cw+cw*.48,PLAY.y,cw*.04,VH-PLAY.y);
  }
  ctx.globalAlpha=.92;ctx.strokeStyle='#a6ffff';ctx.lineWidth=2;ctx.strokeRect(T.left+T.gap*cw+3,PLAY.y+3,cw*2-6,VH-PLAY.y-6);ctx.restore();
}`,
`function tidalCascadeStart(b,step){
  if(!b||b._s9Cascade)return false;const cols=8,left=(typeof camLeftX==='function'?camLeftX():0),right=(typeof camRightX==='function'?camRightX():worldWidth()),cw=(right-left)/cols;
  const gap=clamp(Math.floor(((player?player.x:(left+right)/2)-left)/cw)-1,0,cols-2),rowTell=.62;
  b._s9Cascade={t:0,tell:rowTell,rowTell:rowTell,warnAt:0,wave:0,waves:4,next:rowTell,gap:gap,dir:(step&1)?1:-1,cols:cols,left:left,right:right};
  b.fireCd=Math.max(b.fireCd||0,3.25);b.flash=Math.max(b.flash||0,.38);
  combatWarningTick(b,'stage9-tidal-cascade-0',0,rowTell,true);
  if(typeof floatText==='function')floatText(b.x,(b._drawY!=null?b._drawY:b.y)+b.h*.39,'TIDAL CASCADE!','#79eaff');
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyHeavyLaser))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyHeavyLaser)();
  return true;
}
function tidalCascadeTick(b,dt){
  const T=b&&b._s9Cascade;if(!T)return false;T.t+=dt;
  if(T.wave<T.waves){
    const elapsed=Math.min(T.rowTell,Math.max(0,T.t-T.warnAt));
    combatWarningTick(b,'stage9-tidal-cascade-'+T.wave,elapsed,T.rowTell);
  }
  if(T.t>=T.next&&T.wave<T.waves){
    const cw=(T.right-T.left)/T.cols,y=(b._drawY!=null?b._drawY:b.y)+b.h*.34;
    for(let i=0;i<T.cols;i++){
      if(i===T.gap||i===T.gap+1)continue;const x=T.left+(i+.5)*cw;
      spaceBossShot(x,y-(i&1)*18,Math.PI/2,1.42+T.wave*.15,'s9pair',{silent:i>0,w:34,h:34,szMul:1.22,accel:.24,max:2.48+T.wave*.18,noArsenal:true,forceStageArt:true});
    }
    shipBossMuzzleStart(b,['L','C','R'],{fam:'bfx_cyclone_m',n:6,life:.18,hpx:66});
    shake=Math.max(shake,5+T.wave);T.wave++;
    if(T.wave<T.waves){
      let ng=T.gap+T.dir;if(ng<0||ng>T.cols-2){T.dir*=-1;ng=T.gap+T.dir;}T.gap=clamp(ng,0,T.cols-2);
      T.warnAt=T.t;T.next=T.t+T.rowTell;combatWarningTick(b,'stage9-tidal-cascade-'+T.wave,0,T.rowTell,true);
    }
  }
  if(T.wave>=T.waves&&T.t>T.next+.70){b._s9Cascade=null;b.fireCd=.68;return false;}return true;
}
function tidalCascadeDraw(b){
  const T=b&&b._s9Cascade;if(!T||T.wave>=T.waves)return;const cw=(T.right-T.left)/T.cols,
    k=clamp((T.t-T.warnAt)/T.rowTell,0,1),y=(b._drawY!=null?b._drawY:b.y)+b.h*.34;
  for(let i=0;i<T.cols;i++){
    if(i===T.gap||i===T.gap+1)continue;const x=T.left+(i+.5)*cw;
    combatWarningDraw(b,{x:x,y:y-(i&1)*18,ex:x,ey:VH+40,progress:k,width:Math.max(24,cw*.52),fieldOnly:true});
  }
  const p=shipBossMount(b,'C');combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH+40,progress:k,alertOnly:true});
}`,
'give every Tidal Cascade row an exact shared warning');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE9_TIDAL_CASCADE_WARNING_0915');
