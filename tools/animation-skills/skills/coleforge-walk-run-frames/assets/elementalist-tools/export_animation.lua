-- Batch source document creation; full fixed cells and frame durations survive.
local f=assert(io.open(app.params.metadata,'r'))
local m=json.decode(f:read('*a'));f:close()
local source=app.fs.joinPath(app.fs.filePath(app.params.metadata),m.atlas.image)
local atlas=Image{fromFile=source}
local sprite=Sprite(m.frame_size[1],m.frame_size[2],ColorMode.RGB)
local layer=sprite.layers[1];layer.name='Authored pixels'
for i,name in ipairs(m.animation.frames) do
  if i>1 then sprite:newEmptyFrame(i) end
  local r=m.atlas.rects[i]
  local image=Image(atlas,Rectangle(r.x,r.y,r.w,r.h))
  sprite:newCel(layer,i,image,Point(0,0))
  if m.animation.duration_ms then
    sprite.frames[i].duration=m.animation.duration_ms[i]/1000
  else
    sprite.frames[i].duration=m.animation.duration_ticks[i]/60
  end
end
local tag=sprite:newTag(1,#m.animation.frames);tag.name=m.action
local slice=sprite:newSlice(Rectangle(m.origin[1],m.origin[2],1,1));slice.name='ground-root'
sprite:saveAs(app.params.output)
