'use strict';
/* Non-strip cinematic windows. The native dialogue owner keeps its typewriter,
   full-text fitting, transforms, controls and continuation. Artwork is tiled 1:1. */
const CX4={version:1,revision:2,last:null,base:dlgBox,caption:inv20Text,active:null};
for(const a of Object.values(CX4_ART.banks)){XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);XART.rdy(a.key);}
function cx4Pilot(o){const p=String(o.portrait||o.who||'').toLowerCase();return o.portrait!==false&&CX4_ART.pilots.includes(p)?p:null;}
function cx4Role(o){
 if(CX4_ART.styles.includes(o.cinematicStyle))return o.cinematicStyle;
 const who=String(o.who||'').toLowerCase();
 if(/chronos|dracodia|symbiote|lord of shadows|vile existence|unknown|hostile/.test(who))return 'hostile';
 if(!who||/narrat|caption|system|recorder/.test(who))return 'narration';
 if(/command|control|fury hq|headquarters/.test(who)||(who==='decker'&&[GS.LAUNCH,GS.COCKPIT,GS.CAMPAIGNINTRO].includes(state)))return 'command';
 return 'crew';
}
function cx4Eligible(o){
 if(o.cinematic===false)return false;
 if(o.cinematic===true)return true;
 return [GS.CAMPAIGNINTRO,GS.CUTSCENE,GS.LAUNCH,GS.COCKPIT,GS.VICTORY,GS.WARPENTRY,GS.OPENING,GS.OUTBOUND,GS.FLYOVER,GS.RIVAL,GS.RIVALALLY,GS.RIFTFALLBACK].includes(state)||
  (state===GS.PLAY&&((typeof story!=='undefined'&&!!story)||(typeof s6Opening!=='undefined'&&!!s6Opening?.radio)||
   (typeof fb2IntroActive==='function'&&fb2IntroActive())||(typeof fb2TalkActive==='function'&&fb2TalkActive())));
}
function cx4Frame(style,x,y,w,h,pk){
 const name=style==='crew'?'crew-'+(pk||'cole'):style,a=CX4_ART.banks['frame-'+name+(w<648?'-compact':'')];
 if(!a||w<a.minWidth||!XART.rdy(a.key))return false;
 const im=XART.get(a.key),p=a.parts;
 const blit=(key,dx,dy,cw,ch)=>{const r=p[key];ctx.drawImage(im,r[0],r[1],cw??r[2],ch??r[3],Math.round(dx),Math.round(dy),cw??r[2],ch??r[3]);};
 const tile=(key,dx,dy,tw,th)=>{const r=p[key];for(let yy=0;yy<th;yy+=r[3])for(let xx=0;xx<tw;xx+=r[2])blit(key,dx+xx,dy+yy,Math.min(r[2],tw-xx),Math.min(r[3],th-yy));};
 ctx.save();ctx.imageSmoothingEnabled=false;
 const top=a.header,bottom=a.bottom,edge=p.l[2],left=p.tl[2],right=p.tr[2];
 tile('c',x+edge,y+top,w-edge*2,h-top-bottom);tile('l',x,y+top,edge,h-top-bottom);tile('r',x+w-edge,y+top,edge,h-top-bottom);
 blit('tl',x,y);tile('tc',x+left,y,w-left-right,top);blit('tr',x+w-right,y);
 if(p.badge)blit('badge',x+(w-p.badge[2])/2,y);
 blit('bl',x,y+h-bottom);tile('bc',x+p.bl[2],y+h-bottom,w-p.bl[2]-p.br[2],bottom);blit('br',x+w-p.br[2],y+h-bottom);
 ctx.restore();return true;
}
function cx4Draw(o){
 if(!o||!cx4Eligible(o))return CX4.base.apply(this,arguments);
 const pk=cx4Pilot(o),role=cx4Role(o),record={role,pilot:pk,frame:null,portrait:null,full:o.full||'',budget:0};
 const wide=(o.pw||((state===GS.CUTSCENE||state===GS.CAMPAIGNINTRO)?cutsceneViewWidth():VW)-20)>=648;
 const frameKey=CX4_ART.banks['frame-'+(role==='crew'?'crew-'+(pk||'cole'):role)+(wide?'':'-compact')].key;
 if(!XART.rdy(frameKey)||(pk&&!XART.rdy(CX4_ART.banks['face-'+pk+'-64'].key)))return CX4.base.apply(this,arguments);
 const panel=ui20Panel,contents=ui20PanelContents,comm=commPortrait,width=cd27Width,height=CD27.height;
 let pose=0;
 CX4.active=record;
 try{
  CD27.height=o.ph||(state===GS.PLAY?148:172);
  cd27Width=function(available){return Math.min(available,o.pw||available);};
  ui20Panel=function(who,x,y,w,h,port){
   if(!cx4Frame(role,x,y,w,h,pk))return panel.apply(this,arguments);
   record.frame={x,y,w,h};
   const k=w<648?.5:1,bay=pk?clamp(Math.round(w*.13),76,106):port?76:0,top=64*k,bottom=22*k;
   return {cx4:true,k,x,y,w,h,bw:bay,bay,name:{x:x+44*k,y:y+12*k,w:260*k,h:30*k},
    text:{x:x+(bay?bay+38*k:30*k),y:y+top+6,w:w-(bay?bay+68*k:60*k),h:h-top-6-bottom},
    portraitRect:bay?{x:x+24*k,y:y+top,w:bay-4,h:h-top-16*k}:null};
  };
  commPortrait=function(p,emotion){
   if(!CX4_ART.pilots.includes(p))return comm.apply(this,arguments);
   const count=Math.floor(dlgBox._tw?.count||0),full=String(o.full||'');
   pose=count>0&&count<full.length?[1,2,3,4,5,6,2,1][Math.floor(count/2)%8]:0;
   return CX4_ART.banks['face-'+p+'-64'].key;
  };
  ui20PanelContents=function(who,full,shown,port,r){
   if(!r?.cx4)return contents.apply(this,arguments);
   let portraitDraw=null;
   if(pk&&port){
    const count=Math.floor(dlgBox._tw?.count||0);pose=count>0&&count<full.length?[1,2,3,4,5,6,2,1][Math.floor(count/2)%8]:0;
    const f=r,k=r.k,bay=r.bay,room=f.h-82*k,size=bay>=96&&room>=96?96:bay>=84&&room>=84?84:room>=64?64:48;
    let a=CX4_ART.banks['face-'+pk+'-'+size];if(!XART.rdy(a.key))a=CX4_ART.banks['face-'+pk+'-64'];
    const n=a.size,bottom=f.y+f.h-18*k,baseline=a.baselines[pose],x=Math.round(f.x+16*k+(bay-n)/2),y=Math.round(bottom-baseline+2);
    ctx.save();ctx.beginPath();ctx.rect(r.portraitRect.x,r.portraitRect.y,r.portraitRect.w,r.portraitRect.h);ctx.clip();
    ctx.drawImage(XART.get(a.key),0,pose*n,n,n,x,y,n,n);ctx.restore();
    portraitDraw={x,y,w:n,h:n,key:a.key};record.portrait={pilot:pk,pose,size:n,x,y,baseline,bottom,bleed:2};
   }
   else if(port)portraitDraw=ui20Portrait(ctx,port,r.portraitRect);
   const nh=msgFitH(who,250*r.k,r.k===1?14:10,7);msgText(who,r.x+194*r.k,r.y+34*r.k,nh,'#edf4ff',1,1,0);
   const t=r.text,fit=msgBlockLayout(full,t.w,t.h,r.k===1?14:12,9,1.25);
   const page=fit.height<=t.h?{text:full,budget:shown,H:fit.H,index:0,count:1}:cd27Page(who,full,shown,r,11);
   const layout=msgDrawBlock({text:page.text,budget:page.budget,x:t.x,y:t.y,w:t.w,h:t.h,maxH:page.H,minH:page.H,lineMul:1.25,color:'#fff9eb',alpha:1,outline:false,align:'center',stableCenter:true,valign:'middle'});
   record.budget=shown;record.page={index:page.index,count:page.count,text:page.text};record.layout=layout;
   return {portrait:port,portraitDraw,name:r.name,text:t,portraitRect:r.portraitRect,layout,page:record.page};
  };
  return CX4.base.call(this,o);
 }finally{
  ui20Panel=panel;ui20PanelContents=contents;commPortrait=comm;cd27Width=width;CD27.height=height;
  CX4.last=record;CX4.active=null;
 }
}
Object.assign(cx4Draw,dlgBox);dlgBox=cx4Draw;
inv20Text=function(who,text,W,H,shown=String(text).length,alpha=1){
 if(!cx4Eligible({}))return CX4.caption.apply(this,arguments);
 const w=Math.min(W-20,872),h=W>=496?152:132,p=UI20.pilot(who);
 cx4Draw({who,full:String(text),shown:String(text).slice(0,shown),forceShown:true,fade:alpha,
  portrait:p?p.key:false,portraitKey:/DRACODIA/i.test(who)?DP20.key:undefined,
  pw:w,ph:h,x:Math.round((W-w)/2),y:H-h-10,screenSpace:false,cinematic:true});
 INV20.caption={who,text,x:CX4.last?.frame?.x,y:CX4.last?.frame?.y,w,h,shown,...UI20.dialogue};
};
window.BOF_CINEMATIC_DIALOGUE_1111={version:1,styles:CX4_ART.styles,draw:cx4Draw,last:()=>CX4.last};
