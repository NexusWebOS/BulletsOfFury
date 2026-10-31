local W=app.params['work'];local R=app.params['root'];if W:sub(-1)~='/'then W=W..'/'end;if R:sub(-1)~='/'then R=R..'/'end
local pc=app.pixelColor
local function save(name,cells,cols)
 local w,h=cells[1].width,cells[1].height;local sp=Sprite(w,h,ColorMode.RGB);sp.layers[1].name=name;local sheet=Image(w*cols,h*math.ceil(#cells/cols),ColorMode.RGB)
 for i,im in ipairs(cells)do if i>1 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],i,im,Point(0,0));sp.frames[i].duration=1/18;sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h))end
 sp:saveAs(W..name..'.aseprite');sheet:saveAs(W..name..'.png');sp:close()
end
for _,name in ipairs{'wind_rear','wind_front'}do
 local src=Image{fromFile=R..'assets/game/levels/stage_06/boss/nightwing_stability_1028/'..name..'.png'};local cells={}
 for f=0,23 do local im=Image(src,Rectangle(f%8*384,math.floor(f/8)*384,384,384));im:resize(336,336);cells[#cells+1]=im end
 save(name,cells,8)
end
local src=Image{fromFile=R..'assets/game/levels/stage_06/boss/nightwing_wind_1028/clean_identity_1028b.png'};local masks={};local size=272
for pose,f in ipairs{0,8,16}do
 local im=Image(src,Rectangle(f%8*size,math.floor(f/8)*size,size,size));local solid,outside,dist={},{},{}
 for y=0,size-1 do solid[y]={};outside[y]={};dist[y]={};for x=0,size-1 do solid[y][x]=pc.rgbaA(im:getPixel(x,y))>30;dist[y][x]=99 end end
 local queue={};local at=1
 local function visit(x,y)if x>=0 and x<size and y>=0 and y<size and not solid[y][x]and not outside[y][x]then outside[y][x]=true;queue[#queue+1]={x,y}end end
 for x=0,size-1 do visit(x,0);visit(x,size-1)end;for y=0,size-1 do visit(0,y);visit(size-1,y)end
 while at<=#queue do local p=queue[at];at=at+1;visit(p[1]-1,p[2]);visit(p[1]+1,p[2]);visit(p[1],p[2]-1);visit(p[1],p[2]+1)end
 for y=1,size-2 do for x=1,size-2 do
  if solid[y][x]and(outside[y-1][x]or outside[y+1][x]or outside[y][x-1]or outside[y][x+1])then
   for dy=-6,6 do for dx=-6,6 do local xx,yy=x+dx,y+dy;if xx>=0 and xx<size and yy>=0 and yy<size and outside[yy][xx]then local d=math.max(math.abs(dx),math.abs(dy));dist[yy][xx]=math.min(dist[yy][xx],d)end end end
  end
 end end
 masks[pose]={dist=dist,base=im}
end
local cells={}
for level=0,5 do for pose=1,3 do
 local im=Image(size,size,ColorMode.RGB);local m=masks[pose]
 if level>0 then local radius=level+1
  for y=0,size-1 do for x=0,size-1 do local d=m.dist[y][x]
   if d>0 and d<=radius and pc.rgbaA(m.base:getPixel(x,y))==0 then
    local a=math.floor((1-(d-1)/(radius+1))*(105+level*27));local r,g,b=22,232,163
    if d==1 then r,g,b=120+level*12,255,221+level*5 elseif d==2 then r,g,b=45,250,187 end
    im:drawPixel(x,y,pc.rgba(math.min(255,r),g,math.min(255,b),math.min(255,a)))
   end
  end end
 end
 cells[#cells+1]=im
end end
save('wind_aura',cells,6)
