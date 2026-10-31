local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local A=json.decode(f:read('*a'));f:close()
local function export(name,banks,pivot,delay)
 local first=A.banks[banks[1]][1];local spr=Sprite(first.logical[1],first.logical[2],ColorMode.RGB);local n=0
 for _,bank in ipairs(banks)do for _,a in ipairs(A.banks[bank])do
  local page=Image{fromFile=R..'/'..A.pages[a.key].path};local q=a.rect;local crop=Image(page,Rectangle(q[1],q[2],q[3],q[4]));local im=Image(first.logical[1],first.logical[2],ColorMode.RGB);im:drawImage(crop,Point(a.offset[1]+pivot[1],a.offset[2]+pivot[2]));n=n+1
  if n>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],n,im,Point(0,0));spr.frames[n].duration=delay
 end end
 spr:saveAs(D..'/'..name..'.aseprite');spr:close()
end
export('beam-flow',{'beam_0','beam_1','beam_2','beam_3','beam_4','beam_5'},{40,12},1/24)
export('beam-launch',{'start_0','start_1','start_2','start_3','start_4','start_5'},{40,12},.032)
export('beam-dissipation',{'recover'},{40,12},.02)
export('pose-matched-lenses',{'eyes_brain','eyes_charge','eyes_focus'},{192,192},.1)
print('Exported166 editable source frames across4 Aseprite documents.')
