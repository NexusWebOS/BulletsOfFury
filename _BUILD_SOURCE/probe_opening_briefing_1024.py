from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/intro_order_1024';port,stop=serve(str(R));errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000)
 p.evaluate("()=>{run.pilot='yuri';campaignIntroStart(()=>{window.done24=(window.done24||0)+1});campaignIntroWarm();ob24Keys.forEach(k=>XART.rdy(k));}")
 p.wait_for_function('campaignIntroReady() && ob24Keys.every(k=>XART.rdy(k))',timeout=180000)
 for i,t in [(0,1),(2,1.6),(4,1),(4,4),(5,3),(5,5.5),(6,2),(7,2),(12,2)]:
  result=p.evaluate('([i,t])=>{campaignIntro.t=IP21.beats[i].at+t;drawCampaignIntro(0);return {last:OB24.last,caption:IP21.caption};}',[i,t]);(O/f'shot-{i}-{t}.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL('image/png').split(',')[1]")))
  print(i,t,json.dumps(result)[:220],flush=True)
 checks=[]
 def ck(n,v):
  checks.append({'name':n,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+n,flush=True)
 ck('Warning then run then briefing then replay',p.evaluate("IP21.beats.slice(0,6).map(b=>b.dispatch||b.brief||b.replay).join(',')==='dispatch,turn,run,wide,arrival,takeover'"))
 ck('Storyroom snapshots repaired baseline',p.evaluate("SB24.intro.length===IP21.beats.length && SB24.intro[4].replay==='arrival'"))
 ck('Continuous timing and native finale',p.evaluate("IP21.beats.every((b,i)=>!i||b.at===IP21.beats[i-1].to)&&Math.abs(IP21.end-IP21.finaleAt-14)<1e-9"))
 ck('Selected pilots investigate instead of unexplained return',p.evaluate("Object.values(CAMPAIGN_SOLO_LINES).every(v=>!/coming home|river home|returning/i.test(v.report+' '+v.resolve))"))
 ck('Takeover pixels animate',(O/'shot-5-3.png').read_bytes()!=(O/'shot-5-5.5.png').read_bytes())
 ck('Portal emergence pixels animate',(O/'shot-4-1.png').read_bytes()!=(O/'shot-4-4.png').read_bytes())
 p.set_viewport_size({'width':640,'height':900})
 p.evaluate("()=>{_setCinematicViewport(true);campaignIntro.t=IP21.beats[7].at+5;drawCampaignIntro(0);}")
 (O/'narrow.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL('image/png').split(',')[1]")))
 p.evaluate("()=>{campaignIntroFinish();campaignIntroFinish();}")
 ck('Native completion callback once',p.evaluate('window.done24===1'))
 ck('No page errors',not errors)
 (O/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
 print('errors',errors,flush=True);print('baseline',p.evaluate('IP21.beats.map(b=>({who:b.who,text:b.text,at:b.at,to:b.to}))'),flush=True)
 (O/'report.json').write_text(json.dumps({'errors':errors,'beats':p.evaluate('IP21.beats')}),encoding='utf8');b.close()
stop()
