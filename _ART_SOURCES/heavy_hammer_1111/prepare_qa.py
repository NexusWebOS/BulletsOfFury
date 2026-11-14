from pathlib import Path
W=Path(__file__).resolve().parent;B=W.parent
for stage in [5,8]:
 s=(B/f'verify_caps_stage{stage}.py').read_text().replace('outputs/End-cap-strikes','outputs/Heavy-hammer-motion').replace('from record_loaded import record_loaded','from heavy_record_loaded import record_loaded')
 s=s.replace("q['unique']>=12","q['unique']>=24")
 insert='''
  counts=p.evaluate("""()=>Object.fromEntries(Object.entries(BA119_ART).filter(([n])=>/^(blue|corrupt)-(overhead|sides|right|whirl)$/.test(n)).map(([n,a])=>[n,a.count]))""")
  ck('Real 32-frame overhead banks registered',counts['blue-overhead']==32 and counts['corrupt-overhead']==32,counts)
'''
 if stage==5:
  insert+='''  spin=p.evaluate("""()=>{seed119('normal','regular');hammerWhirlStart(B);const h=B._hammer;let seen=new Set(),keys=new Set();for(let i=0;i<150;i++){updateBoss(1/60);const q=ha21Blue(B);if(q?.a.bank==='blue-whirl'){seen.add(q.a.frame);keys.add(q.a.key);}}return {frames:[...seen],keys:keys.size,whole:ha21Blue(B)?.a.wholeGenerated};}""")
  ck('Native whirlwind uses all 16 complete body turn drawings',len(spin['frames'])==16 and spin['keys']==16,spin)
  p.evaluate("seed119('normal','regular');hammerWhirlStart(B);hammerState(B,'whirlwind');B._hammer.c26SpinClock=B._hammer.ha1111SpinStart+4")
  shot(p,'stage5-native-whirl-back')
'''
 else:
  insert+='''  spin=p.evaluate("""()=>{Q.rf1110=null;Q.rage=Q.chrome=false;Q.action=null;Q.cool=999;B._r30.mode='fight';B._r30.v18.donorAge=0;B.x=worldWidth()/2;B.y=viewTopY()+200;hb20Start(B,'spin');const A=Q.action;let seen=new Set();for(let i=0;i<250&&Q.action===A;i++){v19NativeTick(B,1/60);const q=hb20Pose(B);if(q?.a.bank==='ba119_corrupt-whirl_regular')seen.add(q.a.frame);}return {frames:[...seen]};}""")
  ck('Copied native whirlwind uses all 16 complete body turn drawings',len(spin['frames'])==16,spin)
  p.evaluate("()=>{Q.action=null;hb20Start(B,'spin');Q.action.t=Q.action.tell+.2266;}")
  shot(p,'stage8-native-whirl-back')
'''
 s=s.replace('  from heavy_record_loaded import record_loaded',insert+'  from heavy_record_loaded import record_loaded')
 (B/f'verify_heavy_stage{stage}.py').write_text(s)
s=(B/'record_loaded.py').read_text().replace('outputs/End-cap-strikes','outputs/Heavy-hammer-motion').replace('square end-cap strikes','reference-led heavy hammer motion')
needle=" chapters.append(dict(name='released throw',at=round(time.monotonic()-start,3)))"
add=''' chapters.append(dict(name='whirlwind',at=round(time.monotonic()-start,3)))
 if stage==5:p.evaluate("()=>{seed119('normal','regular');hammerWhirlStart(B);}")
 else:p.evaluate("()=>{B._r30.mode='fight';B._r30.v18.donorAge=0;Q.rf1110=null;Q.rage=Q.chrome=false;Q.action=null;Q.cool=999;Q.speech=null;B.x=worldWidth()/2;B.y=viewTopY()+200;hb20Start(B,'spin');}")
 p.wait_for_timeout(6500)
'''
s=s.replace(needle,add+needle)
s=s.replace("[('hammer',chapters[0]['at'],chapters[1]['at'])]","[('hammer',chapters[0]['at'],chapters[1]['at']),('whirlwind',chapters[2]['at'],chapters[3]['at'])]")
(B/'heavy_record_loaded.py').write_text(s)
print('Prepared native checks and live recordings for both forms including whirlwind.')
