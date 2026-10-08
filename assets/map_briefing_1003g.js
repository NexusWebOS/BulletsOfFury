'use strict';
/* October 3: blank authored panels, centered live copy and a fixed Lizzie portrait bezel. */
const MAPG_BRIEFINGS=[
 'INFILTRATE THE JUNGLE AIRSTRIP. DESTROY THE OCCUPATION FORCES AND BREAK THE DAM.',
 'PUSH THROUGH THE VOLCANIC FOUNDRY BEFORE THE MAGMA DEFENSE GRID ERUPTS.',
 'SURVIVE THE GLACIER CITADEL AND SHATTER ITS CRYO WAR MACHINES.',
 'REACH THE MISSILE AIRBASE AND SILENCE EVERY LAUNCH BATTERY.',
 'TAKE THE WAR INTO ORBIT AND CRUSH THE UNITY FLEET.',
 'ENTER THE STORM FRONT. OUTRUN THE HUNTERS AND THEIR HOMING MISSILES.',
 'DESCEND INTO THE TOXIC SEWER WORKS AND DESTROY THE BIO-SLUDGE CORE.',
 'ASSAULT THE DEATH RUINS AND END FURIOUS DEATH.',
 'ENTER THE SECRET RIFT EARNED THROUGH THE STAGE 5 GATE RUN.'
];
XART._src.mapg_briefing='assets/game/shared/campaign/map_briefing_1003g/briefing_blank.png';
XART._src.mapg_lizzie_frame='assets/game/shared/campaign/map_briefing_1003g/lizzie_frame.png';
XART._src.mapg_lizzie_source='assets/game/pilots/lizzie/portraits/pilots_0922/sheets/lizzie_expressions.png';
const MAPG={typing:null,rect:{x:12,y:390,w:456,h:98},panelSource:[0,98,2170,484],portraitCache:new Map()};
function mapgWarm(){for(const k of ['mapg_briefing','mapg_lizzie_frame','mapg_lizzie_source'])XART.rdy(k);}
const MAPG_OPEN=openStageSelect;
openStageSelect=function(){MAPG.typing=null;mapgWarm();return MAPG_OPEN.apply(this,arguments);};
function mapgCopy(stage){const s=STAGES[stage-1];return s?{key:String(stage),title:s.name+' - '+s.sub,body:MAPG_BRIEFINGS[stage-1]}:null;}
function mapgReveal(copy,now,ready){
 if(!MAPG.typing||MAPG.typing.key!==copy.key)MAPG.typing={key:copy.key,at:now,count:0};
 const t=MAPG.typing;if(!ready)t.at=now;
 t.count=ready?Math.min(copy.title.length+copy.body.length,Math.floor(Math.max(0,now-t.at)*.043)):0;
 return t.count;
}
function mapgBriefingDraw(stage){
 const copy=typeof stage==='object'?stage:mapgCopy(stage);if(!copy)return;
 const ready=XART.rdy('mapg_briefing')&&bmfReady('game')&&bmfReady('dialogue');
 const count=mapgReveal(copy,performance.now(),ready);if(!ready)return;
 const r=MAPG.rect;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get('mapg_briefing'),...MAPG.panelSource,r.x,r.y,r.w,r.h);
 const prior=_msgFace;msgFaceUse('game');
 msgDrawBlock({text:copy.title,budget:count,x:r.x+18,y:r.y+12,w:r.w-36,h:29,maxH:15,minH:10,
   color:'#ffe7a0',align:'center',stableCenter:true,valign:'middle',lineMul:1.15});
 msgFaceUse('dialogue');
 msgDrawBlock({text:copy.body,budget:Math.max(0,count-copy.title.length),x:r.x+22,y:r.y+47,w:r.w-44,h:35,maxH:11,minH:9,
   color:'#ffe7a0',align:'center',stableCenter:true,valign:'middle',lineMul:1.3});
 msgFaceUse(prior);ctx.restore();
}
/* The generated sheet's columns overlap decorative rails and are not equal quarters.
   Keep the approved likeness and pose pixels. Draw its full interior into one new
   complete bezel. Talk cells replace ONLY the mouth, never the body, frame or anchor. */
const MAPG_LIZZIE={
 idle:[29,34,325,302],happy:[378,34,316,302],laugh:[753,34,325,302],anger:[1100,34,316,302],
 sad:[29,398,325,300],crash:[378,398,316,300],victory:[753,398,325,300],
 mouths:{'talk-small':[168,884,48,43],'talk-medium':[501,884,48,43],
   'talk-wide':[892,884,48,43],'talk-o':[1219,884,48,43]}
};
function mapgLizzieCell(em,comm){
 const id=em+':'+comm;if(MAPG.portraitCache.has(id))return MAPG.portraitCache.get(id);
 if(!XART.rdy('mapg_lizzie_source')||!XART.rdy('mapg_lizzie_frame'))return null;
 const source=XART.get('mapg_lizzie_source'),frame=XART.get('mapg_lizzie_frame');
 const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(comm){g.translate(256,0);g.scale(-1,1);}
 g.drawImage(frame,31,45,1191,1167,0,0,256,256);
 g.save();g.beginPath();g.moveTo(45,25);g.lineTo(211,25);g.lineTo(232,46);g.lineTo(232,211);
 g.lineTo(211,234);g.lineTo(45,234);g.lineTo(24,211);g.lineTo(24,46);g.closePath();g.clip();
 const rect=MAPG_LIZZIE[em]||MAPG_LIZZIE.idle;
 g.drawImage(source,...rect,24,25,208,209);
 const mouth=MAPG_LIZZIE.mouths[em];
 if(mouth){const sx=208/325,sy=209/302;g.drawImage(source,...mouth,24+(168-29)*sx,25+(160-34)*sy,48*sx,43*sy);}
 g.restore();c.complete=true;c.naturalWidth=c.naturalHeight=256;MAPG.portraitCache.set(id,c);return c;
}
const MAPG_TOUCH=XART._touch;
XART._touch=function(k){
 const m=/^(comm_lizzie_|port_cf_lizzie_|port_lizzie_)(.+)$/.exec(k||'');
 if(m||k==='face_lizzie'){
  let em=m?m[2]:'idle';if(em==='smile')em='happy';if(em==='alert')em='crash';
  return mapgLizzieCell(em,!!m&&m[1]==='comm_lizzie_');
 }
 return MAPG_TOUCH.apply(this,arguments);
};
mapgWarm();
