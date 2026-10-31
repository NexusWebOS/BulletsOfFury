local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2
local f=io.open(D..'/inputs.json','r');local cfg=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(math.min(255,r)),math.floor(math.min(255,g)),math.floor(math.min(255,b)),math.floor(math.min(255,a)))end
local function cell(a,index)local s=Image{fromFile=R..'/'..a.path};return Image(s,Rectangle(index%a.cols*a.cw,math.floor(index/a.cols)*a.ch,a.cw,a.ch))end
local function front(i)local out=Image(224,288,ColorMode.RGB);for _,v in ipairs({{cfg.core,0,0,0},{cfg.head,i%32,0,-12}})do local a=v[1];out:drawImage(cell(a,v[2]),Point(112+v[3]-a.pivot[1],144+v[4]-a.pivot[2]))end;return out end
local function glow(im,strength)
 local out=Image(im.width,im.height,ColorMode.RGB);local points={}
 for p in im:pixels()do local v=p();if pc.rgbaA(v)>64 then table.insert(points,{p.x,p.y,v})end end
 for _,p in ipairs(points)do for _,d in ipairs({{-4,0},{4,0},{0,-4},{0,4},{-2,-2},{2,-2},{-2,2},{2,2}})do local x,y=p[1]+d[1],p[2]+d[2];if x>=0 and y>=0 and x<im.width and y<im.height then out:drawPixel(x,y,rgba(245,8,28,45+strength*100))end end end
 for _,p in ipairs(points)do local c=p[3];local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c);local lift=12+strength*70
  out:drawPixel(p[1],p[2],rgba(r+lift,g*(.55-strength*.25),b*(.65-strength*.25),pc.rgbaA(c)))end;return out
end
local function white(im)local out=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then out:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return out end
local function transformed(src,w,h,scale,angle)
 local out=Image(w,h,ColorMode.RGB);local c,s=math.cos(angle or 0),math.sin(angle or 0)
 for y=0,h-1 do for x=0,w-1 do local dx,dy=x-w/2,y-h/2;local xx=math.floor((dx*c+dy*s)/scale+src.width/2);local yy=math.floor((-dx*s+dy*c)/scale+src.height/2)
  if xx>=0 and yy>=0 and xx<src.width and yy<src.height then local v=src:getPixel(xx,yy);if pc.rgbaA(v)>0 then out:drawPixel(x,y,v)end end
 end end;return out
end
local function register(name,frames,pivot,extra,hit)
 local w,h=frames[1].width,frames[1].height;local cols=4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close()
 local a={key='hd54_'..name,path='assets/game/levels/stage_08/miniboss/herald_desperation_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot};for k,v in pairs(extra or{})do a[k]=v end;banks[name]=a
 if hit then local frames2={};for _,im in ipairs(frames)do table.insert(frames2,white(im))end;register(name..'_hit',frames2,pivot,extra,false)end
end
local fronts,charge,depart,arrive={},{},{},{}
for i=0,31 do local im=front(i);local p=math.sin(i*tau/32)^2;table.insert(fronts,glow(im,p));table.insert(charge,glow(transformed(im,144,164,.46,0),p))end
register('front',fronts,{112,144},nil,true);register('charge',charge,{72,82})
for i=0,23 do table.insert(depart,glow(transformed(front(i),224,288,1-.54*i/23,0),.7));table.insert(arrive,glow(transformed(front(i),224,288,.46+.54*i/23,0),.3))end
register('depart',depart,{112,144});register('return',arrive,{112,144},nil,true)
local spin,sockets={},{}
for i=0,31 do local j=cfg.selection[i+1] or i;local im=Image{fromFile=D..'/frames/'..string.format('%02d',j)..'.png'}
 local k=cfg.turnScale;local fixed=transformed(im,144,164,k,0);table.insert(spin,glow(fixed,.35+.65*math.sin(i*tau/16)^2))
 table.insert(sockets,{math.floor(math.sin(i*tau/32)*7),-16})
end;register('spin',spin,{72,82},{sockets=sockets})
-- The actual Falva sphere, never the old helix-mass substitute.
local rollers={};for i=1,4 do local a=cfg.rollers[i];local s=Image{fromFile=R..'/'..a.path};local c=a.cell;local im=Image(s,Rectangle(c[2],c[3],c[4],c[5]));local out=Image(im.width,im.height,ColorMode.RGB)
 for p in im:pixels()do local v=p();local alpha=pc.rgbaA(v);if alpha>32 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b)
  if mx<68 then r=mx*.40;g=mx*.08;b=mx*.12 elseif mn>145 then r=255;g=mn*.55;b=mn*.58 else r=math.min(255,mx*1.12);g=mx*.07;b=mx*.14 end
  out:drawPixel(p.x,p.y,rgba(r,g,b,alpha))end end;rollers[i]=out
 if i==1 then out:saveAs(D..'/falva-red-reference.png')end
end
for depth=0,9 do local frames={};local d=12+depth*6
 -- Preserve the dark panel network; Falva's fully white charge-stage plates
 -- would erase the requested red/black structure when recolored.
 for i=0,31 do local src=rollers[1];local k=d/math.max(src.width,src.height);table.insert(frames,glow(transformed(src,88,88,k,i*tau/32),.35+.65*math.sin(i*tau/16)^2))end
 register('orb_'..depth,frames,{44,44},{diameter=d})
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('HD54 banks '..tostring(#spin))
