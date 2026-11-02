"""Explicit migrations to shared HP/cadence helpers; preserve file newlines."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def edits(path,pairs):
 p=R/path;b=p.read_bytes();s=b.decode('utf-8')
 for old,new in pairs:
  if new in s:continue
  assert old in s,(path,old);s=s.replace(old,new)
 p.write_bytes(s.encode('utf-8'))
edits('assets/stage8_amplify_1101.js',[('D.hp*[1,1.30,1.62][s811Rank()]','difficultyHealthBaseline15(D.hp,D.hp*[1,1.30,1.62][s811Rank()])')])
edits('assets/stage9_amplify_1101.js',[('D.hp*[1,1.24,1.5][s911Rank()]','difficultyHealthBaseline15(D.hp,D.hp*[1,1.24,1.5][s911Rank()])')])
edits('assets/highway_armor_1017.js',[
 ('(24+rank*6)*mul','difficultyHealthBaseline15(30,24+rank*6)*mul'),('(18+rank*5)*mul','difficultyHealthBaseline15(23,18+rank*5)*mul'),('(12+rank*3)*mul','difficultyHealthBaseline15(15,12+rank*3)*mul'),('-dt*1.8,dt*1.8','-dt*turretSpeed15(1.8),dt*turretSpeed15(1.8)')])
edits('assets/stage6_roster_1017.js',[('[1000,1350,1650,1950,2100][target17Rank()]','difficultyHealthBaseline15(1350,[1000,1350,1650,1950,2100][target17Rank()])')])
edits('assets/stage7_modular_0927.js',[('DIFF.eHp*(!tank&&n===2?1.12:1)','DIFF.eHp*(DR15.keys.includes(diffKey)?1:(!tank&&n===2?1.12:1))')])
edits('assets/stage1_followup_1031.js',[
 ('-dt*2.8,dt*2.8','-dt*turretSpeed15(2.8),dt*turretSpeed15(2.8)'),('T.timer=.11','T.timer=turretInterval15(.11)'),('(rocket?3:1.75)/[1,1.15,1.35][s1bRank()]','turretInterval15(rocket?3:1.75)')])
edits('assets/stage3_amplify_1031.js',[
 ('-1.4*dt,1.4*dt','-turretSpeed15(1.4)*dt,turretSpeed15(1.4)*dt'),("(T.weapon==='sonic'?3.0:2.1)/[1,1.25,1.55][v31Rank()]","turretInterval15(T.weapon==='sonic'?3.0:2.1)")])
edits('assets/stage2_amplify_1031.js',[('-dt*2.3,dt*2.3','-dt*turretSpeed15(2.3),dt*turretSpeed15(2.3)')])
edits('assets/game.js',[
 ('T.angle+=clamp(delta,-dt*2.8,dt*2.8);','T.angle+=clamp(delta,-dt*turretSpeed15(2.8),dt*turretSpeed15(2.8));'),
 ("const gap=w==='mg'?.11:w==='missile'?.20:.20;","const gap=turretInterval15(w==='mg'?.11:w==='missile'?.20:.20);"),
 ("T.timer=(w==='mg'?2.0:w==='missile'?3.2:w==='sonic'?3.6:2.8)/\n      (diffKey==='furious'?1.25:diffKey==='hard'?1.1:1);","T.timer=turretInterval15(w==='mg'?2.0:w==='missile'?3.2:w==='sonic'?3.6:2.8);"),
 ('-CAN_TRACK*dt, CAN_TRACK*dt','-turretSpeed15(CAN_TRACK)*dt, turretSpeed15(CAN_TRACK)*dt')])
print('Migrated explicit difficulty health and turret owners')

edits('assets/game.js',[('span=camRightX()-L,single=b.maxhp,actors=[]','span=camRightX()-L,single=b.maxhp/2,actors=[]')])
edits('assets/combat_polish_0927b.js',[
 ("const hp=diffKey==='easy'?600:[1050,1250,1450][n];","const hp=difficultyHealthBaseline15(1050,diffKey==='easy'?600:[1050,1250,1450][n]);"),
 ("diffKey==='easy'?140:250+n*40","difficultyHealthBaseline15(250,diffKey==='easy'?140:250+n*40)")])
edits('assets/stage6_roster_1017.js',[
 ('140+rank*22','difficultyHealthBaseline15(162,140+rank*22)'),
 ('105+rank*20','difficultyHealthBaseline15(125,105+rank*20)'),
 ('125+rank*20','difficultyHealthBaseline15(145,125+rank*20)')])
edits('assets/sumpjaw_duo_1031.js',[('Math.ceil(1560*DIFF.eHp*1.10)','difficultyHealthBaseline15(2190,Math.ceil(1560*DIFF.eHp*1.10))')])
edits('assets/stage2_amplify_1031.js',[
 ("A.cd=T.weapon==='laser'?[.22,.13,.065][r]:T.weapon==='mg'?.12:.22;","A.cd=turretInterval15(T.weapon==='laser'?.22:T.weapon==='mg'?.12:.22,T.weapon==='laser'?[.22,.13,.065][r]:T.weapon==='mg'?.12:.22);")])
edits('assets/stage7_amplify_1101.js',[('-dt*1.6,dt*1.6','-dt*turretSpeed15(1.6),dt*turretSpeed15(1.6)')])
edits('assets/stage9_amplify_1101.js',[
 ('A.beat=orbs?.42:[.21,.18,.15][r]','A.beat=turretInterval15(orbs?.42:.21,orbs?.42:[.21,.18,.15][r])')])
edits('assets/cloud_carrier_1101.js',[
 ('e._sc12Fire+[.72,.64,.58][v31Rank()]','e._sc12Fire+turretInterval15(.72,[.72,.64,.58][v31Rank()])'),
 ('e._sc12Ready=CC111.clock+2.0','e._sc12Ready=CC111.clock+turretInterval15(2.0)')])
edits('assets/stage1_followup_1031.js',[
 ("A.cd=corvette?.17:.11","A.cd=turretInterval15(corvette?.17:.11)"),
 ("A.cd=corvette?[1.8,1.5,1.2][rank]:.72","A.cd=turretInterval15(corvette?1.8:.72,corvette?[1.8,1.5,1.2][rank]:.72)")])
edits('assets/modular_roster_0927.js',[
 ("const mul=diffKey==='easy'?.52:diffKey==='normal'?1:diffKey==='hard'?1.18:diffKey==='furious'?1.35:1.5;","const mul=DR15.keys.includes(diffKey)?difficultyEnhancement15():diffKey==='easy'?.52:1.5;")])
edits('assets/stage8_amplify_1101.js',[
 ('A.beat=/orb/.test(kind)?[.38,.32,.27][r]:[.20,.17,.14][r]','A.beat=turretInterval15(/orb/.test(kind)?.38:.20,/orb/.test(kind)?[.38,.32,.27][r]:[.20,.17,.14][r])')])
edits('assets/stage7_amplify_1101.js',[
 ('A.cadence=Math.max([.12,.10,.085][r],[.26,.23,.20][r]-A.t*.055)','A.cadence=turretInterval15(Math.max(.12,.26-A.t*.055),Math.max([.12,.10,.085][r],[.26,.23,.20][r]-A.t*.055))'),
 ("A.beat=K==='crescent'?.30:A.cadence","A.beat=K==='crescent'?turretInterval15(.30):A.cadence"),
 ('A.beat=.12','A.beat=turretInterval15(.12)')])
edits('assets/highway_armor_1017.js',[
 ('p.shot=.23','p.shot=turretInterval15(.23)'),
 ('p.cool=turret?[2.2,1.8,1.4,1.1,.95][rank]:[4,3.4,2.8,2.3,2.1][rank]','p.cool=turretInterval15(turret?1.8:3.4,turret?[2.2,1.8,1.4,1.1,.95][rank]:[4,3.4,2.8,2.3,2.1][rank])')])
edits('assets/stage6_roster_1017.js',[
 ('gap:[.18,.16,.125,.10][rank]','gap:turretInterval15(.16,[.18,.16,.125,.10][rank])'),
 ('rest:[2.4,2.1,1.8,1.6][rank]','rest:turretInterval15(2.1,[2.4,2.1,1.8,1.6][rank])'),
 ('p.shot=.16','p.shot=turretInterval15(.16)'),
 ("p.cool=Math.max(.85,2.5-rank*.35)+(p.kind==='laser'?.4:0)","p.cool=turretInterval15(2.15+(p.kind==='laser'?.4:0),Math.max(.85,2.5-rank*.35)+(p.kind==='laser'?.4:0))")])
edits('assets/missile_truck_1018.js',[
 ('Math.max(8,hp*.75)','Math.max(difficultyHealthBaseline15(8,8),hp*.75)'),
 ('Math.max(4*coop,hp*.30)','Math.max(difficultyHealthBaseline15(4*coop,4*coop),hp*.30)')])
edits('assets/stage5_amplify_1101.js',[('const mul=[1,1.65,2.15][ai27Level()]','const mul=DR15.keys.includes(diffKey)?1:[1,1.65,2.15][ai27Level()]')])
edits('assets/game.js',[("const mult=diffKey==='easy'?.5:diffKey==='hard'?1.22:diffKey==='furious'?1.48:1;","const mult=DR15.keys.includes(diffKey)?1:diffKey==='easy'?.5:1;")])
edits('assets/finale_forms_1008.js',[("(ff8Diff()===3?.45:ff8Diff()===2?.40:.35)","(DR15.keys.includes(diffKey)?.35:ff8Diff()===3?.45:ff8Diff()===2?.40:.35)")])
edits('assets/game.js',[("t.fireShot+=D.straightBeat||(phase>=3?.028:.034)","t.fireShot+=turretInterval15(phase>=3?.028:.034,D.straightBeat||(phase>=3?.028:.034))")])
edits('assets/game.js',[("p=stage4CoreTurretTarget(b,side),hp=170+S.coreGeneration*20,shield=","p=stage4CoreTurretTarget(b,side),hp=difficultyHealthBaseline15(170+S.coreGeneration*20,170+S.coreGeneration*20),shield=")])
# Numeric cadence arrays only: never migrate warm/tell/len/fuse/count/speed.
for name in ['stage1_amplify_1031','stage1_followup_1031','stage2_amplify_1031','stage3_amplify_1031','stage4_amplify_1101','stage5_amplify_1101','stage6_airframe_1101','stage7_amplify_1101','stage8_amplify_1101','stage9_amplify_1101']:
 p=R/'assets'/(name+'.js');s=p.read_bytes().decode('utf-8')
 pat=r'(\b\w+\.(?:cd|beat|cool|fireCd)\s*=)\[([.\d]+),([.\d]+),([.\d]+)\]\[([\w()]+)\]'
 s,n=re.subn(pat,lambda m:m[1]+'turretInterval15('+m[2]+',['+','.join(m.group(i)for i in[2,3,4])+']['+m[5]+'])',s)
 if n:p.write_bytes(s.encode('utf-8'));print(name,'cadence owners',n)
