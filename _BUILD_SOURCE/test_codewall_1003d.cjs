module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['codewall_art_1003d.js','codewall_1003d.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== Authored chrome binary walls, red shield and reconstruction ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;
 run.mode='campaign';beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];groundTargetingReset();boss=null;bossActive=false;spawnBoss('vileexistence');bossActive=true;
 const b=boss,S=b._r30;player.x=worldWidth()/2;player.y=VH-100;player.invuln=1e9;
 S.mode='fight';b.enter=false;S.seq=1;r30Attack(b);S.wallAge1003=.4;
 out['reactor charge grows a finite blue barrier']=S.codeWall1003d==='blue'&&S.shield===Math.ceil(S.base*.055);
 const q=r30ShieldBounds(b);
 out['blue barrier covers the form and has finite geometry']=q.w>b.w&&q.h>b.h&&cwdContains(q,q.x,q.y)&&!cwdContains(q,q.x+q.w,q.y);
 out['growth only intercepts the rendered bottom section']=!cwdContains(q,q.x,q.y-q.h*.30,.2)&&cwdContains(q,q.x,q.y+q.h*.4,.2);
 out['opposite rows maintain opposite horizontal velocities']=cwdOffset(1.1,0,500)>cwdOffset(1,0,500)&&cwdOffset(1.1,1,500)<cwdOffset(1,1,500);
 const hp=b.hp,clock=S.clock,shield=S.shield;b._lastPart=r30At(b,q.x,q.y);modularHit(7);
 out['wall hit never changes animation clock or boss health']=S.clock===clock&&S.shield===shield-7&&b.hp===hp&&CWD.effects.some(f=>f.kind==='impact');
 const size=CWD.effects.length;modularHit(NaN);modularHit(-10);
 out['invalid damage cannot create feedback or corrupt shield']=CWD.effects.length===size&&Number.isFinite(S.shield);
 b._lastPart={id:'codeWall1003d'};modularHit(9999);
 out['break emits 24 moving chips once']=CWD.effects.filter(f=>f.kind==='chip').length===24&&S.history.filter(f=>f.event==='codeWallBreak1003d').length===1;
 const chips=CWD.effects.filter(f=>f.kind==='chip'),x=chips[0].x;cwdEffectsTick(.05);
 out['code fragments move with finite ballistic positions']=chips[0].x!==x&&chips.every(f=>Number.isFinite(f.x+f.y+f.rot));cwdEffectsTick(3);
 out['code effects have bounded finite lifetimes']=CWD.effects.length===0;
 r30Form(b,5);S.mode='fight';b.enter=false;r30Attack(b);S.wallAge1003=.4;
 const red=r30ShieldBounds(b),plate=fmcRig(b).find(v=>v.p.id==='shield');
 out['knight projection is attached to physical shield pivot']=red.color==='red'&&red.x===plate.x&&red.y===plate.y&&red.rot===plate.rot;
 const core=r30Parts(b).find(v=>v.p.id==='core'),before=b.hp,sp=S.shield;b._lastPart=r30At(b,core.x,core.y);modularHit(4);
 out['exposed core bypasses red shield without draining it']=b.hp===before-4&&S.shield===sp;
 out['red shield and exposed body are independently lockable']=retinaBossTargets(b).length>1;
 S.wallAge1003=.15;const target=cwdShieldTargetState(b);
 out['growing rotated shield Retina point stays inside visible code']=cwdContains(r30ShieldBounds(b),target.x,target.y,cwdGrowth(b));
 S.wallAge1003=.4;b._lastPart={id:'codeWall1003d'};modularHit(9999);
 out['red energy break preserves physical module']=fmcAlive(b,'shield')&&CWD.effects.some(f=>f.kind==='chip'&&f.color==='red');
 b._lastPart=b.parts.find(p=>p.id==='shieldArm');modularHit(b._lastPart.hp+1);s81003KnightEnter(b,'guard');
 out['missing shield arm cannot project detached energy']=!fmcAlive(b,'shield')&&S.shield===0;
 r30Form(b,0);S.mode='fight';b.enter=false;S.cd=99;
 const oldLock=retinaBossTargets(b).find(t=>t._retinaId.endsWith('-core'));S.seq=1;r30Attack(b);S.wallAge1003=.4;
 const oldHp=b.hp,oldShield=S.shield;oldLock._retinaHit(9);
 out['pre-acquired Retina lock is intercepted by newly raised wall']=b.hp===oldHp&&S.shield===oldShield-9;
 for(let form=0;form<7;form++){
  r30Clear(b);r30Form(b,form);S.mode='fight';b.enter=false;b._lastPart=b.parts[0];modularHit(b.hp+1);
  for(let i=0;i<170;i++)r30Tick(b,1/60);
  out['reconstruction preserves modular transition '+(form+1)]=S.form===form+1&&r30Live(b)&&b.parts.every(p=>p.hp>0&&!p.destroyed);
 }
 beginStage(1);out['stage reset clears code debris']=CWD.effects.length===0;
 return out;})())`,ctxv));
 for(const [name,pass] of Object.entries(result))ok(pass,name);
};
