local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close();local banks={}
for name,a in pairs(C.banks)do
 local size=a.size;local cols=8;local n=#a.frames;local sheet=Image(size*cols,size*math.ceil(n/cols),ColorMode.RGB);local s=Sprite(size,size,ColorMode.RGB)
 for i,row in ipairs(a.frames)do local im=Image{fromFile=R..'/'..row.path};assert(im.width==im.height);im:resize(size,size)
  sheet:drawImage(im,Point((i-1)%cols*size,math.floor((i-1)/cols)*size));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/a.fps
 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='rd94_'..name,path='assets/game/levels/stage_08/effects/gated_possession_1031/'..name..'.png',cw=size,ch=size,cols=cols,frames=n,pivot={size/2,size/2},fps=a.fps}
end
local out=io.open(D..'/manifest.json','w');out:write(json.encode(banks));out:close()
