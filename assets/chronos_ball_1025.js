'use strict';
// Use the authored intermediate robot folds instead of the four-key unfold bank.
const C40={blue:ha21Blue};
ha21Blue=function(b){if(c25Own(b)&&!b.dead){const h=b._hammer,s=h.state;if(['curl','ball','uncurl'].includes(s)){
 const u=s==='ball'?1:s==='curl'?clamp(h.t/HAMMER_BALL_WARN,0,1):1-clamp(h.t/1.65,0,1);
 const poses=[0,4,5,6,7,8,9,10,12,13,14],ease=u*u*(3-2*u),f=poses[Math.min(poses.length-1,Math.floor(ease*poses.length))];
 const q=ha21Pose('blue_to_ball',(f+.01)/17,1.75,s==='ball'?(h.angle||0):0);return q;
 }}return C40.blue.apply(this,arguments);};
window.BOF_CHRONOS_BALL=C40;
