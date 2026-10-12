"""Own the lightweight part-two visual review and durable QA summary."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/part2_1010';OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'assets/part2_art_1010.js'
banks=json.loads(source.read_text().split('const P2_ART=',1)[1].strip().rstrip(';'))
proofs=[('verified','shield-lizzie','Personal gold shield'),('verified','ice-laser','Live Ice Laser'),
 ('verified','hammer-core-lock','Hammer core lock'),('verified','hammer-missile','Pilot missile'),('verified','hammer-rupture','Hammer destruction'),
 ('verified','storm-defeated','Storm generator defeat'),('verified','local-coop','Two-seat local co-op'),('verified','unlocked-modes','Earned bonus modes'),
 ('presentation','furnace-fire-laser','Furnace 32-frame fire laser'),('presentation','fire-orb-impact','Fire Orb contact'),('presentation','kinetic-orb-impact','Kinetic contact'),
 ('presentation','rebel-helix-charge','Jace registered sphere'),('presentation','rebel-turbo-release','Voss turbo'),('presentation','decker-personal-shield-wave','Decker personal shields'),
 ('presentation','kaia-teal-radar-scan','Kaia teal scanner'),('presentation','radio-nyx','Nyx purple dialogue'),('presentation','radio-kaia','Kaia teal dialogue'),
 ('presentation','radio-jace','Jace red dialogue'),('presentation','radio-rook','Rook orange dialogue'),('presentation','radio-voss','Voss neon-red dialogue'),
 ('presentation','harrier-elite-warnings','Harrier readable fire'),('finishing','hammer-full-height-spike','Hammer full-height shaft'),
 ('finishing','earth-0','Earth approach begins'),('finishing','earth-4','Earth approach midpoint'),('finishing','earth-7-8','Earth arrival'),
 ('finishing','stage-clear-full-screen','Stage Clear without equipment gap'),('finishing','campaign-zoom','Closer campaign view'),
 ('finishing','red-green-stealth-bombers','Opening stealth fighter: red and green palette variants')]
gallery=[]
for folder,name,title in proofs:
 f=ROOT/'_shots/part2_1010'/folder/(name+'.png')
 if not f.exists():continue
 im=Image.open(f);im.thumbnail((960,700));im.convert('RGB').save(OUT/(name+'.webp'),quality=85)
 gallery.append(dict(title=title,image=name+'.webp',native_source=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
for name,title in [('original-opening-fighters','Original blue opening fighters'),('actual-stealth-four-directions','Exact red/green variants in four flight lanes'),('atomic-live-ground','Corrected atomic cloud in the running game')]:
 f=ROOT/'_shots/part2_1011'/(name+'.png')
 if not f.exists():continue
 im=Image.open(f);im.thumbnail((960,700));im.convert('RGB').save(OUT/(name+'.webp'),quality=85)
 gallery.append(dict(title=title,image=name+'.webp',native_source=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
reports={}
for name,title in [('elite-live-roll','Harrier elite: drawn roll'),('elite-live-somersault','Harrier elite: drawn somersault'),('carrier-live-rolls','Carrier-launched fighters: opposite rolls'),('maverick-live-green-charge','Maverick: green helix charge'),('maverick-live-overdrive-flight','Maverick: purple/blue helix release'),('complete-fire-native','Complete fire: root, stream and crown'),('atomic-live-peak','New progressive atomic cloud'),('red-roll-native','All16 red rigid roll views'),('blue-somer-native','All16 blue somersault views')]:
 f=ROOT/'_shots/part2_motion_1011'/(name+'.png')
 if not f.exists():continue
 im=Image.open(f);im.thumbnail((960,1100));im.convert('RGB').save(OUT/(name+'.webp'),quality=90)
 gallery.append(dict(title=title,image=name+'.webp',native_source=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
for folder in ['verified','presentation','finishing','diagnostic','review']:
 f=ROOT/'_shots/part2_1010'/folder/'report.json'
 if f.exists():reports[folder]=json.loads(f.read_text())
f=ROOT/'_shots/part2_1011/report.json'
if f.exists():reports['onion_correction_1011']=json.loads(f.read_text())
f=ROOT/'_shots/part2_motion_1011/report.json'
if f.exists():reports['drawn_motion_1011']=json.loads(f.read_text())
log=ROOT/'_shots/part2_motion_1011/full-tests.log'
if not log.exists():log=ROOT/'_shots/part2_1010/onion-full-tests-final.log'
if not log.exists():log=ROOT/'_shots/part2_1010/full-tests-final.log'
s=log.read_text(encoding='utf-8',errors='replace')
qa=dict(source=dict(file='C:/Users/Mdogg/Videos/2026-10-10 21-25-04.mp4',duration=2266.70875,
 sha256='6f2ec89aa1af4f12ca374edce7cfab6c1dcbdfe3fa0a831518640563c0c71bbd',timeline_captures=151),
 verification=dict(full_suite_final_summary='FALVA/LIZZIE BUILD OK, 0 ERRORS' if 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in s else 'NOT CONFIRMED',
 passing_assertions=sum(x.startswith('  ok ') for x in s.splitlines()),native_reports=reports),
 art={k:dict(frames=len(v),size=[v[0]['w'],v[0]['h']],pivot=v[0]['pivot'],unique_hashes=len(set(a['sha256'] for a in v))) for k,v in banks.items()},
 screenshot_gallery=gallery,limits=['Protected encounter fixtures are not a human Furious campaign clear.',
 'Boss Rush handoffs used real result handlers; the probe did not naturally defeat all nine bosses.',
 'Online co-op connector is wired; a second remote client was not paired.',
 'Local co-op enemy primary aim retains the existing P1 bias.'])
(ROOT/'docs/qa/playthrough_part2_1010.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
(OUT/'review.json').write_text(json.dumps(dict(banks=banks,gallery=gallery,qa=qa),separators=(',',':')),encoding='utf-8')
HTML=r'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bullets of Fury • Part 2 Review</title>
<style>*{box-sizing:border-box}body{margin:0;background:#080d14;color:#d9e7f4;font:15px/1.5 system-ui,sans-serif}main{max-width:1240px;margin:auto;padding:28px}h1{font-size:30px;margin:0;color:#ffc951}h2{font-size:20px;color:#90dcff}p{color:#a9bfcc}a{color:#8adeff}header{border-bottom:1px solid #26415d;padding-bottom:18px}.bar{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:16px 0}button,select{color:#e4f6ff;background:#16273a;border:1px solid #3a617d;border-radius:5px;padding:9px;cursor:pointer}input{accent-color:#ffbf43}.art{display:grid;grid-template-columns:1fr 320px;gap:20px;align-items:start}.stage{min-height:430px;background:radial-gradient(#1f2e45,#080c15);border:1px solid #26415d;display:grid;place-items:center;border-radius:8px}canvas{image-rendering:pixelated;width:400px;height:400px;max-width:100%}.meta{background:#101d2b;border:1px solid #2c4562;padding:20px;border-radius:8px}code{font-size:12px}.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}figure{margin:0;background:#101a28;border:1px solid #263c58;border-radius:6px;overflow:hidden}figure img{width:100%;display:block;cursor:zoom-in}figcaption{padding:10px;font-size:13px}.ok{color:#83e7a5}.limits{border-left:3px solid #ecb653;padding:2px 16px}@media(max-width:800px){.art{grid-template-columns:1fr}.gallery{grid-template-columns:1fr 1fr}main{padding:18px}}@media(max-width:480px){.gallery{grid-template-columns:1fr}}</style>
<main><header><h1>Bullets of Fury · Part 2</h1><p>Gameplay and commentary · 37:46 · Lizzie / Furious</p><p id="qa">Loading verification…</p><a href="../../feedback/DRAWN_MOTION_1011.md">Drawn flips, flame crown and generation sources</a> · <a href="../../feedback/PLAYTHROUGH_PART2_1010.md">Timestamped changes and remaining playtests</a> · <a href="../../../index.html?revision=20261011-motion">Play the updated build</a></header>
<h2>Drawn rotations and complete effects</h2><p>Four fighter variants each have 16 rigid barrel-roll views and 16 somersault views. The cloud has 32 progressive drawings. Maverick shares Jace’s sphere motion in green and overdrive colors. Furnace shows the same complete beam as the game. Onion overlays neighboring poses at their physical anchor.</p><div class="bar"><label>Effect <select id="bank"><option value="atom">Atomic cloud · 32 smooth stages</option><option value="jace">Jace molten helix · 32 poses</option><option value="maverick">Maverick green helix · 32 poses</option><option value="maverick_full">Maverick overdrive helix · 32 poses</option><option value="fire">Furnace complete fire beam · 32 poses</option><option value="fire_tip">Furnace flame crown · 16 poses</option><option value="fire_root">Furnace flared root · 16 poses</option><option value="stealth_roll">Stealth barrel roll · 16 views</option><option value="stealth_somer">Stealth somersault · 16 views</option><option value="stealth">Stealth fighter · idle</option><option value="shield">Nine personal shield shells</option></select></label><label id="airControls" hidden>Palette <select id="airRole"><option value="red">Red</option><option value="green">Green</option><option value="blue">Blue</option><option value="orange">Orange heavy</option></select></label><button id="play">Pause</button><label>Frame <input id="frame" type="range" min="0" max="31" value="0"></label><label><input id="onion" type="checkbox"> Onion</label><span id="number"></span></div>
<div class="art"><div class="stage"><canvas id="art" width="432" height="432"></canvas></div><aside class="meta"><strong id="asset"></strong><p id="detail"></p><p>Animation shows the actual shipped RGBA cells. Position comes from the registered physical pivot.</p><p>No interpolated duplicate frames. Body silhouettes and projectiles retain their owning encounter logic.</p></aside></div>
<h2>Native Chromium captures</h2><p>These are captures from the running game. Click to inspect the full review image.</p><div id="gallery" class="gallery"></div><h2>Verification limits</h2><div id="limits" class="limits"></div></main>
<script src="../../../assets/part2_fire_renderer_1011.js"></script>
<script>
'use strict';let data,loaded={},playing=true,index=0,last=0;const cv=document.getElementById('art'),g=cv.getContext('2d'),bank=document.getElementById('bank'),slider=document.getElementById('frame'),onion=document.getElementById('onion'),airRole=document.getElementById('airRole');
function artList(){return bank.value.startsWith('stealth')?data.banks[bank.value].filter(a=>a.role===airRole.value&&(bank.value==='stealth'?a.pose==='idle':true)):data.banks[bank.value];}
function fitBank(){if(bank.value==='fire')return {k:1,cx:216,cy:378};const bounds=data.banks[bank.value].map(a=>a.opaque_bounds),p=data.banks[bank.value][0].pivot,l=Math.min(...bounds.map(b=>b[0])),t=Math.min(...bounds.map(b=>b[1])),r=Math.max(...bounds.map(b=>b[2])),b=Math.max(...bounds.map(b=>b[3])),k=Math.min(400/(r-l),400/(b-t));return {k,cx:216-((l+r)/2-p[0])*k,cy:216-((t+b)/2-p[1])*k};}
function draw(){const list=artList();index%=list.length;const a=list[index],{k,cx,cy}=fitBank();g.clearRect(0,0,432,432);g.imageSmoothingEnabled=false;
 const paint=(q,alpha)=>{if(bank.value==='fire'){p2RenderFireColumn(g,data.banks,key=>loaded[key]?.complete?loaded[key]:null,cx,cy,-Math.PI/2,300,64,data.banks.fire.indexOf(q)/32,alpha,true);return;}const im=loaded[q.key];if(im?.complete){const p=(data.banks.atom.indexOf(q)+.5)/32;g.globalAlpha=alpha*(bank.value==='atom'&&p>.875?(1-p)/.125:1);g.drawImage(im,cx-q.pivot[0]*k,cy-q.pivot[1]*k,q.w*k,q.h*k);g.globalAlpha=1;}};
 if(onion.checked){if(index>0)paint(list[index-1],.20);if(index+1<list.length)paint(list[index+1],.20);}paint(a,1);
 slider.max=list.length-1;slider.value=index;document.getElementById('airControls').hidden=!bank.value.startsWith('stealth');document.getElementById('number').textContent=(index+1)+' / '+list.length;document.getElementById('asset').textContent=a.key;document.getElementById('detail').textContent=a.w+' × '+a.h+' • pivot '+a.pivot.join(', ')+' • fixed view scale '+k.toFixed(3)+(a.source?' • source '+a.source:'');}
fetch('review.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{data=d;for(const a of Object.values(d.banks).flat()){const im=new Image();im.onload=()=>draw();im.src='../../../'+a.path+'?v='+a.sha256.slice(0,12);loaded[a.key]=im;}const reports=Object.values(d.qa.verification.native_reports).filter(q=>q.checks?.length),passes=reports.reduce((n,q)=>n+(q.passed||0),0),clean=d.qa.verification.full_suite_final_summary==='FALVA/LIZZIE BUILD OK, 0 ERRORS'&&reports.every(q=>!q.failed&&!q.errors?.length);document.getElementById('qa').textContent=d.qa.verification.passing_assertions+' regression assertions · '+passes+' recorded native checks · '+(clean?'final checks: zero errors':'check verification report');document.getElementById('qa').className=clean?'ok':'';for(const a of d.gallery){const f=document.createElement('figure'),link=document.createElement('a'),im=document.createElement('img'),c=document.createElement('figcaption');link.href=a.image+'?v='+a.sha256.slice(0,12);link.target='_blank';im.src=link.href;im.alt=a.title;im.loading='lazy';c.textContent=a.title;link.append(im);f.append(link,c);document.getElementById('gallery').append(f);}for(const l of d.qa.limits){const p=document.createElement('p');p.textContent=l;document.getElementById('limits').append(p);}draw();}).catch(e=>{document.getElementById('qa').textContent='Review failed to load: '+e.message});
bank.onchange=airRole.onchange=()=>{index=0;draw()};onion.onchange=()=>draw();slider.oninput=()=>{playing=false;document.getElementById('play').textContent='Play';index=+slider.value;draw()};document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'Pause':'Play'};function loop(t){if(data&&playing&&t-last>(bank.value==='shield'?800:bank.value==='atom'&&index===31?700:1000/24)){index=(index+1)%artList().length;draw();last=t;}requestAnimationFrame(loop)}requestAnimationFrame(loop);
</script></html>'''
(OUT/'index.html').write_text(HTML,encoding='utf-8',newline='\n')
print(json.dumps(dict(assertions=qa['verification']['passing_assertions'],gallery=len(gallery),reports={k:(v.get('passed'),v.get('failed'),len(v.get('errors',[]))) for k,v in reports.items()})))
