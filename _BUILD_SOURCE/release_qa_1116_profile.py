from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
src=Path(__file__).with_name('release_pacing_1116.py')
if not src.exists():src=Path(__file__).with_name('release_qa_1116_pacing.py')
code=src.read_text(encoding='utf8').replace("O=R/'_shots/release_qa_1116/pacing'","O=R/'_shots/release_qa_1116/profile'").replace('for stage in [5,6,8,9]:','for stage in [6]:').replace("p.keyboard.down('j');p.wait_for_timeout(20000)","cdp=context.new_cdp_session(p);cdp.send('Profiler.enable');cdp.send('Profiler.start');p.keyboard.down('j');p.wait_for_timeout(12000)")
code=code.replace("q=p.evaluate(\"()=>{Pace16.end=performance.now();", "profile=cdp.send('Profiler.stop')['profile'];(O/'stage6-profile.json').write_text(json.dumps(profile),encoding='utf8');q=p.evaluate(\"()=>{Pace16.end=performance.now();")
exec(compile(code,str(src),'exec'),{'__file__':str(src),'__name__':'__main__'})
p=json.loads((R/'_shots/release_qa_1116/profile/stage6-profile.json').read_text(encoding='utf8'));nodes={n['id']:n for n in p['nodes']};weighted={}
for n,dt in zip(p['samples'],p['timeDeltas']):weighted[n]=weighted.get(n,0)+dt
rows=[{'ms':round(t/1000,1),'fn':nodes[n]['callFrame']['functionName'],'url':nodes[n]['callFrame']['url'].split('/')[-1],'line':nodes[n]['callFrame']['lineNumber']+1}for n,t in sorted(weighted.items(),key=lambda a:-a[1])[:35]]
(R/'_shots/release_qa_1116/profile/hotspots.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows[:15]),flush=True)
