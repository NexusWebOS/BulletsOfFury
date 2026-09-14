#!/usr/bin/env python3
"""Capture live Level-5 orbital and Level-9 Velocity Void combat proof GIFs."""

from __future__ import annotations

import functools
import http.server
import subprocess
import sys
import threading
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import Page, sync_playwright

ROOT=Path(__file__).resolve().parents[1]
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass


def serve():
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();return server


def enemy_case(stage:int,kind:str,x:int=240,y:int=132,duration:int=4400):
    side="e._side=1;e._dir=1;" if kind in {"s5skimmer","s9comet"} else ""
    return {"stage":stage,"name":f"Stage{stage}_{kind}_Enemy_AI","duration":duration,
            "setup":f"""() => {{const e=spawnEnemy('{kind}',{x},{y},{{}});if(e){{e.x={x};e.y={y};e._fcd=0;e._stagger=0;{side}}}}}"""}


CASES=[
    *[enemy_case(5,k,80 if k=="s5skimmer" else 240,duration=5200 if k in {"s5gravity","s5station","s5repair"} else 4400)
      for k in ["s5frigate","s5rammer","s5skimmer","s5gravity","s5interceptor","s5minelayer",
                "s5satellite","s5portalmine","s5repair","s5salvage","s5leech","s5station"]],
    {"stage":5,"name":"Stage5_Chaos_Harrier_Miniboss_AI","duration":9800,"setup":r"""() => {
      spawnSubBoss('chaosharrier');subBoss.enter=false;subBoss.x=240;subBoss.y=116;subBoss.ty=116;subBoss.fireCd=.04;
      window.__spaceProofTimeouts.push(setTimeout(()=>{if(subBoss&&!subBoss.dead){subBoss.hp=subBoss.maxhp*.32;subBoss.fireCd=.04;}},4700));}"""},
    {"stage":5,"name":"Stage5_Xeno_Regent_Four_Phase_Boss","duration":15000,"setup":r"""() => {
      spawnBoss('xenoregent');boss.enter=false;boss.x=VW/2;boss.y=118;boss.ty=118;boss.fireCd=.04;
      for(const row of [[3600,.68],[7200,.43],[10800,.18]])window.__spaceProofTimeouts.push(setTimeout(()=>{if(boss&&!boss.dead){boss.hp=boss.maxhp*row[1];boss.fireCd=.04;boss._sba=null;}},row[0]));}"""},
    *[enemy_case(9,k,80 if k=="s9comet" else 240,duration=5200 if k in {"s9prism","s9singularity"} else 4400)
      for k in ["s9beacon","s9chronal","s9comet","s9gunship","s9interceptor","s9gatecarrier",
                "s9gateturret","s9gravity","s9prism","s9warptank","s9ring","s9singularity"]],
    {"stage":9,"name":"Stage9_Rift_Wardens_SubBoss","duration":11500,"setup":r"""() => {
      spawnSubBoss('riftwardens');subBoss.enter=false;subBoss._s9rift.t=1.35;
      window.__spaceProofTimeouts.push(setTimeout(()=>{if(subBoss&&subBoss._s9rift){const F=subBoss._s9rift;F.left.hp=2;s9RiftWardensHit(subBoss,4,F.left.x,F.left.y);}},5600));}"""},
    {"stage":9,"name":"Stage9_Warp_Sentinels_To_Tidal_Sovereign","duration":17000,"setup":r"""() => {
      spawnBoss('tidalfusion');boss.enter=false;boss._s9fusion.t=1.45;boss.fireCd=.04;
      window.__spaceProofTimeouts.push(setTimeout(()=>{if(boss&&boss._s9fusion&&boss._s9fusion.phase==='twins'){const F=boss._s9fusion;F.left.hp=2;F.hit=F.left;s9FusionHit(boss,4);}},3400));
      window.__spaceProofTimeouts.push(setTimeout(()=>{if(boss&&boss._s9fusion&&boss._s9fusion.phase==='twins'){const F=boss._s9fusion;F.right.hp=2;F.hit=F.right;s9FusionHit(boss,4);}},5200));
      for(const row of [[9000,.68],[11500,.43],[14000,.18]])window.__spaceProofTimeouts.push(setTimeout(()=>{if(boss&&boss._ship==='tidalsovereign'){boss.hp=boss.maxhp*row[1];boss.fireCd=.04;boss._sba=null;}},row[0]));}"""},
]


