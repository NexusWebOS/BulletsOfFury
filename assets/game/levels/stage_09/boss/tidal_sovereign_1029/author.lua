local R=app.params.root;local D=app.params.out;local pc=app.pixelColor;local tau=math.pi*2;local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(math.max(0,math.min(255,r))),math.floor(math.max(0,math.min(255,g))),math.floor(math.max(0,math.min(255,b))),math.floor(math.max(0,math.min(255,a))))end
local function bank(name,frames,pivot,cols)
 local w,h=frames[1].width,frames[1].height;cols=cols or 8;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/16 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='ts58_'..name,path='assets/game/levels/stage_09/boss/tidal_sovereign_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot}
end
local function crop(row)local c=row.cell;local im=Image{fromFile=R..'/'..row.path};return Image(im,Rectangle(c[2],c[3],c[4],c[5]))end
local function aqua(v)local r,g,b,a=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v);local m=math.max(r,g,b);return rgba(m*.22+g*.1,m*.82,m,a)end
local function white(src)local out=Image(src.width,src.height,ColorMode.RGB);for p in src:pixels()do if pc.rgbaA(p())>0 then out:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(p())))end end;return out end
local function poly(x,y,p)local inside=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if (a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then inside=not inside end;j=i end;return inside end
local wing={{23,76},{41,80},{61,82},{69,110},{58,108},{40,98},{29,86}};local reservoirs={{160,119,32,31},{96,87,17,17},{224,87,17,17},{160,52,10,19},{122,182,6,10},{198,182,6,10},{160,218,8,18}}
local function liquid(x,y,v)
 local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);if not(b>r*1.3+12 and g>r*1.15+10 and b>85 and pc.rgbaA(v)>0)then return nil end
 for _,s in ipairs(reservoirs)do if ((x-s[1])/s[3])^2+((y-s[2])/s[4])^2<1 then return s end end
 if poly(x,y,wing)then return{46,91,25,19}end;if poly(320-x,y,wing)then return{274,91,25,19}end
end
local water=Image{fromFile=R..'/'..C.water.path};local function tex(frame,x,y)local c=C.water.cells[frame%#C.water.cells+1];return water:getPixel(c[1]+((x+frame*3)%c[3]),c[2]+((y+frame*5)%c[4]))end
local body
for _,state in ipairs({'intact','damaged','critical'})do local src=crop(C['ns9_tidal_'..state]);if state=='intact'then body=src;bank('body_hit',{white(src)},{160,128},1)end;local frames={}
 for level=0,3 do for phase=0,15 do local out=Image(src)
  for p in src:pixels()do local v=p();local fan=nil;for _,cx in ipairs({96,224})do if (p.x-cx)^2+(p.y-87)^2<15^2 then fan=cx end end
   if fan then local a=(fan==96 and 1 or -1)*phase*tau/16;local dx,dy=p.x-fan,p.y-87;v=src:getPixel(math.floor(fan+dx*math.cos(a)+dy*math.sin(a)+.5),math.floor(87-dx*math.sin(a)+dy*math.cos(a)+.5));out:drawPixel(p.x,p.y,v)end
   local s=liquid(p.x,p.y,v);if s then local a=phase*tau/16;local dx,dy=p.x-s[1],p.y-s[2];local xx=math.floor(s[1]+dx*math.cos(a)-dy*math.sin(a));local yy=math.floor(s[2]+dx*math.sin(a)+dy*math.cos(a));local w=tex(phase,xx,yy);local filled=(dy/s[4])>1-level*2/3;local k=fan and .08 or(filled and .6 or .25);local boost=filled and 22+level*12 or 0
   out:drawPixel(p.x,p.y,rgba(pc.rgbaR(v)*(1-k)+pc.rgbaR(w)*k+boost,pc.rgbaG(v)*(1-k)+pc.rgbaG(w)*k+boost,pc.rgbaB(v)*(1-k)+pc.rgbaB(w)*k+boost,pc.rgbaA(v)))end end
  table.insert(frames,out)
 end end;bank('body_'..state,frames,{160,128})
end
local outer={};for phase=0,7 do local out=Image(352,288,ColorMode.RGB);local strength=.35+.65*math.sin(phase*tau/8)^2
 for p in body:pixels()do if pc.rgbaA(p())>64 then for _,d in ipairs({{-4,0},{4,0},{0,-4},{0,4},{-2,-2},{2,2},{2,-2},{-2,2}})do out:drawPixel(p.x+16+d[1],p.y+16+d[2],rgba(45,225,255,60+strength*150))end end end
 for p in body:pixels()do if pc.rgbaA(p())>0 then out:drawPixel(p.x+16,p.y+16,rgba(0,0,0,0))end end;table.insert(outer,out)
end;bank('outer',outer,{176,144})
local function rotated(src,size,a,scale,alpha)
 local out=Image(size,size,ColorMode.RGB);local co,si=math.cos(a),math.sin(a);local cx,cy=src.width/2,src.height/2
 for y=0,size-1 do for x=0,size-1 do local dx,dy=(x-size/2)/scale,(y-size/2)/scale;local xx=math.floor(dx*co+dy*si+cx);local yy=math.floor(-dx*si+dy*co+cy);if xx>=0 and yy>=0 and xx<src.width and yy<src.height then local v=src:getPixel(xx,yy);if pc.rgbaA(v)>0 then out:drawPixel(x,y,rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v)*alpha))end end end end;return out
