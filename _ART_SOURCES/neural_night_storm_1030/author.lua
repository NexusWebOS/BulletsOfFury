local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local A=json.decode(f:read('*a'));f:close()
local spr=Sprite(384,384,ColorMode.RGB);local n=0
for level=0,5 do for _,a in ipairs(A.banks['glow_'..level])do
 local page=Image{fromFile=R..'/'..A.pages[a.key].path};local q=a.rect;local crop=Image(page,Rectangle(q[1],q[2],q[3],q[4]));local im=Image(384,384,ColorMode.RGB);im:drawImage(crop,Point(a.offset[1]+192,a.offset[2]+192));n=n+1
 if n>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],n,im,Point(0,0));spr.frames[n].duration=.1
end end
spr:saveAs(D..'/storm-pose-glow.aseprite');spr:close()
local sky=app.open(R..'/'..A.arena.sky.path);sky:saveAs(D..'/night-sky.aseprite');sky:close()
local clouds=app.open(R..'/'..A.arena.clouds.path);clouds:saveAs(D..'/night-clouds.aseprite');clouds:close()
print('Exported54 editable glow poses and2 editable night-sky documents.')
