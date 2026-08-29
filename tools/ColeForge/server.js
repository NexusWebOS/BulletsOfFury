/*
 * ColeForge - local video forge
 * Zero-dependency Node HTTP server that drives yt-dlp.
 * Binds to loopback only. Nothing leaves this machine except the yt-dlp fetch itself.
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn, spawnSync, execFile } = require('child_process');
const { randomUUID } = require('crypto');

const PORT = Number(process.env.COLEFORGE_PORT || 8420);
const HOST = '127.0.0.1';
const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, 'public');
const CONFIG_PATH = path.join(ROOT, 'coleforge.config.json');

const DEFAULT_CONFIG = {
  outputDir: path.join(ROOT, 'downloads'),
  concurrency: 2,
};

let config = { ...DEFAULT_CONFIG };
try {
  if (fs.existsSync(CONFIG_PATH)) {
    Object.assign(config, JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')));
  }
} catch (err) {
  console.warn('[coleforge] config unreadable, using defaults:', err.message);
}
fs.mkdirSync(config.outputDir, { recursive: true });

/* ------------------------------------------------------------------ *
 * Tool discovery
 * ------------------------------------------------------------------ */

function probeCommand(cmd, args) {
  try {
    const r = spawnSync(cmd, args, { encoding: 'utf8', windowsHide: true, timeout: 20000 });
    if (r.status === 0) return String(r.stdout || '').trim();
  } catch (_) { /* not available */ }
  return null;
}

function resolveYtDlp() {
  const direct = probeCommand('yt-dlp', ['--version']);
  if (direct) return { cmd: 'yt-dlp', pre: [], version: direct };

  for (const py of ['python', 'py', 'python3']) {
    const v = probeCommand(py, ['-m', 'yt_dlp', '--version']);
    if (v) return { cmd: py, pre: ['-m', 'yt_dlp'], version: v };
  }
  return null;
}

/**
 * yt-dlp's --ffmpeg-location wants a real path, not a bare command name,
 * so walk PATH ourselves rather than trusting that "ffmpeg" resolves.
 */
function resolveFfmpeg() {
  const names = process.platform === 'win32' ? ['ffmpeg.exe'] : ['ffmpeg'];
  for (const raw of (process.env.PATH || '').split(path.delimiter)) {
    const dir = raw.trim().replace(/^"|"$/g, '');
    if (!dir) continue;
    for (const name of names) {
      const full = path.join(dir, name);
      try { if (fs.statSync(full).isFile()) return full; } catch (_) { /* keep looking */ }
    }
  }
  return null;
}

const YTDLP = resolveYtDlp();
const FFMPEG = resolveFfmpeg();

/* ------------------------------------------------------------------ *
 * Job registry
 * ------------------------------------------------------------------ */

/** @type {Map<string, Job>} */
const jobs = new Map();
/** @type {string[]} ids waiting for a worker slot */
const queue = [];
let active = 0;

function makeJob(url, opts) {
  const job = {
    id: randomUUID().slice(0, 8),
    url,
    opts,
    title: opts.title || url,
    thumb: opts.thumb || null,
    duration: opts.duration || null,
    status: 'queued',      // queued | running | done | failed | cancelled
    stage: 'WAITING',      // WAITING | VIDEO | AUDIO | MERGING | ...
    percent: 0,
    speed: null,
    eta: null,
    downloaded: 0,
    total: 0,
    files: [],
    error: null,
    log: [],
    proc: null,
    subscribers: new Set(),
    createdAt: Date.now(),
    finishedAt: null,
  };
  jobs.set(job.id, job);
  return job;
}

function publicJob(job) {
  const { proc, subscribers, log, ...rest } = job;
  return rest;
}

function emit(job, event) {
  const payload = `data: ${JSON.stringify(event)}\n\n`;
  for (const res of job.subscribers) {
    try { res.write(payload); } catch (_) { /* client vanished */ }
  }
}

