/* Review-only adapter. No shipping dependency, forced kills, enemy edits or loadout grants.
 * Combat reads native state and writes native Input keys (not a physical human test).
 * Menu navigation is sent by the host with actual CDP keyboard events.
 */
FURYBOT.version='1024-campaign-1';
FURYBOT.health=function(){const b=bossActive?boss:subBossActive?subBoss:null;return b?Math.max(0,b.hp||0):null;};
const betaInput=FURYBOT.pre;
FURYBOT.nextConfirm=Infinity;
FURYBOT.pre=function(now){
 if(state!==GS.PLAY){for(const k of this.owned)Input.keys[k]=false;
  if(state===GS.STAGESEL&&sselBoot===0&&!sselUnlockCine&&this.age()>(this.nextMapFire||0)){cmap2.focus='map';Input.injectTap('j');this.nextMapFire=this.age()+8;}
  return;}
 betaInput.call(this,now);
 // Keep complete naturally timed cinematics. Only advance ordinary portrait lines
 // after five seconds when no cinematic director owns the scene.
 if(BOFCinematicDirector.current&&!BOFCinematicDirector.current.combatLive){Input.keys.j=false;delete Input.taps?.j;}
 if(run.stage===6&&s6Wing?.choice&&!s6Wing.route){Input.keys.j=false;Input.injectTap('d');if(s6Wing.frChoice?.t>.35)Input.injectTap('j');}
};
const betaHit=playerHit;
playerHit=function(source){
 const q=FURYBOT;if(q.started&&state===GS.PLAY&&!player.dead&&player.invuln<=0){
  q.stats.contactAttempts=(q.stats.contactAttempts||0)+1;
  if(q.events.length<20000)q.events.push({t:q.age(),type:DBGT.god?'god-contact':'hit-attempt',source:typeof source==='string'?source:source?.kind||'contact',stage:run.stage,x:player.x,y:player.y});
 }
 return betaHit.apply(this,arguments);
};
FURYBOT.post=function(now){const Q=this;if(!Q.started||Q.finished)return;Q.frames++;const t=Q.age();
 const delta=Q.lastNow?now-Q.lastNow:0;Q.lastNow=now;if(delta>0)(Q.frameTimes??=[]).push(delta);
 if(Q.frameTimes?.length>600000)Q.frameTimes.shift();
 if(player.dead&&!Q.wasDead){
  Q.stats.deaths=(Q.stats.deaths||0)+1;Q.events.push({t,type:'native-player-death',stage:run.stage,lives:run.lives});
  if(!DBGT.god){DBGT.god=true;Q.godAt=t;Q.events.push({t,type:'god-enabled',reason:'Native bot death; user-authorized completion fallback. No loadout/ammo/HP changes.'});}
 }Q.wasDead=!!player.dead;
 if(player.roll&&!Q.wasRoll)Q.stats.rolls++;if(player.somer&&!Q.wasSomer)Q.stats.somersaults++;
 Q.wasRoll=!!player.roll;Q.wasSomer=!!player.somer;
 if(Q.lastBombs!=null&&run.bombs<Q.lastBombs)Q.stats.missiles+=Q.lastBombs-run.bombs;Q.lastBombs=run.bombs;
 for(const b of pBullets)if(!Q.seenShots.has(b)){Q.seenShots.add(b);Q.stats.shots++;}
 const phase=Q.phase(),hp=Q.health(),label=run._gp4StageX?'X-HARRIER':String(run.stage);
 const scene=BOFCinematicDirector.current;
 const chapter=[state,label,bossActive?'BOSS':subBossActive?'MINIBOSS':'',scene?.id||''].join('|');
 if(chapter!==Q.chapter){Q.events.push({t,type:'chapter',chapter,hp,stageTime:stageTimer,score:run.score});Q.chapter=chapter;}
 if(phase!==Q.lastPhase){Q.events.push({t,type:'phase',phase,hp,stage:label});Q.lastPhase=phase;}
 if(t>(Q.nextSample||0)){
  Q.samples.push({t,state,stage:label,stageTime:stageTimer,hp,phase,x:Math.round(player.x),y:Math.round(player.y),god:DBGT.god,lives:run.lives,score:run.score,weapon:run.weapon,level:run.wlevel,bombs:run.bombs,enemyBullets:eBullets.length,enemies:enemies.length,music:Audio.currentMusic||Snd.currentMusic||null});Q.nextSample=t+2;
 }
 if(!(Q.nextPaint>now)){Q.paint();Q.nextPaint=now+1000/30;}
 if(state===GS.VICTORY&&run._trueFinaleCleared){
  Q.victoryAt??=t;
  const endingCard=typeof INV20!=='undefined'&&drawVictory._trueEnding?INV20.end:VICTORY_CARD_AT;
  if((drawVictory._t||0)>endingCard+8){Q.completed=true;Q.stop('native-campaign-victory-and-ending');}
 }
 if(t>Q.config.limit)Q.stop('time-limit');
};
// Southern strategy after immunity; track aim horizontally. Pursue pickups
// only when visible and close, preserving ordinary progression/pickup rewards.
const betaDecide=FURYBOT.decide;
FURYBOT.decide=function(S){
 betaDecide.call(this,S);
 if(DBGT.god){
  const y=VH-74,target=S.target;
  this.commands=[target?Math.abs(target.x-player.x)<12?0:Math.sign(target.x-player.x):Math.abs(player.x-worldWidth()/2)<15?0:Math.sign(worldWidth()/2-player.x),Math.abs(player.y-y)<9?0:Math.sign(y-player.y)];
  const pickup=powerups.filter(p=>!p.dead&&p.y>VH*.55&&p.y<VH-30&&Math.abs(p.x-player.x)<120).sort((a,b)=>Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(b.x-player.x,b.y-player.y))[0];
  if(pickup&&Math.hypot(pickup.x-player.x,pickup.y-player.y)<145)this.commands=[Math.abs(pickup.x-player.x)>9?Math.sign(pickup.x-player.x):0,Math.abs(pickup.y-player.y)>9?Math.sign(pickup.y-player.y):0];
 }
};
FURYBOT.report=function(){const a=[...(this.frameTimes||[])].sort((a,b)=>a-b),pct=p=>a[Math.min(a.length-1,Math.floor(a.length*p))];return{version:this.version,config:this.config,loadout:this.loadout,elapsed:this.elapsed??this.age(),frames:this.frames,fps:this.frames/(this.elapsed??this.age()),completed:this.completed,reason:this.reason,stats:this.stats,godEnabledAt:this.godAt,frameMs:{p50:pct(.5),p95:pct(.95),p99:pct(.99),max:a.at(-1)},samples:this.samples,events:this.events,error:this.error,audioErrors:this.audioErrors,bytes:this.bytes,saved:this.saved,writeError:this.writeError,state,stage:run.stage,score:run.score,playerDead:player.dead,lifeStock:run.lives,difficulty:diffKey,proof:P2M.proof,campaign:{rank:campaign.rank,bonusUnlocked:campaign.bonusUnlocked,stageX:campaign.stageX1004},trueFinale:run._trueFinaleCleared};};
