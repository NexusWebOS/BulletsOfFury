from pathlib import Path
import json,hashlib,zlib,shutil,time
from github_api import R
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';rows=json.loads((O/'changes.json').read_text());objects={};files=[]
for i,r in enumerate(rows):
 p=R/r['path']
 if not p.is_file():continue
 h=hashlib.sha1();h.update(b'blob '+str(p.stat().st_size).encode()+b'\0');z=zlib.compressobj(1);compressed=0
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);compressed+=len(z.compress(b))
 compressed+=len(z.flush());oid=h.hexdigest();objects.setdefault(oid,dict(bytes=p.stat().st_size,compressed=compressed));files.append(dict(path=r['path'],oid=oid,bytes=p.stat().st_size,compressed=compressed))
 if i%700==0:print('HASHED',i,'/',len(rows),'unique compressed MB',round(sum(x['compressed']for x in objects.values())/1e6),flush=True)
result=dict(files=files,uniqueObjects=len(objects),uniqueBytes=sum(x['bytes']for x in objects.values()),compressedBytes=sum(x['compressed']for x in objects.values()),free=shutil.disk_usage(R).free);(O/'object-plan.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items()if k!='files'},flush=True)