function pushLog(job, line) {
  if (!line) return;
  job.log.push(line);
  if (job.log.length > 500) job.log.shift();
  emit(job, { type: 'log', line });
}

function setStatus(job, status, extra) {
  job.status = status;
  if (extra) Object.assign(job, extra);
  emit(job, { type: 'status', job: publicJob(job) });
}

/* ------------------------------------------------------------------ *
 * yt-dlp argument construction
 * ------------------------------------------------------------------ */

const FORMAT_MAP = {
  best:   { sel: 'bv*+ba/b', container: 'mp4', kind: 'video' },
  '2160': { sel: 'bv*[height<=2160]+ba/b[height<=2160]', container: 'mp4', kind: 'video' },
  '1440': { sel: 'bv*[height<=1440]+ba/b[height<=1440]', container: 'mp4', kind: 'video' },
  '1080': { sel: 'bv*[height<=1080]+ba/b[height<=1080]', container: 'mp4', kind: 'video' },
  '720':  { sel: 'bv*[height<=720]+ba/b[height<=720]',   container: 'mp4', kind: 'video' },
  '480':  { sel: 'bv*[height<=480]+ba/b[height<=480]',   container: 'mp4', kind: 'video' },
  mp3:    { audioFormat: 'mp3', kind: 'audio' },
  m4a:    { audioFormat: 'm4a', kind: 'audio' },
  wav:    { audioFormat: 'wav', kind: 'audio' },
};

const PROGRESS_TPL =
  'download:@@P@@%(progress.status)s@@%(progress.downloaded_bytes)s@@' +
  '%(progress.total_bytes)s@@%(progress.total_bytes_estimate)s@@' +
  '%(progress.speed)s@@%(progress.eta)s@@%(info.vcodec)s@@%(info.acodec)s';

const POST_TPL = 'postprocess:@@Q@@%(progress.status)s@@%(progress.postprocessor)s';

function buildArgs(job) {
  const o = job.opts;
  const preset = FORMAT_MAP[o.format] || FORMAT_MAP.best;
  const args = [...YTDLP.pre];

  args.push('--newline', '--no-colors', '--ignore-config');
  args.push('--concurrent-fragments', '4');
  args.push('--retries', '5', '--fragment-retries', '10');
  args.push('--progress-template', PROGRESS_TPL);
  args.push('--progress-template', POST_TPL);
  args.push('--print', 'after_move:@@F@@%(filepath)s');
  args.push('--no-simulate');
  args.push('--trim-filenames', '140');
  args.push('-P', config.outputDir);
  args.push('-o', '%(title)s [%(id)s].%(ext)s');

  if (FFMPEG) args.push('--ffmpeg-location', FFMPEG);
  args.push(o.playlist ? '--yes-playlist' : '--no-playlist');

  if (preset.kind === 'audio') {
    args.push('-x', '--audio-format', preset.audioFormat, '--audio-quality', '0');
    args.push('--embed-metadata');
    if (preset.audioFormat !== 'wav') args.push('--embed-thumbnail');
  } else {
    args.push('-f', preset.sel);
    args.push('--merge-output-format', preset.container);
    args.push('--embed-metadata');
    if (o.subtitles) args.push('--write-subs', '--write-auto-subs', '--sub-langs', 'en.*', '--embed-subs');
    if (o.thumbnailFile) args.push('--write-thumbnail');
  }

  // `--` guarantees a URL starting with `-` is never parsed as a flag.
  args.push('--', job.url);
  return args;
}

/* ------------------------------------------------------------------ *
 * Runner
 * ------------------------------------------------------------------ */

