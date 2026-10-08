const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../coastline');
const out = path.join(root, 'assets');
const records = [];
async function record(name, role, source) {
  const file = path.join(out, name), data = fs.readFileSync(file);
  const m = await sharp(data).metadata();
  const { data: raw, info } = await sharp(data).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let transparent=0, partial=0;
  for(let i=3;i<raw.length;i+=4){if(raw[i]===0)transparent++;else if(raw[i]<255)partial++;}
  records.push({file:'assets/'+name, role, source, width:m.width, height:m.height, transparentPixels:transparent, partialAlphaPixels:partial, sha256:crypto.createHash('sha256').update(data).digest('hex')});
}
async function save(pipeline,name,role,source){await pipeline.png().toFile(path.join(out,name));await record(name,role,source);}
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  await save(sharp(path.join(root,'source/miami_coast_region.png')).resize(768,1024,{kernel:'nearest'}),'miami_coast_region.png','Transparent campaign region','source/miami_coast_region.png');
  for(const key of ['level_01_compound','level_02_gate_highway']){
    const src='source/'+key+'.png';
    const compact=await sharp(path.join(root,src)).trim({threshold:8}).png().toBuffer();
    for(const size of [380,128])await save(sharp(compact).resize(size-24,size-24,{fit:'contain',background:'#00000000',kernel:'nearest'}).extend({top:12,bottom:12,left:12,right:12,background:'#00000000'}),key+(size===128?'_128':'')+'.png',size===128?'Thumbnail':'Campaign level icon; 190 logical pixels at 2x',src);
  }
  for(const key of ['level_01_ocean_approach','level_02_coastal_highway'])await save(sharp(path.join(root,'source/'+key+'.png')).resize(480,720,{kernel:'nearest'}),key+'.png','Finite transition background candidate; not seamless','source/'+key+'.png');
  const W=2560,H=1280, layers=[];
  const ocean=await sharp(path.join(root,'reference/existing_ocean.png')).resize(256,256,{kernel:'nearest'}).toBuffer();
  for(let y=0;y<H;y+=256)for(let x=0;x<W;x+=256)layers.push({input:ocean,left:x,top:y});
  layers.push({input:await sharp(path.join(out,'miami_coast_region.png')).resize(780,1040,{kernel:'nearest'}).toBuffer(),left:70,top:45});
  const pos={1:[120,117],2:[286,80],3:[444,117],4:[517,255],5:[497,390],6:[322,401],7:[137,389],8:[91,252],9:[575,75],hub:[304,245]};
  const order=Object.keys(pos).sort((a,b)=>pos[a][1]-pos[b][1]);
  for(const key of order){const p=pos[key],d=Math.round((key==='hub'?240:key==='9'?130:190)*.96),x=Math.round(1580+(p[0]*1.45+10)*.96-d/2),y=Math.round(230+(p[1]*1.45+10)*.96-d/2);layers.push({input:await sharp(path.join(root,'reference/isl_'+key+'.png')).resize(d,d,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
  await save(sharp({create:{width:W,height:H,channels:4,background:'#041a3b'}}).composite(layers),'connecting_map_clean.png','Campaign layout composite; labels and routes separate','Existing campaign island references + new coast region');
  const route='<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1280" viewBox="0 0 2560 1280"><path d="M1715 860 C1550 1070 1110 1100 900 965 S740 888 617 850" fill="none" stroke="#041020" stroke-width="14"/><path d="M1715 860 C1550 1070 1110 1100 900 965 S740 888 617 850" fill="none" stroke="#71e3ef" stroke-width="5" stroke-dasharray="14 18"/><path d="M642 836 L617 850 L645 863" fill="none" stroke="#9af6ff" stroke-width="6"/><g fill="#051626" stroke="#f8d273" stroke-width="4"><circle cx="604" cy="850" r="24"/><circle cx="505" cy="665" r="24"/></g><g fill="#fff0b3" font-family="monospace" font-size="26" font-weight="bold" text-anchor="middle"><text x="604" y="859">1</text><text x="505" y="674">2</text></g></svg>';
  fs.writeFileSync(path.join(out,'connecting_route.svg'),route);
  await save(sharp(path.join(out,'connecting_map_clean.png')).composite([{input:Buffer.from(route)}]),'connecting_map_route.png','Review composite with proposed route and two mission markers','connecting_map_clean.png + connecting_route.svg');
  const manifest={version:1,project:'Bullets of Fury — Overdrive',region:'Miami coast',status:'Generated art candidates, not integrated gameplay',mapLayout:{canvas:[W,H],coast:{rect:[70,45,780,1040]},originalCampaign:{origin:[1580,230],scale:.96,positionSource:'Current game SSEL_POS / CM2_K 1.45 / offset 10'},nodes:{od01:[604,850],od02:[505,665]},direction:'Existing islands on right → long water crossing left → compound → north gate and highway'},assets:records};
  fs.writeFileSync(path.join(root,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
  fs.writeFileSync(path.join(root,'manifest.js'),'window.COAST_MANIFEST='+JSON.stringify(manifest)+';\nwindow.COAST_STORY='+fs.readFileSync(path.join(root,'story.json'),'utf8')+';\n');
  const issues=[];
  for(const a of records){if(a.role.includes('Transparent')||a.role.includes('icon')||a.role==='Thumbnail'){if(!a.transparentPixels)issues.push(a.file+': expected transparent background');}if(a.width<1||a.height<1)issues.push(a.file+': invalid dimensions');}
  for(const mission of JSON.parse(fs.readFileSync(path.join(root,'story.json'),'utf8')).missions)for(const key of ['icon','plate'])if(!fs.existsSync(path.join(root,mission[key])))issues.push('Missing '+mission[key]);
  fs.writeFileSync(path.join(root,'verification.json'),JSON.stringify({checked:records.length,issues},null,2)+'\n');
  console.log(JSON.stringify({assets:records.length,issues}));
})().catch(e=>{console.error(e);process.exitCode=1;});
