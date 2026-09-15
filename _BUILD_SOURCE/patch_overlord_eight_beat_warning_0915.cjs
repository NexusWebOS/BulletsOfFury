const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),gamePath=path.join(root,'assets','game.js'),suitePath=path.join(root,'_BUILD_SOURCE','test_fl.js');
const recovery=path.join(root,'_shots','overlord_eight_beat_warning_0915','recovery');fs.mkdirSync(recovery,{recursive:true});
const before=fs.readFileSync(gamePath,'utf8'),suite=fs.readFileSync(suitePath,'utf8');
if(before.includes('\r\n'))throw new Error('game must remain LF');
if(/(^|[^\r])\n/.test(suite))throw new Error('suite must remain CRLF');
fs.writeFileSync(path.join(recovery,'game.js.before'),before);
fs.writeFileSync(path.join(recovery,'test_fl.js.before'),suite);
let s=before;
function once(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, got '+n);s=s.replace(a,b);}

once("function ovStartChargeTell(b){\n  b._ovState='chargeTell';\n  b._chargeTell={t:0,dur:b._enraged?0.86:1.08,lane:clamp(player.x,72,VW-72),locked:false,pulse:0};\n",
"const OV_CHARGE_BEATS=8, OV_CHARGE_TELL=1.60, OV_CHARGE_FLASH=.105;\n"+
"function ovChargeWarningProgress(T){return T&&T.flash>0?.999:clamp((T&&T.t||0)/Math.max(.001,T&&T.dur||OV_CHARGE_TELL),0,1);}\n"+
"function ovChargeWarningBeat(T,beat){\n"+
"  if(!T||beat<=T.beat)return;\n"+
"  for(let n=T.beat+1;n<=beat;n++){\n"+
"    T.beat=n;T.flash=OV_CHARGE_FLASH;\n"+
"    try{if(Audio.SFX){const fn=Audio.SFX.retinaLockBeep||Audio.SFX.blip;if(fn)fn();}}catch(_ovb){}\n"+
"  }\n"+
"}\n"+
"function ovStartChargeTell(b){\n"+
"  b._ovState='chargeTell';\n"+
"  b._chargeTell={t:0,dur:OV_CHARGE_TELL,lane:clamp(player.x,72,VW-72),locked:false,pulse:0,beat:-1,flash:0};\n",
'charge constants and exact beat state');

once("      const T=b._chargeTell, p=clamp(T.t/T.dur,0,1), hub=ovMount(b,0,4);\n      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,fieldOnly:true});\n",
"      const T=b._chargeTell, p=ovChargeWarningProgress(T), hub=ovMount(b,0,4);\n"+
"      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,fieldOnly:true});\n",
'field uses red beat flash');

once("      const T=b._chargeTell,p=clamp(T.t/T.dur,0,1),hub=ovMount(b,0,4);\n      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,alertOnly:true});\n",
"      const T=b._chargeTell,p=ovChargeWarningProgress(T),hub=ovMount(b,0,4);\n"+
"      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,alertOnly:true});\n",
'alert uses red beat flash');

once("  if(S==='chargeTell'){\n    const T=b._chargeTell; T.t+=dt; T.pulse=(T.pulse||0)-dt;\n    const p=clamp(T.t/T.dur,0,1);\n    combatWarningTick(b,'overlord-charge',T.t,T.dur);\n",
"  if(S==='chargeTell'){\n"+
"    const T=b._chargeTell; T.t+=dt; T.pulse=(T.pulse||0)-dt;T.flash=Math.max(0,(T.flash||0)-dt);\n"+
"    const p=clamp(T.t/T.dur,0,1),beat=Math.min(OV_CHARGE_BEATS-1,Math.floor(p*OV_CHARGE_BEATS));\n"+
"    ovChargeWarningBeat(T,beat);\n"+
"    combatWarningTick(b,'overlord-charge',T.t,T.dur,true);\n",
'eight-beat simulation owner');

once("function combatWarningTick(owner,id,elapsed,duration){\n  if(!owner)return;const warnings=owner._combatWarnings||(owner._combatWarnings={});\n  let B=warnings[id];\n  if(!B||elapsed<B.t){B=warnings[id]={t:0,warm:duration,released:false};l23FovWarm();}\n  B.t=elapsed;B.warm=duration;B.released=elapsed>=duration;l23WarnSound(B);\n}\n",
"function combatWarningTick(owner,id,elapsed,duration,silent){\n"+
"  if(!owner)return;const warnings=owner._combatWarnings||(owner._combatWarnings={});\n"+
"  let B=warnings[id];\n"+
"  if(!B||elapsed<B.t){B=warnings[id]={t:0,warm:duration,released:false};l23FovWarm();}\n"+
"  B.t=elapsed;B.warm=duration;B.released=elapsed>=duration;if(!silent)l23WarnSound(B);\n"+
"}\n",
'optional shared warning sound suppression');

fs.writeFileSync(gamePath,s,'utf8');
if(s.includes('\r\n'))throw new Error('game line endings changed');
const include="require('./test_overlord_eight_beat_warning_0915.cjs')(vm,ctxv,ok);\r\n";
const marker="require('./test_overlord_flyover_intro_0915.cjs')(vm,ctxv,ok);\r\n";
if(!suite.includes(include)){
  const n=suite.split(marker).length-1;if(n!==1)throw new Error('suite marker count '+n);
  fs.writeFileSync(suitePath,suite.replace(marker,marker+include),'utf8');
}
if(/(^|[^\r])\n/.test(fs.readFileSync(suitePath,'utf8')))throw new Error('suite endings changed');
console.log('patched Overlord eight-beat red charge warning');

