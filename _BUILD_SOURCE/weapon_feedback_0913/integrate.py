"""Integrate the four-weapon feedback pass into the measured 0913 build."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
path=ROOT/'assets/game.js';s=(ROOT/'_shots/weapon_feedback_0913/game.before.js' if '--source-before' in sys.argv else path).read_text(encoding='utf-8')
if 'function weaponFeedbackArt('in s:raise SystemExit('Already integrated; edit the current runtime or regenerate from a reviewed snapshot.')
changes=[]
def replace(a,b,count=1):
    global s
    assert s.count(a)>=count,a[:100]
    s=s.replace(a,b,count);changes.append(a[:80])
def fn(name,source):
    global s
    p=s.index('function '+name+'(');q=s.index('\n}',p)+2
    s=s[:p]+source.rstrip()+s[q:];changes.append(name)
replace('function chargeAvailable(){',(HERE/'feedback.js').read_text()+'\nfunction chargeAvailable(){')
replace('function updatePlay(dt){\n  _lastDt=dt;', "function updatePlay(dt){\n  _lastDt=dt;\n  // A dead pilot no longer reaches the movement pass that normally owns chargeTick.\n  if(player.dead&&(player._chgOn||player._chgDash)){\n    player._chgDash=null;player._chgOn=false;player._chgT=0;player._chgGhosts=[];\n    weaponFeedbackOff('juggernautChargeLoop');weaponFeedbackOff('juggernautRamLoop');\n  }")
replace('if(!_axelAegis && player.invuln>0 && (Math.floor(player.invuln/4)%2)) return;', 'if(!_axelAegis && !chargeDashing() && player.invuln>0 && (Math.floor(player.invuln/4)%2)) return;')
replace('  player._chgOn=true; player._chgT=0;','  player._chgOn=true; player._chgT=0;\n  weaponFeedbackWarm("juggernaut");')
replace("(Audio.SFX.sonicChargeStart||Audio.SFX.fireIceChargeStart||Audio.SFX.select||function(){})();","weaponFeedbackSound('juggernautChargeStart');")
replace('  player._chgOn=false; player._chgT=0;\n  if(t<CHG_ARM)',"  player._chgOn=false; player._chgT=0;\n  weaponFeedbackOff('juggernautChargeLoop');\n  if(t<CHG_ARM)")
replace('  player._chgGhosts=[]; player._chgGhostT=0;',"  player._chgGhosts=[]; player._chgGhostT=0;\n  weaponFeedbackBurst('ram',player.x,player.y+12,72+44*k,.30);")
replace("(Audio.SFX.maverickHelixRelease||Audio.SFX.coleSonicBoom||Audio.SFX.arcBarrelRoll||Audio.SFX.dash||function(){})();", "weaponFeedbackSound('juggernautRamLaunch',.65+.35*k);")
replace("  const d=player._chgDash;\n  if(d){", "  if(player.dead){player._chgDash=null;player._chgOn=false;player._chgT=0;player._chgGhosts=[];weaponFeedbackOff('juggernautChargeLoop');weaponFeedbackOff('juggernautRamLoop');return;}\n  const d=player._chgDash;\n  if(d){\n    weaponFeedbackLoop('juggernautRamLoop',.45+.45*d.k);")
replace('      player._chgDash=null;',"      player._chgDash=null;\n      weaponFeedbackOff('juggernautRamLoop');\n      weaponFeedbackBurst('ram',player.x,player.y-8,56+28*d.k,.28);")
replace("const _f=Audio.SFX.explosionAirSmall01||Audio.SFX.explode; if(_f) _f();","weaponFeedbackSound('juggernautRamStop',.65+.35*d.k);")
replace('    if(player._chgOn){ player._chgOn=false; player._chgT=0; }',"    if(player._chgOn){ player._chgOn=false; player._chgT=0; }\n    weaponFeedbackOff('juggernautChargeLoop');")
replace('    player._chgT=Math.min(CHG_FULL,(player._chgT||0)+dt);',"    player._chgT=Math.min(CHG_FULL,(player._chgT||0)+dt);\n    weaponFeedbackLoop('juggernautChargeLoop',.25+.55*chargeLevel());")
src=(HERE/'charge_draw.js').read_text();fn('drawChargeFX',src[:src.index('function drawWreckBalls')]);fn('drawWreckBalls',src[src.index('function drawWreckBalls'):])
replace('const WB_DRAW=15;', 'const WB_DRAW=17;')
replace('function wreckInit(){\n  wreckBalls=[];', 'function wreckInit(){\n  weaponFeedbackWarm("juggernaut");\n  wreckBalls=[];')
replace('  if(!wreckActive()){ if(wreckBalls.length) wreckBalls=[]; return; }',"  if(!wreckActive()||(player&&player.dead)){ if(wreckBalls.length) wreckBalls=[];weaponFeedbackOff('juggernautChains');return; }")
replace('  if(!wreckBalls.length) wreckInit();\n  for(const b of wreckBalls){',"  if(!wreckBalls.length) wreckInit();\n  weaponFeedbackLoop('juggernautChains',.24+.10*Math.abs(Math.sin(wreckBalls[0].a*2)));\n  for(const b of wreckBalls){\n    b._kick=Math.max(0,(b._kick||0)-dt);")
replace('          e.dead=true; b.hot=1;', '          e.dead=true; wreckStrike(b,e.x,e.y,false);')
replace('          hitEnemy(e,999); b.cd=WB_CD; b.hot=1;', '          hitEnemy(e,999); b.cd=WB_CD; wreckStrike(b,b.x,b.y,true);')
replace("          if(typeof explode==='function') explode(b.x,b.y,20,'red');",'          // The authored steel strike owns the contact flash.')
replace('      b.cd=WB_CD; b.hot=1;', '      b.cd=WB_CD; wreckStrike(b,b.x,b.y,true);')
replace("      if(typeof explode==='function') explode(b.x,b.y,18,'red');",'      // The authored steel strike owns the contact flash.')
replace("if(k==='juggernaut' && typeof wreckBalls!=='undefined') wreckBalls=[];", "if(k==='juggernaut' && typeof wreckBalls!=='undefined'){wreckBalls=[];weaponFeedbackOff('juggernautChains');weaponFeedbackOff('juggernautChargeLoop');}")
replace('function sonicGrant(){\n', 'function sonicGrant(){\n  weaponFeedbackWarm("cole");\n')
replace("run._sonicLoopName||'sonicChargeLoop'", "run._sonicLoopName||'colePressureLoop'",2)
replace('(S.sonicChargeStart||S.chargeStart)) (S.sonicChargeStart||S.chargeStart)();', "(S.sonicChargeStart||S.chargeStart)) weaponFeedbackSound('colePressureStart');")
replace('Snd.pools.sonicChargeLoop', 'Snd.pools.colePressureLoop')
replace("run._sonicLoopName='sonicChargeLoop';", "run._sonicLoopName='colePressureLoop';")
replace('run._sonicPing=true; if(Audio&&Audio.SFX&&Audio.SFX.select) Audio.SFX.select();',"run._sonicPing=true; weaponFeedbackSound('colePressureStart',.33);")
replace('dur:0.26+p*0.18, circ:true', 'dur:0.26+p*0.18, circ:true, p:p')
replace('    if(fn) fn();\n  }\n}\n/* ONE OWNER FOR THE SHOT',"    weaponFeedbackSound('colePressureRelease',.60+.40*p);\n  }\n}\n/* ONE OWNER FOR THE SHOT")
replace('      b.life=(b.life==null?SONIC_LIFE:b.life)-dt;', '      b.t=(b.t||0)+dt;\n      b.life=(b.life==null?SONIC_LIFE:b.life)-dt;')
replace('dur:SONIC_WAKE*0.6, circ:true', 'dur:SONIC_WAKE*0.6, circ:true, p:b._p')
replace('dur:SONIC_WAKE*(0.55+(b._p||0)*0.45)', 'dur:SONIC_WAKE*(0.55+(b._p||0)*0.45), p:b._p, w:sonicFrontGeometry(b).w')
fn('sonicDraw',(HERE/'sonic_draw.js').read_text())
p=s.index("    if(b.kind==='sonic'){",s.index('function draw'))
q=s.index("    if(b.kind==='mg'){",p)
s=s[:p]+"    if(b.kind==='sonic'){sonicDrawFront(b);continue;}\n"+s[q:]
replace('b._hit.push(e);\n            if(chance', "b._hit.push(e);\n            if(b.kind==='sonic')sonicImpact(b.x,e.y,b._p);\n            if(chance")
replace('function laserMistWarm(){\n', "function laserMistWarm(){\n  if(typeof Snd!=='undefined'&&Snd&&Snd.prepare)Snd.prepare(['laserMistFire','laserMistSplit','laserMistBloom','laserMistImpact']);\n")
replace("  b.dead=true;\n  if(Audio&&Audio.SFX&&Audio.SFX.laserMistSplit)Audio.SFX.laserMistSplit();", "  b.dead=true;laserMistFlash(b.x,b.y,b.lv,true);\n  const L=b._mistLedger||(b._mistLedger={hits:[]}),tag=finalSplit?'_bloomSound':'_splitSound';\n  if(!L[tag]){L[tag]=true;weaponFeedbackSound(finalSplit?'laserMistBloom':'laserMistSplit',.65+.07*b.lv);}")
replace('  player._mgMuzT=.09;player._mgMuzLv=Math.max(1,lv);shake=Math.max(shake,2.2);', '  for(let i=0;i<3;i++)laserMistFlash(player.x+(i-1)*42,player.y-18,lv,false);\n  shake=Math.max(shake,2.2);')
replace('function laserMistWarm(){',(HERE/'mist_draw.js').read_text()+'\nfunction laserMistWarm(){')
p=s.index("    if(b.kind==='lasermist'){",s.index('function draw'))
q=s.index("    if(b.kind==='spaceLaser'){",p)
s=s[:p]+"    if(b.kind==='lasermist'){laserMistDraw(b);continue;}\n"+s[q:]
replace('    for(const p of pImpacts){\n      if(p._lmFx)', '    for(const p of pImpacts){\n      if(weaponFeedbackDraw(p))continue;\n      if(p._lmFx)')
mapping={'colePressureStart':'cole_pressure_start','colePressureLoop':'cole_pressure_loop','colePressureRelease':'cole_pressure_release','colePressureImpact':'cole_pressure_impact','juggernautChargeStart':'juggernaut_charge_start','juggernautChargeLoop':'juggernaut_charge_loop','juggernautRamLaunch':'juggernaut_ram_launch','juggernautRamLoop':'juggernaut_ram_loop','juggernautRamStop':'juggernaut_ram_stop','juggernautChains':'juggernaut_chains','juggernautWreckHit':'juggernaut_wreck_hit','juggernautWreckBlock':'juggernaut_wreck_block','laserMistFire':'laser_mist_fire','laserMistSplit':'laser_mist_split','laserMistBloom':'laser_mist_bloom','laserMistImpact':'laser_mist_impact'}
rows='    /* 0913 authored weapon mixes: every cue owns a gain and retrigger gate below. */\n'+''.join("    %s:'assets/game/sounds/%s_0913.wav',\n"%(k,v)for k,v in mapping.items())
replace("    coleSonicBoom:'",rows+"    coleSonicBoom:'")
gates={'colePressureStart':(.66,.18),'colePressureLoop':(.58,0),'colePressureRelease':(.82,.12),'colePressureImpact':(.52,.11),'juggernautChargeStart':(.65,.18),'juggernautChargeLoop':(.55,0),'juggernautRamLaunch':(.85,.12),'juggernautRamLoop':(.62,0),'juggernautRamStop':(.72,.12),'juggernautChains':(.38,0),'juggernautWreckHit':(.78,.14),'juggernautWreckBlock':(.50,.09),'laserMistFire':(.72,.13),'laserMistSplit':(.56,.06),'laserMistBloom':(.62,.06),'laserMistImpact':(.60,.10)}
rows=''.join('    %s:{g:%s,lp:%d,min:%s},\n'%(k,g,6500 if k.startswith('laser')else 5200,m)for k,(g,m)in gates.items())
replace('    coleSonicBoom:       ',rows+'    coleSonicBoom:       ')
from refine import refine
s=refine(s)
if '--dry-run' in sys.argv:
    (ROOT/'_shots/weapon_feedback_0913/game.expected.js').write_bytes(s.encode('utf-8'));raise SystemExit('Wrote expected integration for comparison')
path.write_bytes(s.encode('utf-8'))
(HERE/'integration.json').write_text(json.dumps({'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'changes':changes},indent=2))
print('Integrated %d targeted replacements'%len(changes))
