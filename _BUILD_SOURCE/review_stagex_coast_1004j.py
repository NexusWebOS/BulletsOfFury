"""Playable Stage VI/X route and blue-airframe review using the actual engine."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/stagex_coast_1004j';O.mkdir(exist_ok=True)
page='''<!doctype html><meta charset="utf-8"><title>Stage X arenas and blue fighter</title>
<style>body{margin:0;background:#070e1b;color:#d6e8fa;font:16px system-ui}main{max-width:1450px;margin:auto;padding:24px}h1{font-size:26px}button{padding:12px;background:#142b48;color:#edf5ff;border:1px solid #5979a0;margin:4px;cursor:pointer}a{color:#8bd8ff}iframe{width:100%;height:840px;border:1px solid #385071}img{width:100%;height:auto}.pair{display:grid;grid-template-columns:1fr 1fr;gap:15px}small{color:#9eb3cb}</style>
<main><h1>Stage X coastal city and animated water</h1>
<p>Generated military ports and coastal city around the mountain. Water and painted waterfalls are removed from the terrain layer; the existing four-frame blue water reel animates beneath the native alpha. Summit snow stays intact. XHARR / XREBEL share the new arena; HARR6 / REBEL6 retain Stage VI.</p>
<p><a href="../../index.html?build=stagex-coast-1004j" target="_blank">Open the updated game with real saves</a> · <a href="checks.json">Chromium evidence</a></p>
<div><button data-code="XHARR">X Harrier</button><button data-code="XREBEL">X Rebels</button><button data-code="HARR6">VI Harrier</button><button data-code="REBEL6">VI Rebels</button><button data-code="ACE">Blue giant fighter</button><button data-code="BOMBERS">Bomber passes</button></div>
<iframe id="game" src="../../index.html?build=stagex-coast-1004j-review"></iframe>
<p><small>Furious practice. Demo saves use a separate namespace. The linked game uses your actual campaign saves.</small></p>
<div class="pair"><img src="arena-XHARR.png" alt="Harrier carrier over Stage X mountain and water"><img src="arena-XREBEL.png" alt="Five rebels over the Stage X arena"></div>
<p>Animated water beneath a fixed terrain crop:</p><img src="water-animation.gif" alt="Native animated water beneath the fixed mountain and coast"><p>The terrain-only layer (checkerboard indicates transparency):</p><img style="max-width:680px;background:repeating-conic-gradient(#242833 0% 25%,#111724 0% 50%) 0 / 24px 24px" src="../../assets/game/levels/stage_x/stage/stagex_coast_1004j/terrain.png" alt="Coastal city terrain with no painted water or waterfalls">
</main><script>
const frame=document.querySelector('#game');let initialized=false;
function ready(){try{return frame.contentWindow.__bofFrames>4}catch(e){return false}}
function launch(code){if(!ready()){setTimeout(()=>launch(code),100);return}const w=frame.contentWindow;
 if(!initialized){w.eval('map4hPreviewStorage();ht27Stop();debugFight=null;coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");diffKey="furious";DIFF=DIFFS.furious;');initialized=true;}
 if(code==='ACE'){launch('HARR6');w.eval('whvAceSpawn(boss);boss._whv.mode="ace";boss._whv.ace.st="fight";boss._whv.ace.y=140;boss._whv.ace.x=worldWidth()/2;boss._whv.ace.t=0;boss.enter=false;');}
 else if(code==='BOMBERS')w.eval('GP4.route=null;GP4.routeReady=false;startRun(6);BOFCinematicDirector.cancel();storySkip();setState(GS.PLAY);s6Opening=null;run._mission29OpeningDone=true;stagePlan=[];enemies=[];boss=null;bossActive=false;s6Wing=null;fb2Talk=null;fb2Flights=[];fb2FlightPlan("east","red");fb2FlightPlan("west","green");fb2FlightPlan("south","orange");');
 else w.eval('setState(GS.PASSWORD);pwInput='+JSON.stringify(code)+';submitPassword();startRun(PENDING_STAGE);');
 frame.focus();}
document.querySelectorAll('[data-code]').forEach(b=>b.onclick=()=>launch(b.dataset.code));frame.addEventListener('load',()=>launch('XHARR'));
</script>'''
(O/'review.html').write_text(page,encoding='utf-8');print(O/'review.html')
