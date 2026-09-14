/* Focused regression probe for the 0830 flamethrower + timed weapon HUD repair. */
'use strict';
const fs=require('fs'), vm=require('vm'), path=require('path');
const ROOT=path.resolve(__dirname,'..');
const src=fs.readFileSync(path.join(ROOT,'assets/game.js'),'utf8');
let failed=0;
function ok(v,msg){ console.log((v?'PASS ':'FAIL ')+msg); if(!v)failed++; }
function between(a,b){ const i=src.indexOf(a),j=src.indexOf(b,i+1); return (i>=0&&j>i)?src.slice(i,j):''; }

const hitFn=between('function weaponHitSfx(el){','function flameHit(');
const hitCtx={stateT:8,HITSFX_GAP:.09,_hitSfxAt:{},Audio:{SFX:{hit(){hitCtx.calls++;}}},calls:0};
vm.runInNewContext(hitFn,hitCtx);
hitCtx.weaponHitSfx('fire');
hitCtx.stateT=0; hitCtx.weaponHitSfx('fire');             // a state-clock rewind must not mute
hitCtx.stateT=.03; hitCtx.weaponHitSfx('fire');           // ordinary 90ms throttle still applies
hitCtx.stateT=.10; hitCtx.weaponHitSfx('fire');
ok(hitCtx.calls===3,'normal weapon impacts survive a stateT reset and remain rate-limited');

const hudFn=between('function timedWeaponHUDRows(){','function drawHeavyTurretHUD(){');
function rowsFor(opt){
  const c={clamp:(v,a,b)=>Math.max(a,Math.min(b,v)),LZ_LIFE:15,DK_LIFE:15,
    lzMount:opt.lz||null,run:opt.run||{},sonicActive:()=>!!opt.sonic,dkActive:()=>!!opt.dk};
  vm.runInNewContext(hudFn,c); return c.timedWeaponHUDRows();
}
const lr=rowsFor({lz:{docked:true,life:9}})[0];
const cr=rowsFor({sonic:true,run:{sonicT:12}})[0];
const dr=rowsFor({dk:true,run:{dkT:7}})[0];
ok(lr&&lr.icon==='nsw_icon_lizzie'&&lr.label.includes('9s'),'Lizzie gets a timed Heavy MG bar');
ok(cr&&cr.icon==='nsw_icon_cole'&&cr.label.includes('12s'),'Cole gets a timed Sonic Boom bar');
ok(dr&&dr.icon==='nsw_icon_decker'&&dr.label.includes('7s'),'Decker gets a timed Shotgun bar');

const cadFn=between('function _weaponCadence(){','function flameReach(');
const cadCtx={run:{spaceMode:false,weapon:0,wlevels:[0]},spaceWeaponsActive:()=>false,
  lzMountActive:()=>true,LZ_SLUG_CD:.055};
vm.runInNewContext(cadFn,cadCtx);
ok(cadCtx._weaponCadence()===.055,'docked Lizzie mount owns a 55ms trigger cadence');

const ps=between('function pShoot(){','function updatePlayerLocks');
ok(!/lzMountActive[\s\S]{0,260}run\._lzCd/.test(ps),'Lizzie firing has one cadence owner, not a second hidden cooldown');
const flameTick=between("if(b.kind==='flame'){","if(b.kind==='orb'){");
ok(flameTick.includes('flameSndStart(b._el)'), 'live flame entity refreshes its sustained audio bed every frame');
const begin=between('function beginStage(num){','function coleSceneApply');
ok(begin.includes("loopPrepare('flameThrowerLoop')")&&begin.includes("'hit'"),
   'stage entrance preloads flamethrower loop and shared normal impact sample');
ok(begin.includes("loopPrepare('laserBeamLoop')")&&begin.includes("'hit'"),
   'stage entrance preloads laser beam loop and shared normal impact sample');
const loopAudio=between('A._loopPlay=function(L){','A.startMusic=function(name)');
ok(loopAudio.includes('A._resumeHeldContext')&&loopAudio.includes('c.resume')&&loopAudio.includes('L.playing'),
   'held weapon loops recover a suspended WebAudio graph instead of silently latching');

const pickup=between("if(p.kind==='sonicbox' || p.kind==='lzmgbox' || p.kind==='dkshotbox')","if(p.kind==='special' || p.kind==='specialicon')");
ok(pickup.includes("'nsw_icon_decker'")&&pickup.includes('iconBlit(ctx,_k')&&!pickup.includes("'ndk_shell_0'"),
   'Decker pickup uses the authored shotgun badge and has no shell fallback');
const manifestText=fs.readFileSync(path.join(ROOT,'assets/manifest.js'),'utf8');
const manifest=JSON.parse(manifestText.match(/window\.BOFX=([\s\S]*?\});/)[1]);
const rect=manifest.icons&&manifest.icons.nsw_icon_decker;
ok(rect&&rect[4]==='bof_player_weapon_special_icons_atlas','shotgun badge resolves from the production icon atlas');

for(const f of ['reviewed_flamethrower_start.wav','reviewed_flamethrower_loop.wav',
                 'reviewed_flamethrower_end.wav','reviewed_player_laser_beam_start.wav',
                 'reviewed_player_laser_beam_loop.wav','reviewed_player_laser_beam_end.wav',
                 'explosion_air_small_01.wav']){
  const p=path.join(ROOT,'assets/game/sounds',f);
  ok(fs.existsSync(p)&&fs.statSync(p).size>10000,'audio sample present: '+f);
}
process.exitCode=failed?1:0;
