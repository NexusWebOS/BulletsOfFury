from pathlib import Path
import shutil,json,hashlib,subprocess,os,time
from github_api import R
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';old=R/'UNUSED_ASSETS/retired_art_1022';dest=R/'_BUILD_SOURCE/test_references_1022';dest.mkdir(exist_ok=True);entries=json.loads((old/'manifest.json').read_text())
for q in entries:
 p=old/q['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==q['sha256'];target=dest/q['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
shutil.copy2(old/'manifest.json',dest/'manifest.json')
p=R/'_BUILD_SOURCE/retired_art_archive_1022.cjs';b=p.read_bytes();s=b.decode();nl='\r\n'if'\r\n'in s else'\n';line="const archive=path.resolve(__dirname,'../UNUSED_ASSETS/retired_art_1022');";new="const localArchive=path.resolve(__dirname,'../UNUSED_ASSETS/retired_art_1022');"+nl+"const portableArchive=path.resolve(__dirname,'test_references_1022');"+nl+"const archive=process.env.BOF_RETIREMENT_ARCHIVE||(fs.existsSync(path.join(localArchive,'manifest.json'))?localArchive:portableArchive);"
if line in s:
 (W/'retired_art_archive_1022.before.cjs').write_bytes(b);s=s.replace(line,new);assert p.read_bytes()==b;p.write_bytes(s.encode())
else:assert 'const portableArchive='in s
# Keep the exact recovered leech inputs reproducible without the ignored cleanup folder.
ref=R/'_BUILD_SOURCE/release_checks_1114/references/armored_leech';ref.mkdir(parents=True,exist_ok=True)
for source in(R/'UNUSED_ASSETS/cleanup_2026-10-06/assets/game/stage8_mega_enemies/armored_leech').glob('*.png'):shutil.copy2(source,ref/source.name)
for p in[R/'_BUILD_SOURCE/release_checks_1114/repair.py',W.parent/'release_checks_1114/repair.py']:
 b=p.read_bytes();s=b.decode();line="source=R/'UNUSED_ASSETS/cleanup_2026-10-06/assets/game/stage8_mega_enemies/armored_leech';E=W/'exports';";new="source=R/'UNUSED_ASSETS/cleanup_2026-10-06/assets/game/stage8_mega_enemies/armored_leech';source=source if source.exists()else R/'_BUILD_SOURCE/release_checks_1114/references/armored_leech';E=W/'exports';"
 if line in s:assert p.read_bytes()==b;p.write_bytes(s.replace(line,new).encode())
(dest/'README.md').write_text('Exact development-only retired reference fixtures for the existing integrity harness. These135 files retain the manifest SHA256 values. They are not loaded by index.html or included in the playable Windows payload. The harness uses this tracked fallback when the optional ignored UNUSED_ASSETS archive is absent.\n',encoding='utf-8')
print('Portable reference inputs saved:',len(entries),'files; running full suite with the ignored archive disabled.',flush=True)
env=dict(os.environ,BOF_RETIREMENT_ARCHIVE=str(dest));start=time.monotonic();q=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');text=q.stdout+q.stderr;(O/'full-suite-portable.log').write_text(text,encoding='utf-8');result=dict(exit=q.returncode,passed=sum(l.startswith('  ok')for l in text.splitlines()),summary='==== FALVA/LIZZIE BUILD OK, 0 ERRORS ===='in text,referenceFiles=len(entries),referenceBytes=sum((dest/q['path']).stat().st_size for q in entries),seconds=time.monotonic()-start,failures=[l for l in text.splitlines()if'ASSERT FAIL:'in l]);(O/'portable-checks.json').write_text(json.dumps(result,indent=2));assert result['exit']==0 and result['summary'],text[-3500:];print('PORTABLE FULL CHECKS',result['passed'],'passed,0 failures',flush=True)
