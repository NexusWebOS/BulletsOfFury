local D=app.params['out']
local f=io.open(app.params['jobs']or D..'/jobs.json','r');local jobs=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor
for _,j in ipairs(jobs)do
 local input=Image{fromFile=j.input}
 local s=Sprite(j.cell,j.cell,ColorMode.RGB);s.layers[1].name='Authored whole pose / regular'
 local layers={regular=s.layers[1]};for _,m in ipairs({'chrome','red','hit','red_hit'})do local l=s:newLayer();l.name=m;layers[m]=l;l.isVisible=false end
 local sheets={};for m,_ in pairs(layers)do sheets[m]=Image(j.cell*4,j.cell*4,ColorMode.RGB)end
 for i,z in ipairs(j.frames)do
  if i>1 then s:newEmptyFrame()end
  local c=Image(input,Rectangle(z.crop[1],z.crop[2],z.crop[3],z.crop[4]))
  for it in c:pixels()do local v=it();if pc.rgbaA(v)<96 then it(0)else it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
  -- The generated montage has poses crossing nominal grid gutters. Work from
  -- an expanded source rectangle and retain its connected whole actor.
  local seen={};local best={};local width=c.width
  for it in c:pixels()do local id=it.y*width+it.x
   if pc.rgbaA(it())>0 and not seen[id]then
    local q={id};seen[id]=true;local at=1
    while at<=#q do local n=q[at];at=at+1;local x=n%width;local y=math.floor(n/width)
     for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}})do local xx=x+d[1];local yy=y+d[2];local k=yy*width+xx
      if xx>=0 and xx<width and yy>=0 and yy<c.height and not seen[k]and pc.rgbaA(c:getPixel(xx,yy))>0 then seen[k]=true;q[#q+1]=k end
     end
    end
    if #q>#best then best=q end
   end
  end
  local keep={};for _,id in ipairs(best)do keep[id]=true end
  for it in c:pixels()do if not keep[it.y*width+it.x]then it(0)end end
  c:resize(math.floor(c.width*j.scale+.5),math.floor(c.height*j.scale+.5))
  local im=Image(j.cell,j.cell,ColorMode.RGB)
  im:drawImage(c,Point(math.floor(j.anchor[1]-z.root[1]*j.scale+.5),math.floor(j.anchor[2]-z.root[2]*j.scale+.5)))
  if j.rotate then
   -- Fixed whole-bank socket orientation, baked into native frame pixels.
   local spun=Image(j.cell,j.cell,ColorMode.RGB);local cs=math.cos(j.rotate);local sn=math.sin(j.rotate);local px=j.anchor[1];local py=j.anchor[2]
   for it in spun:pixels()do local dx=it.x-px;local dy=it.y-py;local xx=math.floor(px+dx*cs+dy*sn+.5);local yy=math.floor(py-dx*sn+dy*cs+.5)
    if xx>=0 and xx<im.width and yy>=0 and yy<im.height then it(im:getPixel(xx,yy))end
   end
   im=spun
  end
  if j.mirror then im:flip()end
  for m,l in pairs(layers)do
   local out=Image(im)
   for it in out:pixels()do local v=it();local a=pc.rgbaA(v)
    if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
     if m=='hit' then r,g,b=255,255,255
     elseif m=='red_hit' then r,g,b=255,35,42
     elseif m=='chrome' and hi-lo<60 and hi>30 then local y=math.min(255,math.floor(hi*1.42+10));r,g,b=y,y,math.min(255,y+5)
     elseif m=='red' then
      if (b>r*1.2 and b>g*1.12)or(g>r*1.6 and b>r*1.5)then local y=math.max(g,b);r,g,b=math.min(255,y*1.1),math.floor(y*.12),math.floor(y*.18)
      elseif hi>40 and hi-lo<65 then r,g,b=math.min(255,math.floor(hi*1.2)),math.floor(g*.48),math.floor(b*.52)end
     end
     it(pc.rgba(r,g,b,a))
    end
   end
   s:newCel(l,i,out,Point(0,0));sheets[m]:drawImage(out,Point((i-1)%4*j.cell,math.floor((i-1)/4)*j.cell))
  end
  s.frames[i].duration=.065
 end
 local tag=s:newTag(1,#j.frames);tag.name=j.name
 local sl=s:newSlice(Rectangle(0,0,j.cell,j.cell));sl.name='body-root';sl.pivot=Point(j.pivot[1],j.pivot[2])
 s:saveAs(D..'/exports/'..j.name..'.aseprite')
 for m,im in pairs(sheets)do im:saveAs(D..'/exports/'..j.name..'_'..m..'.png')end
 s:close();print('Exported '..j.name)
end
