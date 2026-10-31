local W=app.params['work'] or 'C:/Users/Mike/Documents/New project/BOF-Riders-Defense-1029/'
if W:sub(-1)~='/'then W=W..'/'end
local pc=app.pixelColor
local function gold(c,p)
 local r,g,b,a=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c);local hi,lo=math.max(r,g,b),math.min(r,g,b)
 if hi-lo>12 and hi>40 then r=hi;g=math.floor(lo+(hi-lo)*.76);b=math.floor(lo+(hi-lo)*.10);r=math.floor(r+(255-r)*p);g=math.floor(g+(245-g)*p);b=math.floor(b+(150-b)*p)end
 return pc.rgba(r,g,b,a)
end
local function save(name,cells,w,h,cols)
 local sp=Sprite(w,h,ColorMode.RGB);local sheet=Image(w*cols,h*math.ceil(#cells/cols),ColorMode.RGB)
 for i,im in ipairs(cells)do if i>1 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],i,im,Point(0,0));sp.frames[i].duration=1/24;sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h))end
 sp:saveAs(W..name..'.aseprite');sheet:saveAs(W..name..'.png');sp:close()
end
local ship=Image{fromFile=W..'ship_decker.png'};ship:resize(52,60)
local aura={};local mask={};for y=0,127 do mask[y]={};for x=0,127 do local sx,sy=x-38,y-34;mask[y][x]=sx>=0 and sy>=0 and sx<52 and sy<60 and pc.rgbaA(ship:getPixel(sx,sy))>80 end end
local edge={};for y=8,119 do edge[y]={};for x=8,119 do
 if not mask[y][x]then local d=99;for yy=math.max(0,y-12),math.min(127,y+12)do for xx=math.max(0,x-12),math.min(127,x+12)do if mask[yy][xx]then d=math.min(d,math.sqrt((xx-x)^2+(yy-y)^2))end end end;edge[y][x]=d end
end end
local pulse={.10,.22,.40,.65,.85,1,.85,.65,.40,.22}
for f=0,15 do local im=Image(128,128,ColorMode.RGB);local p=pulse[f%10+1]
 for y=8,119 do for x=8,119 do local d=edge[y][x];if d and d<=3+9*p then local a=math.floor((1-d/15)*(75+110*p));if d<2 then im:drawPixel(x,y,pc.rgba(255,240,155,230))else im:drawPixel(x,y,pc.rgba(255,165+math.floor(70*p),25,a))end end end end
 aura[#aura+1]=im end
save('decker_charge',aura,128,128,8)
local orb=Image{fromFile=W..'orb_source.png'};orb:resize(40,40);local shots={}
for f=0,15 do local im=Image(64,64,ColorMode.RGB);local a=f*math.pi*2/16;local ca,sa=math.cos(a),math.sin(a)
 for y=0,63 do for x=0,63 do local dx,dy=x-31.5,y-31.5;local sx=math.floor(ca*dx+sa*dy+20);local sy=math.floor(-sa*dx+ca*dy+20);if sx>=0 and sy>=0 and sx<40 and sy<40 then im:drawPixel(x,y,gold(orb:getPixel(sx,sy),pulse[f%10+1]*.3))end end end
 shots[#shots+1]=im end;save('shield_seed',shots,64,64,8)
local wall=Image{fromFile=W..'rr26_wall.png'};local tile=Image(356,96,ColorMode.RGB);tile:drawImage(wall,Point(-14,-32));tile:resize(160,44);local tiles={}
for f=0,39 do local im=Image(480,64,ColorMode.RGB);local opening=f<16 and (f+1)/16 or 1;local fading=f>=32 and (40-f)/8 or 1;local p=pulse[f%10+1]*.35
 for y=0,43 do for x=0,479 do if math.abs(x-239.5)<240*opening then local c=gold(tile:getPixel(x%160,y),p);local a=pc.rgbaA(c);im:drawPixel(x,y+10,pc.rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),math.floor(a*fading)))end end end;tiles[#tiles+1]=im end
save('gold_wall',tiles,480,64,8)
local arrow=Image{fromFile=W..'warn_escape_arrow_0916.png'};arrow:resize(32,24);local arrows={}
for d=0,3 do local im=Image(40,40,ColorMode.RGB);for y=0,23 do for x=0,31 do local dx,dy=x-15.5,y-11.5;local a=d*math.pi/2;local xx=math.floor(19.5+dx*math.cos(a)-dy*math.sin(a)+.5);local yy=math.floor(19.5+dx*math.sin(a)+dy*math.cos(a)+.5);im:drawPixel(xx,yy,arrow:getPixel(x,y))end end;arrows[#arrows+1]=im end;save('entry_arrows',arrows,40,40,4)
local star=Image{fromFile=W..'bmfx_alert_red_impact_imminent.png'};star:resize(34,34);local im=Image(40,40,ColorMode.RGB);im:drawImage(star,Point(3,3));save('entry_star',{im},40,40,1)
