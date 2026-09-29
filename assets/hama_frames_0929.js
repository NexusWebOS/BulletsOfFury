"use strict";
/* Mike's HAMA pack, layered after the 0928 encounter. Audio cues,
   targeting, healing counters and the original HAMMER remain their owners'. */
const HAMA29=HAMA_FRAMES_ART_29.families;
const HAMA29_BASE={warm:ht27Warm,begin:ht27Begin,draw:ht27Draw,
  toss:hamaTossTick,hand:hamaHandPoint,slam:hamaSlamPoint,orbital:hammerOrbitalPose};
const HAMA29_BODY=.646,HAMA29_TOSS=.804,HAMA29_HELPER=.50;
for(const d of Object.values(HAMA29))XART._src[d.key]=d.path;
function hama29Ready(){let ready=true;for(const d of Object.values(HAMA29))if(!XART.rdy(d.key))ready=false;return ready;}
ht27Warm=function(){HAMA29_BASE.warm();if(ht27Variant===HAMA_VARIANT)hama29Ready();};
ht27Begin=function(d){if(hamaOn()&&!hama29Ready())return false;return HAMA29_BASE.begin(d);};
function hama29Cycle(beat,count,beats){return Math.floor(((beat%beats+beats)%beats)/beats*count);}
function hama29TossFrame(T,H){
  if(H.caught>0)return -1;
  const t=T?T.t:0;
  return t<.1?0:t<.2?1:t<.4?2:t<.5?3:t<.72?4:t<.95?5:t<1.2?6:t<1.45?7:
    t<1.58?8:t<1.75?9:t<1.84?10:t<2?11:t<2.2?12:t<2.4?13:t<2.7?14:15;
}
function hama29SlamFrame(c){
  const cue=hamaStopAt(c);if(!cue)return 0;const a=c-cue.t+1e-8;
  // The two actual contacts are frames 2 and 7, at the soundtrack's two cues.
  return a<-.35?0:a<-.22?11:a<0?1:a<.09?2:a<HAMA_P-.27?3:a<HAMA_P-.20?4:
    a<HAMA_P-.12?5:a<HAMA_P?6:a<HAMA_P+.1?7:a<HAMA_P+.2?8:a<HAMA_P+.3?9:a<HAMA_P+.4?10:11;
}
function hama29Point(name,f,p,x,foot,s){const d=HAMA29[name];return {x:x+(p[0]-d.anchor[0])*s,y:foot+(p[1]-d.anchor[1])*s};}
function hama29Vocal(d,who){return d.hama.lines.find(l=>l.who===who&&l.t<l.dur&&(l.text||'').length);}
function hama29Head(name,box,anchor,x,foot,s,line,flash){
  const d=HAMA29[name],f=hama29Cycle(line.t*7,4,1),r=d.frames[f],k=Math.min((box[2]-box[0])/96,(box[3]-box[1])/95)*s;
  const cx=x+((box[0]+box[2])/2-anchor[0])*s;
  const neck=foot+(box[3]-anchor[1])*s;
  const im=flash?xartTint(d.key,'#ffffff',.78):XART.get(d.key);
  ctx.drawImage(im,r[0],r[1],r[2],r[3],cx-d.anchor[0]*k,neck-d.anchor[1]*k,r[2]*k,r[3]*k);
}
function hama29Sprite(name,f,x,foot,s,flash,line,chant,helper,buddyLine){
  const d=HAMA29[name];if(!d||!XART.rdy(d.key))return false;
  f=((f|0)%d.frames.length+d.frames.length)%d.frames.length;const r=d.frames[f],box=line&&d.heads[f],buddyBox=buddyLine&&d.helperHeads&&d.helperHeads[f];
  const dx=x-d.anchor[0]*s,dy=foot-d.anchor[1]*s;
  ctx.save();ctx.imageSmoothingEnabled=false;
  if(box||buddyBox){ctx.beginPath();ctx.rect(dx,dy,r[2]*s,r[3]*s);
    for(const cut of [box,buddyBox])if(cut)ctx.rect(dx+cut[0]*s,dy+cut[1]*s,(cut[2]-cut[0])*s,(cut[3]-cut[1])*s);ctx.clip('evenodd');}
  const im=flash?xartTint(d.key,'#ffffff',.78):XART.get(d.key);
  ctx.drawImage(im,r[0],r[1],r[2],r[3],dx,dy,r[2]*s,r[3]*s);ctx.restore();
  if(box){ctx.save();ctx.imageSmoothingEnabled=false;
    // Neck anchors, rather than image centres, keep replacement helmets seated.
    hama29Head((helper?'helper':'boss')+'_speaker_'+(chant?'chant':'sing'),box,d.anchor,x,foot,s,line,flash);
    ctx.restore();}
  if(buddyBox){ctx.save();ctx.imageSmoothingEnabled=false;
    hama29Head('helper_speaker_sing',buddyBox,d.anchor,x,foot,s,buddyLine,flash);ctx.restore();}
  return true;
}
hamaHandPoint=function(b){
  const d=b&&b._hammerTime;if(!hamaOn()||!d||!d.hama.toss)return HAMA29_BASE.hand(b);
  const f=Math.max(4,Math.min(9,hama29TossFrame(d.hama.toss,d.hama))),p=HAMA29.hammer_toss_helper_throw.held[f];
  return hama29Point('hammer_toss_helper_throw',f,p,b.x,b.y+94,HAMA29_TOSS);
};
hamaSlamPoint=function(b){if(!hamaOn())return HAMA29_BASE.slam(b);
  const d=b._hammerTime,second=hama29SlamFrame(d.clock)>=7;
  return hama29Point('double_hammer_slam',second?7:2,second?[223,444]:[225,444],b.x,b.y+94,HAMA29_BODY);
};
hamaTossTick=function(b,d,dt){
  if(!hamaOn()||!d.hama)return HAMA29_BASE.toss(b,d,dt);
  const H=d.hama,T=H.toss,old=H.flyHammer;
  const r=HAMA29_BASE.toss(b,d,dt),F=H.flyHammer;
  if(F&&F!==old){const p=hama29Point('hammer_toss_helper_throw',2,HAMA29.hammer_toss_helper_throw.launch,b.x,b.y+94,HAMA29_TOSS);
    F.x0=p.x;F.y0=p.y;const catchAt=hama29Point('boss_vocal_leap',0,[105,437],b.x,b.y+94,HAMA29_BODY);F.x1=catchAt.x;F.y1=catchAt.y;}
  if(T&&H.toss===T&&T.thrown&&T.t>=2.4&&!T.recalled){T.recalled=true;ht27Summon(d,false);}
  return r;
};
function hama29LeapFrame(b){const h=b._hammer;
  if(h.state==='warn')return Math.min(3,Math.floor(clamp(h.t/(hammerFurious()?.58:1.2),0,1)*4));
  if(h.state==='leap')return 4+Math.min(3,Math.floor(clamp(h.t/(hammerFurious()?.27:.52),0,1)*4));
  return 8+Math.min(3,Math.floor(clamp(h.t/hammerRecoverDuration(),0,1)*4));
}
hammerOrbitalPose=function(b,f,scale,tint){const d=b&&b._hammerTime;
  if(hamaOn()&&d&&d.hama&&d.mode==='attack'&&['warn','leap','recover'].includes(b._hammer.state))
    return hama29Sprite('boss_vocal_leap',hama29LeapFrame(b),b.x,b.y+94,HAMA29_BODY*scale,b.flash>0,hama29Vocal(d,'boss'),false,false);
  return HAMA29_BASE.orbital.apply(this,arguments);
};
function hama29Wall(d){
  if(!d.shield||d.mode==='break')return;
  const sd=HAMMER_TIME_ART.sheets.wall,fr=sd.frames[Math.floor(d.clock*16)%8],wall=ht27WallBounds(d);
  if(XART.rdy('ht27_wall')){ctx.save();ctx.globalAlpha=wall.alpha;ctx.imageSmoothingEnabled=false;
    ctx.beginPath();ctx.rect(wall.x,VH*.16,wall.w,wall.h);ctx.clip();
    ctx.drawImage(XART.get('ht27_wall'),fr[0],fr[1],fr[2],fr[3],wall.x,wall.y,wall.w,wall.h);ctx.restore();}
  for(const r of d.reflections)hammerLaserDraw(r);
}
ht27Draw=function(b){
  const d=b&&b._hammerTime;if(!hamaOn()||!d||b.dead||!d.hama)return HAMA29_BASE.draw(b);
  const H=d.hama,beat=hamaBeat(d.clock),T=H.toss,tf=T&&T.wait>0?-1:hama29TossFrame(T,H),hop=hamaHop(d);
  const bossLine=hama29Vocal(d,'boss'),crewLine=hama29Vocal(d,'crew'),chant=d.mode==='breakdown'||d.mode==='break';
  // Frames 0..5 already contain a nearby helper, and 6..9 contain the held one.
  // Reserve the buddy before the grab; the actual grabbed helper is already out
  // of the formation. No independent copy is drawn on a composite plate.
  if(d.mode==='toss'&&T&&!T.buddy&&tf>=0&&tf<=5){const live=d.helpers.filter(q=>!q.dead&&q.spawn>=1);
    if(live.length)T.buddy=live.reduce((a,q)=>Math.abs(q.x-b.x)<Math.abs(a.x-b.x)?q:a);}
  for(const q of d.helpers){if(q.dead||q.spawn<=0||(d.mode==='toss'&&T&&tf>=0&&tf<=5&&q===T.buddy))continue;
    const f=d.mode==='breakdown'?hama29Cycle(beat+q.slot*.12,12,4):(Math.floor(beat*2+q.slot)%2?11:0);
    hama29Sprite('helper_lasso_360',f,q.x,q.y+32+hop,HAMA29_HELPER*q.spawn,q.flash>0,crewLine,chant,true);
    if(q.aim)combatWarningDraw(q,{x:q.x,y:q.y+20,ex:q.aim.x,ey:q.aim.y,progress:clamp(q.aim.t/q.aim.dur,0,1),width:18,alertX:q.x,alertY:q.y-40});
  }
  const foot=b.y+94;
  if(d.mode==='attack')HT27_BASE.draw(b); // engine boss only: not a second troupe draw
  else if(d.mode==='intro'&&d.shipFrame!=null){if(d.musicStarted)archBlit('ship_transform',d.shipFrame,b.x,b.y,d.shipFrame===15?192:206);}
  else if(d.mode==='intro'){
    // A rising dance shield is not a Chromium transformation. Keep the same
    // black-steel/cyan character as the regular attack and dance plates.
    const name='boss_moonwalk_'+(H.moonDir<0?'left':'right');
    hama29Sprite(name,hama29Cycle(beat,8,4),b.x,foot,HAMA29_BODY,b.flash>0,null,false,false);
  }else if(d.mode==='breakdown')hama29Sprite('boss_lasso_360',hama29Cycle(beat,12,4),b.x,foot+hop,HAMA29_BODY,b.flash>0,bossLine,true,false);
  else if(d.mode==='break')hama29Sprite('double_hammer_slam',hama29SlamFrame(d.clock),b.x,foot,HAMA29_BODY,b.flash>0,bossLine,true,false);
  else if(d.mode==='toss'&&T&&tf>=0)hama29Sprite('hammer_toss_helper_throw',tf,b.x,foot,HAMA29_TOSS,b.flash>0,bossLine,false,false,hama29Vocal(d,'robot'));
  else hama29Sprite('boss_vocal_leap',0,b.x,foot,HAMA29_BODY,b.flash>0,bossLine,false,false);
  if(T&&T.aim&&!T.thrown)combatWarningDraw(b,{x:T.held?T.held.x:b.x,y:T.held?T.held.y:b.y,ex:T.aim.x,ey:T.aim.y,
    progress:clamp(T.aim.t/T.aim.dur,0,1),width:44,alertX:b.x,alertY:b.y-150});
  const F=H.flyHammer;if(F){const p=clamp(F.t/F.dur,0,1);
    hama29Sprite('hammer_airborne_spin',Math.floor(F.t*14)%8,lerp(F.x0,F.x1,p),lerp(F.y0,F.y1,p)-Math.sin(p*Math.PI)*190,.65,false,null,false,false);}
  for(const r of H.thrown)if(!r.dead)hama29Sprite('helper_airborne_tumble',Math.floor(r.t*12)%8,r.x,r.y,HAMA29_HELPER,r.flash>0,hama29Vocal(d,'robot'),false,true);
  hama29Wall(d);hamaLinesDraw(b,d);
};
