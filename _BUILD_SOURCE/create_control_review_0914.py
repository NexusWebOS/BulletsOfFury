from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'index.html').read_text(encoding='utf-8')
s=s.replace('<head>','<head><base href="/"><script>window.requestAnimationFrame=()=>0;</script>',1)
panel='''<div style="position:fixed;left:0;top:0;z-index:99999;background:#142034;color:white;font:11px monospace;padding:6px;width:220px">
<b>Authored controls / real renderer</b><br><select id="qaScreen"></select>
<button id="qaDraw">Render</button><button id="qaB">B</button><button id="qaDelete">Backspace</button><pre id="qaState"></pre></div>
<script>
const sel=document.getElementById('qaScreen');
for(const name of ['PILOT','TITLE','MODESEL','DIFF','OPTIONS','HELP','PASSWORD','CREDITS','CAMPHUB','BOOT']){const o=document.createElement('option');o.value=name;o.textContent=name;sel.append(o);}
function qaReport(){document.getElementById('qaState').textContent=JSON.stringify({state,back:'B action',backspace:'delete text only'},null,1);}
function qaDraw(){loop(last+1000/60);qaReport();}
function qaReset(){Input.clearTaps();run.mode='arcade';campPick=null;campHubIndex=0;pilotIndex=0;pilotFrom=0;pilotRot=0;pilotPending=null;pilotComm=null;setState(GS[sel.value]);stateT=2;drawPilot._entered=false;drawPilot._pcFor=null;pilotInputArmed=true;rebindAction=null;optSnap=null;helpPage=0;drawPassword.typing=false;qaDraw();if(pcard)pcSkip();qaDraw();}
sel.onchange=qaReset;document.getElementById('qaDraw').onclick=qaDraw;
document.getElementById('qaB').onclick=()=>{Input.injectTap('pad_b1');qaDraw();};
document.getElementById('qaDelete').onclick=()=>{Input.injectTap('backspace');qaDraw();};
window.addEventListener('load',qaReset);
</script>'''
s=s.replace('</body>',panel+'</body>')
q=R/'_shots/control_hints_0914';q.mkdir(parents=True,exist_ok=True)
(q/'review.html').write_bytes(s.encode())
print('Created native menu-control review fixture')
