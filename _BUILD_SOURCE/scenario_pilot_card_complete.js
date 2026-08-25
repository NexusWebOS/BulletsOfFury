(() => {
  const key = (run && run.pilot) || 'axel';
  const index = PILOTS.findIndex(pilot => pilot.key === key);
  if (index >= 0) {
    pilotIndex = index;
    pilotFrom = index;
    pilotRot = 0;
  }
  if (key === 'cole') coleUnlocked = true;
  drawPilot._pcFor = key;
  pcStart(key);
  pcSkip();
})();
