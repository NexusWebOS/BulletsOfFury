local pilots={'cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut'}
local tints={{122,214,58},{58,138,255},{111,208,255},{226,58,58},{58,214,200},{255,42,143},{255,194,26},{255,210,74},{192,138,58}}
local sheet=Image{fromFile=app.params.sheet};local report={}
for i,pk in ipairs(pilots)do
 local tint=tints[i];local palette={{3,8,18},{5,12,26},{9,19,33},{14,29,44},{22,42,58},{0,0,0},{250,237,200},{238,223,184}}
 for _,f in ipairs({.25,.4,.6,.8,1})do table.insert(palette,{math.floor(tint[1]*f),math.floor(tint[2]*f),math.floor(tint[3]*f)})end
 for _,f in ipairs({.2,.4,.65})do table.insert(palette,{math.floor(tint[1]+(255-tint[1])*f),math.floor(tint[2]+(255-tint[2])*f),math.floor(tint[3]+(255-tint[3])*f)})end
 local cache={};local function quant(c)
  if cache[c]then return cache[c]end;local r,g,b=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c);local best,dist=nil,math.huge
  for _,p in ipairs(palette)do local d=(r-p[1])^2+(g-p[2])^2+(b-p[3])^2;if d<dist then best,dist=p,d end end
  local out=app.pixelColor.rgba(best[1],best[2],best[3],255);cache[c]=out;return out
 end
 local image=Image(512,340,ColorMode.RGB);local sx=((i-1)%3)*512;local sy=({0,342,684})[math.floor((i-1)/3)+1]
 for px in image:pixels()do px(quant(sheet:getPixel(sx+px.x,sy+px.y)))end
 local s=Sprite(512,340,ColorMode.RGB);s:newCel(s.layers[1],1,image,Point(0,0));s:saveAs(app.params.output..'/'..pk..'.aseprite');s:saveCopyAs(app.params.output..'/'..pk..'.png');s:close()
 local source=app.open(app.params.portraits..'/'..pk..'/talking.aseprite');local composite=Sprite(384,288,ColorMode.RGB)
 for n,frame in ipairs(source.frames)do
  local original=Image(128,128,ColorMode.RGB);local cel=source.layers[1]:cel(n);original:drawImage(cel.image,cel.position)
  local large=Image(256,256,ColorMode.RGB)
  for px in original:pixels()do local c=px();for dy=0,1 do for dx=0,1 do large:drawPixel(px.x*2+dx,px.y*2+dy,c)end end end
  local canvas=Image(384,288,ColorMode.RGB);canvas:drawImage(image,Point(-64,-26));canvas:drawImage(large,Point(64,40))
  local target=n==1 and composite.frames[1]or composite:newEmptyFrame(n);target.duration=frame.duration;composite:newCel(composite.layers[1],n,canvas,Point(0,0))
 end
 composite:saveAs(app.params.framed..'/'..pk..'.aseprite');composite:saveCopyAs(app.params.framed..'/'..pk..'-comic-talker.gif');composite:close();source:close()
 table.insert(report,{pilot=pk,sourceCrop={sx,sy,512,340},background={512,340},preview={384,288},palette=16,baseline=250,previewOrigin={64,40}})
 collectgarbage('collect')
end
local out=io.open(app.params.report,'w');out:write(json.encode(report));out:close()