end
local roller=Image{fromFile=D..'/bubble_1.png'};local lamp=Image{fromFile=D..'/bubble_2.png'};local sizes={28,40,56,72,96,120};local bubbles={};for _,size in ipairs(sizes)do for phase=0,15 do table.insert(bubbles,rotated(lamp,144,phase*tau/16,size/96,1))end end;bank('bubble',bubbles,{72,72})
for _,row in ipairs({{'roller',96,72},{'bomb',56,40},{'slug',32,20}})do local frames={};for phase=0,15 do table.insert(frames,rotated(roller,row[2],phase*tau/16,row[3]/96,1))end;bank(row[1],frames,{row[2]/2,row[2]/2})end
local muzzle={};for phase=0,15 do local u=phase/15;table.insert(muzzle,rotated(roller,96,phase*tau/16,(.28+math.sin(u*math.pi)*.40),1-u*.75))end;bank('muzzle',muzzle,{48,48})
local geysers={};for phase=0,15 do local src=Image{fromFile=D..'/geyser/'..string.format('%02d',phase+1)..'.png'};local out=Image(160,288,ColorMode.RGB);out:drawImage(src,Point(16,12));table.insert(geysers,out)end;bank('geyser',geysers,{80,268})
local jets,rains,forward,muzzles,fanmuzzles,charges,bursts={},{},{},{},{},{},{}
local function flipv(im)local out=Image(im.width,im.height,ColorMode.RGB);for y=0,im.height-1 do for x=0,im.width-1 do out:drawPixel(x,im.height-1-y,im:getPixel(x,y))end end;return out end
for phase=0,15 do local raw=Image{fromFile=D..'/geyser/'..string.format('%02d',phase%8+1)..'.png'};local jet=Image(raw);jet:resize(48,128);local out=Image(80,176,ColorMode.RGB);out:drawImage(jet,Point(16,16));table.insert(jets,out);if phase%2==0 then local down=Image(80,176,ColorMode.RGB);down:drawImage(flipv(jet),Point(16,16));table.insert(rains,down)end
 local plume=Image(raw);plume:resize(28,56);local muzzle=Image(64,96,ColorMode.RGB);muzzle:drawImage(flipv(plume),Point(18,20));table.insert(muzzles,muzzle)
 local up=Image(raw);up:resize(40,80);local fm=Image(80,112,ColorMode.RGB);fm:drawImage(up,Point(20,16));table.insert(fanmuzzles,fm)
 table.insert(charges,rotated(roller,96,phase*tau/16,.18+phase/15*.57,1))
 local burst=Image(160,160,ColorMode.RGB);local u=phase/16;local foam=Image(raw,Rectangle(0,140,128,116));foam:resize(math.floor(80+u*58),math.floor(56+u*38));local faded=Image(foam.width,foam.height,ColorMode.RGB)
 for p in foam:pixels()do local v=p();local k=math.max(.06,1-u);faded:drawPixel(p.x,p.y,rgba(pc.rgbaR(v)+(phase<3 and 75 or 0),pc.rgbaG(v)+(phase<3 and 40 or 0),pc.rgbaB(v),pc.rgbaA(v)*k))end
 burst:drawImage(faded,Point(math.floor(80-faded.width/2),math.floor(80-faded.height/2)))
 for i=0,7 do local a=i*tau/8;local drop=rotated(roller,24,a,.12+.08*(1-u),math.max(.06,1-u));burst:drawImage(drop,Point(math.floor(68+math.cos(a)*(8+u*53)),math.floor(68+math.sin(a)*(8+u*53))))end;table.insert(bursts,burst)
