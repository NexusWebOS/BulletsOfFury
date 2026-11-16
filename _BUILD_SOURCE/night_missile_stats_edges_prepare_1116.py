from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_contract_final_1116.py');s=p.read_text(encoding='utf8')
needle="return{before,first,second,noRetina,kind:b.kind"
extra="""const edge={};if(run.stage===9&&run.spaceMode){spaceVolleyLaunchRack(1);const volley=pBullets.findLast(q=>q.kind==='spaceVolley'),n=stageStats.mslHits,c=NMS16.credited;retinaMissileDamage(target,2,volley);edge.spaceVolleyNoExtraCredit=stageStats.mslHits===n&&NMS16.credited===c;}if(run.stage===6){const rocket=pBullets.find(q=>q.ally&&hammerMissile(q));if(rocket){const n=NMS16.credited;retinaMissileDamage(target,2,rocket);edge.allyNoExtraCredit=NMS16.credited===n;}}
  return{before,first,second,noRetina,edge,kind:b.kind"""
assert needle in s;s=s.replace(needle,extra)
s=s.replace("O/'contracts-final.json'", "O/'contracts-shipping.json'")
s=s.replace("all(q['checks'].values())for q in rows)", "all(q['checks'].values())and all(q.get('edge',{}).values())for q in rows)")
(p.parent/'night_missile_stats_edges_1116.py').write_text(s,encoding='utf8',newline='\n')
