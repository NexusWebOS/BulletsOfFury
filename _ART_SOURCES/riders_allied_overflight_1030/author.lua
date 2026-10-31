local W=app.params['work'];if W:sub(-1)~='/'then W=W..'/'end
local file=io.open(W..'sources.json','r');local rows=json.decode(file:read('*a'));file:close()
local pc=app.pixelColor
local pilots={}
for _,r in ipairs(rows)do pilots[r.pilot]=pilots[r.pilot]or{};pilots[r.pilot][r.phase+1]=r.path end
local function save(name,cells)
 local sp=Sprite(128,128,ColorMode.RGB);sp.layers[1].name=name;local cols=12
 local sheet=Image(128*cols,128*math.ceil(#cells/cols),ColorMode.RGB)
 for i,im in ipairs(cells)do if i>1 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],i,im,Point(0,0));sp.frames[i].duration=.07;sheet:drawImage(im,Point((i-1)%cols*128,math.floor((i-1)/cols)*128))end
 sp:saveAs(W..name..'.aseprite');sheet:saveAs(W..name..'.png');sp:close()
end
for pilot,paths in pairs(pilots)do
 local sources={};for i=1,3 do sources[i]=Image{fromFile=W..'sources/'..paths[i]}end
 local hull,shadow={},{}
 for height=16,100,2 do
  for phase=1,3 do
   local src=Image(sources[phase]);local width=math.floor(src.width*height/src.height+.5);src:resize(width,height)
   local im=Image(128,128,ColorMode.RGB);im:drawImage(src,Point(math.floor((128-width)/2),math.floor((128-height)/2)));hull[#hull+1]=im
  end
  local src=Image(sources[1]);local sh=math.floor(height*.55+.5);local sw=math.floor(src.width*sh/src.height+.5);src:resize(sw,sh)
  local im=Image(128,128,ColorMode.RGB)
  for y=0,sh-1 do for x=0,sw-1 do local c=src:getPixel(x,y);local a=pc.rgbaA(c);if a>0 then im:drawPixel(math.floor((128-sw)/2)+x,math.floor((128-sh)/2)+y,pc.rgba(3,10,18,math.floor(a*.57)))end end end
  shadow[#shadow+1]=im
 end
 save(pilot..'_hull',hull);save(pilot..'_shadow',shadow)
end
