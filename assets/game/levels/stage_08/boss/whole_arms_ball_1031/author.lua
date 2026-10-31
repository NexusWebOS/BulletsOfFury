local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M)do local im=Image{fromFile=D..'/'..n..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB)
 for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 s:saveAs(D..'/'..n..'.aseprite');s:close()
end
