from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_contract_final_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("[(1,'mini'),(1,'boss'),(4,'boss'),(5,'boss'),(6,'boss'),(7,'boss'),(9,'boss')]","[(1,'mini')]")
needle='return{before,first,second,noRetina,kind:b.kind'
extra="""const terminalBefore={hp:target.hp,hits:stageStats.mslHits};useBomb(target);const finish=pBullets.findLast(q=>hammerMissile(q));finish.x=target.x;finish.y=target.y;retinaMissileDamage(target,target.hp+100,finish);const terminalAfter={hp:target.hp,dead:target.dead,hits:stageStats.mslHits};retinaMissileDamage(target,10,finish);const terminal={before:terminalBefore,after:terminalAfter,lastHits:stageStats.mslHits,checks:{destroyed:target.dead||target.hp<=0,creditedOnce:terminalAfter.hits===terminalBefore.hits+1,noDeadCredit:stageStats.mslHits===terminalAfter.hits}};
  return{before,first,second,noRetina,terminal,kind:b.kind"""
assert needle in s;s=s.replace(needle,extra).replace("O/'contracts-final.json'","O/'terminal.json'")
s=s.replace('len(rows)==7','len(rows)==1').replace("all(q['checks'].values())for q in rows)","all(q['checks'].values())and all(q['terminal']['checks'].values())for q in rows)")
(p.parent/'night_missile_stats_terminal_1116.py').write_text(s,encoding='utf8',newline='\n')
