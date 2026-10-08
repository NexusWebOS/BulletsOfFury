const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname;
const mkdir=p=>fs.mkdirSync(path.join(root,p),{recursive:true});
const save=(p,obj)=>fs.writeFileSync(path.join(root,p),JSON.stringify(obj,null,2)+'\n');
const actions=['wall_tap','duck_to_prone','crawl','grenade_throw','roll_to_prone','roll_to_stand','hit','stun','recovery','death','revive','powerup'];
const guns=['desert_eagle','spread_shotgun','minigun','fusion_beam','napalm_launcher','rocket_launcher'];
const propNames=['cover_crate_single','cover_crate_double','cover_crate_triple','cover_crates_l','brick_wall','brick_corner','fortress_gate_closed','fortress_gate_open','grenade','grenade_bundle','ammo_crate_closed','ammo_crate_broken','supply_box_closed','supply_box_cracked','supply_box_breaking','supply_box_empty'];
const enemyNames=['scout_north','scout_east','scout_south','scout_fire','scout_damaged','scout_wreck','heavy_robot_north','heavy_robot_east','heavy_robot_south','heavy_robot_fire','heavy_robot_damaged','heavy_robot_wreck','turret_north','turret_east','turret_fire','turret_damaged','turret_wreck','turret_base','light_tank_idle','light_tank_tread','light_tank_fire','light_tank_damaged','light_tank_wreck','light_tank_turret','heavy_tank_idle','heavy_tank_tread','heavy_tank_fire','heavy_tank_damaged','heavy_tank_wreck','heavy_tank_turret','scout_air_idle','scout_air_fire','scout_air_wreck','gunship_idle','gunship_fire','gunship_wreck'];
const fxNames=[...Array.from({length:6},(_,i)=>'muzzle_'+i),...guns.map(g=>g+'_projectile'),...Array.from({length:3},(_,i)=>'fusion_pulse_'+i),...Array.from({length:3},(_,i)=>'napalm_pool_'+i),...Array.from({length:6},(_,i)=>'impact_'+i),...Array.from({length:6},(_,i)=>'grenade_blast_'+i),...Array.from({length:6},(_,i)=>'rocket_blast_'+i)];
const stealthNames=[...['calm','suspicious','alert'].flatMap(s=>Array.from({length:4},(_,i)=>'fov_'+s+'_'+i)),'suspicion_mark','alert_mark','sound_ping','target_reticle'];
const manifest={schemaVersion:1,status:'art_review_candidates_no_gameplay',generationTool:'built-in image_gen',stage:{source:'source/stage.png',art:'stage/miami_infiltration.png',size:[512,768],travel:'bottom_to_top',route:['beach','pool_park','brick_fortress_gate'],tileable:false,collisionAuthored:false},hud:{source:'source/hud.png',overlay:'hud/onfoot_overlay.png',size:[512,768],top:'hud/top_strip.png',bottom:'hud/bottom_strip.png',sockets:{portrait:[20,28,41,48],weapon:[181,32,78,43],ammo:[286,41,39,29],grenades:[379,40,43,29],radar:[444,29,50,48],belt:[[25,687,50,51],[93,687,49,51],[162,687,49,51]],stance:[235,681,43,60],detection:[300,676,14,65],objective:[342,689,137,42]},lifeIconsBaked:3,notes:'Center remains transparent. Empty sockets receive runtime text/icons. Baked life icons require masking for variable life count.'},pilots:JSON.parse(fs.readFileSync(path.join(root,'../ground/manifest.json'),'utf8')).pilots,frames:{},sequences:{},sources:{},existingLocomotion:{root:'../ground/infantry/',bodyTypes:['regular','heavy','athletic','female'],aim:['aim_0','aim_1','aim_2','aim_3'],run:['run_north','run_east','run_south'],notes:'Existing 4-frame run and aim poses; use east mirrored for west. Stationary/run fire uses these poses plus muzzle effects. New extended actions face mostly east.'},weapons:guns,extraction:{method:'Connected alpha regions assigned to semantic grid cells, retaining source RGBA. Oversized joined components split at nearest cell center. Centered review canvases; pivots are provisional.',runtimeReady:false}};
const checks={sources:[],frames:0,missingCells:[],joinedComponents:[],notes:['Soft alpha preserved, not flattened.','Original generated sheets are authoritative; frame crops need pose-root and directional cleanup.']};
async function sheet(name,cols,rows,xs,ys,names,folder,scale,canvas){
 mkdir(folder);const source='source/'+name+'.png';const {data,info}=await sharp(path.join(root,source)).ensureAlpha().raw().toBuffer({resolveWithObject:true});const w=info.width,h=info.height;
 const nearest=(x,y)=>{let c=0,r=0;for(let i=1;i<cols;i++)if(Math.abs(xs[i]-x)<Math.abs(xs[c]-x))c=i;for(let i=1;i<rows;i++)if(Math.abs(ys[i]-y)<Math.abs(ys[r]-y))r=i;return r*cols+c;};
 const labels=new Int32Array(w*h);labels.fill(-1);const seen=new Uint8Array(w*h);
 for(let p=0;p<w*h;p++){if(seen[p]||data[p*4+3]<16)continue;const q=[p];seen[p]=1;let sx=0,sy=0,x0=w,x1=0,y0=h,y1=0;for(let j=0;j<q.length;j++){const a=q[j],x=a%w,y=Math.floor(a/w);sx+=x;sy+=y;x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);for(const b of [x>0?a-1:-1,x<w-1?a+1:-1,y>0?a-w:-1,y<h-1?a+w:-1])if(b>=0&&!seen[b]&&data[b*4+3]>=16){seen[b]=1;q.push(b);}}
 const joined=(x1-x0)>(w/cols*1.6)||(y1-y0)>(h/rows*1.6);if(joined&&q.length>500)checks.joinedComponents.push({source,name,bounds:[x0,y0,x1,y1]});const id=nearest(sx/q.length,sy/q.length);for(const a of q)labels[a]=joined?nearest(a%w,Math.floor(a/w)):id;
 }
 // Extend ownership from visible sprite edges into their own soft alpha fringes.
 const fringe=[];for(let p=0;p<w*h;p++)if(labels[p]>=0)fringe.push(p);
 for(let j=0;j<fringe.length;j++){const a=fringe[j],x=a%w,y=Math.floor(a/w);for(const b of [x>0?a-1:-1,x<w-1?a+1:-1,y>0?a-w:-1,y<h-1?a+w:-1])if(b>=0&&labels[b]<0&&data[b*4+3]){labels[b]=labels[a];fringe.push(b);}}
 const bounds=Array.from({length:cols*rows},()=>({x0:w,y0:h,x1:0,y1:0,pixels:0}));let zero=0;
 for(let p=0;p<w*h;p++){if(!data[p*4+3]){zero++;continue;}if(labels[p]<0)labels[p]=nearest(p%w,Math.floor(p/w));const b=bounds[labels[p]],x=p%w,y=Math.floor(p/w);b.x0=Math.min(b.x0,x);b.x1=Math.max(b.x1,x);b.y0=Math.min(b.y0,y);b.y1=Math.max(b.y1,y);b.pixels++;}
 checks.sources.push({file:source,width:w,height:h,transparentPixels:zero,hasRealAlpha:zero>0});manifest.sources[name]={file:source,size:[w,h],grid:[cols,rows]};
 const atlas=[];
 for(let i=0;i<names.length;i++){const b=bounds[i];if(!b.pixels){checks.missingCells.push(names[i]);continue;}const cw=b.x1-b.x0+1,ch=b.y1-b.y0+1,cut=Buffer.alloc(cw*ch*4);for(let y=b.y0;y<=b.y1;y++)for(let x=b.x0;x<=b.x1;x++){const p=y*w+x;if(labels[p]===i)data.copy(cut,((y-b.y0)*cw+x-b.x0)*4,p*4,p*4+4);}
 let nw=Math.max(1,Math.round(cw*scale)),nh=Math.max(1,Math.round(ch*scale));let factor=Math.min(1,(canvas-4)/nw,(canvas-4)/nh);nw=Math.floor(nw*factor);nh=Math.floor(nh*factor);
 const sprite=await sharp(cut,{raw:{width:cw,height:ch,channels:4}}).resize(nw,nh,{kernel:'nearest'}).png().toBuffer();const left=Math.floor((canvas-nw)/2),top=Math.floor((canvas-nh)/2);const output=await sharp({create:{width:canvas,height:canvas,channels:4,background:'#00000000'}}).composite([{input:sprite,left,top}]).png().toBuffer();const file=folder+'/'+names[i]+'.png';fs.writeFileSync(path.join(root,file),output);manifest.frames[names[i]]={file,size:[canvas,canvas],pivot:[canvas/2,canvas/2],source,sourceRect:[b.x0,b.y0,cw,ch],sourceScale:scale*factor,reviewCentered:true};checks.frames++;atlas.push({input:output,left:i%cols*canvas,top:Math.floor(i/cols)*canvas});
 }
 mkdir('atlases');await sharp({create:{width:cols*canvas,height:rows*canvas,channels:4,background:'#00000000'}}).composite(atlas).png().toFile(path.join(root,'atlases/'+name+'.png'));
}
(async()=>{
 for(const d of ['stage','hud','previews'])mkdir(d);
 await sharp(path.join(root,'source/stage.png')).resize(512,768,{kernel:'nearest'}).png().toFile(path.join(root,'stage/miami_infiltration.png'));
 for(const [name,y] of [['fortress',0],['park',448],['beach',960]])await sharp(path.join(root,'source/stage.png')).extract({left:0,top:y,width:1024,height:576}).resize(512,288,{kernel:'nearest'}).png().toFile(path.join(root,'stage/'+name+'.png'));
 await sharp(path.join(root,'source/hud.png')).resize(512,768,{kernel:'nearest'}).png().toFile(path.join(root,'hud/onfoot_overlay.png'));
 await sharp(path.join(root,'hud/onfoot_overlay.png')).extract({left:0,top:0,width:512,height:108}).png().toFile(path.join(root,'hud/top_strip.png'));
 await sharp(path.join(root,'hud/onfoot_overlay.png')).extract({left:0,top:652,width:512,height:116}).png().toFile(path.join(root,'hud/bottom_strip.png'));
 // Assemble the extracted strips over an empty canvas so the gameplay center is exactly alpha zero.
 await sharp({create:{width:512,height:768,channels:4,background:'#00000000'}}).composite([{input:path.join(root,'hud/top_strip.png'),left:0,top:0},{input:path.join(root,'hud/bottom_strip.png'),left:0,top:652}]).png().toFile(path.join(root,'hud/onfoot_overlay.png'));
 for(const body of ['regular','heavy','athletic','female']){
 const names=actions.flatMap(a=>Array.from({length:3},(_,i)=>body+'_'+a+'_'+i));await sheet(body,6,6,[130,330,535,740,930,1130],[140,365,550,750,965,1160],names,'pilots',.18,96);
 for(const a of actions)manifest.sequences[body+'_'+a]={frames:Array.from({length:3},(_,i)=>body+'_'+a+'_'+i),fps:6,loop:['crawl','stun'].includes(a),direction:'east_candidate',rootMotionAuthored:false};
 }
 await sheet('weapons',5,6,[180,460,720,1000,1290],[108,285,462,640,820,1000],guns.flatMap(g=>['pickup','box_closed','box_cracked','box_open','ammo'].map(s=>g+'_'+s)),'weapons',.4,160);
 await sheet('props',4,4,[190,540,900,1260],[210,468,720,949],propNames,'props',.5,224);
 await sheet('enemies',6,6,[110,325,530,740,950,1160],[135,330,530,720,920,1125],enemyNames,'enemies',.4,112);
 await sheet('fx',6,6,[128,384,640,896,1152,1408],[90,250,410,565,745,925],fxNames,'fx',.5,160);
 await sheet('stealth',4,4,[220,582,951,1317],[135,369,605,868],stealthNames,'stealth',.5,192);
 for(const [a,n,fps] of [['muzzle',6,16],['impact',6,14],['grenade_blast',6,12],['rocket_blast',6,12],['fusion_pulse',3,10],['napalm_pool',3,6]])manifest.sequences[a]={frames:Array.from({length:n},(_,i)=>a+'_'+i),fps,loop:['fusion_pulse','napalm_pool'].includes(a),status:'candidate_visual_sequence'};
 for(const state of ['calm','suspicious','alert'])manifest.sequences['fov_'+state]={frames:Array.from({length:4},(_,i)=>'fov_'+state+'_'+i),fps:5,loop:true,direction:'north',status:'presentation_overlay_not_detection_geometry'};
 const backdrop=path.join(root,'stage/miami_infiltration.png');const panels=Buffer.from('<svg width="512" height="768"><g fill="#10191dee"><rect x="18" y="24" width="44" height="51"/><rect x="181" y="31" width="79" height="45"/><rect x="282" y="39" width="44" height="32"/><rect x="376" y="38" width="47" height="34"/><rect x="24" y="683" width="51" height="53"/><rect x="94" y="683" width="49" height="53"/><rect x="162" y="683" width="49" height="53"/><rect x="341" y="687" width="140" height="46"/></g></svg>');
 const text=Buffer.from('<svg width="512" height="768"><g fill="#ffe09a" font-family="monospace" font-weight="bold"><text x="289" y="52" font-size="7">AMMO</text><text x="287" y="64" font-size="12">18/90</text><text x="386" y="59" font-size="17">03</text><text x="191" y="69" font-size="7">DESERT EAGLE</text><text x="351" y="703" font-size="8">BREACH THE GATE</text><text x="351" y="720" font-size="7" fill="#45d9f0">MIAMI / FORTRESS</text></g></svg>');
 const smallEnemy=await sharp(path.join(root,'enemies/scout_south.png')).resize(48,48,{kernel:'nearest'}).png().toBuffer();
 const gun=await sharp(path.join(root,'weapons/desert_eagle_pickup.png')).resize(72,72,{kernel:'nearest'}).png().toBuffer();
 const helm=await sharp(path.join(root,'pilots/regular_wall_tap_0.png')).extract({left:28,top:27,width:37,height:33}).resize(38,34,{kernel:'nearest'}).png().toBuffer();
 const composed=[{input:panels,left:0,top:0},{input:path.join(root,'hud/onfoot_overlay.png'),left:0,top:0},{input:gun,left:185,top:13},{input:helm,left:23,top:31},{input:text,left:0,top:0},{input:path.join(root,'pilots/regular_wall_tap_0.png'),left:184,top:525},{input:smallEnemy,left:210,top:366}];
 await sharp(backdrop).composite(composed).png().toFile(path.join(root,'previews/stage_hud.png'));
 save('manifest.json',manifest);fs.writeFileSync(path.join(root,'manifest.js'),'window.ONFOOT='+JSON.stringify(manifest)+';\n');save('verification.json',checks);console.log(JSON.stringify({frames:checks.frames,sequences:Object.keys(manifest.sequences).length,missing:checks.missingCells,joined:checks.joinedComponents},null,2));
})();
