/* ============================================================
   ColeForge — the animated smithy.
   A 160x120 pixel scene drawn with hard-edged rects, scaled up
   by CSS. Everything here is decoration: if it never runs, the
   downloader still works.
   ============================================================ */
'use strict';

const Forge = (() => {

  const W = 160;
  const H = 120;

  const PAL = {
    K: '#0a0810',  // outline
    D: '#3a3350',  // dark iron
    M: '#5a5478',  // mid iron
    L: '#8d87b3',  // light iron
    W: '#dcd7f0',  // highlight
    H: '#8a5a2b',  // handle
    h: '#5c3a18',  // handle shadow
    S: '#8d87b3',  // steel
    s: '#5a5478',  // steel shadow
    B: '#6b4423',  // wood
    G: '#ffa629',  // gold
    Y: '#7a1f0d',  // keyhole
    C: '#3a3350',  // cartridge shell
    T: '#c93c11',  // label tint
    P: '#ffdd66',  // contacts
  };

  /* ---------- sprite helper: ascii rows -> rect list ---------- */

  function sprite(rows) {
    const cells = [];
    rows.forEach((row, y) => {
      for (let x = 0; x < row.length; x++) {
        const ch = row[x];
        if (ch !== '.') cells.push([x, y, ch]);
      }
    });
    return { w: rows[0].length, h: rows.length, cells };
  }

  function draw(ctx, spr, ox, oy, tint) {
    for (const [x, y, ch] of spr.cells) {
      ctx.fillStyle = (tint && tint[ch]) || PAL[ch] || '#f0f';
      ctx.fillRect(ox + x, oy + y, 1, 1);
    }
  }

  const ANVIL = sprite([
    '..........KKKKKKKKKKKKKKKKKK..',
    '....KKKKKKLLLLLLLLLLLLLLLLLK..',
    '..KKLLLLLLMMMMMMMMMMMMMMMMMK..',
    '.KLLLMMMMMMMMMMMMMMMMMMMMMMK..',
    '.KMMMMMMMMMMMMMMMMMMMMMMMMMK..',
    '..KKKMMMMMMMMMMMMMMMMMMMMMK...',
    '....KKDDDDDDDDDDDDDDDDDDDK....',
    '........KDDDDDDDDDDDDDK.......',
    '..........KDDDDDDDDK..........',
    '..........KDDDDDDDDK..........',
    '..........KDDDDDDDDK..........',
    '.........KDDDDDDDDDDK.........',
    '........KDDDDDDDDDDDDK........',
    '......KKDDDDDDDDDDDDDDKK......',
    '....KKMMMMMMMMMMMMMMMMMMKK....',
    '....KKKKKKKKKKKKKKKKKKKKKK....',
  ]);

  const HAMMER = sprite([
    '.................KK.',
    '................KHK.',
    '...............KHHK.',
    '..............KHHK..',
    '.............KHHK...',
    '............KHHK....',
    '...........KHHK.....',
    '..........KHHK......',
    '.........KHHK.......',
    '........KHHK........',
    '.......KHhK.........',
    '......KHhK..........',
    '.KKKKKHhKKKK........',
    '.KSSSSSSSSSK........',
    '.KSSSSSSSSSK........',
    '.KSSSSSSSSSK........',
    '.KsssssssssK........',
    '.KsssssssssK........',
    '.KKKKKKKKKKK........',
    '....................',
  ]);

  const CHEST = sprite([
    '..KKKKKKKKKKKKKKKKKK..',
    '.KWWWWWWWWWWWWWWWWWWK.',
    'KBBBBBBBBBBBBBBBBBBBBK',
    'KBBBBBBBBGGGGBBBBBBBBK',
    'KBBBBBBBBGYYGBBBBBBBBK',
    'KKKKKKKKKGGGGKKKKKKKKK',
    'KBBBBBBBBBGGBBBBBBBBBK',
    'KBWWBBBBBBBBBBBBBBWWBK',
    'KBWWBBBBBBBBBBBBBBWWBK',
    'KBBBBBBBBBBBBBBBBBBBBK',
    'KBBBBBBBBBBBBBBBBBBBBK',
    'KBWWBBBBBBBBBBBBBBWWBK',
    'KBWWBBBBBBBBBBBBBBWWBK',
    'KBBBBBBBBBBBBBBBBBBBBK',
    '.KBBBBBBBBBBBBBBBBBBK.',
    '..KKKKKKKKKKKKKKKKKK..',
  ]);

  const CARTRIDGE = sprite([
    '.KKKKKKKKKKKKKK.',
    'KCCCCCCCCCCCCCCK',
    'KCLLLLLLLLLLLLCK',
    'KCLTTTTTTTTTTLCK',
    'KCLTTTTTTTTTTLCK',
    'KCLLLLLLLLLLLLCK',
    'KCCCCCCCCCCCCCCK',
    'KCPPCCCCCCCCPPCK',
    'KCPPCCCCCCCCPPCK',
    'KCCCCCCCCCCCCCCK',
    '.KCCCCCCCCCCCCK.',
    '..KKKKKKKKKKKK..',
  ]);

  /* ---------- scene geometry ---------- */

  const FLOOR_Y   = 100;
  const ANVIL_X   = 58;
  const ANVIL_Y   = 70;
  const INGOT_X   = 66;
  const INGOT_Y   = 66;
  const INGOT_W   = 16;
  const INGOT_H   = 4;
  const HAMMER_X  = 62;
  const HAMMER_REST   = 28;   // sprite top y when raised
  const HAMMER_STRUCK = 47;   // sprite top y at impact
  const FURNACE = { x: 6, y: 34, w: 46, h: 66 };
  const CHEST_X = 122;
  const CHEST_Y = 84;

  /* ---------- heat ramp ---------- */

  const HEAT_STOPS = [
    [0.00, [0x5a, 0x54, 0x78]],
    [0.22, [0x7a, 0x1f, 0x0d]],
    [0.48, [0xc9, 0x3c, 0x11]],
    [0.72, [0xf2, 0x6a, 0x1b]],
    [0.90, [0xff, 0xa6, 0x29]],
    [1.00, [0xff, 0xf3, 0xc4]],
  ];

  function heatColor(t) {
    t = Math.max(0, Math.min(1, t));
    for (let i = 1; i < HEAT_STOPS.length; i++) {
      const [p1, c1] = HEAT_STOPS[i - 1];
      const [p2, c2] = HEAT_STOPS[i];
      if (t <= p2) {
        const k = p2 === p1 ? 0 : (t - p1) / (p2 - p1);
        const r = Math.round(c1[0] + (c2[0] - c1[0]) * k);
        const g = Math.round(c1[1] + (c2[1] - c1[1]) * k);
        const b = Math.round(c1[2] + (c2[2] - c1[2]) * k);
        return `rgb(${r},${g},${b})`;
      }
    }
    return '#fff3c4';
  }

  /* ---------- state ---------- */

  const state = {
    canvas: null,
    ctx: null,
    mode: 'idle',        // idle | forging | done | failed
    progress: 0,         // 0..1
    intensity: 0.5,      // strike tempo, 0..1
    t: 0,
    hammerPhase: 0,
    shake: 0,
    sparks: [],
    smoke: [],
    motes: [],
    running: false,
    onStrike: null,
    lastFrame: 0,
  };

  function rnd(a, b) { return a + Math.random() * (b - a); }

  function spawnSparks(n) {
    for (let i = 0; i < n; i++) {
      state.sparks.push({
        x: INGOT_X + rnd(0, INGOT_W),
        y: INGOT_Y + rnd(-1, 2),
        vx: rnd(-52, 52),
        vy: rnd(-64, -18),
        life: rnd(0.35, 0.95),
        age: 0,
      });
    }
  }

  function spawnSmoke() {
    state.smoke.push({
      x: rnd(FURNACE.x + 10, FURNACE.x + FURNACE.w - 10),
      y: FURNACE.y + 40,
      vy: rnd(-14, -7),
      vx: rnd(-5, 5),
      life: rnd(1.4, 2.6),
      age: 0,
    });
  }

  /* ---------- background ---------- */

  function drawWall(ctx) {
    ctx.fillStyle = '#1a1726';
    ctx.fillRect(0, 0, W, FLOOR_Y);

    // brick courses
    const bh = 8, bw = 20;
    for (let row = 0, y = 0; y < FLOOR_Y; row++, y += bh) {
      const offset = (row % 2) * (bw / 2);
      ctx.fillStyle = '#221e33';
      ctx.fillRect(0, y, W, 1);
      for (let x = -bw; x < W + bw; x += bw) {
        ctx.fillRect(x + offset, y, 1, bh);
      }
    }

    // floor
    ctx.fillStyle = '#15121f';
    ctx.fillRect(0, FLOOR_Y, W, H - FLOOR_Y);
    ctx.fillStyle = '#0f0d18';
    for (let x = 0; x < W; x += 12) ctx.fillRect(x, FLOOR_Y, 1, H - FLOOR_Y);
    ctx.fillStyle = '#262238';
    ctx.fillRect(0, FLOOR_Y, W, 1);
  }

  function drawFurnace(ctx, heat) {
    const f = FURNACE;

    // stone housing
    ctx.fillStyle = '#0a0810';
    ctx.fillRect(f.x - 2, f.y - 2, f.w + 4, f.h + 2);
    ctx.fillStyle = '#3a3350';
    ctx.fillRect(f.x, f.y, f.w, f.h);
    ctx.fillStyle = '#262238';
    ctx.fillRect(f.x + 2, f.y + 2, f.w - 4, f.h - 4);

    // arched mouth
    const mx = f.x + 7, my = f.y + 10, mw = f.w - 14, mh = 34;
    ctx.fillStyle = '#0a0810';
    ctx.fillRect(mx, my + 4, mw, mh);
    ctx.fillRect(mx + 3, my, mw - 6, 6);
    ctx.fillRect(mx + 6, my - 3, mw - 12, 5);

    if (heat <= 0.02) {
      // dead coals
      ctx.fillStyle = '#2a2438';
      ctx.fillRect(mx + 2, my + mh - 6, mw - 4, 5);
      return;
    }

    // flame field: per-column height from layered sines
    const t = state.t;
    const base = 10 + heat * 20;
    for (let i = 0; i < mw - 4; i++) {
      const x = mx + 2 + i;
      const n =
        Math.sin(i * 0.55 + t * 5.5) * 0.5 +
        Math.sin(i * 0.23 - t * 3.1) * 0.35 +
        Math.sin(i * 1.10 + t * 8.0) * 0.15;
      const edge = 1 - Math.abs((i - (mw - 4) / 2) / ((mw - 4) / 2)) * 0.55;
      const hgt = Math.max(2, (base + n * 9 * heat) * edge);
      const top = my + mh - 2 - hgt;

      ctx.fillStyle = '#7a1f0d';
      ctx.fillRect(x, top, 1, hgt);
      ctx.fillStyle = '#c93c11';
      ctx.fillRect(x, top + hgt * 0.28, 1, hgt * 0.72);
      ctx.fillStyle = '#f26a1b';
      ctx.fillRect(x, top + hgt * 0.55, 1, hgt * 0.45);
      ctx.fillStyle = '#ffa629';
      ctx.fillRect(x, my + mh - 2 - hgt * 0.28, 1, hgt * 0.28);
      if (n > 0.55) { ctx.fillStyle = '#ffdd66'; ctx.fillRect(x, top - 1, 1, 2); }
    }

    // coal bed
    ctx.fillStyle = '#ffdd66';
    ctx.fillRect(mx + 2, my + mh - 3, mw - 4, 2);
    ctx.fillStyle = '#fff3c4';
    for (let i = 0; i < 5; i++) {
      const x = mx + 4 + ((i * 7 + Math.floor(t * 3) % 5) % (mw - 8));
      ctx.fillRect(x, my + mh - 3, 2, 1);
    }

    // glow spill on the floor
    ctx.fillStyle = `rgba(242,106,27,${0.10 + heat * 0.14})`;
    ctx.fillRect(f.x - 4, FLOOR_Y, f.w + 20, 6);
  }

  function drawStump(ctx) {
    ctx.fillStyle = '#0a0810';
    ctx.fillRect(64, 86, 20, 15);
    ctx.fillStyle = '#5c3a18';
    ctx.fillRect(65, 86, 18, 14);
    ctx.fillStyle = '#6b4423';
    ctx.fillRect(66, 86, 15, 13);
    ctx.fillStyle = '#4a2e13';
    ctx.fillRect(69, 89, 2, 10);
    ctx.fillRect(75, 91, 2, 8);
  }

  function drawIngot(ctx, heat, lift) {
    const y = INGOT_Y - lift;
    const c = heatColor(heat);

    ctx.fillStyle = '#0a0810';
    ctx.fillRect(INGOT_X - 1, y - 1, INGOT_W + 2, INGOT_H + 2);
    ctx.fillStyle = c;
    ctx.fillRect(INGOT_X, y, INGOT_W, INGOT_H);

    // hot top edge
    ctx.fillStyle = heatColor(Math.min(1, heat + 0.22));
    ctx.fillRect(INGOT_X, y, INGOT_W, 1);
    ctx.fillStyle = heatColor(Math.max(0, heat - 0.25));
    ctx.fillRect(INGOT_X, y + INGOT_H - 1, INGOT_W, 1);

    // radiant halo once it is genuinely hot
    if (heat > 0.35) {
      ctx.fillStyle = `rgba(242,106,27,${(heat - 0.35) * 0.45})`;
      ctx.fillRect(INGOT_X - 3, y - 3, INGOT_W + 6, INGOT_H + 6);
    }
  }

  function drawHammer(ctx, y) {
    draw(ctx, HAMMER, HAMMER_X, y);
  }

  function drawChest(ctx, glow) {
    draw(ctx, CHEST, CHEST_X, CHEST_Y);
    if (glow > 0) {
      ctx.fillStyle = `rgba(255,221,102,${glow * 0.5})`;
      ctx.fillRect(CHEST_X + 2, CHEST_Y + 2, CHEST.w - 4, 6);
    }
  }

  function drawParticles(ctx) {
    for (const s of state.sparks) {
      const k = 1 - s.age / s.life;
      ctx.fillStyle = k > 0.66 ? '#fff3c4' : k > 0.33 ? '#ffa629' : '#c93c11';
      ctx.fillRect(Math.round(s.x), Math.round(s.y), 1, 1);
    }
    for (const m of state.smoke) {
      const k = 1 - m.age / m.life;
      ctx.fillStyle = `rgba(90,84,120,${k * 0.55})`;
      ctx.fillRect(Math.round(m.x), Math.round(m.y), 2, 2);
    }
    for (const m of state.motes) {
      const k = 1 - m.age / m.life;
      ctx.fillStyle = `rgba(255,221,102,${k})`;
      ctx.fillRect(Math.round(m.x), Math.round(m.y), 1, 1);
    }
  }

  function drawBanner(ctx, text, color) {
    const w = text.length * 4 + 6;
    const x = Math.round((W - w) / 2);
    ctx.fillStyle = 'rgba(10,8,16,0.85)';
    ctx.fillRect(x - 2, 6, w + 4, 13);
    ctx.fillStyle = color;
    ctx.fillRect(x - 2, 6, w + 4, 1);
    ctx.fillRect(x - 2, 18, w + 4, 1);
    ctx.font = '7px "Press Start 2P", monospace';
    ctx.textBaseline = 'top';
    ctx.fillText(text, x + 1, 10);
  }

  /* ---------- simulation ---------- */

  function step(dt) {
    dt = Math.min(dt, 0.05);
    state.t += dt;

    const forging = state.mode === 'forging';
    const heat = forging ? 0.35 + state.progress * 0.65
      : state.mode === 'done' ? 1
      : state.mode === 'failed' ? 0
      : 0.28;

    // hammer cycle
    if (forging) {
      const rate = 1.1 + state.intensity * 2.0;   // strikes per second
      const prev = state.hammerPhase;
      state.hammerPhase = (state.hammerPhase + dt * rate) % 1;
      if (state.hammerPhase < prev) {
        state.shake = 0.13;
        spawnSparks(10 + Math.round(state.intensity * 14));
        if (state.onStrike) state.onStrike();
      }
    } else {
      state.hammerPhase = Math.min(1, state.hammerPhase + dt * 2);
    }

    if (state.mode === 'failed' && Math.random() < dt * 6) spawnSmoke();

    if (state.mode === 'done' && Math.random() < dt * 14) {
      state.motes.push({
        x: rnd(INGOT_X - 6, INGOT_X + INGOT_W + 6),
        y: rnd(52, 70),
        vx: rnd(-6, 6),
        vy: rnd(-16, -5),
        life: rnd(0.6, 1.3),
        age: 0,
      });
    }

    state.shake = Math.max(0, state.shake - dt);

    const advance = (arr, gravity) => {
      for (let i = arr.length - 1; i >= 0; i--) {
        const p = arr[i];
        p.age += dt;
        if (p.age >= p.life) { arr.splice(i, 1); continue; }
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (gravity) p.vy += gravity * dt;
      }
    };
    advance(state.sparks, 150);
    advance(state.smoke, 0);
    advance(state.motes, 0);

    if (state.sparks.length > 400) state.sparks.length = 400;

    return heat;
  }

  function render(heat) {
    const ctx = state.ctx;
    if (!ctx) return;

    ctx.save();
    if (state.shake > 0) ctx.translate(0, Math.random() < 0.5 ? 1 : 0);

    ctx.fillStyle = '#0d0b14';
    ctx.fillRect(0, 0, W, H);

    drawWall(ctx);
    drawFurnace(ctx, state.mode === 'failed' ? 0 : state.mode === 'forging' ? 0.55 + state.progress * 0.45 : 0.4);
    drawChest(ctx, state.mode === 'done' ? 1 : 0.15);
    drawStump(ctx);
    drawIngot(ctx, heat, state.mode === 'done' ? 0 : 0);

    if (state.mode === 'done') {
      const bob = Math.round(Math.sin(state.t * 2.4) * 2);
      draw(ctx, CARTRIDGE, 66, 44 + bob);
    }

    draw(ctx, ANVIL, ANVIL_X, ANVIL_Y);

    // hammer: ease down fast, rise slow — a real swing
    const p = state.hammerPhase;
    const swing = p < 0.35
      ? Math.pow(p / 0.35, 2)          // fall
      : 1 - (p - 0.35) / 0.65;         // recover
    const hy = state.mode === 'forging'
      ? Math.round(HAMMER_REST + (HAMMER_STRUCK - HAMMER_REST) * swing)
      : HAMMER_STRUCK - 1;   // idle: laid down on the anvil, not hovering
    drawHammer(ctx, hy);

    drawParticles(ctx);

    if (state.mode === 'done')   drawBanner(ctx, 'FORGED', '#4ad66d');
    if (state.mode === 'failed') drawBanner(ctx, 'QUENCHED', '#e8324a');

    ctx.restore();
  }

  function frame(now) {
    if (!state.running) return;
    const dt = state.lastFrame ? (now - state.lastFrame) / 1000 : 1 / 60;
    state.lastFrame = now;
    render(step(dt));
    requestAnimationFrame(frame);
  }

  /* ---------- public API ---------- */

  return {
    init(canvas) {
      state.canvas = canvas;
      state.ctx = canvas.getContext('2d', { alpha: false });
      state.ctx.imageSmoothingEnabled = false;
      state.running = true;
      state.lastFrame = 0;
      requestAnimationFrame(frame);
      render(step(0));   // paint frame zero even if rAF never fires
    },

    setMode(mode) {
      if (state.mode === mode) return;
      state.mode = mode;
      if (mode === 'done') { state.motes.length = 0; spawnSparks(28); }
      if (mode === 'failed') { state.sparks.length = 0; }
      if (mode === 'idle') { state.progress = 0; state.sparks.length = 0; state.motes.length = 0; }
    },

    setProgress(p) { state.progress = Math.max(0, Math.min(1, p || 0)); },

    /** bytes/sec -> strike tempo */
    setIntensity(bytesPerSec) {
      if (!bytesPerSec) return;
      state.intensity = Math.max(0, Math.min(1, Math.log10(bytesPerSec / 1e5 + 1) / 2.6));
    },

    onStrike(fn) { state.onStrike = fn; },

    /** advance + draw a single frame; used where rAF is unavailable */
    tick(dt) { render(step(dt || 1 / 60)); },

    heatColor,

    drawLogo(canvas) {
      const ctx = canvas.getContext('2d');
      ctx.imageSmoothingEnabled = false;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // 1:1 — any fractional scale turns the sprite to mush
      draw(ctx, ANVIL, 9, 15);
      // ember rising off the anvil
      ctx.fillStyle = '#7a1f0d'; ctx.fillRect(20, 2, 9, 12);
      ctx.fillStyle = '#c93c11'; ctx.fillRect(21, 4, 7, 10);
      ctx.fillStyle = '#f26a1b'; ctx.fillRect(22, 6, 5, 8);
      ctx.fillStyle = '#ffa629'; ctx.fillRect(23, 8, 3, 6);
      ctx.fillStyle = '#ffdd66'; ctx.fillRect(24, 10, 1, 4);
    },
  };
})();
