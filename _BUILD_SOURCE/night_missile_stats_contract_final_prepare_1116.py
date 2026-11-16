from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_contract_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("targets[0];if(!target)return{missing:true,kind:b?.kind};", "targets[0]||b;if(!target)return{missing:true};const noRetina=targets.indexOf(target)<0;")
s=s.replace("const returns=[];returns.push(retinaMissileDamage(target,24,shot));", "const returns=[];function damage(n,projectile=shot){if(!noRetina)return retinaMissileDamage(target,n,projectile);const qb=_dmgBullet,qs=_dmgSrc;_dmgBullet=projectile;_dmgSrc='missile';try{return b===boss?hitBoss(n):hitSubBoss(n,target.x,target.y);}finally{_dmgBullet=qb;_dmgSrc=qs;}}returns.push(damage(24));")
s=s.replace("returns.push(retinaMissileDamage(target,10,shot))", "returns.push(damage(10))")
s=s.replace("appliedDamageGetsCredit:!valid||first.hits>before.hits", "appliedDamageGetsCredit:valid?first.hits===before.hits+1:first.hits===before.hits")
s=s.replace("return{before,first,second,kind:b.kind", "return{before,first,second,noRetina,kind:b.kind")
s=s.replace("O/'contracts.json'", "O/'contracts-final.json'")
(p.parent/'night_missile_stats_contract_final_1116.py').write_text(s,encoding='utf8',newline='\n')
