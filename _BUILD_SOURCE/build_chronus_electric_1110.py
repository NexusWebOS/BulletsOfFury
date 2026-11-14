from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,math,sys
from scipy.ndimage import binary_dilation,distance_transform_edt
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
W=R/'_ART_SOURCES/chronus_electric_1110' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).resolve().parent
O=W if Path(__file__).parent.name=='_BUILD_SOURCE' else W.parents[1]/'outputs/chronus-electric'
C=W/'candidate';F=C/'frames';F.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(W/'support'));sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts')
import pixelcore as px
current=(R/'assets/hammer_finale_1017.js').read_bytes();(C/'before.js').write_bytes(current)
basepath=W/'native-original.js'
if not basepath.exists():basepath=W.parents[1]/'work/chronus-death/candidate/hammer_finale_1017.original.js'
base=basepath.read_text(encoding='utf-8')
arttext=(R/'assets/hammer_finale_art_1017.js').read_text(encoding='utf-8');art=json.JSONDecoder().raw_decode(arttext.split('const HF17_ART=',1)[1])[0]
meta={'expected_source_hash':hashlib.sha256(current).hexdigest(),'banks':{},'fragments':art['fragments'],'source_rules':'1015: source emissive clusters and three hard pixel spill steps; source-over baked frames','effects':[]}
keys=[]
def save(im,name):
    im.save(F/(name+'.png'));keys.append(name);return name

# Preserve the source alpha and material, lighting only actual violet/blue emitters.
source=Image.open(R/art['unlit'][0]['path']).convert('RGBA')
lit=Image.open(R/art['stunned'][0]['path']).convert('RGBA');a=np.array(source);v=np.array(lit)
rgb=v[:,:,:3].astype(float);mx=rgb.max(2);mn=rgb.min(2)
mask=(v[:,:,3]>200)&(rgb[:,:,2]>rgb[:,:,1]*1.18)&(rgb[:,:,2]>105)&((mx-mn)>55)
near=distance_transform_edt(~mask,return_distances=False,return_indices=True)
for level in range(6):
    b=a.copy();u=level/5
    target=np.minimum(rgb+np.array([110,135,110]),255)
    b[:,:,:3]=np.where(mask[:,:,None],rgb*(1-u)+target*u,a[:,:,:3]).astype(np.uint8)
    out=Image.fromarray(b)
    # The 1015 spill follows existing source lamps, never a circular heat shield.
    for radius,alpha in [(3,35),(2,75),(1,130)]:
        if not level:continue
        edge=binary_dilation(mask,iterations=radius)&~(b[:,:,3]>0)
        q=np.zeros_like(b);q[:,:,:3]=[155,215,255];q[:,:,3]=np.where(edge,round(alpha*u),0)
        out=Image.alpha_composite(Image.fromarray(q),out)
    for white in [0,1]:
        q=np.array(out)
        if white:q[:,:,:3]=(q[:,:,:3].astype(float)*.12+255*.88).astype(np.uint8)
        # One fixed direct source derivative, matching the native plate's established display size.
        q=Image.fromarray(q).resize((296,296),Image.Resampling.NEAREST)
        save(q,f'body-{level}-{white}')
meta['banks']['body']={'cell':[296,296],'pivot':[148,148],'levels':6,'white_states':2,'source_alpha_unchanged':True}

