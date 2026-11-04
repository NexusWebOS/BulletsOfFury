local file=io.open(app.params.jobs,'r')
local jobs=json.decode(file:read('*a'));file:close()
local results={}
for _,job in ipairs(jobs)do
 local sheet=Image{fromFile=job.input}
 local sprite=Sprite(job.w,job.h,ColorMode.RGB)
 local layer=sprite.layers[1];layer.name='Authored source pixels'
 local originals={}
 for i=0,job.frames-1 do
  local frame=i==0 and sprite.frames[1] or sprite:newEmptyFrame(i+1)
  local cell=Image(job.w,job.h,ColorMode.RGB)
  cell:drawImage(sheet,Point(-(i%job.cols)*job.w,-math.floor(i/job.cols)*job.h))
  sprite:newCel(layer,i+1,cell,Point(0,0));originals[i+1]=cell
  frame.duration=job.frameDurations and job.frameDurations[i+1]/1000 or job.duration
 end
 local tag=sprite:newTag(1,job.frames);tag.name=job.name
 if job.tags then
  for i=1,job.frames do sprite.frames[i].duration=i<=4 and .1 or i<=12 and .13 or .18 end
  for _,info in ipairs(job.tags)do
   local t=sprite:newTag(info.first,info.last);t.name=info.name
  end
 end
 if job.name:sub(1,6)=='actor-'then
  local walk=sprite:newTag(4,7);walk.name='walk';local run=sprite:newTag(8,11);run.name='run'
  for i=4,7 do sprite.frames[i].duration=1/6 end
  for i=8,11 do sprite.frames[i].duration=.1 end
 end
 sprite:saveAs(job.output);sprite:close()
 local loaded=app.open(job.output)
 assert(loaded.width==job.w and loaded.height==job.h and #loaded.frames==job.frames,job.name..' dimensions')
 local different=0
 for i=1,job.frames do
  local cell=Image(job.w,job.h,ColorMode.RGB)
  local cel=loaded.layers[1]:cel(i)
  if cel then cell:drawImage(cel.image,cel.position)end
  if not cell:isEqual(originals[i])then different=different+1 end
 end
 table.insert(results,{name=job.name,frames=job.frames,different=different})
 loaded:close();collectgarbage('collect')
end
local result=io.open(app.params.report,'w');result:write(json.encode(results));result:close()
