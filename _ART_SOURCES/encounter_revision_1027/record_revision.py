from pathlib import Path
import sys,importlib.util
W=Path(__file__).resolve().parent;P=W.parent/'BOF-Final-Pass-1027/record_all.py'
spec=importlib.util.spec_from_file_location('native_recorder',P);rec=importlib.util.module_from_spec(spec);spec.loader.exec_module(rec);rec.OUT=W
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed<25||','const demonstrate=elapsed<(cfg.demonstrate||25)||')
rec.SNAPSHOT=rec.SNAPSHOT.replace('const M=b?._s7mod,F=b?._s9fusion;','const M=b?._s7mod,F=b?._s9fusion,H=b?._hd1003;').replace("mode:M?.mode||S?.mode", "mode:M?.mode||H?.mode||S?.mode").replace("attack:S?.v18?.attack?.type||null", "attack:H?.er28?.kind||S?.v18?.attack?.type||null")
jobs=[dict(id='revised-stage6-harrier',stage=6,role='boss',kind='warhive',name='Stage 6 / Harrier / Revised Turrets and Helpers',limit=1000),
dict(id='revised-stage6-rebels',stage=6,role='boss',kind='rebelsquad',name='Stage 6 / Rebel Fighters / Allied Intro and Rook Guns',limit=1100),
dict(id='final-stage7-dredger',stage=7,role='mini',kind='dualscoopdredger',name='Stage 7 / Caustic Dredger / Toxic Slugs and Mortars',limit=900),
dict(id='stage7-warden-final',stage=7,role='boss',kind='sludgeemperor',name='Stage 7 / Toxic Warden / Canisters and Final Hops',limit=1200,demonstrate=30),
dict(id='final-stage8-herald',stage=8,role='mini',kind='heralddeath',name='Stage 8 / Herald of Death / Red Chaos Arsenal',limit=900,demonstrate=100)]
selected=set(sys.argv[1:])
for job in jobs:
 if selected and job['id']not in selected:continue
 rec.CONFIG=job;rec.record(job['stage'],job['limit'])
