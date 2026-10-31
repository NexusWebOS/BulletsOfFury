local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local A=json.decode(f:read('*a'));f:close()
local function export(name,banks,delay)
 local spr=Sprite(512,512,ColorMode.RGB);local n=0
 for _,bank in ipairs(banks)do
  local first=n+1
  for _,a in ipairs(A.banks[bank])do
   local page=Image{fromFile=R..'/'..A.pages[a.key].path};local q=a.rect;local crop=Image(page,Rectangle(q[1],q[2],q[3],q[4]));local im=Image(512,512,ColorMode.RGB);im:drawImage(crop,Point(a.offset[1]+256,a.offset[2]+256));n=n+1
   if n>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],n,im,Point(0,0));spr.frames[n].duration=delay
  end
  local tag=spr:newTag(first,n);tag.name=bank
 end
 spr:saveAs(D..'/'..name..'.aseprite');spr:close()
end
export('foreground-wing-flight',{'idle','dive_0','dive_1','dive_2','dive_3'},1/24)
export('depth-bank-turn-return',{'recede','cruise','twist_north','twist_south','return_north','return_south'},1/30)
export('accelerating-fire-charge',{'charge_0','charge_1','charge_2','charge_3','charge_4','charge_5'},1/24)
export('digital-fire-phoenix-copies',{'echo_birth','echo'},1/22)
export('fire-wind-spirals',{'wind_rear_0','wind_front_0','wind_rear_1','wind_front_1','wind_rear_2','wind_front_2','wind_rear_3','wind_front_3','wind_rear_4','wind_front_4','wind_out'},1/24)
export('corner-flight-warnings',{'warning_green','warning_yellow','warning_red'},.1)
export('flight-shadows',{'idle_shadow','dive_0_shadow','dive_1_shadow','dive_2_shadow','dive_3_shadow'},1/24)
print('Seven editable Aseprite documents with named animation banks saved.')
