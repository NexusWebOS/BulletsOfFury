-- Source-preserving offline Aseprite author. Fixed even cells and measured pivots.
local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor
local f=io.open(D..'/inputs.json','r');local cfg=json.decode(f:read('*a'));f:close()
local banks={};local images={};local tau=math.pi*2
if app.params['only']=='tornado'then local f=io.open(D..'/manifest.json','r');banks=json.decode(f:read('*a'));f:close()end
local function clamp(x,l,h)return math.max(l,math.min(h,x))end
local function mix(a,b,u)return a+(b-a)*u end
local function rgba(r,g,b,a)return pc.rgba(math.floor(r),math.floor(g),math.floor(b),math.floor(a))end
local function cell(name,i)
 local a=cfg.art[name];if not images[name]then images[name]=Image{fromFile=R..'/'..a.path}end
 return Image(images[name],Rectangle((i%a.cols)*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch)),a.pivot
end
local function register(name,frames,pivot,meta)
 local w,h=frames[1].width,frames[1].height
 local l,t,r,b=w,h,0,0
 for _,im in ipairs(frames)do for it in im:pixels()do if pc.rgbaA(it())>0 then l=math.min(l,it.x);t=math.min(t,it.y);r=math.max(r,it.x+1);b=math.max(b,it.y+1)end end end
 l=math.max(0,math.floor((l-2)/2)*2);t=math.max(0,math.floor((t-2)/2)*2);r=math.min(w,math.ceil((r+2)/2)*2);b=math.min(h,math.ceil((b+2)/2)*2)
 if r>l and b>t then for i,im in ipairs(frames)do frames[i]=Image(im,Rectangle(l,t,r-l,b-t))end;w=r-l;h=b-t;pivot={pivot[1]-l,pivot[2]-t}end
 local cols=4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point(((i-1)%cols)*w,math.floor((i-1)/cols)*h))end
 sheet:saveAs(D..'/'..name..'.png')
 local s=Sprite(w,h,ColorMode.RGB);for i,im in ipairs(frames)do if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 s:saveAs(D..'/'..name..'.aseprite');s:close()
 banks[name]={key='hh52_'..name,path='assets/game/levels/stage_08/miniboss/herald_chaos_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot,poses=meta}
end
local function white(im)
 local out=Image(im.width,im.height,ColorMode.RGB);for it in im:pixels()do local c=it();if pc.rgbaA(c)>0 then out:drawPixel(it.x,it.y,rgba(255,255,255,pc.rgbaA(c)))end end;return out
end
local function transform(src,piv,a,k,size,glow)
 local out=Image(size,size,ColorMode.RGB);local c,s=math.cos(a),math.sin(a);local mid=size/2
 for y=0,size-1 do for x=0,size-1 do
  local dx,dy=x-mid,y-mid;local sx=math.floor((dx*c+dy*s)/k+piv[1]+.5);local sy=math.floor((-dx*s+dy*c)/k+piv[2]+.5)
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height then local v=src:getPixel(sx,sy)
   if pc.rgbaA(v)>0 then
    if glow>0 then local v0=math.max(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v));local u=glow*.50
     v=rgba(mix(pc.rgbaR(v),math.min(255,v0*1.15+38),u),mix(pc.rgbaG(v),v0*.13,u),mix(pc.rgbaB(v),v0*.24,u),pc.rgbaA(v))end
    out:drawPixel(x,y,v)
   end
  end
 end end
 if glow>0 then local halo=Image(size,size,ColorMode.RGB);local rad=glow>.65 and 4 or 2
  for y=rad,size-rad-1 do for x=rad,size-rad-1 do if pc.rgbaA(out:getPixel(x,y))>100 then
   for dy=-rad,rad,2 do for dx=-rad,rad,2 do if dx*dx+dy*dy<=rad*rad then halo:drawPixel(x+dx,y+dy,rgba(244,9,49,glow>.65 and 150 or 95))end end end
  end end end;halo:drawImage(out);out=halo
 end
 return out
end
-- GPT sixteen-cell tornado. Retain generated alpha, reduce with nearest pixels.
local sheet=Image{fromFile=D..'/gpt_tornado_source.png'};local tornado={}
-- GPT spacing is not an atlas contract: measured occupied row bands and common column pivots.
local rows={{100,350},{394,644},{684,934},{960,1210}};local centers={174,478,777,1082}
for i=0,15 do local row=rows[math.floor(i/4)+1];local im=Image(sheet,Rectangle(centers[i%4+1]-122,row[1],244,250));im:resize(184,188)
 local pad=Image(200,216,ColorMode.RGB);pad:drawImage(im,Point(8,14));table.insert(tornado,pad)end
