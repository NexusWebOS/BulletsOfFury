from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True);O=W.parents[1]/'outputs/stage67-repair';O.mkdir(parents=True,exist_ok=True)
def meta(n):
 s=(R/'assets'/n).read_text();return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
E=meta('enemy_hud_art_1007c.js');M=meta('thunderhead_modular_art_1104.js');records={};bars={}
def save(im,n,cell=None):
 im.save(D/(n+'.png'),optimize=True);records[n]={'path':'assets/game/shared/combat/stage67_repair_1110/'+n+'.png','cell':cell or list(im.size)}
for theme,n,variant in [('stage_06','thunder','boss'),('stage_07','snake','mini')]:
 a=E[theme];d=a['variants'][variant];im=Image.open(R/a['path']).convert('RGBA');x,y,w,h=d['crop'];base=im.crop((x,y,x+w,y+h));hx,hy,hw,hh=d['hp'];empty=im.crop((d['emptyX'],hy,d['emptyX']+4,hy+hh)).resize((hw,hh),Image.Resampling.NEAREST);base.paste(empty,(hx-x,hy-y));width=420;height=2*round(h*width/w/2);base=base.resize((width,height),Image.Resampling.NEAREST)
 well=[round((hx-x)*width/w),round((hy-y)*height/h),2*round(hw*width/w/2),2*round(hh*height/h/2)]
 fill=im.crop((d['litX'],hy,d['litX']+4,hy+hh)).resize((well[2],well[3]),Image.Resampling.NEAREST);save(base,n+'-frame');save(fill,n+'-fill');bars[n]={'w':width,'h':height,'well':well,'source':a['path']}
