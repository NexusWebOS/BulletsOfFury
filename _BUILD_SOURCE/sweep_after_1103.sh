#!/usr/bin/env bash
# One process per case with a hard timeout, so a stalled browser costs one case, not a worker.
#   bash _BUILD_SOURCE/sweep_waves_1103.sh "1 2 3" "normal hard furious" "novice" logname
cd "$(dirname "$0")/.."
for st in $1; do for diff in $2; do for bot in $3; do
  f="_shots/waves_1103/after/${st}-${diff}-${bot}.json"
  [ -f "$f" ] && continue
  for attempt in 1 2; do
    timeout 1500 python -u _BUILD_SOURCE/measure_waves_1103.py --tag after --cap 1000 --stages "$st" --diffs "$diff" --bots "$bot" >> "_shots/waves_1103/$4.log" 2>&1
    [ -f "$f" ] && break
    echo "STALL-RETRY $st $diff $bot attempt $attempt" >> "_shots/waves_1103/$4.log"
  done
done; done; done
echo "WORKER-DONE $4" >> "_shots/waves_1103/$4.log"
