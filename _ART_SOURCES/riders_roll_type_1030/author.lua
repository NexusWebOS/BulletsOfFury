local D=app.params.work;local R=app.params.root;local pc=app.pixelColor
local f=io.open(D..'/roll-inputs.json','r');local inputs=json.decode(f:read('*a'));f:close()
local function bank(name,frames,pivot,cols)
 cols=cols or 16;local w,h=frames[1].width,frames[1].height;local out=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do out:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/16 end
 out:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close()
end
for _,row in ipairs(inputs)do local old=Image{fromFile=R..'/assets/game/levels/stage_06/boss/rough_riders_1028/flight_'..row.key..'.png'};local frames={}
 for i=0,71 do table.insert(frames,Image(old,Rectangle(i%16*192,math.floor(i/16)*192,192,192)))end
 local size=math.floor(row.cell*90*row.ratio/row.span/2+.5)*2
 local strip=Image{fromFile=R..'/'..row.path};for i=0,15 do local im=Image(strip,Rectangle(i*row.cell,0,row.cell,row.cell));im:resize(size,size);local out=Image(192,192,ColorMode.RGB);out:drawImage(im,Point((192-size)/2,(192-size)/2));table.insert(frames,out)end
 bank('flight_'..row.key,frames,{96,96},16)
end
local f=io.open(D..'/glyph-masters.json','r');local M=json.decode(f:read('*a'));f:close();local P={'chrome','ice','ember','gold','toxic','rose','signal','corrupt'};local meta={palettes=P,banks={}}
local function rgb(hex,dim)return pc.rgba(math.floor(tonumber(hex:sub(1,2),16)*dim),math.floor(tonumber(hex:sub(3,4),16)*dim),math.floor(tonumber(hex:sub(5,6),16)*dim),255)end
for _,h in ipairs({8,9,10,11,12,14})do local cw=math.ceil((math.floor(5*h/7+.5)+4)/2)*2;local ch=math.ceil((h+8)/2)*2;local sw,sh=cw*16,ch*6;local atlas=Image(sw*2,sh*8,ColorMode.RGB);local glyphs={};local top=2
 for code=32,126 do local c=string.char(code);local rows={};for line in (M.small[c]or M.small['?']):gmatch('[^/]+')do table.insert(rows,line)end
  local short=c:match('%l')and not c:match('[bdfhijklt]');local y0=top+h-math.floor((short and 5 or 7)*h/7+.5);local tw=math.max(1,math.floor(#rows[1]*h/7+.5));local th=math.max(1,math.floor(#rows*h/7+.5));local gx=(code-32)%16*cw;local gy=math.floor((code-32)/16)*ch;local left,right,yt,yb=cw,0,ch,0
  for y=0,th-1 do for x=0,tw-1 do local row=rows[math.min(#rows,math.floor(y/th*#rows)+1)];if row:sub(math.floor(x/tw*#row)+1,math.floor(x/tw*#row)+1)=='1'and code~=32 then
   local xx,yy=x+1,y+y0;left=math.min(left,xx);right=math.max(right,xx+1);yt=math.min(yt,yy);yb=math.max(yb,yy+1)
   for p=1,8 do local hex=M.palettes[P[p]][yy<top+h*.3 and 1 or 2];atlas:drawPixel(gx+xx,gy+yy+(p-1)*sh,rgb(hex,1));atlas:drawPixel(gx+xx+sw,gy+yy+(p-1)*sh,rgb(hex,.43))end
  end end end
  glyphs[tostring(code)]={x=gx,y=gy,advance=code==32 and math.max(3,math.floor(h*.4))or tw+1,ink=right>0 and{left,yt,right,yb}or{0,0,0,0}}
 end
 local name='command_dialogue_'..h;atlas:saveAs(D..'/'..name..'.png');local s=Sprite(atlas.width,atlas.height,ColorMode.RGB);s:newCel(s.layers[1],1,atlas,Point(0,0));s:saveAs(D..'/'..name..'.aseprite');s:close()
 meta.banks[name]={key='pm27_'..name,path='assets/game/shared/ui/riders_dialogue_1030/'..name..'.png',family='command_dialogue',height=h,cw=cw,ch=ch,planeW=sw,planeH=sh,top=top,baseline=top+h,glyphs=glyphs}
end
local f=io.open(D..'/dialogue-manifest.json','w');f:write(json.encode(meta));f:close();print('Authored five actual barrel-roll reels and aligned dialogue glyph banks')
