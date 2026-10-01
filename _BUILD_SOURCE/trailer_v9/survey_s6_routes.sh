#!/bin/sh
# Survey both stage-6 routes (left = HARRIER / warhive, right = REBEL FURY) on the trailer harness, frames not saved.
cd "$(dirname "$0")"
P="({t:+stageTimer.toFixed(1),op:(typeof s6Opening!=='undefined'&&s6Opening)?s6Opening.phase:null,sh:s6Wing?s6Wing.ships.length:0,ph:s6Wing?s6Wing.ships.map(q=>q.phase[0]).join(''):'',beats:s6Wing&&s6Wing.beats,all:s6Wing&&s6Wing.all,fake:!!(s6Wing&&s6Wing.fake),ch:s6Wing&&s6Wing.choice,rt:s6Wing&&s6Wing.route,sb:subBossActive?subBoss.kind:null,sbd:subBossDone,bo:bossActive&&boss?(boss.kind+':'+Math.round(boss.hp)+'/'+Math.round(boss.maxhp)):null,bd:bossDefeated,e:enemies.length,eb:eBullets.length,st:state})"
for R in left right; do
  if [ "$R" = left ]; then KEY=arrowleft; else KEY=arrowright; fi
  nohup python3 -u survey9.py --stage 6 --pilot cole --frames 16000 --every 120 --out survey/s6_$R --probe "$P" \
    --when "subBossActive&&subBoss&&!subBoss.dead:window.__sbAt=window.__i" \
    --when "window.__sbAt&&window.__i-window.__sbAt>600:window.__kill()" \
    --when "s6Wing&&s6Wing.choice&&!s6Wing.route:window.__mode='none';Input.injectTap('$KEY')" \
    --when "s6Wing&&s6Wing.choice&&!s6Wing.route&&s6Wing.frChoice&&s6Wing.frChoice.t>0.5:Input.injectTap('enter')" \
    --when "s6Wing&&s6Wing.route:window.__mode='boss'" \
    --shot 9000 --shot 10000 --shot 11000 --shot 12000 --shot 13000 --shot 14000 > survey_s6_$R.log 2>&1 &
done
