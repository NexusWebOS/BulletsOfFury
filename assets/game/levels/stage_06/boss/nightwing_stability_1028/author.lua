local W=assert(app.params['work'],'Pass --script-param work=<staging folder>')
if W:sub(-1)~='/' then W=W..'/' end
local S=dofile(W..'config.lua');local pc=app.pixelColor
local function crop(im,x,y,w,h)local q=Image(w,h,ColorMode.RGB);q:drawImage(im,Point(-x,-y));return q end
local function source(k,f)local a=S[k];local im=Image{fromFile=a.path};return crop(im,(f%a.cols)*a.w,math.floor(f/a.cols)*a.h,a.w,a.h) end
local function sheet(name,ff,cols)
 local w,h=ff[1].width,ff[1].height;local sp=Sprite(w,h,ColorMode.RGB);local im=Image(w*cols,h*math.ceil(#ff/cols),ColorMode.RGB)
 for i,q in ipairs(ff)do if i>1 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],i,q,Point(0,0));sp.frames[i].duration=.0625;im:drawImage(q,Point((i-1)%cols*w,math.floor((i-1)/cols)*h))end
 sp:saveAs(W..'art/'..name..'.aseprite');im:saveAs(W..'art/'..name..'.png');sp:close()
end
local function bright(im,amount,glow)
 local q=Image(im)
 for it in q:pixels()do local c=it();local r,g,b,a=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)
  if a>0 then
   if glow then
    if g>35 and g>r*1.25 and g>b*.86 then
     r=math.floor(r+(180-r)*amount);g=math.floor(g+(255-g)*amount);b=math.floor(b+(245-b)*amount)
    end
   else
    r=math.min(255,math.floor(r*1.8+100*amount));g=math.min(255,math.floor(g*1.8+85*amount));b=math.min(255,math.floor(b*1.8+85*amount));a=math.min(255,math.floor(a*1.45))
   end
   it(pc.rgba(r,g,b,a))
  end
 end
 return q
end
local glow={};for level=0,5 do for f=0,16 do glow[#glow+1]=bright(source('clean',f),level*.12,true)end end;sheet('clean_charge',glow,8)
-- The same animated PixelLab gusts, with larger fixed cells, bright mint/white
-- cores and a one-pixel dark silhouette so they read against bright clouds.
local gusts={}
for d=0,31 do for f=0,15 do
 local q=bright(source('wind_bullet',d*16+f),.68,false);q:resize(96,96)
 local out=Image(96,96,ColorMode.RGB)
 for y=1,94 do for x=1,94 do local c=q:getPixel(x,y)
  if pc.rgbaA(c)<30 then
   local edge=false;for _,a in ipairs({{-1,0},{1,0},{0,-1},{0,1}})do if pc.rgbaA(q:getPixel(x+a[1],y+a[2]))>100 then edge=true end end
   if edge then out:drawPixel(x,y,pc.rgba(4,32,40,235))end
  end
 end end
 out:drawImage(q);gusts[#gusts+1]=out
end end
sheet('wind_gust',gusts,16)
-- Three counterposed, tangent-facing curls built from the approved animated
-- wind strokes. Every orbital position and luminance step is baked offline.
local rear,front={},{};local box=S.charge_box
for f=0,23 do
 local back=Image(512,512,ColorMode.RGB);local fore=Image(512,512,ColorMode.RGB)
 for j=0,2 do
  local src=source('wind_charge',(f+j*7)%24);local q=crop(src,box[1],box[2],box[3]-box[1],box[4]-box[2]);q:resize(math.floor(q.width*1.25),math.floor(q.height*1.25));q=bright(q,.45,false)
  local a=f*math.pi*2/24+j*math.pi*2/3;local ca,sa=math.cos(a),math.sin(a);local cx=256+math.cos(a)*140;local cy=256+math.sin(a)*140
  -- Curl is tangent to the ring; inverse-map the source into one fixed canvas.
  local ang=a+math.pi/2;local co,si=math.cos(ang),math.sin(ang)
  for y=0,511 do for x=0,511 do
   local dx,dy=x-cx,y-cy;local sx=math.floor(co*dx+si*dy+q.width/2);local sy=math.floor(-si*dx+co*dy+q.height/2)
   if sx>=0 and sy>=0 and sx<q.width and sy<q.height then local c=q:getPixel(sx,sy);if pc.rgbaA(c)>0 then local dest=y<256 and back or fore;dest:drawPixel(x,y,c)end end
  end end
 end
 rear[#rear+1]=back;front[#front+1]=fore
end
sheet('wind_rear',rear,6);sheet('wind_front',front,6)
print('Authored stronger wind and six-stage own-pixel armor illumination')
