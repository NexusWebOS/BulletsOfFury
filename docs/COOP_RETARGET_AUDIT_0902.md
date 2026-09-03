# Co-op enemy retargeting — audit, 0902

`aimPlayer` is FIXED: it resolves its target through `targetShip(x,y)` (nearest live seat),
so every **aimed** enemy shot in the game — all 88 call sites — now leads whichever pilot is
closer. Solo returns the same `player` object and is unchanged.

What follows is what still reads the global `player` DIRECTLY and therefore still behaves as
though seat 1 is the only ship. These are movement and positional decisions, not aimed fire:
dives, lateral tracking, ram lines and a few boss phase checks.

## Why they were not converted in this pass

They are 55 individual expressions spread over five regions, several inside `spawnEnemy`'s
unclosed `if` and several inside boss phase machines with their own local `player` semantics.
A blind sweep of `player.` -> `targetShip(...)` across them would also catch reads that are
legitimately about seat 1 (respawn, camera, HUD), and this file already records what a
confident mass edit costs. Each needs reading in context.

## The list


### misc

- `8292` — `const d = Math.hypot(player.x - e.x, player.y - e.y);`

### boss / shipboss AI

- `13007` — `const a=Math.atan2(player.y-y, player.x-b.x);`
- `13827` — `const C=shipBossMount(b,'C'),a=Math.atan2(player.y-C.y,player.x-C.x),sp=3.55;`
- `13838` — `const dx=Math.cos(a),dy=Math.sin(a),px=player.x-C.x,py=player.y-C.y;`
- `14996` — `const dx=player.x-b.x, dy=Math.max(40,(player.y-y));`
- `15305` — `if(player.y>=_top+b.h && player.y<=_top+b._animH && Math.abs(player.x-b.x)<half){`

### projectile movers

- `17641` — `eBullets.push({x:m.x, y:m.y, vx:(player.x-m.x)*0.006, vy:2.8, w:18, h:22,`
- `20790` — `t.sort((a,b)=> (Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(b.x-player.x,b.y-player.y)));`

### enemy update loop (dive / chase / ram)

- `23590` — `const dxp=player.x-e.x;`
- `23680` — `const _ta=Math.atan2(player.y-e.y, player.x-e.x);`
- `23714` — `e._diveAng=Math.atan2(player.y-e.y, player.x-e.x);`
- `23719` — `const want=Math.atan2(player.y-e.y, player.x-e.x);`
- `23740` — `e.x += (player.x-e.x)*0.9*dt;                     // curves toward the player's column`
- `23744` — `e.x += (player.x-e.x)*3.2*dt;`
- `23748` — `e.x += clamp(player.x-e.x,-1,1)*70*dt;`
- `23832` — `faceStep(e, Math.PI + clamp((player.x-e.x)*0.004, -0.3, 0.3), dt);`
- `23849` — `e.x += clamp(player.x-e.x,-1,1)*52*dt;`
- `23850` — `faceStep(e, Math.PI + clamp((player.x-e.x)*0.004,-0.3,0.3), dt);`
- `23853` — `if(e._mgT>0.42 && e.y>40 && e.y<VH*0.75){ e._mgT=0; const ang=Math.atan2(player.y-e.y,player.x-e.x); eTwinGuns`
- `23882` — `e._diveT=(e._diveT\|\|0)+dt; e.y+=4.0; e.x+=clamp(player.x-e.x,-1,1)*70*dt; e.vx=clamp((player.x-e.x)*0.02,-1,1)`
- `23883` — `faceStep(e, Math.PI + clamp((player.x-e.x)*0.004,-0.3,0.3), dt);`
- `23931` — `const a=Math.atan2(player.y-e.y, player.x-e.x);`
- `23936` — `const want=Math.atan2(player.y-e.y, player.x-e.x);`
- `23988` — `e.x += clamp(player.x-e.x,-1,1)*44*dt;                    // gentle tracking as it dives`
- `24282` — `Math.abs(b.x-player.x)<((b.w\|\|6)/2+(player.w\|\|24)/2) && Math.abs(b.y-player.y)<((b.h\|\|10)/2+(player.h\|\|30)/2))`
- `24974` — `const dx=player.x-b.x,dy=player.y-b.y,d=Math.hypot(dx,dy);`

### post-25000 (enemy AI + boss phases)

