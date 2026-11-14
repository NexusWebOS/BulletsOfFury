/* Recording-only keyboard pilot/observer. Never included in the shipped game.
   Does not write enemy HP, phases, attack clocks, wave gates or clear flags. */
globalThis.FILM1111={enabled:false,start:0,config:null,targetKey:'',lastMissile:-100,lastEvade:-100,lastDialog:-100,errors:[],events:[],spawned:[],waves:[],seenForms:new Set(),seenGuns:new Set(),weak:new WeakMap(),serial:0,lastState:null,everBoss:false,everMini:false,defeated:false,maxEnemies:0,maxRounds:0,gunFrames:new Set(),phase:null};
function film1111ObjectKey(t){const A=FILM1111,owner=t._retinaOwner||t._boss||t.owner||t;if(typeof owner==='object'&&owner&&!A.weak.has(owner))A.weak.set(owner,++A.serial);return(A.weak.get(owner)||'v')+':'+String(t._retinaId||t.id||t.name||t.kind||t.type||'core');}
function film1111Bindings(action){return keybindFor(1)[action]||({left:['a'],right:['d'],up:['w'],down:['s'],fire:['j'],retina:['c'],bomb:['k']})[action]||[];}
function film1111Tap(action){const a=film1111Bindings(action),k=a.find(k=>!k.startsWith('pad_')&&!k.startsWith('mouse'))||a[0];if(k)Input.injectTap(k);}
function film1111Hold(action,on=true){for(const k of film1111Bindings(action))if(!k.startsWith('pad_')&&!k.startsWith('mouse'))Input.keys[k]=on;}
function film1111Input(){const A=FILM1111;if(!A.enabled)return;const elapsed=(performance.now()-A.start)/1000;for(const key of ['left','right','up','down','fire','retina'])film1111Hold(key,false);
 if(A.lastState!==state){A.events.push({event:'screen',state,at:elapsed,stage:run.stage});A.lastState=state;}
 A.everBoss||=!!bossActive;A.everMini||=!!subBossActive;A.defeated||=!!bossDefeated;A.maxEnemies=Math.max(A.maxEnemies,enemies.length);A.maxRounds=Math.max(A.maxRounds,eBullets.length);
 if(state!==GS.PLAY||player.dead||player.out)return;
 if(s6Wing?.choice&&!s6Wing.route){if(elapsed-A.lastDialog>.9){film1111Tap('left');film1111Tap('fire');A.lastDialog=elapsed;}return;}
 if((story||fb2Talk||fb2Intro||thaw)&&elapsed-A.lastDialog>2.5){film1111Tap('fire');A.lastDialog=elapsed;}
 const b=bossActive&&boss&&!boss.dead?boss:subBossActive&&subBoss&&!subBoss.dead?subBoss:null;
 let targets=b?retinaBossTargets(b):_lockTargets();targets=targets.filter(t=>t&&!t.dead&&!t.destroyed&&(t.hp??1)>0&&Number.isFinite(t.x+t.y)&&t.y>=viewTopY()-140&&t.y<VH-18&&t.x>=camLeftX()-30&&t.x<=camRightX()+30);
 if(b&&!targets.length&&b.hp>0)targets=[{x:b.x,y:b.y,hp:b.hp,id:'visible-body',kind:b.kind,_retinaOwner:b}];
 let target=targets.find(t=>film1111ObjectKey(t)===A.targetKey);
 if(!target){targets.sort((a,b)=>{const heavy=t=>t._retinaOwner?._sc12||t._retinaOwner?._ca111||t._sc12||t._ca111?-2000:0;return heavy(a)-heavy(b)+Math.abs(a.x-player.x)-Math.abs(b.x-player.x)+(b.y-a.y)*.15;});target=targets[0];A.targetKey=target?film1111ObjectKey(target):'';A.lastHp=target?.hp;A.lastProgress=elapsed;}
 if(target&&target.hp<(A.lastHp??Infinity)-.01){A.lastHp=target.hp;A.lastProgress=elapsed;}
 if(target&&elapsed-A.lastProgress>8&&targets.length>1){target=targets[(targets.indexOf(target)+1)%targets.length];A.targetKey=film1111ObjectKey(target);A.lastHp=target.hp;A.lastProgress=elapsed;}
 let observe=false;
 if(b){const J=b._r30&&j3State(b),form=J?String(J.encounter)+':'+String(b._r30.v18?.form??0):b.kind;
  if(A.owner!==b||A.form!==form){A.owner=b;A.form=form;A.observeUntil=elapsed+(bossActive?7:4);A.events.push({event:'encounter',at:elapsed,kind:b.kind,form,hp:b.hp,maxhp:b.maxhp});}
  const Q=rd74Own(b)&&hb20State(b);if(Q?.action?.type==='gun'&&!A.seenGuns.has(form)){A.seenGuns.add(form);A.observeUntil=Math.max(A.observeUntil,elapsed+2.7);}
  if(Q&&dgm1111Active(b))A.gunFrames.add(dgm1111Frame(Q));
  const phase=b._hammer?.state||b._s7mod?.mode||b._r30?.mode||b._bomber?.mode||b._late27?.mode||b._whv?.st||null;
  if(A.phase!==phase){A.events.push({event:'action',at:elapsed,kind:b.kind,phase,form,hp:b.hp});A.phase=phase;}
  observe=elapsed<(A.observeUntil||0);
 }
 const tx=clamp(target?.x??worldWidth()/2,camLeftX()+24,camRightX()-24),ty=b?._pb28&&['boost','ahead'].includes(b._pb28.mode)?VH*.35:VH-62;
 film1111Hold('left',player.x>tx+5);film1111Hold('right',player.x<tx-5);film1111Hold('up',player.y>ty+7);film1111Hold('down',player.y<ty-7);
 film1111Hold('fire',!observe&&!!target&&elapsed%1.0<.78);film1111Hold('retina',!observe&&!!target);
 const heavy=!!b||target&&(target._retinaOwner?._sc12||target._retinaOwner?._ca111||target._sc12||target._ca111);
 if(!observe&&heavy&&run.bombs>0&&(b||run.bombs>20)&&elapsed-A.lastMissile>2.2){film1111Tap('bomb');A.lastMissile=elapsed;}
 if(!observe&&elapsed-A.lastEvade>10){Input.injectTap(elapsed%20<10?'q':'e');A.lastEvade=elapsed;}
 A.target=target?{id:A.targetKey,x:target.x,y:target.y,hp:target.hp,kind:target.kind||target.type}:null;
}
function film1111ObservePlan(){const A=FILM1111;A.expected=stagePlan.length;
 for(let i=0;i<stagePlan.length;i++){const w=stagePlan[i],native=w.fn;if(typeof native!=='function')continue;const wrapped=function(){const at=(performance.now()-A.start)/1000;try{return native.apply(this,arguments);}finally{if(waveIdx>=i&&!A.waves.some(e=>e.i===i))A.waves.push({i,planned:w.t,at,clock:stageTimer});}};Object.assign(wrapped,native);w.fn=wrapped;}
 const spawn=spawnEnemy;spawnEnemy=function(){const e=spawn.apply(this,arguments);if(e)A.spawned.push({at:(performance.now()-A.start)/1000,type:e.type,hp:e.hp,model:e._s811?.model||e._s711?.model||e._s511?.model||e._v31?.model});return e;};
}
function film1111Snapshot(){const A=FILM1111,b=bossActive?boss:subBossActive?subBoss:null,J=b?._r30&&j3State(b);return{wall:(performance.now()-A.start)/1000,state,stage:run.stage,difficulty:diffKey,stageTimer,waveIdx,waves:A.waves.length,expected:A.expected,bossActive,subBossActive,bossDefeated,everBoss:A.everBoss,everMini:A.everMini,defeated:A.defeated,kind:b?.kind,hp:b?.hp,maxhp:b?.maxhp,mode:b?._hammer?.state||b?._r30?.mode||b?._s7mod?.mode||b?._whv?.st,phase:J?.encounter,form:b?._r30?.v18?.form,parts:b?.parts?.map(p=>({id:p.id,hp:p.hp,dead:p.destroyed})),armor:b?._hammer?.frArmor?.hp,heldGun:b?._hammer?.chainHP,weapon:run.weapon,level:run.wlevel,spaceWeapon:run.spaceWeapon,spaceLevels:run.spaceLevels,target:A.target,player:{x:player.x,y:player.y,dead:player.dead},god:DBGT.god,preventedHits:captureStats.preventedHits,bombs:run.bombs,director:BOFCinematicDirector.current?.id,story:!!story,nativeFrames:__bofFrames,frames:captureStats.frames,audioPeak:captureStats.peak,botErrors:A.errors,maxEnemies:A.maxEnemies,maxRounds:A.maxRounds,gunPhases:A.gunFrames.size};}
