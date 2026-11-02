from pathlib import Path
import sys,base64,json,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
S=R/'_BUILD_SOURCE/stage7_amplify_1101';S.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
sources={'brood':'exec-5ef10c99-86c5-4520-be9f-d7e4e9762705.png','relay':'exec-03044d01-c071-4d31-a1b6-714a586618bd.png','slime':'exec-420335ab-e728-4c28-9c06-551638acacd2.png','missilejet':'exec-754fa930-57cd-411f-848f-cf5509b257fc.png','barge':'exec-c209c02a-5256-4a93-9a22-c3b5461aa94c.png','crescent':'exec-1f03868d-90aa-4727-b307-916eee6c78d4.png','crawler':'exec-a5f0ec77-62b6-4588-8283-f6b8ebfe847d.png'}
for n,f in sources.items():
 if not(S/(n+'_source.png')).exists():shutil.copyfile(G/f,S/(n+'_source.png'))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page()
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF)
 p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(7,"furious")')
 keys=['s7atk_toxic_mini_tank_0','nst7_master','overhaul_ground_base_7','overhaul_ground_head_mg','overhaul_ground_head_laser','overhaul_ground_head_sonic','rzb_sonic_wave']
 p.wait_for_function('(ks)=>{stageLoadTick();return ks.every(k=>XART.rdy(k))}',arg=keys,timeout=180000)
 for k in keys:
  a=p.evaluate('(k)=>{const a=XART.get(k),c=document.createElement("canvas");c.width=a.naturalWidth||a.width;c.height=a.naturalHeight||a.height;c.getContext("2d").drawImage(a,0,0);return c.toDataURL()}',k)
  (S/(k+'.png')).write_bytes(base64.b64decode(a.split(',')[1]))
 print(p.evaluate('()=>({ground:typeof modularGroundTurretTick,keys:Object.keys(XART._src).filter(k=>/sewer|nst7/.test(k)).slice(0,24)})'))
 b.close()
