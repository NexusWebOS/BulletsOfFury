/* Mechanical extraction/normalization of authored imagegen art. No sprite drawing.
   Run with NODE_PATH pointing to the bundled node_modules or with sharp installed. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const sharp = require('sharp');
const root = path.resolve(__dirname, '../ground');
const source = path.join(root, 'source');
const frames = {};
const sequences = {};
const pilots = {
 axel:{family:'assault',body:'athletic',color:'#348dff',lum:1},
 cole:{family:'assault',body:'regular',color:'#7ad63a',lum:1.35},
 maverick:{family:'assault',body:'regular',color:'#3ad6c8',lum:1.2},
 decker:{family:'assault',body:'regular',color:'#ffe030',lum:1.75},
 yuri:{family:'assault',body:'regular',color:'#ff3030',lum:1.25},
 freezer:{family:'assault',body:'regular',color:'#a060ff',lum:1.25},
 juggernaut:{family:'siege',body:'heavy',color:'#e0662a',lum:1.15},
 lizzie:{family:'panzer',body:'female',color:'#b88a1c',lum:1.3},
 falva:{family:'panzer',body:'female',color:'#ff2a8f',lum:1.25},
 hotwire:{family:'panzer',body:'female',color:'#31d6e8',lum:1.2,secondary:'#d67b35',paletteStatus:'candidate sampled visual identity'},
 phoenix:{family:'siege',body:'athletic',color:'#b84320',lum:1.08,secondary:'#e8a13b',paletteStatus:'candidate ember armor over charcoal steel'}
};
function hash(b){return crypto.createHash('sha256').update(b).digest('hex').slice(0,12)}
async function bounds(buf, threshold=32){
 const {data,info}=await sharp(buf).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 let l=info.width,t=info.height,r=-1,b=-1;
 for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*4+3]>threshold){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)}
 if(r<l)throw Error('Empty authored frame');
 return [l,t,r+1,b+1];
}
async function frame(key,file,rect,opts={}){
 const input=path.join(source,file);
 const original=await sharp(input).extract({left:rect[0],top:rect[1],width:rect[2],height:rect[3]}).png().toBuffer();
 const bb=await bounds(original,opts.threshold||32);
 const margin=opts.margin===undefined?2:opts.margin;
 const trim=[Math.max(0,bb[0]-margin),Math.max(0,bb[1]-margin),Math.min(rect[2],bb[2]+margin),Math.min(rect[3],bb[3]+margin)];
 const width=trim[2]-trim[0],height=trim[3]-trim[1];
 const size=opts.size||[128,128],anchor=opts.anchor||[size[0]/2,size[1]/2];
 const scale=opts.scale||Math.min((size[0]-16)/width,(size[1]-16)/height);
 const w=Math.max(1,Math.round(width*scale)),h=Math.max(1,Math.round(height*scale));
 const pivot=opts.pivot?[opts.pivot[0]-rect[0]-trim[0],opts.pivot[1]-rect[1]-trim[1]]:[width/2,height/2];
 const x=Math.round(anchor[0]-pivot[0]*scale),y=Math.round(anchor[1]-pivot[1]*scale);
 if(x<0||y<0||x+w>size[0]||y+h>size[1])throw Error(`${key}: exceeds canvas ${[x,y,w,h,size]}`);
 const sprite=await sharp(original).extract({left:trim[0],top:trim[1],width,height}).resize(w,h,{kernel:'nearest'}).png().toBuffer();
 const output=await sharp({create:{width:size[0],height:size[1],channels:4,background:'#00000000'}}).composite([{input:sprite,left:x,top:y}]).png().toBuffer();
 const folder=opts.folder||'frames'; fs.mkdirSync(path.join(root,folder),{recursive:true});
 const rel=`${folder}/${key}.png`; fs.writeFileSync(path.join(root,rel),output);
 frames[key]={path:rel,size,pivot:anchor,source:file,sourceRect:[rect[0]+trim[0],rect[1]+trim[1],width,height],sourcePivot:opts.pivot||null,scale,alphaBounds:await bounds(output),sha12:hash(output),...(opts.note?{note:opts.note}:{})};
 return output;
}
const tankDefs={
 siege:{file:'tank_siege_modules.png',scale:104/454,rects:[[35,0,455,458],[500,90,480,369],[995,90,278,369],[1310,85,464,379],[0,480,548,400],[640,480,177,390],[1030,480,178,390],[1410,500,290,350]],pivots:[[265,261],[739,257],[1132,355],[1538,258],[274,665],[730,670],[1119,670],[1553,731]],muzzles:[[-8,-56],[8,-56]]},
 assault:{file:'tank_assault_modules.png',scale:92/380,rects:[[70,0,410,491],[527,120,413,374],[996,70,279,423],[1320,120,412,374],[40,501,495,369],[656,501,172,365],[1037,501,171,365],[1408,510,280,345]],pivots:[[272,288],[733,287],[1135,386],[1524,287],[284,668],[741,681],[1121,681],[1546,727]],muzzles:[[0,-72]]},
 panzer:{file:'tank_panzer_modules_v1.png',scale:72/270,rects:[[85,0,305,545],[470,95,305,449],[835,75,234,470],[1145,95,307,449],[77,568,319,439],[540,573,163,416],[862,573,164,416],[1178,564,242,419]],pivots:[[237,310],[621,310],[951,438],[1297,310],[236,772],[622,785],[945,785],[1300,856]],muzzles:[[0,-87]]}
};
async function tanks(){
 const names=['concept','hull','turret','damaged_hull','wreck','left_track','right_track','recoil_candidate'];
 for(const [id,d] of Object.entries(tankDefs)){
  for(let i=0;i<names.length;i++)await frame(`${id}_${names[i]}`,d.file,d.rects[i],{size:[192,192],anchor:[96,120],scale:d.scale,pivot:d.pivots[i],folder:'tanks',note:i===7?'Generated recoil candidate changes barrel length; use base turret translation for runtime recoil until repaired.':undefined});
  const base=path.join(root,frames[`${id}_hull`].path),turret=path.join(root,frames[`${id}_turret`].path);
  const buffer=await sharp(base).composite([{input:turret,left:0,top:0}]).png().toBuffer();
  const rel=`tanks/${id}_assembled.png`;fs.writeFileSync(path.join(root,rel),buffer);frames[`${id}_assembled`]={path:rel,size:[192,192],pivot:[96,120],alphaBounds:await bounds(buffer),sha12:hash(buffer),derivedFrom:[`${id}_hull`,`${id}_turret`]};
 }
}
async function grid(file,cols,rows,keys,options={}){
 const m=await sharp(path.join(source,file)).metadata();
 for(let i=0;i<keys.length;i++){
  const col=i%cols,row=Math.floor(i/cols),x=Math.round(col*m.width/cols),y=Math.round(row*m.height/rows);
  const right=Math.round((col+1)*m.width/cols),bottom=Math.round((row+1)*m.height/rows);
  await frame(keys[i],file,[x,y,right-x,bottom-y],typeof options==='function'?options(i,[x,y,right-x,bottom-y]):options);
 }
}
async function effects(){
 const keys=['shell','ap_shell','rocket','plasma_shell','rifle_tracer','twin_tracer'];
 for(const name of ['muzzle','impact','destruction'])for(let i=0;i<6;i++)keys.push(`${name}_${i}`);
 const fxY=[0,270,512,735,1024],fxCenters=[152,401,650,900,1142,1394];
 for(let i=0;i<keys.length;i++){
  const row=Math.floor(i/6),col=i%6,xc=row===3?[0,266,511,790,1040,1288,1536]:[0,278,524,779,1027,1275,1536];
  const rect=[xc[col],fxY[row],xc[col+1]-xc[col],fxY[row+1]-fxY[row]];
  const opts={folder:'fx',size:row===0?[32,64]:[128,128],...(row===1?{scale:.43,pivot:[fxCenters[col],479],anchor:[64,112]}:row>1?{scale:.44,pivot:[fxCenters[col],row===2?628:866]}:{})};
  await frame(keys[i],'tank_fx_sheet.png',rect,opts);
 }
 for(const name of ['muzzle','impact','destruction'])sequences[name]={frames:Array.from({length:6},(_,i)=>`${name}_${i}`),fps:name==='muzzle'?24:12,loop:false};
 const supplies=['weapon_crate_closed','weapon_crate_open','weapon_crate_broken','ammo_crate_closed','ammo_crate_open','ammo_crate_broken','ammo_rifle','ammo_shells','ammo_rockets','ammo_energy','ammo_tank','ammo_grenade','weapon_rifle','weapon_spread','weapon_launcher','power_speed','power_sensor','power_magnetic'];
 const supplyY=[0,332,601,887];
 for(let i=0;i<supplies.length;i++){
  const row=Math.floor(i/6),col=i%6,xc=row===2?[0,294,598,916,1195,1474,1774]:[0,298,591,889,1190,1476,1774];
  await frame(supplies[i],'ground_supplies.png',[xc[col],supplyY[row],xc[col+1]-xc[col],supplyY[row+1]-supplyY[row]],{folder:'pickups',size:[64,64]});
 }
 const god=[];for(const name of ['god_charge','god_burst'])for(let i=0;i<6;i++)god.push(`${name}_${i}`);
 god.push('god_bolt','god_split_bolt','god_hit','god_ring','god_wave','god_core');
 await grid('god_burst_sheet.png',6,3,god,(i,r)=>({folder:'fx',size:[128,128],scale:.36,pivot:[r[0]+r[2]*.5,r[1]+r[3]*(i<6?.57:i<12?.55:.49)]}));
 for(const name of ['god_charge','god_burst'])sequences[name]={frames:Array.from({length:6},(_,i)=>`${name}_${i}`),fps:12,loop:false};
}
function runs(values,min=4){let a=[];for(let i=0;i<values.length;i++)if(values[i]){if(!a.length||i>a.at(-1)[1]+1)a.push([i,i]);else a.at(-1)[1]=i}return a.filter(r=>r[1]-r[0]+1>=min)}
function components(data,w,h,top,bottom){
 const seen=new Uint8Array(w*h),queue=new Int32Array(w*h),out=[];
 for(let y=top;y<=bottom;y++)for(let x=0;x<w;x++){
  const start=y*w+x;if(seen[start]||data[start*4+3]<=64)continue;
  let head=0,tail=1,l=x,r=x,t=y,b=y;queue[0]=start;seen[start]=1;
  while(head<tail){const p=queue[head++],px=p%w,py=Math.floor(p/w);l=Math.min(l,px);r=Math.max(r,px);t=Math.min(t,py);b=Math.max(b,py);
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const xx=px+dx,yy=py+dy;if(xx<0||xx>=w||yy<top||yy>bottom)continue;const q=yy*w+xx;if(!seen[q]&&data[q*4+3]>64){seen[q]=1;queue[tail++]=q}}
  }
  if(tail>100)out.push({rect:[l,t,r+1,b+1],area:tail});
 }
 return out.sort((a,b)=>b.area-a.area).slice(0,4).sort((a,b)=>a.rect[0]-b.rect[0]).map(c=>c.rect);
}
async function infantry(){
 for(const [body,scale] of Object.entries({heavy:.19,athletic:.17,female:.16,regular:.16})){
  const file=`infantry_${body}_actions.png`;
  const {data,info}=await sharp(path.join(source,file)).raw().toBuffer({resolveWithObject:true});
  const yr=runs(Array.from({length:info.height},(_,y)=>{for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*4+3]>64)return true;return false}));
  if(yr.length!==7)throw Error(`${file}: expected 7 content rows, saw ${yr.length}`);
  for(let row=0;row<7;row++){
   const [top,bottom]=yr[row];
   const xr=runs(Array.from({length:info.width},(_,x)=>{for(let y=top;y<=bottom;y++)if(data[(y*info.width+x)*4+3]>64)return true;return false}),20);
   let rects=xr.length===4?xr.map(([l,r])=>[l,top,r+1,bottom+1]):components(data,info.width,info.height,top,bottom);
   if(rects.length!==4)throw Error(`${file} row ${row}: cannot separate four poses`);
   const group=['aim','run_north','run_east','run_south','roll_east','prone','death'][row];
   const keys=[];
   for(let col=0;col<4;col++){
    const rr=rects[col],l=Math.max(0,rr[0]-2),t=Math.max(0,rr[1]-2),r=Math.min(info.width,rr[2]+2),b=Math.min(info.height,rr[3]+2);
    const key=`${body}_${group}_${col}`;keys.push(key);
    const px=row===2?.38:row===0&&col===1?.37:row===0&&col===3?.63:.5;
    const py=row===1?.56:row===3?.51:.5;
    await frame(key,file,[l,t,r-l,b-t],{folder:'infantry',size:[96,96],anchor:[48,48],scale,pivot:[l+(r-l)*px,t+(b-t)*py],note:'Four-frame candidate; native-scale playback and collision sockets need integration review.'});
   }
   sequences[`${body}_${group}`]={frames:keys,fps:row===4?12:9,loop:row>=1&&row<=3,...(row===0||row===5?{directions:['north','east','south','west'],playback:'directional_poses_not_animation'}:{})};
  }
  sequences[`${body}_run_west`]={...sequences[`${body}_run_east`],mirrorX:true};
  sequences[`${body}_roll_west`]={...sequences[`${body}_roll_east`],mirrorX:true};
 }
}
async function main(){
 await tanks();await effects();await infantry();
 const manifest={schemaVersion:1,status:'review_candidates_not_runtime_registered',generationTool:'built-in image_gen',paletteMaskRule:'Only cobalt-blue painted panels; preserve neutral steel, black outlines and warm weapon/effect colors.',pilots,tanks:Object.fromEntries(Object.entries(tankDefs).map(([id,d])=>[id,{pivot:[96,120],canvas:[192,192],facing:'north',muzzles:d.muzzles.map(p=>[96+p[0],120+p[1]]),trackModuleStatus:'isolated source modules, not animated',recoilRecommendation:'Translate base turret backward 2-3 native pixels; generated recoil source requires geometry repair.'}])),frames,sequences};
 manifest.sources=Object.fromEntries(fs.readdirSync(source).filter(f=>f.endsWith('.png')).map(f=>[f,{sha12:hash(fs.readFileSync(path.join(source,f)))}]));
 fs.writeFileSync(path.join(root,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 fs.writeFileSync(path.join(root,'manifest.js'),'window.OVERDRIVE_GROUND = '+JSON.stringify(manifest)+';\n');
 console.log(JSON.stringify({frames:Object.keys(frames).length,sequences:Object.keys(sequences).length,pilots:Object.keys(pilots).length}));
}
main().catch(e=>{console.error(e);process.exitCode=1});
