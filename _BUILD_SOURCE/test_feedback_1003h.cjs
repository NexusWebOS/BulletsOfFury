module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/feedback_1003h.js'),'utf8'),ctxv,{filename:'feedback_1003h.js'});
 console.log('=== October 3h protected story sequences and Hammer homecoming ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;s6Opening=null;s6Wing=null;boss=null;bossActive=false;enemies=[];eBullets=[];pBullets=[];special=null;
 fb2TalkStart();const initial=fb2Talk.i,ammo=run.bombs,clock=stageTimer;
 const tap=Input.tapAny;Input.tapAny=()=>true;
 for(let i=0;i<30;i++){updatePlay(1/60);pShoot();useBomb();startSpecial();}
 Input.tapAny=tap;
 o['held confirm cannot reveal or skip the team speech']=fb2Talk.i===initial&&fb2Talk.shown<fb2Talk.beats[initial].text.length;
 o['locked speech cannot spend ammo, create attacks, or advance combat']=run.bombs===ammo&&pBullets.length===0&&stageTimer===clock&&!special;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;spawnBoss('rebelsquad');
 const b=boss;updatePlay(.1);const hp=b.hp;b._rebels.hit=0;rebelSquadDamage(b,1000);
 o['rebel speech owns vulnerability before combat starts']=b.hp===hp&&b._noHit&&h3Locked();
 o['every live rebel gets its own line']=b._rebels.ships.filter(q=>!q.dead).every(q=>b._rebels.h3Intro.rows.some(l=>l.who===q.key.toUpperCase()));
 for(const d of ['normal','furious']){
  diffKey=d;DIFF=DIFFS[d];beginStage(5);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;spawnBoss(curStage.boss);const b=boss,hp=b.hp;const a=fr27BeginArmor(b);
  o[d+' Hammer armor reduction does not alter body HP']=Math.abs(a.max-(d==='furious'?Math.round(b.maxhp*.75):b.maxhp*.3))<.001&&b.hp===hp;
 }
 return o;})())`,ctxv));
 for(const [name,pass] of Object.entries(rows))ok(pass,name);
};
