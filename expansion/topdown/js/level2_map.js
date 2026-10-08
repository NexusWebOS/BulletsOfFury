/*
 * Level 2 map data: the compound plate (nst4b_master, 800x3616) and its solid rectangles.
 * Authored by hand off a gridded render of the plate's LEFT half and mirrored, because the plate is
 * built mirror-symmetric. 'b' building/wall, 'h' hedge (hides you, blocks sight, tanks push through
 * slowly), 'v' a pit punched through the plate (blocks movement, not sight).
 * _research/check_map.py renders these over the plate - re-run it after any edit.
 */
(function (root) {
  'use strict';
  const LEFT = [
    // north plaza flanks (the boss arena is x 175..625, y 0..760)
    [0, 200, 170, 375, 'b'], [170, 258, 214, 355, 'v'], [70, 376, 168, 400, 'v'], [70, 376, 94, 510, 'v'], [0, 495, 94, 575, 'v'],
    [0, 383, 70, 495, 'b'], [0, 600, 125, 760, 'b'], [170, 645, 214, 742, 'v'], [172, 462, 262, 552, 'b'],
    // the terraces south of the plaza
    [120, 740, 200, 848, 'b'], [0, 830, 94, 870, 'v'], [0, 965, 200, 1000, 'h'], [0, 1060, 200, 1100, 'h'], [200, 965, 250, 1100, 'h'],
    [13, 1103, 200, 1260, 'b'], [222, 1150, 258, 1285, 'v'], [100, 1268, 225, 1298, 'v'], [0, 1298, 105, 1340, 'v'],
    [256, 1130, 295, 1300, 'h'], [0, 1340, 200, 1380, 'h'], [268, 1365, 345, 1425, 'b'], [0, 1465, 75, 1500, 'h'],
    // the office blocks
    [0, 1480, 165, 1590, 'b'], [165, 1520, 260, 1580, 'h'], [0, 1626, 207, 1648, 'v'], [0, 1626, 24, 1730, 'v'], [180, 1626, 207, 1700, 'v'],
    [24, 1650, 180, 1745, 'b'], [222, 1600, 242, 1745, 'h'], [0, 1842, 90, 1875, 'h'], [126, 1845, 155, 1898, 'h'], [176, 1806, 262, 1842, 'h'],
    [0, 1940, 97, 2082, 'b'], [127, 1907, 265, 2082, 'b'], [263, 1905, 288, 2085, 'h'], [0, 2080, 288, 2100, 'h'], [0, 2122, 88, 2158, 'v'],
    [378, 1935, 400, 2185, 'b'], [378, 1800, 400, 1890, 'b'],
    // the plaza and garden block
    [0, 2322, 48, 2382, 'v'], [0, 2300, 57, 2395, 'b'], [0, 2465, 240, 2615, 'b'], [380, 2447, 400, 2620, 'b'],
    [10, 2678, 293, 2708, 'h'], [8, 2678, 30, 2905, 'h'], [43, 2738, 195, 2922, 'b'], [230, 2705, 297, 2762, 'h'], [230, 2845, 297, 2908, 'h'],
    // the residential blocks at the south gate
    [10, 3025, 297, 3052, 'h'], [22, 3092, 262, 3222, 'b'], [0, 3218, 300, 3236, 'h'], [0, 3330, 287, 3368, 'h'], [40, 3378, 240, 3548, 'b'],
    [0, 3330, 30, 3600, 'h'], [0, 3550, 290, 3582, 'h'], [247, 3490, 290, 3582, 'h'],
  ];
  const RECTS = [];
  for (const r of LEFT) { RECTS.push(r); if (r[2] <= 400) RECTS.push([800 - r[2], r[1], 800 - r[0], r[3], r[4]]); }
  root.TD = root.TD || {};
  // Open authored sectors replace the baked, indestructible building plate.
  // Only the arena perimeter and outside hedges are static; scenery is dynamic.
  root.TD.LEVEL2_MAP = { key: 'compound_ground', w: 800, h: 3600, rects: [
    [0, 0, 800, 75, 'b'], [0, 75, 60, 680, 'b'], [740, 75, 800, 680, 'b'],
    [0, 680, 310, 800, 'b'], [490, 680, 800, 800, 'b'],
    [0, 800, 75, 3600, 'h'], [725, 800, 800, 3600, 'h'],
  ] };
  if (typeof module !== 'undefined') module.exports = root.TD.LEVEL2_MAP;
}(typeof window !== 'undefined' ? window : globalThis));
