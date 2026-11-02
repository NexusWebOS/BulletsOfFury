"""Bake actual native Stage4-9 projectile renders into directional asset cells.
Only authored drawImage pixels are exported, retaining source colors/alpha.
Native launch flags, collision, interception and attack books remain in game.
"""
from pathlib import Path
from io import BytesIO
import ast,sys,json,base64,hashlib,http.server,re,math
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
Q=R/'_shots/enemy_flight_1031';S=R/'_BUILD_SOURCE/enemy_flight_1031/ordnance_sources';S.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/shared/combat/enemy_flight_1031/ordnance';O.mkdir(exist_ok=True)
def pack(source,sig,record):
 im=Image.open(source).convert('RGBA');kind=json.loads(sig)[2];flags=json.loads(sig)[3];text=(R/'assets/game.js').read_text(encoding='utf-8');book=text.split('const CFX_STAGE_PROJECTILE=',1)[1].split('});',1)[0]
 spin=set(re.findall(r"(\w+)\s*:\s*\[[^\n]*['\"]spin['\"]",book));rotate=kind in spin and not flags.get('_bf22Theme')
 if rotate:
  cell=record['cell'];out=Image.new('RGBA',(cell,cell*32))
  for f in range(32):
   src=f%4;tile=im.crop((0,src*cell,cell,(src+1)*cell));angle=f*360/32-src/18*2.25*180/math.pi;out.alpha_composite(tile.rotate(-angle,Image.Resampling.NEAREST),(0,f*cell))
  im=out;record.update(dirs=1,frames=32,fps=32/(math.tau/2.25),fullSpin=True)
 target=R/record['path'];im.save(target,format='WEBP',lossless=True,method=4);record['sha256']=hashlib.sha256(target.read_bytes()).hexdigest();return record
if'--repack-only'in sys.argv:
 meta=json.loads((O/'manifest.json').read_text())
 for sig,B in meta['glyphs'].items():pack(R/B['source'],sig,B)
 (O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');(R/'assets/enemy_ordnance_art_1031.js').write_text('"use strict";\nconst R46_ORDNANCE='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Repacked',len(meta['glyphs']),'native source banks');sys.exit(0)
