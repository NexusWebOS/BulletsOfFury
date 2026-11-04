local root='C:/Users/Mike/Documents/New project/BOF-StageX-Pickups-1104/'
local pc=app.pixelColor
local function clean(path)
 local source=Image{fromFile=root..path};local im=Image(444,444,ColorMode.RGB);im:drawImage(source,Point(0,0))
 -- Flood only the exterior matte, preserving enclosed ivory glyphs.
 local visited={};local qx,qy={},{};local tail=0;local head=1
 local function candidate(x,y)local p=im:getPixel(x,y);local r,g,b,a=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p),pc.rgbaA(p);return a<195 or (math.min(r,g,b)>150 and math.max(r,g,b)-math.min(r,g,b)<42)end
 local function push(x,y)local k=y*444+x;if x>=0 and x<444 and y>=0 and y<444 and not visited[k]and candidate(x,y)then visited[k]=true;tail=tail+1;qx[tail]=x;qy[tail]=y end end
 for i=0,443 do push(i,0);push(i,443);push(0,i);push(443,i)end
 while head<=tail do local x,y=qx[head],qy[head];head=head+1;push(x-1,y);push(x+1,y);push(x,y-1);push(x,y+1)end
 local minx,miny,maxx,maxy=444,444,0,0
 for it in im:pixels()do local p=it();if visited[it.y*444+it.x]or pc.rgbaA(p)<195 then it(0)else it(pc.rgba(pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p),255));minx=math.min(minx,it.x);miny=math.min(miny,it.y);maxx=math.max(maxx,it.x);maxy=math.max(maxy,it.y)end end
 local w,h=maxx-minx+1,maxy-miny+1;assert(w>100 and h>80,'Malformed cutout');local out=Image(w,h,ColorMode.RGB);out:drawImage(im,Point(-minx,-miny));out:saveAs(root..path:gsub('-generated.png','-cutout.png'));return out
end
local pulse={-.14,0,.12,.24,.12,0,-.08,-.14}
for _,name in ipairs({'power','speed'})do
 local base=clean(name..'-generated.png')
 for _,size in ipairs(name=='power'and{64}or{64,36})do
  local height,width
  if name=='power'then height=56;width=math.floor(base.width*height/base.height/2+.5)*2 else width=size==64 and 56 or 34;height=math.floor(base.height*width/base.width/2+.5)*2 end
  local body=Image(base);body:resize(width,height);local sprite=Sprite(size,size,ColorMode.RGB);sprite.layers[1].name='Stage X '..name..' / locked canonical shell'
  local sheet=Image(size*9,size,ColorMode.RGB)
  for i=1,9 do
   local cell=Image(size,size,ColorMode.RGB);cell:drawImage(body,Point(math.floor((size-width)/2),math.floor((size-height)/2)))
   for it in cell:pixels()do local p=it();if pc.rgbaA(p)>0 then local r,g,b=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
    if i==9 then it(pc.rgba(255,255,255,255))elseif b>r*1.6 and b>g*1.15 and b>90 then local k=1+pulse[i];it(pc.rgba(math.min(255,math.floor(r*k+.5)),math.min(255,math.floor(g*k+.5)),math.min(255,math.floor(b*k+.5)),255))end
   end end
   if i>1 then sprite:newEmptyFrame(i)end;sprite:newCel(sprite.layers[1],i,cell,Point(0,0));sprite.frames[i].duration=.10;sheet:drawImage(cell,Point((i-1)*size,0))
  end
  local out=name..'_'..size;sheet:saveAs(root..out..'.png');sprite:saveAs(root..out..'.aseprite');sprite:close()
 end
end
local f=assert(io.open(root..'build.done','w'));f:write('3 banks / 27 cells');f:close()
