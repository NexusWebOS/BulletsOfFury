'use strict';
/* C113: all Chronos speech uses his approved portraits and the native compact
   panel. The existing director/radio owns typing, lifetime and combat clocks. */
const C113={base:{touch:XART._touch,dlg:dlgBox,contents:ui20PanelContents,portrait:ui20Portrait,world:drawWorld,load:stageLoadBegin},
 aliases:new Set(['fb2_hammer_avatar','fb1002_hammer_portrait','h3_hammer_portrait','cin30_cronos']),pose:null,last:null,draws:0,history:[]};
for(const a of Object.values(C113_ART.poses))Object.assign(XART._src,a.files);
function c113Who(who){return /^(?:CHRONOS|CRONOS)(?:\b|\s*[-–—])/i.test(String(who||''));}
function c113Key(key){return C113.aliases.has(key)||/^c11[23]_chronos_|^cp112_chronos_|^c113_/.test(String(key||''));}
function c113Pose(text,key){
 if(/^c112_chronos_/.test(key||'')){const pose=key.slice('c112_chronos_'.length);if(C113_ART.poses[pose])return pose;}
 const t=String(text||'').toUpperCase();
 if(/ARMOR|CHROMIUM|ACTIVAT|RAGE|POWER|FURIOUS|ENOUGH|TERMINAT/.test(t))return 'stern';
 if(/TRAP|LEGION|FOOL|DANCE|MORTAL/.test(t)&&!/WORTHY/.test(t))return 'turn_right';
 if(/DODGE|THIS CANNOT|WORTHY|CHAINGUN|WEAPON|SHOOT/.test(t))return 'turn_left';
 return 'neutral';
}
function c113Compact(pose='neutral',size=68){return C113_ART.poses[pose].compact[String(size)];}
function c113Warm(){for(const a of Object.values(C113_ART.poses))for(const k of Object.keys(a.files))XART.rdy(k);}
stageLoadBegin=function(n,keys){if(n===5)keys=[...(keys||[]),...Object.values(C113_ART.poses).flatMap(a=>Object.keys(a.files))];return C113.base.load.call(this,n,keys);};
XART._touch=function(key){if(C113.aliases.has(key))return C113.base.touch.call(this,C113_ART.poses[C113.pose||'neutral'].full);return C113.base.touch.apply(this,arguments);};
dlgBox=function(o){
 if(!o||(!c113Who(o.who)&&!c113Key(o.portraitKey)))return C113.base.dlg.apply(this,arguments);
 const old=C113.pose,pose=c113Pose(o.full,o.portraitKey);C113.pose=pose;c113Warm();
 const terminal=o.portraitKey==='sm10_hammer_portrait';
 try{return C113.base.dlg.call(this,{...o,portraitKey:terminal?o.portraitKey:c113Compact(pose)});}finally{C113.pose=old;}
};
ui20PanelContents=function(who,full,shown,port,r){
 if(!c113Who(who)&&!c113Key(port))return C113.base.contents.apply(this,arguments);
 const old=C113.pose,pose=old||c113Pose(full,port);C113.pose=pose;
 try{return C113.base.contents.call(this,who,full,shown,port==='sm10_hammer_portrait'?port:c113Compact(pose),r,arguments[5],arguments[6]);}finally{C113.pose=old;}
};
ui20Portrait=function(g,key,r){
 if(!r||!/^c113_/.test(key||''))return C113.base.portrait.apply(this,arguments);
 const pose=C113.pose||Object.keys(C113_ART.poses).find(p=>key.startsWith('c113_'+p+'_'))||'neutral';
 const size=C113_ART.sizes.find(n=>n<=Math.min(r.w,r.h));if(!size)return null;
 const actual=c113Compact(pose,size);if(!XART.rdy(actual)){c113Warm();return null;}
 const x=Math.round(r.x+(r.w-size)/2),y=Math.round(r.y+(r.h-size)/2);
 g.save();g.imageSmoothingEnabled=false;g.drawImage(XART.get(actual),x,y);g.restore();
 const result={x,y,w:size,h:size,key:actual,pose};C113.last=result;C113.draws++;
 C113.history.push({...result});if(C113.history.length>100)C113.history.shift();return result;
};
function c113Combat(){
 if(state!==GS.PLAY||run.stage!==5||!boss||boss.dead||fb2IntroActive()||fb2TalkActive()||H3.ending)return;
 const q=ui20Radio();if(!q||!c113Who(q.who))return;
 const current=BOFCinematicDirector.current,beat=current?.beats?.[current.i];
 const shown=beat?.text===q.text?Math.min(q.text.length,current.shown):Math.min(q.text.length,Math.floor(Math.max(0,q.age||0)*38));
 // The director already emitted the letter sounds. Keep the existing cursor
 // before the portrait panel draws, so it cannot restart typing or double-beep.
 dlgBox._tw={key:String(state)+'|'+q.who+'|'+q.text,count:shown,at:performance.now(),auto:false};
 dlgBox({who:q.who,full:q.text,shown:q.text.slice(0,shown),forceShown:true,portrait:false,pw:VW-20});
 C113.radio={text:q.text,who:q.who,shown,pose:c113Pose(q.text),live:!!current?.combatLive};
}
drawWorld=function(dt){const r=C113.base.world.apply(this,arguments);C113.radio=null;c113Combat();return r;};
globalThis.BOF_CHRONOS_DIALOGUE={state:C113,pose:c113Pose,warm:c113Warm,key:c113Compact};
// The four tiny dialogue cells are available even when a story preview starts
// outside Stage5. Full-resolution busts and other sizes keep normal lazy loads.
for(const a of Object.values(C113_ART.poses))XART.rdy(a.compact['68']);
