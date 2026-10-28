"use strict";
/* Approved Pixelmap typography. The text-only front end is a playable ?pixelmap=1
   concept; native game modes, confirmations, saves, unlocks and inputs remain owners. */
const PM27={enabled:!new URLSearchParams(location.search).has('classicfont'),concept:new URLSearchParams(location.search).get('pixelmap')==='1',ready:false,role:null,names:null,rows:{},events:[],draws:0,
 base:{ready:bmfReady,measure:bmfMeasure,draw:bmfDraw,on:bmfDrawOn,msg:msgText,left:msgTextLeft,width:msgMeasure,stage:stageText,stageWidth,ui:ui20Text,lines:ui20Lines,name:pilotNameDraw,pcMeasure:pcFontMeasure,pcLeft:pcFontLeft,camp:campText,title:bofTitle,contents:ui20PanelContents,
 titleRows:titleMenuLayout,buttons:drawMenuButtons,modeRows,modePanel:modePanelDraw,mark:menuSelMark,lock:modeLockDraw,hub:drawCampaignHub,choice:p2ChoiceDraw,diff:drawDiff,arrow:drawSelArrow,flash:selFlashDraw,load:stageLoadBegin,footer:menuControlFooter,rail:ui20Rail,compact:ui20Compact}};
if(PM27.concept)PM27.enabled=true;
for(const a of [...Object.values(PM27_ART.banks),...Object.values(PM27_ART.arrows)])XART._src[a.key]=a.path+'?v=solid-r-square-hud-1027d';
function pm27Warm(){if(PM27.enabled)for(const a of [...Object.values(PM27_ART.banks),...Object.values(PM27_ART.arrows)])XART.rdy(a.key);}
function pm27Live(){if(!PM27.enabled)return false;if(!PM27.ready){PM27.ready=Object.values(PM27_ART.banks).every(a=>XART.rdy(a.key));if(PM27.ready){UI20.dirty=true;UI20.cache.clear();pilotNamePlates.clear();}}return PM27.ready;}
function pm27Concept(){return PM27.concept&&pm27Live();}
pm27Warm();
stageLoadBegin=function(n,keys){return PM27.base.load.call(this,n,PM27.enabled?[...(keys||[]),...Object.values(PM27_ART.banks).map(a=>a.key)]:keys);};
function pm27Text(s){return String(s??'').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/×/g,'x').replace(/[·•]/g,'/').replace(/→/g,'>').replace(/←/g,'<').replace(/°/g,'o');}
function pm27Family(h,face){return PM27.role||(/dialogue|cutscene|invasion/.test(String(face))?'command':h>=16?'fury_strike':'command');}
function pm27Bank(family,h){const list=Object.values(PM27_ART.banks).filter(a=>a.family===family);return list.filter(a=>a.height<=h+.01).at(-1)||list[0];}
function pm27Run(s,h,family){const a=pm27Bank(family||pm27Family(h,_msgFace),h);s=pm27Text(s);let pen=0,left=Infinity,right=-Infinity,top=Infinity,bottom=-Infinity;
 for(const c of s){const q=a.glyphs[c.codePointAt(0)]||a.glyphs[63],r=q.ink||[0,0,a.cw,a.ch];if(r[2]>r[0]){left=Math.min(left,pen+r[0]);right=Math.max(right,pen+r[2]);top=Math.min(top,r[1]);bottom=Math.max(bottom,r[3]);}pen+=q.advance;}
 if(!Number.isFinite(left)){left=0;right=pen;top=0;bottom=0;}if(s.startsWith(' '))left=Math.min(left,0);if(s.endsWith(' '))right=Math.max(right,pen);return {left,right,top,bottom,width:right-left,advance:pen};}
