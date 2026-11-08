local root=app.params.root
local banks={{name="tornado",n=20,fps=20},{name="cyclone",n=16,fps=24},{name="tempest",n=24,fps=24},{name="muzzle",n=4,fps=24},{name="impact",n=14,fps=24},{name="retina",n=24,fps=16},{name="core",n=32,fps=16},{name="bolt",n=8,fps=24},{name="orb",n=16,fps=24},{name="cloud_far",n=6,fps=4},{name="cloud_near",n=6,fps=4},{name="grade",n=7,fps=1},{name="rain",n=16,fps=24}}
for _,b in ipairs(banks)do
local first=Image{fromFile=root.."/frames/"..b.name.."/000.png"}
local s=Sprite(first.width,first.height,ColorMode.RGB);s.layers[1].name=b.name.." / authored fixed cells"
for i=0,b.n-1 do if i>0 then s:newEmptyFrame(i+1)end
local im=Image{fromFile=root.."/frames/"..b.name.."/"..string.format("%03d",i)..".png"}
s:newCel(s.layers[1],i+1,im,Point(0,0));s.frames[i+1].duration=1/b.fps end
s:saveAs(root.."/"..b.name..".aseprite");s:close()end
