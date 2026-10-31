local D=app.params['out'];local I=app.params['input'];local R=app.params['root'];local pc=app.pixelColor;local tau=math.pi*2;local banks={}
local function rgba(r,g,b,a)return pc.rgba(math.floor(r),math.floor(g),math.floor(b),math.floor(math.max(0,math.min(255,a))))end
local source={};for i=1,8 do source[i]=Image{fromFile=I..'/plasma-'..string.format('%02d',i)..'.png'}end
local function register(name,frames)
 local w,h,cols=80,80,32;local sheet=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local s=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sheet:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=1/30 end
 sheet:saveAs(D..'/'..name..'.png');s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='eh85_'..name,path='assets/game/levels/stage_09/miniboss/horizon_plasma_1031/'..name..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot={40,40}}
end
local beams,dash={},{ }
for dir=0,63 do for f=0,15 do
 local im=Image(80,80,ColorMode.RGB);local src=source[f%8+1];local a=dir*tau/64;local co,si=math.cos(a),math.sin(a)
 -- Normalize the commissioned plasma filaments around an uninterrupted ivory core.
 -- Longitudinal endpoints overlap by 16 pixels; all turns are exported here.
 for y=0,79 do for x=0,79 do
  local dx,dy=x-40,y-40;local along=dx*co+dy*si;local cross=-dx*si+dy*co
  if math.abs(along)<32 and math.abs(cross)<15 then
   local xx=math.floor(32+cross*1.7);local yy=math.floor(64+((along+32)*2+f*8)%128);local v=src:getPixel(xx,yy);local al=pc.rgbaA(v);local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v)
   local dist=math.abs(cross);local glow=dist<10 and (1-dist/10)*85 or 0
   if al>0 then v=rgba(math.min(240,r*.70+g*.20),math.min(255,g*1.06+25),math.min(255,b*.8+g*.2+20),math.max(al,glow))else v=rgba(30,218,202,glow)end
   if dist<3 then v=rgba(233,255,247,255)elseif dist<4.5 then v=rgba(112,255,225,245)elseif dist<6 then v=rgba(31,229,211,math.max(al,165))end
   im:drawPixel(x,y,v)
  end
 end end
 table.insert(beams,im);if f%2==0 then table.insert(dash,im)end
end end
register('beam',beams);register('dash',dash)
if R then
 local f=io.open(R..'/assets/game/levels/stage_09/miniboss/horizon_symbiote_1029/manifest.json','r');local old=json.decode(f:read('*a'));f:close()
 for _,name in ipairs({'eye_glow','eye_white','orb','orb_water'})do
  local a=old[name];local im=Image{fromFile=R..'/'..a.path}
  for p in im:pixels()do local v=p();if pc.rgbaA(v)>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local l=math.max(r,g,b);local lo=math.min(r,g,b)
   if l-lo>20 then p(rgba(math.min(255,r*.75+l*.20),math.min(255,g*.75+l*.30),math.min(255,b*.74+g*.20),pc.rgbaA(v)))end
  end end
  im:saveAs(D..'/'..name..'.png');local s=Sprite(a.cw,a.ch,ColorMode.RGB)
  for n=0,a.frames-1 do if n>0 then s:newEmptyFrame()end;local cell=Image(im,Rectangle(n%a.cols*a.cw,math.floor(n/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],n+1,cell,Point(0,0));s.frames[n+1].duration=1/30 end
  s:saveAs(D..'/'..name..'.aseprite');s:close();banks[name]={key='eh85_'..name,path='assets/game/levels/stage_09/miniboss/horizon_plasma_1031/'..name..'.png',cw=a.cw,ch=a.ch,cols=a.cols,frames=a.frames,pivot={a.pivot[1],a.pivot[2]}}
 end
end
local out=io.open(D..'/manifest.json','w');out:write(json.encode(banks));out:close();print('Cyan plasma authored:1024 beam frames +512 dash frames')
