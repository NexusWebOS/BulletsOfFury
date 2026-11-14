local function run()
local D=app.params['out'];local pc=app.pixelColor;local input=Image{fromFile=D..'/exports/wave_purple-source.png'};local base=Image(input,Rectangle(100,0,120,90));local sheet=Image(1024,1024,ColorMode.RGB)
for d=0,7 do
 local size=.6+.4*d/7;local c=Image(base);c:resize(math.max(1,math.floor(10*size)),math.floor(54*size));local w,h=c.width,c.height
 for a=0,31 do
  local cell=Image(64,64,ColorMode.RGB);local ang=a*math.pi*2/32;local cs,sn=math.cos(ang),math.sin(ang)
  for it in cell:pixels()do local dx,dy=it.x-31.5,it.y-31.5;local x=math.floor(dx*cs+dy*sn+w/2);local y=math.floor(-dx*sn+dy*cs+h/2);if x>=0 and y>=0 and x<w and y<h then it(c:getPixel(x,y))end end
  local f=d*32+a;sheet:drawImage(cell,Point(f%16*64,math.floor(f/16)*64))
 end
end
sheet:saveAs(D..'/exports/fx_purple_projectiles.png')

end
local ok,err=pcall(run);local f=io.open('C:/Users/Mike/Documents/New project/BOF-Rage-Polish-1110/projectile-build.log','w');f:write(tostring(ok)..' '..tostring(err));f:close()