end
for direction=0,4 do for phase=0,15 do local slug=Image{fromFile=D..'/water_bullet_master.png'};slug:resize(16,32);local glow=math.sin(phase*tau/16)*12+phase%4
 for p in slug:pixels()do local v=p();local r,g,b,a=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v);if a>0 and r<b*.75 then p(rgba(r+glow*.3,g+glow,b+glow*.5,a))end end
 local centred=Image(48,48,ColorMode.RGB);centred:drawImage(slug,Point(16,8));table.insert(forward,rotated(centred,64,(direction-2)*.12,1,1))end end
bank('jet',jets,{40,144});bank('rain',rains,{40,144});bank('forward_slug',forward,{32,32},16);bank('forward_muzzle',muzzles,{32,20});bank('fan_muzzle',fanmuzzles,{40,96});bank('grenade_charge',charges,{48,48});bank('grenade_burst',bursts,{80,80})
local function watercolor(v)
 local a=pc.rgbaA(v);local l=(pc.rgbaR(v)*.2126+pc.rgbaG(v)*.7152+pc.rgbaB(v)*.0722)/255
 local colors={{0,12,38},{0,55,140},{0,145,220},{80,224,255},{240,255,255}};local u=l*4;local i=math.min(4,math.floor(u)+1);local k=u-(i-1);local c,d=colors[i],colors[i+1];return rgba(c[1]+(d[1]-c[1])*k,c[2]+(d[2]-c[2])*k,c[3]+(d[3]-c[3])*k,a)
end
local waves,falls={},{ };for _,size in ipairs({190,242,294,346,398,452})do for phase=0,7 do local raw=crop(C.stage2Waves[phase+1]);local src=Image(raw.width,raw.height,ColorMode.RGB)
 for y=0,raw.height-1 do for x=0,raw.width-1 do src:drawPixel(x,raw.height-1-y,watercolor(raw:getPixel(x,y)))end end
 local h=math.floor(src.height*size/src.width+.5);src:resize(size,h);local out=Image(480,480,ColorMode.RGB);out:drawImage(src,Point(math.floor((480-size)/2),math.floor((480-h)/2)));table.insert(waves,out)
 if size==190 then src:resize(108,108);local fall=Image(128,128,ColorMode.RGB);fall:drawImage(src,Point(10,10));table.insert(falls,fall)end
end end;bank('wave',waves,{240,240});bank('fall_wave',falls,{64,64})
local trails,arrows={},{ };for phase=0,15 do local out=Image(112,160,ColorMode.RGB);for y=8,151 do for x=8,103 do local dx,dy=(x-56)/46,(y-80)/72;if dx*dx+dy*dy<1 then local v=tex(phase,x,y);out:drawPixel(x,y,rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),180))end end end;table.insert(trails,out)
 if phase%2==0 then local a=Image(48,64,ColorMode.RGB);for y=8,55 do for x=8,39 do if (y<36 and x>=19 and x<=28)or(y>=30 and y<54 and math.abs(x-24)<(54-y)*.7)then local v=tex(phase,x,y);a:drawPixel(x,y,rgba(100+pc.rgbaR(v),150+pc.rgbaG(v),255,255))end end end;table.insert(arrows,a)end
end;bank('trail',trails,{56,80});bank('arrow',arrows,{24,32})
local sentinel=crop(C.ns9_warpsen_intact);sentinel:resize(188,142);local hit=Image(208,176,ColorMode.RGB);hit:drawImage(white(sentinel),Point(10,17));bank('sentinel_hit',{hit},{104,88},1)
for _,variant in ipairs({'alpha','beta'})do local frames={};for phase=0,15 do local src=Image(sentinel);local k=.5+.5*math.sin(phase*tau/16)^2
 for p in src:pixels()do local v=p();local r,g,b,al=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v);if al>0 and b>r*1.15 and b>g*1.25 and b>80 then if variant=='alpha'then p(rgba(r*.55,g+35*k,b+35*k,al))else p(rgba(r+20*k,g,b+25*k,al))end end end
 local out=Image(208,176,ColorMode.RGB);out:drawImage(src,Point(10,17));table.insert(frames,out)
end;bank('sentinel_'..variant,frames,{104,88})end
local signs={};for _,file in ipairs({'wall_yield_master.png','wall_alert_master.png'})do
 local im=Image{fromFile=D..'/'..file};local h=52;local w=math.floor(im.width*h/im.height+.5);im:resize(w,h);
 local out=Image(64,64,ColorMode.RGB);out:drawImage(im,Point(math.floor((64-w)/2),6));table.insert(signs,out)
end;bank('wall_warning',signs,{32,32},2)
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('TS58 banks exported')
