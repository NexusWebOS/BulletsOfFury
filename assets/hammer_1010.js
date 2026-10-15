"use strict";
/* Mike 1010: depth-safe committed Hammer, authored Chromium and side swings.
   The encounter's armor/recovery/HP owners remain authoritative. */
const HM10={version:1,bodyScale:.70,events:[],draws:{},drawing:null,base:{init:hammerBossInit,tick:hammerBossTick,draw:hammerBossDraw,
 moduleBreak:hammerBossModuleBreak,activation:repair30ChromiumActivationDraw,stormDraw:hammerStormDraw,
 counterHead:bm9CounterHead,spikeShape:hammerStormSpikeShape,spikeDraw:hammerStormSpikeDraw,
 cell:fr27Cell,effect:archEffectBlit,load:stageLoadBegin}};
for(const bank of Object.values(HM10_ART))for(const a of bank)XART._src[a.key]=a.path;
function hm10Log(event,data={}){HM10.events.push({event,...data});if(HM10.events.length>160)HM10.events.shift();}
function hm10Warm(){for(const bank of Object.values(HM10_ART))for(const a of bank)XART.rdy(a.key);}
function hm10Ready(){return Object.values(HM10_ART).every(bank=>bank.every(a=>XART.rdy(a.key)));}
stageLoadBegin=function(n,keys){return HM10.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?Object.values(HM10_ART).flat().map(a=>a.key):[])]);};
hammerBossInit=function(b){const r=HM10.base.init.apply(this,arguments);b._hammer.hm10={age:0,wallAge:0,wallOn:false,wallBreak:99,hits:[]};hm10Warm();return r;};
function hm10Data(b){return b._hammer.hm10||(b._hammer.hm10={age:0,wallAge:0,wallOn:false,wallBreak:99,hits:[]});}
function hm10Blit(name,f,x,y,k=1,flash=0){
 const a=HM10_ART[name][clamp(f|0,0,15)];if(!XART.rdy(a.key))return false;
 const im=flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,Math.round(x-a.pivot[0]*k),Math.round(y-a.pivot[1]*k),a.w*k,a.h*k);ctx.restore();
 HM10.draws[name]=(HM10.draws[name]||0)+1;return true;
}
function hm10ShieldImpact(b,x,y){hm10Data(b).hits.push({x,y,t:0});if(hm10Data(b).hits.length>12)hm10Data(b).hits.shift();}
hammerBossModuleBreak=function(b,which){
 if(which==='hammer'&&hammerStrikeCommitted(b)){
  b._hammer.hm10BreakPending=true;b._hammer.hammerHP=0;markHit(b);hm10Log('hammer-break-queued',{state:b._hammer.state});return;
 }
 return HM10.base.moduleBreak.apply(this,arguments);
};
function hm10WallActive(b){const h=b._hammer,A=fr27Armor(b);return !!(A?.barrier>0||h.state==='shield'||h.state==='fr_activation');}
hammerBossTick=function(b,dt){
 const h=b._hammer,Q=hm10Data(b),previous=h.state;Q.age+=dt;Q.wallBreak+=dt;
 Q.hits=Q.hits.filter(q=>(q.t+=dt)<.30);
 const r=HM10.base.tick.apply(this,arguments),active=hm10WallActive(b);
 if(active){Q.wallAge=Q.wallOn?Q.wallAge+dt:0;Q.wallOn=true;}
 else if(Q.wallOn){Q.wallOn=false;Q.wallBreak=0;hm10Log('shield-shatter',{state:h.state});}
 if(h.hm10BreakPending&&!hammerStrikeCommitted(b)&&!b.dead){
  h.hm10BreakPending=false;HM10.base.moduleBreak(b,'hammer');hm10Log('hammer-break-after-strike',{state:previous});
 }
 if(previous==='giant_dive'&&h.state==='giant_sweep')hm10Log('orbital-strike-landed',{x:b.x,y:b.y,scale:hammerDepthScale(b)});
 return r;
};
repair30ChromiumActivationDraw=function(b){
 const f=Math.min(15,Math.floor(clamp(b._hammer.t/FR27_ACT.end,0,.9999)*16));
 if(!hm10Blit('shield_form',f,b.x,b.y,HM10.bodyScale,b.flash||0))return HM10.base.activation.apply(this,arguments);
 return true;
};
// Suppress only the superseded Hammer wall and core effects while its own draw runs.
fr27Cell=function(key,col,row){if(HM10.drawing&&key==='fr27_chromium_actions'&&row===3)return true;return HM10.base.cell.apply(this,arguments);};
archEffectBlit=function(cell,x,y,size,rot,alpha){
 const b=HM10.drawing;if(b&&cell===9&&x===b.x&&y===b.y&&fr27Armor(b)?.hp>0&&alpha===.7)return true;
 return HM10.base.effect.apply(this,arguments);
};
function hm10WallDraw(b){const Q=hm10Data(b);let f;
 if(Q.wallOn||hm10WallActive(b)){f=Q.wallAge<.65?Math.min(7,Math.floor(Q.wallAge/.65*8)):8+(Math.floor((Q.wallAge-.65)*12)%4);}
 else if(Q.wallBreak<.55)f=12+Math.min(3,Math.floor(Q.wallBreak/.55*4));else return;
 hm10Blit('shield_wall',f,b.x,b.y+85,.78,fr27Armor(b)?.flash||0);
 for(const q of Q.hits)hm10Blit('core',Math.min(7,Math.floor(q.t/.3*8)),q.x,q.y,.17);
}
hammerBossDraw=function(b){
 const old=HM10.drawing;HM10.drawing=b;
 try{HM10.base.draw.apply(this,arguments);}finally{HM10.drawing=old;}
 if(b.dead||b._hammerTime&&b._hammerTime.mode!=='attack'||b._hama&&b._hama.mode!=='attack')return;
 // The core belongs inside the authored chest; never paste a free-floating disc.
 hm10WallDraw(b);
};
function hm10CounterBank(C){return C.side>0?'swing_right':'swing_left';}
function hm10CounterFrame(C){
 if(C.t<C.tell)return Math.min(7,Math.floor(C.t/C.tell*8));
 if(C.t<C.tell+.4)return 8+Math.min(3,Math.floor((C.t-C.tell)/.4*4));
 return 12+Math.min(3,Math.floor((C.t-C.tell-.4)/.75*4));
}
function hm10CounterPoint(b,C,f=hm10CounterFrame(C)){
 const a=HM10_ART[hm10CounterBank(C)][f];return{x:b.x+(a.tip[0]-a.pivot[0])*HM10.bodyScale,y:b.y+(a.tip[1]-a.pivot[1])*HM10.bodyScale};
}
function hm10CounterLane(b,C){
 const a=hm10CounterPoint(b,C,7),z=hm10CounterPoint(b,C,11),L={x:a.x,y:a.y,ex:z.x,ey:z.y};
 // Warn the complete authored arc, including the curved travel between poses.
 // The actual impact still uses the original 38-pixel hammer strike width.
 const bend=Math.max(...[8,9,10].map(f=>{const p=hm10CounterPoint(b,C,f);return s81003Distance(p.x,p.y,L);}));
 return{...L,width:38+bend*2,progress:C.t/C.tell,laneShape:'line'};
}
bm9CounterHead=function(b,C,legacyFrame){
 const f=legacyFrame==null?hm10CounterFrame(C):legacyFrame===(C.side>0?0:4)+1?7:11;
 return hm10CounterPoint(b,C,f);
};
hammerStormDraw=function(b){const C=b?._hammer?.bm9Counter;
 if(!C||!XART.rdy(HM10_ART[hm10CounterBank(C)][0].key))return HM10.base.stormDraw.apply(this,arguments);
 hm10Blit(hm10CounterBank(C),hm10CounterFrame(C),b.x,b.y,HM10.bodyScale,b.flash||0);
 if(C.t<C.tell)combatWarningDraw(C,hm10CounterLane(b,C));
 for(const q of b._hammer.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}
 return true;
};
hammerStormSpikeShape=function(q){
 if(!XART.rdy(HM10_ART.spike[0].key))return HM10.base.spikeShape.apply(this,arguments);
 const age=q.t-q.split-(q.delay||0)-q.warm,rise=.38/(q.riseRate||1),hold=.24,shatter=.60;
 if(age<0||age>=rise+hold+shatter)return null;
 const f=age<rise?Math.min(7,Math.floor(age/rise*8)):age<rise+hold?8+Math.min(3,Math.floor((age-rise)/hold*4)):12+Math.min(3,Math.floor((age-rise-hold)/shatter*4));
 const a=HM10_ART.spike[f],k=q.height/Math.max(...HM10_ART.spike.map(p=>p.height));
 return{f,kx:k,ky:k,height:a.height*k,hm10:true};
};
hammerStormSpikeDraw=function(q){const a=hammerStormSpikeShape(q);if(!a?.hm10)return HM10.base.spikeDraw.apply(this,arguments);hm10Blit('spike',a.f,q.x,q.y,a.ky);};
