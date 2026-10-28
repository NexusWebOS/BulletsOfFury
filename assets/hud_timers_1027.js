'use strict';
/* Stage completion and encounter clocks live outside the playfield. This owner
   observes native simulation updates; it never advances waves, health or phases. */
const HUD28={stage:null,encounter:null,serial:0,draws:0,portrait:{x:70,y:74,w:228,h:228},
 base:{begin:beginStage,update:updatePlay,state:setState,fit:SC12.fit,render:SC12.render},
 art:{wide:'hud28_timer_wide',compact:'hud28_timer_compact'}};
XART._src.hud28_right='assets/game/shared/ui/hud_timers_1027/hud-right-square.png?v=square-clocks-1027';
XART._src.hud28_timer_wide='assets/game/shared/ui/hud_timers_1027/timer-376.png';
XART._src.hud28_timer_compact='assets/game/shared/ui/hud_timers_1027/timer-480.png';
UI20_KEYS.push('hud28_right');
for(const k of [...Object.values(HUD28.art),'hud28_right'])XART.rdy(k);
function hud28Reset(n){HUD28.stage={stage:n,seconds:0,finished:false,serial:++HUD28.serial};HUD28.encounter=null;}
function hud28StageSeconds(){return HUD28.stage?.seconds??0;}
function hud28ClockTick(dt){
 if(!(Number.isFinite(dt)&&dt>0)||state!==GS.PLAY)return;
 if(!HUD28.stage||HUD28.stage.stage!==run.stage)hud28Reset(run.stage);
 if(!HUD28.stage.finished)HUD28.stage.seconds+=dt;
 const b=bossActive&&boss&&!boss.dead?boss:subBossActive&&subBoss&&!subBoss.dead?subBoss:null;
 if(b){if(!HUD28.encounter||HUD28.encounter.actor!==b)HUD28.encounter={actor:b,kind:b===boss?'BOSS':'MINIBOSS',seconds:0,finished:false};
  HUD28.encounter.seconds+=dt;
 }else if(HUD28.encounter)HUD28.encounter.finished=true;
}
beginStage=function(n){const r=HUD28.base.begin.apply(this,arguments);hud28Reset(n);return r;};
updatePlay=function(dt){const previous=HUD28.stage,was=state;const out=HUD28.base.update.apply(this,arguments);
 if(was===GS.PLAY&&state===GS.PLAY&&(previous===HUD28.stage||!previous))hud28ClockTick(dt);
 else if(was===GS.PLAY&&HUD28.stage&&['flyover','outbound'].includes(state))HUD28.stage.finished=true;
 return out;
};
const HUD28_HOST=document.getElementById('room');
HUD28.canvases=['stage','encounter','compact'].map((name,i)=>{const c=document.createElement('canvas');c.id='hud28-'+name;c.width=i===2?960:376;c.height=88;Object.assign(c.style,{position:'fixed',display:'none',pointerEvents:'none',zIndex:'8',imageRendering:'pixelated'});HUD28_HOST.appendChild(c);return c;});
function hud28Position(vw=innerWidth,vh=innerHeight){
 const [left,right,compact]=HUD28.canvases,active=SC12.active();if(!active||!SC12.layout){for(const c of HUD28.canvases)c.style.display='none';return;}
 const rows=seatList().length;HUD28.mode=SC12.mode;
 if(SC12.mode==='sides'){
  compact.style.display='none';const field=SC12.layout.field,roomW=(vw-field.w)/2-12,k=Math.min((vh-64)/(1024*rows+88),roomW/376),w=376*k,h=1024*rows*k,top=64+(vh-64-h-88*k)/2;
  for(const [i,c]of SC12.panels.entries()){const x=i?field.x+field.w+6:field.x-w-6;Object.assign(c.style,{width:w+'px',height:h+'px',top:top+88*k+'px',left:x+'px'});Object.assign(HUD28.canvases[i].style,{display:'block',left:x+'px',top:top+'px',width:w+'px',height:88*k+'px'});}
 }else{
  left.style.display=right.style.display='none';const k=Math.min(vw/VW,vh/(VH+196*rows+44)),w=VW*k,h=VH*k,x=(vw-w)/2,y=(vh-(VH+196*rows+44)*k)/2;
  for(const el of [document.getElementById('game-frame'),document.getElementById('screen-area'),cv])Object.assign(el.style,{width:w+'px',height:h+'px'});
  Object.assign(document.getElementById('game-frame').style,{left:x+'px',top:y+'px'});Object.assign(compact.style,{display:'block',left:x+'px',top:y+h+'px',width:w+'px',height:44*k+'px'});
  Object.assign(SC12.compact.style,{left:x+'px',top:y+h+44*k+'px',width:w+'px',height:196*rows*k+'px'});SC12.layout.field={x,y,w,h};
 }
 HUD28.layout={mode:SC12.mode,headers:HUD28.canvases.map(c=>{const r=c.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,visible:c.style.display!=='none'};})};
}
SC12.fit=function(){const r=HUD28.base.fit.apply(this,arguments);hud28Position(...arguments);return r;};
setState=function(){const r=HUD28.base.state.apply(this,arguments);hud28Position();return r;};
function hud28Text(g,s,x,y,h,w,palette='chrome'){
 if(typeof pm27Live==='function'&&pm27Live())return pm27Draw(g,s,x,y,h,{family:'command',palette,width:w});
 return ui20Text(g,s,x,y,h,w);
}
function hud28Header(g,x,w,label,value){const key=w===480?HUD28.art.compact:HUD28.art.wide;if(!XART.rdy(key))return;
 g.drawImage(XART.get(key),x,0);hud28Text(g,label,x+w/2,17,18,w-44);hud28Text(g,value,x+w/2,54,28,w-56,'gold');
}
function hud28DrawClocks(){
 if(!SC12.active()){for(const c of HUD28.canvases)c.style.display='none';return;}
 const E=HUD28.encounter,stage=encounterClockText(hud28StageSeconds()),fight=E?encounterClockText(E.seconds):'00:00';
 const label=E?E.kind:'ENCOUNTER';HUD28.values={stage:HUD28.stage?.stage??run.stage,stageSeconds:hud28StageSeconds(),stageText:stage,encounterLabel:label,encounterSeconds:E?.seconds??null,encounterText:fight,encounterFinished:!!E?.finished};
 if(SC12.mode==='sides')for(let i=0;i<2;i++){const g=HUD28.canvases[i].getContext('2d');g.clearRect(0,0,376,88);g.imageSmoothingEnabled=false;hud28Header(g,0,376,i?label:'STAGE COMPLETION',i?fight:stage);}
 else{const g=HUD28.canvases[2].getContext('2d');g.clearRect(0,0,960,88);g.imageSmoothingEnabled=false;hud28Header(g,0,480,'STAGE COMPLETION',stage);hud28Header(g,480,480,label,fight);}
 HUD28.draws++;
}
SC12.render=function(){const r=HUD28.base.render.apply(this,arguments);hud28DrawClocks();return r;};
UI20.dirty=true;window.__bofFit();globalThis.BOF_HUD_TIMERS_1027=HUD28;
