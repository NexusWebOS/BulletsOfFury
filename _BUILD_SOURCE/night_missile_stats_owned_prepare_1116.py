from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_final_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("targets.find(t=>t._retinaOwner===b)||targets.find(t=>t===b)||targets[0]||b", "targets.find(t=>t._retinaOwner===b||t._spaceBossOwner===b||t._spaceSubOwner===b||t._xenoOwner===b)||targets.find(t=>t===b)||b")
s=s.replace("const first={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits}", "const first={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits,observerCredits:NMS16.credited}")
s=s.replace("const second={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits}", "const second={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits,observerCredits:NMS16.credited}")
s=s.replace("const sameProjectile=second.hits===first.hits", "const sameProjectile=second.observerCredits===first.observerCredits")
(p.parent/'night_missile_stats_owned_1116.py').write_text(s,encoding='utf8',newline='\n')
