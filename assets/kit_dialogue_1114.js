"use strict";
/* KD18: one native hardware assembly, code-only relay corruption, and one
   proportional metal radio plate. Native dialogue/input/audio clocks stay owners. */
const KD18={base:{dlg:dlgBox,load:stageLoadBegin,keys:d1110Keys,visual:d1110Visual},last:null,radio:null,plates:new Map(),history:[]};
const KD18_SAT={key:'kd18_satellite',path:'assets/game/shared/cinematics/kit_dialogue_1114/satellite-code.webp',w:418,h:236,cols:4,frames:16};
XART._src[KD18_SAT.key]=KD18_SAT.path;
function kd18Warm(){XART.rdy(KD18_SAT.key);XART.rdy('cd27_neutral_460');for(const p of PILOTS)XART.rdy('pav_'+p.key);for(const k of ['voss','nyx','rook','kaia','jace'])XART.rdy('rr_portrait_'+k);XART.rdy(DP20.key);XART.rdy(c113Compact('neutral',68));}
kd18Warm();
stageLoadBegin=function(n,keys){return KD18.base.load.call(this,n,[...new Set([...(keys||[]),KD18_SAT.key,'cd27_neutral_460',...PILOTS.map(p=>'pav_'+p.key)])]);};
d1110Keys=function(){return [...new Set([...KD18.base.keys.apply(this,arguments),KD18_SAT.key])];};
// Retire every legacy satellite illustration at registration, including context
// inserts. Keep their layouts but replace ALL cells with code-only native crops.
function kd18RetireSatellite(bank){if(!bank)return;Object.assign(bank,{...KD18_SAT,key:bank.key});XART._src[bank.key]=KD18_SAT.path;}
kd18RetireSatellite(KD17_ART.banks.satellite);
kd18RetireSatellite(D1110_ART.banks['satellite-takeover']);
kd18RetireSatellite(C16_ART.banks['art-satellite-takeover']);
const kd18Retired=new Set(['kd17_satellite','d1110_satellite-takeover','c16_art-satellite-takeover']);
const kd18Get=XART.get.bind(XART),kd18Ready=XART.rdy.bind(XART);
XART.get=function(k){return kd18Get(kd18Retired.has(k)?KD18_SAT.key:k);};
XART.rdy=function(k){return kd18Ready(kd18Retired.has(k)?KD18_SAT.key:k);};
function kd18SatelliteFrame(t){return t<.45?0:t<2.45?Math.min(15,Math.floor((t-.45)*8)):12+Math.floor((t-2.45)*12)%4;}
function kd18Satellite(box,t){if(!XART.rdy(KD18_SAT.key))return false;const a=KD18_SAT,f=kd18SatelliteFrame(t),[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k;
 ctx.drawImage(XART.get(a.key),f%4*a.w,Math.floor(f/4)*a.h,a.w,a.h,Math.round(x+(w-dw)/2),Math.round(y+(h-dh)/2),dw,dh);
 KD18.last={mode:'satellite',key:a.key,frame:f,time:t,codeOnly:true,singlePanel:true,dialogueBox:false};return true;}
d1110Visual=function(b,s){if(b.kit17!=='satellite')return KD18.base.visual.apply(this,arguments);
 const box=[12,12,888,488];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#080d14';ctx.fillRect(0,0,912,512);
 c16Clip(box,()=>kd18Satellite(box,Math.max(0,s.t)));sl14Frame(box);msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],730,505,887,9);msgFaceUse(null);ctx.restore();
 KD17.last=D1110.last={...KD18.last,shot:b.id,pilot:run.pilot,caption:false};};
// Use the cinematic clock for both hull exhaust pixels and the extended plume.
// XART's ordinary ship getter otherwise follows the idle combat clock here.
pt11OpeningShip=function(pk,t,x,y,h,power){
 const base='ship_'+pk,ph=SHIP_GLOW_SEQ[Math.floor(t*1000/SHIP_GLOW_MS)%SHIP_GLOW_SEQ.length],key=ph&&BOFX.ships?.[base+'_'+ph]?base+'_'+ph:base;
 if(!XART.rdy(key))return false;const frame=Math.floor(t*1000/55),im=d27ShipFrame(key,frame)||XART.get(key),w=h*im.width/im.height;
 const pulse=[.76,.88,1,.92,.8,.96,.86,1][frame%8],burn=clamp((power??.62)*pulse,0,1),previous=player._thrustFrame;
 let plume=false;player._thrustFrame=frame;try{plume=pf27PlaneThrustDraw(ctx,key,x,y,w,h,burn);}finally{player._thrustFrame=previous;}
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();
 PT11_UI.ship={pilot:pk,key,x,y,w,h,power:burn,plume,thrustFrame:frame};return true;};
function kd18Material(o){const s=String(o.who||'')+' '+String(o.portraitKey||'');
 if(/chronos|chronus|cronos/i.test(s))return 'chronos';
 if(/dracodia|symbiote|lord of shadows|vile existence/i.test(s))return 'dracodia';
 if(/rook|kaia|voss|nyx|jace|spectre|specter|rebel|rival|rough rider/i.test(s)||[GS.RIVAL,GS.RIVALALLY].includes(state))return 'rebel';
 return 'crew';}
