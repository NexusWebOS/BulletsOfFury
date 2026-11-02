# October31 weapon contact decals

Mike requested distinct contact FX for machine guns, laser cannons, lasers,
orbs, Maverick's Helix ball and Helix lasers. Ordinary hits now select authored
weapon-specific reels instead of small generic explosions. Genuine enemy/part
destruction, missiles, grenade blasts, Helix flurries/whiteout, orb AoE/shards,
elemental riders, shield absorption and native hit flashes retain their owners.

## Ownership and art

- `assets/weapon_contacts_1031.js` owns contact selection, short attached residue,
  nested-router deduplication, simulation expiry and bounded rendering. The
  launched projectile supplies identity, level and element, including co-op.
- Machine guns/heavy slugs use the authored chaingun metal contact and Decker
  scorch pixels. Laser cannons preserve their five native tier palettes. Lasers
  get matching energy contacts plus scorch; orb elements get their authored
  splash and cooling energy residue. Helix half contacts stay green, the full
  ball purple/blue, and released Maverick lances follow their real color tier.
- `assets/game.js` only changes the explicit contact decoration branches and
  shard/Helix decorative burst fallback. `assets/orbs_1010.js` replaces its
  decorative generic explosion; native AoE, shards, riders and dedicated energy
  rings remain. No weapon stats or homing-laser upgrades changed.
- `_BUILD_SOURCE/build_weapon_contacts_1031.py` owns the standalone sheets,
  manifest and `assets/weapon_contacts_art_1031.js`.34 banks/212 frames, all96x96,
  centre48, one proportional source scale per bank, even grid. Original atlases
  are unchanged. Sources:0928 weapon animation reels, Laser Mist impact/decal,
  space laser tier impacts and Decker scorch cells. Palette changes preserve
  neutral ink/highlights and alpha. Scorch expiry is baked into frames.
- No CSS/canvas rotation, per-frame fitting or runtime alpha fade for these
  new reels. Short marks follow the actual hull or persistent Retina component;
  killed/removed/untargetable targets stop drawing them. Three live marks per
  target, 180 shared impact entries, short per-family retrigger gates.
- Existing shared hit/cannon/orb/Helix audio remains native. No new cue routes.

## Verification

`_BUILD_SOURCE/probe_weapon_contacts_1031.py` uses real Edge Chromium, shoot.py
manual RAF and actual native collision/damage/rendering. Its pinned high-HP
diagnostic fixtures are not balance or survival runs. Final results are in
`_shots/weapon_contacts_1031/checks.json` and `probe.log`:

-32 focused checks cover MG/spread/heavy slug/lightning, held laser, cannon,
  mist, Maverick lance/Helix, all ten orb elements, damage parity, actual native
  white damaged pixels and recovery, moving hull marks, expiry, untargetable
  units, native energy shields, budgets and lethal native explosions.
- Actual live Stage1 miniboss component receives exactly one contact through
  nested space/Retina/hit routers; residue moves with its real socket.
- Native screenshots and the full new reel sheet were inspected. Page and
  console errors:zero. The authored hull's idle animation continues, so pixel
  expiry checks measure white damaged pixels rather than demanding frozen art.
- `node --check` passes for game.js, the new module and orbs_1010.js;
  whitespace checks pass with CRLF awareness. game.js remains LF; test_fl.js
  remains its original CRLF.
- Required `node _BUILD_SOURCE/test_fl.js` exits1 **before assertions/final
  summary**, because this machine lacks
  `UNUSED_ASSETS/retired_art_1022/manifest.json`. This is not a passing full suite
  and cannot be compared with the historical five-assertion baseline here.

## Review

`_BUILD_SOURCE/preview_weapon_contacts_1031.py` exports a14.4s silent visual
comparison using direct native damage calls, native updateEffects/drawWorld
and ctx.drawImage. Six closeups use actual rendered pixels, not an HTML sprite
mockup. Native travel/collision is independently covered by the probe.

Current local preview:
`http://127.0.0.1:8805/current/weapon-contacts-1031.html`

Media: `_shots/weapon_contacts_1031/contacts-closeups-1031.mp4`, closeup0â€“5 JPGs
and closeups-report.json. The initial27s real-RAF fixture picked up unrelated
campaign waves, so it is retained only as QA scratch and is not presented as a
fight or final visual proof. Its shared mixer capture decoded successfully
(-29.0dB mean/-10.5dB peak); no tap/page/console errors. No new sounds generated.

Preview player: nine checks pass, including all six actual seek/play chapters,14.4s decoded H264 at1280x800, and no page/console errors.

Prior review films remain intact. No commit, push or GitHub publication.
