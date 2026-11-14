local root=app.params['root'];local dir=root..'/outputs/helicopter-death';local file=io.open(dir..'/art.json','r');local art=json.decode(file:read('*a'));file:close();file=io.open(dir..'/editor-plan.json','r');local plan=json.decode(file:read('*a'));file:close();app.fs.makeAllDirectories(dir..'/editable');local pages={};local mapping={}
for group,config in pairs(plan)do
 local s=Sprite(config.logical[1],config.logical[2],ColorMode.RGB);local count=0;mapping[group]={}
 for _,name in ipairs(config.banks)do local first=count+1
  for f,a in ipairs(art.banks[name])do if count>0 then s:newEmptyFrame()end;if not pages[a.key]then pages[a.key]=Image{fromFile=root..'/work/helicopter-death/candidate/art/'..a.key..'.png'}end;local r=a.rect;local im=Image(pages[a.key],Rectangle(r[1],r[2],r[3],r[4]));s:newCel(s.layers[1],count+1,im,Point(a.offset[1]+a.pivot[1],a.offset[2]+a.pivot[2]));s.frames[count+1].duration=name:match('^burst')and .05 or name:match('^chunk')and 1/14 or 1/24;count=count+1 end
  local tag=s:newTag(first,count);tag.name=name;mapping[group][name]={first=first,count=count-first+1}
 end
 s:saveAs(dir..'/editable/'..group..'.aseprite');s:close()
end
file=io.open(dir..'/editable/timeline.json','w');file:write(json.encode(mapping));file:close()
