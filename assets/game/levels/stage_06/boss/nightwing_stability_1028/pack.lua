local W=assert(app.params['work'],'Pass --script-param work=<staging folder>')..'/art/'
local src=Image{fromFile=W..'clean_charge.png'};local sheet=Image(1632,816,ColorMode.RGB);local sp=Sprite(272,272,ColorMode.RGB)
for level=0,5 do for pose=0,2 do
 local f=level*17+({0,8,16})[pose+1];local im=Image(272,272,ColorMode.RGB);im:drawImage(src,Point(-(f%8)*272,-math.floor(f/8)*272));local n=level*3+pose
 if n>0 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],n+1,im,Point(0,0));sp.frames[n+1].duration=.0625;sheet:drawImage(im,Point((n%6)*272,math.floor(n/6)*272))
end end
sp:saveAs(W..'clean_charge.aseprite');sheet:saveAs(W..'clean_charge.png');sp:close()
for _,name in ipairs({'wind_rear','wind_front'})do
 local src=Image{fromFile=W..name..'.png'};local sp=Sprite(384,384,ColorMode.RGB);local sheet=Image(3072,1152,ColorMode.RGB)
 for f=0,23 do local im=Image(384,384,ColorMode.RGB);im:drawImage(src,Point(-(f%6)*512-64,-math.floor(f/6)*512-64));if f>0 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],f+1,im,Point(0,0));sp.frames[f+1].duration=1/18;sheet:drawImage(im,Point(f%8*384,math.floor(f/8)*384))end
 sp:saveAs(W..name..'.aseprite');sheet:saveAs(W..name..'.png');sp:close()
end
