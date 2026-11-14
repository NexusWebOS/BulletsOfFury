from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
from scipy.ndimage import binary_dilation,distance_transform_edt
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True)
O=W if W.parent.name=='_ART_SOURCES' else W.parents[1]/'outputs/dracodia-overload';O.mkdir(parents=True,exist_ok=True)
def meta(name):
 s=(R/'assets'/name).read_text();return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
A=meta('dracodia_terminal_art_1030.js');I=meta('stage8_identity_art_1018.js')
raw=I['clips']['colossus_roar']['frames'][12];src=Image.open(R/raw['path']).convert('RGBA');a=np.array(src);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
energy=(a[:,:,3]>200)&(r>95)&(r>g*1.35)&(b>g*1.15);energy|=(rgb.min(2)>205)&(a[:,:,3]>200)&binary_dilation(energy,iterations=2)
dist,near=distance_transform_edt(~energy,return_indices=True);value=rgb.max(2);red=np.stack([value,value*.14,value*.08],2)
records={};sizes=[]
def save(im,key,size=None):
 im.save(D/(key+'.png'),optimize=True);records[key]={'path':'assets/game/levels/stage_08/ending/dracodia_overload_1110/'+key+'.png','cell':size or im.width}
def palette(u,flash=False):
 q=a.copy();color=rgb*(1-u)+red*u;out=rgb.copy();out[energy]=np.minimum(255,color[energy]*1.23)
 for lo,hi,amount in [(0,1,.24),(1,2,.12),(2,3,.05)]:
  edge=(dist>lo)&(dist<=hi)&~energy;v=color[near[0],near[1]];out[edge]=np.minimum(255,out[edge]+v[edge]*amount)
 if flash:out[energy]=out[energy]*.13+np.array([255,245,232])*.87
 q[:,:,:3]=out.clip(0,255).astype('uint8');q[q[:,:,3]==0]=0;return Image.fromarray(q)
