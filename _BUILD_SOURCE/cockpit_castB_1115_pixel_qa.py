from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import hashlib,json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/cockpit_castB_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
data=json.loads((R/'assets/cockpit_talk_art_1114.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'));old=json.loads((R/'_ART_SOURCES/cockpit_castB_1115/previous-cockpit-registry.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
checks=[];errors=[]
def ck(n,v,meta=None):checks.append({'name':n,'ok':bool(v),'data':meta})
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?castB-pixel-oracle=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.wait_for_function('()=>[...Object.values(CP15_ART.banks),...Object.values(CP15_ART.minis)].map(a=>XART.rdy(a.key)).every(Boolean)',polling=50)
 for pilot,B in data['banks'].items():
  ck(pilot+' registry names new castB source and new page hash',B['family']=='castB-1115'and '/cockpit_castB_1115/'in B['path']and B['sha256']!=old['banks'][pilot]['sha256']and hashlib.sha256((R/B['path']).read_bytes()).hexdigest()==B['sha256'],B)
  atlas=Image.open(R/B['path']).convert('RGBA')
  for f in range(8):
   im=atlas.crop((f%4*544,f//4*364,(f%4+1)*544,(f//4+1)*364));bg=Image.new('RGBA',(544,364),(8,13,20,255));bg.alpha_composite(im);expected=hashlib.sha256(bg.tobytes()).hexdigest()
   q=p.evaluate("""async([pilot,frame])=>{const pose=cp15Pose;ctx.save();try{cp15Pose=()=>frame;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.filter='none';ctx.clearRect(0,0,544,364);ctx.fillStyle='#080d14';ctx.fillRect(0,0,544,364);const drawn=cp15Draw(pilot,[0,0,544,364],{who:pilot.toUpperCase(),text:'test'},{age:0,shown:1,t:1});const a=ctx.getImageData(0,0,544,364).data,h=await crypto.subtle.digest('SHA-256',a);return{hash:Array.from(new Uint8Array(h)).map(n=>n.toString(16).padStart(2,'0')).join(''),drawn};}finally{cp15Pose=pose;ctx.restore();}}""",[pilot,f])
   ck(pilot+' frame'+str(f)+' native pixels equal new authored source',q['hash']==expected and q['drawn']['artFamily']=='castB-1115'and q['drawn']['assetSha256']==B['sha256'],q)
 q=p.evaluate("()=>CP15_ART.pilots.flatMap(p=>['cockpit-sky','cockpit-space','cockpit-tunnel'].flatMap(room=>[48,64,84,96].map(n=>({p,room,n,path:FP5_ART.banks['mini-'+room+'-'+p+'-'+n].path,family:FP5_ART.banks['mini-'+room+'-'+p+'-'+n].family}))))")
 ck('all108 small radio bindings use new castB files',len(q)==108 and all(v['family']=='castB-1115'and '/cockpit_castB_1115/'in v['path']for v in q),q)
 ck('no page/console/HTTP errors',not errors,errors);b.close()
(O/'pixel-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Actual CP15 canvas blits at1:1 backing pixels compared byte-exact to all72 new source cells over their real underlay. Original rejected page hashes are explicitly excluded. Renderer checkpoints, not personal likeness approval or campaign wins.'},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' new-file/pixel checks passed',flush=True);assert all(c['ok']for c in checks)
