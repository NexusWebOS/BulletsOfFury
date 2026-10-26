"""Timestamped visual review frames from the preserved native boss recordings."""
from pathlib import Path
import argparse
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/furious_789_1025/analysis'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def source(stage):
    data = json.loads((OUT.parent / 'delivery.json').read_text())
    return Path(next(c['video'] for c in data['clips'] if c['stage'] == stage))


def overview(stage, step=2):
    dest = OUT / f'stage{stage}'
    dest.mkdir(parents=True, exist_ok=True)
    duration = json.loads((source(stage).parent / 'verification.json').read_text())['duration']
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-threads', '2', '-i', str(source(stage)),
                    '-vf', f'fps=1/{step},scale=320:200', str(dest / 'sample-%04d.png')], check=True)
    frames = sorted(dest.glob('sample-*.png'))
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 17)
    for group in range(math.ceil(len(frames) / 16)):
        canvas = Image.new('RGB', (1280, 904), '#070b13')
        draw = ImageDraw.Draw(canvas)
        for j, path in enumerate(frames[group * 16:(group + 1) * 16]):
            index = group * 16 + j
            t = min(duration, (index + .5) * step)
            x, y = j % 4 * 320, j // 4 * 226
            with Image.open(path) as frame:
                canvas.paste(frame, (x, y))
            draw.text((x + 6, y + 202), f'S{stage}  {int(t//60):02}:{int(t%60):02}', fill='#ebcb78', font=font)
        canvas.save(dest / f'overview-{group:02}.jpg', quality=92)
    print(json.dumps({'stage': stage, 'samples': len(frames), 'step': step, 'sheets': math.ceil(len(frames)/16)}), flush=True)


def sequence(stage, start, span, count=12, label='detail', crop=None):
    dest = OUT / f'stage{stage}'
    dest.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(count):
        t = start + span * i / max(1, count - 1)
        frame = dest / f'{label}-{i:02}.png'
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-threads', '2', '-ss', str(t),
                        '-i', str(source(stage)), '-frames:v', '1', str(frame)], check=True)
        frames.append((t, frame))
    width, height = (640, 400) if crop is None else (crop[2] - crop[0], crop[3] - crop[1])
    scale = min(1, 600 / width)
    tw, th = int(width * scale), int(height * scale)
    canvas = Image.new('RGB', (tw * 3, (th + 28) * math.ceil(count / 3)), '#070b13')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 17)
    for i, (t, path) in enumerate(frames):
        with Image.open(path) as image:
            if crop is not None:
                image = image.crop(crop)
            image = image.resize((tw, th))
            x, y = i % 3 * tw, i // 3 * (th + 28)
            canvas.paste(image, (x, y))
            draw.text((x + 6, y + th + 3), f'S{stage}  {int(t//60):02}:{t%60:05.2f}', fill='#ebcb78', font=font)
    path = dest / f'{label}-sequence.jpg'
    canvas.save(path, quality=94)
    print(str(path), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', default='7,8,9')
    parser.add_argument('--step', type=float, default=2)
    parser.add_argument('--start', type=float)
    parser.add_argument('--span', type=float, default=3)
    parser.add_argument('--count', type=int, default=12)
    parser.add_argument('--label', default='detail')
    parser.add_argument('--crop')
    args = parser.parse_args()
    for stage in map(int, args.stages.split(',')):
        if args.start is None:
            overview(stage, args.step)
        else:
            sequence(stage, args.start, args.span, args.count, args.label,
                     tuple(map(int, args.crop.split(','))) if args.crop else None)
