from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_edges_1116.py');s=p.read_text(encoding='utf8')
old="q.update({'stage':stage,'role':role});rows.append(q);"
new="""q.update({'stage':stage,'role':role})
  if stage==6:
   found=False
   for j in range(150):
    if p.evaluate('pBullets.some(q=>q.ally&&hammerMissile(q))'):found=True;break
    e=p.evaluate(shoot.STEP,6);assert not e;p.wait_for_timeout(1)
   if found:
    edge=p.evaluate('''()=>{const shot=pBullets.find(q=>q.ally&&hammerMissile(q)),t=_lockTargets().find(t=>!t.dead&&t.hp>0),before=NMS16.credited;if(!shot||!t)return{unavailable:true};const hp=t.hp;retinaMissileDamage(t,2,shot);return{allyNoExtraCredit:NMS16.credited===before,allyApplied:hp>t.hp,key:shot._wingKey};}''');q['edge'].update({k:v for k,v in edge.items()if k=='allyNoExtraCredit'});q['allyEvidence']=edge
   else:q['allyEvidence']={'unavailable':True,'nativeWaitSeconds':15}
  rows.append(q);"""
assert old in s;s=s.replace(old,new)
(p.parent/'night_missile_stats_final_1116.py').write_text(s,encoding='utf8',newline='\n')
