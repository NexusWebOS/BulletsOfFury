"""verify9.py - check a finished trailer file: full decode, frame count, durations, and stills at the named beats.

    python verify9.py BulletsOfFury_Trailer_v9.mp4 edl9.json stills.jpg
"""
import os, sys, json, re, subprocess
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def ff():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def main():
    mp4, edl_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    E = json.load(open(edl_path))
    want = max(int(round(c['t1'] * 60)) for c in E['clips'])
    r = subprocess.run([ff(), '-v', 'error', '-i', mp4, '-map', '0:v:0', '-f', 'null', '-'], capture_output=True, text=True)
    print('video decode errors:', repr(r.stderr.strip())[:300] or 'none')
    r = subprocess.run([ff(), '-v', 'error', '-i', mp4, '-map', '0:a:0', '-f', 'null', '-'], capture_output=True, text=True)
    print('audio decode errors:', repr(r.stderr.strip())[:300] or 'none')
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                        'stream=nb_read_frames,width,height,r_frame_rate', '-of', 'json', mp4], capture_output=True, text=True)
    v = json.loads(r.stdout)['streams'][0]
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_name,duration,sample_rate,channels',
                        '-of', 'json', mp4], capture_output=True, text=True)
    info = json.loads(r.stdout)
    print('video: %sx%s @ %s, %s frames (EDL wants %d)' % (v['width'], v['height'], v['r_frame_rate'], v['nb_read_frames'], want))
    for s in info['streams']:
        print('stream %s: duration %s %s' % (s.get('codec_name'), s.get('duration'), ('%s Hz x%s' % (s.get('sample_rate'), s.get('channels'))) if s.get('sample_rate') else ''))
    print('file: %.1f MB, %.2f s' % (int(info['format']['size']) / 1e6, float(info['format']['duration'])))
    # stills: one per labelled clip start (+0.4 s), in a grid
    picks = []
    for c in E['clips']:
        t = min(c['t1'] - 0.05, c['t0'] + 0.4)
        picks.append((t, c.get('label', '')[:34]))
    tw, th, cols = 320, 180, 6
    rows = (len(picks) + cols - 1) // cols
    S = Image.new('RGB', (tw * cols, (th + 14) * rows), (8, 8, 10))
    d = ImageDraw.Draw(S)
    tmp = os.path.join(HERE, '_verify_still.jpg')
    for k, (t, lab) in enumerate(picks):
        subprocess.run([ff(), '-v', 'error', '-y', '-ss', '%.3f' % t, '-i', mp4, '-frames:v', '1', '-q:v', '3', tmp], check=True)
        im = Image.open(tmp).convert('RGB').resize((tw, th), Image.BILINEAR)
        x, y = (k % cols) * tw, (k // cols) * (th + 14)
        S.paste(im, (x, y + 14))
        d.text((x + 2, y + 1), '%.1f %s' % (t, lab), fill=(255, 220, 140))
    os.remove(tmp)
    S.save(out, quality=86)
    print('wrote', out, len(picks), 'stills')


if __name__ == '__main__':
    main()
