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
        pg.evaluate('()=>window.__fight(4,"mini","yuri")')
        pg.evaluate("()=>{stagePlan=[];enemies=[];playerHit=function(){};story=null;window.__auto=function(){};Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);}")
        for _ in range(80):
            if pg.evaluate("()=>subBoss&&!subBoss.enter&&subBoss.y>0"):break
            pg.evaluate("()=>window.__step(6)");pg.wait_for_timeout(12)
        pg.evaluate("()=>window.__step(83)")
        details=pg.evaluate('()=>{window.__hits=[];const z=ctx.stroke;ctx.stroke=function(){if(__hits.length<20)__hits.push({type:"stroke",style:this.strokeStyle,stack:new Error().stack});return z.apply(this,arguments);};const f=ctx.fillRect;ctx.fillRect=function(x,y,w,h){if(h>150&&w<30&&__hits.length<30)__hits.push({type:"fill",style:this.fillStyle,args:[x,y,w,h],stack:new Error().stack});return f.apply(this,arguments);};const d=ctx.drawImage;ctx.drawImage=function(){const ar=Array.from(arguments),w=ar[ar.length-2],h=ar[ar.length-1];if(h>150&&w<35&&__hits.length<30)__hits.push({type:"image",args:ar.slice(1),stack:new Error().stack});return d.apply(this,arguments);};drawWorld(0);return {state,mini:{y:subBoss.y,x:subBoss.x,mode:subBoss._s4war.mode,t:subBoss._s4war.t,enter:subBoss.enter},hits:__hits,shots:pBullets.map(q=>({kind:q.kind,x:q.x,y:q.y})),weapon:run.weapon,debug:!!debugFight,sba:subBoss._sba};}')
        b.close()
    stop();details['errors']=errors;(OUT/'diagnosis.json').write_text(json.dumps(details,indent=2),encoding='utf-8')
    print(json.dumps(details),flush=True)
if __name__=="__main__":main()