function num(v) {
  if (v === undefined || v === null) return null;
  const s = String(v).trim();
  if (!s || s === 'NA' || s === 'None') return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

function handleProgressLine(job, line) {
  if (line.startsWith('@@P@@')) {
    const [, status, dl, total, est, speed, eta, vcodec, acodec] = line.split('@@');
    const downloaded = num(dl) || 0;
    const size = num(total) || num(est) || 0;

    if (vcodec && vcodec !== 'none' && vcodec !== 'NA') job.stage = 'VIDEO';
    else if (acodec && acodec !== 'none' && acodec !== 'NA') job.stage = 'AUDIO';

    job.downloaded = downloaded;
    job.total = size;
    job.speed = num(speed);
    job.eta = num(eta);
    job.percent = size > 0 ? Math.min(100, (downloaded / size) * 100) : job.percent;

    if (status === 'finished') job.percent = 100;
    emit(job, { type: 'progress', job: publicJob(job) });
    return true;
  }

  if (line.startsWith('@@Q@@')) {
    const [, status, pp] = line.split('@@');
    if (status === 'started') {
      job.stage = /Merger/i.test(pp) ? 'MERGING'
        : /ExtractAudio/i.test(pp) ? 'EXTRACTING'
        : /Embed/i.test(pp) ? 'EMBEDDING'
        : 'FINISHING';
      emit(job, { type: 'progress', job: publicJob(job) });
    }
    return true;
  }

  if (line.startsWith('@@F@@')) {
    const file = line.slice(5).trim();
    if (file && !job.files.includes(file)) {
      job.files.push(file);
      emit(job, { type: 'file', file, job: publicJob(job) });
    }
    return true;
  }

  return false;
}

function startJob(job) {
  const args = buildArgs(job);
  active++;
  setStatus(job, 'running', { stage: 'SUMMONING', percent: 0 });
  pushLog(job, `$ ${YTDLP.cmd} ${args.join(' ')}`);

  const proc = spawn(YTDLP.cmd, args, { windowsHide: true });
  job.proc = proc;

  let outBuf = '';
  let errBuf = '';

  const consume = (chunk, isErr) => {
    const buf = (isErr ? errBuf : outBuf) + chunk.toString();
    const lines = buf.split(/\r?\n/);
    const tail = lines.pop();
    if (isErr) errBuf = tail; else outBuf = tail;

    for (const raw of lines) {
      const line = raw.replace(/\r/g, '').trim();
      if (!line) continue;
      if (handleProgressLine(job, line)) continue;
      pushLog(job, line);
      if (isErr && /^ERROR:/i.test(line)) job.error = line.replace(/^ERROR:\s*/i, '');
    }
  };

  proc.stdout.on('data', (c) => consume(c, false));
  proc.stderr.on('data', (c) => consume(c, true));

  proc.on('error', (err) => {
    job.error = err.message;
  });

  proc.on('close', (code) => {
    active = Math.max(0, active - 1);
    job.proc = null;
    job.finishedAt = Date.now();

    if (job.status === 'cancelled') {
      setStatus(job, 'cancelled', { stage: 'CANCELLED' });
    } else if (code === 0) {
      setStatus(job, 'done', { stage: 'COMPLETE', percent: 100, speed: null, eta: 0 });
    } else {
      setStatus(job, 'failed', {
        stage: 'FAILED',
        error: job.error || `yt-dlp exited with code ${code}`,
      });
    }
    emit(job, { type: 'end', job: publicJob(job) });
    pump();
  });
}

function pump() {
  while (active < config.concurrency && queue.length) {
    const id = queue.shift();
    const job = jobs.get(id);
    if (job && job.status === 'queued') startJob(job);
  }
}

function enqueue(url, opts) {
  const job = makeJob(url, opts);
  queue.push(job.id);
  pump();
  return job;
}

function cancelJob(job) {
  if (job.status === 'queued') {
    const i = queue.indexOf(job.id);
    if (i >= 0) queue.splice(i, 1);
    setStatus(job, 'cancelled', { stage: 'CANCELLED' });
    emit(job, { type: 'end', job: publicJob(job) });
    return true;
  }
  if (job.status === 'running' && job.proc) {
    job.status = 'cancelled';
    const pid = job.proc.pid;
    if (process.platform === 'win32') {
      // yt-dlp spawns ffmpeg; kill the whole tree or the merge keeps running.
      execFile('taskkill', ['/pid', String(pid), '/T', '/F'], () => {});
    } else {
      try { process.kill(-pid, 'SIGKILL'); } catch (_) { job.proc.kill('SIGKILL'); }
    }
    return true;
  }
  return false;
}

/* ------------------------------------------------------------------ *
 * Probe (metadata lookup)
 * ------------------------------------------------------------------ */

function probeUrl(url, playlist) {
  return new Promise((resolve, reject) => {
    const args = [
      ...YTDLP.pre,
      '--ignore-config', '--no-colors', '--no-warnings',
      '--dump-single-json',
      playlist ? '--yes-playlist' : '--no-playlist',
    ];
    if (playlist) args.push('--flat-playlist');
    args.push('--', url);

    const proc = spawn(YTDLP.cmd, args, { windowsHide: true });
    let out = '';
    let err = '';
    let killed = false;

    const timer = setTimeout(() => { killed = true; proc.kill(); }, 90000);

    proc.stdout.on('data', (c) => {
      out += c;
      if (out.length > 64 * 1024 * 1024) { killed = true; proc.kill(); }
    });
    proc.stderr.on('data', (c) => { err += c; });
    proc.on('error', (e) => { clearTimeout(timer); reject(e); });
    proc.on('close', (code) => {
      clearTimeout(timer);
      if (killed) return reject(new Error('Probe timed out.'));
      if (code !== 0) {
        const msg = (err.split(/\r?\n/).find((l) => /^ERROR:/i.test(l)) || err || 'yt-dlp could not read that URL.')
          .replace(/^ERROR:\s*/i, '').trim();
        return reject(new Error(msg));
      }
      try {
        resolve(JSON.parse(out));
      } catch (e) {
        reject(new Error('Could not parse yt-dlp output.'));
      }
    });
  });
}

function summarize(info) {
  const isPlaylist = info._type === 'playlist' || Array.isArray(info.entries);

  if (isPlaylist) {
    const entries = (info.entries || []).filter(Boolean).map((e) => ({
      id: e.id,
      title: e.title || '(untitled)',
      duration: e.duration || null,
      url: e.url || e.webpage_url || (e.id ? `https://www.youtube.com/watch?v=${e.id}` : null),
      thumb: pickThumb(e),
    }));
    return {
      type: 'playlist',
      title: info.title || 'Playlist',
      uploader: info.uploader || info.channel || null,
      count: entries.length,
      thumb: entries.find((e) => e.thumb)?.thumb || null,
      entries,
    };
  }

  const heights = [...new Set(
    (info.formats || [])
      .map((f) => f.height)
      .filter((h) => typeof h === 'number' && h > 0)
  )].sort((a, b) => b - a);

  return {
    type: 'video',
    id: info.id,
    title: info.title || '(untitled)',
    uploader: info.uploader || info.channel || null,
    duration: info.duration || null,
    thumb: pickThumb(info),
    viewCount: info.view_count || null,
    uploadDate: info.upload_date || null,
    heights,
    webpageUrl: info.webpage_url || null,
  };
}

function pickThumb(info) {
  if (info.thumbnail) return info.thumbnail;
  const t = info.thumbnails;
  if (Array.isArray(t) && t.length) return t[t.length - 1].url || null;
  return null;
}

/* ------------------------------------------------------------------ *
 * HTTP plumbing
 * ------------------------------------------------------------------ */

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};