# New prompt-generated aura: key/despill and one shared palette at native crop resolution.
master=W/'electric-aura-master.png'
if not master.exists():master=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a/exec-fb5378f1-4f32-46b8-a16f-0cd3aee9dd3e.png')
if master.resolve()!=(O/'electric-aura-master.png').resolve():shutil.copy2(master,O/'electric-aura-master.png')
im=Image.open(master).convert('RGB');frames=[];samples=[]
for i in range(16):
    x,y=round(i%4*im.width/4),round(i//4*im.height/4);rgb=np.array(im.crop((x,y,x+313,y+313)))
    alpha=px.key_mask(rgb,'magenta');rgb=px.despill(rgb,alpha,'magenta');frames.append((rgb,alpha));samples.append(rgb[alpha])
pal,_=px.build_palette([np.concatenate(samples)],18,max_extra=4)
sheet=Image.new('RGBA',(320*16,320));areas=[]
for i,(rgb,alpha) in enumerate(frames):
    out=Image.new('RGBA',(320,320));q=Image.fromarray(np.dstack([px.map_to_palette(rgb,pal),alpha.astype(np.uint8)*255]));out.paste(q,(4,4));sheet.paste(out,(i*320,0));areas.append(int(alpha.sum()))
save(sheet,'aura');meta['banks']['aura']={'cell':[320,320],'count':16,'areas':areas,'palette':['#%02x%02x%02x'%tuple(c) for c in pal]}

# The exact three user-selected effects, including their original shared-palette frames.
families=['boss-heavy','dracodia-surge','stage5-core']
for n in families:
    folder=W/'selected-effects'/n
    if not folder.exists():folder=W.parents[1]/'outputs/boss-deaths'/n
    meta['effects'].append({'family':n,'frames':14,'cell':176})
    strip=Image.new('RGBA',(176*14,176))
    for i in range(14):strip.paste(Image.open(folder/'frames'/f'{n}-{i:02}.png').convert('RGBA'),(i*176,0))
    save(strip,n)
    # Large frame bank directly from the user's lossless master, retaining the same palette.
    source=Image.open(folder/'generated-master.png').convert('RGB');palette=np.array([list(bytes.fromhex(c[1:])) for c in json.loads((folder/f'{n}-sheet.json').read_text())['meta']['palette']],dtype=np.uint8)
    strip=Image.new('RGBA',(320*14,320))
    for i in range(14):
        x,y=round(i%4*source.width/4),round(i//4*source.height/4);rgb=np.array(source.crop((x,y,x+313,y+313)));alpha=px.key_mask(rgb,'magenta');rgb=px.despill(rgb,alpha,'magenta')
        out=Image.new('RGBA',(320,320));out.paste(Image.fromarray(np.dstack([px.map_to_palette(rgb,palette),alpha.astype(np.uint8)*255])),(4,4));strip.paste(out,(i*320,0))
    save(strip,n+'-large')

# Exact existing armor pieces, with rotations authored offline into fixed-cell banks.
for i,a in enumerate(art['fragments']):
    piece=Image.open(R/a['path']).convert('RGBA').resize((110,110),Image.Resampling.NEAREST)
    strip=Image.new('RGBA',(160*16,160))
    for f in range(16):
        rotated=piece.rotate(-f*22.5,resample=Image.Resampling.NEAREST,expand=True)
        out=Image.new('RGBA',(160,160));out.alpha_composite(rotated,((160-rotated.width)//2,(160-rotated.height)//2));strip.paste(out,(f*160,0))
    save(strip,f'piece-{i:02}')
meta['banks']['shatter']={'pieces':18,'rotations':16,'cell':[160,160],'source_pieces':'unchanged original HF17 source-pixel cuts; no invented replacement armor'}
(O/'manifest.json').write_text(json.dumps(meta,indent=2))

helper='''
// CE110: source-pixel 1015 lighting, authored electrical aura and exact source-piece breakup.
const CE110={keys:KEYS,stats:{white:0,normal:0,aura:{},fx:[0,0,0],pieces:0,maxFx:0},families:['boss-heavy','dracodia-surge','stage5-core']};
for(const key of CE110.keys)XART._src['ce110_'+key]='assets/game/levels/stage_05/boss/chronus_electric_1110/'+key+'.png';
function ce110Warm(){let ready=true;for(const k of CE110.keys)if(!XART.rdy('ce110_'+k))ready=false;return ready;}
function ce110Blit(key,frame,size,x,y){const k='ce110_'+key;if(!XART.rdy(k))return;const im=XART.get(k);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,frame*size,0,size,size,Math.round(x-size/2),Math.round(y-size/2),size,size);ctx.restore();}
function ce110Offset(F){const a=[[2,0],[-2,1],[1,-2],[-1,2],[3,-1],[-3,0],[1,2],[-2,-1]];return a[Math.floor(F.age*24)%a.length];}
function ce110Body(e){const F=e.hf17,q=ce110Offset(F),level=Math.min(5,Math.floor(F.age/1.7)),white=e.boss.flash>0||Math.floor(F.age*16)%3===0?1:0;
 const key='body-'+level+'-'+white,im=XART.get('ce110_'+key);if(im)ctx.drawImage(im,Math.round(F.anchor.x+q[0]-148),Math.round(F.anchor.y+q[1]-148));
 CE110.stats[white?'white':'normal']++;const progress=Math.min(8,Math.floor(F.age/.8)),frame=progress<8?progress:8+Math.floor(F.age*14)%8;
 ce110Blit('aura',frame,320,F.anchor.x+q[0],F.anchor.y+q[1]+24);CE110.stats.aura[frame]=(CE110.stats.aura[frame]||0)+1;
}
function ce110Emit(F,x,y,large=false){if(F.blasts.length>=20)return;const family=F.blastSerial++%3;F.blasts.push({x,y,t:0,life:.78,family,large});CE110.stats.fx[family]++;CE110.stats.maxFx=Math.max(CE110.stats.maxFx,F.blasts.length);}
'''.replace('KEYS',json.dumps(keys))
base=base.replace('function hf17Warm()',helper+'\nfunction hf17Warm()',1)
a=base.index('function hf17Warm()');b=base.index('stageLoadBegin=function',a)
base=base[:a]+'function hf17Warm(){return ce110Warm();}\n'+base[b:]
base=base.replace("F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;","F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;F.centerCd=0;",1)
a=base.index('  for(const f of F.blasts)');b=base.index('  if(F.t>=5.1)',a)
base=base[:a]+'''  for(const f of F.blasts)f.t+=dt;F.blasts=F.blasts.filter(f=>f.t<f.life);F.blastCd-=dt;F.centerCd-=dt;F.blastSound-=dt;
  if(F.t<4.1&&F.blastCd<=0){F.blastCd=.11;
   for(let j=0;j<2;j++){const i=F.blastSerial%HF17_ART.fragments.length,p=hf17Fragment(F,i,Math.max(.28,F.t));
    if(p.x>=F.camX-40&&p.x<=F.camX+VW+40&&p.y>=-40&&p.y<=VH+40)ce110Emit(F,p.x,p.y,false);else F.blastSerial++;}
   if(F.blastSound<=0){F.blastSound=.20;Audio.SFX.expSmall?.();}}
  if(F.t<4.1&&F.centerCd<=0){F.centerCd=.20;const n=F.blastSerial,angle=n*2.39996;
   ce110Emit(F,F.core.x+Math.cos(angle)*58,F.core.y+Math.sin(angle)*66,n%3===0);}
'''+base[b:]
a=base.index('function hf17Actor(e)');b=base.index('function hf17Missile(F)',a)
base=base[:a]+'''function hf17Actor(e){const F=e.hf17,p=F.phase;
 if(p!=='burst')ce110Body(e);
 else{
  if(F.t<.28)ce110Body(e);
  if(F.t>=.28)for(let i=0;i<HF17_ART.fragments.length;i++){
   const q=hf17Fragment(F,i),size=160;if(q.x+80<F.camX||q.x-80>F.camX+VW||q.y+80<0||q.y-80>VH)continue;
   const frame=((Math.round(q.rot/(Math.PI*2)*16)%16)+16)%16;ce110Blit('piece-'+String(i).padStart(2,'0'),frame,size,q.x,q.y);CE110.stats.pieces++;}
  for(const f of F.blasts){const size=f.large?320:176,name=CE110.families[f.family]+(f.large?'-large':'');ce110Blit(name,Math.min(13,Math.floor(f.t/.055)),size,f.x,f.y);}
 }
 HF17.last={phase:p,age:F.age,t:F.t,anchor:{...F.anchor},core:{...F.core},impacts:F.impacts};
}
'''+base[b:]
(C/'hammer_finale_1017.js').write_text(base,encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(keys),'body_states':12,'aura_frames':16,'source_shards':18,'effect_families':families,'expected_source_hash':meta['expected_source_hash']}))
