from pathlib import Path
p=Path(__file__).with_name('night_scroll_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("b.text?.length>=210", "b.text?.length>=100")
needle='QSC16.sort((a,b)=>b.b.text.length-a.b.text.length);'
addition="const text=PILOT_OPENINGS.axel.beats.find(b=>b.who==='freezer').text;QSC16.push({pilot:'freezer',scene:'retained-optional-opening-widget',b:{id:'SCROLL-FREEZER',who:'FREEZER',text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people:['freezer','axel'],fpLocations:{freezer:'cockpit-sky',axel:'cockpit-sky'},duration:text.length/30+4,readings:[],_cueSet:new Set(),cm3:{group:'scroll-freezer',readAt:.42,newStrip:true,baseDuration:text.length/30+4}}});"
if addition not in s:s=s.replace(needle,addition+needle)
s=s.replace(" for i,c in enumerate(cases):", " (O/'cases.json').write_text(json.dumps(cases,indent=2),encoding='utf8');assert cases, 'No long-line candidates selected'\n for i,c in enumerate(cases):")
s=s.replace("assert not errors and all(q['done']", "assert len(rows)==24 and not errors and all(q['done']")
s=s.replace("24 longest distinct current native pilot/shot lines", "23 longest distinct current pilot/shot lines plus the retained real Freezer optional-opening line through the native current widget; no archived scene activated in the campaign")
p.write_text(s,encoding='utf8',newline='\n')
