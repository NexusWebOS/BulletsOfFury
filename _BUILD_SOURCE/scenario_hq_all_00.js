(() => {
  run.mode = 'campaign';
  hqSeen = {};
  hqPlay('HQ_ALL_00');
  hqChars = (hqSc && hqSc.lines[0] && hqSc.lines[0][2].length) || 0;
})();
