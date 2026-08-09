const fs=require('fs'), vm=require('vm');
const listeners=[];
const mkCtx=()=>new Proxy({},{get:(t,k)=>{
  if(k==='canvas') return mkEl();
  if(k==='measureText') return ()=>({width:10});
  if(k==='createLinearGradient'||k==='createRadialGradient'||k==='createPattern') return ()=>({addColorStop(){}});
  if(k==='getImageData') return ()=>({data:new Uint8ClampedArray(4)});
  if(k==='save'||k==='restore') return ()=>{};
  return typeof k==='string' ? ()=>{} : undefined;
},set:()=>true});
function mkEl(id){ return { id:id||'', style:{}, width:480, height:512, dataset:{},
  getContext:()=>mkCtx(),
  addEventListener:(k,f)=>{ listeners.push('el:'+k); const key='el#'+(id||'')+':'+k;
    (sandbox.__handlers[key]=sandbox.__handlers[key]||[]).push(f); },
  removeEventListener(){},
  appendChild(){}, removeChild(){}, setAttribute(){}, getAttribute:()=>null, focus(){}, blur(){},
  getBoundingClientRect:()=>({left:0,top:0,width:480,height:512}),
  classList:{add(){},remove(){},toggle(){},contains:()=>false},
  querySelector:()=>mkEl(), querySelectorAll:()=>[], insertBefore(){}, cloneNode(){return mkEl();} }; }
const sandbox={};
sandbox.window=sandbox;
sandbox.globalThis=sandbox;
sandbox.self=sandbox;
sandbox.__errs=[];
sandbox.console={log:()=>{}, warn:()=>{}, info:()=>{},
  error:function(){ sandbox.__errs.push(Array.from(arguments).map(function(a){
    return (a&&a.message)? (a.message+' @ '+String(a.stack||'').split('\n')[1]) : String(a); }).join(' | ')); }};
sandbox.document={ createElement:(t)=>mkEl(t), getElementById:(id)=>mkEl(id),
  body:mkEl('body'), documentElement:mkEl('html'), head:mkEl('head'),
  addEventListener:(k,f)=>{ listeners.push('doc:'+k); (sandbox.__handlers[k]=sandbox.__handlers[k]||[]).push(f); }, removeEventListener(){},
  querySelector:()=>mkEl(), querySelectorAll:()=>[], fonts:{ready:Promise.resolve(),load:()=>Promise.resolve(),add(){}},
  visibilityState:'visible', hidden:false, title:'' };
sandbox.__handlers={};
sandbox.addEventListener=(k,f)=>{ listeners.push('win:'+k); (sandbox.__handlers[k]=sandbox.__handlers[k]||[]).push(f); };
sandbox.removeEventListener=()=>{};
sandbox.Image=function(){ const o={complete:false,naturalWidth:0,naturalHeight:0,onload:null,onerror:null};
  Object.defineProperty(o,'src',{set(){},get(){return '';}}); return o; };
sandbox.Audio=function(){ return {play:()=>Promise.resolve(),pause(){},load(){},addEventListener(){},
  currentTime:0,volume:1,muted:false,preload:''}; };
sandbox.AudioContext=function(){ throw new Error('AudioContext CONSTRUCTION BLOCKED'); };
sandbox.__unusedAudioCtx=function(){ return {createGain:()=>({connect(){},gain:{value:1,setValueAtTime(){}}}),
  createBufferSource:()=>({connect(){},start(){},stop(){},buffer:null}),
  createBuffer:()=>({getChannelData:()=>new Float32Array(128),duration:0.1,length:128,sampleRate:44100}),
  createDynamicsCompressor:()=>({connect(){},threshold:{value:0},knee:{value:0},ratio:{value:0},attack:{value:0},release:{value:0}}),
  createBiquadFilter:()=>({connect(){},frequency:{value:0},Q:{value:0},type:''}),
  createConvolver:()=>({connect(){},buffer:null}),
  sampleRate:44100, createOscillator:()=>({connect(){},start(){},stop(){},frequency:{value:0}}),
  decodeAudioData:()=>Promise.resolve({}), destination:{}, state:'running', resume:()=>Promise.resolve(), currentTime:0 }; };
