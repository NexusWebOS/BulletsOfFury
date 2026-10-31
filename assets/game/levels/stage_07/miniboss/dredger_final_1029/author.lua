local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2;local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(math.min(255,r)),math.floor(math.min(255,g)),math.floor(math.min(255,b)),math.floor(a))end
local function cell(a,i)local s=Image{fromFile=R..'/'..a.path};return Image(s,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch))end
local function register(name,frames,pivot,cols)
 local w,h=frames[1].width,frames[1].height;cols=cols or 4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='df55_'..name,path='assets/game/levels/stage_07/miniboss/dredger_final_1029/'..name..'.png',cw=w,ch=h,pivot=pivot,cols=cols,frames=#frames}
end
local function emit(im,amount,magma)
 local out=Image(im.width,im.height,ColorMode.RGB)
 for p in im:pixels()do local v=p();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v)
  if magma and g>r*1.15 then r=math.min(255,g*1.7);g=g*.28;b=b*.12 end
  if not magma and g>r*1.1 and g>b*1.15 then r=r+amount*90;g=g+amount*100;b=b+amount*30 end
  out:drawPixel(p.x,p.y,rgba(r,g,b,a))end end
 for p in im:pixels()do local v=p();if pc.rgbaA(v)>64 and pc.rgbaG(v)>pc.rgbaR(v)*1.1 then
  for _,d in ipairs({{-2,0},{2,0},{0,-2},{0,2}})do local x,y=p.x+d[1],p.y+d[2];if x>=0 and y>=0 and x<im.width and y<im.height and pc.rgbaA(out:getPixel(x,y))==0 then out:drawPixel(x,y,magma and rgba(255,65,8,50+100*amount)or rgba(100,255,12,50+100*amount))end end
 end end;return out
end
local tops,hot={},{ };for i=0,15 do local im=Image(92,84,ColorMode.RGB);im:drawImage(cell(C.dc.top,0),Point(8,8));table.insert(tops,emit(im,.2+.8*math.sin(i*tau/16)^2,false));table.insert(hot,emit(im,.3+.7*math.sin(i*tau/16)^2,true))end
register('top_green',tops,{46,42});register('top_magma',hot,{46,42})
local charged={};for track=0,7 do local src=cell(C.dc.body,track);for phase=0,15 do local out=Image(192,208,ColorMode.RGB);local p=.2+.8*math.sin(phase*tau/16)^2
 for y=0,src.height-1 do for x=0,src.width-1 do local v=src:getPixel(x,y);if pc.rgbaA(v)>0 then
  for _,d in ipairs({{-3,0},{3,0},{0,-3},{0,3}})do out:drawPixel(x+8+d[1],y+8+d[2],rgba(155,255,12,35+p*135))end
 end end end
 for p2 in src:pixels()do local v=p2();if pc.rgbaA(v)>0 then out:drawPixel(p2.x+8,p2.y+8,rgba(pc.rgbaR(v)+p*28,pc.rgbaG(v)+p*38,pc.rgbaB(v),pc.rgbaA(v)))end end;table.insert(charged,out)
 end end;register('body_charge',charged,{96,104},8)
local spew=Image{fromFile=R..'/'..C.spew};local green,red={},{ }
for i=0,15 do local im=Image(spew,Rectangle(i%4*320,math.floor(i/4)*320,320,320));im:resize(80,80)
 local o=Image(96,120,ColorMode.RGB);o:drawImage(im,Point(8,32));table.insert(green,o);table.insert(red,emit(o,.5,true))
end;register('ooze',green,{48,102});register('magma_spew',red,{48,102})
local balls={};for i=0,15 do local im=cell(C.er.toxic_orb,i);local out=Image(40,40,ColorMode.RGB)
 for p in im:pixels()do local v=p();if pc.rgbaA(v)>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);if g>r*1.1 then r=math.min(255,g*1.3+25);g=g*.46;b=b*.10 end;out:drawPixel(p.x+2,p.y+2,rgba(r,g,b,pc.rgbaA(v)))end end;table.insert(balls,out)end;register('magma_ball',balls,{20,20})
local mark=Image{fromFile=R..'/assets/game/levels/stage_05/boss/stage5_hammer/reticle.png'}
mark=Image(mark,Rectangle(128,240,1544,530));mark:resize(80,28)
for _,color in ipairs({'green','yellow','red'})do local out=Image(96,48,ColorMode.RGB)
 for p in mark:pixels()do local c=p();if pc.rgbaA(c)>0 then local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  if color~='green'and g>r then if color=='yellow'then r=g;g=g*.83;b=b*.2 else r=g;g=g*.15;b=b*.2 end end
  out:drawPixel(p.x+8,p.y+10,rgba(r,g,b,pc.rgbaA(c)))end end;register('ground_'..color,{out},{48,24})
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('DF55 export done')
