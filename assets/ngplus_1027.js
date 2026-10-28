"use strict";
/* NG+ changes live in their own owner. Ordinary campaigns/passwords retain
   their original budgets; native part routing and cinematic clocks remain owners. */
const NG27={hp:1.25,attack:1.15,damage:1.12,scaled:new WeakMap(),events:[],
 base:{spawn:spawnBoss,mini:spawnSubBoss,enemy:spawnEnemy,forms:ensureForgeForms,
 enter:v18Enter,budget:v18Budget,s7:s7mInit,play:updatePlay,damage:elementalDamageResult,
 load:stageLoadBegin,bullets:drawBullets,shot:eShootT,reward:ap10StageXReward,
 forgeBudget:hf23Budget,earned:hf23Earned,snapshot:campSnapshot,apply:campApply,
 mist:laserMistIsUnlocked,chain:chaingunIsUnlocked,orb:yuriLightningOrbIsUnlocked,start:startRun,hasForms:hf23HasForms}};
function ng27On(){return !!run?.ngplus;}
laserMistIsUnlocked=function(){return ng27On()||NG27.base.mist.apply(this,arguments);};
chaingunIsUnlocked=function(){return ng27On()||NG27.base.chain.apply(this,arguments);};
yuriLightningOrbIsUnlocked=function(){return ng27On()||NG27.base.orb.apply(this,arguments);};
startRun=function(){const out=NG27.base.start.apply(this,arguments);if(ng27On()){
 ensureForgeForms();for(const a of Object.values(NG27_ART))XART.rdy(a.key);
 }return out;};
function ng27Log(event,data={}){NG27.events.push({event,...data});if(NG27.events.length>160)NG27.events.shift();}
// Scale a health pair once at its creation, preserving partial health and zero.
function ng27Pair(q,h,m,fields){
 if(!q||!Number.isFinite(q[h])||!Number.isFinite(q[m])||q[m]<=0)return;
 let memo=NG27.scaled.get(q);if(!memo)NG27.scaled.set(q,memo={});
 if(memo[m]===q[m]){fields?.add(h);return;}
 const k=NG27.hp;if(!fields?.has(h))q[h]*=k;q[m]*=k;memo[m]=q[m];fields?.add(h);
}
function ng27Health(root){
 if(!ng27On()||!root)return;const seen=new Set();
 function visit(q,depth){
  if(!q||typeof q!=='object'||seen.has(q)||depth>7)return;seen.add(q);
  const fields=new Set();
  for(const [h,m]of [['hp','maxhp'],['hp','max'],['core','coreMax'],['shield','shieldMax'],
    ['hammerHP','hammerMax'],['chainHP','chainMax'],['health','maxHealth']])ng27Pair(q,h,m,fields);
  // Future Nightwing life is a stored budget, not the current carrier's HP.
  if(Number.isFinite(q.aceMax)&&!q._ng27Ace){q.aceMax*=NG27.hp;q._ng27Ace=true;}
  for(const k of Object.keys(q)){
   if(/^(history|events|fx|shots|beams|bombs|pillars|trail|trails|spec|def|art|owner|parent|target|targets|_ng)/i.test(k))continue;
   const v=q[k];if(v&&typeof v==='object')visit(v,depth+1);
  }
 }visit(root,0);
}
spawnBoss=function(){const out=NG27.base.spawn.apply(this,arguments);if(boss&&!boss._r30)ng27Health(boss);return out;};
spawnSubBoss=function(){const out=NG27.base.mini.apply(this,arguments);ng27Health(subBoss);return out;};
s7mInit=function(b){const out=NG27.base.s7.apply(this,arguments);if(ng27On()){ng27Health(out);ng27Health(b);}return out;};
// Copy pools are born before their modules. Scale the source budgets, so future
// modules and restored copies inherit exactly the same 25%, without healing.
v18Budget=function(b){const out=NG27.base.budget.apply(this,arguments),J=j3State(b);
 if(ng27On()&&J&&!J._ng27Budget){J.max=J.max.map(v=>v*NG27.hp);J.hp=J.hp.map(v=>v*NG27.hp);J._ng27Budget=true;}
 return out;};
v18Enter=function(b,n,form=0){const out=NG27.base.enter.apply(this,arguments);
 if(ng27On()&&n!==2){ng27Health(b.parts);ng27Pair(b,'hp','maxhp');b._vPhaseHp=b.maxhp;}
 return out;};
