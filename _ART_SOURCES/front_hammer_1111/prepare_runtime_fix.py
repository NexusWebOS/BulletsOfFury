from pathlib import Path
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
s=(W/'whole_hammer_1110.js').read_text().split('// FH1111')[0];(W/'whole_hammer_1110.js').write_text(s+(W/'runtime-front.js').read_text())
s=(R/'assets/boss_animation_1109.js').read_text();old="function ba119Corrupt(Q,f,bank='corrupt-overhead'){return BA119.base.sample('ba119_'+bank+'_'+rd74Mat(Q),f*(BA119_ART[bank].count/16));}"
new="function ba119Corrupt(Q,f,bank='corrupt-overhead'){const name='ba119_'+bank+'_'+rd74Mat(Q),count=RD74_ART.banks[name]?.frames||16;return BA119.base.sample(name,f*(count/16));}"
assert s.count(old)==1;s=s.replace(old,new);(W/'boss_animation_1109.js').write_text(s)
p=W.parent/'verify_front_stage8.py';s=p.read_text();needle='  counts=p.evaluate'
extra='''  ball=p.evaluate("""()=>{let out=[];for(const mat of ['regular','chrome','red']){Q.rf1110=null;Q.rage=mat==='red';Q.chrome=mat!=='regular';Q.action=null;Q.cool=999;hb20Start(B,'ball');const A=Q.action;for(const t of [A.approach+.5,A.tell+.2,A.tell+A.rollTime+A.settle+.4]){A.t=t;const q=hb20Pose(B),a=RD74_ART.banks[q.a.bank];out.push({mat,bank:q.a.bank,frame:q.a.frame,valid:!!a&&q.a.frame>=0&&q.a.frame<a.frames});}}Q.action=null;Q.rage=Q.chrome=false;return out;}""")
  ck('Copied fold/roll/unfold preserve separately registered frames in all materials',all(r['valid']for r in ball),ball)
'''
assert needle in s;s=s.replace(needle,extra+needle);p.write_text(s)
print('Prepared native registry fallback and password intro/dance ownership repair.')
