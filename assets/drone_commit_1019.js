"use strict";
/* A diagonal Sharddart crossed the firing field before its native charge could
   finish, even when followed on Furious. Let its first existing tell complete;
   movement and fire clocks retain their native owners, then the route resumes. */
const DC19={base:{tick:aiTick}};
aiTick=function(e,dt){
 const A=e?._ai,D=e?._dr;
 if(window.DC19_OFF===1||D?.slug!=='sharddart'||A?.kind!=='diag'||e._dc19Done)
  return DC19.base.tick.apply(this,arguments);
 if(D.phase==='recover'||(e._dc19Age||0)>=3){e._dc19Done=true;return DC19.base.tick.apply(this,arguments);}
 const visible=e.x>=camLeftX()+32&&e.x<=camRightX()-32&&e.y>=PLAY.y+8&&e.y<player.y-65;
 if(visible)e._dc19Commit=true;
 const x=e.x,y=e.y,r=DC19.base.tick.apply(this,arguments);
 if(e._dc19Commit&&['idle','tell','commit'].includes(D.phase)){
  // aiTick integrates these authored paths per frame. Scaling dt would only
  // change deceleration, so slow the actual integrated displacement instead.
  e.x=x;e.y=y+(e.y-y)*.30;e._dc19Age=(e._dc19Age||0)+dt;
 }
 return r;
};
window.BOF_DRONE_COMMIT={state:DC19};
