"""Inspect authored plates through XART and the game's Chromium canvas."""
import base64,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/encounter_cleanup_0914';OUT.mkdir(parents=True,exist_ok=True)
keys=['mgcf_1_5', 's4w_muzzle_mg_4', 's4w_mg_round_4', 'bpfx_muzzle_machinegun_4', 'bpfx_muzzle_void_4', 'bpfx_proj_missile_0', 'l23fx_rime_laser_3', 'nlz_3_b3', 'bfx_cryo_p_3', 'nsb_rimewall_intact', 'nsb_olivewarden_intact', 's4w_boss_idle']

def main():
    errors=[];details={};port,stop=shoot.serve(str(ROOT));frames=[]
    with sync_playwright()as p:
        b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB);pg.evaluate('()=>window.__auto=function(){}')
        for _ in range(100):
            r=pg.evaluate('(ks)=>{ks.forEach(k=>XART.rdy(k));return ks.every(k=>XART.rdy(k))&&XART.rdy("cfx_stage2_volcanic_projectiles");}',keys)
            if r:break
            pg.wait_for_timeout(60)
        for i in range(0,len(keys),12):
            r=pg.evaluate('''ks=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#17222d';ctx.fillRect(0,0,480,512);const dims={};ks.forEach((k,i)=>{const x=(i%4)*120,y=Math.floor(i/4)*170;ctx.fillStyle='white';ctx.font='7px monospace';ctx.fillText(k,x+2,y+160);if(!XART.rdy(k))return;const im=XART.get(k),w=im.width||im.naturalWidth,h=im.height||im.naturalHeight,sc=Math.min(110/w,145/h);dims[k]=[w,h];ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x+(120-w*sc)/2,y+(150-h*sc)/2,w*sc,h*sc);});return {png:document.querySelector('#screen').toDataURL().split(',')[1],dims};}''',keys[i:i+12]);path=OUT/('art_%d.png'%i);path.write_bytes(base64.b64decode(r.pop('png')));frames.append(path);details.update(r['dims'])
        b.close()
    stop();details['errors']=errors;(OUT/'inspection.json').write_text(json.dumps(details,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(480*4,540*((len(frames)+3)//4)),'#17222d');d=ImageDraw.Draw(sheet)
    for i,path in enumerate(frames):sheet.paste(Image.open(path).convert('RGB'),(i%4*480,i//4*540));d.text((i%4*480+5,i//4*540+514),path.stem,fill='white')
    sheet.save(OUT/'inspection.png');print(json.dumps(details),flush=True)
if __name__=='__main__':main()
