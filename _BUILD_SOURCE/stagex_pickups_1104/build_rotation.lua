local root=app.params.root or 'C:/Users/Mike/Documents/New project/BOF-StageX-Box-Rotation-1104/'
local pc=app.pixelColor;local raw=Image{fromFile=root..'power-turn-generated.png'}
local frames={};local preview=Sprite(128,128,ColorMode.RGB);preview.layers[1].name='Authored yaw poses / nearest2x preview'
local full=Sprite(64,64,ColorMode.RGB);full.layers[1].name='16 rotation views +16 matching white hits'
local sheet=Image(2048,64,ColorMode.RGB);local contact=Image(256,256,ColorMode.RGB)
for i=0,15 do
 -- The generator reversed two rear-left views. Bake the symmetric opposing
 -- rear-right views into the correct left-facing poses before export.
 local sourceIndex=i==9 and 7 or (i==11 and 5 or i)
 local sx=math.floor((sourceIndex%4)*raw.width/4+.5);local sy=math.floor(math.floor(sourceIndex/4)*raw.height/4+.5)
 local ex=math.floor(((sourceIndex%4)+1)*raw.width/4+.5);local ey=math.floor((math.floor(sourceIndex/4)+1)*raw.height/4+.5)
 local cut=Image(ex-sx,ey-sy,ColorMode.RGB);cut:drawImage(raw,Point(-sx,-sy))
 local sourceCell=math.ceil(math.max(raw.width,raw.height)/4);local im=Image(sourceCell,sourceCell,ColorMode.RGB);im:drawImage(cut,Point(math.floor((sourceCell-cut.width)/2),math.floor((sourceCell-cut.height)/2)))
 if i==9 or i==11 then local flipped=Image(im.width,im.height,ColorMode.RGB);for y=0,im.height-1 do for x=0,im.width-1 do flipped:drawPixel(im.width-1-x,y,im:getPixel(x,y))end end;im=flipped end
 -- Generated exterior alpha is retained; only faint edge residue is removed.
 for it in im:pixels()do local p=it();if pc.rgbaA(p)<180 then it(0)else it(pc.rgba(pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p),255))end end
 im:resize(64,64)
 local minx,miny,maxx,maxy=64,64,0,0
 for it in im:pixels()do if pc.rgbaA(it())>0 then minx=math.min(minx,it.x);miny=math.min(miny,it.y);maxx=math.max(maxx,it.x);maxy=math.max(maxy,it.y)end end
 -- Integer translation aligns the physical cube centre. Scale is identical for
 -- every full source cell; individual poses are never stretched or cropped.
 local aligned=Image(64,64,ColorMode.RGB);aligned:drawImage(im,Point(32-math.floor((minx+maxx)/2+.5),32-math.floor((miny+maxy)/2+.5)));im=aligned
 frames[i+1]=im;sheet:drawImage(im,Point(i*64,0));contact:drawImage(im,Point((i%4)*64,math.floor(i/4)*64))
 if i>0 then full:newEmptyFrame(i+1);preview:newEmptyFrame(i+1)end
 full:newCel(full.layers[1],i+1,im,Point(0,0));full.frames[i+1].duration=.08
 local zoom=Image(im);zoom:resize(128,128);preview:newCel(preview.layers[1],i+1,zoom,Point(0,0));preview.frames[i+1].duration=.08
end
for i=1,16 do
 local im=Image(frames[i]);for it in im:pixels()do if pc.rgbaA(it())>0 then it(pc.rgba(255,255,255,255))end end
 full:newEmptyFrame(16+i);full:newCel(full.layers[1],16+i,im,Point(0,0));full.frames[16+i].duration=.08;sheet:drawImage(im,Point((15+i)*64,0))
end
sheet:saveAs(root..'power_turn_64.png');contact:saveAs(root..'rotation-contact.png');full:saveAs(root..'power_turn_64.aseprite');preview:saveAs(root..'rotation-preview.gif');preview:close();full:close()
local f=assert(io.open(root..'build.done','w'));f:write('16 yaw poses;16 pose-matched white hits; fixed64cells');f:close()
