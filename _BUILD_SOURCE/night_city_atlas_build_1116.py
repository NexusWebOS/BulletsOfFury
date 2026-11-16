from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/cinema_overnight_1116';A=R/'assets/game/shared/cinematics/cinema_overnight_1116';O=R/'_shots/cinema_overnight_1116/city-atlas';S.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
audit=json.loads((O/'before.json').read_text(encoding='utf8'));changes=[]
for q in audit['pagesNeedingPadding']:
 src=R/q['path'];im=Image.open(src).convert('RGBA');out=Image.new('RGBA',tuple(q['required']));out.paste(im,(0,0));assert out.crop((0,0,*im.size)).tobytes()==im.tobytes()
 stem=src.stem;png=S/('city-'+stem+'.png');out.save(png);path=A/('city-'+stem+'.webp');out.save(path,lossless=True,exact=True);decoded=Image.open(path).convert('RGBA');assert decoded.tobytes()==out.tobytes()
 changes.append({'oldKey':q['key'],'key':'nqa16_'+q['key'],'source':q['path'],'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'sourceSize':list(im.size),'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':list(out.size),'padding':[0,0,out.width-im.width,out.height-im.height],'sourcePixelsUnchanged':True,'editableLosslessSource':png.relative_to(R).as_posix()})
manifest={'owner':'_BUILD_SOURCE/night_city_atlas_build_1116.py','normalization':'Transparent page padding to the maximum declared cell extent, rounded even. All original RGBA pixels and every source rectangle, pivot, heading, depth and animation count remain unchanged. This does not reconstruct or claim missing authored ink.','affectedCells':len(audit['badCells']),'changes':changes}
(S/'city-atlas.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
js='"use strict";\n/* Technical atlas extent repair. No new sprite poses or effects. */\nconst NQA16='+json.dumps(changes,separators=(',',':'))+';\nfor(const p of NQA16){\n XART._src[p.key]=p.path+"?v="+p.sha256.slice(0,12);\n for(const B of Object.values(CITY16_ART.banks)){\n  for(const c of B.cells)if(c[0]===p.oldKey)c[0]=p.key;\n  for(const page of B.pages)if(page.key===p.oldKey)Object.assign(page,{key:p.key,path:p.path,sha256:p.sha256});\n }\n}\n'
(R/'assets/night_city_atlas_1116.js').write_text(js,encoding='utf8',newline='\n')
p=R/'index.html';raw=p.read_text(encoding='utf8');tag='<script src="assets/night_city_atlas_1116.js?v=1"></script>'
if tag not in raw:raw=raw.replace('</body>',tag+'\n</body>');p.write_text(raw,encoding='utf8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf8'));d={'nqa16_':{'role':'lossless_existing_atlas_extent_repair','owner':'_BUILD_SOURCE/night_city_atlas_build_1116.py','manifest':'_ART_SOURCES/cinema_overnight_1116/city-atlas.json','note':'Transparent2px page padding only; all16 animation phases, heading/nozzle pivots and original pixels retained.'},**d};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'pages':len(changes),'cellsRepaired':len(audit['badCells']),'sourcesUnchanged':all(q['sourcePixelsUnchanged']for q in changes)},indent=2))
