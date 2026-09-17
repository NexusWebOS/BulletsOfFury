# Bullets of Fury — social playbook

Everything needed to run the YouTube / X / Instagram presence, written 2026-09-16.
Copy is drafted to be pasted as-is. Art and clips are built from the shipped game, not mocked up.

---

## 0. The one thing I cannot do, and the 4 minutes it costs you

**I cannot create the YouTube account.** Signing up for an account means entering a password and
completing an identity/bot check on your behalf, and that is off-limits for me regardless of how
it's framed — it's your identity, your recovery options, and your liability if it's wrong. Same
answer for Instagram and for any new X account.

That is the *only* blocked item. Everything downstream of it is done and waiting:

**Your 4 minutes, once:**

1. youtube.com → your Google account → **Settings → Add or manage your channel(s) → Create a new
   channel** (a brand channel, not your personal one — a brand channel can be handed to a team
   later and doesn't put your real name on comments).
2. Name: `Bullets of Fury`   Handle: `@BulletsOfFury` (fallbacks in §2 if taken)
3. Customise channel → paste the description from §2, upload the art from §3.
4. Tell me it's live. From then on I can draft, build, render and hand you upload-ready packages
   indefinitely — I just can't be the one who clicks *Publish* without you saying so each time.

**X:** I can write every post and schedule the calendar. To actually post from your account I'd
drive your logged-in Chrome — and I'll show you each post and wait for a yes before it goes out.
Publishing is one-way; it gets cached and indexed even if you delete it. So: drafts by default,
posting on your explicit go-ahead.

---

## 1. Positioning — what this channel is

> A nine-stage vertical shmup in the Raiden II / Fire Shark line, hand-authored pixel art, nine
> playable pilots with genuinely different weapons, built by one person.

Three content pillars, in priority order:

| Pillar | What it is | Why it works |
|---|---|---|
| **Boss showcases** | One boss, one clip, 30–60s | Shmup audiences judge a game by its bosses. Highest share rate, lowest production cost — the clip *is* the video. |
| **Pilot / weapon spotlights** | One pilot, their kit, 45–90s | Answers "why would I replay this", which is the whole sell for an arcade game. |
| **Devlog** | 3–8 min, the interesting problem of the week | Builds the audience that actually wishlists. Slow burn, do not lead with it. |

**Do not lead the channel with a devlog.** A cold channel with no gameplay reads as vapourware.
Ship the trailer and three boss clips first, *then* start the devlog.

**Tone:** confident and specific, never hype-speak. "Nine bosses, none of them split into pieces —
each one is a single authored plate with damage states" beats "EPIC BOSS BATTLES". The audience for
this genre is small, knowledgeable and allergic to marketing voice.

---

## 2. Channel setup — paste these

**Name:** `Bullets of Fury`

**Handle:** `@BulletsOfFury` → if taken: `@BulletsOfFuryGame`, `@PlayBulletsOfFury`, `@ColeForge`

**Description (paste whole):**

```
Bullets of Fury is a nine-stage vertical shoot-em-up in the arcade tradition —
Raiden II, Fire Shark, Truxton — built from scratch with hand-authored pixel art.

Nine pilots, and the pilot is the weapon: Cole's sonic boom, Freezer's ice breath,
Juggernaut's wrecking balls, Lizzie's turret mount, Decker's shotgun. Nine stages
from jungle river to orbital void, seventeen bosses and minibosses, four difficulties,
local co-op, and an arcade mode with real credits.

In development. New footage every week.

Wishlist / Steam page: coming soon
Discord: [your invite]
```

**Channel keywords** (Settings → Channel → Basic info → Keywords):

```
shmup, shoot em up, bullet hell, vertical shmup, arcade shooter, indie game,
pixel art, raiden, fire shark, truxton, danmaku, retro arcade, indie dev,
bullets of fury, game development, boss fight
```

**Links to add** (Customise → Basic info → Links): Steam page, Discord, X, itch.io if you have one.
Put Discord first until the Steam page is live — it's the only place a lead can actually go today.

---

## 3. The art kit — built and on disk

All in `docs/marketing_0916/social/`, built by `_BUILD_SOURCE/social_kit_0916.py` from the shipped
wordmark (`assets/game/ui/logo_0916/bof_logo.png`) and the cover painting. Re-run the script any
time the logo changes and every plate rebuilds.

| File | Size | Where it goes |
|---|---|---|
| `avatar_d_stack.png` | 800×800 | **YouTube + X + Instagram avatar.** The recommended one. |
| `avatar_b_fury.png` | 800×800 | Alternate — FURY only, cleaner at tiny sizes |
| `avatar_c_full.png` | 800×800 | The untouched wordmark, if you want no re-layout at all |
| `youtube_banner.png` | 2560×1440 | YouTube channel banner |
| `x_header.png` | 1500×500 | X profile header |
| `ig_square.png` | 1080×1080 | Instagram feed |
| `ig_portrait.png` | 1080×1350 | Instagram feed (portrait, gets more screen) |
| `thumb_base_cover.png` | 1280×720 | Thumbnail bed for non-gameplay videos |

**On the avatar.** The wordmark is 2:1 and every avatar surface is a square cropped to a circle, so
dropping the logo in whole leaves dead air top and bottom and clips the chevron wings. `avatar_d`
cuts BULLETS / OF / FURY apart and restacks them square, with FURY at 92% width so both wings stay
inside the circle. Checked at 88 / 48 / 32 px — the size YouTube actually draws in a comment thread.

**On the banner.** 2560×1440 is the upload size but only the centre **1546×423** is safe on desktop
and **1235×338** on a phone. The wordmark and tagline both sit inside the phone box; the painting
fills the rest and is darkened outside the safe area so the logo always has contrast.

Tagline currently reads `NINE PILOTS.  NINE STAGES.  ONE SKY.` — one-line change in the script.

---

## 4. The clip library — captured from the real game

`_BUILD_SOURCE/capture_clip_0916.py` records real gameplay headlessly through the game's own
MediaRecorder clip recorder (the `R` key in debug mode). Output lands in
`docs/marketing_0916/clips/` as `.webm` masters plus `.mp4`.

```bash
python _BUILD_SOURCE/capture_clip_0916.py --list-fights
python _BUILD_SOURCE/capture_clip_0916.py --fight "DOOMSDAY CARRIER" --stage 6 --seconds 22
python _BUILD_SOURCE/capture_batch_0916.py bosses
```

Frame is **960×1152** — the full cabinet: HUD strip, EQUIPPED box and play field, the same
composite the in-game recorder makes, so a marketing frame and a QA frame are the same picture.

**Three things the tool measures and prints, because all three have burned this project before:**

- **Achieved fps.** It records in real time, so the clip is only as smooth as the headless browser.
  It prints frames-drawn ÷ wall-seconds and warns under 45. Current machine holds ~55.
- **Ship blits per frame.** Must be 1.00. Pinning `player.invuln` to keep the pilot alive *strobes
  the ship four frames on, four frames off* — the first capture came back with 556 shots fired,
  score 0→1590 and no aircraft in three of four sampled frames. The pilot is kept alive by stubbing
  `playerHit` instead.
- **Shots fired.** The harness does not simulate an input tap, so a clip left alone is the ship
  gliding through a battle without shooting. `pShoot()` is driven directly on the weapon's cooldown.

The recorder's own red `REC 00:00` badge is drawn *inside* the captured composite, so it is stubbed
out for the length of a marketing capture.

### Measured capture rate per encounter — read before planning a shot

Headless Chromium here has **no GPU**; this is software rasterisation, so these are a *floor*, not
what the game runs at on your machine. The spread is the useful part:

| Encounter | fps | usable |
|---|---:|---|
| Stage 3 ordinary play | 56.5 | yes |
| Stage 1 ordinary play | 55.4 | yes |
| Toxic Portal Warden (s7) | 50.2 | yes |
| Black Cocoon (s8) | 42.4 | acceptable |
| Doomsday Carrier Mk II (s6) | 41.8 | acceptable |
| Stage 6 ordinary play | 40.0 | acceptable |
| Storm Sovereign Mk II (s4) | 32.2 | visible stutter |
| Warp Sentinels (s9 boss) | 6.5 | unusable |
| **Stage 5 ordinary play** | **2.9** | **unusable** |
| **Stage 9 ordinary play** | **1.1** | **unusable — 18 frames in 16 s** |

### ⚠⚠ And then the pilot clips found the actual cause

Adding the weapon tier and the special to the autopilot — so the nine pilots would stop looking
like nine clips of the same gun — dropped most of them off a cliff. So I isolated it. **Same stage
(1), same pilot (maverick), same tier (5), 8 seconds each, only `run.weapon` different:**

| Weapon at tier 5, stage 1 | fps |
|---|---:|
| MACHINE GUN | **54.7** |
| ICE ORB | 30.7 |
| SPREAD FIRE | 8.9 |
| **LASER** | **1.5** |

**The laser costs about 36× the machine gun to draw, on identical content.** And it is the weapon,
not the stage and not the tier:

```
laser tier 3, stage 1 .... 2.5 fps
laser tier 5, stage 1 .... 1.5 fps
laser tier 5, stage 6 .... 1.5 fps     <- stage makes no difference at all
```

The **specials are cheap** — Juggernaut went from 7.7 fps to 50.9 purely by swapping spread for the
machine gun, with the wrecking balls still spinning.

CLAUDE.md already names this class *and* already contains the fix that worked once: the Magma
Ward's fireballs drew through `shadowBlur=10` under `'lighter'`, ~32 a frame, measured at **78 ms a
frame**, and baking the glow into a cached canvas gave the same pixels at **2.6 ms**. That note ends
"`drawBullets` still sets `shadowBlur` in 46 places — that is the next optimisation target." This is
that target, with a number on it.

**Caveat, stated plainly:** headless here has no GPU, and Canvas2D `shadowBlur` is the single op
software rasterisation punishes hardest. Your machine will not show 1.5 fps. But a 36× ratio between
two weapons in the same engine is not something a GPU makes go away — it makes it survivable on
*your* hardware and not on a Steam Deck. I've queued this as its own task rather than fixing it
here, since it's an engine job and you own that call.

**Three pilot clips are affected and need re-recording on your machine** — the rest captured clean:

| | fps | |
|---|---:|---|
| Juggernaut / Lizzie / Cole / Freezer | 51–54 | good |
| Decker | 35.9 | fine |
| Axel | 23.5 | usable |
| **Yuri** (lightning orb) | 15.3 | re-record |
| **Falva** (her special *is* laser balls) | 9.2 | re-record |
| **Maverick** (the widening laser is his identity — no substitute) | 2.3 | re-record |

To replace one: run the game, debug menu, pick the pilot and stage, press `R`, and drop the file in
`docs/marketing_0916/clips/` under the same name (`pilot_maverick.mp4`). `make_reel_0916.py pilots`
picks it up by filename with no other change.

### ⚠ The space-stage numbers, which may be the same cause

**Stage 5 and stage 9 — the two space stages — run 20 to 50 times slower than every other stage
in the game.** Not 20% slower. Stage 3 draws 904 frames in the same 16 seconds that stage 9 draws
18. Every other stage in the game, including three boss fights with a screen full of ordnance,
lands between 32 and 56.

Headless here has no GPU, and software rasterisation does punish things a GPU gives away free —
large composites, canvas filters, `shadowBlur`. So some gap is expected and **the absolute numbers
are not what your machine will do.** But a 50× gap against the rest of the same engine is too big
to attribute to that alone, and it is isolated to exactly the two stages that share the space
rendering path — the starfield, `l5FieldDraw`/`l5RocksDraw`, and the 0912v warp drive layer.

Given what the weapon test found above, my guess is these two are the same bug seen from a
different angle — the space stages draw a lot of glowing objects. But that is a guess and I have
not profiled either. Both are queued as one task.

For now: **capture stages 5 and 9 yourself.** Run the game, debug menu, pick the fight, press `R`.
On a GPU it will hold 60 and the clip drops straight into `docs/marketing_0916/clips/` naming.

⚠ **A trap worth keeping.** The first stage-9 capture reported `ship blits 0 over 144 frames` and
warned that the ship was missing. It wasn't — stage 9 flies the **Furyship**, which resolves
through `fury_` and the space atlas, not `ship_`. A counter keyed on one family read a clip with
the ship plainly in it as an empty one, which is the exact false negative the counter exists to
catch. Both families are counted now.

---

## 4b. What is already rendered and ready to upload

In `docs/marketing_0916/video/`:

| File | Length | Use |
|---|---:|---|
| `bosses_reel.mp4` | 1:51 | **Video 2 on the slate** — "Every Boss in Bullets of Fury". Eight bosses, name-carded, arcade-cabinet framing. |
| `pilots_reel.mp4` | 1:37 | **Video 3** — all nine pilots with their real affiliations. Three segments stutter; see above. |
| `minis_reel.mp4` | ~0:55 | Week-3 upload — the four minibosses. |
| `boss_s2_furnace_short.mp4` | 0:20 | **A Short / Reel / TikTok**, 1080×1920, ready as-is. |

Rebuild any of them after replacing a clip:

```bash
python _BUILD_SOURCE/make_reel_0916.py bosses
python _BUILD_SOURCE/make_short_0916.py boss_s7_warden --title "TOXIC PORTAL WARDEN" --seconds 25
```

They are rendered at CRF 17, so the files are large — that is deliberate, YouTube re-encodes and
you want to hand it the best master you have. Do not compress before uploading.

---

## 5. The video slate — first ten uploads

Order matters. 1–4 in the first week, then one a week.

### 1 · Announce trailer — `Bullets of Fury — Announcement Trailer`
60–75s. The existing trailer, or re-cut from the boss clips. Ends on the logo + "Wishlist soon".
**Pin it. Set it as the channel trailer for non-subscribers.**

> **Description**
> ```
> Nine pilots. Nine stages. Seventeen bosses. One sky.
>
> Bullets of Fury is a vertical shoot-em-up in the arcade tradition — hand-authored
> pixel art, four difficulties, local co-op, and an arcade mode with real credits.
> Built from scratch by one person.
>
> Wishlist: [Steam link]
> Discord: [invite]
>
> 0:00 Scramble
> 0:12 Stage 1 — Rumble in the Jungle
> 0:24 The bosses
> 0:48 Nine pilots
> 1:02 Coming soon
> ```
> **Tags:** `shmup, shoot em up, bullet hell, indie game trailer, pixel art game, vertical shmup, raiden, arcade shooter, indie dev, bullets of fury`

### 2 · `Every Boss in Bullets of Fury (So Far)`
2–3 min. All eight boss clips back to back, each with a name card. This is the single highest-value
video on the list — it's the one people link.
**Thumbnail:** Doomsday Carrier mid-attack + `17 BOSSES`.

### 3 · `Nine Pilots, Nine Completely Different Guns`
90s. All nine, each with their real affiliation card (read out of the game's own `AINTRO_AFFIL`
table, not invented):

| Pilot | Affiliation | The hook |
|---|---|---|
| COLE | FURY FOUNDER | Sonic boom, Aegis, MG tiers to 8 |
| AXEL | AIRFORCE | Five-orb Aegis aura |
| DECKER | ORDER OF THE MATRIX | The shotgun |
| FREEZER | AIRFORCE | Ice breath — a separate weapon, not a recoloured flamethrower |
| JUGGERNAUT | BROTHERHOOD OF FURY | Two counter-rotating wrecking balls, charge dash |
| YURI | INDEPENDENT | Lightning orb |
| LIZZIE | STRATEGIC ORDNANCE | Turret mount, and a hidden B-42 bomber skin |
| FALVA | PRINCESSES OF THE SKY | Anchored laser balls |
| MAVERICK | INDEPENDENT | The widening laser — the only pilot who keeps it |

### 4 · `The Stage 5 Transformation` (Short, vertical)
The plane flying into the cloud deck, the twelve kit pieces arriving, the Furyship assembling, the
white flash, then space. Under 60s. **This is the best Shorts candidate in the whole game** — it's
a visual payoff with no context required.

### 5 · `Stage 6: Doomsday Carrier Mk II — full fight`
Boss showcase format. No commentary, just the fight, text card at the top.

### 6 · `Jungle Overlord-X — Stage 1 Boss`
Same format. Earlier bosses are more approachable for a cold audience than late ones.

### 7 · Devlog #1 — `I built a shmup where every boss is one piece`
3–5 min. The no-boss-splits rule and why: one authored plate, damaged/critical as *states*, never
sections with their own hitboxes. Genuine craft content, and it's a real design position other
devs will argue with — which is engagement.

### 8 · Devlog #2 — `The bug that made my boss unwinnable`
The Stage 6 carrier's hit box being 640×320 on a 680-wide world, swallowing the one shot the fight
depends on. Compress the whole fight into a 50px band. This is a *great* story and it's true.

### 9 · `Furious difficulty vs the Razorback Siege Tank`
Hard fields two tanks; Furious fields one at 150% scale in crimson. Side-by-side.

### 10 · `Local Co-op` — two seats, one screen
Short, if co-op footage captures cleanly.

**Every description ends with the same block:**
```
Bullets of Fury — a nine-stage vertical shmup, in development.
Wishlist: [Steam]   Discord: [invite]   X: @BulletsOfFury
```

**Thumbnail rules** (`build_thumb_from_frame` in the kit script does all of this):
- Subject fills the frame. Pull the frame from the clip itself, don't use cover art for gameplay videos.
- Wordmark top-left at ~30% width, never centred — the centre is for the boss.
- Three to four words maximum, bottom, on a dark ramp so they survive YouTube's compression.
- Check it at 210px wide. If you can't read it there it doesn't exist.

---

## 6. X — 30 posts, ready to go

Cadence: **4–5 a week.** Two clips, one still, one dev note, one reply-bait. Never more than one
link post a week — X suppresses them.

Every clip post: **video first, text short, no link in the post.** Put the link in a reply.

### Launch week
1. `Bullets of Fury. Nine pilots, nine stages, seventeen bosses, one sky.` + trailer
2. `Stage 1 is called RUMBLE IN THE JUNGLE and it opens on open water, which is entirely on purpose.` + stage 1 clip
3. `Every boss in this game is ONE authored plate. No sections, no pieces falling off, no separate hitboxes. Damaged and critical are states, not debris.` + carrier clip
4. `Freezer is the only pilot who gets ice breath, and it's a completely different weapon from the flamethrower — not a recolour.` + clip
5. `Juggernaut gets two wrecking balls on chains, counter-rotating, and a charge dash. Not a stat line — a different aircraft to fly.` + wrecking balls clip

### Weeks 2–4 (pick and rotate)
6. `The Stage 5 transformation, uninterrupted.` + furyship clip
7. `Found a bug where the boss's hit box was 640px wide on a 680px screen. It ate every shot aimed at the thing you're supposed to deflect. The fight was mathematically unwinnable and it had shipped.`
8. `Warning colours are green → yellow → red and they mean the same thing on all nine stages. The alert has to contrast with the FIELD, not match the beam — an ice-blue warning on an ice stage is invisible.` + clip
9. `Cole's Aegis.` + clip
10. `Seventeen bosses and minibosses. Here's four of them.` + montage
11. `Lizzie has a bomber costume hidden behind a password and it had been chopped-up pieces of three other pilots' aircraft for a month. Fixed.`
12. `The Razorback Siege Tank. Hard gives you two. Furious gives you one at 150% and paints it red.` + clip
13. `Which one are you picking?` + nine-pilot lineup still
14. `Stage 7 is called NOT ANOTHER SEWER LEVEL and I regret nothing.` + clip
15. `Four difficulties. Furious is not a joke.` + clip
16. `Every enemy gets a shock ring, debris, a white flash and smoke. Tanks and jets also get a smoke ring. It's a rule, not a case-by-case thing.` + explosion clip
17. `Local co-op, one screen.` + clip
18. `The player death is a spin-out — 540 to 900 degrees with the fire and explosions ANCHORED to the ship as it turns, then a crash and a shock ring. Anchored is the load-bearing word.` + clip
19. `Nine stages. Jungle river to orbital void.` + stage montage
20. `The wordmark.` + logo still
21. `Missiles come in Standard, Super, Ultra and Uber. You earn the next tier by surviving a wave with the current one, and dying knocks you back to Standard.` + clip
22. `The retina lock: bosses paint a reticle on you before the homing missiles launch, and it STAYS locked until you barrel roll, somersault, dodge at the last second, or shoot the missiles down.` + clip
23. `Yuri's lightning orb.` + clip
24. `66 achievements, all of them earnable in a real run.` + gallery still
25. `Stage 4 is CROUCHING MISSILES, HIDDEN DEATH.` + clip
26. `Shipping a new boss this week. Guess which stage.` + cropped teaser
27. `Devlog 1 is up.` + link in reply
28. `Somebody asked why the bosses don't break apart. Because a boss that comes apart is four small enemies wearing a boss's name.`
29. `Steam page is live.` — hold until it is
30. `Wishlist if you want this to exist.` + best 15 seconds of footage

**Hashtags:** at most two, at the end. `#shmup #indiedev` on weekdays, `#screenshotsaturday` on
Saturdays (still the single best-performing indie game tag on X).

**Reply strategy is worth more than the posts.** Search `shmup` and `bullet hell` weekly and reply
with substance to three or four people. A small account grows from replies, not from broadcasts.

---

## 7. Instagram & TikTok

Same clips, reformatted. `ig_square.png` / `ig_portrait.png` are the profile-side plates.

Gameplay is **960×1152 (5:6)** — already nearly portrait, which is lucky. For 9:16 Reels/Shorts:

```bash
ffmpeg -i clip.mp4 -vf "scale=1080:-2,\
  split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40[bg];\
  [b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -crf 18 out_vertical.mp4
```

That blurs the clip's own frame as the backdrop rather than black bars — it reads far better on a
phone and keeps the palette.

**Post three a week**, clip only, caption under 100 characters. Instagram is a discovery surface,
not a community one; don't spend energy there beyond reposting.

---

## 8. The first fortnight, day by day

| Day | YouTube | X | IG |
|---|---|---|---|
| 1 | Trailer (pin, set as channel trailer) | Post 1 + trailer | Trailer |
| 2 | — | Post 2 | — |
| 3 | Every Boss So Far | Post 3 + clip | Boss clip |
| 5 | — | Post 4 | — |
| 6 | — | Post 5 | Pilot clip |
| 7 | Nine Pilots (Short) | #screenshotsaturday still | — |
| 9 | — | Post 6 | Transformation |
| 10 | Stage 5 Transformation (Short) | Post 7 | — |
| 12 | — | Post 8 + clip | Clip |
| 13 | Doomsday Carrier full fight | Post 10 | — |
| 14 | — | #screenshotsaturday | — |

Then steady state: **one YouTube a week, four X a week, three IG a week.** That is sustainable
alongside actually building the game, which matters more than any of this.

---

## 9. Where the leads actually go

Right now: Discord. That's it.

The moment the Steam page exists it becomes the call-to-action everywhere and Discord drops to
second. Until then, every video description and every pinned post should point at Discord, because
a channel with no destination converts nothing.

**Reddit** — you've posted. The ones that work for this game, in order: r/shmups (small, expert,
will actually play it), r/IndieGaming, r/IndieDev, r/pixelart (art posts only, no gameplay),
r/Games (only for the Steam launch, and only once). Post the *clip*, not the trailer, and never the
same clip in two subs in the same week.

