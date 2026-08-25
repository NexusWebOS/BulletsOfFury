window.FURY_DATA = (() => {
  const atlas = "library/runtime/bullets-of-fury-sheet-clean.png";
  const frame = (id, x, y, w, h, image = atlas) => ({ id, label: id, image, sourceRect: { x, y, w, h } });
  const mainAtlas = "library/runtime/atlases/main.png";
  const mainFrame = (id, x, y, w, h) => frame(id, x, y, w, h, mainAtlas);
  const proceduralFrame = (id, procedural) => ({ id, label:id, image:null, sourceRect:null, procedural });
  const point = (kind, x, y, name) => ({ id: `${kind}-${Math.random().toString(36).slice(2, 8)}`, kind, x, y, name });
  const box = (kind, x, y, w, h, name) => ({ id: `${kind}-${Math.random().toString(36).slice(2, 8)}`, kind, x, y, w, h, name });

  const patterns = [
    { id:"straight", name:"Straight Descent", tags:["enemy","tank","drone"], description:"Constant downward travel. Clean, readable baseline for mixed formations.", params:{ amplitude:0, frequency:0 } },
    { id:"sine", name:"Sine Weaver", tags:["enemy","jet","drone"], description:"Vertical advance with a horizontal sine sweep around the spawn lane.", params:{ amplitude:66, frequency:2.8 } },
    { id:"vee", name:"V Formation", tags:["enemy","jet"], description:"Formation members drift outward from a shared centerline while advancing.", params:{ amplitude:30, frequency:1 } },
    { id:"side", name:"Side Needle", tags:["enemy","jet"], description:"Enters from a side edge with vertical bob and sustained lateral velocity.", params:{ amplitude:18, frequency:4 } },
    { id:"dive", name:"Targeted Dive", tags:["enemy","drone","alienoid"], description:"Accelerating descent that begins tracking the player after a short tell.", params:{ amplitude:68, frequency:1 } },
    { id:"snake", name:"Screen Snake", tags:["enemy","drone","alienoid"], description:"Wide synchronized weave around the game-space centerline.", params:{ amplitude:118, frequency:3.1 } },
    { id:"carrier", name:"Carrier Drift", tags:["boss","miniboss","boat"], description:"Slow armored drift with timed child-unit deployments.", params:{ amplitude:22, frequency:1.2 } },
    { id:"grid", name:"Combat Grid", tags:["tank","turret","enemy"], description:"Stable lane advance with restrained synchronized oscillation.", params:{ amplitude:20, frequency:1.8 } },
    { id:"gate", name:"Turret Gate", tags:["turret","tank","miniboss"], description:"Alternating edge lanes create a closing weapon gate.", params:{ amplitude:32, frequency:2.4 } },
    { id:"fan", name:"Asteroid Fan", tags:["drone","alienoid","enemy"], description:"A broad fan opens from a narrow entry, ideal for swarms.", params:{ amplitude:42, frequency:1 } },
    { id:"spiral", name:"Expanding Spiral", tags:["drone","alienoid","boss"], description:"Oscillation radius expands with age to build escalating screen pressure.", params:{ amplitude:54, frequency:4 } },
    { id:"drift", name:"Organic Drift", tags:["boat","drone","sludge"], description:"Slow advance with irregular lateral pressure and a soft silhouette.", params:{ amplitude:30, frequency:2 } },
    { id:"hoverStrafe", name:"Hover + Strafe", tags:["jet","miniboss","boss"], description:"Approach, hold at a combat band, then strafe between safe margins.", params:{ amplitude:150, frequency:1.2 } },
    { id:"orbit", name:"Player Orbit", tags:["drone","alienoid","boss"], description:"Curves around the player at a configurable radius while maintaining aim.", params:{ amplitude:110, frequency:1.4 } },
    { id:"pounceRetreat", name:"Pounce + Retreat", tags:["lava","ice","sludge","alienoid"], description:"Telegraphed rush toward the player followed by a fast reset to the top band.", params:{ amplitude:90, frequency:0.8 } },
    { id:"bossPhases", name:"Boss Phase Loop", tags:["boss","miniboss"], description:"Health-gated hover, side sweep, center burst, and recovery sequence.", params:{ amplitude:145, frequency:0.65 } },
    { id:"drawn", name:"Custom Drawn Path", tags:["all"], description:"Follows normalized path points authored in Wave Studio.", params:{ amplitude:0, frequency:1 } }
  ];

  const base = (id, name, category, wired, f, stats = {}, movement = {}) => ({
    id, name, category, wired, tags:[category], frames:Array.isArray(f)?f:[f], selectedFrame:0,
    size:{ width:stats.width || 30, height:stats.height || 30, displayScale:100, lockAspect:true },
    combat:{ hp:stats.hp || 1, damage:stats.damage || 1, score:stats.score || 100, speed:stats.speed || 80, fireRate:stats.fireRate || 1.4 },
    movement:{ pattern:movement.pattern || "straight", amplitude:movement.amplitude ?? 40, frequency:movement.frequency ?? 2, customPath:[] },
    annotations:[point("anchor",.5,.5,"body-origin"), point("muzzle",.5,.88,"primary-muzzle"), box("damage",.16,.12,.68,.75,"hull")],
    aiNotes:"", runtimeRef:wired ? `game.js:${id}` : null
  });
  const legacy = (id, name, category, runtimeType, f, stats, movement) => {
    const entity=base(id,name,category,true,f,stats,movement);
    entity.runtimeRef=`assets/game.js:${runtimeType}`;
    entity.tags=[category,"classic-runtime",runtimeType];
    return entity;
  };

  const entities = [
    base("scout","Scout","enemy",true,frame("swarm-03",616,96,96,80),{width:26,height:24,hp:2,damage:1,score:110,speed:88,fireRate:1.45},{pattern:"straight"}),
    base("needle","Needle","enemy",true,frame("swarm-01",382,88,88,86),{width:20,height:28,hp:1,score:90,speed:124,fireRate:1.85},{pattern:"side",amplitude:18,frequency:4}),
    base("weaver","Weaver","enemy",true,frame("swarm-02",500,88,94,86),{width:30,height:26,hp:3,score:170,speed:82,fireRate:1.25},{pattern:"sine",amplitude:66,frequency:2.8}),
    base("turret","Assault Turret","enemy",true,frame("assault-03",740,302,128,94),{width:34,height:30,hp:5,damage:2,score:260,speed:55,fireRate:.95},{pattern:"gate",amplitude:32,frequency:2.4}),
    base("bomber","Bomber","enemy",true,frame("assault-01",408,296,138,100),{width:38,height:34,hp:7,damage:3,score:360,speed:62,fireRate:1.05},{pattern:"straight"}),
    base("carrier","Carrier","miniboss",true,frame("heavy-01",408,590,144,160),{width:46,height:38,hp:10,damage:3,score:520,speed:48,fireRate:.8},{pattern:"carrier",amplitude:22,frequency:1.2}),
    base("drone","Drone","enemy",true,frame("swarm-05",872,100,118,78),{width:18,height:18,hp:1,score:75,speed:142,fireRate:2.2},{pattern:"dive",amplitude:68,frequency:1}),
    base("boss-dread-kite","Dread Kite","boss",true,frame("heavy-01",408,590,144,160),{width:124,height:136,hp:70,damage:4,score:2500,speed:44,fireRate:.62},{pattern:"bossPhases",amplitude:145,frequency:.65}),
    base("boss-molten-wyrm","Molten Wyrm","boss",true,frame("heavy-02",574,592,140,154),{width:124,height:136,hp:98,damage:5,score:3700,speed:46,fireRate:.57},{pattern:"bossPhases",amplitude:150,frequency:.7}),
    base("boss-rail-cyclops","Rail Cyclops","boss",true,frame("heavy-03",732,592,134,154),{width:124,height:136,hp:126,damage:5,score:4900,speed:48,fireRate:.53},{pattern:"bossPhases",amplitude:155,frequency:.75}),
    base("boss-void-lance","Void Lance","boss",true,frame("heavy-04",884,590,126,154),{width:124,height:136,hp:154,damage:6,score:6100,speed:51,fireRate:.49},{pattern:"orbit",amplitude:120,frequency:1.1}),
    base("boss-fury-gun","The Fury Gun","boss",true,frame("heavy-01",408,590,144,160),{width:136,height:148,hp:182,damage:7,score:7300,speed:53,fireRate:.44},{pattern:"bossPhases",amplitude:165,frequency:.82}),
    ...["axel","decker","maverick","freezer","juggernaut","yuri"].map((name,i) => base(`pilot-${name}`,name[0].toUpperCase()+name.slice(1),"pilot",true,{
      id:name,label:`${name}-base`,image:`library/runtime/ships/ship_${name}.png`,sourceRect:null
    },{width:40+(i%3)*4,height:56,hp:3,damage:1.2,score:0,speed:244,fireRate:.082},{pattern:"straight"})),
    base("unwired-ice-drone","Ice Drone Mk I","ice",false,frame("ice-28",580,82,83,94,"library/runtime/atlases/full_sheets/iceenemies_extracted.png"),{width:42,height:48,hp:4,damage:2,score:240,speed:106,fireRate:1.3},{pattern:"pounceRetreat",amplitude:90,frequency:.8}),
    base("unwired-ice-alienoid","Ice Alienoid","alienoid",false,frame("ice-40",550,179,99,83,"library/runtime/atlases/full_sheets/iceenemies_extracted.png"),{width:52,height:44,hp:7,damage:2.5,score:420,speed:74,fireRate:1.1},{pattern:"orbit",amplitude:110,frequency:1.4}),
    base("unwired-tank-light","Light Strike Tank","tank",false,frame("tank-38",265,144,102,84,"library/runtime/atlases/full_sheets/tanks_extracted.png"),{width:58,height:48,hp:12,damage:3,score:560,speed:42,fireRate:1.4},{pattern:"grid",amplitude:20,frequency:1.8}),
    base("unwired-tank-heavy","Heavy Siege Tank","tank",false,frame("tank-121",74,849,300,254,"library/runtime/atlases/full_sheets/tanks_extracted.png"),{width:86,height:72,hp:28,damage:6,score:1200,speed:28,fireRate:2.1},{pattern:"gate",amplitude:24,frequency:1.1}),
    base("unwired-turret-cannon","Rotary Cannon","turret",false,frame("turret-18",247,332,225,218,"library/runtime/atlases/full_sheets/turrets_extracted.png"),{width:64,height:62,hp:14,damage:4,score:720,speed:20,fireRate:.72},{pattern:"hoverStrafe",amplitude:80,frequency:.8}),
    base("unwired-turret-boss","Fortress Turret","miniboss",false,frame("turret-08",3,36,717,293,"library/runtime/atlases/full_sheets/turrets_extracted.png"),{width:140,height:70,hp:50,damage:7,score:2200,speed:18,fireRate:.55},{pattern:"bossPhases",amplitude:120,frequency:.55}),

    // Full classic runtime roster from assets/game.js. These were previously missing because
    // Fury Forge only scanned the newer root game.js runtime.
    legacy("classic-drone","Classic Beetle Drone","drone","drone",[
      mainFrame("drone0",517,325,30,22),mainFrame("drone1",549,325,29,22),mainFrame("drone2",580,325,37,22)
    ],{width:22,height:18,hp:1,damage:1,score:120,speed:90,fireRate:2.2},{pattern:"sine",amplitude:36,frequency:2.8}),
    legacy("classic-assault","Classic Assault Striker","jet","assault",[
      mainFrame("assault-v0",137,325,35,30),mainFrame("assault-v1",174,325,34,30),mainFrame("assault-v2",210,325,30,30),mainFrame("assault-v3",242,325,33,30)
    ],{width:30,height:30,hp:3,damage:1,score:300,speed:48,fireRate:1.5},{pattern:"dive",amplitude:40,frequency:2}),
    legacy("classic-gunship","Classic Heavy Gunship","miniboss","gunship",[
      mainFrame("gunship-v0",771,263,36,40),mainFrame("gunship-v1",809,263,36,40),mainFrame("gunship-v2",847,263,36,40),mainFrame("gunship-v3",885,263,37,40)
    ],{width:40,height:44,hp:7,damage:2,score:700,speed:33,fireRate:1.1},{pattern:"hoverStrafe",amplitude:120,frequency:1.2}),
    legacy("classic-ground-turret","Classic Ground Turret","turret","turret",[
      mainFrame("turret0",277,325,24,28),mainFrame("turret1",303,325,25,28),mainFrame("turret2",330,325,26,28),mainFrame("turret3",358,325,25,28),mainFrame("turret4",385,325,28,28),mainFrame("turret5",415,325,28,28)
    ],{width:26,height:26,hp:5,damage:2,score:400,speed:42,fireRate:1.3},{pattern:"straight"}),
    legacy("classic-mine","Classic Spike Mine","enemy","mine",proceduralFrame("procedural-mine","classic-mine"),{width:18,height:18,hp:2,damage:2,score:150,speed:66,fireRate:99},{pattern:"dive",amplitude:30,frequency:1}),
    legacy("classic-octo","Classic Octo Bot","miniboss","octo",proceduralFrame("procedural-octo","classic-octo"),{width:34,height:34,hp:6,damage:2,score:600,speed:36,fireRate:1.4},{pattern:"orbit",amplitude:95,frequency:1.4}),
    legacy("classic-mech","Classic War Mech","miniboss","mech",proceduralFrame("procedural-mech","classic-mech"),{width:30,height:34,hp:8,damage:3,score:800,speed:27,fireRate:1.2},{pattern:"hoverStrafe",amplitude:105,frequency:.9}),
    legacy("classic-tank","Classic Scout Tank","tank","tank",proceduralFrame("procedural-tank","classic-tank"),{width:40,height:38,hp:6,damage:2,score:550,speed:30,fireRate:1.4},{pattern:"straight"}),
    legacy("classic-heavy-tank","Classic Heavy Cannon Tank","miniboss","htank",proceduralFrame("procedural-heavy-tank","classic-heavy-tank"),{width:46,height:44,hp:12,damage:4,score:950,speed:20,fireRate:1.7},{pattern:"grid",amplitude:18,frequency:.7}),
    legacy("classic-frost","Classic Frost Scout","ice","frost",[
      mainFrame("ice-frost0",245,1525,60,72),mainFrame("ice-frost1",307,1525,58,72)
    ],{width:26,height:28,hp:2,damage:1.5,score:200,speed:72,fireRate:1.8},{pattern:"sine",amplitude:40,frequency:2.8}),
    legacy("classic-ice-gunship","Classic Ice Gunship","miniboss","icegun",[
      mainFrame("ice-gun0",98,1525,70,80),mainFrame("ice-gun1",170,1525,73,80)
    ],{width:36,height:38,hp:7,damage:3,score:650,speed:30,fireRate:1.1},{pattern:"hoverStrafe",amplitude:115,frequency:1}),
    legacy("classic-cryo","Classic Cryo Bomber","miniboss","cryo",[
      mainFrame("ice-cryo0",512,1525,78,67),mainFrame("ice-cryo1",592,1525,78,67)
    ],{width:34,height:30,hp:5,damage:3,score:600,speed:42,fireRate:1.5},{pattern:"pounceRetreat",amplitude:75,frequency:.8}),

    legacy("classic-boss-damkeeper","The Dam Keeper","boss","damkeeper",[
      mainFrame("boss-idle",762,2,158,116),mainFrame("boss-d1",2,2,150,141),mainFrame("boss-d2",154,2,150,140),mainFrame("boss-d3",458,2,150,127),mainFrame("boss-core",2,145,158,116)
    ],{width:170,height:130,hp:340,damage:6,score:5000,speed:32,fireRate:1.5},{pattern:"bossPhases",amplitude:130,frequency:.65}),
    legacy("classic-boss-dreadnought","Hellfire Gunship","boss","dreadnought",[
      mainFrame("boss2-0",608,588,200,187),mainFrame("boss2-1",406,588,200,194),mainFrame("boss2-2",2,588,200,196),mainFrame("boss2-3",204,588,200,196)
    ],{width:150,height:118,hp:460,damage:7,score:10000,speed:34,fireRate:1.2},{pattern:"bossPhases",amplitude:145,frequency:.72}),
    legacy("classic-boss-wargod","The War God","boss","wargod",[
      mainFrame("boss3-0",608,911,200,162),mainFrame("boss3-1",406,911,200,178),mainFrame("boss3-2",2,911,200,181),mainFrame("boss3-3",204,911,200,181)
    ],{width:132,height:122,hp:580,damage:8,score:15000,speed:38,fireRate:1.05},{pattern:"orbit",amplitude:120,frequency:1}),
    legacy("classic-boss-spider","Arachnon MK-IX","boss","spider",proceduralFrame("procedural-arachnon","classic-boss-spider"),{width:160,height:130,hp:700,damage:9,score:20000,speed:40,fireRate:.9},{pattern:"bossPhases",amplitude:155,frequency:.82}),
    legacy("classic-boss-leviathan","Leviathan Core","boss","leviathan",proceduralFrame("procedural-leviathan","classic-boss-leviathan"),{width:170,height:150,hp:820,damage:10,score:25000,speed:42,fireRate:.78},{pattern:"bossPhases",amplitude:165,frequency:.9})
  ];

  const stageDefs = [
    ["rumble-jungle","Rumble in the Jungle",48,66,"#173b20",["vee","sine","gate","side"]],
    ["cinder-jungle","Cinder Jungle",52,72,"#3c2414",["snake","straight","dive","carrier"]],
    ["neon-fortress","Neon Fortress",56,78,"#292631",["grid","side","gate","sine"]],
    ["orbital-grave","Orbital Grave",58,82,"#111527",["fan","side","spiral","straight"]],
    ["fury-core","Fury Core",64,88,"#351313",["bossPhases","side","carrier","spiral"]]
  ];
  const waveUnits = ["scout","weaver","turret","needle","drone","bomber","carrier"];
  const levels = stageDefs.map((s, si) => ({
    id:s[0], name:s[1], duration:s[2], scroll:s[3], background:s[4], boss:entities.filter(e=>e.category==="boss")[si].id,
    spawns:Array.from({length:12},(_,i)=>({ id:`${s[0]}-spawn-${i+1}`, time:+(2.5+i*(s[2]-8)/11).toFixed(1), entityId:waveUnits[(i+si)%waveUnits.length], x:55+((i*83+si*37)%370), y:-35-(i%3)*24, count:i%4===0?5:i%3===0?3:1, interval:i%4===0?.18:.35, pattern:s[5][i%s[5].length], hpMultiplier:1+si*.08 }))
  }));

  return { version:"1.2.0", runtime:{ width:480,height:720,tickRate:60,source:"game.js + assets/game.js" }, patterns, entities, levels };
})();
