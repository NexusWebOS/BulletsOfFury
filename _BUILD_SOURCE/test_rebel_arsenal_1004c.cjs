module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const name of ['rebel_arsenal_art_1004c.js','rebel_arsenal_1004c.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+name),'utf8'),ctxv,{filename:name});
 console.log('=== Rebel pilot bars, survivor counter-scan and personal arsenals ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;debugFight=null;run.pilot='yuri';run.mode='campaign';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];
 spawnBoss('rebelsquad');const b=boss,R=b._rebels;rf28Init(b,R);R.frIntro={done:true};b.enter=false;b._noHit=false;b._be=null;
 for(const q of R.ships){q.mode='fight';q.warp=0;q.x=camLeftX()+64+q.i*75;q.y=160;}
 const G=rg4Init(b);G.rescueDone=true;G.releaseAt=9999;
 out['five personal roles match the requested dogfight arsenals']=R.ships.map(q=>q.rg4.role).join(',')==='turbo,cloak,slug,rockets,helix';
 for(const q of R.ships){q.rg4.cd=999;q.rg4.gunCd=0;}rebelSquadTick(b,.05);
 out['all five rebels fire actual baseline gun rounds']=R.ships.every(q=>eBullets.some(p=>p._ra4Gun&&p.owner===q));
 function clear(){G.scene=null;G.ord=[];G.beams=[];G.rebelBoxes=[];G.releaseAt=9999;eBullets=[];pBullets=[];for(const q of R.ships){q.rg4.act=null;q.rg4.supply=null;q.rg4.armed=null;q.rg4.cd=999;q.dead=false;q.hp=q.max;q.frCloak=0;q.x=camLeftX()+64+q.i*75;q.y=160;}}
 function attack(key,kind){clear();const q=R.ships.find(q=>q.key===key);rg4Attack(q,R,G,kind);return q;}
 function tick(q,seconds){for(let t=0;t<seconds;t+=.05)rg4AttackTick(q,R,G,.05);}
 const v=attack('voss','turbo');tick(v,v.rg4.act.warm+.05);const x=v.x,y=v.y;tick(v,.1);
 out['Voss releases a fast physical dash after its warning']=Math.hypot(v.x-x,v.y-y)>70&&G.events.some(e=>e.event==='specialRelease'&&e.kind==='turbo');
 tick(v,1.0);out['Voss schedules warned offscreen horizontal ram passes']=v.rg4.act?.kind==='turbo'&&v.rg4.act.cycle>=1&&['row','fire'].includes(v.rg4.act.phase);
 const rook=attack('rook','slug');tick(rook,rook.rg4.act.warm+1.1);
 out['Rook fires .50-cal slug bursts from alternating attached guns']=eBullets.filter(p=>p._ra4Slug).length>=8&&eBullets.filter(p=>p._ra4Slug).every(p=>Math.hypot(p.vx,p.vy)>4.8);
 const kaia=attack('kaia','rockets');kaia.rg4.act.locked=true;tick(kaia,kaia.rg4.act.warm+1.8);const rockets=eBullets.filter(p=>p._ra4Rocket);
 out['Kaia launches four super-size rockets one barrel at a time']=rockets.length===4&&rockets.map(p=>p.side).join(',')==='1,-1,1,-1'&&rockets.every(p=>p.h===32&&p._shootable&&p.hp===2);
 out['Kaia lock mode retains the selected live target']=rockets.every(p=>p.lock?.ref&&p.lock.ref===kaia.rg4.act.target.ref);
 clear();rg4Attack(kaia,R,G,'rockets');kaia.rg4.act.locked=false;tick(kaia,kaia.rg4.act.warm+.2);
 out['Kaia also fires free rockets without target steering']=eBullets.some(p=>p._ra4Rocket&&!p.lock);
 clear();const nyx=R.ships[1],oldLock=retinaBossTargets(b).find(p=>p._retinaId==='nyx-hull');rg4Attack(nyx,R,G,'cloak');tick(nyx,nyx.rg4.act.warm+2.0);
 out['Nyx fires ambush rounds while her tracing stays cloaked']=nyx.frCloak>0&&eBullets.some(p=>p._ra4Ghost);
 out['Nyx cloak hides her attached HP readout and missile target']=!ra4BarPose(nyx).visible&&!retinaBossTargets(b).some(p=>p._retinaId==='nyx-hull');
 out['Nyx cloak also invalidates an already acquired missile lock']=!!oldLock&&!retinaTargetValid(oldLock);
 tick(nyx,4.5);out['Nyx eventually reveals and can be targeted again']=nyx.frCloak===0&&retinaBossTargets(b).some(p=>p._retinaId==='nyx-hull');
 const jace=attack('jace','helix');tick(jace,jace.rg4.act.warm+.1);const ball=G.ord.find(p=>p.kind==='helix');
 out['Jace releases a destructible authored helix ball']=!!ball&&retinaBossTargets(b).some(t=>t.kind==='support');
 ball.t=ball.life-.01;rg4OrdnanceTick(b,G,.05);const nova=eBullets.filter(p=>p._ra4MiniBall);
 out['Jace nova creates exactly eight spherical energy directions']=nova.length===8&&new Set(nova.map(p=>Math.round(Math.atan2(p.vy,p.vx)*100))).size===8;
 out['Jace nova emits no helix laser strands']=nova.every(p=>p.kind==='s6orb')&&G.novaFx.length===1;
 clear();const q=R.ships[0],before=ra4BarPose(q);q.x+=37;q.y+=29;const after=ra4BarPose(q);
 out['health bars follow their own pilot coordinates']=after.x-before.x===37&&after.y-before.y===29;
 q.dead=true;out['defeated pilots have no health bar']=!ra4BarPose(q).visible;
 clear();rg4Attack(R.ships[3],R,G);let box=G.rebelBoxes[0];
 out['natural specials begin with a real personal ability box']=box?.key==='kaia'&&!R.ships[3].rg4.act&&retinaBossTargets(b).some(p=>p.kind==='support');
 pBullets.push({kind:'mg',x:box.x,y:box.y,w:6,h:10,dmg:9});ra4SupplyTick(G,.01);
 out['shooting an enemy ability box denies its pickup and delays its special']=box.dead&&!R.ships[3].rg4.supply&&R.ships[3].rg4.cd===4;
 clear();rg4Attack(R.ships[4],R,G);box=G.rebelBoxes[0];R.ships[4].x=box.x;R.ships[4].y=box.y;ra4SupplyTick(G,.01);rg4Attack(R.ships[4],R,G);
 out['collecting a personal box starts the correct warned special']=box.dead&&R.ships[4].rg4.act?.kind==='helix'&&R.ships[4].rg4.act.phase==='charge';
 for(const [dead,expected]of [[[],'kaia'],[['kaia'],'nyx'],[['kaia','nyx'],'jace'],[['kaia','nyx','jace'],'rook'],[['kaia','nyx','jace','rook'],'voss']]){
  clear();for(const p of R.ships)if(dead.includes(p.key)){p.dead=true;p.hp=0;}G.rescueDone=false;rg4RescueStart(b,G);
  const lines=G.scene.lines;out['living '+expected+' owns the counter-scan']=G.scanner===expected&&lines.find(l=>l.event==='scan').who===expected&&lines.find(l=>l.event==='reveal').who===expected;
  out[expected+' scene never assigns a defeated Rebel dialogue']=lines.every(l=>!dead.includes(l.who));
  if(expected==='jace')out['Jace uses the new recruit boast']=lines.some(l=>l.text.includes('NEW RECRUIT'));
  if(expected==='rook')out['living Voss corrects Rook about the big boss']=lines.some(l=>l.who==='voss'&&l.text.includes('ACTUAL BIG BOSS'));
  if(expected==='voss')out['Voss instructs the radar hack himself']=lines.some(l=>l.who==='voss'&&l.text.includes('RADAR HACK'));
 }
 clear();R.ships.forEach(q=>{q.dead=true;q.hp=0;});G.rescueDone=false;out['no dead pilot is resurrected to scan']=!rg4RescueStart(b,G)&&!G.scene;
 out['all generated boxes and hex icons have registered source cells']=REBEL_KEYS.every(k=>RA4_ART.cells['box_'+k]&&RA4_ART.cells['icon_'+k]);
 out['red-orange authored swaps preserve alpha and luminance']=Object.values(RA4_ART.palette).length===12&&Object.values(RA4_ART.palette).every(p=>p.alpha_identical&&p.max_luminance_error<.004);
 beginStage(7);return out;
})())`,ctxv));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