sandbox.webkitAudioContext=sandbox.AudioContext;
sandbox.localStorage={getItem:()=>null,setItem(){},removeItem(){},clear(){}};
sandbox.sessionStorage=sandbox.localStorage;
sandbox.navigator={userAgent:'node-browser',maxTouchPoints:0,getGamepads:()=>[],language:'en'};
sandbox.location={href:'file:///x/index.html',search:'',hash:''};
sandbox.performance={now:()=>Date.now()};
sandbox.requestAnimationFrame=()=>0; sandbox.cancelAnimationFrame=()=>{};
sandbox.setTimeout=setTimeout; sandbox.clearTimeout=clearTimeout;
sandbox.setInterval=()=>0; sandbox.clearInterval=()=>{};
sandbox.devicePixelRatio=1;
sandbox.matchMedia=()=>({matches:false,addEventListener(){},addListener(){}});
sandbox.fetch=()=>Promise.resolve({ok:true,json:()=>Promise.resolve({}),text:()=>Promise.resolve('')});
vm.createContext(sandbox);
function runScript(file){
  try{
    vm.runInContext(fs.readFileSync(file,'utf8'), sandbox, {filename:file});
    return null;
  }catch(e){ return e; }
}
for(const f of ['assets/manifest.js','assets/game.js']){
  const err=runScript(f);
  if(err){
    console.log('*** '+f+' THREW ***');
    console.log('    '+String(err.message||err));
    const st=String(err.stack||'').split('\n').filter(l=>l.includes(f)).slice(0,2).join('\n');
    if(st) console.log(st);
    process.exit(1);
  }
  console.log('OK  '+f);
}
console.log();
console.log('listeners bound:', listeners.length, listeners.slice(0,8).join(', '));
console.log('BOF/BOFX/BOFA  :', typeof sandbox.BOF, typeof sandbox.BOFX, typeof sandbox.BOFA);
console.log('drawScene      :', typeof sandbox.drawScene);
console.log('BootChime      :', typeof sandbox.BootChime, sandbox.BootChime===null?'(NULL)':'');

