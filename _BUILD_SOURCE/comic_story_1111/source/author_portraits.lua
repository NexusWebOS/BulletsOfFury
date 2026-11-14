local file=io.open(app.params.jobs,'r');local jobs=json.decode(file:read('*a'));file:close();local report={}
local function mask(j,x,y)local m=j.mouth;return ((x-m[1])/m[3])^2+((y-m[2])/m[4])^2<=1 end
for _,j in ipairs(jobs)do
 local native=Image{fromFile=j.native};local palette={};local found={}
 for px in native:pixels()do local c=px();if app.pixelColor.rgbaA(c)>0 and not found[c]then found[c]=true;table.insert(palette,c)end end
 for _,rgb in ipairs({{22,10,17},{242,231,207},{178,75,85}})do table.insert(palette,app.pixelColor.rgba(rgb[1],rgb[2],rgb[3],255))end
 local function closest(c)
  local best,dist=nil,math.huge;local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c)
  for _,p in ipairs(palette)do local d=(r-app.pixelColor.rgbaR(p))^2+(g-app.pixelColor.rgbaG(p))^2+(b-app.pixelColor.rgbaB(p))^2;if d<dist then best,dist=p,d end end
  return best
 end
 local clean,raw={},{},{}
 for i,path in ipairs(j.poses)do
  local original=Image{fromFile=path};table.insert(raw,original);local image=Image(native)
  if i>1 then for px in image:pixels()do if mask(j,px.x,px.y)and app.pixelColor.rgbaA(native:getPixel(px.x,px.y))>0 then px(closest(original:getPixel(px.x,px.y)))end end end
  -- Keep Maverick's teal uniform palette out of teeth and the oral cavity.
  -- This tiny fixed mouth region excludes the beard, headset, glasses and collar.
  if j.pilot=='maverick' and i>1 then
   for y=69,81 do for x=59,78 do
    local c=image:getPixel(x,y);local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c)
    if g>r*1.35 and b>r*1.2 and g>60 then
     image:putPixel(x,y,g>=180 and app.pixelColor.rgba(242,231,207,255) or app.pixelColor.rgba(96,56,48,255))
    end
   end end
  end
  table.insert(clean,image);image:saveAs(j.output..'/'..(i-1)..'.png')
 end
 local sprite=Sprite(128,128,ColorMode.RGB)
 for i,im in ipairs(clean)do local frame=i==1 and sprite.frames[1]or sprite:newEmptyFrame(i);sprite:newCel(sprite.layers[1],i,im,Point(0,0));frame.duration=i==1 and .25 or .09 end
 local tag=sprite:newTag(1,7);tag.name='closed-a-e-o-u-f-l';sprite:saveAs(j.aseprite);sprite:close()
 local demo=Sprite(128,128,ColorMode.RGB)
 for i,info in ipairs(j.demo)do
  local source=Image{fromFile=info.path};local best,bestD=1,math.huge
  for k,pose in ipairs(raw)do
   local total=0
   for y=0,127 do for x=0,127 do if mask(j,x,y)then local a,b=source:getPixel(x,y),pose:getPixel(x,y);total=total+(app.pixelColor.rgbaR(a)-app.pixelColor.rgbaR(b))^2+(app.pixelColor.rgbaG(a)-app.pixelColor.rgbaG(b))^2+(app.pixelColor.rgbaB(a)-app.pixelColor.rgbaB(b))^2 end end end
   if total<bestD then best,bestD=k,total end
  end
  if i==#j.demo then best=1 end
  local f=i==1 and demo.frames[1]or demo:newEmptyFrame(i);demo:newCel(demo.layers[1],i,clean[best],Point(0,0));f.duration=info.ms/1000
 end
 demo:saveCopyAs(j.gif);demo:saveAs(j.output..'/talking.aseprite');demo:close()
 local loaded=app.open(j.aseprite);local different=0
 for i=1,7 do local im=Image(128,128,ColorMode.RGB);local c=loaded.layers[1]:cel(i);if c then im:drawImage(c.image,c.position)end;if not im:isEqual(clean[i])then different=different+1 end end
 loaded:close();table.insert(report,{pilot=j.pilot,frames=7,different=different});collectgarbage('collect')
end
local out=io.open(app.params.report,'w');out:write(json.encode(report));out:close()