function sendJson(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store',
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (c) => {
      data += c;
      if (data.length > 1e6) { reject(new Error('Body too large')); req.destroy(); }
    });
    req.on('end', () => {
      if (!data) return resolve({});
      try { resolve(JSON.parse(data)); } catch (e) { reject(new Error('Invalid JSON body')); }
    });
    req.on('error', reject);
  });
}

function validUrl(u) {
  if (typeof u !== 'string') return null;
  const s = u.trim();
  if (!/^https?:\/\/\S+$/i.test(s)) return null;
  if (/\s/.test(s)) return null;
  return s;
}

function serveStatic(req, res, urlPath) {
  const rel = urlPath === '/' ? 'index.html' : decodeURIComponent(urlPath).replace(/^\/+/, '');
  const full = path.join(PUBLIC_DIR, rel);
  if (!full.startsWith(PUBLIC_DIR)) { res.writeHead(403).end('Forbidden'); return; }

  fs.readFile(full, (err, data) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain' }).end('Not found'); return; }
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(full).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    res.end(data);
  });
}

function serveVault(res, name) {
  const full = path.join(config.outputDir, path.basename(name));
  if (!full.startsWith(config.outputDir)) { res.writeHead(403).end('Forbidden'); return; }
  fs.stat(full, (err, st) => {
    if (err || !st.isFile()) { res.writeHead(404).end('Not found'); return; }
    res.writeHead(200, {
      'Content-Type': 'application/octet-stream',
      'Content-Length': st.size,
      'Content-Disposition': `attachment; filename="${encodeURIComponent(path.basename(full))}"`,
    });
    fs.createReadStream(full).pipe(res);
  });
}

