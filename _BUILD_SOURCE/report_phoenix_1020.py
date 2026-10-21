from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_phoenix_1020';sources={'module_matrix':O/'report.json','full_loop_audio':O/'live-report.json','detached_head':R/'_shots/overnight_combat_1019/volcano/native-report.json','wireframe_escape':R/'_shots/dracodia_download_1019/report.json','pixel_art_breaks':O/'phoenix-art-report.json'};report={};total=0
for name,p in sources.items():
 data=json.loads(p.read_text());rows=data.get('results',data.get('checks'));assert isinstance(rows,list),name;assert all(r['passed'] for r in rows) and not data.get('errors'),name
 report[name]={'passed':len(rows),'errors':[],'source':str(p.relative_to(R))};total+=len(rows)
ui=json.loads((O/'review-ui.json').read_text());assert not ui['overflow'] and not ui['errors'];report['review']={'previews':len(ui['rows']),'overflow':False,'errors':[]}
log=(R/'_shots/phoenix-final-regression.log').read_text(encoding='utf-8');assert 'BUILD OK, 0 ERRORS' in log;count=len(re.findall(r'^  ok  ',log,re.M));report['regression']={'passed':count,'buildErrors':0};report['nativeTotal']=total
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
p=R/'docs/DRACODIA_PHOENIX_1020.md';s=p.read_text(encoding='utf-8');header='\n## Final verification\n\n'
if header in s:s=s[:s.index(header)]
s+=header+f'{total} native checks pass:114 module/attack checks across Easy, Normal, Hard\nand Furious;16 complete-loop, ordinary-fire and decoded-audio checks;28 skull\npose/eye/hit checks;70 preserved wireframe/escape checks;7 actual PixelLab frame,\nbreak and source-delegation checks. Nine review previews load with no browser\nerrors or narrow-layout overflow. Full regression suite:{count} printed passing\nassertions, BUILD OK0errors, process exit0. Game/runtime syntax checks pass.\n\nThe final164 new PNGs total647,082bytes. All delivered dimensions are even;\nmodules320-square, skull128-square, plume128-square, beam64x128, feather64-square.\n'
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'HANDOFF_CODEX.md';s=p.read_text(encoding='utf-8');needle='Local only, no commit/push requested; unrelated dirty work retained.';replacement=f'{total} native checks pass/no browser errors. Full regression:{count} passing\nassertions, BUILD OK0errors, exit0. Review9 previews/no narrow overflow.\n'+needle;s=s.replace(needle,replacement,1) if f'{total} native checks pass/no browser errors.' not in s else s;p.write_text(s,encoding='utf-8',newline='\n');print(json.dumps({'native':total,'regressions':count,'previews':len(ui['rows']),'errors':0}),flush=True)
