local R=app.params['root'];local D=app.params['out'];local pc=app.pixelColor;local tau=math.pi*2;local banks={}
local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close()
local function clamp(x,l,h)return math.max(l,math.min(h,x))end
local function rgba(r,g,b,a)return pc.rgba(math.floor(clamp(r,0,255)),math.floor(clamp(g,0,255)),math.floor(clamp(b,0,255)),math.floor(clamp(a,0,255)))end
local function white(im)local o=Image(im.width,im.height,ColorMode.RGB);for p in im:pixels()do local c=p();if pc.rgbaA(c)>0 then o:drawPixel(p.x,p.y,rgba(255,255,255,pc.rgbaA(c)))end end;return o end
local function transform(src,piv,a,k,size)
 local o=Image(size,size,ColorMode.RGB);local c,s=math.cos(a),math.sin(a)
 for y=0,size-1 do for x=0,size-1 do local dx,dy=x-size/2,y-size/2;local xx=math.floor((dx*c+dy*s)/k+piv[1]+.5);local yy=math.floor((-dx*s+dy*c)/k+piv[2]+.5);if xx>=0 and yy>=0 and xx<src.width and yy<src.height then o:drawPixel(x,y,src:getPixel(xx,yy))end end end;return o
end
local function register(n,frames,pivot,extra,hit)
 local w,h=frames[1].width,frames[1].height;local cols=#frames>64 and 16 or 8;local sh=Image(w*cols,h*math.ceil(#frames/cols),ColorMode.RGB);local spr=Sprite(w,h,ColorMode.RGB)
 for i,im in ipairs(frames)do sh:drawImage(im,Point((i-1)%cols*w,math.floor((i-1)/cols)*h));if i>1 then spr:newEmptyFrame()end;spr:newCel(spr.layers[1],i,im,Point(0,0));spr.frames[i].duration=1/24 end
 sh:saveAs(D..'/'..n..'.png');spr:saveAs(D..'/'..n..'.aseprite');spr:close();local a={key='rd72_'..n,path='assets/game/levels/stage_08/boss/claw_laser_1030/'..n..'.png',cw=w,ch=h,cols=cols,frames=#frames,pivot={pivot[1],pivot[2]}};for k,v in pairs(extra or{})do a[k]=v end;banks[n]=a
 if hit then local a={};for _,im in ipairs(frames)do table.insert(a,white(im))end;register(n..'_hit',a,pivot,extra,false)end
end
local function purple(src,strength)
 local o=Image(src.width,src.height,ColorMode.RGB);for p in src:pixels()do local v=p();local a=pc.rgbaA(v);if a>0 then local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local mx=math.max(r,g,b);local mn=math.min(r,g,b)
  if mx-mn>20 then r,g,b=math.min(255,mx*1.12),mn*.20,math.min(255,mx*.98)elseif mx<230 then r,g,b=mx*(.80+strength*.16),mx*.46,mx*.95 end
  o:drawPixel(p.x,p.y,rgba(r,g,b,a))end end;return o
end
-- Original physical claw, with four baked finger closure stages and64 headings.
local raw=Image{fromFile=D..'/claw-reference.png'};local claw={}
for grip=0,3 do local closed=Image(160,160,ColorMode.RGB)
 for p in raw:pixels()do local v=p();if p.y>=43 and pc.rgbaA(v)>0 then local shift=0;if p.y>72 then shift=p.x<79 and grip*3 or p.x>89 and-grip*3 or 0 end;closed:drawPixel(p.x+shift,p.y,v)end end
 for dir=0,63 do table.insert(claw,transform(closed,{80,55},dir*tau/64-math.pi/2,.80,160))end
end;register('claw',claw,{80,80},{angles=64,grips=4,gripDistance=34},true)
-- A continuous black/purple ligament; no repeated wrist/hand silhouettes in the extension.
local links={}
for phase=0,3 do local src=Image(24,36,ColorMode.RGB)
 for y=0,35 do local half=8+(y%9<5 and 1 or 0)
  for x=12-half,12+half do local edge=math.abs(x-12);local c=edge>=half and rgba(5,3,9,255)or edge>=half-2 and rgba(57,35,70,255)or rgba(17,10,25,255)
   if x==8 or x==9 then c=rgba(92,72,109,255)end
   if x==13+(math.floor((y+phase*3)/4)%3-1)*2 then c=rgba(192+phase*12,49+phase*9,231,255)end
   src:drawPixel(x,y,c)
  end
 end
 for dir=0,63 do table.insert(links,transform(src,{12,18},dir*tau/64-math.pi/2,1,64))end
end;register('tendon',links,{32,32},{angles=64,cycles=4},true)
-- Whole original shoulders stay on the body; only the distal arm extends.
for _,side in ipairs({'left','right'})do local a=C.rd71['host_dracodia_wind_'..side];local sh=Image{fromFile=R..'/'..a.path};local src=Image(sh,Rectangle(0,0,360,360));local im=Image(360,360,ColorMode.RGB)
 for p in src:pixels()do if p.y<=207 then im:drawPixel(p.x,p.y,p())end end;register('root_'..side,{im},{180,180},nil,true)
end
-- Source red eye-beam body and proper optical root, never an orb muzzle.
local laser=Image{fromFile=R..'/assets/game/shared/combat/encounter_revision_1023/laser_down.webp'};local roots=Image{fromFile=R..'/assets/game/shared/combat/stage78_review_1025/eye_root.webp'};local beams,muzzles,guides={},{},{}
for phase=0,3 do local src=Image(laser,Rectangle(phase*104+36,132,32,96));local root=Image(roots,Rectangle(phase*104,0,104,80))
 for dir=0,63 do local a=dir*tau/64-math.pi/2;table.insert(beams,transform(src,{16,48},a,1,128));table.insert(muzzles,transform(root,{52,12},a,.80,160));local ghost=Image(src.width,src.height,ColorMode.RGB)
  for p in src:pixels()do local v=p();if pc.rgbaA(v)>0 then ghost:drawPixel(p.x,p.y,rgba(255,45,65,pc.rgbaA(v)*.28))end end;table.insert(guides,transform(ghost,{16,48},a,1,128))
 end
end
register('beam',beams,{64,64},{angles=64,cycles=4});register('optic_root',muzzles,{80,80},{angles=64,cycles=4});register('guide',guides,{64,64},{angles=64,cycles=4})
-- Warning strips are authored transparent pixels at every physical firing direction.
for _,q in ipairs({{'green',65,230,92},{'yellow',245,210,55},{'red',255,55,68}})do local src=Image(32,96,ColorMode.RGB)
 for y=0,95 do for x=0,31 do if math.abs(x-15.5)<13 then local border=math.abs(x-15.5)>11;src:drawPixel(x,y,rgba(q[2],q[3],q[4],border and 120 or 48))end end end
 local fs={};for dir=0,63 do table.insert(fs,transform(src,{16,48},dir*tau/64-math.pi/2,1,128))end;register('warning_'..q[1],fs,{64,64},{angles=64})
 local field=Image{fromFile=R..'/assets/game/levels/stage_06/boss/rook_circle_1029/field_'..q[1]..'.png'};register('circle_'..q[1],{field},{202,202})
 local symbol=Image{fromFile=R..'/assets/game/levels/stage_06/boss/rook_circle_1029/symbol_'..q[1]..'.png'};register('rotate_'..q[1],{symbol},{24,24})
end
local sign=Image{fromFile=R..'/assets/game/levels/stage_09/boss/tidal_sovereign_1029/wall_warning.png'};register('asterisk',{Image(sign,Rectangle(0,0,64,64)),Image(sign,Rectangle(64,0,64,64))},{32,32})
local rocket=Image{fromFile=R..'/assets/game/shared/combat/encounters_0930/jet_missile.png'};rocket=Image(rocket,Rectangle(12,7,12,46));rocket=purple(rocket,.45);local rockets,flashes={},{ }
for phase=0,3 do local src=Image(32,68,ColorMode.RGB);src:drawImage(rocket,Point(10,0))
 for y=43,58+phase*2 do local half=math.floor((59+phase*2-y)/4)
  for x=16-half,16+half do local c=rgba(159,30,221,170);if math.abs(x-16)<=math.max(0,half-2)then c=rgba(255,159+phase*15,255,255)end;src:drawPixel(x,y,c)end
 end
 local flame=Image{fromFile=R..'/assets/game/shared/combat/enemy_overhaul_0925/sprites/weapon_muzzle_missile_'..phase..'.png'};flame=purple(flame,.65);flame:resize(48,48)
 for dir=0,63 do table.insert(rockets,transform(src,{16,23},dir*tau/64+math.pi/2,1,96));table.insert(flashes,transform(flame,{24,24},dir*tau/64-math.pi/2,1,64))end
end;register('missile',rockets,{32,32},{angles=64,cycles=4});register('missile_muzzle',flashes,{32,32},{angles=64,cycles=4})
-- Inset tube patches and anchors follow each actual body pose, not the claws.
for _,name in ipairs({'dracodia_wind','dracodia_strike','dracodia_recover'})do local a=C.bi.banks[name];local sheet=Image{fromFile=R..'/'..C.bi.sheets[name].path}
 for _,side in ipairs({'left','right'})do local fs,anchors={},{}
  for f=0,a.count-1 do local lift=name=='dracodia_wind'and clamp(f/8,0,1)or name=='dracodia_strike'and(1-clamp(f/2,0,1))or 0;local arm=a.arms[f+1][side];local x=arm[1]*2+(side=='left'and 34 or-34);local y=arm[2]*2+10+16*lift;local src=Image(sheet,Rectangle(f%4*512+math.floor(x)-20,math.floor(f/4)*512+math.floor(y)-26,40,52));src=purple(src,.8);src:resize(28,36);local out=Image(48,48,ColorMode.RGB);out:drawImage(src,Point(10,6));table.insert(fs,out);table.insert(anchors,{(x-256)*360/512,(y-256)*360/512})
  end;register('turret_'..name..'_'..side,fs,{24,24},{anchors=anchors},true)
 end
end
local f=io.open(D..'/manifest.json','w');f:write(json.encode(banks));f:close();print('RD72 physical claw and optic-beam exports complete')
