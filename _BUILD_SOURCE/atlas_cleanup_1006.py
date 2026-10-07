"""Archive obsolete art; losslessly prune the superseded portrait atlas.

--apply uses the measured cleanup plan. --verify checks every archived byte and
every retained atlas cell. --restore restores this batch only if its edited files
still match, protecting later work. The archive is never part of a release.
"""
import argparse,hashlib,json,re,shutil,io
from pathlib import Path
from PIL import Image

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def assignment(raw,name):
 text=raw.decode('utf-8');marker='window.'+name+'=';i=text.index(marker)+len(marker)
 value,n=json.JSONDecoder().raw_decode(text[i:]);return value,text,i,i+n
def replace_assignment(raw,name,value):
 _,text,a,b=assignment(raw,name)
 return (text[:a]+json.dumps(value,ensure_ascii=False,separators=(',',':'))+text[b:]).encode('utf-8')
def inside(p,root):
 p=p.resolve();assert p.is_relative_to(root.resolve()),f'Unsafe path: {p}';return p
def packing(items):
 best=None
 for width in range(1472,3073,64):
  x=y=4;row=0;rects={}
  for k,im in sorted(items.items(),key=lambda v:(-v[1].height,-v[1].width,v[0])):
   if x+im.width+4>width:x=4;y+=row+4;row=0
   rects[k]=[x,y,im.width,im.height];x+=im.width+4;row=max(row,im.height)
  height=((y+row+4+7)//8)*8
  if best is None or width*height<best[0]:best=(width*height,width,height,rects)
 _,w,h,rects=best;canvas=Image.new('RGBA',(w,h))
 for k,im in items.items():canvas.paste(im,(rects[k][0],rects[k][1]))
 return canvas,rects

ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--plan-file',type=Path);ap.add_argument('--apply',action='store_true');ap.add_argument('--verify',action='store_true');ap.add_argument('--restore',action='store_true');args=ap.parse_args()
R=args.root.resolve();O=R/'_BUILD_SOURCE/asset_cleanup_1006';P=args.plan_file or O/'plan.json';A=inside(R/'UNUSED_ASSETS/cleanup_2026-10-06',R);J=A/'archive-manifest.json'
if args.restore:
 j=json.loads(J.read_text());assert j['status']=='complete'
 for path,digest in j['edited_after'].items():assert sha(R/path)==digest,f'Later edits found: {path}; restore manually from journal'
 for entry in j['files']:
  src=inside(A/entry['path'],A);dst=inside(R/entry['path'],R)
  assert sha(src)==entry['sha256']
  assert not dst.exists() or entry['path']=='assets/game/atlas/ui_dialogue.png' or entry['path'] in j.get('reserved_after',[]),f'New file would be overwritten: {dst}'
 for entry in j['files']:
  src=A/entry['path'];dst=R/entry['path'];dst.parent.mkdir(parents=True,exist_ok=True)
  if dst.exists():dst.unlink()
  src.rename(dst)
 for path in ['assets/manifest.js','assets/game.js']:shutil.copy2(A/'_snapshots'/path,R/path)
 j['status']='restored';J.write_text(json.dumps(j,indent=2));print('Restored cleanup batch; archive snapshots and journal retained.');raise SystemExit
if args.verify:
 j=json.loads(J.read_text());assert j['status']=='complete'
 for entry in j['files']:
  p=inside(A/entry['path'],A);assert sha(p)==entry['sha256'],str(p)
  if entry['path']!='assets/game/atlas/ui_dialogue.png' and entry['path'] not in j.get('reserved_after',[]):assert not (R/entry['path']).exists(),entry['path']
 for path,digest in j['edited_after'].items():assert sha(R/path)==digest,path
 before=assignment((A/'_snapshots/assets/manifest.js').read_bytes(),'BOFX')[0];after=assignment((R/'assets/manifest.js').read_bytes(),'BOFX')[0]
 old=Image.open(A/'assets/game/atlas/ui_dialogue.png').convert('RGBA');new=Image.open(R/'assets/game/atlas/ui_dialogue.png').convert('RGBA');compared=0
 for k,c in after['cells'].items():
  if c[0]=='ui_dialogue':
   b=before['cells'][k];assert old.crop((b[1],b[2],b[1]+b[3],b[2]+b[4])).tobytes()==new.crop((c[1],c[2],c[1]+c[3],c[2]+c[4])).tobytes(),k;compared+=1
  else:assert c==before['cells'][k],k
 assert not any(k.startswith(('port_','face_')) for k,c in after['cells'].items() if c[0]=='ui_dialogue')
 print(json.dumps({'archived_files':len(j['files']),'archived_bytes':sum(x['bytes'] for x in j['files']),'live_cells':len(after['cells']),'pixel_identical_repacked_cells':compared,'other_cells_unchanged':len(after['cells'])-compared,'status':'verified'},indent=2));raise SystemExit
plan=json.loads(P.read_text());raw=(R/'assets/manifest.js').read_bytes();game=(R/'assets/game.js').read_bytes()
assert hashlib.sha256(raw).hexdigest()==plan['manifest_sha256'],'Manifest changed since audit'
assert hashlib.sha256(game).hexdigest()==plan['game_sha256'],'Runtime changed since audit'
fx=assignment(raw,'BOFX')[0];entries=list(plan['candidates']);names={e['path'] for e in entries}
for sheet in ['retired_rigs_0','retired_rigs_1','retired_rigs_2']:
 path=fx['img']['nca_'+sheet];assert path=='assets/game/atlas/'+sheet+'.png'
 if path not in names:entries.append({'path':path,'bytes':(R/path).stat().st_size,'sha256':sha(R/path),'reason':'Retired prototype/editor-only sheet; available from separate archive, excluded from release'})
path='assets/game/atlas/ui_dialogue.png';entries.append({'path':path,'bytes':(R/path).stat().st_size,'sha256':sha(R/path),'reason':'Original atlas snapshot; only current dialogue panels are losslessly repacked'})
old=Image.open(R/path).convert('RGBA');removed={k:c for k,c in fx['cells'].items() if c[0]=='ui_dialogue' and k.startswith(('port_','face_'))}
items={k:old.crop((c[1],c[2],c[1]+c[3],c[2]+c[4])) for k,c in fx['cells'].items() if c[0]=='ui_dialogue' and k not in removed}
image,rects=packing(items);buf=io.BytesIO();image.save(buf,format='PNG',compress_level=9);png=buf.getvalue()
for k in removed:del fx['cells'][k]
for k,rect in rects.items():fx['cells'][k]=['ui_dialogue']+rect
archive_paths={e['path'] for e in entries if e['path']!=path};changed_registrations=0
for k,v in list(fx['img'].items()):
 if v in archive_paths:fx['img'][k]=A.relative_to(R).as_posix()+'/'+v;changed_registrations+=1
newraw=replace_assignment(raw,'BOFX',fx)
audio=assignment(newraw,'BOFA')[0];unused=[k for k in audio['music'] if k.startswith('unused')]
for k in unused:del audio['music'][k]
newraw=replace_assignment(newraw,'BOFA',audio)
newgame,n=re.subn(rb'^[ \t]*BOFA\.music\.unused\w*=.*;\n',b'',game,flags=re.M);assert n==6,n
# Archived prototype roots are local tooling dependencies, never stage preload items.
newgame=newgame.replace(b'    if(!root||seen[root]||!XART._src[root])continue;\n    seen[root]=1;roots.push(root);',b"    if(!root||seen[root]||!XART._src[root])continue;\n    /* Archived prototype cells remain available to local art tools. Broad legacy prefix lists\n       must never queue their sheets as production stage dependencies. */\n    if(XART._src[root].startsWith('UNUSED_ASSETS/'))continue;\n    seen[root]=1;roots.push(root);")
summary={'files':len(entries),'archived_MB':sum(e['bytes'] for e in entries)/1e6,'removed_portrait_cells':len(removed),'old_atlas_size':list(old.size),'new_atlas_size':list(image.size),'atlas_bytes_saved':len((R/path).read_bytes())-len(png),'archive_only_registrations':changed_registrations,'removed_unused_music_aliases':unused}
print(json.dumps(summary,indent=2),flush=True)
if not args.apply:raise SystemExit
assert not A.exists(),'Archive batch already exists; use --verify or --restore'
# Preflight every source and resolved target before moving any file.
for e in entries:
 src=inside(R/e['path'],R/'assets');dst=inside(A/e['path'],A)
 assert src.is_file() and sha(src)==e['sha256'],str(src);assert not dst.exists(),str(dst)
A.mkdir(parents=True)
for p in ['assets/manifest.js','assets/game.js']:
 dest=A/'_snapshots'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/p,dest)
j={'status':'prepared','files':entries,'removed_cells':removed,'summary':summary,'edited_after':{}}
J.write_text(json.dumps(j,indent=2))
for e in entries:
 src=R/e['path'];dst=A/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
(R/path).write_bytes(png);(R/'assets/manifest.js').write_bytes(newraw);(R/'assets/game.js').write_bytes(newgame)
j['edited_after']={p:sha(R/p) for p in ['assets/manifest.js','assets/game.js','assets/game/atlas/ui_dialogue.png']};j['status']='complete';J.write_text(json.dumps(j,indent=2))
(A/'README.txt').write_text('Unused BOF assets archived October 6, 2026. Original relative paths and hashes are in archive-manifest.json. Packed source donors and superseded art are preserved unchanged. Retired prototype sheets can still be opened locally by the developer tools through archive-only registrations; they do not ship. Production portrait aliases resolve to the current authored renderer. Before rebuilding an older atlas, restore its archived source files with _BUILD_SOURCE/restore_art_source_1006.py. Do not include UNUSED_ASSETS in game ZIPs.\n')
print('Cleanup complete. Run --verify and the game test suite.',flush=True)
