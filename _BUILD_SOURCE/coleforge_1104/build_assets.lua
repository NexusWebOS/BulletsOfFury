local cfgpath=app.params.config or 'C:/Users/Mike/Documents/New project/BOF-Space-Arsenal-FX-1104/build-config.json'
local f=assert(io.open(cfgpath,'r'));local cfg=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor;local cache={}
local function image(path)if not cache[path]then cache[path]=Image{fromFile=path}end return cache[path]end
local function crop(src,r)local o=Image(r[3],r[4],ColorMode.RGB);o:drawImage(src,Point(-r[1],-r[2]));return o end
local function limit(n)return math.max(0,math.min(255,math.floor(n+.5)))end
local function tint(src,palette,pulse,dither,smoke)
 local out=Image(src);local w,h=src.width,src.height
 for it in out:pixels()do local p=it();local a=pc.rgbaA(p)
  if a>0 then
   local r,g,b=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
   if palette=='white'then r,g,b=255,255,255
   elseif palette=='blue'then local v=math.max(r,g,b);local white=math.min(r,g,b)/255;r=v*(.15+.65*white);g=v*(.66+.30*white);b=v
   elseif palette=='cole' then
    local v=.2126*r+.7152*g+.0722*b
    if r>g*1.08 and r>b*1.14 then
     local white=math.max(0,(math.min(r,g,b)-130)/125)
     r=v*(.30+.70*white);g=math.min(255,v*1.44);b=v*(.22+.78*white)
    elseif math.max(r,g,b)-math.min(r,g,b)<50 then r,g,b=v*.90,v,v*.91 end
   end
   if palette=='cole' then
    local v=.2126*pc.rgbaR(p)+.7152*pc.rgbaG(p)+.0722*pc.rgbaB(p)
    local m=math.max(v<100 and .80 or 0,smoke or 0)
    if v>190 then m=m*.30 end
    r=r*(1-m)+v*.86*m;g=g*(1-m)+v*.92*m;b=b*(1-m)+v*.86*m
   end
   if pulse and pulse~=0 then local k=1+pulse;r=r*k;g=g*k;b=b*k end
   if dither then
    local dx=(it.x-w/2)/(w*.40);local dy=(it.y-h/2)/(h*.40)
    if dx*dx+dy*dy<.60*.60 and (it.x%2+2*(it.y%2))~=0 then a=0 end
   end
   it(pc.rgba(limit(r),limit(g),limit(b),a))
  end
 end return out
end
local function pose(src,cw,ch,cropRect,height,angle,pulse,glow)
 local c=crop(src,cropRect);c=tint(c,'none',pulse,false)
 local scale=height/c.height;local out=Image(cw,ch,ColorMode.RGB);local co,si=math.cos(angle),math.sin(angle)
 for y=0,ch-1 do for x=0,cw-1 do
  local dx=x+.5-cw/2;local dy=y+.5-ch/2
  local sx=math.floor((dx*co+dy*si)/scale+c.width/2);local sy=math.floor((-dx*si+dy*co)/scale+c.height/2)
  if sx>=0 and sx<c.width and sy>=0 and sy<c.height then local p=c:getPixel(sx,sy);if pc.rgbaA(p)>0 then out:drawPixel(x,y,p)end end
 end end
 if glow then
  local base=Image(out)
  for y=1,ch-2 do for x=1,cw-2 do
   if pc.rgbaA(base:getPixel(x,y))==0 then
    local hit=false
    for dy=-1,1 do for dx=-1,1 do if math.abs(dx)+math.abs(dy)==1 and pc.rgbaA(base:getPixel(x+dx,y+dy))>0 then hit=true end end end
    if hit then local q=1+(pulse or 0);out:drawPixel(x,y,pc.rgba(limit(14*q),limit(85*q),limit(132*q),255))end
   end
  end end
 end
 return out
end
local atlas=image(cfg.atlas);local mf=assert(io.open(cfg.atlasMeta,'r'));local meta=json.decode(mf:read('*a'));mf:close()
local function icon(j)
 local r=assert(meta.frames['laser_icon_'..math.floor(j.level)],'Missing icon tier '..tostring(j.level));local c=crop(atlas,{r.x,r.y,r.w,r.h});local out=Image(112,112,ColorMode.RGB);out:drawImage(c,Point(math.floor((112-r.w)/2),0))
 local design=image(assert(cfg.iconSources[j.icon],'Generated icon design required: '..j.icon))
 -- Preserve the existing frame and Roman tier plaque exactly. Only the inner
 -- weapon panel is replaced, using the genuinely new generated designs.
 local poly={{46,12},{66,12},{96,33},{96,78},{74,91},{38,91},{16,78},{16,33}}
 local function pane(x,y)
  if y>=85 and x>=34 and x<=78 then return false end
  for n=1,#poly do local a=poly[n];local b=poly[n%#poly+1];if (b[1]-a[1])*(y-a[2])-(b[2]-a[2])*(x-a[1])<0 then return false end end
  return true
 end
 for y=0,111 do for x=0,111 do if pane(x+.5,y+.5)then
  local p=design:getPixel(x,y);out:drawPixel(x,y,pc.rgba(pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p),255))
 end end end
 if j.palette=='white'then out=tint(out,'white',0,false)end
 out:resize(j.cw,j.ch);return out
end
local ok,err=xpcall(function()
for _,j in ipairs(cfg.jobs)do
 local progress=assert(io.open(cfgpath..'.progress','w'));progress:write(j.id);progress:close()
 local sprite=Sprite(j.cw,j.ch,ColorMode.RGB);sprite.layers[1].name='Authored pixels'
 local rows=math.ceil(#j.files/j.cols);local sheet=Image(j.cw*j.cols,j.ch*rows,ColorMode.RGB)
 for i,path in ipairs(j.files)do
  local out
  if j.icon then out=icon(j)
  elseif j.projectile then
   local d=(i-1)%(j.dirs or 1)+1;local step=math.floor((i-1)/(j.dirs or 1))+1
   out=pose(image(path),j.cw,j.ch,j.crop,j.bodyHeight,j.angles[d],j.pulses[step],j.glow)
  else
   out=tint(image(path),j.palette or'none',j.pulses and j.pulses[i]or 0,j.dither,j.palette=='cole'and math.min(1,math.max(0,(i-10)/12))or 0)
   out:resize(j.cw,j.ch)
   if j.fadeStart and j.fadeStart>0 and i>j.fadeStart then
    local step=i-j.fadeStart
    for it in out:pixels()do local p=it();if pc.rgbaA(p)>0 and ((it.x*3+it.y*5)%7)<math.ceil(step*7/6) then it(0)end end
   end
  end
  if i>1 then sprite:newEmptyFrame(i)end
  sprite:newCel(sprite.layers[1],i,out,Point(0,0));sprite.frames[i].duration=(j.durations[i]or 67)/1000
  sheet:drawImage(out,Point(((i-1)%j.cols)*j.cw,math.floor((i-1)/j.cols)*j.ch))
 end
 sheet:saveAs(j.out);sprite:saveAs(j.source);sprite:close();collectgarbage('collect')
end
end,debug.traceback)
if not ok then local f=assert(io.open(cfgpath..'.error','w'));f:write(tostring(err));f:close();error(err)end
local f=assert(io.open(cfgpath..'.done','w'));f:write(tostring(#cfg.jobs));f:close()
