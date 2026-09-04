'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const game = fs.readFileSync(path.join(root, 'assets', 'game.js'), 'utf8');
let passed = 0;

function ok(condition, message) {
  if (!condition) throw new Error('ENDING QA FAILED: ' + message);
  passed += 1;
}

const pilots = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri'];
for (const pilot of pilots) {
  ok(new RegExp('\\b' + pilot + ':\\{head:').test(game), pilot + ' has a pilot-specific ending');
  for (const file of ['04_rear_left_3q.png', '05_rear_right_3q.png', '07_center_rear.png']) {
    ok(fs.existsSync(path.join(root, 'assets', 'game', 'cinematic_ships', pilot, 'cutouts_native', file)), pilot + ' has ' + file);
  }
}

const assets = [
  'ending_fury_hq_restored_dawn_v1.png',
  'ending_damaged_satellite_dish_v1.png',
  'ending_symbiote_ooze_survivor_rgba_v2.png',
  'ending_bof2_shadow_mech_rgba_v2.png',
  'ending_deep_space_starfield_v1.png'
];
for (const file of assets) {
  ok(fs.existsSync(path.join(root, 'assets', 'game', 'cinematic_campaign', 'ending_generated', file)), file + ' exists');
  ok(game.includes(file), file + ' is registered by the runtime');
}

ok(game.includes("s===GS.CUTSCENE || s===GS.CAMPAIGNINTRO || s===GS.VICTORY"), 'victory owns the widescreen cinematic viewport');
ok(game.includes("function victoryRearView(){return 7;}"), 'every ending selects the dedicated centered rear ship');
ok(game.includes("cinDrawShip(pk,rv,x,y,h,false,aShip,0)"), 'restoration flies away straight with no three-quarter rotation');
ok((game.match(/const side=i-\(cast\.length-1\)\/2,sep=\.54-\.28\*e;/g)||[]).length>=2, 'two-pilot approaches preserve non-overlapping formation spacing');
ok((game.match(/cinDrawShip\(p,7,W\*\(\.50\+side\*sep\)/g)||[]).length>=2, 'HQ and jungle approaches use the centered rear view');
ok(game.includes("cinShipKey(pk,victoryRearView(pk))"), 'the selected pilot rear view is warmed before the ending');
ok(game.includes("s===GS.STAGECLEAR && run.stage>=CAMPAIGN_STAGES && !(curStage&&curStage.bonus)"), 'final-stage results prewarm the ending without warming it for the bonus stage');
ok(game.includes("if(!drawVictory._ready){") && game.includes("if(!victoryEndingReady())return;"), 'the ending clock is held until every required plate and the dialogue face are ready');
ok(game.includes("cinCover('cinend_deep_space'"), 'the sequel contact and jump-scare use the dedicated deep-space plate');
ok(!game.includes("const earth=clamp(1-q/3.2"), 'the old atmospheric Earth/sky layer is absent from the sequel approach');
ok(game.includes('victoryCaption(E.head,E.body'), 'pilot-specific copy is drawn through the cinematic dialogue face');
ok(game.includes('SPACE FEDERATION - PRIORITY CHANNEL'), 'Space Federation warning is present');
ok(game.includes('victorySprite(\'cinend_bof2_shadow\''), 'BOF2 shadow form is animated at the camera');
ok(game.includes("strokeStyle='rgba(0,3,1,'") && game.includes("strokeStyle='rgba(82,255,108,'"), 'survivor launch uses a black ooze trail with restrained green virus light');
ok(game.includes("Math.sin(q*8)*.015,.90"), 'BOF2 model remains heavily shadowed during the jump-scare');
ok(game.includes("s7WardenMechSound('scream')"), 'mechanical scream cue is wired');
ok(game.includes("msgText('BULLETS OF FURY,'") && game.includes("msgText('WILL RETURN!'"), 'return card matches final copy');
ok(!game.includes('ALL 5 STAGES CLEARED.'), 'obsolete five-stage ending copy is removed');

console.log('ENDING CINEMATIC QA OK - ' + passed + ' checks');
