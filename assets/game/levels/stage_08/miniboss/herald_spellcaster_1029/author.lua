-- Original GPT seal/orb + inspected native prism glass. All transforms authored offline.
local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2
local f=io.open(D..'/inputs.json','r');local cfg=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(r),math.floor(g),math.floor(b),math.floor(a))end
local function clamp(x,l,h)return math.max(l,math.min(h,x))end
local function register(name,frames,piv,cols)
 local w,h=frames[1].width,frames[1].height;cols=cols or 4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB)
 local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='hs53_'..name,path='assets/game/levels/stage_08/miniboss/herald_spellcaster_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=piv}
end
local function fitSource(file,size)
 local src=Image{fromFile=D..'/'..file};local b=cfg.bounds[file];src=Image(src,Rectangle(b[1],b[2],b[3]-b[1],b[4]-b[2]));local k=size/math.max(src.width,src.height);src:resize(math.floor(src.width*k+.5),math.floor(src.height*k+.5));return src
end
local function white(im)
 local out=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then out:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return out
end
local function xform(src,size,a,k,glow)
 local out=Image(size,size,ColorMode.RGB);local c,s=math.cos(a),math.sin(a);local half=size/2
 for y=0,size-1 do for x=0,size-1 do local dx,dy=x-half,y-half;local sx=math.floor((dx*c+dy*s)/k+src.width/2);local sy=math.floor((-dx*s+dy*c)/k+src.height/2)
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height then local v=src:getPixel(sx,sy);if pc.rgbaA(v)>0 then
   if glow>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);v=rgba(math.min(255,r+glow*65),math.min(255,g+glow*70),math.min(255,b+glow*85),pc.rgbaA(v))end
   out:drawPixel(x,y,v)end end
 end end;return out
end
local seal=fitSource('gpt_seal.png',240);local base=xform(seal,256,0,1,0)
-- Assign each pixel of the generated inner star to its nearest original line.
-- Measured five vertices on this generated plate; preserve the source's actual geometry.
local pts={{128,70},{197,112},{170,186},{88,186},{59,112}}
local order={1,3,5,2,4,1};local pixels={}
for p in base:pixels()do local v=p();if pc.rgbaA(v)>0 then
 local dx,dy=p.x-128,p.y-128;local rad=math.sqrt(dx*dx+dy*dy);local best,segment,along=1e9,0,0
 for j=1,5 do local a,b=pts[order[j]],pts[order[j+1]];local vx,vy=b[1]-a[1],b[2]-a[2];local u=clamp(((p.x-a[1])*vx+(p.y-a[2])*vy)/(vx*vx+vy*vy),0,1);local d=(p.x-a[1]-u*vx)^2+(p.y-a[2]-u*vy)^2
  if d<best then best=d;segment=j-1;along=u end end
 local ang=(math.atan(dy,dx)+math.pi/2)%tau
 table.insert(pixels,{x=p.x,y=p.y,c=v,r=rad,segment=segment,along=along,ang=ang,dist=math.sqrt(best)})
end end
local build={};for f=0,55 do local out=Image(256,256,ColorMode.RGB);local line=f/6;local circle=clamp((f-30)/24,0,1)
 for _,p in ipairs(pixels)do local show=false
  if p.r<93 then show=(p.dist<12 and p.segment+p.along<=line)or f>=30
  else show=f>=30 and p.ang/tau<=circle end
  if f>=54 then show=true end
  if show then out:drawPixel(p.x,p.y,p.c)end
 end;table.insert(build,out)
end;register('seal_build',build,{128,128})
local spin={};for i=0,31 do table.insert(spin,xform(seal,360,i*tau/32,1,.1))end;register('seal_spin',spin,{180,180})
local pulse={};for i=0,23 do local u=i/23;local k=u<.36 and 1+.26*u/.36 or u<.86 and 1.26-.30*(u-.36)/.50 or .96+.04*(u-.86)/.14;table.insert(pulse,xform(seal,448,i*tau/32,k,math.sin(u*math.pi)*.85))end;register('seal_pulse',pulse,{224,224})
local burstsource=xform(seal,360,23*tau/32,1,0);local bp={};for p in burstsource:pixels()do if pc.rgbaA(p())>0 then table.insert(bp,{x=p.x,y=p.y,c=p()})end end
local burst={};for f=0,15 do local out=Image(544,544,ColorMode.RGB);local u=f/15
 for _,p in ipairs(bp)do local a=math.floor((math.atan(p.y-180,p.x-180)+math.pi)/tau*12)*tau/12-math.pi+tau/24;local dist=u*86
  local x=math.floor(p.x+92+math.cos(a)*dist+.5);local y=math.floor(p.y+92+math.sin(a)*dist+.5);local v=p.c
  local alpha=pc.rgbaA(v)*math.max(0,1-u)^.6;if f<3 then v=rgba(255,130+f*20,145+f*20,alpha)else v=rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),alpha)end
  if x>=0 and y>=0 and x<544 and y<544 then out:drawPixel(x,y,v)end
 end;table.insert(burst,out)
