local root=app.params['root'];local dir=root..'/outputs/dracodia-energy/editable';local out=root..'/work/dracodia-energy/roundtrip';app.fs.makeAllDirectories(out)
for _,group in ipairs({'eyes','cores','vortex','shield','lightning','markers'})do
 local s=app.open(dir..'/'..group..'.aseprite');local count=#s.frames
 for _,f in ipairs({1,math.floor(count/2),count})do
  local im=Image(s.width,s.height,ColorMode.RGB);for _,cel in ipairs(s.cels)do if cel.frame.frameNumber==f then im:drawImage(cel.image,cel.position)end end;im:saveAs(out..'/'..group..'-'..f..'.png')
 end
 print(group..' '..s.width..'x'..s.height..' '..count);s:close()
end
