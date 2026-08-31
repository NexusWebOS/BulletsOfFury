/* Static integration proof for the 2026-08-31 cinematic, Stage 2-6 boss and audio pass. */
const fs=require('fs');
const game=fs.readFileSync('assets/game.js','utf8');
const html=fs.readFileSync('index.html','utf8');
const checks=[];
function ok(name,pass){checks.push({name,pass:!!pass});if(!pass)throw new Error(name);}
function pos(needle){const p=game.indexOf(needle);if(p<0)throw new Error(`Missing: ${needle}`);return p;}

ok('Cinematics own the full browser viewport',
  /body\.cinematic-full #game-frame/.test(html)&&/width:100vw/.test(html)&&/height:100vh/.test(html));
ok('Cinematic backing width follows the browser aspect ratio',
  /function _setCinematicViewport\(on\)/.test(game)&&/Math\.round\(VH\*ar\)/.test(game)&&
  /_setCinematicViewport\(s===GS\.CUTSCENE\)/.test(game));
ok('HQ command deck V2 is the active cinematic plate',
  /cut_furyhq_command_center[^\n]*hq_command_deck_v2\.png/.test(game)&&/cutsceneViewWidth\(\)/.test(game));
ok('Dialogue is centered with a four-way black contour',
  (game.match(/msgText\(_part[^\n]*'#000000'/g)||[]).length>=4&&
  /msgText\(_part,_cx,_yy,_H,DIALOGUE_BODY_COLOR/.test(game));

ok('Stage 5 sky fades continuously into space during assembly',
  /function stage5SpaceAscentProgress/.test(game)&&/if\(p==='scatter'\)return \.08\+\.22/.test(game)&&
  /ctx\.globalAlpha=p\*p\*\(3-2\*p\)/.test(game));
for(const key of ['spaceLaserCannon','spaceLaserHit','spaceShadowCharge','spaceShadowRelease',
  'spaceShadowHit','spaceVolleyLaunch','spaceVolleyHit']){
  ok(`${key} is a foreground native sound`,new RegExp(`${key}:\\s*\\{[^}]*native:true`).test(game));
}

ok('Stage 2 shield hit ramp is red to grey to white',
  /ratio>\.66\?'#ff2f18':\(ratio>\.33\?'#8b8b8b':'#ffffff'\)/.test(game));
ok('Stage 2 boss projectiles are high-visibility yellow orange',
  /xartTint\(k,'#ffb51f'/.test(game)&&/shadowColor='#ff7b16'/.test(game));
ok('Stage 2 flame art is enlarged',
  (game.match(/drawImage\(im,-62,0,124,/g)||[]).length>=2&&/drawImage\(im,-84,0,168,/.test(game));

ok('Stage 3 fortress uses the Axel Falva helper laser art',
  /const hk='nlz_3_b'/.test(game)&&/s3wallcannons[\s\S]*?width:44/.test(game)&&
  /l23BossBeamStart\(b,'rime',[^\n]*46\)/.test(game));

ok('Stage 4 boss fires authored lightning rounds at a reduced cadence',
  /S\.coreSpreadCd=Math\.max\(\.82,1\.04/.test(game)&&
  /'lightningmg'/.test(game)&&/S\.shot\+=phase>=3\?\.105:\.132/.test(game));
ok('Stage 4 helper damage is routed before the carrier shield',
  pos("stage4CoreTurretAbsorbHit==='function'")<pos("stage4ShieldAbsorbHit==='function'"));
ok('Stage 4 helper targets are tested before the carrier hull',
  pos("boss._s4CoreHit=stage4CoreTurretAt")<pos('const _hw = boss.w*0.42'));

ok('Maverick ordinary laser uses a per-volley damage budget',
  /const perLance=dmg\*\(0\.34\+lv\*0\.025\)/.test(game));
ok('Lizzie mounted rounds are another 25 percent slower',/const LZ_SLUG_SPD = 7\.875/.test(game));

ok('Stage 5 Regent has shootable mothership and helper targets',
  /function xenoRegentInit/.test(game)&&/function xenoRegentPartDamage/.test(game)&&
  /_xenoOwner/.test(game)&&/xenoRegentShieldAbsorb/.test(game));
ok('Regent mothership shield breaks only with the mothership',
  /part\.role==='mother'&&b&&b\._xenoRig/.test(game)&&/b\._xenoRig\.shield=false/.test(game));
ok('Regent uses authored alien ammunition',
  /'s5fracture'/.test(game)&&/'s5null'/.test(game)&&/'s5halo'/.test(game)&&/'s5chaos'/.test(game));

ok('Stage 6 miniboss has dedicated tracer missile and lightning modes',
  /function stage6MiniTick/.test(game)&&/mode==='tracer'/.test(game)&&/mode==='missile'/.test(game)&&
  /mode==='storm'/.test(game)&&/'lightningmg'/.test(game)&&/'s6missile'/.test(game)&&/'s6bolt'/.test(game));
ok('Stage 6 miniboss uses authored muzzle and attack frames',
  /s6mb_cyclonemuzzle_/.test(game)&&/s6atk_reactor_storm_bomber_/.test(game));

console.log(JSON.stringify({pass:true,checks},null,2));