function pm27Width(s,h,family){return pm27Run(s,h,family).width;}
function pm27Palette(color){if(!color)return'chrome';let c=String(color).toLowerCase();if(['white','#fff','#ffffff'].includes(c))return'chrome';
 const names={red:'ember',orange:'ember',yellow:'gold',green:'toxic',cyan:'signal',blue:'ice',purple:'corrupt',pink:'rose',gold:'gold'};if(names[c])return names[c];
 const m=c.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/);if(!m)return'chrome';c=m[1];if(c.length===3)c=[...c].map(x=>x+x).join('');const[r,g,b]=[0,2,4].map(i=>parseInt(c.slice(i,i+2),16)),max=Math.max(r,g,b),min=Math.min(r,g,b);
 if(max-min<45||min>180)return'chrome';if(r>g*1.18&&r>b*1.12)return g>130?'gold':'ember';if(r>150&&b>110&&g<170)return r>b*1.3?'rose':'corrupt';if(g>r*1.15&&g>b*1.05)return'toxic';if(b>r*1.15&&g>b*.68)return'signal';if(b>r*1.15)return'ice';if(r>150&&g>130)return'gold';return'chrome';}
function pm27Fit(s,h,w,family){let a=pm27Bank(family,h);const list=Object.values(PM27_ART.banks).filter(q=>q.family===family&&q.height<=a.height).reverse();for(const q of list)if(pm27Width(s,q.height,family)<=w)return q;
 if(family!=='command')return pm27Fit(s,Math.min(h,14),w,'command');return list.at(-1)||a;}
function pm27Draw(g,s,x,cy,h=10,{family,color,palette,align='center',width=Infinity,alpha=1}={}){
 if(!pm27Live()||alpha<=0)return 0;s=pm27Text(s);family=family||pm27Family(h,_msgFace);const a=pm27Fit(s,h,width,family),p=PM27_ART.palettes.indexOf(palette||pm27Palette(color)),dim=alpha<.55,
  sw=a.planeW,sh=a.planeH,im=XART.get(a.key),run=pm27Run(s,a.height,a.family),w=run.width;let pen=Math.round(x-(align==='center'?(run.left+run.right)/2:align==='right'?run.right:run.left));const y=Math.round(cy-a.height/2-a.top);
 g.save();g.globalAlpha=1;g.globalCompositeOperation='source-over';g.filter='none';g.shadowBlur=0;g.imageSmoothingEnabled=false;
 for(const c of s){const q=a.glyphs[c.codePointAt(0)]||a.glyphs[63];g.drawImage(im,q.x+(dim?sw:0),q.y+Math.max(0,p)*sh,a.cw,a.ch,pen,y,a.cw,a.ch);pen+=q.advance;}g.restore();PM27.draws++;
 if(PM27.events.length<200)PM27.events.push({state,text:s,family:a.family,height:a.height,palette:palette||pm27Palette(color),width:w,available:Number.isFinite(width)?width:null});return w;
}
function pm27Wrap(s,w,h,family='command'){const rows=[];for(const para of pm27Text(s).split('\n')){let line='';for(let word of para.split(/\s+/).filter(Boolean)){if(pm27Width(line?(line+' '+word):word,h,family)<=w){line=line?line+' '+word:word;continue;}if(line){rows.push(line);line='';}while(pm27Width(word,h,family)>w){let part='';for(const c of word){if(part&&pm27Width(part+c,h,family)>w)break;part+=c;}rows.push(part);word=word.slice(part.length);}line=word;}rows.push(line);}return rows;}
bmfReady=function(k){return pm27Live()&&(BMF[k]||['game','dialogue','cutscene','invasion'].includes(k))?true:PM27.base.ready.apply(this,arguments);};
bmfMeasure=function(k,s,h){return pm27Live()?pm27Width(s,h,pm27Family(h,k)):PM27.base.measure.apply(this,arguments);};
bmfDraw=function(k,s,x,y,h,alpha,color){if(!pm27Live())return PM27.base.draw.apply(this,arguments);pm27Draw(ctx,s,x,y+h/2,h,{align:'left',family:pm27Family(h,k),color,alpha:alpha??1});return true;};
bmfDrawOn=function(g,k,s,x,y,h,align){if(!pm27Live())return PM27.base.on.apply(this,arguments);pm27Draw(g,s,x,y,h,{family:pm27Family(h,k),align:align||'left'});return true;};
msgMeasure=function(s,h){return pm27Live()?pm27Width(s,h):PM27.base.width.apply(this,arguments);};
msgText=function(s,x,y,h,color,tint,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{color,alpha:alpha??1}):PM27.base.msg.apply(this,arguments);};
msgTextLeft=function(s,x,y,h,color,tint,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{align:'left',color,alpha:alpha??1}):PM27.base.left.apply(this,arguments);};
stageWidth=function(a,s,h){return pm27Live()?pm27Width(s,h,pm27Family(h,null)):PM27.base.stageWidth.apply(this,arguments);};
stageText=function(a,s,x,y,h,color,tint,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{family:pm27Family(h,null),color,alpha:alpha??1}):PM27.base.stage.apply(this,arguments);};
pcFontMeasure=function(s,h){return pm27Live()?pm27Width(s,h,'command'):PM27.base.pcMeasure.apply(this,arguments);};
pcFontLeft=function(s,x,y,h,color,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{family:'command',align:'left',color,alpha:alpha??1}):PM27.base.pcLeft.apply(this,arguments);};
campText=function(s,x,y,h,color,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{color,alpha:alpha??1}):PM27.base.camp.apply(this,arguments);};
bofTitle=function(s,x,y,h){return pm27Live()?pm27Draw(ctx,s,x,y,h||16,{family:'fury_strike',palette:'chrome'}):PM27.base.title.apply(this,arguments);};
pilotNameDraw=function(s,x,y,h,color,alpha){return pm27Live()?pm27Draw(ctx,s,x,y,h,{family:'fury_strike',color,alpha:alpha??1}):PM27.base.name.apply(this,arguments);};
ui20PanelContents=function(who){const old=PM27.names;PM27.names=String(who);try{return PM27.base.contents.apply(this,arguments);}finally{PM27.names=old;}};
ui20Rail=function(g,side,v){const old=PM27.hudSide;PM27.hudSide=side;try{return PM27.base.rail.apply(this,arguments);}finally{PM27.hudSide=old;}};
ui20Compact=function(){const old=PM27.hudCompact;PM27.hudCompact=true;try{return PM27.base.compact.apply(this,arguments);}finally{PM27.hudCompact=old;}};
ui20Text=function(g,s,x,y,h,w,align='center',color){if(!pm27Live())return PM27.base.ui.apply(this,arguments);s=String(s??'').toUpperCase();
 if(PM27.hudSide===0&&y===268)w=Math.min(w,244);
 if(PM27.hudSide===1){if(y===351){y=348;h=Math.min(h,28);}else if(y===826)y=822;else if(y===915)y=909;else if(y===756){x=244;w=Math.min(w,152);}if(y===464||y===568)w=Math.min(w,256);}
 const name=s===String(PM27.names).toUpperCase(),numeric=(PM27.hudSide!=null||PM27.hudCompact)&&/\d/.test(s),family=name?(pm27Width(s,8,'fury_strike')<=w?'fury_strike':'command_narrow'):numeric?'command':pm27Family(h,null);return pm27Draw(g,s,x,y,h,{family,color,align,width:w});};
