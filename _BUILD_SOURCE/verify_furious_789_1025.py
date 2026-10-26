"""Decode each delivered boss MP4, measure audio, and make inspection contact sheets."""
from pathlib import Path
import argparse
import json
import re
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots' / 'furious_789_1025'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def verify(stage):
    candidates = [p for p in OUT.glob(f'stage{stage}*/stage{stage}-furious.mp4')
                  if (p.parent / 'report.json').exists()]
    if not candidates:
        raise RuntimeError(f'No completed video file for Stage {stage}')
    video = max(candidates, key=lambda p: p.stat().st_mtime)
    report = json.loads((video.parent / 'report.json').read_text(encoding='utf8'))
    decoded = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-threads', '2', '-i', str(video),
                              '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
    (video.parent / 'decode.log').write_text(decoded.stderr, encoding='utf8')
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', decoded.stderr)
    seconds = int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3]) if duration else 0
    peak = re.search(r'max_volume: ([\-\d.inf]+) dB', decoded.stderr)
    mean = re.search(r'mean_volume: ([\-\d.inf]+) dB', decoded.stderr)
    audio = float(peak[1]) if peak else float('-inf')
    errors = [line for line in decoded.stderr.splitlines()
              if re.search(r'(error while|invalid data|corrupt|decode error)', line, re.I)]
    frames = []
    for index, at in enumerate([min(16, seconds * .08), seconds * .25, seconds * .45,
                                seconds * .65, seconds * .82, max(0, seconds - 4)]):
        path = video.parent / f'decoded-{index:02}.png'
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-threads', '2', '-ss', str(at), '-i', str(video),
                        '-frames:v', '1', str(path)], check=True)
        frames.append((at, path))
    sheet = Image.new('RGB', (1280, 1260), '#0a0e15')
    draw = ImageDraw.Draw(sheet)
    for index, (at, path) in enumerate(frames):
        with Image.open(path) as frame:
            frame.thumbnail((640, 400))
            x, y = (index % 2) * 640, (index // 2) * 420
            sheet.paste(frame, (x, y))
            draw.text((x + 10, y + 402), f'Stage {stage} / {int(at//60):02}:{int(at%60):02}', fill='#f4d380')
    contact = video.parent / 'decoded-contact.jpg'
    sheet.save(contact, quality=90)
    checks = dict(fullDecode=decoded.returncode == 0 and not errors,
                  audioStream='Audio: aac' in decoded.stderr,
                  audibleDecodedAudio=audio > -60,
                  durationMatches=abs(seconds - report['timeline'][-1]['seconds']) < 3,
                  noPageErrors=not report.get('pageErrors'),
                  noConsoleErrors=not report.get('consoleErrors'),
                  noAssetErrors=not report.get('assetErrors'),
                  nativeDefeat=report.get('completed', False),
                  zeroPlayerDeaths=report.get('audio', {}).get('deaths', 0) == 0)
    result = dict(stage=stage, video=str(video), duration=round(seconds, 3),
                  sizeBytes=video.stat().st_size, decodedPeakDb=audio,
                  decodedMeanDb=float(mean[1]) if mean else None,
                  checks=checks, decodeErrors=errors, contactSheet=str(contact))
    (video.parent / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', default='7,8,9')
    parser.add_argument('--out', help='Recording folder inside this workspace')
    args = parser.parse_args()
    if args.out:
        OUT=(ROOT/args.out).resolve()
        if not OUT.is_relative_to(ROOT):raise ValueError('Verification output must stay in workspace')
    for value in args.stages.split(','):
        verify(int(value))
