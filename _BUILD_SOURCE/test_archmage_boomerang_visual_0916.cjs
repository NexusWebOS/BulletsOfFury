module.exports=function testArchmageBoomerangVisual(vm,ctxv,ok){
  console.log('=== 342. Active Archmage boomerang warning and authored reels ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={draw:combatWarningDraw,ret:hammerGroundReticleDraw,blit:archBlit,frame:hammerFrame,boss:boss,diff:diffKey};
    const calls={warn:[],ret:[],blit:[]};
    try{
      combatWarningDraw=function(owner,q){calls.warn.push({x:q.x,y:q.y,ex:q.ex,ey:q.ey,progress:q.progress,width:q.width,alertX:q.alertX,alertY:q.alertY});};
      hammerGroundReticleDraw=function(im,x,y,w,a){calls.ret.push({tint:im&&im.tint,x:x,y:y,w:w,a:a});return true;};
      archBlit=function(key,frame,x,y,h,tint,rot,alpha){calls.blit.push({key:key,frame:frame,x:x,y:y,h:h,alpha:alpha});return true;};
      hammerFrame=function(key,frame,tint){return {key:key,tint:tint==null?'green':tint,width:64,height:64};};
      diffKey='normal';boss={x:240,y:168,w:158,h:176,hp:1000,maxhp:1000,flash:0,enter:false,dead:false,_noHit:false};hammerBossInit(boss);
      boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;boss._hammer.state='spin';boss._hammer.throwX=326;boss._hammer.throwY=392;
      for(const t of [.18,.80,1.40]){boss._hammer.t=t;hammerBossDraw(boss);}
      const warning=calls.warn.length===3&&calls.warn.every(q=>q.ex===326&&q.ey===VH&&q.width===42&&q.alertX===316&&q.alertY===86)&&calls.warn[0].progress<calls.warn[1].progress&&calls.warn[1].progress<calls.warn[2].progress;
      const reticles=calls.ret.length===3&&calls.ret.map(q=>q.tint).join(',')==='green,yellow,red'&&calls.ret.every(q=>q.x===326&&q.y===392&&q.w===122);
      const reels=calls.blit.length===3&&calls.blit.every(q=>q.key==='twirl_throw_0922')&&calls.blit[0].frame<calls.blit[1].frame&&calls.blit[1].frame<calls.blit[2].frame;
      calls.blit.length=0;boss._hammer.state='throw';boss._hammer.throw={x:326,y:360,angle:2,trail:[{x:318,y:340,angle:1.8},{x:305,y:315,angle:1.5},{x:288,y:286,angle:1.2},{x:268,y:252,angle:.9},{x:244,y:216,angle:.6},{x:220,y:184,angle:.3}]};hammerBossDraw(boss);
      const echoes=calls.blit.filter(q=>q.key==='hammer_spin'),afterimages=echoes.length===4&&echoes.slice(0,-1).every(q=>q.alpha>0&&q.alpha<=.22)&&echoes[echoes.length-1].alpha===1;
      const assets=XART._src.arch_twirl_throw==='assets/game/stage5_archmage_0916/twirl_throw.png'&&XART._src.arch_hammer_spin==='assets/game/stage5_archmage_0916/hammer_spin.png';
      return JSON.stringify({warning:warning,reticles:reticles,reels:reels,afterimages:afterimages,assets:assets,name:boss.name==='CHROME HAMMER ARCHMAGE'});
    }finally{combatWarningDraw=save.draw;hammerGroundReticleDraw=save.ret;archBlit=save.blit;hammerFrame=save.frame;boss=save.boss;diffKey=save.diff;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Archmage boomerang visual: '+k);
};
