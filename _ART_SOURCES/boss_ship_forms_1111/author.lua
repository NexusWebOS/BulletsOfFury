local W=app.params['out'];local f=io.open(W..'/manifest.json','r');local jobs=json.decode(f:read('*a'));f:close();local audit={}
for name,j in pairs(jobs)do
 local cw,ch=j.cell[1],j.cell[2];local s=Sprite(cw,ch,ColorMode.RGB);s.layers[1].name='Complete authored actor / released prop'
 for i=1,j.count do
  if i>1 then s:newEmptyFrame()end
  local im=Image{fromFile=W..'/exports/'..name..'/'..string.format('%02d',i-1)..'.png'};s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=string.find(name,'transform')and .083 or .055
 end
 local root=s:newSlice(Rectangle(j.pivot[1],j.pivot[2],1,1));root.name='Fixed native origin';s:newTag(1,j.count).name=name
 s:saveAs(W..'/exports/'..name..'.aseprite');s:close();s=app.open(W..'/exports/'..name..'.aseprite');assert(#s.frames==j.count and #s.layers==1)
 local out=Image(cw*4,math.ceil(j.count/4)*ch,ColorMode.RGB);out:clear()
 for i=1,j.count do local c=s.layers[1]:cel(i);out:drawImage(c.image,Point((i-1)%4*cw+c.position.x,math.floor((i-1)/4)*ch+c.position.y))end
 out:saveAs(W..'/exports/'..name..'_roundtrip.png');audit[#audit+1]={bank=name,frames=#s.frames,layers=#s.layers};s:close()
end
local f=io.open(W..'/aseprite-audit.json','w');f:write(json.encode(audit));f:close()
