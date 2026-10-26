/* Presentation-only checkpoints. Uses live routing and native draw functions;
   never loaded by index.html and never changes encounter code or authored art. */
window.CHRONOS_CATALOG={chapters:[
 ['Arrival / unfolding',4,'Shared entrance — chromium is not active yet'],
 ['Idle / hammer guard',3,'Current regular and chromium guard plates'],
 ['Chromium armor activation',4,'Shared transition — energy strike, conduction and plating'],
 ['Jump / overhead strike',4,'Wind-up, airborne strike, impact and recovery'],
 ['Furious double slam / side swings',5,'Current Furious follow-up sequence'],
 ['Depth jump / giant strike',7,'Takeoff → offscreen → small background drop → second jump → overhead strike'],
 ['Backward retreat / braking',4,'Current recoil, retreat and landing poses'],
 ['Extended hammer rotation',4,'Forward spin followed by shoot-response backspin'],
 ['Hammer throw / flight / catch',6,'Current throwing plates and independent flying hammer'],
 ['Shield formation',4,'Whole actor with the authored shield forming in front'],
 ['Shielded recharge',4,'Fixed one-handed side hammer, energy and foreground SHOOT objective'],
 ['Ball / three laser volleys / unfolding',8,'Native ball plates, laser projectiles and glow unfolding'],
 ['Nova charge / release',4,'Current charge and release animation routing'],
 ['Spell casting',4,'Current casting and release plates'],
 ['Laser charge / beam',5,'Current beam posture and native chromium beam'],
 ['Arsenal pickup / hammer release',6,'Current crate strike, tool toss and weapon catch'],
 ['Chaingun draw / firing / cooling',5,'Current tactical body and native muzzle flashes'],
 ['Rage charge / rage',4,'PixelLab rising golden flame aura, body strain and cyan lightning'],
 ['Hit flash',3,'Native white damage feedback on both armor materials'],
 ['Stun / magnetic hammer recall',6,'Empty-hand kneeling, departure, recall and recovery'],
 ['Death / kneeling',4,'Current death pose uses the same kneeling identity']
],seen:{},errors:[],lastChapter:-1};
{
const C=CHRONOS_CATALOG;let cursor=0;C.chapters=C.chapters.map(([name,duration,note],id)=>{const q={id,name,duration,note,start:cursor};cursor+=duration;return q});C.duration=cursor;
const seed=structuredClone(boss);C.actors=[false,true].map(chrome=>{const b=structuredClone(seed);b.x=320;b.y=315;b.dead=false;b.enter=b._noHit=false;b.flash=0;b.hp=b.maxhp=11220;
 b._hammer.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,flash:0,barrier:0,t:0,checkpoints:[]}:null;return b});
const baseH=C.actors.map(b=>structuredClone(b._hammer));
C.reset=(b,lane)=>{b._hammer=structuredClone(baseH[lane]);const h=b._hammer;b.x=320;b.y=315;b._drawY=b.y;b.dead=false;b.dying=0;b.flash=0;b._lastPart=null;b.enter=b._noHit=false;
 for(const k of ['throw','recovery','hb20Pickup','hc11Counter','c25Knock','c26Return','_hj22Pair','_hf22StormPair','er23DepthCombo','_hf22Charge','whirl','frAct'])h[k]=null;
 h.hammerDestroyed=false;h._hf22Red=false;h.mode='hammer';h.state='hammer';h.t=0;h.bombs=[];h.pillars=[];h.spellTargets=[];h.cp12Caption=null;h._ht23ArmorGun=false;h.chainMuzzle=0;h.c26SpinClock=0;h.c25ArmorAtDeath=lane===1;};
