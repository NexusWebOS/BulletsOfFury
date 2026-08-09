# TO-DO: Emotion Portraits (waiting on Mike's re-upload)

## What's needed
Dedicated emotion portrait sheets for the pilots that DON'T have them yet:
- **Maverick, Decker, Freezer** — confirmed WRONG/missing (currently head-crops of full-body card art)
- **Axel, Cole** — also only have card composites, no real portraits
- Emotions to cover: **sad / anger / happy / laugh / crash** (+ victory) per character, including Cole

## What already exists (the target quality/format)
- `assets/ui/portraits/jugg_{sad,crash,victory}.png` — framed bust portraits w/ expression + name banner
- `assets/ui/portraits/yuri_{sad,crash,victory}.png` — same format
These are the standard. New sheets should match this framed-portrait style.

## When Mike sends them, ask/confirm:
1. Layout: one pilot per row, emotions across columns? Get exact grid (rows x cols) + column order of emotions.
2. Combined sheet vs per-pilot files?
3. Are they pre-framed (like jugg/yuri) or raw busts needing the frame?

## Wiring plan once received
- Slice each cell, box on atlas, key as `port_<pilot>_<emotion>` (match existing jugg/yuri naming; jugg uses 'jugg' not 'juggernaut').
- Add to manifest BOFX img map.
- Extend `rivalPortrait(kind)` + dialogue calls so comm windows pick the right emotion per beat.
- Replace the face_* head-crops for maverick/decker/freezer/axel/cole in dialogue boxes with proper portraits.
- Strip any baked emote/"emoji" elements from portrait cells if present.
