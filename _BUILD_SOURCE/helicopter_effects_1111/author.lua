local root=app.params['root'];local file=io.open(root..'/outputs/dracodia-helicopter/art.json','r');local art=json.decode(file:read('*a'));file:close();local dir=root..'/outputs/dracodia-helicopter/editable';app.fs.makeAllDirectories(dir);local pages={};local mapping={}
for name,rows in pairs(art.banks)do
 local size=rows[1].logical;local s=Sprite(size[1],size[2],ColorMode.RGB);local native={};local count=0;local directional=name=='muzzle'or name=='launch'or name=='missile'or name=='tracer';local dirs=directional and 64 or 1;local phases=directional and 8 or 16
 for d=0,dirs-1 do
  local first=count+1
  for f=0,phases-1 do
   local index=directional and f*64+d+1 or f+1;local a=rows[index];if count>0 then s:newEmptyFrame()end;if not pages[a.key]then pages[a.key]=Image{fromFile=root..'/work/helicopter-1111/candidate/art/'..a.key..'.png'}end;local r=a.rect;local im=Image(pages[a.key],Rectangle(r[1],r[2],r[3],r[4]));s:newCel(s.layers[1],count+1,im,Point(a.offset[1]+a.pivot[1],a.offset[2]+a.pivot[2]));s.frames[count+1].duration=(name=='muzzle'and .02)or(name=='launch'and .025)or(name=='missile'and 1/24)or(name=='tracer'and 1/30)or .05;count=count+1;native[count]=index
  end
  local tag=s:newTag(first,count);tag.name=directional and('heading-'..d)or'one-shot'
 end
 s:saveAs(dir..'/'..name..'.aseprite');s:close();mapping[name]={native=native,logical=size,pivot=rows[1].pivot}
end
local out=io.open(dir..'/timeline.json','w');out:write(json.encode(mapping));out:close()
