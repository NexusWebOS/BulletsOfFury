local root=app.params['root'];local out=app.params['out'];local pc=app.pixelColor
local files={green='fov-light-green.png',yellow='fov-yellow.png',red='fov-neon-red.png'}
local symbol=Image{fromFile=root..'/assets/game/levels/stage_06/boss/rook_barrage_1028/spin_symbol.png'};symbol:resize(46,46)
local function save(name,im)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s:newCel(s.layers[1],1,im,Point(0,0));s:saveAs(out..'/'..name..'.aseprite');im:saveAs(out..'/'..name..'.png');s:close()
end
for colour,file in pairs(files)do
 local src=Image{fromFile=root..'/assets/bossmode/ui/'..file};local fallback=src:getPixel(320,320);local im=Image(404,404,ColorMode.RGB)
 for y=0,403 do for x=0,403 do local dx,dy=x-201.5,y-201.5;local r=math.sqrt(dx*dx+dy*dy)
  if r<=200 then im:drawPixel(x,y,fallback)end
 end end;save('field_'..colour,im)
 local badge=Image(48,48,ColorMode.RGB);for y=0,45 do for x=0,45 do local c=symbol:getPixel(x,y);if pc.rgbaA(c)>0 then local v=math.max(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c))/255;badge:drawPixel(x+1,y+1,pc.rgba(math.floor(pc.rgbaR(fallback)*v),math.floor(pc.rgbaG(fallback)*v),math.floor(pc.rgbaB(fallback)*v),pc.rgbaA(c)))end end end;save('symbol_'..colour,badge)
end