C.configure=(b,lane,id,z)=>{C.reset(b,lane);const h=b._hammer,u=z/C.chapters[id].duration;h.chromiumT=z;h.angle=z*8;h.state='hammer';h.t=z;
 switch(id){
 case 0:h.state=z<1.3?'flyby':z<2?'return':'unfold';h.t=z<2?0:(z-2);break;
 case 1:break;
 case 2:h.state='fr_activation';h.t=Math.min(FR27_ACT.end-.001,z/4*FR27_ACT.end);break;
 case 3:if(z<1.1){h.state='warn';h.t=z/1.1*.58}else if(z<1.8){h.state='leap';h.t=(z-1.1)/.7*.27}else{h.state='recover';h.t=(z-1.8)/2.2*.5}break;
 case 4:h.state='recover';h._hj22Pair=hj22Pair(b,'blue',{x:320,y:475});h._hj22Pair.clock=(z%2.5)/2.5*2.18;h.t=h._hj22Pair.clock;break;
 case 5:{
  if(z<.55){h.state='giant_windup';h.t=z;}
  else if(z<1.5){h.state='giant_rise';h.t=z-.55;b.y=lerp(315,-470,clamp(h.t/.8,0,1));}
  else if(z<2.25){h.state='giant_bg_drop';h.t=z-1.5;b.y=lerp(-210,210,h.t/.75);}
  else if(z<2.55){h.state='giant_bg_land';h.t=z-2.25;b.y=210;}
  else if(z<3.4){h.state='giant_bg_jump';h.t=z-2.55;b.y=210-Math.sin(h.t/.85*Math.PI/2)*55;}
  else if(z<4){h.state='giant_warn';h.t=z-3.4;b.y=155;}
  else if(z<4.65){h.state='giant_dive';h.t=z-4;h.tx=320;h.ty=450;const end=ha21Landing(b,{x:320,y:450},'slam',16,1.65),u=(h.t/.65)**2;b.x=lerp(320,end.x,u);b.y=lerp(155,end.y,u);}
  else{const a=c27Row('strike_'+(lane?'chrome':'regular'),16),end={x:320-(a.tip[0]-a.pivot[0])*1.65,y:450-(a.tip[1]-a.pivot[1])*1.65};
   if(z<5.09){h.state='giant_sweep';h.t=z-4.65;b.x=end.x;b.y=end.y;}
   else{h.state='giant_recover';h.t=z-5.09;const u=clamp(h.t/1.05,0,1);h.c26Return={t:h.t,duration:1.05,scale:lerp(1.65,1,u)};b.x=lerp(end.x,320,u);b.y=lerp(end.y,315,u);}}
  h.tx=320;h.ty=450;b._drawY=b.y;break;}
 case 6:h.state='back';h.c26Return={t:(z%2)/2*1.05,duration:1.05,scale:lerp(1.25,1,(z%2)/2)};break;
 case 7:h.state='whirlwind';h.c26SpinClock=z<2?z*12:24-(z-2)*12;break;
 case 8:if(z<1.4){h.state='spin';h.t=z/1.4*HAMMER_SPIN_TIME}else if(z<4.9){h.state='throw';h.t=z-1.4;const a=hf22Row('blue_throw',4),origin=hb20World(a,a.tip,b,1,0),at=hf22Orbit(b,.2+(z-1.4)%2.4,origin);h.throw={x:at.x,y:at.y,angle:z*18,_hf22Origin:origin,_hf22Age:z-1.4,t:z-1.4,phase:'hf22_orbit',trail:[]}}else{h.state='hammer_catch';h.t=(z-4.9)/1.1*.65}break;
 case 9:h.state='shield';h.t=Math.min(.95,(z%2.4)/1.5*.95);break;
 case 10:h.state='storm_raise';h.t=z;h.recovery={status:'charging',elapsed:z,coreHP:100,coreMax:100};b.y=235-(c27Row('palm_'+(lane?'chrome':'regular'),16).tip[1]-c27Row('palm_'+(lane?'chrome':'regular'),16).pivot[1]);b._drawY=b.y;break;
 case 11:if(z<1.4){h.state='curl';h.t=z/1.4*HAMMER_BALL_WARN}else if(z<5.6){h.state='ball';h.t=z-1.4;h.c26Ball={t:h.t,volley:Math.min(3,Math.max(0,Math.floor((h.t-.9)/1.15)+1)),next:.9+Math.max(0,Math.floor((h.t-.9)/1.15)+1)*1.15}}else{h.state='uncurl';h.t=(z-5.6)/2.4*1.65}break;
 case 12:h.state=z<2.1?'nova_charge':'nova_release';h.t=z<2.1?z/2.1*1.6:z-2.1;break;
 case 13:h.state=z<2.4?'spell':'spell_blast';h.t=z<2.4?z/2.4*2.35:z-2.4;break;
 case 14:h.hammerDestroyed=true;h.state=z<1.8?'mega_charge':'mega_beam';h.t=z<1.8?z/1.8*1.65:(z-1.8)/3.2*hammerEradDuration();break;
 case 15:h.hb20Pickup={t:z/6*4.5,origin:{x:320,y:315},station:{x:320,y:315},box:{x:445,y:430}};{const p=h.hb20Pickup;p.released=p.t>=2.26;p.opened=p.t>=2.86;p.obtained=p.t>=4.05;p.release={x:245,y:143};h.hammerDestroyed=p.released;}break;
 case 16:h.hammerDestroyed=true;h.state=z<1.3?'chaingun_draw':z<2?'chain_warn':z<4?'chaingun':'chain_cool';h.t=z<1.3?z/1.3*2:z<2?(z-1.3)/.7*.65:z<4?z-2:z-4;h.chainHeat=z<4?1:1-(z-4);h.chainMuzzle=h.state==='chaingun'&&z%.16<.09?.09-z%.16:0;break;
 case 17:h._hf22Red=true;h.state=z<1.8?'hf22_rage_charge':'hammer';if(z<1.8)h._hf22Charge={t:z};break;
 case 18:b.flash=z%.7<.16?.16:0;break;
 case 19:h.state='fr_stun';h.t=z/6*4.3;h.hammerDestroyed=true;h.c25Knock={t:h.t,from:{x:320,y:135},away:{x:470,y:95}};break;
 case 20:b.dead=true;b.dying=z/4*1.2;break;
 }
 return ha21Blue(b);
};
cv.width=cv.height=640;C.canvas=document.createElement('canvas');C.canvas.width=1280;C.canvas.height=800;C.g=C.canvas.getContext('2d');C.g.imageSmoothingEnabled=false;
hammerBossAtmosphereDraw=function(){};BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;eBullets=[];pBullets=[];enemies=[];powerups=[];l5Rocks=[];diffKey='furious';run.stage=5;
C.draw=(time)=>{const chapter=C.chapters.find(q=>time<q.start+q.duration)||C.chapters.at(-1),z=Math.max(0,time-chapter.start),g=C.g;
 g.fillStyle='#091320';g.fillRect(0,0,1280,800);g.textAlign='center';g.fillStyle='#f3f7fc';g.font='bold 27px sans-serif';g.fillText(String(chapter.id+1).padStart(2,'0')+'  '+chapter.name,640,40);g.font='16px sans-serif';g.fillStyle='#b9cddd';g.fillText(chapter.note,640,69);
 g.strokeStyle='#30485d';g.beginPath();g.moveTo(640,92);g.lineTo(640,748);g.stroke();
 for(let lane=0;lane<2;lane++){
  boss=C.actors[lane];const b=boss;efxClock=time;const q=C.configure(b,lane,chapter.id,z),h=b._hammer;
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,640,640);ctx.save();
  const camera=chapter.id===5?.92:1.12;ctx.translate(320,320);ctx.scale(camera,camera);ctx.translate(-320,-320);
  try{hammerBossDraw(b);
   if(chapter.id===11&&h.state==='ball'){for(let volley=0;volley<3;volley++){const age=z-1.4-(.9+volley*1.15);if(age>=0&&age<1.05)for(const off of [-.28,-.14,0,.14,.28]){const angle=Math.PI/2+off;hammerLaserDraw({x:b.x+Math.cos(angle)*348*age,y:b.y+Math.sin(angle)*348*age,vx:Math.cos(angle)*5.8,vy:Math.sin(angle)*5.8,t:age,w:8,h:42});}}}
  }catch(e){const key=chapter.id+':'+lane+':'+String(e);if(!C.errors.includes(key))C.errors.push(key)}finally{ctx.restore()}
  g.drawImage(cv,lane*640,96,640,640);g.fillStyle=lane?'#e7ecff':'#76dde6';g.font='bold 22px sans-serif';g.fillText(lane?'CHROMIUM ARMOR':'REGULAR ARMOR',lane*640+320,113);
  const key=q?.a?.key||(['chaingun_draw','chain_warn','chaingun','chain_cool'].includes(h.state)?ht23GunPose(b)?.key:h.hb20Pickup?'tactical pickup':'native layered draw');
  (C.seen[chapter.id+':'+lane]||=new Set()).add(key);g.fillStyle='#7995aa';g.font='13px monospace';g.fillText(key||'No whole-actor frame selected',lane*640+320,742);
 }
 g.fillStyle='#a2b8cd';g.font='15px sans-serif';g.fillText('CURRENT IN-GAME ANIMATION CATALOG • STAGED POSE REVIEW • NOT CONTINUOUS GAMEPLAY',640,776);
 g.fillStyle='#74dce9';g.fillRect(0,794,1280*clamp(time/C.duration,0,1),6);return chapter.id;
};
}
