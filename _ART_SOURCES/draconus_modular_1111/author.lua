local W=app.params['out'];local audit={}
for _,mat in ipairs({'regular','chrome'}) do
 local dir=W..'/editable/'
 local body=Image{fromFile=dir..'body_'..mat..'.png'}
 local grip=Image{fromFile=dir..'grip_'..mat..'.png'}
 local sheet=Image{fromFile=dir..'gun_'..mat..'.png'}
 local s=Sprite(512,512,ColorMode.RGB)
 s.layers[1].name='Complete fixed body'
 local gun=s:newLayer();gun.name='Independent solid gun / axial barrel phases'
 local hand=s:newLayer();hand.name='Foreground grips / same body source pixels'
 for i=1,36 do
  if i>1 then s:newEmptyFrame() end
  s:newCel(s.layers[1],i,body,Point(0,0))
  local im=Image(104,208,ColorMode.RGB);im:clear()
  im:drawImage(sheet,Point(-((i-1)%4)*104,-math.floor((i-1)/4)*208))
  s:newCel(gun,i,im,Point(198,224));s:newCel(hand,i,grip,Point(0,0));s.frames[i].duration=.03
 end
 s:newTag(1,36).name='Full axial revolution / slow inspection'
 local origin=s:newSlice(Rectangle(256,256,1,1));origin.name='Fixed actor origin'
 local muzzle=s:newSlice(Rectangle(252,404,1,1));muzzle.name='Actual bore / warnings and rounds'
 s:saveAs(dir..'draconus_modular_'..mat..'.aseprite');s:close()
 s=app.open(dir..'draconus_modular_'..mat..'.aseprite');assert(#s.frames==36 and #s.layers==3)
 for k,layer in ipairs(s.layers) do
  local out=Image(512*4,512*9,ColorMode.RGB);out:clear()
  for i=1,36 do
   local c=layer:cel(i);assert(c)
   out:drawImage(c.image,Point((i-1)%4*512+c.position.x,math.floor((i-1)/4)*512+c.position.y))
  end
  out:saveAs(dir..mat..'-layer-'..k..'-roundtrip.png')
 end
 audit[#audit+1]={material=mat,frames=#s.frames,layers=#s.layers};s:close()
end
local f=io.open(W..'/aseprite-audit.json','w');f:write(json.encode(audit));f:close()