const NG27_ELEMENT={1:'kinetic',2:'fire',3:'ice',4:'lightning',5:'chrome',6:'wind',7:'toxic',8:'dark',9:'water',10:'wind'};
spawnEnemy=function(){const e=NG27.base.enemy.apply(this,arguments);if(ng27On()&&e){
 ng27Health(e);const stage=run.stage|0,hash=[...String(e.type)].reduce((n,c)=>n+c.charCodeAt(0),0);
 e._ng27Element=hash%4===0?['fire','ice','lightning','dark'][(hash>>2)%4]:NG27_ELEMENT[stage]||'dark';
 // Native fire/ice resist/weakness logic reads this same launch identity.
 e.element=e._ng27Element;
 }return e;};
ensureForgeForms=function(){const F=NG27.base.forms.apply(this,arguments);
 if(ng27On()){
  run.forgeElems??={};run.forgeElems.dark=1;
  // NG+ rewards are available through the existing in-flight loadout at no cost.
  // Re-Spec suppresses profile imports, not this earned NG+ arsenal.
  for(const w of FORGE_WEAPONS){F[w]??={};F[w].dark??={elem:'dark',lv:1};}
 }return F;};
hf23Budget=function(){
 if(run._forgeBudget23||!ng27On())return NG27.base.forgeBudget.apply(this,arguments);
 const forms=run.forgeForms,forge=run.forge,free=(el,w)=>el==='dark'||rs22Kept(el,w);
 run.forgeForms=Object.fromEntries(Object.entries(forms||{}).map(([w,F])=>[w,Object.fromEntries(Object.entries(F).filter(([el])=>!free(el,w)))]));
 run.forge=Object.fromEntries(Object.entries(forge||{}).filter(([w,F])=>!free(F.elem,w)));
 try{return NG27.base.forgeBudget.apply(this,arguments);}finally{run.forgeForms=forms;run.forge=forge;}
};
hf23Earned=function(){return NG27.base.earned.apply(this,arguments)+(hf23Budget().bonus27||0);};
hf23HasForms=function(){if(!ng27On())return NG27.base.hasForms.apply(this,arguments);
 return Object.keys(run.forge||{}).length>0||Object.values(run.forgeForms||{}).some(F=>Object.keys(F).some(el=>el!=='dark'));
};
elementalDamageResult=function(t,role,b,dmg,x,y){
 // Maverick's separate homing lances retain their fixed combat contract.
 if(ng27On()&&b?.kind!=='mavlaser')dmg*=NG27.damage;
 return NG27.base.damage.call(this,t,role,b,dmg,x,y);
};
// Accelerate only actual decreasing attack cooldowns and recovery/idle clocks.
// No global dt multiplier: entrances, warnings, bullets and deaths keep real time.
function ng27Clocks(root){const list=[],seen=new Set();
 function visit(q,d){if(!q||typeof q!=='object'||seen.has(q)||d>6)return;seen.add(q);
  const mode=q.mode??q.state??q.st??q.phase??null;
  if(/warn|tell|charge|windup|entry|arriv|portal|reveal|transform|rebirth|monologue|stun|dead|death/i.test(String(mode)))return;
  for(const k of Object.keys(q)){
   const v=q[k];
   if(typeof v==='number'&&v>0&&v<100&&/^(fireCd|shotCD|shotCd|gunCd|mslCd|attackCd|cd|cooldown)$/.test(k))list.push({q,k,v,mode});
   if(v&&typeof v==='object'&&!/^(history|events|fx|shots|beams|bombs|pillars|trail|spec|def|art|owner|parent|target)/i.test(k))visit(v,d+1);
  }
  if(/^(idle|hammer|rest|recover|cool|chain_cool|storm_idle)$/.test(mode)&&Number.isFinite(q.t))list.push({q,k:'t',v:q.t,mode,up:true});
 }visit(root,0);return list;}
function ng27Advance(list){for(const a of list){const now=a.q[a.k],mode=a.q.mode??a.q.state??a.q.st??a.q.phase??null;
 if(mode!==a.mode||!Number.isFinite(now))continue;
 if(a.up&&now>a.v&&now-a.v<=.051)a.q[a.k]+= (now-a.v)*(NG27.attack-1);
 else if(!a.up&&now>0&&now<a.v&&a.v-now<=.25)a.q[a.k]=Math.max(0,now-(a.v-now)*(NG27.attack-1));
 }}
