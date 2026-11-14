local D=app.params['out'];local f=io.open(app.params['jobs']or D..'/jobs.json','r');local cfg=json.decode(f:read('*a'));f:close();local pc=app.pixelColor
local function clean(im)
 for it in im:pixels()do local v=it();if pc.rgbaA(v)<190 then it(0)else it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end
end
local function connected(im)
 local seen={};local best={};local w=im.width
 for it in im:pixels()do local id=it.y*w+it.x;if pc.rgbaA(it())>0 and not seen[id]then
  local q={id};seen[id]=true;local at=1
  while at<=#q do local n=q[at];at=at+1;local x=n%w;local y=math.floor(n/w)
   for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}})do local xx,yy=x+d[1],y+d[2];local k=yy*w+xx
    if xx>=0 and yy>=0 and xx<w and yy<im.height and not seen[k]and pc.rgbaA(im:getPixel(xx,yy))>0 then seen[k]=true;q[#q+1]=k end
   end
  end
  if #q>#best then best=q end
 end end
 local keep={};for _,id in ipairs(best)do keep[id]=true end
 for it in im:pixels()do if not keep[it.y*w+it.x]then it(0)end end
end
local function material(im,unit,power,hit)
 local out=Image(im)
 for it in out:pixels()do local v=it();if pc.rgbaA(v)>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
  if hit then r,g,b=255,255,255
  elseif unit=='drac' then if b>g*1.18 and r>g*1.12 then r=math.min(255,r*(1+power*.55));g=g*(1-power*.15);b=b*(1-power*.37)end
  elseif hi-lo<68 and hi>30 then r=math.min(255,r*(1+power*.4));g=g*(1-power*.57);b=b*(1-power*.53)end
  it(pc.rgba(math.floor(r),math.floor(g),math.floor(b),255))
 end end
 return out
end
local function outline(im,unit,power)
 local out=Image(im);local radius=power>.1 and 3 or 1
 for it in im:pixels()do if pc.rgbaA(it())>0 then
  for _,d in ipairs({{-radius,0},{radius,0},{0,-radius},{0,radius}})do local x=it.x+d[1];local y=it.y+d[2]
   if x>=0 and y>=0 and x<im.width and y<im.height and pc.rgbaA(im:getPixel(x,y))==0 then
    local c=unit=='drac'and pc.rgba(146+math.floor(power*70),15,96+math.floor(power*100),255)or pc.rgba(165+math.floor(power*80),20+math.floor(power*46),24,255);out:putPixel(x,y,c)
   end
  end
 end end
 out:drawImage(im);return out
end
-- Identity lock: retain the established native helmet/skull pixels. The new
-- GPT gestures may move the neck, but never invent a different face or crest.
local heads={}
for _,unit in ipairs({'chronos','drac'})do
 local input=Image{fromFile=D..'/references/'..(unit=='chronos'and 'chronos-approved-master.png'or 'drac-approved-master.png')}
 local rect=unit=='chronos'and Rectangle(147,43,65,57)or Rectangle(136,53,82,80)
 local h=Image(input,rect);clean(h)
 for it in h:pixels()do
  if unit=='chronos'and it.y>=36 and(it.x<16 or it.x>48)then it(0)end
  if unit=='drac'and it.y>=52 and(it.x<25 or it.x>57)then it(0)end
 end
 heads[unit]=h
end
local function graftHead(im,j)
 local head=Image(heads[j.unit]);local scale=(j.unit=='chronos'and 1.12 or .98)*j.depth
 head:resize(math.floor(head.width*scale+.5),math.floor(head.height*scale+.5))
 local px=j.pivot[1];local top=im.height
 -- Head height comes from the authored silhouette, not from individual fitting.
 for y=0,im.height-1 do
  local found=false
  for x=math.floor(px-35*j.depth),math.floor(px+35*j.depth)do if x>=0 and x<im.width and pc.rgbaA(im:getPixel(x,y))>128 then found=true;break end end
  if found then top=y;break end
 end
 local base=top+math.floor((j.unit=='chronos'and 58 or 68)*j.depth)
 local half=math.floor((j.unit=='chronos'and 38 or 44)*j.depth)
 for y=top,base-math.floor(10*j.depth) do for x=math.max(0,px-half),math.min(im.width-1,px+half)do
  -- Horn tips may extend sideways; only the face/neck is removed below them.
  local width=math.floor(half*(1-.70*math.max(0,(y-top-20*j.depth)/(math.max(1,base-top-20*j.depth)))))
  if math.abs(x-px)<=width then im:putPixel(x,y,0)end
 end end
 im:drawImage(head,Point(math.floor(px-head.width/2),base-head.height))
 return im
end
for _,j in ipairs(cfg.jobs)do
 local input=Image{fromFile=j.input};local s=Sprite(j.cw,j.ch,ColorMode.RGB);s.layers[1].name='GPT whole pose / baked rage';local hit=s:newLayer();hit.name='native white hit';hit.isVisible=false
 local plain=j.bank=='charge'and Image(j.cw*4,j.ch*math.ceil(#j.frames/4),ColorMode.RGB)or nil
 local rows=math.ceil(#j.frames/4);local sheets={power=Image(j.cw*4,j.ch*rows,ColorMode.RGB),hit=Image(j.cw*4,j.ch*rows,ColorMode.RGB)}
 for i,z in ipairs(j.frames)do
  if i>1 then s:newEmptyFrame()end
  local im=Image(input,Rectangle(z.crop[1],z.crop[2],z.crop[3],z.crop[4]));clean(im);connected(im);im:resize(math.floor(im.width*j.scale+.5),math.floor(im.height*j.scale+.5))
  local cell=Image(j.cw,j.ch,ColorMode.RGB);cell:drawImage(im,Point(math.floor(j.pivot[1]-z.root[1]*j.scale+.5),math.floor(j.foot-z.root[2]*j.scale+.5)))
  cell=graftHead(cell,j)
  if plain then local p=outline(material(cell,j.unit,0,false),j.unit,0);plain:drawImage(p,Point((i-1)%4*j.cw,math.floor((i-1)/4)*j.ch))end
  local power=j.bank=='charge'and math.min(1,math.max(0,(i-3)/10))or 1
  for _,m in ipairs({'power','hit'})do local c=material(cell,j.unit,power,m=='hit');c=outline(c,j.unit,power);if m=='hit'then for it in c:pixels()do if pc.rgbaA(it())>0 then it(pc.rgba(255,255,255,255))end end end
   s:newCel(m=='hit'and hit or s.layers[1],i,c,Point(0,0));sheets[m]:drawImage(c,Point((i-1)%4*j.cw,math.floor((i-1)/4)*j.ch))
  end
  s.frames[i].duration=.06
 end
 s:newTag(1,#j.frames).name=j.name;local sl=s:newSlice(Rectangle(0,0,j.cw,j.ch));sl.name='registered-root';sl.pivot=Point(j.pivot[1],j.pivot[2]);s:saveAs(D..'/exports/'..j.name..'.aseprite')
 if plain then plain:saveAs(D..'/exports/'..j.name..'_plain.png')end
 for m,im in pairs(sheets)do im:saveAs(D..'/exports/'..j.name..'_'..m..'.png')end;s:close();print(j.name)
end
-- Prepared lightning and radial palm energies: no play-time glow masks or resizing.
for _,unit in ipairs({'red','purple'})do
 for _,kind in ipairs({'lightning','gather'})do
  local input=Image{fromFile=cfg.fx[kind]};local n=kind=='lightning'and 8 or 16;local iw=kind=='lightning'and 38 or 64;local ih=kind=='lightning'and 640 or 64;local cw=kind=='lightning'and 40 or 80;local ch=kind=='lightning'and 768 or 80;local sheet=Image(cw*4,ch*math.ceil(n/4),ColorMode.RGB)
  for i=0,n-1 do local c=Image(input,Rectangle(i%4*iw,math.floor(i/4)*ih,iw,ih));c:resize(cw,ch)
   for it in c:pixels()do local v=it();local a=pc.rgbaA(v);if a>0 then local hi=math.max(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v));local lo=math.min(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v));local r,g,b
    if hi-lo<35 and hi>200 then r,g,b=255,239,255 elseif unit=='red'then r,g,b=hi,math.floor(lo*.6),math.floor(hi*.24)else r,g,b=math.floor(hi*.8),math.floor(lo*.8),hi end
    it(pc.rgba(r,g,b,a))end end
   sheet:drawImage(c,Point(i%4*cw,math.floor(i/4)*ch))
  end
  sheet:saveAs(D..'/exports/fx_'..unit..'_'..kind..'.png')
 end
end