function listVault() {
  let names = [];
  try { names = fs.readdirSync(config.outputDir); } catch (_) { return []; }
  return names
    .filter((n) => !n.endsWith('.part') && !n.endsWith('.ytdl'))
    .map((n) => {
      const full = path.join(config.outputDir, n);
      try {
        const st = fs.statSync(full);
        if (!st.isFile()) return null;
        return { name: n, size: st.size, mtime: st.mtimeMs };
      } catch (_) { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, 100);
}

const server = http.createServer(async (req, res) => {
  const { pathname, searchParams } = new URL(req.url, `http://${HOST}:${PORT}`);

  try {
    if (req.method === 'GET' && pathname === '/api/health') {
      return sendJson(res, 200, {
        ok: !!YTDLP,
        ytdlp: YTDLP ? YTDLP.version : null,
        ffmpeg: !!FFMPEG,
        outputDir: config.outputDir,
        platform: os.platform(),
      });
    }

    if (!YTDLP && pathname.startsWith('/api/')) {
      return sendJson(res, 503, { error: 'yt-dlp is not installed. Run: python -m pip install -U yt-dlp' });
    }

    if (req.method === 'POST' && pathname === '/api/probe') {
      const body = await readBody(req);
      const url = validUrl(body.url);
      if (!url) return sendJson(res, 400, { error: 'That does not look like a http(s) link.' });
      try {
        const info = await probeUrl(url, !!body.playlist);
        return sendJson(res, 200, summarize(info));
      } catch (e) {
        return sendJson(res, 502, { error: e.message });
      }
    }

    if (req.method === 'POST' && pathname === '/api/forge') {
      const body = await readBody(req);
      const items = Array.isArray(body.items) ? body.items : [{ url: body.url }];
      const created = [];
      for (const item of items) {
        const url = validUrl(item.url);
        if (!url) continue;
        created.push(publicJob(enqueue(url, {
          format: typeof body.format === 'string' ? body.format : 'best',
          playlist: !!body.playlist,
          subtitles: !!body.subtitles,
          title: item.title,
          thumb: item.thumb,
          duration: item.duration,
        })));
      }
      if (!created.length) return sendJson(res, 400, { error: 'No valid links to forge.' });
      return sendJson(res, 200, { jobs: created });
    }

    if (req.method === 'GET' && pathname === '/api/jobs') {
      return sendJson(res, 200, { jobs: [...jobs.values()].map(publicJob) });
    }

    if (req.method === 'POST' && pathname === '/api/cancel') {
      const body = await readBody(req);
      const job = jobs.get(body.id);
      if (!job) return sendJson(res, 404, { error: 'No such job.' });
      return sendJson(res, 200, { cancelled: cancelJob(job) });
    }

    if (req.method === 'POST' && pathname === '/api/clear') {
      for (const [id, job] of jobs) {
        if (['done', 'failed', 'cancelled'].includes(job.status)) jobs.delete(id);
      }
      return sendJson(res, 200, { ok: true });
    }

    if (req.method === 'GET' && pathname === '/api/events') {
      const job = jobs.get(searchParams.get('id'));
      if (!job) { res.writeHead(404).end(); return; }
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive',
        'X-Accel-Buffering': 'no',
      });
      res.write(`data: ${JSON.stringify({ type: 'status', job: publicJob(job) })}\n\n`);
      job.subscribers.add(res);
      const ping = setInterval(() => { try { res.write(': ping\n\n'); } catch (_) {} }, 15000);
      req.on('close', () => { clearInterval(ping); job.subscribers.delete(res); });
      return;
    }

    if (req.method === 'GET' && pathname === '/api/log') {
      const job = jobs.get(searchParams.get('id'));
      if (!job) return sendJson(res, 404, { error: 'No such job.' });
      return sendJson(res, 200, { log: job.log });
    }

    if (req.method === 'GET' && pathname === '/api/vault') {
      return sendJson(res, 200, { dir: config.outputDir, files: listVault() });
    }

    if (req.method === 'POST' && pathname === '/api/reveal') {
      const body = await readBody(req);
      const target = body.name
        ? path.join(config.outputDir, path.basename(body.name))
        : config.outputDir;
      if (process.platform === 'win32') {
        execFile('explorer.exe', body.name ? ['/select,', target] : [target], () => {});
      } else if (process.platform === 'darwin') {
        execFile('open', body.name ? ['-R', target] : [target], () => {});
      } else {
        execFile('xdg-open', [config.outputDir], () => {});
      }
      return sendJson(res, 200, { ok: true });
    }

    if (req.method === 'GET' && pathname.startsWith('/vault/')) {
      return serveVault(res, pathname.slice('/vault/'.length));
    }

    if (req.method === 'GET') return serveStatic(req, res, pathname);

    res.writeHead(405, { 'Content-Type': 'text/plain' }).end('Method not allowed');
  } catch (err) {
    sendJson(res, 500, { error: err.message });
  }
});

