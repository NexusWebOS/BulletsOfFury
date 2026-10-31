/* Overdrive debrief uses the campaign's existing score, rank and password owners. */
(function(root){
 'use strict';const TD=root.TD,A=TD.AssaultArt;
 const fit=(ctx,key,x,y,w,h)=>{const g=ART.get(key);if(g)ART.draw(ctx,key,x,y,{s:Math.min(w/g.sw,h/g.sh)});};
 TD.Results39={draw(ctx,text,G){
  const R=G.results;if(!R||!ART.get('od39_results_backplate'))return false;
  const w=TD.VW,h=TD.VH;ctx.save();ctx.scale(w/640,h/480);ctx.fillStyle='#03070c';ctx.fillRect(0,0,640,480);A.draw(ctx,'od39_results_backplate',0,0,{s:640/1448});
  fit(ctx,'logo',320,39,302,62);fit(ctx,'overdrive',320,74,192,27);text('LEVEL '+(TD.MISSIONS.find(m=>m.id===G.mission)?.displayNumber||G.mission)+' / MISSION COMPLETE',320,95,12,'#c1fff0','center');
  const mins=Math.floor(R.time/60),secs=String(Math.floor(R.time%60)).padStart(2,'0');
  const extras=(R.extraRows||[]).slice(0,3),rows=[['TIME',mins+':'+secs],['ENEMIES DESTROYED',R.kills],['DEATHS',R.deaths],['TIME BONUS',R.timeBonus],['NO-DEATH BONUS',R.noDeath],...extras,['TOTAL SCORE',G.score]],pitch=Math.min(27,230/rows.length);
  rows.forEach(([label,value],i)=>{if(G.stateT<.2+i*.12)return;const y=145+i*pitch,last=i===rows.length-1;text(label,39,y,last?12:10,last?'#ffcb71':'#a8d7df');text(String(value),384,y,last?15:12,last?'#fff2ad':'#fff','right');});
  fit(ctx,'pav_'+(G.player?.pilot||TD.pilot),510,192,104,106);text('OPERATION RANK',510,126,10,'#ffcf88','center');if(G.stateT>.8)fit(ctx,'rank_'+R.rank,510,291,120,106);
  text('OVERDRIVE PASSWORD',320,405,10,'#a7d8db','center');text(String(R.password||'').toUpperCase(),320,426,17,'#ffe39a','center');
  if(G.stateT>2.5&&Math.floor(G.t/30)%2===0)fit(ctx,'pad_start',320,458,52,22);ctx.restore();return true;
 }};
})(window);
