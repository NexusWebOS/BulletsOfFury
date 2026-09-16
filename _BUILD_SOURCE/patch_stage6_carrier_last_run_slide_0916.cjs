const fs=require('fs'),path=require('path');
const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function once(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"  if(carrierThunderheadTick(b,dt))return;\n",
`  /* PHASE 6 "CONSTANTLY SLIDES". This traverse belongs to the frame clock, including warning,
     cannon and cooldown frames. Keeping it before every controller return makes the giant hull
     continue flying while its live hardpoints, fields and effects remain anchored to it. */
  if(M.phase===5){const W=worldWidth(),amp=Math.max(60,W*.5-Math.max(150,b.w*.5));b.x=W*.5+Math.sin(M.t*.85)*amp;}
  if(carrierThunderheadTick(b,dt))return;
`,
'continuous last-run traverse');
once(
`  /* ⚠ PHASE 6 "CONSTANTLY SLIDES" - a continuous traverse, driven per FRAME, not per volley. It
     has to sit above the M.cd gate below or it would only move when the guns happen to fire. */
  if(M.phase===5){ const _W=worldWidth(), _amp=Math.max(60,_W*0.5-Math.max(150,b.w*0.5));
    b.x=_W*0.5+Math.sin(M.t*0.85)*_amp; }
`,
"",
'remove gated last-run traverse');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);
const testPath=path.resolve(__dirname,'test_fl.js');let t=fs.readFileSync(testPath),old=Buffer.from("require('./test_stage6_carrier_gravity_mine_warning_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),add=Buffer.from("require('./test_stage6_carrier_gravity_mine_warning_0916.cjs')(vm,ctxv,ok);\r\nrequire('./test_stage6_carrier_last_run_slide_0916.cjs')(vm,ctxv,ok);\r\n",'ascii'),at=t.indexOf(old);if(at<0||t.indexOf(old,at+old.length)>=0)throw new Error('test_fl anchor missing or repeated');t=Buffer.concat([t.subarray(0,at),add,t.subarray(at+old.length)]);if(!t.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(testPath,t);console.log('PATCHED_STAGE6_CARRIER_LAST_RUN_SLIDE_0916');
