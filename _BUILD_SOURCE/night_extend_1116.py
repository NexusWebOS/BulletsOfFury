from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
O=R/'_shots/cinema_overnight_1116'
# Retain current native probe semantics; isolate evidence and disable public submission.
specs=[('probe_drone_rework_1026.py','night_drone_1116.py',"'_shots/drone_rework_1026/probe'","'_shots/cinema_overnight_1116/drone'"),('probe_dracodia_forms_1026.py','night_forms_1116.py',"'_shots/dracodia_forms_1026/probe'","'_shots/cinema_overnight_1116/forms'")]
for src,dst,old,new in specs:
 s=(R/'_BUILD_SOURCE'/src).read_text(encoding='utf8').replace(old,new)
 s=s.replace("p.wait_for_function('()=>{stageLoadTick();", "p.evaluate('()=>{BOFOnline.submitScore=()=>{}}');p.wait_for_function('()=>{stageLoadTick();",1)
 (R/'_BUILD_SOURCE'/dst).write_text(s,encoding='utf8',newline='\n')
s=(R/'_BUILD_SOURCE/stage56_cinematics_1114_record.py').read_text(encoding='utf8')
s=s.replace("ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source')",'ROOT=Path(__file__).resolve().parents[1]')
s=s.replace("'_shots/stage56_cinematics_1114'","'_shots/cinema_overnight_1116/stage56'")
s=s.replace("p.evaluate(shoot.TRAP_RAF)","p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{}}')")
(R/'_BUILD_SOURCE/night_stage56_record_1116.py').write_text(s,encoding='utf8',newline='\n')
summary={}
for part in ['dialogue/after.json','loading/after.json','arrivals-fresh/report.json']:
 d=json.loads((O/part).read_text(encoding='utf8'))
 if 'checks'in d:summary[part]={'pass':sum(bool(q.get('ok',q.get('passed')))for q in d['checks']),'fail':[q['name']for q in d['checks']if not q.get('ok',q.get('passed'))]}
 else:summary[part]={'count':len(d['rows']),'approaches':sum(q.get('approachSeen')is True for q in d['rows']),'fail':[q['case']for q in d['rows']if not q['reachedPlay']or q['errors']or q['stepError']]}
files=sorted((O/'arrivals-fresh').glob('*-play.png'))
sheet=Image.new('RGB',(1440,((len(files)+3)//4)*278),(7,12,19));draw=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((360,250));x=i%4*360;y=i//4*278;sheet.paste(im,(x,y));draw.text((x+5,y+252),f.stem,fill='white')
sheet.save(O/'arrivals-fresh/contact.jpg')
print(json.dumps(summary,indent=2))
