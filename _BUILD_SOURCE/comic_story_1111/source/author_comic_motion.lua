local f=io.open(app.params.jobs,'r');local jobs=json.decode(f:read('*a'));f:close();local checks={}
for _,j in ipairs(jobs)do
 local s=Sprite(j.w,j.h,ColorMode.RGB)
 for i,path in ipairs(j.frames)do local im=Image{fromFile=path};local frame=i==1 and s.frames[1]or s:newEmptyFrame(i);s:newCel(s.layers[1],i,im,Point(0,0));frame.duration=.07 end
 s:saveAs(j.output);s:close()
 local read=app.open(j.output);local errors=0
 for i,path in ipairs(j.frames)do local original=Image{fromFile=path};local restored=Image(j.w,j.h,ColorMode.RGB);local c=read.layers[1]:cel(i);if c then restored:drawImage(c.image,c.position)end;if not original:isEqual(restored)then errors=errors+1 end end
 read:close();table.insert(checks,{bank=j.name,frames=#j.frames,different=errors});collectgarbage('collect')
end
local out=io.open(app.params.report,'w');out:write(json.encode(checks));out:close()
