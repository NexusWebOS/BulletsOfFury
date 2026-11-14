local root=app.params['root'];local dir=root..'/outputs/cannon-cover/editable';app.fs.makeAllDirectories(dir)
for p=0,1 do for _,mode in ipairs({'body','hit'}) do
 local name='cannon'..p..'-'..mode;local im=Image{fromFile=root..'/work/cannon-cover/candidate/frames/'..name..'.png'};local s=Sprite(256,832,ColorMode.RGB)
 for f=0,27 do if f>0 then s:newEmptyFrame() end;s:newCel(s.layers[1],f+1,Image(im,Rectangle(f%8*256,math.floor(f/8)*832,256,832)),Point(0,0));s.frames[f+1].duration=1/24 end
 s:saveAs(dir..'/'..name..'.aseprite');s:close()
end end
