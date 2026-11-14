from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,sys
from scipy.ndimage import distance_transform_edt,binary_dilation
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent
O=W if W.parent.name=='_ART_SOURCES' else W.parents[1]/'outputs/chronus-overload';O.mkdir(parents=True,exist_ok=True)
C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True)
before=(W/'before.js').read_bytes() if (W/'before.js').exists() else (R/'assets/hammer_finale_1017.js').read_bytes();(C/'before.js').write_bytes(before);code=before.decode()
S=R/'_ART_SOURCES/hammer_finale_1017';src=Image.open(S/'references/stunned.png').convert('RGBA');a=np.array(src);rgb=a[:,:,:3].astype(float)
r,g,b=rgb.transpose(2,0,1);mask=(a[:,:,3]>200)&(b>75)&(b>r*1.16)&(b>g*1.05)
Y,X=np.mgrid[:256,:256];core=(X>=116)&(X<=139)&(Y>=134)&(Y<=157);mask|=core&(a[:,:,3]>0)&(b>95)&(b>r*1.03)
mask|=(a[:,:,3]>200)&(rgb.min(2)>190)&binary_dilation(mask,iterations=2)
all_emitters=mask.copy();sockets=np.zeros(mask.shape,bool)
for cx,cy,rx,ry in [(128,145,12,11),(95,124,12,8),(160,120,12,9),(165,166,8,14),(77,185,5,11),(93,183,5,9)]:
 sockets|=((X-cx)/rx)**2+((Y-cy)/ry)**2<=1
mask&=sockets
dist,idx=distance_transform_edt(~mask,return_indices=True)
# Palette swap the source emitters only; preserve metal, source alpha and value shading.
value=rgb.max(2);red=np.stack([value,np.minimum(value*.21,rgb[:,:,1]*.35),np.minimum(value*.11,rgb[:,:,2]*.2)],2)
raw=sorted((S/'returned/drain').glob('frame_*.png'))[1:];assert len(raw)==32
keys=[];sizes=[];reds=[];counts=[]
def save(im,key):im.save(D/(key+'.png'),optimize=True);keys.append(key)
for i in range(40):
 t=5.2*i/39;u=min(1,t/1.25);size=296+2*round(89*(i/39)**.82);sizes.append(size);reds.append(round(u,5))
 color=rgb*(1-u)+red*u;normal=rgb.copy();normal[mask]=color[mask];normal[mask]=np.clip(normal[mask]+color[mask]*.30,0,255)
 for lo,hi,amount in [(0,1,.27),(1,2,.14),(2,3,.06)]:
  edge=(dist>lo)&(dist<=hi)&~mask;near=color[idx[0],idx[1]];normal[edge]=np.minimum(255,normal[edge]+near[edge]*amount)
 # Retain original PixelLab energy motion, registered to the same swelling plate.
 frame=int((8*min(10,9.35+t)+1.6*min(10,9.35+t)**2+max(0,t-.65)*40))%32
 v=np.array(Image.open(raw[frame]).convert('RGBA'));vrgb=v[:,:,:3].astype(float);rr,gg,bb=vrgb.transpose(2,0,1)
 blue=(v[:,:,3]>0)&(bb>85)&(bb>rr*1.18)&(bb>gg*1.08);white=(v[:,:,3]>0)&(vrgb.min(2)>185)&binary_dilation(blue,iterations=2)
 keep=(blue|white)&~binary_dilation(all_emitters,iterations=1);v[:,:,3]=np.where(keep,v[:,:,3],0)
 val=vrgb.max(2);warm=np.stack([val,val*.26,val*.18],2);v[:,:,:3]=np.clip(vrgb*(1-u)+warm*u,0,255).astype('uint8');v[v[:,:,3]==0]=0
 energy=Image.fromarray(v);counts.append(int(keep.sum()))
 for flash in [0,1]:
  body=a.copy();body[:,:,:3]=normal.clip(0,255).astype('uint8')
  if flash:
   # Fast core-only white-hot/red alternation leaves the armor readable.
   body[mask,:3]=np.clip(normal[mask]*.18+np.array([255,238,215])*.82,0,255).astype('uint8')
  im=Image.fromarray(body);im.alpha_composite(energy)
  cell=Image.new('RGBA',(480,480));scaled=im.resize((size,size),Image.Resampling.NEAREST)
  # Existing reactor128,145 is the immutable impact mount within the480px cell.
  cell.alpha_composite(scaled,(240-round(127*size/256),240-round(145*size/256)))
  assert cell.getbbox() and cell.getbbox()[0]>0 and cell.getbbox()[2]<480
  save(cell,f'overload-{i:02}-{flash}')
