local W=assert(app.params['work'],'Pass --script-param work=<staging folder>')
if W:sub(-1)~='/'then W=W..'/'end
local pc=app.pixelColor;local rear,front={},{}
local function export(name,ff)
 local s=Sprite(512,512,ColorMode.RGB);local sheet=Image(3072,2048,ColorMode.RGB)
 for f,q in ipairs(ff)do if f>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],f,q,Point(0,0));s.frames[f].duration=1/18;sheet:drawImage(q,Point((f-1)%6*512,math.floor((f-1)/6)*512))end
 s:saveAs(W..'art/'..name..'.aseprite');sheet:saveAs(W..'art/'..name..'.png');s:close()
end
for f=1,24 do
 local im=Image{fromFile=W..'pixellab/vortex-'..string.format('%02d',f)..'.png'};im:resize(384,384)
 local back=Image(512,512,ColorMode.RGB);local fore=Image(512,512,ColorMode.RGB)
 for y=0,383 do for x=0,383 do
  local c=im:getPixel(x,y);local a=pc.rgbaA(c);local dx,dy=x-192,y-192
  -- Authored clear opening: no funnel or opaque wind plate covers the hull.
  if a>0 and (dx/102)^2+(dy/112)^2>=1 then
   local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c);local hi=math.max(r,g,b);local lo=math.min(r,g,b)
   -- Remove the generator's neutral charcoal bands so this reads as open air,
   -- while retaining teal outlines and the authored white/mint wind ribbons.
   if not (hi<155 and hi-lo<35) then
    if hi-lo<35 and hi<225 then c=pc.rgba(math.min(225,r+25),math.min(250,g+45),math.min(245,b+40),math.floor(a*.70))end
    local target=y<192 and back or fore;target:drawPixel(x+64,y+64,c)
   end
  end
 end end
 rear[#rear+1]=back;front[#front+1]=fore
end
export('wind_rear',rear);export('wind_front',front)
print('Packed24 PixelLab vortex frames with a stable clear aircraft opening')
