local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local banks=json.decode(f:read('*a'));f:close()
for name,a in pairs(banks)do local im=Image{fromFile=D..'/'..name..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB);s.layers[1].name='Authored level-4 white cannon / '..name
for n=0,a.frames-1 do if n>0 then s:newEmptyFrame()end;local cell=Image(im,Rectangle(n%a.cols*a.cw,math.floor(n/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],n+1,cell,Point(0,0));s.frames[n+1].duration=1/30 end
local slice=s:newSlice(Rectangle(0,0,a.cw,a.ch));slice.name='optical-pivot';slice.pivot=Point(a.pivot[1],a.pivot[2]);s:saveAs(D..'/'..name..'.aseprite');s:close()end
