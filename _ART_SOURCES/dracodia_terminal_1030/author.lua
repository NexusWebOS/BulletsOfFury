local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local A=json.decode(f:read('*a'));f:close()
local function export(name,banks,delay)
 local first=A.banks[banks[1]][1];local spr=Sprite(first.logical[1],first.logical[2],ColorMode.RGB);local n=0
 for _,bank in ipairs(banks)do local start=n+1;for _,a in ipairs(A.banks[bank])do
  local page=Image{fromFile=R..'/'..A.pages[a.key].path};local q=a.rect;local crop=Image(page,Rectangle(q[1],q[2],q[3],q[4]));local im=Image(first.logical[1],first.logical[2],ColorMode.RGB);im:drawImage(crop,Point(a.offset[1]+a.pivot[1],a.offset[2]+a.pivot[2]));n=n+1
  if n>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],n,im,Point(0,0));spr.frames[n].duration=delay
 end;local tag=spr:newTag(start,n);tag.name=bank end;spr:saveAs(D..'/'..name..'.aseprite');spr:close()
end
local body={};for level=0,5 do table.insert(body,'idle_'..level);table.insert(body,'roar_'..level)end
export('terminal-idle-roar-white1015',body,1/24)
export('formation-lightning',{'lightning_strong','lightning_tail'},1/24)
export('electrified-coleforge-explosions',{'electric_small','electric_medium','electric_final'},1/24)
export('blue-mechanical-gate',{'gate_form','gate_loop','gate_close'},1/20)
export('rapid-download-erase',{'download_erase'},1/24)
export('complete-body-shatter',{'body_shatter'},1/20)
for _,pk in ipairs(A.pilots)do export('aircraft-depth-'..pk,{'ship_north_'..pk,'ship_south_'..pk,'shadow_'..pk},1/24)end
print('Saved terminal poses, original-pack electric effects, gate, exact body fragments and all nine aircraft source documents.')
