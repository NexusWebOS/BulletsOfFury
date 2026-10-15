module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'..');
 console.log('=== October 10 part two: beam safety, encounter integrity and earned modes ===');
 for(const [file,symbol] of [['part2_art_1010.js','P2_ART'],['part2_fire_renderer_1011.js','p2RenderFireColumn'],['part2_combat_1010.js','P2'],['part2_encounters_1010.js','P2E'],['part2_modes_1010.js','P2M'],['part2_motion_1011.js','P2MC']])
  if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',file),'utf8'),c,{filename:file});
 const banks=JSON.parse(vm.runInContext('JSON.stringify(P2_ART)',c));
 for(const [name,bank]of Object.entries(banks)){
  ok(bank.length===({shield:9,fire_root:16,fire_tip:16,stealth:8,stealth_roll:64,stealth_somer:64}[name]||32),name+': every requested authored frame ships');
  ok(bank.every(a=>{const b=fs.readFileSync(path.join(root,a.path));return a.w%2===0&&a.h%2===0&&a.w===b.readUInt32BE(16)&&a.h===b.readUInt32BE(20)&&String(a.pivot)===String(bank[0].pivot)&&crypto.createHash('sha256').update(b).digest('hex')===a.sha256;}),name+': pixels, even dimensions and fixed pivots match registration');
  if(name!=='stealth')ok(new Set(bank.map(a=>a.sha256)).size===bank.length,name+': all poses contain distinct pixels');
  else ok(bank.every(a=>a.source_sha256&&a.scale===(a.role==='orange'?.66:1)),name+': idle fighter plates retain their exact authored source and proportional scale');
 }
 const audit=JSON.parse(fs.readFileSync(path.join(root,'_ART_SOURCES/part2_1011/audit.json'),'utf8'));
 for(const name of ['fire','fire_root'])ok(audit[name].padded_edges&&audit[name].unique_hashes===banks[name].length,name+': repaired visible pixels clear all four canvas borders');
 const motionAudit=JSON.parse(fs.readFileSync(path.join(root,'_ART_SOURCES/part2_motion_1011/audit.json'),'utf8'));
 for(const [name,q]of Object.entries(motionAudit))ok(q.padded_edges&&q.common_scale&&q.unique_hashes===banks[name].length,name+': common proportional scale and transparent margins protect the entire new bank');
 ok(banks.atom.length===32&&new Set(banks.atom.map(a=>a.source_index)).size===32&&banks.atom.every(a=>a.source==='part2_motion_1011/atom_raw.png'),'Atomic animation uses32 new progressive authored poses, with no mixed source sizes');
 ok(banks.stealth.filter(a=>a.role!=='orange').every(a=>/skycarrier\/ace_(top|damaged)\.png$/.test(a.source)),'Blue/red/green idle variants preserve the exact original opening fighter');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},sv={draw:ctx.drawImage,curve:ctx.bezierCurveTo,wing:s6Wing,boss,story,rdy:XART.rdy,get:XART.get,owned:achievementState.owned,receipt:P2M.receipt,clear:bonusModesUnlocked};
  try{
   let draws=0;ctx.drawImage=()=>{draws++;};if(typeof ctx.bezierCurveTo!=='function')ctx.bezierCurveTo=()=>{};XART.rdy=()=>true;XART.get=()=>({width:256,height:448});
   for(const bad of [0,1e-14,-1,NaN,Infinity]){
    const before=draws;av3Beam(ctx,100,100,0,650,bad,'ice',0);ap10FusionBeam(ctx,100,100,0,650,bad,0);
    o['Beam width '+String(bad)+' paints no tiles and returns']=before===draws;
   }
   let before=draws;av3Beam(ctx,100,100,0,650,.51,'ice',0);o['A barely visible ice column has a bounded tile budget']=draws>before&&draws-before<=129;
   before=draws;av3Beam(ctx,100,100,0,650,.51,'fire',0);o['A barely visible fire column has a bounded tile budget']=draws>before&&draws-before<=129;
   before=draws;ap10FusionBeam(ctx,100,100,0,650,.51,0);o['A barely visible fusion column has a bounded tile budget']=draws>before&&draws-before<=128;
   ctx.drawImage=sv.draw;XART.rdy=sv.rdy;XART.get=sv.get;
   for(const kind of ['mg','s6tracer','heavy-slug','lightningmg','pellet'])o[kind+': spread fire cannot erase an ordinary pellet']=!enemyOrdnanceCanIntercept({kind,mg:kind==='mg',_shootable:true,hp:2})&&enemyOrdnanceElement({kind,mg:kind==='mg',_inf:'fire'})===null;
   o['Missiles remain interceptable']=enemyOrdnanceCanIntercept({kind:'emissile',_shootable:true,hp:2});
   run.mode='arcade';run.ngplus=false;run.forge={};run.forgeForms={};achievementState.owned={forge_fire_5_C:true,forge_kinetic_1_C:true};ensureForgeForms();
   o['Ordinary arcade runs do not silently acquire profile recipes']=Object.keys(run.forgeForms).length===0;
   run.ngplus=true;ensureForgeForms();o['Explicit New Game Plus imports the owned recipes']=!!run.forgeForms[5]?.fire&&!!run.forgeForms[1]?.kinetic;
   P2M.receipt=null;bonusModesUnlocked=true;p2HubSync();
   o['A legacy flag alone cannot open Boss Rush or Time Attack']=modeList().filter(m=>['bossrush','timeattack'].includes(m.mode)).every(m=>!modeItemOpen(m));
   o['New Game Plus has no standalone mode card']=!modeList().some(m=>m.mode==='ngplus');
   o['New Game Plus is absent from an uncompleted Campaign hub']=!CAMPHUB_ITEMS.some(m=>m.act==='ngplus');
   o['An incomplete route cannot validate completion']=!p2CampaignReceipt({version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,7]});
   o['A password route cannot validate completion']=!p2CampaignReceipt({version:2,mode:'arcade',stages:[1,2,3,4,5,6,7,8]});
   P2M.receipt={version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,8]};p2HubSync();
   o['Completed campaign puts New Game Plus immediately above New Game']=CAMPHUB_ITEMS[0].act==='ngplus'&&CAMPHUB_ITEMS[1].act==='new';
   o['Completion opens the two implemented encounter/time routes']=modeList().filter(m=>['bossrush','timeattack'].includes(m.mode)).every(modeItemOpen);
   p2ModeChoose('arcade');o['Arcade asks for New Game or New Game Plus before difficulty']=P2M.choice==='arcade';P2M.choice=null;
   p2ModeChoose('bossrush');o['Boss Rush chooses difficulty through the existing input route']=P2M.pending==='bossrush'&&state===GS.DIFF;
   p2ModeChoose('coop');o['Co-op first chooses local or online']=P2M.choice==='coop'&&!coopOn;
   P2M.choice=null;P2M.pending=null;P2M.active=null;
   run.ngplus=false;run.mode='arcade';run.pilot='lizzie';run.stage=2;run.spaceMode=false;run.weapon=0;run.wlevel=3;special={pilot:'lizzie',t:4,dur:15};
   atomBooms=[{x:100,y:100,t:.1,dur:1.9}];pBullets=[];pShoot();o['Atomic impact blocks a simultaneous ordinary gun volley']=pBullets.length===0;
   atomBooms=[];pShoot();o['The ordinary gun resumes after the atomic impact']=pBullets.some(q=>q.kind==='mg');special=null;
   const orb={kind:'orb',x:220,y:250,vx:1,vy:-4,w:44,h:44,lv:3,_el:'kinetic',shardN:7};fb10Steer(orb,.016);player.x+=140;fb10Steer(orb,.016);
   o['A launched orb keeps its own velocity when the player strafes']=orb.vx===1;
   const prior=P2.orbBursts;P2.orbBursts=[];const prev={stage:run.stage,space:run.spaceMode,held:run._spaceShadowHeld};
   run.stage=5;run.spaceMode=true;run._spaceShadowHeld=true;const P=forgePreviewNew(5,'fire',3);let scoped=false;
   forgePreviewSwap(P,260,300,()=>{scoped=run.stage===1&&!run.spaceMode&&!run._spaceShadowHeld;P2.orbBursts.push({x:100,y:100,at:0,life:1});});
   o['A post-space Forge preview scopes the aircraft and held charge, then restores the live run']=scoped&&run.stage===5&&run.spaceMode&&run._spaceShadowHeld;
   o['Preview impact reels cannot leak into the live world']=P._p2Bursts.length===1&&P2.orbBursts.length===0;
   P2.orbBursts=prior;run.stage=prev.stage;run.spaceMode=prev.space;run._spaceShadowHeld=prev.held;
   const frost={_ship:'frostcruiser',_mr27:{parts:[{id:'gunL',dead:true},{id:'gunR',dead:true}]}};
   o['A disarmed Frost Cruiser still has core balls, a beam and a committed charge']=String(er26Book(frost))==='p2-core-balls,p2-core-laser,p2-core-charge';
   o['All three Stage 4 attack families preserve an authored emitter owner']=er26Book({_ship:'stormsovereign'}).includes('p2-battery')&&er26Book({_ship:'stormsovereign'}).includes('p2-rockets')&&er26Book({_ship:'stormsovereign'}).includes('ap10-stormburst');
   o['Personal dialogue and lock colors match their pilots']=RETINA_TINTS.lizzie==='#ffd438'&&RETINA_TINTS.kaia==='#25d9bd'&&dialogueNameColor('JACE')==='#ff4838'&&dialogueNameColor('ROOK')==='#ff9b30';
   boss={_rebels:{}};story=null;s6Wing={route:'right'};o['Rebel pursuit cannot play the obsolete storm-platform scene']=!storyPlay(6,'boss')&&story===null&&arcStageCard(6,'boss_warning')[0]==='REBEL FURY SQUADRON';
   boss={_whv:{}};s6Wing={route:'left'};storyPlay(6,'boss');o['Harrier pursuit owns its weather dialogue and actual cannon objectives']=story.key==='P2.S06.HARRIER'&&story.lines.some(q=>q[0]==='YURI')&&/HARRIER/.test(arcStageCard(6,'boss_warning')[0]);
   return o;
  }finally{s6Wing=sv.wing;boss=sv.boss;story=sv.story;ctx.drawImage=sv.draw;ctx.bezierCurveTo=sv.curve;XART.rdy=sv.rdy;XART.get=sv.get;achievementState.owned=sv.owned;P2M.receipt=sv.receipt;bonusModesUnlocked=sv.clear;P2M.active=P2M.pending=P2M.choice=null;p2HubSync();}
 })())`,c));
 for(const [name,passed]of Object.entries(out))ok(passed,name);
};
