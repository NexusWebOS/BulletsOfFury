'use strict';
/* Menu-only generated frames. Portrait cinematic plates never enter this owner. */
const MW21={sizes:{s:[384,132],m:[456,196],l:[456,286],xl:[456,366]},last:null};
for(const [n,a] of Object.entries(MW21_ART))XART._src[a.key]=a.path;
function mw21Window(size,x,y,w,h){const a=MW21_ART[size]||MW21_ART.l,key=a.key;
 if(!XART.rdy(key))return null;const im=XART.get(key),k=w/a.w;
 const q=ui20Nine(ctx,im,[0,0,a.w,a.h],x,y,w,h,[64,74,64,32]);
 const header=q.rect(72,24,a.w-144,23),body=q.rect(52,85,a.w-104,a.h-130);
 MW21.last={size,x,y,w,h,header,body,avatar:false};return MW21.last;
}
function mw21Text(text,r,max=14,color='#edf5ff'){
 const face=window.BOF_UI_FACE||'game',words=String(text).toUpperCase().split(/\s+/);let rows=[],size=max;
 for(;size>=9;size--){let line='';rows=[];for(const word of words){const next=line?line+' '+word:word;
  if(line&&bmfMeasure(face,next,size)>r.w){rows.push(line);line=word;}else line=next;}if(line)rows.push(line);
  if(rows.length*size*1.45<=r.h)break;}
 const step=size*1.45,top=r.y+(r.h-rows.length*step)/2+step/2;
 ctx.save();ctx.beginPath();ctx.rect(r.x,r.y,r.w,r.h);ctx.clip();rows.forEach((s,i)=>ui20Text(ctx,s,r.x+r.w/2,top+i*step,size,r.w,'center',color));ctx.restore();
 return {rows,size,rect:{...r}};
}
const mw21Open=tutAskOpen;
tutAskOpen=function(){for(const a of Object.values(MW21_ART))XART.rdy(a.key);const r=mw21Open.apply(this,arguments);if(tutAsk)tutAsk.md=!!Input.mouse.down;return r;};
tutAskDraw=function(dt){const A=tutAsk;if(!A){setState(GS.TITLE);return;}A.t+=dt;
 if(!drawCanonBackdrop('nbt_2',.62)){ctx.fillStyle='#04060b';ctx.fillRect(0,0,VW,VH);}
 ui20Text(ctx,'TRAINING FLIGHT',VW/2,48,24,VW-30,'center','#f2f7ff');
 const w=VW-24,h=286,x=12,y=91,r=mw21Window('l',x,y,w,h);
 if(r){mw21Text('BEFORE YOU DEPLOY',r.header,13,'#ffd47d');
  MW21.prompt=mw21Text('Bullets of Fury mixes Arcade shooter action with Dodge rolls, Lock-On Missile targeting systems, Warning Systems, Special Abilities per Pilot & More. It is STRONGLY recommended you try the tutorial in the exclusive level: Stormglass.',{x:x+38,y:y+65,w:w-76,h:91},13);
  ui20Text(ctx,A.seen?'REFRESH YOUR FLIGHT SKILLS':'RECOMMENDED FOR NEW PILOTS',VW/2,y+169,12,w-64,'center','#ffd47d');
  const rows=['YES - FLY STORMGLASS ACADEMY',run.mode==='campaign'?'NO - START THE CAMPAIGN':'NO - STRAIGHT TO STAGE 1'];
  const moved=Input.consumeMouseMoved(),click=Input.mouse.down&&!A.md;A.md=!!Input.mouse.down;
  for(let i=0;i<2;i++){const cy=y+202+i*36,over=Input.mouse.inside&&Math.abs(Input.mouse.x-VW/2)<w*.42&&Math.abs(Input.mouse.y-cy)<17;
   if(moved&&over)A.sel=i;ui20Text(ctx,rows[i],VW/2+6,cy,A.sel===i?14:12,w-90,'center',A.sel===i?'#ffffff':'#9eacbd');
   if(A.sel===i)drawSelArrow(x+32,cy-4,18,false,'g');if(click&&over&&A.t>.35){tutAskChoose(i);return;}}
 }
 ui20Text(ctx,'ABOUT FOUR MINUTES - SKIP FROM THE PAUSE MENU',VW/2,407,11,VW-36,'center','#a2b4c8');
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM'],['pad_b','BACK']]);
 if(A.t<.35)return;if(Input.menuUp()||Input.menuDown()){A.sel=1-A.sel;Audio.SFX.blip();}
 if(Input.menuConfirm()){tutAskChoose(A.sel);return;}if(Input.menuBack()){tutAsk=null;if(A.prev===GS.PILOT){drawPilot._entered=false;drawPilot._pcFor=null;pilotPending=null;pilotSlide=0;}setState(A.prev||GS.PILOT);}
};
globalThis.BOF_MENU_WINDOWS=MW21;
