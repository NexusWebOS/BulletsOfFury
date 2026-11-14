from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');B=W/'before';B.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/boss_animation_1109.js','assets/whole_hammer_1110.js','assets/overhead_slam_art_1111.js']
hashes={n:sha(R/n)for n in protected}
for n in protected:
 p=B/Path(n).name
 if not p.exists():p.write_bytes((R/n).read_bytes())
s=(R/'assets/boss_animation_1109.js').read_text()
patches=[('hitKey:\'nca_ba119_\'+name+\'_hit\',frames:16,cols:4','hitKey:\'nca_ba119_\'+name+\'_hit\',frames:a.count,cols:4'),
 ('f=clamp(Math.floor(f),0,a.count-1);const key=','f=clamp(Math.floor(f*(a.count/16)),0,a.count-1);const key='),
 ('function ba119Frame(list,u){return list[Math.min(list.length-1,Math.floor(clamp(u,0,.999999)*list.length))];}',
  'function ba119Frame(list,u){const v=clamp(u,0,.999999)*list.length,i=Math.floor(v),a=list[i],b=list[i+1]??a+1,d=(b-a+16)%16;return (a+(v-i)*(d<=2?d:0))%16;}'),
 ("function ba119Corrupt(Q,f,bank='corrupt-overhead'){return BA119.base.sample('ba119_'+bank+'_'+rd74Mat(Q),f);}","function ba119Corrupt(Q,f,bank='corrupt-overhead'){return BA119.base.sample('ba119_'+bank+'_'+rd74Mat(Q),f*(BA119_ART[bank].count/16));}")]
for a,b in patches:assert s.count(a)==1,a;s=s.replace(a,b)
(W/'boss_animation_1109.js').write_text(s)
s=(R/'assets/whole_hammer_1110.js').read_text();assert 'const HA1111='not in s
(W/'whole_hammer_1110.js').write_text(s+(W/'runtime-whirl.js').read_text())
# The addon keeps pre-existing fold/roll/empty/other boss banks from its original
# provider. Only the requested eight attack/whirl banks are overridden.
(W/'installation-plan.json').write_text(json.dumps({'before':hashes,'changes':['8 whole-character motion banks','32 overhead drawings per form','15 unique side drawings plus contact hold and whole-pose right mirrors','16 wholebody turn drawings per form','native frame-index sampling and whirlwind selection'],'coreUnchanged':'assets/game.js'},indent=2))
print('Prepared narrowly scoped runtime changes; original sources backed up.')
