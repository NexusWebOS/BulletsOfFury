"""Offline export of archived PixelLab sources. No generation/API required."""
from pathlib import Path
import argparse,json,subprocess,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_09/miniboss/horizon_plasma_1031'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);p.add_argument('--ffmpeg',default='ffmpeg');args=p.parse_args()
subprocess.run([args.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script-param','input='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for a in m.values():a['sha256']=hashlib.sha256((R/a['path']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/horizon_plasma_art_1031.js').write_text("'use strict';\nconst EH85_ART="+json.dumps(m,separators=(',',':'))+';\n')
A=R/'_ART_SOURCES/horizon_plasma_1031';A.mkdir(parents=True,exist_ok=True)
for f in D.glob('*.aseprite'):shutil.copy2(f,A/f.name)
S=R/'assets/game/shared/audio/horizon_mix_1031';sources=json.loads((S/'provenance.json').read_text())
for role,q in sources.items():
 if role=='sustain':continue
 src=R/q['source'];assert hashlib.sha256(src.read_bytes()).hexdigest()==q['sourceSHA256']
 subprocess.run([args.ffmpeg,'-v','error','-y','-i',str(src),'-af',q['processing'],'-ar','44100','-ac','2',str(R/q['master'])],check=True)
 subprocess.run([args.ffmpeg,'-v','error','-y','-i',str(R/q['master']),'-c:a','libmp3lame','-b:a','192k',str(R/q['runtime'])],check=True)
q=sources['sustain'];subprocess.run([args.ffmpeg,'-v','error','-y','-stream_loop','4','-i',str(S/'release.wav'),'-af','atrim=duration=2.4,afade=t=in:d=0.04,afade=t=out:st=2.36:d=0.04','-ar','44100',str(R/q['master'])],check=True);subprocess.run([args.ffmpeg,'-v','error','-y','-i',str(R/q['master']),'-b:a','192k',str(R/q['runtime'])],check=True)
print('Exported six bounded authored banks and six sound roles')
