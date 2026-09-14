"""render_audio.py - turn a take's sound log into takes3/<id>/sfx.wav, frame-aligned to s00000.jpg.

    python render_audio.py S1_cole C_flame        # these takes
    python render_audio.py --all [--force]        # every finished take with an audio_events.json
    python render_audio.py W_warp --dir diag3 --exclude @synth --suffix _nosynth     # a diagnostic stem

Rendered in Chromium's OfflineAudioContext, through the GAME'S OWN sound code rather than an imitation:
  samples  every logged Snd.play at the volume Snd computes (vol x TAME.g x sfx-or-voice x master), through
           the same lowpass -> high shelf -> boost chain Snd._shape builds for a non-native TAME row, and
           through Snd's element POOL: at most max(3, variations) copies of one cue at once, a new shot
           cutting whichever copy last held its element
  loops    each held bed as a looping source whose gain follows the logged per-frame level, restarting
           from zero on the frames the game restarted it
  synth    the Audio module's source is lifted out of assets/game.js and evaluated a second time with its
           AudioContext pointed at the offline context. Every logged cue is replayed with currentTime AND
           performance.now() set to the frame it fired on, so the module's own throttles gate the replay
           exactly as they gated the game. Its oscillators call start() with no time, which means "now" to
           a live context and "zero" to an offline one - start() is pinned to the cue's time for that reason.
Output is 48 kHz stereo 32-bit float, so a busy take keeps its headroom until the mix decides levels.
--exclude takes cue names, plus @synth for the whole Audio-module replay (synth cues and the warp bed).
"""
import os, sys, json, struct, base64, argparse, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from capture3 import serve, ROOT, TAKES_DIR   # noqa: E402

SR = 48000
TAIL = 2.0

