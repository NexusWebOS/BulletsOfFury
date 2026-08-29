/* ============================================================
   ColeForge — control panel
   ============================================================ */
'use strict';

const $ = (id) => document.getElementById(id);

const els = {
  url: $('url'),
  scry: $('btn-scry'),
  forge: $('btn-forge'),
  hint: $('hint'),
  error: $('error-line'),
  preview: $('preview'),
  previewImg: $('preview-img'),
  previewTitle: $('preview-title'),
  previewSub: $('preview-sub'),
  playlistBox: $('playlist-box'),
  playlistList: $('playlist-list'),
  playlistCount: $('playlist-count'),
  metalGrid: $('metal-grid'),
  optPlaylist: $('opt-playlist'),
  optSubs: $('opt-subs'),
  optSound: $('opt-sound'),
  queue: $('queue'),
  vault: $('vault'),
  vaultPath: $('vault-path'),
  chipYtdlp: $('chip-ytdlp'),
  chipFfmpeg: $('chip-ffmpeg'),
  chipVault: $('chip-vault'),
  forgeState: $('forge-state'),
  forgeTitle: $('forge-title'),
  forgeSpeed: $('forge-speed'),
  forgeEta: $('forge-eta'),
  forgeSize: $('forge-size'),
  heatFill: $('heat-fill'),
  heatLabel: $('heat-label'),
  heatGauge: $('heat-gauge'),
  dialogue: $('dialogue'),
  dialogueText: $('dialogue-text'),
};

const store = {
  format: 'best',
  scryed: null,      // last probe result
  jobs: new Map(),   // id -> job
  streams: new Map() // id -> EventSource
};

/* ------------------------------------------------------------------ *
 * Chiptune — a few oscillators, no assets
 * ------------------------------------------------------------------ */

