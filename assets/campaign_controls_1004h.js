'use strict';
/* One owner for map/menu/slot input. Start selects the menu; FIRE deploys. */
const MAP4H={page:4,xMouse:false,modalMouse:false,resumeX:false,rows:[],base:{
 campaign:campaignMenuInputTick,rivalInput:Rival24.mapInput,rivalBack:Rival24.mapBack,
 apply:campApply,open:openStageSelect,heading:map4eShipHeading,slots:drawCampSlots}};
for(const v of ['red','white','blue','red_hi','white_hi','blue_hi','flash'])
 XART._src['map4h_slot_'+v]='assets/game/campaign_controls_1004h/slot_'+v+'.png';
function map4hWarm(){for(const v of ['red','white','blue','red_hi','white_hi','blue_hi','flash'])XART.rdy('map4h_slot_'+v);}
function map4hLive(){return campPauseIsCampaignScreen()&&!sselZoom&&!riftReturn;}
function map4hXFocused(){return CF4.focus||MAP4E.xPreview;}
function map4hLeaveX(){CF4.focus=false;MAP4E.xPreview=false;sselCursor=Math.min(6,campaign.unlockedMax||1);MAP4E.focus=true;MAP4E.last=null;}
function map4hSelectX(){
 if(campaign.bonusUnlocked)return;
 if(Rival24.mapAvailable&&!cf4Pending()){
  Input.injectTap(keybind.down[0]);MAP4H.base.rivalInput();return;
 }
 CF4.previous=6;CF4.focus=!!cf4Pending();MAP4E.xPreview=!cf4Pending();
 Audio.SFX.blip();
}
// Left and right traverse the complete mission ring, including VIII -> VII
// when travelling left from I. The earned bonus portal remains its own gate.
sselMoveHorizontal=function(dir,lo,hi,from){const cur=from==null?sselCursor:from;
 if(lo===hi)return lo;return lo+((cur-lo+(dir<0?-1:1)+(hi-lo+1))%(hi-lo+1));};
