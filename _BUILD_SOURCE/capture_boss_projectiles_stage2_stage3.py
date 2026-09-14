#!/usr/bin/env python3
"""Live-canvas QA for the Stage-2/3 authored boss projectile families."""

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
OUT = ROOT / "docs" / "proofs" / "boss_projectiles_stage2_stage3_live"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


COMMON = r"""(stage) => {
  beginStage(stage); player.reset(); player.invuln=999999; player.x=240; player.y=438;
  snapCamToPlayer(); setState(GS.PLAY);
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=0; mapScroll=levelScrollRange();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  particles.length=0; explosions.length=0; smokeTrails.length=0; playerLocks.length=0;
  thaw=null; _frzNarr=null; boss=null; bossActive=false; bossDefeated=false;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  if(window.__l23Pilot)clearInterval(window.__l23Pilot);
  if(window.__l23Sampler)clearInterval(window.__l23Sampler);
  window.__l23Seen={fx:{},beams:[],angleChecks:[],nextBeam:1};
  const born=performance.now();
  window.__l23Pilot=setInterval(()=>{
    const t=(performance.now()-born)/1000;
    player.x=240+Math.sin(t*.93)*142;player.y=438;player.invuln=999999;
  },16);
  window.__l23Sampler=setInterval(()=>{
    for(const q of eBullets){if(q&&q._l23fx)window.__l23Seen.fx[q._l23fx]=1;}
    const b=boss||subBoss;
    if(b&&b._l23Beam){
      if(!b._l23Beam._qaId)b._l23Beam._qaId=window.__l23Seen.nextBeam++;
      const a=b._l23Beam.angles.slice();window.__l23Seen.beams.push({id:b._l23Beam._qaId,family:b._l23Beam.family,angles:a,t:b._l23Beam.t});
    }
  },20);
}"""


CASES = [
    {
        "slug": "stage2_inferno_reaver",
        "label": "INFERNO REAVER — STAGE 2 BOSS",
        "stage": 2,
        "spawn": "spawnBoss('infernoreaver'); boss.enter=false; boss.x=240; boss.y=116; boss.ty=116; boss._sbm=SBM_HOLD; boss._sbmT=999;",
        "entity": "boss",
        "steps": [(.95, 2, 650), (.55, 2, 700), (.35, 1, 2600), (.15, 2, 800)],
        "expected_fx": ["inferno_mg", "inferno_shotgun"],
        "expected_beam": "inferno",
        "beam_mode": "bounded45",
    },
    {
        "slug": "stage3_cryo_spear_miniboss",
        "label": "CRYO SPEAR — STAGE 3 MINIBOSS",
        "stage": 3,
        "spawn": "spawnSubBoss('rimewall'); subBoss.enter=false; subBoss.x=240; subBoss.y=116; subBoss.ty=116; subBoss._sbm=SBM_HOLD; subBoss._sbmT=999;",
        "entity": "subBoss",
        "steps": [(.84, 2, 650), (.49, 2, 850), (.15, 1, 2300)],
        "expected_fx": ["cryo_ball"],
        "expected_beam": "rime",
        "beam_mode": "locked",
    },
    {
        "slug": "stage3_rime_wall_boss",
        "label": "RIME WALL — STAGE 3 BOSS",
        "stage": 3,
        "spawn": "spawnBoss('cryospear'); boss.enter=false; boss.x=240; boss.y=116; boss.ty=116; boss._sbm=SBM_HOLD; boss._sbmT=999;",
        "entity": "boss",
        "steps": [(.88, 2, 650), (.63, 2, 800), (.38, 2, 900), (.13, 1, 2500)],
        "expected_fx": ["rime_orb"],
        "expected_beam": "rime",
        "beam_mode": "locked",
    },
]


def start_capture(page):
    return page.evaluate(r"""() => {
      const c=document.getElementById('screen'),stream=c.captureStream(24);
      const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']
        .find(t=>MediaRecorder.isTypeSupported(t))||'';
      const chunks=[],rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
      rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
      window.__l23Capture={rec,chunks,mime,stop:()=>new Promise(resolve=>{
        rec.onstop=()=>resolve(new Blob(chunks,{type:mime||'video/webm'}));rec.stop();
      })};rec.start(250);return {w:c.width,h:c.height,mime};
    }""")


def stop_capture(page, path: Path):
    with page.expect_download(timeout=30_000) as info:
        page.evaluate(r"""async () => {
          const blob=await window.__l23Capture.stop(),a=document.createElement('a');
          a.href=URL.createObjectURL(blob);a.download='l23-boss-projectiles.webm';
          document.body.appendChild(a);a.click();a.remove();
        }""")
    info.value.save_as(path)


def render_derivatives(webm: Path, gif: Path, contact: Path):
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-lavfi",
        "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];"
        "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
        "-loop", "0", str(gif),
    ], check=True)
    subprocess.run([
        FFMPEG, "-loglevel", "error", "-y", "-i", str(webm), "-vf",
        "fps=1,scale=240:-1:flags=lanczos,tile=4x3:padding=4:margin=4:color=black",
        "-frames:v", "1", str(contact),
    ], check=True)


