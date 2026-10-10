/*
 * Top-down engine core: fixed 60 Hz step, 6-button input, sound, the solid map, line of sight,
 * a flow-field for pursuit, camera and particles. Speeds are pixels per 60 Hz frame - the unit the
 * Genesis research measured in (Granada tank ~2.0, heavy shell ~15.6, Mercs rifle ~5.7).
 */
(function (root) {
  'use strict';
  const TD = root.TD = root.TD || {};
  TD.VW = 480; TD.VH = 360; TD.HZ = 60;

  // ------------------------------------------------------------------ math
  const M = TD.M = {
    clamp: (v, a, b) => v < a ? a : v > b ? b : v,
    lerp: (a, b, t) => a + (b - a) * t,
    wrap: a => { while (a > Math.PI) a -= Math.PI * 2; while (a < -Math.PI) a += Math.PI * 2; return a; },
    dist: (ax, ay, bx, by) => Math.hypot(bx - ax, by - ay),
    // the engine's heading convention is the Razorback's: a=0 faces SOUTH (+y), forward = (-sin a, cos a)
    fwd: (a) => [-Math.sin(a), Math.cos(a)],
    angTo: (ax, ay, bx, by) => Math.atan2(-(bx - ax), by - ay),
    rnd: (a, b) => a + Math.random() * (b - a),
  };
  M.turnTo = (a, target, rate) => { const d = M.wrap(target - a); return Math.abs(d) <= rate ? target : a + Math.sign(d) * rate; };

  // Stick-free six-button controls. Movement and firing direction are independent.
  const BIND = TD.BIND = {
    up:['arrowup','w'],down:['arrowdown','s'],left:['arrowleft','a'],right:['arrowright','d'],
    A:['j','z'],B:['k','x'],C:['l','c','shift'],X:['h','v',' '],Y:['u'],retina:['i','n'],
    aimLeft:['q'],aimRight:['e'],back:['b','escape'],help:['f1','?'],setup:['f2'],start:['enter','p'],
    reload:['r'],prone:['f'],tapWall:['t'],crash:['g'],exitVehicle:['o'],swap:['tab'],
  };
  const keys = {}, pointer = {active:false,x:0,y:0,buttons:{}}, screen=document.getElementById('screen');
  root.addEventListener('keydown',e=>{const k=e.key.toLowerCase();keys[k]=true;if(k.startsWith('arrow')||[' ','f1','f2'].includes(k))e.preventDefault();TD.Audio.unlock();});
  root.addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;});
  root.addEventListener('blur',()=>{for(const k in keys)keys[k]=false;pointer.buttons={};pointer.active=false;});
  function locate(e){const r=screen.getBoundingClientRect();pointer.x=(e.clientX-r.left)*TD.VW/r.width;pointer.y=(e.clientY-r.top)*TD.VH/r.height;pointer.active=pointer.x>=0&&pointer.y>=0&&pointer.x<TD.VW&&pointer.y<TD.VH;}
  screen.addEventListener('pointermove',locate);
  screen.addEventListener('pointerdown',e=>{locate(e);pointer.buttons[e.button]=true;TD.Audio.unlock();e.preventDefault();});
  root.addEventListener('pointerup',e=>{delete pointer.buttons[e.button];});
  screen.addEventListener('pointerleave',()=>{pointer.active=false;});
  screen.addEventListener('contextmenu',e=>e.preventDefault());
  const DEFAULT_PAD={A:0,B:1,C:5,X:2,Y:3,Z:4,mode:8,start:9};
  const SETUP_STEPS=['up','down','left','right','A','B','C','X','Y','Z','mode','start'];
  let wheel=0;root.addEventListener('wheel',e=>{wheel+=Math.sign(e.deltaY);},{passive:true});
  let queuedClick=false;screen.addEventListener("pointerdown",e=>{if(e.button===0)queuedClick=true;});
  let activePad=null, profile=DEFAULT_PAD, saved={}, previousId=null;
  try{saved=JSON.parse(localStorage.getItem('bof_td_controllers')||'{}');}catch(e){}
  const Input=TD.Input={
    state:{},last:{},pointer,setup:null,padId:null,
    beginSetup(){this.setup={i:0,bindings:{},neutral:false,done:false};},
    update(){
      const pads=root.navigator.getGamepads?root.navigator.getGamepads():[];
      activePad=Array.from(pads).find(p=>p&&p.connected!==false)||null;
      this.padId=activePad?activePad.id:null;
      if(this.padId!==previousId){profile=saved[this.padId]||DEFAULT_PAD;previousId=this.padId;}
      const held=i=>!!(activePad&&activePad.buttons[i]&&activePad.buttons[i].pressed);
      const mapped=name=>{const b=profile[name];return typeof b==='number'?held(b):b&&b.axis!=null?((activePad.axes[b.axis]||0)*b.sign>.55):false;};
      this.last=this.state;const s={};for(const a in BIND)s[a]=BIND[a].some(k=>keys[k]);
      if(this.setup){
        if(this.setup.done)s.start||=mapped("start");
        const q=this.setup;
        if(s.back){this.setup=null;this.state=s;return;}
        if(activePad&&!q.done){
          const buttons=activePad.buttons.map((b,i)=>b.pressed?i:-1).filter(i=>i>=0);
          const axes=activePad.axes.map((v,i)=>Math.abs(v)>.65&&Math.abs(v)<=1?{axis:i,sign:Math.sign(v)}:null).filter(Boolean);
          // Hat axes often rest at >1. Ignore those; mapped D-pad buttons remain supported.
          if(!buttons.length&&!axes.length)q.neutral=true;
          else if(q.neutral){const move=q.i<4, binding=buttons.length===1?buttons[0]:move&&axes.length===1?axes[0]:null;
            if(binding!=null){q.bindings[SETUP_STEPS[q.i++]]=binding;q.neutral=false;
              if(q.i===SETUP_STEPS.length){profile=q.bindings;saved[activePad.id]=profile;try{localStorage.setItem('bof_td_controllers',JSON.stringify(saved));}catch(e){}q.done=true;}
            }
          }
        }
        this.state=s;return;
      }
      const menu=!TD.game||TD.game.state!=='play',mode=mapped('mode');
      if(activePad){
        if(activePad.buttons[12]?.pressed||mapped('up'))s.up=true;
        if(activePad.buttons[13]?.pressed||mapped('down'))s.down=true;
        if(activePad.buttons[14]?.pressed||mapped('left'))s.left=true;
        if(activePad.buttons[15]?.pressed||mapped('right'))s.right=true;
        // Default M30 X-input D-pad can emulate the left stick. Learned profiles take precedence.
        if(profile===DEFAULT_PAD){const ax=activePad.axes[0]||0,ay=activePad.axes[1]||0;if(ax<-.35)s.left=true;if(ax>.35)s.right=true;if(ay<-.35)s.up=true;if(ay>.35)s.down=true;}
        if(mapped('start'))s.start=true;
        if(menu){s.A||=mapped('A');s.back||=mapped('B')||mode;s.setup||=mode&&mapped('start');}
        else{
          const foot=TD.game.player?.onfoot;
          if(mode){s.C=!foot||s.C;s.Y||=!foot&&mapped('Z');s.reload||=foot&&mapped('A');s.prone||=foot&&mapped('X');s.tapWall||=foot&&mapped('Y');s.swap||=foot&&mapped('B');s.crash||=foot&&mapped('C');s.exitVehicle||=!foot&&mapped('B');}
          const dx=(mapped('B')?1:0)-(mapped('Y')?1:0),dy=(mapped('A')?1:0)-(mapped('X')?1:0);
          if(!mode&&(dx||dy)){s.aim=[dx,dy];s.A=true;s.directionalFire=true;}
          s.X||=mapped('C');if(!mode){if(foot)s.Y||=mapped('Z');else s.retina||=mapped('Z');}
        }
        if(Object.values(s).some(Boolean))TD.Audio.unlock();
      }
      s.wheel=wheel;wheel=0;s.click=!!pointer.buttons[0]||queuedClick;queuedClick=false;if(pointer.buttons[0])s.A=true;
      if(pointer.buttons[2])s.X=true;if(pointer.buttons[1])s.Y=true;
      s.padActive=!!activePad&&(!!s.aim||!!s.up||!!s.down||!!s.left||!!s.right||mapped("Z")||mapped("C"));
      this.state=s;
    },
    down(a){return !!this.state[a];},tap(a){return !!this.state[a]&&!this.last[a];},released(a){return !this.state[a]&&!!this.last[a];},
    dir(){const s=this.state;return[(s.right?1:0)-(s.left?1:0),(s.down?1:0)-(s.up?1:0)];},
    aim(p){if(this.state.aim)return TD.M.angTo(0,0,...this.state.aim);if(pointer.active&&!this.state.padActive)return TD.M.angTo(p.x,p.y,pointer.x/TD.Cam.zoom+TD.Cam.x,pointer.y/TD.Cam.zoom+TD.Cam.y);return null;},
    confirm(){return this.tap('A')||this.tap('start');},
    setupLabel(){return this.setup?.done?'SAVED - RELEASE START, THEN PRESS START':!activePad?'CONNECT YOUR CONTROLLER':('PRESS '+SETUP_STEPS[this.setup?.i||0].toUpperCase());},
  };

  // ------------------------------------------------------------------ audio (BOF's own samples)
  // Every key has a retrigger gate: an ungated sample fired by many units is the beeping this
  // project has been chasing for months (0912j). HTMLAudio only - no WebAudio graph, so it plays
  // from file:// (0918: a media element routed through WebAudio is silent there).
  const SFX = {
    mg: ['nsp_bof2_shot.mp3', 0.30, 0.05], cannon: ['nsp_bof2_charge_shot.mp3', 0.70, 0.08], eshot: ['enemyShoot.mp3', 0.30, 0.07],
    hit: ['hit.mp3', 0.45, 0.04], expS: ['expSmall.mp3', 0.75, 0.04], expB: ['expBig.mp3', 0.85, 0.07], pick: ['nsp_bof2_pickup.mp3', 0.6, 0.05],
    blip: ['nsp_console_beep.mp3', 0.45, 0.06], alert: ['nsp_alert_critical.mp3', 0.8, 1.2], warn: ['nsp_bof2_boss_warning.mp3', 0.8, 2.0],
    laser: ['nsp_heavy_laser.mp3', 0.45, 0.12], missile: ['nsp_rocket_launch.mp3', 0.5, 0.12], lock: ['nsp_nav_lock.mp3', 0.5, 0.2],
    charge: ['retina_charge.mp3', 0.55, 0.5], intro: ['nsp_bof2_stage_intro.mp3', 0.7, 1.0], phase: ['bossPhase.mp3', 0.8, 0.5],
    whiteout: ['nsp_bof2_ultra_blast.mp3', 0.8, 1.0], engine: ['nsp_engine_loop.mp3', 0.0, 0],
  };
  const MUSIC = {
    level2: 'assets/game/shared/audio/music/Unused1.mp3', boss2: 'assets/game/shared/audio/music/Unused11.mp3',
    clear: 'assets/game/shared/audio/music/Password_StageClear.mp3', title: 'assets/game/shared/audio/music/Unused10.mp3',
  };
  const Audio = TD.Audio = {
    on: false, vol: 0.8, mvol: 0.55, pools: {}, lastT: {}, music: null, musicKey: null,
    unlock() { if (this.on) return; this.on = true; if (this._pending) { const k = this._pending; this._pending = null; this.playMusic(k); } },
    play(k, gain) {
      const d = SFX[k]; if (!d || !this.on) return;
      const now = performance.now() / 1000; if (now - (this.lastT[k] || -9) < d[2]) return; this.lastT[k] = now;
      let pool = this.pools[k];
      if (!pool) { pool = this.pools[k] = []; for (let i = 0; i < 4; i++) { const a = new root.Audio(ART.BASE + 'assets/game/shared/audio/sounds/' + d[0]); a.preload = 'auto'; pool.push(a); } pool.i = 0; }
      const a = pool[pool.i = (pool.i + 1) % pool.length];
      try { a.currentTime = 0; a.volume = M.clamp(d[1] * (gain == null ? 1 : gain) * this.vol, 0, 1); a.play().catch(() => { }); } catch (e) { }
    },
    playMusic(k) {
      if (this.musicKey === k && this.music) return;
      if (!this.on) { this._pending = k; return; }
      this.stopMusic(); const p = MUSIC[k]; if (!p) return;
      const a = new root.Audio(ART.BASE + p); a.loop = k !== 'clear'; a.volume = this.mvol; a.play().catch(() => { });
      this.music = a; this.musicKey = k;
    },
    stopMusic() { if (this.music) { this.music.pause(); this.music = null; this.musicKey = null; } },
  };

  // ------------------------------------------------------------------ the solid map
  // rects: [x0,y0,x1,y1,type]   'b' building/wall: blocks movement AND sight
  //                             'h' hedge: blocks sight, slows a tank, hides whoever is inside it
  //                             'v' pit: blocks movement, not sight
  const World = TD.World = {
    w: 800, h: 3616, rects: [], buckets: [], BK: 128, smokes: [],
    load(w, h, rects) {
      this.w = w; this.h = h; this.rects = rects.map(r => ({ x0: r[0], y0: r[1], x1: r[2], y1: r[3], t: r[4] }));
      this.buckets = []; for (let i = 0; i <= Math.ceil(h / this.BK); i++) this.buckets.push([]);
      for (const r of this.rects) for (let b = Math.floor(r.y0 / this.BK); b <= Math.floor(r.y1 / this.BK); b++) if (this.buckets[b]) this.buckets[b].push(r);
      this.smokes = []; this.navR = 14; Nav.build();
    },
    near(y0, y1) {
      const out = new Set();
      for (let b = Math.max(0, Math.floor(y0 / this.BK)); b <= Math.min(this.buckets.length - 1, Math.floor(y1 / this.BK)); b++) for (const r of this.buckets[b]) out.add(r);
      return out;
    },
    // push a circle out of every blocking rect; returns true if it touched something
    collide(o, r, blocksHedge) {
      let hit = false;
      if (o.x < r) { o.x = r; hit = true; } if (o.x > this.w - r) { o.x = this.w - r; hit = true; }
      if (o.y < r) { o.y = r; hit = true; } if (o.y > this.h - r) { o.y = this.h - r; hit = true; }
      for (const q of this.near(o.y - r, o.y + r)) {
        if (q.dead || (q.t === 'h' && !blocksHedge) || (q.t === 'd' && o.stance === 'prone')) continue;   // 'd' duct: crawl only
        const cx = M.clamp(o.x, q.x0, q.x1), cy = M.clamp(o.y, q.y0, q.y1), dx = o.x - cx, dy = o.y - cy, d2 = dx * dx + dy * dy;
        if (d2 >= r * r) continue;
        hit = true;
        if (d2 > 1e-6) { const d = Math.sqrt(d2), p = r - d; o.x += dx / d * p; o.y += dy / d * p; }
        else { // centre inside: leave by the shortest side
          const l = o.x - q.x0, rr = q.x1 - o.x, t = o.y - q.y0, bb = q.y1 - o.y, m = Math.min(l, rr, t, bb);
          if (m === l) o.x = q.x0 - r; else if (m === rr) o.x = q.x1 + r; else if (m === t) o.y = q.y0 - r; else o.y = q.y1 + r;
        }
      }
      return hit;
    },
    add(q) { this.rects.push(q); for (let b = Math.floor(q.y0 / this.BK); b <= Math.floor(q.y1 / this.BK); b++) if (this.buckets[b]) this.buckets[b].push(q); this.navDirty=true; return q; },
    remove(q) { q.dead = true; this.navDirty = true; },
    inType(x, y, t) { for (const q of this.near(y, y)) if (!q.dead && q.t === t && x >= q.x0 && x <= q.x1 && y >= q.y0 && y <= q.y1) return q; return null; },
    solidAt(x, y) { if (x < 0 || y < 0 || x > this.w || y > this.h) return true; for (const q of this.near(y, y)) if (!q.dead && q.t === 'b' && x >= q.x0 && x <= q.x1 && y >= q.y0 && y <= q.y1) return true; return false; },
    // line of sight: buildings and hedges block; so does smoke. A viewer standing INSIDE a hedge sees out of it.
    los(ax, ay, bx, by) {
      for (const q of this.near(Math.min(ay, by), Math.max(ay, by))) {
        if (q.dead) continue;
        if (q.t === 'v') continue;
        if ((q.t === 'h' || q.t === 'd') && ((ax >= q.x0 && ax <= q.x1 && ay >= q.y0 && ay <= q.y1) || (bx >= q.x0 && bx <= q.x1 && by >= q.y0 && by <= q.y1))) continue;
        if (segRect(ax, ay, bx, by, q)) return false;
      }
      for (const s of this.smokes) if (segCircle(ax, ay, bx, by, s.x, s.y, s.r * Math.min(1, s.t / 0.6))) return false;
      return true;
    },
    // a projectile path: buildings only (rounds fly over hedges and pits)
    rayBlock(ax, ay, bx, by) { for (const q of this.near(Math.min(ay, by), Math.max(ay, by))) if (!q.dead && q.t === 'b' && segRect(ax, ay, bx, by, q)) return true; return false; },
  };
  function segRect(ax, ay, bx, by, q) {
    let t0 = 0, t1 = 1; const dx = bx - ax, dy = by - ay;
    const P = [-dx, dx, -dy, dy], Q = [ax - q.x0, q.x1 - ax, ay - q.y0, q.y1 - ay];
    for (let i = 0; i < 4; i++) {
      if (P[i] === 0) { if (Q[i] < 0) return false; continue; }
      const t = Q[i] / P[i];
      if (P[i] < 0) { if (t > t1) return false; if (t > t0) t0 = t; } else { if (t < t0) return false; if (t < t1) t1 = t; }
    }
    return true;
  }
  function segCircle(ax, ay, bx, by, cx, cy, r) {
    const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1, t = M.clamp(((cx - ax) * dx + (cy - ay) * dy) / l2, 0, 1);
    const px = ax + dx * t - cx, py = ay + dy * t - cy; return px * px + py * py < r * r;
  }

  // ------------------------------------------------------------------ flow field (pursuit / search)
  const Nav = TD.Nav = {
    C: 24, cols: 0, rows: 0, walk: null, fields: {},
    build() {
      const C = this.C; this.cols = Math.ceil(World.w / C); this.rows = Math.ceil(World.h / C);
      this.walk = new Uint8Array(this.cols * this.rows);
      for (let r = 0; r < this.rows; r++) for (let c = 0; c < this.cols; c++) {
        const x = c * C + C / 2, y = r * C + C / 2; let ok = 1;
        const R = World.navR;   // clearance: 14 for tanks; an infantry mission narrows it (museum galleries)
        for (const q of World.near(y - R, y + R)) if (!q.dead && (q.t === 'b' || q.t === 'v' || q.t === 'd') && x + R > q.x0 && x - R < q.x1 && y + R > q.y0 && y - R < q.y1) { ok = 0; break; }
        this.walk[r * this.cols + c] = ok;
      }
      this.fields = {};
    },
    // distances from a goal, BFS, cached per goal cell for a short while
    field(gx, gy, t) {
      const C = this.C, gc = M.clamp(Math.floor(gx / C), 0, this.cols - 1), gr = M.clamp(Math.floor(gy / C), 0, this.rows - 1), id = gr * this.cols + gc;
      const f = this.fields[id]; if (f && t - f.t < 0.5) return f;
      const D = new Int32Array(this.cols * this.rows).fill(-1), q = new Int32Array(this.cols * this.rows); let h = 0, tl = 0;
      D[id] = 0; q[tl++] = id;
      while (h < tl) {
        const i = q[h++], c = i % this.cols, r = (i / this.cols) | 0;
        for (const [dc, dr] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nc = c + dc, nr = r + dr; if (nc < 0 || nr < 0 || nc >= this.cols || nr >= this.rows) continue;
          const j = nr * this.cols + nc; if (D[j] >= 0 || !this.walk[j]) continue; D[j] = D[i] + 1; q[tl++] = j;
        }
      }
      const out = { t, D };
      const ks = Object.keys(this.fields); if (ks.length > 24) delete this.fields[ks[0]];
      return (this.fields[id] = out);
    },
    // the direction one step downhill from (x,y)
    step(f, x, y) {
      const C = this.C, c = M.clamp(Math.floor(x / C), 0, this.cols - 1), r = M.clamp(Math.floor(y / C), 0, this.rows - 1);
      let best = f.D[r * this.cols + c], bx = 0, by = 0;
      if (best < 0) best = 1e9;
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
        if (!dr && !dc) continue; const nc = c + dc, nr = r + dr; if (nc < 0 || nr < 0 || nc >= this.cols || nr >= this.rows) continue;
        const d = f.D[nr * this.cols + nc]; if (d < 0) continue;
        if (dr && dc && (!this.walk[r * this.cols + nc] || !this.walk[nr * this.cols + c])) continue;
        if (d < best) { best = d; bx = dc; by = dr; }
      }
      return (bx || by) ? [nx(c + bx) - x, nx(r + by) - y] : null;
      function nx(i) { return i * C + C / 2; }
    },
  };

  // ------------------------------------------------------------------ camera
  const Cam = TD.Cam = {
    x: 0, y: 0, shake: 0, zoom: 1, minY: 0, maxY: 1e9, minX: 0,
    follow(tx, ty, k) {
      const vw = TD.VW / this.zoom, vh = TD.VH / this.zoom;
      this.x += (tx - vw / 2 - this.x) * k; this.y += (ty - vh / 2 - this.y) * k;
      this.x = vw > World.w ? (World.w - vw) / 2 : M.clamp(this.x, Math.max(0, this.minX), Math.max(0, World.w - vw));
      this.y = M.clamp(this.y, Math.max(0, this.minY), Math.max(0, Math.min(World.h, this.maxY) - vh));
    },
    kick(n) { this.shake = Math.max(this.shake, n); },
  };

  // ------------------------------------------------------------------ particles: authored reels only
  const FX = TD.FX = {
    list: [],
    // explosion: an 8-frame nxp_ reel played once
    boom(x, y, size, kind, n) {
      const fam = kind || (size > 70 ? 'nxp_dense_' : 'nxp_clus_');
      this.list.push({ k: 'reel', fam, n: n || 8, x, y, t: 0, life: 0.5 + size / 300, s: size / 200, a: Math.random() * 6.28 });
    },
    smoke(x, y, s, life, vx, vy) { this.list.push({ k: 'img', key: 'rzb_dust', x, y, vx: vx || 0, vy: vy || 0, t: 0, life: life || 1.2, s: s || 0.25, a: Math.random() * 6.28, fade: 1, grow: 0.6 }); },
    debris(x, y, s) { this.list.push({ k: 'img', key: 'rzb_debris', x, y, vx: 0, vy: 0, t: 0, life: 0.7, s: s || 0.3, a: Math.random() * 6.28, fade: 1, grow: 0.5 }); },
    fragment(key, x, y, a, s, vx, vy, anchor) {
      this.list.push({ k: 'fragment', key, x, y, a, s, vx, vy, ax: anchor && anchor[0], ay: anchor && anchor[1],
        t: 0, life: 1.5, z: 0, vz: 105, spin: M.rnd(-8, 8), concrete: key.includes('concrete') });
    },
    concrete(x, y, size) {
      this.list.push({ k: 'reel', fam: 'concrete_break_', n: 4, x, y, t: 0, life: 0.45, s: size / 192, a: Math.random() * 6.28 });
      this.list.push({ k: 'reel', fam: 'concrete_dust_', n: 4, x, y, t: 0, life: 1.1, s: size / 160, a: Math.random() * 6.28 });
    },
    casing(x, y, a) {
      const [fx, fy] = M.fwd(a + Math.PI / 2), sp = M.rnd(1.2, 2.2);
      this.list.push({ k: 'img', key: 'ndk_shell_' + ((Math.random() * 6) | 0), x, y, vx: fx * sp, vy: fy * sp, t: 0, life: 0.6, s: 0.3, a: Math.random() * 6.28, spin: M.rnd(-0.4, 0.4), drag: 0.9 });
    },
    flash(x, y, a, s) { this.list.push({ k: 'reel', fam: 'gfx_muzzle_', n: 6, x, y, t: 0, life: 0.14, s: (s || 0.18) * 1.6, a: a + Math.PI, ay: 0.8 }); },
    ring(x, y, s, key) { this.list.push({ k: 'img', key: key || 'rzb_sonic_ring', x, y, vx: 0, vy: 0, t: 0, life: 0.35, s: s * 0.4, a: 0, fade: 1, grow: 2.2 }); },
    update(dt) {
      for (const p of this.list) {
        if (p.k === 'fragment') {
          p.t += dt; p.x += p.vx * dt; p.y += p.vy * dt; p.a += p.spin * dt;
          p.z += p.vz * dt; p.vz -= 300 * dt;
          if (p.z < 0 && p.t > 0.2) {
            p.z = 0;
            if (Math.abs(p.vz) > 35 && !p.bounced) { p.vz *= -0.25; p.vx *= 0.55; p.vy *= 0.55; p.bounced = true; }
            else { p.t = p.life; if (TD.game) TD.game.wrecks.push({ x: p.x, y: p.y, a: p.a, art: p.key, s: p.s, ax: p.ax, ay: p.ay, fragment: true }); }
          }
          continue;
        }
        p.t += dt; if (p.vx != null) { p.x += p.vx; p.y += p.vy; if (p.drag) { p.vx *= p.drag; p.vy *= p.drag; } }
        if (p.spin) p.a += p.spin;
      }
      this.list = this.list.filter(p => p.t < p.life);
    },
    draw(ctx, layer) {
      for (const p of this.list) {
        if ((p.key === 'rzb_dust' || p.fam === 'concrete_dust_' ? 0 : 1) !== layer) continue;
        if (p.k === 'fragment') {
          ART.draw(ctx, p.key, p.x + 3, p.y + 4, { s: p.s, a: p.a, ax: p.ax, ay: p.ay, tint: '#000000', alpha: 0.3 });
          ART.draw(ctx, p.key, p.x, p.y - p.z, { s: p.s, a: p.a, ax: p.ax, ay: p.ay }); continue;
        }
        const q = p.t / p.life;
        if (p.k === 'reel') { const key = p.fam + Math.min(p.n - 1, (q * p.n) | 0); ART.draw(ctx, key, p.x, p.y, { s: p.s, a: p.a, ay: p.ay != null ? (ART.size(key) || [0, 0])[1] * p.ay : null }); }
        else ART.draw(ctx, p.key, p.x, p.y, { s: p.s * (1 + (p.grow || 0) * q), a: p.a, alpha: p.fade ? (1 - q) * (p.key === 'rzb_dust' ? 0.85 : 1) : 1, ay: p.ay != null ? (ART.size(p.key) || [0, 0])[1] * p.ay : null });
      }
    },
  };
}(window));