const Chip = (() => {
  let ctx = null;
  const on = () => els.optSound.checked;

  function ac() {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function tone(freq, dur, type, gain, delay) {
    const a = ac();
    if (!a) return;
    const t0 = a.currentTime + (delay || 0);
    const osc = a.createOscillator();
    const g = a.createGain();
    osc.type = type || 'square';
    osc.frequency.setValueAtTime(freq, t0);
    g.gain.setValueAtTime(0, t0);
    g.gain.linearRampToValueAtTime(gain === undefined ? 0.06 : gain, t0 + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g).connect(a.destination);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  function noise(dur, gain) {
    const a = ac();
    if (!a) return;
    const n = Math.floor(a.sampleRate * dur);
    const buf = a.createBuffer(1, n, a.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 3);
    const src = a.createBufferSource();
    src.buffer = buf;
    const f = a.createBiquadFilter();
    f.type = 'highpass';
    f.frequency.value = 1800;
    const g = a.createGain();
    g.gain.value = gain === undefined ? 0.05 : gain;
    src.connect(f).connect(g).connect(a.destination);
    src.start();
  }

  return {
    clang() { if (!on()) return; noise(0.09, 0.045); tone(1180, 0.07, 'square', 0.035); tone(760, 0.11, 'triangle', 0.03, 0.01); },
    blip()  { if (!on()) return; tone(880, 0.06, 'square', 0.05); },
    select(){ if (!on()) return; tone(660, 0.05, 'square', 0.04); tone(990, 0.05, 'square', 0.035, 0.05); },
    start() { if (!on()) return; [523, 659, 784].forEach((f, i) => tone(f, 0.1, 'square', 0.05, i * 0.06)); },
    done()  { if (!on()) return; [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.16, 'square', 0.055, i * 0.09)); },
    fail()  { if (!on()) return; [392, 330, 262].forEach((f, i) => tone(f, 0.2, 'sawtooth', 0.045, i * 0.11)); },
  };
})();

/* ------------------------------------------------------------------ *
 * Formatting
 * ------------------------------------------------------------------ */

function bytes(n) {
  if (!n || n < 0) return '—';
  const u = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  while (n >= 1024 && i < u.length - 1) { n /= 1024; i++; }
  return `${n < 10 && i > 0 ? n.toFixed(1) : Math.round(n)} ${u[i]}`;
}

function rate(n) { return n ? `${bytes(n)}/s` : '—'; }

function clock(sec) {
  if (sec === null || sec === undefined || !Number.isFinite(sec)) return '—';
  sec = Math.max(0, Math.round(sec));
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return h ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
           : `${m}:${String(s).padStart(2, '0')}`;
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/* ------------------------------------------------------------------ *
 * Dialogue box
 * ------------------------------------------------------------------ */

let dialogueTimer = null;
function say(text, ms) {
  els.dialogueText.textContent = text;
  els.dialogue.hidden = false;
  clearTimeout(dialogueTimer);
  dialogueTimer = setTimeout(() => { els.dialogue.hidden = true; }, ms || 3600);
}

function showError(msg) {
  els.error.textContent = msg;
  els.error.hidden = false;
}
function clearError() { els.error.hidden = true; }

/* ------------------------------------------------------------------ *
 * API
 * ------------------------------------------------------------------ */

async function api(path, opts) {
  const res = await fetch(path, {
    ...opts,
    headers: opts && opts.body ? { 'Content-Type': 'application/json' } : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

/* ------------------------------------------------------------------ *
 * Health
 * ------------------------------------------------------------------ */

async function checkHealth() {
  try {
    const h = await api('/api/health');
    els.chipYtdlp.textContent = h.ytdlp ? `yt-dlp ${h.ytdlp}` : 'yt-dlp MISSING';
    els.chipYtdlp.className = `chip ${h.ytdlp ? 'chip-ok' : 'chip-bad'}`;
    els.chipFfmpeg.textContent = h.ffmpeg ? 'ffmpeg OK' : 'ffmpeg MISSING';
    els.chipFfmpeg.className = `chip ${h.ffmpeg ? 'chip-ok' : 'chip-bad'}`;
    els.vaultPath.textContent = h.outputDir;
    if (!h.ytdlp) showError('yt-dlp is not installed. Run:  python -m pip install -U yt-dlp');
  } catch (e) {
    els.chipYtdlp.textContent = 'server down';
    els.chipYtdlp.className = 'chip chip-bad';
  }
}

/* ------------------------------------------------------------------ *
 * Scrying (probe)
 * ------------------------------------------------------------------ */

function setMetalAvailability(heights) {
  const max = heights && heights.length ? heights[0] : Infinity;
  let selectedGotDisabled = false;

  for (const btn of els.metalGrid.querySelectorAll('.metal')) {
    const h = Number(btn.dataset.height || 0);
    const unavailable = h > 0 && h > max;
    btn.disabled = unavailable;
    if (unavailable && btn.classList.contains('selected')) {
      btn.classList.remove('selected');
      selectedGotDisabled = true;
    }
  }
  if (selectedGotDisabled) selectMetal('best');
}

function selectMetal(format) {
  store.format = format;
  for (const btn of els.metalGrid.querySelectorAll('.metal')) {
    btn.classList.toggle('selected', btn.dataset.format === format);
  }
}

function renderPlaylist(info) {
  els.playlistCount.textContent = `${info.count} TRACK${info.count === 1 ? '' : 'S'}`;
  els.playlistList.innerHTML = info.entries.map((e, i) => `
    <li data-i="${i}">
      <input type="checkbox" checked data-i="${i}">
      <span class="pl-title">${esc(e.title)}</span>
      <span class="pl-dur">${e.duration ? clock(e.duration) : ''}</span>
    </li>`).join('');
  els.playlistBox.hidden = false;
}

async function scry() {
  const url = els.url.value.trim();
  clearError();
  if (!url) { showError('Give me a link to scry first.'); return; }

  els.scry.disabled = true;
  els.scry.textContent = '...';
  els.hint.textContent = 'Peering into the link...';
  Chip.blip();

  try {
    const info = await api('/api/probe', {
      method: 'POST',
      body: JSON.stringify({ url, playlist: els.optPlaylist.checked }),
    });
    store.scryed = info;

    if (info.type === 'playlist') {
      els.preview.hidden = false;
      els.previewImg.src = info.thumb || '';
      els.previewTitle.textContent = info.title;
      els.previewSub.textContent = `${info.uploader || 'unknown smith'} · ${info.count} videos`;
      renderPlaylist(info);
      setMetalAvailability(null);
      els.hint.textContent = 'Playlist read. Untick anything you do not want.';
    } else {
      els.playlistBox.hidden = true;
      els.preview.hidden = false;
      els.previewImg.src = info.thumb || '';
      els.previewTitle.textContent = info.title;
      const bits = [info.uploader, info.duration ? clock(info.duration) : null,
        info.heights.length ? `up to ${info.heights[0]}p` : null].filter(Boolean);
      els.previewSub.textContent = bits.join(' · ');
      setMetalAvailability(info.heights);
      els.hint.textContent = 'Ore identified. Choose your metal and strike.';
    }
    Chip.select();
  } catch (e) {
    store.scryed = null;
    els.preview.hidden = true;
    els.playlistBox.hidden = true;
    showError(e.message);
    els.hint.textContent = 'The link would not yield. Check it and try again.';
    Chip.fail();
  } finally {
    els.scry.disabled = false;
    els.scry.textContent = 'SCRY';
  }
}

/* ------------------------------------------------------------------ *
 * Forging
 * ------------------------------------------------------------------ */

function selectedPlaylistItems() {
  const info = store.scryed;
  if (!info || info.type !== 'playlist') return null;
  const picked = [];
  els.playlistList.querySelectorAll('input[type=checkbox]').forEach((cb) => {
    if (cb.checked) {
      const e = info.entries[Number(cb.dataset.i)];
      if (e && e.url) picked.push({ url: e.url, title: e.title, thumb: e.thumb, duration: e.duration });
    }
  });
  return picked;
}

async function forge() {
  const url = els.url.value.trim();
  clearError();
  if (!url) { showError('Nothing to forge — paste a link.'); return; }

  let items;
  const picked = selectedPlaylistItems();
  if (picked) {
    if (!picked.length) { showError('Every track is unticked. Pick at least one.'); return; }
    items = picked;
  } else if (store.scryed && store.scryed.type === 'video') {
    items = [{
      url,
      title: store.scryed.title,
      thumb: store.scryed.thumb,
      duration: store.scryed.duration,
    }];
  } else {
    items = [{ url }];
  }

  els.forge.disabled = true;
  try {
    const res = await api('/api/forge', {
      method: 'POST',
      body: JSON.stringify({
        items,
        format: store.format,
        playlist: false,
        subtitles: els.optSubs.checked,
      }),
    });
    Chip.start();
    say(items.length > 1
      ? `${items.length} ingots on the fire.`
      : 'Into the fire it goes.');
    for (const job of res.jobs) {
      store.jobs.set(job.id, job);
      subscribe(job.id);
    }
    renderQueue();
    els.url.value = '';
    els.preview.hidden = true;
    els.playlistBox.hidden = true;
    store.scryed = null;
    setMetalAvailability(null);
    els.hint.textContent = 'Work order placed. Watch the anvil.';
  } catch (e) {
    showError(e.message);
    Chip.fail();
  } finally {
    els.forge.disabled = false;
  }
}

/* ------------------------------------------------------------------ *
 * Live job streams
 * ------------------------------------------------------------------ */

function subscribe(id) {
  if (store.streams.has(id)) return;
  const es = new EventSource(`/api/events?id=${encodeURIComponent(id)}`);

  es.onmessage = (ev) => {
    let msg;
    try { msg = JSON.parse(ev.data); } catch (_) { return; }

    if (msg.job) {
      store.jobs.set(msg.job.id, msg.job);
      updateJobRow(msg.job);
      syncForgeScene();
    }

    if (msg.type === 'end') {
      es.close();
      store.streams.delete(id);
      const j = msg.job;
      if (j.status === 'done') {
        Chip.done();
        say(`FORGED — ${j.title}`, 5000);
        loadVault();
      } else if (j.status === 'failed') {
        Chip.fail();
        say(`The metal cracked: ${j.error || 'unknown failure'}`, 6000);
      }
      renderQueue();
      syncForgeScene();
    }
  };

  es.onerror = () => { /* server restarted or job gone; the row keeps its last state */ };
  store.streams.set(id, es);
}

/* ------------------------------------------------------------------ *
 * Queue rendering
 * ------------------------------------------------------------------ */

function jobRowHtml(j) {
  const pct = Math.round(j.percent || 0);
  const isLive = j.status === 'running' || j.status === 'queued';
  return `
    <li class="job is-${j.status}" data-id="${j.id}">
      <div class="job-thumb">${j.thumb ? `<img src="${esc(j.thumb)}" alt="">` : ''}</div>
      <div class="job-body">
        <p class="job-title" title="${esc(j.title)}">${esc(j.title)}</p>
        <div class="job-bar"><div class="job-fill" style="width:${pct}%"></div></div>
        <div class="job-meta">
          <span class="job-stage">${esc(j.stage)}</span>
          <span class="job-pct">${pct}%</span>
          <span class="job-speed">${j.status === 'running' ? rate(j.speed) : ''}</span>
          <span class="job-eta">${j.status === 'running' && j.eta ? `ETA ${clock(j.eta)}` : ''}</span>
          <span class="job-size">${j.total ? bytes(j.total) : ''}</span>
        </div>
        ${j.error ? `<p class="job-error">${esc(j.error)}</p>` : ''}
      </div>
      <div class="job-actions">
        ${isLive ? `<button class="btn btn-mini job-cancel">STOP</button>` : ''}
        ${j.status === 'done' && j.files.length
          ? `<button class="btn btn-mini job-reveal" data-file="${esc(j.files[0])}">SHOW</button>` : ''}
      </div>
    </li>`;
}

function renderQueue() {
  const list = [...store.jobs.values()].sort((a, b) => b.createdAt - a.createdAt);
  els.queue.innerHTML = list.length
    ? list.map(jobRowHtml).join('')
    : '<li class="queue-empty">The order book is empty. Summon something.</li>';
}

function updateJobRow(j) {
  const row = els.queue.querySelector(`.job[data-id="${j.id}"]`);
  if (!row) { renderQueue(); return; }

  row.className = `job is-${j.status}`;
  const pct = Math.round(j.percent || 0);
  row.querySelector('.job-fill').style.width = `${pct}%`;
  row.querySelector('.job-pct').textContent = `${pct}%`;
  row.querySelector('.job-stage').textContent = j.stage;
  row.querySelector('.job-speed').textContent = j.status === 'running' ? rate(j.speed) : '';
  row.querySelector('.job-eta').textContent = j.status === 'running' && j.eta ? `ETA ${clock(j.eta)}` : '';
  row.querySelector('.job-size').textContent = j.total ? bytes(j.total) : '';
  if (j.title && row.querySelector('.job-title').textContent !== j.title) {
    row.querySelector('.job-title').textContent = j.title;
  }
}

/* ------------------------------------------------------------------ *
 * Forge scene binding
 * ------------------------------------------------------------------ */

let lastSceneMode = 'idle';

function syncForgeScene() {
  const all = [...store.jobs.values()];
  const running = all.find((j) => j.status === 'running');
  const queued = all.find((j) => j.status === 'queued');

  if (running) {
    Forge.setMode('forging');
    Forge.setProgress((running.percent || 0) / 100);
    Forge.setIntensity(running.speed);
    els.forgeState.textContent = running.stage;
    els.forgeTitle.textContent = running.title;
    els.forgeSpeed.textContent = rate(running.speed);
    els.forgeEta.textContent = running.eta ? `ETA ${clock(running.eta)}` : '—';
    els.forgeSize.textContent = running.total
      ? `${bytes(running.downloaded)} / ${bytes(running.total)}` : bytes(running.downloaded);
    setHeat(running.percent || 0);
    lastSceneMode = 'forging';
    return;
  }

  if (queued) {
    Forge.setMode('idle');
    els.forgeState.textContent = 'QUEUED';
    els.forgeTitle.textContent = queued.title;
    setHeat(0);
    return;
  }

  const recent = all.sort((a, b) => (b.finishedAt || 0) - (a.finishedAt || 0))[0];
  if (recent && lastSceneMode === 'forging') {
    if (recent.status === 'done') {
      Forge.setMode('done');
      els.forgeState.textContent = 'COMPLETE';
      els.forgeTitle.textContent = recent.title;
      setHeat(100);
    } else if (recent.status === 'failed') {
      Forge.setMode('failed');
      els.forgeState.textContent = 'FAILED';
      els.forgeTitle.textContent = recent.error || recent.title;
      setHeat(0);
    } else {
      Forge.setMode('idle');
      els.forgeState.textContent = 'IDLE';
      setHeat(0);
    }
    els.forgeSpeed.textContent = '—';
    els.forgeEta.textContent = '—';
    lastSceneMode = recent.status;
    return;
  }

  if (!recent) {
    Forge.setMode('idle');
    els.forgeState.textContent = 'IDLE';
    els.forgeTitle.textContent = '— no work on the anvil —';
    setHeat(0);
  }
}

function setHeat(pct) {
  const p = Math.max(0, Math.min(100, pct));
  els.heatFill.style.width = `${p}%`;
  els.heatLabel.textContent = `${Math.round(p)}%`;
  els.heatGauge.setAttribute('aria-valuenow', String(Math.round(p)));
}

/* ------------------------------------------------------------------ *
 * Vault
 * ------------------------------------------------------------------ */

async function loadVault() {
  try {
    const v = await api('/api/vault');
    els.vaultPath.textContent = v.dir;
    els.vault.innerHTML = v.files.length
      ? v.files.map((f) => `
        <li>
          <span class="vault-name" title="${esc(f.name)}">${esc(f.name)}</span>
          <span class="vault-size">${bytes(f.size)}</span>
          <button class="btn btn-mini vault-reveal" data-name="${esc(f.name)}">SHOW</button>
          <a class="btn btn-mini" href="/vault/${encodeURIComponent(f.name)}" download>SAVE</a>
        </li>`).join('')
      : '<li class="queue-empty">Nothing forged yet.</li>';
  } catch (e) {
    els.vault.innerHTML = `<li class="queue-empty">Vault unreadable: ${esc(e.message)}</li>`;
  }
}

/* ------------------------------------------------------------------ *
 * Wiring
 * ------------------------------------------------------------------ */

els.scry.addEventListener('click', scry);
els.forge.addEventListener('click', forge);

els.url.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') { e.preventDefault(); scry(); }
});

els.url.addEventListener('paste', () => {
  setTimeout(() => { if (els.url.value.trim().startsWith('http')) scry(); }, 60);
});

els.metalGrid.addEventListener('click', (e) => {
  const btn = e.target.closest('.metal');
  if (!btn || btn.disabled) return;
  selectMetal(btn.dataset.format);
  Chip.select();
});

els.optPlaylist.addEventListener('change', () => {
  if (els.url.value.trim()) scry();
});

$('btn-select-all').addEventListener('click', () => {
  els.playlistList.querySelectorAll('input').forEach((c) => { c.checked = true; });
});
$('btn-select-none').addEventListener('click', () => {
  els.playlistList.querySelectorAll('input').forEach((c) => { c.checked = false; });
});

els.playlistList.addEventListener('click', (e) => {
  if (e.target.tagName === 'INPUT') return;
  const li = e.target.closest('li');
  if (!li) return;
  const cb = li.querySelector('input');
  cb.checked = !cb.checked;
});

els.queue.addEventListener('click', async (e) => {
  const cancel = e.target.closest('.job-cancel');
  if (cancel) {
    const id = cancel.closest('.job').dataset.id;
    await api('/api/cancel', { method: 'POST', body: JSON.stringify({ id }) }).catch(() => {});
    say('Pulled from the fire.');
    return;
  }
  const reveal = e.target.closest('.job-reveal');
  if (reveal) {
    api('/api/reveal', { method: 'POST', body: JSON.stringify({ name: reveal.dataset.file.split(/[\\/]/).pop() }) }).catch(() => {});
  }
});

els.vault.addEventListener('click', (e) => {
  const btn = e.target.closest('.vault-reveal');
  if (!btn) return;
  api('/api/reveal', { method: 'POST', body: JSON.stringify({ name: btn.dataset.name }) }).catch(() => {});
});

els.chipVault.addEventListener('click', () => {
  api('/api/reveal', { method: 'POST', body: JSON.stringify({}) }).catch(() => {});
});

$('btn-clear').addEventListener('click', async () => {
  await api('/api/clear', { method: 'POST', body: '{}' }).catch(() => {});
  for (const [id, j] of store.jobs) {
    if (['done', 'failed', 'cancelled'].includes(j.status)) store.jobs.delete(id);
  }
  lastSceneMode = 'idle';
  renderQueue();
  syncForgeScene();
});

$('btn-refresh-vault').addEventListener('click', loadVault);

/* ------------------------------------------------------------------ *
 * Boot
 * ------------------------------------------------------------------ */

async function restoreJobs() {
  try {
    const { jobs } = await api('/api/jobs');
    for (const j of jobs) {
      store.jobs.set(j.id, j);
      if (j.status === 'running' || j.status === 'queued') subscribe(j.id);
    }
    renderQueue();
    syncForgeScene();
  } catch (_) { /* server not up yet */ }
}

Forge.init($('forge'));
Forge.onStrike(() => Chip.clang());
Forge.drawLogo($('logo-anvil'));
selectMetal('best');
checkHealth();
loadVault();
restoreJobs();

// The scene reads state each frame; nudge it when nothing else is happening.
setInterval(syncForgeScene, 1000);
