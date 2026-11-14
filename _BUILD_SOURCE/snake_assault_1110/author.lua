local root=app.params['root'];local file=io.open(root..'/outputs/snake-assault/art.json','r');local art=json.decode(file:read('*a'));file:close();local dir=root..'/outputs/snake-assault/editable';app.fs.makeAllDirectories(dir)
for name,a in pairs(art) do
 local im=Image{fromFile=root..'/work/snake-assault/candidate/frames/'..name..'.png'};local w=a.cell[1];local h=a.cell[2];local s=Sprite(w,h,ColorMode.RGB)
 for f=0,a.frames-1 do if f>0 then s:newEmptyFrame()end;s:newCel(s.layers[1],f+1,Image(im,Rectangle(f%a.cols*w,math.floor(f/a.cols)*h,w,h)),Point(0,0));s.frames[f+1].duration=1/24 end
 s:saveAs(dir..'/'..name..'.aseprite');s:close()
end