function ng27Combat(b){return !!b&&!b.dead&&!b.enter&&(!b._r30||b._r30.mode==='fight');}
// Keep physical ordnance, launch vectors, native interception and collision sizes.
// Only generic small-energy rounds receive authored elemental flight plates.
function ng27Stamp(b,owner){if(!ng27On()||!b||!owner?._ng27Element||!/^(mg|bolt|pellet|s1bullet|plasma)$/.test(b.kind))return;
 b._ng27Element=owner._ng27Element;b._el=b._ng27Element;b._ng27Shot=true;
}
eShootT=function(x,y,a,s,k,o){const b=NG27.base.shot.apply(this,arguments);
 if(ng27On()){let owner=o?.owner;if(!owner)owner=enemies.filter(e=>!e.dead&&e._ng27Element).sort((u,v)=>Math.hypot(u.x-x,u.y-y)-Math.hypot(v.x-x,v.y-y))[0];
  if(owner&&Math.hypot(owner.x-x,owner.y-y)<Math.max(owner.w||0,owner.h||0,75))ng27Stamp(b,owner);
 }return b;};
updatePlay=function(dt){
 if(!ng27On()||state!==GS.PLAY)return NG27.base.play.apply(this,arguments);
 const clock=[...ng27Combat(boss)?ng27Clocks(boss):[],...ng27Combat(subBoss)?ng27Clocks(subBoss):[]];
 const old=new Set(eBullets),out=NG27.base.play.apply(this,arguments);ng27Advance(clock);
 for(const b of eBullets)if(!old.has(b)&&!b._ng27Shot){
  const e=enemies.filter(e=>!e.dead&&e._ng27Element).sort((u,v)=>Math.hypot(u.x-b.x,u.y-b.y)-Math.hypot(v.x-b.x,v.y-b.y))[0];
  if(e&&Math.hypot(e.x-b.x,e.y-b.y)<Math.max(e.w||0,e.h||0,75))ng27Stamp(b,e);
 }return out;};
for(const [el,a]of Object.entries(NG27_ART))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return NG27.base.load.call(this,n,ng27On()?[...(keys||[]),...Object.values(NG27_ART).map(a=>a.key)]:keys);};
function ng27ShotDraw(b){const a=NG27_ART[b._ng27Element];if(!b._ng27Shot||b.dead||!a||!XART.rdy(a.key))return false;
 const direction=((Math.round((Math.atan2(b.vy,b.vx)+Math.PI/2)*32/TAU)%32)+32)%32,
 frame=Math.floor(projectileVisualAge(b)*24)%16;
 ctx.drawImage(XART.get(a.key),direction*72,frame*72,72,72,Math.round(b.x-36),Math.round(b.y-36),72,72);return true;}
drawBullets=function(){if(!ng27On())return NG27.base.bullets.apply(this,arguments);
 const all=eBullets,owned=all.filter(b=>b._ng27Shot&&NG27_ART[b._ng27Element]&&XART.rdy(NG27_ART[b._ng27Element].key));
 eBullets=all.filter(b=>!owned.includes(b));try{NG27.base.bullets.apply(this,arguments);}finally{eBullets=all;}
 for(const b of owned)ng27ShotDraw(b);
};
// Existing Air Superiority reward: either route, native defeat, one receipt.
ap10StageXReward=function(){if(!bossDefeated)return;
 const first=!!run._gp4StageX&&!run._ap10XReward&&!campaign.stageX1004?.rewarded;
 if(first)hf23Budget();const out=NG27.base.reward.apply(this,arguments);
 if(first&&run._ap10XReward){hf23Budget().bonus27=(hf23Budget().bonus27||0)+1;ng27Log('stage-x-reward',{route:run._gp4StageX});}
 return out;};
campSnapshot=function(){const s=NG27.base.snapshot.apply(this,arguments);if(s)s.forgeBonus27=hf23Budget().bonus27||0;return s;};
campApply=function(s){const out=NG27.base.apply.apply(this,arguments);if(out){
 const B=hf23Budget();B.bonus27=s?.rival24?.stageX1004?.rewarded?1:Math.min(1,Math.max(0,s?.forgeBonus27|0));
 run.forgeCombos=clamp(s.forgeCombos|0,0,hf23Earned());if(ng27On())ensureForgeForms();
 }return out;};
