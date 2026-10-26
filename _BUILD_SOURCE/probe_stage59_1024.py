from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage59_1024';D=R/'_ART_SOURCES/stage59_1024/references';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  rows=[]
  for diff in ['normal','hard','furious']:
   row=p.evaluate('''diff=>{diffKey=diff;debugStartFight({stage:5,role:'mini',kind:'spacebomber',name:'Space bomber'},{pilot:'maverick'});spawnSubBoss__inner('spacebomber');window.B=subBoss;debugFight.spawned=true;B.enter=B._noHit=false;B.y=B.ty;B._drawY=B.y;const targets=retinaBossTargets(B);return{diff,kind:B.kind,space:B._bomber.space,mode:B._bomber.mode,parts:siegeBomberParts(B),targets:targets.map(t=>({id:t._retinaId,x:t.x,y:t.y,hp:t.hp,dead:t.dead,valid:retinaTargetValid(t)}))}}''',diff);rows.append(row)
  rows.append(p.evaluate('''()=>{const B=subBoss;B._bomber.mode='hc-recover';B._bomber.core=0;for(const p of B._bomber.parts)if(p.id!=='laserR')p.hp=0;B.hp=B._bomber.parts.find(p=>p.id==='laserR').hp;const q=siegeBomberParts(B).find(p=>p.id==='laserR'),part=B._bomber.parts.find(p=>p.id==='laserR'),before=part.hp;const bullet={kind:'spaceLaser',x:q.x,y:q.y,w:8,h:24,dmg:10,lv:1,t:0,vx:0,vy:0};const hit=spaceBulletHit(bullet,false);retinaScanClear();const targets=retinaBossTargets(B);for(const t of targets)retinaScanAdd(t);return{lastRight:part.hp,before,hit:hit?._retinaId,targets:targets.map(t=>({id:t._retinaId,dead:t.dead,valid:retinaTargetValid(t)})),marks:retinaScanState().marks.map(m=>m.target._retinaId)}}'''))
  p.evaluate('()=>["ns9x_horizonblk_0","ns9x_horizonblk_3","ns9x_horizonblk_6"].forEach(k=>XART.rdy(k))');p.wait_for_function('()=>["ns9x_horizonblk_0","ns9x_horizonblk_3","ns9x_horizonblk_6"].every(k=>XART.rdy(k))')
  for i in [0,3,6]:
   q=p.evaluate('''i=>{const im=XART.get('ns9x_horizonblk_'+i),c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;const k=232/Math.max(im.width,im.height);g.drawImage(im,128-im.width*k/2,128-im.height*k/2,im.width*k,im.height*k);return{png:c.toDataURL(),size:[im.width,im.height],k}}''',i);(D/f'black-{i}.png').write_bytes(base64.b64decode(q.pop('png').split(',')[1]));rows.append(dict(black=i,**q))
  (O/'baseline.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2)+'\n');print(json.dumps(rows)[:4000]);br.close()
finally:stop()
