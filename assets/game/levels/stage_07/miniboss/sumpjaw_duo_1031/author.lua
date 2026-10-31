local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB)
 for _,page in ipairs(a.pages)do local path=page.path:match('([^/]+)$');local im=Image{fromFile=D..'/'..path}
  for j=0,page.frames-1 do local i=page.start+j;if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(j%a.cols*a.w,math.floor(j/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 end;s:saveAs(D..'/'..n..'.aseprite');s:close()
end
