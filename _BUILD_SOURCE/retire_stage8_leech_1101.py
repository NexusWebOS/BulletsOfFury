"""User-authorized Stage8 Leech deletion; no art archive or backups.
Owning atlas/reel/feedback builders call the matching migration functions.
Every retained packed cell is verified pixel-identical before registration.
"""
from pathlib import Path
import json,re,hashlib,subprocess,sys
from PIL import Image
R=Path(__file__).resolve().parents[1];Q=R/'_shots/stage8_amplify_1101';Q.mkdir(exist_ok=True)
def jsread(p):
 s=p.read_text(encoding='utf-8');m=re.search(r'(?:const\s+\w+|window\.BOF_STAGE_RUNTIME_ATLASES)\s*=\s*',s);return s[:m.end()],json.JSONDecoder().raw_decode(s[m.end():])[0]
def jswrite(p,head,x):p.write_text(head+json.dumps(x,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
def safe_unlink(p,deleted):
 p=p.resolve();assert p.is_relative_to(R.resolve()),p
 if p.is_file():p.unlink();deleted.append(p.relative_to(R).as_posix())
def retire_runtime_cells():
 p=R/'assets/game/shared/atlases/stage_runtime_atlases.js';head,x=jsread(p);keys=[k for k in x['cells']if'armored_leech'in k];pages={x['cells'][k][0]for k in keys};verified=0
 for page in pages:
  file=R/x['roots']['nca_'+page];im=Image.open(file).convert('RGBA');retained={k:v for k,v in x['cells'].items()if v[0]==page and k not in keys};hashes={k:hashlib.sha256(im.crop((v[1],v[2],v[1]+v[3],v[2]+v[4])).tobytes()).hexdigest()for k,v in retained.items()}
  for k in keys:
   v=x['cells'][k]
   if v[0]!=page:continue
   _,xx,yy,w,h=v
   assert all(xx+w<=z[1]or xx>=z[1]+z[3]or yy+h<=z[2]or yy>=z[2]+z[4]for z in retained.values()),'Overlapping retained atlas cell'
   im.paste((0,0,0,0),(xx,yy,xx+w,yy+h))
  for k,v in retained.items():assert hashes[k]==hashlib.sha256(im.crop((v[1],v[2],v[1]+v[3],v[2]+v[4])).tobytes()).hexdigest();verified+=1
  im.save(file,optimize=True)
 for k in keys:x['cells'].pop(k)
 jswrite(p,head,x);receipt={'removedCells':keys,'retainedCellsPixelIdentical':verified};(Q/'leech-atlas-removal.json').write_text(json.dumps(receipt,indent=2));print('Removed',len(keys),'Leech cells;',verified,'retained cells pixel-identical')
def retire_reels():
 p=R/'assets/stage8_art_1003.js';head,x=jsread(p);entry=x.pop('gravity',None);deleted=[]
 if entry:safe_unlink(R/entry['path'],deleted)
 jswrite(p,head,x)
 for p in[R/'assets/game/stage8_1003/manifest.json',R/'assets/game/levels/stage_08/stage/stage8_1003/manifest.json']:
  if p.exists():m=json.loads(p.read_text());m.pop('gravity',None);p.write_text(json.dumps(m,indent=2)+'\n')
 print('Removed gravity/Leech reel registration and',len(deleted),'runtime sheets')
def retire_feedback():
 p=R/'assets/animation_feedback_art_1023.js';head,x=jsread(p);x['models'].pop('s8leech',None)
 for k in list(x['sheets']):
  if's8leech'in k:x['sheets'].pop(k)
 jswrite(p,head,x)
 for folder in[R/'assets/game/levels/stage_08/enemies/animation_feedback_1023',R/'_ART_SOURCES/animation_feedback_1023/shipping']:
  p=folder/'manifest.json'
  if p.exists():p.write_text(json.dumps(x,indent=2)+'\n')
  p=folder/'animation_feedback_art_1023.js'
  if p.exists():jswrite(p,'"use strict";\nconst AQ23_ART=',x)
 print('Removed Leech feedback registrations')
def main():
 for script,flag in [('tools/pack_stage_runtime_atlases.py','--retire-stage8-leech'),('_BUILD_SOURCE/build_stage8_1003.py','--retire-leech'),('_BUILD_SOURCE/install_animation_feedback_1023.py','--retire-leech')]:subprocess.run([sys.executable,str(R/script),flag],cwd=R,check=True)
 candidates=[]
 r=subprocess.run(['rg','--files','assets','_ART_SOURCES','_BUILD_SOURCE','-g','*s8leech*','-g','*armored_leech*'],cwd=R,capture_output=True,text=True)
 candidates.extend(R/v for v in r.stdout.splitlines())
 for folder in[R/'assets/game/levels/stage_08/enemies/air_motion_1013/void_leech',R/'_ART_SOURCES/animation_feedback_1023/shipping']:
  if folder.exists():candidates.extend(p for p in folder.iterdir()if p.is_file()and(folder.name=='void_leech'or's8leech'in p.name))
 candidates.extend([R/'_ART_SOURCES/stage8_1003/gravity.png',R/'_BUILD_SOURCE/stage8_amplify_1101/gravity_identity.png',Q/'reference-contact.jpg'])
 deleted=[]
 for p in set(candidates):
  if p.suffix.lower()in['.png','.webp','.gif']or p.parent.name=='void_leech':safe_unlink(p,deleted)
 p=R/'assets/air_motion_art_1013.js';head,x=jsread(p);x.pop('s8leech',None);jswrite(p,head,x)
 p=R/'assets/data/AIR_MOTION_1013.json';x=json.loads(p.read_text());x['entries'].pop('s8leech',None);p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
 def rejected(x):return any(v in str(x)for v in ['s8leech','armored_leech','/void_leech/','stage8_1003/gravity.png','s81003_gravity'])
 def prune(x):
  if isinstance(x,list):return[prune(v)for v in x if not(isinstance(v,(str,dict))and rejected(v))]
  if isinstance(x,dict):return{k:prune(v)for k,v in x.items()if not rejected(k)and not(isinstance(v,str)and rejected(v))}
  return x
 for p in[R/'assets/game/levels/stage_08/asset_index.json',R/'assets/data/asset_catalog.json']:
  x=json.loads(p.read_text(encoding='utf-8-sig'));p.write_text(json.dumps(prune(x),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (Q/'leech-deletion.json').write_text(json.dumps({'deletedFiles':sorted(deleted),'archiveCreated':False,'scope':'Stage8 Leech only; Stage5/Stage9 and shared weapon graphics retained'},indent=2));print('Deleted',len(deleted),'unique Leech graphics without an archive')
if __name__=='__main__':main()
