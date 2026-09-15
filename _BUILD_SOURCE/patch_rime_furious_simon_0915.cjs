const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
const backup=path.join(root,'_shots','backups','game_pre_rime_furious_simon_0915.js');
let s=fs.readFileSync(file,'utf8');
if(s.includes('\r\n'))throw new Error('assets/game.js must remain LF-only');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.copyFileSync(file,backup);
function rep(from,to,label){
  const n=s.split(from).length-1;
  if(n!==1)throw new Error(label+' expected exactly once, found '+n);
  s=s.replace(from,to);
}
function repBetween(start,end,to,label){
  const a=s.indexOf(start),b=s.indexOf(end,a+start.length);
  if(a<0||b<0||s.indexOf(start,a+1)>=0)throw new Error(label+' boundaries are not unique');
  s=s.slice(0,a)+to+s.slice(b);
}

rep(
  "  b._s3boss={role:b._ship==='rimewall'?'spear':'wall',volley:null,charge:null,cannonSeq:null,cannonGlow:null,slide:null,\n",
  "  b._s3boss={role:b._ship==='rimewall'?'spear':'wall',volley:null,charge:null,cannonSeq:null,cannonGlow:null,slide:null,furyFeint:null,\n",
  'stage3 init');
rep(
  "  const col=l23FovPhase(k), key='bmfx_fov_'+col+'_tall';\n",
  "  const col=B.fovColor||l23FovPhase(k), key='bmfx_fov_'+col+'_tall';\n",
  'FOV color override');
rep(
  "function stage3CoreWarningDraw(b){\n  const C=b&&b._s3boss&&b._s3boss.charge;if(!C||C.kind!=='centerPulse'||C.t>=C.dur)return;\n",
  "function stage3CoreWarningDraw(b){\n  const C=b&&b._s3boss&&b._s3boss.charge;if(!C||C.kind!=='centerPulse'||C.t>=C.dur||b._s3boss.furyFeint)return;\n",
  'Furious center-warning suppression');

const simon=`/* Furious Rime Wall Simon-Says cannon tell. Five short authored FOV beats alternate between the
   visible side cannons: yellow, red, yellow, red, then one rapidly flashing red commitment lane.
   Only that final cannon fires. There is deliberately no overhead alert plate on Furious; the
   player has to read the mount/lane sequence itself, but the final flash still leaves a fixed
   commitment window and the released beam never tracks. */
const S3_FURY_FEINT_BEAT=.34;
const S3_FURY_FEINT_COLORS=['yellow','red','yellow','red','red'];
function stage3FuryFeintAngle(pat,slot){
  if(pat==='s3wallgate')return Math.PI/2+(slot==='L'?.72:-.72);
  if(pat==='s3walloverdrive')return Math.PI/2+(slot==='L'?.95:-.95);
  return Math.PI/2;
}
function stage3FuryFeintStart(b,pat,step,active,width){
  const S=b&&b._s3boss;if(!S||S.role!=='wall'||S.furyFeint||b._l23Beam)return false;
  const actual=(step&1)?'L':'R',other=actual==='L'?'R':'L';
  S.furyFeint={t:0,i:-1,beat:S3_FURY_FEINT_BEAT,pat:pat,actual:actual,active:active,width:width,
    seq:[other,actual,actual,other,actual],colors:S3_FURY_FEINT_COLORS.slice(),log:[]};
  l23FovWarm();
  return true;
}
function stage3FuryFeintTick(b,dt){
  const S=b&&b._s3boss,F=S&&S.furyFeint;if(!F)return false;
  F.t+=dt;const ni=Math.min(F.seq.length-1,Math.floor(F.t/F.beat));
  while(F.i<ni){
    F.i++;F.log.push({type:'cue',slot:F.seq[F.i],color:F.colors[F.i],at:F.i*F.beat});
    try{if(Audio&&Audio.SFX){const fn=F.i===F.seq.length-1?(Audio.SFX.dangerAlert||Audio.SFX.alertLockon):(F.colors[F.i]==='red'?(Audio.SFX.alertLockon||Audio.SFX.dangerAlert):Audio.SFX.blip);if(fn)fn();}}catch(_s3ffx){}
  }
  if(F.t<F.seq.length*F.beat)return true;
  const a=stage3FuryFeintAngle(F.pat,F.actual);
  b._l23Beam={family:'rime',slots:[F.actual],angles:[a],t:L23_WARN_T,warm:L23_WARN_T,
    active:F.active,retract:.24,width:F.width,released:true,spin:0,baseAngles:[a],sweepArc:0,sweepRate:0,sweepPhase:0,_furySimon:true};
  shipBossMuzzleStart(b,[F.actual],{life:.24,hpx:62});
  S.cannonGlow={slot:F.actual,t:F.active};
  F.log.push({type:'fire',slot:F.actual,color:'red',at:F.t});S.lastFeintLog=F.log.slice();S.furyFeint=null;
  try{if(Audio.SFX&&(Audio.SFX.enemyHeavyLaser||Audio.SFX.laserShot||Audio.SFX.enemyBossCannon))(Audio.SFX.enemyHeavyLaser||Audio.SFX.laserShot||Audio.SFX.enemyBossCannon)();}catch(_s3ffs){}
  return false;
}
function stage3FuryFeintDraw(b){
  const F=b&&b._s3boss&&b._s3boss.furyFeint;if(!F||typeof XART==='undefined')return false;
  const i=clamp(Math.floor(F.t/F.beat),0,F.seq.length-1),local=clamp((F.t-i*F.beat)/F.beat,0,1),final=i===F.seq.length-1;
  if(final&&(Math.floor(local*10)&1))return true;
  const slot=F.seq[i],a=stage3FuryFeintAngle(F.pat,slot),p=shipBossMount(b,slot),lane=F.width*1.35;
  const B={family:'rime',angles:[a],t:local*F.beat,warm:F.beat,released:false,fovColor:F.colors[i]};
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);l23FovDraw(b,B,0,p,Math.max(.18,local),lane);ctx.restore();
  return true;
}
`;
rep(
  "function stage3BossTick(b,dt){\n",
  simon+"function stage3BossTick(b,dt){\n",
  'Furious Simon functions');
