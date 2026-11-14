local root=app.params['root'];local file=io.open(root..'/outputs/dracodia-energy/art.json','r');local art=json.decode(file:read('*a'));file:close()
local dir=root..'/outputs/dracodia-energy/editable';app.fs.makeAllDirectories(dir)
local groups={eyes={},cores={},vortex={},shield={},lightning={},markers={}}
for name,rows in pairs(art.banks)do local group=name:match('^eye')and'eyes'or name:match('^core')and'cores'or name:match('^wind')and'vortex'or name:match('^shield')and'shield'or name=='bolt'and'lightning'or'markers';table.insert(groups[group],name)end
local sizes={eyes={128,80},cores={64,64},vortex={288,288},shield={352,352},lightning={192,512},markers={128,64}}
local pages={};local mapping={}
for group,names in pairs(groups)do
 table.sort(names);local size=sizes[group];local s=Sprite(size[1],size[2],ColorMode.RGB);local count=0;mapping[group]={}
 for _,name in ipairs(names)do
  local first=count+1
  for _,a in ipairs(art.banks[name])do
   if count>0 then s:newEmptyFrame()end
   if not pages[a.key]then pages[a.key]=Image{fromFile=root..'/work/dracodia-energy/candidate/art/'..a.key..'.png'}end
   local r=a.rect;local im=Image(pages[a.key],Rectangle(r[1],r[2],r[3],r[4]));s:newCel(s.layers[1],count+1,im,Point(a.offset[1]+a.pivot[1],a.offset[2]+a.pivot[2]));s.frames[count+1].duration=group=='lightning'and .08 or 1/24;count=count+1
  end
  local tag=s:newTag(first,count);tag.name=name;mapping[group][name]={first=first,count=count-first+1,pivot=art.banks[name][1].pivot}
 end
 s:saveAs(dir..'/'..group..'.aseprite');s:close();print(group..': '..count..' frames')
end
local out=io.open(dir..'/timeline.json','w');out:write(json.encode(mapping));out:close()
