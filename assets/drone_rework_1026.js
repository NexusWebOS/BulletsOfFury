'use strict';
/* Mike Oct26: stage warp -> palette darkening -> arena -> amethyst gate ->
   real drone -> synthetic code/1015 charge -> covering white flash -> host. */
const RD29={base:{spawn:spawnBoss,tick:r30Tick,draw:r30DrawBoss,bg:drawBG,world:drawWorld,arena:v17ArenaDraw,load:stageLoadBegin},events:[],last:null,bgPass:null,background:null,skin:null};
XART._src[RD29_ART.key]=RD29_ART.path;
function rd29Own(b){return rb23Host(b)&&['dr5er23entry','v18arrival','v18conversion'].includes(b._r30.mode);}
function rd29Init(b){const N=b._r30.v18;N.rb23Entrance=null;
 return N.rd29||(N.rd29={home:{...N.home},ships:null,flags:{},time:0,crackle:-1});}
function rd29Time(b){const S=b._r30;return S.mode==='dr5er23entry'?S.t:S.mode==='v18arrival'?7.2+S.t:S.mode==='v18conversion'?9+S.t:16.8+S.t;}
function rd29Log(b,event,data={}){RD29.events.push({event,time:rd29Time(b),...data});}
function rd29Cue(b,key,at,name,gain=1){const R=rd29Init(b);if(rd29Time(b)<at||R.flags[key])return;
 R.flags[key]=true;Snd.play(name,gain);rd29Log(b,key,{cue:name});}
spawnBoss=function(){const out=RD29.base.spawn.apply(this,arguments);if(rd29Own(boss))rd29Init(boss);return out;};
stageLoadBegin=function(n,keys){if(n===8)for(const k of ['combatEnergy0927','warpGate','combatAlien0927','combatModule0927','bossWeaponCharge','crackle','expBig','dracodiaShriek'])Snd.prepare(k);
 return RD29.base.load.call(this,n,[...(keys||[]),...(n===8?[...PL11.keys('amethyst_gate'),RD29_ART.key]:[])]);};
