(() => {
  'use strict';
  const manifest = window.SOUND_REVIEW;
  const entries = manifest.entries;
  const byId = new Map(entries.map(entry => [entry.id, entry]));
  const player = document.querySelector('#player');
  const library = document.querySelector('#library');
  const stateKey = 'bof-sound-review-v1';
  const decisions = ['primary', 'alternate', 'layer', 'reserve', 'reject'];
  let state = loadState();
  let currentId = null;
  let focusedId = entries[0]?.id || null;
  let compare = [];
  let queue = [];

  function loadState() {
    try { return JSON.parse(localStorage.getItem(stateKey)) || {}; }
    catch (_) { return {}; }
  }
  function saveState() { localStorage.setItem(stateKey, JSON.stringify(state)); renderSummary(); }
  function review(id) { return state[id] || { decision: 'undecided', notes: '' }; }
  function audioUrl(entry) { return manifest.audioBase + encodeURIComponent(entry.file); }
  function formatTime(value) {
    if (!Number.isFinite(value)) return '0:00';
    const min = Math.floor(value / 60), sec = Math.floor(value % 60);
    return `${min}:${String(sec).padStart(2, '0')}`;
  }
  function esc(value) {
    return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  }

  function renderSummary() {
    const count = value => entries.filter(entry => review(entry.id).decision === value).length;
    const hot = entries.filter(entry => entry.flags.includes('hot-peak')).length;
    document.querySelector('#summary').innerHTML = [
      [entries.length, 'new sounds'],
      [new Set(entries.map(entry => entry.category)).size, 'categories'],
      [count('primary'), 'primary picks'],
      [count('alternate') + count('layer'), 'alternates / layers'],
      [hot, 'hot-peak checks'],
    ].map(([value, label]) => `<div class="summary-card"><strong>${value}</strong><span>${label}</span></div>`).join('');
  }

  function filters() {
    return {
      q: document.querySelector('#search').value.trim().toLowerCase(),
      category: document.querySelector('#categoryFilter').value,
      decision: document.querySelector('#decisionFilter').value,
      flag: document.querySelector('#flagFilter').value,
    };
  }
  function visibleEntries() {
    const f = filters();
    return entries.filter(entry => {
      const data = `${entry.label} ${entry.file} ${entry.proposedUse} ${entry.group}`.toLowerCase();
      return (!f.q || data.includes(f.q)) &&
        (f.category === 'all' || entry.category === f.category) &&
        (f.decision === 'all' || review(entry.id).decision === f.decision) &&
        (f.flag === 'all' || (f.flag === 'clean' ? entry.flags.length === 0 : entry.flags.includes(f.flag)));
    });
  }

  function card(entry) {
    const saved = review(entry.id);
    const variant = entry.variation ? `VAR ${entry.variation}` : 'VAR —';
    const flags = entry.flags.map(flag => `<span class="pill warn">${esc(flag)}</span>`).join('');
    const buttons = decisions.map((decision, index) =>
      `<button type="button" data-action="decision" data-value="${decision}" title="${index + 1}: ${decision}" class="${saved.decision === decision ? 'selected' : ''}">${decision}</button>`
    ).join('');
    return `<article class="sound-card ${currentId === entry.id ? 'active' : ''} ${focusedId === entry.id ? 'focused' : ''}" data-id="${entry.id}" data-decision="${saved.decision}">
      <div class="sound-head">
        <div class="sound-title"><h3>${esc(entry.label)}</h3><code title="${esc(entry.file)}">${esc(entry.file)}</code></div>
        <span class="variation">${variant}</span>
      </div>
      <p class="use">${esc(entry.proposedUse)}</p>
      <div class="meta">
        <span class="pill">${entry.duration.toFixed(2)}s</span>
        <span class="pill">peak ${entry.peakDb.toFixed(1)} dB</span>
        <span class="pill">mean ${entry.meanDb.toFixed(1)} dB</span>
        <span class="pill">${entry.sampleRate / 1000} kHz · ${entry.channels === 2 ? 'stereo' : 'mono'}</span>
        ${flags}
      </div>
      <div class="wave-row" data-action="seek" title="Click to seek">
        <img src="${esc(entry.waveform)}" alt="Waveform for ${esc(entry.label)}">
        <i class="wave-playhead"></i>
      </div>
      <div class="controls">
        <button class="play" type="button" data-action="play" aria-label="Play ${esc(entry.label)}">${currentId === entry.id && !player.paused ? 'Ⅱ' : '▶'}</button>
        <span class="time card-time">${currentId === entry.id ? formatTime(player.currentTime) : '0:00'} / ${formatTime(entry.duration)}</span>
        <button class="compare ${compare.includes(entry.id) ? 'selected' : ''}" type="button" data-action="compare">${compare.includes(entry.id) ? 'In A/B' : 'Add A/B'}</button>
      </div>
      <div class="decision" aria-label="Review decision">${buttons}</div>
      <textarea class="notes" data-action="notes" placeholder="Notes: trim, layer, lower volume, best use…">${esc(saved.notes || '')}</textarea>
    </article>`;
  }

  function render() {
    const list = visibleEntries();
    if (!list.length) { library.innerHTML = '<div class="empty">No sounds match these filters.</div>'; return; }
    library.innerHTML = manifest.categoryOrder.map(category => {
      const categoryEntries = list.filter(entry => entry.category === category);
      if (!categoryEntries.length) return '';
      return `<section class="category-section" data-category="${esc(category)}">
        <div class="category-header">
          <div><h2>${esc(category)}</h2><p>${categoryEntries.length} sound${categoryEntries.length === 1 ? '' : 's'} available</p></div>
          <div class="category-actions">
            <button class="mini-button" data-play-category="${esc(category)}" type="button">Play category</button>
            <button class="mini-button" data-stop-category type="button">Stop</button>
          </div>
        </div>
        <div class="sound-grid">${categoryEntries.map(card).join('')}</div>
      </section>`;
    }).join('');
  }

  function setFocused(id) {
    focusedId = id;
    document.querySelectorAll('.sound-card.focused').forEach(node => node.classList.remove('focused'));
    const card = document.querySelector(`.sound-card[data-id="${id}"]`);
    if (card) { card.classList.add('focused'); card.scrollIntoView({block: 'nearest', behavior: 'smooth'}); }
  }
  function play(id, restart = false) {
    const entry = byId.get(id); if (!entry) return;
    if (currentId !== id) {
      currentId = id;
      player.src = audioUrl(entry);
      player.load();
    } else if (restart) player.currentTime = 0;
    player.play().catch(() => {});
    setFocused(id);
    updateNowPlaying();
    render();
  }
  function togglePlay(id) {
    if (currentId === id && !player.paused) player.pause(); else play(id);
    render(); updateNowPlaying();
  }
  function stop() {
    queue = [];
    player.pause(); player.currentTime = 0;
    render(); updateNowPlaying();
  }
  function playCategory(category) {
    queue = visibleEntries().filter(entry => entry.category === category).map(entry => entry.id);
    const first = queue.shift(); if (first) play(first, true);
  }
  function setDecision(id, decision) {
    const old = review(id);
    state[id] = { ...old, decision: old.decision === decision ? 'undecided' : decision };
    saveState(); render(); setFocused(id);
  }
  function updateNotes(id, notes) {
    state[id] = { ...review(id), notes };
    saveState();
  }
  function toggleCompare(id) {
    compare = compare.includes(id) ? compare.filter(value => value !== id) : [...compare.slice(-1), id];
    renderCompare(); render();
  }
  function renderCompare() {
    const drawer = document.querySelector('#compareDrawer');
    drawer.classList.toggle('show', compare.length > 0);
    document.querySelector('#compareSlots').innerHTML = compare.map((id, index) => {
      const entry = byId.get(id);
      return `<button class="compare-slot" type="button" data-compare-play="${id}"><b>${index ? 'B' : 'A'}</b>${esc(entry.label)} ${entry.variation ? `#${entry.variation}` : ''}</button>`;
    }).join('');
  }

  function updateNowPlaying() {
    const entry = byId.get(currentId);
    document.querySelector('#globalPlay').textContent = entry && !player.paused ? 'Ⅱ' : '▶';
    document.querySelector('#nowTitle').textContent = entry ? `${entry.label}${entry.variation ? ` — Variation ${entry.variation}` : ''}` : 'Nothing selected';
    document.querySelector('#nowUse').textContent = entry ? entry.proposedUse : 'Choose a sound to begin.';
    document.querySelector('#nowTime').textContent = `${formatTime(player.currentTime)} / ${formatTime(player.duration || entry?.duration || 0)}`;
    const ratio = entry && player.duration ? player.currentTime / player.duration : 0;
    document.querySelector('#globalProgress').style.width = `${ratio * 100}%`;
    document.querySelectorAll('.sound-card').forEach(node => {
      const active = node.dataset.id === currentId;
      node.classList.toggle('active', active);
      if (active) {
        node.querySelector('.wave-playhead').style.width = `${ratio * 100}%`;
        node.querySelector('.card-time').textContent = `${formatTime(player.currentTime)} / ${formatTime(player.duration || entry.duration)}`;
        node.querySelector('.play').textContent = player.paused ? '▶' : 'Ⅱ';
      }
    });
  }

  function exportReview() {
    const picked = entries.map(entry => ({
      file: entry.file,
      label: entry.label,
      variation: entry.variation,
      category: entry.category,
      proposedUse: entry.proposedUse,
      decision: review(entry.id).decision,
      notes: review(entry.id).notes || '',
      duration: entry.duration,
      peakDb: entry.peakDb,
      sha256: entry.sha256,
    }));
    const output = {
      project: 'Bullets of Fury',
      source: manifest.source,
      exportedAt: new Date().toISOString(),
      productionAudioReplaced: false,
      sounds: picked,
    };
    const blob = new Blob([JSON.stringify(output, null, 2)], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'bullets-of-fury-sound-library-decisions.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  library.addEventListener('click', event => {
    const card = event.target.closest('.sound-card');
    const categoryPlay = event.target.closest('[data-play-category]');
    if (categoryPlay) { playCategory(categoryPlay.dataset.playCategory); return; }
    if (event.target.closest('[data-stop-category]')) { stop(); return; }
    if (!card) return;
    const id = card.dataset.id;
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (action === 'play') togglePlay(id);
    if (action === 'compare') toggleCompare(id);
    if (action === 'decision') setDecision(id, event.target.closest('[data-value]').dataset.value);
    if (action === 'seek') {
      const wave = event.target.closest('.wave-row');
      const ratio = (event.clientX - wave.getBoundingClientRect().left) / wave.clientWidth;
      if (currentId !== id) play(id); else player.currentTime = Math.max(0, Math.min(player.duration || 0, ratio * (player.duration || 0)));
    }
    setFocused(id);
  });
  library.addEventListener('input', event => {
    if (!event.target.matches('[data-action="notes"]')) return;
    updateNotes(event.target.closest('.sound-card').dataset.id, event.target.value);
  });

  ['search', 'categoryFilter', 'decisionFilter', 'flagFilter'].forEach(id => {
    document.querySelector(`#${id}`).addEventListener(id === 'search' ? 'input' : 'change', render);
  });
  document.querySelector('#masterVolume').addEventListener('input', event => {
    player.volume = Number(event.target.value);
    document.querySelector('#volumeReadout').textContent = `${Math.round(player.volume * 100)}%`;
  });
  document.querySelector('#stopAll').addEventListener('click', stop);
  document.querySelector('#exportReview').addEventListener('click', exportReview);
  document.querySelector('#globalPlay').addEventListener('click', () => currentId ? togglePlay(currentId) : entries[0] && play(entries[0].id));
  document.querySelector('#clearCompare').addEventListener('click', () => { compare = []; renderCompare(); render(); });
  document.querySelector('#compareSlots').addEventListener('click', event => {
    const target = event.target.closest('[data-compare-play]'); if (target) play(target.dataset.comparePlay, true);
  });
  player.addEventListener('play', () => { render(); updateNowPlaying(); });
  player.addEventListener('pause', () => { render(); updateNowPlaying(); });
  player.addEventListener('timeupdate', updateNowPlaying);
  player.addEventListener('ended', () => { const next = queue.shift(); if (next) play(next, true); else updateNowPlaying(); });
  window.addEventListener('keydown', event => {
    if (/INPUT|TEXTAREA|SELECT/.test(event.target.tagName)) return;
    const visible = visibleEntries();
    const index = Math.max(0, visible.findIndex(entry => entry.id === focusedId));
    if (event.code === 'Space') { event.preventDefault(); focusedId && togglePlay(focusedId); }
    if (event.key.toLowerCase() === 'j') setFocused(visible[Math.max(0, index - 1)]?.id);
    if (event.key.toLowerCase() === 'k') setFocused(visible[Math.min(visible.length - 1, index + 1)]?.id);
    if (/^[1-5]$/.test(event.key) && focusedId) setDecision(focusedId, decisions[Number(event.key) - 1]);
  });

  for (const category of manifest.categoryOrder) {
    const option = document.createElement('option'); option.value = category; option.textContent = category;
    document.querySelector('#categoryFilter').appendChild(option);
  }
  player.volume = .65;
  renderSummary(); render(); renderCompare(); updateNowPlaying();
})();
