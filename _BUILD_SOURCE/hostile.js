/* HOSTILE ASSET TEST: every image is permanently unloaded (complete=false, naturalWidth=0).
   That is the worst case a lazy loader can present, and it is what Mike's flood of
   HTMLImageElement errors means. If the game can render a full frame under this, the class is dead. */
const fs=require('fs'), vm=require('vm');
let drawImageBad=0, drawCalls=0, thrown=[], firstStack='', tags=[];
const mkCtx=()=>new Proxy({},{get:(t,k)=>{
  if(k==='canvas') return mkEl();
  if(k==='measureText') return ()=>({width:10});
  if(k==='createLinearGradient'||k==='createRadialGradient'||k==='createPattern') return ()=>({addColorStop(){}});
  if(k==='getImageData') return ()=>({data:new Uint8ClampedArray(4)});
  if(k==='drawImage') return function(img){
    drawCalls++;
    if(!img){ drawImageBad++; throw new TypeError("Failed to execute 'drawImage': The provided value is not of type '(CSSImageValue or HTMLImageElement or ...)'"); }
    if(img.__isImg && !(img.complete && img.naturalWidth>0)){ drawImageBad++; throw new Error("Failed to execute 'drawImage' on 'CanvasRenderingContext2D': The HTMLImageElement provided is in the 'broken' state."); }
  };
  return typeof k==='string' ? ()=>{} : undefined;
},set:()=>true});
function mkEl(id){ return { __isCanvas:true, id:id||'', style:{}, width:480, height:512, dataset:{},
  getContext:()=>mkCtx(), addEventListener(){}, removeEventListener(){}, appendChild(){}, setAttribute(){},
  getBoundingClientRect:()=>({left:0,top:0,width:480,height:512}), focus(){},
  classList:{add(){},remove(){},toggle(){},contains:()=>false}, querySelector:()=>mkEl(), querySelectorAll:()=>[] }; }
const S={}; S.window=S; S.globalThis=S; S.self=S;
S.console={log(){},warn(){},error:function(){ thrown.push(Array.from(arguments).map(a=>(a&&a.message)||String(a)).join(' ')); },info(){}};
S.document={ createElement:(t)=>mkEl(t), getElementById:(id)=>mkEl(id), body:mkEl('body'),
  documentElement:mkEl('html'), head:mkEl('head'), addEventListener(){}, removeEventListener(){},
  querySelector:()=>mkEl(), querySelectorAll:()=>[], fonts:{ready:Promise.resolve(),load:()=>Promise.resolve()},
  visibilityState:'visible', hidden:false };
S.addEventListener=()=>{}; S.removeEventListener=()=>{};
/* EVERY image never loads */
S.Image=function(){ const o={__isImg:true, complete:true, naturalWidth:0, naturalHeight:0, __broken:true};
  Object.defineProperty(o,'__src',{value:'',writable:true});
  Object.defineProperty(o,'src',{set(v){ o.__src=String(v); },get(){return o.__src;}}); return o; };
S.Audio=function(){ return {play:()=>Promise.resolve(),pause(){},load(){},addEventListener(){},currentTime:0,volume:1,muted:false}; };
S.AudioContext=function(){ throw new Error('no audio'); };
S.webkitAudioContext=S.AudioContext;
S.localStorage={getItem:()=>null,setItem(){},removeItem(){},clear(){}};
S.navigator={userAgent:'node',maxTouchPoints:0,getGamepads:()=>[]};
S.location={href:'file:///x'}; S.performance={now:()=>Date.now()};
S.requestAnimationFrame=()=>0; S.cancelAnimationFrame=()=>{};
S.setTimeout=setTimeout; S.clearTimeout=clearTimeout; S.setInterval=()=>0; S.clearInterval=()=>{};
S.devicePixelRatio=1; S.matchMedia=()=>({matches:false,addEventListener(){}});
vm.createContext(S);
for(const f of ['assets/manifest.js','assets/game.js']){
  try{ vm.runInContext(fs.readFileSync(f,'utf8'), S, {filename:f}); }
  catch(e){ console.log('*** '+f+' THREW: '+e.message); process.exit(1); }
}
vm.runInContext("drawBoot._started=true; drawBoot._ct=99; setState(GS.TITLE);", S);
/* tag every image the loader hands out, so a failure names its own key */
vm.runInContext("(function(){ var g=XART.get, r=XART.raw, s=XART.safe; globalThis.__lastKey='-';\
  XART.get=function(k){ __lastKey=k; return g(k); };\
  if(r) XART.raw=function(k){ __lastKey=k+'(raw)'; return r(k); };\
  if(s) XART.safe=function(k){ __lastKey=k+'(safe)'; return s(k); };\
})();", S);
let now=1000;
for(let i=0;i<240;i++){ now+=16.7; try{ vm.runInContext('loop('+now+');', S); }catch(e){ thrown.push('LOOP: '+e.message); } }
console.log('frames run          : 240');
console.log('drawImage calls     :', drawCalls);
console.log('drawImage BAD arg   :', drawImageBad, drawImageBad===0?'  <-- none: the blank placeholder is doing its job':'  <-- STILL PASSING NULL');
const img=thrown.filter(t=>/drawImage|HTMLImageElement/.test(t)).length;
console.log('HTMLImageElement err:', img);
console.log('total logged errors :', thrown.length);
console.log();
console.log('WHAT drawImage WAS HANDED:');
tags.forEach(function(t){ console.log('   '+t); });
console.log('state after 240f    :', vm.runInContext('String(state)', S));
console.log();
console.log('CALLER OF THE FIRST BROKEN drawImage:');
console.log(firstStack.split('\n').slice(1,8).map(l=>'   '+l.trim()).join('\n'));
