const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),gamePath=path.join(root,'assets','game.js'),testPath=path.join(root,'_BUILD_SOURCE','test_fl.js');
const recovery=path.join(root,'_shots','overlord_gauge_intro_0915','recovery');fs.mkdirSync(recovery,{recursive:true});
const original=fs.readFileSync(gamePath,'utf8'),originalTest=fs.readFileSync(testPath,'utf8');
if(original.includes('\r\n'))throw new Error('assets/game.js must remain LF');
if(!originalTest.includes('\r\n')||/(^|[^\r])\n/.test(originalTest))throw new Error('test_fl.js must remain CRLF');
fs.writeFileSync(path.join(recovery,'game.js.before'),original,'utf8');fs.writeFileSync(path.join(recovery,'test_fl.js.before'),originalTest,'utf8');
let game=original;
function once(a,b,label){const n=game.split(a).length-1;if(n!==1)throw new Error(label+' expected once, got '+n);game=game.replace(a,b);}

once("function bossHealthVisible(b){\n  if(!b||b.dead)return false;\n  if(b._s7FinalNoBar)return false;\n  const F=b._s9fusion;\n  return !(F&&F.phase!=='tidal');\n}\n",
"function bossHealthVisible(b){\n  if(!b||b.dead)return false;\n  if(b._s7FinalNoBar)return false;\n  if(b.kind==='damkeeper'&&b._ovIntro&&!b._ovIntro.done)return b._ovIntro.phase!=='approach';\n  const F=b._s9fusion;\n  return !(F&&F.phase!=='tidal');\n}\n"+
"function bossHealthFraction(b){\n"+
"  if(!b)return 0;\n"+
"  if(b.kind==='damkeeper'&&b._ovIntro&&!b._ovIntro.done)return clamp(b._ovIntro.gauge||0,0,1);\n"+
"  return clamp((b.hp||0)/(b.maxhp||1),0,1);\n"+
"}\n"+
"function bossHealthAlpha(b){\n"+
"  return (b&&b.kind==='damkeeper'&&b._ovIntro&&!b._ovIntro.done)?clamp(b._ovIntro.alpha||0,0,1):1;\n"+
"}\n",'boss intro health helpers');

once("function drawHealthBarV2(kind, frac, cx, cy, w, inWorld){\n  if(typeof ctx==='undefined') return false;\n  const ok = drawHealthBarArt(kind, frac, cx, cy, w, inWorld)\n",
"function drawHealthBarV2(kind, frac, cx, cy, w, inWorld){\n"+
"  if(typeof ctx==='undefined') return false;\n"+
"  const _barBoss=(kind==='boss'&&typeof boss!=='undefined')?boss:null;\n"+
"  if(_barBoss&&typeof bossHealthFraction==='function')frac=bossHealthFraction(_barBoss);\n"+
"  ctx.save();ctx.globalAlpha*=(_barBoss&&typeof bossHealthAlpha==='function')?bossHealthAlpha(_barBoss):1;\n"+
"  const ok = drawHealthBarArt(kind, frac, cx, cy, w, inWorld)\n",'health bar intro alpha start');
once("  return ok;\n}\nlet _bmShieldDepth=0;\n",
"  ctx.restore();\n  return ok;\n}\nlet _bmShieldDepth=0;\n",'health bar intro alpha restore');

once("    case 'damkeeper': b.name='JUNGLE OVERLORD-X'; b.w=170; b.h=130; break;\n",
"    case 'damkeeper':\n"+
"      b.name='JUNGLE OVERLORD-X'; b.w=170; b.h=130; b._noHit=true;\n"+
"      b._ovIntro={phase:'approach',t:0,fromY:b.y,gauge:0,alpha:0,beat:-1,done:false};\n"+
"      break;\n",'Overlord intro initialization');

