"use strict";
/* LP116: source-preserving, authored gray/black locked Cole frames.
   Native unlock/password/save/selection owners remain authoritative. */
const LP116={banks:LOCKED_PILOT_ART_1106.banks,seconds:.45,draws:0,lastCard:null,lastMini:null};
for(const a of Object.values(LP116.banks))XART._src[a.key]=a.path;
function lp116Warm(){for(const a of Object.values(LP116.banks))XART.rdy(a.key);}
function lp116Phase(){return Math.floor(Math.max(0,stateT||0)/LP116.seconds)%2;}
function lp116LockedScreen(){return state===GS.PILOT&&isPilotLocked(PILOTS[pilotRot>.5?pilotFrom:pilotIndex]);}
function lp116Background(){return lp116Phase()===0?'#000000':'#484848';}
function lp116Panel(){return lp116Phase()===0?'#181818':'#686868';}
function lp116Blit(id,cx,cy,phase=lp116Phase()){
 const a=LP116.banks[id];if(!a||!XART.rdy(a.key))return null;
 const x=Math.round(cx-a.w/2),y=Math.round(cy-a.h/2);
 ctx.drawImage(XART.get(a.key),phase*a.w,0,a.w,a.h,x,y,a.w,a.h);
 LP116.draws++;
 return {id,phase,x,y,w:a.w,h:a.h};
}
function lp116Label(text,cx,cy,width,height=12,color='#b8b8b8'){
 const h=pcFontFit(text,width,height,7),w=pcFontMeasure(text,h);
 pcFontLeft(text,Math.round(cx-w/2),Math.round(cy),h,color,1);
}
function lockedPilotCard116(P,PX,PY,PW,PH){
 const wide=PW>560,pad=12,bodyW=PW*(wide?.28:.38),shipW=wide?PW*.29:PW-bodyW-pad*2;
 const by=PY+32,bh=PH-44,bx=PX+pad,sx=bx+bodyW+pad;
 const shipH=wide?bh*.82:Math.min(bh*.39,190),shipY=by+shipH/2;
 const infoX=wide?sx+shipW+pad:sx,infoY=wide?by:by+shipH+10;
 const infoW=PX+PW-pad-infoX,infoH=PY+PH-pad-infoY,phase=lp116Phase();
 pilotNameDraw('LOCKED PILOT',PX+PW/2,PY+17,20,'#b8b8b8',1);
 const body=lp116Blit('pilot_large',bx+bodyW/2,by+bh/2,phase);
 const ship=lp116Blit(wide?'ship_large':'ship_small',sx+shipW/2,shipY,phase);
 const lockSize=wide?64:48,lockY=infoY+(wide?infoH*.32:lockSize/2);
 const lock=lp116Blit('lock_'+lockSize,infoX+infoW/2,lockY,phase);
 const labelY=lockY+lockSize/2+18;
 lp116Label('LOCKED',infoX+infoW/2,labelY,infoW,16);
 lp116Label('PASSWORD REQUIRED',infoX+infoW/2,labelY+23,infoW,10);
 LP116.lastCard={pilot:P.key,phase,body,ship,lock,box:[PX,PY,PW,PH]};
 PT11_UI.card={pilot:P.key,locked:true,body:[bx,by,bodyW,bh],ship:[sx,by,shipW,shipH],info:[infoX,infoY,infoW,infoH]};
}
function lockedPilotMini116(kind,x,y,size){
 const n=[64,56,48,44,40,32].find(n=>n<=size-4)||32,phase=lp116Phase();
 const shape=lp116Blit(kind+'_mini_'+n,x+size/2,y+size/2,phase);
 const lock=lp116Blit('lock_12',x+size-8,y+8,phase);
 LP116.lastMini={kind,phase,shape,lock};
}
const LP116_WARM=pilotSelectWarm;
pilotSelectWarm=function(){lp116Warm();return LP116_WARM.apply(this,arguments);};
lp116Warm();
globalThis.BOF_LOCKED_PILOT_1106=LP116;
