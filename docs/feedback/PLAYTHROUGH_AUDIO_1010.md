# October 10 full-campaign audio direction

Source: `C:/Users/Mdogg/Videos/2026-10-10 12-28-50.mp4`, duration 44:32.48.
Full local speech recognition: 307 timestamped segments, including the closing
comments. Source hash and verbatim working transcript are retained under
`_shots/playthrough_audio_1010/`. Video samples at 0, 10, 20, 30 and 40 minutes
are black; this is audio evidence, not a visual gameplay review. Mike states
that this entire run is on Normal. Referenced unnamed units are inferred from
the campaign order and must be checked against encounter code; two ambiguous
groups have been raised with Mike while independent work continues.

## Requested work

| Time | Direction | Implementation status |
| --- | --- | --- |
| 1:24–2:11 | Regenerate full-width bottom HUD; move angled lives/missile tabs above, enlarge wells, put radar next to top score. | Implemented. Native housing checks at 480/820/1280/1920px; screenshot inspected. |
| 2:14–2:30 | Stop cycling the player's ordinary flight sprite; one steady frame is sufficient. | Implemented: original neutral pilot/Fury frame; authored maneuver poses remain. |
| 2:33–2:57, 4:44–4:52, 7:46–7:53 | Larger shieldless kamikaze fodder; readable Normal, fast circular dive patterns on Hard/Furious, easy to destroy. | Implemented: 48×52 shieldless fodder, 6 HP on Normal, warned dives; faster circular entry on Hard/Furious. |
| 3:03–3:20 | Audible incoming firewall; remove stuck Retina. | Implemented: firewall birth sound once; stale/dead Retina targets clear. |
| 3:37–4:31 | Stage 2 twin turrets: aggressive charged fire lasers; larger beams; magma balls emphasize damaged state. | Implemented. Native live laser release ≥32px; healthy laser-heavy book, damaged magma book confirmed. |
| 5:04–5:47 | Remove duplicate local boss HP rail; shield waits for full formation; improve chains, shield and Normal challenge. | Implemented: formation gate, one HP rail, 32-frame formation/loop/shatter and 16-frame real chains; native screenshots inspected. |
| 6:30–7:34 | Larger map ship, stronger hover levitation, prevent top menu covering islands, fix white artifacts, preload side menu. | Implemented: larger map ship/hover, preloading and menu focus. The reported white artifacts cannot be identified from black video. |
| 8:06–8:09 | Do not release three ice orbs at once. | Implemented; native repeated fire produces one committed Level V orb. |
| 8:32–8:48 | Suppress missile firing while any primary/special/space weapon is charging. | Implemented; native manual/automatic/space missile paths spend no ammo during a charge. |
| 8:55–9:06 | Ice bosses resist ice sufficiently; avoid instant boss kills on all difficulties. | Implemented: 80% same-element absorption on all four difficulties; suite and native checks pass. |
| 10:15–10:20 | Generate a genuine ice laser. | Generated 16 frames and wired at the actual Cryospear hardpoints; native beam/muzzle screenshot inspected. |
| 11:46–12:38 | Replace Stage 4 center cannon/giant beam with darkened, audible lightning charge, southbound fusion shot, mid-screen burst into approaching lightning balls; difficulty-scaled speed. | Implemented; native charge → south release → five Normal lightning balls at mid-screen. Hard/Furious increase speed and count. |
| 13:06–13:13 | Boss helpers must attack. | Implemented; independent helper cycle fired 30 shots from both actual barrels in the native fixture. |
| 14:01–14:12 | Decker owns the message; improve spaceship fusion animation. | Implemented: Decker message, 16-frame assembly and 16-frame fusion beam/release. Cole plate follows his aircraft size; other pilots retain their authored parts. |
| 14:25, 15:40 | Slower space scrolling. | Implemented: space cruise 360 instead of 1000. |
| 14:54–17:44 | Weak, stationary/ineffective enemies; improve attacks, smooth frames and modular miniboss. | Moving/firing frigate, gravity and station units verified. Existing space miniboss retains five targetable pieces and pursuit patterns. Exact unnamed units still need identification for a specific remake. |
| 18:07–18:54 | Space/portal excursion resumes at its prior level position without unrelated cinematic or repeated miniboss. | Fixed an undeclared-scroll abort; exact timer, future waves, miniboss completion and backdrop position resume. Suite passes. |
| 20:31–21:11 | Improve Hammer ending animation; Earth stays fixed as ship approaches; use existing space backdrop. | Implemented: fixed Earth size, existing space backdrop and current Furyship; prior Hammer 1010 death work retained. |
| 21:39–21:54, 23:03–23:28 | Chaingun/weapon attachment visible in menus and game; no firing lock once hostile missiles arrive. | Implemented; native loadout draws attached chainguns, and ending dialogue releases the fire latch. |
| 22:09–22:52 | Stage 5→6: land at HQ, base attack/radar panic, Cole orders two pilots to defend HQ while others scramble. | Generated four HQ plates and wired into the active cinematic director, including landing, attack, radar panic and scramble. |
| 23:00–24:58 | No unrelated Chromium flyover; use actual red/green palette-swapped blue stealth fighters; faster Normal aircraft, more waves/allies, remove satellite-looking aircraft. | Implemented: actual red/green/blue stealth art, south orientation, faster Normal aircraft and earlier four allies; native fixtures pass. |
| 25:39–27:35 | Preserve in-game scene during rebel dialogue, remove duplicated dialogue windows, lock player movement for the demonstration. | Implemented; native movement input is blocked while effect/dialogue clocks advance; one dialogue owner. |
| 27:42–28:09 | Cloak spiral ends when cloaked and has completion sound; improve Jace charge/ball agitation and Voss charge art. | Implemented: cloak completion sound/end, full 104px agitated Jace ball southbound at 690px/s, 16-frame Voss charge/snap and 1250px/s return. |
| 28:36–29:24 | Improve completion animation; no stretched artwork. | Native completion holds the original ship scale and flies straight north; panel aspect matches its authored plate. No new bespoke completion reel; the unseen effect still needs a visual reference. |
| 29:38–29:48 | Replace Stage 6 Prism rewards and weapon family with Wind. | Implemented: nine craftable Wind carriers with authored gust/tornado/impact effects and nine icons; existing Prism saves migrate without losing levels. |
| 30:04–30:25 | Map escape animation uses rotating Harrier, not blue elite jet. | Implemented: map escape uses whv_closed Harrier with actual rotation. |
| 30:27–31:28 | Stage X needs intro/title card/allied arrival, accurate Harrier HP, effective attacks. | Implemented; native protected five-ship arrival/title, Normal cannon volley, and full core HP gate pass. |
| 31:41–31:52 | Earn a meaningful completion reward for Stage X; Mike authorizes choosing the surprise. | Implemented: once-only Air Superiority reward gives one life, 12 missiles, super-missile progress and a forge credit. |
| 32:06–32:45 | Directional map navigation agrees with screen direction; no ring wrap to Stage 1 before Stage 8 is beaten. | Implemented; nearest physical direction, Stage 6↔X vertical link, and no 7/8→1 wrap until Stage 8 is cleared. |
| 32:50–33:04 | Decker finds alien signal and explains the sewer mission in a cinematic. | Implemented in the active director: Decker identifies the alien signal beneath the city and gives the sewer mission. |
| 33:21–33:30 | All MG/Gatling upgrades use only two bullet lanes. | Implemented; all MG/Gatling tiers cap at two physical lanes; max chaingun native check passes with preserved total damage. |
| 34:42–34:55 | Shield matches each ship; turret warnings originate from actual turrets. | Implemented: fitted personal shields; Harrier and core-helper FOV cues use their physical muzzle positions. |
| 35:05–36:08 | Portal takeover is safe and straight flight, no forced spin; startled pilot/team dialogue, smooth animated portal. | Implemented: protected straight portal flight, no forced spin, and 32-frame void opening/held/closing reels; original startled dialogue retained. |
| 36:08–36:33 | Spread fan behavior appears wrong. | Removed the shared homing override from spread pellets; fan angles remain authored. Exact visual complaint is unobservable from this recording. |
| 36:41–36:44 | Time-slow does not allow effective missile use. | Not reproduced: native Freezer time-slow launches and lands a guided missile, consumes one missile and remains at 0.5 time scale. |
| 36:54–40:17, 44:00–44:07 | Stage 8 fierce enemies; portal behind drone, Dracodia emerges and consumes it, shriek/raised arms, real swipes, better effects and repeated lock/fire behavior. | Implemented: more committed Stage 8 volleys, 16-frame drone consumption/arm raise and shriek, 32-frame void, shared real claw geometry, stronger phase 1/2 attack cadence; native live attacks pass. |
| 40:38–42:53 | Each defeated form visibly explodes; smooth poses/transition effects. | Defeated copied forms rupture before changing and retain zero HP. Unnamed pose/animation complaints at 41–42 minutes still need an identified form. |
| 43:16–43:44 | No final upgrade menu after already returning home; generate better multi-shot ending. | Implemented: four new return-home plates and final clear bypasses upgrades plus the redundant cinematic. Native final exit passes. |
| 44:14–44:32 | Normal must offer actual challenge; Furious remains hardest. | Actual Normal attack participation checked before HP tuning; Hard/Furious retain faster cadence. Controlled fixtures are not a human campaign balance verdict. |

Existing Hammer 1010, siege tanks and incoming GitHub 7539951 work are retained.
Completed implementation and native verification are recorded above. Remaining identification, visual-reference and human-balance work is explicit.

Full regression: 8,170 passing assertions / 0 failures / exit 0. Native gameplay checks: 52 passing / 0 failures, with no page, console or asset errors. Sources and hashes: `_ART_SOURCES/audio_1010/generation_manifest.json`. Durable evidence: `docs/qa/audio_playthrough_1010.json`. Preview: `docs/previews/audio_1010/index.html`.
