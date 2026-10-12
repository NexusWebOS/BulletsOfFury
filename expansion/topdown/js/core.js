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
    up:['w','arrowup'],down:['s','arrowdown'],left:['a','arrowleft'],right:['d','arrowright'],
    A:['j','z'],B:['k','x'],C:['l','c','shift'],X:['h','v',' '],Y:['u'],retina:['i','n'],
    aimLeft:['q'],aimRight:['e'],back:['b','escape'],help:['f1','?'],setup:['f2'],start:['enter','p'],
    reload:['r'],boost:['r'],cruise:['f'],prone:['f'],tapWall:['t'],crash:['g'],exitVehicle:['o'],swap:['tab'],
  };
  const KEY_DEFAULTS=JSON.parse(JSON.stringify(BIND));
  try{const b=JSON.parse(localStorage.getItem('bof_od_keys')||'{}');for(const k in BIND)if(Array.isArray(b[k])&&b[k].length&&b[k].every(v=>typeof v==='string'&&v!=='backspace'))BIND[k]=b[k];}catch(e){}
  const keys = {}, pointer = {active:false,x:0,y:0,buttons:{}}, screen=document.getElementById('screen');
  let aimSource=null, previousPadAim=null;
  root.addEventListener('keydown',e=>{const k=e.key.toLowerCase();TD.Audio.unlock();if(k==='enter'&&e.altKey&&!TD.Input.rebind&&!TD.OriginalOptions?.snapshot().capture&&!TD.Frontend?.typing)return;if(TD.Input.textSink&&TD.Input.textSink(e)){e.preventDefault();return;}if(TD.Input.rebind?.kind==='key'){e.preventDefault();if(k==='escape'){TD.Input.rebind=null;return;}if(k==='backspace'||['alt','control','meta'].includes(k))return;BIND[TD.Input.rebind.action]=[k];TD.Input.saveKeys();TD.Input.rebind=null;for(const v in keys)keys[v]=false;return;}keys[k]=true;if(k.startsWith('arrow')||[' ','f1','f2','tab'].includes(k))e.preventDefault();});
  root.addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;});
  root.addEventListener('blur',()=>{for(const k in keys)keys[k]=false;pointer.buttons={};pointer.active=false;aimSource=null;});
  function locate(e){const r=screen.getBoundingClientRect(),v=TD.Display||{w:TD.VW,h:TD.VH};const x=(e.clientX-r.left)*v.w/r.width,y=(e.clientY-r.top)*v.h/r.height;const moved=Math.hypot(x-pointer.x,y-pointer.y)>.5;pointer.x=x;pointer.y=y;pointer.active=x>=0&&y>=0&&x<v.w&&y<v.h;if(pointer.active&&(moved||e.type==='pointerdown'))aimSource='mouse';}
  screen.addEventListener('pointermove',locate);
  screen.addEventListener('pointerdown',e=>{locate(e);pointer.buttons[e.button]=true;TD.Audio.unlock();e.preventDefault();});
  root.addEventListener('pointerup',e=>{delete pointer.buttons[e.button];});
  screen.addEventListener('pointerleave',()=>{pointer.active=false;});
  screen.addEventListener('contextmenu',e=>e.preventDefault());
  const DEFAULT_PAD={A:0,B:1,C:5,X:2,Y:3,Z:4,mode:8,start:9,L:6,R:7};
  const STANDARD_PAD={style:'standard',A:0,B:1,X:2,Y:3,L:4,R:5,boost:6,mode:8,start:9};
  const SETUP_STEPS=['up','down','left','right','A','B','C','X','Y','Z','mode','start','L','R'];
  let wheel=0;root.addEventListener('wheel',e=>{wheel+=Math.sign(e.deltaY);},{passive:true});
  let queuedClick=false;screen.addEventListener("pointerdown",e=>{if(e.button===0)queuedClick=true;});
  let activePad=null, profile=DEFAULT_PAD, saved={}, previousId=null,defaultStyle='six';
  try{defaultStyle=localStorage.getItem('bof_od_pad_style')||'six';if(defaultStyle==='standard')profile=STANDARD_PAD;}catch(e){}
  try{saved=JSON.parse(localStorage.getItem('bof_td_controllers')||'{}');}catch(e){}
  const Input=TD.Input={
    state:{},last:{},raw:{},lastRaw:{},pointer,setup:null,padId:null,
    rebind:null,textSink:null,combatLatch:new Set(),
    // Only physical fire inputs held at the cutscene boundary need a release.
    // Other buttons/devices remain usable, including a held Retina shoulder.
    holdCombat(){this.combatLatch.clear();for(const a of ['A','B','X','Y'])for(const k of BIND[a])if(this.raw[k])this.combatLatch.add(k);for(const a of ['A','B','C','X','Y']){const b=profile[a];const k=typeof b==='number'?'pad_'+b:b&&b.axis!=null?'pad_axis'+b.axis+'_'+(b.sign<0?'neg':'pos'):null;if(k&&this.raw[k])this.combatLatch.add(k);}for(let i=0;i<3;i++)if(pointer.buttons[i])this.combatLatch.add('mouse'+i);return this.combatLatch.size>0;},
    saveKeys(){try{localStorage.setItem('bof_od_keys',JSON.stringify(BIND));}catch(e){}},
    resetKeys(){for(const k in BIND)BIND[k]=KEY_DEFAULTS[k].slice();this.saveKeys();},
    keyLabel(a){return(BIND[a]||[]).map(k=>({' ':'SPACE',arrowup:'UP',arrowdown:'DOWN',arrowleft:'LEFT',arrowright:'RIGHT'}[k]||k.toUpperCase())).join(' / ');},
    padStyle(){return profile.style==='standard'?'standard':'six';},
    padProfile(){const p=Object.assign({},this.padStyle()==='standard'?STANDARD_PAD:DEFAULT_PAD,profile);delete p.style;return p;},
    // BOF accepts non-Back face/shoulder buttons in menus: the printed A on
    // a six-button controller is not necessarily browser button zero.
    menuFaceTokens(){const token=b=>typeof b==='number'?'pad_'+b:b&&b.axis!=null?'pad_axis'+b.axis+'_'+(b.sign<0?'neg':'pos'):null;const excluded=new Set(['B','mode','start','up','down','left','right'].map(k=>token(profile[k])).filter(Boolean));return [...new Set([0,2,3,4,5,7].map(n=>'pad_'+n).concat(['A','C','X','Y','Z','L','R'].map(k=>token(profile[k]))))].filter(k=>k&&!excluded.has(k));},
    setPadBinding(a,b){profile=Object.assign({},this.padStyle()==='standard'?STANDARD_PAD:DEFAULT_PAD,profile,{[a]:b});if(activePad){saved[activePad.id]=profile;try{localStorage.setItem('bof_td_controllers',JSON.stringify(saved));}catch(e){}}},
    setPadStyle(style){defaultStyle=style;profile=Object.assign({},style==='standard'?STANDARD_PAD:DEFAULT_PAD);try{localStorage.setItem('bof_od_pad_style',style);}catch(e){}if(activePad){saved[activePad.id]=profile;try{localStorage.setItem('bof_td_controllers',JSON.stringify(saved));}catch(e){}}},
    resetPad(){this.setPadStyle(this.padStyle());},
    beginSetup(){const standard=this.padStyle()==='standard';this.setup={i:0,bindings:standard?{style:'standard'}:{},steps:standard?['up','down','left','right','A','B','X','Y','mode','start','L','R','boost']:SETUP_STEPS,neutral:false,done:false};},
    update(){
      const pads=root.navigator.getGamepads?root.navigator.getGamepads():[];
      activePad=Array.from(pads).find(p=>p&&p.connected!==false)||null;
      this.padId=activePad?activePad.id:null;
      if(this.padId!==previousId){const stored=saved[this.padId];const style=stored?.style||defaultStyle;profile=Object.assign({},style==='standard'?STANDARD_PAD:DEFAULT_PAD,stored);previousId=this.padId;previousPadAim=null;}
      this.lastRaw=this.raw;this.raw={...keys};
      if(activePad){activePad.buttons.forEach((b,i)=>{this.raw['pad_'+i]=!!b.pressed||b.value>.5;});activePad.axes.forEach((v,i)=>{this.raw['pad_axis'+i+'_neg']=v<-.55&&v>=-1;this.raw['pad_axis'+i+'_pos']=v>.55&&v<=1;});}
      for(const k of this.combatLatch)if(k.startsWith('mouse')?!pointer.buttons[+k.slice(5)]:!this.raw[k])this.combatLatch.delete(k);
      const held=(i,combat=false)=>!!this.raw['pad_'+i]&&(!combat||!this.combatLatch.has('pad_'+i));
      const mapped=(name,combat=false)=>{const b=profile[name];if(typeof b==='number')return held(b,combat);if(b&&b.axis!=null){const k='pad_axis'+b.axis+'_'+(b.sign<0?'neg':'pos');return!!this.raw[k]&&(!combat||!this.combatLatch.has(k));}return false;};
      const fireMapped=name=>mapped(name,true);
      this.last=this.state;const s={};for(const a in BIND)s[a]=BIND[a].some(k=>keys[k]);
      if(TD.game?.state==='play'&&!TD.BossIntro?.active(TD.game))for(const a of ['A','B','X','Y'])s[a]=BIND[a].some(k=>this.raw[k]&&!this.combatLatch.has(k));
      if(this.rebind){if(s.back){this.rebind=null;this.state={};return;}const q=this.rebind;if(q.kind==='pad'&&activePad){const pressed=activePad.buttons.map((b,i)=>held(i)?i:-1).filter(i=>i>=0);if(!pressed.length)q.neutral=true;else if(q.neutral&&pressed.length===1){this.setPadBinding(q.action,pressed[0]);this.rebind=null;}}this.state={};return;}
      if(this.setup){
        if(this.setup.done){s.start||=mapped("start");s.A||=this.menuFaceTokens().some(k=>this.raw[k]);s.back||=mapped('B');}
        const q=this.setup;
        s.click=!!pointer.buttons[0]||queuedClick;queuedClick=false;
        if(s.back){this.setup=null;this.state=s;return;}
        if(activePad&&!q.done){
          const buttons=activePad.buttons.map((b,i)=>held(i)?i:-1).filter(i=>i>=0);
          const axes=activePad.axes.map((v,i)=>Math.abs(v)>.65&&Math.abs(v)<=1?{axis:i,sign:Math.sign(v)}:null).filter(Boolean);
          // Hat axes often rest at >1. Ignore those; mapped D-pad buttons remain supported.
          if(!buttons.length&&!axes.length)q.neutral=true;
          else if(q.neutral){const move=q.i<4, binding=buttons.length===1?buttons[0]:move&&axes.length===1?axes[0]:null;
            if(binding!=null){q.bindings[q.steps[q.i++]]=binding;q.neutral=false;
              if(q.i===q.steps.length){profile=q.bindings;saved[activePad.id]=profile;try{localStorage.setItem('bof_td_controllers',JSON.stringify(saved));}catch(e){}q.done=true;}
            }
          }
        }
        this.state=s;return;
      }
      const menu=!TD.game||TD.game.state!=='play'||TD.BossIntro?.active(TD.game),mode=mapped('mode');
      if(activePad){
        // A saved binding (including an intentional unbind) owns its direction.
        // Default D-pad/stick fallbacks must not also fire reassigned buttons.
        const ax=activePad.axes[0]||0,ay=activePad.axes[1]||0;
        for(const [name,button,axis,sign]of [['up',12,ay,-1],['down',13,ay,1],['left',14,ax,-1],['right',15,ax,1]]){
          const custom=Object.prototype.hasOwnProperty.call(profile,name);
          if(custom?mapped(name):held(button)||(Math.abs(axis)<=1&&axis*sign>.35))s[name]=true;
        }
        if(mapped('start'))s.start=true;
        if(menu){s.A||=this.menuFaceTokens().some(k=>this.raw[k]);s.back||=mapped('B')||mode;s.setup||=mode&&mapped('start');}
        else{
          const foot=TD.game.player?.onfoot;
          s.cruise||=!foot&&mapped('L');s.retina||=!foot&&mapped('R');
          if(this.padStyle()==='standard'){
            s.A||=fireMapped('A');s.B||=fireMapped('B');s.X||=fireMapped('X');s.Y||=fireMapped('Y');s.C||=mode&&!foot;s.boost||=!foot&&mapped('boost');
            if(foot&&mode){s.reload||=mapped('A');s.prone||=mapped('X');s.tapWall||=mapped('Y');s.swap||=mapped('B');s.A=s.B=s.X=s.Y=false;}
            const ax=activePad.axes[2]||0,ay=activePad.axes[3]||0;if(Math.hypot(ax,ay)>.3)s.aim=[ax,ay];
          }else{
          if(mode){s.C=!foot||s.C;s.Y||=!foot&&fireMapped('Z');s.reload||=foot&&mapped('A');s.prone||=foot&&mapped('X');s.tapWall||=foot&&mapped('Y');s.swap||=foot&&mapped('B');s.crash||=foot&&mapped('C');s.exitVehicle||=!foot&&mapped('B')&&!mapped('C');}
          const dx=(fireMapped('B')?1:0)-(fireMapped('Y')?1:0),dy=(fireMapped('A')?1:0)-(fireMapped('X')?1:0);
          const cruiseFire=s.cruise&&fireMapped('A')&&!fireMapped('B')&&!fireMapped('X')&&!fireMapped('Y');
          if(cruiseFire)s.A=true;
          else if((!mode||(!foot&&mapped('C')))&&(dx||dy)){s.aim=[dx,dy];s.A=true;s.directionalFire=true;}
          s.boost||=!foot&&mode&&mapped('C');
          s.X||=fireMapped('C')&&(foot||!mode);if(!mode){if(foot)s.Y||=fireMapped('Z');else s.retina||=mapped('Z');}
          }
        }
        if(Object.values(s).some(Boolean))TD.Audio.unlock();
      }
      s.wheel=wheel;wheel=0;s.click=!!pointer.buttons[0]||queuedClick;queuedClick=false;
      if(pointer.buttons[0]&&(menu||!this.combatLatch.has('mouse0')))s.A=true;
      if(pointer.buttons[2]&&(menu||!this.combatLatch.has('mouse2')))s.X=true;if(pointer.buttons[1]&&(menu||!this.combatLatch.has('mouse1')))s.Y=true;
      // Movement, cruise and Retina never take aim away from the mouse.
      // A new stick deflection takes over; an unchanged held stick cannot
      // immediately steal aim back after an actual pointer movement.
      if(s.aim&&(!previousPadAim||Math.hypot(s.aim[0]-previousPadAim[0],s.aim[1]-previousPadAim[1])>.12))aimSource='pad';
      previousPadAim=s.aim?s.aim.slice():null;
      if(s.cruise&&!menu){const dx=(s.right?1:0)-(s.left?1:0),dy=(s.down?1:0)-(s.up?1:0);if(dx||dy){s.freeAim=[dx,dy];if(!s.aim&&(!this.last.cruise||this.last.freeAim?.[0]!==dx||this.last.freeAim?.[1]!==dy))aimSource='cruise';}}
      if(s.aimLeft||s.aimRight)aimSource='keyboard';
      s.aimSource=aimSource;s.padActive=!!s.aim;
      this.state=s;
    },
    down(a){return !!this.state[a];},tap(a){return !!this.state[a]&&!this.last[a];},released(a){return !this.state[a]&&!!this.last[a];},
    dir(){const s=this.state;return[(s.right?1:0)-(s.left?1:0),(s.down?1:0)-(s.up?1:0)];},
    aim(p){const s=this.state;if(s.directionalFire)return TD.M.angTo(0,0,...s.aim);if(s.aimLeft||s.aimRight)return null;if(s.freeAim&&s.aimSource==='cruise')return TD.M.angTo(0,0,...s.freeAim);if(s.aim&&(s.aimSource!=='mouse'||!pointer.active))return TD.M.angTo(0,0,...s.aim);if(pointer.active&&s.aimSource==='mouse')return TD.M.angTo(p.x,p.y,pointer.x/TD.Cam.zoom+TD.Cam.x,pointer.y/TD.Cam.zoom+TD.Cam.y);return null;},
    confirm(){return this.tap('A')||this.tap('start');},
    setupLabel(){return this.setup?.done?'SAVED - RELEASE START, THEN PRESS START':!activePad?'CONNECT YOUR CONTROLLER':('PRESS '+(this.setup?.steps||SETUP_STEPS)[this.setup?.i||0].toUpperCase());},
  };

  TD.Text={fit(ctx,draw,value,box,size,col,measure){const [x,y,w,h]=box,s=String(value);ctx.save();ctx.font='bold '+size+'px BOFCommand, "Arial Black", monospace';const width=measure?measure(s,size):ctx.measureText(s).width;const fitted=Math.min(size,Math.max(1,h-4),Math.max(1,w-4)*size/Math.max(1,width));draw(s,x+w/2,y+h/2,fitted,col,'center');ctx.restore();return{text:s,box:box.slice(),size:fitted,width:width*fitted/size,center:[x+w/2,y+h/2]};}};

  // Audio is owned by audio_1011.js, loaded immediately after this module.

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
