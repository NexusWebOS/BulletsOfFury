# FURY HQ — Earth Division campaign cinematics

This pack establishes the official Earth Division branding, exterior geography, lounge relationships, restricted Cole/Decker technology, and one campaign-introduction plate for every pilot.

## Deliverables

- Three unified official branding assets: a transparent master insignia/wordmark, horizontal headquarters sign and vertical hangar standard
- Three native-size **1672 × 941** exterior plates with fully generated, architecturally integrated **FURY HQ — EARTH DIVISION** insignia signage
- Nine reusable native-resolution seated RGBA pilot cutouts
- Seven baked lounge/alliance story frames
- Nine baked individual pilot campaign introductions
- Five production ending assets: restored-dawn HQ, damaged satellite dish, tar-black RGBA ooze survivor, reference-locked RGBA BOF2 shadow mech and a dedicated black deep-space starfield
- Contact sheets and edge-QA previews
- Reproducible built-in ImageGen prompt specifications in `GENERATION_PROMPTS.md`

## Canon relationships

- **Cole** is the Earth Division leader and commanding officer. His likeness is distinct from his calm, management-driven command personality.
- **Decker** is the systems, engineering and code specialist. He secretly developed prototype lasers and a photon cannon that only Cole is authorized to access.
- **Axel** and **Freezer** joined from Air Force recruitment together. Axel became air commander; Freezer remains his right-hand man and trusted wingman.
- **Falva** and **Lizzie** are sisters known as the **Princesses of the Sky**. Lizzie is the eldest and naturally takes the protective lead.
- **Yuri** and **Maverick** arrived separately as lone wolves: Maverick as a mercenary, Yuri as a young lost cadet seeking answers. Mutual skepticism develops into camaraderie.
- **Juggernaut** gets along with everyone. He is enormous, loud, funny and serves as the social heart of the crew.

## Scene routing

- `cutscenes/lounge_and_alliances/` contains the brotherhood, sisters, lone wolves, Juggernaut social scenes, complete team lounge shot and classified Cole/Decker laboratory reveal.
- `cutscenes/pilots/` contains one clean 16:9 introduction frame for every character with role and campaign hook.
- `branding_generated_official/` contains the approved master insignia plus matching horizontal and vertical generated standards.
- `exteriors_generated_official/` contains the active island aerial, beach approach and concealed jungle gate. Every plate carries the same generated Earth Division identity as a physical part of the headquarters architecture.
- `branding/` and `exteriors/` contain the retired first-pass flat-panel treatment and are retained only as legacy source material.
- `seated_poses/` contains the reusable identity-locked cutouts used for the lounge scenes.
- `ending_generated/` contains the active victory-cinematic plates and transparent sequel-stinger creatures. The active V2 survivor is a black ooze-virus fragment with a dim green core; the V2 sequel silhouette preserves the round spiked hull, green slit-eye, two articulated arms and three-prong claws of the supplied model. The enemy approach uses the dedicated black starfield rather than the generic blue space/sky gradient. Runtime keys are code-owned in `assets/game.js` as `cinend_*`.
- The selected pilot now departs FURY HQ with their existing native `04_rear_left_3q` or `05_rear_right_3q` sprite. The ship holds in rear view, climbs, banks and shrinks into the distance; no top-down gameplay frame is used for this fly-off.

## Production notes

Built-in ImageGen reference mode created the official master identity, horizontal sign, vertical standard and all three replacement exterior signs. The words **FURY HQ** and **EARTH DIVISION** are part of the generated illustrated metalwork itself: embossed, engraved, lit, weathered and mounted with the crest. No system font or deterministic text layer is used in the active official branding.

The established six-pose character masters remain the sole identity/costume references for the seated poses. Character matte extraction, staging, titles and final character/background composites use the deterministic Pillow pipeline.

Generated checker/black mattes were removed from the seated cutouts with connected-border extraction. The supplied standing poses remain unchanged. Baked cutscenes are RGB master plates; reusable crest, wordmark and seated-pose files retain real RGBA transparency.
