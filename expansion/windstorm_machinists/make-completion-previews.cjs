const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,M=JSON.parse(fs.readFileSync(path.join(root,'manifest.json')));
const canvas=(w,h)=>sharp({create:{width:w,height:h,channels:4,background:'#10212b'}});
const label=(text,w,h=34)=>({input:Buffer.from(`<svg width="${w}" height="${h}"><text x="12" y="24" fill="#dbeee9" font-family="Arial" font-size="18">${text}</text></svg>`)});
(async()=>{
 const rows=[['phoenix_grenade_throw','PHOENIX / GRENADE'],['phoenix_roll_to_prone','PHOENIX / ROLL INTO PRONE'],['phoenix_death','PHOENIX / DOWNED'],['phoenix_revive','PHOENIX / REVIVE'],['hotwire_grenade_throw','HOTWIRE / GRENADE'],['hotwire_roll_to_stand','HOTWIRE / ROLL TO STAND'],['hotwire_death','HOTWIRE / DOWNED'],['hotwire_revive','HOTWIRE / REVIVE']];
 const w=864,rowH=148,layers=[];
 for(let row=0;row<rows.length;row++){const [id,title]=rows[row];layers.push({...label(title,w),left:0,top:row*rowH});for(let i=0;i<M.sequences[id].frames.length;i++){let f=M.frames[M.sequences[id].frames[i]];layers.push({input:await sharp(path.join(root,f.file)).resize(144,144,{kernel:'nearest'}).png().toBuffer(),left:i*144,top:row*rowH+15});}}
 await canvas(w,rows.length*rowH+12).composite(layers).png().toFile(path.join(root,'previews/ally_completion.png'));
 const tankLayers=[];for(let row=0;row<3;row++){let who=['wren','rolf','chaz'][row],tank=M.tanks[who];tankLayers.push({...label(who.toUpperCase()+' / '+tank.name.toUpperCase()+' / SIX TRACK PHASES',1536),left:0,top:row*290});for(let i=0;i<6;i++){const list=tank.layerOrder.map(p=>({input:path.join(root,M.frames[p.endsWith('_track')?M.sequences[tank.trackSequences[p.startsWith('left')?'left':'right']].frames[i]:tank.parts[p].frame].file),left:0,top:0}));const im=await sharp({create:{width:256,height:256,channels:4,background:'#00000000'}}).composite(list).png().toBuffer();tankLayers.push({input:im,left:i*256,top:row*290+34});}}await canvas(1536,870).composite(tankLayers).png().toFile(path.join(root,'previews/tank_tracks_completion.png'));
 console.log('Completion contact sheets written.');
})();
