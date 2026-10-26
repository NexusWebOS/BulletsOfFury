from pathlib import Path
import json,base64,html
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/opening_storyboard_1024';port,stop=serve(str(R));errors=[];checks=[]
with sync_playwright() as pw:
 br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000)
 p.evaluate("()=>{run.pilot='yuri';campaignIntroStart(()=>{window.done24=(window.done24||0)+1});campaignIntroWarm();}")
 p.wait_for_function('campaignIntroReady()&&Object.values(OT24_ART).every(a=>XART.rdy(a.key))',timeout=180000)
 rows=p.evaluate("IP21.beats.map(b=>({...b,text:ip21Line(b,{pilot:'yuri'})}))")
 titles=['Fury HQ — 2026','After the Cold War','Why Fury exists','The remaining nine','One day, it happened','Machines turn on man','Alarms at dispatch','Tell the others','Running from dispatch','Portal at orbital watch','Satellite takeover','Corrupted signal to Earth','Infrastructure hijacked','Homes under attack','City under attack','Worldwide chaos','Power fails at Fury HQ','Selected pilot near the jungle','No answer','Return to base','Something in the jungle']
 cards=[]
 for i,b in enumerate(rows):
  t=2 if b.get('dispatch')=='run' else min(b['duration']-.1,6)
  data=p.evaluate('([i,t])=>{campaignIntro.t=IP21.beats[i].at+t;drawCampaignIntro(0);return cv.toDataURL("image/png").split(",")[1];}',[i,t]);name=f'authored-{i+1:02}.png';(O/name).write_bytes(base64.b64decode(data));cards.append({'title':titles[i],'image':name,'who':b.get('who'),'text':b.get('text','')})
 data=p.evaluate('()=>{campaignIntro.t=IP21.finaleAt+1;drawCampaignIntro(0);return cv.toDataURL("image/png").split(",")[1];}');(O/'authored-logo.png').write_bytes(base64.b64decode(data));cards.append({'title':'Logo, boost and fade','image':'authored-logo.png','who':'Action','text':'The Bullets of Fury logo flashes in with rumble. The selected pilot’s active thrusters flare; the actual aircraft accelerates off screen without firing. Picture and music fade into the campaign map.'})
 checks.append({'name':'HQ is the first native shot', 'passed':p.evaluate('IP21.beats[0].hq===true')})
 checks.append({'name':'Authored order and no added briefing','passed':p.evaluate("IP21.beats[6].who==='DECKER'&&IP21.beats[7].who==='LIZZIE'&&IP21.beats[10].replay==='takeover'&&IP21.beats[11].replay==='downlink'&&IP21.beats[16].blackout&&IP21.beats[17].flight&&!IP21.beats.some(b=>b.brief)")})
 checks.append({'name':'Storyroom preserves new baseline and finale','passed':p.evaluate('SB24.intro[0].hq&&Math.abs(SB24.finaleDuration-6)<1e-9')})
 for pilot in ['axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva','cole']:
  r=p.evaluate("pilot=>{campaignIntro.pilot=pilot;campaignIntro.t=IP21.beats[17].at+2;drawCampaignIntro(0);return{pilot:OB24.last.pilot,ship:PT11_UI.ship?.key};}",pilot)
  checks.append({'name':'Selected aircraft '+pilot,'passed':r['pilot']==pilot,'data':r})
 p.evaluate("()=>{campaignIntroFinish();campaignIntroFinish();}");checks.append({'name':'Completion exactly once','passed':p.evaluate('window.done24===1')})
 p.evaluate('()=>{openStageSelect(1,{boot:true});}');p.wait_for_timeout(14000);(O/'authored-map.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL("image/png").split(",")[1]')))
 nextlines=p.evaluate("BOF_STORYBOARD.native('post1','yuri')")
 p.set_viewport_size({'width':640,'height':900});p.evaluate("()=>{run.pilot='cole';campaignIntroStart(()=>{});_setCinematicViewport(true);}");p.wait_for_function('campaignIntroReady()&&Object.values(OT24_ART).every(a=>XART.rdy(a.key))',timeout=180000)
 for i in [0,7,17,20]:
  data=p.evaluate('i=>{campaignIntro.t=IP21.beats[i].to-.1;drawCampaignIntro(0);return cv.toDataURL("image/png").split(",")[1];}',i);(O/f'narrow-{i}.png').write_bytes(base64.b64decode(data))
 p.mouse.click(3,3)
 audio=p.evaluate("""async()=>{Snd.resume();Snd.prepare(['retinaLockBeep']);const pool=Snd.pools.retinaLockBeep;const slot=pool.slots.find(v=>v&&v.el);const url=slot.el.src;const ac=new AudioContext();const buffer=await ac.decodeAudioData(await(await fetch(url)).arrayBuffer());let peak=0;for(const v of buffer.getChannelData(0))peak=Math.max(peak,Math.abs(v));Snd.play('retinaLockBeep');await new Promise(r=>setTimeout(r,120));const played=pool.slots.some(v=>v?.el?.currentTime>0&&!v.el.error);await ac.close();return{duration:buffer.duration,peak,played};}""")
 checks.append({'name':'Warning beep decodes and plays through shared mixer','passed':audio['peak']>0 and audio['played'],'data':audio})
 checks.append({'name':'No page or console errors' ,'passed':not errors,'data':errors});br.close()
