"use strict";
/* A living satellite infection, followed by a code takeover of the screen.
   Load before homecoming so its next-scene fade captures this renderer. */
const SV10={base:{keys:victoryEndingKeys,load:stageLoadBegin},last:null,draws:{},events:[],
 codeGlyphs:{},
 times:{close:2.20,latch:3.0,corrupt:5.80,screen:8.60,transmit:12.40,fade:15.55,end:16.40}};
for(const bank of Object.values(SV10_ART))for(const a of bank)XART._src[a.key]=a.path;
function sv10Assets(){return [...SV10_ART.background,...SV10_ART.detail,...SV10_ART.crawl,...SV10_ART.contact,
 ...HC10_ART.infection,...HC10_ART.infected_detail];}
function sv10Warm(){let ready=true;for(const a of sv10Assets())if(!XART.rdy(a.key))ready=false;return ready;}
victoryEndingKeys=function(){
 const retired=new Set(['cinend_satellite_dish','cinend_symbiote_survivor','cinend_hq_restored',
  cinShipKey(typeof _pilotKey==='function'?_pilotKey():'axel',victoryRearView())]);
 return [...SV10.base.keys.apply(this,arguments).filter(k=>!retired.has(k)),...sv10Assets().map(a=>a.key)];
};
stageLoadBegin=function(n,keys){return SV10.base.load.call(this,n,[...(keys||[]),...(n>=7?sv10Assets().map(a=>a.key):[])]);};
// Resizing an active ending also updates the native cinematic viewport,
// otherwise CSS can stretch the freshly generated art after a window resize.
if(typeof window.addEventListener==='function')window.addEventListener('resize',()=>{
 if(state===GS.VICTORY)_setCinematicViewport(true);
});
function sv10Ease(q){q=clamp(q,0,1);return q*q*(3-2*q);}
function sv10Sample(q){
 const T=SV10.times,s={q,phase:q<T.close?'wide-crawl':q<T.latch?'close-crawl':q<T.corrupt?'infection':q<T.screen?'corruption':q<T.fade?'virus':'fade',
  background:q>=T.close?'detail':'background',bank:q<T.latch?'crawl':'infection',frame:Math.floor(Math.max(0,q)*24)%32,
  corruption:sv10Ease((q-3.7)/4.7),code:sv10Ease((q-T.corrupt)/6.0)};
 if(s.bank==='infection')s.frame=q<T.corrupt?Math.min(31,Math.floor((q-T.latch)/(T.corrupt-T.latch)*32)):
  16+Math.floor((q-T.corrupt)*24)%16;
 return s;
}
function sv10Cell(bank,f,x,y,width,alpha=1){
 const a=SV10_ART[bank]?.[f];if(!a||!XART.rdy(a.key))return false;
 const k=width/a.w;ctx.save();ctx.globalAlpha=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 SV10.draws[a.key]=(SV10.draws[a.key]||0)+1;return true;
}
function sv10Plate(bank,W,H,focus,zoom=1){
 const a=SV10_ART[bank][0],c=a.content_rect,k=Math.max(W/c[2],H/c[3])*zoom,
  w=c[2]*k,h=c[3]*k,R={x:clamp(W*.5-focus[0]*w,W-w,0),y:clamp(H*.5-focus[1]*h,H-h,0),w,h,scale:k};
 if(XART.rdy(a.key)){
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),...c,R.x,R.y,w,h);ctx.restore();
  SV10.draws[a.key]=(SV10.draws[a.key]||0)+1;
 }return R;
}
function sv10Sound(q,S){
 const A=S.sv10||(S.sv10={time:Math.max(0,q-1/60),tick:-1,cues:{}}),prev=A.time;
 for(const [cue,at,fn] of [['infection',3.0,'bossWeaponCharge'],['corruption',5.8,'crackle'],['transmit',12.4,'warpGate']])if(q>=at&&!A.cues[cue]){
  A.cues[cue]=true;const f=Audio.SFX?.[fn],played=prev<at&&q-prev<.75;
  if(f&&played)f();SV10.events.push({cue,q,available:!!f,played});
 }
 if(q>=6.2&&q<15.3){const tick=Math.floor((q-6.2)/.36);
  if(tick!==A.tick){const f=Audio.SFX?.blip;if(f&&q-prev<.75)f();A.tick=tick;SV10.events.push({cue:'code',q,available:!!f});}
 }
 A.time=q;if(SV10.events.length>100)SV10.events.splice(0,SV10.events.length-100);
}
function sv10CodeSample(q,W,H){
 const begin=SV10.times.corrupt,cols=Math.max(2,Math.min(7,Math.floor(W/104))),size=Math.max(8,Math.round(H/58)),
  pitch=Math.round(size*1.95),rows=Math.floor((H-20)/pitch),out=[];
 if(q<begin)return out;
 const logs=['SYS.UPLINK=10001001000','MEMORY.WRITE(10001001000)','OVERRIDE::SATELLITE','ROOT.ACCESS=10001001000','PAYLOAD::DRACODIA','SIGNAL.CORRUPTED'];
 for(let c=0;c<cols;c++)for(let r=0;r<rows;r++){
  const born=begin+c*.36+r*.11,chars=Math.floor((q-born)*25);if(chars<=0)continue;
  const text=(r%8===c%8?logs[(c+r)%logs.length]:'10001001000'),width=(W-24)/cols,
   full=text.slice(0,Math.max(11,Math.floor(width/(size*.68)))),shown=full.slice(0,chars),
   active=Math.floor((q-begin)*8+c*3)%rows===r;
  out.push({text:shown,x:12+c*width,y:10+r*pitch+Math.floor((q-born)*7)%pitch,size,
   alpha:active?.98:.30+.42*(.5+.5*Math.sin(q*2.7+c+r*.65)),color:active?'#dbffd7':'#64ff79'});
 }return out;
}
function sv10CodeDraw(q,W,H){
 const lines=sv10CodeSample(q,W,H);if(!lines.length)return lines;
 if(!bmfReady('dialogue'))return lines;
 const font=BMF.dialogue,space=font.map.glyphs[' '];
 ctx.save();ctx.beginPath();ctx.rect(0,0,W,H);ctx.clip();ctx.imageSmoothingEnabled=false;
 for(const L of lines){
  let pen=L.x;const scale=bmfScale('dialogue',L.size);ctx.globalAlpha=L.alpha;
  for(const ch of L.text){
   const glyph=bmfGlyph(font,ch),r=glyph?.sprite_rect;
   if(r&&r[2]>0){
    const key=L.color+'|'+ch;let image=SV10.codeGlyphs[key];
    if(!image){
     // Palette-map the authored font's bright face and dark bevel together.
     // Multiplication preserves its shade hierarchy and all original alpha;
     // caching avoids re-tinting hundreds of glyphs every cinematic frame.
     image=document.createElement('canvas');image.width=r[2];image.height=r[3];const g=image.getContext('2d');
     g.drawImage(font.img,...r,0,0,r[2],r[3]);g.globalCompositeOperation='multiply';g.fillStyle=L.color;g.fillRect(0,0,r[2],r[3]);
     g.globalCompositeOperation='destination-in';g.drawImage(font.img,...r,0,0,r[2],r[3]);
     SV10.codeGlyphs[key]=image;
    }
    const b=glyph.bounds_in_cell;
    ctx.drawImage(image,Math.round(pen+b[0]*scale),Math.round(L.y+b[1]*scale),Math.max(1,Math.round(r[2]*scale)),Math.max(1,Math.round(r[3]*scale)));
   }
   pen+=((glyph||space)?(glyph||space).x_advance:6)*scale;
  }
 }
 ctx.restore();return lines;
}
victoryDish=function(t,W,H,S){
 const q=Math.max(0,t-VICTORY_DISH_AT),s=sv10Sample(q),T=SV10.times;
 sv10Warm();
 const close=s.background==='detail',crawl=sv10Ease(q/T.latch),
  R=sv10Plate(s.background,W,H,close?[.56,.50]:[.71,.38],close?1.04:1+sv10Ease(Math.min(q,T.close)/T.close)*.035);
 let root=null;
 if(s.bank){
  let nx,ny,width;
  if(close){const d=sv10Ease((q-T.close)/(T.latch-T.close));nx=lerp(.47,.55,d);ny=lerp(.56,.48,d);
   width=s.bank==='crawl'?H*lerp(.88,.38,d):Math.min(W*.42,H*.46)*384/HC10_METRICS.infection.body_width;}
  else{nx=lerp(.685,.750,crawl);ny=lerp(.315,.245,crawl);width=H*.40;}
  let x=R.x+nx*R.w,y=R.y+ny*R.h;
  if(s.corruption>0){
   // Generated black roots and green circuitry are registered to the exact
   // same dish plate. The infection reel supplies the moving leading edge.
   const a=HC10_ART.infected_detail[0];if(XART.rdy(a.key)){
    ctx.save();ctx.globalAlpha=s.corruption;ctx.drawImage(XART.get(a.key),...a.content_rect,R.x,R.y,R.w,R.h);ctx.restore();
    HC10.draws[a.key]=(HC10.draws[a.key]||0)+1;
   }
  }
  if(q>=T.latch){
   const ef=Math.floor((q-T.latch)*24)%16;sv10Cell('contact',ef,x,y,Math.min(W*.34,H*.37));s.effectFrame=ef;
   s.roots=[];
   // Fixed seams and equipment sockets on the same concave dish plate.
   // Small authored roots latch in succession, spreading over the hardware.
   for(const [rx,ry,scale,delay] of [[.36,.60,.36,1.1],[.78,.58,.33,1.8],[.66,.29,.28,2.4],
    [.30,.35,.31,3.0],[.86,.32,.27,3.6],[.24,.79,.35,4.2]]){
    const age=q-T.latch-delay;if(age<0)continue;
    const frame=age<2.8?Math.min(31,Math.floor(age/2.8*32)):16+Math.floor(age*24)%16,
     root={x:R.x+rx*R.w,y:R.y+ry*R.h,width:width*scale,frame};
    hc10Cell('infection',frame,root.x,root.y,root.width);s.roots.push(root);
   }
   hc10Cell(s.bank,s.frame,x,y,width);
  }else sv10Cell(s.bank,s.frame,x,y,width);
  root={x,y,width};
 }
 if(q<4.65){
  const a=Math.min(clamp(q/.32,0,1),clamp((4.65-q)/.38,0,1));
  victoryCaption('THE FINAL BATTLE WAS OVER...','But a piece of the alien symbiote survived. Hidden. Watching. Waiting.',W,H,a);
 }
 if(s.code>0){ctx.save();ctx.globalAlpha=s.code*.56;ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.restore();}
 const codeLines=sv10CodeDraw(q,W,H),fade=sv10Ease((q-T.fade)/.70);
 if(fade>0){ctx.save();ctx.globalAlpha=fade;ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.restore();}
 SV10.last={...s,rect:R,root,fade,codeLines};sv10Sound(q,S);
};
