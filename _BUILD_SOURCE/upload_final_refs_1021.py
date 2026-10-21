from pathlib import Path
from PIL import Image
import sys,json,urllib.request,uuid,concurrent.futures
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';U=sys.argv[1]
rows=json.loads((S/'air-reference-manifest.json').read_text());refs=[]
# Only mobile aircraft/spacecraft are aircraft replacements. Stations, mines,
# elemental cores and walking machines retain their authored unit identities.
skip={'s5gravity','s5minelayer','s5satellite','s5portalmine','s5station','s5leech','s6probe','s6turbine','mm1003_riflelocust','mm1003_impharrow','mm1003_hellhugger','mm1003_hexpyre','s8leech','s8deathorb','s8solar','s8hunter','s8tentacle','pt11frostcarrier','mm1003_bluehybrid','mm1003_furnacemaw','s9beacon','s9ring','s9gateturret','s9prism','s9singularity','pmine','cbreak','mm1003_hellram','pneedle','dreadv','gleech'}
for row in rows:
 if row['id'] in skip:continue
 p=Path(row['path']);im=Image.open(p).convert('RGBA');im=im.resize((128,128),Image.Resampling.NEAREST);q=S/'refs'/('air128-'+row['id']+'.png');im.save(q);refs.append({**row,'path':str(q),'purpose':'air'})
for key in ['native-nes_bubble_0','native-nes_bubble_void_0','native-nx_small_3','fx_32bit_1','fx_FX_Vol1_0']:
 p=S/'refs'/(key+'.png');im=Image.open(p).convert('RGBA');im.thumbnail((256,256),Image.Resampling.NEAREST);q=S/'refs'/(key+'-upload.png');im.save(q);refs.append(dict(id=key,path=str(q),purpose='fx'))
def upload(row):
 p=Path(row['path']);boundary='bof-'+uuid.uuid4().hex;body=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="'+p.name+'"\r\nContent-Type: image/png\r\n\r\n').encode()+p.read_bytes()+('\r\n--'+boundary+'--\r\n').encode();req=urllib.request.Request(U,data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary},method='POST')
 with urllib.request.urlopen(req,timeout=90) as r:row['ref']=json.load(r)['ref']
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:refs=list(ex.map(upload,refs))
(S/'uploaded-final-references.json').write_text(json.dumps(refs,indent=2));print(json.dumps(refs))
