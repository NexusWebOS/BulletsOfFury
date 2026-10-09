/* Overdrive ground campaign. Authored Miami route, six finite-ammo infantry
 * weapons, companion support, new armor roles, and the rogue Machinists squad.
 * Every combat module uses its draw transform for hitboxes and muzzle sockets. */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World, FX = TD.FX, I = TD.Input, A = TD.Audio;
  const PACK = root.TD_CAMPAIGN_ART, FR = PACK.frames, SEQ = PACK.sequences;
  TD.COMPANIONS = ['hotwire', 'phoenix', 'niel']; TD.companion = 'hotwire';
  if (!TD.PILOTS.includes('niel')) TD.PILOTS.push('niel');
  const DIR = ['south', 'west', 'north', 'east'];
  const MIAMI_COVER = [[265,172,306,218],[214,208,247,272],[483,175,539,228],[595,224,633,305],
    [173,297,231,359],[523,394,569,453],[273,566,320,628],[434,620,494,688]];
  const direction = a => DIR[((Math.round(a / (Math.PI / 2)) % 4) + 4) % 4];
  function anim(key, time, loop) {
    const q = SEQ[key]; if (!q) return null;
    const frame = Math.floor(time * (q.fps || 9));
    return q.frames[loop === false ? Math.min(frame, q.frames.length - 1) : frame % q.frames.length];
  }
  function frame(ctx, key, x, y, opts) {
    if (!key) return; const meta = FR[key];
    ART.draw(ctx, key, x, y, Object.assign({ ax: meta ? meta.anchor[0] : 48, ay: meta ? meta.anchor[1] : 48 }, opts));
  }
  TD.bodyOf = pk => PACK.pilots[pk].body;
  TD.FOOT_GUNS = {
    desert_eagle: { name: 'DESERT EAGLE', cap: 12, reserve: 60, cd: 14, damage: 3, k: 'vulcan', speed: 8.5 },
    spread_shotgun: { name: 'SPREAD SHOTGUN', cap: 8, reserve: 32, cd: 30, damage: 2, k: 'vulcan', speed: 7, fan: [-.3,-.15,0,.15,.3] },
    minigun: { name: 'MINIGUN', cap: 60, reserve: 180, cd: 4, damage: 1, k: 'vulcan', speed: 9 },
    fusion_beam: { name: 'FUSION BEAM', cap: 36, reserve: 108, cd: 7, damage: 2, k: 'laser', speed: 12, pierce: 3 },
    napalm_launcher: { name: 'NAPALM', cap: 6, reserve: 18, cd: 38, damage: 4, k: 'crash', speed: 4, splash: 35 },
    rocket_launcher: { name: 'ROCKET LAUNCHER', cap: 4, reserve: 16, cd: 35, damage: 8, k: 'homing', speed: 5, splash: 48 },
  };
  TD.makeFootPlayer = (x, y) => Object.assign(TD.makePlayer(x,y), {
    onfoot: true, r: 8, hp: 1, max: 1, speed: 2.35, smoke: 5, stance: 'stand',
    weapons: [{ id: 'desert_eagle', lv: 1, ammo: 12, reserve: 60 }], roll: 0, reload: 0, action: null, footTime: 0,
  });
  function reload(p, G) {
    const gun = p.weapons[p.wi], def = TD.FOOT_GUNS[gun.id];
    if (p.reload || p.action || gun.ammo >= def.cap || !gun.reserve) return;
    p.reload = 1.15; p.reloadGun = gun; G.say('RELOADING',p); A.play('blip');
  }
  function fireFoot(p, G) {
    const gun = p.weapons[p.wi], def = TD.FOOT_GUNS[gun.id];
    if (gun.ammo <= 0) { if (p.fireCd <= 0) { G.say(gun.reserve ? 'RELOAD' : 'OUT OF AMMO',p); p.fireCd=25; } return; }
    const lv=gun.lv||1; gun.ammo--; p.fireCd=Math.max(3,Math.round(def.cd*(1-.12*(lv-1))));
    const forward = M.fwd(p.aim), x = p.x + forward[0]*15, y = p.y + forward[1]*15;
    // A blocked hand socket cannot shoot through a wall when pressed against cover.
    if (W.rayBlock(p.x,p.y,x,y)) { FX.boom(p.x,p.y,18,'gfx_impact_',6); return; }
    for (const delta of def.fan || [0]) {
      const a=p.aim+delta, f=M.fwd(a);
      G.shots.push({ k:def.k,x,y,a,vx:f[0]*def.speed,vy:f[1]*def.speed,dmg:def.damage*(1+.4*(lv-1)),life:60,r:3,
        pierce:def.pierce||0,splash:def.splash,sdmg:4,lv:1,t:0,napalm:gun.id==='napalm_launcher' });
    }
    FX.flash(x,y,p.aim,.1); A.play(def.k==='laser'?'laser':def.splash?'cannon':'mg',.55);
    TD.Stealth.noise(p.x,p.y,def.splash?270:150,.5,G.units);
  }
  TD.footTick = function(p,G,dt) {
    if (p.dead) return; p.footTime+=dt;
    p.inv=Math.max(0,p.inv-1); p.flash=Math.max(0,p.flash-dt); p.fireCd=Math.max(0,p.fireCd-1);
    const [dx,dy]=I.dir(), len=Math.hypot(dx,dy)||1, aim=I.aim(p);
    if (aim!=null) {p.aim=M.turnTo(p.aim,aim,.25);p.manualAim=60;}
    else if (I.down('aimLeft')||I.down('aimRight')) {p.aim+=(I.down('aimRight')?1:-1)*.09;p.manualAim=120;}
    else if (p.manualAim>0) p.manualAim--;
    else if ((dx||dy)&&!I.down('C')) p.aim=M.angTo(0,0,dx,dy);
    if (dx||dy) p.a=M.angTo(0,0,dx,dy);
    if (I.tap('prone') || I.tap('C')) p.stance=p.stance==='prone'?'stand':'prone';
    if (I.tap('X') && !p.action && !p.reload && p.roll<=0) {p.roll=.42;p.rollAim=(dx||dy)?p.a:p.aim;}
    const speed=p.roll>0?5.1:p.stance==='prone'?.85:2.35;
    const v=p.roll>0?M.fwd(p.rollAim):[dx/len,dy/len];
    p.vx=v[0]*speed;p.vy=v[1]*speed;p.moving=Math.hypot(p.vx,p.vy)>.1;
    if (!p.action) {p.x+=p.vx;p.y+=p.vy;} W.collide(p,p.r,false);
    for(const q of G.props) if(!q.dead) TD.pushOut(p,q);
    p.roll=Math.max(0,p.roll-dt); p.hidden=!!W.inType(p.x,p.y,'h')||!!W.inType(p.x,p.y,'d');
    if (I.tap('reload') || I.tap('B')) reload(p,G);
    if (p.reload>0 && (p.reload-=dt)<=0) {
      const w=p.reloadGun,def=TD.FOOT_GUNS[w.id],n=Math.min(def.cap-w.ammo,w.reserve);
      w.ammo+=n;w.reserve-=n;p.reload=0;p.reloadGun=null;A.play('pick');
    }
    if ((I.tap('Z')||I.state.wheel) && !p.reload && !p.action) p.wi=(p.wi+1)%p.weapons.length;
    if (I.tap('Y') && p.smoke>0 && !p.action && !p.reload) p.action={kind:'grenade',t:0,committed:false,aim:p.aim};
    if (p.action) {
      const action=p.action; action.t+=dt;
      // Dedicated six-frame throw: release at authored frame 4; inventory commits once.
      if (!action.committed && action.t>=.3) {
        action.committed=true;p.smoke--; const f=M.fwd(action.aim);
        G.footGrenades.push({x:p.x,y:p.y,tx:p.x+f[0]*115,ty:p.y+f[1]*115,t:0,done:false}); A.play('missile',.4);
      }
      if(action.t>=.6)p.action=null;
    } else if (I.down('A') && p.fireCd<=0 && !p.reload && p.roll<=0) fireFoot(p,G);
    if (I.tap('tapWall')) {
      const f=M.fwd(p.aim),x=p.x+f[0]*20,y=p.y+f[1]*20;
      if(W.solidAt(x,y)){TD.Stealth.noise(x,y,180,.25,G.units);G.say('TAP',p);A.play('blip',.2);}
    }
  };
  TD.drawFoot = function(ctx,p,o) {
    const t=p.footTime||0,body=TD.bodyOf(p.pilot),dir=direction(p.moving?p.a:p.aim);
    let key='fp_'+p.pilot+'_aim_'+({north:0,east:1,south:2,west:3}[direction(p.aim)]);
    if (p.moving) key='fp_'+p.pilot+'_run_'+dir+'_'+(Math.floor(t*9)%4);
    if (p.stance==='prone') {
      const poses=SEQ['wm_'+body+'_prone_fire_'+dir].frames;
      const def=TD.FOOT_GUNS[p.weapons[p.wi].id],firing=p.fireCd>def.cd-6;
      key=poses[firing?1:p.moving?[0,2,4][Math.floor(t*6)%3]:0];
    }
    if(p.roll>0) key=anim('of_'+body+'_roll_to_stand',.42-p.roll,false);
    if(p.action) key=anim('of_'+body+'_grenade_throw',p.action.t,false);
    if(p.dead) key=anim('of_'+body+'_death',p.deadT||0,false);
    frame(ctx,key,p.x+2,p.y+3,{s:.75,tint:'#000',alpha:.3});
    frame(ctx,key,p.x,p.y,{s:.75,flash:o&&o.flash||0});
    if (!p.dead&&!p.action&&p.roll<=0) {
      const f=M.fwd(p.aim); frame(ctx,'of_'+p.weapons[p.wi].id+'_pickup',p.x+f[0]*8,p.y+f[1]*8,{s:.13,a:p.aim+Math.PI/2});
    }
  };
  TD.FOOT_EXTRA=['pow','crash','life','score'];   // 1009 museum: Mercs POW, Mega Crash stock, 1UP, score
  TD.footDrop=function(G,x,y,kind) {
    if (!TD.FOOT_GUNS[kind]&&!TD.FOOT_EXTRA.includes(kind)) kind=kind==='smoke'||kind==='grenades'?'grenades':'ammo';
    G.pickups.push({kind,x,y,t:0,foot:true});
  };
  TD.footPickups=function(G,dt) {
    const p=G.player;
    for(const k of G.pickups) {
      k.t+=dt;if(p.dead||M.dist(k.x,k.y,p.x,p.y)>22)continue;k.dead=true;A.play('pick');
      const d=TD.FOOT_GUNS[k.kind];
      if(d){let w=p.weapons.find(q=>q.id===k.kind);
        // Hard Corps: four carried weapons (A-D); a fifth replaces the one in hand
        if(!w){w={id:k.kind,lv:1,ammo:d.cap,reserve:d.reserve};if(p.slots4&&p.weapons.length>=4)p.weapons[p.wi]=w;else p.weapons.push(w);}else w.reserve+=d.reserve;p.wi=p.weapons.indexOf(w);G.say(d.name,p);}
      else if(k.kind==='pow'){const w=p.weapons[p.wi];w.lv=Math.min(3,(w.lv||1)+1);G.say('POW - '+TD.FOOT_GUNS[w.id].name+' LV'+w.lv,p);}
      else if(k.kind==='crash'){G.crash=Math.min(5,(G.crash||0)+1);G.say('MEGA CRASH +1',p);}
      else if(k.kind==='life'){G.lives++;G.say('1UP',p);}
      else if(k.kind==='score'){G.score+=1000;G.say('+1000',p);}
      else if(k.kind==='grenades'){p.smoke=Math.min(9,p.smoke+3);G.say('GRENADES +3',p);}
      else {const w=p.weapons[p.wi];w.reserve+=TD.FOOT_GUNS[w.id].cap*3;G.say('AMMO',p);}
    }
    G.pickups=G.pickups.filter(k=>!k.dead);
  };
  const EXTRA_ART={pow:['pow_badge',.42],crash:['fury_bomb',.16],life:['life_up',.22],score:['score_1000',.24]};
  TD.drawFootPickup=(ctx,k)=>{const e=EXTRA_ART[k.kind];if(e){ART.draw(ctx,e[0],k.x,k.y+Math.sin(k.t*4)*2,{s:e[1]});return;}
    const p=TD.game.player;frame(ctx,'of_'+(TD.FOOT_GUNS[k.kind]?k.kind+'_pickup':k.kind==='grenades'?'grenade_bundle':(q=>q.weapons[q.wi]||q.weapons[0])(p.onfoot?p:TD.game.footSave||p).id+'_ammo'),k.x,k.y,{s:.25});};
  const base={vis:{range:230,half:.65},prefer:[95,180],gun:'burst',cd:1.8,r:11,speed:.85,ds:.75};
  TD.ET.robotScout=Object.assign({},base,{foot:'scout',art:'of_scout_south',wreck:'of_scout_wreck',hp:4,score:350});
  TD.ET.robotHeavy=Object.assign({},base,{foot:'heavy',art:'of_heavy_robot_south',wreck:'of_heavy_robot_wreck',hp:10,score:700,speed:.6,gun:'twin',cd:2.8,r:14});
  TD.ET.rocketTank={mod:'chaz',ds:.65,hp:16,r:26,speed:1.2,vis:{range:300,half:.7},prefer:[170,260],gun:'rocket',cd:3.4,score:1100};
  TD.ET.railTank={mod:'rolf',ds:.62,hp:13,r:26,speed:1.35,vis:{range:340,half:.4},prefer:[210,300],gun:'snipe',cd:3.1,warn:.55,score:1000};
  TD.ET.siegeTank={mod:'wren',ds:.74,hp:24,r:32,speed:.75,vis:{range:280,half:.7},prefer:[130,230],gun:'twin',cd:2.5,warn:.35,score:1500};
  TD.drawRobot=function(ctx,u,type) {
    const dir=direction(u.a),time=TD.game.t/60;
    const key=anim('wm_enemy_'+type+'_patrol_'+dir,time)||'of_'+(type==='heavy'?'heavy_robot_':'scout_')+(dir==='west'?'east':dir);
    frame(ctx,key,u.x,u.y,{s:.75,flash:u.flash>0?1:0});
  };
  // Common calibrated layer canvases keep both static and animated track roots fixed.
  TD.drawModTank=function(ctx,u,crew,scale) {
    const state=u.parts||{hull:1,left_track:1,right_track:1,turret:1,special_module:1};
    for(const part of ['left_track','right_track','hull','special_module','turret']) {
      if(state[part]<=0)continue;
      const key=TD.modPartKey(u,crew,part);
      const a=(part==='turret'?(u.look==null?u.a:u.look):u.a)+Math.PI;
      const f=M.fwd(u.look==null?u.a:u.look),kick=part==='turret'?(u.recoil||0):0;
      frame(ctx,key,u.x-f[0]*kick,u.y-f[1]*kick,{a,s:scale,flash:u.flash>0?1:0});
    }
  };
  TD.modPartKey=function(u,crew,part){
    if(part.includes('_track')&&u.trackDistance){const side=part==='left_track'?0:1,phase=((Math.floor(u.trackDistance[side]/5)%6)+6)%6;return 'wm_tank_'+crew+'_'+part+'_move_'+phase+'_layer';}
    return 'wm_tank_'+crew+'_'+(part==='hull'&&u.hp<u.max*.4?'damaged_hull':part)+'_layer';
  };
  TD.hurtAlly=function(G,damage) {
    const p=G.ally;if(!p||p.dead||p.inv>0)return;p.hp-=damage;p.inv=55;
    if(p.hp<=0){p.dead=true;p.downT=8;FX.boom(p.x,p.y,85,'gfx_destruction_',6);G.say(p.pilot.toUpperCase()+' REGROUPING',p);}
  };
  TD.allyTick=function(G,dt) {
    const ally=G.ally,p=G.player;if(!ally)return;
    if(ally.dead){if((ally.downT-=dt)<=0){ally.dead=false;ally.hp=ally.max;ally.inv=120;ally.x=p.x-65;ally.y=p.y+40;W.collide(ally,ally.r,false);}return;}
    ally.inv=Math.max(0,ally.inv-1);ally.fireCd-=dt;
    let goal={x:p.x+(p.x<400?75:-75),y:p.y+35};
    if(M.dist(ally.x,ally.y,goal.x,goal.y)>35&&!p.dead){if(W.rayBlock(ally.x,ally.y,goal.x,goal.y)){const f=TD.Nav.step(TD.Nav.field(goal.x,goal.y,G.t/60),ally.x,ally.y);if(f)goal={x:ally.x+f[0]*80,y:ally.y+f[1]*80};}const a=M.angTo(ally.x,ally.y,goal.x,goal.y);ally.a=M.turnTo(ally.a,a,.12);const f=M.fwd(a);ally.x+=f[0]*2.5;ally.y+=f[1]*2.5;}
    W.collide(ally,ally.r,false);TD.pushOut(ally,p);
    let targets=G.units.filter(u=>!u.dead&&u.mode==='alert');
    if(G.boss&&G.boss.alive()){const q=G.boss.aim(ally.x,ally.y);if(q)targets.push(q);}
    const target=targets.filter(q=>M.dist(ally.x,ally.y,q.x,q.y)<330&&!W.rayBlock(ally.x,ally.y,q.x,q.y)).sort((a,b)=>M.dist(ally.x,ally.y,a.x,a.y)-M.dist(ally.x,ally.y,b.x,b.y))[0];
    if(target){ally.aim=M.turnTo(ally.aim,M.angTo(ally.x,ally.y,target.x,target.y),.14);if(ally.fireCd<=0){ally.fireCd=ally.pilot==='phoenix'?.45:.6;const f=M.fwd(ally.aim),laser=ally.pilot==='hotwire';G.shots.push({k:laser?'laser':'vulcan',x:ally.x+f[0]*35,y:ally.y+f[1]*35,vx:f[0]*8,vy:f[1]*8,a:ally.aim,dmg:laser?2:1,life:55,r:4,t:0,lv:1,ally:true});FX.flash(ally.x+f[0]*35,ally.y+f[1]*35,ally.aim,.12);}}
    else ally.aim=M.turnTo(ally.aim,p.aim,.08);
  };
  function placement(type,x,y,extra){return Object.assign({type,x,y,a:0,wp:[[x-55,y],[x+55,y]]},extra);}
  const n=Math.PI;
  TD.MISSIONS=[
    {id:2,mode:'tank',map:TD.LEVEL2_MAP,data:TD.LEVEL2_DATA,boss:TD.makeWarrior},
    {id:3,mode:'foot',map:{key:'miami_ground',w:800,h:1200,rects:[
      [0,0,285,155,'b'],[520,0,800,155,'b'],[0,155,85,700,'b'],[715,155,800,1200,'v'],
      [115,465,270,635,'v'],[545,465,690,635,'v'],[0,700,105,1200,'b'],
      [310,415,445,610,'b'],[320,675,420,795,'h'],[105,810,300,945,'b'],[490,800,655,985,'b'],
      // Painted tall stacks: independently authored footprint and sight blockers.
      [265,192,306,218,'b'],[214,244,247,272,'b'],[483,202,539,228,'b'],[595,277,633,305,'b'],
      [173,331,231,359,'b'],[523,425,569,453,'b'],[273,600,320,628,'b'],[434,660,494,688,'b'],
    ]},data:{title:'LEVEL 3',name:'BOOTS ON THE GROUND',brief:['MOVE FROM MIAMI BEACH THROUGH THE PALM PARK.','NORMAL INFANTRY COMBAT IS ONE HIT = ONE LIFE.','DISABLE THREE FORTRESS SENTRIES TO OPEN THE GATE.','BREACH THE NORTH EXIT AND REJOIN THE FURY TANKS.'],
      start:{x:400,y:1150,a:n},checkpoints:[[400,970],[400,700],[470,380]],gates:[[400,1200],[400,700]],bossLine:415,boss:{x:400,y:185},structures:[],
      units:[placement('robotScout',400,1020),placement('robotScout',350,870),placement('robotHeavy',475,750),placement('robotScout',310,680),placement('robotScout',600,440),placement('robotScout',195,430),placement('robotHeavy',465,320),placement('robotHeavy',340,225,{role:'sentry'}),placement('robotHeavy',470,225,{role:'sentry'}),placement('robotHeavy',400,185,{role:'sentry'})],
      props:[{kind:'pbox',x:455,y:1110,drop:'spread_shotgun'},{kind:'crate',x:440,y:945,drop:'minigun'},{kind:'pbox',x:470,y:655,drop:'fusion_beam'},{kind:'crate',x:170,y:695,drop:'rocket_launcher'},{kind:'pbox',x:640,y:395,drop:'napalm_launcher'},{kind:'crate',x:490,y:340,drop:'grenades'},{kind:'crate',x:305,y:1010,drop:'ammo'},{kind:'crate',x:585,y:625,drop:'ammo'}]},boss:null},
    {id:4,mode:'tank',map:{key:'rebel_ground',w:800,h:2400,rects:[[0,0,800,65,'b'],[0,65,80,2400,'b'],[720,65,800,2400,'b'],[80,2200,720,2400,'v']]},
      data:{title:'LEVEL 4',name:'MACHINISTS - REBEL SIEGE',brief:['WREN, ROLF AND CHAZ HAVE TURNED ROGUE.','THEIR TANK SQUAD WILL ATTACK YOU AND YOUR PARTNER.','BREAK TRACKS, TURRETS AND SPECIAL MODULES.','CLEAR THE FACTORY YARD AND RECOVER THE AIR ROUTE.'],start:{x:400,y:2140,a:n},checkpoints:[[400,1950],[400,1400],[400,880]],gates:[[400,2145],[400,1300]],bossLine:690,boss:{x:400,y:320},
      units:[placement('rocketTank',450,1950),placement('scout',245,1880),placement('railTank',545,1790),placement('siegeTank',260,1620),placement('rocketTank',470,1410),placement('railTank',300,1260),placement('heavy',575,1100),placement('siegeTank',420,870)],
      structures:[{kind:'warehouse',x:210,y:2050},{kind:'relay',x:595,y:2000},{kind:'warehouse',x:215,y:1760},{kind:'relay',x:580,y:1550},{kind:'warehouse',x:215,y:1380},{kind:'warehouse',x:575,y:1250},{kind:'relay',x:210,y:1000},...[220,580].flatMap(x=>[{kind:'barrier',x,y:530},{kind:'barrier',x,y:400}])],
      props:[{kind:'pbox',x:350,y:2090,drop:'homing'},{kind:'crate',x:435,y:1940,drop:'laser'},{kind:'crate',x:380,y:1450,drop:'repair'},{kind:'pbox',x:440,y:925,drop:'homing'},{kind:'crate',x:350,y:775,drop:'repair'}]},boss:null},
  ];
  TD.makeFortress=function(G,x,y) {
    const gate=W.add({x0:285,y0:100,x1:520,y1:155,t:'b'});
    return {name:'FORTRESS SENTRIES',x,y,state:'fight',dead:false,opened:false,alive:()=>!G.boss.opened,
      hpFrac:()=>G.units.filter(q=>q.role==='sentry'&&!q.dead).length/3,
      aim:()=>G.units.find(q=>q.role==='sentry'&&!q.dead),hit:()=>false,blast:()=>{},drawUnder:()=>{},drawOver:()=>{},
      draw(ctx){frame(ctx,'of_fortress_gate_'+(this.opened?'open':'closed'),400,125,{s:1.05});},
      tick(){if(!this.opened&&!G.units.some(q=>q.role==='sentry'&&!q.dead)){this.opened=true;W.remove(gate);G.say('GATE OPEN - NORTH EXIT',{x:400,y:200});}
        if(this.opened&&G.player.y<83&&!this.dead){this.dead=true;G.bossDown();}}
    };
  };
  TD.MISSIONS[1].boss=TD.makeFortress;
  TD.campaignTick=function(G,dt) {
    TD.allyTick(G,dt);
    for(const g of G.footGrenades) {
      g.t+=dt;const q=Math.min(1,g.t/.65),x=M.lerp(g.x,g.tx,q),y=M.lerp(g.y,g.ty,q);
      if(!g.done&&g.t>=.9){g.done=true;TD.blast(G,x,y,65,12,false);FX.boom(x,y,145,'of_grenade_blast_',6);A.play('expB');TD.Stealth.noise(x,y,400,.85,G.units);}
    }
    G.footGrenades=G.footGrenades.filter(g=>!g.done);
    G.burns=G.burns||[];
    for(const b of G.burns){b.t+=dt;b.next-=dt;if(b.next<=0){b.next=.4;TD.blast(G,b.x,b.y,30,1,false);}if(G.t%8===0)FX.boom(b.x,b.y,45,'nex_fireball_',4);}
    G.burns=G.burns.filter(b=>b.t<2.4);
  };
  TD.campaignDraw=function(ctx,G) {
    if(G.ally&&!G.ally.dead)TD.drawPlayerTank(ctx,G.ally);
    for(const g of G.footGrenades){const q=Math.min(1,g.t/.65),x=M.lerp(g.x,g.tx,q),y=M.lerp(g.y,g.ty,q);frame(ctx,'of_grenade',x,y-Math.sin(q*Math.PI)*32,{s:.28,a:g.t*14});}
  };
  TD.drawFootCover=function(ctx,G){
    if(!G.player.onfoot||G.mission!==3)return;const plate=ART.get('miami_ground');if(!plate)return;
    const actors=[G.player,...G.units.filter(u=>!u.dead)];
    for(const [x0,y0,x1,y1] of MIAMI_COVER)if(actors.some(p=>p.x+p.r>x0&&p.x-p.r<x1&&p.y>y0-18&&p.y<y1-18)){
      // Redraw the exact authored tall-stack pixels above a pilot behind its base.
      ctx.drawImage(plate.im,plate.sx+x0,plate.sy+y0,x1-x0,y1-y0,x0,y0,x1-x0,y1-y0);
    }
  };
  TD.CAMPAIGN_WARM=['miami_ground','rebel_ground','of_fortress_gate_closed','of_fortress_gate_open',
    ...Object.keys(FR).filter(k=>k.startsWith('wm_tank_')&&k.includes('_layer')),
    ...Object.keys(FR).filter(k=>k.startsWith('fp_')||k.startsWith('pt_niel_')||/^of_.*(pickup|ammo|grenade|wreck)$/.test(k)),
    ...['scout','heavy'].flatMap(b=>DIR.flatMap(d=>SEQ['wm_enemy_'+b+'_patrol_'+d].frames)),
    ...['regular','heavy','athletic','female'].flatMap(b=>['death','roll_to_stand'].flatMap(a=>SEQ['of_'+b+'_'+a].frames)),
    ...SEQ.wm_phoenix_grenade_throw.frames,...SEQ.wm_hotwire_grenade_throw.frames,
    ...Object.keys(FR).filter(k=>/^wm_.*(prone_fire|crouch_walk)/.test(k)),
    ...['hotwire','phoenix','niel'].map(p=>'pav_'+p),...Object.keys(FR).filter(k=>/^of_grenade_blast_|^wm_(wren|rolf|chaz)_(muzzle|special)_/.test(k))];
}(window));
