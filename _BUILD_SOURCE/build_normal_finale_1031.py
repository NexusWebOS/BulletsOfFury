from pathlib import Path
import json,math,hashlib,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1]
D=R/'assets/game/shared/cinematics/normal_finale_1031';D.mkdir(parents=True,exist_ok=True)
M={'banks':{},'sources':{},'format':'Fixed even authored cells; offline depth/fades; original pilot aircraft.'}
def source(p):
 M['sources'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest();return Image.open(R/p).convert('RGBA')
def bank(n,ims,fps=20):
 w,h=ims[0].size;assert w%2==h%2==0
 cols=min(8,4096//w);per=cols*(4096//h);pages=[]
 for start in range(0,len(ims),per):
  batch=ims[start:start+per];sheet=Image.new('RGBA',(cols*w,math.ceil(len(batch)/cols)*h))
  for j,im in enumerate(batch):sheet.alpha_composite(im,(j%cols*w,j//cols*h))
  fn=n+'_'+str(start//per)+'.png';sheet.save(D/fn);pages.append({'key':'nf100_'+n+'_'+str(start//per),'path':str((D/fn).relative_to(R)).replace('\\','/'),'start':start,'frames':len(batch)})
 M['banks'][n]={'w':w,'h':h,'cols':cols,'frames':len(ims),'fps':fps,'pages':pages}
def cover(im,anchor=.5):
 k=max(480/im.width,512/im.height);im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);x=round((im.width-480)*anchor);return im.crop((x,0,x+480,512))
earth=cover(source('assets/game/shared/cinematics/homecoming_1010/earth.png'))
hq=cover(source('assets/game/shared/cinematics/hq_landing_1010/background_00.png'),.76)
bank('earth',[earth]);bank('hq',[hq])
# Re-author the approved menu-only frame at its actual output size.
im=source('assets/game/shared/ui/menu_windows_1021/xl.webp');out=Image.new('RGBA',(456,404))
sx=[0,64,im.width-64,im.width];sy=[0,74,im.height-32,im.height];dx=[0,64,392,456];dy=[0,74,372,404]
for j in range(3):
 for i in range(3):out.alpha_composite(im.crop((sx[i],sy[j],sx[i+1],sy[j+1])).resize((dx[i+1]-dx[i],dy[j+1]-dy[j]),Image.Resampling.NEAREST),(dx[i],dy[j]))
bank('window',[out])
bank('fade',[Image.new('RGBA',(480,512),(0,0,0,round(i/15*255)))for i in range(16)],fps=30)
s=(R/'assets/manifest.js').read_text(encoding='utf8');d=json.JSONDecoder().raw_decode(s[s.index('{',s.index('window.BOFX')):])[0]
for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
 row=d['ships']['ship_'+pk+'_so2'];im=source(d['img']['nsa_ship_'+pk]);x,y,w,h=row[:4];im=im.crop((x,y,x+w,y+h));ims=[]
 for i in range(48):
  k=i/47;size=round(108*(1-k)+14*k);ww=size;hh=max(2,round(size*h/w));f=im.resize((ww,hh),Image.Resampling.NEAREST);c=Image.new('RGBA',(128,96));c.alpha_composite(f,((128-ww)//2,(96-hh)//2));ims.append(c)
 bank('ship_'+pk,ims,fps=20)
(D/'manifest.json').write_text(json.dumps(M,separators=(',',':')),encoding='utf8')
(R/'assets/normal_finale_art_1031.js').write_text("'use strict';\nconst NF100_ART="+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB)
 for _,page in ipairs(a.pages)do local path=page.path:match('([^/]+)$');local im=Image{fromFile=D..'/'..path}
  for j=0,page.frames-1 do local i=page.start+j;if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(j%a.cols*a.w,math.floor(j/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 end;s:saveAs(D..'/'..n..'.aseprite');s:close()
end"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
print('Authored',sum(a['frames']for a in M['banks'].values()),'frames;',len(M['banks']),'editable banks.')
