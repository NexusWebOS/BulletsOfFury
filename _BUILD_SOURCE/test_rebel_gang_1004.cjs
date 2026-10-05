module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/rebel_gang_1004.js'),'utf8'),ctxv,{filename:'rebel_gang_1004.js'});
 console.log('=== Five Rebel specials, Gang Mode and Decker rescue ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.pilot='yuri';run.mode='campaign';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];
 spawnBoss('rebelsquad');const b=boss,R=b._rebels;rf28Init(b,R);R.frIntro={done:true};b.enter=false;b._noHit=false;b._be=null;
 for(const q of R.ships){q.mode='fight';q.warp=0;q.y=125;q.x=camLeftX()+60+q.i*70;}
 const G=rg4Init(b),step=(s)=>{for(let t=0;t<s;t+=.05)rebelSquadTick(b,.05);};
 out['all five rebels own their requested weapons']=R.ships.map(q=>q.rg4.role).join(',')==='fusion,ghost,heavy,roller,stealth';
 for(const q of R.ships){for(const other of R.ships){other.rg4.act=null;other.rg4.cd=99;}G.releaseAt=G.age+99;
  rg4Attack(q,R,G);G.releaseAt=G.age+99;const A=q.rg4.act;
  step(A.warm+.1);
  out[q.key+' releases its own special after a tell']=G.events.some(e=>e.event==='specialRelease'&&e.pilot===q.key&&e.kind===q.rg4.role);
  if(q.key==='voss')out['Fusion has a live beam only after its charge']=G.beams.length===1;
  if(q.key==='kaia'){out['upgraded roller starts as Falva ordnance']=G.ord.some(o=>o.kind==='roller'&&o.r===23);step(1.0);out['roller splits into separate dodgeable satellites']=G.ord.filter(o=>o.kind==='roller').length>=3;}
  if(['nyx','jace'].includes(q.key))out[q.key+' reveals before firing']=q.frCloak===0;
  G.beams=[];G.ord=[];eBullets=[];
 }
 for(const q of R.ships){q.rg4.act=null;q.hp=q.max;q.dead=false;}
 R.ships[0].hp=R.ships[0].max*.5;R.ships[1].hp=R.ships[1].max*.5;
 out['two wounded pilots cannot start Gang Mode']=!rg4Threshold(b,G)&&!G.gang;
 R.ships[2].hp=R.ships[2].max*.5;out['exactly three pilots at half HP start Gang Mode']=rg4Threshold(b,G)&&G.gang;
 const hp=R.ships[0].hp;R.hit=0;rebelSquadDamage(b,99999);
 out['Gang radio is protected from damage without refilling HP']=R.ships[0].hp===hp;
 out['Gang charge does not give rebels shields']=R.ships.every(q=>q.shield===0&&q.shieldMax===0);
 step(3.2);out['Gang charge ends and the new buffs start']=!G.scene&&G.ord.some(o=>o.kind==='helper')&&R.ships[4].rg4.turbo;
 out['Gang Mode cannot retrigger']=!rg4Threshold(b,G)&&G.events.filter(e=>e.event==='gangStart').length===1;
 const owner=R.ships[0];rg4Missiles(owner,G,{a:Math.PI/2});
 out['Gang missiles can be shot down and cannot track']=eBullets.filter(q=>q._rg4&&q.kind==='emissile').every(q=>q._shootable&&q.hp===1&&!q.homing);
 const orb=G.ord.find(o=>o.kind==='helper');orb.x=player.x;orb.y=player.y-100;
 const targets=retinaBossTargets(b),target=targets.find(t=>t.kind==='support');const hull=b.hp;target._retinaHit(999);
 out['helper orb has its own destructible HP and Retina target']=orb.dead&&b.hp===hull;
 rg4RescueStart(b,G);out['destroyed helper stays destroyed through rescue']=!G.savedHelper;
 out['Decker is the leading ship of the team formation']=G.members[0].key==='decker'&&G.members.length===5;
 out['formation includes the actual player rather than a copy']=G.members.some(m=>m.ref===player);
 out['combat is locked during the scene while game stays PLAY']=h3Locked()&&state===GS.PLAY;
 const scene=G.scene;out['Kaia owns the counter-scan and both requested lines']=scene.lines.filter(l=>l.who==='kaia').length===2&&scene.lines.some(l=>l.event==='scan');
 step(45);out['timed rescue ends and returns control']=!G.scene&&G.events.some(e=>e.event==='rescueComplete')&&!h3Locked();
 out['cloaking, scan and reveal occur in order']=G.events.filter(e=>['cast','cloak','scan','reveal'].includes(e.event)).map(e=>e.event).join(',')==='cast,cloak,scan,reveal';
 out['the scene cannot run twice']=!rg4RescueStart(b,G);
 out['rebel wings remain intact after every new ability']=R.ships.every(q=>fr27RebelModules(q).every(m=>m.hp===m.max));
 beginStage(7);out['a new stage clears encounter-specific protection']=rg4State()===null&&!rg4Scene();
 return out;
})())`,ctxv));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
