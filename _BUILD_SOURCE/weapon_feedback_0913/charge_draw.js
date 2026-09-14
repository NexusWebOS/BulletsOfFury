function drawChargeFX(){
  if(!player||player.dead||(!chargeWinding()&&!chargeDashing()))return;
  const d=player._chgDash,k=d?d.k:chargeLevel();if(k<=.02)return;
  if(d){
    const u=clamp(d.t/d.dur,0,1),f=Math.floor(d.t*28)%4;
    // Two authored exhaust reels dock at the aft hull; the nose remains clear.
    for(const side of [-1,1])weaponFeedbackArt('ndr_dambreaker_bottomthruster_'+f,player.x+side*15,player.y+39+20*k,24+10*k,66+65*k,.82*(1-u*.3),0,false);
    weaponFeedbackArt('jchg_3',player.x,player.y-23,52+26*k,22+12*k,.55*(1-u*.5),0,true);
  }else{
    const f=Math.min(3,Math.floor(k*4)),w=52+48*k;
    weaponFeedbackArt('jchg_'+f,player.x,player.y,w,w,.42+.35*k,0,true);
    if(k>=.995)weaponFeedbackArt('jchg_3',player.x,player.y,70,70,.20+.12*Math.sin(stateT*19),0,true);
  }
}
function drawWreckBalls(){
  if(!wreckBalls.length||!wreckActive()||!player||player.dead)return;
  wreckSync();
  for(const b of wreckBalls){
    const hot=b.hot>.35,kick=clamp((b._kick||0)/.07,0,1);
    ctx.save();if(hot){ctx.shadowColor='#ff9a3a';ctx.shadowBlur=7+6*b.hot;}
    // Full-opacity steel retains the authored rivets; recoil is visual, not orbital physics.
    weaponFeedbackArt(hot?'jwb_ball_hot':'jwb_ball',b.x,b.y,WB_DRAW*2*(1+.10*kick),null,1,b.a*1.7-kick*.18,false);
    ctx.restore();
  }
}