once("// ===== JUNGLE OVERLORD-X — smart health-gated helicopter boss AI =====\n",
"// ===== JUNGLE OVERLORD-X — smart health-gated helicopter boss AI =====\n"+
"function overlordIntroTick(b,dt){\n"+
"  const I=b&&b._ovIntro;if(!I||I.done)return false;I.t+=dt;\n"+
"  if(I.phase==='approach'){\n"+
"    const p=clamp(I.t/1.35,0,1),e=1-Math.pow(1-p,3);b.y=lerp(I.fromY,b.ty,e);\n"+
"    if(p>=1){b.y=b.ty;I.phase='fade';I.t=0;I.alpha=0;I.gauge=0;}\n"+
"    return true;\n"+
"  }\n"+
"  if(I.phase==='fade'){\n"+
"    I.alpha=clamp(I.t/.46,0,1);I.gauge=0;\n"+
"    if(I.t>=.46){I.phase='fill';I.t=0;I.alpha=1;I.beat=-1;}\n"+
"    return true;\n"+
"  }\n"+
"  if(I.phase==='fill'){\n"+
"    const p=clamp(I.t/1.68,0,1);I.alpha=1;I.gauge=p;const beat=Math.min(7,Math.floor(p*8));\n"+
"    if(beat>I.beat){I.beat=beat;if(Audio.SFX&&Audio.SFX.blip)Audio.SFX.blip();}\n"+
"    if(p>=1){I.phase='ready';I.t=0;I.gauge=1;if(Audio.SFX&&Audio.SFX.select)Audio.SFX.select();}\n"+
"    return true;\n"+
"  }\n"+
"  I.alpha=1;I.gauge=1;\n"+
"  if(I.t>=.28){I.done=true;b.enter=false;b._noHit=false;b.fireCd=.72;if(Audio.startMusic)Audio.startMusic('boss1');return false;}\n"+
"  return true;\n"+
"}\n",'Overlord gauge choreography');

once("function bossHitTest(x,y){\n  if(!boss) return false;\n",
"function bossHitTest(x,y){\n  if(!boss) return false;\n  if(boss.kind==='damkeeper'&&boss._ovIntro&&!boss._ovIntro.done)return false;\n",'Overlord intro collision gate');
once("  if(!boss||boss.dead) return;\n  const _elem=",
"  if(!boss||boss.dead) return;\n  if(boss.kind==='damkeeper'&&boss._ovIntro&&!boss._ovIntro.done)return;\n  const _elem=",'Overlord intro damage gate');

once("  if(b._hammer&&!b.dead){b.t+=dt;b.flash=Math.max(0,b.flash-dt);hammerBossTick(b,dt);return;}\n  b.t+=dt; if(!b.dead) b.rotor+=dt*30;\n",
"  if(b._hammer&&!b.dead){b.t+=dt;b.flash=Math.max(0,b.flash-dt);hammerBossTick(b,dt);return;}\n"+
"  b.t+=dt; if(!b.dead) b.rotor+=dt*30;\n"+
"  if(!b.dead&&b.kind==='damkeeper'&&b._ovIntro&&typeof overlordIntroTick==='function'&&overlordIntroTick(b,dt))return;\n",'Overlord intro update ownership');

once("          if(curStage.boss){ spawnBoss(curStage.boss); Audio.startMusic('boss'+run.stage); }\n",
"          if(curStage.boss){\n"+
"            spawnBoss(curStage.boss);\n"+
"            if(run.stage===1&&boss&&boss.kind==='damkeeper')Audio.stopMusic();\n"+
"            else Audio.startMusic('boss'+run.stage);\n"+
"          }\n",'deferred Overlord music');

fs.writeFileSync(gamePath,game,'utf8');if(game.includes('\r\n'))throw new Error('game line endings changed');
const include="require('./test_overlord_gauge_intro_0915.cjs')(vm,ctxv,ok);\r\n";
const marker="require('./test_locked_modes_0915.cjs')(vm,ctxv,ok);\r\n";
if(!originalTest.includes(include)){
  const n=originalTest.split(marker).length-1;if(n!==1)throw new Error('suite include marker count '+n);
  fs.writeFileSync(testPath,originalTest.replace(marker,marker+include),'utf8');
}
if(/(^|[^\r])\n/.test(fs.readFileSync(testPath,'utf8')))throw new Error('test line endings changed');
console.log('patched Jungle Overlord-X boss-gauge entrance');

