local f=io.open(app.params.jobs,'r');local jobs=json.decode(f:read('*a'));f:close();local report={}
local function gifPalette(sprite,images)
 local palette=Palette(256);palette:setColor(0,Color{r=0,g=0,b=0,a=0});local seen={};local n=1
 for _,image in ipairs(images)do for px in image:pixels()do local c=px();if app.pixelColor.rgbaA(c)>0 and not seen[c]then
  assert(n<256,'Shared GIF palette overflow');seen[c]=true;palette:setColor(n,Color{r=app.pixelColor.rgbaR(c),g=app.pixelColor.rgbaG(c),b=app.pixelColor.rgbaB(c),a=255});n=n+1
 end end end
 sprite:setPalette(palette);app.activeSprite=sprite;app.command.ChangePixelFormat{format='indexed',dithering='none'}
end
for _,j in ipairs(jobs)do
 local native=Image{fromFile=j.native};local m=j.mouth;local palette={};local seen={}
 for y=j.minY,j.maxY+6 do for x=m[1]-34,m[1]+34 do local c=native:getPixel(x,y);if app.pixelColor.rgbaA(c)>0 and not seen[c]then seen[c]=true;table.insert(palette,c)end end end
 for _,p in ipairs({{22,10,17},{242,231,207},{178,75,85}})do table.insert(palette,app.pixelColor.rgba(p[1],p[2],p[3],255))end
 local cache={};local function quant(c)
  if cache[c]then return cache[c]end;local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c)
  if j.pilot=='maverick'and g>r*1.35 and b>r*1.2 and g>60 then return g>=145 and app.pixelColor.rgba(242,231,207,255)or app.pixelColor.rgba(22,10,17,255)end
  local best,dist=nil,math.huge
  for _,p in ipairs(palette)do local d=(r-app.pixelColor.rgbaR(p))^2+(g-app.pixelColor.rgbaG(p))^2+(b-app.pixelColor.rgbaB(p))^2;if d<dist then best,dist=p,d end end
  cache[c]=best;return best
 end
 local clean={}
 for i,path in ipairs(j.poses)do
  local image=Image(native);local raw=Image{fromFile=path}
  if i>1 then for y=j.minY,j.maxY do for x=m[1]-m[3],m[1]+m[3]do
   if ((x-m[1])/m[3])^2+((y-m[2])/m[4])^2<=1 and app.pixelColor.rgbaA(native:getPixel(x,y))>0 then
    local c=raw:getPixel(x-j.offset[1],y-j.offset[2]);if app.pixelColor.rgbaA(c)>0 then image:putPixel(x,y,quant(c))end
   end
  end end end
  image:saveAs(j.output..'/'..(i-1)..'.png');table.insert(clean,image)
 end
 local sprite=Sprite(320,320,ColorMode.RGB)
 for i,im in ipairs(clean)do local frame=i==1 and sprite.frames[1]or sprite:newEmptyFrame(i);sprite:newCel(sprite.layers[1],i,im,Point(0,0));frame.duration=i==1 and .25 or .08 end
 sprite:newTag(1,7).name='closed-a-e-o-u-f-l';sprite:saveAs(j.aseprite);sprite:close()
 local demo=Sprite(320,320,ColorMode.RGB)
 for i,step in ipairs(j.plan)do local frame=i==1 and demo.frames[1]or demo:newEmptyFrame(i);demo:newCel(demo.layers[1],i,clean[step.pose+1],Point(0,0));frame.duration=step.ms/1000 end
 demo:saveAs(j.output..'/talking.aseprite');gifPalette(demo,clean);demo:saveCopyAs(j.gif);demo:close()
 local check=app.open(j.aseprite);local exact=true
 for i,im in ipairs(clean)do local out=Image(320,320,ColorMode.RGB);local c=check.layers[1]:cel(i);if c then out:drawImage(c.image,c.position)end;if not out:isEqual(im)then exact=false end end
 check:close();table.insert(report,{pilot=j.pilot,frames=7,exact=exact});collectgarbage('collect')
end
local out=io.open(app.params.report,'w');out:write(json.encode(report));out:close()
