#!/usr/bin/env python3
"""Live-canvas QA and visual proof for the Stage-3 Cryo Spear/Rime Wall role swap."""

from __future__ import annotations

import functools
import http.server
import json
import subprocess
import threading
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "stage3_boss_swap_0830"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


COMMON = r"""() => {
  beginStage(3); player.reset(); player.invuln=999999; player.x=240; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0; mapScroll=levelScrollRange();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  thaw=null; _frzNarr=null; boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  if(window.__s3SwapPilot)clearInterval(window.__s3SwapPilot);
  const born=performance.now();
  window.__s3SwapPilot=setInterval(()=>{
    const t=(performance.now()-born)/1000;player.x=240+Math.sin(t*.83)*132;
    player.y=438+Math.sin(t*.47)*8;player.invuln=999999;
  },16);
}"""


CASES = [
    {
        "slug": "stage3_cryospear_miniboss",
        "label": "CRYO SPEAR — MINIBOSS",
        "spawn": "spawnSubBoss('rimewall'); subBoss.enter=false; subBoss.x=240; subBoss.y=118; subBoss.ty=118; subBoss.fireCd=.02; subBoss._sbm=SBM_HOLD; subBoss._sbmT=999;",
        "entity": "subBoss",
        "expected": {"ship": "rimewall", "name": "CRYO SPEAR", "key": "nsb_cryo_spear", "role": "spear"},
        "ratios": [0.92, 0.56, 0.20],
        "patterns": ["s3spearburst", "s3spearcross", "s3spearcore"],
        "hold_ms": 2600,
    },
    {
        "slug": "stage3_rimewall_boss",
        "label": "RIME WALL — MAIN BOSS",
        "spawn": "spawnBoss('cryospear'); boss.enter=false; boss.x=240; boss.y=118; boss.ty=118; boss.fireCd=.02; boss._sbm=SBM_HOLD; boss._sbmT=999;",
        "entity": "boss",
        "expected": {"ship": "cryospear", "name": "RIME WALL", "key": "nsb_rimewall_intact", "role": "wall"},
        "ratios": [0.92, 0.68, 0.43, 0.18],
        "patterns": ["s3wallcannons", "s3wallgate", "s3wallhalo", "s3walloverdrive"],
        "hold_ms": 2850,
    },
]


def start_capture(page):
    return page.evaluate(r"""() => {
      const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
        .find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
      rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__s3SwapCapture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
        rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();
      })};rec.start(250);return {w:c.width,h:c.height,mime};
    }""")


def stop_capture(page, path: Path):
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(r"""async () => {
          const blob=await window.__s3SwapCapture.stop(),a=document.createElement('a');
          a.href=URL.createObjectURL(blob);a.download='stage3-swap.webm';document.body.appendChild(a);a.click();a.remove();
        }""")
    info.value.save_as(path)


def render_derivatives(webm: Path, gif: Path, contact: Path):
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi",
                    "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=112:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
                    "-loop", "0", str(gif)], check=True)
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
                    "fps=1,scale=240:-1:flags=lanczos,tile=4x3:padding=4:margin=4:color=black",
                    "-frames:v", "1", str(contact)], check=True)


def diagnostics(page, entity: str):
    return page.evaluate(f"""() => {{
      const b={entity},D=b&&SHIPBOSS[b._ship],S=b&&b._s3boss,L=(S&&S.releaseLog)||[];
      const muzzles=L.filter(x=>x.type==='muzzle'),shots=L.filter(x=>x.type==='shot');
      let maxAnchorError=0,matched=0;
      for(const m of muzzles){{
        const q=shots.filter(s=>s.slot===m.slot&&Math.abs(s.t-m.t)<.025)
          .sort((a,c)=>Math.abs(a.t-m.t)-Math.abs(c.t-m.t))[0];
        if(q){{matched++;maxAnchorError=Math.max(maxAnchorError,Math.hypot(q.x-m.x,q.y-m.y));}}
      }}
      return {{ship:b&&b._ship,name:b&&b.name,key:D&&D.key,role:S&&S.role,w:b&&b.w,h:b&&b.h,
        hp:b&&b.maxhp,shots:S&&S.shots,muzzles:S&&S.muzzles,kinds:S&&Object.assign({{}},S.kinds),
        patterns:S&&Object.keys(S.patternsSeen),matchedMuzzles:matched,maxAnchorError,
        projectiles:eBullets.filter(q=>q&&q._s3BossRole).map(q=>({{kind:q.kind,bfam:q._bfam,shootable:!!q._shootable}})).slice(-40),
        pageState:state,bossActive:!!bossActive,subBossActive:!!subBossActive}};
    }}""")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve(); errors = []; results = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof stage3BossAttack==='function' && (window.__bofFrames|0)>4", timeout=60_000)
            page.evaluate("""() => ['nsb_cryo_spear','nsb_rimewall_intact','nsb_rimewall_damaged','nsb_rimewall_critical'].forEach(k=>XART._touch(k))""")
            page.wait_for_function("() => XART.rdy('nsb_cryo_spear') && XART.rdy('nsb_rimewall_intact') && XART.rdy('nsb_rimewall_damaged') && XART.rdy('nsb_rimewall_critical')", timeout=60_000)

            for case in CASES:
                page.evaluate(COMMON);page.evaluate(f"() => {{{case['spawn']}}}")
                cap=start_capture(page)
                for idx,ratio in enumerate(case["ratios"]):
                    page.evaluate(f"""() => {{
                      const b={case['entity']};b.hp=b.maxhp*{ratio};b.fireCd=.01;b._sba=null;
                      if(b._s3boss){{b._s3boss.volley=null;b._s3boss.charge=null;}}
                    }}""")
                    page.wait_for_timeout(case["hold_ms"])
                    page.locator("#screen").screenshot(path=str(OUT / f"{case['slug']}_phase{idx+1}.png"))
                webm=OUT/f"{case['slug']}.webm";gif=OUT/f"{case['slug']}.gif";contact=OUT/f"{case['slug']}_contact.png"
                stop_capture(page,webm);render_derivatives(webm,gif,contact)
                d=diagnostics(page,case["entity"]);d.update({"case":case["label"],"capture":cap})
                exp=case["expected"]
                assert d["ship"]==exp["ship"] and d["name"]==exp["name"] and d["key"]==exp["key"] and d["role"]==exp["role"], d
                assert all(p in d["patterns"] for p in case["patterns"]), d
                assert d["shots"]>=20 and d["muzzles"]>=8, d
                assert d["matchedMuzzles"]>=6 and d["maxAnchorError"]<=0.01, d
                assert len(d["kinds"])>=3, d
                results.append(d)
                print(f"{case['label']}: shots={d['shots']} muzzles={d['muzzles']} patterns={d['patterns']} anchor={d['maxAnchorError']:.3f}px")

            page.evaluate("() => {if(window.__s3SwapPilot)clearInterval(window.__s3SwapPilot)}")
            browser.close()
    finally:
        server.shutdown();server.server_close()
    if errors:
        raise RuntimeError("Browser errors: "+" | ".join(errors))
    (OUT/"qa_results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")


if __name__ == "__main__":
    main()
