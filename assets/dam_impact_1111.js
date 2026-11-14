'use strict';
/* H127: Stage1's dying helicopter impacts the actual authored central dam gate.
   Both terrain states register; their swap is hidden by authored white frames. */
const H127={base:{load:stageLoadBegin,start:h126Start,position:h126Position,update:updateBoss,master:drawLevelMaster,world:drawWorld,begin:beginStage},events:[],draws:0};
for(const[k,a]of Object.entries(H127_ART.pages))XART._src[k]=a.path;
function h127Keys(){return [...Object.keys(H127_ART.pages),'bg_stage01_intact','bg_stage01_destroyed'];}
stageLoadBegin=function(n,keys){return H127.base.load.call(this,n,n===1?[...(keys||[]),...h127Keys()]:keys);};
function h127Own(){const D=boss?._h126;return run.stage===1&&D?.kind==='stage1'&&D.dam?D:null;}
function h127Log(D,event,data={}){H127.events.push({event,t:D.t,...data});if(H127.events.length>160)H127.events.shift();}
function h127Ease(u){u=clamp(u,0,1);return u*u*(3-2*u);}
h126Start=function(b,kind,mask){const D=H127.base.start.apply(this,arguments);if(kind!=='stage1')return D;const cfg=_levelCfg(),height=cfg.h||4212,winH=Math.round(viewH()),range=cfg.scrollLen||Math.max(0,height-VH),rangeSrc=Math.max(0,height-winH),from=clamp(mapScroll,0,range),target=Math.max(from,range*(1-H127_ART.dam.target_src_y/Math.max(1,rangeSrc))),finalSrc=rangeSrc*(1-target/Math.max(1,range)),top=Math.round(viewTopY()),rise=H126.reduced?.42:.16,hold=H126.reduced?.16:.18,fall=H126.reduced?1.0:1.18;
 D.dam={from,target,range,rangeSrc,source:H127_ART.dam.source.slice(),impact:{x:340,y:286-finalSrc+top},staging:{x:clamp(D.origin.x+60,D.L+110,D.R-110),y:VH-160},rise,hold,fall,flashAt:D.blast-.02};D.damSwapAt=D.dam.flashAt+rise+.04;h127Log(D,'dam-approach',{scrollFrom:from,scrollTarget:target,source:D.dam.source,impact:D.dam.impact,swapAt:D.damSwapAt});return D;
};
h126Position=function(D,t,u,targetX,targetY){if(!D.dam)return H127.base.position.apply(this,arguments);const S=D.dam,wait=3.8;if(t<1.1){const k=h127Ease(t/1.1);return{x:lerp(D.origin.x,S.staging.x,k)+Math.sin(t*5)*8*Math.sin(Math.PI*k),y:lerp(D.origin.y,S.staging.y,k)};}if(t<wait)return{x:S.staging.x+Math.sin(t*5)*18,y:S.staging.y+Math.sin(t*4)*11};const k=h127Ease((t-wait)/(D.blast-wait));return{x:lerp(S.staging.x,S.impact.x,k)+Math.sin(t*5)*25*(1-k),y:lerp(S.staging.y,S.impact.y,k)+Math.sin(t*4)*14*(1-k)};};
function h127Level(D){const S=D.dam,t=D.t-S.flashAt;if(t<0||t>=S.rise+S.hold+S.fall)return 0;if(t<S.rise)return Math.round(h127Ease(t/S.rise)*32);if(t<S.rise+S.hold)return 32;return Math.round((1-h127Ease((t-S.rise-S.hold)/S.fall))*32);}
updateBoss=function(dt){const D=h127Own();if(D&&!D.finished){const now=D.t+clamp(dt||0,0,.05),s=h127Ease(now/3.6);mapScroll=Math.min(D.dam.range,Math.max(mapScroll,lerp(D.dam.from,D.dam.target,s)));}const intact=!damBroken,out=H127.base.update.apply(this,arguments);if(D){if(!D.dam.hit&&D.shattered){D.dam.hit=true;h127Log(D,'dam-impact',{x:D.final.x,y:D.final.y});}if(intact&&damBroken)h127Log(D,'dam-swap',{flash:h127Level(D),scroll:mapScroll});if(!D.dam.revealed&&D.t>D.dam.flashAt+D.dam.rise+D.dam.hold&&h127Level(D)===0){D.dam.revealed=true;h127Log(D,'dam-revealed');}}return out;};
drawLevelMaster=function(dt){const D=h127Own();return H127.base.master.call(this,D&&!D.finished?0:dt);};
drawWorld=function(){const out=H127.base.world.apply(this,arguments),D=h127Own();if(!D)return out;const level=h127Level(D);if(level){const a=H127_ART.frames[level],im=XART.get(a.key);if(im){ctx.drawImage(im,...a.rect,0,0,480,512);H127.draws++;}}return out;};
beginStage=function(){H127.events.length=0;return H127.base.begin.apply(this,arguments);};
globalThis.BOF_DAM_IMPACT_1111=H127;
