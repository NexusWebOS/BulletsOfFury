# Five HUD concepts — October 11, 2026

Mike requested concepts first: make lives and missile stocks easy to read below
the score, enlarge the lower cockpit while keeping the bars and text, and remove
the radar. These are review assets; no shipping HUD or game behavior was changed.

The five concepts are:

1. **Fury Classic** — orange-lit steel, closest to the current cockpit.
2. **Bold Cabinet** — red fascia, strong resource hierarchy, right-side maneuvers.
3. **White Interceptor** — white alloy and cyan rails, long special meter.
4. **Armored Command** — olive/brass wings, centered weapon icon.
5. **Neon Fury** — black chrome and cyan circuitry, horizontal meters.

Open `docs/previews/hud_concepts_1011/index.html` through the local game server.
The review uses actual Stage1/Stage6 captures and exports of the native icons,
Command Alloy bitmap lettering and existing authored meter pixels. Controls
switch concepts, backgrounds and stock states, enlarge the preview and export
a full mockup. The lower strip is wider and larger; the playfield remains clear.

Five independent calls used the built-in `image_gen` tool with the current
`assets/game/shared/ui/audio_hud_1010.png` as a style reference. Exact prompts,
original generated file paths and design directions are in `prompts.json`.
The five PNGs here are the unchanged generated originals, all1536x1024.
`registration.json` records SHA256, two even crops per plate and55 measured
even display windows. Rendering uses one uniform scale for each banner;
original icon proportions and ordnance colors are retained. No atlas was edited.

The registration builder is `_BUILD_SOURCE/build_hud_concepts_1011.py`.
Native reference exporter: `_BUILD_SOURCE/export_hud_concept_refs_1011.py`.
Preview verification: `_BUILD_SOURCE/probe_hud_concepts_1011.py`.
QA: `docs/qa/hud_concepts_1011.json`.

The first screenshot review caught special-title/timer overlap and crowded
extra maneuver percentages. The final revision separates the special text,
puts compact status into the bar where needed and keeps maneuver labels clear.
Browser verification covers all five selectors, low/empty stock states,
real PNG export, enlargement,360/480px layout, reduced motion and asset errors.
The concepts use sample values and still gameplay captures, not live encounters.
Mike's choice and live integration are the next steps. No commit/push requested.