register('tornado',tornado,{100,108})
if app.params['only']=='tornado'then local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();return end
-- The actual source skull has eight authored depth/size variants, not runtime scaling.
for level=0,7 do local frames={};local size=40+level*12
 for i=0,15 do local im=cell('death_ball',i);im:resize(size,size);local out=Image(132,132,ColorMode.RGB);out:drawImage(im,Point(66-size/2,66-size/2));table.insert(frames,out)end
 register('skull_'..level,frames,{66,66})
 local impacts={};local size=64+level*12
 for i=0,15 do local im=cell('nuke',i);im:resize(size,size);local out=Image(156,156,ColorMode.RGB);out:drawImage(im,Point(78-size/2,78-size/2));table.insert(impacts,out)end
 register('impact_'..level,impacts,{78,78})
end
local orbs=Image{fromFile=R..'/assets/game/levels/stage_06/miniboss/fortress_red_1028/red_orbs.png'};local orbframes={}
for i=0,15 do local im=Image(orbs,Rectangle(i%8*72,math.floor(i/8)*72,72,72));im:resize(44,44);table.insert(orbframes,im)end
register('lightning_ball',orbframes,{22,22})
for level=0,3 do local frames={};local size=16+level*6
 for i=0,15 do local im=cell('code_round',i);im:resize(size,size);local out=Image(40,40,ColorMode.RGB);out:drawImage(im,Point(20-size/2,20-size/2));table.insert(frames,out)end
 register('chunk_'..level,frames,{20,20})
end
local star=Image{fromFile=R..'/assets/game/levels/stage_06/boss/riders_defense_1029/entry_star.png'};register('star',{star},{20,20})
for _,color in ipairs({'green','yellow','red'})do local src=Image{fromFile=R..'/assets/game/levels/stage_06/boss/rook_circle_1029/field_'..color..'.png'};src:resize(92,92);register('impact_'..color,{src},{46,46})end
-- Physical modules stay separate. Pose data drives native masks/sockets and the exact same frames.
local clips={cast=32,raised=16,depart=20,far=16,arrive=20,turn=32,grow=16}
for id,spec in pairs(cfg.parts)do
 local base,piv=cell(id=='head'and'head_rage'or'herald_'..id,id=='core'and 0 or id=='head'and 8 or 15)
 local size=(id:sub(1,4)=='wing'and 360 or id=='core'and 264 or id=='head'and 200 or 248)
 for clip,n in pairs(clips)do local frames,hits,poses={},{},{}
  for i=0,n-1 do local u=i/math.max(1,n-1);local a,k,glow,localA=0,1,0,0;local dx,dy=spec.attach[1],spec.attach[2];local side=id:sub(-1)=='L'and-1 or 1
   if clip=='cast'then local charge=clamp(i/23,0,1);local lift=clamp((i-23)/8,0,1);glow=.35+.65*math.sin(charge*math.pi/2)
    if id:sub(1,3)=='gun'then localA=side*mix(.82,2.4,lift)*charge;dy=dy-24*charge end
   elseif clip=='raised'then glow=.65+.35*math.sin(u*tau)^2;if id:sub(1,3)=='gun'then localA=side*2.4;dy=dy-24 end
   elseif clip=='depart'then k=mix(1,.30,u);a=u*math.pi;glow=.5
   elseif clip=='far'then k=.30;glow=.7
   elseif clip=='arrive'then k=mix(.30,1,u);a=math.pi+math.pi*u;glow=.5*(1-u)
   elseif clip=='turn'then k=.70;a=i*tau/n
   elseif clip=='grow'then k=mix(.70,1,u)
   end
   if id:sub(1,4)=='wing'then localA=side*(-.14+math.sin(u*tau*2)*.16)end
   local c,s=math.cos(a),math.sin(a);local px,py=(dx*c-dy*s)*k,(dx*s+dy*c)*k
   local im=transform(base,piv,a+localA,k,size,glow);table.insert(frames,im);table.insert(hits,white(im));table.insert(poses,{x=px,y=py,a=a+localA,s=spec.scale*k})
  end
  register(id..'_'..clip,frames,{size/2,size/2},poses);register(id..'_'..clip..'_hit',hits,{size/2,size/2},poses)
 end
 print('module '..id)
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close()
print('HH52 authored exports complete')
