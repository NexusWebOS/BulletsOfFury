local D=app.params['out'];local f=io.open(D..'/jobs.json','r');local J=json.decode(f:read('*a'));f:close();local pc=app.pixelColor;local inputs={};local cache={}
local function prepare(z)
 local id=z.source..':'..z.sourceCell;if cache[id]then return cache[id]end
 if not inputs[z.input]then inputs[z.input]=Image{fromFile=z.input}end
 local c=z.crop;local im=Image(inputs[z.input],Rectangle(c[1],c[2],c[3],c[4]))
 for it in im:pixels()do local v=it();if pc.rgbaA(v)<180 then it(0)else it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
 im:resize(math.floor(im.width*z.scale+.5),math.floor(im.height*z.scale+.5));local out=Image(640,640,ColorMode.RGB);out:clear();out:drawImage(im,Point(math.floor(320-z.root[1]*z.scale+.5),math.floor(474-z.root[2]*z.scale+.5)));cache[id]=out;return out
end
for _,j in ipairs(J)do local s=Sprite(640,640,ColorMode.RGB);s.layers[1].name='Complete generated actor and held hammer';local sheet=Image(2560,2560,ColorMode.RGB);sheet:clear()
 for i,z in ipairs(j.frames)do if i>1 then s:newEmptyFrame()end;local im=Image(prepare(z));if z.mirror then im:flip()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=z.duration or .065;sheet:drawImage(im,Point((i-1)%4*640,math.floor((i-1)/4)*640))end
 s:newTag(1,16).name=j.name..' / end-cap strikes';s:saveAs(D..'/exports/'..j.name..'.aseprite');s:close();sheet:saveAs(D..'/exports/'..j.name..'_regular.png');print(j.name)
end