server.listen(PORT, HOST, () => {
  const line = '='.repeat(52);
  console.log(`\n${line}`);
  console.log('  COLEFORGE  ::  the video forge is lit');
  console.log(line);
  console.log(`  Forge open at : http://${HOST}:${PORT}`);
  console.log(`  Vault         : ${config.outputDir}`);
  console.log(`  yt-dlp        : ${YTDLP ? YTDLP.version : 'NOT FOUND -> pip install -U yt-dlp'}`);
  console.log(`  ffmpeg        : ${FFMPEG || 'missing (merging/mp3 will fail)'}`);
  console.log(`${line}\n  Press Ctrl+C to bank the fire.\n`);

  // The .bat launcher sets this; `node server.js` on its own stays quiet.
  if (process.env.COLEFORGE_OPEN === '1') {
    const url = `http://${HOST}:${PORT}`;
    if (process.platform === 'win32') execFile('cmd', ['/c', 'start', '', url], () => {});
    else if (process.platform === 'darwin') execFile('open', [url], () => {});
    else execFile('xdg-open', [url], () => {});
  }
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\n[coleforge] Port ${PORT} is already in use.`);
    console.error(`[coleforge] Another forge may already be running at http://${HOST}:${PORT}`);
    console.error('[coleforge] Or start on another port:  set COLEFORGE_PORT=8421 && node server.js\n');
  } else {
    console.error('[coleforge]', err.message);
  }
  process.exit(1);
});

for (const sig of ['SIGINT', 'SIGTERM']) {
  process.on(sig, () => {
    for (const job of jobs.values()) if (job.proc) cancelJob(job);
    process.exit(0);
  });
}