ui20Lines=function(g,s,x,y,h,w,step){if(!pm27Live())return PM27.base.lines.apply(this,arguments);const a=pm27Bank('command',Math.min(h,14)),rows=pm27Wrap(s,w,a.height);rows.forEach((s,i)=>pm27Draw(g,s,x,y+i*step,a.height,{family:'command',width:w}));return rows.length;};
drawSelArrow=function(x,y,h,mirror,variant){if(!pm27Concept()||h!==22)return PM27.base.arrow.apply(this,arguments);const a=PM27_ART.arrows[variant||'b']||PM27_ART.arrows.b;if(!XART.rdy(a.key))return false;const f=Math.floor(performance.now()/50)%16+(mirror?16:0);ctx.save();ctx.globalAlpha=1;ctx.shadowBlur=0;ctx.filter='none';ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);ctx.restore();return true;};
function pm27Row(label,x,y,h=20,selected=false,enabled=true,variant){const a=pm27Fit(label,h,VW-110,'fury_strike'),w=pm27Width(label,a.height,a.family),r={x:x-w/2-4,y:y-a.height/2-5,w:w+8,h:a.height+10,pmText:label,pmH:a.height,pmFamily:a.family,cx:x,cy:y};
 pm27Draw(ctx,label,x,y,a.height,{family:a.family,palette:selected&&enabled?'gold':'chrome',alpha:enabled?1:.4});if(selected){drawSelArrow(x-w/2-24,y,22,false,variant);drawSelArrow(x+w/2+24,y,22,true,variant);}return r;}
