/*
 * Level 5 - MUSEUM OF VIOLENCE: the solid map and the authored placements, as pure data so
 * _research/check_museum_1009.py can draw every rectangle and unit over the plate.
 * World = the 800x1422 plate. Rect types (core.js): 'b' wall, 'h' hedge, 'v' pit, 'd' duct (crawl only).
 * Rotunda ring rects are generated in museum.js from RING (centre, radius, thickness, door arcs).
 */
(function (root) {
  'use strict';
  const PI = Math.PI;
  root.TD_LEVEL5 = {
    w: 800, h: 1422,
    rects: [
      // outer shell and the grand hall's column banks
      [0, 0, 800, 10, 'b'], [0, 0, 100, 345, 'b'], [700, 0, 800, 345, 'b'], [0, 345, 58, 1422, 'b'], [742, 345, 800, 1422, 'b'],
      // grand hall south wall either side of the rotunda
      [0, 340, 290, 384, 'b'], [510, 340, 800, 384, 'b'],
      // WEST GALLERY partitions (paintings hang on every one of these)
      [50, 370, 226, 425, 'b'], [62, 455, 102, 502, 'b'], [140, 448, 238, 500, 'b'], [140, 448, 155, 580, 'b'], [270, 452, 298, 500, 'b'],
      [60, 525, 110, 580, 'b'], [185, 525, 255, 580, 'b'], [287, 550, 360, 600, 'b'], [298, 500, 358, 550, 'b'],
      [60, 620, 105, 645, 'b'], [140, 620, 200, 660, 'b'], [245, 645, 320, 700, 'b'], [130, 672, 200, 740, 'b'],
      [60, 705, 100, 775, 'b'], [185, 720, 200, 780, 'b'], [235, 722, 275, 780, 'b'], [312, 722, 360, 780, 'b'],
      [358, 500, 380, 850, 'b'],                                   // gallery east wall = divider west face
      [50, 820, 240, 880, 'b'], [298, 820, 380, 880, 'b'],         // gallery south wall, door x 240-298
      // the divider's unlit service corridor: prone only, hides you, guards cannot follow
      [380, 505, 420, 878, 'd'],
      // EAST VEHICLE HALL
      [420, 500, 446, 850, 'b'], [420, 830, 498, 880, 'b'], [556, 830, 800, 880, 'b'],
      // HALL OF ARMS (Smash TV room): side galleries behind the plinths, south wall with the lobby arch
      [0, 860, 112, 1180, 'b'], [690, 860, 800, 1180, 'b'], [0, 1130, 300, 1185, 'b'], [500, 1130, 800, 1185, 'b'],
      // LOBBY reception desks and the front wall (the glass doors are behind you)
      [55, 1215, 120, 1335, 'b'], [680, 1215, 745, 1335, 'b'], [0, 1362, 340, 1422, 'b'], [460, 1362, 800, 1422, 'b'], [340, 1394, 460, 1422, 'b'],
    ],
    ring: { x: 400, y: 397, r: 104, t: 22, doors: [[-PI / 2, 0.34], [PI, 0.43], [0, 0.43], [PI / 2, 0.20]] },   // doors: top, west, east, duct mouth (centre angle, half-width in radians)
    // the Smash TV lock: laser curtains across every doorway of the Hall of Arms
    curtains: [[300, 1152, 500, 1152], [240, 856, 298, 856], [498, 856, 556, 856], [380, 874, 420, 874]],
    start: { x: 400, y: 1345, a: PI },
  };
}(window));
