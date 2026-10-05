module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 for(const n of ['overnight_art_1005.js','overnight_finale_1005.js','overnight_combat_1005.js','overnight_routes_1005.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+n),'utf8'),c,{filename:n});
 console.log('=== Overnight persistent finale, sustained Rebel beams and live Gang shields ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;debugFight=null;diffKey='furious';DIFF=DIFFS.furious;run.pilot='cole';run.mode='campaign';
 beginStage(8);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();H3.release=false;fb2Talk=null;s6Opening=null;s6Wing=null;player.reset();
 spawnBoss('vileexistence');const b=boss,J=j3State(b),S=b._r30;
 out['copies get larger budgets than each live source boss']=J.max.every((h,i)=>h>J3_SOURCE_HP.furious[i]);
 out['outer fight one starts as normal drone before mutation']=J.encounter===0&&S.mode==='arrival1003j';
 for(const n of [0,1]){j3Encounter(b,n);on5FightStart(b);const seen=[];eBullets=[];
  for(let i=0;i<4;i++){r30Attack(b);seen.push(S.attack.type);r30AttackTick(b,S.attack.tell+.01);S.attack=null;}
  out['outer phase '+(n+1)+' has four independent attack signatures']=new Set(seen).size===4&&seen.every(t=>t.startsWith(n?'ghost':'host'));
  out['outer phase '+(n+1)+' emits real projectiles']=eBullets.some(q=>q._r30Owner===b&&!q.dead);
 }
 j3Encounter(b,1);out['ghost receives its own cinematic']=S.mode==='ghostIntro1005';
 j3Encounter(b,2);out['Dracula begins in black void cinematic']=S.mode==='voidIntro1005';
 const fills=[];for(let i=0;i<8;i++){S.t=4.3+i*.5+.1;fills.push(fmcGauge(b).charge);}out['one housing fills all eight colors']=fills.join(',')==='0,1,2,3,4,5,6,7';
 S.mode='fight';b.enter=false;b.hp=J.max[0]*.42;j3Save(b);const host=b.hp;j3Mimic(b,5);S.mode='fight';b.enter=false;
 const max=b.maxhp;b.hp=max*.51;j3Save(b);const hp=b.hp;j3Home(b);
 out['returning to Dracula does not borrow fresh copy health']=b.hp===host&&J.hp[5]===hp;
 j3Mimic(b,5);S.mode='fight';b.enter=false;out['wounded copy resumes its exact HP']=b.hp===hp&&b.maxhp===max;
 out['knight body remains whole with only weapons separate']=b.parts.map(p=>p.id).sort().join(',')==='core,shield,sword';
 const blade=b.parts.find(p=>p.id==='sword');blade.destroyed=true;out['destroying sword cannot remove the knight head']=fmcAlive(b,'head')&&fmcRig(b).some(v=>v.p.id==='core')&&!fmcRig(b).some(v=>v.p.id==='sword');blade.destroyed=false;
 on5Shield(b,'red',39);S.wallAge1003=1;b._lastPart={id:'codeWall1003d'};modularHit(14);out['code shield takes exact damage']=S.shield===25;
 modularHit(25);out['shield reaches zero and shatters all digit fragments']=S.shield===0&&!S.on5Shield&&CWD.effects.filter(f=>f.owner===b&&f.kind==='chip').length>=24;
 r30Clear(b);out['copy cleanup cannot erase ongoing code shatter']=CWD.effects.some(f=>f.owner===b&&f.kind==='shatter');
 J.hp[2]=0;J.cursor=1;J.mimic=null;J.active=0;j3Morph(b,0);out['dead copies cannot be selected again']=J.destination!==2&&J.hp[J.destination]>0;
 beginStage(6);spawnBoss('rebelsquad');const R=boss._rebels;rf28Init(boss,R);R.frIntro={done:true};boss.enter=false;boss._noHit=false;const G=rg4Init(boss);G.rescueAt=G.releaseAt=9999;
 for(const q of R.ships){q.mode='fight';q.warp=0;q.x=player.x;q.y=200;q.rg4.act=null;}const q=R.ships[0],old=q.hp;
 on5RebelLaser({kind:'beam',x:q.x,top:0,bot:500,w:12,dmg:3},1/60);out['sustained laser routes damage to Rebel hull']=q.hp<old;
 const nyx=R.ships.find(q=>q.key==='nyx');nyx.frCloak=5;const cloakHP=nyx.hp;
 on5RebelLaser({kind:'beam',x:nyx.x,top:0,bot:500,w:12,dmg:3},1/60);out['cloak blocks missile acquisition but not direct laser collision']=nyx.hp<cloakHP;
 const timer=stageTimer,bullets=eBullets;rg4GangStart(boss,G);out['Gang defense does not freeze time or clear hostile fire']=G.gang&&!G.scene&&!boss._noHit&&stageTimer===timer&&eBullets===bullets;
 const guarded=q.hp;R.hit=q.i;rebelSquadDamage(boss,q._on5Guard.hp+1);out['live Gang shield breaks independently']=!q._on5Guard&&q.hp===guarded;
 const A={a:Math.PI/4};ra4Helix(R.ships.find(q=>q.key==='jace'),G,A);const ball=G.ord.at(-1);out['Jace helix ball travels fast directly south']=ball.vx===0&&ball.vy===380;
 rg4Round(q,0,6,'mg',{_ra4Slug:true});const slug=eBullets.at(-1);out['Rook special slugs travel south']=slug.vy>0&&Math.abs(slug.vx)<1e-6;
 out['robot chant premix is not used']=BOFA.music.hama==='assets/game/music/HAMA_Instrumental.mp3'&&!hamaRecordedVocals1001();
 out['epsilon-width animated beams cannot stall the renderer']=av3Beam(null,10,20,Math.PI/2,500,1e-12,'ice')===false;
 out['invalid beam geometry never enters authored-strip tiling']=av3Beam(null,10,20,Math.PI/2,Infinity,20,'ice')===false;
 out['boss passwords respect six-character input']=Object.keys(ON5_CODES).every(k=>k.length<=6);
 out['all nine boss slots and three outer phases have passwords']=Array.from({length:9},(_,i)=>ON5_CODES['BOSS'+(i+1)]).every(Boolean)&&[1,2,3].every(n=>ON5_CODES['FINAL'+n].phase===n-1);
 for(const code of ['FINAL1','FINAL2','FINAL3','KNIGHT','MINI8','ALT6']){pwInput=code;submitPassword();const E=ON5_CODES[code];startRun(E.stage);out[code+' uses actual start-run route']=run.stage===E.stage&&!!(E.role==='boss'?boss:subBoss)&&ON5.pending===null;}
 setState(GS.TITLE);return out;
 })())`,c));for(const[n,v]of Object.entries(out))ok(v,n);
};
