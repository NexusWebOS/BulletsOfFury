module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['rotation5_0930.js','realm_art_0930.js','realm_0930.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== 383. Three-form alien finale, destructible code barriers and portable headings ===');
 const results=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 for(const dk of ['normal','hard','furious','insanity']){
  diffKey=dk;DIFF=DIFFS[dk];beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;
  spawnBoss('vileexistence');bossActive=true;const b=boss,S=b._r30;
  out[dk+' starts with the possessed gray host, no active health bar']=S.form===0&&S.mode==='takeover'&&!bossHealthVisible(b);
  for(let i=0;i<360;i++)r30Tick(b,1/60);
  out[dk+' finishes takeover before accepting combat']=r30Live(b)&&bossHealthVisible(b);
  r30Form(b,2);S.mode='fight';b.enter=false;
  out[dk+' colossus always has four complete life layers']=b.maxhp===S.base*4;
  S.shieldMax=S.shield=20;const hp=b.hp;b._lastPart=b.parts[0];modularHit(7);
  out[dk+' shield absorbs direct and splash hits before hull']=S.shield===13&&b.hp===hp;
  modularHit(20);out[dk+' binary shield can be shot down']=S.shield===0&&b.hp===hp;
  enemies=[];r30Wall(b,'binarywall');const wall=enemies[0];hitEnemy(wall,wall.maxhp);
  out[dk+' wall leaves a safe lane and a second destructible gap']=enemies.length===4&&wall.dead&&enemies.filter(e=>!e.dead).length===3;
  r30Form(b,0);S.mode='fight';b.enter=false;const score=run.score;b._lastPart=b.parts[0];modularHit(b.maxhp+1);
  out[dk+' false death stops the bar and does not grant rewards']=S.mode==='fall'&&!bossHealthVisible(b)&&run.score===score&&!bossDefeated;
  for(let i=0;i<600;i++)r30Tick(b,1/60);
  out[dk+' fragments reform the second combat form']=S.form===1&&S.mode==='fight'&&S.history.some(x=>x.event==='fragmentsRise')&&run.score===score;
 }
 out['5 degree headings wrap clockwise across zero']=rot5Index(0)===0&&rot5Index(Math.PI/36)===1&&rot5Index(-Math.PI/36)===71&&rot5Index(Math.PI*2)===0;
 run.stage=1;run.spaceMode=false;gravityMode=null;player.roll=null;player.somer=null;
 out['every normal pilot uses the neutral hull for ordinary steering']=PILOTS.every(p=>_shipFrameKey(p.key)==='ship_'+p.key);
 return out;
 })())`,ctxv));
 for(const [name,pass]of Object.entries(results))ok(pass,name);
};
