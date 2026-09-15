const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..'),gamePath=path.join(root,'assets','game.js'),suitePath=path.join(root,'_BUILD_SOURCE','test_fl.js');
const recovery=path.join(root,'_shots','overlord_flyover_intro_0915','recovery');fs.mkdirSync(recovery,{recursive:true});
const before=fs.readFileSync(gamePath,'utf8'),suite=fs.readFileSync(suitePath,'utf8');if(before.includes('\r\n'))throw new Error('game must remain LF');if(/(^|[^\r])\n/.test(suite))throw new Error('suite must remain CRLF');
fs.writeFileSync(path.join(recovery,'game.js.before'),before);fs.writeFileSync(path.join(recovery,'test_fl.js.before'),suite);
let s=before;function once(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, got '+n);s=s.replace(a,b);}

once("      b.name='JUNGLE OVERLORD-X'; b.w=170; b.h=130; b._noHit=true;\n      b._ovIntro={phase:'approach',t:0,fromY:b.y,gauge:0,alpha:0,beat:-1,done:false};\n",
"      b.name='JUNGLE OVERLORD-X'; b.w=170; b.h=130; b._noHit=true;\n"+
"      b.y=VH+b.h*.82;b.x=clamp(player.x,86,VW-86);\n"+
"      b._ovIntro={phase:'approach',t:0,fromX:b.x,fromY:b.y,gauge:0,alpha:0,beat:-1,done:false};b._ovAirborne=true;\n",'bottom approach initialization');

const oldTick=`function overlordIntroTick(b,dt){
  const I=b&&b._ovIntro;if(!I||I.done)return false;I.t+=dt;
  if(I.phase==='approach'){
    const p=clamp(I.t/1.35,0,1),e=1-Math.pow(1-p,3);b.y=lerp(I.fromY,b.ty,e);
    if(p>=1){b.y=b.ty;I.phase='fade';I.t=0;I.alpha=0;I.gauge=0;}
    return true;
  }
  if(I.phase==='fade'){
    I.alpha=clamp(I.t/.46,0,1);I.gauge=0;
    if(I.t>=.46){I.phase='fill';I.t=0;I.alpha=1;I.beat=-1;}
    return true;
  }
  if(I.phase==='fill'){
    const p=clamp(I.t/1.68,0,1);I.alpha=1;I.gauge=p;const beat=Math.min(7,Math.floor(p*8));
    if(beat>I.beat){I.beat=beat;if(Audio.SFX&&Audio.SFX.blip)Audio.SFX.blip();}
    if(p>=1){I.phase='ready';I.t=0;I.gauge=1;if(Audio.SFX&&Audio.SFX.select)Audio.SFX.select();}
    return true;
  }
  I.alpha=1;I.gauge=1;
  if(I.t>=.28){I.done=true;b.enter=false;b._noHit=false;b.fireCd=.72;if(Audio.startMusic)Audio.startMusic('boss1');return false;}
  return true;
}`;
const newTick=`function overlordIntroTick(b,dt){
  const I=b&&b._ovIntro;if(!I||I.done)return false;I.t+=dt;
  if(!b._stageAudioWarm){stageRevisionWarm('damkeeper');b._stageAudioWarm=true;}
  weaponFeedbackLoop('overlordRotor',.32);
  if(I.phase==='approach'){
    const p=clamp(I.t/1.18,0,1),e=p*p*(3-2*p);b.y=lerp(I.fromY,b.ty,e);b.x=lerp(I.fromX,VW/2,e);
    b._pivot=Math.sin(p*Math.PI)*.10*(I.fromX<VW/2?1:-1);
    if(p>=1){b.x=VW/2;b.y=b.ty;b._pivot=0;b._ovAirborne=false;I.phase='whip';I.t=0;stageRevisionCue(b,'overlordWind',0);}
    return true;
  }
  if(I.phase==='whip'){
    const p=clamp(I.t/.48,0,1),e=1-Math.pow(1-p,3);b._pivot=e*TAU;
    if(p>=1){b._pivot=0;I.phase='fade';I.t=0;I.alpha=0;I.gauge=0;}
    return true;
  }
  if(I.phase==='fade'){
    I.alpha=clamp(I.t/.46,0,1);I.gauge=0;
    if(I.t>=.46){I.phase='fill';I.t=0;I.alpha=1;I.beat=-1;}
    return true;
  }
  if(I.phase==='fill'){
    const p=clamp(I.t/1.68,0,1);I.alpha=1;I.gauge=p;const beat=Math.min(7,Math.floor(p*8));
    if(beat>I.beat){I.beat=beat;if(Audio.SFX&&Audio.SFX.blip)Audio.SFX.blip();}
    if(p>=1){I.phase='ready';I.t=0;I.gauge=1;if(Audio.SFX&&Audio.SFX.select)Audio.SFX.select();}
    return true;
  }
  I.alpha=1;I.gauge=1;
  if(I.t>=.28){I.done=true;b.enter=false;b._noHit=false;b.fireCd=.72;if(Audio.startMusic)Audio.startMusic('boss1');return false;}
  return true;
}`;
once(oldTick,newTick,'flyover/whip intro tick');

once("function drawBoss(){\n  /* The death-visibility rule lives here at the one entry point. bossDeathAlpha is deliberately\n     binary: full-opacity hull, then authored explosion takeover; never a dissolve. */\n  const _b = boss;\n",
`function overlordIntroOverflightDraw(){
  const b=(typeof boss!=='undefined')?boss:null,I=b&&b._ovIntro;if(!b||b.dead||b.kind!=='damkeeper'||!b._ovAirborne||!I)return false;
  if(typeof XART==='undefined'||!XART.rdy('ovbody_intact'))return false;
  const body=XART.get('ovbody_intact'),w=b.w*1.15,h=w*(body.naturalHeight/body.naturalWidth),ri=(Math.round((((b.t||0)*900)%360)/5)%72+72)%72;
  const rk='ovrotor_'+String(ri).padStart(2,'0'),shadowBody=xartTint('ovbody_intact','#020407',.98),shadowRotor=XART.rdy(rk)?xartTint(rk,'#020407',.98):null;
  const p=clamp(I.t/1.18,0,1),sx=b.x+lerp(20,8,p),sy=b.y+lerp(34,18,p),sc=lerp(1.12,1.02,p);
  ctx.save();ctx.translate(sx,sy);ctx.rotate(b._pivot||0);ctx.scale(sc,sc);ctx.translate(-sx,-sy);ctx.globalAlpha=.48;
  if(shadowBody)ctx.drawImage(shadowBody,sx-w/2,sy-h/2,w,h);if(shadowRotor)ctx.drawImage(shadowRotor,sx-w/2,sy-h/2,w,h);ctx.restore();
  drawBossSprite(b);return true;
}
function drawBoss(){
  /* The death-visibility rule lives here at the one entry point. bossDeathAlpha is deliberately
     binary: full-opacity hull, then authored explosion takeover; never a dissolve. */
  const _b = boss;
  if(_b&&_b.kind==='damkeeper'&&_b._ovAirborne)return;
`,'overflight renderer and ordinary draw suppression');

once("  });\n  stage4OverflightDraw();\n",
"  });\n  overlordIntroOverflightDraw();\n  stage4OverflightDraw();\n",'overflight above player draw');

fs.writeFileSync(gamePath,s,'utf8');if(s.includes('\r\n'))throw new Error('game line endings changed');
const include="require('./test_overlord_flyover_intro_0915.cjs')(vm,ctxv,ok);\r\n",marker="require('./test_overlord_gauge_intro_0915.cjs')(vm,ctxv,ok);\r\n";
if(!suite.includes(include)){const n=suite.split(marker).length-1;if(n!==1)throw new Error('suite marker count '+n);fs.writeFileSync(suitePath,suite.replace(marker,marker+include),'utf8');}
if(/(^|[^\r])\n/.test(fs.readFileSync(suitePath,'utf8')))throw new Error('suite endings changed');
console.log('patched Overlord bottom flyover, full shadow and whip spin');

