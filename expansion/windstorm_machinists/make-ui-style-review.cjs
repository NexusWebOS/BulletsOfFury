const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,w=1020,h=1030,layers=[];
const txt=(s,x,y,size=20,color='#e0efed')=>layers.push({input:Buffer.from(`<svg width="${w}" height="44"><text x="${x}" y="30" fill="${color}" font-family="Arial" font-size="${size}">${s}</text></svg>`),left:0,top:y});
async function fit(file,x,y,width,height){const im=await sharp(path.join(root,file)).resize(width,height,{fit:'contain',kernel:'nearest',background:'#00000000'}).png().toBuffer();layers.push({input:im,left:x,top:y});}
(async()=>{
 txt('NIEL / WINDSTORM — MATCHED TO THE CURRENT GAME',24,8,24);
 ['CURRENT GAME','PREVIOUS NIEL','MATCHED NIEL'].forEach((s,i)=>txt(s,40+i*340,54,19,i===2?'#84dbc2':'#93a9b5'));
 for(const [i,f]of ['reference/ui_match_v2/cole_portrait.png','identity/niel_portrait.png','identity/niel_portrait_v2.png'].entries())await fit(f,42+i*340,108,256,256);
 txt('256 × 256 portrait frame',24,370,18);
 for(const [i,f]of ['reference/ui_match_v2/maverick_icon.png','ship/windstorm_icon.png','ui/spicon_niel_v2.png'].entries())await fit(f,58+i*340,421,224,224);
 txt('112 × 112 hex special badge — shown at 2×',24,635,18);
 for(const [i,f]of ['reference/ui_match_v2/maverick_box.png','ship/windstorm_box.png','ui/special_niel_box_v2.png'].entries())await fit(f,30+i*340,686,280,310);
 txt('Vented special pickup housing · Niel export 360 × 400',24,995,18);
 await sharp({create:{width:w,height:h,channels:4,background:'#101c24'}}).composite(layers).png().toFile(path.join(root,'previews/ui_style_match_v2.png'));
 console.log('Style comparison saved.');
})();
