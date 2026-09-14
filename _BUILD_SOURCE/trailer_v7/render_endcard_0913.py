"""Render the approved end-card change through the existing trailer compositor.

Pass --scratch to the original trailer workspace containing brand/ and takes3/.
Only the requested frame range is encoded; the original trailer supplies the
unchanged prefix and audio during assembly.
"""
import argparse
import json
from pathlib import Path
import subprocess

import compose
from PIL import Image
import typeset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--start-frame', type=int, default=9566)
    parser.add_argument('--preview-only', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    compose.HERE = str(args.scratch.resolve())
    edl_path = Path(__file__).with_name('edl3.json')
    edl = compose.load_edl(edl_path)
    card = next(c for c in edl['clips'] if c.get('label') == 'END CARD')
    credit = next(l for l in card['layers'] if l.get('text', '').startswith('BUILT WITH'))
    expected = 'BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS.'
    if credit['text'] != expected:
        raise ValueError('The EDL must contain the approved credit verbatim.')
    glyph = typeset.text(expected, face=credit['face'], height=credit['height'])
    rendered = compose.Assets().image(credit)
    if rendered.width > compose.W - 160:
        raise ValueError('Credit extends into the outer 80-pixel safe margins.')
    preview_frame = round(162.5 * compose.FPS)
    preview = compose.render_frame(edl, preview_frame, compose.Takes(), compose.Assets())
    Image.fromarray(preview).save(args.out / 'endcard_v8.png')
    report = {
        'credit': credit['text'], 'glyph_dimensions': list(glyph.size),
        'layer_dimensions_with_shadow': list(rendered.size),
        'preview_frame': preview_frame, 'start_frame': args.start_frame,
        'end_frame': edl['_frames'], 'fps': compose.FPS,
        'dimensions': [compose.W, compose.H],
    }
    if not args.preview_only:
        tail_path = args.out / 'endcard_tail_v8.mp4'
        command = [compose.ffmpeg_exe(), '-y', '-loglevel', 'error',
                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080',
                   '-r', '60', '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                   '-crf', '18', '-pix_fmt', 'yuv420p', '-threads', '3',
                   '-x264-params', 'keyint=120:min-keyint=1', str(tail_path)]
        takes, assets = compose.Takes(), compose.Assets()
        with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
            try:
                for frame in range(args.start_frame, edl['_frames']):
                    encoder.stdin.write(compose.render_frame(edl, frame, takes, assets).tobytes())
            finally:
                encoder.stdin.close()
            if encoder.wait() != 0:
                raise RuntimeError('End-card encoder failed.')
        report['tail_file'] = str(tail_path)
    (args.out / 'endcard_render_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
