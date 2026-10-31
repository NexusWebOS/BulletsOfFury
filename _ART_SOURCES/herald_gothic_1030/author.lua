-- HG70: source skull, coherent charge/arm poses and pre-rendered 3D spiral.
local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2
local f=io.open(D..'/inputs.json','r');local cfg=json.decode(f:read('*a'));f:close();local banks={};local images={}
local function clamp(x,l,h)return math.max(l,math.min(h,x))end
local function mix(a,b,u)return a+(b-a)*u end
local function rgba(r,g,b,a)return pc.rgba(math.floor(clamp(r,0,255)),math.floor(clamp(g,0,255)),math.floor(clamp(b,0,255)),math.floor(clamp(a,0,255)))end
local function cell(name,i)local a=cfg.art[name];if not images[name]then images[name]=Image{fromFile=R..'/'..a.path}end;return Image(images[name],Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch)),a.pivot end
local function white(im)local o=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then o:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return o end
local function register(name,frames,pivot,extra,hit)
 local w,h=frames[1].width,frames[1].height;local cols=#frames>32 and 8 or 4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close()
 local a={key='hg70_'..name,path='assets/game/levels/stage_08/miniboss/herald_gothic_1030/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot={pivot[1],pivot[2]}};for k,v in pairs(extra or{})do a[k]=v end;banks[name]=a
 if hit then local h={};for _,im in ipairs(frames)do table.insert(h,white(im))end;register(name..'_hit',h,pivot,extra,false)end
end
local function transform(src,piv,a,k,size,glow)
 local out=Image(size,size,ColorMode.RGB);local c,s=math.cos(a),math.sin(a);local mid=size/2
 for y=0,size-1 do for x=0,size-1 do local dx,dy=x-mid,y-mid;local sx=math.floor((dx*c+dy*s)/k+piv[1]+.5);local sy=math.floor((-dx*s+dy*c)/k+piv[2]+.5)
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height then local v=src:getPixel(sx,sy);if pc.rgbaA(v)>0 then
   if glow>0 then local mx=math.max(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v));local u=glow*.5;v=rgba(mix(pc.rgbaR(v),math.min(255,mx*1.15+38),u),mix(pc.rgbaG(v),mx*.13,u),mix(pc.rgbaB(v),mx*.24,u),pc.rgbaA(v))end
   out:drawPixel(x,y,v)end end
 end end
 if glow>0 then local halo=Image(size,size,ColorMode.RGB);local rad=glow>.65 and 4 or 2
  for y=rad,size-rad-1 do for x=rad,size-rad-1 do if pc.rgbaA(out:getPixel(x,y))>100 then for dy=-rad,rad,2 do for dx=-rad,rad,2 do if dx*dx+dy*dy<=rad*rad then halo:drawPixel(x+dx,y+dy,rgba(244,9,49,glow>.65 and 150 or 95))end end end end end end;halo:drawImage(out);out=halo end
 return out
end
-- The generated layout is measured, never treated as an exact atlas promise.
local orb=Image{fromFile=D..'/gpt_gothic_skull.png'};local burst=Image{fromFile=D..'/gpt_gothic_shatter.png'}
local cx={168,478,788,1099};local cy={175,475,785,1091}
local function generated(sheet,i,size,pad)
 local im=Image(310,310,ColorMode.RGB);im:drawImage(sheet,Point(155-cx[i%4+1],155-cy[math.floor(i/4)+1]));im:resize(size,size)
 local out=Image(pad,pad,ColorMode.RGB);out:drawImage(im,Point((pad-size)/2,(pad-size)/2));return out