- `25100` — `const ta=Math.atan2(player.y-b.y,player.x-b.x); let da=((ta-ang+Math.PI*3)%(Math.PI*2))-Math.PI; ang+=clamp(da`
- `25161` — `const dx=player.x-b.x, dy=player.y-b.y;`
- `25176` — `if(!b.mg){ const ta=Math.atan2(player.y-b.y,player.x-b.x); let ang=Math.atan2(b.vy,b.vx);`
- `25213` — `if(Math.abs(b.x-player.x)<(_hx+b.w*0.15) && Math.abs(b.y-player.y)<(_hy+b.h*0.15)){`
- `25255` — `if(Math.abs(e.x-player.x)<(e.w/2+_hx) && Math.abs(e.y-player.y)<(e.h/2+_hy)){`
- `25501` — `const a=Math.atan2(player.y-e.y, player.x-e.x);`
- `28687` — `const want = (!player.dead) ? clamp(Math.atan2(player.x-e.x, Math.max(1,player.y-e.y)), -0.55, 0.55) : 0;`
- `31625` — `const aim=Math.atan2(player.y-e.y,player.x-e.x), mode=e._s9;`
- `31661` — `e.y+=e._s9vy*1.35*dt; e.x+=clamp(player.x-e.x,-1,1)*90*dt;`
- `32432` — `const dx=player.x-e.x, dy=Math.max(70,player.y-e.y), mag=Math.max(1,Math.hypot(dx,dy));`
- `32458` — `const band=clamp(54+Math.max(0,Math.abs(e.x-player.x)-54)*.48,54,156);`
- `32568` — `const canFire = player.y > e.y+8 && Math.abs(player.x-e.x) < 150;`
- `32789` — `const canFire = player.y > e.y+8 && Math.abs(player.x-e.x) < 120;`
- `32834` — `return player.y > e.y+10 && Math.abs(player.x-e.x) < 96;`
- `37595` — `if(Math.hypot(player.x-m.x, player.y-m.y)<R*0.7) playerHit();`
- `37645` — `if(Math.abs(player.x-m.x)<hw*0.72 && Math.abs(player.y-m.y)<hh*0.72){`
- `39066` — `if(e.y<VH*.33)e.y+=34*dt;const dx=clamp(player.x-e.x,-1,1);e.x+=dx*42*dt;e._bank=dx>0?1:-1;`
- `39246` — `if(e.y<VH*.32)e.y+=43*dt;else{const dx=clamp(player.x-e.x,-1,1);e.x+=dx*32*dt;}`
- `39346` — `e.y+=58*dt;e.x+=clamp(player.x-e.x,-1,1)*18*dt;`
- `39798` — `e.y+=60*dt;e.x+=clamp(player.x-e.x,-1,1)*38*dt;e.spin=Math.sin(e._s5t*1.5)*.18;`
- `39868` — `if(e.y<VH*.25)e.y+=88*dt;else{e.x+=clamp(player.x-e.x,-1,1)*72*dt;e.y=VH*.25+Math.sin(e._s8t*1.8)*12;e.spin=Ma`
- `39883` — `if(e.y<VH*.20)e.y+=72*dt;else{let ally=null,bd=1e9;for(const q of enemies){if(q===e\|\|q.dead\|\|!q._s8mega)contin`
- `39913` — `if(e.y<VH*.22)e.y+=138*dt;else e.x+=clamp(player.x-e.x,-1,1)*112*dt;`
- `39921` — `if(e.y<VH*.23)e.y+=76*dt;else e.x+=clamp((player.x-e.x)*1.8,-96,96)*dt;`
- `40124` — `const dy=player.y-b.y;`
- `41221` — `let deg=Math.atan2(player.y-e.y, player.x-e.x)*180/Math.PI;   // 0 = right, +down`
- `41307` — `const ang=Math.atan2(player.y-e.y, player.x-e.x);      // ~0 (right) .. PI (left) when below`
- `41387` — `const want=clamp((player.x-e.x)/120,-1,1);`
- `42442` — `Math.abs(player.x-b.x)<(b.w*0.42) && Math.abs(player.y-b.y)<(b.h*0.46)){`

## Recommended order

1. **enemy update loop** (18) — the dives and lateral tracking. This is what a player FEELS:
   P2 can fly under a diving unit and be passed over.
2. **post-25000** (29) — later enemy AI and boss phases.
3. **boss / shipboss AI** (5) — a boss that positions against seat 1 only.
4. **projectile movers** (2) — homing rounds that re-acquire seat 1 after launch.

A per-enemy `const _P = targetShip(e.x, e.y);` at the top of each tick, then `_P.` in place of
`player.` on the targeting expressions only, is the shape that fits — it matches the `withSeat`
idiom already in the file and keeps every non-targeting read pointing where it points today.
