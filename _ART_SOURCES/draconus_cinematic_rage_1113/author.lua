local W=app.params['out'];local f=io.open(W..'/manifest.json','r');local banks=json.decode(f:read('*a'));f:close();local audit={}
for name,a in pairs(banks)do
 local s=Sprite(a.cw,a.ch,ColorMode.RGB);s.layers[1].name=string.match(name,'^center') and 'Complete actor and single rigid held hammer' or 'Complete authored actor or baked original effect'
 for i=1,a.count do
  if i>1 then s:newEmptyFrame()end
  local image=Image{fromFile=W..'/exports/'..name..'/'..string.format('%02d',i-1)..'.png'};s:newCel(s.layers[1],i,image,Point(0,0));s.frames[i].duration=.06
 end
 local pivot=s:newSlice(Rectangle(a.pivot[1],a.pivot[2],1,1));pivot.name='Native registered pivot'
 s:newTag(1,a.count).name=name;s:saveAs(W..'/exports/'..name..'.aseprite');s:close()
 s=app.open(W..'/exports/'..name..'.aseprite');local out=Image(a.cw*4,math.ceil(a.count/4)*a.ch,ColorMode.RGB);out:clear()
 for i=1,a.count do local c=s.layers[1]:cel(i);out:drawImage(c.image,Point((i-1)%4*a.cw+c.position.x,math.floor((i-1)/4)*a.ch+c.position.y))end
 out:saveAs(W..'/exports/'..name..'_roundtrip.png');audit[#audit+1]={bank=name,frames=#s.frames};s:close()
end
local f=io.open(W..'/aseprite-audit.json','w');f:write(json.encode(audit));f:close()
