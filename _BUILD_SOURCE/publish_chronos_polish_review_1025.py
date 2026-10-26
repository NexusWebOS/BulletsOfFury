"""Publish the completed local capture with chapters from its actual timeline."""
from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parents[1]
report=json.loads((R/'_shots/chronos_polish_1025/video/review.json').read_text())
assert report['defeated'], 'Do not publish an incomplete capture as a full fight'
p=R/'docs/previews/chronos_frames_1025/index.html'
archive=p.with_name('palm-volleys-review.html')
if not archive.exists():shutil.copyfile(p,archive)
old=archive.read_text(encoding='utf8')
style=re.search(r'<style>(.*?)</style>',old,re.S).group(0)
videojs=re.search(r"const fight=document.querySelector\('#fight'\);(.*?)\nlet frame=",old,re.S).group(1)
chapters=[('Opening dialogue',6.8)]
for label,state in [('Electric chromium laser volleys','nova_release'),('Side-swing FOV','c27_depth_combo'),('Two-handed overhead', 'warn'),('Two-handed depth strike','giant_dive'),('Two-handed spin','whirlwind'),('Chromium activation','fr_activation'),('Armor break','c29_break'),('Minigun pickup','hb20_pickup'),('Minigun firing','chaingun'),('Rage transformation','hf22_rage_charge'),('Foreground palms','c30_volley_fire'),('Red lightning wave','c30_beam')]:
 rows=[q for q in report['timeline'] if q.get('state')==state]
 if rows:chapters.append((label,max(0,rows[0]['videoSeconds']-.5)))
for label,predicate in [('Background palms',lambda q:q.get('state')=='c30_volley_fire' and q.get('scale',1)<.5),('Minigun destroyed',lambda q:q.get('state')=='c29_break' and (q.get('gun') or 0)<0)]:
 rows=[q for q in report['timeline'] if predicate(q)]
 if rows:chapters.append((label,max(0,rows[0]['videoSeconds']-.5)))
rows=[q for q in report['timeline'] if q.get('state')=='c30_volley_move' and q.get('scale',1)<.5]
if rows:chapters.append(('Flight into background',max(0,rows[0]['videoSeconds']-1)))
if rows:
 returns=[q for q in report['timeline'] if q.get('state')=='c30_volley_move' and q.get('scale',0)>1 and q['videoSeconds']>rows[0]['videoSeconds']]
 if returns:chapters.append(('Return to foreground',max(0,returns[0]['videoSeconds']-1)))
armor=next((q for q in report['timeline'] if q.get('state')=='c29_break'),None)
if armor:chapters.append(('Hammer recall and catch',armor['videoSeconds']+3.1))
chapters.sort(key=lambda q:q[1])
dead=next(q for q in report['timeline'] if q['dead']);chapters.append(('Defeat',max(0,dead['videoSeconds']-2)))
buttons=''.join(f'<button onclick="playAt({t:.2f})">{label}</button>' for label,t in chapters)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Chronos â€” full fight with red lightning and ElevenLabs audio</title>'''+style+'''
<main><h1>Chronos â€” full fight</h1><p>Minigun reaches full speed at four seconds, with triple module health. Shorter hit flashes preserve pose readability; new ambient rocks and supply arrivals pause during major charge-ups. Pilot portraits restored. Chronos speaks beside his body in the stylish font. Blue recovery frames, authored death-pose armor stun, absorbing shield, and dedicated ElevenLabs effects for hammer smash and charge. Opening dialogue through defeat. Red-and-white waves darken the scene and bring down animated red lightning. New ElevenLabs effects cover rage, energy gathering, palm blasts, wave release and electrical impacts.</p>
<video id="fight" controls playsinline preload="metadata" src="../../../_shots/chronos_polish_1025/video/chronos-full-fight.mp4?revision=gun-flash-clutter-1025"></video>
<nav><button onclick="playAt(0)">Play full fight with sound</button>'''+buttons+'''</nav>
<nav><label>Speed <select onchange="fight.playbackRate=Number(this.value)"><option value="1">Normal</option><option value=".5">Half speed</option><option value=".25">Quarter speed</option></select></label><button onclick="stepVideo(-1)">Previous frame</button><button onclick="stepVideo(1)">Next frame</button></nav>
<p>Furious difficulty, Cole, level-5 Fusion starting loadout. Invulnerability is enabled and labelled for this animation review. One continuous native fight using movement and firing inputs; no health or phase checkpoints. The opening radio dialogue is included, with scrolling active.</p>
<p><a href="palm-volleys-review.html">Previous palm-animation review</a> Â· <a href="full-turn-gold-red-review.html">Previous minigun review</a></p></main><script>const fight=document.querySelector('#fight');'''+videojs+'''</script></html>'''
p.write_bytes(html.encode('utf8'))
qa=R/'docs/qa/chronos_polish_video_1025.json';d=json.loads(qa.read_text());d['recording']={k:report[k] for k in ['difficulty','invulnerable','loadout','route','defeated','errors','video']};d['recording']['audio']=report['audio'];d['recording']['chapters']=chapters;qa.write_text(json.dumps(d,indent=2),encoding='utf8')
print(json.dumps({'chapters':chapters,'seconds':report['timeline'][-1]['videoSeconds'],'audio':report['audio']['playing'],'errors':report['errors']}))
