"""Build a live engine map review; isolate practice from campaign saves."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_landscape_1004e';O.mkdir(parents=True,exist_ok=True)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Campaign world · Bullets of Fury</title>
<style>*{box-sizing:border-box}body{margin:0;background:#071526;color:#edf5ff;font:16px/1.5 system-ui}main{max-width:1540px;margin:auto;padding:28px 22px 60px}h1{font-size:clamp(34px,4vw,54px);line-height:1.1;margin:8px 0}p{max-width:1000px;color:#b7cadd}.buttons{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}button{padding:10px 14px;color:white;background:#153950;border:1px solid #5286a5;cursor:pointer;font:inherit;border-radius:5px}button:hover{background:#276780}iframe{display:block;width:100%;height:880px;border:1px solid #45677d;background:#010810}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:24px}figure{margin:0;border:1px solid #37566d}img{display:block;width:100%;image-rendering:pixelated}figcaption{padding:12px}.tag{font-size:12px;letter-spacing:2px;color:#8ce4ff}#status{min-height:24px;color:#b7cadd}@media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:20px 10px}iframe{height:760px}}</style>
<main><div class="tag">BULLETS OF FURY · CAMPAIGN MAP</div><h1>One campaign world.</h1><p>A connected continent beneath the stage regions: jungle rivers, lava foothills, glacier ridges, desert roads, storm highlands and toxic canals. The central city, Fury HQ and cosmic bonus rift retain the original navigation markers. Blue water and drifting clouds surround the coast.</p>
<div class="buttons"><button data-stage="0">Full world</button>'''
for n in range(1,10): page+=f'<button data-stage="{n}">Stage {n}</button>'
page+='''<button data-stage="x">Stage X city</button></div><p id="status">Loading the campaign map…</p><iframe id="game" title="Live campaign map" allow="autoplay;fullscreen" src="../../index.html?build=campaign-landscape-1004e"></iframe>
<div class="grid"><figure><img src="live-overview-screen.png" alt="Connected campaign continent in the actual game"><figcaption>Complete campaign world over the original blue ocean.</figcaption></figure><figure><img src="live-focused-volcano-screen.png" alt="Volcanic region camera focus"><figcaption>Stage regions lift on selection; the landscape remains connected below.</figcaption></figure></div></main>
<script>
const frame=document.getElementById('game'),status=document.getElementById('status');let ready=false;
function setup(){const w=frame.contentWindow;if(!w||typeof w.map4eWarm!=='function')return false;
 w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};
 w.eval('ht27Stop();debugFight=null;coopOn=false;run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.rank={1:"S",2:"A",3:"B"};campaign.bonusUnlocked=false;campaign.stageX1004=null;campaign.rivalScattered=false;CF4.focus=false;CF4.flight=4;s9MapCine=null;riftReturn=null;openStageSelect(1,{boot:true});sselUnlockCine=null;Input.mouse.moved=false;window.sselCommitted=false;map4eWarm();');ready=true;status.textContent='Explore with the stage buttons or the game controls. Preview changes do not write campaign saves.';return true;}
frame.addEventListener('load',()=>{let n=0;const timer=setInterval(()=>{try{if(setup()||++n>120)clearInterval(timer);}catch(e){clearInterval(timer);status.textContent='Map preview failed to initialize.';console.error(e);}},100);});
document.querySelectorAll('button[data-stage]').forEach(button=>button.onclick=()=>{if(!ready)return;const w=frame.contentWindow,stage=button.dataset.stage;
 w.eval('sselBoot=0;sselZoom=null;sselUnlockCine=null;window.sselCommitted=false;campPause=null;s9MapCine=null;riftReturn=null;campaign.bonusUnlocked=false;campaign.stageX1004=null;CF4.focus=false;Input.clearTaps?.();Input.mouse.moved=false;');
 if(stage==='x')w.eval('campaign.stageX1004={route:"right",done:false};CF4.flight=4;CF4.focus=true;sselCursor=7;MAP4E.focus=true;');
 else if(stage==='0')w.eval('MAP4E.focus=false;MAP4E.last=sselCursor;cmap2.focus="map";');
 else{w.eval('sselCursor='+Number(stage)+';campaign.bonusUnlocked='+(stage==='9')+';MAP4E.focus=true;cmap2.focus="map";');}
 status.textContent=button.textContent+' selected. Hover lifts the stage landmark above its landscape.';
});
</script></html>'''
(O/'review.html').write_text(page,encoding='utf-8');print(O/'review.html')
