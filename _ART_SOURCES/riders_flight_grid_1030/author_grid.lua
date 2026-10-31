local W=app.params['work'];if W:sub(-1)~='/'then W=W..'/'end
local pc=app.pixelColor
local cw,ch=480,64
local cells={}
-- Filled rectangular energy membrane. Pixel palette, scan sweeps and assembly
-- are authored here; the runtime only selects a fixed-size transparent cell.
for f=0,39 do
 local im=Image(cw,ch,ColorMode.RGB)
 local open=f<16 and (f+1)/16 or 1
 local strength=f>=32 and (40-f)/8 or 1
 local scan=(f%16)*30
 for y=7,56 do for x=4,475 do
  local cut=math.abs(x-239.5)>236*open
  if not cut then
   local rim=(y<=9 or y>=54 or x<=6 or x>=473)
   local corner=(x<12 or x>467)and(y<15 or y>48)
   local grid=(x-7)%16==0 or(y-8)%12==0
   local seam=(x-7)%16==1 or(y-8)%12==1
   local node=(x-7)%16<=2 and(y-8)%12<=2
   local swept=math.abs(x-scan)<7
   local r,g,b,a=96,65,12,174
   if (x+y)%4==0 then r,g,b,a=131,91,20,185 end
   if seam then r,g,b,a=184,123,23,230 end
   if grid then r,g,b,a=250,192,53,248 end
   if swept and not rim then r,g,b=math.min(255,r+35),math.min(244,g+35),math.min(154,b+45)end
   if rim then r,g,b,a=255,223,101,255 end
   if node or rim and(y==8 or y==55)then r,g,b,a=255,247,181,255 end
   if corner then r,g,b,a=218,157,35,255 end
   im:drawPixel(x,y,pc.rgba(r,g,b,math.floor(a*strength)))
  end
 end end
 cells[#cells+1]=im
end
local sp=Sprite(cw,ch,ColorMode.RGB);sp.layers[1].name='Golden Aegis / solid force-field grid'
local sheet=Image(cw*8,ch*5,ColorMode.RGB)
for i,im in ipairs(cells)do if i>1 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],i,im,Point(0,0));sp.frames[i].duration=1/24;sheet:drawImage(im,Point((i-1)%8*cw,math.floor((i-1)/8)*ch))end
for _,row in ipairs{{'deploy',1,16},{'energized',17,32},{'release',33,40}}do local t=sp:newTag(row[2],row[3]);t.name=row[1]end
sp:saveAs(W..'gold_grid.aseprite');sheet:saveAs(W..'gold_grid.png');sp:close()
