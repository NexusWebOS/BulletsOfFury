/* Review-only native fixtures. Never loaded by the game. */
window.HR23={states:new Set(),keys:new Set(),bad:[],events:[],baseDraw:ctx.drawImage,baseCue:Snd.play};
ctx.drawImage=function(im,...a){if(HR23.active){const key=HA21.tags.get(im)||AF21.tags.get(im)?.key||'';HR23.keys.add(key);if(a.some(x=>!Number.isFinite(x)))HR23.bad.push({key,a});}return HR23.baseDraw.call(this,im,...a);};
Snd.play=function(name){if(HR23.active)HR23.events.push(name);return HR23.baseCue.apply(this,arguments);};
HR23.clean=function(){BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];B=boss;B.enter=B.dead=B._noHit=false;B._cin30Spoke=B._fb2IntroSeen=true;B.hp=B.maxhp=9000;B.flash=0;B.x=worldWidth()/2;B.y=210;B._drawY=B.y;camX=B.x-viewW()/2;player.x=B.x;player.y=VH-110;player.invuln=40002;player.dead=player.out=false;enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;stagePlan=[];spawnClock=9999;};
HR23.blue=function(){HR23.clean();const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.phasePending=h.frRecovery=h.openingJump1003=false;h.recovery=h.hc11Counter=h.bm9Counter=h.hb20Pickup=null;h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[],rage:false};h.mode='hammer';h.hammerDestroyed=false;h.charged=true;h.empowered=false;h.pillars=[];h.spellTargets=[];h.throw=null;delete h._hf22StormPair;delete h._hj22Pair;delete h._hf22Charge;h._hf22Red=false;h.stormHome={x:B.x,y:B.y};if(B._hammerTime){B._hammerTime.mode='attack';B._hammerTime.hama=false;}if(B._hama)B._hama.mode='attack';hammerState(B,'hammer');};
HR23.corrupt=function(){HR23.clean();v18Budget(B);v18Enter(B,2,8);v18Fight(B);hb20Init(B);B.enter=B._noHit=false;const Q=hb20State(B);Q.action=null;Q.cool=999;Q.rage=Q.broken=false;Q.scale=1;Q.angle=0;Q._hf22Red=false;Q.waves=[];Q.fire=[];};
HR23.start=function(name,diff){diffKey=diff;DIFF=difficultyForRun(run.mode,diff);HR23.label=name;HR23.states.clear();HR23.keys.clear();HR23.bad=[];HR23.events=[];HF22.events=[];
 if(run.stage===8){HR23.corrupt();hb20Start(B,name);}
 else {HR23.blue();const h=B._hammer;
  if(name==='jump'){hammerTarget(B);hammerState(B,'warn');}
  else if(name==='throw')hammerBoomerangStart(B);
  else if(name==='whirlwind')hammerWhirlStart(B);
  else if(name==='storm'){hammerStormStart(B);hammerStormTarget(B);hammerState(B,'storm_warn');}
  else if(name==='giant'){hammerGiantArm(B);hammerState(B,'giant_windup');}
  else if(name==='pickup'){h.hb20PickupDone=false;hammerPhaseTwoStart(B);}
  else if(name==='spell')hammerSpellStart(B);
  else if(name==='chaingun'){h.mode='chaingun';h.hammerDestroyed=true;hammerChainStart(B);}
  else if(name==='rage')hf22BeginBlueRage(B);
  else if(name==='beam'){h.mode='chaingun';h.hammerDestroyed=true;hammerState(B,'mega_charge');}
  else if(name==='ball')hammerState(B,'curl');
  else if(name==='stun')hammerState(B,'hammer_stun');
  else if(name==='heal'){h.frArmor={hp:600,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[],rage:false};fr27Restore(B,.2,false,false);}
 }HR23.active=true;};
HR23.step=function(dt=1/60){player.invuln=40002;player.dead=player.out=false;player.fireCd=9999;pBullets=[];updatePlay(dt);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt);HR23.states.add(run.stage===5?B?._hammer?.state:hb20State(B)?.action?.type||'ready');return{state,finite:Number.isFinite(B.x+B.y),keys:[...HR23.keys],states:[...HR23.states],bad:HR23.bad.slice(0,10),events:[...new Set(HR23.events)],combatEvents:HF22.events};};
HR23.capture=function(){return cv.toDataURL().split(',')[1];};
HR23.audio=async function(){const ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),seen=new WeakSet(),base=HTMLMediaElement.prototype.play,nodes=[],gains=[];
 const attach=el=>{if(seen.has(el))return;seen.add(el);try{if(el._bofNode){el._bofNode.connect(dest);gains.push(el._bofNode);}else{const stream=el.captureStream?.();if(stream&&stream.getAudioTracks().length){const n=ac.createMediaStreamSource(stream);n.connect(dest);nodes.push({n,stream});}}}catch(e){HR23.audioErrors??=[];HR23.audioErrors.push(String(e));}};
 HTMLMediaElement.prototype.play=function(){const r=base.apply(this,arguments);attach(this);return r;};for(const el of Object.values(Snd.music||{}))if(el instanceof HTMLMediaElement&&!el.paused)attach(el);
 HR23.audioRestore=()=>{HTMLMediaElement.prototype.play=base;for(const g of gains)try{g.disconnect(dest);}catch{}for(const{n,stream}of nodes){n.disconnect();stream.getTracks().forEach(t=>t.stop());}dest.stream.getTracks().forEach(t=>t.stop());};return dest.stream;};


