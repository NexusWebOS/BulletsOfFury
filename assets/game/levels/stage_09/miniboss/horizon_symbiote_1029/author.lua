local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2;local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(math.max(0,math.min(255,r))),math.floor(math.max(0,math.min(255,g))),math.floor(math.max(0,math.min(255,b))),math.floor(math.max(0,math.min(255,a))))end
local function register(name,frames,pivot,cols)
 local w,h=frames[1].width,frames[1].height;cols=cols or 8;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/30 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='eh57_'..name,path='assets/game/levels/stage_09/miniboss/horizon_symbiote_1029/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot}
end
local function aqua(v)
 local r,g,b,a=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b)
 if mx-mn<24 and mx<180 then return rgba(r*.42,g*.84+mx*.30,b*.90+mx*.42,a)end
 if mx-mn<30 and mn>180 then return rgba(255,255,255,a)end
 return rgba(mx*.22,mx*.94,mx,a)
end
local ships,water,hits,eyes,whiteeyes={},{},{},{},{}
for frame=0,31 do
 local j=C.selection[frame+1];local src=Image{fromFile=D..'/spin/'..string.format('%02d',j)..'.png'};local pivot=C.anchors[j+1];local a=frame*tau/32-C.angles[j+1];local co,si=math.cos(a),math.sin(a);local out=Image(384,384,ColorMode.RGB)
 for y=0,383 do for x=0,383 do local dx,dy=(x-192)/1.25,(y-192)/1.25;local xx=math.floor(dx*co+dy*si+pivot[1]);local yy=math.floor(-dx*si+dy*co+pivot[2]);if xx>=0 and yy>=0 and xx<256 and yy<256 then local v=src:getPixel(xx,yy);if pc.rgbaA(v)>32 then out:drawPixel(x,y,v)end end end end
 for p in out:pixels()do local v=p();local r,g,b,al=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b);if al>0 and mx-mn<24 and mx>25 and mx<150 then p(rgba(r*1.3+6,g*1.4+8,b*1.55+12,al))end end
 local wet=Image(384,384,ColorMode.RGB);local white=Image(384,384,ColorMode.RGB);local pulse=.3+.7*math.sin(frame*tau/16)^2
 for p in out:pixels()do local v=p();if pc.rgbaA(v)>64 then for _,d in ipairs({{-2,0},{2,0},{0,-2},{0,2}})do local x,y=p.x+d[1],p.y+d[2];if x>=0 and y>=0 and x<384 and y<384 then wet:drawPixel(x,y,rgba(35,220,255,45+pulse*100))end end end end
 for p in out:pixels()do local v=p();local al=pc.rgbaA(v);if al>0 then local c=aqua(v);wet:drawPixel(p.x,p.y,rgba(pc.rgbaR(c)+pulse*12,pc.rgbaG(c)+pulse*22,pc.rgbaB(c)+pulse*26,al));white:drawPixel(p.x,p.y,rgba(255,255,255,al))end end
 table.insert(ships,out);table.insert(water,wet);table.insert(hits,white)
 for phase=0,7 do local e=Image(80,80,ColorMode.RGB);local ew=Image(80,80,ColorMode.RGB);local strength=phase/7
  for y=155,229 do for x=155,229 do local v=out:getPixel(x,y);local r,g,b,al=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v)
   if al>0 and g>80 and b>100 and g>r*1.12 and (x-192)^2+(y-192)^2<900 then local xx,yy=x-152,y-152
    for _,d in ipairs({{-2,0},{2,0},{0,-2},{0,2}})do e:drawPixel(xx+d[1],yy+d[2],rgba(35,170,255,35+strength*115));ew:drawPixel(xx+d[1],yy+d[2],rgba(185,255,255,50+strength*145))end
   end end end
  for y=155,229 do for x=155,229 do local v=out:getPixel(x,y);local r,g,b,al=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),pc.rgbaA(v)
   if al>0 and g>80 and b>100 and g>r*1.12 and (x-192)^2+(y-192)^2<900 then e:drawPixel(x-152,y-152,rgba(r+strength*160,g+strength*70,b+strength*40,al));ew:drawPixel(x-152,y-152,rgba(220+35*strength,250+5*strength,255,al))end
  end end;table.insert(eyes,e);table.insert(whiteeyes,ew)
 end
end
register('ship',ships,{192,192});register('ship_water',water,{192,192});register('ship_hit',hits,{192,192});register('eye_glow',eyes,{40,40},16);register('eye_white',whiteeyes,{40,40},16)
local raw=Image{fromFile=D..'/beam.png'};local segment=Image(raw,Rectangle(96,20,128,56));segment:resize(64,28)
local beam,beamwater,dashes={},{},{}
local function turn(src,size,a,cx,cy)
 local out=Image(size,size,ColorMode.RGB);local c,s=math.cos(a),math.sin(a)
 for y=0,size-1 do for x=0,size-1 do local dx,dy=x-size/2,y-size/2;local xx=math.floor(dx*c+dy*s+cx);local yy=math.floor(-dx*s+dy*c+cy);if xx>=0 and yy>=0 and xx<src.width and yy<src.height then local v=src:getPixel(xx,yy);if pc.rgbaA(v)>0 then out:drawPixel(x,y,v)end end end end;return out
end
for dir=0,63 do for phase=0,15 do local flow=Image(64,28,ColorMode.RGB);local wf=Image(64,28,ColorMode.RGB)
 for y=0,27 do for x=0,63 do local c=segment:getPixel((x+phase*4)%64,y);flow:drawPixel(x,y,c);wf:drawPixel(x,y,aqua(c))end end
 table.insert(beam,turn(flow,80,dir*tau/64,32,14));table.insert(beamwater,turn(wf,80,dir*tau/64,32,14))
 if phase%2==0 then table.insert(dashes,turn(wf,80,dir*tau/64,32,14))end
end end
register('beam',beam,{40,40},16);register('beam_water',beamwater,{40,40},16);register('dash',dashes,{40,40},16)
local orbsource=Image{fromFile=D..'/orb_0.png'};orbsource:resize(72,72);local orbs,orbwet={},{ }
for phase=0,15 do local im=turn(orbsource,112,phase*tau/16,36,36);local wet=Image(112,112,ColorMode.RGB);for p in im:pixels()do if pc.rgbaA(p())>0 then wet:drawPixel(p.x,p.y,aqua(p()))end end;table.insert(orbs,im);table.insert(orbwet,wet)end
register('orb',orbs,{56,56});register('orb_water',orbwet,{56,56})
local smokes={};for phase=0,15 do local row=C.smoke[phase%8+1];local c=row.cell;local src=Image{fromFile=R..'/'..row.path};local im=Image(src,Rectangle(c[2],c[3],c[4],c[5]));im:resize(48,64);local out=Image(80,96,ColorMode.RGB);out:drawImage(im,Point(16,24));table.insert(smokes,out)end
register('smoke',smokes,{40,80})
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('EH57 authored banks complete')
