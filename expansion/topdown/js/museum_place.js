/*
 * Level 5 placements (pure data, drawn by _research/check_museum_1009.py over the plate).
 *   units:    guard / camera / turret placements; radio is the local radio range (MGS: a guard calls the guards near him)
 *   props:    exhibits ('mx_' kinds) with their FIXED contents - Demolition Man: shoot the art for the power-ups
 *   hostages: Fury ground crew held in the museum, each carrying the reward it hands over when freed
 *   lasers:   tripwire beams between two emitter posts; prone crawls under, shooting a post kills the beam
 */
(function (root) {
  'use strict';
  const PI = Math.PI;
  const u = (type, x, y, wp, extra) => Object.assign({ type, x, y, a: 0, wp: wp || null, radio: 240 }, extra);
  const ex = (kind, x, y, drop) => ({ kind: 'mx_' + kind, x, y, drop: drop || null });
  root.TD_LEVEL5_PLACE = {
    units: [
      // lobby
      u('robotScout', 300, 1290, [[190, 1300], [610, 1300]]), u('robotScout', 450, 1214, [[330, 1214], [470, 1214]]),
      u('camera', 130, 1202, null, { a: -PI / 4 }), u('camera', 670, 1202, null, { a: PI / 4 }),
      // west gallery: stealth wing
      u('robotScout', 90, 800, [[90, 800], [340, 800]], { a: -PI / 2 }), u('robotScout', 120, 600, [[120, 600], [272, 604]], { a: -PI / 2 }),
      u('robotScout', 338, 612, [[338, 612], [338, 705]]), u('camera', 245, 438, null, { a: PI / 2 }),
      // east vehicle hall: armour wing
      u('robotHeavy', 520, 520, [[520, 470], [520, 760]]), u('robotHeavy', 690, 700, [[690, 460], [690, 780]]),
      u('robotScout', 600, 452, [[480, 452], [720, 452]]), u('robotScout', 600, 790, [[480, 790], [720, 790]]),
      u('turret', 720, 410, null, { a: PI / 4 }),
      // rotunda
      u('robotScout', 340, 360, [[340, 360], [460, 360], [460, 448], [340, 448]]), u('camera', 400, 322, null, { a: 0 }),
    ],
    props: [
      ex('statue', 200, 1250, 'grenades'), ex('statue', 600, 1250, 'pow'), ex('vase', 300, 1335, 'ammo'), ex('vase', 500, 1335, 'score'),
      ex('rope', 250, 1205), ex('rope', 550, 1205), ex('alarm', 112, 1350),
      // Hall of Arms: the Museum of Violence's weapon cases sit on the painted plinth sockets
      ex('rifle_case', 139, 895, 'spread_shotgun'), ex('vase', 139, 948, 'ammo'), ex('plasma_case', 139, 1000, 'fusion_beam'), ex('vase', 139, 1052, 'grenades'), ex('statue', 139, 1104, 'crash'),
      ex('rifle_case', 662, 895, 'minigun'), ex('vase', 662, 948, 'ammo'), ex('plasma_case', 662, 1000, 'rocket_launcher'), ex('vase', 662, 1052, 'pow'), ex('statue', 662, 1104, 'life'),
      // gallery
      ex('painting', 240, 604, 'crash'), ex('vase', 122, 806, 'grenades'), ex('alarm', 78, 793),
      // vehicle hall
      ex('statue', 562, 412, 'grenades'), ex('alarm', 470, 418), ex('plasma_case', 722, 600, 'pow'), ex('vase', 470, 805, 'ammo'),
      ex('rope', 540, 640), ex('rope', 660, 640),
      // rotunda + grand hall (the boss arena's cover)
      ex('alarm', 468, 352), ex('statue', 210, 215, 'crash'), ex('statue', 590, 215, 'pow'), ex('vase', 168, 92, 'ammo'), ex('vase', 632, 92, 'grenades'),
    ],
    hostages: [
      { x: 652, y: 1340, body: 'regular', reward: 'grenades' }, { x: 218, y: 752, body: 'female', reward: 'pow' },
      { x: 340, y: 668, body: 'athletic', reward: 'crash' }, { x: 716, y: 806, body: 'heavy', reward: 'pow' }, { x: 430, y: 440, body: 'female', reward: 'life' },
    ],
    lasers: [{ x: 215, y: 584, x2: 215, y2: 626 }, { x: 300, y: 782, x2: 300, y2: 818 }, { x: 160, y: 432, x2: 160, y2: 447 }],
    vehicle: { x: 600, y: 622, a: PI, hp: 14, pilot: 'niel' },
    waves: [
      [['robotScout', 270, 892], ['robotScout', 527, 892], ['robotScout', 400, 900]],
      [['robotHeavy', 270, 892], ['robotScout', 527, 892], ['robotScout', 330, 900], ['robotHeavy', 527, 900]],
      [['robotHeavy', 400, 896], ['robotScout', 270, 892], ['robotScout', 527, 892], ['robotScout', 220, 960], ['robotScout', 580, 960]],
    ],
    gates: [[400, 1380], [270, 890], [527, 890], [600, 420], [230, 440], [400, 330]],
    checkpoints: [[400, 1100], [400, 845], [400, 480]],
    bossLine: 300, boss: { x: 400, y: 150 },
  };
}(window));
