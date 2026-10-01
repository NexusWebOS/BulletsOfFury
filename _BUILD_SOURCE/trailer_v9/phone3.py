"""phone3.py - the trailer as ONE phone-sized file.

    python phone3.py trailer_v3.mp4 trailer_v3_phone.mp4 [--mb 29] [--size 960x540] [--ak 128]

Mike, on v2: "The trailer was supposed to be all one trailer." v2's phone copy came in two parts because the whole
thing at a watchable bitrate did not fit under the attachment limit. This makes one file: two-pass H.264 at the
video bitrate the size budget leaves after the audio, measured afterwards, and re-encoded lower if the container
overshot. The budget is DECIMAL megabytes so it holds whichever way the limit is counted.
"""
import os, re, sys, argparse, subprocess


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def duration(path):
    r = subprocess.run([ffmpeg(), '-hide_banner', '-i', path], capture_output=True, text=True)
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def encode(src, out, w, h, vk, ak):
    log = out + '.pass'
    base = [ffmpeg(), '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=%d:%d:flags=lanczos,fps=30' % (w, h),
            '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-b:v', '%dk' % vk,
            '-passlogfile', log]
    subprocess.check_call(base + ['-pass', '1', '-an', '-f', 'null', '-'])
    subprocess.check_call(base + ['-pass', '2', '-c:a', 'aac', '-b:a', '%dk' % ak, '-ar', '48000',
                                  '-movflags', '+faststart', out])
    for f in os.listdir(os.path.dirname(os.path.abspath(out))):
        if f.startswith(os.path.basename(log)):
            try:
                os.remove(os.path.join(os.path.dirname(os.path.abspath(out)), f))
            except OSError:
                pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--mb', type=float, default=29.0)
    ap.add_argument('--size', default='960x540')    # measured on v2's busiest bar: at ~1.3 Mbps 720p smears the ice and the dither, 540p holds them
    ap.add_argument('--ak', type=int, default=128)
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.split('x'))
    limit = int(a.mb * 1000 * 1000)
    dur = duration(a.src)
    vk = int(((limit * 8.0) / dur - a.ak * 1000) / 1000 * 0.96)
    for attempt in range(4):
        encode(a.src, a.out, w, h, vk, a.ak)
        size = os.path.getsize(a.out)
        print('attempt %d: %dx%d, video %d kbps + audio %d kbps over %.1fs -> %.2f MB (limit %.2f)'
              % (attempt + 1, w, h, vk, a.ak, dur, size / 1e6, limit / 1e6), flush=True)
        if size <= limit:
            return
        vk = int(vk * (limit / float(size)) * 0.97)
    sys.exit('could not fit %s under %.1f MB' % (a.out, a.mb))


if __name__ == '__main__':
    main()
