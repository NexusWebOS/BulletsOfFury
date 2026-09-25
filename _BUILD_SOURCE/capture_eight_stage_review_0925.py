#!/usr/bin/env python3
"""Record in-engine field and boss samples for campaign stages 1-8.

Each segment is a fresh real Chromium stage. The boss is entered through the
engine's spawnBoss path after a short field sample; this is a review montage,
not a claim of eight unassisted full clears. Frames are streamed to ffmpeg so
the low-space workspace does not fill with hundreds of PNGs.
"""
import base64
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

OUT = os.path.join(ROOT, '_shots', 'eight_stage_review_0925')
FPS = 10
STEPS = 6

GRAB = """() => {
  const g=document.querySelector('#screen-area canvas')||document.querySelector('canvas');
  if(!g)return null;
  const h=document.querySelector('#hud'),e=document.querySelector('#equipcv');
  const hw=h?h.width:0,hh=h?h.height:0,ew=e?e.width:0,eh=e?e.height:0;
  const row=Math.max(hh,eh),w=Math.max(hw+ew,g.width),z=row+g.height;
  let c=window.__reviewCanvas;
  if(!c)c=window.__reviewCanvas=document.createElement('canvas');
  if(c.width!==w||c.height!==z){c.width=w;c.height=z;}
  const x=c.getContext('2d');x.fillStyle='#000';x.fillRect(0,0,w,z);
  if(h)x.drawImage(h,0,0);if(e)x.drawImage(e,hw,0);
  x.drawImage(g,0,row);return c.toDataURL('image/png');
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--extended', action='store_true',
                    help='Capture longer field and boss samples so late attacks become visible')
    args = ap.parse_args()
    suffix = '_extended' if args.extended else ''
    os.makedirs(OUT, exist_ok=True)
    target = os.path.join(OUT, f'BulletsOfFury_Stages1-8_Review_0925{suffix}.mp4')
    ff = subprocess.Popen([
        imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error',
        '-f', 'image2pipe', '-vcodec', 'png', '-framerate', str(FPS), '-i', '-',
        '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '25',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', target,
    ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    log = []
    count = 0
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            for stage in range(1, 9):
                page = browser.new_page(viewport={'width': 1100, 'height': 1200})
                errors = []
                page.on('pageerror', lambda e: errors.append('page: '+str(e)))
                page.on('console', lambda m: errors.append('console: '+m.text) if m.type == 'error' else None)
                page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
                page.wait_for_function("() => typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4", timeout=60000)
                page.evaluate(sh.TRAP_RAF)
                page.wait_for_timeout(50)
                setup = page.evaluate(sh.SETUP, {'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
                if not setup.get('ok'):
                    raise RuntimeError(f'stage {stage} setup: {setup}')
                page.evaluate("() => {diffKey='normal';DIFF=difficultyForRun(run.mode,'normal');"
                              "player.invuln=1e9;run.lives=9;}")
                # Allow XART families to decode over actual frames, then start
                # near the first authored field wave for a useful view.
                page.evaluate("() => {if(typeof warmStage==='function')warmStage(run.stage);}")
                for _ in range(3):
                    page.evaluate(sh.STEP, 12)
                    page.wait_for_timeout(120)
                page.evaluate("() => {stageTimer=10;mapScroll=Math.max(mapScroll,360);}")
                if args.extended and stage == 6:
                    # Stage 6 opens with a long scripted intercept and carrier flyover.
                    # The shorter cut already preserves that opening; this cut samples
                    # active field combat after it, through the ordinary wave director.
                    page.evaluate("() => {s6Opening=null;playerLocks=[];}")

                def capture(phase, frames):
                    nonlocal count
                    peak = 0
                    for j in range(frames):
                        err = page.evaluate(sh.STEP, STEPS)
                        if err: raise RuntimeError(f'stage {stage} {phase}: {err}')
                        if j % 8 == 0: page.wait_for_timeout(24)
                        data = page.evaluate(GRAB)
                        if not data: raise RuntimeError(f'stage {stage}: no canvas')
                        raw = base64.b64decode(data.split(',',1)[1])
                        ff.stdin.write(raw)
                        if j == min(4, frames-1):
                            with open(os.path.join(OUT, f'stage{stage}_{phase}{suffix}.png'),'wb') as f:
                                f.write(raw)
                        count += 1
                        peak = max(peak, page.evaluate("() => eBullets.length"))
                    return peak

                field_frames = (80 if stage == 6 else 42) if args.extended else 21
                boss_frames = (160 if stage in (5, 7, 8) else 120) if args.extended else 39
                field_peak = capture('field', field_frames)
                page.evaluate("() => {enemies.length=0;eBullets.length=0;"
                              "subBoss=null;subBossActive=false;subBossDone=true;"
                              "stageTimer=curStage.length;spawnBoss(curStage.boss);}")
                boss_kind = page.evaluate("() => boss&&boss.kind")
                boss_peak = capture('boss', boss_frames)
                details = page.evaluate("() => ({state,stage:run.stage,bossActive,"
                                        "bossHp:boss&&boss.hp,bossParts:boss&&boss.parts&&boss.parts.length,"
                                        "enemies:enemies.length})")
                entry = {'stage':stage,'boss':boss_kind,'fieldFrames':field_frames,
                         'bossFrames':boss_frames,'fieldPeakBullets':field_peak,
                         'bossPeakBullets':boss_peak,'details':details,'errors':errors[:10]}
                log.append(entry)
                print(json.dumps(entry), flush=True)
                page.close()
            browser.close()
    finally:
        stop()
        ff.stdin.close()
        stderr = ff.stderr.read().decode(errors='replace')
        code = ff.wait()
        if code:
            raise RuntimeError(f'ffmpeg exit {code}: {stderr[-1000:]}')
        with open(os.path.join(OUT,f'review_log{suffix}.json'),'w',encoding='utf-8') as f:
            json.dump(log,f,indent=2)
        print(f'Encoded {count} real Chromium frames to {target}',flush=True)


if __name__ == '__main__':
    main()
