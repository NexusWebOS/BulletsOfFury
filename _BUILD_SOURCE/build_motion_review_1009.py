"""Build a local review from actual engine captures, not a substitute renderer."""
from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/boss_motion_1009'
UNITS=[('s1tankheavy','Heavy tank'),('s1tanklight','Light tank'),('s1tankapc','APC'),
       ('s1truckmissile','Missile buggy'),('s1boatpatrol','Patrol boat'),
       ('s1boatgun','Missile boat'),('s1corvette','Corvette'),
       ('s1landingcraft','Landing craft'),('s1jetdelta','Delta fighter'),('s1jetbomber','Bomber')]
VIDEOS=[('hammer-death','Hammer: intact acting, rupture, cutaway'),
        ('hammer-counter','Hammer: bottom storm and upper counter'),
        ('dracodia-claws','Dracodia: hover, shriek, physical swipes'),
        ('dracodia-enraged','Dracodia: below-half-HP combination'),
        ('warden-claws','Warden: raised claws and cross-slash'),
        ('warden-leap','Warden: crouch, leap and gravel landing'),
        ('warden-battery','Warden: converged alternating barrage'),
        ('turrets-cryospear','Stage 3 boss: physical turret charge'),
        ('turrets-frostcruiser','Stage 3 miniboss: physical turret charge'),
        ('turrets-stormsovereign','Stage 4 boss: physical turret charge')]
def result(name):
    q=json.loads((OUT/name).read_text());return f'{q["passed"]} pass / {len(q["failed"])} fail / {len(q["errors"])} errors'
def video(name,title):
    return f'<article><h3>{title}</h3><video controls muted playsinline preload="none" poster="{name}/0000.png" src="{name}.mp4"></video><a href="{name}.mp4">Open capture</a></article>'
cards=[]
for key,title in UNITS:
    path='../../_ART_SOURCES/stage1_motion_1009/returned_live/'+key
    canvases=f'<div><span>Idle / flight · 8 cells</span><canvas width="256" height="256" data-reel="{path}__idle_intact__01-08.png" data-count="8" data-fps="10"></canvas></div>'
    if key!='s1landingcraft':canvases+=f'<div><span>Fire · 4 cells</span><canvas width="256" height="256" data-reel="{path}__fire_intact__01-04.png" data-count="4" data-fps="15"></canvas></div>'
    else:canvases+='<p class="quiet">Unarmed mine deployment remains its existing role.</p>'
    cards.append(f'<article><h3>{title}</h3><div class="reels">{canvases}</div><details><summary>Native normal / white hit flash</summary><div class="reels"><img src="{key}-normal.png"><img src="{key}-hit.png"></div></details></article>')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bullets of Fury · October 9 motion review</title><style>
