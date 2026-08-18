/* WHICH GLOBALS ARE REAL? (drop 0814a)
   ---------------------------------------------------------------------------
   `spawnEnemy`'s unclosed `if(base.art===undefined){` swallows everything below it, so a
   `function` written at column 0 after that point is FUNCTION-SCOPED and invisible to the rest
   of the file. CLAUDE.md says to bound it by the next top-level function; both brace-matching
   and line-bounding are recorded as giving wrong answers.

   So ask the engine instead of the source. This reuses test_fl.js's own vm bootstrap verbatim
   (everything up to its bridge line), then reports `typeof <name>` at global scope for each name
   passed on the command line. A name that comes back "undefined" is inside the swallow.

       node _BUILD_SOURCE/probe_scope_0814a.js flameIsIce orbIsFire tsFx explode
*/
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(__dirname, 'test_fl.js'), 'utf8');

/* cut the harness at the point where game.js is loaded and the bridge is installed —
   everything above that is pure setup and is what we want */
const CUT = "const G = sandbox.window.__B;";
const i = src.indexOf(CUT);
if (i < 0) { console.error('probe_scope: test_fl.js bootstrap marker moved; update CUT'); process.exit(2); }
const prefix = src.slice(0, i);

const names = process.argv.slice(2);
if (!names.length) { console.error('usage: probe_scope_0814a.js <globalName> ...'); process.exit(2); }

const tail = `
;const __out = {};
for (const n of __NAMES) {
  try { __out[n] = vm.runInContext('typeof ' + n, ctxv); }
  catch (e) { __out[n] = 'THREW: ' + e.message; }
}
return __out;
`;

const fn = new Function('require', '__dirname', '__filename', '__NAMES', prefix + tail);
let out;
try {
  out = fn(require, __dirname, path.join(__dirname, 'test_fl.js'), names);
} catch (e) {
  console.error('probe_scope: bootstrap failed —', e.message);
  process.exit(1);
}

let bad = 0;
for (const n of names) {
  const t = out[n];
  const global = (t === 'function' || t === 'object' || t === 'number' || t === 'string' || t === 'boolean');
  if (!global) bad++;
  console.log((global ? '  GLOBAL  ' : '  SWALLOWED  ') + n + '  (typeof ' + t + ')');
}
console.log(bad ? bad + ' of ' + names.length + ' are NOT visible at global scope' : 'all ' + names.length + ' visible at global scope');
process.exit(bad ? 1 : 0);