function map4hVertical(dir){
 if(campaign.bonusUnlocked)return;
 if(sselCursor===6&&dir<0){map4hSelectX();return;}
 const p=cmap2World(sselCursor);let best=sselCursor,score=Infinity;
 for(let k=1;k<=Math.min(8,campaign.unlockedMax||1);k++){
  const q=cmap2World(k),dy=q.y-p.y,dx=q.x-p.x;if(k===sselCursor||dy*dir<=0)continue;
  const d=Math.hypot(dx,dy)+Math.abs(dx)*1.6;if(d<score){score=d;best=k;}
 }
 if(best!==sselCursor){sselCursor=best;Audio.SFX.blip();}
}
map4eShipHeading=function(from,to,dx){
 if(from===6&&to==='x')return 0;
 if(from==='x'&&to===6)return Math.PI;
 if(from===3&&to===4||from===1&&to===8||from===8&&to===7)return Math.PI;
 if(from===4&&to===3)return 0;
 return MAP4H.base.heading(from,to,dx);
};
cmap2StartPressed=function(){
 if(cmap2.focus==='bar')cmap2BarActivate(cmap2.bar||0);
 else{cmap2.focus='bar';Input.mouse.moved=false;Audio.SFX.blip();}
};
campaignMenuInputTick=function(){
 if(state!==GS.STAGESEL||run.mode!=='campaign'||!cmap2On())return MAP4H.base.campaign();
 if(campPause)return false;
 // Consume Start once, before Stage X or deployment gets a chance to read it.
 if(Input.menuStart()){if(map4hLive()&&!_selFlash)cmap2StartPressed();return true;}
 if(Input.menuBack()){
  if(map4hLive()&&!_selFlash){
   if(cmap2.focus==='bar')cmap2.focus='map';
   else if(map4hXFocused())map4hLeaveX();
   else cmap2.focus='bar';
   Audio.SFX.blip();
  }return true;
 }return false;
};
cmap2BarInput=function(lo,hi){
 if(campPause)return true;if(_selFlash)return cmap2.focus==='bar';
 const m=Input.mouse||{},R=cmap2._btnRects||cmap2BtnRects();let hov=-1;
 for(let i=0;i<R.length;i++){const r=R[i];if(m.x>=r.x&&m.x<=r.x+r.w&&m.y>=r.y&&m.y<=r.y+r.h){hov=i;break;}}
 if(hov>=0&&Input.consumeMouseMoved()){cmap2.focus='bar';cmap2.bar=hov;}
 if(hov>=0&&m.down&&!cmap2._mdPrev){cmap2.focus='bar';cmap2.bar=hov;cmap2BarActivate(hov);return true;}
 if(cmap2.focus==='bar'){
  if(Input.menuDown()){cmap2.focus='map';Input.mouse.moved=false;Audio.SFX.blip();return true;}
  Input.menuUp();const n=CAMP_PAUSE_BTN.length;
  if(Input.menuLeft()){cmap2.bar=(cmap2.bar+n-1)%n;Audio.SFX.blip();}
  if(Input.menuRight()){cmap2.bar=(cmap2.bar+1)%n;Audio.SFX.blip();}
  if(stateT>.4&&Input.menuConfirm())cmap2BarActivate(cmap2.bar);
  return true;
 }
 if(Input.menuUp()){map4hVertical(-1);return true;}
 if(Input.menuDown()){map4hVertical(1);return true;}
 return false;
};
Rival24.mapInput=function(){
 // The bar and open slot picker always own input, even over a pending fight.
 if(campPause||cmap2.focus==='bar'||_selFlash||sselBoot)return false;
 if(Rival24.mapAvailable&&!cf4Pending())return MAP4H.base.rivalInput();
 const m=Input.mouse||{},click=!!m.down&&!MAP4H.xMouse;MAP4H.xMouse=!!m.down;
 const p=map4eStageXPoint(),q=cmap2ToScreen(p.x,p.y);
 const hit=map4eStageXAt(m.x,m.y)||Math.abs(m.x-q.x)<19&&m.y>q.y-34&&m.y<q.y+7;
 if(click&&hit){
  if(map4hXFocused()&&cf4Pending()&&CF4.flight>=3.2)cf4LaunchX();else map4hSelectX();return true;
 }
 if(!map4hXFocused())return false;
 if(Input.menuDown()||Input.menuUp()){map4hLeaveX();Audio.SFX.blip();return true;}
 if(Input.menuLeft()){map4hLeaveX();Input.injectTap(keybind.left[0]);return false;}
 if(Input.menuRight()){map4hLeaveX();Input.injectTap(keybind.right[0]);return false;}
 if(Input.menuConfirm()){
  if(cf4Pending()&&CF4.flight>=3.2)cf4LaunchX();
  else cmap2Toast(cf4Pending()?'FIGHTERS APPROACHING':'COMPLETE STAGE 6 TO OPEN STAGE X');
 }return true;
};
Rival24.mapBack=function(){return campPause||cmap2.focus==='bar'?false:MAP4H.base.rivalBack();};
campApply=function(s){const ok=MAP4H.base.apply(s);if(ok)MAP4H.resumeX=!!s.mapStageX;return ok;};
openStageSelect=function(){const r=MAP4H.base.open.apply(this,arguments);
 MAP4H.xMouse=false;MAP4H.modalMouse=false;
 if(MAP4H.resumeX){MAP4H.resumeX=false;CF4.focus=!!cf4Pending();MAP4E.xPreview=!cf4Pending();}
 return r;
};
function map4hSlotKey(index,selected){return 'map4h_slot_'+['red','white','blue'][index%3]+(selected?'_hi':'');}
function map4hSlotDraw(index,r,selected,mode){
 const auto=index===CAMP_SLOTS,data=auto?campReadAuto():campReadSlot(index),used=!!data&&data.v===CAMP_SAVE_VER;
 const key=map4hSlotKey(index,selected);if(!XART.rdy(key))return;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=selected?1:.83;
 ctx.drawImage(XART.get(key),r.x,r.y,r.w,r.h);ctx.restore();
 const left=r.x+r.w*.065,top=r.y+r.h*.25,side=r.h*.52;
 if(used){const ship='ship_'+data.pilot;if(XART.rdy(ship)){
  const im=XART.get(ship),s=Math.min(side/im.width,side/im.height);ctx.drawImage(im,left+(side-im.width*s)/2,top+(side-im.height*s)/2,im.width*s,im.height*s);
 }}
 const x=r.x+r.w*.55,w=r.w*.61,f=uiFontArt();if(!f)return;
 const title=(auto?'AUTO SAVE':'SLOT '+String(index+1).padStart(2,'0'))+(used?'   STAGE '+(data.mapStageX?'X':data.stage):'   EMPTY');
 const pilot=used?(PILOTS.find(p=>p.key===data.pilot)?.name||data.pilot).toUpperCase():'';
 const body=used?pilot+'   '+String(data.diff||'normal').toUpperCase():mode==='save'?'READY TO SAVE':'NO SAVED CAMPAIGN';
 const date=used&&data.t?new Date(data.t):null;
 const detail=used?'SCORE '+(data.score||0)+(date?'   '+String(date.getMonth()+1).padStart(2,'0')+'/'+String(date.getDate()).padStart(2,'0')+' '+String(date.getHours()).padStart(2,'0')+':'+String(date.getMinutes()).padStart(2,'0'):''):'';
 stageText(f,title,x,r.y+r.h*.32,11,selected?'#ffe082':'#d9e8f5',.85,1,.06);
 stageText(f,body,x,r.y+r.h*.52,9,'#b9d9ea',.85,1,.05);
 if(detail)stageText(f,detail,x,r.y+r.h*.71,8,'#8eb3c6',.85,1,.04);
}
function map4hSlotCommit(P,index,bar){
 if(P.mode==='save'){
  if(campWriteSlot(index)){campSession=campReadSlot(index);P.msg='SAVED TO SLOT '+(index+1);P.msgT=2;Audio.SFX.select();}
  else{P.msg='SAVE FAILED - STORAGE BLOCKED';P.msgT=3;Audio.SFX.error?.();}
  if(!bar){campHubMsg=P.msg;campHubMsgT=P.msgT;}
  return;
 }
 const data=index===CAMP_SLOTS?campReadAuto():campReadSlot(index);
 if(!data){P.msg='THAT SLOT IS EMPTY';P.msgT=2;if(!bar){campHubMsg=P.msg;campHubMsgT=P.msgT;}Audio.SFX.blip();return;}
 if(campApply(data)){campSession=data;campPauseClose();campPick=null;openStageSelect(run.stage,{});cmap2Toast(index===CAMP_SLOTS?'LOADED AUTO SAVE':'LOADED SLOT '+(index+1));Audio.SFX.select();}
 else{P.msg='THAT SAVE IS FROM AN OLDER BUILD';P.msgT=2;if(!bar){campHubMsg=P.msg;campHubMsgT=P.msgT;}}
}
function map4hSlotInput(P,rows,count,bar){
 if(_selFlash)return;const m=Input.mouse||{},edge=!!m.down&&!MAP4H.modalMouse;MAP4H.modalMouse=!!m.down;
 for(const r of rows)if(m.x>=r.x&&m.x<=r.x+r.w&&m.y>=r.y&&m.y<=r.y+r.h){
  if(Input.consumeMouseMoved())P.sel=r.index;
  if(edge&&P.t>.2){P.sel=r.index;selFlash(()=>map4hSlotCommit(P,r.index,bar),.18,{...r,key:'map4h_slot_flash'});return;}
 }
 if(Input.menuLeft()){P.sel=Math.max(0,P.sel-MAP4H.page);Audio.SFX.blip();}
 if(Input.menuRight()){P.sel=Math.min(count-1,P.sel+MAP4H.page);Audio.SFX.blip();}
 if(Input.menuUp()){P.sel=(P.sel+count-1)%count;Audio.SFX.blip();}
 if(Input.menuDown()){P.sel=(P.sel+1)%count;Audio.SFX.blip();}
 if(Input.menuBack()){if(bar){campPauseClose();cmap2.focus='bar';}else{campPick=null;campHubIndex=0;}return;}
 if(P.t>.2&&Input.menuConfirm()){
  const index=P.sel,r=rows.find(r=>r.index===index);if(r)selFlash(()=>map4hSlotCommit(P,index,bar),.18,{...r,key:'map4h_slot_flash'});
 }
}
const MAP4H_BAR_DRAW=campBarMenuDraw;
const MAP4H_HINT_DRAW=drawHintBar;
drawHintBar=function(){if(state===GS.STAGESEL&&campPause)return;return MAP4H_HINT_DRAW.apply(this,arguments);};
campBarMenuDraw=function(dt){
 const P=campPause;if(!P)return;if(P.mode==='exit')return MAP4H_BAR_DRAW(dt);
 map4hWarm();P.t+=dt||0;P.msgT=Math.max(0,P.msgT-(dt||0));
 const count=CAMP_SLOTS+(P.mode==='load'?1:0),page=Math.floor(P.sel/MAP4H.page),start=page*MAP4H.page,n=Math.min(MAP4H.page,count-start);
 const pw=390,px=(VW-pw)/2,top=CM2_BAR.y+CM2_BAR.h+2,pad=48,rowH=82,gap=5,ph=pad+n*(rowH+gap)+24;
 const e=1-Math.pow(1-clamp(P.t/.18,0,1),3),py=top-(1-e)*ph,rows=[];
 ctx.save();ctx.fillStyle='rgba(0,0,0,.62)';ctx.fillRect(-campaignViewOffset(),top,campaignViewWidth(),VH-top);
 ctx.beginPath();ctx.rect(-campaignViewOffset(),top,campaignViewWidth(),VH-top);ctx.clip();
 ctx.fillStyle='#03080f';ctx.fillRect(px+12,py+10,pw-24,ph-10);
 drawPanel('dlg_window','black',px,py,pw,ph);const f=uiFontArt();
 if(f){stageText(f,P.mode==='save'?'SAVE GAME':'LOAD GAME',VW/2,py+19,14,'#d3eaff',.85,1,.1);
 stageText(f,'PAGE '+(page+1)+' / '+Math.ceil(count/MAP4H.page),VW/2,py+34,9,'#91bdd7',.85,1,.05);}
 for(let i=0;i<n;i++){const index=start+i,r={index,x:px+14,y:py+pad+i*(rowH+gap),w:pw-28,h:rowH};rows.push(r);map4hSlotDraw(index,r,index===P.sel,P.mode);}
 MAP4H.rows=rows;
 if(P.msgT>0&&f)stageText(f,P.msg,VW/2,py+ph-13,11,'#ffe082',.85,1,.08);
 ctx.restore();controlHintRow([['pad_dpad','SLOT / PAGE'],['pad_a',P.mode==='save'?'SAVE':'LOAD'],['pad_b','MENU']]);
 if(e>=.99)map4hSlotInput(P,rows,count,true);
};
drawCampSlots=function(dt){
 map4hWarm();const mode=campPick,count=CAMP_SLOTS+(mode==='load'?1:0),page=Math.floor(campHubIndex/MAP4H.page),start=page*MAP4H.page,rows=[];
 campText(mode==='save'?'SAVE GAME':'LOAD GAME',VW/2,99,14,'#d3eaff');campText('PAGE '+(page+1)+' / '+Math.ceil(count/MAP4H.page),VW/2,120,9,'#91bdd7');
 for(let i=0;i<Math.min(MAP4H.page,count-start);i++){const index=start+i,r={index,x:59,y:135+i*80,w:362,h:76};rows.push(r);map4hSlotDraw(index,r,index===campHubIndex,mode);}
 campHubMsgT=Math.max(0,campHubMsgT-dt);const P={sel:campHubIndex,mode,t:stateT,msg:campHubMsg,msgT:campHubMsgT};
 if(campHubMsgT>0)campText(campHubMsg,VW/2,470,11,'#ffe082');
 controlHintRow([['pad_dpad','SLOT / PAGE'],['pad_a',mode==='save'?'SAVE':'LOAD'],['pad_b','BACK']]);
 if(!campPause){map4hSlotInput(P,rows,count,false);if(campPick){campHubIndex=P.sel;campHubMsg=P.msg;campHubMsgT=P.msgT;}}
};
// Review saves really persist, but in their own namespace. Authored campaign
// fixtures must never overwrite a player's live slots or claim a no-op saved.
function map4hPreviewStorage(){
 if(window.__map4hPreviewStorage)return;const native=window.localStorage,prefix='bof_map_review_1004h_';
 const adapter={getItem:k=>native.getItem(prefix+k),setItem:(k,v)=>native.setItem(prefix+k,String(v)),removeItem:k=>native.removeItem(prefix+k)};
 Object.defineProperty(window,'localStorage',{configurable:true,value:adapter});window.__map4hPreviewStorage=true;
}
map4hWarm();
