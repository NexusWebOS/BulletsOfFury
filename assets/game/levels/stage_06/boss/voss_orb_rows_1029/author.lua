local W=app.params['work'] or 'C:/Users/Mike/Documents/New project/BOF-Orb-Rows-1029/'
if W:sub(-1)~='/'then W=W..'/'end
local pc=app.pixelColor;local src=Image{fromFile=W..'florb_0.png'};src:resize(32,32)
local sheet=Image(384,384,ColorMode.RGB);local sp=Sprite(48,48,ColorMode.RGB);local cells={}
local ladder={0,.16,.32,.52,.74,.95,.74,.52,.32,.16}
for f=0,31 do
 local out=Image(48,48,ColorMode.RGB);local angle=f*math.pi*2/32;local ca,sa=math.cos(angle),math.sin(angle);local pulse=ladder[(f%10)+1]
 for y=0,47 do for x=0,47 do
  local dx,dy=x-23.5,y-23.5;local sx=math.floor(ca*dx+sa*dy+15.5+.5);local sy=math.floor(-sa*dx+ca*dy+15.5+.5)
  if sx>=0 and sy>=0 and sx<32 and sy<32 then
   local c=src:getPixel(sx,sy);local r,g,b,a=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)
   if a>0 then
    local hi,lo=math.max(r,g,b),math.min(r,g,b);local diff=hi-lo
    -- Preserve the white core, dark outline and source alpha. The existing
    -- energy pixels carry red chroma and the six-step1015 emission ladder.
    if diff>15 and hi>35 then
     r=hi;g=math.floor(lo+diff*.08);b=math.floor(lo+diff*.12)
     local light=pulse*.34;r=math.floor(r+(255-r)*light);g=math.floor(g+(160-g)*light);b=math.floor(b+(128-b)*light)
    end
    out:drawPixel(x,y,pc.rgba(r,g,b,a))
   end
  end
 end end
 if f>0 then sp:newEmptyFrame()end;sp:newCel(sp.layers[1],f+1,out,Point(0,0));sp.frames[f+1].duration=1/24
 sheet:drawImage(out,Point(f%8*48,math.floor(f/8)*48))
 cells[f+1]=out
end
for f=0,31 do
 local out=Image(cells[f+1])
 for it in out:pixels()do local c=it();local a=pc.rgbaA(c);if a>0 then it(pc.rgba(255,255,255,a))end end
 sp:newEmptyFrame();sp:newCel(sp.layers[1],f+33,out,Point(0,0));sp.frames[f+33].duration=1/24
 sheet:drawImage(out,Point(f%8*48,192+math.floor(f/8)*48))
end
sp:saveAs(W..'orb_rows.aseprite');sheet:saveAs(W..'orb_rows.png');sp:close()
