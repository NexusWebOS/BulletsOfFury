"""Inspect authored plates through XART and the game's Chromium canvas."""
import base64,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/stage_1_5_0914';OUT.mkdir(parents=True,exist_ok=True)
keys=['nef_s1_camo_attack_jet_intact','nef_s1_camo_attack_jet_damaged','nef_s1_camo_attack_jet_critical','nef_s1_jungle_tank_intact','nsd_chim_0','nsd_chim_4','nxp_upward_0','nxp_upward_4','s4w_boss_idle','nsb_olivewarden_intact','nsb_cryospear_intact','nsb_xenoregent_intact']+['l23fx_inferno_mg_'+str(i)for i in range(8)]+['l23fx_inferno_shotgun_'+str(i)for i in range(8)]+['bpfx_proj_laser_0','bpfx_proj_missile_0','bfx_cryo_p_0','s4w_mg_round_0','s4w_helper_dual_0']
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
        for row in range(8):
            r=pg.evaluate('''row=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#17222d';ctx.fillRect(0,0,480,512);for(let f=0;f<4;f++){combatAtlasDraw('cfx_stage2_volcanic_projectiles',4,8,row*4+f,60+f*120,200,114,114,{});ctx.fillStyle='white';ctx.font='12px monospace';ctx.fillText('row '+row+' frame '+f,f*120+5,280);}return document.querySelector('#screen').toDataURL().split(',')[1];}''',row);path=OUT/('s2_row_%d.png'%row);path.write_bytes(base64.b64decode(r));frames.append(path)
        for stage,role in [(1,'mini'),(1,'boss'),(3,'boss'),(4,'mini'),(4,'boss'),(5,'boss')]:
            pg.evaluate('a=>window.__fight(a[0],a[1],"yuri")',[stage,role]);pg.evaluate('()=>{playerHit=function(){};Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);}');
            for _ in range(8):pg.evaluate('()=>window.__step(60)');pg.wait_for_timeout(60)
            info=pg.evaluate('''role=>{const b=role==='mini'?subBoss:boss;if(!b)return null;const slots={};if(b._ship)for(const s in SHIPBOSS[b._ship].mounts)slots[s]=shipBossMount(b,s);return {kind:b.kind,ship:b._ship,name:b.name,x:b.x,y:b.y,w:b.w,h:b.h,slots,war:b._s4war?{mode:b._s4war.mode,nodes:b._s4war.shield&&b._s4war.shield.nodes}:null,shots:eBullets.slice(0,8).map(q=>({kind:q.kind,fx:q._l23fx,s4:q._s4wKind}))};}''',role);details[str(stage)+role]=info
            pg.evaluate('()=>drawWorld(0)');r=pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]");path=OUT/('before_%d_%s.png'%(stage,role));path.write_bytes(base64.b64decode(r));frames.append(path)
        b.close()
    stop();details['errors']=errors;(OUT/'inspection.json').write_text(json.dumps(details,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(480*4,540*((len(frames)+3)//4)),'#17222d');d=ImageDraw.Draw(sheet)
    for i,path in enumerate(frames):sheet.paste(Image.open(path).convert('RGB'),(i%4*480,i//4*540));d.text((i%4*480+5,i//4*540+514),path.stem,fill='white')
    sheet.save(OUT/'inspection.png');print(json.dumps(details),flush=True)
if __name__=='__main__':main()