// Recolor the existing metal's pixels once; apertures, alpha, bolts and all
// luminance detail stay identical. This is the native UI material treatment.
function kd18Plate(material){const key='cd27_neutral_460';if(!XART.rdy(key))return null;if(KD18.plates.has(material))return KD18.plates.get(material);
 const im=XART.get(key),c=document.createElement('canvas');c.width=460;c.height=84;const g=c.getContext('2d');g.drawImage(im,0,0);
 const rgb={rebel:[1.22,.61,.4],dracodia:[1.02,.63,1.4],chronos:[.52,.85,1.4]}[material];
 if(rgb){const d=g.getImageData(0,0,460,84),v=d.data;for(let i=0;i<v.length;i+=4){if(!v[i+3])continue;const r=v[i],b=v[i+2],gr=v[i+1],lum=.2126*r+.7152*gr+.0722*b;
   // Leave amber pilot lamps and the black reading surface readable.
   if(Math.max(r,gr,b)-Math.min(r,gr,b)>50&&r>gr*1.3)continue;
   const mix=lum>190?.46:.86;for(let n=0;n<3;n++)v[i+n]=Math.round(clamp(lum*((1-mix)+rgb[n]*mix),0,255));}
  g.putImageData(d,0,0);}
 KD18.plates.set(material,c);return c;}
function kd18Pilot(o){if(o.portrait===false)return null;return UI20.pilot(o.portrait||o.who)?.key||null;}
function kd18DrawDialogue(o){if(!o)return;const view=CD27.viewport?.w||cd27View(),width=Math.min(view-20,460*(view/VW)),scale=width/460,height=84*scale;
 const material=kd18Material(o),pk=kd18Pilot(o),plate=kd18Plate(material);if(!plate||(pk&&!XART.rdy('pav_'+pk))){kd18Warm();return;}
 const panel=ui20Panel,contents=ui20PanelContents,getWidth=cd27Width,oldHeight=CD27.height;
 const rec={who:o.who,material,pilot:pk,avatar:pk?'pav_'+pk:null,frame:null,page:null};
 try{CD27.height=height;cd27Width=()=>width;
  ui20Panel=function(who,x,y){x=Math.round(clamp((o.x??(view-width)/2),8,view-width-8));y=Math.round(y);
   ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(plate,x,y,width,height);ctx.restore();
   const r={kd18:true,x,y,w:width,h:height,k:scale,name:{x:x+106*scale,y:y+9*scale,w:68*scale,h:14*scale},
    text:{x:x+104*scale,y:y+32*scale,w:338*scale,h:38*scale},portraitRect:{x:x+17*scale,y:y+8*scale,w:68*scale,h:68*scale}};
   rec.frame={x,y,w:width,h:height};CD27.last=r;return r;};
  ui20PanelContents=function(who,full,shown,port,r){if(!r?.kd18)return contents.apply(this,arguments);
   const avatar=pk?'pav_'+pk:port,draw=avatar?ui20Portrait(ctx,avatar,r.portraitRect):null,n=r.name,t=r.text;
   rec.avatar=avatar;rec.portraitDraw=draw;
   ui20Text(ctx,who,n.x+n.w/2,n.y+n.h/2,10*scale,n.w,'center',UI20.color(who));
   // Page at a fixed font and row height, driven by the original letter budget.
   const local={text:{x:0,y:0,w:t.w/scale,h:t.h/scale}},page=cd27Page(who,String(full),shown,local,10);
   const layout=msgDrawBlock({text:page.text,budget:page.budget,x:t.x,y:t.y,w:t.w,h:t.h,maxH:page.H*scale,minH:page.H*scale,lineMul:1.25,color:'#fff9eb',alpha:1,outline:false,align:'center',stableCenter:true,valign:'middle'});
   rec.page={index:page.index,count:page.count,text:page.text,budget:page.budget};rec.layout=layout;
   return {portrait:avatar,portraitDraw:draw,portraitRect:r.portraitRect,name:n,text:t,layout,page:rec.page};};
  const enemy=material==='dracodia'?DP20.key:material==='chronos'?c113Compact(C113.pose||'neutral',68):material==='rebel'?'rr_portrait_'+String(o.who||'').toLowerCase():null;
  const args={...o,cinematic:false,pw:width,ph:height,fixedHeight:true,x:(view-width)/2,portraitKey:pk?'pav_'+pk:o.portraitKey||(enemy&&XART.rdy(enemy)?enemy:undefined)};
  const result=KD18.base.dlg.call(this,args);if(rec.frame&&UI20.dialogue)Object.assign(UI20.dialogue,rec.frame);return result;
 }finally{ui20Panel=panel;ui20PanelContents=contents;cd27Width=getWidth;CD27.height=oldHeight;
  KD18.radio=rec;CX4.last={role:material,pilot:pk,frame:rec.frame,portrait:rec.portraitDraw,budget:dlgBox._tw?.count||0,page:rec.page};
  if(rec.frame){KD18.history.push(rec);if(KD18.history.length>120)KD18.history.shift();}}
}
Object.assign(kd18DrawDialogue,dlgBox);dlgBox=cx4Draw=kd18DrawDialogue;
inv20Text=function(who,text,W,H,shown=String(text).length,alpha=1){
 const old=CD27.viewport;CD27.viewport={w:W,h:H};const p=UI20.pilot(who),w=Math.min(W-20,460*W/VW),h=84*w/460;
 try{kd18DrawDialogue({who,full:String(text),shown:String(text).slice(0,shown),forceShown:true,fade:alpha,portrait:p?p.key:false,
  portraitKey:/DRACODIA/i.test(who)?DP20.key:undefined,pw:w,ph:h,x:(W-w)/2,y:H-h-13,screenSpace:false});
  INV20.caption={who,text,...KD18.radio?.frame,shown,...UI20.dialogue};
 }finally{CD27.viewport=old;}
};
window.BOF_CINEMATIC_DIALOGUE_1111.draw=kd18DrawDialogue;
window.BOF_KIT_DIALOGUE_1114=KD18;
