"""Native Cole comm/menu/shouting pixels and live dialogue animation."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/cole_portraits_1005';O.mkdir(parents=True,exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8');report={'checks':[],'errors':[]}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def save(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:800]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};setState(GS.CUTSCENE);for(const em of CP5.poses){XART.rdy("port_cf_cole_"+em);XART.rdy("comm_cole_"+em);}for(let i=0;i<3;i++)XART.rdy("fb2_cole_rage_"+i);XART.rdy("dlg_rect_0914");bmfReady("dialogue");}')
  p.wait_for_function('()=>CP5.poses.every(em=>XART.rdy("port_cf_cole_"+em)&&XART.rdy("comm_cole_"+em))&&[0,1,2].every(i=>XART.rdy("fb2_cole_rage_"+i))&&XART.rdy("dlg_rect_0914")&&bmfReady("dialogue")',timeout=120000,polling=50)
  report['pixels']=p.evaluate('''()=>{
   const pix=im=>im.getContext('2d').getImageData(0,0,256,256).data;
   function compare(a,b,box){let outside=0,inside=0;for(let y=0;y<256;y++)for(let x=0;x<256;x++){let diff=false;for(let c=0;c<4;c++)if(a[(y*256+x)*4+c]!==b[(y*256+x)*4+c])diff=true;if(diff){if(x>=box[0]&&x<box[2]&&y>=box[1]&&y<box[3])inside++;else outside++;}}return {outside,inside};}
   const out={};for(const comm of [false,true]){
    const prefix=comm?'comm_cole_':'port_cf_cole_',idle=pix(XART.get(prefix+'idle')),mouth=comm?[119,140,164,174]:[92,140,137,174];
    out[prefix]=['talk-closed','talk-small','talk-medium','talk-wide','talk-o'].map(em=>({em,...compare(idle,pix(XART.get(prefix+em)),mouth)}));
   }
   out.rails=CP5.poses.map(em=>({em,...compare(pix(XART.get('port_cf_cole_idle')),pix(XART.get('port_cf_cole_'+em)),[23,24,234,234])}));
   out.rage=[0,1].map(i=>compare(pix(XART.get('fb2_cole_rage_2')),pix(XART.get('fb2_cole_rage_'+i)),[110,130,154,172]));
   out.mirror=CP5.poses.every(em=>{const a=pix(XART.get('port_cf_cole_'+em)),d=pix(XART.get('comm_cole_'+em));for(let y=0;y<256;y++)for(let x=0;x<256;x++)for(let c=0;c<4;c++)if(a[(y*256+x)*4+c]!==d[(y*256+255-x)*4+c])return false;return true;});return out;
  }''')
  for key in ['comm_cole_','port_cf_cole_']:
   for q in report['pixels'][key]:
    ck(q['outside']==0,key+q['em']+' retains fixed head/body/frame pixels')
    ck(q['inside']>25 if q['em']!='talk-closed' else q['inside']==0,key+q['em']+' mouth pixels correct')
  for q in report['pixels']['rails']:ck(q['outside']==0,'Complete four-sided frame: '+q['em'])
  for i,q in enumerate(report['pixels']['rage']):ck(q['outside']==0 and q['inside']>25,'Shouting frame '+str(i)+' retains head/frame and animates mouth')
  ck(report['pixels']['mirror'],'All comm portraits retain right-facing treatment')
  # Pixels go through the game's own context, not browser image elements.
  p.evaluate('''()=>{cv.width=1350;cv.height=820;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#0b1520';ctx.fillRect(0,0,1350,820);['idle','talk-small','talk-medium','talk-wide','talk-o'].forEach((em,i)=>{ctx.drawImage(XART.get('port_cf_cole_'+em),i*270,0,256,256);ctx.drawImage(XART.get('comm_cole_'+em),i*270,280,256,256);});for(let i=0;i<3;i++)ctx.drawImage(XART.get('fb2_cole_rage_'+i),i*270,560,256,256);}''');save(p,'poses')
  p.evaluate('()=>{cv.width=960;cv.height=1024;window.cp5Seen=[];window.cp5Get=XART.get;XART.get=function(k){if(/^comm_cole_/.test(k))cp5Seen.push(k);return cp5Get.apply(this,arguments);};}')
  for i in range(16):
   p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1520';ctx.fillRect(0,0,cutsceneViewWidth(),VH);dlgBox({who:'COLE',portrait:'cole',full:'Listen up, team. We are bringing everyone home. Stay sharp and watch those fighters!',shown:'Listen up, team.',forceShown:true,pw:440,ph:140,x:20,y:180});}''')
   save(p,'talk-%02d'%i);p.wait_for_timeout(85)
  ck(p.evaluate('()=>new Set(cp5Seen).size>=4'),'Live dialogue cycles authored mouth poses')
  p.evaluate('''()=>{cp5Seen=[];ctx.setTransform(SS,0,0,SS,0,0);dlgBox({who:'COLE',portrait:'cole',full:'We are bringing everyone home.',shown:'We are bringing everyone home.',forceShown:true});}''')
  ck(p.evaluate('()=>cp5Seen.includes("comm_cole_idle")'),'Completed dialogue returns to neutral portrait');save(p,'completed')
  # Render actual Stage 6 shouting caller rather than only direct image keys.
  p.evaluate('''()=>{run.stage=6;setState(GS.PLAY);fb2Talk={done:false,i:0,shown:12,beats:[{who:'COLE',rage:true,text:'Listen up! Nobody is being left behind.'}]};ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1520';ctx.fillRect(0,0,VW,VH);fb2TalkDraw();}''');save(p,'stage6-rage')
  ck(p.evaluate('()=>fb2TalkActive()&&[0,1,2].every(i=>XART.get("fb2_cole_rage_"+i).width===256)'),'Stage 6 shouting dialogue uses complete fixed portraits')
  b.close()
finally:
 stop();(O/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
assert not report['errors'],report['errors']
assert all(c['ok'] for c in report['checks']),report['checks']
from PIL import Image
frames=[Image.open(O/('talk-%02d.png'%i)).convert('RGB') for i in range(16)]
frames[0].save(O/'talk.gif',save_all=True,append_images=frames[1:],duration=85,loop=0)
(O/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Cole portrait repair</title>
<style>body{background:#0b1520;color:#e9f4ff;font:17px Arial;max-width:1400px;margin:28px auto;padding:20px}img{max-width:100%;image-rendering:pixelated}.dialogue{width:480px;vertical-align:top}a{color:#74d9ff}</style>
<h1>Cole's stable talking portrait</h1><p>Complete fixed bezel, anchored head/shoulders and authored animated lips. All expression rails retain the same complete frame.</p>
<img src="poses.png" alt="Native regular, comm and shouting frames"><p>Live game dialogue animation and Stage 6 shouting box:</p>
<img class="dialogue" src="talk.gif" alt="Native talking animation"><img class="dialogue" src="stage6-rage.png" alt="Stage 6 shouting dialogue">
<p><a href="checks.json">Native checks</a> · <a href="../../index.html?build=cole-portraits-1005">Open game</a></p>''',encoding='utf-8')
