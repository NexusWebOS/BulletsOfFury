module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof RA7',ctxv)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/rebel_air_1007.js'),'utf8'),ctxv,{filename:'rebel_air_1007.js'});
 console.log('=== Rookhook, Ghostknife spiral and blue ace air battle ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;debugFight=null;run.pilot='yuri';run.mode='campaign';diffKey='normal';DIFF=DIFFS.normal;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];
 spawnBoss('rebelsquad');const b=boss,R=b._rebels;rf28Init(b,R);R.frIntro={done:true};b.enter=false;b._noHit=false;b._be=null;
 const G=rg4Init(b),q=R.ships[2];G.rescueDone=true;G.releaseAt=9999;
 function reset(){rg4Clear(G);G.scene=null;G.releaseAt=99999;G.gang=false;G.rescueDone=true;G.rebelBoxes=[];G.novaFx=[];G.ord=[];G.beams=[];
  eBullets=[];pBullets=[];RA7.deaths=[];RA7.events=[];GP4.death=null;GP4.deaths=[];
  for(const s of R.ships){delete s._ra7Death;delete s._gpDeath;delete s._on5Guard;s.dead=false;s.hp=s.max;s.mode='fight';s.warp=0;s.x=camLeftX()+64+s.i*75;s.y=150;s.rg4.act=null;s.rg4.armed=null;s.rg4.supply=null;s.rg4.cd=s.rg4.gunCd=999;}
  player.dead=false;player.out=false;player.roll=player.somer=player._chgDash=null;player.x=camLeftX()+viewW()/2;player.y=VH-100;player.invuln=1e9;delete player._ra7Caught;q.x=player.x;q.y=150;b.dead=false;bossActive=true;b.hp=b.maxhp;
 }
 function tick(seconds){for(let t=0;t<seconds;t+=.02)rg4AttackTick(q,R,G,.02);}
 reset();q.rg4.serial=0;out['Rook naturally cycles hook, slugs and ram']=Array.from({length:3},()=>ra4AttackKind(q,G)).join(',')==='rookhook,slug,ram';
 for(const d of ['easy','normal','hard','furious']){reset();diffKey=d;DIFF=DIFFS[d];rg4Attack(q,R,G,'rookhook');const A=q.rg4.act;
  out[d+' hook has at least 1.2 seconds of warning']=A.warm>=1.2&&A.phase==='charge';tick(A.warm*.6);const a=A.a;player.x+=100;tick(A.warm*.25);
  out[d+' hook commits before release']=A.a===a&&A.phase==='charge';tick(2.2);out[d+' committed hook misses a late sidestep']=A.reason==='miss'&&!player._ra7Caught;
 }
 reset();rg4Attack(q,R,G,'rookhook');let A=q.rg4.act;tick(A.warm+1);out['hook physically catches a stationary target']=A.phase==='reel'&&player._ra7Caught===A;
 tick(.5);out['reel pulls target toward the winch']=player.y<VH-140;
 tick(1.0);out['sling throws and releases before recovery']=A.phase==='recover'&&A.reason==='edge'&&!player._ra7Caught;
 out['edge throw stays in bounds']=player.x>=camLeftX()+20&&player.x<=camRightX()-20&&player.y<VH;
 reset();rg4Attack(q,R,G,'rookhook');A=q.rg4.act;A.phase='cast';A.ox=q.x;A.oy=q.y+25;A.a=Math.PI/2;A.distance=70;A.hx=q.x;A.hy=q.y+95;
 pBullets.push({kind:'mg',x:A.hx,y:A.hy+10,w:12,h:20,dmg:9});rg4AttackTick(q,R,G,.02);
 out['normal projectile can cut the grapple']=A.reason==='cut'&&pBullets[0].dead;
 reset();rg4Attack(q,R,G,'rookhook');A=q.rg4.act;A.phase='reel';A.px=player.x;A.py=player.y;A.reelX=q.x+70;A.reelY=q.y+110;player._ra7Caught=A;player.roll={t:0,dur:.4};rg4AttackTick(q,R,G,.02);
 out['barrel roll escapes an attached grapple']=A.reason==='evade'&&!player._ra7Caught;
 reset();rg4Attack(q,R,G,'rookhook');A=q.rg4.act;A.phase='reel';player._ra7Caught=A;q.dead=true;rebelSquadTick(b,.02);
 out['dead owner cancels a tether even after older layers clear its action']=!q.rg4.act&&!player._ra7Caught;
 reset();rg4Attack(q,R,G,'rookhook');A=q.rg4.act;A.phase='cast';A.hx=q.x;A.hy=q.y+50;
 out['airborne hook exposes an independent Retina target']=retinaBossTargets(b).some(t=>t._retinaId==='rookhook-'+A.serial);
 reset();rg4Attack(q,R,G,'rookhook');A=q.rg4.act;A.phase='reel';player._ra7Caught=A;R.hit=q.i;rebelSquadDamage(b,q.hp+1);
 out['real lethal hull damage releases the captured player immediately']=q.dead&&!player._ra7Caught;
 out['new death retires the old second wreck']=!!q._ra7Death&&!q._gpDeath;
 out['death uses original pilot timing and angle range']=q._ra7Death.dur===DS_DUR&&q._ra7Death.crashT===DS_CRASH&&q._ra7Death.turns>=540&&q._ra7Death.turns<=900;
 for(let i=0;i<64;i++)rebelSquadTick(b,.02);
 out['rebel crashes at pilot spin duration']=q._ra7Death.crashed&&q._ra7Death.t<1.3;
 reset();G.gang=true;for(const s of R.ships){R.hit=s.i;rebelSquadDamage(b,s.hp+1);}GP4.deaths=[];GP4.death=null;
 for(let i=0;i<95;i++)rebelSquadTick(b,.02);
 out['all dead rebel wrecks still resolve the real boss reward']=b.dead&&bossDefeated;
 reset();const nyx=R.ships[1];rg4Attack(nyx,R,G,'cloak');for(let i=0;i<62;i++)rg4AttackTick(nyx,R,G,.02);
 const pulse=nyx.rg4.act._ra7Pulse;out['cloaked Nyx warns a complete committed ambush']=!!pulse&&pulse.t<pulse.warm;
 const angle=pulse.a;player.x+=100;for(let i=0;i<40;i++)rg4AttackTick(nyx,R,G,.02);
 out['Nyx fires three real rounds along her earlier committed aim']=eBullets.filter(p=>p._ra7Ghost).length===3&&Math.abs(Math.atan2(eBullets.find(p=>p._ra7Ghost).vy,eBullets.find(p=>p._ra7Ghost).vx)-(angle-.14))<.0001;
 beginStage(6);setState(GS.PLAY);spawnBoss('warhive');const blue=boss;whvAceSpawn(blue);blue._whv.mode='ace';const ace=blue._whv.ace;ace.st='fight';ace.x=player.x=camLeftX()+viewW()/2;ace.y=180;ace.dash=ace.desp=ace.roll=ace.somer=null;ace._pw5Gun=null;eBullets=[];
 ra7AceStart(blue,ace);for(let i=0;i<180;i++)ra7AceTick(blue,ace,.02);
 out['blue ace paired batteries emit three six-round salvos']=eBullets.filter(p=>p._ra7Gate).length===18;
 out['blue ace wing rounds diverge away from the central corridor']=eBullets.filter(p=>p._ra7Gate).every(p=>p.x<ace.x?p.vx<=.001:p.vx>=-.001);
 out['blue ace has recovery after the last salvo']=ace._ra7Gate?.phase==='recover';
 blue._gp4Host={};out['new ace motif does not hijack copied finale controller']=!ra7AceReady(blue,ace);
 delete blue._gp4Host;blue.dead=true;blue.dying=0;ace.desp={st:'cross',t:0,lead:.62};ace.dash={st:'warn'};whvAceDeathTick(blue,.02);
 out['ace death retires living warnings that would hide its wreck']=!ace.desp&&!ace.dash&&!ace.roll&&!ace.somer&&ace._ra7Death&&!ace.crash;
 beginStage(1);out['fresh stage clears death and tether session state']=RA7.deaths.length===0&&!player._ra7Caught;
 return out;})())`,ctxv));
 for(const [name,value] of Object.entries(out))ok(value,name);
 const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/game/rebel_air_1007/manifest.json'),'utf8'));
 ok(Object.keys(manifest.cells).length===12&&manifest.nativeSize.join('x')==='1448x1086','twelve authored cells retain native dimensions');
 const crypto=require('crypto');ok(crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'../assets/game/rebel_air_1007/rebel_air.png'))).digest('hex')===manifest.sha256,'deployed native-alpha art matches its generated source hash');
};
