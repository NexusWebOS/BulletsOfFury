from pathlib import Path
import sys,http.server
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='rough-riders-kaia-ricochet-live',stage=6,role='boss',kind='rebelsquad',name='Rough Riders / Kaia faster four-edge roller ricochets',limit=480,demonstrate=240)
rec.CAPTURE=rec.CAPTURE.replace(' const audio=Snd._audioCtx();',"""
 window.rr45Film={maxOverlap:0,frames:0,worst:null,maxIdleStep:0,last:{}};
 const rrTick=rebelSquadTick;rebelSquadTick=function(b,dt){const out=rrTick.apply(this,arguments);if(rr45Scope(b)&&(!rr33Protected(b)||['settle','dialogue'].includes(b._rebels.rough33?.phase))){const F=rr45Film,ss=b._rebels.ships.filter(q=>!q.dead&&q.y>PLAY.y-100&&q.y<VH+100&&q.x>camLeftX()-100&&q.x<camRightX()+100);F.frames++;for(let i=0;i<ss.length;i++)for(let j=i+1;j<ss.length;j++){const a=ss[i],b=ss[j],A=rr45Bounds(a),B=rr45Bounds(b),x=A.w+B.w+7-Math.abs(a.x-b.x),y=A.h+B.h+9-Math.abs(a.y-b.y);if(x>0&&y>0&&Math.min(x,y)>F.maxOverlap){F.maxOverlap=Math.min(x,y);F.worst={a:a.key,b:b.key,phase:a.rg4?.act?.phase||b.rg4?.act?.phase,x,y};}}for(const q of ss){const prev=F.last[q.key];if(prev&&!q.rg4?.act&&!prev.act&&q.mode==='fight')F.maxIdleStep=Math.max(F.maxIdleStep,Math.hypot(q.x-prev.x,q.y-prev.y));F.last[q.key]={x:q.x,y:q.y,act:!!q.rg4?.act};}}return out;};
 const rrBG=drawBG;drawBG=function(){const m=ctx.getTransform();window.rrFilmMatrix=[m.a,m.b,m.c,m.d,m.e,m.f];return rrBG.apply(this,arguments);};
 const audio=Snd._audioCtx();""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"defense:{audit:rr45Film,events:RR45.events.slice(-12),wall:rg4State()?.rr26?.wall?{t:rg4State().rr26.wall.t,hits:rg4State().rr26.wall.hits,gold:rg4State().rr26.wall._rr45}:null,returns:rg4State()?.rr26?.returns.length},steady:{active:RR43.scope(),camX,matrix:window.rrFilmMatrix},music:{path:Snd.cur?.currentSrc,stagexPaused:Snd.music.stagex?.paused},pilotActs:b?._rebels?.ships.map(q=>({key:q.key,x:q.x,y:q.y,act:q.rg4?.act?.kind,phase:q.rg4?.act?.phase,hp:q.hp})),target:reviewBot.targetInfo,")
rec.CAPTURE=rec.CAPTURE.replace('  K.j=!demonstrate',"  const multiKey=keybindFor(1).multilock?.[0];if(multiKey)K[multiKey]=elapsed>60;\n  K.j=!demonstrate")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"nyx:(()=>{const q=b?._rebels?.ships.find(q=>q.key==='nyx');return q?{hp:q.hp,max:q.max,hidden:q._ny46Hidden,revealing:q._ny46Revealing,fade:q._rr26Fade,events:NY46.events.slice(-5)}:null})(),target:reviewBot.targetInfo,")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"firing:{events:NY47.events.slice(-12),nyx:(()=>{const q=b?._rebels?.ships.find(q=>q.key==='nyx');return q?{x:q.x,y:q.y,visible:ny47Visible(q),phase:q.rg4?.act?.phase,hidden:ny46Hidden(q),rect:ny47Rect()}:null})()},target:reviewBot.targetInfo,")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"kaiaRollers:{dispatch:RD42.events.slice(-10),supply:(rg4State()?.rebelBoxes||[]).map(o=>({owner:o.key,x:o.x,y:o.y,kind:o.kind})),events:KR48.events.slice(-100),live:(rg4State()?.ord||[]).filter(o=>o._kr48).map(o=>({id:o._kr48,x:o.x,y:o.y,vx:o.vx,vy:o.vy,t:o.t,bounces:o.bounces})),bounds:{left:camLeftX()+24,right:camRightX()-24,top:PLAY.y+24,bottom:VH-24}},target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,480),flush=True)