*{box-sizing:border-box}body{margin:0;background:#09101b;color:#dfeafa;font:16px/1.5 system-ui,sans-serif}main{max-width:1260px;margin:auto;padding:28px}h1{font-size:34px;margin:0 0 8px}h2{margin:48px 0 12px}h3{font-size:17px;margin:0 0 14px}a{color:#80c6ff}nav{display:flex;gap:22px;margin:20px 0}.quiet{color:#9db0ca}.status{padding:16px;background:#142233;border:1px solid #27425b;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}article{padding:18px;background:#111c2b;border:1px solid #2a3d54;border-radius:8px}.reels{display:flex;gap:12px;flex-wrap:wrap}.reels>div{flex:1;min-width:130px}.reels span{font-size:13px;color:#9eb9d0}canvas,.reels img{display:block;width:100%;max-width:256px;background:#061321;image-rendering:pixelated}.reels img{width:45%;margin-top:12px}video{width:100%;max-height:620px;background:#03060b}details{margin-top:16px}button{border:1px solid #427399;color:#e6f4ff;background:#193552;padding:9px 16px;cursor:pointer;border-radius:5px}figure{margin:18px 0}figure img{max-width:100%;image-rendering:pixelated}figcaption{font-size:13px;color:#aac1d7}
</style><main><h1>October 9 motion review</h1><p>Current Stage 1 vehicles and the continued boss direction from Mike’s recording.</p>
<nav><a href="#roster">Current roster</a><a href="#live">Live Stage 1</a><a href="#bosses">Filmed boss motion</a><a href="#checks">Verification</a></nav>
<p class="status">STATUS</p><p class="quiet">These are actual engine pixels. Clips are silent visual captures, simulated at 60 Hz and saved at 15 FPS. Focused encounter clips establish motion, warnings and recovery; they do not claim a complete campaign-clear balance test.</p>
<h2 id="roster">Current Stage 1 roster</h2><p>The ten live designs, with independently aimed tank turrets, destructible boat weapons and existing jet banks/rolls. Static props stay static.</p><button id="toggle">Pause reel previews</button><p><a href="stage1_returned_1009.zip">Download the 8-idle / 4-fire review reels</a> · <a href="../../docs/STAGE1_MOTION_1009.md">Implementation notes</a></p><div class="grid">CARDS</div>
<h2 id="live">Stage 1 ocean-to-land play</h2><p>Actual frame-loop recording of the existing naval, jet and tank controllers releasing their projectiles.</p>LIVE
<h2 id="bosses">Continued video direction</h2><p>Hammer keeps two arms and his seated head through intact death poses. Dracodia uses attached-head acting and committed physical claws; Warden uses generated limbs, landing and its own guns. Stage 3/4 charges stay at their physical turrets.</p><div class="grid">VIDEOS</div>
<h2 id="checks">Verification</h2><p><a href="verification.json">Boss native checks</a> · <a href="edge-verification.json">Every-difficulty counter edges</a> · <a href="stage1-verification.json">Stage 1 native checks</a> · <a href="suite.txt">Complete base suite</a> · <a href="stage3-regression.txt">Existing Stage 3 regression</a></p><p><a href="../../docs/feedback/BOSS_DIRECTION_1009.md">Timestamped boss direction and implementation checkpoint</a></p><figure><img src="native-art-contact.png"><figcaption>64 accepted boss cells through the game’s own drawImage context.</figcaption></figure><figure><img src="stage1-motion-contact.png"><figcaption>48 new Stage 1 moving-part cells; existing hulls and ordnance remain authored.</figcaption></figure>
</main><script>
let playing=true;const items=[...document.querySelectorAll('canvas[data-reel]')].map(c=>{const im=new Image();im.src=c.dataset.reel;return{c,im,n:+c.dataset.count,fps:+c.dataset.fps};});let clock=0,last=performance.now();function frame(t){if(playing)clock+=(t-last)/1000;last=t;for(const {c,im,n,fps} of items){if(!im.complete||!im.naturalWidth)continue;const g=c.getContext('2d'),w=im.naturalWidth/n,f=Math.floor(clock*fps)%n;g.clearRect(0,0,c.width,c.height);g.imageSmoothingEnabled=false;g.drawImage(im,f*w,0,w,im.naturalHeight,0,0,c.width,c.height);}requestAnimationFrame(frame);}requestAnimationFrame(frame);document.querySelector('#toggle').onclick=function(){playing=!playing;this.textContent=playing?'Pause reel previews':'Play reel previews';};
</script></html>'''
status='Stage 1: '+result('stage1-verification.json')+' · Boss motion: '+result('verification.json')+' · Counter edges: '+result('edge-verification.json')
html=html.replace('STATUS',status).replace('CARDS',''.join(cards)).replace('LIVE',video('stage1-gameplay','Stage 1 · 40-second live waves')).replace('VIDEOS',''.join(video(*v) for v in VIDEOS))
(OUT/'review.html').write_text(html,encoding='utf-8',newline='\n')
with zipfile.ZipFile(OUT/'stage1_returned_1009.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in (ROOT/'_ART_SOURCES/stage1_motion_1009/returned_live').iterdir():
        if f.is_file():z.write(f,'returned/'+f.name)
    z.write(ROOT/'docs/STAGE1_MOTION_1009.md','README.md')
print(status)