titleMenuLayout=function(){if(!pm27Concept())return PM27.base.titleRows.apply(this,arguments);return{w:300,h:32,pitch:38,y0:167};};
drawMenuButtons=function(){if(!pm27Concept())return PM27.base.buttons.apply(this,arguments);const L=titleMenuLayout();PM27.rows.title=TITLE_ITEMS.map((s,i)=>pm27Row(s,VW/2,L.y0+i*L.pitch,20,menuIndex===i,true));};
modeRows=function(list){if(!pm27Concept())return PM27.base.modeRows.apply(this,arguments);PM27.rows.mode=[];return list.map((_,i)=>({y:140+i*Math.min(56,280/Math.max(1,list.length-1)),h:40,pw:290}));};
menuSelMark=function(){if(pm27Concept()&&state===GS.MODESEL)return;return PM27.base.mark.apply(this,arguments);};
modePanelDraw=function(it,x,y,pw,locked){if(!pm27Concept())return PM27.base.modePanel.apply(this,arguments);const r=pm27Row(it.name,x,y,22,modeList()[modeIndex]?.mode===it.mode,!locked,'r');(PM27.rows.mode||=[]).push(r);return r;};
modeLockDraw=function(r){if(!pm27Concept())return PM27.base.lock.apply(this,arguments);if(r?.pmText)pm27Draw(ctx,'LOCKED',r.cx,r.cy+20,8,{family:'command',palette:'chrome'});return true;};
menuControlFooter=function(){if(pm27Concept()&&state===GS.DIFF)return;return PM27.base.footer.apply(this,arguments);};
selFlashDraw=function(){if(pm27Concept()&&_selFlash&&[GS.MODESEL,GS.CAMPHUB].includes(state)&&_selFlash.rect?.pmText){const r=_selFlash.rect;pm27Draw(ctx,r.pmText,r.cx,r.cy,r.pmH,{family:r.pmFamily,palette:Math.floor(_selFlash.t*16)%2?'gold':'chrome'});return;}return PM27.base.flash.apply(this,arguments);};
drawCampaignHub=function(dt){if(!pm27Concept())return PM27.base.hub.apply(this,arguments);p2HubSync();if(campPick)return PM27.base.hub.apply(this,arguments);
 drawCanonBackdrop('nbt_5',.58);pm27Draw(ctx,'CAMPAIGN',VW/2,64,26,{family:'fury_strike',palette:'chrome'});const n=CAMPHUB_ITEMS.length,gap=54,start=254-(n-1)*gap/2;PM27.rows.hub=[];
 for(let i=0;i<n;i++){const it=CAMPHUB_ITEMS[i],r=pm27Row(it.label,VW/2,start+i*gap,22,i===campHubIndex,campHubEnabled(it.act),'y');PM27.rows.hub.push(r);if(i===campHubIndex)drawCampaignHub._selRect=r;}
 if(campHubMsgT>0){campHubMsgT-=dt;pm27Draw(ctx,campHubMsg,VW/2,430,10,{family:'command',width:VW-36,palette:'signal'});}controlHintRow([['pad_dpad','SELECT'],['pad_a','CONFIRM'],['pad_b','BACK']]);
 if(!campPause){menuMouseList('pm27-camphub',n,i=>({cx:VW/2,cy:start+i*gap,hw:170,hh:22}),()=>campHubIndex,v=>campHubIndex=v,stateT>.25);campHubInput();}
};
p2ChoiceDraw=function(dt){if(!pm27Concept())return PM27.base.choice.apply(this,arguments);const coop=P2M.choice==='coop',labels=coop?['LOCAL CO-OP','ONLINE CO-OP']:['NEW GAME','NEW GAME +'];drawCanonBackdrop('nbt_3',.65);pm27Draw(ctx,coop?'CO-OP':'ARCADE',VW/2,82,26,{family:'fury_strike'});
 if(Input.menuUp()||Input.menuDown())P2M.row=1-P2M.row;const click=Input.mouse.down&&!P2M.md;P2M.md=Input.mouse.down;PM27.rows.choice=[];
 for(let i=0;i<2;i++){const y=210+i*80;PM27.rows.choice.push(pm27Row(labels[i],VW/2,y,24,P2M.row===i,true));if(click&&Input.mouse.inside&&Math.abs(Input.mouse.x-VW/2)<165&&Math.abs(Input.mouse.y-y)<30){P2M.row=i;p2ChoiceConfirm();return;}}
 pm27Draw(ctx,coop?'TWO PILOTS / SEPARATE LIVES AND SCORES':'CHOOSE BEFORE DIFFICULTY',VW/2,414,10,{family:'command',palette:'signal',width:VW-40});controlHintRow([['pad_dpad','SELECT'],['pad_a','CONFIRM'],['pad_b','BACK']]);if(stateT>.25&&Input.menuConfirm())p2ChoiceConfirm();if(Input.menuBack()){P2M.choice=null;Input.clearTaps?.();}
};
drawDiff=function(dt){if(!pm27Concept())return PM27.base.diff.apply(this,arguments);drawCanonBackdrop('nbt_2',.55);pm27Draw(ctx,'SELECT DIFFICULTY',VW/2,52,22,{family:'fury_strike'});const L=diffList(),N=L.length,gap=Math.min(58,260/Math.max(1,N-1)),start=238-(N-1)*gap/2;PM27.rows.diff=[];
 for(let i=0;i<N;i++){const r=pm27Row(DIFFS[L[i]].name,VW/2,start+i*gap,22,menuIndex===i,!diffLocked(L[i]),'g');PM27.rows.diff.push(r);if(diffLocked(L[i]))modeLockDraw(r);}
 const parts=difficultyDescription(menuIndex).split(' · ');for(let i=0;i<parts.length;i++)pm27Draw(ctx,parts[i],VW/2,424+i*14,8,{family:'command',width:VW-32,palette:'signal'});modeDenyDraw(dt);controlHintRow([['pad_dpad','SELECT'],['pad_a','CONFIRM'],['pad_b','BACK']]);
 if(diffFlash>0)diffFlash-=dt;if(diffPending!=null&&diffFlash<=0){const m=diffPending;diffPending=null;menuIndex=m;pickDiff();return;}if(diffPending!=null)return;
 if(Input.menuDown()){menuIndex=(menuIndex+1)%N;Audio.SFX.blip();}if(Input.menuUp()){menuIndex=(menuIndex+N-1)%N;Audio.SFX.blip();}const moved=Input.consumeMouseMoved();for(let i=0;i<N;i++)if(Input.mouse.inside&&Math.abs(Input.mouse.x-VW/2)<160&&Math.abs(Input.mouse.y-(start+i*gap))<24){if(moved)menuIndex=i;if(Input.mouse.down&&!drawDiff._md){menuIndex=i;confirmDiff();}}drawDiff._md=Input.mouse.down;if(Input.menuConfirm())confirmDiff();if(Input.menuBack()){setState(passwordDifficulty?GS.PASSWORD:run.mode==='campaign'?GS.CAMPHUB:GS.MODESEL);menuIndex=0;}
};
globalThis.BOF_PIXELMAP_UI_1027=PM27;

