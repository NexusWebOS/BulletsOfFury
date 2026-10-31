local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2
local function read(n)local f=io.open(D..'/'..n,'r');local c=json.decode(f:read('*a'));f:close();return c end
local C=read('inputs.json');local dna=read('dna.json');local data=read('d20.json');local banks={}
local function clamp(x,l,h)return math.max(l,math.min(h,x))end
local function mix(a,b,t)return a+(b-a)*t end
local function rgba(r,g,b,a)return pc.rgba(math.floor(clamp(r,0,255)),math.floor(clamp(g,0,255)),math.floor(clamp(b,0,255)),math.floor(clamp(a,0,255)))end
local function recolor(im,kind,power)
 local out=Image(im.width,im.height,ColorMode.RGB)
 for p in im:pixels()do local v=p();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b)
  if kind=='bomb'then
   if r>g*1.35 and b>g*1.35 then r,g,b=mx*.76,mn*.75,mx
   elseif g>r*1.12 and g>b*1.08 then r,g,b=mx,mn*.20,mn*.35
   elseif b>r*1.22 then r,g,b=mx*.76,mx*.73,mx*.79
   elseif g>r*1.08 and b>r*1.15 then r,g,b=mx*.96,mx*.92,mx end
  elseif kind=='purple'or kind=='red'then if g>r*1.13 and g>b*1.08 then if kind=='purple'then r,g,b=mx*.76,mn*.5,mx else r,g,b=mx,mn*.30,mn*.40 end end
  elseif kind=='charge'then local u=power or 0;if g>r*1.25 and g>b*1.25 then r,g,b=mix(r,255,u),mix(g,20,u),mix(b,45,u)elseif mx-mn>24 then r,g,b=mix(r,mx,u),mix(g,mn*.08,u),mix(b,mx*.15,u)else r,g,b=r+u*34,g*(1-u*.42),b*(1-u*.30)end end
  out:drawPixel(p.x,p.y,rgba(r,g,b,a))end end;return out
end
local function white(im)local o=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then o:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return o end
local function fade(im,k)local o=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then o:drawPixel(p.x,p.y,rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)*k))end end;return o end
local function register(n,frames,pivot,extra,hit)
 local w,h=frames[1].width,frames[1].height;local cols=4;if math.ceil(#frames/4)*h>4096 then cols=8 end
 local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local spr=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],i,im,Point(0,0));spr.frames[i].duration=1/24 end
 sheet:saveAs(D..'/'..n..'.png');spr:saveAs(D..'/'..n..'.aseprite');spr:close()
 local a={key='rd71_'..n,path='assets/game/levels/stage_08/boss/possession_1030/'..n..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot={pivot[1],pivot[2]}};for k,v in pairs(extra or{})do a[k]=v end;banks[n]=a
 if hit then local a={};for _,im in ipairs(frames)do table.insert(a,white(im))end;register(n..'_hit',a,pivot,extra,false)end
end
local function transformed(src,piv,a,k,w,h)
 local out=Image(w,h,ColorMode.RGB);local c,s=math.cos(a),math.sin(a)
 for y=0,h-1 do for x=0,w-1 do local dx,dy=x-w/2,y-h/2;local xx=math.floor((dx*c+dy*s)/k+piv[1]+.5);local yy=math.floor((-dx*s+dy*c)/k+piv[2]+.5);if xx>=0 and yy>=0 and xx<src.width and yy<src.height then out:drawPixel(x,y,src:getPixel(xx,yy))end end end;return out
end
local toxic=Image{fromFile=R..'/assets/game/levels/stage_07/effects/stage7_modular_0927/portal_16.png'}
for _,q in ipairs({{'purple',256},{'red',192}})do local frames={};for i=0,15 do local x0=math.floor(i%4*1254/4);local y0=math.floor(math.floor(i/4)*1254/4);local im=Image(toxic,Rectangle(x0,y0,313,313));im=recolor(im,q[1]);im:resize(q[2],q[2]);table.insert(frames,im)end;for i=1,8 do table.insert(frames,fade(frames[16],1-i/8))end;register('gate_'..q[1],frames,{q[2]/2,q[2]/2})end
local ufo=Image{fromFile=D..'/gpt_dracodia_ufo.png'};local frames={}
for i=0,15 do local im=Image(ufo,Rectangle(math.floor(i%4*ufo.width/4),math.floor(math.floor(i/4)*ufo.height/4),math.floor(ufo.width/4),math.floor(ufo.height/4)));im:resize(100,100);local o=Image(112,112,ColorMode.RGB);o:drawImage(im,Point(6,6));table.insert(frames,o)end;register('ufo',frames,{56,56})
local emerging={};for i=0,15 do table.insert(emerging,transformed(frames[i+1],{56,56},0,.35+.65*i/15,112,112))end;register('ufo_emerge',emerging,{56,56})
local drone=Image{fromFile=R..'/'..C.drone.path};local body=Image(256,256,ColorMode.RGB);local arms={left=Image(256,256,ColorMode.RGB),right=Image(256,256,ColorMode.RGB)}
for p in drone:pixels()do local v=p();if pc.rgbaA(v)>0 then local id=p.y>117 and p.x<111 and'left'or p.y>117 and p.x>145 and'right'or'core';if id=='core'then body:drawPixel(p.x,p.y,v)else arms[id]:drawPixel(p.x,p.y,v)end end end
local function posed(lift,power,look)
 local out=Image(320,320,ColorMode.RGB);local face=Image(body)
 -- Move the actual aperture pixels inside its own black eye socket.
 local eye=Image(24,13,ColorMode.RGB);for y=98,110 do for x=116,139 do local c=face:getPixel(x,y);if pc.rgbaG(c)>pc.rgbaR(c)*1.25 and pc.rgbaG(c)>pc.rgbaB(c)*1.25 then eye:drawPixel(x-116,y-98,c);face:drawPixel(x,y,rgba(17,20,19,pc.rgbaA(c)))end end end
 face:drawImage(eye,Point(116+look,98));face=recolor(face,'charge',power)
 for _,id in ipairs({'left','right'})do local side=id=='left'and-1 or 1;local piv={id=='left'and 83 or 173,117};local a=-side*lift*2.25;local im=transformed(recolor(arms[id],'charge',power),piv,a,1.22,320,320);out:drawImage(im,Point(math.floor((piv[1]-128)*1.22),math.floor((piv[2]-128)*1.22)))end
 local im=transformed(face,{128,128},0,1.22,320,320);out:drawImage(im)
 if power>0 then local g=Image(320,320,ColorMode.RGB);for p in out:pixels()do local v=p();if pc.rgbaA(v)>100 then for _,d in ipairs({{-2,0},{2,0},{0,-2},{0,2}})do local x,y=p.x+d[1],p.y+d[2];if x>=0 and y>=0 and x<320 and y<320 then g:drawPixel(x,y,rgba(255,9,42,60+power*100))end end end end;g:drawImage(out);out=g end
 return out
