/* xart_usage_log.js — record every art key the game ACTUALLY requests during play.

   WHY THIS EXISTS
   Static analysis cannot tell you what this codebase uses. Keys are assembled at runtime:
   'card_'+P.key builds ten pilot cards, 'ncm_font_'+n builds ninety-four, art:'mbv_f1' sits in
   a table and becomes mbv_f1_idle_0 three functions away. Grepping for literals missed the Vile
   Existence boss entirely (126 keys of shipped art), then scard_/card_ (18), then dlg_* (9);
   a looser matcher then swung the other way and called 100% of ice/laser/chain/shield live.
   Four wrong answers in one session. The tool is not the problem — the approach is.

   This records the truth instead. Every XART.get / XART.rdy call is counted, so after a
   playthrough you have the exact set of keys the game touched, with hit counts.

   HOW TO USE
     1. paste this file's contents into gamecode.js just after the XART block, or append it to
        assets/game.js for a one-off run (it patches XART in place, so either works)
     2. rebuild if you edited gamecode.js
     3. play — ideally every stage, both a win and a death, the map, stage select, the pause
        and options screens, and each pilot, so the per-pilot art gets touched
     4. in the browser console:   copy(XART_LOG.dump())
     5. save the clipboard as _BUILD_SOURCE/xart_used.json
     6. python3 organize_fx_0730e.py plan     -> every -d is now evidence, not a guess

   XART_LOG.report()   prints a summary to the console
   XART_LOG.misses()   keys that were REQUESTED but never resolved -- broken lookups worth seeing
   XART_LOG.reset()    start a fresh recording

   Cost is one Map increment per lookup. Leave it out of the jam build.
*/
(function(){
  if (typeof XART === 'undefined' || XART.__logged) return;

  var hits   = new Map();   // key -> times resolved
  var misses = new Map();   // key -> times requested but not ready

  var _get = XART.get, _rdy = XART.rdy;

  XART.get = function(k){
    var im = _get.apply(XART, arguments);
    if (im) hits.set(k, (hits.get(k) || 0) + 1);
    else    misses.set(k, (misses.get(k) || 0) + 1);
    return im;
  };
  XART.rdy = function(k){
    var ok = _rdy.apply(XART, arguments);
    if (ok) hits.set(k, (hits.get(k) || 0) + 1);
    else    misses.set(k, (misses.get(k) || 0) + 1);
    return ok;
  };
  XART.__logged = true;

  window.XART_LOG = {
    /* the file organize_fx_0730e.py reads: a flat array of keys that resolved at least once */
    dump: function(){
      return JSON.stringify(Array.from(hits.keys()).sort(), null, 1);
    },
    /* same thing with counts, if you want to see what is hot */
    dumpCounts: function(){
      var o = {};
      Array.from(hits.keys()).sort().forEach(function(k){ o[k] = hits.get(k); });
      return JSON.stringify(o, null, 1);
    },
    misses: function(){
      return Array.from(misses.keys()).sort().filter(function(k){ return !hits.has(k); });
    },
    report: function(){
      var m = this.misses();
      console.log('  resolved : ' + hits.size);
      console.log('  requested but NEVER resolved : ' + m.length);
      if (m.length) {
        console.log('  (these are broken lookups — the game asked for art that is not there)');
        console.log('  ' + m.slice(0, 40).join(', ') + (m.length > 40 ? ' ...' : ''));
      }
      console.log('run copy(XART_LOG.dump()) and save as _BUILD_SOURCE/xart_used.json');
      return hits.size;
    },
    reset: function(){ hits.clear(); misses.clear(); }
  };

  console.log('[XART_LOG] recording. play, then: copy(XART_LOG.dump())');
})();
