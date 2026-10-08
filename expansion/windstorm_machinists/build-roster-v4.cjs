const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const ROOT=__dirname,blank=(w,h,bg='#00000000')=>sharp({create:{width:w,height:h,channels:4,background:bg}});
module.exports=async function(M,Q){
 Q.rosterV4=[];
 const source='source/machinists_identity_v4.png',file=path.join(ROOT,source),md=await sharp(file).metadata();const sx=md.width/1536,sy=md.height/1024;
 const baseFrame=path.join(ROOT,'reference/ui_match_v2/portrait_frame_template.png');
 const configs=[{who:'wren',color:'#f1f1ef',secondary:'#17191b',led:[235,235,235],look:'black/white armor; gray android face and black crewcut'}, {who:'rolf',color:'#286ddd',secondary:'#142b54',led:[34,113,235],look:'blue hair and blue outfit'}, {who:'chaz',color:'#cb302d',secondary:'#491b23',led:[230,35,30],look:'blond hair, red forehead bandana and red outfit'}];
 const selected=[];
 async function save(id,buffer,size,meta){const rel='identity/'+id+'_v4.png';await sharp(buffer).png().toFile(path.join(ROOT,rel));M.frames[id]={file:rel,size,pivot:[size[0]/2,size[1]/2],source,styleRevision:4,...meta};selected.push(id);}
 for(const [i,c]of configs.entries()){
  const rect={left:Math.round((i*512+46)*sx),top:0,width:Math.round(420*sx),height:Math.round(420*sy)};
  const face=await sharp(file).extract(rect).resize(202,212,{kernel:'nearest'}).png().toBuffer();
  const {data,info}=await sharp(baseFrame).ensureAlpha().raw().toBuffer({resolveWithObject:true});const alpha=Buffer.from(data.filter((_,i)=>i%4===3));
  for(let p=0;p<data.length;p+=4){const r=data[p],g=data[p+1],b=data[p+2],max=Math.max(r,g,b),min=Math.min(r,g,b);if(data[p+3]&&b>r+10&&b>g*1.05&&max-min>max*.55){const brightness=b/255;for(let k=0;k<3;k++)data[p+k]=Math.round(c.led[k]*brightness);}}
  const border=await sharp(data,{raw:info}).png().toBuffer(),portrait=await blank(256,256,'#070b13').composite([{input:face,left:27,top:27},{input:border,left:0,top:0}]).png().toBuffer();
  const meta={sourceRect:Object.values(rect),frameTemplate:'reference/ui_match_v2/portrait_frame_template.png',innerPlacement:[27,27,202,212],appearance:c.look};
  await save(c.who+'_portrait',portrait,[256,256],meta);await save(c.who+'_avatar',portrait,[256,256],{...meta,usage:'pilot-select avatar'});
  const frontRect={left:Math.round(i*512*sx),top:Math.round(424*sy),width:Math.round(512*sx),height:md.height-Math.round(424*sy)};
  const front=await sharp(file).extract(frontRect).resize(504,504,{fit:'contain',kernel:'nearest',background:'#00000000'}).png().toBuffer();
  await save(c.who+'_front',await blank(512,512).composite([{input:front,left:4,top:4}]).png().toBuffer(),[512,512],{sourceRect:Object.values(frontRect),appearance:c.look,usage:'full-body identity pose'});
  Object.assign(M.pilots[c.who],{color:c.color,secondary:c.secondary});
  Q.rosterV4??=[];Q.rosterV4.push({pilot:c.who,appearance:c.look,frameAlphaUnchanged:alpha.equals(Buffer.from(data.filter((_,i)=>i%4===3)))});
 }
 M.sources.machinists_identity_v4={file:source,size:[md.width,md.height],type:'selected_identity_revision'};
 M.rosterV4={selected,source,prompts:'roster-v4-generation.json',status:'selected_user_palette_revision'};
 for(const id of selected){const f=M.frames[id],png=fs.readFileSync(path.join(ROOT,f.file));f.sha256=crypto.createHash('sha256').update(png).digest('hex').slice(0,16);const {data,info}=await sharp(png).ensureAlpha().raw().toBuffer({resolveWithObject:true});let alpha=0,border=0;for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){const a=data[(y*info.width+x)*4+3];if(a)alpha++;if(a&&(x===0||y===0||x===info.width-1||y===info.height-1))border++;}if(!alpha)throw Error('Empty '+id);Q.frameChecks=Q.frameChecks.filter(c=>c.id!==id);Q.frameChecks.push({id,nonzeroAlphaPixels:alpha,borderAlphaPixels:border,size:[info.width,info.height]});}
 Q.totals.sourceMasters=fs.readdirSync(path.join(ROOT,'source')).length;
 const layers=[];for(const [i,c]of configs.entries()){layers.push({input:await sharp(path.join(ROOT,M.frames[c.who+'_portrait'].file)).resize(256,256,{kernel:'nearest'}).png().toBuffer(),left:30+i*310,top:55});layers.push({input:await sharp(path.join(ROOT,M.frames[c.who+'_front'].file)).resize(300,300,{kernel:'nearest'}).png().toBuffer(),left:8+i*310,top:320});}
 const labels=Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640"><g font-family="sans-serif" font-size="23" fill="#d8e5ed" text-anchor="middle"><text x="158" y="32">WREN</text><text x="468" y="32">ROLF</text><text x="778" y="32">CHAZ</text></g></svg>');layers.push({input:labels,left:0,top:0});await blank(960,640,'#101920').composite(layers).png().toFile(path.join(ROOT,'previews/machinists_v4.png'));
};
if(require.main===module)(async()=>{const M=JSON.parse(fs.readFileSync(path.join(ROOT,'manifest.json'))),Q=JSON.parse(fs.readFileSync(path.join(ROOT,'verification.json')));await module.exports(M,Q);fs.writeFileSync(path.join(ROOT,'manifest.json'),JSON.stringify(M,null,2)+'\n');fs.writeFileSync(path.join(ROOT,'manifest.js'),'window.EXPANSION='+JSON.stringify(M)+';\n');fs.writeFileSync(path.join(ROOT,'verification.json'),JSON.stringify(Q,null,2)+'\n');console.log(JSON.stringify({selected:M.rosterV4.selected,checks:Q.rosterV4,totals:Q.totals}));})();
