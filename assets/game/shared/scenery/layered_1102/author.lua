local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for name,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB);local im=Image{fromFile=D..'/'..name..'.png'}
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%a.cols*a.w,math.floor(i/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
s:saveAs(D..'/'..name..'.aseprite');s:close()end
