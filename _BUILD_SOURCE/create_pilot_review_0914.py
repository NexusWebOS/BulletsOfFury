from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'index.html').read_text(encoding='utf-8')
s=s.replace('<head>','<head><base href="/"><script>window.requestAnimationFrame=()=>0;</script>',1)
panel='''
<div id="qa" style="position:fixed;left:0;top:0;z-index:99999;background:#142034;color:white;font:14px monospace;padding:8px;max-width:85vw">
<b>UI-09 / real engine / controlled time</b><br>
<select id="qaPilot"></select>
<button id="qaReset">Restart</button><button id="qaStep">+0.25 sec</button>
<button id="qaSecond">+1 sec</button><button id="qaSkip">Enter</button>
<button id="qaFinish">Finish reveal</button><pre id="qaState"></pre></div>
<script>
const select=document.getElementById('qaPilot');
for(const P of PILOTS){const o=document.createElement('option');o.value=P.key;o.textContent=P.name;select.append(o);}
function qaReport(){document.getElementById('qaState').textContent=JSON.stringify({state,pilot:PILOTS[pilotIndex].key,phase:pcard&&pcard.phase,typed:pcard&&Math.floor(pcard.typed),bar:pcard&&pcard.bar,segments:pcard&&pcard.seg,done:pcard&&pcard.done},null,1);}
function qaStep(seconds){for(let i=0;i<Math.max(1,Math.round(seconds*60));i++)loop(last+(seconds?1000/60:0));qaReport();}
function qaReset(){run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key===select.value);pilotFrom=pilotIndex;setState(GS.PILOT);drawPilot._entered=false;drawPilot._pcFor=null;pilotInputArmed=true;qaStep(.05);}
document.getElementById('qaReset').onclick=qaReset;select.onchange=qaReset;
document.getElementById('qaStep').onclick=()=>qaStep(.25);
document.getElementById('qaSecond').onclick=()=>qaStep(1);
document.getElementById('qaSkip').onclick=()=>{Input.injectTap('enter');qaStep(1/60);};
document.getElementById('qaFinish').onclick=()=>{pcSkip();qaStep(1/60);};
window.addEventListener('load',qaReset);
</script>'''
s=s.replace('</body>',panel+'</body>')
target=R/'_shots/pilot_reveal_0914/review.html'
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(s,encoding='utf-8')
print('Created ignored native-renderer review fixture')
