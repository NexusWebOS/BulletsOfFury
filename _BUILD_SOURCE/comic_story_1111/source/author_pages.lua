local f=io.open(app.params.jobs,'r');local jobs=json.decode(f:read('*a'));f:close()
local colors={{9,11,19},{11,22,32},{23,37,48},{40,64,74},{5,8,15},{247,232,191},{222,195,145},{182,140,85},{136,100,61},{94,66,46},{142,40,44},{192,75,66},{237,128,99},{203,161,74},{242,201,101},{255,244,217}}
local function quant(c)
 local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c);local best,dist=nil,math.huge
 for _,p in ipairs(colors)do local d=(r-p[1])^2+(g-p[2])^2+(b-p[3])^2;if d<dist then best,dist=p,d end end
 return app.pixelColor.rgba(best[1],best[2],best[3],app.pixelColor.rgbaA(c))
end
for _,j in ipairs(jobs)do
 local im=Image{fromFile=j.input};local mask=Image{fromFile=j.mask}
 for px in im:pixels()do if app.pixelColor.rgbaA(px())>0 then px(quant(px()))end end
 local s=Sprite(j.w,j.h,ColorMode.RGB);s:newCel(s.layers[1],1,im,Point(0,0));s:saveAs(app.params.output..'/page-'..j.id..'-bg.aseprite');s:saveCopyAs(app.params.output..'/page-'..j.id..'-bg.png');s:close()
 local fg=Image(im);for px in fg:pixels()do if app.pixelColor.rgbaR(mask:getPixel(px.x,px.y))>128 then px(0)end end
 local p=Sprite(j.w,j.h,ColorMode.RGB);p:newCel(p.layers[1],1,fg,Point(0,0));p:saveAs(app.params.output..'/page-'..j.id..'-fg.aseprite');p:saveCopyAs(app.params.output..'/page-'..j.id..'-fg.png');p:close()
end
