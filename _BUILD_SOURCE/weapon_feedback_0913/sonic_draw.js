function sonicDraw(){
  if(typeof XART==='undefined')return;
  if(sonicActive()&&!player.dead&&(run._sonicChg||0)>0){
    const p=clamp(run._sonicChg/SONIC_MAX,0,1),t=run._sonicChg;
    const pulse=(t*2.9)%1,w=62-26*p-12*pulse;
    // Authored compression rings cycle inward around the hull while pressure builds.
    weaponFeedbackArt('nsw_circ_'+Math.min(3,Math.floor(p*4)),player.x,player.y-10,w,w,.35+.45*p,0,true);
    weaponFeedbackArt('nsw_ring_3',player.x,player.y-10,w+14*(1-pulse),w+14*(1-pulse),(.16+.24*p)*(1-pulse),0,true);
    if(p>=.995)weaponFeedbackArt('nsw_circ_3',player.x,player.y-10,42,42,.28+.15*Math.sin(stateT*18),0,true);
  }
  for(const s of sonicTrail){
    const u=clamp(s.t/s.dur,0,1),fi=Math.min(3,Math.floor(u*4));
    const key=s.imp?'ndk_imp_'+fi:s.circ?'nsw_circ_'+fi:'nsw_dist_'+fi;
    const p=clamp(s.p||0,0,1),w=s.imp?46*(.8+u*.5):s.circ?(s.hit?38:50)*(1+p*.65)*(.7+u*.65):(s.w||48)*(1+u*.22);
    const h=s.imp||s.circ?w:18+12*p;
    weaponFeedbackArt(key,s.x,s.y,w,h,(s.hit?.72:s.circ?.56:.30)*(1-u),0,true);
  }
}
