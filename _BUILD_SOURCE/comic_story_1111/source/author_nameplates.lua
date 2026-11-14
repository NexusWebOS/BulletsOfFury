local f=io.open(app.params.jobs,'r');local jobs=json.decode(f:read('*a'));f:close()
local tints={cole={122,214,58},axel={58,138,255},freezer={111,208,255},yuri={226,58,58},maverick={58,214,200},falva={255,42,143},lizzie={255,194,26},decker={255,210,74},juggernaut={192,138,58}}
for _,j in ipairs(jobs)do
 local original=Image{fromFile=app.params.output..'/page-'..tostring(j.id)..'-bg.png'};local box=j.name
 for name,tint in pairs(tints)do
  local image=Image(box[3]+box[3]%2,box[4]+box[4]%2,ColorMode.RGB)
  for y=0,box[4]-1 do for x=0,box[3]-1 do local c=original:getPixel(box[1]+x,box[2]+y);local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c)
   if r>110 and g>75 and b<150 and r>g*1.05 then local factor=.35*(r+g+b)/(203+161+74);c=app.pixelColor.rgba(math.min(255,math.floor(tint[1]*factor)),math.min(255,math.floor(tint[2]*factor)),math.min(255,math.floor(tint[3]*factor)),255)end
   image:drawPixel(x,y,c)
  end end
  image:saveAs(app.params.output..'/name-'..math.floor(j.id)..'-'..name..'.png')
 end
end
