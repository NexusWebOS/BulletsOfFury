from pathlib import Path
W=Path(__file__).resolve().parent;B=W.parent
p=B/'verify_front_stage5.py';s=p.read_text()
insert='''
  activation=p.evaluate("""()=>{seed119('normal','regular');const hp=B.hp,armor=fr27BeginArmor(B);for(let i=0;i<1000&&B._hammer.state==='fr_activation';i++)fr27ActivationTick(B,1/60);const q=ha21Blue(B);return {activated:!!fr27Armor(B)?.activated,armorHP:fr27Armor(B)?.hp,state:B._hammer.state,bank:q?.a.bank,key:q?.a.key,hpSame:B.hp===hp,whole:q?.a.wholeGenerated};}""")
  ck('Native Chromium activation returns to new held-hammer form',activation['activated'] and activation['armorHP']>0 and activation['state']=='hammer' and activation['bank']=='blue-overhead' and '_chrome_'in activation['key'] and activation['hpSame'] and activation['whole'],activation)
  shot(p,'stage5-chromium-native-ready')
  p.evaluate("hammerState(B,'recover');B._hammer.t=0;B._hammer._hj22Pair=null;B._hammer.c27Combo=null;B._hammer._hf22StormPair=null")
  shot(p,'stage5-chromium-front-contact')
  matrices=p.evaluate("""()=>{let out=[];for(const mat of ['regular','chrome','red']){seed119('normal',mat);for(const s of ['warn','leap','recover','giant_idle','giant_windup','giant_rise','giant_warn','giant_dive','giant_sweep','storm_warn','storm_slam','storm_split']){hammerState(B,s);B._hammer.t=s==='warn'?.5:s==='recover'?0:.2;const q=ha21Blue(B);out.push({mat,state:s,bank:q?.a.bank,key:q?.a.key,front:!!q?.a.faceForward,whole:!!q?.a.wholeGenerated});}}seed119('normal','regular');return out;}""")
  ck('Every normal/Chromium/red held strike and depth windup selects frontal art',all(q['bank']=='blue-overhead'and q['front']and q['whole']and ('_'+q['mat']+'_')in q['key']for q in matrices),matrices)
'''
needle='  counts=p.evaluate';assert needle in s;s=s.replace(needle,insert+needle);p.write_text(s)
p=B/'verify_front_stage8.py';s=p.read_text()
insert='''
  activation=p.evaluate("""()=>{Q.rf1110=null;Q.rage=Q.chrome=false;Q.action=null;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;Q.cool=999;B._r30.mode='fight';B._r30.v18.donorAge=0;B._noHit=B.dead=B.enter=false;B.hp=B.maxhp;const hp=B.hp;hb20Start(B,'armor');const A=Q.action;for(let i=0;i<900&&Q.action===A;i++)v19NativeTick(B,1/60);Q.action=null;Q.cool=999;const q=hb20Pose(B);return {chrome:Q.chrome,bank:q?.a.bank,whole:q?.a.wholeGenerated,hpSame:B.hp===hp};}""")
  ck('Copied native Chromium activation returns to frontal held-hammer form',activation['chrome']and activation['bank']=='ba119_corrupt-overhead_chrome'and activation['whole']and activation['hpSame'],activation)
  shot(p,'stage8-chromium-native-ready')
  p.evaluate("()=>{Q.action=null;hb20Start(B,'skystrike');Q.action.t=Q.action.tell+1;ba119Root(B,Q.action);}")
  shot(p,'stage8-chromium-front-contact')
  matrices=p.evaluate("""()=>{let out=[];for(const mat of ['regular','chrome','red']){Q.rf1110=null;Q.rage=mat==='red';Q.chrome=mat!=='regular';Q.action=null;Q.cool=999;for(const type of ['skystrike','side']){hb20Start(B,type);for(const age of [0,.8,1.1,2.1]){Q.action.t=Q.action.tell+age;const q=hb20Pose(B);out.push({mat,type,bank:q?.a.bank,front:!!q?.a.faceForward,whole:!!q?.a.wholeGenerated});}}}Q.rage=Q.chrome=false;Q.action=null;return out;}""")
  ck('Copied normal/Chromium/red down and side attacks select frontal whole poses',all(q['front']and q['whole']and q['bank'].endswith('_'+q['mat'])and q['bank'].startswith('ba119_corrupt-')for q in matrices),matrices)
'''
assert needle in s;s=s.replace(needle,insert+needle);p.write_text(s)
print('Added actual Chromium activation, material coverage and extended held-attack routing checks.')
