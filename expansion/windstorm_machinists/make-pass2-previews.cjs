const fs=require('fs'),path=require('path'),ROOT=__dirname;
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const M=JSON.parse(fs.readFileSync(path.join(ROOT,'manifest.json')));
const label=(text,w=400,h=32,size=20)=>Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'"><text x="0" y="'+(size+2)+'" font-family="sans-serif" font-size="'+size+'" fill="#b5d5de">'+text+'</text></svg>');
async function img(id,width,height){return sharp(path.join(ROOT,M.frames[id].file)).resize(width,height,{fit:'contain',kernel:'nearest',background:'#00000000'}).png().toBuffer();}
async function save(file,w,h,layers){await sharp({create:{width:w,height:h,channels:4,background:'#101c25'}}).composite(layers).png().toFile(path.join(ROOT,'previews/'+file));}
(async()=>{
 const actors=['regular','heavy','athletic','female','phoenix','hotwire'],dirs=['north','east','south','west'];const layers=[{input:label('FOUR-DIRECTION CROUCH WALK / PRONE FIRE',1720,50,30),left:30,top:15}];
 ['Crouch N','Crouch E','Crouch S','Crouch W','Prone N','Prone E','Prone S','Prone W'].forEach((t,i)=>layers.push({input:label(t,192,40,20),left:190+i*196,top:75}));
 for(let r=0;r<actors.length;r++){layers.push({input:label(actors[r].toUpperCase(),170,40,22),left:20,top:160+r*196});for(let c=0;c<8;c++){const id=actors[r]+'_'+(c<4?'crouch_walk':'prone_fire')+'_'+dirs[c%4]+'_0';layers.push({input:await img(id,192,192),left:190+c*196,top:108+r*196});}}
 await save('pass2_directional.png',1790,1320,layers);
 const el=[{input:label('ALIEN ROBOT MOTION / SELECTED REAR-VIEW CORRECTIONS',1220,50,28),left:25,top:15}];let row=0;
 for(const kind of ['scout','heavy'])for(const action of ['patrol_north','patrol_east','patrol_south','patrol_west','fire_east','hit_death_east']){el.push({input:label(kind.toUpperCase()+' '+action.replaceAll('_',' '),330,32,19),left:20,top:110+row*122});for(let i=0;i<6;i++)el.push({input:await img('enemy_'+kind+'_'+action+'_'+i,144,144),left:355+i*150,top:55+row*122});row++;}
 await save('pass2_enemies.png',1280,1570,el);
 const ul=[{input:label('THE MACHINISTS / CURRENT GAME UI FAMILY',1000,45,27),left:28,top:14}];
 for(const [i,who]of ['wren','rolf','chaz'].entries()){const x=30+i*330;ul.push({input:label(who.toUpperCase(),300,36,25),left:x,top:65});ul.push({input:await img(who+'_portrait',256,256),left:x,top:106});ul.push({input:await img(who+'_special_icon',112,112),left:x,top:410});ul.push({input:await img(who+'_special_box',162,180),left:x+135,top:380});}
 await save('machinists_ui_v3.png',1030,590,ul);
 console.log('Created 3 pass-two contact sheets');
})();