for i in range(40):
 u=i/39;size=410+2*round(98*u**.82);sizes.append(size)
 for flash in [0,1]:
  im=palette(min(1,5.2*u/1.25),flash);im=im.resize((size,size),Image.Resampling.NEAREST);cell=Image.new('RGBA',(640,640));cell.alpha_composite(im,(320-size//2,320-size//2+round(45*u)));assert cell.getbbox()[0]>0 and cell.getbbox()[2]<640;save(cell,f'body-{i:02}-{flash}')
# Partition the actual full source body once, never an invented replacement wreck.
v=np.array(palette(1));yy,xx=np.indices(v.shape[:2]);coords=np.argwhere(v[:,:,3]>48);rng=np.random.default_rng(84030);samples=coords[rng.choice(len(coords),56,replace=False)];labels=np.stack([(yy-sy)**2+(xx-sx)**2 for sy,sx in samples]).argmin(0);rebuild=np.zeros_like(v);pieces=[]
for n,(sy,sx) in enumerate(samples):
 mask=(labels==n)&(v[:,:,3]>0);q=np.zeros_like(v);q[mask]=v[mask];rebuild[mask]=q[mask];im=Image.fromarray(q);box=im.getbbox();assert box;im=im.crop(box);cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
 scale=606/320;sz=(max(2,2*round(im.width*scale/2)),max(2,2*round(im.height*scale/2)));im=im.resize(sz,Image.Resampling.NEAREST);cellsize=2*math.ceil((math.hypot(*sz)+8)/2);strip=Image.new('RGBA',(cellsize*16,cellsize))
 for f in range(16):
  rot=im.rotate(-f*22.5,Image.Resampling.NEAREST,expand=True);cell=Image.new('RGBA',(cellsize,cellsize));cell.alpha_composite(rot,((cellsize-rot.width)//2,(cellsize-rot.height)//2));strip.paste(cell,(f*cellsize,0))
 save(strip,f'piece-{n:02}',cellsize);pieces.append({'key':f'piece-{n:02}','cell':cellsize,'dx':(cx-160)*scale,'dy':(cy-160)*scale+45,'angle':math.atan2(cy-160,cx-160),'sourceCut':box})
assert np.array_equal(rebuild,v)
families=['boss-heavy','dracodia-surge','stage5-core']
for n in families:
 for suffix,size,folder in [('',176,'chronus_electric_1110'),('-large',320,'chronus_electric_1110'),('-mega',480,'chronus_overload_1110')]:
  records[n+suffix]={'path':f'assets/game/levels/stage_05/boss/{folder}/{n+suffix}.png','cell':size}
before=(W/'before.js').read_bytes() if (W/'before.js').exists() else (R/'assets/dracodia_terminal_1030.js').read_bytes();(C/'before.js').write_bytes(before);code=before.decode()
helper='''
// DF110: post-teleport red overload, massive blasts and exact source-body fragments.
const DF110_ART=RECORDS;
const DF110={pieces:PIECES,families:['boss-heavy','dracodia-surge','stage5-core'],stats:{poses:{},redSteps:{},coreFlashes:0,cookoff:0,mega:0,shards:0,trailBlasts:0,maxFx:0,fx:[0,0,0]}};
for(const [k,a]of Object.entries(DF110_ART))XART._src['df110_'+k]=a.path;
function df110Blit(k,f,x,y){const a=DF110_ART[k],key='df110_'+k;if(!a||!XART.rdy(key))return;const size=a.cell;ctx.drawImage(XART.get(key),f*size,0,size,size,Math.round(x-size/2),Math.round(y-size/2),size,size);}
function df110State(b){const Q=dr5State(b).rd84;return Q.df110||=( {blasts:[],serial:0,next:1.7,sound:0,trail:0,center:0} );}
function df110Emit(b,x,y,size=176){const E=df110State(b);if(E.blasts.length>=24)return;const family=E.serial++%3;E.blasts.push({x,y,size,family,t:0,life:.78});DF110.stats.fx[family]++;DF110.stats.maxFx=Math.max(DF110.stats.maxFx,E.blasts.length);if(size===480)DF110.stats.mega++;}
function df110Fragment(b,i,t){const p=DF110.pieces[i],speed=180+i%7*29,spin=(i%2?1:-1)*(2+i%4),u=Math.max(0,t-.12);return{x:b.x+p.dx+Math.cos(p.angle)*speed*u,y:b.y+p.dy+Math.sin(p.angle)*speed*u-35*u+24*u*u,f:((Math.round(u*spin/(Math.PI*2)*16)%16)+16)%16};}
function df110Tick(b,dt){const Q=dr5State(b).rd84,E=df110State(b),t=b._r30.t,age=t-13.2;
 for(const f of E.blasts)f.t+=dt;E.blasts=E.blasts.filter(f=>f.t<f.life);E.sound-=dt;
 if(age<5.2){if(age>=E.next){const u=Math.min(1,(age-1.7)/3.5),interval=.72*(1-u)+.085*u,n=E.serial,angle=n*2.39996,r=58+70*u;E.next=age+interval;df110Emit(b,b.x+Math.cos(angle)*r,b.y+22+Math.sin(angle)*r,age>4.3&&n%3===0?320:176);DF110.stats.cookoff++;rd84Log(b,'overload-cookoff',{age,interval});if(E.sound<=0){E.sound=.2;rd84Cue(b,'expSmall',.7);}}return;}
 const burst=age-5.2;
 if(!Q.events.has('df110-shatter')){Q.events.add('df110-shatter');Q.shatterAt={x:b.x,y:b.y};dr5State(b).bodyGone=true;for(const p of [[-65,-24],[65,-18],[0,70]])df110Emit(b,b.x+p[0],b.y+p[1],480);rd84Cue(b,'rd71ScreamB',.9);rd84Cue(b,'expBig',1);rd84Log(b,'whole-body-shatter',{pieces:56});rd84Log(b,'massive-blowup',{cookoff:DF110.stats.cookoff});}
 E.trail-=dt;E.center-=dt;if(burst<4.1&&E.trail<=0){E.trail=.085;for(let j=0;j<2;j++){const i=E.serial%56,p=df110Fragment(b,i,burst);if(p.x>=camLeftX()-60&&p.x<=camLeftX()+viewW()+60&&p.y>=viewTopY()-60&&p.y<=viewTopY()+VH+60){df110Emit(b,p.x,p.y);DF110.stats.trailBlasts++;}else E.serial++;}if(E.sound<=0){E.sound=.2;rd84Cue(b,'expSmall',.65);}}
 if(burst<3.4&&E.center<=0){E.center=.22;const a=E.serial*2.39996;df110Emit(b,b.x+Math.cos(a)*72,b.y+38+Math.sin(a)*75,320);}
}
function df110Draw(b){const Q=dr5State(b).rd84,age=b._r30.t-13.2,burst=age-5.2,E=df110State(b);
 if(burst<.12){const i=Math.min(39,Math.floor(Math.max(0,age)/5.2*39)),d=Math.max(0,age-1.25),flash=!RD84.reducedMotion&&age>=1.25&&Math.floor(d*10+d*d*2)%2===0?1:0;df110Blit('body-'+String(i).padStart(2,'0')+'-'+flash,0,b.x+Q.dx,b.y+Q.dy);DF110.stats.poses[i]=(DF110.stats.poses[i]||0)+1;DF110.stats.redSteps[Math.min(10,Math.floor(Math.max(0,age)/1.25*10))]=true;if(flash)DF110.stats.coreFlashes++;}
 else for(let i=0;i<56;i++){const p=df110Fragment(b,i,burst),m=DF110.pieces[i],r=m.cell/2;if(p.x+r<camLeftX()||p.x-r>camLeftX()+viewW()||p.y+r<viewTopY()||p.y-r>viewTopY()+VH)continue;df110Blit(m.key,p.f,p.x,p.y);DF110.stats.shards++;}
 for(const f of E.blasts)df110Blit(DF110.families[f.family]+(f.size===480?'-mega':f.size===320?'-large':''),Math.min(13,Math.floor(f.t/.055)),f.x,f.y);
}
'''.replace('RECORDS',json.dumps(records,separators=(',',':'))).replace('PIECES',json.dumps(pieces,separators=(',',':')))
idx=code.index('function rd84Keys()');code=code[:idx]+helper+'\n'+code[idx:]
code=code.replace("return[...Object.keys(RD84_ART.pages)","return[...Object.keys(DF110_ART).map(k=>'df110_'+k),...Object.keys(RD84_ART.pages)",1)
start=code.index("}else if(t<16.4){Q.phase='shatter'");end=code.index(' if(t>=18.4)',start)
code=code[:start]+"""}else if(t<18.4){Q.phase='post-teleport-overload';Q.white=0;Q.flash=0;df110Tick(b,dt);
 }else if(t<23.5){Q.phase='shatter';Q.white=0;Q.flash=0;df110Tick(b,dt);
 }else{Q.phase='aftermath';Q.white=0;Q.flash=0;df110Tick(b,dt);}
"""+code[end:]
code=code.replace("if(t>=18.4){S.mode='dr5Portal'","if(t>=25.5){S.mode='dr5Portal'",1)
old="const x=b.x+Q.dx,y=b.y+Q.dy;if(t<13.2)"
assert old in code;code=code.replace(old,"const x=b.x+Q.dx,y=b.y+Q.dy;if(t>=13.2){df110Draw(b);return;}if(t<13.2)",1)
code=code.replace("if(t>=13.2&&t<16.4)rd84Bank('body_shatter',(t-13.2)*20,Q.shatterAt.x,Q.shatterAt.y);",'// Post-download breakup is owned by the source-fragment overload above.')
(C/'dracodia_terminal_1030.js').write_text(code,encoding='utf-8',newline='\n')
manifest={'expected_source_hash':hashlib.sha256(before).hexdigest(),'source':raw,'teleport_preserved_until':13.2,'overload':[13.2,18.4],'shatter':[18.4,23.5],'portal':25.5,'body_cell':[640,640],'body_sizes':sizes,'red_transition':1.25,'first_cookoff':1.7,'pieces':pieces,'reassembles_exact_source_rgba':True,'records':records,'draw':'fixed authored frames, no runtime scale/tint/rotation/alpha changes'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
contact=Image.new('RGB',(1280,640),'#10192b')
for j,i in enumerate([0,39]):
 im=Image.open(D/f'body-{i:02}-0.png');contact.paste(im,(640*j,0),im)
contact.save(W/'overload-contact.png');print(json.dumps({'new_assets':len(list(D.glob('*.png'))),'pieces':len(pieces),'source':raw['path'],'sizes':[sizes[0],sizes[-1]]}))
