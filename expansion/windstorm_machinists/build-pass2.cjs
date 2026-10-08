const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const ROOT=__dirname;
const blank=(w,h,bg='#00000000')=>sharp({create:{width:w,height:h,channels:4,background:bg}});
function hsv(r,g,b){r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;let h=0;if(d){if(max===r)h=((g-b)/d+6)%6;else if(max===g)h=(b-r)/d+2;else h=(r-g)/d+4;h/=6;}return [h,max?d/max:0,max];}
function rgb(h,s,v){const k=n=>(n+h*6)%6,f=n=>Math.round(255*v*(1-s*Math.max(0,Math.min(k(n),4-k(n),1))));return [f(5),f(3),f(1)];}
module.exports=async({M,Q,sheet,seq,exportFrame})=>{
 const dirs=['north','east','south','west'],actors=['regular','heavy','athletic','female','phoenix','hotwire'];
 const six=id=>Array.from({length:6},(_,i)=>id+'_'+i),anchored={cellAnchored:true,targetAnchor:[48,48]};
 for(const who of actors){const actions=['crouch_walk','prone_fire'].flatMap(a=>dirs.map(d=>who+'_'+a+'_'+d));const family=['phoenix','hotwire'].includes(who)?'ally':'player_interaction';
  await sheet('stealth_'+who+'_4dir',6,8,actions.flatMap(six),family==='ally'?'allies':'players',.225,96,anchored);
  for(const a of actions){const fire=a.includes('prone_fire');seq(a,six(a),fire?10:7,true,{family,body:who,direction:a.split('_').at(-1),stance:fire?'prone':'crouch',motion:fire?'stationary':'in_place',events:fire?[{frame:1,type:'fire'},{frame:3,type:'fire'}]:[],state:'motion_candidate',rootMotionAuthored:false,anchorPolicy:'fixed source cell; body drift still requires pixel review'});}
 }
 // Remove two source phases that change facing instead of advancing the gait.
 M.sequences.phoenix_crouch_walk_east.frames=[0,1,2,3,5].map(i=>'phoenix_crouch_walk_east_'+i);
 M.sequences.phoenix_crouch_walk_south.frames=[0,1,2,4,5].map(i=>'phoenix_crouch_walk_south_'+i);
 for(const d of ['east','south'])M.sequences['phoenix_crouch_walk_'+d].reviewNote='Five selected phases; excluded source phase turns out of requested facing. Gait wrap needs cleanup.';
 await sheet('west_runs',6,6,actors.flatMap(w=>six(w+'_run_west')),'players',.20,96,anchored);
 for(const who of actors)seq(who+'_run_west',six(who+'_run_west'),9,true,{family:['phoenix','hotwire'].includes(who)?'ally':'player_interaction',body:who,direction:'west',state:'motion_candidate',rootMotionAuthored:false});
 for(const kind of ['scout','heavy']){const who='enemy_'+kind,actions=['patrol_north_draft','patrol_east','patrol_south','patrol_west','fire_east','hit_death_east'];await sheet(who+'_patrol',6,6,actions.flatMap(a=>six(who+'_'+a)),'enemies',kind==='heavy'?.235:.215,96,anchored);for(const action of actions.slice(1)){const id=who+'_'+action;seq(id,six(id),action.startsWith('patrol')?7:10,!action.includes('death'),{family:'enemy',enemy:kind,direction:action.includes('south')?'south':action.includes('west')?'west':'east',state:'motion_candidate',events:action==='fire_east'?[{frame:1,type:'fire'},{frame:3,type:'fire'}]:[],terminal:action.includes('death')?'wreck':null});}}
 await sheet('enemy_patrol_north_fix',6,2,['scout','heavy'].flatMap(k=>six('enemy_'+k+'_patrol_north')),'enemies',.13,96,anchored);
 for(const kind of ['scout','heavy'])seq('enemy_'+kind+'_patrol_north',six('enemy_'+kind+'_patrol_north'),7,true,{family:'enemy',enemy:kind,direction:'north',state:'motion_candidate',replaces:'source/'+('enemy_'+kind+'_patrol.png')+' row 1',reviewNote:'Rear-view correction; original misdirected row archived and hidden.'});
 await sheet('machinists_icons_v3',3,1,['wren','rolf','chaz'].map(w=>w+'_special_icon'),'ui',.15,112);
 await sheet('machinists_boxes_v3',3,1,['wren','rolf','chaz'].map(w=>w+'_special_box'),'ui',1,400);
 const canonical=path.join(ROOT,'reference/ui_match_v2/portrait_frame_template.png');
 for(const [who,hue] of [['wren',.01],['rolf',.99],['chaz',.08]]){
  const {data,info}=await sharp(canonical).ensureAlpha().raw().toBuffer({resolveWithObject:true});const before=Buffer.from(data.filter((_,i)=>i%4===3));
  for(let i=0;i<data.length;i+=4){const [h,s,v]=hsv(data[i],data[i+1],data[i+2]);if(data[i+3]&&h>.48&&h<.71&&s>.22&&data[i+2]>data[i]+10){const c=rgb(hue,s,v);for(let k=0;k<3;k++)data[i+k]=c[k];}}
  const frame=await sharp(data,{raw:info}).png().toBuffer();const crop={left:30,top:22,width:263,height:274};
  const face=await sharp(path.join(ROOT,'identity/'+who+'_portrait.png')).extract(crop).resize(202,212,{kernel:'nearest'}).png().toBuffer();
  const portrait=await blank(256,256,'#070b13').composite([{input:face,left:27,top:27},{input:frame,left:0,top:0}]).png().toBuffer();
  const file='identity/'+who+'_portrait_v3.png';fs.writeFileSync(path.join(ROOT,file),portrait);M.frames[who+'_portrait']={file,size:[256,256],pivot:[128,128],source:'source/machinists_identity_v2.png',derivativeSource:'identity/'+who+'_portrait.png',derivativeRect:Object.values(crop),frameTemplate:'reference/ui_match_v2/portrait_frame_template.png',innerPlacement:[27,27,202,212],styleRevision:3,frameHue:hue};
  const avatar='identity/'+who+'_avatar_v3.png';fs.writeFileSync(path.join(ROOT,avatar),portrait);M.frames[who+'_avatar']={...M.frames[who+'_portrait'],file:avatar,usage:'pilot-select avatar'};
  for(const [type,w,h,pad] of [['icon',112,112,8],['box',360,400,6]]){const id=who+'_special_'+(type==='box'?'box':'icon'),cut=path.join(ROOT,'cuts/'+id+'.png');const input=await sharp(cut).resize(w-pad*2,h-pad*2,{fit:'inside',kernel:'nearest'}).png().toBuffer(),md=await sharp(input).metadata();await blank(w,h).composite([{input,left:Math.floor((w-md.width)/2),top:Math.floor((h-md.height)/2)}]).png().toFile(path.join(ROOT,M.frames[id].file));Object.assign(M.frames[id],{size:[w,h],pivot:[w/2,h/2],styleRevision:3,usage:type==='icon'?'112x112 hex ability badge':'360x400 vented pickup box'});}
  Q.machinistsUi??=[];Q.machinistsUi.push({pilot:who,frameAlphaUnchanged:before.equals(Buffer.from(data.filter((_,i)=>i%4===3))),portrait:[256,256],icon:[112,112],box:[360,400]});
 }
 M.pass2={actors,enemyTypes:['scout','heavy'],directionalActions:['crouch_walk','prone_fire'],westRuns:true,machinistsUiRevision:3,prompts:'passes-2-generation.json',notes:'Graphics only. Fixed source cell anchors prevent bounding-box recentering on flashes. Five selected Phoenix crouch phases; others six. Source pose drift remains; not eight-direction gameplay-ready animation.'};
};
