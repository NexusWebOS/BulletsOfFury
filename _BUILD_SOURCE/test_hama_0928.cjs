module.exports=function(vm,ctxv,ok){
 /* 0928 - HAMA: the second Hammer Time password, on Mike's MC Hammer instrumental. Behaviour only, driven
    through the real updatePlay with the song's clock stepped 1/60 s a frame; nothing reads source text. */
 const fs=require('fs'),path=require('path');
 for(const [file,sentinel] of [['hammer_time_art_0927.js','HAMMER_TIME_ART'],['hammer_time_0927.js','ht27Variant'],
   ['hama_art_0928.js','HAMA_ART'],['hama_0928.js','HAMA_VARIANT']])
   if(vm.runInContext('typeof '+sentinel,ctxv)==='undefined')
     vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 console.log('=== 377. HAMA: the instrumental, the moonwalk, HAMMER / TIME slams, the breakdown, the robot toss ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};let hits=0;const realHit=playerHit;playerHit=function(){hits++;};
  diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='hama';submitPassword();
  o['HAMA routes through difficulty selection to Stage 5']=ht27Pending&&hamaPending&&PENDING_STAGE===5&&state===GS.DIFF;
  setState(GS.PASSWORD);o['backing out cancels the route and the song choice']=!ht27Pending&&!hamaPending&&ht27Variant===null;
  const C=HAMA_CUES,P=60/HAMA_ART.audio.bpm;
  o['the cue sheet is the measured one: 132.55 BPM, three STOPs, two breakdowns']=Math.abs(HAMA_ART.audio.bpm-132.55)<.01&&
    C.stops.map(s=>s.t).join()==='61.8,115.44,158.64'&&C.breakdowns.length===2&&C.breakdowns.every(w=>w.t1>w.t0+10)&&C.introEnd>14&&C.introEnd<16;
  pwInput='HAMA';submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');startRun(PENDING_STAGE);
  const b=boss,d=b._hammerTime,m=Snd.music.hama;m.readyState=4;m.paused=false;m.currentTime=0;
  updatePlay(1/60);
  o['the run plays the instrumental, not the remix']=ht27Active&&hamaOn()&&d.musicStarted&&Snd.cur===m&&m.src.indexOf('hama_instrumental_0928.mp3')>=0&&!!d.hama;
  function advance(to){while(m.currentTime<to){m.currentTime=Math.min(to,m.currentTime+1/60);updatePlay(1/60);}}
  const origin={x:player.x,y:player.y};for(const a of ['up','fire'])for(const k of keybind[a])Input.keys[k]=true;
  advance(8);const x0=b.x;advance(8.9);
  o['after the unfold he moonwalks back and forth, and the player waits']=d.mode==='intro'&&d.hama.pose==='moonwalk'&&Math.abs(b.x-x0)>10&&ht27Locked()&&player.x===origin.x&&player.y===origin.y&&pBullets.length===0;
  advance(12);o['the shield rises while he moonwalks']=d.shield&&ht27WallBounds(d).rise>0&&ht27WallBounds(d).rise<1;
  for(const k of Object.keys(Input.keys))Input.keys[k]=false;
  advance(C.introEnd-.05);o['four robots arrive during the intro']=d.helpers.length===4;
  advance(C.introEnd+.1);o['at the verse the fight opens and the player is free']=!ht27Locked()&&!d.shield&&['dance','toss'].includes(d.mode);
  /* the robot toss */
  d.mode='dance';d.t=9;d.hama.attacks=0;advance(m.currentTime+1/30);
  o['the first attack is the robot toss']=d.mode==='toss'&&!!d.hama.toss;
  let held=false,thrown=null,hammerUp=false;const t0=m.currentTime;
  while(m.currentTime<t0+2.2){advance(m.currentTime+1/60);const T=d.hama.toss;if(d.hama.flyHammer)hammerUp=true;if(T&&T.held&&!T.thrown)held=true;if(d.hama.thrown.length)thrown=thrown||d.hama.thrown[0];}
  o['the hammer goes up behind him, he grabs a robot, and chucks it']=hammerUp&&held&&!!thrown&&thrown._hamaThrown;
  o['the grabbed robot leaves the formation while it is carried']=!d.helpers.includes(thrown);
  o['the thrown robot sings on the way in']=d.hama.lines.some(l=>l.who==='robot'&&/THI/.test(l.text));
  if(thrown&&!thrown.dead){hitEnemy(thrown,999);}o['a thrown robot is a target and can be shot down']=!thrown||thrown.dead;
  let g0=0,launches=0,was=false;while(d.mode==='toss'&&g0++<600){advance(m.currentTime+1/60);const up=!!d.hama.flyHammer;if(up&&!was)launches++;was=up;}
  o['he catches the hammer once and goes back to dancing (it does not fly forever)']=d.mode!=='toss'&&launches<=1&&!d.hama.flyHammer&&g0<600;
  /* a second toss, flown into the player */
  d.mode='dance';d.t=9;d.hama.attacks=0;advance(m.currentTime+1/30);const h0=hits;
  let r=null;const t1=m.currentTime;while(m.currentTime<t1+2.2&&!r){advance(m.currentTime+1/60);r=d.hama.thrown[0]||null;}
  if(r){r.x=player.x;r.y=player.y-6;advance(m.currentTime+1/60);}
  o['a thrown robot that reaches the player hits and explodes']=!!r&&r.dead&&hits===h0+1;
  /* STOP ... HAMMER ... TIME */
  const s0=C.stops[0],slams=[];const sl=hamaSlam;hamaSlam=function(bb,dd,w){slams.push({t:dd.clock,w});return sl.apply(this,arguments);};
  m.currentTime=s0.t-3;updatePlay(1/60);advance(s0.t+.1);
  const lockedAt=ht27Locked()&&d.mode==='break';advance(s0.t+2);hamaSlam=sl;
  o['every STOP freezes the player for the slam']=lockedAt;
  o['two ground slams: one on HAMMER, one on TIME, a beat apart']=slams.length===2&&slams[0].w==='HAMMER'&&slams[1].w==='TIME!'&&
    Math.abs(slams[0].t-s0.t)<.02&&Math.abs(slams[1].t-(s0.t+P))<.02;
  /* the breakdown */
  const w0=C.breakdowns[0];m.currentTime=w0.t0-.5;updatePlay(1/60);advance(w0.t0+.5);
  const hp=b.hp;hitBoss(500);
  o['the breakdown raises the shield but leaves the player free']=d.mode==='breakdown'&&d.shield&&!ht27Locked()&&b.hp===hp;
  o['the robots are not targets behind the shield']=ht27HelperTargets().every(q=>!q._ht27Helper);
  const poses={},chants=[];advance(w0.t0+2*4*P+.5);
  const sg=hamaSing;hamaSing=function(dd,who,t){chants.push(t);return sg.apply(this,arguments);};
  const tb=m.currentTime;while(m.currentTime<tb+4*4*P){advance(m.currentTime+1/60);poses[d.hama.pose]=(poses[d.hama.pose]||0)+1;}hamaSing=sg;
  o['lasso bars and jumping 360 turn bars alternate on the beat']=poses.lasso>60&&poses.spin>60;
  o['OH, OH-OH, OH-OH-OH on the beat']=chants.filter(c=>c==='OH!').length>=4&&chants.includes('OH-OH!')&&chants.includes('OH-OH-OH!');
  advance(w0.t1+.2);o['the breakdown hands over to its STOP']=d.mode==='break'&&ht27Locked();
  /* the hammer jumps are sung */
  advance(w0.t1+3.5);d.mode='attack';hammerTarget(b);hammerState(b,'warn');const lines=[];const sg2=hamaSing;hamaSing=function(dd,who,t){lines.push(who+':'+t);return sg2.apply(this,arguments);};
  let g=0;while(b._hammer.state!=='leap'&&g++<600)advance(m.currentTime+1/60);let g2=0;while(b._hammer.state==='leap'&&g2++<600)advance(m.currentTime+1/60);hamaSing=sg2;
  o['a hammer jump is sung: AHHH-WOOO! going up, HEY! coming down']=lines.includes('boss:AHHH-WOOO!')&&lines.includes('crew:HEY!');
  setState(GS.TITLE);
  o['leaving stops the song and clears the route']=!ht27Active&&ht27Variant===null&&Snd.cur!==m;
  /* HAMMER is untouched */
  setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();startRun(PENDING_STAGE);
  o['HAMMER still plays Mike\\'s remix with its 0:16 break']=ht27Active&&ht27Variant===null&&ht27SongName()==='hammerTime'&&!hamaOn()&&ht27IntroEnd()===16;
  setState(GS.TITLE);playerHit=realHit;
  return o;
 })())`,ctxv));
 for(const k in out)ok(out[k],'HAMA 0928: '+k);
};
