local R=app.params['root'];local D=app.params['out'];local f=io.open(D..'/inputs.json','r');local C=json.decode(f:read('*a'));f:close()
local out=Image(192,256,ColorMode.RGB)
for _,q in ipairs({{C.core,0,0},{C.head,0,-12}})do local a=q[1];local src=Image{fromFile=R..'/'..a.path};local im=Image(src,Rectangle(0,0,a.cw,a.ch));out:drawImage(im,Point(96+q[2]-a.pivot[1],128+q[3]-a.pivot[2]))end
out:saveAs(D..'/reference.png')
