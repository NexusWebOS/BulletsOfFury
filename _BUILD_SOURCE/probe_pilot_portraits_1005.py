"""All nine pilots' actual XART portraits, frame rails and live mouth animation."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
from PIL import Image
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/pilot_portraits_1005';O.mkdir(parents=True,exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8');report={'checks':[],'errors':[]}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def save(p,n):(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:800]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('''()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};setState(GS.CUTSCENE);window.pp5Pilots=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'];for(const p of pp5Pilots)for(const em of PP5.poses){XART.rdy('port_cf_'+p+'_'+em);XART.rdy('comm_'+p+'_'+em);}XART.rdy('dlg_rect_0914');bmfReady('dialogue');}''')
  p.wait_for_function('()=>pp5Pilots.every(p=>PP5.poses.every(em=>XART.rdy("port_cf_"+p+"_"+em)&&XART.rdy("comm_"+p+"_"+em)))&&XART.rdy("dlg_rect_0914")&&bmfReady("dialogue")',timeout=120000,polling=50)
  report['pixels']=p.evaluate('''()=>{
   const out=[];function pixels(k){const im=XART.get(k);return {w:im.width,h:im.height,d:im.getContext('2d').getImageData(0,0,im.width,im.height).data};}
   for(const p of pp5Pilots)for(const comm of [false,true]){
    const prefix=(comm?'comm_':'port_cf_')+p+'_',a=pixels(prefix+'idle'),r=p==='cole'?[92,140,45,34]:p==='lizzie'?[110,109,38,37]:PP5.mouths[p];
    const box=comm?[a.w-r[0]-r[2],r[1],r[2],r[3]]:r;
    const poses=PP5.poses.map(em=>{const b=pixels(prefix+em);let outside=0,inside=0,rails=0;
     for(let y=0;y<a.h;y++)for(let x=0;x<a.w;x++){let diff=false;for(let c=0;c<4;c++)if(a.d[(y*a.w+x)*4+c]!==b.d[(y*b.w+x)*4+c])diff=true;if(diff){if(x>=box[0]&&x<box[0]+box[2]&&y>=box[1]&&y<box[1]+box[3])inside++;else outside++;if(x<23||x>=a.w-23||y<24||y>=a.h-23)rails++;}}
     return {em,w:b.w,h:b.h,outside,inside,rails};});out.push({p,comm,w:a.w,h:a.h,poses});
   }return out;
  }''')
  for q in report['pixels']:
   tag=q['p']+(' comm' if q['comm'] else ' menu')
   ck(all(r['w']==q['w'] and r['h']==q['h'] for r in q['poses']),tag+' keeps one intrinsic size')
   ck(all(r['rails']==0 for r in q['poses']),tag+' complete rails remain fixed for every expression')
   for r in q['poses']:
    if r['em'].startswith('talk-'):
     ck(r['outside']==0,tag+' '+r['em']+' head/body/border stay anchored')
     ck(r['inside']==0 if r['em']=='talk-closed' else r['inside']>20,tag+' '+r['em']+' correct mouth animation')
  ck(p.evaluate('()=>Object.keys(PP5.mouths).every(p=>XART.get("face_"+p)===XART.get("port_cf_"+p+"_idle")&&XART.get("port_"+p+"_talk")===XART.get("port_cf_"+p+"_talk-closed"))'),'Legacy face and talk keys use repaired portraits')
  ck(p.evaluate('()=>XART.get("yuri_avatar")===XART.get("port_cf_yuri_idle")&&XART.get("yuri_v2_idle")===XART.get("port_cf_yuri_idle")'),'Yuri alternate entry points use repaired frame')
  for j,pilot in enumerate(['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']):
   p.evaluate('''pilot=>{cv.width=1350;cv.height=550;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#0b1520';ctx.fillRect(0,0,1350,550);['idle','talk-small','talk-medium','talk-wide','talk-o'].forEach((em,i)=>{ctx.drawImage(XART.get('port_cf_'+pilot+'_'+em),i*270,0);ctx.drawImage(XART.get('comm_'+pilot+'_'+em),i*270,280);});}''',pilot);save(p,pilot+'-poses')
  p.evaluate('''()=>{cv.width=960;cv.height=1024;window.pp5Seen={};window.pp5Get=XART.get;XART.get=function(k){if(/^comm_/.test(k))pp5Seen[k]=(pp5Seen[k]||0)+1;return pp5Get.apply(this,arguments);};window.pp5NativeNow=performance.now.bind(performance);window.pp5Now=pp5NativeNow();performance.now=()=>pp5Now;}''')
  # Step the browser clock one authored mouth interval per frame. PNG capture cost
  # must not skip different poses for later speakers in this nine-pilot batch.
  for i in range(10):
   p.evaluate('()=>{pp5Now+=85;}')
   for pilot in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
    p.evaluate('''pilot=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1520';ctx.fillRect(0,0,cutsceneViewWidth(),VH);dlgBox({who:pilot.toUpperCase(),portrait:pilot,full:'Keep formation, team. We are bringing everyone home. Stay sharp!',shown:'Keep formation, team.',forceShown:true,pw:440,ph:140,x:20,y:180});}''',pilot);save(p,pilot+'-talk-%02d'%i)
  p.evaluate('()=>{window.pp5TalkSeen=Object.keys(pp5Seen);performance.now=pp5NativeNow;}')
  for pilot in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
   ck(p.evaluate('p=>pp5TalkSeen.filter(k=>k.startsWith("comm_"+p+"_talk-")).length>=4',pilot),pilot+' live dialogue cycles mouth poses')
   p.evaluate('''pilot=>{pp5Seen={};dlgBox({who:pilot.toUpperCase(),portrait:pilot,full:'Ready, team.',shown:'Ready, team.',forceShown:true});}''',pilot)
   ck(p.evaluate('p=>!!pp5Seen["comm_"+p+"_idle"]',pilot),pilot+' returns to idle once speaking ends')
  b.close()
finally:
 stop();(O/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
assert not report['errors'],report['errors']
assert all(c['ok'] for c in report['checks']),[c for c in report['checks'] if not c['ok']]
for pilot in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
 fs=[Image.open(O/(pilot+'-talk-%02d.png'%i)).convert('RGB') for i in range(10)]
 fs[0].save(O/(pilot+'.gif'),save_all=True,append_images=fs[1:],duration=85,loop=0)
html='<!doctype html><meta charset="utf-8"><title>All pilot portraits</title><style>body{background:#0b1520;color:#e9f4ff;font:17px Arial;margin:28px}img{max-width:100%;image-rendering:pixelated}.live{width:430px}a{color:#74d9ff}</style><h1>All nine pilots: fixed portraits</h1><p>Complete authored borders and fixed heads/shoulders; mouth-only speech animation.</p>'
for pilot in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:html+='<h2>'+pilot.upper()+'</h2><img src="'+pilot+'-poses.png"><br><img class="live" src="'+pilot+'.gif">'
(O/'review.html').write_text(html+'<p><a href="checks.json">Native checks</a> · <a href="../../index.html?build=pilot-portraits-1005">Open game</a></p>',encoding='utf-8')
