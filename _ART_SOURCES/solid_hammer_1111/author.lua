local W=app.params['out'];local f=io.open(W..'/aseprite-jobs.json','r');local jobs=json.decode(f:read('*a'));f:close();local audit={}
for _,j in ipairs(jobs)do
 local s=Sprite(512,512,ColorMode.RGB);s.layers[1].name='Complete authored character and held hammer'
 local durations={30,30,30,30,30,30,30,30,55,55,55,55,55,55,55,55,60,55,45,40,35,30,100,65,50,50,50,50,50,50,50,50}
 for i=1,j.count do if i>1 then s:newEmptyFrame()end;local im=Image{fromFile=W..'/exports/'..j.name..'/'..string.format('%02d',i-1)..'.png'};s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=j.count==32 and durations[i]/1000 or .055 end
 local root=s:newSlice(Rectangle(256,256,1,1));root.name='Actor root / fixed native origin'
 if j.count==32 then s:newTag(1,16).name='Lift and load';s:newTag(17,22).name='Downstroke';s:newTag(23,24).name='Cap contact';s:newTag(25,32).name='Rebound and regrip'else s:newTag(1,j.count).name=j.name end
 s:saveAs(W..'/exports/'..j.name..'.aseprite');s:close()
 s=app.open(W..'/exports/'..j.name..'.aseprite');assert(#s.frames==j.count and #s.layers==1)
 local out=Image(2048,math.ceil(j.count/4)*512,ColorMode.RGB);out:clear()
 for i=1,j.count do local c=s.layers[1]:cel(i);out:drawImage(c.image,Point((i-1)%4*512+c.position.x,math.floor((i-1)/4)*512+c.position.y))end
 out:saveAs(W..'/exports/'..j.name..'_roundtrip.png');audit[#audit+1]={bank=j.name,frames=#s.frames,layers=#s.layers};s:close()
end
local f=io.open(W..'/aseprite-audit.json','w');f:write(json.encode(audit));f:close()