stop()
body=''
for j,c in enumerate(cards):
 text=html.escape(c['text']) or {'Running from dispatch':'Decker and Lizzie run to warn the others.','Portal at orbital watch':'A portal opens. The faceless symbiote emerges and flows onto the satellite.','Satellite takeover':'Alien machinery spreads across the satellite until the relay is fully corrupted.','Corrupted signal to Earth':'The corrupted satellite transmits pulsing alien data down to Earth.', 'Power fails at Fury HQ':'Cut back to Fury HQ. Its power fades out.'}.get(c['title'],'')
 body+=f'<article><h2>{j+1:02} — {html.escape(c["title"])}</h2><img src="{c["image"]}"><p><b>{html.escape(c.get("who") or "Action")}:</b> {text}</p></article>'
nextbody='<article><h2>Next — campaign map</h2><img src="authored-map.png"><p>The native campaign map opens with Stage 1 available. The player chooses to enter the jungle stage. There is no new squad briefing inserted before the map.</p></article><article><h2>After Stage 1 — current continuation</h2><p>This is the existing post-Stage-1 dialogue for review; it has not been rewritten in this pass.</p>'+''.join('<p><b>'+html.escape(str(b.get('who','')))+':</b> '+html.escape(str(b.get('text','')))+'</p>'for b in nextlines)+'</article>'
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Fury opening — Mike’s sequence</title><style>body{margin:0;background:#10161d;color:#e8edf3;font:18px/1.55 system-ui}header,main{max-width:1100px;margin:auto;padding:24px}h1{margin:0;font-size:30px}header p{color:#b8c7d5}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:#1b2530;padding:20px;border-radius:12px;border:1px solid #354454}h2{margin:0 0 14px;font-size:21px;color:#98e3d6}img{width:100%;display:block;background:#000}p{margin:12px 0}b{color:#ffda8b}@media(max-width:850px){main{grid-template-columns:1fr}}@media print{article{break-inside:avoid}main{display:block}}</style><header><h1>Fury opening — from Fury HQ to the campaign map</h1><p>Mike’s revised order. Actual game frames and native dialogue. Yuri illustrates the selected-pilot shots; every pilot uses their own aircraft. Establishing narration is split across four readable shots. Beeps accompany the dispatch warning and flight-system failure.</p></header><main>'''+body+nextbody+'</main>',encoding='utf8')
(O/'dialogue.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf8');(R/'_shots/intro_order_1024/authored-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print(json.dumps(checks,indent=2));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