---

## 9b. One risk worth five minutes of your time

The clips are silent — the in-game recorder is video-only — so every video needs a music bed, and
that bed goes through YouTube's Content ID on upload.

Two filenames in `assets/game/music/` are song titles by well-known bands:

- `boss4_cowboyfromhell.mp3`
- `boss3_lie_down_or_stay_down.wav` (in `newboss/`)

`docs/NEW_BOSS_MUSIC_0914.md` describes the three `newboss/` WAVs as **"original WAV files supplied
by Mike"**, so those are presumably yours and the title is a nod. `boss4_cowboyfromhell.mp3` has no
such note anywhere in the repo.

I can't identify a recording by listening, so I'm not asserting anything about what these are —
I'm flagging the filenames and asking. It matters twice over:

1. **A trailer** with a claimed track gets muted, region-blocked or monetised by someone else, and
   the strike lands on a channel that is one day old.
2. **The game itself** ships that file. A Content ID claim on a video is annoying; unlicensed music
   in a Steam release is a different category of problem entirely.

The reels currently use `boss1_minderaser.mp3` and `title_main_menu.mp3` as the bed — the two the
repo gives most reason to believe are yours. **If you confirm which tracks are original and
cleared, I'll set the bed per reel and stop hedging.** If any are not, that's a rename-and-replace
job in the game, not a marketing one, and better found now than after the Steam page is up.

---

## 10. Open, and what I need from you

- [ ] **YouTube channel created** — 4 minutes, §0. Nothing else in this document can start without it.
- [ ] Discord invite link (permanent, non-expiring) so I can put it in every description
- [ ] Steam page URL when it exists
- [ ] Pick an avatar: `avatar_d_stack` (recommended), `avatar_b_fury`, or `avatar_c_full`
- [ ] Say whether the tagline `NINE PILOTS. NINE STAGES. ONE SKY.` stays
- [ ] For X posting: confirm you want me driving your logged-in Chrome, and that you want to see
      each post before it goes out
- [ ] **Confirm the music licensing question in §9b** — which tracks are original and cleared
- [ ] Capture the stage 9 Warp Sentinels fight yourself (`R` in debug mode) — it runs at 6.5 fps
      headless here and is the only encounter I can't produce a usable clip of

**Once the channel exists** I can hand you upload-ready packages — video file, thumbnail, title,
description, tags, end screen — as a folder per video. You upload; I don't publish for you.
