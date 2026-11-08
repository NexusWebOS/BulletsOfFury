local root=app.params.root
local pc=app.pixelColor
local source={pilot=Image{fromFile=root..'/source/pilot.png'},ship=Image{fromFile=root..'/source/ship.png'}}
local function inkBounds(im)
 local l,t,r,b=im.width,im.height,-1,-1
 for y=0,im.height-1 do for x=0,im.width-1 do if pc.rgbaA(im:getPixel(x,y))>=96 then l=math.min(l,x);t=math.min(t,y);r=math.max(r,x);b=math.max(b,y) end end end
 return {x=l,y=t,w=r-l+1,h=b-t+1}
end
local bounds={pilot=inkBounds(source.pilot),ship=inkBounds(source.ship)}
local specs={{id='pilot_large',kind='pilot',w=128,h=216,pad=4},{id='ship_large',kind='ship',w=176,h=176,pad=6},{id='ship_small',kind='ship',w=80,h=80,pad=4}}
for _,n in ipairs({32,40,44,48,56,64}) do for _,kind in ipairs({'pilot','ship'}) do specs[#specs+1]={id=kind..'_mini_'..n,kind=kind,w=n,h=n,pad=4} end end
for _,n in ipairs({12,48,64}) do specs[#specs+1]={id='lock_'..n,kind='lock',w=n,h=n,pad=0} end
local small={"....####....","...######...","..##....##..","..##....##..","..##....##..",".##########.",".##########.",".####..####.",".####..####.",".####..####.",".##########.","..########.."}
local function lockPixel(x,y,n)
 if n==12 then return small[y+1]:sub(x+1,x+1)=='#' end
 local X=math.floor(x*32/n);local Y=math.floor(y*32/n)
 local body=X>=6 and X<=25 and Y>=13 and Y<=29 and not((X==6 or X==25)and(Y==13 or Y==29))
 local shackle=(X>=10 and X<=21 and Y>=3 and Y<=5)or(X>=8 and X<=11 and Y>=6 and Y<=14)or(X>=20 and X<=23 and Y>=6 and Y<=14)or((X==9 or X==22)and Y==5)
 local key=X>=15 and X<=16 and Y>=19 and Y<=25
 return (body or shackle)and not key
end
local manifest={frameSeconds=.45,colors={gray='#606060',black='#000000'},banks={},sources={pilot={key='cole_body_0922',bounds=bounds.pilot},ship={key='ship_cole_pv2',bounds=bounds.ship}}}
for _,spec in ipairs(specs) do
 local s=Sprite(spec.w,spec.h,ColorMode.RGB);s.layers[1].name='Locked silhouette'
 local sheet=Image(spec.w*2,spec.h,ColorMode.RGB)
 for f=1,2 do
  if f==2 then s:newEmptyFrame(2) end
  local im=Image(spec.w,spec.h,ColorMode.RGB);local c=f==1 and 96 or 0;local color=pc.rgba(c,c,c,255)
  if spec.kind=='lock' then
   for y=0,spec.h-1 do for x=0,spec.w-1 do if lockPixel(x,y,spec.w)then im:drawPixel(x,y,color)end end end
  else
   local src=source[spec.kind];local b=bounds[spec.kind];local scale=math.min((spec.w-spec.pad*2)/b.w,(spec.h-spec.pad*2)/b.h)
   local w,h=math.max(1,math.floor(b.w*scale+.5)),math.max(1,math.floor(b.h*scale+.5));local ox,oy=math.floor((spec.w-w)/2),math.floor((spec.h-h)/2)
   for y=0,h-1 do for x=0,w-1 do
    local sx=math.min(b.x+b.w-1,b.x+math.floor((x+.5)/scale));local sy=math.min(b.y+b.h-1,b.y+math.floor((y+.5)/scale))
    if pc.rgbaA(src:getPixel(sx,sy))>=96 then im:drawPixel(x+ox,y+oy,color)end
   end end
  end
  s:newCel(s.layers[1],f,im,Point(0,0));s.frames[f].duration=.45
  sheet:drawImage(im,Point((f-1)*spec.w,0))
 end
 local tag=s:newTag(1,2);tag.name='gray-black';s:saveAs(root..'/editable/'..spec.id..'.aseprite')
 sheet:saveAs(root..'/exports/'..spec.id..'.png');s:close()
 manifest.banks[spec.id]={key='lp116_'..spec.id,path='assets/game/shared/ui/locked_pilot_1106/'..spec.id..'.png',w=spec.w,h=spec.h,frames=2,pivot={spec.w/2,spec.h/2},order={'gray','black'}}
end
local f=io.open(root..'/manifest.json','w');f:write(json.encode(manifest));f:close()
print('AUTHORED '..#specs..' two-frame silhouette banks')
