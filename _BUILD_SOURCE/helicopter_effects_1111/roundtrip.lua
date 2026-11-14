local root=app.params['root'];local dir=root..'/outputs/dracodia-helicopter/editable';local out=root..'/work/helicopter-1111/roundtrip';app.fs.makeAllDirectories(out)
for _,name in ipairs({'muzzle','launch','tracer','missile','burst72','burst112','burst160'})do local s=app.open(dir..'/'..name..'.aseprite');local count=#s.frames
 for _,f in ipairs({1,math.floor(count/2),count})do local im=Image(s.width,s.height,ColorMode.RGB);for _,cel in ipairs(s.cels)do if cel.frame.frameNumber==f then im:drawImage(cel.image,cel.position)end end;im:saveAs(out..'/'..name..'-'..f..'.png')end;s:close()
end
