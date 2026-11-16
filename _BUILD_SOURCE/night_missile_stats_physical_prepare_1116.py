from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_1116.py');s=p.read_text(encoding='utf8')
s=s.replace(' for guided in[False,True]:',' for mode in["baseline","current"]:\n  guided=False')
needle='  p.evaluate("()=>{BOFOnline'
replacement="  if mode=='baseline':p.evaluate('()=>{hitBoss=NMS16.base.boss;hitSubBoss=NMS16.base.mini;retinaMissileDamage=NMS16.base.retina;}')\n"+needle
assert needle in s;s=s.replace(needle,replacement)
s=s.replace("rows.append({'guided':guided,", "rows.append({'mode':mode,'guided':guided,")
s=s.replace("(('guided'if guided else'unguided')+'.png')", "(mode+'-physical.png')")
s=s.replace("O/'before.json'", "O/'physical-shipping.json'")
s=s.replace("Tests accounting, not campaign wins.", "Baseline restores only the three pre-accounting native routers; current uses the shipping accounting owner. Tests accounting, not campaign wins.")
s+="\nassert not errors and len(rows)==2 and all(r['setup']['hp']-r['hp']==34 for r in rows)and rows[0]['stats']['mslHits']==0 and rows[1]['stats']['mslHits']==1\n"
(p.parent/'night_missile_stats_physical_1116.py').write_text(s,encoding='utf8',newline='\n')