end;register('seal_burst',burst,{272,272})
local orb=fitSource('gpt_penta_ball.png',48);local roll,hot={},{ }
for f=0,31 do table.insert(roll,xform(orb,72,f*tau/32,1,.18*math.sin(f*tau/16)^2))end;register('orb',roll,{36,36})
for f=0,15 do table.insert(hot,xform(orb,80,f*tau/16,1+.18*math.sin(f*math.pi/15),.3+.6*f/15))end;register('orb_hot',hot,{40,40})
-- Glass is the actual game's prism shard, recolored offline, including its white glints.
local shards={};local sources={}
local function red(im)
 local o=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local v=p();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b)
  if mx>175 and mn>105 then r=255;g=mx*.82;b=mx*.87
  elseif mx-mn>18 then r=math.min(255,mx*1.08);g=mx*.13;b=mx*.27 end;o:drawPixel(p.x,p.y,rgba(r,g,b,a))end end;return o
end
for i=0,7 do local im=red(Image{fromFile=R..'/assets/game/levels/stage_09/projectiles/s9_attacks/warpprismshard_'..i..'.png'});local k=34/im.height;im:resize(math.floor(im.width*k+.5),34);sources[i+1]=im end
for heading=0,31 do for cycle=0,7 do table.insert(shards,xform(sources[cycle+1],48,heading*tau/32+math.pi/2,1,cycle/24))end end;register('glass_shard',shards,{24,24},8)
local impacts={};for f=0,15 do local out=Image(160,160,ColorMode.RGB);local u=f/15;local orbflash=xform(orb,160,f*tau/16,math.max(.1,1-u),.7*(1-u));out:drawImage(orbflash)
 for i=0,11 do local a=i*tau/12+f*.04;local s=xform(sources[f%8+1],48,a+math.pi/2,1-u*.4,.3*(1-u));local faded=Image(48,48,ColorMode.RGB)
  for p in s:pixels()do local c=p();if pc.rgbaA(c)>0 then faded:drawPixel(p.x,p.y,rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)*(1-u)))end end
  out:drawImage(faded,Point(math.floor(56+math.cos(a)*u*51),math.floor(56+math.sin(a)*u*51)))
 end;table.insert(impacts,out)
end;register('orb_shatter',impacts,{80,80})
-- Animated eyes/jaw retained from the existing Herald's source head, with authored 1015 emission.
local H=cfg.art.head_grin;local headsheet=Image{fromFile=R..'/'..H.path};local heads,hits={},{}
for f=0,31 do local index=f%16;local im=Image(headsheet,Rectangle(index%H.cols*H.cw,math.floor(index/H.cols)*H.ch,H.cw,H.ch));local out=Image(128,144,ColorMode.RGB);local pulse=.35+.65*math.sin(f*tau/32)^2
 for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c);if r>g*1.35 and r>b*.9 and r>45 then r=255;g=math.min(240,g+110*pulse);b=math.min(240,b+90*pulse)end
  local x,y=p.x+64-H.pivot[1],p.y+104-H.pivot[2];out:drawPixel(x,y,rgba(r,g,b,pc.rgbaA(c)))
  if pc.rgbaR(c)>pc.rgbaG(c)*1.5 and pc.rgbaR(c)>100 then for dx=-2,2,2 do for dy=-2,2,2 do local xx,yy=x+dx,y+dy;if xx>=0 and yy>=0 and xx<128 and yy<144 and pc.rgbaA(out:getPixel(xx,yy))==0 then out:drawPixel(xx,yy,rgba(245,12,45,115*pulse))end end end end
 end end;table.insert(heads,out);table.insert(hits,white(out))
end;register('head_cast',heads,{64,104});register('head_cast_hit',hits,{64,104})
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('HS53 complete')