// ---- FUNCTIONAL: does the boot gate release on a keypress?
console.log();
try{
  const S=sandbox;
  const g=vm.runInContext('typeof state', S);
  console.log('state var       :', g, vm.runInContext("typeof state!=='undefined'?String(state):'-'", S));
  console.log('Input exposed   :', vm.runInContext("typeof Input", S));
  console.log('Input.keys      :', vm.runInContext("typeof Input!=='undefined'?typeof Input.keys:'-'", S));
  console.log('anyTap          :', vm.runInContext("typeof anyTap", S));
  console.log('drawBoot        :', vm.runInContext("typeof drawBoot", S));
  // simulate: press a key, then run the boot gate
  // fire a REAL keydown through whatever the game bound, exactly as a browser would
  const hs=(S.__handlers&&S.__handlers['keydown'])||[];
  console.log('keydown handlers:', hs.length);
  for(const h of hs){ try{ h({key:'Enter', code:'Enter', keyCode:13, preventDefault(){}, repeat:false, target:{tagName:'CANVAS'}}); }catch(e){ console.log('   handler threw:', e.message); } }
  console.log('after keydown -> Input.down(enter):', vm.runInContext("typeof Input!=='undefined'?String(Input.down('enter')):'-'", S));
  const before=vm.runInContext("typeof drawBoot!=='undefined'?String(drawBoot._started):'-'", S);
  vm.runInContext("try{ stateT=1.0; for(var i=0;i<3;i++) drawBoot(1/60); }catch(e){ globalThis.__bootErr=String(e.message); }", S);
  const err=vm.runInContext("typeof __bootErr!=='undefined'?__bootErr:''", S);
  const after=vm.runInContext("typeof drawBoot!=='undefined'?String(drawBoot._started):'-'", S);
  console.log('drawBoot threw  :', err||'no');
  console.log('_started        :', before, '->', after);
  // ---- FULL PATH: boot -> title -> can the menu cursor move?
  vm.runInContext("try{ stateT=9; for(var i=0;i<400;i++){ stateT+=1/60; drawScene(1/60);} }catch(e){ globalThis.__flowErr=String(e.message); }", S);
  console.log('flow threw      :', vm.runInContext("typeof __flowErr!=='undefined'?__flowErr:'no'", S));
  console.log('state now       :', vm.runInContext("String(state)", S));
  const mi0=vm.runInContext("typeof menuIndex!=='undefined'?menuIndex:-1", S);
  const hs2=(S.__handlers&&S.__handlers['keydown'])||[];
  for(const h of hs2){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},repeat:false,target:{tagName:'CANVAS'}}); }catch(e){} }
  vm.runInContext("try{ drawScene(1/60); }catch(e){ globalThis.__navErr=String(e.message); }", S);
  const mi1=vm.runInContext("typeof menuIndex!=='undefined'?menuIndex:-1", S);
  console.log('menuIndex       :', mi0, '->', mi1, mi0===mi1 ? '  *** CURSOR DID NOT MOVE ***' : '  (moved)');
  console.log('nav threw       :', vm.runInContext("typeof __navErr!=='undefined'?__navErr:'no'", S));
  // RUN THE REAL LOOP, and surface what its try/catch swallows
  let t=1000;
  vm.runInContext("globalThis.__now=1000;", S);
  for(let i=0;i<600;i++){
    t+=16.7;
    vm.runInContext("__now="+t+"; try{ loop(__now); }catch(e){ (globalThis.__errs=globalThis.__errs||[]).push('LOOP THREW: '+e.message); }", S);
  }
  const errs=S.__errs||[];
  console.log();
  console.log('=== errors the loop SWALLOWED over 600 frames ===');
  if(!errs.length) console.log('   none');
  else errs.slice(0,5).forEach(function(e){ console.log('   '+e); });
  console.log('state after loop:', vm.runInContext("String(state)", S));
  console.log('stateT          :', vm.runInContext("String(stateT)", S));
  console.log('goTitle reached?:', vm.runInContext("(function(){ try{ var n=0; var o=goTitle; goTitle=function(){ n++; return o.apply(null,arguments); }; drawLoading(1/60); goTitle=o; return 'called '+n+' time(s)'; }catch(e){ return 'probe threw: '+e.message; } })()", S));
  console.log('goTitle direct  :', vm.runInContext("(function(){ try{ goTitle(); return 'ok, state='+state; }catch(e){ return 'THREW: '+e.message; } })()", S));
  console.log('frames drawn    :', vm.runInContext("String(window.__bofFrames||0)", S));
  // NAVIGATE THE MENU now that we have actually reached the title
  const before2=vm.runInContext("String(menuIndex)", S);
  const hs3=(S.__handlers&&S.__handlers['keydown'])||[];
  for(const h of hs3){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},repeat:false,target:{tagName:'CANVAS'}}); }catch(e){} }
  t+=16.7; vm.runInContext("__now="+t+"; loop(__now);", S);
  const after2=vm.runInContext("String(menuIndex)", S);
  console.log();
  console.log('MENU NAV at title: menuIndex '+before2+' -> '+after2+(before2!==after2?'   CURSOR MOVES':'   still stuck'));
  // and confirm the boot chime object exists
  console.log('menuDown() direct:', vm.runInContext("(function(){ try{ Input.keys['arrowdown']=true; var r=[]; r.push('down()='+Input.down('arrowdown')); return r.join(' '); }catch(e){ return 'ERR '+e.message; } })()", S));
  console.log('tap path         :', vm.runInContext("(function(){ try{ var hs=window.__handlers&&window.__handlers['keydown']; return hs? hs.length+' handlers':'none'; }catch(e){ return 'n/a'; } })()", S));
  // SURGICAL: at title, set the tap by hand and call the input handler directly
  console.log();
  console.log('--- input chain at title ---');
  console.log('state           :', vm.runInContext("String(state)", S));
  console.log('titlePending    :', vm.runInContext("String(titlePending)", S));
  console.log('keybind.down    :', vm.runInContext("JSON.stringify(keybind.down)", S));
  vm.runInContext("Input.clearTaps();", S);
  const hs4=(S.__handlers&&S.__handlers['keydown'])||[];
  const hu4=(S.__handlers&&S.__handlers['keyup'])||[];
  // release first — key() suppresses auto-repeat via !keys[k], so a stale 'down' blocks every tap
  for(const h of hu4){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},target:{tagName:'CANVAS'}}); }catch(e){} }
  for(const h of hs4){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},repeat:false,target:{tagName:'CANVAS'}}); }catch(e){ console.log('   kd threw:',e.message); } }
  console.log('menuDown() now  :', vm.runInContext("(function(){ try{ return String(Input.menuDown()); }catch(e){ return 'ERR '+e.message; } })()", S));
  vm.runInContext("Input.clearTaps();", S);
  for(const h of hu4){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},target:{tagName:'CANVAS'}}); }catch(e){} }
  for(const h of hs4){ try{ h({key:'ArrowDown',code:'ArrowDown',keyCode:40,preventDefault(){},repeat:false,target:{tagName:'CANVAS'}}); }catch(e){} }
  const m0=vm.runInContext("String(menuIndex)", S);
  console.log('handleTitleInput:', vm.runInContext("(function(){ try{ handleTitleInput(); return 'ran'; }catch(e){ return 'THREW: '+e.message; } })()", S));
  console.log('menuIndex       :', m0, '->', vm.runInContext("String(menuIndex)", S));
  // ---- MOUSE: click a menu row on the canvas
  console.log();
  console.log('--- click path ---');
  const canvasKeys=Object.keys(S.__handlers||{}).filter(function(k){ return k.indexOf('el#screen:')===0; });
  console.log('canvas listeners:', canvasKeys.map(function(k){return k.split(':')[1];}).join(', ')||'NONE');
  const y0=vm.runInContext("typeof TMENU_Y0!=='undefined'?TMENU_Y0:-1", S);
  const gap=vm.runInContext("typeof TMENU_GAP!=='undefined'?TMENU_GAP:-1", S);
  console.log('TMENU_Y0 / GAP  :', y0, '/', gap);
  const md=(S.__handlers||{})['el#screen:mousedown']||[];
  const mm=(S.__handlers||{})['el#screen:mousemove']||[];
  const ev={clientX:240, clientY:(y0>0?y0+gap:200), touches:null, preventDefault(){}};
  for(const h of mm){ try{ h(ev); }catch(e){ console.log('   mousemove threw:', e.message); } }
  for(const h of md){ try{ h(ev); }catch(e){ console.log('   mousedown threw:', e.message); } }
  console.log('mouse.down      :', vm.runInContext("String(Input.mouse.down)", S));
  console.log('mouse x,y       :', vm.runInContext("Input.mouse.x+','+Input.mouse.y", S));
  const tp0=vm.runInContext("String(titlePending)", S);
  vm.runInContext("try{ handleTitleInput(); }catch(e){ globalThis.__hti=String(e.message); }", S);
  console.log('titlePending    :', tp0, '->', vm.runInContext("String(titlePending)", S));
  // ---- SELECT "NEW GAME" AND FOLLOW IT
  console.log();
  console.log('--- selecting NEW GAME ---');
  vm.runInContext("menuIndex=0; titlePending=null; menuFlash=0;", S);
  vm.runInContext("try{ chooseTitle(); }catch(e){ globalThis.__ct=String(e.message); }", S);
  console.log('chooseTitle threw:', vm.runInContext("typeof __ct!=='undefined'?__ct:'no'", S));
  console.log('titlePending     :', vm.runInContext("String(titlePending)", S), ' menuFlash:', vm.runInContext("String(menuFlash)", S));
  for(let i=0;i<40;i++){ t+=16.7; vm.runInContext("__now="+t+"; loop(__now);", S); }
  console.log('state after 40f  :', vm.runInContext("String(state)", S));
  console.log('titlePending now :', vm.runInContext("String(titlePending)", S));
  const errs2=S.__errs||[];
  console.log('errors swallowed :', errs2.length? errs2.slice(-3).join(' || ') : 'none');
  // ---- WALK THE WHOLE MENU CHAIN with confirm presses
  console.log();
  console.log('--- walking the menu chain ---');
  const hsK=(S.__handlers&&S.__handlers['keydown'])||[];
  const huK=(S.__handlers&&S.__handlers['keyup'])||[];
  function press(k){
    for(const h of huK){ try{ h({key:k,code:k,preventDefault(){},target:{tagName:'CANVAS'}}); }catch(e){} }
    for(const h of hsK){ try{ h({key:k,code:k,repeat:false,preventDefault(){},target:{tagName:'CANVAS'}}); }catch(e){} }
  }
  for(let step=0; step<10; step++){
    const before=vm.runInContext("String(state)", S);
    press('Enter');
    for(let i=0;i<45;i++){ t+=16.7; vm.runInContext("__now="+t+"; loop(__now);", S); }
    const after=vm.runInContext("String(state)", S);
    console.log('  press '+(step+1)+': '+before+'  ->  '+after+(before===after?'   *** STUCK ***':''));
    if(after==='play') break;
    if(before===after && step>1) break;
  }
  const e3=S.__errs||[];
  if(e3.length) console.log('  swallowed:', e3.slice(-2).join(' || '));
  console.log();
  console.log('--- why is PILOT stuck? ---');
  console.log('state          :', vm.runInContext("String(state)", S));
  console.log('pilotIndex     :', vm.runInContext("String(pilotIndex)", S), vm.runInContext("String((PILOTS[pilotIndex]||{}).key)", S));
  console.log('pilotPending   :', vm.runInContext("String(pilotPending)", S));
  console.log('pilotRot       :', vm.runInContext("String(pilotRot)", S));
  console.log('locked?        :', vm.runInContext("String(isPilotLocked(PILOTS[pilotIndex]))", S));
  console.log('pilotComm      :', vm.runInContext("String(pilotComm)", S));
  console.log('menuConfirm()  :', vm.runInContext("(function(){ Input.clearTaps(); return 'need a tap'; })()", S));
  press('Enter');
  console.log('after press cfm:', vm.runInContext("(function(){ try{ return String(Input.menuConfirm()); }catch(e){ return 'ERR'; } })()", S));
  vm.runInContext("try{ confirmPilot(); }catch(e){ globalThis.__cp=String(e.message); }", S);
  console.log('confirmPilot   :', vm.runInContext("typeof __cp!=='undefined'?__cp:'no throw'", S), ' pilotPending now', vm.runInContext("String(pilotPending)", S));
  for(let i=0;i<180;i++){ t+=16.7; vm.runInContext("__now="+t+"; loop(__now);", S); }
  console.log('state after 3s :', vm.runInContext("String(state)", S));
  // KEEP GOING to gameplay, and report the first state that stops changing
  let prev=vm.runInContext("String(state)", S), stall=0;
  for(let i=0;i<1200;i++){
    t+=16.7; vm.runInContext("__now="+t+"; loop(__now);", S);
    if(i%40===0){ press('Enter'); }
    const cur=vm.runInContext("String(state)", S);
    if(cur!==prev){ console.log('   -> '+cur+' (frame '+i+')'); prev=cur; stall=0; }
    else stall++;
    if(cur==='play') break;
  }
  console.log('FINAL state    :', vm.runInContext("String(state)", S));
  const eF=S.__errs||[];
  console.log('errors swallowed:', eF.length? eF.slice(-3).join(' || ') : 'none');
  console.log('BootChime ready  :', vm.runInContext("(function(){ try{ return typeof BootChime==='object' && BootChime!==null ? 'yes' : String(BootChime); }catch(e){ return 'not in scope (vm artefact)'; } })()", S));
}catch(e){ console.log('functional probe failed:', e.message); }