rep(
  "  S.damaged=frac<=.52;S.critical=frac<=.25;\n  if(S.volley){\n",
  "  S.damaged=frac<=.52;S.critical=frac<=.25;\n  stage3FuryFeintTick(b,dt);\n  if(S.volley){\n",
  'Furious Simon tick hook');
rep(
  "  if(b._brk && typeof beamRakeDraw==='function') beamRakeDraw(b);\n  if(b._l23Beam&&typeof l23BossBeamDraw==='function')l23BossBeamDraw(b);\n",
  "  if(b._brk && typeof beamRakeDraw==='function') beamRakeDraw(b);\n  if(b._s3boss&&b._s3boss.furyFeint&&typeof stage3FuryFeintDraw==='function')stage3FuryFeintDraw(b);\n  if(b._l23Beam&&typeof l23BossBeamDraw==='function')l23BossBeamDraw(b);\n",
  'Furious Simon under-hull draw hook');

const liveRouter=`function stage3WallLaserAttack(b,pat,step){
  const S=b&&b._s3boss;if(!S||S.role!=='wall')return false;
  const slots=['L','R'],angles=[Math.PI/2,Math.PI/2];let arc=[0,0],width=30,active=.72;
  if(pat==='s3wallgate'){angles[0]+=.72;angles[1]-=.72;arc=[.22,-.22];active=.95;}
  else if(pat==='s3wallhalo'){slots.splice(step&1?1:0,1);angles.splice(step&1?1:0,1);arc=[0];width=30;active=.88;}
  else if(pat==='s3walloverdrive'){angles[0]+=.95;angles[1]-=.95;arc=[.42,-.42];width=34;active=1.05;}
  else if(pat!=='s3wallcannons')return false;
  /* The Hard laser-ball pair must be wired at the live router. The older phase blocks below this
     function are historical and unreachable because this function owns every Rime Wall pattern. */
  if(pat==='s3wallhalo'||pat==='s3walloverdrive')stage3BossHardLaserPair(b);
  if(typeof diffKey!=='undefined'&&diffKey==='furious'){
    if(S.furyFeint||b._l23Beam)return true;
    if(!stage3FuryFeintStart(b,pat,step,active,width))return true;
    const total=S3_FURY_FEINT_COLORS.length*S3_FURY_FEINT_BEAT;
    S.volley=null;S.cannonSeq=null;S.charge={t:0,dur:total,slot:'C',kind:'centerPulse',released:false};
    S.lastPattern=pat;S.patternsSeen[pat]=(S.patternsSeen[pat]||0)+1;
    stage3BossBeginSlide(b,total+active+1.05);b.fireCd=(total+active+1.0)*1.22;
    return true;
  }
  if(!l23BossBeamStart(b,'rime',slots,angles,L23_WARN_T,active,.24,width,{sweepArc:arc,sweepRate:2.6}))return true;
  S.volley=null;S.cannonSeq=null;S.charge={t:0,dur:L23_WARN_T,slot:'C',kind:'centerPulse',released:false};
  S.lastPattern=pat;S.patternsSeen[pat]=(S.patternsSeen[pat]||0)+1;
  stage3BossBeginSlide(b,L23_WARN_T+active+1.05);b.fireCd=(L23_WARN_T+active+1.0)*1.35;
  return true;
}
`;
repBetween('function stage3WallLaserAttack(b,pat,step){','function stage4GeneratorColumn(',liveRouter,'live Rime Wall router');

if(s.includes('\r\n'))throw new Error('patch introduced CRLF');
fs.writeFileSync(file,s,'utf8');
console.log('patched Rime Wall Furious Simon-Says tell and live Hard laser-ball route');
