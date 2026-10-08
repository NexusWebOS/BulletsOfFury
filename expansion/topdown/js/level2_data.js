/*
 * Level 2 "IRON INFILTRATION" - placement. Headings: a=0 faces south, PI north, -PI/2 east, PI/2 west.
 * The route runs south -> north up the compound's main road (x 310..480) with four cross streets;
 * every patrol is laid on open ground and checked against the solid map by _research/check_map.py.
 */
(function (root) {
  'use strict';
  const N = Math.PI, E = -Math.PI / 2, Wd = Math.PI / 2, S = 0;
  root.TD = root.TD || {};
  root.TD.LEVEL2_DATA = {
    title: 'LEVEL 2', name: 'IRON INFILTRATION',
    brief: ['THE WARRIOR HOLDS THE COMMAND PLAZA.', 'BREAK ITS ARMS AND HELMET, THEN THE CHASSIS.',
      'BUILDINGS AND ARENA COVER CAN BE DESTROYED.', 'ITS RAM SMASHES WALLS. KEEP A CLEAR ESCAPE.'],
    start: { x: 400, y: 3540, a: N },
    checkpoints: [[400, 3000], [400, 2230], [400, 1460], [400, 830]],
    bossLine: 690, boss: { x: 400, y: 305 },
    structures: [
      ...[3380, 3035, 2670, 2200, 1845, 1450, 1060].flatMap((y, i) => [
        { kind: i % 3 === 1 ? 'relay' : 'warehouse', x: 245, y },
        { kind: i % 3 === 2 ? 'relay' : 'warehouse', x: 555, y, drop: i === 5 ? 'homing' : null },
      ]),
      { kind: 'barrier', x: 240, y: 555 }, { kind: 'barrier', x: 560, y: 555 },
      { kind: 'barrier', x: 215, y: 425 }, { kind: 'barrier', x: 585, y: 425 },
      { kind: 'barrier', x: 275, y: 330 }, { kind: 'barrier', x: 525, y: 330 },
    ],
    gates: [[400, 3610], [400, 2400], [400, 1500], [400, 830]],
    units: [
      // south gate
      { type: 'camera', x: 292, y: 3392, a: E },
      { type: 'scout', x: 200, y: 3290, a: Wd, wp: [[150, 3290], [650, 3290]] },
      { type: 'rifle', x: 430, y: 3150, a: S, wp: [[430, 3150], [430, 3010]] },
      { type: 'camera', x: 508, y: 3062, a: Wd },
      // the garden crossing
      { type: 'turret', x: 520, y: 2950, a: Wd },
      { type: 'heavy', x: 440, y: 2790, a: S, wp: [[440, 2790], [440, 2690]] },
      { type: 'scout', x: 150, y: 2645, a: Wd, wp: [[150, 2645], [650, 2645]] },
      { type: 'camera', x: 305, y: 2445, a: S },
      { type: 'sniper', x: 400, y: 2415, a: S },
      // office blocks
      { type: 'rifle', x: 120, y: 2110, a: E, wp: [[120, 2110], [680, 2110]] },
      { type: 'scout', x: 340, y: 2350, a: N, wp: [[340, 2350], [340, 1790], [460, 1790], [460, 2350]] },
      { type: 'turret', x: 300, y: 1880, a: E },
      { type: 'camera', x: 500, y: 1765, a: S },
      { type: 'sniper', x: 400, y: 1560, a: S },
      // terraces
      { type: 'turret', x: 400, y: 1395, a: S },
      { type: 'heavy', x: 400, y: 1300, a: S, wp: [[330, 1300], [470, 1300]] },
      { type: 'rifle', x: 300, y: 1040, a: E, wp: [[280, 1040], [520, 1040]] },
      { type: 'scout', x: 520, y: 1200, a: N, wp: [[520, 1200], [520, 900], [300, 900], [300, 1200]] },
      { type: 'camera', x: 262, y: 880, a: S },
      { type: 'heavy', x: 560, y: 860, a: S },
    ],
    props: [
      { kind: 'barrel', x: 360, y: 3300 }, { kind: 'barrel', x: 374, y: 3320 }, { kind: 'barrel', x: 352, y: 3324 },
      { kind: 'crate', x: 462, y: 3420, drop: 'crash' },
      { kind: 'pbox', x: 340, y: 3330, drop: 'laser' }, { kind: 'crate', x: 462, y: 3210, drop: 'homing' },
      { kind: 'crate', x: 330, y: 2900, drop: 'repair' }, { kind: 'pbox', x: 600, y: 2960, drop: 'laser' },
      { kind: 'pbox', x: 680, y: 2645, drop: 'life' },
      { kind: 'barrel', x: 490, y: 1990 }, { kind: 'barrel', x: 506, y: 2008 }, { kind: 'barrel', x: 490, y: 2026 },
      { kind: 'crate', x: 290, y: 2240, drop: 'smoke' },
      { kind: 'pbox', x: 380, y: 1180, drop: 'repair' }, { kind: 'crate', x: 440, y: 910, drop: 'homing' },
      { kind: 'barrel', x: 330, y: 1480 }, { kind: 'barrel', x: 470, y: 1480 },
    ],
  };
  if (typeof module !== 'undefined') module.exports = root.TD.LEVEL2_DATA;
}(typeof window !== 'undefined' ? window : globalThis));