end
local emerge,ready,charge={},{},{}
for i=0,23 do local src=posed(0,0,0);local im=transformed(src,{160,160},0,.35+.65*i/23,320,320);table.insert(emerge,im)end
for i=0,15 do table.insert(ready,posed(i/15*.55,0,math.floor(math.sin(i*tau/16)*3)))end
for i=0,63 do local u=i/63;table.insert(charge,posed(clamp(u*1.4,0,1),u,math.floor(math.sin(u*tau*3)*3)))end
register('drone_emerge',emerge,{160,160});register('drone_ready',ready,{160,160});register('drone_charge',charge,{160,160})
-- Reuse actual native code-bomb charge and burst pixels, baked to final display sizes.
for _,q in ipairs({{'bomb_charge',64},{'bomb_burst',180}})do local a={};for _,v in ipairs(data.fx[q[1]].frames)do local im=Image{fromFile=R..'/'..v.path};im:resize(q[2],q[2]);im=recolor(im,'bomb');table.insert(a,im)end;register(q[1],a,{q[2]/2,q[2]/2})end
-- Source-glyph helices: rear/front layering and the fade are stored frame pixels.
local codes=Image{fromFile=R..'/'..dna.code.path};local helix={back={},front={},arriveBack={},arriveFront={}}
for i=0,47 do local back=Image(384,384,ColorMode.RGB);local front=Image(384,384,ColorMode.RGB)
 for side=0,1 do for j=0,31 do local u=j/31;local angle=u*tau*1.6-i*tau/24+side*math.pi;local x=192+math.sin(angle)*(74+16*math.sin(u*math.pi));local y=338-u*300;local z=math.cos(angle);local f=(i+math.floor(u*11))%12
  local tile=Image(codes,Rectangle(f%4*362+149,math.floor(f/4)*362+96+((j*7+i*4)%192),52,52));tile:resize(22,22);(z>0 and front or back):drawImage(tile,Point(math.floor(x-11),math.floor(y-11)))
 end end
 table.insert(helix.back,back);table.insert(helix.front,front);if i<8 then table.insert(helix.arriveBack,fade(back,(i+1)/8));table.insert(helix.arriveFront,fade(front,(i+1)/8))end
end
register('helix_back',helix.back,{192,192});register('helix_front',helix.front,{192,192});register('helix_in_back',helix.arriveBack,{192,192});register('helix_in_front',helix.arriveFront,{192,192})
-- Pose-specific anatomical seams include the complete shoulder from its crown.
-- The union reconstructs the exact original body; no horizontal frame strip is removed.
local function boundary(y,lift)
 local ys={0,70,90,120,150,180,210,240,280,320,360,512};local xs={0,0,164,181,194,192,177,168,174+lift*15,190+lift*22,210,210}
 for i=1,#ys-1 do if y>=ys[i]and y<=ys[i+1]then return mix(xs[i],xs[i+1],(y-ys[i])/(ys[i+1]-ys[i]))end end;return 0
end
for _,name in ipairs({'dracodia_wind','dracodia_strike','dracodia_recover'})do local a=C.bi.banks[name];local sheet=Image{fromFile=R..'/'..C.bi.sheets[name].path};local split={core={},left={},right={}}
 for i=0,a.count-1 do local src=Image(sheet,Rectangle(i%a.cols*512,math.floor(i/a.cols)*512,512,512));local out={core=Image(512,512,ColorMode.RGB),left=Image(512,512,ColorMode.RGB),right=Image(512,512,ColorMode.RGB)}
  local lift=name=='dracodia_wind'and clamp(i/8,0,1)or name=='dracodia_strike'and(1-clamp(i/2,0,1))or 0
  for p in src:pixels()do local c=p();if pc.rgbaA(c)>0 then local b=boundary(p.y,lift);local id=p.x<b and'left'or p.x>512-b and'right'or'core';out[id]:drawPixel(p.x,p.y,c)end end
  for _,id in ipairs({'core','left','right'})do out[id]:resize(360,360);table.insert(split[id],out[id])end
 end
 for _,id in ipairs({'core','left','right'})do register('host_'..name..'_'..id,split[id],{180,180},nil,true)end
 print('whole shoulders '..name)
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('RD71 authored banks complete')
