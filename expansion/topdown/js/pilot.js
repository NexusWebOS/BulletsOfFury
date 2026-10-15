/* Same full-body / vehicle selection bays and framed avatars as the base game,
 * with twelve unlocked expansion pilots in two horizontal rows of six. */
(function(root){
  'use strict';
  const TD=root.TD;
  TD.PILOT_INFO={
    cole:['#7ad63a','SONIC BOOM / WARHEAD','FLIGHT MASTER'],axel:['#3a8aff','MEGA SHIELD','COMMANDER'],maverick:['#3ad6c8','HELIX BEAM','VENOM STRIKE'],
    decker:['#ffd24a','CLOAKING SYSTEM','TECH CONNOISSEUR'],yuri:['#e23a3a','CHAIN LIGHTNING','LIGHTNING STRIKE'],freezer:['#6fd0ff','TIME FREEZE + THERMOSHOCK','FROSTBITE'],
    juggernaut:['#c08a3a','WRECKING BALL','UNSTOPPABLE'],lizzie:['#ffc21a','ATOM BOMB + HEAVY TURRET','BOMBSHELL'],falva:['#ff2a8f','ROLLER BALL','THE OG'],
    hotwire:['#ffb458','FIBER WHIP','Compound mechanic'],phoenix:['#ff6454','ARMAGEDDON','Compound defender'],niel:['#76f4c1','WINDSTORM','Wind specialist'],
  };
  TD.PILOT_WARM=TD.PILOTS.flatMap(p=>['pav_'+p,'select_body_'+p,'pt_'+p+'_hull','pt_'+p+'_turret']);
  TD.pilotRects=[];
  function fit(ctx,key,x,y,w,h){const g=ART.get(key);if(g)ART.draw(ctx,key,x,y,{s:Math.min(w/g.sw,h/g.sh)});}
  function panel(ctx,x,y,w,h,col,glow){ctx.save();ctx.fillStyle='rgba(8,11,18,.78)';ctx.fillRect(x,y,w,h);ctx.strokeStyle=glow?col:'rgba(120,140,170,.45)';ctx.lineWidth=glow?2:1;if(glow){ctx.shadowColor=col;ctx.shadowBlur=7;}ctx.strokeRect(x+.5,y+.5,w-1,h-1);ctx.restore();}
  TD.drawPilotSelect=function(ctx,text,G){
    const pk=TD.pilot,info=TD.PILOT_INFO[pk],col=info[0],t=G.t/60;
    ctx.fillStyle='#08080e';ctx.fillRect(0,0,480,360);
    const gradient=ctx.createLinearGradient(0,0,0,360);gradient.addColorStop(0,col+'18');gradient.addColorStop(.45,col+'60');gradient.addColorStop(1,col+'08');ctx.fillStyle=gradient;ctx.fillRect(0,0,480,360);
    text('CHOOSE YOUR PILOT!',240,21,19,'#f2f5ff','center');
    panel(ctx,16,39,448,170,col,true);panel(ctx,22,45,205,158,col,false);panel(ctx,237,45,221,158,col,false);
    fit(ctx,'select_body_'+pk,124,124,190,149);
    TD.drawPlayerTank(ctx,{pilot:pk,x:348,y:104,a:Math.PI+Math.sin(t*1.4)*.4,aim:Math.PI+Math.sin(t*.9)*.6,hp:1,max:1});
    text(pk.toUpperCase(),348,149,17,col,'center');text(info[2].toUpperCase(),348,168,8,'#dbe8f3','center');
    const label='SPECIAL: '+info[1];ctx.font='bold 9px BOFCommand, monospace';const size=Math.min(9,9*205/ctx.measureText(label).width);text(label,348,188,size,col,'center');
    TD.pilotRects=[];
    TD.PILOTS.forEach((p,i)=>{const x=24+(i%6)*73,y=218+Math.floor(i/6)*61,on=p===pk,c=TD.PILOT_INFO[p][0];TD.pilotRects.push([x,y,67,57]);
      panel(ctx,x,y,67,57,c,on);fit(ctx,'pav_'+p,x+33.5,y+23,45,45);text(p.toUpperCase(),x+33.5,y+51,7,on?'#fff':'#9aa8ba','center');
    });
    ART.draw(ctx,'pad_dpad',151,349,{s:.07});text('PILOT',177,349,8,'#dbe8f3');ART.draw(ctx,'pad_start',272,349,{s:.09});text('SELECT',299,349,8,'#dbe8f3');
  };
}(window));
