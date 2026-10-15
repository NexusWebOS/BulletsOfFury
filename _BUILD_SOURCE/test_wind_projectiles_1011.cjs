'use strict';
module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
 for(const [file,symbol] of [['wind_projectile_painter_1011.js','WP11_FAMILIES'],['wind_projectiles_1011.js','WP11']])
  if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',file),'utf8'),c,{filename:file});
 const report=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={},g={save(){},restore(){},translate(){},rotate(){},beginPath(){},rect(){},clip(){},drawImage(){}};
  const resolve=key=>({key}),samples=[{kind:'mg'},{kind:'spread'},{kind:'missile'},{kind:'beam'},{kind:'flame'},
   {kind:'orb'},{kind:'lasermist'},{kind:'mg',_cal50:true},{kind:'yuriLightningOrb'}];
  out['All nine native carriers select independent Wind reels']=samples.every((b,i)=>wp11Family({...b,_inf:'wind'})===WP11_FAMILIES[i]);
  out['Enemy and ordinary ammunition cannot become Wind from the equipped weapon']=samples.every(b=>wp11Family({...b,_inf:null})===null);
  for(let i=0;i<9;i++){
   const f=WP11_FAMILIES[i],bank=AP10_FX_ART['wind_'+f];
   const b={...samples[i],_inf:'wind',x:120,y:210,top:12,bot:210,w:24,h:24,t:0,_infLv:5,vy:-4};
   const before=JSON.stringify(b),n=wp11Paint(g,bank,resolve,b,1);
   out[f+': authored draws do not alter flight, collision, damage or ammunition']=n>0&&JSON.stringify(b)===before;
  }
  const laser=AP10_FX_ART.wind_laser;
  out['Subpixel Wind beams cannot enter an unbounded tile loop']=wp11Paint(g,laser,resolve,{x:120,top:-1e6,bot:210,w:.01},0)===0;
  out['Invalid Wind beam dimensions fail without drawing']=wp11Paint(g,laser,resolve,{x:120,top:NaN,bot:210,w:24},0)===0;
  const n=wp11Paint(g,laser,resolve,{x:120,top:-1e6,bot:210,w:1},0);
  out['Even an extreme valid beam has a finite draw budget']=n>0&&n<=130;
  const cold=wp11Frame(AP10_FX_ART.wind_bullets,()=>null,1);
  const partial=wp11Frame(AP10_FX_ART.wind_bullets,k=>k.endsWith('_03')?{key:k}:null,1);
  out['Cold reels fall back, and a partly decoded reel keeps its ready frame']=cold===null&&partial?.a.frame===3;
  const poses=new Set();for(let i=0;i<16;i++)poses.add(wp11Frame(AP10_FX_ART.wind_heavy,resolve,(i+.2)/24)?.a.frame);
  out['The flight clock plays all16 genuinely drawn poses']=poses.size===16;
  out['Unlaunched and dead rounds cannot draw Wind trails']=wp11Paint(g,AP10_FX_ART.wind_missile,resolve,{x:120,y:150,_launchDelay:.2},1)===0&&wp11Paint(g,AP10_FX_ART.wind_missile,resolve,{x:120,y:150,dead:true},1)===0;
  return out;
 })())`,c));
 for(const [name,passed] of Object.entries(report))ok(passed,'Wind1011: '+name);
};