art=json.loads((R/'assets/game/levels/stage_05/boss/hammer_finale_1017/manifest.json').read_text())
for i,p in enumerate(art['fragments']):
 im=Image.open(R/p['path']).convert('RGBA').resize((176,176),Image.Resampling.NEAREST);sheet=Image.new('RGBA',(256*16,256))
 for f in range(16):
  q=im.rotate(-f*22.5,resample=Image.Resampling.NEAREST,expand=True);cell=Image.new('RGBA',(256,256));cell.alpha_composite(q,((256-q.width)//2,(256-q.height)//2));sheet.paste(cell,(256*f,0))
 save(sheet,f'piece-{i:02}')
sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts');import pixelcore as px
for n in ['boss-heavy','dracodia-surge','stage5-core']:
 folder=R/'_ART_SOURCES/chronus_electric_1110/selected-effects'/n
 source=Image.open(folder/'generated-master.png').convert('RGB');pal=np.array([list(bytes.fromhex(c[1:])) for c in json.loads((folder/f'{n}-sheet.json').read_text())['meta']['palette']],dtype=np.uint8);strip=Image.new('RGBA',(480*14,480))
 for i in range(14):
  x,y=round(i%4*source.width/4),round(i//4*source.height/4);q=np.array(source.crop((x,y,x+313,y+313)));alpha=px.key_mask(q,'magenta');q=px.despill(q,alpha,'magenta');im=Image.fromarray(np.dstack([px.map_to_palette(q,pal),alpha.astype('uint8')*255]));im=im.resize((464,464),Image.Resampling.NEAREST);cell=Image.new('RGBA',(480,480));cell.paste(im,(8,8));strip.paste(cell,(480*i,0))
 save(strip,n+'-mega')
helper='''
// CO110: authored swelling, source-core red transition and staged cookoff after missile impact.
const CO110={keys:KEYS,stats:{poses:{},redSteps:{},coreFlashes:0,cookoff:0,mega:0,maxCookoff:0},duration:5.2,sizes:SIZES};
for(const k of CO110.keys)XART._src['co110_'+k]='assets/game/levels/stage_05/boss/chronus_overload_1110/'+k+'.png';
function co110Warm(){let ready=true;for(const k of CO110.keys)if(!XART.rdy('co110_'+k))ready=false;return ready;}
function co110Blit(key,frame,size,x,y){const k='co110_'+key;if(!XART.rdy(k))return;const im=XART.get(k);ctx.drawImage(im,frame*size,0,size,size,Math.round(x-size/2),Math.round(y-size/2),size,size);}
function co110Body(e){const F=e.hf17;if(F.phase==='engulf'&&F.t<.12&&e.boss.flash>0){ce110Body(e);return;}const t=F.phase==='burst'?CO110.duration:F.t,i=Math.min(39,Math.floor(t/CO110.duration*39)),flash=t>=1.25&&Math.floor((t-1.25)*10+(t-1.25)**2*2)%2===0?1:0,q=ce110Offset(F);
 co110Blit('overload-'+String(i).padStart(2,'0')+'-'+flash,0,480,F.core.x+q[0],F.core.y+q[1]);CO110.stats.poses[i]=(CO110.stats.poses[i]||0)+1;CO110.stats.redSteps[Math.min(10,Math.floor(t/1.25*10))]=true;if(flash)CO110.stats.coreFlashes++;
}
function co110TickBlasts(F,dt){for(const f of F.blasts)f.t+=dt;F.blasts=F.blasts.filter(f=>f.t<f.life);}
function co110DrawBlasts(F){for(const f of F.blasts||[]){const frame=Math.min(13,Math.floor(f.t/.055));if(f.mega)co110Blit(CE110.families[f.family]+'-mega',frame,480,f.x,f.y);else{const size=f.large?320:176;ce110Blit(CE110.families[f.family]+(f.large?'-large':''),frame,size,f.x,f.y);}}}
function co110Mega(F,x,y){const n=F.blasts.length;ce110Emit(F,x,y,true);if(F.blasts.length>n){F.blasts[F.blasts.length-1].mega=true;CO110.stats.mega++;}}
'''.replace('KEYS',json.dumps(keys)).replace('SIZES',json.dumps(sizes))
idx=code.index('function hf17Warm()');code=code[:idx]+helper+'\n'+code[idx:]
code=code.replace('function hf17Warm(){return ce110Warm();}','function hf17Warm(){const a=ce110Warm(),b=co110Warm();return a&&b;}')
code=code.replace("F.impacts++;e.boss.dying=0;markHit(e.boss);", "F.blasts=[];F.blastCd=1.7;F.blastSerial=0;F.blastSound=0;F.impacts++;e.boss.dying=0;markHit(e.boss);")
old="if(name==='burst'){F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;F.centerCd=0;Audio.SFX.expBig?.();Audio.SFX.hammerImpact?.();}"
new="if(name==='burst'){F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;F.centerCd=0;Audio.SFX.expBig?.();Audio.SFX.hammerImpact?.();for(const q of [[-58,-26],[58,-20],[0,60]])co110Mega(F,F.core.x+q[0],F.core.y+q[1]);hf17Log('massive-blowup',{cookoff:CO110.stats.cookoff});}"
assert old in code;code=code.replace(old,new)
old="e.boss.dying=F.t;shake=2+F.t*2;\n  if(F.t>=2)hf17Phase(e,'burst');"
new="""e.boss.dying=F.t;shake=2+F.t;co110TickBlasts(F,dt);F.blastCd-=dt;F.blastSound-=dt;
  if(F.t>=1.7&&F.blastCd<=0){const u=Math.min(1,(F.t-1.7)/3.5);F.blastCd=.72*(1-u)+.085*u;const n=F.blastSerial,angle=n*2.39996,r=54+u*66;
   ce110Emit(F,F.core.x+Math.cos(angle)*r,F.core.y+Math.sin(angle)*r*.8,u>.78&&n%3===0);CO110.stats.cookoff++;CO110.stats.maxCookoff=Math.max(CO110.stats.maxCookoff,F.blasts.length);
   if(F.blastSound<=0){F.blastSound=.2;Audio.SFX.expSmall?.();}hf17Log('cookoff',{t:F.t,interval:F.blastCd});}
  if(F.t>=CO110.duration)hf17Phase(e,'burst');"""
assert old in code;code=code.replace(old,new)
code=code.replace('const a=HF17_ART.fragments[i],k=240/208,t=Math.max(0,age-.28)', 'const a=HF17_ART.fragments[i],k=474/256,t=Math.max(0,age-.28)')
code=code.replace('v=150+(i%5)*24;', 'v=190+(i%5)*28;')
code=code.replace('F.anchor.x+(a.origin[0]-128)*k','F.core.x+(a.origin[0]-127)*k').replace('F.anchor.y+(a.origin[1]-128)*k','F.core.y+(a.origin[1]-145)*k')
start=code.index('function hf17Actor(e)');end=code.index('function hf17Missile(F)',start)
code=code[:start]+'''function hf17Actor(e){const F=e.hf17,p=F.phase;
 if(p==='engulf'){co110Body(e);co110DrawBlasts(F);}
 else if(p!=='burst')ce110Body(e);
 else{
  if(F.t<.28)co110Body(e);
  if(F.t>=.28)for(let i=0;i<HF17_ART.fragments.length;i++){
   const q=hf17Fragment(F,i),size=256;if(q.x+128<F.camX||q.x-128>F.camX+VW||q.y+128<0||q.y-128>VH)continue;
   const frame=((Math.round(q.rot/(Math.PI*2)*16)%16)+16)%16;co110Blit('piece-'+String(i).padStart(2,'0'),frame,size,q.x,q.y);CE110.stats.pieces++;}
  co110DrawBlasts(F);
 }
 HF17.last={phase:p,age:F.age,t:F.t,anchor:{...F.anchor},core:{...F.core},impacts:F.impacts};
}
'''+code[end:]
(C/'hammer_finale_1017.js').write_text(code,encoding='utf-8',newline='\n')
meta={'expected_source_hash':hashlib.sha256(before).hexdigest(),'duration':5.2,'red_transition_seconds':1.25,'first_explosion':1.7,'size_range':[296,474],'size_steps':sizes,'red_steps':reds,'cell':[480,480],'pivot':[240,240],'fixed_mount':'original reactor127,145','files':keys,'source':'original256px stunned pose and preserved PixelLab drain32frames; direct master exports','effects':'same three selected families; added480px direct-master final blasts','render':'authored frames, ordinary source-over; no runtime scaling, tint or alpha fade'}
(O/'manifest.json').write_text(json.dumps(meta,indent=2))
contact=Image.new('RGB',(1440,960),'#10192b');d=ImageDraw.Draw(contact)
for j,i in enumerate([0,7,12,20,29,39]):
 im=Image.open(D/f'overload-{i:02}-0.png');contact.paste(im,(j%3*480,j//3*480),im);d.text((j%3*480+5,j//3*480+5),f'{5.2*i/39:.2f}s / {sizes[i]}px',fill='white')
contact.save(W/'overload-contact.png');print(json.dumps({'files':len(keys),'sizes':[sizes[0],sizes[-1]],'duration':5.2}))