RENDER = r"""async ({ev, iife, tail, exclude}) => {
  const SR = 48000, rec0 = ev.rec0, frames = ev.frames;
  const dur = frames / 60 + tail;
  const off = new OfflineAudioContext(2, Math.ceil(dur * SR), SR);
  const T = (i) => (i - rec0) / 60;
  const tame = ev.tame || {}, vol = ev.vol || {master: 1, sfx: 0.42, voice: 0.85}, voice = ev.voice || {};
  const errs = [], counts = {snd: 0, cut: 0, loopSeg: 0, syn: 0, warp: 0, skipped: 0};
  const ex = new Set(exclude || []);

  /* Snd's own URI rule (_au): a manifest path is fetched as it is, anything else is base64 mp3. A BOFA.sfx
     entry may also be an ARRAY of authored variations, which the pool rotates through. */
  const au = (u) => (typeof u === 'string' && u.lastIndexOf('assets/', 0) === 0) ? u : ('data:audio/mpeg;base64,' + u);
  const bufs = {}, byUri = {};
  for (const n in (ev.files || {})) {
    const raw = ev.files[n]; if (raw == null) continue;
    bufs[n] = [];
    for (const u of (Array.isArray(raw) ? raw : [raw]).map(au)) {
      if (!(u in byUri)) {
        byUri[u] = null;
        try { const r = await fetch(u); const ab = await r.arrayBuffer(); byUri[u] = await off.decodeAudioData(ab); }
        catch (e) { errs.push('decode ' + n + ': ' + String(e).slice(0, 80)); }
      }
      bufs[n].push(byUri[u]);
    }
  }
  const chains = {};
  const dest = function(name){
    if (chains[name]) return chains[name];
    const cfg = tame[name];
    let node = off.destination;
    if (cfg && !cfg.native && cfg.lp) {
      const lp = off.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = cfg.lp; lp.Q.value = 0.7;
      const sh = off.createBiquadFilter(); sh.type = 'highshelf'; sh.frequency.value = 2600; sh.gain.value = -6;
      const g = off.createGain(); g.gain.value = cfg.boost || 1;
      lp.connect(sh); sh.connect(g); g.connect(off.destination);
      node = lp;
    }
    return (chains[name] = node);
  };
  const c01 = (x) => Math.max(0, Math.min(1, x || 0));

  /* ---- samples, through Snd's POOL ----
     A.play takes p.list[p.i] and sets currentTime=0 on it, so max(3, variations) elements means at most that
     many copies of one cue sound at once, and a new shot CUTS whichever copy last held that element. Stacking
     every logged play in full is not what the game does. */
  const pools = {};
  const cut = function(L, t){
    const tc = Math.max(L.t0, t);
    try {
      if (tc - 0.004 > L.t0) { L.g.gain.setValueAtTime(L.v, tc - 0.004); L.g.gain.linearRampToValueAtTime(0, tc); L.src.stop(tc + 0.001); }
      else L.src.stop(L.t0);
    } catch (e) {}
    counts.cut++;
  };
  for (const [i, name, v] of (ev.snd || [])) {
    if (ex.has(name)) continue;
    const list = bufs[name]; if (!list || !list.length) { counts.skipped++; continue; }
    const P = pools[name] || (pools[name] = {n: Math.max(3, list.length), i: 0, live: []});
    const slot = P.i; P.i = (P.i + 1) % P.n;
    const t = T(i);
    const prev = P.live[slot]; P.live[slot] = null;
    if (prev && prev.end > t) cut(prev, t);
    const b = list[slot % list.length]; if (!b) { counts.skipped++; continue; }
    if (t + b.duration < 0 || t > dur) continue;
    const cfg = tame[name], gm = cfg ? cfg.g : 1;
    const ch = voice[name] ? (vol.voice != null ? vol.voice : 1) : vol.sfx;
    const gv = c01(v * gm * ch * vol.master);
    const src = off.createBufferSource(); src.buffer = b;
    const g = off.createGain(); g.gain.value = gv;
    src.connect(g); g.connect(dest(name));
    if (t >= 0) src.start(t); else src.start(0, -t);
    P.live[slot] = {src: src, g: g, v: gv, t0: Math.max(0, t), end: t + b.duration};
    counts.snd++;
  }

  // ---- held beds ----
  for (const name in (ev.loops || {})) {
    if (ex.has(name)) continue;
    const b = (bufs[name] || [])[0]; if (!b) { counts.skipped++; continue; }
    const cfg = tame[name], gm = cfg ? cfg.g : 1;
    const rs = (ev.restarts || []).filter(r => r[1] === name).map(r => r[0]).sort((a, c) => a - c);
    const pts = ev.loops[name];
    let k = 0;
    while (k < pts.length) {
      let j = k;
      while (j + 1 < pts.length && pts[j + 1][0] === pts[j][0] + 1) j++;
      const seg = pts.slice(k, j + 1).filter(p => T(p[0]) >= 0);
      k = j + 1;
      if (!seg.length) continue;
      const t0 = T(seg[0][0]);
      let r0 = null; for (const r of rs) { if (r <= seg[0][0]) r0 = r; }
      const phase = r0 == null ? 0 : ((t0 - T(r0)) % b.duration + b.duration) % b.duration;
      const src = off.createBufferSource(); src.buffer = b; src.loop = true;
      const g = off.createGain(); g.gain.setValueAtTime(0, 0);
      for (const [fi, lv] of seg) g.gain.linearRampToValueAtTime(c01(lv * gm * vol.sfx * vol.master), T(fi));
      const tEnd = T(seg[seg.length - 1][0]) + 1 / 60;
      g.gain.linearRampToValueAtTime(0, tEnd + 0.03);
      src.connect(g); g.connect(dest(name));
      src.start(t0, phase); src.stop(tEnd + 0.06);
      counts.loopSeg++;
    }
  }

  // ---- synth cues, through a second copy of the game's own Audio module ----
  const evs = [].concat((ev.syn || []).map(e => ['s', e[0], e[1], e[2]]), (ev.warp || []).map(e => ['w', e[0], e[1], e[2]]))
                .sort((a, c) => a[1] - c[1]);
  if (evs.length && !ex.has('@synth')) {
    window.__tOff = 0; window.__synthOn = false;
    const _start = AudioScheduledSourceNode.prototype.start;
    AudioScheduledSourceNode.prototype.start = function(when, offset, duration){
      if (window.__synthOn && this.context === off) when = Math.max(when || 0, window.__tOff);
      if (duration !== undefined) return _start.call(this, when, offset, duration);
      if (offset !== undefined) return _start.call(this, when, offset);
      return _start.call(this, when);
    };
    const proxy = new Proxy(off, {get: function(t, p){
      if (p === 'currentTime') return window.__tOff;
      const v = Reflect.get(t, p);
      return (typeof v === 'function') ? v.bind(t) : v;
    }});
    const _AC = window.AudioContext, _WAC = window.webkitAudioContext;
    let OA = null;
    try {
      window.AudioContext = function(){ return proxy; };
      window.webkitAudioContext = window.AudioContext;
      OA = (new Function(iife + '\nreturn __OA_RET;'))();
      OA.init();
    } catch (e) { errs.push('module ' + String(e).slice(0, 160)); }
    window.AudioContext = _AC; window.webkitAudioContext = _WAC;
    const _pnow = performance.now;
    window.__synthOn = true;
    for (const [kind, i, name, args] of evs) {
      if (ex.has(name)) continue;
      const t = T(i); if (t < -0.5 || t > dur) continue;
      window.__tOff = Math.max(0, t);
      performance.now = function(){ return 1e6 + t * 1000; };
      try {
        if (kind === 's') { const fn = OA && OA.SFX[name]; if (fn) { fn.apply(OA.SFX, args || []); counts.syn++; } }
        else { const fn = OA && OA[name]; if (fn) { fn.apply(OA, args || []); counts.warp++; } }
      } catch (e) { if (errs.length < 12) errs.push(name + ': ' + String(e).slice(0, 100)); }
    }
    performance.now = _pnow;
    window.__synthOn = false;
    AudioScheduledSourceNode.prototype.start = _start;
  }

  const rb = await off.startRendering();
  const n = rb.length, L = rb.getChannelData(0), R = rb.getChannelData(1);
  const inter = new Float32Array(n * 2);
  let peak = 0, sq = 0;
  for (let q = 0; q < n; q++) {
    const l = L[q], r = R[q];
    inter[2 * q] = l; inter[2 * q + 1] = r;
    const a = Math.max(Math.abs(l), Math.abs(r)); if (a > peak) peak = a;
    sq += l * l + r * r;
  }
  const bytes = new Uint8Array(inter.buffer);
  let s = ''; const CH = 0x8000;
  for (let q = 0; q < bytes.length; q += CH) s += String.fromCharCode.apply(null, bytes.subarray(q, q + CH));
  return {b64: btoa(s), n: n, peak: peak, rms: Math.sqrt(sq / Math.max(1, 2 * n)), counts: counts, errs: errs};
}"""


