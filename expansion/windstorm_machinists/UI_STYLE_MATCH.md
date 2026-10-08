# Niel / Windstorm: current-game UI match

The user identified that the first Windstorm assets did not follow the current pilot UI family. Revision 2 corrects the selected portrait, special icon and pickup box while retaining Niel's approved character identity, haircut, beard, scarf, armor and spiral insignia.

The references were taken from the 6 October portable build under `output/bof-portable-1006/Two ZIP Launch Test/BulletsOfFury`: current Cole, Axel and Maverick idle portraits, special icons from `bof_player_weapon_special_icons.webp`, and vented special boxes from `ui_hud.webp`. Local reference crops are retained in `reference/ui_match_v2/`.

| Selected export | Contract | Correction |
| --- | --- | --- |
| `identity/niel_portrait_v2.png` | 256×256 | Existing authored portrait-frame template, mint/sea-green accent, dark cockpit background, portrait crop matched to current pilots |
| `identity/niel_avatar_v2.png` | 256×256 | Same canonical frame and face for pilot selection |
| `identity/niel_smile_v2.png` | 256×256 | Approved smile artwork fitted to the same exact frame |
| `identity/niel_combat_v2.png` | 256×256 | Approved combat artwork fitted to the same exact frame |
| `ui/spicon_niel_v2.png` | 112×112 RGBA | Point-up gunmetal hex badge with corner bolts and a wind funnel; replaces the square badge |
| `ui/special_niel_box_v2.png` | 360×400 RGBA | Four bolted corner caps, ribbed side columns, top/bottom vents and a rectangular inset screen; replaces the round white/gold housing |

The portrait uses the actual `avatar_frame_template_0919.png` with the canonical existing-pilot placement: a 202×212 inner image at `(27,27)`. The original builder's paint-only HSV selection is reused with hue `0.44`. It changes the frame accent color while preserving every frame alpha pixel, fastener, rail, corner and light position. The frame itself is authored game art, not a newly generated approximation. The portrait's outer panel follows the existing avatar builder's opaque dark background convention.

The two special-ability items are generated family matches using the actual game references. They are not claimed to be pixel-identical copies of another pilot's housing. Their native canvases match the established special asset sizes, and transparent margins are preserved. The icon retains green/white wind light; the box and portrait use Niel's darker sea-green paint.

`build-ui-style-match.cjs` runs from `build-assets.cjs` and redirects the existing manifest IDs to versioned files. Old PNGs and generation masters are retained. The review displays the corrected exports and a [comparison sheet](previews/ui_style_match_v2.png). Three new source images bring the preserved source count to 26; the number of selected manifest entries remains 510.

Generated with the **built-in image_gen tool**. Exact prompts, reference paths and output provenance are in [ui-style-match-generation.json](ui-style-match-generation.json). Sharp performs extraction, sizing and composition with the authored frame. `verification.json` records dimensions, transparency and the unchanged frame alpha mask. No gameplay or shipping atlas registration is changed.
