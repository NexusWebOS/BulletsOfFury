"""Render the existing weapon art through the runtime's own XART resolver."""
import base64,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/weapon_feedback_0913'
OUT.mkdir(parents=True,exist_ok=True)
before=OUT/'game.before.js'
if not before.exists():before.write_bytes((ROOT/'assets/game.js').read_bytes())
keys=['nsw_ring_'+str(i)for i in range(4)]+['nsw_circ_'+str(i)for i in range(4)]+['nsw_dist_'+str(i)for i in range(4)]+['jchg_'+str(i)for i in range(4)]+['jwb_ball','jwb_ball_hot','jwb_link','jwb_burst']+['ndr_dambreaker_bottomthruster_'+str(i)for i in range(4)]
errors=[]
port,stop=shoot.serve(str(ROOT))
with sync_playwright()as p:
    b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1100,'height':1200})
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
    pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000)
    pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
    pg.evaluate(shoot.TRAP_RAF)
    for _ in range(100):
        ready=pg.evaluate('(ks)=>ks.every(k=>XART.rdy(k))&&XART.rdy("bof_laser_mist_weapon_atlas")',keys)
        if ready:break
        pg.wait_for_timeout(80)
    r=pg.evaluate('''(keys)=>{const c=document.createElement('canvas');c.width=1024;c.height=1080;const g=c.getContext('2d');g.fillStyle='#101923';g.fillRect(0,0,c.width,c.height);const dims={};
    const all=keys.concat(['lmfx_beam_1_2','lmfx_beam_5_2','lmfx_impact_3','lmfx_decal_3','lmfx_bubble_3']);
    all.forEach((k,i)=>{const x=(i%8)*128,y=Math.floor(i/8)*216;g.fillStyle='#a7b5c6';g.font='10px monospace';g.fillText(k,x+3,y+200);if(k.startsWith('lmfx'))laserMistAtlasBlit(g,k,x+64,y+92,90,120,true);else if(XART.rdy(k)){const im=XART.get(k),w=im.naturalWidth||im.width,h=im.naturalHeight||im.height,sc=Math.min(112/w,174/h);dims[k]={w:w,h:h,nw:im.naturalWidth,nh:im.naturalHeight};g.imageSmoothingEnabled=false;g.drawImage(im,x+(128-w*sc)/2,y+(182-h*sc)/2,w*sc,h*sc);}});return {png:c.toDataURL().split(',')[1],dims:dims};}''',keys)
    (OUT/'assets.png').write_bytes(base64.b64decode(r.pop('png')))
    r['errors']=errors;(OUT/'asset-inspection.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r),flush=True);b.close()
stop()
