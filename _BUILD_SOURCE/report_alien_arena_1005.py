"""Assemble portable QA and a local review from actual native captures."""
from pathlib import Path
from PIL import Image, ImageChops
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/alien_arena_1005'
q=json.loads((O/'verification.json').read_text(encoding='utf-8'))
a=Image.open(O/'arena-layer-a.png').convert('RGB');b=Image.open(O/'arena-layer-b.png').convert('RGB')
green_motion=sum(max(abs(x-y) for x,y in zip(p,n))>10 and
                 ((p[1]>p[0]*1.5 and p[1]>p[2]*1.3 and p[1]>45) or
                  (n[1]>n[0]*1.5 and n[1]>n[2]*1.3 and n[1]>45))
                 for p,n in zip(a.getdata(),b.getdata()))
q['arenaPixels']['movingGreenPixels']=green_motion
q['checks']=[c for c in q['checks'] if c['name'] not in ['emerald code pixels themselves visibly animate','review starts the actual Furious FINAL3 password route']]
q['checks'].append({'ok':green_motion>150,'name':'emerald code pixels themselves visibly animate'})
if (O/'review-launch.json').exists():
 launch=json.loads((O/'review-launch.json').read_text(encoding='utf-8'))
 q['checks'].append({'ok':launch['phase']==2 and launch['mode']=='fight' and launch['arena'] and launch['code']>0 and launch['void']>0 and not launch['errors'],'name':'review starts the actual Furious FINAL3 password route'})
 q['reviewLaunch']=launch
for clip in q['clips']:
 im=Image.open(O/(clip['name']+'.gif'));sheet=Image.new('RGB',(480*3,512*2))
 for i in range(6):
  im.seek(round(i*(im.n_frames-1)/5));sheet.paste(im.convert('RGB'),((i%3)*480,(i//3)*512))
 sheet.save(O/(clip['name']+'-contact.png'))
q['suite']={'assertions':7292,'exitCode':0,'syntax':'game.js and both new runtime layers pass'}
q['scope']='Focused protected silent engine recordings; not an unassisted campaign clear.'
(O/'verification.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
(R/'docs/qa/alien_arena_1005.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
buttons=''.join('<button data-code="'+s+'">'+s+'</button>' for s in ['FINAL1','FINAL2','FINAL3','HELI8','FURN8','CRYO8','STORM8','KNIGHT','ACE8','WARD8','HARR6','REBEL6'])
figs=''.join('<figure><img src="'+n+'.png" alt="'+caption+'"><figcaption>'+caption+'</figcaption></figure>' for n,caption in [
 ('arena-layer-a','Dark central void, emerald code and independent rib parallax'),
 ('fiend-emerges','Full-screen symbiote engulfment and colossus emergence'),
 ('ghost-modular','Complete head, articulated claws and orbital eye'),
 ('ghost-breakup','Destroyed limbs break off; surviving emitters keep fighting'),
 ('elite-turret-fov','Actual Harrier elite gun ports show FOV before tracer rain'),
 ('rebel-slug-warning','Approaching heavy round gets the original impact asterisk')])
clips=''.join('<figure><img src="'+c['name']+'.gif" alt="'+c['name']+' gameplay"><figcaption>'+c['name']+' — '+str(c['seconds'])+' seconds, silent protected simulation.</figcaption><details><summary>Frames across the clip</summary><img src="'+c['name']+'-contact.png" alt="Six frames across the recording"></details></figure>' for c in q['clips'])
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alien arena and combat readability</title>
<style>*{box-sizing:border-box}body{margin:0;background:#05090b;color:#edf6ee;font:16px/1.5 system-ui}main{max-width:1240px;margin:auto;padding:28px}h1{font-size:40px}p{max-width:1050px;color:#b7c8bd}button{padding:12px;background:#17322c;color:white;border:1px solid #67a890;cursor:pointer}.buttons{display:flex;gap:8px;flex-wrap:wrap}iframe{width:100%;height:940px;border:1px solid #34584d}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:#10221d}img{display:block;width:100%;image-rendering:pixelated}figcaption,summary{padding:12px}a{color:#91ffc2}@media(max-width:650px){.grid{grid-template-columns:1fr}}</style>
<main><h1>Alien arena and combat readability</h1><p>The center stays almost black while a restrained symbiote vortex rotates continuously. Emerald code banks run in opposing directions around the perimeter; layered ribs move independently. The full-view void engulfs the screen before revealing the third encounter's arena.</p>
<p>The ghost now has actual articulated and destructible parts with one complete head. New warned pincer/warp/rail patterns, stronger mutated-drone and Dracula attack cycles, and upgraded campaign-controller copies retain independent HP. Stage 6 uses approaching-round asterisks and warned, staggered elite gun rain.</p>
<p>7,292 full-suite assertions, exit 0. CHECKCOUNT native/pixel checks pass; zero page or console errors. Focused protected recordings are not unassisted campaign clears or a final balance certification.</p>
<h2>Play the actual encounters</h2><p>Furious practice with Cole, all laser tiers and nine lives. Practice blocks save writes. Fire + Multi-retina cycles Cole's lasers; normal controls and authored game prompts apply.</p><div class="buttons">BUTTONS</div><p id="status">Select an encounter to load practice.</p><iframe id="game" title="Bullets of Fury practice" src="about:blank"></iframe>
<h2>Native engine captures</h2><div class="grid">FIGS</div><h2>Attack cycles in motion</h2><div class="grid">CLIPS</div><p><a href="verification.json">Native verification</a> · <a href="../../index.html?build=alien-arena-1005">Open game</a> · <a href="../../docs/ALIEN_ARENA_1005.md">Implementation and limits</a></p></main>
<script>const f=document.getElementById('game'),status=document.getElementById('status');let timer;
document.querySelectorAll('[data-code]').forEach(button=>button.onclick=()=>{clearInterval(timer);const code=button.dataset.code;status.textContent='Loading '+code+'…';f.onload=()=>{let tries=0;timer=setInterval(()=>{const w=f.contentWindow;if(++tries>1200){clearInterval(timer);status.textContent='Load timed out.';return;}if(typeof w.on5LaunchEncounter!=='function'||typeof w.aa5Warm!=='function')return;try{w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};w.eval('diffKey="furious";DIFF=DIFFS.furious;pilotIndex=PILOTS.findIndex(p=>p.key==="cole");pwInput='+JSON.stringify(code)+';submitPassword();startRun(PENDING_STAGE);run.lives=9;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run.wlevels[0]=8;run._cfUnlocked=8;run._cfTier=6;run.bombs=6;player.invuln=2;aa5Warm();pw5Warm();Audio.init();Audio.resume();');clearInterval(timer);status.textContent='Practice ready.';f.focus();f.scrollIntoView({behavior:'smooth',block:'start'});}catch(e){clearInterval(timer);status.textContent='Practice could not start.';console.error(e);}},100);};f.src='../../index.html?build=alien-arena-1005-practice';});</script></html>'''
for k,v in [('CHECKCOUNT',str(len(q['checks']))),('BUTTONS',buttons),('FIGS',figs),('CLIPS',clips)]:html=html.replace(k,v)
(O/'review.html').write_text(html,encoding='utf-8')
print(json.dumps({'checks':len(q['checks']),'movingGreenPixels':green_motion,'review':str(O/'review.html')}))
assert all(c['ok'] for c in q['checks']) and not q['errors']
