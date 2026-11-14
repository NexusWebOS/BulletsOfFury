local D=app.params['out'];local f=io.open(D..'/jobs.json','r');local J=json.decode(f:read('*a'));f:close();local pc=app.pixelColor;local inputs={};local cache={}
local function prepare(z)
 local id=z.source..':'..z.sourceCell;if cache[id]then return cache[id]end
 if not inputs[z.input]then inputs[z.input]=Image{fromFile=z.input}end
 local c=z.crop;local im=Image(inputs[z.input],Rectangle(c[1],c[2],c[3],c[4]))
 for it in im:pixels()do local v=it();if pc.rgbaA(v)<180 then it(0)else it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
 im:resize(math.floor(im.width*z.scale+.5),math.floor(im.height*z.scale+.5));local out=Image(640,640,ColorMode.RGB);out:clear();out:drawImage(im,Point(math.floor(320-z.root[1]*z.scale+.5),math.floor(474-z.root[2]*z.scale+.5)));cache[id]=out;return out
end
local function material(im,m)
 if m=='regular'then return Image(im)end
 local out=Image(im);for it in out:pixels()do local v=it();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
 if m=='hit'then r,g,b=255,255,255 elseif m=='red_hit'then r,g,b=255,35,42 elseif m=='chrome'and hi-lo<65 and hi>30 then local k=math.min(255,hi*1.4+9);r,g,b=k,k,math.min(255,k+5)elseif m=='red'then if b>g*1.4 and(b>r*1.15 or r>g*1.4)and b>115 then local k=math.max(r,b);r,g,b=math.min(255,k*1.1),k*.12,k*.18 elseif hi>40 and hi-lo<65 then r,g,b=math.min(255,hi*1.2),g*.48,b*.52 end end
 it(pc.rgba(math.floor(r),math.floor(g),math.floor(b),a))end end;return out
end
for _,j in ipairs(J)do local s=Sprite(640,640,ColorMode.RGB);s.layers[1].name='GPT complete figure + held hammer';local sheets={};for _,m in ipairs({'regular','chrome','red','hit','red_hit'})do sheets[m]=Image(2560,2560,ColorMode.RGB);sheets[m]:clear()end
 for i,z in ipairs(j.frames)do if i>1 then s:newEmptyFrame()end;local im=Image(prepare(z));if z.mirror then im:flip()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=.065
  for m,sh in pairs(sheets)do sh:drawImage(material(im,m),Point((i-1)%4*640,math.floor((i-1)/4)*640))end
 end
 s:newTag(1,16).name=j.name..' / complete generated figure';s:saveAs(D..'/exports/'..j.name..'.aseprite');s:close();for m,im in pairs(sheets)do im:saveAs(D..'/exports/'..j.name..'_'..m..'.png')end;print(j.name)
end
