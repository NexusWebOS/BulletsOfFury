from pathlib import Path
import json,html
W=Path(__file__).resolve().parent;O=W/'review';R=json.loads((O/'report.json').read_text(encoding='utf-8'))
def stamp(t):
 s=int(t);return f'{s//3600:02}:{s//60%60:02}:{s%60:02}'
chapters=[];last=None;stage7visits=0
for e in R['events']:
 if e['type']!='chapter':continue
 state,stage,role,scene=e['chapter'].split('|',3)
 if state not in ['campaignintro','play','stageclear','cutscene','victory','stagesel']:continue
 if stage=='7' and state=='play' and not role:stage7visits+=1
 label=('Stage '+stage+' '+role if role else {'campaignintro':'Opening cinematic','stageclear':'Stage '+stage+' results','cutscene':'Stage '+stage+' story','victory':'Final ending (continues in supplement)','stagesel':'Campaign map'}.get(state,'Stage '+stage+' flight'))+((' / '+scene)if scene else'')
 if scene.startswith('ht23-announcement'):continue
 if stage=='7':label+= ' (first visit, abandoned)' if e['t']<2800 else ' (full return)'
 if label==last:continue
 chapters.append({'time':e['t'],'title':label});last=label
for e in R['events']:
 if e['type']=='god-enabled':chapters.append({'time':e['t'],'title':'God mode enabled after native death'})
 if e['type']=='route-navigation' and e['t']>2700:chapters.append({'time':e['t'],'title':'Review map intervention for earned Harrier route'})
 if e['type']!='phase' or not e.get('phase','').startswith('vileexistence'):continue
 phase=e['phase'];label=None
 if 'dr5er23rebirth|encounter0' in phase:label='Dracodia symbiote rebirth'
 elif 'v18formIn' in phase:
  form=phase.split(':form')[1].split(':')[0]
  label='Dracodia copy: '+{'8':'corrupted Hammer','1':'helicopter','6':'Neural Archon brain','2':'volcano'}.get(form,form)
 elif '|dr5Death|' in phase:label='Dracodia final destruction'
 if label:chapters.append({'time':e['t'],'title':label})
chapters.sort(key=lambda c:c['time'])
for c in chapters:
 cue=[e for e in R['events'] if e['type']=='music' and e['t']<=c['time']+.5]
 c['musicCue']=cue[-1]['name'] if cue else 'native opening audio'
buttons='\n'.join(f'<button data-time="{c["time"]}"><time>{stamp(c["time"])}</time> {html.escape(c["title"])}</button>'for c in chapters)
body='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BOF Maverick Furious Beta Playthrough</title><style>body{background:#10151c;color:#edf3f8;font:16px system-ui;max-width:1450px;margin:24px auto;padding:0 20px}h1{font-size:27px}video{width:100%;background:black}main{display:grid;grid-template-columns:1fr 320px;gap:20px}aside{max-height:78vh;overflow:auto}button{display:block;text-align:left;width:100%;padding:9px;border:0;border-bottom:1px solid #3a4656;color:#e6effa;background:#192533;cursor:pointer}button:hover{background:#30465d}time{color:#88d7ff;margin-right:8px}a{color:#8bdcff}@media(max-width:900px){main{display:block}aside{max-height:350px}}.note{color:#d4bfa1}</style><h1>Maverick / Furious — full beta playthrough</h1><p class="note">Actual live BOF engine. Native combat, audio and campaign progression. God mode enabled after the first native death; normal weapons, pickups, ammunition and enemy health. Automated input, not a human skill clear.</p><p><a href="BETA_TEST_REPORT_1024.md">Beta report and recommended change strategy</a> · <a href="chapters.txt">Chapters</a></p><main><section><video controls preload="metadata" src="Maverick-Furious-Beta-Playthrough.mp4"></video><p id="status"></p></section><aside>'''+buttons+'''</aside></main><script>const v=document.querySelector('video');for(const b of document.querySelectorAll('button'))b.onclick=()=>{v.currentTime=+b.dataset.time;v.play()};v.ontimeupdate=()=>document.querySelector('#status').textContent=new Date(v.currentTime*1000).toISOString().slice(11,19);</script></html>'''
body=body.replace('</p><main>', ' · <a href="Maverick-Story-Replays.mp4">Complete post-1 / post-3 scenes</a> · <a href="Maverick-Complete-Ending-Replay.mp4">Complete ending replay</a></p><main>')
body=body.replace('Automated input, not a human skill clear.', 'Automated input, not a human skill clear. An earned-route map intervention is retained. The movie stops during the expanded ending; its complete native replay is supplied separately. Two early story scenes also have complete separate replays.')
(O/'index.html').write_text(body,encoding='utf-8')
(O/'chapters.json').write_text(json.dumps(chapters,indent=2),encoding='utf-8')
(O/'chapters.txt').write_text('\n'.join(stamp(c['time'])+' '+c['title']for c in chapters)+'\n',encoding='utf-8')
print('Gallery:',len(chapters),'chapters')