def common_setup(stage:int):
    return f"""() => {{
      if(window.__spaceProofTimer)clearInterval(window.__spaceProofTimer);
      if(window.__spaceProofTimeouts)for(const id of window.__spaceProofTimeouts)clearTimeout(id);window.__spaceProofTimeouts=[];
      beginStage({stage});player.reset();player.invuln=999999;player.x=240;player.y=438;snapCamToPlayer();setState(GS.PLAY);
      stagePlan=[{{t:9999,fn:function(){{}}}}];waveIdx=0;stageTimer=0;enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;explosions.length=0;smokeTrails.length=0;playerLocks.length=0;
      boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
      const started=performance.now();window.__spaceProofTimer=setInterval(()=>{{const t=(performance.now()-started)/1000;player.x=240+Math.sin(t*.91)*128;player.y=438+Math.sin(t*.53)*9;player.invuln=999999;}},16);
    }}"""


def start_capture(page:Page):
    return page.evaluate("""() => {const c=document.getElementById('screen'),stream=c.captureStream(24),mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t))||'',chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};window.__spaceCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();})};rec.start(250);return {w:c.width,h:c.height};}""")


def stop_capture(page:Page,webm:Path):
    with page.expect_download(timeout=30000) as info:
        page.evaluate("""async()=>{const blob=await window.__spaceCapture.stop(),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='space-ai.webm';document.body.appendChild(a);a.click();a.remove();}""")
    info.value.save_as(webm)


def make_gif(webm:Path,gif:Path):
    vf=("fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=112:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run([FFMPEG,"-loglevel","error","-y","-i",str(webm),"-lavfi",vf,"-loop","0",str(gif)],check=True)


def make_contact(webm:Path,png:Path):
    subprocess.run([FFMPEG,"-loglevel","error","-y","-i",str(webm),"-vf","fps=2,scale=240:-1:flags=lanczos,tile=4x2:padding=4:margin=4:color=black","-frames:v","1",str(png)],check=True)


def main():
    selected=set(sys.argv[1:]);server=serve();errors=[]
    try:
      with sync_playwright() as pw:
        browser=pw.chromium.launch(args=["--disable-gpu","--no-sandbox","--mute-audio"]);page=browser.new_page(viewport={"width":760,"height":820})
        page.on("pageerror",lambda err:errors.append(str(err)));page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html",wait_until="load",timeout=60000)
        page.wait_for_function("() => typeof s5SpaceTick==='function'&&typeof s9VoidTick==='function'&&(window.__bofFrames|0)>4",timeout=60000)
        page.evaluate("""() => {for(const H of [S5SPACE,S9VOID])for(const k in H)for(let i=0;i<8;i++)XART._touch((H===S5SPACE?'s5atk_':'s9atk_')+H[k].art+'_'+i);for(let i=0;i<12;i++){XART._touch('s5fracture_'+i);XART._touch('s9lattice_'+i);}}""")
        page.wait_for_function("() => XART.rdy('s5atk_beam_frigate_0')&&XART.rdy('s5atk_twin_station_7')&&XART.rdy('s9atk_alien_beacon_0')&&XART.rdy('s9atk_singularity_mine_7')&&XART.rdy('s5fracture_11')&&XART.rdy('s9lattice_11')",timeout=60000)
        for case in CASES:
          if selected and case["name"] not in selected:continue
          out=ROOT/"docs"/"proofs"/f"stage{case['stage']}_ai_live";out.mkdir(parents=True,exist_ok=True)
          page.evaluate(common_setup(case["stage"]));page.evaluate(case["setup"]);page.wait_for_timeout(350);cap=start_capture(page);page.wait_for_timeout(case["duration"])
          page.locator("#screen").screenshot(path=str(out/f"{case['name']}.png"));webm=out/f"{case['name']}.webm";gif=out/f"{case['name']}.gif"
          stop_capture(page,webm);make_gif(webm,gif);make_contact(webm,out/f"{case['name']}_contact.png");print(f"{case['name']}: {cap['w']}x{cap['h']} gif={gif.stat().st_size}",flush=True)
        page.evaluate("() => {if(window.__spaceProofTimer)clearInterval(window.__spaceProofTimer);}");browser.close()
    finally:server.shutdown();server.server_close()
    if errors:raise RuntimeError("Browser errors: "+" | ".join(errors))


if __name__=="__main__":main()
