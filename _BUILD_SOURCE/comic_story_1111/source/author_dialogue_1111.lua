local file=io.open(app.params.jobs,'r');local jobs=json.decode(file:read('*a'));file:close();local report={}
for _,j in ipairs(jobs)do
 local original=Image{fromFile=j.input};local sprite=app.open(j.input);sprite:saveAs(j.output);sprite:close()
 local loaded=app.open(j.output);local im=Image(loaded.width,loaded.height,ColorMode.RGB)
 for _,layer in ipairs(loaded.layers)do local c=layer:cel(1);if c then im:drawImage(c.image,c.position)end end
 table.insert(report,{source=j.output,exact=im:isEqual(original)});loaded:close();collectgarbage('collect')
end
local out=io.open(app.params.report,'w');out:write(json.encode(report));out:close()
