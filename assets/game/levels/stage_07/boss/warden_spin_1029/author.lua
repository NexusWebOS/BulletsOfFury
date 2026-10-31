local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2;local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(r),math.floor(g),math.floor(b),math.floor(a))end
local function register(name,frames,pivot)
 local w,h=frames[1].width,frames[1].height;local cols=4;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='ws56_'..name,path='assets/game/levels/stage_07/boss/warden_spin_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot}
end
local head=Image{fromFile=R..'/'..C.head};head=Image(head,Rectangle(1188,610,330,329));local l,t,r,b=head.width,head.height,0,0
for p in head:pixels()do if pc.rgbaA(p())>0 then l=math.min(l,p.x);t=math.min(t,p.y);r=math.max(r,p.x);b=math.max(b,p.y)end end
head=Image(head,Rectangle(l,t,r-l+1,b-t+1));head:resize(47,43)
local function composite(i)
 local a=C.core;local sheet=Image{fromFile=R..'/'..a.path};local im=Image(sheet,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch));local out=Image(256,256,ColorMode.RGB)
 out:drawImage(im,Point(128-a.pivot[1],128-a.pivot[2]));out:drawImage(head,Point(105,142));return out
end
local function turn(im,a)
 local out=Image(288,288,ColorMode.RGB);local c,s=math.cos(a),math.sin(a)
 for y=0,287 do for x=0,287 do local dx,dy=x-144,y-144;local xx=math.floor(dx*c+dy*s+128);local yy=math.floor(-dx*s+dy*c+128)
  if xx>=0 and yy>=0 and xx<256 and yy<256 then local v=im:getPixel(xx,yy);if pc.rgbaA(v)>0 then out:drawPixel(x,y,v)end end
 end end;return out
end
local function white(im)local out=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then out:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return out end
local spin,hit,shadow,front,frontHit={},{},{},{},{}
for i=0,31 do local im=turn(composite(i%16),i*tau/32);table.insert(spin,im);table.insert(hit,white(im));local sh=Image(192,96,ColorMode.RGB)
 for y=0,95 do for x=0,191 do local xx=math.floor((x-96)/.62+144);local yy=math.floor((y-48)/.24+144);if xx>=0 and xx<288 and yy>=0 and yy<288 then local c=im:getPixel(xx,yy);if pc.rgbaA(c)>0 then sh:drawPixel(x,y,rgba(4,10,6,pc.rgbaA(c)*.46))end end end end;table.insert(shadow,sh)
end
for i=0,15 do local im=turn(composite(i),0);table.insert(front,im);table.insert(frontHit,white(im))end
register('core',spin,{144,144});register('core_hit',hit,{144,144});register('front',front,{144,144});register('front_hit',frontHit,{144,144});register('shadow',shadow,{96,48})
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('WS56 authored source spin')
