"use strict";
/* Late heavy hulls retain authored weight. A visible weapon muzzle can begin
   its native tell while a large hull is still entering the playfield. */
const LF19={base:{spawn:spawnEnemy,begin:ai27Begin,hit:_hitEnemyCore},heavy:new Set(['s7tank','s7barge','s8deathorb','s8carrier','s8bomber','s8tentacle'])};
function lf19Spec(e){return run.stage===7?S7TOXIC[e?._s7toxic]:run.stage===8?S8MEGA[e?._s8mega]:null;}
function lf19Pool(e){const spec=lf19Spec(e);if(window.LF19_OFF===1||!spec||!LF19.heavy.has(e.type)||e._lf19Hp)return;
 const current=EHP(spec.hp),saved=diffKey;let normal=current;
 try{diffKey='normal';normal=EHP(spec.hp);}finally{diffKey=saved;}
 e.hp=e.maxhp=e._maxhp=Math.max(current,Math.round(spec.hp*current/Math.max(1,normal)*le19PartyFactor()));e._lf19Hp=true;
}
spawnEnemy=function(){const first=enemies.length,r=LF19.base.spawn.apply(this,arguments);for(let i=first;i<enemies.length;i++){
 const e=enemies[i];lf19Pool(e);
 // The independent Stage 5 helper owns its solo pool. Restore only the canceled
 // party factor here, keeping that helper and its baseline switch intact.
 if(run.stage===5&&e._ca19Hp&&!e._lf19Party&&window.CA19_OFF!==1&&le19PartyFactor()>1){
  e.hp=e.maxhp=e._maxhp=Math.round(e.hp*le19PartyFactor());e._lf19Party=true;
 }
}return r;};
ai27Begin=function(e,dt){const old=LF19.base.begin.apply(this,arguments);
 if(window.LF19_OFF===1||!lf19Spec(e)||!LF19.heavy.has(e.type)||!e._ai27)return old;
 const p=e._modTank?modularTankMuzzle(e):combatHardpoint(e,0,.31),visible=p.x>=camLeftX()+12&&p.x<=camRightX()-12&&p.y>=PLAY.y+8&&p.y<VH-30;
 e._lf19Seen=visible?(e._lf19Seen||0)+dt:0;e._ai27.visible=visible;e._ai27.seen=e._lf19Seen;
 return old;
};
_hitEnemyCore=function(e){const b=typeof _dmgBullet==='undefined'?null:_dmgBullet;
 // This only rejects projectile contacts outside the actual playfield. Area
 // attacks keep their native owner and visible hulls keep normal hit feedback.
 if(window.LF19_OFF!==1&&lf19Spec(e)&&b&&Number.isFinite(b.x)&&Number.isFinite(b.y)&&
  (b.y<0||b.y>VH||b.x<camLeftX()||b.x>camRightX()))return;
 return LF19.base.hit.apply(this,arguments);
};
window.BOF_LATE_FLEET={state:LF19,pool:lf19Pool};
