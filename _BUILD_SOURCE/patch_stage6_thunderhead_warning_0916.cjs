const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');
const one=(a,b,label)=>{const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);};
if(!s.includes("stage6-thunderhead-0")){
  one("  M.thunderhead={t:0,tell:.66,wave:0,waves:4,next:.66,gap:start,cols:cols};",
    "  const rowTell=.66;M.thunderhead={t:0,rowTell:rowTell,wave:0,waves:4,next:rowTell,warnAt:0,gap:start,cols:cols,finishAt:0};",
    'Thunderhead row state');
  one("  M.cd=2.1;b.fireCd=Math.max(b.fireCd||0,2.1);b.flash=Math.max(b.flash||0,.42);",
    "  M.cd=2.1;b.fireCd=Math.max(b.fireCd||0,2.1);b.flash=Math.max(b.flash||0,.42);\n  combatWarningTick(b,'stage6-thunderhead-0',0,rowTell,true);",
    'Thunderhead first warning');
  one("  const M=b&&b._mega,T=M&&M.thunderhead;if(!T)return false;T.t+=dt;\n  if(T.t>=T.next&&T.wave<T.waves){",
    "  const M=b&&b._mega,T=M&&M.thunderhead;if(!T)return false;T.t+=dt;\n  if(T.wave<T.waves){const elapsed=Math.max(0,T.t-T.warnAt);\n    combatWarningTick(b,'stage6-thunderhead-'+T.wave,Math.min(elapsed,T.rowTell),T.rowTell);}\n  if(T.t>=T.next&&T.wave<T.waves){",
    'Thunderhead warning tick');
  one("    T.wave++;T.gap=clamp(T.gap+(T.wave&1?1:-1),0,T.cols-2);T.next+=.34;",
    "    T.wave++;\n    if(T.wave<T.waves){\n      T.gap=clamp(T.gap+(T.wave&1?1:-1),0,T.cols-2);T.warnAt=T.t;T.next=T.t+T.rowTell;\n      combatWarningTick(b,'stage6-thunderhead-'+T.wave,0,T.rowTell,true);\n    }else T.finishAt=T.t+.48;",
    'Thunderhead next row');
  one("  if(T.wave>=T.waves&&T.t>T.next+.48){M.thunderhead=null;M.cd=.72;return false;}",
    "  if(T.wave>=T.waves&&T.t>T.finishAt){M.thunderhead=null;M.cd=.72;return false;}",
    'Thunderhead finish');
  one(`function carrierThunderheadDraw(b){
  const M=b&&b._mega,T=M&&M.thunderhead;if(!T||T.t>=T.tell)return;
  const W=worldWidth(),cw=W/T.cols,pulse=.28+.20*Math.sin(T.t*22);
  ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<T.cols;i++){
    if(i===T.gap||i===T.gap+1)continue;
    ctx.globalAlpha=pulse;ctx.fillStyle='#67dcff';ctx.fillRect(i*cw+cw*.38,PLAY.y,cw*.24,VH-PLAY.y);
    ctx.globalAlpha=.85;ctx.fillStyle='#eaffff';ctx.fillRect(i*cw+cw*.49,PLAY.y,cw*.035,VH-PLAY.y);
  }
  ctx.globalAlpha=.82;ctx.strokeStyle='#9bffdb';ctx.lineWidth=2;
  ctx.strokeRect(T.gap*cw+3,PLAY.y+3,cw*2-6,VH-PLAY.y-6);ctx.restore();
}`,
`function carrierThunderheadDraw(b,front){
  const M=b&&b._mega,T=M&&M.thunderhead;if(!T||T.wave>=T.waves||T.t>=T.next)return false;
  const W=worldWidth(),cw=W/T.cols,k=clamp((T.t-T.warnAt)/T.rowTell,0,1),top=(typeof viewTopY==='function'?viewTopY():0)+18;
  if(!front){for(let i=0;i<T.cols;i++)if(i!==T.gap&&i!==T.gap+1){const x=(i+.5)*cw;
    combatWarningDraw(b,{x:x,y:top,ex:x,ey:VH+40,progress:k,width:Math.max(24,cw*.52),fieldOnly:true});}}
  else{const p=shipBossMount(b,'C');combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH+40,progress:k,alertOnly:true,alertX:b.x,alertY:48});}
  return true;
}`,'Thunderhead shared draw');
  one("  carrierThunderheadDraw(b);","  carrierThunderheadDraw(b,false);",'Thunderhead field layer');
  one("    const r=clamp(n.hp/n.maxhp,0,1);ctx.fillStyle='#06111c';ctx.fillRect(p.x-21,p.y+26,42,4);ctx.fillStyle='#54e8ff';ctx.fillRect(p.x-20,p.y+27,40*r,2);\n  }\n}",
    "    const r=clamp(n.hp/n.maxhp,0,1);ctx.fillStyle='#06111c';ctx.fillRect(p.x-21,p.y+26,42,4);ctx.fillStyle='#54e8ff';ctx.fillRect(p.x-20,p.y+27,40*r,2);\n  }\n  carrierThunderheadDraw(b,true);\n}",
    'Thunderhead alert layer');
  fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE6_THUNDERHEAD_WARNING_0916');
}else console.log('STAGE6_THUNDERHEAD_WARNING_0916_PRESENT');