end
for level=0,7 do local a,b={},{};for i=0,15 do table.insert(a,generated(orb,i,40+level*12,132));table.insert(b,generated(burst,i,64+level*12,156))end;register('skull_'..level,a,{66,66});register('impact_'..level,b,{78,78})end
local red=Image{fromFile=R..'/assets/game/levels/stage_06/miniboss/fortress_red_1028/red_orbs.png'}
for level=0,3 do local a={};for i=0,15 do local im=Image(red,Rectangle(i%8*72,math.floor(i/8)*72,72,72));im:resize(22+level*6,22+level*6);local o=Image(44,44,ColorMode.RGB);o:drawImage(im,Point((44-im.width)/2,(44-im.height)/2));table.insert(a,o)end;register('chunk_'..level,a,{22,22})end
-- Arms now reach their raised pose continuously before emission and lower through24 frames.
for id,spec in pairs(cfg.parts)do
 local clips={cast=32,raised=16,lower=24};if id=='head'then clips.far=16;clips.depart=20;clips.arrive=20;clips.grow=16 end
 local sz=id:sub(1,4)=='wing'and 360 or id=='core'and 264 or id=='head'and 200 or 248
 for clip,n in pairs(clips)do local frames,poses={},{}
  for i=0,n-1 do local u=i/math.max(1,n-1);local lift=clip=='cast'and clamp(i/23,0,1)or clip=='lower'and(1-u*u*(3-2*u))or 1
   local localA,k,a=0,1,0;local dx,dy=spec.attach[1],spec.attach[2];local side=id:sub(-1)=='L'and-1 or 1;local g=.35+.65*lift
   if clip=='raised'then g=.65+.35*math.sin(u*tau)^2 end
   if id:sub(1,3)=='gun'then localA=side*2.4*lift;dy=dy-24*lift end
   if id:sub(1,4)=='wing'then localA=side*(-.14+math.sin(u*tau*2)*.16)end
   if clip=='far'then k=.30;g=.7 elseif clip=='depart'then k=mix(1,.30,u);a=u*math.pi;g=.5 elseif clip=='arrive'then k=mix(.30,1,u);a=math.pi+math.pi*u;g=.5*(1-u)elseif clip=='grow'then k=mix(.70,1,u);g=0 end
   local src,piv
   if id=='head'then local j=clip=='lower'and math.floor((1-u)*15)or clip=='cast'and math.min(15,math.floor(i/23*15))or(8+math.floor((math.sin(u*tau)+1)*3.5));src,piv=cell('head_rage',j)
   else src,piv=cell('herald_'..id,id=='core'and 0 or 15)end
   local c,s=math.cos(a),math.sin(a);table.insert(frames,transform(src,piv,a+localA,k,sz,g));table.insert(poses,{x=(dx*c-dy*s)*k,y=(dx*s+dy*c)*k,a=a+localA,s=spec.scale*k})
  end
  register(id..'_'..clip,frames,{sz/2,sz/2},{poses=poses},true)
 end
 print('authored '..id)
end
-- Existing genuine32-view PixelLab turntable, rolled offline into96 new fixed frames.
local raw={};for i=0,31 do raw[i]=Image{fromFile=R..'/assets/game/levels/stage_08/miniboss/herald_desperation_1029/frames/'..string.format('%02d',i)..'.png'}end
for _,kind in ipairs({'yaw','spiral'})do local a,sockets={},{};local n=kind=='yaw'and 32 or 96
 for i=0,n-1 do local angle=kind=='spiral'and i*tau*2/n or 0;local scale=kind=='spiral'and(.88+.12*math.cos(i*tau/n))or 1;local src=raw[i%32];local pix=transform(src,{src.width/2,src.height/2},angle,scale,320,.4+.5*math.sin(i*tau/16)^2);table.insert(a,pix)
  local x,y=math.sin((i%32)*tau/32)*15,-35;table.insert(sockets,{math.floor((x*math.cos(angle)-y*math.sin(angle))*scale),math.floor((x*math.sin(angle)+y*math.cos(angle))*scale)})
 end;register(kind,a,{160,160},{sockets=sockets},true)
end
-- Background counter hits flash against the exact same visible alpha, too.
for _,name in ipairs({'spin','charge'})do local a=cfg.depth[name];local sheet=Image{fromFile=R..'/'..a.path};local frames={};for i=0,a.frames-1 do table.insert(frames,white(Image(sheet,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch))))end;register(name..'_hit',frames,a.pivot)end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('HG70 complete')
