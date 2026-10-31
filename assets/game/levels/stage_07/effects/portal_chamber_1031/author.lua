local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
for _,color in ipairs({'green','blue'})do for _,phase in ipairs({'form','loop','close'})do
 local name=color..'_'..phase;local a=C.banks[name];local size=a.size;local cols=8;local n=#a.frames;local sheet=Image(size*cols,size*math.ceil(n/cols),ColorMode.RGB);local s=Sprite(size,size,ColorMode.RGB)
 for i,row in ipairs(a.frames)do local im=Image{fromFile=R..'/'..row.path};if size~=im.width then im:resize(size,size)end
  sheet:drawImage(im,Point((i-1)%cols*size,math.floor((i-1)/cols)*size));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/a.fps
 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='sc86_'..name,path='assets/game/levels/stage_07/effects/portal_chamber_1031/'..name..'.png',cw=size,ch=size,cols=cols,frames=n,pivot={size/2,size/2},fps=a.fps}
end end
local seal=Image(256,256,ColorMode.RGB);for y=0,255 do for x=0,255 do if((x-128)/99)^2+((y-128)/100)^2<=1 then seal:drawPixel(x,y,app.pixelColor.rgba(1,4,2,255))end end end
seal:saveAs(D..'/seal.png');local s=Sprite(256,256,ColorMode.RGB);s:newCel(s.layers[1],1,seal,Point(0,0));s:saveAs(D..'/seal.aseprite');s:close();banks.seal={key='sc86_seal',path='assets/game/levels/stage_07/effects/portal_chamber_1031/seal.png',cw=256,ch=256,cols=1,frames=1,pivot={128,128},fps=1}
local out=io.open(D..'/manifest.json','w');out:write(json.encode(banks));out:close();print('Correct PixelLab green/blue metal gate banks exported')
