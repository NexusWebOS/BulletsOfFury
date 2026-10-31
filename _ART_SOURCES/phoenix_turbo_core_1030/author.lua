local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local A=json.decode(f:read('*a'));f:close()
local function export(name,banks,pivot,delay)
 local first=A.banks[banks[1]][1];local spr=Sprite(first.logical[1],first.logical[2],ColorMode.RGB);local n=0
 for _,bank in ipairs(banks)do for _,a in ipairs(A.banks[bank])do
  local page=Image{fromFile=R..'/'..A.pages[a.key].path};local q=a.rect;local crop=Image(page,Rectangle(q[1],q[2],q[3],q[4]));local im=Image(first.logical[1],first.logical[2],ColorMode.RGB);im:drawImage(crop,Point(a.offset[1]+pivot[1],a.offset[2]+pivot[2]));n=n+1
  if n>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],n,im,Point(0,0));spr.frames[n].duration=delay
 end end
 spr:saveAs(D..'/'..name..'.aseprite');spr:close()
end
local bodies={};local cores={}
for _,phase in ipairs({'recover','wind','strike'})do for dead=0,3 do table.insert(bodies,'body_'..phase..'_'..dead)end;for level=1,5 do table.insert(cores,'core_'..phase..'_'..level)end end
export('phoenix-cannon-poses',bodies,{256,256},.1)
export('phoenix-core-light',cores,{256,256},.1)
export('core-beam-canonical',{'launch_6','beam_6','recover_6','green_6','yellow_6','red_6'},{640,640},1/24)
for _,name in ipairs({'lava','wire','left','right'})do
 local a=A.arena[name][1];local spr=Sprite(a.w,a.h,ColorMode.RGB)
 for i,q in ipairs(A.arena[name])do if i>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],i,Image{fromFile=R..'/'..q.path},Point(0,0));spr.frames[i].duration=.1 end
 spr:saveAs(D..'/arena-'..name..'.aseprite');spr:close()
end
print('Editable whole-body, core light, canonical optics and four arena banks saved.')