def diagnostics(page, entity: str):
    return page.evaluate(f"""() => {{
      const b={entity},seen=window.__l23Seen||{{fx:{{}},beams:[]}};
      const groups={{}};
      for(const s of seen.beams||[]){{(groups[s.id]||(groups[s.id]=[])).push(s);}}
      const angleChecks=[];
      for(const [id,samples] of Object.entries(groups)){{
        if(samples.length<2)continue;
        const first=samples[0].angles,last=samples[samples.length-1].angles;
        let max=0,minAngle=Infinity,maxAngle=-Infinity,maxSouthOffset=0;
        for(let i=0;i<Math.min(first.length,last.length);i++)max=Math.max(max,Math.abs(first[i]-last[i]));
        for(const sample of samples)for(const ang of sample.angles){{minAngle=Math.min(minAngle,ang);maxAngle=Math.max(maxAngle,ang);maxSouthOffset=Math.max(maxSouthOffset,Math.abs(ang-Math.PI/2));}}
        angleChecks.push({{id:Number(id),family:samples[0].family,samples:samples.length,maxAngleDrift:max,
          minAngle,maxAngle,sweepRange:maxAngle-minAngle,maxSouthOffset}});
      }}
      return {{ship:b&&b._ship,name:b&&b.name,fx:Object.keys(seen.fx||{{}}),beamFamilies:[...new Set((seen.beams||[]).map(s=>s.family))],
        angleChecks,live:eBullets.filter(q=>q&&q._l23fx).map(q=>q._l23fx),
        activeBeam:b&&b._l23Beam?b._l23Beam.family:null}};
    }}""")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve(); page_errors = []; console_errors = []; results = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 760, "height": 820}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
            page.wait_for_function("() => typeof l23BossBeamStart==='function' && (window.__bofFrames|0)>4", timeout=60_000)
            page.evaluate(r"""() => {
              const names=['inferno_mg','inferno_shotgun','cryo_ball','rime_orb'];
              for(const name of names)for(let i=0;i<8;i++)XART._touch('l23fx_'+name+'_'+i);
              for(const name of ['inferno_laser','rime_laser'])for(let i=0;i<12;i++)XART._touch('l23fx_'+name+'_'+i);
            }""")
            page.wait_for_function(r"""() => {
              for(const name of ['inferno_mg','inferno_shotgun','cryo_ball','rime_orb'])
                for(let i=0;i<8;i++)if(!XART.rdy('l23fx_'+name+'_'+i))return false;
              for(const name of ['inferno_laser','rime_laser'])
                for(let i=0;i<12;i++)if(!XART.rdy('l23fx_'+name+'_'+i))return false;
              return true;
            }""", timeout=60_000)

            for case in CASES:
                page.evaluate(COMMON, case["stage"])
                page.evaluate(f"() => {{{case['spawn']}}}")
                capture = start_capture(page)
                for index, (ratio, repeats, wait_ms) in enumerate(case["steps"]):
                    for _ in range(repeats):
                        page.evaluate(f"""() => {{
                          const b={case['entity']};b.hp=b.maxhp*{ratio};b.fireCd=.01;b._sba=null;
                          if(b._s3boss){{b._s3boss.volley=null;b._s3boss.charge=null;}}
                          shipBossAttack(b);
                        }}""")
                        page.wait_for_timeout(wait_ms)
                    page.locator("#screen").screenshot(path=str(OUT / f"{case['slug']}_phase{index+1}.png"))
                webm = OUT / f"{case['slug']}.webm"
                gif = OUT / f"{case['slug']}.gif"
                contact = OUT / f"{case['slug']}_contact.png"
                stop_capture(page, webm); render_derivatives(webm, gif, contact)
                result = diagnostics(page, case["entity"])
                result.update({"case": case["label"], "capture": capture})
                assert all(fx in result["fx"] for fx in case["expected_fx"]), result
                assert case["expected_beam"] in result["beamFamilies"], result
                checks = [c for c in result["angleChecks"] if c["family"] == case["expected_beam"]]
                if case["beam_mode"] == "bounded45":
                    assert any(c["sweepRange"] > 1.40 and c["sweepRange"] <= 1.58 and c["maxSouthOffset"] <= .80 for c in checks), result
                else:
                    assert any(c["maxAngleDrift"] < 1e-9 for c in checks), result
                results.append(result)
                print(f"{case['label']}: fx={result['fx']} beams={result['beamFamilies']} locks={result['angleChecks']}")

            page.evaluate("() => {clearInterval(window.__l23Pilot);clearInterval(window.__l23Sampler);}")
            browser.close()
    finally:
        server.shutdown(); server.server_close()

    report = {"cases": results, "pageErrors": page_errors, "consoleErrors": console_errors, "assetsReady": 56}
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    if page_errors or console_errors:
        raise RuntimeError(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
