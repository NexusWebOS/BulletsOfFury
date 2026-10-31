local D=app.params['out'];local pc=app.pixelColor;local f=io.open(D..'/manifest.json','r');local m=json.decode(f:read('*a'));f:close()
-- Begin after the generated skull is completely gone: only glass and lightning remain.
for level=0,7 do local a=m['impact_'..level];local src=Image{fromFile=D..'/impact_'..level..'.png'};local sheet=Image(a.cw*4,a.ch*4,ColorMode.RGB);local s=Sprite(a.cw,a.ch,ColorMode.RGB)
 for i=0,15 do local j=7+math.floor(i/15*8);local im=Image(src,Rectangle(j%4*a.cw,math.floor(j/4)*a.ch,a.cw,a.ch));sheet:drawImage(im,Point(i%4*a.cw,math.floor(i/4)*a.ch));if i>0 then s:newEmptyFrame()end;s:newCel(s.layers[1],i+1,im,Point(0,0));s.frames[i+1].duration=1/32 end
 local n='glass_'..level;sheet:saveAs(D..'/'..n..'.png');s:saveAs(D..'/'..n..'.aseprite');s:close();m[n]={key='hg70_'..n,path='assets/game/levels/stage_08/miniboss/herald_gothic_1030/'..n..'.png',cw=a.cw,ch=a.ch,cols=4,frames=16,pivot={a.pivot[1],a.pivot[2]}}
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(m));f:close()
