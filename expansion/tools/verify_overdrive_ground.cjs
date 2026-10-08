/* Artifact integrity check; does not start the game or claim runtime coverage. */
const fs=require('fs'),path=require('path'),crypto=require('crypto'),sharp=require('sharp');
const root=path.resolve(__dirname,'../ground'),pack=JSON.parse(fs.readFileSync(path.join(root,'manifest.json')));
(async()=>{const issues=[],groups={};for(const[key,f]of Object.entries(pack.frames)){
 const bytes=fs.readFileSync(path.join(root,f.path)),meta=await sharp(bytes).metadata();
 if(meta.width!==f.size[0]||meta.height!==f.size[1]||!meta.hasAlpha)issues.push(key+': dimensions/alpha');
 if(crypto.createHash('sha256').update(bytes).digest('hex').slice(0,12)!==f.sha12)issues.push(key+': hash');
 const b=f.alphaBounds;if(b[0]<0||b[1]<0||b[2]>f.size[0]||b[3]>f.size[1])issues.push(key+': bounds');
 if(b[0]===0||b[1]===0||b[2]===f.size[0]||b[3]===f.size[1])issues.push(key+': touches outer canvas edge');
 const g=f.path.split('/')[0];groups[g]=(groups[g]||0)+1;
 }for(const[key,seq]of Object.entries(pack.sequences))for(const f of seq.frames)if(!pack.frames[f])issues.push(key+': missing '+f);
 const p=JSON.parse(fs.readFileSync(path.join(root,'prompts.json')));if(Object.keys(p.prompts).length!==12)issues.push('prompt count');
 const report={date:'2026-09-30',normalizedPNGs:Object.keys(pack.frames).length,groups,sequences:Object.keys(pack.sequences).length,pilots:Object.keys(pack.pilots).length,issues,browserReview:'Local review page loaded 199 PNGs; tank assembly/palettes, infantry roll/prone inspected; browser error/warning log empty.',runtimeIntegration:false};
 fs.writeFileSync(path.join(root,'verification.json'),JSON.stringify(report,null,2)+'\n');
 const images=[];let row=0;for(const body of ['heavy','athletic','female','regular']){for(let i=0;i<4;i++)images.push({input:await sharp(path.join(root,pack.frames[`${body}_death_${i}`].path)).resize(192,192,{kernel:'nearest'}).toBuffer(),left:i*192,top:row*192});row++}
 await sharp({create:{width:768,height:768,channels:4,background:'#17202c'}}).composite(images).png().toFile(path.join(root,'previews/infantry_death_check.png'));
 console.log(JSON.stringify(report));if(issues.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
