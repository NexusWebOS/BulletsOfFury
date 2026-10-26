from pathlib import Path
import json,base64,html
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/opening_storyboard_1024';O.mkdir(parents=True,exist_ok=True)
shots=[
('A world at peace',-1,2,[('Narration','For years, Fury Division kept watch over Earth. Most days, there was nothing to report.'),('Action','Open on the city and harbor. Civilian aircraft cross the sky. Let the ordinary life register before the alarm.')]),
('Fury satellite — orbital watch',-2,2,[('Action','Cut to Fury satellite above Earth. Its lights and relay systems are operating normally. Nothing is corrupted yet.'),('Narration','Above them, Fury satellite kept the defense network connected. Every aircraft. Every ship. Every command.')]),
('01 — The warning',0,1.2,[('Lizzie','Decker, look at this. The satellite’s reporting something inside the perimeter.'),('Decker','One of ours?'),('Lizzie','No identification. Hang on… it’s sending commands through our relay.')]),
('02 — No control',1,1.8,[('Decker','Disconnect us.'),('Lizzie','I did. The commands are still going out.'),('Decker','We gotta get to the others. Now!')]),
('03 — Run to the squad',2,1.4,[('Action','They leave their stations and run. The warning continues behind them.')]),
('04 — Gather around',3,2,[('Cole','What happened?'),('Lizzie','We got a warning from Fury satellite. Then this came through. It’s the last recording we received.')]),
('05 — The portal opens',4,.9,[('Action','Lizzie brings up the security feed. A portal opens beside the satellite.'),('Axel','What the hell is that?'),('Decker','Keep watching.')]),
('06 — Dracodia emerges',4,4.8,[('Action','Dracodia comes through the portal and moves toward Fury satellite. Hold this shot long enough to see him approach.')]),
('07 — The takeover',5,4.5,[('Falva','Is it… growing into it?'),('Lizzie','That’s what it looks like. We lost control of the relay a few seconds later.'),('Cole','Can we shut it down from here?'),('Decker','We tried. It won’t accept our commands.')]),
('08 — He is listening',7,3,[('Dracodia','Your machines already know my voice.'),('Action','The transmission cuts out. Nobody speaks for a moment.'),('Maverick','Please tell me that was a recording.'),('Lizzie','That last part wasn’t.')]),
('09 — Live reports',8,3,[('Action','Screens switch between fighters over the city, moving armor and ships firing.'),('Axel','Those are our fighters.'),('Lizzie','Their crews aren’t responding. Neither are the ground units.'),('Cole','Get a warning out. Tell everyone to disconnect from the network.'),('Decker','I’m trying. We’re losing channels faster than I can reach them.')]),
('10 — The plan',12,3,[('Falva','What about our jets?'),('Decker','Manual controls still work. Leave the network link off.'),('Cole','Where do we start?'),('Lizzie','There’s a signal over the jungle. It appeared just before the satellite warning. It’s the only lead we have.')]),
('11 — Launch orders',13,3,[('Cole','Then we check it out. Stay together, and don’t trust your instruments.'),('Lizzie','And if the radios go?'),('Cole','Keep flying. Find somewhere safe to regroup.')]),
('12 — Alone over the jungle',17,3,[('Yuri','HQ, Yuri. I’m over the river. Do you still have me?'),('Action','Static.'),('Yuri','Lizzie?'),('Ship system','Communications link lost.'),('Yuri','…All right. Follow the river. Find the signal.'),('Yuri','You’re going to pay for this.'),('Action','Logo transition. His thrusters flare, and he accelerates out of view.')])]
port,stop=serve(str(R));errors=[]
with sync_playwright() as pw:
 br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000)
 p.evaluate("()=>{run.pilot='yuri';campaignIntroStart(()=>{});campaignIntroWarm();ob24Keys.forEach(k=>XART.rdy(k));}");p.wait_for_function('campaignIntroReady()&&ob24Keys.every(k=>XART.rdy(k))',timeout=180000)
 for j,(title,i,t,lines) in enumerate(shots):
  p.evaluate('([i,t])=>{campaignIntro.t=(i<0?0:IP21.beats[i].at)+t;const b=i<0?{}:IP21.beats[i];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);if(i===-1)c22Plate("peace_city",cutsceneViewWidth(),VH,t);else if(i===-2){cinCover("cinend_deep_space",cutsceneViewWidth(),VH,.5);ip21Blit("clean",0,cutsceneViewWidth()/2,VH*.45,VH*.76,VH*.76);}else ip21Visual(b,campaignIntro,t,cutsceneViewWidth(),VH);ctx.restore();}',[i,t])
  (O/f'{j+1:02}.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL('image/png').split(',')[1]")))
 br.close()
stop()
body=''
for j,(title,i,t,lines) in enumerate(shots):
 title=f'{j+1:02} — '+title.split(' — ',1)[-1]
 body+=f'<article id="shot-{j+1}"><h2>{html.escape(title)}</h2><img src="{j+1:02}.png" alt="{html.escape(title)}">'+''.join(f'<p><b>{html.escape(who)}:</b> {html.escape(text)}</p>' for who,text in lines)+'</article>'
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Fury opening — dialogue storyboard</title><style>body{margin:0;background:#10161d;color:#e8edf3;font:18px/1.55 system-ui}header,main{max-width:1100px;margin:auto;padding:24px}h1{margin:0;font-size:30px}header p{color:#b8c7d5}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:#1b2530;padding:20px;border-radius:12px;border:1px solid #354454}h2{margin:0 0 14px;font-size:21px;color:#98e3d6}img{width:100%;display:block;background:#000}p{margin:12px 0}b{color:#ffda8b}@media(max-width:850px){main{grid-template-columns:1fr}}@media print{body{background:white;color:black}article{break-inside:avoid;background:white}header{break-after:page}main{display:block}article{margin:20px 0}}</style><header><h1>Fury opening — suggested dialogue</h1><p>14 story images from the opening establishing shot through the jungle launch. Existing in-game art illustrates the proposed shots; dialogue below each image is the suggestion. Still images represent animation beats. The Dracodia interruption and reaction shot are proposed staging, not a claim of completed lip-sync or transmission animation. No saved game dialogue changed.</p></header><main>'''+body+'</main>',encoding='utf8')
(O/'dialogue.json').write_text(json.dumps([{'title':a,'lines':d}for a,b,c,d in shots],ensure_ascii=False,indent=2),encoding='utf8')
print('Created 14 storyboard images and review page. Page errors:',errors)
