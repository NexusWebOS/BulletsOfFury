from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,sys,json,shutil,re,hashlib
sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts')
import pixelcore as px
WORK=Path(__file__).resolve().parent;OUT=WORK.parents[1]/'outputs/chronus-death'
ROOT=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
GEN=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a')
C=WORK/'candidate';F=C/'frames';F.mkdir(parents=True,exist_ok=True)
sources={'aura':'exec-2912f995-e4d8-4710-9363-94cec38dd4fc.png','implosion':'exec-b8fcd839-b7a5-41b8-89d4-452719602fb3.png'}
banks={};samples=[]
for name,file in sources.items():
    shutil.copy2(GEN/file,OUT/f'{name}-master.png')
    im=Image.open(GEN/file).convert('RGB');w,h=im.size;bank=[]
    for i in range(16):
        x0,y0=round(i%4*w/4),round(i//4*h/4)
        # Fixed-size native crop and shared transparent padding. No downscale/upscale cycle.
        rgb=np.asarray(im.crop((x0,y0,x0+313,y0+313)))
        mask=px.key_mask(rgb,'magenta');rgb=px.despill(rgb,mask,'magenta')
        bank.append((rgb,mask));
        if mask.any():samples.append(rgb[mask])
    banks[name]=bank
pal,extra=px.build_palette([np.concatenate(samples)],32,max_extra=6)
manifest={'palette':['#%02x%02x%02x'%tuple(c) for c in pal],'banks':{},'source_hash':hashlib.sha256((ROOT/'assets/hammer_finale_1017.js').read_bytes()).hexdigest()}
for name,bank in banks.items():
    frames=[];areas=[]
    for i,(rgb,mask) in enumerate(bank):
        mapped=px.map_to_palette(rgb,pal)
        rgba=np.dstack([mapped,mask.astype(np.uint8)*255]);native=Image.new('RGBA',(320,320))
        native.paste(Image.fromarray(rgba),(4,4))
        # Implosion has a larger authored size bank, exported directly from the native master.
        if name=='implosion':native=native.resize((640,640),Image.Resampling.NEAREST)
        native.save(F/f'{name}-{i:02}.png');frames.append(native);areas.append(int(mask.sum()))
    w,h=frames[0].size
    sheet=Image.new('RGBA',(w*16,h))
    for i,im in enumerate(frames):sheet.paste(im,(i*w,0))
    sheet.save(OUT/f'{name}-sheet.png')
    manifest['banks'][name]={'frames':16,'cell':[w,h],'pivot':[w//2,h//2],'areas':areas,'duration_ms':80 if name=='aura' else 110}
    preview=[]
    for im in frames:
        p=Image.new('RGBA',im.size,(13,18,34,255));p.alpha_composite(im)
        preview.append(p.convert('RGB'))
    preview[0].save(OUT/f'{name}-effect.gif',save_all=True,append_images=preview[1:],duration=80 if name=='aura' else 110,loop=0)
    board=Image.new('RGB',(w*4,h*4),(13,18,34))
    for i,im in enumerate(frames):board.paste(im,(i%4*w,i//4*h),im)
    board.save(WORK/f'{name}-contact.png')
assert all(a==0 for a in manifest['banks']['implosion']['areas'][-2:])
assert manifest['banks']['implosion']['areas'][11]<manifest['banks']['implosion']['areas'][5]/8
(OUT/'effect-manifest.json').write_text(json.dumps(manifest,indent=2))
code=(ROOT/'assets/hammer_finale_1017.js').read_text(encoding='utf-8')
addition='''
// Chronus death: authored aura, chromium expansion and inward collapse.
const CI109={banks:{},draws:0};
for(const name of ['aura','implosion']){CI109.banks[name]=[];for(let i=0;i<16;i++){
 const im=new Image();im.src='assets/game/levels/stage_05/boss/chronus_implosion_1109/'+name+'-'+String(i).padStart(2,'0')+'.png';CI109.banks[name].push(im);}}
function ci109Ready(){return Object.values(CI109.banks).flat().every(im=>im.complete&&im.naturalWidth>0);}
function ci109Draw(name,index,x,y){const im=CI109.banks[name][Math.max(0,Math.min(15,index|0))];if(!im?.complete||!im.naturalWidth)return;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,Math.round(x-im.width/2),Math.round(y-im.height/2));ctx.restore();CI109.draws++;}
'''
code=code.replace('function hf17Warm()',addition+'\nfunction hf17Warm()',1)
code=code.replace('let ready=true;for(const bank','let ready=ci109Ready();for(const bank',1)
start=code.index('function hf17Actor(e)');end=code.index('function hf17Missile(F)',start)
old=code[start:end]
# Keep the original drain/pulse/lock/missile acting. Swap only the requested fire and terminal effect.
prefix=old[:old.index(" if(p==='burst')")]
normal=old[old.index(" }else{\n  hf17Cell('stunned'"):]
normal=normal.replace("if(p==='engulf')hf17Cell('engulf',Math.floor(F.t*16),F.anchor.x,F.anchor.y,k);","if(p==='engulf')ci109Draw('aura',Math.floor(F.t*12)%16,F.anchor.x,F.anchor.y+24);")
replacement=prefix+''' if(p==='burst'){
  const age=F.t;
  if(age<.28){hf17Cell('unlit',0,F.anchor.x,F.anchor.y,k,1,e.boss.flash);ci109Draw('aura',Math.floor(age*12)%16,F.anchor.x,F.anchor.y+24);}
  ci109Draw('implosion',Math.floor(age/0.11),F.core.x,F.core.y);
'''+normal
code=code[:start]+replacement+code[end:]
# Retire the old outward decorative fireworks during this native terminal phase.
a=code.index('  if(F.t>=.28&&!F.released)');b=code.index('  if(F.t>=5.1)',a)
code=code[:a]+"  if(F.t>=.28&&!F.released){F.released=true;hf17Log('chromium-implosion');}\n"+code[b:]
code=code.replace('if(F.t>=5.1)','if(F.t>=2.35)',1)
(C/'hammer_finale_1017.js').write_text(code,encoding='utf-8',newline='\n')
shutil.copy2(ROOT/'assets/hammer_finale_1017.js',C/'hammer_finale_1017.original.js')
print(json.dumps(manifest))
