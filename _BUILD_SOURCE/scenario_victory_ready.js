async () => {
  victoryEndingWarm();
  await new Promise(resolve => {
    const until = performance.now() + 30000;
    const poll = () => {
      if (victoryEndingReady() || performance.now() >= until) resolve();
      else setTimeout(poll, 50);
    };
    poll();
  });
  drawVictory._ready = false;
  drawVictory._t = 0;
  drawVictory._scroll = 0;
  drawVictory._sfx = {};
}
