local root=app.params['root'];local out=app.params['out']
local pc=app.pixelColor
local function red(im)
 local q=Image(im)
 for it in q:pixels() do local c=it();local a=pc.rgbaA(c)
  if a>0 then local r=pc.rgbaR(c);local g=pc.rgbaG(c);local b=pc.rgbaB(c);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
   it(pc.rgba(hi,math.floor(lo+(hi-lo)*.16+.5),math.floor(lo+(hi-lo)*.22+.5),a))
  end
 end
 return q
end
local function bank(name,stem,h)
 local sheet=Image(2048,1024,ColorMode.RGB)
 local spr=Sprite(64,64,ColorMode.RGB)
 for phase=0,7 do
  local src=Image{fromFile=root..'/assets/game/shared/player_weapons/boss_projectile_overhaul/'..stem..phase..'.png'}
  src=red(src);local w=math.floor(src.width*h/src.height+.5);src:resize(w,h)
  for d=0,63 do
   local cell=Image(64,64,ColorMode.RGB);local a=d*math.pi*2/64;local co=math.cos(a);local si=math.sin(a)
   for y=0,63 do for x=0,63 do
    local dx=x+.5-32;local dy=y+.5-32;local sx=math.floor(dx*co+dy*si+w/2);local sy=math.floor(-dx*si+dy*co+h/2)
    if sx>=0 and sy>=0 and sx<w and sy<h then cell:drawPixel(x,y,src:getPixel(sx,sy)) end
   end end
   local f=phase*64+d;sheet:drawImage(cell,Point(f%32*64,math.floor(f/32)*64))
   if d==0 then if phase>0 then spr:newFrame() end;app.activeFrame=phase+1;spr:newCel(spr.layers[1],phase+1,cell,Point(0,0)) end
  end
 end
 spr:saveAs(out..'/'..name..'.aseprite');sheet:saveAs(out..'/'..name..'.png');spr:close()
end
bank('projectile','bpfx_proj_laser_',46)
bank('muzzle','bpfx_muzzle_laser_',64)
print('Herald red laser and larger muzzle: 8 phases x64 authored headings')
