local root=app.params['root'];local out=app.params['out'];local pc=app.pixelColor
local src=Image{fromFile=root..'/assets/game/levels/stage_05/boss/stage5_hammer/reticle.png'}
src:resize(64,32)
local sheet=Image(512,96,ColorMode.RGB);local spr=Sprite(64,32,ColorMode.RGB)
local levels={.08,.17,.29,.43,.59,.76,.88,1}
for colour=0,2 do for frame=0,7 do
 local cell=Image(src)
 for it in cell:pixels() do local c=it();local a=pc.rgbaA(c)
  if a>0 then local r=pc.rgbaR(c);local g=pc.rgbaG(c);local b=pc.rgbaB(c)
   if colour>0 then local l=r*.21+g*.72+b*.07
    if colour==1 then r=math.min(255,l*1.4);g=math.min(255,l*1.25);b=l*.15
    else r=math.min(255,l*1.55);g=l*.23;b=l*.22 end
   end
   it(pc.rgba(math.floor(r+.5),math.floor(g+.5),math.floor(b+.5),math.floor(a*levels[frame+1]+.5)))
  end
 end
 sheet:drawImage(cell,Point(frame*64,colour*32))
 local f=colour*8+frame+1;if f>1 then spr:newFrame() end
 spr.frames[f].duration=.025;spr:newCel(spr.layers[1],f,cell,Point(0,0))
end end
spr:saveAs(out..'/retina.aseprite');sheet:saveAs(out..'/retina.png');spr:close()
print('Authored24 ground Retina colour/fade frames')
