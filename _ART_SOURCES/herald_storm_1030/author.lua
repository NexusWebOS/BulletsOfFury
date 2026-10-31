local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor
local f=io.open(D..'/inputs.json','r');local cfg=json.decode(f:read('*a'));f:close()
local banks={};local tp={cfg.tornado.pivot[1],cfg.tornado.pivot[2]}
local function cell(a,i)local im=Image{fromFile=R..'/'..a.path};return Image(im,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch))end
local function write(name,frames,pivot,cols)
 local w=frames[1].width;local h=frames[1].height;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/24 end
 s:saveAs(D..'/'..name..'.aseprite');sheet:saveAs(D..'/'..name..'.png');s:close()
 banks[name]={key='hh69_'..name,path='assets/game/levels/stage_08/miniboss/herald_storm_1030/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot=pivot}
end
local function fade(im,a)local q=Image(im);for it in q:pixels()do local c=it();it(pc.rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),math.floor(pc.rgbaA(c)*a+.5)))end;return q end
local incoming={};local outgoing={};local alpha={.05,.12,.24,.40,.60,.78,.92,1}
for i=0,7 do table.insert(incoming,fade(cell(cfg.tornado,i),alpha[i+1]));table.insert(outgoing,fade(cell(cfg.tornado,(11+i)%16),i==7 and 0 or alpha[8-i]))end
write('arrive',incoming,tp,4);write('depart',outgoing,tp,4)
local flashes={}
for level=1,3 do for phase=0,15 do
 local im=cell(cfg.tornado,phase);local bolt=cell(cfg.lightning,phase);bolt:resize(26,188)
 local intensity=({.32,.64,1})[level];local offset=math.floor(math.sin(phase*1.9)*10)
 for it in im:pixels()do local c=it();local a=pc.rgbaA(c)
  if a>0 then local r=pc.rgbaR(c);local g=pc.rgbaG(c);local b=pc.rgbaB(c)
   r=math.min(255,r+(255-r)*intensity*.35);g=math.min(255,g+(r*.50-g)*intensity*.65);b=math.min(255,b+(r*.66-b)*intensity*.65)
   local bx=it.x-cfg.tornado.pivot[1]+13-offset;local by=it.y-2
   if a>40 and bx>=0 and bx<26 and by>=0 and by<188 then local v=bolt:getPixel(bx,by)
    if pc.rgbaA(v)>50 then r=255;g=math.max(g,235*intensity);b=math.max(b,245*intensity)end
   end
   it(pc.rgba(math.floor(r+.5),math.floor(g+.5),math.floor(b+.5),a))
  end
 end
 table.insert(flashes,im)
end end
write('flash',flashes,tp,8)
local bolts={}
for phase=0,15 do local im=cell(cfg.lightning,phase);im:resize(26,188);local q=Image(64,224,ColorMode.RGB)
 for it in im:pixels()do local c=it();local a=pc.rgbaA(c);local reach=math.min(1,(phase+1)/5);local tail=phase<12 and 1 or (15-phase)/3
  if it.y<188*reach and a>0 then q:drawPixel(it.x+19,it.y+18,pc.rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),math.floor(a*tail+.5)))end
 end
 table.insert(bolts,q)
end
write('summon',bolts,{32,112},4)
write('warning',{cell(cfg.warning,0),cell(cfg.warning,1)},{32,32},2)
f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('Authored storm arrivals, departures,1015 lightning flashes, forming bolts and actual warning')
