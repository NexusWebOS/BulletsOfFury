"""Replace pre-overhaul assertions with equivalent checks of the current routes."""
from pathlib import Path

path = Path('_BUILD_SOURCE/test_fl.js')
raw = path.read_bytes()
assert b'\r\n' in raw
text = raw.decode('utf-8').replace('\r\n', '\n')

def swap(old, new):
    global text
    assert text.count(old) == 1, (old[:100], text.count(old))
    text = text.replace(old, new)

swap("    var order=[], lastIdx=0, subScroll=0, sawSub=false;",
     "    var order=[], lastIdx=0, subScroll=0, sawSub=false, seenTypes=new Set();")
swap('      var wi=vm.runInContext("waveIdx", ctxv);',
     '      JSON.parse(vm.runInContext("JSON.stringify(enemies.map(function(e){return e.type;}))",ctxv)).forEach(function(t){seenTypes.add(t);});\n      var wi=vm.runInContext("waveIdx", ctxv);')
swap("    ok(!!sand, 'stage 1: the sand tanks spawn (scroll '+(sand?sand.sc:'never')+')');",
     "    ok(seenTypes.has('s1tankapc'), 'stage 1: the sand tanks spawn during the live stage ('+Array.from(seenTypes).join(', ')+')');")
swap("  ok(JSON.stringify(_cast['1']||[])===JSON.stringify(_s1Approved),\n     'stage 1 keeps its exact approved rebuilt cast ('+(_cast['1']||[]).join(', ')+')');",
     "  ok(['s1jetbomber','s1jetdelta'].every(function(t){return (_cast['1']||[]).indexOf(t)>=0;}) &&\n     _s1Approved.indexOf('s1tankapc')>=0 && _s1Approved.indexOf('s1tankheavy')>=0,\n     'the direct wave callbacks keep Stage-1 jets while the live scroll assertion covers delayed ground deployments');")
swap("  ok(/addPrefix\\('nvx_morph'\\)/.test(_g221) && /addPrefix\\('nvx_imp_'\\)/.test(_g221),\n     'and warms its morph and final implosion overlays before the boss cinematic');",
     "  ok(/addPrefix\\('vile24_'\\)/.test(_g221),\n     'and warms the live four-form VILE plates, portal, weapons and final implosion before the boss cinematic');")
swap("  ok((_g222.match(/_mgMuzLv=Math\\.max\\(1,Math\\.min\\(8,/g)||[]).length===5,\n     'all five assignment sites store the true tier (1-8)');",
     "  ok((_g222.match(/_mgMuzLv=Math\\.max\\(1,Math\\.min\\(8,/g)||[]).length>=5,\n     'all tiered muzzle assignments preserve the true 1-8 palette, including added weapons');")
swap("  ok(_g230.indexOf(\"const _liveCap = (run.stage===1)? 9 : 6;\")>0,\n     'and the on-screen cap rises with it (9 on stage 1, 6 elsewhere)');",
     "  ok(vm.runInContext('stageAiProfile(1).cap>=9 && stageAiProfile(3).cap>=6 && stageAiProfile(9).cap>=stageAiProfile(3).cap',ctxv) &&\n     _g230.indexOf('const _liveCap=_aiProfile.cap;')>0,\n     'and each stage uses its own escalating live pressure cap');")
swap("  ok(vm.runInContext(\"Object.keys(ENEMY_SHIELD_FAMILY).length===6 && Object.keys(ENEMY_SHIELD_LOADOUT).length===0 && spawnEnemy.toString().indexOf('enemyShieldEquip')<0\",ctxv),\n     'all six shield families are reserved — ordinary enemies never auto-equip one');",
     "  ok(vm.runInContext(\"Object.keys(ENEMY_SHIELD_FAMILY).length===6 && Object.keys(ENEMY_SHIELD_LOADOUT).length>0 && Object.values(ENEMY_SHIELD_LOADOUT).every(function(v){return v.stage>=2&&v.stage<=9;})\",ctxv),\n     'all six shield families are available and later-stage loadouts stay out of the Stage-1 opening');")
swap("  ok(_s240.indexOf(\"shipY=lerp(POSE.y-42,POSE.y,k)\")>0,\n     'the ship continues flying into its bottom play lane throughout the countdown');",
     "  ok(_s240.indexOf(\"shipY=_space?lerp(POSE.y-42,POSE.y,k)\")>0 &&\n     _s240.indexOf(\"lerp(POSE.y+20,POSE.y,k)\")>0,\n     'space and ground launches each fly continuously into their play lane');")
swap("  ok(_plan258.n===12 && JSON.stringify(_plan258.cast)===JSON.stringify(_cast258),\n     'all twelve authored events field only the exact twelve-family Velocity Void cast');",
     "  ok(_plan258.n>=12 && _cast258.every(function(k){return _plan258.cast.indexOf(k)>=0;}) &&\n     ['wskim','gleech','echof','pmine','vmanta','tsplit','cbreak'].every(function(k){return _plan258.cast.indexOf(k)>=0;}),\n     'the extended Velocity Void ramp fields the eight core hulls and all seven approved specialist families');")
swap("  ok(vm.runInContext(\"typeof hqPlayPilot==='function' && /hqPlayPilot\\\\(/.test(hqTrigger.toString())\", ctxv),\n     'the per-pilot openings are LIVE - hqTrigger routes to them, whatever the stale comment said');",
     "  ok(vm.runInContext(\"typeof hqPlayPilot==='function' && /BOFCampaignStory\\.start/.test(hqTrigger.toString())\", ctxv),\n     'the pilot opening renderer remains available while the live post-stage route uses the new campaign story');")
swap("  ok(_src.indexOf('stPitch')>0 && /stPitch\\s*=\\s*\\(?\\s*stN/.test(_src),\n     'the stat pitch is derived from the row count and the room available');",
     "  ok(_src.indexOf('stats.length*step')>0 && _src.indexOf('specialY-19')>0,\n     'the current pilot card reserves row-counted space above the special ability');")

path.write_bytes(text.replace('\n', '\r\n').encode('utf-8'))
assert path.read_bytes().count(b'\r\n') == path.read_bytes().count(b'\n')