if'--install-escort'in sys.argv or'--install-rain'in sys.argv:
 which='rain'if'--install-rain'in sys.argv else'escort';meta=json.loads((Q/(which+'-ordnance-candidate.json')).read_text());(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');(R/'assets/enemy_ordnance_art_1031.js').write_text('"use strict";\nconst R46_ORDNANCE='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Installed native',which,'glyph supplement');sys.exit(0)
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));glyphs={};errors=[]
escort='--prepare-escort'in sys.argv
rain='--prepare-rain'in sys.argv
if escort or rain:glyphs=json.loads((O/'manifest.json').read_text())['glyphs']
script=ast.parse((R/'_BUILD_SOURCE/audit_enemy_flight_1031.py').read_text(encoding='utf-8'));LAB=next(ast.literal_eval(n.value)for n in script.body if isinstance(n,ast.Assign)and any(getattr(t,'id','')=='LAB'for t in n.targets))
CAP=r'''()=>{
 // Export original native art, never the already migrated glyph bank itself.
 ovSonicProjectileDraw=R46.base.early;air17DrawProjectile=R46.base.airProjectile;
 window.GLY31={protos:new Map(),sources:new Map(),base:ctx.drawImage};
 GLY31.collect=function(){for(const b of eBullets){if(!b||b.dead||b._r46Pending||!b._r46Owner)continue;const sig=r46GlyphSignature(b);if(!GLY31.protos.has(sig))GLY31.protos.set(sig,{...b});}};
 GLY31.render=function(sig,cell,dirs,frames){const proto=GLY31.protos.get(sig),sheet=document.createElement('canvas');sheet.width=cell*dirs;sheet.height=cell*frames;const sg=sheet.getContext('2d');let calls=0;const sources=new Set();
  const oldE=eBullets,oldP=pBullets,draw=ctx.drawImage,oldTime=efxClock;
  try{for(let f=0;f<frames;f++)for(let d=0;d<dirs;d++){
   const tile=document.createElement('canvas');tile.width=tile.height=cell;const g=tile.getContext('2d'),angle=Math.PI/2+d*TAU/dirs,t=f/18,sp=Math.hypot(proto.vx,proto.vy)||3;
   const q={...proto,x:cell/2,y:cell/2,vx:Math.cos(angle)*sp,vy:Math.sin(angle)*sp,ang:angle,angle,t,_visualAge:t,_bf22Born:efxClock-t,_ph:0,dead:false};
   eBullets=[q];pBullets=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';
   ctx.drawImage=function(im,...a){const m=ctx.getTransform();g.setTransform(m);g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=ctx.imageSmoothingEnabled;g.drawImage(im,...a);calls++;const key=FA31.keys.get(im)?.key||R46.tags.get(im)?.key;if(key)sources.add(key);};
   try{drawBullets();}finally{ctx.drawImage=draw;ctx.restore();}
   sg.drawImage(tile,d*cell,f*cell);
  }}finally{eBullets=oldE;pBullets=oldP;efxClock=oldTime;ctx.drawImage=draw;}
  const a=sg.getImageData(0,0,sheet.width,sheet.height).data;let ink=0,edge=0;for(let y=0;y<sheet.height;y++)for(let x=0;x<sheet.width;x++){if(a[(y*sheet.width+x)*4+3]>25){ink++;if(x%cell<2||x%cell>cell-3||y%cell<2||y%cell>cell-3)edge++;}}
  return{data:sheet.toDataURL().split(',')[1],calls,ink,edge,sources:[...sources],kind:proto.kind,w:proto.w,h:proto.h};};
}'''
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  for stage in([7]if escort else[6]if rain else range(4,10)):
   p=browser.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate(LAB);p.evaluate(CAP)
   p.evaluate('(s)=>EA11.setup(s,"furious")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
   specs=json.loads((Q/'before'/f'stage{stage}-specs.json').read_text())
   if escort:
    specs=[s for s in specs if s['type']=='ll18brood'];p.evaluate('()=>{const release=ll18Release;ll18Release=function(){const old=FA31.allowSpawn;FA31.allowSpawn=true;try{return release.apply(this,arguments);}finally{FA31.allowSpawn=old;}};}')
   if rain:specs=[next(s for s in specs if s['type']=='s1jetbomber_b')]
   for spec in specs:
    p.evaluate('s=>{FA31.allowSpawn=true;return EA11.case(s)}',spec)
    if rain:p.evaluate('()=>{for(const e of enemies)e.dead=true;enemies=[];window.E=fb2FlightSpawn({direction:"south",role:"red",x:worldWidth()/2,_cp22Mode:"rain"});}')
    p.evaluate('FA31.reset()')
    for i in range(105):
     result=p.evaluate('()=>{FA31.step(8);GLY31.collect();return !!E&&!E.dead}');p.wait_for_timeout(1)
     if not result:break
   signatures=p.evaluate('[...GLY31.protos.keys()]');print('STAGE',stage,len(signatures),'native glyphs',flush=True)
   for sig in signatures:
    if sig in glyphs:continue
    cell=128;dirs=32;frames=4;r=p.evaluate('([sig,c,d,f])=>GLY31.render(sig,c,d,f)',[sig,cell,dirs,frames])
    if not r['ink']:p.wait_for_timeout(180);r=p.evaluate('([sig,c,d,f])=>GLY31.render(sig,c,d,f)',[sig,cell,dirs,frames])
    if r['edge']>8:
     cell=256;r=p.evaluate('([sig,c,d,f])=>GLY31.render(sig,c,d,f)',[sig,cell,dirs,frames])
    if r['ink']<20 or r['calls']==0:errors.append('No authored pixels for '+sig);continue
    name='p'+hashlib.sha256(sig.encode()).hexdigest()[:16];source=S/(name+'.png');source.write_bytes(base64.b64decode(r.pop('data')));im=Image.open(source).convert('RGBA');target=O/(name+'.webp');im.save(target,format='WEBP',lossless=True,method=4)
    glyphs[sig]=pack(source,sig,{'key':'r46_'+name,'path':target.relative_to(R).as_posix(),'cell':cell,'dirs':dirs,'frames':frames,'fps':18,'source':source.relative_to(R).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),**r})
   p.close()
  browser.close()
finally:stop()
meta={'owner':'_BUILD_SOURCE/build_enemy_ordnance_1031.py','method':__doc__,'glyphs':glyphs,'errors':errors}
if escort or rain:
 which='rain'if rain else'escort';(Q/(which+'-ordnance-candidate.json')).write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');print('Prepared native',which,'supplement;',len(glyphs),'total glyphs; errors',errors);assert not errors;sys.exit(0)
(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
(R/'assets/enemy_ordnance_art_1031.js').write_text('"use strict";\nconst R46_ORDNANCE='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Exported',len(glyphs),'native authored projectile banks; errors',errors[:5],flush=True)
assert not errors,errors[:5]