def audio_module_source():
    src = open(os.path.join(ROOT, 'assets', 'game.js'), encoding='utf-8').read()
    a = src.index('const Audio = (()=>{')
    b = src.index('\n})();', a) + len('\n})();')
    body = src[a:b]
    assert body.startswith('const Audio = ')
    return 'var __OA_RET = ' + body[len('const Audio = '):]


def write_wav_float(path, raw, channels=2, sr=SR):
    data = raw
    hdr = b'RIFF' + struct.pack('<I', 4 + 26 + 8 + len(data)) + b'WAVE'
    hdr += b'fmt ' + struct.pack('<IHHIIHH', 18, 3, channels, sr, sr * channels * 4, channels * 4, 32) + struct.pack('<H', 0)
    hdr += b'data' + struct.pack('<I', len(data))
    with open(path, 'wb') as fh:
        fh.write(hdr)
        fh.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--dir', default=TAKES_DIR, help='the takes directory (default takes3)')
    ap.add_argument('--exclude', default='', help='comma-separated cue names to leave out; @synth drops the Audio-module replay')
    ap.add_argument('--suffix', default='', help='writes sfx<suffix>.wav, so a diagnostic stem never replaces the real one')
    a = ap.parse_args()
    tdir = os.path.abspath(a.dir)
    exclude = [s for s in a.exclude.split(',') if s]
    out_name = 'sfx%s.wav' % a.suffix
    ids = sorted(os.listdir(tdir)) if a.all else a.ids
    todo = []
    for tid in ids:
        d = os.path.join(tdir, tid)
        finished = os.path.exists(os.path.join(d, 'audio_events.json')) and os.path.exists(os.path.join(d, 'meta.json'))
        if finished and (a.force or not os.path.exists(os.path.join(d, out_name))):
            todo.append(tid)
    if not todo:
        print('nothing to render')
        return
    iife = audio_module_source()
    from playwright.sync_api import sync_playwright
    port, stop = serve()
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required', '--mute-audio'])
        page = None
        for k, tid in enumerate(todo):
            if page is None or k % 12 == 0:
                if page is not None:
                    page.close()
                page = b.new_page()
                page.goto('http://127.0.0.1:%d/index.html' % port)
                page.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
            ev = json.load(open(os.path.join(tdir, tid, 'audio_events.json')))
            if not ev.get('rec0') or not ev.get('frames'):
                print('%-14s no recorded frames' % tid)
                continue
            t0 = time.time()
            r = page.evaluate(RENDER, {'ev': ev, 'iife': iife, 'tail': TAIL, 'exclude': exclude})
            raw = base64.b64decode(r['b64'])
            write_wav_float(os.path.join(tdir, tid, out_name), raw)
            print('%-14s %5.1fs audio  peak %.3f rms %.4f  %s  %.1fs%s' % (
                tid, r['n'] / SR, r['peak'], r['rms'], r['counts'], time.time() - t0,
                ('  ERR ' + ' | '.join(r['errs'])) if r['errs'] else ''), flush=True)
        if page is not None:
            page.close()
        b.close()
    stop()


if __name__ == '__main__':
    main()
