local D=app.params['out'];local pc=app.pixelColor;local source=Image{fromFile=D..'/sources/blue-master.png'};source=Image(source,Rectangle(0,0,384,512));local out=Image(3072,2048,ColorMode.RGB);out:clear();local white=Image(3072,2048,ColorMode.RGB);white:clear();local heads={}
for f=0,31 do local im=Image(384,512,ColorMode.RGB);im:clear();local a=f*math.pi/16;local cs,sn=math.cos(a),math.sin(a)
 for it in im:pixels()do local dx,dy=(it.x-192)/.9,(it.y-256)/.9;local x=math.floor(dx*cs+dy*sn+220+.5);local y=math.floor(-dx*sn+dy*cs+253+.5);if x>=0 and y>=0 and x<384 and y<512 then local v=source:getPixel(x,y);if pc.rgbaA(v)>96 then it(pc.rgba(pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v),255))end end end
 out:drawImage(im,Point(f%8*384,math.floor(f/8)*512));for it in im:pixels()do if pc.rgbaA(it())>0 then it(pc.rgba(255,255,255,255))end end;white:drawImage(im,Point(f%8*384,math.floor(f/8)*512));heads[#heads+1]={f%8*384+192-144*.9*cs,math.floor(f/8)*512+256-144*.9*sn}
end
out:saveAs(D..'/exports/flight.png');white:saveAs(D..'/exports/flight_hit.png');local f=io.open(D..'/flight-meta.json','w');f:write(json.encode(heads));f:close()
