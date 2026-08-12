/* scenario_propseek.js — jump the scroll to a fixed world prop so it can be looked at.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 4 \
 *           --script _BUILD_SOURCE/scenario_propseek.js --seconds 3 --fps 2 --warm 260
 *
 * Fixed props sit at a map coordinate and the world scrolls past them, so reaching one means
 * playing the level to that point — minutes, and unreachable from a capture. This sets mapScroll
 * directly to just before the first prop so it comes down the screen while the shots are taken.
 *
 * Reads the placement from _levelCfg().props rather than hardcoding a number, so it follows the
 * prop wherever it is moved to and cannot quietly go stale.
 */
(() => {
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0; eBullets.length = 0;
  const cfg = (typeof _levelCfg === 'function') ? _levelCfg() : null;
  const props = (cfg && cfg.props) || [];
  if (props.length) {
    // land it just above the screen so it scrolls INTO view rather than starting mid-frame
    mapScroll = Math.max(0, props[0].y - VH * 0.9);
  }
})();
