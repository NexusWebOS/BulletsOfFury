from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/instructor_bob_1020';D=R/'assets/game/levels/tutorial/stormglass_1020/instructor_bob';O=R/'_shots/instructor_bob_1020'
report={}
original=Image.open(A/'returned/bob.png').convert('RGBA');combined=Image.new('RGBA',(256,256))
for n in ['core','missile','cannon']:combined.alpha_composite(Image.open(D/n/'live.webp').convert('RGBA'))
report['live_recomposition_exact']=np.array_equal(np.array(original),np.array(combined))
art=json.loads((D/'manifest.json').read_text(encoding='utf-8'));report['no_pending_jobs']=not art['pending_turntables'];report['turntables']={}
for name,a in art['views'].items():
 frames=[Image.open(p).convert('RGBA') for p in sorted((A/'returned'/('turn_'+name)).glob('frame_*.png'))][1:]
 bounds=[im.getbbox() for im in frames];w,h=frames[0].size
 unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames})
 margins=[min(b[0],b[1],w-b[2],h-b[3]) for b in bounds]
 sheet=Image.open(R/a['path']).convert('RGBA')
 exact=all(np.array_equal(np.array(im),np.array(sheet.crop((x,y,x+cw,y+ch)))) for im,(x,y,cw,ch) in zip(frames,a['cells']))
 report['turntables'][name]={'frames':len(frames),'unique':unique,'canvas':[w,h],'pivot':[w//2,h//2],'minimum_alpha_margin':min(margins),'cells_exact':exact,'max_texture_side':max(sheet.size),'all_nonblank':all(bounds)}
report['protected_hashes']={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['assets/game.js','_BUILD_SOURCE/test_fl.js','assets/command_ui_1020.js','assets/stormglass_tutorial_1020.js','assets/stage1_water_1020.js']}
images=[R/a['path'] for a in [*art['portraits'],art['whole'],art['card'],*art['parts'].values(),*art['views'].values()]]
report['runtime_bytes']=sum(p.stat().st_size for p in images)+sum((R/p).stat().st_size for p in ['assets/instructor_bob_1020.js','assets/instructor_bob_art_1020.js'])
report['even_images']=all(Image.open(p).width%2==Image.open(p).height%2==0 for p in images)
report['passed']=report['live_recomposition_exact'] and report['no_pending_jobs'] and report['even_images'] and all(a['frames']==32 and a['unique']>=30 and a['cells_exact'] and a['minimum_alpha_margin']>=1 and a['all_nonblank'] and a['max_texture_side']<=2048 for a in report['turntables'].values())
(O/'art-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