function rd29Ready(){return PL11.ready('amethyst_gate',XART)&&XART.rdy(RD29_ART.key)&&rd28Ready();}
r30Tick=function(b,dt){if(!rd29Own(b))return RD29.base.tick.apply(this,arguments);
 dt=clamp(dt||0,0,.05);const R=rd29Init(b),S=b._r30,N=S.v18;
 if(!R.ships)R.ships=seatList().map(seat=>withSeat(seat,()=>({seat,x:player.x,y:player.y})));
 dr5Protect(b,dt);b._noHit=true;N.attack=null;R.time=rd29Time(b);
 for(const q of R.ships)withSeat(q.seat,()=>{player.x=q.x;player.y=q.y;});
 if(S.mode==='dr5er23entry'){
  rd29Cue(b,'background-warp',0,'combatEnergy0927',.45);
  if(S.t>=3.4&&!R.flags.arena){R.flags.arena=true;N.arenaPhase=0;rb23Log('arena-teleported',{style:'background-warp-no-ship-teleport'});rd29Log(b,'arena-palette-handoff');}
  rd29Cue(b,'amethyst-gate-opens',5.4,'warpGate',.8);
  if(S.t>=7.2){b.x=R.home.x;b.y=viewTopY()+170;v18SetMode(b,'v18arrival');rd29Log(b,'drone-emerges');}
 }else if(S.mode==='v18arrival'){
  const u=rd25Ease(S.t/1.8);b.x=R.home.x;b.y=lerp(viewTopY()+170,R.home.y,u);
  rd29Cue(b,'drone-mechanical-emergence',7.2,'combatModule0927',.45);
  if(S.t>=1.8){v18SetMode(b,'v18conversion');dr5Say(b,run.pilot.toUpperCase(),'The drone... something is taking it over!');rd29Log(b,'synthetic-conversion-start');}
 }else{
  const t=S.t,power=clamp((t-.4)/4.8,0,1),amp=t<5.75?power*power*7:0;
  b.x=R.home.x+Math.sin(t*73)*amp;b.y=R.home.y+Math.sin(t*61)*amp*.65;shake=Math.max(shake,amp*.35);
  rd29Cue(b,'synthetic-code-rises',9,'combatAlien0927',.7);
  rd29Cue(b,'drone-charge',11.2,'bossWeaponCharge',.8);
  if(t>1&&t<5.75){const beat=Math.floor(t*(3+power*4));if(beat!==R.crackle){R.crackle=beat;Snd.play('crackle',.20+.45*power);}}
  if(t>=5.3)dr5State(b).radio=null;
  rd29Cue(b,'covering-white-impact',14.75,'expBig',1);
  rd29Cue(b,'infused-host-reveal',15.4,'dracodiaShriek',.9);
  if(t>=5.75){b.x=R.home.x+Math.sin(S.clock*.65)*Math.min(24,viewW()*.04);b.y=R.home.y+Math.sin(S.clock*.9)*5;}
  if(t>=7.8){RD28.last=null;dr5State(b).radio=null;v18Fight(b);rd29Log(b,'native-phase1-fight');}
 }
};
v17ArenaDraw=function(b){if(rd29Own(b)&&b._r30.mode==='dr5er23entry'&&RD29.bgPass==='old')return false;return RD29.base.arena.apply(this,arguments);};aa5ArenaDraw=v17ArenaDraw;
drawBG=function(dt){const b=boss;if(!rd29Own(b)||b._r30.mode!=='dr5er23entry')return RD29.base.bg.apply(this,arguments);
 const t=b._r30.t,old=t<3.4;RD29.bgPass=old?'old':'new';let out;
 try{out=RD29.base.bg.apply(this,arguments);}finally{RD29.bgPass=null;}
 const left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),m=ctx.getTransform(),c=RD29.background||(RD29.background=document.createElement('canvas')),
  W=Math.ceil(w/2)*2,H=Math.ceil(h/2)*2;if(c.width!==W||c.height!==H){c.width=W;c.height=H;}
 const g=c.getContext('2d');g.globalAlpha=1;g.globalCompositeOperation='source-over';g.clearRect(0,0,W,H);
 g.drawImage(ctx.canvas,left*m.a+m.e,top*m.d+m.f,w*m.a,h*m.d,0,0,W,H);
 const cycle=['#9a41b8','#5e55ce','#ce426d','#5565ba','#ab3dba','#58386f'],level=old?Math.floor((1-clamp((t-1.2)/2.2,0,1))*24)/24:Math.floor(clamp((t-3.4)/2,0,1)*24)/24;
 if(old){g.globalCompositeOperation='color';g.globalAlpha=clamp(t/.7,0,1)*.85;g.fillStyle=cycle[Math.floor(t*6)%cycle.length];g.fillRect(0,0,W,H);g.globalAlpha=1;}
 g.globalCompositeOperation='multiply';const gray=Math.round(255*level);g.fillStyle='rgb('+gray+','+gray+','+gray+')';g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';
 const drive=old?clamp(t/1.8,0,1):0;ctx.save();ctx.beginPath();ctx.rect(left,top,w,h);ctx.clip();ctx.fillStyle='#000';ctx.fillRect(left,top,w,h);ctx.imageSmoothingEnabled=false;
 for(let y=0;y<H;y+=4){const offset=(Math.sin(y*.045+t*(3+drive*7))*24+Math.sin(y*.014-t*5)*12)*drive,
  scale=1+drive*.11*Math.sin(t*3+y*.016);for(const repeat of [-1,0,1])ctx.drawImage(c,0,y,W,Math.min(4,H-y),left+offset+repeat*w*scale-w*(scale-1)/2,top+y*h/H,w*scale,4*h/H+.1);}
 ctx.restore();RD29.backgroundLast={time:t,source:old?'current-stage':'new-arena',level,warp:drive*36,palette:old?Math.floor(t*6)%6:null};return out;
};
function rd29White(t){if(t<5.3)return 0;if(t<5.75)return Math.floor((t-5.3)/.45*16);if(t<6.1)return 16;return 16-Math.floor(clamp((t-6.1)/1.6,0,1)*16);}
function rd29Code(b){const t=b._r30.t,S=rd28State(b,b.x,b.y,6.2+t*1.4),absorb=clamp((t-4.4)/1.35,0,1);
 return{...S,y:b.y,height:270*(1-absorb*.35),absorb,alpha:clamp((t-.2)/.65,0,1)*(1-absorb*.75)};
}
function rd29CodeSkin(b,size){const c=RD29.skin||(RD29.skin=document.createElement('canvas'));if(c.width!==256)c.width=c.height=256;
 const g=c.getContext('2d'),a=RD28.sources.code[Math.floor(b._r30.t*12)%12],scroll=(b._r30.t*72)%256;
 g.clearRect(0,0,256,256);g.globalCompositeOperation='source-over';g.imageSmoothingEnabled=false;
 for(let x=0;x<256;x+=64)for(const y of [-256,0,256])g.drawImage(rd28Image(a),149,96,64,256,x,y-scroll,64,256);
 g.globalCompositeOperation='destination-in';g.drawImage(XART.get(V18_ART.drone.key),0,0);g.globalCompositeOperation='source-over';
 ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=.15+.5*clamp(b._r30.t/5,0,1);ctx.drawImage(c,b.x-size/2,b.y-size/2,size,size);ctx.restore();
}
function rd29Drone(b,size,charge=false){const t=b._r30.t,power=charge?clamp((t-.4)/4.8,0,1):0,
 level=charge?pxgStep(power*(.8+.2*Math.sin(t*(6+power*12)))):0,blink=charge&&t>3.7&&Math.floor((t-3.7)*(7+power*10))%3===0,
 image=blink?xartTint(V18_ART.drone.key,'#ffffff',1):XART.get(V18_ART.drone.key),active=PXG.active;
 PXG.active=null;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(image,b.x-size/2,b.y-size/2,size,size);
 if(level){ctx.globalCompositeOperation='lighter';ctx.globalAlpha=level;ctx.drawImage(XART.get(RD29_ART.key),b.x-size/2,b.y-size/2,size,size);}ctx.restore();PXG.active=active;
 if(charge)rd29CodeSkin(b,size);return{level,blink};
}
r30DrawBoss=function(b){if(!rd29Own(b))return RD29.base.draw.apply(this,arguments);
 const S=b._r30,total=rd29Time(b),gateTime=total-5.4,gate=gateTime>=0&&gateTime<4.6,white=S.mode==='v18conversion'?rd29White(S.t):0;
 if(gate)pl11World('amethyst_gate',PL11.sequence('amethyst_gate',gateTime,{form:1.8,loop:1.8,close:1}),worldWidth()/2,viewTopY()+170,250,clamp(gateTime/.35,0,1));
 let glow=null,code=null,host=false,drone=false;
 if(S.mode==='v18arrival'){const u=rd25Ease(S.t/1.8),size=v18Size(b)*lerp(.18,.8,u);glow=rd29Drone(b,size);drone=true;}
 if(S.mode==='v18conversion'){
  if(S.t<5.75){code=rd29Code(b);rd28Begin(code);rd28Strands(code,false);glow=rd29Drone(b,v18Size(b)*.8,true);rd28Strands(code,true);drone=true;}
  else{bi24Draw(bi24AttackPose(b,'dracodia'),b,360);host=true;}
 }
 RD29.last={time:total,mode:S.mode,gate,gateFrame:gate?PL11_GAME.last?.from:null,drone,host,white,glow,code:code?{front:RD28.last.front,back:RD28.last.back,alpha:code.alpha}:null,protected:b._noHit};
};

// Cover every world actor, including the pilot, with the authored flash frames.
drawWorld=function(){const out=RD29.base.world.apply(this,arguments),b=boss;
 if(rd29Own(b)&&b._r30.mode==='v18conversion'){const white=rd29White(b._r30.t);if(white){
  ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const z=viewZoom();ctx.scale(z,z);ctx.translate(-camLeftX(),VH*(1-z)/z);
  er23Curtain('whiteout',white);ctx.restore();}}
 return out;
};
globalThis.BOF_DRONE_REWORK_1026=RD29;
