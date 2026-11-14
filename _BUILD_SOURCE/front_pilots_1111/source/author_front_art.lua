local f=io.open(app.params.jobs,'r');local jobs=json.decode(f:read('*a'));f:close();local report={}
if app.params.previewOnly~='1'then for _,j in ipairs(jobs)do
 local sheet=Image{fromFile=j.input};local sprite=Sprite(j.w,j.h,ColorMode.RGB);local exact=true
 for i=1,j.frames do
  local x=((i-1)%j.cols)*j.w;local y=math.floor((i-1)/j.cols)*j.h;local image=Image(sheet,Rectangle(x,y,j.w,j.h))
  local frame=i==1 and sprite.frames[1]or sprite:newEmptyFrame(i);sprite:newCel(sprite.layers[1],i,image,Point(0,0));frame.duration=.1
 end
 if j.frames==49 then for z=0,6 do sprite:newTag(z*7+1,z*7+7).name='zoom-'..z end end
 sprite:saveAs(j.output);sprite:close();local loaded=app.open(j.output)
 for i=1,j.frames do
  local expected=Image(sheet,Rectangle(((i-1)%j.cols)*j.w,math.floor((i-1)/j.cols)*j.h,j.w,j.h));local got=Image(j.w,j.h,ColorMode.RGB);local c=loaded.layers[1]:cel(i);if c then got:drawImage(c.image,c.position)end
  if not got:isEqual(expected)then exact=false end
 end
 loaded:close();table.insert(report,{name=j.name,frames=j.frames,exact=exact});collectgarbage('collect')
end end
local pilots={'cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut'}
local defaults={cole='conference',axel='hangar',freezer='hangar',yuri='conference',maverick='hangar',falva='hangar',lizzie='hangar',decker='workshop',juggernaut='lounge'}
for _,pk in ipairs(pilots)do
 local source=app.open(app.params.portraits..'/'..pk..'/talking.aseprite');local bg=Image{fromFile=app.params.masters..'/background-'..defaults[pk]..'.png'};local composite=Sprite(512,340,ColorMode.RGB)
 for i,frame in ipairs(source.frames)do
  local image=Image(bg);local c=source.layers[1]:cel(i);if c then image:drawImage(c.image,Point(96+c.position.x,22+c.position.y))end
  local f=i==1 and composite.frames[1]or composite:newEmptyFrame(i);composite:newCel(composite.layers[1],i,image,Point(0,0));f.duration=frame.duration
 end
 composite:saveAs(app.params.portraits..'/framed/'..pk..'.aseprite')
 local palette=Palette(256);palette:setColor(0,Color{r=0,g=0,b=0,a=0});local seen={};local n=1
 local images={bg};for k=0,6 do table.insert(images,Image{fromFile=app.params.portraits..'/'..pk..'/'..k..'.png'})end
 for _,im in ipairs(images)do for px in im:pixels()do local c=px();if app.pixelColor.rgbaA(c)>0 and not seen[c]then
  assert(n<256,'Shared preview GIF palette overflow');seen[c]=true;palette:setColor(n,Color{r=app.pixelColor.rgbaR(c),g=app.pixelColor.rgbaG(c),b=app.pixelColor.rgbaB(c),a=255});n=n+1
 end end end
 composite:setPalette(palette);app.activeSprite=composite;app.command.ChangePixelFormat{format='indexed',dithering='none'}
 composite:saveCopyAs(app.params.portraits..'/framed/'..pk..'-front-talking.gif');composite:close();source:close()
end
local out=io.open(app.params.report,'w');out:write(json.encode(report));out:close()