# One continuous funnel, with no copied fan/sticker. The real animated metal cannon covers its root.
B=M['banks']['wind_beam'];strip=Image.new('RGBA',(288*28,544))
for f,c in enumerate(B['cells']):
 im=Image.open(R/M['pages'][c[0]]['path']).convert('RGBA').crop((c[1],c[2],c[1]+288,c[2]+512));cell=Image.new('RGBA',(288,544))
 for y in range(512):
  u=min(1,y/150);u=u*u*(3-2*u);width=2*round((76+212*u)/2);row=im.crop((0,y,288,y+1)).resize((width,1),Image.Resampling.NEAREST);cell.alpha_composite(row,((288-width)//2,y))
 strip.paste(cell,(288*f,0))
save(strip,'beam',[288,544])
# Wider overlapping source-rib sections with a genuinely tapered tail; every turn is baked.
source=Image.open(R/'_ART_SOURCES/sumpjaw_duo_1031/sources/pixellab/body_01.png').convert('RGBA').crop((46,23,76,53));mask=Image.new('L',(30,30));ImageDraw.Draw(mask).polygon([(7,1),(22,1),(29,10),(27,23),(18,29),(5,26),(0,13)],fill=255);source.putalpha(Image.fromarray(np.minimum(np.array(source.getchannel('A')),np.array(mask))))
for i,size in enumerate([42,38,32,26,20,12]):
 for mode in ['body','hit','shadow']:
  im=source.resize((size,size),Image.Resampling.NEAREST);v=np.array(im)
  if mode=='hit':v[:,:,:3]=255
  if mode=='shadow':v[:,:,:3]=[3,10,8];v[:,:,3]=(v[:,:,3]*.5).astype('uint8')
  im=Image.fromarray(v);base=Image.new('RGBA',(64,64));base.alpha_composite(im,((64-size)//2,(64-size)//2));strip=Image.new('RGBA',(64*32,64))
  for n in range(32):strip.paste(base.rotate(-n*360/32,Image.Resampling.NEAREST),(64*n,0))
  save(strip,f'rib{i}-{mode}',[64,64])
files=['thunderhead_reactor_1105.js','sumpjaw_tandem_1105.js','playtest_repairs_1108.js'];hashes={};codes={}
for n in files:
 live=(R/'assets'/n).read_bytes();p=C/(n+'.before');b=p.read_bytes() if p.exists() else live
 assert live==b or (C/n).exists() and live==(C/n).read_bytes(),'Concurrent source change: '+n
 hashes[n]=hashlib.sha256(live).hexdigest()
 if not p.exists():p.write_bytes(b)
 codes[n]=b.decode()
helper='''
// SR110: original generated HUD derivatives, source-authored funnel and serpentine ribs.
const SR110={art:@@ART@@,bars:@@BARS@@,hud:{},beams:0};
for(const[k,a]of Object.entries(SR110.art))XART._src['sr110_'+k]=a.path;
function sr110Ready(){return Object.keys(SR110.art).map(k=>XART.rdy('sr110_'+k)).every(Boolean);}
function sr110Blit(k,f,x,y,pivot){const a=SR110.art[k],im=XART.get('sr110_'+k);if(!im)return;const[w,h]=a.cell,p=pivot||[w/2,h/2];ctx.drawImage(im,f*w,0,w,h,Math.round(x-p[0]),Math.round(y-p[1]),w,h);}
function sr110Hud(n,values,cx,cy){const a=SR110.bars[n];if(!XART.rdy('sr110_'+n+'-frame')||!XART.rdy('sr110_'+n+'-fill'))return;const x=Math.round(cx-a.w/2),y=Math.max(2,Math.round(cy-a.h/2)),[hx,hy,hw,hh]=a.well;ctx.drawImage(XART.get('sr110_'+n+'-frame'),x,y);const im=XART.get('sr110_'+n+'-fill');let widths=[];
 for(let i=0;i<values.length;i++){const span=values.length===2?Math.floor((hw-4)/2):hw,dx=values.length===2?i*(span+4):0,w=Math.ceil(span*clamp(values[i],0,1));if(w>0)ctx.drawImage(im,0,0,w,hh,x+hx+dx,y+hy,w,hh);widths.push(w);}SR110.hud[n]={x,y,well:a.well,values:[...values],widths};}
const sr110Bar=drawHealthBarV2;drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld){if(kind!=='boss'||!tc119Own(boss))return sr110Bar.apply(this,arguments);ctx.save();if(inWorld===true)ctx.translate(camX,0);sr110Hud('thunder',[boss.hp/Math.max(1,boss.maxhp)],cx,cy);ctx.restore();return true;};
'''.replace('@@ART@@',json.dumps(records,separators=(',',':'))).replace('@@BARS@@',json.dumps(bars,separators=(',',':')))
t=codes[files[0]];idx=t.index('function tc119Own');t=t[:idx]+helper+'\n'+t[idx:]
t=t.replace('function fb112', 'function fb112')
t=t.replace('if(TC119.ready)return true;', 'if(!sr110Ready())return false;if(TC119.ready)return true;',1)
start=t.index('function tc119Beams(b)');end=t.index('fb112Draw=function',start)
t=t[:start]+'''function sr110CannonBeams(b){for(const B of tm115State(b).beams){if(B.part.hp<=0)continue;const at=fb112Bore(b,B.part);const f=B.recovery?22+Math.min(5,Math.floor(B.tail*24)):B.age<TM115.beamGrow?Math.min(5,Math.floor(B.age*24)):6+Math.floor((B.age-TM115.beamGrow)*24)%16;sr110Blit('beam',f,at.x,at.y,[144,0]);const m=fb112PartPoint(b,B.part);tc119Blit('pod'+B.part.index+'_lip',0,m.x,m.y);SR110.beams++;}}
function tc119Beams(b){return sr110CannonBeams(b);}
'''+t[end:]
codes[files[0]]=t
s=codes[files[1]];s=s.replace('if(SJ120.ready)return true;', 'if(!sr110Ready())return false;if(SJ120.ready)return true;',1)
start=s.index('function sj120ResetTrail');end=s.index('function sj120Set',start)
s=s[:start]+'''function sj120ResetTrail(a){const p=sj120Neck(a);a.trail=Array.from({length:85},(_,i)=>({x:p.x+Math.sin(a.heading)*i*4,y:p.y-Math.cos(a.heading)*i*4,h:p.h,heading:a.heading}));}
function sj120Trail(a){const p=sj120Neck(a),q=a.trail[0],d=Math.hypot(p.x-q.x,p.y-q.y),n=Math.max(1,Math.ceil(d/3));if(d>1||Math.abs(p.h-q.h)>1){for(let i=1;i<=n;i++){const u=i/n;a.trail.unshift({x:lerp(q.x,p.x,u),y:lerp(q.y,p.y,u),h:lerp(q.h,p.h,u),heading:p.heading});}}if(a.trail.length>240)a.trail.length=240;}
'''+s[end:]
start=s.index('function sj120Segments');end=s.index('function sj120Warnings',start)
s=s[:start]+'''function sr110SnakePoint(a,d){const p=ss116Point(a,d),amp=Math.min(24,d*.19)*Math.min(1,(250-d)/70),wave=Math.sin(a.clock*7-d*.048+a.i*Math.PI)*Math.max(0,amp);return{x:p.x+Math.cos(p.heading)*wave,y:p.y+Math.sin(p.heading)*wave,h:p.h};}
function sj120Segments(a,shadow){for(let i=15;i>=0;i--){const d=i*15,p=sr110SnakePoint(a,d),lead=sr110SnakePoint(a,Math.max(0,d-3)),tail=sr110SnakePoint(a,d+3),angle=Math.atan2(-(lead.x-tail.x),lead.y-tail.y),n=((Math.round(angle/TAU*32)%32)+32)%32,type=i<3?0:i<6?1:i<9?2:i<12?3:i<14?4:5;sr110Blit('rib'+type+'-'+(shadow?'shadow':a.flash>0?'hit':'body'),n,p.x,p.y+(shadow?12:-p.h));}}
'''+s[end:]
start=s.index('function sj120Bar');end=s.index('sj98Draw=function',start)
s=s[:start]+'''function sj120Bar(b){const C=b._sj120;C.bar=b._sj98.actors.map(a=>clamp(a.hp/a.maxhp,0,1));screenBar(()=>{sr110Hud('snake',C.bar,VW/2,34);pm27Draw(ctx,'01',VW/2-70,65,8,{family:'command',palette:'toxic',width:30});pm27Draw(ctx,'02',VW/2+70,65,8,{family:'command',palette:'toxic',width:30});});}
'''+s[end:]
# Follow the head's path on unarmed portions of each leap, keeping the committed south firing interval intact.
s=s.replace("a.y=a.gy-a.height;sj120Trail(a);", "a.y=a.gy-a.height;sj120Trail(a);",1)
codes[files[1]]=s
p=codes[files[2]];start=p.index('tc119Beams=function(b)');end=p.index('const PR118_TH=',start);p=p[:start]+"tc119Beams=function(b){return sr110CannonBeams(b);};\n"+p[end:];codes[files[2]]=p
for n,c in codes.items():(C/n).write_text(c,encoding='utf-8',newline='\n')
manifest={'hashes':hashes,'art':records,'bars':bars,'snake_sections':16,'source':'approved Sumpjaw rib source plus original generated Stage6/7 HUDs and authored Thunderhead wind beam','beam_pivot':[144,0],'behavior':'native attack book, health pools, hit sockets and firing timing retained'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'assets':len(records),'bars':bars,'files':files}))
