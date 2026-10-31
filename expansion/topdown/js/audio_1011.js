/* ColeForge chip sound pass for the standalone Overdrive campaign.
 * HTMLAudio keeps the expansion usable from file://. Loops belong to live
 * actors/actions, never to a frame counter; a stopped action releases its voice.
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, BANK = root.TD_CHIP_AUDIO;
  const LEGACY = {
    mg: ['nsp_bof2_shot.mp3', .30, .05], eshot: ['enemyShoot.mp3', .30, .07], crashShot: ['nsp_bof2_charge_shot.mp3', .70, .08],
    hit: ['hit.mp3', .45, .04], expS: ['expSmall.mp3', .75, .04], expB: ['expBig.mp3', .85, .07],
    pick: ['nsp_bof2_pickup.mp3', .6, .05], blip: ['nsp_console_beep.mp3', .45, .06],
    warn: ['nsp_bof2_boss_warning.mp3', .8, 2], laser: ['nsp_heavy_laser.mp3', .45, .12],
    charge: ['retina_charge.mp3', .55, .5], intro: ['nsp_bof2_stage_intro.mp3', .7, 1],
    phase: ['bossPhase.mp3', .8, .5], whiteout: ['nsp_bof2_ultra_blast.mp3', .8, 1],
  };
  const MUSIC = {
    level2: 'assets/game/shared/audio/music/Unused1.mp3', boss2: 'assets/game/shared/audio/music/Unused11.mp3',
    warrior: 'expansion/topdown/audio/BOF-O-BOSS1.mp3',
    base: 'expansion/topdown/audio/music23/BOF-BASE.wav',
    gosfar43: 'expansion/topdown/audio/music43/gosfar-last-hope.wav',
    lastHope: 'expansion/topdown/audio/music23/rise_of_the_last_hope_fast_riff_genesis.wav',
    clear: 'assets/game/shared/audio/music/Password_StageClear.mp3', title: 'assets/game/shared/audio/music/Title.mp3',select:'assets/game/shared/audio/music/PilotSelect.mp3',
  };
  const sounds = {}, aliases = { cannon: 'gd_tankCannon', missile: 'missileLaunch', lock: 'lockon', engine: 'gd_tankEngineLoop' };
  for (const [key, d] of Object.entries(LEGACY)) sounds[key] = { file: 'assets/game/shared/audio/sounds/' + d[0], gain: d[1], min: d[2] };
  for (const [key, d] of Object.entries(BANK.cues)) {
    sounds[key] = Object.assign({}, d, { file: BANK.base + d.file });
    aliases[d.sourceKey] = key;
  }
  // Public spellings match both the approved library and the expansion vocabulary.
  for (const key of Object.keys(BANK.cues).filter(k => k.startsWith('gd_'))) aliases[key.slice(3)] = key;
  const previous = new WeakMap(), identities = new WeakMap(); let nextId = 0;
  const identity = owner => { if (!identities.has(owner)) identities.set(owner, ++nextId); return identities.get(owner); };
  function inView(owner, radius) {
    const c = TD.Cam, r = radius || owner.r || 20;
    return owner.x + r >= c.x && owner.x - r <= c.x + TD.VW / c.zoom && owner.y + r >= c.y && owner.y - r <= c.y + TD.VH / c.zoom;
  }
  const A = TD.Audio = {
    on: false, vol: .8, mvol: .55, master:1,voiceVol:.8,engineVol:1, pools: {}, lastT: {}, music: null, musicKey: null,
    sounds, aliases, loops: new Map(), waves: new Map(), failures: [], stats: {}, suspended: false,
    musicVoices: new Set(), musicGain: 1, _musicFrame: null,
    resolve(key) { return aliases[key] || key; },
    unlock() { if (this.on) return; this.on = true; if (this._pending) { const p = this._pending; this._pending = null; this.playMusic(p.key, p.seconds, p.gain); } },
    media(file) {
      const audio = new root.Audio(ART.BASE + file); audio.preload = 'auto';
      audio.addEventListener('error', () => { if (this.failures.length < 24) this.failures.push({ file, code: audio.error && audio.error.code }); });
      return audio;
    },
    start(audio, key, onFailure) {
      this.stats[key] = (this.stats[key] || 0) + 1;
      const failed = e => { if (e.name !== 'AbortError') { if (this.failures.length < 24) this.failures.push({ key, error: e.name }); if (onFailure) onFailure(e); } };
      try { audio.play().catch(failed); } catch (e) { failed(e); }
      return audio;
    },
    play(key, gain) {
      key = this.resolve(key); const d = sounds[key];
      if (!d || d.loop || !this.on || this.suspended) return null;
      const now = performance.now() / 1000;
      if (now - (this.lastT[key] ?? -9) < d.min) return null;
      this.lastT[key] = now;
      const pool = this.pools[key] || (this.pools[key] = []);
      let audio = pool.find(a => a.paused || a.ended);
      if (!audio && pool.length < 4) { audio = this.media(d.file); pool.push(audio); }
      if (!audio) { audio = pool.shift(); pool.push(audio); audio.pause(); }
      // A death or a large volley cannot leave hundreds of overlapping voices.
      const active = Object.values(this.pools).flat().filter(a => !a.paused);
      if (active.length >= 24) active[0].pause();
      try { audio.currentTime = 0; audio.volume = M.clamp(d.gain * (gain ?? 1) * this.vol*this.master, 0, 1); } catch (e) {}
      return this.start(audio, key);
    },
    loop(key, token, gain, rate) {
      key = this.resolve(key); const d = sounds[key];
      if (!d || !d.loop || !this.on || this.suspended) return null;
      let voice = this.loops.get(token);
      if (voice && voice.key !== key) { voice.audio.pause(); this.loops.delete(token); voice = null; }
      if (!voice) {
        if (this.loops.size >= 12) return null;
        const audio = this.media(d.file); audio.loop = true;
        voice = { key, audio, wanted: true }; this.loops.set(token, voice);
        audio.volume = M.clamp(d.gain * (gain ?? 1) * this.vol*this.master, 0, 1);
        audio.playbackRate = rate || 1; audio.preservesPitch = true; this.start(audio, key);
      }
      voice.wanted = true; voice.audio.volume = M.clamp(d.gain * (gain ?? 1) * this.vol*this.master, 0, 1);
      voice.audio.playbackRate = rate || 1;
      return voice.audio;
    },
    stopLoops() { for (const v of this.loops.values()) v.audio.pause(); this.loops.clear(); },
    stopEffects() {
      this.stopLoops();
      for (const pool of Object.values(this.pools)) for (const audio of pool) audio.pause();
      for (const v of this.waves.values()) v.audio.pause(); this.waves.clear();
    },
    reset() { this.stopEffects(); this.lastT = {}; },
    impact(shot, gain) {
      if (!inView(shot, 60)) return;
      this.play(shot.k === 'shell' ? 'gd_shellImpact' : shot.k === 'homing' || shot.k === 'missile' ? 'missileHit' : shot.k === 'laser' || shot.k === 'snipe' ? 'laserBeamHit' : 'impactMetal', gain);
    },
    // Call when an authored firewall is launched, with its expected visible travel
    // time. Pitch-preserving 1/2/4/8s source spans keep media rate within [0.5,2].
    // The live owner bounds cancel it earlier on impact, death or leaving view.
    firewall(owner, seconds, visible) {
      if (!this.on || this.suspended || !owner || !Number.isFinite(seconds) || seconds <= 0) return null;
      const old = this.waves.get(owner); if (old) { old.audio.pause(); this.waves.delete(owner); }
      seconds = M.clamp(seconds, .5, 16);
      const variant = BANK.firewallVariants.reduce((a, b) => Math.abs(Math.log(a.duration / seconds)) < Math.abs(Math.log(b.duration / seconds)) ? a : b);
      const audio = this.media(BANK.base + variant.file), voice = { audio, owner, elapsed: 0, seconds, visible };
      audio.volume = M.clamp(sounds.firewallLaunch.gain * this.vol * this.master, 0, 1);
      audio.playbackRate = variant.duration / seconds; audio.preservesPitch = true;
      this.waves.set(owner, voice); audio.addEventListener('ended', () => { if (this.waves.get(owner) === voice) this.waves.delete(owner); });
      this.start(audio, 'firewallLaunch'); return voice;
    },
    scene(G, dt) {
      const p = G.player;
      if (G.state !== 'play' || !p || p.dead || this.suspended) { this.stopLoops(); for (const v of this.waves.values()) v.audio.pause(); this.waves.clear(); return; }
      for (const v of this.loops.values()) v.wanted = false;
      this.actor(p, 1, true);
      // Nearby companion/boss vehicles are quiet layers, capped to three actors.
      const others = [G.ally, ...(G.boss?.tanks || (G.boss?.parts ? [G.boss] : [])), ...G.units.filter(u => !TD.ET[u.type].foot && !TD.ET[u.type].still)];
      for (const u of others.filter(u => u && !u.dead && inView(u, 80)).sort((a, b) => M.dist(p.x, p.y, a.x, a.y) - M.dist(p.x, p.y, b.x, b.y)).slice(0, 3)) this.actor(u, .3, false);
      if (TD.Stealth.phase === 'ALERT' && !G.gosfar43?.power) this.loop('gd_alarmLoop', 'alarm', .65);
      const wren = G.boss?.tanks?.find(u => u.crew === 'wren');
      if (wren && !wren.dead && wren.parts.special_module > 0 && wren.recover <= 0 && wren.t % 9 < 3 && inView(wren, 90)) this.loop('bossShieldStatic', 'wren-shield', .75);
      for (const [token, voice] of this.loops) if (!voice.wanted) { voice.audio.pause(); this.loops.delete(token); }
      for (const [owner, voice] of this.waves) {
        voice.audio.volume = M.clamp(sounds.firewallLaunch.gain * this.vol * this.master, 0, 1);
        voice.elapsed += dt;
        if (owner.dead || voice.elapsed >= voice.seconds || !(voice.visible ? voice.visible(owner) : inView(owner))) { voice.audio.pause(); this.waves.delete(owner); }
      }
    },
    actor(p, gain, player) {
      const aim = p.aim ?? p.look ?? p.turret ?? p.upper ?? p.a ?? 0;
      const before = previous.get(p) || { x: p.x, y: p.y, aim, distance: 0, side: 0 };
      const distance = M.dist(p.x, p.y, before.x, before.y), moving = distance > .08 && distance < 40;
      if (p.onfoot) {
        if (moving && p.stance !== 'prone' && !p.roll && !p.action) {
          before.distance += distance;
          if (before.distance >= 24) { this.play(before.side++ % 2 ? 'gd_footstepB' : 'gd_footstepA', gain); before.distance %= 24; }
        } else before.distance = 0;
      } else {
        const id = identity(p);
        this.loop('gd_tankEngineLoop', id + ':engine', gain*this.engineVol * (moving ? 1 : .65), p.boosting ? 1.12 : 1);
        if (moving) this.loop('gd_tankTreadLoop', id + ':treads', gain, p.boosting ? 1.2 : 1);
        if (p.parts?.turret !== 0 && Math.abs(M.wrap(aim - before.aim)) > .002) this.loop('gd_turretTraverse', id + ':turret', gain);
        if (player && p.boosting && !before.boosting) this.play('chargeDash', .75);
      }
      previous.set(p, { x: p.x, y: p.y, aim, boosting: p.boosting, distance: before.distance, side: before.side });
    },
    // Wall-clock fades also run through protected dialogue and paused gameplay.
    // Wait for actual playback before fading away the outgoing stage track.
    syncMusicVolumes() {
      for (const v of this.musicVoices) v.audio.volume = M.clamp(this.mvol * this.master * v.gain, 0, 1);
    },
    _updateMusic() {
      this._musicFrame = null;
      const now = performance.now(); let fading = false;
      for (const v of this.musicVoices) {
        if (v.fade) {
          const t = M.clamp((now - v.fade.at) / v.fade.ms, 0, 1);
          v.gain = M.lerp(v.fade.from, v.fade.to, t * t * (3 - 2 * t));
          if (t === 1) v.fade = null; else fading = true;
        }
        if (v.retiring && !v.fade && v.gain === 0) { v.audio.pause(); this.musicVoices.delete(v); }
      }
      this.syncMusicVolumes();
      if (fading) this._musicFrame = root.requestAnimationFrame(() => this._updateMusic());
    },
    _rampMusic(v, gain, seconds, retiring = false) {
      v.retiring = retiring;
      if (seconds > 0) v.fade = { from: v.gain, to: gain, at: performance.now(), ms: seconds * 1000 };
      else { v.gain = gain; v.fade = null; }
      if (this._musicFrame != null) root.cancelAnimationFrame(this._musicFrame);
      this._updateMusic();
    },
    fadeMusic(gain, seconds = 1.8) {
      gain = M.clamp(gain, 0, 1); this.musicGain = gain;
      if (this._pending) this._pending.gain = gain;
      const v = [...this.musicVoices].find(v => v.audio === this.music);
      if (v && v.playing) this._rampMusic(v, gain, seconds);
    },
    playMusic(key, seconds = 0, gain = 1) {
      if (this.musicKey === key && this.music || this._pending?.key === key) return;
      const file = MUSIC[key]; if (!file) return;
      if (!this.on) { this._pending = { key, seconds, gain }; return; }
      if (!(seconds > 0)) this.stopMusic();
      const audio = this.media(file), v = { audio, key, gain: seconds > 0 ? 0 : gain, playing: false };
      audio.loop = key !== 'clear'; this.music = audio; this.musicKey = key; this.musicGain = gain;
      this.musicVoices.add(v); this.syncMusicVolumes();
      audio.addEventListener('playing', () => {
        if (this.music !== audio || !this.musicVoices.has(v)) return;
        v.playing = true;
        for (const old of this.musicVoices) if (old !== v) this._rampMusic(old, 0, seconds, true);
        this._rampMusic(v, this.musicGain, seconds);
      }, { once: true });
      this.start(audio, 'music:' + key);
    },
    stopMusic() {
      if (this._musicFrame != null) root.cancelAnimationFrame(this._musicFrame);
      this._musicFrame = null; this._pending = null;
      for (const v of this.musicVoices) v.audio.pause(); this.musicVoices.clear();
      this.music = null; this.musicKey = null; this.musicGain = 1;
    },
  };
  root.addEventListener('blur', () => { A.suspended = true; A.stopEffects(); });
  root.addEventListener('focus', () => { A.suspended = false; });
  document.addEventListener('visibilitychange', () => { A.suspended = document.hidden; if (document.hidden) A.stopEffects(); });
}(window));
