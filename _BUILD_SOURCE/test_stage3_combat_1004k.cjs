module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/stage3_combat_1004k.js'),'utf8'),c,{filename:'stage3_combat_1004k.js'});
 console.log('=== Recording: Stage 3 turrets, charge and hostile ordnance ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.pilot='yuri';run.mode='campaign';beginStage(3);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;
 for(const q of [{kind:'mg'},{kind:'groundup',mg:true},{kind:'shell',_shootable:true},{kind:'s3lance',_er26Art:'ice'},{kind:'shard',_er26Art:'ice'}]){
  s3kOrdnanceRules(q);out[q.kind+' stays weapon-proof']=q._weaponProof&&!q._shootable;
 }
 for(const q of [{kind:'emissile'},{kind:'s1jungleMissile'},{kind:'omegawarhead'},{kind:'magma'},{kind:'s3mortar',_er26Art:'ice'}]){
  s3kOrdnanceRules(q);out[q.kind+' can be intercepted']=!q._weaponProof&&q._shootable;
 }
 const pellet={kind:'mg',x:240,y:300,vx:0,vy:2,w:4,h:14};s3kOrdnanceRules(pellet);eBullets=[pellet];pBullets=[];
 out['gunfire stays reflectable by the original chrome defense']=!enemyDefensiveProof(pellet)&&chromeMirror(240,300,30,1)===1;
 const bombPellet={kind:'mg',x:240,y:300,vx:0,vy:2};s3kOrdnanceRules(bombPellet);eBullets=[bombPellet];enemies=[];boss=null;bossActive=false;
 detonateBomb({x:240,y:300});out['bombs retain their original gunfire clear']=!eBullets.includes(bombPellet);
 spawnBoss('cryospear');const b=boss;b.enter=false;b._be=null;b.x=worldWidth()/2;b.y=b._er26.home;b._drawY=b.y;
 const hp=b.maxhp;player.x=b.x-120;player.y=VH-110;er26Set(b,'rime-orbit1004k');
 for(let i=0;i<45;i++){mr27Tick(b,1/60);b._er26.t+=1/60;}
 const p=mr27Shape(b,'gunL'),m=shipBossMount(b,'L'),raw=S3K_BASE.shape(b,'gunL');
 out['orbit moves real hittable module geometry']=Math.hypot(p.x-raw.x,p.y-raw.y)>30&&mr27At(b,p.x,p.y)==='gunL';
 out['orbit muzzle follows that geometry']=Math.hypot(p.x-m.x,p.y-m.y)<p.h;
 er26Set(b,'recover');for(let i=0;i<120;i++)mr27Tick(b,1/60);
 out['turrets return continuously to the hull']=!mr27Part(b,'gunL')._s3kPos;
 er26Set(b,'rime-missile1004k');b._er26.t=b._er26.warm+.01;eBullets=[];er26Combat(b,.02);
 out['two live rocket banks launch a four missile volley']=eBullets.filter(q=>q.kind==='emissile').length===4;
 mr27Part(b,'rocketL').dead=true;b._er26.shot=0;er26Combat(b,.02);
 out['destroyed rocket bank stops firing']=eBullets.filter(q=>q.kind==='emissile').length===6;
 out['upgrades do not inflate boss HP']=b.maxhp===hp;
 const ball=er26Shot(b,'R',Math.PI/2,2,{});out['ordinary elemental balls are shootable']=ball._shootable&&!ball._weaponProof;
 const before=efxBursts.length;ordnanceBreak1002(ball);ordnanceBreak1002(ball);
 out['one interception produces one authored elemental impact']=efxBursts.length===before+1&&ball._fbImpact1002&&s3kResidue.length===1;
 spawnSubBoss__inner('frostcruiser');const mini=subBoss;mini.enter=false;mini._be=null;mini.x=worldWidth()/2;mini.y=mini._er26.home;mini._drawY=mini.y;
 out['miniboss book retains its attacks and adds charge']=er26Book(mini).includes('elite-ram1004k')&&er26Book(mini).includes('elite-beam1002');
 er26Set(mini,'elite-ram1004k');const y=mini.y;mini._er26.t=.5;er26Combat(mini,.02);
 out['charge warns before moving']=mini.y===y&&mini._er26.warnings.length===1;
 mini._er26.t=mini._er26.warm+.2;er26Combat(mini,.02);const dx=mini._er26.s3kDash.tx;player.x+=100;mini._er26.t+=.1;er26Combat(mini,.02);
 out['charge commits once and advances toward the pilot']=mini.y>y&&mini._er26.s3kDash.tx===dx;
 beginStage(1);setState(GS.TITLE);return out;
})())`,c));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
