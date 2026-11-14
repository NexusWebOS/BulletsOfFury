local D=app.params['out'];local f=io.open(D..'/jobs.json','r');local jobs=json.decode(f:read('*a'));f:close();local pc=app.pixelColor
local b=Image{fromFile=D..'/sources/blue-master.png'};local blue=Image(b,Rectangle(0,0,384,512));local drac=Image{fromFile=D..'/sources/drac-master.png'}
local props={blue={image=blue,pivot={76,253},scale=.648,head={24,185,140,325}},drac={image=drac,pivot={334,442},scale=.13,head={125,85,570,800}}}
local function stamp(im,P,tip,ang,head)
 local src=P.image;local cs,sn=math.cos(ang),math.sin(ang);local radius=math.ceil(math.max(src.width,src.height)*P.scale)
 for y=math.max(0,math.floor(tip[2]-radius)),math.min(575,math.ceil(tip[2]+radius))do for x=math.max(0,math.floor(tip[1]-radius)),math.min(575,math.ceil(tip[1]+radius))do
  local dx,dy=(x-tip[1])/P.scale,(y-tip[2])/P.scale;local sx=math.floor(dx*cs+dy*sn+P.pivot[1]+.5);local sy=math.floor(-dx*sn+dy*cs+P.pivot[2]+.5)
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height and(not head or sx>=P.head[1]and sy>=P.head[2]and sx<P.head[3]and sy<P.head[4])then local v=src:getPixel(sx,sy);if pc.rgbaA(v)>96 then im:putPixel(x,y,pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
 end end
end
local function mat(im,m)
 local out=Image(im);for it in out:pixels()do local v=it();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
 if m=='hit'then r,g,b=255,255,255 elseif m=='red_hit'then r,g,b=255,35,42 elseif m=='chrome'and hi-lo<60 and hi>30 then local v=math.min(255,hi*1.42+10);r,g,b=v,v,math.min(255,v+5)elseif m=='red'then if(b>r*1.2 and b>g*1.12)or(g>r*1.6 and b>r*1.5)then local v=math.max(g,b);r,g,b=math.min(255,v*1.1),v*.12,v*.18 elseif hi>40 and hi-lo<65 then r,g,b=math.min(255,hi*1.2),g*.48,b*.52 end end
 it(pc.rgba(math.floor(r),math.floor(g),math.floor(b),a))end end;return out
end
for _,j in ipairs(jobs)do
 local input=Image{fromFile=j.input};local s=Sprite(576,576,ColorMode.RGB);s.layers[1].name='Clean GPT body / construction';s.layers[1].isVisible=false;local l=s:newLayer();l.name='Immutable rigid hammer / construction';l.isVisible=false;local production=s:newLayer();production.name='Production whole pose';local sheets={};for _,m in ipairs({'regular','chrome','red','hit','red_hit'})do sheets[m]=Image(2304,2304,ColorMode.RGB);sheets[m]:clear()end
 for i,z in ipairs(j.frames)do
  if i>1 then s:newEmptyFrame()end
  local body=Image(input,Rectangle(z.crop[1],z.crop[2],z.crop[3],z.crop[4]));for it in body:pixels()do local v=it();if pc.rgbaA(v)<170 then it(0)else it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
  body:resize(math.floor(body.width*j.scale+.5),math.floor(body.height*j.scale+.5));local whole=Image(576,576,ColorMode.RGB);whole:clear();whole:drawImage(body,Point(math.floor(288-z.root[1]*j.scale+.5),math.floor(442-z.root[2]*j.scale+.5)))
  local weapon=Image(576,576,ColorMode.RGB);weapon:clear();stamp(weapon,props[j.unit],z.tip,z.angle,false)
  local final=Image(576,576,ColorMode.RGB);final:clear();if j.name:find('overhead')and i>=5 and i<=9 then final:drawImage(weapon);final:drawImage(whole);stamp(final,props[j.unit],z.tip,z.angle,true)else final:drawImage(whole);final:drawImage(weapon)end
  -- Exact body-layer glove pixels sit over the rigid shaft, never cut away.
  local r=22
  for y=math.max(0,math.floor(z.grip[2]-r)),math.min(575,math.ceil(z.grip[2]+r))do for x=math.max(0,math.floor(z.grip[1]-r)),math.min(575,math.ceil(z.grip[1]+r))do if(x-z.grip[1])^2+(y-z.grip[2])^2<r*r then local v=whole:getPixel(x,y);if pc.rgbaA(v)>96 then final:putPixel(x,y,v)end end end end
  if j.mirror then final:flip();whole:flip();weapon:flip()end
  s:newCel(s.layers[1],i,whole,Point(0,0));s:newCel(l,i,weapon,Point(0,0));s:newCel(production,i,final,Point(0,0));s.frames[i].duration=.065
  for m,sh in pairs(sheets)do sh:drawImage(mat(final,m),Point((i-1)%4*576,math.floor((i-1)/4)*576))end
 end
 s:newTag(1,16).name=j.name..' / fixed T-joint';s:saveAs(D..'/exports/'..j.name..'.aseprite');s:close();for m,im in pairs(sheets)do im:saveAs(D..'/exports/'..j.name..'_'..m..'.png')end;print(j.name)
end