// Pilot copy fits above the unchanged stat and special-ability regions.
PM27.base.pilotCard=pt11PilotCard;
pt11PilotCard=function(P,PX,PY,PW,PH,spin,locked){
 if(!pm27Live())return PM27.base.pilotCard.apply(this,arguments);
 const wide=PW>560,pad=12,bodyW=PW*(wide?.28:.38),shipW=wide?PW*.29:PW-bodyW-pad*2;
 const by=PY+32,bh=PH-44,bx=PX+pad,sx=bx+bodyW+pad;
 const shipH=wide?bh*.82:Math.min(bh*.39,190),shipY=by+shipH/2;
 const infoX=wide?sx+shipW+pad:sx,infoY=wide?by:by+shipH+10;
 const infoW=PX+PW-pad-infoX,infoH=PY+PH-pad-infoY;
 psPanelBox(PX,PY,PW,PH,P.tint,true);
 const launching=pilotPending!=null;
 if(locked){pcFontLeft('LOCKED',bx+8,by+bh*.42,16,'#dce2ea',1);pcFontLeft('PASSWORD REQUIRED',infoX,infoY+32,10,'#ffe98a',1);return;}
 const body=psBodyKey(P.key);psBlitFit(body||'port_'+P.key+'_idle',bx+bodyW/2,by+bh/2,bodyW-8,bh,1);
 // The broad actual gameplay ship is easiest to identify; no generated substitute.
 const ship=psShipKey(P.key,null);psBlitFit(ship,sx+shipW/2,shipY,shipW-12,shipH-8,1);
 const M=BOFX.pilotcard?.[P.key]||{},stats=pcStats(P.key),sp=pcSpecial(P.key),copy=pcScreenCopy(P);
 pilotNameDraw(launching?'GOOD LUCK, '+P.name+'!':pcRevealText(copy,0),PX+PW/2,PY+17,20,P.tint,1);
 PT11_UI.card={pilot:P.key,body:[bx,by,bodyW,bh],ship:[sx,by,shipW,shipH],info:[infoX,infoY,infoW,infoH],key:ship};
 if(launching)return;
 const title=pcRevealText(copy,1),call=pcRevealText(copy,2),aff=pcRevealText(copy,3);
 pcFontLeft(title,infoX,infoY+5,pcFontFit(title,infoW,10,8),P.tint,1);
 pcFontLeft(call,infoX,infoY+20,pcFontFit(call,infoW,10,8),'#f0f4ff',1);
 const emblem=affilEmblemKey(M.affil),eh=Math.min(28,infoH*.12),emblemReady=!!(emblem&&XART.rdy(emblem)),emblemSpace=emblemReady?eh+8:0;
 if(emblemReady)psBlitFit(emblem,infoX+eh/2,infoY+31+eh/2,eh,eh,1);
 for(const [i,line] of pcFontWrap(aff,infoW-emblemSpace,10).entries())pcFontLeft(line,infoX+emblemSpace,infoY+42+i*14,10,'#cfeaff',1);
 const specialH=44,statH=stats.length*11,statY=infoY+infoH-specialH-statH-5,bioTop=infoY+33+eh,bioBottom=statY-6;
 const bio=pcRevealText(copy,4);let bioH=9,bioLines=pm27Wrap(bio,infoW,bioH);
 while(bioH>7&&bioH+Math.max(0,bioLines.length-1)*(bioH+2)>bioBottom-bioTop){bioH--;bioLines=pm27Wrap(bio,infoW,bioH);}
 const bioStep=bioH+2;for(let i=0;i<bioLines.length&&bioTop+bioH+i*bioStep<=bioBottom;i++)pcFontLeft(bioLines[i],infoX,bioTop+bioH/2+i*bioStep,bioH,'#dbe8f3',1);
 PM27.pilotCopy={pilot:P.key,height:bioH,lines:bioLines.length,available:bioBottom-bioTop,used:bioH+Math.max(0,bioLines.length-1)*bioStep};
 const barX=infoX+infoW*.51,barW=infoW*.49;
 for(let i=0;i<stats.length;i++){
  const y=statY+i*11,frac=pcVisibleSegments(i,stats[i].val)/PC_MAX_SEG;
  const ready=pcard&&(pcard.done||pcard.phase==='special'||pcard.phase==='hold'||pcard.phase==='bars'&&pcard.bar>=i);
  if(ready)pcFontLeft(stats[i].label,infoX,y,pcFontFit(stats[i].label,infoW*.49,9,8),'#dbe8ff',1);
  ctx.fillStyle='#0c1522';ctx.fillRect(barX,y-3,barW,7);ctx.fillStyle=P.tint;ctx.fillRect(barX+1,y-2,(barW-2)*frac,5);
 }
 if(pcard&&(pcard.done||pcard.phase==='special'||pcard.phase==='hold')){
  const y=infoY+infoH-22,a=pcard.done?1:pcard.spT||0;ctx.save();ctx.globalAlpha=a;
  iconDraw('spicon_'+P.key,infoX+20,y,40,true);ctx.restore();
  const lines=sp.name.replace(' + ',' / ').split(' / '),width=infoW-48;
  lines.forEach((line,i)=>pcFontLeft(line,infoX+48,y+(i-(lines.length-1)/2)*13,pcFontFit(line,width,10,7),P.tint,a));
 }
}
;
