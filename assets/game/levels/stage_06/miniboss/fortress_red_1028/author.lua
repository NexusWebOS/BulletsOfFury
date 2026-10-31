local W=assert(app.params['work'],'Pass --script-param work=<staging folder with sources/ and art/>')..'/'
local R=assert(app.params['repo'],'Pass --script-param repo=<repository root>')..'/'
local pc=app.pixelColor
local function image(path) return Image{fromFile=path} end
local function crop(src,x,y,w,h)
 local im=Image(w,h,ColorMode.RGB);im:drawImage(src,Point(-x,-y));return im
end
local function scale(src,w,h)
 local im=Image(src);im:resize(w,h);return im
end
local function red(src,pulse)
 local im=Image(src)
 for it in im:pixels() do
  local c=it();local a=pc.rgbaA(c)
  if a>0 then
   local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
   local hi,lo=math.max(r,g,b),math.min(r,g,b);local d=hi-lo
   if d>12 then
    local v=math.min(255,math.floor(hi*pulse+.5));local base=math.floor(lo*v/math.max(1,hi))
    it(pc.rgba(v,math.floor(base+(v-base)*.10),math.floor(base+(v-base)*.19),a))
   end
  end
 end
 return im
end
local function rotate(src,angle,side)
 local im=Image(side,side,ColorMode.RGB);local ca,sa=math.cos(angle),math.sin(angle)
 for y=0,side-1 do for x=0,side-1 do
  local dx,dy=x-(side-1)/2,y-(side-1)/2
  local sx=math.floor(ca*dx+sa*dy+(src.width-1)/2+.5)
  local sy=math.floor(-sa*dx+ca*dy+(src.height-1)/2+.5)
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height then im:drawPixel(x,y,src:getPixel(sx,sy)) end
 end end
 return im
end
local function bank(name,frames,cols)
 local w,h=frames[1].width,frames[1].height;local s=Sprite(w,h,ColorMode.RGB)
 local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB)
 for i,im in ipairs(frames) do
  if i>1 then s:newEmptyFrame() end
  s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=.0625
  sheet:drawImage(im,Point(((i-1)%cols)*w,math.floor((i-1)/cols)*h))
 end
 s:saveAs(W..'art/'..name..'.aseprite');sheet:saveAs(W..'art/'..name..'.png');s:close()
end
local hull=image(R..'assets/game/levels/stage_06/boss/siege_carrier_1013/hull.png')
local fan=crop(hull,64,148,128,128);local clean=Image(hull)
for _,cx in ipairs({128,896}) do for y=175,249 do for x=cx-37,cx+37 do
 if (x-cx)^2+(y-212)^2<36^2 then clean:drawPixel(x,y,pc.rgba(6,12,18,255)) end
end end end
bank('hull',{clean},1)
local fans={};local hit=Image(fan);local wreck=Image(fan)
for it in hit:pixels() do local c=it();if pc.rgbaA(c)>0 then it(pc.rgba(239,249,255,pc.rgbaA(c))) end end
for y=0,127 do for x=0,127 do
 if (x-64)^2+(y-64)^2<38^2 then
  local c=wreck:getPixel(x,y);wreck:drawPixel(x,y,pc.rgba(math.floor(pc.rgbaR(c)*.45),math.floor(pc.rgbaG(c)*.32),math.floor(pc.rgbaB(c)*.27),pc.rgbaA(c)))
 end
end end
for f=0,15 do
 local out=Image(fan);local a=f*math.pi/8;local ca,sa=math.cos(a),math.sin(a)
 for y=27,101 do for x=27,101 do
  if (x-64)^2+(y-64)^2<35^2 then
   local dx,dy=x-64,y-64;local sx=math.floor(ca*dx+sa*dy+64+.5);local sy=math.floor(-sa*dx+ca*dy+64+.5)
   out:drawPixel(x,y,fan:getPixel(sx,sy))
  end
 end end
 fans[#fans+1]=out
end
bank('fans',fans,8);bank('fan_hit',{hit},1);bank('fan_wreck',{wreck},1)
local bolts={};local src=image(R..'assets/game/levels/stage_04/stage/combat_upgrade_0901/stage4_chain_lightning_atlas.png')
for dir=0,31 do for f=0,7 do
 local im=crop(src,(f%4)*256,math.floor(f/4)*384,256,384)
 im=red(scale(im,80,120),({.86,.95,1.06,1.12})[(f%4)+1])
 bolts[#bolts+1]=rotate(im,dir*math.pi*2/32,152)
end end
bank('red_bolts',bolts,16)
local orbs={};for f=0,15 do
 orbs[#orbs+1]=red(scale(image(W..'sources/s4w_lightning_ball_'..f..'.png'),72,72),({.86,.95,1.06,1.12})[(f%4)+1])
end
bank('red_orbs',orbs,8)
local coreSrc=image(W..'sources/mr27_corefx.png');local cores={};local whites={}
for f=0,11 do
 local n=5+(f%3);local x=122+(n%4)*444;local y=n<4 and 4 or 448
 local im=red(scale(crop(coreSrc,x,y,201,434),50,108),({.86,.95,1.06,1.12})[(f%4)+1]);cores[#cores+1]=im
 local hi=Image(im);for it in hi:pixels()do local c=it();if pc.rgbaA(c)>0 then it(pc.rgba(255,245,248,pc.rgbaA(c))) end end;whites[#whites+1]=hi
end
bank('red_core',cores,6);bank('core_hit',whites,6)
local smoke,fire={},{};for f=0,7 do
 local im=Image(96,144,ColorMode.RGB);im:drawImage(scale(image(W..'sources/nsd_chim_'..f..'.png'),96,126),Point(0,0));smoke[#smoke+1]=im
 fire[#fire+1]=scale(image(W..'sources/nxp_upward_'..f..'.png'),64,64)
end
bank('fan_smoke',smoke,8);bank('fan_fire',fire,8)
print('Authored fixed-cell Fortress fan and red lightning banks')
