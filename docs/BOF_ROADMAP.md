
## DROP 0724dr — THE ROOT CAUSE WAS MY OWN ASSET SWEEP, TEN DROPS AGO

Build: 1788 assertions, 0 errors.

**"The HTMLImageElement provided is in the 'broken' state"** — climbing past 10,000 at the title.
A BROKEN image is one whose src 404'd: complete === true, naturalWidth === 0. It is TRUTHY, so every
`if(img)` guard in the codebase waves it through and drawImage throws. The loop catches it, THE FRAME
SILENTLY STOPS, and handleTitleInput is the last statement in drawTitle. Menu animates, never
responds. That is the entire bug, and it has been there since drop 0724ce.

**WHY THE FILES WERE MISSING — AND IT WAS ME.** My drop-0724ce cleanup built its keep-set from
BOFX.img and BOFA and NEVER READ THE BOF NAMESPACE. So it moved 50 files to _unused/ that only BOF
references, including:
    BOF.atlas     assets/atlases/main.png     the sprite atlas every ASSETS.blit needs
    BOF.menu      assets/ui/menu.jpg          the TITLE background
    BOF.menuLogo  assets/ui/menuLogo.png
    BOF.banner    assets/ui/banner.png
    BOF.boot      assets/boot/boot.jpg
I deleted the title screen's own artwork and then spent ten drops looking for a logic bug. All 50
restored, and there is now an assertion that walks EVERY namespace — BOF included — and fails if any
referenced path is missing from disk.

**AND A SAFETY NET SO THIS CLASS CANNOT RECUR.** ctx.drawImage is wrapped once, at creation: a null,
an unloaded image, a broken image or anything else the method rejects is SKIPPED, not thrown. 334
call sites, one guard. Verified in isolation: good image and canvas draw, broken/unloaded/null/
undefined all skip, ZERO exceptions. Skips are counted on window.__skippedDraws() so a missing asset
stays discoverable rather than merely invisible.

**THE LESSON I SHOULD HAVE LEARNED SOONER.** Mike said "missing assets" in his very first description
of the error flood. I read past it three times because I was certain the fault was logical. The error
message named the cause and I did not believe it.

---

## DROP 0724dq — FOUND IT: drawImage WAS BEING HANDED NULL, EVERY FRAME

Build: 1776 assertions, 0 errors.

**MIKE'S REPORT WAS THE WHOLE ANSWER:** "over 4000 errors and climbing regarding draw error and
htmlimage element and missing assets."

    ctx.drawImage(XART.get(k), ...)      with k missing or not yet decoded

get() returned NULL, and drawImage throws
    "The provided value is not of type '(CSSImageValue or HTMLImageElement or ...)'"
EVERY FRAME. The loop catches it, so nothing crashes — THE FRAME SIMPLY STOPS AT THAT POINT. And
handleTitleInput() is the LAST statement in drawTitle. So the menu drew, animated, and was never
reached by its own input handler. Every symptom of the last ten drops in one line.

It was ALWAYS happening. Two things I did made it visible and made it worse: DBG.verbose stopped
suppressing everything after the first report, and the lazy loader turned a rare miss into a
constant one — before it, images were all created up front, so most were eventually ready.

**FIXED AT THE LOADER, NOT AT 334 CALL SITES.** get() now returns a 1x1 CANVAS when an asset is not
ready. A canvas is a legal CanvasImageSource and needs no decode, so it cannot have the same
not-loaded problem an Image would. rdy() is untouched, so every site that checks first behaves
exactly as before, and raw() is there for the few that need the real object.

**PROVEN WITH THE WORST CASE:** a loader where EVERY image is permanently unloaded
(complete=false, naturalWidth=0). 240 frames at the title: 5,760 drawImage calls, ZERO bad
arguments, ZERO errors. Before this change that same run threw on the first call.

**AND THE ASSET SWEEP IS REVERTED.** It passed 1,751 assertions and then produced 4,000 errors in a
real browser. The suite exercises a fraction of the draw paths a single frame does, so green was
never the same as safe. All 585 files restored; only cabinet_frame stays out, because the cabinet
itself is gone. If the asset count needs cutting later it has to be driven by something better than
my test coverage.

**MIKE ASKED FOR THE PRE-TRANSITIONS ZIP AND I DID NOT HAVE IT** — I had been writing every build to
the same filename. That is a straightforward process failure on my part. It also would not have
helped: DBG.transitions was already false in the build he was testing, so the transitions were not
the cause. Builds get unique filenames from here.

---

## DROP 0724dp — ASSET SWEEP, DRIVEN BY THE SUITE INSTEAD OF BY ARGUMENT

Build: 1768 assertions, 0 errors. Manifest 7,166 -> 6,578 image keys.

**A STATIC SCAN CANNOT DO THIS, AND I PROVED IT TWICE.** Keys in this codebase are built:
    by concatenation        'nsx_' + code + '_' + part
    by TEMPLATE LITERAL     `n6j_${short}_${state}_${n}`     <- my regex never looked at backticks
    from stage config DATA  liquid:'fx_lava' fed into _liquidFrames(key + '_' + i)
    by prefix ARGUMENT      buildModularBoss(b, IRONREV_SPEC, 'mbp_ir')
My best static model called 1,983 keys unreachable. Removing them broke 42 ASSERTIONS — thrusters,
buttons, terrain flats, weather, boss part grids, the liquid beds. Restored all 1,980 files and
started over.

**SO THE SUITE BECAME THE ORACLE.** Remove ONE family, run 1,751 assertions, restore it if anything
goes red. Every removal is empirically safe rather than argued safe:
    REMOVED  nui_fill 192, n6e_tlj 129, nthr_* 40 (five unused plume sets), chain_* 41,
             nsb_* 32, mfx_ex/las 39, nbk_* 19, n6w_* 30, cabinet_frame, nx_big, nx_ice,
             np5_orb, nex_smallanim ... 588 keys total
    REFUSED  fx_lava, nmb_fill, nxp_fall, nxp_roll, nwx_rainD/L, n6e_sky, mfx_bshot, nlqf_*,
             every nrc_* rival cutscene plate
The refusals are the interesting half — each is reached by a path no scan found, and there are now
assertions naming them so a future sweep does not try again and waste the same afternoon.

**QUARANTINED, NOT DELETED.** 585 files, 5.3 MB, in _sweep/. Excluded from the shipping zip and
restorable in one command.

**HONEST ABOUT THE SIZE.** 588 keys is 8 percent of the count but only ~5 MB, because the removals
were small UI and FX frames. The real weight is elsewhere: master maps at 4-6 MB each, the rival
cutscene plates at ~3 MB per pair, and 65 MB of music. Cutting the COUNT and cutting the BYTES are
different jobs — if the goal is package size, downscaling a dozen masters would do more than
deleting a thousand keys.

---

## DROP 0724do — THE COUNTER WAS LYING, AND key() WAS THE THROWER

Build: 1751 assertions, 0 errors. Transitions OFF. Debug mode on.

**"REGISTERING ALL MOVEMENTS, NUMBERS ARE CHANGING, BUT THE CURSOR IS JUST NOT MOVING."**
Those two facts together are the whole answer, and my own instrumentation was hiding it.

    window.addEventListener('keydown', e => { window.__inp.key++; ... key(e,true); ... });
    function key(e,d){ const k = e.key.toLowerCase(); ... }

The probe incremented its counter BEFORE calling key(). And key() opened with an UNGUARDED
`e.key.toLowerCase()`. If e.key is undefined — synthetic events, some IME and remapping layers, a
few keyboard drivers — that throws a TypeError before a single key is stored. So the counter rose on
every press while NOTHING was ever recorded, and my readout confidently reported input that had
already been dropped. I built the instrument that told me input was fine.

**FIXED:** keyName() falls back to e.code (KeyA -> a, Digit4 -> 4) then e.keyCode, the whole body of
key() is guarded, an unreadable event is ignored rather than fatal, and even preventDefault is
wrapped. The counter now increments AFTER the key is stored and shows UNREADABLE when nothing could
be extracted — a probe that lies is worse than no probe.

**DEBUG MODE, as asked.** A DBG switchboard on window, read live:
    DBG.transitions = false   OFF at Mike's request — the stage-1 opening AND the outbound routes
    DBG.spriteFont  = false
    DBG.probe       = true    the on-screen readout
    DBG.verbose     = true    log EVERY swallowed loop error, not only the first
The single-report limit on loop errors is what let three separate exceptions hide this week; verbose
removes that.

**THE PATTERN, THIRD TIME THIS SESSION:** I was misled by my own scaffolding. A stub that swallowed
actx.createBuffer. A harness that stubbed Input.down to return false. Now a counter that counted
events it then discarded. Every one of them told me the code was fine when it was not.

---

## DROP 0724dn — THE ANIMATING CURSOR WAS THE ANSWER

Build: 1738 assertions, 0 errors.

**MIKE'S OBSERVATION CRACKED IT:** "the in-game cursor was animating, which tells me the menu isn't
frozen." That is not a small detail — it is the whole diagnosis.

In drawTitle, EVERYTHING VISIBLE is drawn at lines 25-48: the logo, the menu items, the pulsing
INSERT COIN, the cursor. handleTitleInput() is line 49 — the LAST statement in the function. So a
throw there produces a title screen that animates perfectly and responds to nothing, and the loop's
try/catch keeps the frames coming so it never looks like a crash. Invisible by construction, which
is exactly why it survived eight rounds of me looking everywhere else.

**FIXED BY ORDER AND ISOLATION, not by finding the thrower.** I still do not know what throws on
Mike's machine — a clean browser simulation of this build runs to PLAY with zero swallowed errors.
So rather than guess a ninth time:
    1. CURSOR MOVEMENT RUNS FIRST, in a block that reads RAW held keys (not taps, so nothing can
       starve it) with its own edge detection, and it is itself wrapped so nothing can stop it.
    2. Every audio call on the path is individually guarded — a missing SFX must not cost the cursor.
    3. EVERYTHING ELSE moved into _handleTitleInputRest() behind a guard that CAPTURES the exception
       and PAINTS it on screen: `title input error: <message>`.
So the menu now works even if the rest of the handler is broken, and if anything still throws it
names itself instead of hiding.

**ALSO CONFIRMED FOR MIKE:** nothing in this build is base64-embedded. All 7,167 image paths, 148
audio paths and 884 BOF entries are real `assets/...` references — zero exceptions. The four
`data:...;base64` mentions in game.js are the dead branch of a ternary that always takes the
file-path side. manifest.js is 0.45 MB and game.js 0.98 MB; an embedded build would be hundreds of
megabytes and would choke the parser before a frame drew.

**AND I RAN THE SANDBOX OUT OF DISK** copying the asset tree for the tenth time. Cleaned up; tests
now run in place rather than against a copy.

---

## DROP 0724dm — MY OWN HARNESS WAS LYING TO ME ABOUT INPUT

Build: 1729 assertions, 0 errors.

**test_fl.js STUBS Input.down AND Input.tap IN THREE PLACES AND NEVER RESTORES THEM.**
    line ~419   Input.down=function(){return false;}
    line ~3234  Input.down=function(k){ return keybind.fire.indexOf(k)>=0; }
Everything after those points was testing MY STUB, not the game. When I tested the new title
fallback and it "did not move the cursor", I was measuring a function I had replaced with
`return false`. That is why a game that works in the browser-level simulation looked broken here.
Recorded permanently in section 146: THIS HARNESS CANNOT TEST INPUT. Input conclusions come from
the browser simulation, which drives real listeners against a real-shaped DOM.

**WHAT SHIPPED THAT ACTUALLY HELPS:**
  1. DIRECT FALLBACK on the title — reads the raw held-key state with its own edge detection, so it
     cannot be consumed by the shared tap pool and does not depend on keybind being intact. It runs
     alongside the normal path; whichever fires first moves the cursor.
  2. FULL-WIDTH CLICK ROWS — the old hit test required the pointer within 165px of centre. Mike's
     readout put his pointer at x=471 on a 480-wide field, so every click missed on x alone. The
     rows read as full-width bands on screen; now the hit box matches.
  3. F1 = RESET CONTROLS, labelled on the title screen, clearing all stored state and reloading.
     I have guessed wrong about this bug eight times. This is an escape hatch that does not require
     me to have guessed right.

**THE LESSON, AND IT IS THE SAME ONE AS THE STUB THAT SWALLOWED actx.createBuffer:** when a test
environment disagrees with reality, the environment is the first suspect, not the code. I have now
been misled by my own stubs twice in one session — once patching around a real error, once measuring
a function I had disabled myself.

---

## DROP 0724dl — THE FAULT WAS IN HIS BROWSER'S STORAGE, NOT IN ANY BUILD

Build: 1721 assertions, 0 errors.

**THE READOUT ANSWERED IT IN ONE LINE:**
    state title   kd40 ku41 md5 mm86   last shift   menu 0
Forty keypresses ARRIVING. The menu never moving. And the last recorded key was SHIFT.

His keybinds were broken AND SAVED. That is why reinstalling never helped and why my simulation
never reproduced it — the fault lived in localStorage, which a clean environment does not have.

**TWO BUGS MADE IT POSSIBLE:**
  1. The loader was `if(!j[a]) j[a]=DEFAULT[a]`. That only replaces a MISSING action. An EMPTY ARRAY
     IS TRUTHY, so {"down":[]} passed straight through and menuDown() returned false forever.
  2. The rebind screen did `keybind[action]=[k]` for whatever key was pressed — including a bare
     modifier. Bind a menu key to shift once and it is dead permanently, across every reload, with
     nothing on screen to say so.

**NOW:** every action must end up with at least one USABLE key; bare modifiers (shift, control, alt,
meta, capslock) are refused both at load and at rebind time; anything that fails is restored from
the defaults AND the save is rewritten so it cannot return on the next load. A legitimate custom
bind is still preserved — validation must not quietly erase customisation.

**WHAT THIS COST AND WHY.** Eight drops. Every fix along the way was a real bug — the chime key, the
eager loader, the dt clamp, audio-before-input, audio-before-setState, the build deleting
drawStaticPlayer. All worth having. But I spent eight rounds looking inside the build for something
that was in the USER'S PERSISTED STATE, and the only thing that found it was putting a readout on
the screen and asking Mike to photograph it. When a failure cannot be reproduced in a clean
environment, the difference between the environments IS the bug — I should have gone looking for
persisted state on the second report, not the tenth.

---

## DROP 0724dk — CABINET REMOVED, CREDIT RAILS IN

Build: 1704 assertions, 0 errors. The game still reaches PLAY.

**WHY THE CABINET WAS A GOOD THING TO CUT.** It was not just decoration. It gave the page:
  - a stacking context above the play area
  - a drop-shadow FILTER, and any filtered ancestor changes what `position:fixed` means for every
    descendant — the file already carried a long comment about fighting exactly that
  - a JS pass that mapped #game-frame into a hard-coded window rect (WIN_L/T/R/B as fractions of a
    1448x1086 plate) and positioned it absolutely
Three separate ways for a click to land somewhere other than where it appears. All gone.

**REPLACED WITH A PLAIN CENTRED ROW:** credits, game, credits. fit() sizes the play window to the
viewport at the game's own aspect, accounting for the HUD and divider, scaling on whichever axis
binds. The old layout function was called L and its listeners still referenced it, so the new one
is aliased rather than hunting every call site.

**THE RAILS ARE pointer-events:none AND user-select:none.** That is the whole point of the exercise
— nothing beside the canvas may intercept a click meant for it, and nothing may be dragged over the
game as selectable text. They hide in fullscreen and below 820px so they can never squeeze the play
window.

    left   COLEFORGE PRODUCTIONS 2026
    right  A GAME BY MIKE "FORGEMASTER" COLE

**NINE ASSERTIONS DELETED.** They all defended the cabinet layout — its window rect, its filter,
its fullscreen margin juggling. Keeping them would have meant asserting the correctness of
something that no longer exists. Replaced with seven that check the layout that took its place.

---

## DROP 0724dj — FOUND IT. THE BUILD WAS DELETING A FUNCTION THE GAME STILL CALLS

Build: 1694 assertions, 0 errors. The game reaches PLAY.

**MIKE'S BISECT WAS THE KEY.** "The last playable version was right before the transitions work."
That turned an unbounded search into a bounded one, and the answer was not in the transitions at
all — it was in the build.

    draw error in state launch: drawStaticPlayer is not defined
      at drawShipSprite (assets/game.js:15625)

**drawStaticPlayer IS DEFINED IN THE SOURCE — at gamecode.js:14072.** It sits INSIDE the span
assemble.py replaces (TITLE_ITEMS .. tryExit), so the build deleted it, and the replacement block
never re-defined it. drawShipSprite still calls it. So the moment the game reached LAUNCH it threw
EVERY FRAME, the loop's try/catch swallowed it and logged once, and the screen simply froze. Menus
worked. Nothing past them did. No error was ever visible.

**WHY EVERY TOOL I HAD MISSED IT:**
    node --check   valid syntax, nothing to report
    the harness    drives drawScene directly and never reaches LAUNCH
    1,689 assertions   all read the built file for STRINGS; none compared it against the source
Only diffing the built output against the source finds this class of bug, and I had never done it.

**NOW PERMANENT:** an assertion extracts every `function name(` from gamecode.js and from the built
game.js, and fails if anything defined in the source is missing from the build WHILE STILL BEING
CALLED. 531 source functions, 615 in the build, 1 lost, 0 lost-and-called.

**THE HONEST PART.** I chased this for six drops — the chime key, the eager loader, the dt clamp,
the audio-before-input handlers, the audio-before-setState. Every one of those was a REAL bug and
every one is worth having fixed. None of them was this. What actually found it was running the
built game in a loop until something threw, and reading the message instead of theorising. I should
have done that on the first report.

---

## DROP 0724di — THE READOUT HE COULD NOT SEE WAS THE ANSWER

Build: 1689 assertions, 0 errors.

**"I don't even see any numbers on the game screen"** was the most useful thing Mike has told me all
session. The probe draws on the TITLE. If he cannot see it, he is never reaching the title.

    function goTitle(){ Audio.init(); Audio.startMusic('title'); setState(GS.TITLE); menuIndex=0; }

Audio FIRST, unguarded, before the state change — the same shape as the input bug, one level up. If
init() throws, setState is NEVER REACHED. drawLoading calls goTitle every frame because its DONE
gate has passed, it throws every frame, the loop's try/catch swallows it, and the game sits on the
LOADING screen forever. No title. No menu. Nothing to click. And no readout to photograph, which is
why my instrumentation looked like it had failed too.

The chime plays at BOOT, before any of this — which is why sound seemed to come back while the game
stayed dead. Two symptoms, two different causes, and the returning sound made it look like progress
on the wrong one.

**FIXED AT THE SOURCE, NOT THE CALL SITE.** assemble.py uses the exact text of that goTitle line as
a span marker, so the line cannot be reshaped. Guarding init() and startMusic() internally fixes
goTitle and every other caller at once, which is the better fix anyway. A browser with no usable
AudioContext should lose sound, not the game.

**PROVEN WITH THE HARDEST CASE:** an AudioContext whose CONSTRUCTOR throws outright. The shipped
build now reaches 'title', the cursor moves 0 -> 1, and a click sets titlePending null -> 1, with
audio completely unavailable.

**THE PATTERN I KEPT MISSING:** audio was load-bearing in three separate places — the keydown
handler, the state transition, and the chime construction. Each looked like its own bug. It was one
architectural mistake repeated: a subsystem that is allowed to fail was being called before things
that must not.

---

## DROP 0724dh — SOUND IS BACK; INPUT PROBE FOR THE REST

Build: 1682 assertions, 0 errors.

**THE AUDIO GUARD WORKED** — Mike has sound again. That confirms the diagnosis was right as far as
it went: Audio.resume() was throwing and taking the keydown handler down with it.

**BUT CLICKS STILL DO NOT REGISTER, AND I CANNOT REPRODUCE IT.** In a faithful browser simulation
of the shipped build, with an audio stack that throws on EVERY call:
    keyboard   menuIndex 0 -> 1
    mouse      mouse.down true, coords map correctly (240,234), titlePending null -> 1
Both paths work. The canvas exists before the scripts run (line 75 vs 118). cabinet-img is
pointer-events:none. Nothing I can see intercepts the click.

**SO THE GAME NOW COUNTS ITS OWN EVENTS.** keydown, keyup, mousedown and mousemove each increment a
counter, and the title screen draws them with the last key and the last mapped coordinate. The
readout is GREEN if anything is arriving and RED if nothing is — the colour answers the question
before any number is read.

That splits the remaining possibilities cleanly:
    ALL ZERO / RED   the browser is not delivering events to the page at all — extension, focus,
                     iframe sandbox, or something outside the game entirely
    COUNTS RISE      events arrive and the fault is downstream in the menu, and the coordinates
                     shown will say whether the click is landing where the rows are

I have guessed four times on this bug and been wrong three of them. One photograph of that readout
is worth more than a fifth guess.

---

## DROP 0724dg — THE REAL CAUSE: INPUT WAS BEHIND AUDIO

Build: 1673 assertions, 0 errors.

    window.addEventListener('keydown', e => { Audio.resume(); key(e,true); });

**AUDIO FIRST, UNGUARDED.** If Audio.resume() throws — a blocked context, an autoplay policy, any
broken audio stack — key() NEVER RUNS. The keypress is never recorded and the game is completely
unresponsive. And the same broken subsystem is the one that would have played the chime, so it
produced the silence too. ONE LINE, BOTH SYMPTOMS, every single report.

**FOUR MORE HANDLERS HAD THE SAME SHAPE:** mousedown, touchstart, gamepadconnected, and both
once-only Audio.init hooks. All five now run their input work FIRST and attempt audio afterwards
inside a try. Audio.resume() itself is throw-proof, because every input path calls it.

**PROVEN, NOT ASSUMED.** Built a hostile audio stub whose every method throws, and ran the shipped
build against it: before the fix menuDown() stayed false forever; after it, menuIndex moves 0 -> 1
with the entire audio stack failing. That is the correct behaviour — a dead audio context should
cost sound and nothing else.

**AND I HAD ALREADY SEEN THIS.** Two drops ago my browser simulation printed
`handler threw: actx.createBuffer is not a function` — the bug announcing itself. I read it as a
gap in my stub, patched the stub, and moved on. The stub was incomplete AND the game was broken;
I fixed the wrong one and lost two drops.

**ALSO FIXED, FOUND ON THE WAY:** key() suppresses auto-repeat with `if(d && !keys[k])`, so a key
recorded as down that never receives its keyup can never produce another tap for the rest of the
session. Alt-tab is enough. Everything now releases on blur and on visibilitychange.

---

## DROP 0724df — FOUND IT: THE FRAME CLOCK HAD NO LOWER BOUND

Build: 1666 assertions, 0 errors.

Mike asked what keeps causing this. It was one line, and it was there the whole time:

    let dt=(now-last)/1000;  dt=Math.min(dt,0.05);  stateT+=dt;

**Math.min CAPS THE TOP ONLY.** A single negative frame makes stateT negative, and because stateT
ACCUMULATES it never recovers. Every state gate that waits on `t >= X` then fails FOREVER:
drawLoading never reaches its DONE test, goTitle() is never called, the game sits on the loading
screen, no input is processed — and the loop's own try/catch keeps the frames coming, so nothing
ever looks like it crashed. Silent, permanent, and it presents as exactly what Mike described:
cannot access the game, no chime, nothing responds.

**MEASURED, NOT GUESSED.** Ran the shipped build in a faithful browser simulation — two separate
scripts sharing one global, as index.html loads them. stateT reached -1,785,288,103 and the game
was still on 'loading' after 1,001 frames. With dt clamped to [0, 0.05] it reaches 'title'
normally. Same build, same simulation, one line different.

**WHY IT KEPT COMING BACK.** Nothing I had been fixing was the cause, so nothing I fixed helped.
The missing BOFX.chime key was real. The 7,166-request eager loader was real. Neither was THIS.
And my test suite could never have caught it: 1,660 assertions all ran against a harness that
drives drawScene directly and never exercises loop()'s clock at all.

**THE GUARD FORM MATTERS:** `if(!(stateT>=0)) stateT=0` rather than `if(stateT<0)`, because the
first also catches NaN and the second does not. A NaN dt would be just as permanent and even
harder to see.

**WHAT I SHOULD HAVE DONE SOONER.** Three reports of an irreproducible failure should have sent me
to simulate the real load path immediately, not to guess a fourth fix. The simulation took twenty
minutes and found it in one pass.

---

## DROP 0724de — I STOPPED GUESSING AND MADE THE GAME REPORT ITSELF

Build: 1660 assertions, 0 errors.

**THIRD REPORT OF THE SAME TWO SYMPTOMS.** No boot chime, dead menu. I have now shipped two fixes
for causes I could not reproduce — the missing BOFX.chime key (real, but not sufficient) and the
7,166-request eager loader (real, but not sufficient either). Both were genuine problems. Neither
was THE problem.

**WHAT THE SYMPTOMS ACTUALLY MEAN.** No chime AND no input, together, is what you get when the
script THROWS during load: everything after the throw never executes, so the input listeners are
never attached and the chime is never reached. It is one failure, not two.

**I CANNOT SEE HIS CONSOLE, SO THE GAME NOW SHOWS IT.** A window error handler paints the message,
the file and the line ON THE CANVAS in plain text, with 'Screenshot this and send it to Claude.'
underneath. A dead screen becomes one photograph instead of another round of me guessing.

**PLUS A WATCHDOG,** because a throw is not the only way to get a dead menu — a render loop that
never starts looks identical from the outside. drawScene ticks a counter; if fewer than 3 frames
have drawn after 8 seconds it says so in plain words. That distinguishes the two cases immediately.

**AND ONE REAL BUG FOUND BY READING.** newbootimage was missing from the lazy loader's PRELOAD list,
so drawLoading had nothing to cover with — the first four seconds were black. Found by reading the
loading screen rather than by testing it.

**THE HONEST NOTE:** I built a DOM stub to reproduce the load in node and it kept reporting a
failure that turned out to be an artefact of my own harness, not the game. I spent several attempts
chasing it. Instrumenting the real environment is what I should have done after the FIRST
irreproducible report, not the third.

---

## DROP 0724dd — BOSS FURY, AND A GAP THAT CANNOT CLOSE

Build: 1651 assertions, 0 errors.

**ON SOURCES, HONESTLY:** Mike asked me to research shmup boss patterns. I cannot browse from this
environment, so this is applied from knowledge of the genre rather than from pages I have just
read. Recorded in the code comment too, so nobody later mistakes it for a citation.

**THE ACTUAL DESIGN QUESTION — PREDICTABLE vs UNPREDICTABLE:**
    PREDICTABLE (fixed geometry: rings, spirals, walls, lattices) is LEARNABLE, and that is the
      point — it rewards mastery and lets a player feel themselves improve. A boss made only of
      this is trivial once solved.
    UNPREDICTABLE (aimed at where the player IS) cannot be memorised, so it stops a solved boss
      being a formality. A boss made only of this feels arbitrary, because there is nothing to
      learn.
Every pattern here is fixed geometry PLUS an aimed element whose weight rises with fury. The
skeleton tells the player where the safe space is; the aim makes them keep moving inside it.

**FOUR FURY TIERS, HP-GATED:** engaged / pressing / furious / desperate. Rate 1.00 -> 1.70, density
1.00 -> 1.90, aimed weight 0.20 -> 0.65. The fight TIGHTENS as the boss dies instead of thinning
out, which is the opposite of what a plain HP bar does.

**WOUNDED ANIMAL:** a sectional boss that has lost limbs fights harder with what is left (rate
1.18 -> 1.36 with three mounts gone), so stripping a boss escalates the fight rather than defusing
it.

**THE RULE THAT MAKES FURY FAIR, AND IT IS ENFORCED NOT HOPED FOR:**
  1. Every pattern TELEGRAPHS — a wind-up ring drawn UNDER the boss, before the shots it warns
     about. Unreadable is not the same as hard.
  2. A GAP ALWAYS EXISTS. Rings, walls and fans are generated with an opening, and the ring's gap
     is placed AWAY from the player so it is reachable.
  3. There is an assertion that walks the fired angles of every pattern at every tier and measures
     the widest opening. At desperate the ring still leaves 164px against a ~10px hitbox — while
     firing MORE (10 -> 21 shots), so the gap is not being preserved by simply not shooting.
A pattern that cannot be dodged is a bug, not a difficulty setting, and the suite now says so.

---

## DROP 0724dc — A PART IS A WEAPON MOUNT, NOT DECORATION

Build: 1641 assertions, 0 errors.

**THE SECTIONAL SYSTEM WAS COSMETIC AND I HAD NOT NOTICED.** L2 and L3 already had per-part damage
art and positional hits from 0724br — but there were ZERO references linking _sx to firing. A boss
with both arms shot off kept every weapon. The player was rearranging a sprite, not changing a
fight.

**WHAT CONTRA 3, R-TYPE AND FIRESHARK ACTUALLY SHARE.** Mike asked me to look at how those bosses
operate. The common mechanic is one rule, not three:
    R-TYPE     armour segments shield a core. Break the segments, expose the core. The fight has a
               SHAPE — you are opening a route, not grinding a bar.
    CONTRA 3   each limb owns an attack. Kill the limb, that attack stops. You choose which gun to
               silence first, and the choice matters.
    FIRESHARK  the boss visibly sheds parts and its pattern thins. Progress is legible without
               reading a health bar.
All three reduce to: A PART IS A WEAPON MOUNT. So every attack now declares which part it fires
from, and if that part is gone the attack is skipped and the boss rolls again.

**MEASURED END TO END:** concentrated fire on the magma colossus's left arm destroys it, its gun
returns false from sxCanFire, the right arm keeps firing, armament-left drops 0.71 -> 0.43 as the
second arm goes, and the boss is still alive with both arms gone — the core still has to be
finished.

**AND THE ASSERTION CAUGHT ME ARMING A CORE PART.** I had put ground_wave on lower_hull. A core
part with a weapon means a player who clears every limb still faces something they cannot remove,
and the fight loses the shape that makes the system worth having. Moved to the wing. The rule is
now checked across all five units.

**LEVEL 6 JET IS SECTIONAL TOO** — nose, both wings, body and tail, built from the 3x3 part grid
its art already shipped with (mbp_rl_rNcM clean/dam/ruin) rather than commissioning anything new.

---

## DROP 0724db — ONE CAUSE FOR ALL THREE SYMPTOMS: THE LOADER

Build: 1625 assertions, 0 errors.

**XART BUILT A new Image() FOR EVERY KEY THE MOMENT THE FILE PARSED.**
    if(window.BOFX&&BOFX.img){ for(const k in BOFX.img) X.img[k]=mk(BOFX.img[k]); }
The manifest has grown to 7,166 images totalling 295 MB, so that fired 7,166 simultaneous requests
before the first frame. That is one cause for everything Mike reported: the browser crawled, the
main menu could not respond because the main thread never got a clear frame, and the boot chime
never got the bandwidth to decode.

I GREW THIS PROBLEM. The manifest went 5,820 -> 7,166 keys across this session — every pack I
added made the opening flood worse, and the loader was never designed for it.

**IMAGES ARE NOW CREATED ON FIRST USE.** Every call site already guards on rdy(), which returns
false until an image has decoded, so nothing else had to change: a sprite appears a frame or two
after something first asks for it. PRELOAD covers the short list needed before the player can act —
boot plate, logos, stage 1 card, all nine ships, the thrusters, portraits and cards.
    288 of 7,166 keys up front. 33 MB instead of 295. A 96 percent cut in requests.

**THE CHIME IS FETCHED EAGERLY AND CALLS load() EXPLICITLY.** It is one small file and the first
thing the player hears; leaving it to compete with the image flood is why restoring BOFX.chime last
drop was not enough on its own.

---

## DROP 0724da — BOLTS GLOW, THEY DO NOT ANIMATE

Build: 1612 assertions, 0 errors.

**THE LASER WAS STROBING, NOT TRAVELLING.** fllaser cycled 8 frames at 40fps. The frames differ
enough that a bolt read as a flickering object rather than a fast one. One frame now, chosen at
spawn, with the GLOW pulsing — brightness and shadow, not geometry.

**AND IT POINTED THE WRONG WAY.** flaser drew unrotated while flspread, two lines below it in the
same function, already computed atan2 and rotated. So Falva's straight bolts pointed up no matter
which direction they were actually travelling. Both now orient to velocity, the way the missiles
always have.

**MISSILES: NO FRAME WALK, NO GROWTH, NO RANDOM FLAME.** They walked mfx_hom_0_5 through _9 AND
grew the sprite by 7px a step, so a missile changed shape as it flew. The exhaust length was
Math.random() per frame, which reads as a rendering artefact rather than a burning motor. Fixed
frame, fixed size, and a smooth pulse on the same clock the bolt uses.

**THERE WERE TWO MISSILE DRAWS AND I ONLY FIXED ONE.** The assertion greps the WHOLE FILE rather
than the block I was editing, and caught the second at line 8100 still walking its frames. That is
the difference between an assertion and a spot check — I had already convinced myself the job was
done.

---

## DROP 0724cz — CONNECTORS OUT, TERRAIN ROUTES IN

Build: 1601 assertions, 0 errors.

**THE CONNECTOR AND TRANSITION PLATES ARE REJECTED.** Mike saw the 3>4 plate scrolling and called
it: a snowy suburb that belongs to neither the ice stage nor the airbase. `outbound.con` is now
forced null even for the four joins that HAVE a plate on disk, so none of them can appear.

**EVERY JOIN NOW CARRIES A TERRAIN ROUTE.** TRANS[from] says what the player travels through, built
from the stage backgrounds and the 64x64 flats — the real terrain either side, not a bridging plate:
    1>2 water                    5>6 sky -> space (the chase ends there)
    2>3 water -> lava            6>7 space -> sky
    3>4 lava -> ice              7>8 sky -> metal
    4>5 ice -> sky               8   metal -> space

**STAGE 6 IS A SKY STAGE, NOT SAND.** Mike called this out specifically. Heavy Turbulence is flown
in the air, so 6>7 descends from SPACE to SKY and touches no ground at all. Asserted that sand
appears nowhere in that route, so it cannot creep back in.

**AND sky/space DELIBERATELY HAVE NO FLAT.** TRANS_FLAT maps them to null rather than to
tflat_sky — because tflat_sky is a crop of the ORBITAL stage, and using it as a daytime sky is
exactly the starfield mistake Mike could not identify two drops ago. The assertion names that
mistake so the next person to reach for a flat called 'sky' finds out why it is null.

---

## DROP 0724cy — THE SEAM, THE VERGES, THE WATER

Build: 1586 assertions, 0 errors.

**MY "FIX" REPRODUCED THE BUG EXACTLY.** The plate has TWO fully transparent 14-row bands: 114-127
and 986-999. Stepping by H-128 = 872 lands the next tile's 114-127 band precisely on the previous
tile's 986-999 band — both empty, black stripe across the road. I had measured that its top-128
matched its bottom-128 and concluded it tiled, without checking that BOTH of those bands were
transparent. 858 = 986-128 puts each tile's band over the other's solid content. Measured across a
5-tile composite: 0 black rows at 858, 42 at 872.

**AND I DESTROYED SIX PLATES ON THE WAY.** My first repair took min and max of ALL empty rows
rather than grouping them into CONTIGUOUS runs, so it blended rows 114 through 995 — the entire
image. nst4b_exit came out as 1000 empty rows. Restored all six from the original zips and redid it
properly. The lesson is the same one as the regex edits: a range built from min/max of a scattered
set is not a range, it is the whole thing.

**GRASS VERGES ROUNDED.** The alpha down the sides was a hard vertical cut, reading as a sliced
strip. Only the OUTERMOST rim of alpha is softened — never the interior, never the roadway.

**THE WATER WAS A KALEIDOSCOPE, AND THAT WAS MY DOING.** I built the liquid flats with a 4-way
mirror because it wraps at exactly 0.00 by construction. It does — and it looks like a
kaleidoscope, which is worse than a faint seam. Water scrolls VERTICALLY, so only the horizontal
edge has to mirror; the vertical one can be offset-blended. Rebuilt water, icewater and lava that
way: still 0.00 wrap, but vertical mirror symmetry went from 0.0 (perfectly reflected) to 22-34.

---

## DROP 0724cx — THREE FAULTS MIKE SPOTTED IN THE MOCKUP, ALL REAL

Build: 1581 assertions, 0 errors.

He asked whether it was a mockup. It was — a render driven by the shipped build's own constants,
which is why all three things he spotted were genuine code faults and not artefacts of the render.

**1. THE RUNWAY DID NOT CONNECT.** I tiled the EXIT plate by butting it, on the strength of its
top ROW matching its bottom ROW. That measurement was wrong twice over: its top and bottom 4 rows
are FULLY TRANSPARENT, so butting left a black band, and its own top-128 differs from its
bottom-128 by 24 — it was never the repeating piece. nst4b_run IS: top-128 equals bottom-128 at
0.000, exactly as the pack's `seam_overlap:128` describes. Stepping by H-128 overlaps those
identical bands. Verified in a render: zero near-black rows across the road.

**2. PURPLE HALOS.** 5,469 purple pixels on nst4b_exit with 96% sitting on the alpha edge — key
bleed from when the field was cut out. All six runway plates repaired by pulling colour in from
the nearest clean neighbour rather than punching the halo through, so the runway's own edge detail
survives. Worst plate 6,175 -> 272.

**3. THE SKY WAS A STARFIELD.** I tiled 'tflat_sky' — which I had extracted from the ORBITAL
stage. A fine space texture and a terrible daytime sky; Mike could not tell what he was looking at
and neither could I have. Now uses nl6sky_stage06_sky_scroll_640x960, the authored sky. Frame mean
went from near-black to (6,37,171).

**4. THE COAST CAME AT US BACKWARDS.** I had the shoreline rising out of the BOTTOM, which reads as
the coast advancing on the player. In a vertical scroller everything the player approaches enters
from the TOP and travels down past them. The shore now starts above the view with open water below
and sweeps down: sand pixels 0 -> 104,118 -> 230,669 across the phase.

**THE PATTERN:** every one of these came from me measuring a proxy and stopping there — a matching
ROW instead of a matching BAND, a flat named 'sky' instead of a sky, a direction that looked like
motion without asking which way. The renders are worth making precisely because they surface this
before Mike has to play it.

---

## DROP 0724cw — LEVEL 1 OPENING CINEMATIC

Build: 1569 assertions, 0 errors.

**THE TRANSITION PLATES IN THE ZIPS ARE THERE, AND MIKE CALLED THEM USELESS.** Found 4 of the 7
joins (3>4, 4>5, 6>7, 7>8) plus 4 ordered-dither seam strips. Recorded, not used.

**FIVE PHASES, ONE CLOCK:**
    RUNWAY   the runway EXIT plate tiled vertically. Verified it wraps at 0.00 top-to-bottom,
             which is what lets the roll-out be any length — the other two sections overlap by
             128 instead and would not have tiled.
    TAKEOFF  the ship SCALES DOWN as it climbs away (1.00 -> 0.50) with a camera pan. We hold.
    SKY      cut to sky and cloud, scroll ramping 74 -> 900 on a cubic. By SCROLL RATE ALONE —
             no blur, no filter, no overlay, because Mike asked for Genesis speed and that is
             exactly how Genesis did it.
    COAST    a coastline GENERATED from the sand and water flats: two sine terms at different
             rates so it does not read as a repeating wave, clipped so the shore is a real edge,
             rising toward the player as they approach.
    HANDOFF  3-2-1-GO over the live field.

**THE RULE, AND HOW IT IS GUARANTEED.** Mike has flagged jerky cuts repeatedly. The sequence flies
the REAL player object the whole way and PLAY simply takes over in place — nothing is handed over
except control. Asserted across all 960 frames of the sequence: the player's x and y never change,
not once, and the handoff does not touch them either.

**A BUG THE SUITE CAUGHT IMMEDIATELY.** My first wiring did `setState(GS.OPENING); return;` near
the TOP of beginStage — which skipped everything below it: the wave script, the spawn tables, the
timers. Level 1 stopped spawning its approved enemies entirely. The flag is now raised at the top
and applied at the END, once the stage is fully built underneath the cinematic. Without that
assertion I would have shipped a beautiful opening onto an empty level.

**NEXT:** this is the pattern for the other transitions. The 4>5 boss chase is the big one and
should be built on its own.

---

## DROP 0724cu — LANDMARK AT THE TOP, SKY EXCLUDED, TRANSITION FLATS

Build: 1553 assertions, 0 errors.

**I HAD THE STACK UPSIDE DOWN.** The scroll maps as `sY = H - scroll - winH`, so the view starts at
the BOTTOM of the assembled image and climbs. I put the landmark LAST in the array, which places it
at the bottom — the player would have flown into the dam in the opening seconds and then spent the
rest of the stage over ordinary jungle. The landmark is now FIRST, with the boss approach directly
beneath it and the loops filling downward to the start.

**THE SKY STAGE GETS NO LANDMARK.** Stage 5 is orbital — there is no ground destination to arrive
at, and grafting the void plate on read as a scene change rather than a climax. It keeps its loops
and boss approach.

**13 TRANSITION FLATS, 64x64, in assets/graphics/transition-flats/**
    terrain  grass sand gravel ice road concrete sky metal
    liquid   lava water icewater lavafall waterfall
Not cropped at a guessed position: every 64x64 window in each source is scored on local variance,
wrap error and agreement with the terrain's target colour, and the best wins.

**TWO THINGS I GOT WRONG AND FIXED BY MEASURING:**
  1. The first pass returned ORANGE DIRT for 'grass'. The scorer weighted flatness at 1.0 and
     colour at 0.30, so it optimised for smoothness and ignored what the material actually was.
     Colour now dominates at 2.20. Verified by hue: grass 65 deg, ice 212, lava 7.
  2. My first seamless step rolled each tile by half and feathered the interior seams. That is
     wrong — the OUTER edge afterwards is the old centre, and nothing makes the old centre
     self-match. Grass still wrapped at 20. Replaced with a 4-way MIRROR, which wraps exactly by
     construction. All 13 now measure 0.00 on both axes, and tiling each 4x4 produces no grid line.
  3. The liquid pass silently produced NOTHING at first: lava and water are high-variance by
     nature, so every window failed the terrain flatness threshold. Liquids get their own.

---

## DROP 0724ct — STACK-SAFE BACKGROUNDS + ORIGINAL LANDMARK END-PIECES

Build: 1524 assertions, 0 errors. Manifest 7105 -> 7153.

**THE PACK'S CLAIM IS LITERALLY TRUE.** Tested every one of the 37 modules against its stage's
universal socket and against its own opposite edge: 0 failures, mean difference 0.0000. Byte
identical, not approximately matching — so "stack in any order" holds, and the loop order is now
SHUFFLED per run.

**LANDMARK END-PIECES, BUILT FROM THE ORIGINAL MASTERS.** The dam, volcano and ice circle sit at
the TOP of lvl1_master_dam / lvl2_master / lvl3_master (confirmed by measuring which 100px band
differs most from each map's own median — y=0 in every case). Each end-piece is assembled as:
    the stage's universal socket, copied VERBATIM   128px  -> docks at exactly 0.0000
    a smoothstep cross-fade into the landmark       160px  -> no hard cut
    the landmark itself, widened 325 -> 800
Copying the socket rows rather than resampling them is what makes the dock exact; a resize of even
one row would have put a visible line at every stage's climax.

**STAGES ARE NOW ROUGHLY 2.2x LONGER.** Stage 1 goes from one 3616px image to 8011px assembled, and
stages 2, 3, 4, 5 and 7 get scrolling backgrounds they never had. Every join in every full stack
measures 0.0000, landmark included.

**A ZERO-HEIGHT STACK I AVOIDED BY LUCK.** The first version read module heights from
im.naturalHeight. That is 0 until an image finishes loading, so building the stack one frame early
would have produced a stack of zero-height modules and a background that never scrolled. The
harness exposed it by returning stub dimensions — 448px instead of 8011. Heights are now measured
from the files at build time and baked into the code.

**AND A WARNING FOR MY OWN TOOLING:** the magenta in these plates is INTENTIONAL liquid and void
placement — solid regions up to 106,130px, against the single-pixel fringe that marks key residue.
The chroma sweeps must never run on assets/levels/stack/. Verified before importing, not after.

---

## DROP 0724cs — THE CHIME, AND THE MONKEY-PATCH REMOVED

Build: 1497 assertions, 0 errors.

**THE CHIME: I DELETED IT FROM THE MANIFEST WITHOUT NOTICING.** One of my manifest rewrites wrote
    json.dumps({'img': X})
which discarded every OTHER top-level key in BOFX — BOFX.chime among them. BootChime's first line
is `if(!window.BOFX||!BOFX.chime||!window.Audio) return null;`, so it returned null and the chime
was never constructed. No error, no warning, just silence. The audio file was on disk the whole
time. Key restored, and there are now assertions that BOFX keeps chime AND img, that BOFA keeps
sfx AND music, and that BOF keeps atlas/boot/cards/stageArt/stageFont — so a rewrite that drops a
namespace fails the build instead of shipping.

**THE FREEZE: I REMOVED THE MONKEY-PATCH RATHER THAN GUESS AGAIN.** Wrapping ctx.fillText and
ctx.measureText at load was the only change touching a canvas API used on every screen. I could
not reproduce the freeze here because the harness STUBS the canvas — a monkey-patch behaves
differently against a stub than against a real CanvasRenderingContext2D, which is exactly the gap
that let this ship. Turning GF.on off was not enough: the wrapper was still installed either way.
It is now not applied at all. The game uses the TTF exactly as it did before drop 0724cq.

GF and installGameFont stay in the build. `installGameFont(ctx)` with `GF.on=true` from the console
enables the sprite font on demand — which is how we find out whether it really was the culprit
without betting the build on it.

**WHAT I SHOULD HAVE DONE:** not monkey-patched a browser API I cannot exercise in the harness. If
a change cannot be tested where I work, it needs to be opt-in from the start, not opt-out after it
breaks.

---

## DROP 0724cr — SPRITE FONT DEFAULTED OFF AFTER AN INPUT REGRESSION

Build: 1483 assertions, 0 errors.

**MIKE COULD NOT MOVE OR SELECT ANYTHING AT THE START SCREEN.** That is a hard regression and it
came in with the sprite font wrap, which is the only thing that touched a canvas API used on every
screen.

**I COULD NOT REPRODUCE IT.** The harness stubs the canvas, so wrapping ctx.fillText and
ctx.measureText behaves differently there than in a browser. Traced what I could and cleared:
  - drawTitle DOES call handleTitleInput, and handleTitleInput DOES read menuUp/menuDown/confirm
    (verified by brace-matching the shipped build, not by grep — my first check used lastIndexOf
    without the paren and matched the wrong string, reporting a break that was not there)
  - all 132 font strings are valid; the four that looked malformed are concatenated expressions
    my regex truncated at the first quote
  - both installGameFont calls are guarded and cannot throw at load

**SO I TURNED IT OFF RATHER THAN SHIP A GUESS.** GF.on defaults to false and the game runs on the
TTF exactly as it did before drop 0724cq. The renderer, the metrics and the 94 glyphs all stay in
the build; GF.on=true enables it without a rebuild.

**THE JUDGEMENT:** I broke a working build with a change I cannot verify from here. Reverting to
the known-good path costs a feature; leaving it on costs Mike a game he cannot start. If turning it
off restores input, the wrap is confirmed as the cause and I can fix it properly. If it does NOT,
the cause is elsewhere and I have narrowed it usefully either way.

---

## DROP 0724cq — THE SPRITE GAME FONT IS NOW THE GAME'S FONT

Build: 1483 assertions, 0 errors.

**INSTALLED BY WRAPPING ctx.fillText ONCE, NOT BY EDITING 132 CALL SITES.** Every existing text
call keeps working untouched: the wrapper reads ctx.font for the size, ctx.textAlign for the
anchor and ctx.fillStyle for the colour, then draws the sprite glyphs. Anything the glyph set
cannot handle falls straight back to the original fillText. measureText is wrapped alongside it so
centring and layout stay consistent. One install point, one place to switch it off.

**METRICS MEASURED, NOT GUESSED.** The glyphs are uniform 32x40 cells with a median cap height of
22px and a baseline at y=29. So a request for Npx draws a cell of N*(40/22) with its top at
baseline-29*scale, which lands the sprite where the TTF would have put it. Verified across
8/10/12/14/16/18/24px: cap heights land within 0-12 percent of the request and every baseline is
exact.

**A THREE-DIGIT PAD THAT COST EVERY PUNCTUATION GLYPH.** My key builder padded character codes to
TWO digits ('c33' for '!') while the extractor had written THREE ('c033'). Letters and digits use
the character directly so they resolved fine — only punctuation failed, and it failed SILENTLY,
falling back to the TTF. The assertion that walks all 94 printable ASCII codes caught it; a spot
check of "does the font work" would have passed.

**SAFETY.** GF.on=false returns the whole game to the TTF instantly. A glyph failure is caught and
falls through rather than killing the frame. Installing twice is a no-op. The tint cache is bounded
at 900 entries so a colour-cycling effect cannot grow it without limit.

---

## DROP 0724cp — ONE FONT EVERYWHERE, PORTRAITS UPGRADED

Build: 1470 assertions, 0 errors.

**MOST OF THE GAME'S TEXT WAS NOT IN THE GAME'S FONT.** Of 164 ctx.font call sites, only 41 asked
for BOFmil — the other 112 fell back to plain `monospace`, meaning whatever face the browser
happens to supply. That is why the typography looked inconsistent between screens: it genuinely
was two different fonts. All 112 moved over; zero system-font sites remain.

**THE PORTRAIT SYSTEM WAS ALREADY COMPLETE — I ALMOST BUILT A SECOND ONE.** I had registered
Mike's new Falva and Lizzie art as `face_<pilot>_<emo>` and listed "portraits not wired" as
outstanding. The game already had all NINE pilots x SEVEN emotions as `port_<pilot>_<emo>`, 63 keys,
with a resolver picking by emotion. My 14 keys were duplicates under a name nothing reads.
Checked which art was actually better before choosing: the new files are 238x347 and 295x399
against the old 181x265 and 190x265 — roughly 40 percent more detail. So the new art now backs the
LIVE port_ keys, the old files are retired to _unused/, and the duplicate face_ keys are gone.

**THE LESSON IS THE SAME ONE AS THE BOSS BARS.** Before wiring an asset, check whether the thing it
feeds already exists under a different name. Twice now the "missing feature" was a naming mismatch
between what I registered and what the code reads.

---

## DROP 0724co — TWIN ENGINES ARE THE SINGLE PLUME, DRAWN TWICE

Build: 1464 assertions, 0 errors.

**THE TWIN COMPOSITE COULD NEVER HAVE LINED UP.** It was ONE wide image with its two flames baked
at a FIXED spacing. Ships' engine bells sit at different offsets — cole 0.126 of hull width,
decker 0.123, maverick 0.165, juggernaut 0.160, axel 0.179 — so no single spacing fits all five.
Being one wide image, it also read oversized next to the singles, which is what Mike saw.

**ONE SHAPE FOR EVERYONE.** Every pilot now uses Yuri's single plume, hue-swapped to their colours.
Twin-engine airframes draw that SAME plume TWICE, at their own measured nozzle offsets. Size is
identical everywhere because it is literally the same sprite at the same dimensions, and alignment
is correct by construction rather than by a spacing that happens to fit. Lizzie keeps her warbird
flame — one engine, one plume.

**AND THE OFFSETS TOOK THREE ATTEMPTS TO MEASURE.** Detecting nozzles by the bottom row caught
wingtips (cole read 5 nozzles). Detecting by which columns extend furthest back caught wingtips
again (axel +/-0.40). What works is the INNERMOST symmetric pair at the tail: engine bells sit
either side of the spine, never at the extremities. Asserted that every offset lands between 0.10
and 0.22, so a future mis-detection fails the build instead of shipping.

---

## DROP 0724cn — EVERY PLUME THE SAME SIZE

Build: 1456 assertions, 0 errors.

**A SHARED WIDTH DID NOT PRODUCE A SHARED SIZE.** The plumes were sized off _dw. Two things made
that fail: _dw now follows each hull's own aspect (from the height normalisation last drop), AND
the three plume shapes have different aspects of their own —
    twin 0.88     single 1.13     Lizzie's warbird 1.36
so one width gave three different lengths, with Lizzie's running far longer than the rest.

**NORMALISED ON LENGTH.** Every plume is now the same fraction of the CONSTANT target hull height.
The formula has no per-pilot term at all, which is the property worth asserting: it cannot differ
between planes, rather than merely happening not to today.

Width still follows each shape, and that is deliberate — a twin plume is two nozzles side by side
and should span wider than a single. Same length, correct proportions:
    twin  32 x 37     single 32 x 28     Lizzie 32 x 24

---

## DROP 0724cm — FALVA'S PLUME: IT WAS THE SHIP, NOT THE THRUSTER

Build: 1450 assertions, 0 errors.

**THREE WRONG SUSPECTS BEFORE THE RIGHT ONE.** Falva's thruster looked missing. I checked the
anchor (correct — 336 vs a hull ending at 345, tucked in exactly like everyone else). I checked
colour contrast against her hull (231, well clear of the 95 threshold). Neither was the problem.

**SHIPS WERE SCALED TO A FIXED WIDTH.** Their content HEIGHTS are near-identical — 202 to 236px —
but their WIDTHS run 143 (decker) to 222 (lizzie). Width-scaling therefore made the narrow
airframes draw far taller than the wide ones:
    falva  150px wide -> 385px tall drawn        cole 203px wide -> 279px
Falva rendered around a third larger than everyone else, so her hull bottom — and her correctly
anchored plume with it — sat far below where every other pilot's did. The plume was never wrong;
it was following a ship that was the wrong size.

**NORMALISED ON CONTENT HEIGHT.** Every pilot's hull now draws to the same on-screen height, with
the canvas height derived from it and the width following the aspect rather than driving it.
Measured: Falva 128 -> 88 drawn height, every other pilot moving under 8 percent. Drawn heights
now agree within 13 percent across all nine, against 38 percent for Falva alone before.
Verified in a render: her plume reads at 1264 visible px, against Maverick's 1232 — previously it
ran off the bottom of the frame entirely.

**THE PATTERN WORTH KEEPING.** When an element looks wrong, check what it is ANCHORED TO before
changing the element. Three drops of thruster adjustments could not have fixed a ship that was the
wrong size.

---

## DROP 0724cl — PER-PILOT THRUSTERS: TWIN / SINGLE, PALETTE-SWAPPED

Build: 1443 assertions, 0 errors.

**ONLY THE TWO PLUMES MIKE PICKED ARE USED NOW.** Decker/Maverick's TWIN for airframes with two
exhausts (cole, maverick, axel, decker, juggernaut); Yuri's SINGLE for the rest (falva, yuri,
freezer). Lizzie keeps her own — classic B-series warbird flame. The other three types in the sheet
are no longer drawn on anyone.

**PALETTE SWAP IS HUE-ONLY, AND THAT MATTERS.** Rotating hue in HSV preserves the authored shading,
the white-hot core and the alpha edge; only the colour moves. A flat recolour would have flattened
the core, which is the part that makes it read as fire rather than as a coloured shape. Brighter
pixels take the primary hue and dimmer edges the accent, so each plume keeps its hot centre.
    axel 205 (blue/white)   freezer 275 (purple/orange)   maverick 100 (green/orange)
    cole 105  yuri 0 (red)  falva 320 (pink)  decker 45 (gold)  juggernaut 25 (orange)
Verified by converting the rendered means back to hue: 9 of 9 palettes distinct.

**FALVA WAS INVISIBLE AND THAT WAS TWO PROBLEMS, NOT ONE.** She was on type 2 — a plume that is
narrow AND warm-coloured, sitting under a hot-pink hull, so it vanished into her own airframe. She
is on the single plume in pink now, and the global size went 0.30 -> 0.42 of the ship width, which
also fixed Cole reading faintly.

**POSITION: 3px INTO the tail** rather than 2px below it, so the plume tucks under the bottom tip
instead of hanging off it.

---

## DROP 0724ck — THRUSTER: UNIFORM SIZE, ATTACHED TO EACH HULL

Build: 1432 assertions, 0 errors.

**SIZE IS NOW ONE CONSTANT.** Every pilot's plume is the same fraction (0.30) of the ship's drawn
width, so all nine read at the same scale. Previously it tracked each sprite's own proportions,
which made them subtly different sizes for no reason.

**THE ANCHOR COULD NOT BE A CONSTANT, AND MEASURING PROVED IT.** The plain sprites do not end at
the same point in their canvases — the opaque content stops at:
    yuri 0.834   decker 0.895   falva 0.896   juggernaut 0.898   maverick 0.901
    cole/axel/freezer 0.904   lizzie 0.921
An 8.8% spread. A single offset would have left Yuri's plume floating in the empty gap below his
tail and buried Lizzie's inside her fuselage — the exact class of "close enough" that produces a
bug report two drops later. _HB holds each pilot's measured hull bottom, with a 2px overlap so the
plume attaches rather than hovers.

The anchor is computed from the ship's OWN draw box (the same _dw/_dh the sprite draw uses) rather
than from player.w, so it stays correct if the ship scale ever changes.

**VERIFIED BY PIXEL, NOT BY EYE.** Rendered all nine with the build's own constants and checked for
a vertical gap between the hull's last row and the plume's first: 9/9 contiguous.

---

## DROP 0724cj — THE FLAMELESS AIRFRAME, THIRD TIME AND CORRECT

Build: 1424 assertions, 0 errors.

**I GOT THIS WRONG TWICE AND THE MEASUREMENTS ARE WHY.**
  Attempt 1 (0724bn): counted OPAQUE pixels in the tail. ship_<pilot>_t had fewer, so I called it
  the stripped frame. Opaque count cannot tell a flame from a tailfin.
  Attempt 2 (0724cb): counted HOT COLOUR and the answer INVERTED — _t carries the MOST flame
  (lizzie 1218 px, decker 470, yuri 383). _t is the THRUST frame. I had been drawing the most-lit
  airframe in the set and overlaying a second engine on top of it, which is exactly the doubled-up
  thruster Mike photographed twice.
  Attempt 3: I stopped measuring and rendered all 5 variants x 9 pilots for Mike to point at. He
  did, in seconds. THE PLAIN FRAME — ship_<pilot> — is the flameless idle, for every pilot.

**THE LESSON IS ABOUT WHEN TO ASK.** Both measurements were competently executed and both were
aimed at a proxy for the thing I cared about. When a proxy has failed once, the next move is to
show the human the actual images, not to invent a third proxy. That took two wasted drops.

**FALVA IS THE ONLY EXCEPTION.** Every other pilot's turn, bank and barrel-roll frames are drawn
without an engine; hers all carry one. She now holds her flameless idle frame through rolls, banks
and twists, so our thruster stays attached and hers never reappears.

**AND THERE WAS A THIRD ENGINE.** Three legacy `player_thrust` blits were still firing under
everything — two in gamecode, one in patches — plus an else-branch that drew a hand-rolled blue
RECTANGLE as a thruster. All removed. Our own sheet is now the only engine drawn anywhere.

---

## DROP 0724ch — REAL HIT ART, PER-BOSS MUSIC, THRUSTERS, SHRAPNEL

Build: 1417 assertions, 0 errors.

**THE "CSS DECALS" WERE ctx.arc AND fillRect.** Every impact in the game — bullets on enemies,
crates, pills, bosses — drew flat vector primitives: stroked rings, filled discs, rectangles. On
top of pixel art that reads exactly like a web overlay, which is what Mike was seeing.
Impacts now blit the authored 8-frame spark set (nx_small_) with debris on the smoke set, tinted to
each particle's own colour so the per-weapon palettes still read. The primitives survive ONLY as a
fallback for frames where the art has not loaded — not as the normal path.

**EVERY BOSS HAS ITS OWN TRACK.** The engine already built 'boss'+run.stage; the keys simply did not
exist, so all eight fell back to one. Named for the boss they belong to:
    1 dam_keeper  2 magma_colossus  3 cryo_behemoth  4 iron_revenant
    5 unity_breaker  6 battle_in_the_sky  7 boss7  8 vile_existence (Iron Cage)
Eight distinct files, asserted no two share.

**THRUSTERS MAPPED BY CHARACTER, NOT ROUND-ROBIN.** Six authored types across nine pilots — the
heavies share the heavy plume, the fast jets the tight one. Juggernaut gets its own.

**ROLLERBALL DEBRIS, TWO BEHAVIOURS.** On COLLISION the ball chips fragments where it struck —
cosmetic, marking the hit. On BURST it comes apart into SHRAPNEL that DAMAGES enemies, sub-bosses
and bosses on the way out, so holding a full ball until it expires is now worth something. Each
shard hits a given unit once, tracked per shard. Verified an enemy actually loses health.

**AND AN EARLY RETURN THAT WOULD HAVE HIDDEN THE PLAYER.** My first thruster mapping returned after
drawing the new plume — but the thruster is drawn BEFORE the hull, so that would have skipped the
ship entirely on every frame the new art loaded. Restructured as an else branch. node --check could
never have caught it: perfectly valid code that draws nothing.

---

## DROP 0724cg — MUSIC REASSIGNED AND FOLDERED, CAMPAIGN ENTRY

Build: 1400 assertions, 0 errors. 35 music keys, 0 broken.

**EVERY TRACK REASSIGNED TO MIKE'S MAP AND RENAMED TO SAY WHAT IT IS:**
    stage 1  lvl1.mp3               -> stages/1/stage1_rumble_in_the_jungle.mp3
    stage 2  Hot_Flight.mp3         -> stages/2/stage2_its_hot_in_here.mp3
    stage 3  lvl3.wav               -> stages/3/stage3_ice_still_cant_see.wav
    stage 4  crawling.mp3           -> stages/4/stage4_crouching_missiles.mp3
    stage 5  Lord_of_the_shadows    -> stages/5/stage5_all_for_one.mp3
    stage 6  Deathtrap.mp3          -> stages/6/stage6_heavy_turbulence.mp3
    stage 7  Fierce_Planes.mp3      -> stages/7/stage7_not_another_sewer.mp3
    stage 8  lvl5.mp3 (old lvl5)    -> stages/8/stage8_furious_death.mp3
    stage 9  rival.mp3              -> stages/9/stage9_bonus_warp_run.mp3
    boss 6   Battle_in_the_sky      -> boss/boss6_battle_in_the_sky.mp3
    boss 7   boss6.mp3 (old)        -> boss/boss7.mp3
    menu     untitled.mp3           -> menu/password_and_stage_clear.mp3
Filenames now state their job, so nobody has to consult a table to know what lvl5.mp3 is.

**A CONFLICT IN THE BRIEF, FLAGGED NOT GUESSED:** lvl3-alt AND Fierce Planes were both assigned to
stage 7. Took Fierce Planes (the later instruction) and left lvl3-alt in unassigned/ rather than
silently dropping one.

**THREE ASSEMBLE ANCHORS I BROKE AND RESTORED.** assemble.py already owns the stage-music rows, so
editing gamecode.js directly consumed its anchors and failed the build twice. The reassignment now
lives IN assemble.py alongside the existing steps. Same lesson as the drawBoot / pickDiff overrides:
find who owns the line before editing it.

**CAMPAIGN BOOT TYPES.** The log popped whole lines in at 0.26s intervals in silence. It now types
character by character at 34 cps and ticks as it goes, so it reads as a terminal coming up.

**MUSIC CROSSES AT DIFFICULTY SELECT, NOT WHEN THE MAP FORMS.** Choosing a difficulty is the moment
the player commits, so the menu track fades and the campaign track comes up UNDER the boot
sequence. The three sites that used to start it now only do so if nothing is already playing, which
keeps password entry and mid-run returns working. pickDiff is defined in BOTH files and patches
wins — SIXTH time that file has held the live copy, and I checked first this time.

---

## DROP 0724cf — ROLLERBALL, CHARGE RING, PORTRAITS, THRUSTERS

Build: 1385 assertions, 0 errors. Manifest 7012 -> 7074 (+62).

**THE CHROMA KEY WAS DIFFERENT PER SHEET AND I MEASURED IT RATHER THAN ASSUMING.**
    rollerball / debris / charge frames   CYAN key
    thrusters                             MAGENTA key
    portraits                             BLACK background
Every previous pack in this project has been magenta. Keying magenta on the cyan sheets would have
left the entire background intact and keyed nothing; keying cyan on the thrusters would have eaten
the blue in the flame. One test per sheet, 0 semi-alpha across all 62 extracted files.

**THE REAL ROLLERBALL, AT LAST.** nfrb_0..3 — the authored sphere at four charge stages. This
replaces fball_ which replaced the recoloured helix-mass: three generations, and only now is it the
art that was actually drawn for it. Plus 12 debris shards sliced out of the field sheet by
connected-component size.

**CHARGE RING — BUILDS, THEN HOLDS. NO SPINNING.** Four authored frames that grow around the hull
(0 -> 1 -> 2 -> 3 as the charge rises), then hold by alternating the last two while the jet glows,
exactly as specified. The old orbiting-circle path is gone entirely rather than left as a fallback,
because a fallback would eventually be what someone sees. Maverick gets the SAME four frames
palette-swapped to neon green (nchgM_), so both pilots read as the same mechanic.

**FALVA'S WEAPON RULES.** Her helper balls fire STRAIGHT lasers only — the alternating spread burst
is removed. And the rollerball is now EXCLUSIVE: while it is equipped pShoot returns immediately,
so she has no primary, no spread, no laser. Verified end to end: 3 shots without the ball, 0 with
it.

**ALSO IN:** Lizzie and Falva portraits, 7 emotions each (idle / smile / anger / laugh / sad /
victory / crash), and 24 thruster frames — 6 types x 4 — ready to overlay on the flameless
airframes wired last drop.

**A REGEX THAT CUT THROUGH A FUNCTION.** Removing the spread path with a line-matching regex took
16 lines including structural braces and left two orphaned blocks plus an extra brace. node --check
caught it immediately; repaired by reading the function and editing it deliberately. Second time
this session a blanket pattern has damaged code that a targeted edit would have handled cleanly.

---

## DROP 0724ce — ASSET RESTRUCTURE

Build: 1368 assertions, 0 errors. Manifest 7012 keys, 0 broken paths.

**bosses_new WAS NOT DEAD — IT WAS THE ACTIVE BOSS ART.** Mike asked me to delete the folder. It
held 67 keys and NOT ONE is referenced by a literal, so a naive check would have called it unused
and thrown it away. Every family is addressed by CONCATENATION: chopper_idle_N, tankboss_fire_N,
fboss_death_N, iboss2_atk_N. Deleting it would have removed the stage-1 chopper, the tank boss and
two others. The folder NAME was the problem, not the contents — merged into enemies/boss along with
the old bosses/ and enemies/bosses/ folders, so there is now ONE boss location holding 143 files.

**170 LOOSE SPRITES FILED.** assets/enemies/ had ~160 PNGs sitting directly in it beside the proper
subfolders — that is the disorganisation Mike pointed at. Filed by what they ARE:
    aircraft 36   boats 28   drones 24   gunships 24   tanks 34   turrets 12   scenery 12
Nothing is loose any more, and the trt_ set went to drones/ — matching the code, where t1-t6 are
classed as drones rather than turrets. The folder now tells the truth about the classification.

**FONTS.** One folder per stage under fonts/stages/ (1,3,4,6,7,8,9 — stages 2 and 5 use atlas
fonts). And fonts/gamefont/ holds the 95-glyph ASCII 32-126 set recovered from the world map, which
is the fullest we own — stage 1 has 58 and every other stage font has 46.

**88.4 MB REMOVED.** 265 files with no manifest reference at all, moved to _unused/ rather than
deleted and excluded from the shipping zip.

**THE ASSERTION THAT MADE ANY OF THIS SAFE:** every one of the 7012 image paths must resolve after
the move. Restructuring an asset tree by hand is exactly the kind of change that breaks silently
weeks later; with that check it either passes or it names the file it broke. It is now permanent,
along with checks that bosses_new stays gone, that nothing sits loose in enemies/, and that trt_
stays filed as drones.

---

## DROP 0724ce — STAGE 6 ENVIRONMENT + SECTIONAL COMBAT RULES

Build: 1350 assertions, 0 errors.

**THE STAGE-6 ART WAS REGISTERED AND NEVER DRAWN.** The 640x960 sky plate and all eight authored
cloud types came in with the Heavy Turbulence pack and went straight into the manifest — while the
stage kept running a two-colour gradient and ten procedural circles. That is the "old stage
graphics" exactly. Now: the sky plate scrolls as a real parallax bed, with a seeded cloud system at
two depths — high-altitude banks drifting slowly behind the fight, low rolling banks and storm
cells sweeping faster in front.

**EACH SECTION OWNS A FIXED SHARE OF THE BOSS.** Even split across the parts, so destroying every
section kills the boss with NO hidden remainder. Honest arithmetic: 5 parts = 20%, 6 = 16.7%,
7 = 14.3%, 8 = 12.5%. Mike asked for 15-20%; the larger bosses land slightly under, and that is the
direct consequence of the sections summing to exactly 100%. Reported rather than weighted to hit a
number.

**A HOLE IS A HOLE.** My first version only considered LIVING parts when routing a hit, so shooting
the gap where a wing used to be silently rolled the damage onto a neighbouring section — the exact
behaviour Mike asked to prevent. It now finds the closest section INCLUDING destroyed ones: if the
nearest thing to the shot is already blown off, the round passes through empty air and does
nothing. The test caught this; my own assertion text had claimed it worked.

**DESTROYED SECTIONS DISAPPEAR.** They used to keep drawing their 'destroyed' frame, which on a
shared canvas reads as a SQUARE of the boss changing rather than a wing coming off. A dead section
now stops drawing entirely and smoke + fire mark the stump, so the silhouette actually loses that
piece.

**BULLETS PIERCE SECTIONAL BOSSES.** A boss built from separate wings and engines is a frame of
pieces, not a solid wall — shots pass through and can strike more than one section on the way, each
hit routed to the section it passed through. Gated behind _armored / _shielded flags for units that
should stop them; nothing carries those yet, the hook is ready.

**STILL OPEN on Mike's stage-6 list:** the invisible-bullet deadzones, removing the shootable
objects, enemy plane facing, the boss facing, and the nuke section rebuilt as a parallax approach
(small under the player -> large threat coming at us) on a high-speed scroll.

---

## DROP 0724cd — STAGE CARDS: THE MAGENTA IS GONE

Build: 1333 assertions, 0 errors.

**FIFTEEN ASKS, AND I HAD NEVER ONCE SCANNED THE STAGE CARDS.** Every previous chroma sweep ran
over families I went looking for — ship sprites, boss frames, explosions, helix art. The cards are
keyed `scard_1..8` and none of my scans ever matched them. I was cleaning the game repeatedly and
never touching the thing being reported.

**WHY THE USUAL TEST DID NOT APPLY.** These are full-bleed 800x480 images with no transparent
region, so the edge-halo test — magenta sitting against transparency — has nothing to measure. A
different discriminator was needed, and the data gave two:
  BLOB SIZE   median blob was 1.0 PIXEL on every card. Scattered single-pixel specks are
              anti-aliased fringe; authored detail is never one pixel repeated hundreds of times.
  GREEN       residue is the key colour darkened by blending, so green sits near ZERO —
              (90,0,85), (51,2,53), (83,0,90). Authored violet carries real green: stage 5's
              nebula measures (146,93,232) and repeats across large contiguous regions.
Removed anything with green under 25 in a blob under 400px. Result:
    stage 1  816 -> 0      stage 5  8580 -> 5972 (authored nebula kept)
    stage 2   21 -> 0      stage 6   650 -> 21
    stage 3   14 -> 0      stage 7   254 -> 0
    stage 4  716 -> 0      stage 8   237 -> 0
SEVEN OF EIGHT CARDS ARE NOW COMPLETELY FREE OF MAGENTA. 5,457 pixels removed. Originals kept in
assets/fx/_scard_before/ so any of this is reversible.

**THE REAL LESSON, AND IT IS NOT ABOUT COLOUR.** Every time Mike reported halos I scanned whatever
I had scanned last and reported it clean. The scan was honest; it was aimed at the wrong assets. A
sweep that does not enumerate what the USER is looking at can pass forever while the bug sits in
plain sight. I should have asked which screen he was on the first time, not the fifteenth.

---

## DROP 0724cc — EVERY HUD BAR IS SCREEN-FIXED

Build: 1322 assertions, 0 errors.

**THE CAUSE WAS THE COORDINATE SPACE, NOT THE POSITIONS.** Everything in the play field is drawn
inside `ctx.translate(-camX, 0)` so the world scrolls under the player on the 800px-wide stages.
The miniboss HP bar, the special meter and the missile meter were all drawn inside that SAME
transform — so they scrolled with the world and drifted off centre the moment the player moved
sideways. Their maths was already VW/2-centred and correct; they were just being centred in the
wrong space.

**ONE WRAPPER, NOT FIVE FIXES.** screenBar(fn) cancels the camera for the duration of one draw.
Measured: at camX 0 / 80 / 160 / 240 / 320 the net screen offset is 0 every time, and on a
non-scrolling stage it applies no shift at all — which matters, because a blanket +camX would have
pushed the bars the wrong way on the six stages that do not scroll.
Applied to all four in-world bars, and drawHealthBarV2 now pins ITSELF so no future caller has to
remember which space it is in. That is the part that stops this recurring: a new bar added tomorrow
is correct by default rather than correct only if someone remembers the rule.

The boss bar was already fine — it draws on the HUD canvas, which is outside the world transform
entirely.

---

## DROP 0724cb — PROGRESSION, MINIBOSS FLASH, THRUSTERS, CHAIN TARGETS

Build: 1314 assertions, 0 errors.

**THE GAME ENDED AT STAGE 5.** patches.js: `if(run.stage>=5){ triggerVictory(); }` — a leftover
from when only five stages were built. gamecode.js already used `run.stage>=STAGES.length`
CORRECTLY; the patched override did not, and the override is the one that runs. Fifth time that
file has held the losing copy of something. Now driven off the stage table, so adding a stage
cannot desync it again. Clearing 6 continues to 7.

**MINIBOSS HIT FLASH — drawSubBoss HAS SEVERAL DRAW BRANCHES AND ONLY SOME TINTED.** The level-1
crawler took one that did not, so it never lit up however hard you shot it. Verified the state was
never the problem: a real 3-second burst took it 225 -> 131 hp with flash sitting at 0.12. Fixed
with ONE guaranteed pass at the end of the function, using the key whichever branch actually drew
with — so it covers every branch including any added later. Flash held 0.12 -> 0.18 so a single hit
registers. All three stages verified.

**THRUSTERS — I HAD THIS INVERTED AND HAVE NOW MEASURED ALL NINE.** In 0724bn I switched to the
plain sprite because it had more tail pixels, concluding it carried the baked flame. It does — but
Mike wants the OPPOSITE: the flameless airframe, so the thruster can be animated separately.
    plain vs _t tail pixels:  maverick 6337/1509  juggernaut 4929/1298  falva 3641/820
    cole 5946/3847  axel 4975/1501  decker 4007/1434  freezer 4616/2502  yuri 4399/2520
    lizzie 2342/2025
_t is the stripped airframe on EVERY pilot, and every pilot has one. Now drawing _t with our own
ntr_ thruster, pilot-tinted and throttle-reactive, drawn BEFORE the hull so the plume comes from
behind the tail. Nothing stacks, because the airframe has no flame of its own.

**CHAIN LIGHTNING NO LONGER EATS PICKUPS.** It treated floating powerups and missile pickups as
valid arc targets and destroyed the things the player was flying over to collect. Hostiles only.

**A BLANKET REGEX THAT BROKE THE BUILD.** My first flash fix inserted `b._lastKey=key` at every
`XART.get(key)` in the file — 21 sites, most in functions with no `b` in scope, and bakeGlow threw
immediately. The test suite caught it on the next run. Reverted and re-applied INSIDE drawSubBoss
only, by locating the function and patching within its own body. Never run a project-wide regex for
a change that belongs to one function.

---

## DROP 0724ca — WHY THE EXPLOSIONS NEVER "COVERED" ANYTHING

Build: 1300 assertions, 0 errors.

**EIGHT REPORTS, AND THE SIZE WAS NEVER THE PROBLEM.** I scaled the blast, normalised it per
family, measured the coverage at a consistent 1.38x — and Mike still said deaths were not covered,
because TWO OTHER THINGS WERE DRAWING ON TOP OF THE EXPLOSION:

    fadeOuts    kept drawing the WRECK for a further 0.5s at declining alpha. The explosion peaks
                early and fades from 65% of its life, so the sprite was visible underneath it and
                then ALONE after the fire had gone. No blast size can hide a sprite that outlives
                it — I could have scaled it to 10x and the wreck would still have faded out in
                plain view afterwards.
    legacy      mgturret and rockturret ALSO fired a 4-frame turret explosion in addition to the
                class one, so those units detonated twice. That is the oversized level-1 turret
                death exactly as reported.

Both removed. A unit now stops drawing the instant it dies and the class explosion carries the
whole death. Measured on mgturret, rockturret, tank and microturret: 1 explosion, 0 legacy anims,
0 lingering wrecks.

**THE LESSON I SHOULD HAVE DRAWN FIVE DROPS AGO:** "the explosion does not cover the death" is a
statement about the WHOLE death sequence, not about the explosion. I read it as a sizing complaint
every single time and measured only the thing I had already decided was at fault. The wreck
outliving the fire was visible in any frame of the footage.

**STATS SCREEN RE-FLOWED.** The portrait sat at y=96 while the COMBAT STATS header occupied ~44
plus its own height — they overlapped, and the pilot name landed on the header. Seven rows at a
38px pitch ran to y=368 with a bar under each, pushing the last rows and the password off the
panel. Bars also ran 20px from each SCREEN edge, which is outside the authored 640x480 window, so
they crossed its frame on both sides.
Portrait moved to y=128 and shrunk, rows start at 186 with a 31px pitch, bars inset to the panel
margin. Asserted the whole block fits with 124px clear for the password.

---

## DROP 0724bz — FALVA'S BALL IS HERS AGAIN

Build: 1291 assertions, 0 errors.

**THE RELEASED BALL WAS MAVERICK'S HELIX-MASS RECOLOURED PINK.** The code said so itself:
    // DROP 0720: rebuilt FALVA rollerball from VFX v2.2 helix-mass (recolored pink), 12 frames.
And it was drawn FIRST, with her own authored art sitting underneath as the fallback — so her real
ball has never once been on screen.

**THE MEASUREMENT THAT SETTLED IT:**
    nrb_    208x384   15 unique colours across the entire sprite
    fball_  183x192   16,194 / 18,280 / 18,483 / 18,552 unique colours per frame
Fifteen colours is a flat posterised tint. Eighteen thousand is authored artwork. On top of that
fball_'s four frames BRIGHTEN in sequence (mean 123 -> 176 -> 202 -> 219) — the ball visibly spins
up, which is the behaviour a charge release should have.
Priority swapped: fball_ first, nrb_ kept underneath as the fallback rather than deleted.

**A CLAIM I NEARLY MADE AND CHECKED INSTEAD.** nrb_0 and nrb_4 have identical opaque counts and
identical colour counts, and I was one sentence from writing that the 12 frames were duplicates.
They are not — frame-to-frame difference is 25-37, a genuine rotation. A rotating sprite preserves
both of those statistics exactly, so the coincidence meant nothing. The unique-colour count was the
measurement that actually distinguished the two assets; the opaque count never could have.

---

## DROP 0724by — EXPLOSION COVERAGE NORMALISED PER FAMILY

Build: 1285 assertions, 0 errors.

**THE SWAPS:** tank <-> boat and crate <-> mboat, secondaries moved with them.
    tank  nxp_smoke  / nxp_radial      boat  nxp_upward / nxp_clus
    crate nxp_radial / nxp_clus        mboat nxp_clus   / nxp_radial

**AND THE REAL REASON SOME LOOKED OVERSIZED.** Mike said they looked large but wanted them to cover
the sprite. Measuring found the actual problem: THE FAMILIES DO NOT FILL THEIR OWN FRAMES EQUALLY.
Across all 8 frames of each set the visible blast spans
    ring 0.75  white 0.76  radial 0.77  clus 0.81  barrage 0.81  dense 0.82  upward 0.86  smoke 0.89
of the frame. So under one global multiplier a ring death covered 1.21x the unit while a smoke
death covered 1.44x — a 19% swing caused purely by transparent padding in the ART, not by any
setting. That is why some deaths read "about right" and others read too big, and why no single
number could ever fix both.

EXPLODE_FILL now holds each family's measured span and the draw divides by it, so every class lands
on the SAME visible coverage whatever art it uses. Measured spread across crate/drone/turret/jet/
tank: 0.000.

**COVER_TARGET = 1.38x** the unit for fodder — the fireball comfortably hides the sprite vanishing
underneath (the point Mike actually raised) with a margin either side, without swamping neighbours.
**COVER_TARGET_BIG = 1.62x** for bosses and minibosses, because a set-piece death should not read
the same size as a drone. Measured: magma colossus 269px hull -> 435px visible blast.

The class now rides on the explosion object so the draw knows which target to use — previously
there was no way for a boss blast to be treated differently once it left unitDeathFX.

---

## DROP 0724bx — RETINA SOUND RESTORED, SECTIONAL DEATH ART, ASSET SWEEP

Build: 1277 assertions, 0 errors. Manifest 7390 -> 7012.

**RETINA SOUND RESTORED.** The space pack re-pointed the retina lock at nsp_scanner_sweep, which is
a completely different cue. The original retina_charge.mp3 was still on disk untouched — registered
under its own key and cycleLock() plays it again. lockAlert also restored to its own original file
rather than the space-pack nav_lock.

**BOSS 2/3 DEATH FRAMES WERE REVERTING TO THE OLD ART, AND HERE IS WHY:**
    if(boss && boss.modular && !boss.dead){ drawModularBoss(boss); ... return; }
Gated on !boss.dead. The instant a sectional boss died it fell OUT of the modular path and
drawBossSprite picked up the legacy body art (mba_mc / mba_cb _ruin) — the old boss, exactly as
Mike described. A sectional unit already HAS its death art: every component's 'destroyed' state.
It now keeps drawing its own parts through death, and once the unit is dead every remaining
component reads DESTROYED, so the wreck looks like a wreck rather than a healthy hull missing an
arm.

**ASSET SWEEP — 378 KEYS, 4.4 MB.** Files moved to _removed_assets/ rather than deleted.

**AND THE SWEEP IS WHY THE TEST SUITE EARNS ITS KEEP.** My first pass flagged 934 keys across 206
families as unreferenced, using a family-level scan of the built game.js. Removing them broke FOUR
assertions immediately: the lava and icewater liquid frames and the level-6 jet reels are addressed
through CONFIG tables, not string literals, so no source scan could ever see them. Restored all 934
from the shipped zip, then removed families one at a time keeping only those that left every
assertion green. Verified afterwards that zero remaining manifest keys point at a missing file.
Without those assertions I would have shipped a build with the liquids and the L6 jets gone.

---

## DROP 0724bw — BOOT PLATE UNCROPPED, OLD INTRO REMOVED

Build: 1276 assertions, 0 errors.

**COVER WAS EATING 430 PIXELS OF THE LOGO.** I fitted the 1672x941 boot plate with COVER, which
fills the viewport by CROPPING. In a 480x512 window that draws it at 910x512 and throws away 430px
of width — most of the hangar and a good part of the ColeForge mark with it. Measured:
    COVER    910x512   430px cropped horizontally
    CONTAIN  480x270     0px cropped, 242px letterbox
Switched to CONTAIN. Aspect was never the issue — both preserve it. The difference is WHAT gets
sacrificed: cover sacrifices the image, contain sacrifices empty screen. For a logo plate the image
is the whole point.

**THE OLD SPACE BOOT IS GONE.** Removed the starfield tile from the press-start gate, the assembled
ColeForge text, and the star-tile parallax from the boot body. The press-start gate now shows the
same new plate at 85% alpha, so the sequence is one continuous image rather than two different
intros stitched together.

**A DANGLING BLOCK I CAUSED AND CAUGHT.** My first removal cut the star-tile if-block but left its
trailing `restore(); } else { ... }`, producing a syntax error. node --check caught it immediately
— which is exactly the check that could NOT have caught the dead-switch regression in 0724bb,
because that one was valid JavaScript. Different failure, different net.

---

## DROP 0724bv — STAGE-CLEAR WINDOW + BOSS BARS v2

Build: 1274 assertions, 0 errors. Manifest 7007 -> 7390 (+383).

**THE BOSS BAR ART WAS ALREADY IN THE BUILD AND COULD NEVER APPEAR.** patches.js already had a v2
bar path, guarded like this:
    const _bfk='nbb'+_bst+'_frame', _bik='nbb'+_bst+'_fill_'+(...)
The shipped pack registers as `nbb_frame_<N>` and `nbb_fill_<N>_<f>`. The keys never resolved, the
guard always failed, and it fell through to the legacy gradient bar every single time. Not a
missing asset, not a missing feature — a NAMING MISMATCH between the loader and the pack, silently
swallowed by a defensive `if(XART.rdy(...))`. Exactly the same failure shape as the Audio.SFX
whitelist: the safety guard is what hid it.

**PER-STAGE THEMED BARS, NOW LIVE.** All 8 stages have their own boss AND miniboss bar — frame,
segment overlay and an 8-frame animated fill, plus authored critical-pulse overlays. The fill is
CLIPPED to the health fraction rather than scaled, so the gauge drains like a real instrument
instead of the artwork squashing horizontally.

**STAGE-CLEAR WINDOW.** The authored 640x480 stats window now draws on the stage-clear screen with
the animated COMBAT STATS header above it. Applied to patches.js directly — drawStageClear is
defined in BOTH files and patches wins, which is the FOURTH time that file has taken an edit I
made to the losing copy. I checked first this time.

**383 KEYS**, alpha variants only (every asset ships alpha and chroma; alpha has no key to strip).
Magenta classified before touching anything: 64,792 px is legitimate body colour on the bars and
was left alone; only 9 assets carried a true edge halo, healed 5,508 -> 9.

**ALSO REGISTERED, NOT YET DRIVEN:** the full player stat-bar kit — 8 stats x 3 sizes x 8 fill
frames, with frames, segments and labels. That is the material for a proper equipment/stats
readout whenever we want one.

---

## DROP 0724bu — THE SEVENTH EXPLOSION REPORT, AND WHY

Build: 1261 assertions, 0 errors.

**I HAD THE RULE BACKWARDS.** Mike has said "scale the explosion to the enemy unit" seven times. I
read that as MATCH the unit and set EXPLODE_SCALE to 1.0 in 0724bk — measured, asserted, and
wrong. The rule is that the blast is SIZED FROM the unit and reads LARGER than it. At 1.0 every
death looked weak, which is why the report kept coming back even after the measurement said the
numbers were perfect.
EXPLODE_SCALE=1.62, scatter widened to 0.34 of the hull. Measured on real kills: 44px jet -> 71px
blast, 43px tank -> 70px. Scales with the unit, draws bigger than it. Assertions inverted to demand
ext > w*1.35 rather than ext <= w*1.05.
The lesson is not about explosions. Six of those seven fixes were correct code changes to the wrong
target because I never checked I had understood the RULE, only that I had implemented my reading of
it. A measurement can only confirm the thing you decided to measure.

**DAM SWAP WAS MOVING THE CAMERA.** `damBroken=true; mapScroll=0;` — that snapped the view to the
TOP of the level at the exact moment the boss died, so the broken-dam art appeared nowhere near
where the fight happened. The swap is an ART change, not a camera move. mapScroll now untouched.

**NOTHING DRIVES OUT OF THE DAM.** Ground units still mid-approach when the stage-1 boss engages
are now cleared with a proper death, because the level has stopped at the wall and a tank rolling
on would be driving out of solid concrete.

**STAGE AMBIENCE OFF.** The beds sat under the music at 0.55 and muddied it. Disabled behind
AMBIENCE_ON=false — intact, not deleted.

**CAMPAIGN MUSIC RESTARTS ON RE-ENTRY.** Deploying calls Audio.stopMusic(), and the map only ever
started its track during the first boot sequence — so coming back after clearing a level left it
silent.

**JUNGLE WAS SMOKING BECAUSE OF THE SPRITE I CHOSE.** The 'leaf' effect used nx_small — an
explosion spark — at 9% of the region width, tinted green. Scaled up that reads as haze drifting
off the jungle, which is exactly what Mike saw. Now 3% of region width, faster, source-over, low
alpha: specks catching light. Verified by sampling the map pixels that stage02 IS the volcano, so
the smoke was always on the right region — it was the JUNGLE effect that looked wrong.

**STILL OPEN:** stage-clear menu, and scaled jets orbiting level 4.

---

## DROP 0724bt — THE LIVE CAMPAIGN WORLD MAP

Build: 1245 assertions, 0 errors. Manifest 6856 -> 7007 (+151).

**THE NEW PLATE IS IN, AND IT IS THE CLEAN ONE.** The pack ships three maps: a 1448x1086 master, a
640x480 runtime master, and a region-GUIDE with the boundaries painted on. Compared them directly —
the guide differs from the master by 12,593 px, and that difference IS the overlay. Took the clean
runtime master; asserted the manifest path contains no 'guide'.

**REGION SELECTS SHOW THE ENTIRE OUTLINE.** The reels are FULL-CANVAS 640x480 overlays
position-locked to the master (the pack's own coordinate_policy says so), so drawing one at the
map's own rect shows the whole territory boundary with no crop, no offset maths and no clipped
edges. 40 frames, 10 regions x 4, all registered and following the cursor.

**AND THE MAP BREATHES.** Every territory runs its own ambient effect, built ENTIRELY from art the
game already owned — nothing new was needed:
    stage 2 volcano      smoke rising off the caldera        (nx_smoke)
    stage 6 turbulence   storm cells rolling across          (nl6c_low_rolling_bank)
    stage 3 ice shelf    drifting snow                       (nwf_snowB)
    stage 1 jungle       drifting foliage                    (nx_small, green-tinted)
    stages 4/5/8 + hub   embers rising, tinted per territory
Each effect is scaled to its OWN region's width and height and anchored to its polygon centroid, so
nothing is hand-placed and a region can be moved by editing the JSON alone.

**A GLOBAL I ALMOST REASSIGNED.** My first version set VW=640 temporarily so the FX helper would
read the right frame. VW is a const — that would have thrown every frame the map was open, and the
frame guard from 0724bi would have swallowed it into a blank map. The helper now takes the frame as
a PARAMETER, which is what it should have been. Asserted that it never reassigns a global.

**Also registered but not yet driven:** the 8-state perimeter (dormant -> power -> charge -> scan
x3 -> lock -> selected), the region focus and dialogue windows, and the 94-glyph world map font.

---

## DROP 0724bs — SECTIONAL SUB-BOSSES IN PLAY

Build: 1225 assertions, 0 errors.

**STAGES 2 AND 3 NOW FIELD THE REBUILT SUB-BOSSES.**
    stage 2   OBSIDIAN DRILL TANK     (was CRIMSON TALON)     6 components
    stage 3   GLACIER RAIL FORTRESS   (was ENERGY CORE)       6 components
Both are TRACKED GROUND VEHICLES, flagged _tracked + ground, so they inherit the drive-and-stop
movement from 0724ay rather than bobbing on a sine — which is what these units need, since both
have visible tracks in the art.

**POSITIONAL DAMAGE WORKS ON SUB-BOSSES TOO.** hitSubBoss routes each impact to the nearest
component. Verified through the real hit path: shooting the left track destroys the left track, the
right track survives, and the hull keeps fighting. All 48 sub-boss part-states registered.

**A FLAKY TEST FIXED RATHER THAN IGNORED.** The road-tank patrol assertion failed in this run and
passed on the next three. The tank starts at a random point on the road heading a random way, and
900 frames was not always a full patrol leg — so it failed intermittently on CORRECT behaviour.
Extended to 2400 frames, now 4/4 stable. A flaky assertion is worse than no assertion: it trains
you to ignore failures, and this suite is the only thing standing between a change and a broken
build.

---

## DROP 0724br — SECTIONAL BOSSES + LEVEL 6 ENVIRONMENT

Build: 1186 assertions, 0 errors. Manifest 6016 -> 6856 (+840 across both packs).

**THE SECTIONAL DESTRUCTION SYSTEM — the thing the old modular bosses could never do.**
Four units rebuilt with PER-COMPONENT damage:
    magma_colossus        L2 boss      7 parts
    cryo_behemoth         L3 boss      8 parts
    obsidian_drill_tank   L2 sub-boss  6 parts
    glacier_rail_fortress L3 sub-boss  6 parts
Every part carries intact / damaged / critical / destroyed — 108 part-state combinations, all
registered. Plus idle reels, destructive-swap and destruction-overlay animations, and each unit's
own primary and special projectiles.

**DAMAGE IS POSITIONAL.** sxHit() routes each impact to the component NEAREST the hit, so shooting
a wing breaks THAT wing. Verified: concentrated fire on the left wing destroys the left wing, the
right wing stays intact, the core survives and the boss keeps fighting with a wing gone. Parts walk
intact -> damaged -> critical as they are worn down, and a destruction overlay plays on the part
that just died. Core parts (head/torso/hull) carry ~2x the health of limbs, so losing an arm is a
setback rather than the end of the fight.

**LEVEL 6 ENVIRONMENT:** 8 cloud types x 6 frames (thunderhead, storm vortex, rain, heavy rain,
speed wisps, low rolling bank, high-altitude bank and stack) plus the 640x960 scrolling sky plate.

**KEY BLEED HEALED ON ARRIVAL.** 11,608 -> 11 magenta px across 124 assets. Every one measured
100% ON THE TRANSPARENT EDGE with ZERO body magenta, so the classification was unambiguous — no
judgement call needed, and no legitimate colour at risk.

**A TEST THAT PROVED NOTHING.** My first version fired 400 hits of 50 damage at one wing. That
destroyed the wing and then kept going into whatever became nearest, killing the whole boss — so
the assertion "the right wing is untouched" failed on CORRECT behaviour. Bounded to exactly that
part's health, it now tests what it claims to.

---

## DROP 0724bq — LEVEL 6 EXPANSION: 558 KEYS, AND THE SECTIONAL SYSTEM ARRIVES

Build: 1192 assertions, 0 errors. Manifest 6016 -> 6574.

**SIX FIGHTER FAMILIES, SEVEN AUTHORED STATES EACH** — storm talon, tempest fang, cyclone widow,
cloud raptor, thunder lance, hurricane warden:
    idle 6f   bank-left 5f   bank-right 5f   damage 3f   destruction 8f   homing-launch 8f
    reload 6f
Wired so STATE FOLLOWS BEHAVIOUR: banking reads lateral velocity, damage reads HP, launch and
reload read the unit's own weapon cycle. The animation cannot disagree with what the unit is doing,
which is the failure mode that has bitten this codebase repeatedly. Asserted every transition
individually and confirmed all 6 x 41 frames resolve. Six new waves added to the stage-6 plan
BETWEEN the existing ones, not replacing them.

**THE SECTIONAL DESTRUCTION ART IS HERE.** This is what Mike asked for back in the Contra III
conversation: "cutting up the boss into sectional frames like arms, legs, body, head, wings, and we
can attack those sections separately, and blow them up."
    Skyhammer Rocket Fortress  320x320, 7 components
    Thunder Lance Rocket Jet   256x256, 7 components
    Tempest Missile Wall       640x192, 5 wall modules + 2 turrets with FOUR FACINGS each
Each component carries intact / damaged / critical, and each DETACHABLE one carries a six-frame
body breakup, a six-frame explosion and a six-frame smoke loop.

**THE DESIGN DETAIL THE TEST CAUGHT:** seven components, but only SIX are detachable. The core
fuselage has its three state layers and NO death reel — the pack ships no Section_Death for it at
all. That is correct: the core IS the hull, so it does not blow off; when it goes the unit goes. My
first assertion assumed all seven were detachable and failed. Verified against the source (zero
core_fuselage death files) rather than assuming the pack was incomplete.

**POSITION LOCK VERIFIED.** component_map.json: "All component layers are full-canvas and
position-locked. Draw at identical boss x/y." Asserted that every layer of a set-piece shares ONE
canvas size — sky all 320x320, tlj all 256x256 — so that rule can actually hold. Geometry comes
from the art, not from offsets I invent.

Pack arrived clean: 0 magenta, 0 semi-alpha across all 558 files.

**NEXT:** wiring the set-pieces themselves — per-section HP, hit routing to the right component,
and blowing a section off with its own reels while the rest of the unit keeps fighting.

---

## DROP 0724bq — RECOVERED STAGE FONTS + COLEFORGE BRAND PACK

Build: 1175 assertions, 0 errors. Manifest 5820 -> 6016 (+196).

**THE MISSING STAGE FONTS ARE BACK — THE ORIGINALS, NOT SUBSTITUTES.** Stages 6/7/8 plus the bonus
stage 9 each shipped a 13x4 atlas at 96px cells with an explicit JSON glyph map, so no cell order
had to be guessed. 46 glyphs each, 184 sliced in total, ZERO empty cells.
Took the ALPHA atlas rather than the chroma one — the pack ships both, and the alpha version has no
key to strip and therefore no halo to create. Verified 0 magenta on all four.
fontGlyph() now prefers the stage's OWN recovered glyph, with the stage-1 fallback still underneath
for any character none of them carries. Stage 6 resolves sfont6_H instead of falling back.

**COLEFORGE BRAND PACK, 12 keys.**
  cf_boot     the new 16x9 hangar boot plate
  cf_logo     Phoenix Engine logo
  cf_sdk      SDK splash        } stored under assets/sdk/ for the Phoenix Engine SDK,
  cf_banner   3x1 wide banner   } the editor shipping alongside the game
  cfic_*      4 badge icons sliced from the 2x2 sheet — shield, star, wings, radar
  cfui_*      4 UI frames sliced from the 2x2 sheet — banner, panel, small, bar

**BOOT SCREEN REPLACED.** COVER-fitted, never stretched: a 16:9 plate scaled into a 480x512
viewport has to be cropped, not squashed. Fades in, holds and fades out on the EXACT timeline the
old assembled-text intro used, so the chime and the hand-off to the title screen are untouched.

**AND I ALMOST SHIPPED IT INTO THE WRONG FUNCTION.** drawBoot is defined in BOTH gamecode.js and
patches.js, and patches wins. My first edit went into the losing copy — the assertion caught it,
exactly as it did for drawPassword and drawOptions before. Third time this file has bitten; the
lesson holds: when a change appears to do nothing, check whether patches.js overrides it.

**CREDITS** now carry the Phoenix Engine logo, a bobbing row of the four badges, and a cfui_panel
plate behind the text block.

---

## DROP 0724bp — DRONE CANNON ATTACHMENTS

Build: 1140 assertions, 0 errors.

**THE wab_/wam_ SETS ARE MODULAR WEAPON MOUNTS, NOT TURRETS.** Mike: cannon attachments for drones.
Two configurations, exactly as specified:
    SINGLE   baseplate (wab_) + one centred barrel (wam_)
    TWIN     two mirrored barrels, NO baseplate — the Metal Slug look
Five weapons, each already having its projectile wired in FIRETYPES:
    chaingun->chaingunT  minigun->minigunT  railgun->railshot  rocket->rocketW  tesla->teslaW

**DRAW ORDER MATTERS AND IS DELIBERATE.** The baseplate draws UNDER the hull so the drone sits ON
its mount; the barrels draw OVER it, in their own transform so the sprite's translate/rotate does
not apply to them. Muzzle flash fires from each barrel independently.

**AIM IS CLAMPED TO +/-0.55 RAD.** Measured first: every one of the 10 parts runs content to all
four canvas edges with zero margin, so a freely-rotating barrel would clip its own corners. The
cone keeps the rotation inside what the art can survive. If we ever want full traverse, the parts
need re-exporting with margin (or padding at load) — noted rather than bodged.

**A TEST THAT READ ZERO ON A WORKING WEAPON.** My first assertion checked eBullets.length after
3 seconds and reported 0 shots. The drone had been firing the whole time — bullets fly off screen
and get culled, so the final frame said nothing about whether it ever fired. Now counts shots AS
THEY ARE FIRED. Sampling the end state is not the same as measuring the behaviour.

---

## DROP 0724bo — TURRETS ARE NOT DRONES

Build: 1129 assertions, 0 errors.

**THE SIZE INCONSISTENCY HAD A CAUSE, AND IT WAS CLASSIFICATION.** The art pools mixed them:
    TURR_MG=['trt1','trt3','esturret1']   TURR_RK=['trt4','trt2','esturret2']
    TURR_G =['trt5','trt6','trt1']        microturret=['esturret1','esturret2','trt1']
So a single 'turret' spawn came out as EITHER a trt_ unit or an esC emplacement — completely
different art with different silhouette coverage inside the same 128px canvas, at the same
footprint multiplier. That is why some turrets looked bigger than others: they were not the same
kind of thing. Mike: "t1 t2 t3 t4 t5 t6 are drones."
Turret roles now draw ONLY the real emplacements (esC_turretC2, esC_turretC4, esA_navalturret).
The trt_ sets are now drone art, wired to turdrone, shieldd, drone, mdrone and minidrone.

**UNIFORM TURRET SCALE.** TURRET_FOOT=1.95 applies to every turret emplacement regardless of which
art it drew, so two turrets side by side are always the same size on screen. Everything else keeps
the general ENEMY_ART_FOOT.

**NO MORE DEATH FRAMES.** Each turret had exactly ONE death frame — a static pose that cross-faded
out underneath the explosion and only muddied it. A dying unit now stops drawing its sprite
entirely and the class explosion carries the whole death, which is what Mike asked for and is also
consistent with the unit-sized blast work from 0724bk/bl.

---

## DROP 0724bn — THRUSTER (MEASURED), L6 INTRO, STAGE FONTS

Build: 1120 assertions, 0 errors.

**THE THRUSTER — I HAD IT BACKWARDS.** Measured the sprites instead of guessing again:
    ship_maverick     tail-fifth 6337 opaque px
    ship_maverick_t   tail-fifth 1509 opaque px
The PLAIN sprite has the engine flame BAKED IN. The _t variant has it STRIPPED, so a separate trail
can be attached. My "STABLE AIRFRAME" fix chose _t and then drew an ntr_ trail on top — I was using
the flameless frame AND adding a flame, which is precisely the double-thruster Mike reported twice.
Now: level flight uses the IDLE sprite (ship_<pilot>) and the ntr_ overlay is REMOVED entirely.
Mike's exact words were "just animate those thrusters they already had" — the art does that alone.
Verified all 9 pilots have an idle sprite, so this holds for every character.

**LEVEL 6 INTRO.** ASSETS.stageArt only has entries for stages 1-5. curArt() returned undefined for
6, 7 and 8, so the intro card had nothing to draw from. Now falls back to stage 1's atlas —
those stages get a card in the base style instead of no card at all.

**STAGE FONTS 5-8.** All eight font atlases DO exist and load. The real gap: stage 1 carries 58
glyphs, every other stage carries 46 — the punctuation set (" # $ % ( ) * ; = @ \ _) is absent, and
a stage font missing a character drew nothing for it. Added fontGlyph(), which takes any glyph the
stage font lacks from stage 1's complete set. Verified all 11 missing punctuation glyphs now
resolve on stage 6.

**THE PATTERN AGAIN:** I fixed the thruster twice by adjusting offsets and alpha, without ever
measuring which sprite had the flame. Two minutes of measurement would have found it the first
time. Measure the asset before changing the code that draws it.

---

## DROP 0724bm — LEVEL 2 AND 3 BOSSES: THE ACTUAL REASONS

Build: 1114 assertions, 0 errors.

**LEVEL 3 — THE PHASE ART WAS DRAWING AND BEING COVERED.** I sliced the 5-phase sheet last drop,
wired cryoBodyDraw, and verified it returned true. It WAS rendering. Then drawModularBoss's parts
loop ran three lines later and painted the boss's own mba_cb art straight over the top. The new
body was correct and invisible — which is exactly why Mike saw no change at all.
cryoBodyDraw now RETURNS before the parts loop. The sheet contains the hull and its cannons, so
nothing else needs to draw. Asserted that the decision happens before the loop AND that it returns,
so nothing can paint over it again.

**LEVEL 2 — THERE IS NO MAGMA BODY ART, AND THE REAL DEFECT IS BRIGHTNESS.** The pack contains 16
PNGs: 12 chains, 2 cannon masters, 1 cryo phase sheet, 1 atlas. Its own recovery-audit.json states
png_count 16, status pass. There is no magma colossus body in it, and never was.
What IS measurably wrong is that the magma art in the game is far too dark: 51/255 against the cryo
behemoth's 135 from the same set — nearly 3x darker, on a stage whose background is bright lava.
Lifted by GAMMA rather than a flat multiply, so the darkest ink and the highlights both survive
instead of the sprite washing out: clean 51 -> 132, dam 41 -> 111, ruin 32 -> 92. The damage
progression is preserved and not one pixel changed alpha.

**WHAT I GOT WRONG BEFORE:** I reported "the phase sheet is wired" as if that meant it was visible.
Returning true from a draw function is not the same as appearing on screen. The assertion I needed
was about DRAW ORDER, not about the function succeeding — the same class of mistake as asserting a
function exists rather than that it is called.

---

## DROP 0724bl — THE STAGE END

Build: 1105 assertions, 0 errors.

**bossDie() DETONATED EVERY SURVIVING ENEMY AT A FIXED 38px.**
    for(const e of enemies){ if(!e.dead) explode(e.x,e.y,38,'red'); }
A 20px turret and a 58px hauler produced identical blasts — at the exact moment the player is
watching the level finish. That is why the stage end kept looking wrong no matter how many times
the per-kill paths were corrected: the end-of-stage sweep was a completely separate call that never
touched deathClassOf, never touched unitDeathFX, and never asked how big anything was.
Now routed through the same class death every other kill uses. Measured on a mixed field:
units [18, 43, 44] -> blasts [18, 43, 44]. Previously all three were 38.

**FIVE MORE FIXED-SIZE BLASTS TIED TO THEIR UNIT:** the boss transform (90 -> 55% of hull), the two
modular part hits (46/48 -> 22/24% of hull), the leviathan door (70 -> 30%), and the rival wreck
(70 -> 55%). Asserted that bossDie, modularHit and levDoorHit contain NO fixed-size blast at all.
Deliberately left alone: bombs, the atom blast, nukes, player-hit sparks and chain hits — those are
EFFECT sizes that belong to the weapon, not to a unit.

**SEVENTH TIME ON THIS BUG, AND THE REASON IT KEPT SURVIVING:** each fix targeted the path I had
just been shown. unitDeathFX, then the engine default, then disintegrate, then killEnemy, then
EXPLODE_SCALE — every one correct, none of them this. The lesson is to enumerate EVERY caller of
explode() and check each against the unit, which is what finally found it. That audit is now a
standing assertion.

---

## DROP 0724bk — THE SCAN THAT LIED, AND THE 558-ASSET HALO SWEEP

Build: 1097 assertions, 0 errors.

**MY VIDEO SCAN WAS WRONG AND I REPORTED IT AS CLEAN.** I extracted the footage with
`-vf scale=480:-1`. Downscaling INTERPOLATES: a 1px magenta rim gets averaged into its neighbours
and disappears completely. I measured 0.0% magenta across 299 frames and told Mike the chroma work
was holding. Re-extracted at NATIVE 1280x720 with nearest-neighbour: up to 3983 magenta px in a
single frame, 20 flagged frames in one video. The bug was always there; my instrument destroyed the
evidence before measuring it. Mike has now had to tell me this three times.

**558 ASSETS CARRIED A MAGENTA EDGE HALO.** 251,272 px -> 35,923. Families hit: nmt (104), mbv
(97), ship (76), nsw (50), nhb (33), nrh (32) and more — boss frames, ship sprites, water craft.
THE TEST THAT MADE IT SAFE: a halo is magenta sitting ON the transparent edge. Art that is
legitimately pink carries its colour in the BODY. Measured per asset before touching it —
nhxf_0 was 61% edge (halo, healed), nrb_0 was 27% edge (Falva's roller ball, LEFT ALONE).
Verified after: special_falva keeps all 38,039 pink px, card_falva 30,050, nrb_0 15,726.

**THE BLAST IS NOW EXACTLY THE UNIT.** EXPLODE_SCALE was 1.15, so every primary overshot by 15%
before the scattered secondaries were added on top — measured total cloud 1.16x to 1.49x the hull.
Set to 1.0 and the secondary scatter tightened from 0.45 to 0.26 of the hull. Measured on real
kills through killEnemy: mgturret 44->44, tank 43->43, racer 44->44, fang 44->44. Exactly 1.00x on
every unit type, asserted, so this cannot drift again.

**THE LESSON, AND IT IS THE SAME ONE.** Every time I have measured something and reported it clean,
I should have checked what my measurement could NOT see. A downscaled frame cannot show a 1px rim.
A bounding-box check cannot show a shape. A syntax check cannot show a dead switch. The instrument
has to be able to detect the failure, or a pass means nothing.

---

## DROP 0724bj — FALVA'S CHARGE WAS DEAD CODE

Build: 1086 assertions, 0 errors.

**MIKE'S HINT WAS EXACT.** "Falva's missing her roller ball charge ability." She was.
falvaCharge() was written. Her aura art (fchg_0..3) and orbiting roller-ball art (forb_0..11) were
registered. drawFalvaAura(), drawFalvaOrbs() and drawFalvaCharge() were all written and correct.
And NONE of it ran:
  · updateSpecial dispatched mavCharge(dt) for Maverick but had NO falva branch, so
    special.charging was never set
  · drawFalvaCharge() was defined and never called from anywhere
_falvaP() therefore returned -1 forever and every draw bailed on its first line. An entire pilot
ability sat dead, one line away from Maverick's working equivalent.
Both wired. Verified end to end through the real update: holding fire charges her, the charge
accumulates, _falvaP() reads positive, the orbs get a spin phase.

**AND IT EXPOSED A LATENT HARNESS BUG.** test_fl.js line 265 stubbed
`Input.down = k => (fire.includes(k) ? held : false)` where `held` was never declared. That threw
ReferenceError the instant anything called Input.down — and it had survived unnoticed for the
entire project BECAUSE Falva's charge was dead and nothing invoked it. Fixing her ability made a
year-old test bug fire immediately. Declared properly.

**VIDEO ANALYSIS.** Extracted 299 frames across 15 minutes of footage and scanned numerically:
zero magenta anywhere in gameplay (the chroma work is holding), and no sustained frozen sections
(the frame guard from 0724bi is doing its job). Also swept every modulo-indexed animation family in
the source against the manifest — no family requests a frame that does not exist.

**HONEST LIMIT:** I can extract and measure frames, but I cannot reliably read fine sprite detail
from downscaled video. The Maverick helix, boss and effect issues in Mike's hints need either a
still screenshot at native resolution or a one-line description of what looks wrong — otherwise I
would be guessing, and guessing is what has cost us the most time in this project.

---

## DROP 0724bi — THE LOCK-UP MECHANISM, AND THE GUARD THAT ENDS IT

Build: 1077 assertions, 0 errors.

**THE BUG.** menuSelMark tints the cursor by drawing it into an offscreen CANVAS. The guard directly
below then tested `im.naturalWidth` — but a canvas has `width`, not `naturalWidth`. So the tinted
buffer measured as undefined, a perfectly good sprite was treated as unloadable, execution fell out
of the if/else and threw. MODE SELECT is the only screen using a tinted cursor, which is exactly
where Mike froze.

**THE REAL PROBLEM IS THE MECHANISM, NOT THE BUG.** requestAnimationFrame(loop) sits at the BOTTOM
of the frame function. Any exception escaping the update or the draw stops that reschedule, and the
game locks forever — no error on screen, no console message, just a frozen picture with the music
still playing. That is the mechanism behind BOTH hard locks: the dead switch in 0724bb and this.
One bad line in one draw function has been enough to end a session, twice.
The frame is now guarded on BOTH halves. The update is wrapped as well as the draw — deliberately,
because updatePlay carries far more logic than drawScene, so guarding only the draw would have left
the larger half of the risk uncovered. A bad frame now costs ONE FRAME and logs once, and the loop
always reschedules.

**THE TEST THAT NEARLY LIED.** My assertion "the catch sits before the reschedule" FAILED — because
the explanatory comment I had just written contains the words requestAnimationFrame(loop), and a
naive index search found the COMMENT rather than the call. Eleventh instance of the same
string-vs-behaviour trap. The test now strips comments before matching. It also caught something
real: writing it made me look at the loop body properly, which is how I noticed updatePlay was
sitting outside the guard.

---

## DROP 0724bh — COLESOUND v5.1 SPACE SERIES WIRED

Build: 1068 assertions, 0 errors. SFX bank 77 -> 109.

**32 SOUNDS x 3 CHIP VARIANTS.** Took the YM2151 set — that is the Neo-Geo sound chip, and the
whole game is styled "Fireshark meets Raiden II on Neo-Geo". All three variants measured identical
in duration and peak (-0.7 dB), so the choice was purely tonal, not technical.
Source was 48kHz STEREO; converted to MONO 44.1kHz per the engine's own audio spec. Stereo is
wasted because every sound is positioned in code, and mono halves the payload.

**NOTHING WAS DESTROYED.** Every sound registers under its own nsp_ key FIRST, then existing engine
keys are re-pointed at those files. The old audio stays on disk and every mapping is one line to
revert. Asserted that both the nsp_ key and the engine key resolve.

**25 ENGINE SOUNDS RE-POINTED**, chosen on what each sound IS rather than name similarity:
  laser<-pulse-laser  laserShot<-heavy-laser  spread<-scatter-laser  shoot<-bof2-shot
  helixCharge<-bof2-charge-shot  helixBurst<-charge-release  helixVolley<-railgun
  bossWhiteout<-bof2-ultra-blast  bossAlarm<-bof2-boss-warning  powerup<-bof2-pickup
  getready<-bof2-stage-intro  missile<-rocket-launch  launch<-booster-ignite  dash<-rcs-thruster
  thruster<-engine-loop  crash<-comet-impact  firewall<-solar-flare  dangerAlert<-alert-critical
  lockAlert<-nav-lock  blip<-console-beep  mapMove<-nav-ping  mapDeploy<-warp-jump
  enemyApproach<-rocket-flyby  amb_orbital<-meteor-shower  amb_void<-space-rumble
The "BOF II Prototypes" folder was authored for this game by name, so those went to the moments
they were clearly written for.

**FOUR MOMENTS THAT HAD NO SOUND AT ALL, now do:**
  docking-clamp   boss parts CLUNK as they lock into place during the assembly entrance
  asteroid-break  stage-5 rocks shatter
  shield-down     losing a shield is finally audible
  scanner-sweep   the retina lock sweeps as it cycles targets

---

## DROP 0724bg — I WAS WRONG: THE CRYO PHASE SHEET WAS THERE ALL ALONG

Build: 1059 assertions, 0 errors.

**MY ERROR, PLAINLY.** Last drop I told Mike no upgraded boss bodies had been delivered. That was
false. cryo-behemoth-upgrade-concept-corrected.png was sitting in the pack I had already extracted,
and I catalogued it as "a 5-phase cryo CONCEPT image" and skipped it — BECAUSE THE FILENAME SAID
"concept". I never opened it.
It is a finished five-phase boss progression: 5 cells of 228px, 123,597 opaque pixels, mean
brightness 136-145 — brighter than the mba_cb art actually in the game (135 clean, 80 ruin), with
the cannons already posed per phase exactly as cannon-consistency.json describes.
This is the precise mistake I have been documenting in this file for weeks: judging an asset by its
NAME instead of measuring it. I did it while telling Mike I had searched everything.

**NOW WIRED.** Sliced to ncbp_0..4, square-canvassed and centre-anchored (measured: 0px centre
offset on all five, 0 magenta, 0 semi-alpha). Phase is driven by HP — 82% / 62% / 40% / 18% — so
the behemoth visibly deploys as you break it down, and the sheet's own cannons mean the separate
cannon pass is skipped when it is active. Asserted all five phases are reachable and ordered.

**THE CHAINS — MEASURED, AND MY IMPLEMENTATION IS STILL WRONG.** Bounding boxes across the six
phases: 40 -> 55 -> 30 -> 25 -> 20 -> 17 px wide at a constant ~158px tall. That is a chain going
from SLACK (sagging wide) to TAUT (pulled straight), which matches the slack->charged phase names.
So the ART is a tension progression. What I built was decorative overlays hanging either side of
the hull, which is why Mike says they are not the chains he means. The missing piece is what they
ATTACH to — I need that answer before rebuilding the rig rather than guessing a third time.

---

## DROP 0724bf — BALANCE, ASSEMBLY SCOPE, AND THE L2/L3 BOSS ART ANSWER

Build: 1052 assertions, 0 errors.

**THE BALANCE PROBLEM, MEASURED.** Mike: "after level 1 all fodder enemies are extremely tough."
I measured time-to-kill with the DEFAULT gun before changing anything, and the fodder was not the
problem — most units die in 0.1-0.7s. The gun was: weapon 0 fired ONE pellet of ONE damage at
0.085s = 11.8 dps, and every upgrade added WIDTH but never per-pellet punch. So the starting weapon
never got stronger while the game did.
Per-pellet damage now scales: 2 + floor(lv/2). L0 doubles to 24 dps, and the curve runs
24 / 47 / 71 / 106 / 188 / 235 across the six tiers. L0 and L1 still share a per-pellet value, so
the L1 upgrade remains purely "a second bullet" exactly as specified.

**ASSEMBLY IS FOR FORTRESS BOSSES ONLY.** Mike: "do not form the bosses from bits and pieces like
that, they are jets and planes." I had applied the entrance to EVERY modular boss in 0724ay, which
meant aircraft assembled themselves out of flying parts. Now gated to magmacolossus, cryobehemoth
and vileexistence. Magma and cryo are single-hull, so theirs is the POWER-ON wash; the Vile
Existence has 5 components and gets the full multi-part dock. Everything else simply flies in.
The old test asserted the behaviour Mike asked me to REMOVE (it used ironrev, a jet), so it now
asserts the opposite: a jet must NOT assemble.

**THE L2/L3 BOSS ART — MEASURED ANSWER, NOT AN OPINION.**
    mba_mc_body_clean (magma colossus)  mean brightness 51 / 255
    mba_cb_body_clean (cryo behemoth)   mean brightness 135 / 255
The level-2 boss art is genuinely, measurably dark — nearly 3x darker than the level-3 boss from
the same pack — and it is the CLEAN frame, not a damage state. It is not a tint being applied; the
canvas brightness filters were removed last drop and both now tint identically through xartTint.
Searched every source folder for magma/colossus/cryo/behemoth: the ONLY body art anywhere is the
mba_mc / mba_cb set already in the game. CF_BossUpgradeCorrections-Vol_1 contained 12 chain
overlays, 2 cannon masters and a concept image — no upgraded BODIES. If upgraded bodies exist they
have not been uploaded.

**STILL OPEN:** the level-6 missile approach (scale up from the background, shootable, area damage,
facing the player) and the chain rig, which Mike has confirmed is not what he meant by chains.

---

## DROP 0724be — STAGE 5 REBALANCE

Build: 1054 assertions, 0 errors.

**THE ASTEROIDS WERE ENORMOUS, AND THE NUMBERS SAY WHY.** The art is already 146-202px at native,
and l5RockSpawn multiplied it by up to 1.55 — so a single big rock rendered at 313px on a 480px
screen, two thirds of the play area. Scale cut to 0.45-0.70 (big) / 0.26-0.42 (small): the widest
rock is now 141px. A hazard you fly around instead of a wall.

**AND THEY WERE TOUGHER THAN THE ENEMIES.** hp = 30 + sc*70 gave a big rock ~138hp — more than the
hauler, the toughest unit on the stage. Now 10 + sc*22, so a big one breaks at 25hp. Scenery should
break in a burst.

**THE WHOLE ORBITAL CAST DE-BEEFED ~45%:** needle 24->13, crescent 44->24, hauler 68->37,
oracle 56->30. Stage 5 fields big slow targets inside an asteroid field, and at the old values
every single one outlasted its welcome — the level read as a chore. SCORES UNCHANGED, so nothing
is lost in reward, only in grind.

**BACKGROUND FURNITURE READS AS BACKGROUND.** Satellites, hulks and drifting debris do NOT damage
the player, but were drawn at full brightness and full size — so they competed with real threats
and the player kept dodging scenery. Now 55% alpha, 78% scale, with a dark source-atop wash.

**A TEST THAT PASSED FOR THE WRONG REASON, CAUGHT.** My first assertion called
l5RockSpawn(true) — but the signature is (x, big), so `true` landed in the X slot and it spawned
SMALL rocks. It reported a max scale of 0.42 and passed happily while never testing the big tier at
all. Fixed to l5RockSpawn(null, true) and tightened to assert the value is IN the big range, not
merely below a ceiling. A bound that only checks "small enough" cannot tell you it measured the
right thing.

---

## DROP 0724bd — SHADOWS OUT, POWERUPS IN, BARS PINNED

Build: 1045 assertions, 0 errors.

**DROP SHADOWS REMOVED.** drawUnitShadow() painted a soft black ellipse under EVERY unit — player,
enemies, vehicles — offset by distance from screen centre. It is a procedural CSS-style effect
pasted under 16-bit art: it never matched the sprites and smeared against the terrain. Kept as a
no-op rather than deleted so its ~6 call sites stay harmless instead of leaving holes.

**POWERUPS SPAWN DURING BOSS FIGHTS.** The container spawner was gated on `!bossActive`, so the
instant a boss engaged the player was cut off from health, shields and weapon upgrades for the
entire fight — precisely when they need them most. They now spawn throughout, at 1.45x the interval
during a boss so it stays a fight rather than a restock.

**HEALTH BARS PINNED TO THE SCREEN.** The boss bar draws on the HUD canvas and was always fine. The
MINIBOSS bar I added in 0724ao draws inside the WORLD transform, so on the 800px-wide stages it
scrolled sideways with the camera and drifted off centre. Now cancels camX.

**STORM SOVEREIGN FACING.** Measured rather than guessed: its front-core art is 15px wide at the
top and 86px at the bottom — an unmistakable nose-up silhouette, so it was flying tail-first at the
player. Added to ASSIGNED_FLIP alongside lr/jc/cc.

**NOT DONE — the naval chase.** Mike wants this boss fight to become a high-speed pursuit over
water with the naval arsenal. That is a genuine set-piece: scrolling water bed, a fleeing boss with
its own movement rules, escorting naval units, and a scripted camera. It deserves its own pass, not
a corner of a bugfix drop.

---

## DROP 0724bc — PLAYTEST BATCH: DEATH SCALE, HTML EFFECTS, CHAIN, ALERTS, SNOW

Build: 1035 assertions, 0 errors.

**THE EXPLOSION SCALE — A THIRD DEATH PATH.** Mike flagged this four times. I fixed unitDeathFX,
then the engine default, then disintegrate. The remaining offender was killEnemy() itself:
  · tanks fired 3-4 explosions at e.w*0.6/0.8 AND then ran disintegrate -> unitDeathFX. Every tank
    died TWICE, which is why they bloomed past the hull.
  · turret deaths drew a sprite anim at e.w*2.3 — a 20px emplacement detonating as a 46px sprite.
  · boss death used a FIXED rnd(34,72) whatever the boss's size; sub-bosses rnd(28,54).
All four now derive from the unit. Four separate call sites, one rule.

**NO MORE HTML EFFECTS FOR DAMAGE.** ctx.filter='brightness()' removed from the enemy draw, the zap
flash, the sub-boss draw and the modular part draw. Canvas filters are a CSS-style effect: they
render inconsistently per context and were why several units never appeared to light up. Everything
now tints through xartTint, which preserves the sprite silhouette exactly. The zap flash became an
additive wash.

**TANK MINIBOSS GLOWS.** It had NO flash of any kind — you could empty a clip into it with zero
feedback. Now tints like every other unit.

**CHAIN LIGHTNING.** No sound on release (it only had a hit sound) — now fires chainShoot. And it
can now target ENEMY MISSILES: swatting a homing missile out of the air is exactly what a chain
weapon should do, and it could not touch them.

**FIREWAVE ALERTS REBUILT to Mike's spec.** Numbers gone. Orange translucent lane wash gone. Each
alert now LEVITATES and BUMPS on every bob — scaling up with a white unit-glow flash (the cursor
trick) and a beat on each bump. They appear in wave order and each VANISHES as its own wave
launches, so what is on screen is always exactly what is still coming. Side variants carry a
direction arrow beneath the sign.

**SNOW VISIBILITY.** The storm dim was 42% AND was drawn in wfxDraw, which runs AFTER the units —
so the wash sat on top of the enemies. Split into its own pass drawn on the TERRAIN, under
everything that moves, and halved to 21%. Terrain darkens; the things trying to kill you stay
readable.

---

## DROP 0724bb — CRITICAL REGRESSION FIXED: THE DRAW DISPATCH WAS CUT IN HALF

Build: 1016 assertions, 0 errors.

**THIS ONE WAS MINE AND IT BROKE THE GAME.** In drop 0724ar I injected the selection flash into
drawScene by SPLITTING its switch statement in two:
      case GS.OUTBOUND: return drawOutbound(dt);
    }
    ...flash...
    switch(0){ case -1:            <- everything below here is now UNREACHABLE
      case GS.PLAY: return drawWorld(dt);
      ...
`switch(0)` never matches `case -1`, so NINE states stopped rendering entirely: PLAY, paused,
STAGECLEAR, GAMEOVER, CONTINUE, VICTORY, RIVAL, FLYOVER, STAGESEL and MODESEL.
Symptoms matched exactly: NEW GAME goes to MODESEL -> frozen static screen with music playing.
Password goes straight to PLAY -> invisible gameplay with audible firing. Audio and input were
never affected because only the DRAW path was severed.

**WHY NOTHING CAUGHT IT.** `node --check` passed — it is perfectly valid JavaScript. The harness
never exercised drawScene's dispatch, only the individual draw functions, so 1010 assertions all
passed on a game that could not render itself.

**FIX.** The dead switch is gone; the dispatch is one switch again with all 20 states. The flash
overlay moved to the FRAME LOOP, painted after drawScene returns — which is where a full-screen
overlay belonged in the first place. Never split a dispatch to inject an overlay.

**NEW GUARD.** The harness now asserts drawScene contains exactly ONE switch, no `switch(0)`, all
20 states dispatched, and every one resolving to a real function. This class of failure is now a
build error.

**THE HONEST LESSON.** I reached for a quick structural hack instead of finding the right insertion
point, and I verified it with a syntax check instead of behaviour. Both were shortcuts, and they
cost Mike a broken build. The same principle I have written into this roadmap five times —
assert what the code DOES — is exactly what I skipped.

---

## DROP 0724ba — WHY ALMOST NONE OF THE SOUND PACK WAS AUDIBLE

Build: 1010 assertions, 0 errors.

**A HARDCODED WHITELIST OF 33 NAMES.** Snd re-points Audio.SFX at the real samples like this:
    const SFXMETHODS=['shoot','spread',...,'missile','crackle'];   // 33 names, written by hand
    for(const m of SFXMETHODS){ ... Audio.SFX[m]=function(){ Snd.play(m); } }
Only names ON THAT LIST ever got a method. Every sound added since — the 18 that were silent, the
helix set, the boss stinger, the ally cues, the whole race, the campaign map — was registered in
BOFA.sfx, had a real file on disk, and was CALLED at exactly the right moment... and did nothing,
because no handle was ever built for it.
And it failed COMPLETELY SILENTLY: the call sites are all written defensively as
`if(Audio.SFX.helixBurst) Audio.SFX.helixBurst();`, which is simply false when the method does not
exist. No error, no warning, no missing-asset message. Exactly "very few made it through".
Now driven off BOFA.sfx itself: registering a sound is all it takes. 77/77 handles, and every one
of the 66 distinct SFX calls in the source resolves.

**AMBIENCE NEVER PLAYED EITHER — my bug.** ambStart looked for `Snd.sfx[key]`. Snd has no .sfx map;
its buffers live on Snd.pools. The guard bailed every single time, so not one of the 8 stage beds
ever started. Now reads Snd.pools[key].list[0].

**FOUR MORE WIRED:** insertCoin (title), mapDeploy (campaign map commit), enemyApproach (miniboss
warning), impactImminent (a firewave crossing the halfway line). 36 of the 38 delivered pack sounds
now fire on a real event; falvaCharge/falvaBurst still wait on her charge-tier ART.

**THE PATTERN, SIXTH TIME:** a correct system defeated by a second one upstream — and once again a
hand-maintained list that nobody updated. The defensive `if(Audio.SFX.x)` idiom is what hid it, so
the new assertion checks that every SFX call resolves to a registered sound, which turns this class
of failure into a build error instead of silence.

---

## DROP 0724az — FULLSCREEN: THE CONTAINING-BLOCK TRAP

Build: 1002 assertions, 0 errors.

**THE ACTUAL CAUSE, after five previous attempts at the wrong layer.**
    #cabinet{position:relative; ... filter:drop-shadow(...)}
ANY ancestor carrying a `filter` becomes the containing block for its `position:fixed` descendants.
#game-frame is position:fixed in fullscreen with left/top computed from the VIEWPORT — but those
values were being resolved against #cabinet's box instead, and since #cabinet is flex-centred
inside #room, the whole game was displaced by the cabinet's own offset. That is the "sitting more
to the right" Mike saw, and it is why fixing fitCanvas twice, the canvas CSS once and the stale
margin once all failed: every one of those was downstream of a coordinate system that was wrong.
Fixed by clearing the filter and collapsing the cabinet in fullscreen only (it is invisible there
anyway). Windowed mode keeps its drop-shadow — asserted, so the fix cannot cost the cabinet art.

**AND THE DIVIDER THE FULLSCREEN BRANCH FORGOT.** The windowed branch reserves divH=3 for the
strip between the HUD and the game; fullscreen never did. So the frame was 3px short, overflow:
hidden clipped the bottom of the play area, and centring by a too-small height sat it low. Now
reserved before fitting AND counted in the frame height.

**VERIFIED BY REPLICATING THE LAYOUT** at six resolutions: horizontal and vertical gaps balanced to
within 1px everywhere (1920x1080 510/510 and 1/0, 3840x2160 1018/1018 and 0/0), and the frame never
exceeds the screen on either axis.

**FIFTH TIME THIS EXACT SHAPE:** silent modular bosses, the helix split, explosion scaling,
the stale margin, and now this — a correct-looking fix defeated by a second thing further up the
chain. The rule earns another line: when a fix does not take, stop editing it and go find what ELSE
owns the value. Here it was not even code, it was a CSS property changing what "fixed" means.

---

## DROP 0724ay — BOSS ASSEMBLY ENTRANCE + VEHICLES THAT DRIVE

Build: 995 assertions, 0 errors.

**THE ENTRANCE WAS THE MISSING HALF.** Bosses lerped down from off-screen and started shooting.
That is a spawn, not an entrance — and it is the single biggest reason they did not feel like
Contra III / Shinobi III bosses. In those games the fight has not started yet and you are being
made to WATCH something assemble itself.

FOUR BEATS, built entirely on the part list the modular system already had — no new art:
  1 HULL      the bare body arrives, unpowered
  2 DOCKING   each part FLIES IN from alternating sides, fast, then decelerates hard into its
              socket. Staggered bottom-up so it builds legs-to-head like a real machine. Every
              dock lands an impact: whoosh on launch, CLUNK + shake + spark on arrival.
  3 POWER-ON  the assembled unit floods WHITE FROM THE BOTTOM UP through a clipped band that
              climbs the hull, with a scan line riding its top edge — the same white-flash
              language as the Phoenix selection rule, scaled to a boss.
  4 LIVE      only now does b.enter clear and the fight begin.
Measured on the Iron Revenant: 12 parts, both sides alternating, all 12 registering an impact,
wash climbing 0.48 -> 0.95, fight gated until the end.

**VEHICLES DRIVE, THEY DO NOT FLOAT.** Mike: "tank minibosses never swerve or bob side to side."
They were on a sine drift (x = centre + sin(t)*96) plus a vertical bob — the exact motion of a
hovering airframe, which is why they read as weightless. Ground units now REPOSITION: pick a lane,
accelerate out, brake in, ARRIVE AND STOP, hold still, pick again. Vertical bob removed for ground
units only; air units keep both. Measured over 8s: 5 fully-stationary samples and 1 direction
reversal, against the constant oscillation of a sine.

**STILL TO DO on Mike's brief:** chains should visibly dangle and swing during the dock (the art
supports it, the swing physics do not exist yet); per-section destruction EXISTS (parts already
carry role, hp and clean/dam/ruin art) but sections cannot yet be blown off INDEPENDENTLY of the
boss dying; and the intro needs a name card. Those are the next pass.

---

## DROP 0724ax — EVERY BOSS HAS A SIGNATURE ATTACK

Build: 978 assertions, 0 errors.

**CF_LevelMap-Lvl4 — NOT WIRED, DELIBERATELY.** Compared byte-for-byte before touching anything:
9 of 10 files are IDENTICAL (md5) to what already ships. The tenth, the boss arena, differs only
because WE flipped it in drop 0724h so the run ends on the dense base — re-importing would have
silently undone that, and the symptom would have surfaced drops later with no obvious cause.
Genuinely new: a pre-assembled complete-route-with-boss (800x4488) which our master matches at
diff 0.00 when flipped, plus a 4th seam strip for that variant. No new artwork. Left alone.

**THE REAL BOSS GAP.** Audited all 8: only ONE (magma colossus) has its own _profile. The other
seven use the shared bossAttack(), which has a per-stage SIGNATURE move... that stops at stage 5.
    floatText(... [5 names][clamp(run.stage-1,0,4)])   <- silently reused CORE MELTDOWN for 6/7/8
    switch(run.stage){ case 1..5 }                     <- fell straight through for 6/7/8
So the storm boss, the sewer boss AND THE FINALE all fought with nothing but the generic
left-hand/right-hand/dual machine-gun patterns. The clamp is what hid it: they still SHOUTED a
signature name, so it looked like they had one.

**THREE NEW SIGNATURES, each with a different answer for the player:**
  6 THUNDERHEAD    three lightning lanes walk across with readable gaps — you read the gaps
  7 FLOOD SURGE    a rising wall of sludge with ONE moving gap — the gap IS the answer
  8 ANNIHILATION   converging cross into a 16-way radial burst plus a 4-missile spread
Verified through the REAL update path, all 8 stages: every boss fires (24/28/110/74/67/56/56/56
bullets over 6s). Not one is silent.

---

## DROP 0724aw — BOSS DETAIL PARTS: MAGMA CHAINS + CRYO CANNONS

Build: 971 assertions, 0 errors. Manifest 5801 -> 5815 (+14).

**THESE ARE NOT ROTORS.** I asked for separated rotor sprites in the art spec; the pack delivered
something better suited to these two bosses, and reading its own JSON first is what stopped me
wiring it wrong:
  MAGMA CHAINS   12 overlays (6 per side), 128x192. Phases: slack / tension / rising / alignment /
                 docking / charged. A STATE PROGRESSION, not an animation loop — cycling them would
                 read as decoration instead of the boss winding up.
  CRYO CANNONS   ONE immutable 7-barrel master plus its exact pixel mirror, 128x128.
                 cannon-consistency.json: "Never redraw the cannon. Move/rotate the immutable
                 master and its exact mirror only."

**THE MIRROR RULE IS A HARD CONTRACT.** Verified on arrival that the right master is a BYTE-EXACT
mirror of the left, and asserted it again after the copy. The draw path only ever translates and
rotates those two sprites — the harness asserts there is no fillStyle and no xartTint anywhere in
it, so the five phases (detached / rising / aligned / docked / firing) are produced purely by pose.

**BOTH DRIVEN OFF EXISTING BOSS STATE.** The chains read the same _muzT and _mcd the magma attack
profile already uses, and the cannons read HP fraction plus _muzT. Nothing keeps its own private
timer, so the parts can never disagree with what the boss is actually doing — which is exactly how
the boss animation and the boss attacks drifted apart before.
Asserted end to end: idle boss hangs slack, damage tightens to tension, winding up walks 2 -> 4,
firing hits charged; cannons deploy 0 -> 1 -> 2 -> 3 as HP falls and reach firing on the shot.

**Pack quality:** 0 semi-alpha and 0 magenta across all 16 files on arrival. Nothing needed repair.

---

## DROP 0724av — DETACHED SPRITE SPECKS

Build: 955 assertions, 0 errors.

**IT WAS NOT ONLY YURI.** Mike reported "a weird speck on the bottom of this frame" for Yuri.
Scanning every ship sprite for detached blobs found the problem across SIX pilots, 12 sprites:
Yuri, Cole, Falva, Lizzie, Maverick and Juggernaut. Yuri's was simply the most visible — a 149px
blob sitting 5px BELOW the hull, horizontally centred under it, so it read as a piece of debris
permanently trailing the ship.

**THE CARE THAT MATTERED — not everything detached is a mistake.** Barrel-roll frames legitimately
have wingtips that read as separate blobs (Falva's br5 has a 1045px and a 176px wing section,
Cole's br1 a 439px one). Deleting "all small detached blobs" would have amputated them.
The rule used: a blob is a SPECK only if it is <=200px AND separated from the hull by a real gap
AND horizontally INSIDE the hull's own column range. Wingtips sit BESIDE the body and extend past
its x-range, so they fail the third test and are untouched. Sub-5px orphans are removed regardless.
Result: 10 sprites cleaned, every wingtip preserved, every hull byte-identical in size.

---

## DROP 0724au — FULLSCREEN CENTRING, FIFTH ATTEMPT AND ACTUALLY FOUND

Build: 951 assertions, 0 errors.

**WHY FOUR PREVIOUS ATTEMPTS FAILED.** I kept fixing fitCanvas (twice) and the canvas CSS (once),
because that is where "the canvas is the wrong size" logically lives. The canvas was never the
problem. index.html has a layout function L() with two completely separate branches, and the bug
was a variable leaking from one into the other:
    windowed branch:   sa.style.marginLeft = screenX    // centres the game in the cabinet window
    fullscreen branch: (never touched marginLeft)
So entering fullscreen kept whatever left margin the windowed layout had last written, and the
entire play area sat pushed left by that amount. It was not a sizing bug at all — it was stale
state carried across a mode switch.
Fixed by clearing it in the fullscreen branch, and while there, sizing the HUD strip, equip box and
divider for the new width — they were also keeping stale windowed values.

**VERIFIED BY REPLICATING THE LAYOUT MATHS** rather than eyeballing: centre offset at 1920x1080,
2560x1080 ultrawide, 1366x768, 3840x2160, 1280x1024 and 800x600 is at most 0.5px (a rounding
half-pixel), and the 480x512 aspect holds at every one.

**THE LESSON:** when a fix does not take, check whether the OTHER branch of the same function is
writing the state you are fixing. Same shape as the modular-boss silence, the helix split and the
explosion scaling — four times now, always a second path.

---

## DROP 0724at — BULLET SPRITE FLICKER + LEVEL-3 DRONES

Build: 943 assertions, 0 errors.

**THE BULLETS SWITCHING BETWEEN A CIRCLE AND A SPRITE — ROOT CAUSE.** FIRETYPES build their art key
from the bullet's `_ph` field (mfx_ea_0_<2+_ph%3>, mfx_bshot_0_<...>, and the two-frame pellet
alternation). eShoot() — the ORIGINAL fire helper, used at 77 call sites across the whole game —
never assigned one. With _ph undefined the key came out malformed, XART.rdy() returned false, and
drawFireType fell through to the procedural circle fallback. So a bullet drew as its sprite on some
frames and as a plain dot on others, exactly as Mike described.
Fixed in eShoot itself (and `t` with it) rather than at 77 call sites. Asserted that every bullet
from BOTH fire helpers carries a phase, and that every phase of every family resolves to real art.
Note eShootT — the NEWER helper — already set _ph correctly, which is why only some bullets
flickered and why it looked intermittent rather than broken.

**LEVEL 3 GETS DRONES.** The arctic stage was almost entirely fast airframes: 13 spawn types, of
which only mdrone and turdrone appeared once each. Added six drone waves (mdrone rows, drone
formations, minidrone weaves, turdrone pairs, shield drones) slotted BETWEEN the existing jet waves
rather than replacing any of them — the stage needed slower, denser targets so the pacing breathes
between interceptor passes. Plan grew to 28 events.

---

## DROP 0724as — L2/L3 PURPLE PURGED, RESPAWN HOLDS POSITION

Build: 931 assertions, 0 errors.

**THE PURPLE — TWO DIFFERENT DEFECTS, WHICH IS WHY IT KEPT COMING BACK.**
  nst3_master  4575 px of ONE flat violet (166,57,221) — textbook unfilled key. Gone.
  nst2_master  933 px seeded from raw #FF00FF plus the anti-aliased fringe hugging it. Gone.
What REMAINS on both is genuine art: 2019 separate blobs across 2346 unique colours on stage 2,
largest blob 20px. Residue is flat and contiguous; art is scattered and varied. That distinction is
the whole test.

**I DAMAGED STAGE 2 AGAIN AND ROLLED IT BACK — SECOND TIME.** My heal dilated 2px into the fringe
and, because volcanic rock genuinely lives near the key colour, it took 20% of the image with it
(std 76.6 -> flattened). Restored from the shipped zip and redone with EXACT seed values and NO
dilation: 933 px healed, 557 px changed, std still 76.6.
STANDING RULE, now learned twice on the same file: on a stage master, seed from exact values and
never grow the mask. The neighbourhood is not safe.

**ALSO CAUGHT: 253,167 "raw key" pixels on nst2_master are the TRANSPARENT BACKDROP** and must not
be touched — only 35 were actually VISIBLE. My first check counted all of them and reported a
failure that would have led me to destroy the file a third time. The test now measures visible
pixels only.

**RESPAWN HOLDS POSITION.** player.reset() always teleported to screen centre, so dying mid-fight
also relocated you — worst during a boss, where the centre can be the most dangerous spot. Losing a
life now respawns you WHERE YOU DIED, with the usual invulnerability so it is not a death trap. A
fresh stage start still centres the ship.

---

## DROP 0724ar — PHOENIX SELECTION RULE + CAMPAIGN MAP DEPLOY

Build: 919 assertions, 0 errors.

**PHOENIX ENGINE RULE, MADE ACTUAL CODE.** Mike: "all selections flash white like the buttons have
been. This is a phoenix engine rule and never changes." Mode select was jumping straight to the next
state with no flash and no transition, which is exactly why it felt disconnected from the rest of
the game. Added selFlash(fn) as a SHARED helper: it runs the white strobe and only fires the action
when the flash completes. Mode select and the campaign map both go through it, so the behaviour
cannot drift apart per screen again — which is how it drifted in the first place.

**RED CURSOR ON MODE SELECT.** Same cursor art as everywhere else, palette-swapped through a cached
source-atop buffer. Deliberately NOT getImageData — that call killed the whole campaign map on
file:// once already, and a cosmetic tint must never be able to do that again.

**THE MAP SHIP FACES WHERE IT IS GOING.** The sprite's nose points up by default, so flying in from
the left it travelled right while still facing up-screen. It now aims along its actual velocity
(with a +90 degree correction for the art's default orientation), eases into new headings rather
than snapping, and holds the last heading when it settles. Verified: entering from the left it
faces right.

**DEPLOY IS A SEQUENCE NOW.** Selecting a stage used to cut straight to beginStage. Now:
white flash -> medium zoom (1.25s smoothstep) pushing in on the chosen flag while "GOOD LUCK"
plays -> stage card. Asserted end to end through the real handler.

**Note:** drawStageSelect is now a thin wrapper that applies the zoom transform around
_drawStageSelectInner, so several existing assertions had to be retargeted at the inner function.
They were inspecting the function body, and the body moved.

---

## DROP 0724aq — EXPLOSION SCALE: THE SECOND DEATH PATH

Build: 903 assertions, 0 errors.

**Mike flagged blast scaling as a standing engine rule twice, and I fixed the wrong thing twice.**
I moved unit deaths onto the class system, then made the reference pack the engine default — both
correct, neither the cause. Instrumenting an actual jet kill end to end found it in one step:
    disintegrate()  ->  explode(cx, cy, e.w * 1.4, 'red')
A SECOND death path, bypassing unitDeathFX entirely. A 44px jet detonated at 62px before
EXPLODE_SCALE had even touched it — about 1.6x the airframe on screen.
Now routed through unitDeathFX like every other death, so family, size, secondaries and shake all
come from the unit class. Measured on real kills through the real path:
    fang jet   44px unit -> 44px blast
    drone      29px unit -> 29px blast
    road tank  52px unit -> 52px blast
Asserted across all three, so any future death path that inflates the blast fails the build.

**THE LESSON, and it is now the third time in this shape:** when a fix "does not take", stop
re-fixing the thing you already changed and go find the OTHER caller. Same as the silent modular
bosses and the helix split — a correct system with a second path routing around it. I should have
instrumented the real kill on the first report instead of the third.

**STAGED, NOT WIRED:** CF_BossUpgradeCorrections-Vol_1 (magma-colossus chains, cryo-behemoth
cannons — the separated boss detail parts requested in the art spec) and CF_LevelMap-Lvl4.
37 PNGs held in /tmp/build/staged for the next pass.

---

## DROP 0724ap — BOSS SCROLL LOCK + THRUSTER OVERLAY

Build: 897 assertions, 0 errors.

**THE TERRAIN NO LONGER RACES DURING A BOSS FIGHT.** There was a deliberate BOSS_SCROLL_MUL that
made the ground scroll FASTER and loop forever once a boss engaged — the fight played out over
continuously racing terrain. That is backwards for the helicopter: it is supposed to be BLOCKING
the player at the dam, and instead the level carried you through it while you fought.
A boss is a wall. The level now stops advancing and you fight it where it stands. It EASES to a
standstill over ~0.6s rather than snapping, so the arrival still reads as arriving (97% of normal
speed on the first frame, zero within a second), and the hold resets on the boss's death so the
level resumes normally afterwards.

**THRUSTER OVERLAY.** Every pilot sprite already has its engine flame drawn INTO the art, and the
ntr_ trail was being drawn directly on top of it — two thrusters fighting for the same pixels,
which is exactly what Mike was seeing. The trail now starts BELOW the tail flame and reads as the
wake trailing behind it: narrower (9px vs 13), softer (0.60 alpha ceiling vs 0.95), and pushed
back from y+12 to y+22. The pilot-coloured, throttle-reactive behaviour is unchanged — it just no
longer competes with the sprite it is attached to.

**Test note:** drawLevelMaster needs real assets to reach its scroll code, so the harness exercises
the HOLD CURVE directly rather than asserting on a function that returns early headlessly. Testing
what the code computes, not what a stub happens to return.

---

## DROP 0724ao — RIVAL DISABLED, SNOW FULL-SCREEN, MINIBOSS BAR

Build: 885 assertions, 0 errors.

**RIVAL ENCOUNTERS DISABLED** behind a single flag, RIVAL_ENABLED=false. Nothing deleted — the
courses, the 69 art keys, the ally system, the phase machine and every test remain in place and
still pass. Flipping the flag back restores all three encounters. In its current state the mode was
worse than absent, and it may not make the jam.

**SNOW IS A STORM, NOT PATCHES.** The bed drew one square sprite per particle, so at storm density
it read as a grid of tiles rather than weather. Now a full-screen sheet tiled across the whole
viewport at TWO parallax speeds (one drifting right, one left), with the particles kept underneath
as close-up flurries. The post-miniboss ramp and the level dimming are unchanged.

**MINIBOSS HEALTH BAR.** Sub-bosses had none at all, so there was no way to tell a miniboss from a
tough enemy or read how the fight was going. Deliberately styled DIFFERENT from the full boss bar —
thinner, amber, centred under the HUD line, with the unit's name above it and a flash under 25% —
so the two are never confused. Hidden while the unit is still flying in.

**Also verified fixed by 0724an:** the level-1 siege crawler is modular, so it now lights up on hit
through the xartTint change made for the L2/L3 bosses.

---

## DROP 0724an — PLAYTEST FIXES (4 of 16)

Build: 875 assertions, 0 errors.

**EXPLOSIONS — the actual root cause, finally.** Mike has flagged the old small "atomic" bursts
three times and I kept moving unit DEATHS onto the reference pack, which was never the problem.
explode() has a five-tier legacy fallback chain (nex_ -> nx_fire -> mfx_ex -> ASSETS) that runs
whenever no family is named. Only deaths name a family. Every OTHER explosion in the game — bullet
impacts, scenery, debris, boss hull cracks, the 58 direct explode() calls — still fell straight
through to the legacy art. THE REFERENCE PACK IS NOW THE ENGINE DEFAULT: an unnamed explosion picks
a round reference set by size (<=26 clus, <=44 barrage, <=80 white, <=130 dense, else ring).
Asserted across every size from 8 to 220 that nothing reaches the legacy families.
This is the "engine header rule" Mike asked for — one place, applies everywhere, cannot drift.

**PASSWORD -> ARCADE, STRAIGHT TO THE LEVEL.** startRun branches on run.mode; if a previous session
left it on 'campaign' a password dropped the player on the campaign MAP instead of the stage.
Enforced in startRun (fromStage>1 can only be a password) rather than the password screen, because
there are TWO drawPassword definitions and the outcome must not depend on which wins at runtime —
my first fix went into the losing one and the assertion caught it.

**HUD HIDDEN OUTSIDE GAMEPLAY.** The score strip and equipment box are DOM elements in index.html,
so they were always on screen — through boot, title, menus and the campaign map, where the player
has no ship, score or equipment. Now tied to the state machine.

**MODULAR BOSSES LIGHT UP WHEN HIT.** They used ctx.filter='brightness()', inconsistent with every
other enemy (which tints via xartTint) and unreliable depending on canvas context — which is why
the L2/L3 bosses looked dark and never flashed. Switched to xartTint, matching the rest of the game.

**NOT DONE — 12 items, stated plainly:** fullscreen alignment; thruster overlay on pilot sprites;
Yuri's stray speck; enemy bullets switching shape; L1 miniboss no flash/health bar; stage still
scrolling at the helicopter; death position/dam swap; purple halos on L2 and L3; rival fight should
be vs Juggernaut and is broken; snow as square patches instead of full-screen; drones on L3;
explosion scaling on jets.

---

## DROP 0724am — SOUND PACK WIRED

Build: 862 assertions, 0 errors. SFX bank 31 -> 77 entries.

**THE PACK IS COMPLETE.** 46 files, named exactly to the engine-key convention, so registration was
mechanical rather than guesswork. Verified on arrival: all 18 previously-SILENT keys filled,
0 keys left that the code calls without a file, SFX normalised to -3 dBFS and ambience to -10 dBFS
(correct — the beds must sit under the music, not compete with it).

**THE 18 SILENT KEYS ARE NOW AUDIBLE.** Every player laser, missile launch, takeoff, brake, dash,
the GO marker, the stats tally, the firewave roar, the lightning crack and the blizzard whip were
all being CALLED during play with nothing behind them. That is fixed.

**28 NEW SOUNDS WIRED TO THEIR EVENTS:**
  helixCharge  fires when the lance reaches the line and begins to glow
  helixBurst   the merge-ball detonation
  helixVolley  the 8-lance volley launching
  bossWhiteout the boss death stack (boss only, not minibosses)
  allyArrive / allyLeave  spared-rival wingman in and out
  raceStart / raceObstacle / raceWin / raceLose  the rival race
  mapMove      campaign-map cursor travelling to a new stage
  flagPlant    firewave alert appearing
  dangerAlert  layered under the firewave roar

**STAGE AMBIENCE.** New system: one looping bed per stage (AMB_KEY 1-8), started with the stage and
stopped on exit, playing at 0.55 volume under the music. All 8 beds registered and mapped.

**Still unwired, deliberately:** falvaCharge / falvaBurst wait on Falva's charge-tier ART (her
current 4 frames cannot show the tiers the sound implies); bossPhase, insertCoin, enemyApproach,
impactImminent and mapDeploy are registered and ready but need their trigger points agreed.

---

## DROP 0724ak — BOSS DEATH SET-PIECE

Build: 835 assertions, 0 errors.

**Mike's spec:** ~6 seconds of explosions, then the screen goes FULL WHITE, then it fades back to
normal while the boss is STILL coming apart for another 2-3 seconds.

**What it was:** blasts thinned out at 3.4s, the white-out bloomed at 3.0s and the whole thing was
finished by 7.0s. It never earned the whiteout — the flash arrived while the boss was barely done
detonating, and the stage cut away almost immediately after.

**NEW TIMELINE (all asserted against the real update path, sampled per second over 10.5s):**
   0.0 - 2.2   blasts accelerate in
   2.2 - 6.0   SUSTAINED detonation — six full seconds, screen stays normal throughout
   6.0 - 6.7   white blooms to FULL (measured peak 1.00)
   6.7 - 7.3   held at full white
   7.3 - 8.6   fades back to colour WHILE the boss keeps exploding
   8.2 - 9.4   blasts taper and stop
Hull sink, debris and shake now run to 8.4s instead of 3.4/3.6, so the boss is visibly coming apart
for the whole sequence rather than sitting still after the first few seconds.
Stage-end hold raised 7.0 -> 9.8 (stage 1: 8.9 -> 11.0) so the payoff can never be cut off
mid-explosion. Stage 1's dam-break now swaps under the PEAK of the white at 6.7s rather than 4.3s.

---

## DROP 0724aj — EXPLOSION FRAMES ANCHORED

Build: 826 assertions, 0 errors.

**Mike: "frames sitting on bottoms of animations or sides."** Measured and real. The frames were
not clipped and nothing touched a canvas edge — the content was simply OFF-CENTRE inside its own
384px frame, and badly so on the opening frames:
    clus frame 0     61px LOW
    upward frame 0   91px LOW
    barrage frame 0  75px LEFT and 77px DOWN
    fall frame 3     55px LEFT
An explosion is drawn CENTRED on the unit that died, so a frame whose blast sits 91px low puts the
fire below the wreck. That is the "sitting on the bottom" exactly.

All 80 frames re-anchored: content bounding-box centre moved to the canvas centre, largest
correction 91px. Verified afterwards that ZERO frames sit >2px off-centre and ZERO now touch an
edge, so the shift did not push anything into a clip.

**Note on what NOT to preserve:** the upward set had a deliberate rising drift baked into its frame
positions. That drift is what made it wander off the unit, and the ascendant secondaries already
provide the rising motion through their own vy. Anchoring the frames and keeping the motion in the
system is the correct split — art holds position, code provides movement.

---

## DROP 0724ai — SIDE-VIEW EXPLOSIONS REMOVED FROM A TOP-DOWN GAME

Build: 821 assertions, 0 errors.

**Mike: "idk what those vertical explosions are but looks weird being added on."** He was right and
the reason is measurable. Two sets in the pack are SIDE-VIEW art with a built-in gravity direction:
  02 falling blast chain   bbox aspect 0.38  — a tall narrow column dropping downward
  03 sideways rolling burst bbox aspect 1.66 — a wide horizontal sweep
Everything else measures 0.78-1.13, i.e. roughly round. On a top-down screen there is no up and no
sideways, so a falling column reads as a stray effect pasted OVER the unit rather than an explosion
coming out of it. My first measurement (centre-of-mass bias) said all ten were fine — it was the
wrong metric; SHAPE was the tell, not position.

Both sets are now used by NOTHING: removed from crate, boat, mini-boat, tank and miniboss
assignments and from the boss death stack. The eight round sets still give every class a distinct
primary and a different secondary, asserted.

They stay registered — they are good art and would be correct for a side-scrolling context or a
scripted set-piece. They are simply wrong for a unit death seen from above.

GIFs re-rendered for every affected class.

---

## DROP 0724ah — EVERY DESTRUCTIBLE FAMILY + BOSS DEATH STACK

Build: 817 assertions, 0 errors.

**NINE FAMILIES NOW, one per destructible class** — the pack's 10 sets cover the whole roster:
  crate 02 falling blast chain · drone 08 multi-hit barrage · turret 01 clustered chain reaction
  jet/plane 05 white-core overpressure · mini-tank + tank 09 heavy upward impact cluster
  mini-boat 07 radial chain detonation · boat 06 red-smoke bloom
  miniboss 04 dense room filler · boss 10 hollow-ring collapse
Every class pairs its primary with a DIFFERENT secondary family, asserted, so no death is one
sprite repeated. Boats split on size — >=40px reads as a boat, smaller as a mini-boat.

**BOSS DEATH IS A SEQUENCE, NOT A POP.** Bosses (7 waves) and minibosses (4) now queue a stack of
overlapping primaries at descending size across the hull, each on a different family, spread over
time. Measured on a boss: 17 queued blasts across 7 families, sequenced 0.10s -> 1.35s. Small units
are explicitly excluded — a turret still gets 1 secondary.

**SCALE IS TIED TO THE UNIT**, asserted end to end: drone 22px, tank 44px, boss 150px.

**GIFS DELIVERED** — one per class plus boom_ALL_scale.gif, which plays all ten side by side at
TRUE relative scale so the size relationship is visible rather than described.

---

## DROP 0724ag — COLEFORGE EXPLOSION PACK WIRED

Build: 806 assertions, 0 errors. Manifest 5721 -> 5801 keys (+80).

**ONE UNIFORM FAMILY PER UNIT CLASS**, which is what Mike asked for and what the pack finally makes
possible. Chosen on what each set actually LOOKS like, not alphabetically:
  turret  01 clustered chain reaction    small and tight — right for a 20px emplacement
  jet     05 white-core overpressure     sharp bright airburst, reads instantly against sky
  tank    09 heavy upward impact cluster ground-up cone; it looks like it came off the deck
  mini    04 dense room filler           fills its own footprint without swamping the screen
  boss    10 hollow-ring collapse        the biggest, and it collapses inward as it ends
SECONDARIES get their OWN family per class (radial chain / multi-hit barrage / sideways rolling
burst / falling blast chain / red-smoke bloom), so a death is a primary plus a DIFFERENT scatter
rather than the same sprite eight times. Asserted all five primaries are distinct and that every
secondary family differs from its own primary.

**TURRETS ARE NOW THEIR OWN DEATH CLASS.** They were classified as tanks, which is why a 20px
emplacement detonated like a 44px vehicle. Split out, with 2 secondaries instead of 4.

**explode() TAKES AN EXPLICIT FAMILY.** Previously every call fell through a fixed guess-chain, so
no caller could ask for a specific set. A death class now names its art directly and that wins;
the old chain remains as the fallback for everything else.

**THE ROLLING-BURST CLIPPING — MEASURED AND FIXED.** Frame 01 had 56 opaque rows at x=366 and ZERO
at x=367; frames 02 and 05 cut identically. The blast is genuinely sliced by a hard vertical edge.
The missing fire cannot be invented, so every hard cut is FEATHERED — alpha ramps down over the
last columns so it dissolves instead of showing a razor line. 45 frames across the pack had a cut;
all now verified to have no bright truncation left. The scan runs over ALL ten sets, not just the
one Mike spotted, and it found cuts in others too.

---

## DROP 0724af — THE PILOT FLIES THE CAMPAIGN MAP

Build: 794 assertions, 0 errors.

**WHAT IT DOES.** Once the flags have finished dropping, the pilot Mike actually selected flies IN
from off the left edge of the map, crosses to stage 1 and settles there under the cursor. Moving
the cursor sends the ship travelling to that stage, easing as it arrives so it drifts to a stop
instead of snapping. It banks into the direction of travel and leaves a short engine trail only
while it is genuinely moving — gold at distance, blue as it closes.

**Asserted, all through the real update path:**
 · it does NOT appear until the boot sequence has finished placing the flags
 · it enters from off the LEFT edge (x = -61)
 · it settles on stage 1 within 6px and switches to its idle hold
 · selecting another stage makes it travel there
 · the motion EASES: 15.17 px/frame early vs 0.000 late — a drift to a stop, not a snap
 · bank stays within its clamp so it never over-rotates
 · reopening the map flies it in fresh

**Safety:** the whole ship pass sits inside its own try/catch beside the per-flag guard. This screen
has already been killed once by an unguarded draw (the getImageData taint), and a cosmetic flourish
must never be able to cost the player the campaign map.

---

## DROP 0724ae — THE HELIX SPLIT: FOUND

Build: 784 assertions, 0 errors.

**Mike's description solved it in one line:** "straight from lance to split lasers to the same
lasers going forward again after the burst." That is three stages, and the MIDDLE one was the bug.

helixDetonate was calling BOTH the merge ball AND helixBurstSpawn. The latter blooms two nhb_ BEAM
sprites outward from the burst point at up to 2.95x scale, and helixBurstsDraw painted them OVER
the ball — larger, brighter, additive. So the ball WAS being created and drawn correctly every
time, and then immediately buried under a laser spray. That spray is what read as "the lasers
splitting", and it is why two previous attempts at "merging the volley" changed nothing: the volley
was already merged, and the thing on screen was not the volley at all.
Removed the bloom from the detonation. Sequence is now strictly BALL -> VOLLEY with nothing in
between, and the ball draws first with no competition.

**Asserted:** exactly one ball, ZERO beam-bloom entries, the volley launches with only a 10px
spread (so it genuinely leaves as one mass) and fans out from velocity as it travels.

**LESSON, and it is the same one as the modular-boss silence:** when a fix "does nothing", stop
re-fixing the thing you already changed and go find what ELSE is drawing. Both bugs were a correct
system being masked by a second one nobody was looking at.

**Also fixed:** the string-vs-behaviour trap for the EIGHTH time — my own comment named the removed
function and failed the assertion checking it was gone. Reworded.

---

## DROP 0724ad — FIREWAVE 1-2-3, RETINA + FIRE

Build: 777 assertions, 0 errors.

**FIREWAVE REBUILT AS A 1-2-3 SET-PIECE.** It was one wave sweeping sideways from a single alert.
Now: three lanes are chosen, then ALERT 1 appears, ALERT 2, ALERT 3 — each numbered, each with a
pulsing lane band running the full height of the screen so you can see exactly where it will fall.
After a hold, the waves come down ONE AT A TIME, each in its own alert's lane, VERTICALLY, growing
0.9x -> 2.15x as they fall, drawn 210px wide and rotated upright so it reads as a wall of fire
rather than a streak. Getting caught still routes through playerHit().
Asserted: the alert count climbs 1 -> 2 -> 3 (never jumps), the first wave drops alone in a lane an
alert actually marked, x NEVER changes while it falls (it is genuinely vertical), it scales up as
it comes, standing in it registers a hit and standing in another lane does not.

**RETINA + FIRE.** The locked-retina branch only accepted the BOMB key, so holding the retina and
pressing FIRE did nothing — you had to tap retina, release, then shoot. It now accepts either
button while the retina is held.

**STILL OPEN from Mike's list:** tanks/planes stacking, uniform explosion families, the helix
energy-ball merge, campaign music fade-in on mode start, and the helicopter holding you at the dam.

---

## DROP 0724ac — MODULAR BOSSES COULD NEVER FIRE

Build: 775 assertions, 0 errors.

**"He just flies around" was the whole diagnosis.** updateBoss had:
    if(b.modular && !b.dead){ updateModularBoss(b, dt); return; }
That `return` sat ABOVE the fireCd countdown and the bossAttack() call. So EVERY modular boss
returned out of updateBoss before it could ever fire. The Magma Colossus's attack profile was
correctly written and correctly hooked into bossAttack() — bossAttack() was simply never reached
for it. Nothing was wrong with the profile at all.
Fixed by driving the same cadence inside the modular branch (gated on !b.enter so it cannot shoot
while flying in). Measured: 49 bullets in 12 seconds where there were previously zero.

**THIS WAS NOT JUST STAGE 2.** Every modular boss was affected — Vile Existence, Cesspool
Leviathan, Iron Revenant. All of them now fire from the real path, asserted individually.

**WHY THE OLD TESTS PASSED.** They called magmaColossusAttack() DIRECTLY and confirmed its four
beats produced bullets — which was true and useless, because nothing in the game ever called it.
Exactly the same failure shape as unitDeathFX in drop 0724t: a correct function nobody invoked,
with tests that exercised the function instead of the path.
The new assertion drives updateBoss() and counts real bullets, which is what would have caught
both. Standing rule now: for anything that must HAPPEN in play, assert through the update path,
never by calling the leaf function.

---

## DROP 0724ab — L2 PURPLE (REAL SOURCE), BOSS-2 HP, TURRET DEATH SIZE

Build: 771 assertions, 0 errors.

**THE LEVEL-2 PURPLE WAS NOT WHERE I LOOKED.** I healed nst2_master last pass, but stage 2 does not
draw it — drawStage2 uses ASSETS.mapVolcano, which is CLEAN (0 purple px). The residue was in the
LAVA FALL frames: nlqf_lava_0..5 carried 294 px of magenta-family key bleed at values like
(208,3,169) and (219,4,167). Healed with a mask that requires BOTH red and blue far above green and
near each other — molten lava is red-dominant with LOW blue, so the art itself can never match it.
294 -> 8 px remaining.
LESSON: check which asset the stage ACTUALLY draws before healing anything. nst2_master was the
obvious name and the wrong file.

**BOSS 2 HP.** hpBase*2.5 made the Magma Colossus a damage sponge for a stage-2 boss. Cut to
hpBase*1.35, in line with the other early bosses — it should test the player, not outlast them.

**TURRET DEATHS.** Diagnosed headlessly first: a microturret has 4 HP, dies to a normal burst, and
its primary blast is 18px against an 18px sprite — all correct. The problem was COUNT, not size:
it was getting the same four overlapping secondaries as a 44px tank, six explosions stacked on one
tiny sprite, which is what read as an enormous death. Secondary count now scales with unit size
(0.25x-1.0x across 16-50px). Turret death went from 6 blasts to 3; big units are unchanged.

**NOT DONE THIS PASS — stated plainly, not buried:**
 - boss 2 attacks: the profile IS wired and its four beats are asserted to fire, so if Mike still
   sees nothing the bug is elsewhere and I need to watch it rather than guess again
 - tanks/planes stacking (needs a separation pass)
 - firewave 1-2-3 sequenced alerts, vertical, wider
 - helix still splitting instead of balling
 - retina + missiles simultaneously
 - campaign music fade-in on mode start
 - helicopter should hold you at the dam instead of scrolling on
None of these are claimed as fixed.

---

## DROP 0724aa — EXPLOSIONS FADE OUT AGAIN

Build: 770 assertions, 0 errors.

**THE BUG.** Both sprite-based explosion paths bottomed out at roughly a third of full alpha at the
end of their life (the reel-driven path and the legacy ASSETS path used slightly different curves,
but both ended visible). So an explosion played its animation and then POPPED out of existence at
~30-35% opacity instead of fading. Only the procedural circle fallback ever faded to zero, which is
why it was not obvious until the death FX started routing everything through the sprite reels in
drop 0724t — that change did not create the bad curve, it made it visible on every kill.

**THE FIX — a proper tail fade.** Full brightness is held through the first 65% of an explosion's
life so the frames keep their punch, then alpha ramps cleanly to ZERO over the last 35%. One shared
value drives both sprite paths, so they can no longer drift apart. The ascendant secondaries all
delegate to explode(), so they inherit it automatically.

**Asserted behaviourally:** the curve is evaluated at six points across an explosion's life — 1.0
at the start and at 65%, partial at 80%, and exactly 0 at expiry — plus a check that an explosion
still spawns and is still cleaned up when its life ends.

**The string-vs-behaviour trap appeared for the SEVENTH time:** the assertion that the old curves
were gone failed against my own comment, which quoted them. Comment reworded. The recurring lesson
stands — assert what the code DOES, and keep literals out of explanatory comments near their own
assertions.

---

## DROP 0724z — HELIX NEVER STOPS, BIGGER VOLLEY, TANKS STAY ON TERRAIN

Build: 763 assertions, 0 errors.

**THE LANCE NO LONGER STALLS.** mavHelixTick zeroed vy/vx when it reached the line, so a released
full charge visibly PARKED mid-screen while it glowed. It now keeps travelling and keeps piercing
the entire time. It does EASE to 42% speed during the tell — at full speed the 0.42s glow could not
finish before the lance left the top of the screen, so the burst happened off-camera and the payoff
was invisible (that is why the volley "wasn't there"). Tell shortened to 0.34s and the burst also
fires the moment it nears the top edge, so it can never be lost off-screen again.

**VOLLEY: 8-9 BIG LANCES, NOT 31 THIN ONES.** Count dropped from 22+lv*3 to 8 (+1 at L4+), bolt
size raised 12x30 -> 26x64, and each bolt now GROWS up to 2.35x as it climbs. Thirty-one thin bolts
read as confetti; a small number of large lances that build as they travel reads as a charge payoff.

**TANKS AND TURRETS STAY ON DRIVABLE GROUND.** tankDrivable() returned TRUE whenever the mask was
missing or invalid — "fail open". That is exactly why tanks and turrets were seen crawling off the
water and the dam onto the sand: with no mask every position read as drivable, so the hard boundary
in tankhold/tankpatrol had nothing to enforce. Movement now fails CLOSED — an unproven spot is
never driven onto. Two call sites keep failOpen=true deliberately: spawn placement (so a unit is
never stranded unplaceable) and the road patrol's along-row drive (it was deliberately placed on
that row). Asserted both directions.

**VERIFIED, NOT CHANGED:** every campaign-map music reference is 'neonvelocity' (zero 'ironcage'
left in source) and the Snd loader is path-aware via assemble.py's "Snd music url-aware" step, so
the new track resolves. If it is still playing the old cue in Mike's build, it is a stale zip.

**STILL OPEN:** retina-hold + missile fire, and fullscreen. Retina currently pairs with the BOMB
key (keybind.bomb) while held, which is not the same as firing missiles — needs Mike to say which
button he means. Fullscreen has now had three attempts (JS twice, CSS once) and I do not yet know
what is still overriding it; guessing again would waste another pass.

---

## DROP 0724y — MAGMA COLOSSUS PRESENCE + MANIFEST SWEPT CLEAN

Build: 762 assertions, 0 errors. Manifest 5885 -> 5721 keys (164 dangling removed).

**LEVEL-2 BOSS — why it "looked terrible".** The attack pass fixed what it DOES; this fixes what it
IS on screen. It is a single 256px body with three damage states and no separate moving parts, and
it was pinned at a fixed position with no reaction to anything — so it read as a static image
pasted onto the arena rather than a boss. No art needed to fix that, only behaviour:
 · a slow lateral drift plus a heavy vertical "breath", clamped so it never leaves the screen
 · heat shimmer: embers rising off it constantly, heavier as it burns down
 · HP-gated damage smoke from 60% — AUTHORED nx_smoke frames, same standing rule as every other boss
 · at 25% it cracks and spits real explosions off the hull
 · shoulder muzzle flashes on every attack beat, so its shots visibly come FROM it
Asserted: 74 distinct drift positions over 4s, healthy boss emits zero smoke, damaged boss emits 58
authored puffs, critical boss throws explosions, and attacking lights the muzzles.
NOTE: whether the SPRITE itself is the problem is still Mike's call — this pass only removed the
"it just sits there" half of the complaint, which was objectively measurable.

**MANIFEST SWEPT.** All 164 dangling keys removed (registered, no file behind them). Verified first
that NONE were referenced by name anywhere in the source, so nothing could break. Groups were
crates 7-9, e5cc_/mbp_ boss component sets and stage/level boxes 6-9 — all pre-existing, none from
this session.
New permanent guard: the harness now walks EVERY registered key and asserts the file exists. A
manifest entry with no file is a promise the loader cannot keep, and 164 of them were hiding
genuinely missing art behind noise.

---

## DROP 0724x — CAMPAIGN CURSOR, FULLSCREEN CENTRING

Build: 765 assertions, 0 errors.

**FULLSCREEN — the real cause was CSS, not JS.** index.html had
`#screen-area canvas{width:100%;height:100%}`, which stretched the canvas to whatever shape the
box was and made every fitCanvas() sizing pass pointless. I had been fixing the JS twice while a
stylesheet rule quietly overrode it. The canvas is now absolutely positioned and centred with
`transform:translate(-50%,-50%)`, and fitCanvas owns SIZE ONLY — it no longer sets margins, which
were fighting the transform. Aspect stays locked at 480x512 whatever the window shape.

**CAMPAIGN-MAP CURSOR — red, and inside the box.**
It was drawn additively with a red SHADOW, but the cursor ART IS GOLD and additive compositing
cannot subtract yellow — so it stayed gold no matter what glow was put behind it. Now tinted
through a cached offscreen buffer with source-atop, which needs no getImageData (that is exactly
what broke this whole screen on file:// two drops ago) and preserves the sprite's alpha shape.
Position moved from an offset above the flag to the dead centre of the flag's own rect
(fx+fw/2, fy+fh/2), so it sits INSIDE the box.
Asserted that the map still renders under a tainted canvas with the new tint path in place.

**VERIFIED ALREADY LIVE (checked, not assumed):** stage-2 shootable scenery is gone, the launch
tiles textures at native size instead of scaling them, and the magma colossus has a real four-beat
attack profile that speeds up past half HP. All three confirmed in the built game.js.

---

## DROP 0724w — LEVEL-2 PURPLE, MG PELLETS, MERGED HELIX BURST

Build: 743 assertions, 0 errors.

**LEVEL-2 PURPLE EDGES — FIXED, BUT I DAMAGED THE ART FIRST AND HAD TO ROLL BACK.**
nst2_master carried 4149 px of a single flat value (165,15,170) — unfilled key. My first heal
masked the whole magenta FAMILY (r and b both above green, r~b) and hit 257425 px = 20% of the
image, because dark volcanic rock legitimately sits in that range. It flattened the master from
std 76.6 to 21.3 and destroyed the artwork. Restored from the last verified zip extract and redone
against the EXACT flat value only: 4149 -> 0, std still 76.6, art untouched.
LESSON: for a stage master, heal the exact key VALUE, never a colour family. Rock and lava live in
the same neighbourhood as the key and a family mask cannot tell them apart.

**MACHINE GUN** already matched the spec on inspection: L0 fires ONE pellet at the full 0.085 L1
cadence, L1 fires TWO at the same colour and per-pellet damage (~1.5x), L2+ keeps the existing
colour tiers. Verified rather than rewritten.

**HELIX BURST — MERGED.** The volley used to spawn pre-spread across 118px, which is exactly why it
read as the lasers being split apart. Every bolt now launches from essentially the same point and
the fan comes from VELOCITY as it climbs, so it bursts out of one mass of light. The merge ball
(built from the game's own lzr_ reels, blue -> purple -> green) was already in place; I had added a
second push and double-flashed it, caught by the 'ONE merged ball' assertion. Bolts carry
_pierceAll so the volley runs the full height of the screen.

**NOT DONE THIS PASS — being explicit rather than implying coverage:**
 - fullscreen centring still wrong for Mike
 - campaign-map cursor: must sit INSIDE the boxes and glow RED as a retina, not gold
 - liquids scaled up during the runway scenes
 - level-2 shootable obstacles to be removed
 - level-2 boss (magmacolossus) has no attacks and needs a real behaviour pass
These are queued, untouched, and none of them are claimed as fixed.

---

## DROP 0724w — MG REWORK, HELIX PIERCE/MERGE, LEVEL-2 FIXES, RED MAP CURSOR

Build: 743 assertions, 0 errors.

**MACHINE GUN, to Mike's spec.** L0 now fires ONE pellet at the FAST L1 cadence (0.085, was 0.14) —
speed is no longer what the first upgrade buys. L1 fires TWO pellets, same colour tier and same
per-bullet damage, sitting tight at 7px so it reads as the default gun doubled rather than a wide
row. L2+ unchanged. Asserted: 1 -> 2 pellets, identical damage and tier, double per-volley output.

**MAVERICK.** The flurry now carries _pierceAll so it runs the full height of the screen instead of
stopping on the first thing it touches. The burst MERGES before it spreads: a single bright ball
built from the laser art itself, ringed around its own centre and flashing blue -> purple -> green,
then the volley fans out behind it. The old version threw the strands apart immediately, which read
as the shot falling to pieces.

**LEVEL 2.** The MAGMA COLOSSUS had NO attack profile whatsoever — it fell through every branch of
bossAttack and never fired, which is why it "has no attacks, no nothing". Given four escalating
beats (magma fan / eruption ring / aimed lance / slam) that fire faster past half HP. Verified all
four actually produce bullets (9/14/3/7) and that they differ from each other.
Also removed the shootable scenery obstacles from stage 2 only — other stages keep theirs.

**LAUNCH LIQUIDS.** _region stretched every texture to full screen width, so the 128px liquid tiles
were ~3.75x upscaled during the runway scenes. Small square textures now tile at native 1:1 and
repeat across, matching the in-level tiler; wide plates still fill the width.

**CAMPAIGN MAP CURSOR.** Moved INSIDE the flag box and re-tinted RED with a pulsing lock ring, so it
reads as a targeting retina instead of another gold UI accent.

**STILL OPEN — NOT FIXED THIS PASS, AND I AM NOT CLAIMING THEM:**
 · FULLSCREEN centring. I changed fitCanvas in 0724r and Mike reports it is still wrong, so my fix
   did not address the real cause. The fullscreen branch in index.html sizes #game-frame itself
   (position:fixed, its own centring maths) and that path needs reading before touching again.
 · PURPLE EDGES on level 2. The manifest sweep found no key residue in the lava art, so this is
   likely a draw-layer artifact (additive blending or the liquid tint) rather than the source PNGs.
   Needs its own investigation rather than another guess.

---

## DROP 0724v — NEON VELOCITY + DEATHTRAP, AND A REAL MUSIC LEVEL BUMP

Build: 721 assertions, 0 errors.

**THE VOLUME COULD NOT BE FIXED IN CODE.** Snd sets `m.volume = c01(A.vol.music * A.vol.master)`
and both are already 1.0 — c01 clamps to 1, and an HTML5 media element cannot exceed 1.0. There was
no software headroom left at all, which is exactly why it stayed quiet however Mike set the sliders.
So the FILES were raised: +2.3 dB (~30% amplitude) across all 27 tracks, applied through a LIMITER
rather than a flat multiply, because several tracks (Iron Cage, Fierce Planes, crawling, untitled)
already peaked at 0.0 dBFS and a naive x1.3 would simply have clipped them into distortion. True
peaks now sit at or under -0.1 dBFS with the perceived level up.

**NEW TRACKS.** Neon Velocity -> the campaign map (replacing Iron Cage, 3 call sites).
Deathtrap -> level 6's stage theme.

**A PRE-EXISTING MUSIC BUG FOUND WHILE WIRING IT.** assemble.py step 26 had a replacement labelled
"stage4 music" whose anchor was `bg:'sky',    music:'stage'`. BOTH stage 4 and stage 6 are bg:'sky',
and the anchor's padded spacing only lined up with STAGE 6's row — so that step was setting stage 6
to level 4's track, and stage 4 was left on the generic 'stage' fallback and never had its own
music at all. Found because setting stage 6 to deathtrap removed the step's only match and the
build failed loudly.
Both now set explicitly in gamecode.js (stage 4 -> lvl4, stage 6 -> deathtrap) and the broken
assemble step is deleted rather than re-aimed. Asserted that stages 4 and 6 no longer share a theme
and that every music key any stage or screen asks for actually exists.

---

## DROP 0724u — THE PURPLE HALO: FOUND, FIXED, AND THE GUARD THAT MISSED IT

Build: 707 assertions, 0 errors.

**WHAT IT ACTUALLY WAS — and it was mine.** A full-manifest sweep (5721 files) found exactly ONE
file carrying a magenta halo: nmvh_helix, Maverick's helix laser, with 8084 semi-transparent
near-pure magenta pixels at alpha ~140 (r=255, b=255, g=129-181). I created it two drops ago: when
I keyed Mike's upload I "feathered" the key edge by multiplying its alpha by 0.55. That did not
REMOVE the backdrop — it turned it into a translucent magenta RIM. Every time the helix drew, that
rim glowed purple over whatever was behind it, including tanks and planes mid-fight.
Re-keyed properly: hard key, then any surviving magenta-DOMINANT pixel dropped as bleed, then alpha
forced binary so no semi-transparency can exist to become a halo. Result 0 semi-alpha, 0 magenta.

**WHY THE GUARD DID NOT CATCH IT.** audit_chroma only ever tested OPAQUE flat blobs >=100px. It was
structurally incapable of seeing a translucent rim — there is no opaque blob to find. A guard that
cannot fail on a whole class of defect is worse than no guard, because it reads as coverage.
Added a SECOND check for semi-alpha near-pure key bleed, and the harness now asserts it.

**TUNING THE NEW CHECK HONESTLY.** My first halo test flagged 240 files / 152k px — all of it real
art: Falva is the pink pilot, Yuri's retro sprites are magenta, the beams and pilot trails are
violet by design. Loosely-defined "purple" is not a defect. Tightened to require BOTH red and blue
pinned near maximum with green well below, which is the signature of un-removed #FF00FF and not of
anti-aliased pink art. That takes it to 31 files, worst 271px, all on Falva/orb art — i.e. noise,
against the 8084px real defect. Threshold set at 500px so a genuine rim fails the build and edge
anti-aliasing does not.

**THE DAMAGE-FRAME REPORT.** Swept every damage/destruction state directly. The magenta in frames
like nel_talon_d2 is 95px across 95 UNIQUE colours — anti-aliased spark art, not key residue (real
residue is 1-3 unique colours). Level masters and nsky6_par came back with 0 semi-alpha entirely.
So the purple Mike saw on deteriorating units was the helix rim drawing over them, not the unit art.

---

## DROP 0724t — DEATH FX ACTUALLY WIRED, EMPLACEMENT DRIFT, REAL SMOKE

Build: 705 assertions, 0 errors.

**THE HEADLINE: unitDeathFX WAS BUILT AND NEVER CALLED.** A previous pass wrote the whole
class-based death system — DEATH_CLASS (jet / tank / mini / boss), unit-sized primaries, ascendant
secondaries, EXPLODE_SCALE dropped from 1.9 to 1.15 — and even wrote tests for the pieces. But the
enemy death path still called explodeAircraft()/explode() directly, so NONE of it ran in game.
That is exactly why Mike still saw giant death sprites and a turret dying like a jet. The tests
passed because they tested the parts in isolation and never asserted that the death path USES them.
Now wired, and there is an assertion that updatePlay actually calls unitDeathFX — the thing that
would have caught this originally.

**UNIFORM DEATHS BY CLASS**, sized to the unit and scaling with it:
  jet  3 secondaries, shake 4   ·  tank 4, shake 7 (heavy rolling ground fireball)
  mini 6 secondaries, shake 10  ·  boss 10, shake 14
Every secondary RISES out of the wreck (asserted vy<0 on all of them) so the fire climbs like a
real explosion rather than popping flat. Measured: an 18px turret now produces an 18px blast.
The atomic/atom set is asserted absent from every death class and unit deaths never call atomBlast.

**EMPLACEMENT DRIFT.** emplaceStep fell back to the UNIT'S OWN vy when the terrain delta was not
yet measurable — so different emplacements fell back to DIFFERENT speeds and crept apart from each
other and from the ground they are bolted to. Now every emplacement falls back to the same shared
cached figure. Asserted: two emplacements with wildly different vy get an identical step, and it
still fails open rather than freezing a turret mid-air.

**SMOKE.** The last particle-blob smoke path (flat '#1c1c1c' circles, which read as CSS dots
against 16-bit art) now emits authored nx_smoke frames, matching what the Overlord-X tail plume
already did.

**TEST QUALITY.** The boss-smoke intensity check measured PEAK CONCURRENT puffs, which is throttled
by lifetime and the 240 cap and is a poor proxy — it started failing for the wrong reason once
smoke became real frames. Rewritten to measure the SPAWN RATE over a fixed window (45% HP -> 20% HP).
Also removed a string-matching assertion that was tripping on my own comment: the SIXTH time that
trap has appeared, and the behavioural assertion beside it already covered the same ground.

---

## DROP 0724t — UNIT DEATH FX, EXPLOSION SIZING, BOSS SMOKE, EMPLACEMENT SCROLL

Build: 684 assertions, 0 errors.

**THE OVERSIZE BUG — found, and it was one number.** Explosions were DRAWN at 1.9x (and 1.85x on
the fallback path) the requested size. Every death bloomed into a sprite far larger than the unit
that produced it. Replaced with a named EXPLODE_SCALE = 1.15, so a blast COVERS its unit and
overhangs slightly — which is what a hit should look like, and nothing more. A 20px turret now
gets a ~20px blast; asserted.

**ONE RULE FOR EVERY DEATH.** unitDeathFX(e) with deathClassOf(e) picking the family, so no call
site has to remember and two units of the same class can never die differently:
    jet   -> nx_fire0/1/2   quick bright airburst      3 secondaries
    tank  -> nex_fireball   heavy rolling ground fire  4 secondaries
    mini  -> nx_big         big sustained blast        6 secondaries
    boss  -> nx_big         same family, longer beat  10 secondaries
The blast is sized from the UNIT (max of w/h), never a constant.
ATOMIC FAMILIES ARE NOT USED — asserted, so Mike's atomic weapon keeps its own visual language.

**ASCENDANT SECONDARIES (the Genesis look).** Each class scatters smaller blasts across the hull
that DRIFT UPWARD while they wait to go off, so the fire climbs out of the wreck instead of sitting
flat. Asserted that every secondary has negative vy and that pending ones actually move up.

**BOSS SMOKE NOW USES THE SMOKE FRAMES.** The damage plume was pushing tinted particle circles
('#0e0e0e' blobs) — CSS dots, exactly what Mike called out. It now emits nx_smoke (authored 8-frame
puff) through the existing smokeTrails system, and damage plumes RISE rather than only drifting
down with the map.

**TURRETS WERE SLIDING.** Emplacements advanced on a hardcoded vy (0.34) that had no relationship
to how fast the ground was actually moving, so they drifted against the terrain they are bolted to.
They now ride a shared per-frame figure derived from the levelSrcY() delta — computed once per
frame so every emplacement gets the identical number and they can never separate from each other
(asserted: two turrets stay locked as the ground scrolls).
FAILS OPEN: if the scroll can never be measured, emplaceStep falls back to the unit's own vy. A
frozen turret hanging in mid-air would be worse than the sliding this replaced.

**MY OWN FIX HAD A BUG, AND THE TEST CAUGHT IT.** The first version gated the per-frame calculation
on a `frameCount` global. Where that global does not exist, EVERY CALL counted as a new frame — so
the first turret to ask each frame saw the real ground delta and the second saw zero, and the two
drifted apart (measured 13.3px over 2 seconds). Rewritten to key off whether levelSrcY() actually
MOVED: the first caller in a frame refreshes the figure, every later caller gets the cached value.
The assertion that found it is now stated as the invariant itself — every emplacement asking in the
same frame receives the identical step — rather than as 120 frames of full-game simulation, which
was itself flaky for unrelated reasons (units get culled mid-run). Eight consecutive clean runs.

---

## DROP 0724s — WEATHER v2: FIREWAVE (L2), SNOWSTORM (L3), STORM (L6)

Build: 661 assertions, 0 errors. The 0724c weather was cosmetic ambience; this is three real event
systems with consequences.

**STAGE 2 — FIREWAVE.** nwarn_alert flashes on ONE side of the screen with a pulsing edge band, so
the side is unmistakable. FIRE_ALERT = 2.6s later a firewave enters FROM THAT SIDE, animating
through nwf_fire 8f and SCALING 0.55 -> 1.70 as it comes, arcing down like a breaking wave. Getting
caught routes through playerHit() — the same path as every other lethal contact, so shields,
invulnerability and the death sequence all behave normally instead of a private death path.
Sounds: lockAlert on the warning, firewall on the wave.
**BUG FOUND BY THE COLLISION TEST:** travel was `f.x += f.side*...`, but `side` is where it ENTERS
FROM — so the wave accelerated further off the edge it started on and NEVER CROSSED THE SCREEN.
Now `-=`, and there is an assertion that it actually travels across.

**STAGE 3 — SNOWSTORM.** Held back entirely until subBossDone. Then the level DIMS (up to 42%,
tied to the ramp so it is a slow fade, not a cut) while snow builds from 0 to 74 particles over
SNOW_RAMP = 6s, with blizzard/snowburst gusts once it is past a quarter strength. Asserted: nothing
at all before the miniboss, full storm after.

**STAGE 6 — STORM.** Rain fades in from the instant the stage starts — you are already in the sky —
reaching full over 2.5s. Lightning now drives ITSELF on a 2.2-6.5s timer at a random on-screen
position, using the real bolt art (sheet / chain / forked), with a screen flash, shake, thunder
(crackle) and a kick to the existing l6Wx.flash so the old storm system stays in sync. Measured:
9 strikes over 40s at differing positions.

**Care:** stages 1, 4, 5, 7 and 8 still have no weather, asserted, so none of this leaks.

---

## DROP 0724r — CHARGE = ENERGY ORBS, AND THE FULLSCREEN FIT

Build: 639 assertions, 0 errors.

**CHARGE VISUAL.** The charge drew two counter-rotating BEAM sprites (nhb_blue / nhb_pink /
nhb_green) whipping around the ship — which read exactly as Mike said: lasers spiralling. Replaced
with the charge art the pack already ships and nothing was using: nchg_sph_ (8f) as a swelling
energy CORE under the ship, and nchg_orb_ (8f) as a ring of orbs wheeling INWARD to the nose,
tightening and accelerating as the charge tops out. Asserted by behaviour: orbs spawn, more gather
as it builds (4 -> 7), and mean orbit radius falls (40.4 -> 28.1) — they really do draw in.

**FULLSCREEN — two bugs stacked, and the second one was hiding the first.**
assemble.py replaces fitCanvas TWICE. Step 26 ("supersample setup") installs one version; step 27
("cabinet-aware fitCanvas") then replaces it again, and step 27 is what actually ships. My first
attempt fixed step 26 — invisible, because step 27 overwrote it, and it also broke step 27's
end-anchor. Fixed properly in step 27.
The real defect: step 27 set cv.style.width/height to #screen-area's clientWidth/clientHeight
EXACTLY and returned. Whenever that box's aspect did not match the game's 480x512 the picture was
stretched, and nothing ever re-centred it, so fullscreen sat off-centre AND distorted.
Now: fit the largest 480x512-proportioned rectangle inside the host, then centre on both axes.
Also hooked fullscreenchange / webkitfullscreenchange / orientationchange, since entering
fullscreen does not always fire a resize. Verified across 1920x1080, 2560x1080 (ultrawide),
1280x1024, 800x600 and 480x512 — aspect holds at 0.938 in every case.

**FLAKY TEST FIXED (pre-existing).** 'cook-offs walk outward' asserted `at100 < 22`, but the
secondaries are scheduled with random delays and on an unlucky seed all 22 legitimately land inside
1.00s — it failed roughly 1 run in 4. Re-stated to assert the PROGRESSION (first beat is a genuine
subset, count never decreases) instead of an arbitrary ceiling. Six consecutive clean runs.

**Note:** the string-vs-behaviour trap appeared for the FOURTH time — an assertion checked the draw
functions for 'nchg_' when the key is built inside a helper. Rewritten to call the resolver. This
keeps recurring, so it stays in the standing notes: assert what the code DOES.

---

## DROP 0724q — MAVERICK HELIX OVERDRIVE (glow -> burst -> flurry)

Build: 623 assertions, 0 errors. Manifest 5885 keys (+1: nmvh_helix).

**BEFORE:** a fully charged helix just flew off the top of the screen and bloomed once it exited.
**NOW — three beats, full charge only** (a half charge still behaves exactly as it did):
  TRAVEL  the lance climbs as before.
  GLOW    at HELIX_LINE (52% of screen height) it STOPS and charges. A bottom-to-top wash runs up
          the lance, green washing into WHITE as it tops out, with shake ramping. HELIX_TELL =
          0.42s of unmistakable warning before it lets go.
  BURST   flash, shake, the existing bloom at ~2x scale, and it detonates.
  FLURRY  22 + 3*level bolts (31 at L3) race the rest of the way up and out at vy < -14.

**DAMAGE MODEL — the part that needed a real decision.** The flurry DELETES ordinary enemies
(dmg 9999): that is the payoff for holding a full charge. Bosses are NOT deleted — they take heavy
but explicitly CAPPED damage via a new `_bossDmg` field (HELIX_FLURRY_BOSS = 90 per bolt). Measured
in test: 2340 damage to a boss, boss survives. A charge attack should feel devastating without
trivialising a boss fight.
`_bossDmg` was deliberately built as a GENERAL mechanism and wired into both the boss and the
sub-boss collision paths, so any future one-shot-class weapon can use it instead of each one
re-inventing the rule.

**ART.** Mike's helix image was chroma-keyed (49.7% magenta backdrop), edge-feathered, cropped and
registered as nmvh_helix — 0 residual magenta. It drives the lance through beats 1-2. The flurry
deliberately reuses the game's existing lzr_ laser reels rather than inventing a new effect, which
is what Mike asked for: "a bunch of our laser graphics".

**Care taken:** the old age-based bloom (b._age > 1.05) is now scoped to HALF charges only, so the
full-charge path cannot bloom twice — the line/glow sequence owns it end to end.

---

## DROP 0724p — MENU CURSOR CONSISTENCY (mode select + options)

Build: 610 assertions, 0 errors.

**THE GAP.** Every other menu drew a pulsing cursor either side of the selected item and flashed
its label white. MODE SELECT (the screen you land on after NEW GAME) and OPTIONS did neither —
mode select had only a shadow/border change, options had a flat '> ' text caret. Next to the rest
of the game they read as dead screens.

**FIX — one shared helper, not two more copies.** menuSelMark() + menuSelWhite() now serve every
menu, so the treatment cannot drift apart again. The marker prefers the animated nss_cursor_ reel
(8 frames, mirrored on the right side), falls back to the drawSelArrow glyphs, then to text
triangles. Applied to mode select and to options.

**THREE THINGS THE TESTS CAUGHT, ALL WORTH RECORDING**
1. I EDITED THE WRONG FUNCTION. There are two drawOptions — one in gamecode.js and the LIVE one in
   patches.js (plus drawOptionsLegacy). My first edit went to the dead one and the assertion for
   'OPTIONS now draws the cursor' failed, which is exactly what that assertion is for. Re-applied
   to the patches.js version.
2. A CRASH I INTRODUCED. menuSelMark trusted XART.rdy() and then read naturalWidth. rdy() can be
   true while the image is not yet measurable, and every menu now calls this — so it is guarded and
   degrades to the arrow glyphs instead of throwing. A helper this widely shared must never be the
   thing that kills a screen.
3. HARNESS GAPS. The canvas stub had no arcTo, which the real options screen uses, and the frozen
   performance.now() made the white-pulse test sample one value 40 times. Both fixed in the harness
   (arcTo/ellipse/roundRect stubbed; the pulse test drives the clock) rather than by weakening the
   assertions — otherwise the render test could never have caught a crash on that screen at all.

---

## DROP 0724o — CAMPAIGN MAP: "one flag, then completely dead"

Build: 598 assertions, 0 errors.

**CAUSE — a tainted canvas, and a function that lost its input handler to the throw.**
The flag palette-swap called getImageData() on a canvas it had just drawn an image into. Drawing an
image TAINTS a canvas; on a file:// page (how index.html is opened) getImageData then throws
SecurityError. That call was unguarded.
Stage 1 is the AVAILABLE flag and takes the plain draw path, so it rendered. Stage 2 is LOCKED and
takes the gray palette-swap path — it threw, and the throw escaped drawStageSelect entirely.
The input handling for the whole screen lives at the BOTTOM of that same function, so it never ran.
That is why the map was not merely missing flags but completely unresponsive: one flag, then dead.

**FIX — two layers, because either alone leaves it fragile.**
1. TAINT GUARD: try the pixel ramp; if the canvas is tainted, fall back to a source-atop composite
   tint that needs no pixel readback at all. Same look, works from the filesystem, and untainted
   pages still get the nicer luminance ramp.
2. PER-FLAG GUARD: each flag draws inside its own try/catch. One bad flag must never cost the
   player the entire screen — the input handler is always reached no matter what happens above it.

**VERIFIED BY REPRODUCING THE ACTUAL FAILURE.** The test forces getImageData to throw SecurityError
exactly as file:// does, then asserts the map survives 10s, all 8 flags place (gray ones included),
the boot sequence completes, and FIRE actually deploys to the selected stage. I also demonstrated
the ORIGINAL code shape throwing on a tainted canvas, so the reproduction is the real mechanism and
not a test that happens to pass.

**Note:** the flag art was never at fault — all four states (av / lock / done / hi0-hi1) exist for
all 8 stages. Two other getImageData sites (the land mask and the tank drivability mask) were
already inside try blocks and are unaffected.

---

## DROP 0724n — TWO REAL BUGS FROM MIKE'S SCREENSHOTS

Build: 587 assertions, 0 errors. Both root-caused, neither patched around.

**BUG 1 — THE SHIP JERK.** _drawPlayerCore was alternating the airframe between 'ship_<pilot>_t'
and 'ship_<pilot>_pv2' every ~90ms (~11Hz) whenever the ship was flying level, i.e. almost always.
My own comment on that code called it "ANIMATED THRUSTERS". It was not: those are two DIFFERENT
poses at different dimensions, so a large fraction of the ship's pixels changed twice a second and
the whole airframe visibly snapped back and forth.
FIX: the body holds ONE frame. The thruster animation was ALREADY there and already correct — the
ntr_ trail, 8 authored frames, throttle-reactive, drawn a few lines above. Animate the flame, never
the airframe. Asserted the alternation is gone and the trail is still driven.
Swept for the same pattern elsewhere: it was unique to the player. Enemy craft pick frames from
live STATE (volcanic cast, L8 elites) or play authored reels (L6 jets), which is correct.

**BUG 2 — THE STAGE-1 MINIBOSS WAS INVULNERABLE.** The Jungle Siege Crawler spawns at y=-120 and
flies in to ty=150. crawlerUpdate runs at the TOP of updateSubBoss, before the entry lerp, and it
captured its patrol anchor (_cy0) from the OFF-SCREEN spawn row. Its patrol band then fought the
entry lerp for control of b.y; the two balanced at ~145.6, which never satisfies the |y-ty|<2
arrival test, so b.enter stayed TRUE FOREVER.
Every hit test in the game gates on !subBoss.enter -> the crawler could never be damaged. Its own
guns gate on the same flag -> it never actually attacked either. It just sat there, exactly as the
screenshot showed.
ROOT FIX: entry OWNS y. crawlerUpdate returns early while b.enter is true, so the patrol anchors
where the unit actually settled (verified _cy0 = 150, not -120).
SAFETY NET: arrival now also completes on a hard timeout. A stuck entry flag produces an
invulnerable AND mute boss — a silent, catastrophic failure — so it must never be able to hang
again even if some future unit can never reach its target row.
SWEPT THE CLASS, not the instance: all 8 sub-bosses across all 8 stages are now asserted to arrive.
Measured on the crawler after the fix: 225 -> 185 hp from a burst, and 17 rounds fired back.

**Note on how this was found:** I reproduced both headlessly before touching anything rather than
guessing from the screenshots. The probe printed 'enter=true' after 6 simulated seconds, which
pointed straight at the gate every hit test shares.

---

## DROP 0724m — STAGE-8 ROSTER AUTHORED + THE RIVAL SWITCH

Build: 578 assertions, 0 errors. Net -307 lines (dead dogfight removed).

**STAGE 8 — "FURIOUS DEATH".**
WAS a clip show: on a SPACE background it re-spawned jungle jetflybys, ground mechs, racers,
bombers, topguns, sideswirls, turdrones, minicarriers, shielddrones — units from every other stage.
"Everything the game has" is not an identity, it is the absence of one, and it made the finale feel
like a highlight reel of levels already beaten.
NOW: THE VOID CLOSES IN, three escalating movements, each ending on an elite:
  I   0-20s  ORBITAL SCREEN  needle / crescent / hauler / oracle — the deep-space cast is the only
                             one that belongs on this background
  II  20-40s THE CARRIERS    hellwing death carriers anchor the middle; mines and octos deny space
  III 40-60s ALL FOUR        every L8 elite on screen at once, overlapping into the boss
Asserted: 12 named out-of-stage units are GONE, all 4 elites + el_hd appear, no VW* remains, and a
150s soak sees all four elites and the full orbital cast with nothing non-finite and no NaN bullets.

**THE RIVAL SWITCH — flagged for three drops, now closed.**
The free-flight dogfight is DELETED, not bypassed: updateRivalFight (235 lines) and drawRivalFight
(72 lines) removed outright. The rival 'fight' phase now drives the RACE, using the main game's
movement feel and shooting path; player bullets clear obstacles and an obstacle you fail to clear
costs race time. End-to-end test plays a full race through the real update path and lands in the
choice phase.
UNCHANGED deliberately: the dialogue script and the SPARE / SHOOT THEM DOWN branch. The race hands
into the exact same 'choice' phase the duel used, so that whole path is untouched, and sparing
still banks the callable ally.

**TWO THINGS THE DELETION SURFACED**
1. assemble.py had an anchor expecting TWO copies of the player fire-cd path — the dogfight carried
   its own duplicate of it. With the dogfight gone there is genuinely one. Fixed by correcting the
   count IN assemble.py, never by patching generated output: that region is assemble-owned and a
   direct edit would break the anchor silently.
2. My first "the dogfight is unreachable" assertion FAILED against my own removal comment, which
   names the deleted functions. Exactly the same string-vs-behaviour trap as the level-6 jets one
   drop earlier. Rewritten to actually call the function and expect a throw. Third time this class
   of mistake has appeared: assert what the code DOES, never what the source text says.

**Also fixed:** my race end-to-end initially timed out at 45s and looked like a stall. It was not —
eating obstacles slows a racer to as low as 0.55x, so a hit-heavy run legitimately runs long. The
time penalty working, not a bug. Loop extended and the penalty is now asserted explicitly.

---

## DROP 0724l — STAGE-1 WATER SWAP + LEVEL-6 JET ANIMATION AUDIT

Build: 532 assertions, 0 errors.

**STAGE-1 WATER — swapped on Mike's explicit go-ahead.** fx_water -> nlq2_water, the seam-healed
128px set (wrap seam measured 0.00 on BOTH axes after healing) at true native 1:1, replacing a
legacy bed that was being crushed to ~23px by the old tile 0.18.
The never-touch rule still holds for EVERYTHING else on stage 1: master, roster and font are
unchanged, and that is now asserted so it cannot drift. Only the liquid moved.

**ANIMATION AUDIT — and a false positive I caught before acting on it.**
I scanned for registered multi-frame sets with no code reference, looking for unwired animation.
It reported the six level-6 jets (fang / lance / raptor / talon / warden / widow) as never
referenced — 35 frames each (idle 6, bank-L 5, bank-R 5, damaged 3, death 8, launch 8), 210 frames
total, apparently dead.
They are NOT dead. drawL6Jet builds its keys with template literals — n6j_${jet}_${state}_${frame}
— so a plain text search for the family name cannot see them. I nearly rebuilt a working system.
Verified by BEHAVIOUR instead and it is correct: jets spawn with the _h6 flag, _drawEnemyInner
routes them into the animated path, banking follows real vx, damaged triggers at <=45% hp, and the
8-frame death reel plays off the dying clock rather than looping.
LESSON, same shape as the nwx_ clobber in 0724c: a text search over source is not a behaviour
test. Assert what the code DOES, not what it says.

**Also corrected:** an assertion of mine referenced drawEnemy when the dispatch actually lives in
_drawEnemyInner. Fixed rather than loosened.

**Remaining animation work is genuinely blocked on art, not wiring:** ANIMATION_NEEDS.md's
"baked frames only" list (dam-breaker, magma-colossus, cryo-behemoth and ~11 more) needs separate
rotor/turret assets authored before they can be smoothed — the Overlord-X rotor treatment
(72 frames at 5 degrees) is already built and shipping. Emotion portraits still await Mike's
re-upload per TODO_PORTRAITS.md.

---

## DROP 0724k — LEVEL-1 RUNWAY, OUTBOUND CINEMATIC, FULL RUNWAY SEQUENCE, LEVEL-4 CONSOLIDATION

Build: 520 assertions, 0 errors. Manifest 5884 keys.

**LEVEL 1 RUNWAY.** Now launches on the existing legacy 'runway' strip (360x955 jpg). It is not an
800x1000 keyed plate, so it gets its own 'legacy' marker rather than being faked into the nstXX_
triad naming — it resolves the MAIN part only and has no approach/exit siblings to invent.

**OUTBOUND CINEMATIC (GS.OUTBOUND) — the missing half of the sequence.**
Two beats: CLIMB (accelerate up and off the top, still over the level you just cleared) then
FOLLOW (camera keeps going and the N->N+1 connector scrolls through). Then the normal per-stage
launch takes over with its own 3-2-1-GO. Asserted that the climb draws the LEVEL MASTER and that
_liquidFrame appears nowhere in the outbound — flying off into liquid was the actual complaint.
Pairs with no connector art (1>2, 2>3, 5>6) still get the CLIMB and simply skip the follow beat
rather than showing a missing plate.
GS.OUTBOUND was added through assemble.py's enum + dispatch replacement strings, NOT by editing
generated output — that region is assemble.py-owned and direct edits break anchors silently.

**FULL RUNWAY SEQUENCE.** approach -> main -> exit, in the order you actually fly it. Stages 4 and
7 have all three plates; stage 1's legacy strip fills the exit band with its main tile.

**LEVEL-4 LEFTOVERS — a duplication I caused, found and fixed.** nst4b_tr_in and nst4b_tr_out were
BYTE-IDENTICAL to ncon_3_4 and ncon_4_5: I registered the same two plates twice under different
names in drops 0724f and 0724i. Consolidated onto the canonical connector files and deleted the
redundant copies, which also cleared 4 dangling keys (168 -> 164).

**STILL UNFINISHED, EXPLICITLY:** the rival phase machine still drives the OLD dogfight. The race
core, art and ally are in and passing, but in-game the duel would still play. ~250 lines of dead
dogfight code remain resident. This is the one place where what ships does not match what was
asked for, and it stays top of the list.

---

## DROP 0724j — RIVAL DOGFIGHT REPLACED BY RIVAL RACE + SPARED-RIVAL ALLY

Build: 500 assertions, 0 errors. Manifest 5815 -> 5884 (+69).

**THE PACK DECIDED THE DESIGN.** Its courses are literally named rival-02-03 / rival-04-05 /
rival-06-07 — exactly the three encounters Mike asked for. 3 variants each (open-air-a,
open-air-b, tunnel), 800x1000 sections. 8 airborne objects, each a 4-frame 256x192 atlas:
6 breakable obstacles (intact/damaged/breaking/debris), 1 pickup crate (sealed/glint/opening/
empty), 1 checkpoint beacon (red/amber/green/finish_flash).
Tunnel variants are NOT named "section" — they are exterior-entry / interior-run / exterior-escape,
which my first extractor silently skipped (3 courses came back with 0 sections). Caught and fixed.

**RACE, not duel.** Obstacles have hp 2: one hit damages, a second breaks, so you must COMMIT to
clearing a lane rather than brushing it. Eating one costs race time. The RIVAL races the same
course under the same rules — it shoots what is dead ahead, slides around what is not, and wrecks
itself when it misjudges. Asserted that it is NOT immune: a rival that never fails is not a race.
Pack implementation notes followed: side walls only ("never treat the art as two fixed lanes"),
gates drawn as a PAIR ("duplicate the beacon on both sides"), gates not shootable.

**THREE encounters** after stages 2, 4 and 6. Asserted no encounter fires on any other stage, and
that every encounter starts a course that actually has sections registered.

**KEPT:** the dialogue script and the SPARE / SHOOT THEM DOWN choice, untouched.

**NEW — SPARED RIVAL BECOMES A CALLABLE ALLY.** Sparing banks that pilot. Calling them in during
a later stage: they arrive with a line, fly loose formation off the player's wing, put fire
downrange for exactly ALLY_DUR = 30s (measured 6 shots/sec), then sign off with a parting line and
climb out. One call per spared rival per run — a favour, not a turret. A thin HUD bar shows the 30s.

**NOT DONE, AND I AM NOT CLAIMING IT:** "start adjusting the overall gameplay" was too vague for me
to act on safely, so I did not guess — that needs Mike to name what feels wrong. The OLD dogfight
code (updateRivalFight / drawRivalFight, ~250 lines) is still resident and still referenced by the
rival phase machine; the race core, art and ally are in and tested, but the phase machine has not
yet been switched over to drive raceUpdate instead of the dogfight. That is the next pass.

---

## DROP 0724i — PER-STAGE SEQUENCE KIT (runway / connector / sky launch)

Build: 473 assertions, 0 errors. Manifest 5808 -> 5815 (+7 plates).

**ART INVENTORY FIRST — this is the honest headline.**
Inventoried every pack before designing anything:
  RUNWAY triads (approach/main/exit, 800x1000): stage 4 and stage 7 ONLY.
  CONNECTORS (800x1000): 3>4, 4>5 (Lvl4 pack) and 6>7, 7>8 (Lvl7 pack) ONLY.
  NOT DRAWN ANYWHERE: runways for stages 1,2,3,5,6,8 · connectors 1>2, 2>3, 5>6.
The Rival pack does ship raw magenta source sheets (runways-source / transitions-source,
1536x1024, ~46% magenta) holding 8 runway cells and ~6 transition cells — but those are ~240x492
RIVAL-MODE cells, not 800x1000 world plates. Slicing them into stage plates would be guesswork
about intent, so they were left alone rather than forced.
Mike had already named the fallback — "use our new water tiles again at regular size" — so stages
without a plate tile their own upgraded bed at native 1:1, which drop 0724f made genuinely native.

**THE BACKWARDS SHOVE IS GONE.** Mike: "dont push our player backwards or do anything weird."
Found it: drawLaunch had a `reverse` phase adding up to -300px of travel right before the
countdown. Replaced with a `settle` phase that simply comes to rest. Asserted BEHAVIOURALLY (no
code path adds negative distance) rather than by string match — the first version of that
assertion failed against my own explanatory comment, which is a good reminder that string-matching
a source file is not a behaviour test.

**FLOW, every stage:** stage card (the screen face stays) -> connector for N-1>N if one exists ->
runway plate or bed -> lift off and accelerate -> bed at speed -> level entrance -> 3-2-1-GO ->
play. The player holds position through the countdown and the game starts at the GO marker.

**LAUNCH BEDS UPGRADED.** The launch was still drawing the OLD ASSETS.water / ASSETS.lava frames
even after drop 0724f replaced the in-level liquids. It now pulls the seam-healed nlq2_* beds, so
the intro and the level itself finally show the same water.

**STAGE 6 — the stated exception.** Runway -> SKY. It never brakes into ground: speed cap x1.35
and the parallax cloud deck thickens as it climbs, 1 cloud pass low up to 4 near the top, each at
a different parallax rate. Asserted as the only sky launch of the eight.

**STILL OPEN:** the stage-CLEAR fly-off still uses the legacy exit; the connector currently plays
on the INBOUND side of the next stage's launch rather than as a separate outbound cinematic. That
reads correctly (you fly out of one level and into the next) but it is not yet the two-part
"fly off screen, then follow" Mike described. Flagging rather than claiming it.

---

## DROP 0724h — LEVEL 4 ROUTES FLIPPED + ROAD PATROL + PRE-DEFINED JET WAVES

Build: 453 assertions, 0 errors.

**FLIP.** The engine scrolls srcY from the image BOTTOM up to row 0, so the top row is where a run
FINISHES. Measured road coverage on nst4b_master: 23.3% in the top 200 rows, 50.5% in the bottom
200 — the run was ending on the sparse approach and starting on the built-up base. Flipped, so both
routes now finish at the base. Asserted end-road > start-road on both.
Flip-safety was CHECKED, not assumed: a vertical flip destroys art that carries baked directional
lighting. Vertical luminance-step bias measured 0.999 (horizontal 1.007 for comparison) — no
consistent drop-shadow direction, so this top-down airbase flips cleanly. The flip genuinely
reorients (89.5% of pixels move by >12), it is not a symmetric image.
master, remix and boss arena all flipped together so the approach reads consistently. Regenerated
from the pack source (and recomposed for the remix) rather than flipped in place, so re-running is
idempotent instead of flipping back and forth.
The remix is composed FIRST and flipped ONCE — flipping the plates individually and restacking
would have silently reversed the authored 1>2>1>2>3>4 progression.

**ROAD PATROL (new `tankpatrol` pattern, `roadtank` kind).** `tankhold` planted a tank on the
terrain and let the scroll carry it — it never drove. `tankpatrol` rides the same terrain anchor but
moves its LEVEL-space row, so it drives the road up-screen and back, reversing at the end of its
beat OR when the tarmac runs out. It also drifts toward the player's lane while patrolling.
Measured over a 15s headless run: 172px of level-space travel, 2 direction reversals.
It checks drivability on BOTH axes so it can never leave the tarmac, and fails OPEN when the mask
is unavailable so a tank never freezes on an unfamiliar master.
Stage-4 ground armour at 8s / 23.5s / 37.5s converted to road patrols, plus a new pair at 40s so
the base end is defended — which is the point of flipping the route.

**JET WING ON THE PRE-DEFINED PATTERNS.** The level-4 jets were on loose ad-hoc sine/weave/dive.
Now: f16 -> aiWaveColumns · m29 -> aiWaveSplit · su27 -> aiWaveCross · f15 -> aiWaveLoopCurved ·
hwk -> aiWaveSweep mirrored · shn -> aiWaveCross · j20 -> aiWaveRush (f18/f22 already were).
Asserted: zero stage-4 jets left on an ad-hoc pattern. el_iv IRON VULTURE keeps its own line —
an elite should not fly the standard sheet.

---

## DROP 0724g — LEVEL 4 REMIX ROUTE

Build: 435 assertions, 0 errors. Manifest 5807 -> 5808 (+1: nst4b_remix, composed).

**MIKE WAS RIGHT, AND THE MEASUREMENT SAYS WHERE.**
Road-column agreement across a join, all 16 ordered pairs:
          ->s1   ->s2   ->s3   ->s4
    s1    92.5  100.0   88.0   77.8
    s2    90.5   88.0  100.0   79.8
    s3    76.8   77.8   79.8  100.0
    s4    54.2   54.2   56.8   67.0
 · The shipped order scores 100/100/100 — because the plates do not abut, they OVERLAP by 128px
   and those bands are BYTE-IDENTICAL (diff 0.0000). nst4b_master was seamless by construction.
 · The three Gameplay seam strips ARE those bands, found in the master at y=872/1744/2616 with
   diff 0.00. They are the artist's transitions for THAT order, not generic bridges.
 · So the roads only break once you REORDER — exactly what Mike spotted. A remix cannot shuffle.
 · sec4's tail scores 54-67% into everything: it is the level end and was never drawn to lead
   anywhere. Any good route keeps it last.

**ROUTE CHOSEN BY SEARCH, NOT BY SHUFFLE:** 1>2>1>2>3>4, 800x5360 (48% longer than stock).
Constraints: all four plates used, no immediate repeat, sec4 last. Four of five joins land on
100% road continuity; the one join the artist never drew (2>1) holds 90.5%.
First attempt scored 1>1>1>2>3>4 highest — a plate joins ITSELF at 92.5%, so the optimiser happily
proposed walking one corridor three times. Constraints added.

**TRANSITION: ordered dither (8x8 Bayer)**, matching the artist's own naming. It PICKS the
outgoing or incoming plate's pixel per position and never averages them, so the result stays crisp
and palette-exact — alpha-blending two 16-bit tilesets produces off-palette mud. Every output pixel
is one of Mike's.

**THE VERIFICATION WAS WRONG TWICE BEFORE IT WAS RIGHT.**
 1. First metric compared peak row-step to the GLOBAL median. Dithering raises local row variance
    by design, so it punished the technique for being the technique.
 2. Second metric compared peak to the band's own median and still failed at 21.42x — until I
    measured the SHIPPED master the same way and got 10.61x / 12.58x / 21.42x. Those peaks are
    ARTWORK (road markings, building fronts) sitting exactly at the join rows. An absolute
    threshold would have failed Mike's own master.
 The gate now compares against the shipped master as the definition of "clean". Remix worst
 21.42x == shipped worst 21.42x.

**DEFAULT UNCHANGED.** Stage 4 runs the stock route; `run.remix4 = true` takes the long one.
Left un-triggered on purpose — which run gets the long route (bonus, warp, second loop) is a
design call, not a side effect of a composition pass.

---

## DROP 0724f — ALL LIQUIDS UPGRADED, TRUE NATIVE TILING, LEVEL 4 MAP

Build: 423 assertions, 0 errors. Manifest 5748 -> 5807 keys (+59).

**THE TILER WAS LYING.** drawAnimTerrain's own comment read "draw the texture at its EXACT native
pixel size — never stretched or scaled", and the very next line multiplied by cfg.tile, which
_levelCfg passed as 0.18-0.22. A 128px liquid was rendering at ~25px and the 256px sludge at ~56px:
mushy, over-repeated, and not the square tiles the art was drawn as. Every liquid stage now runs
tile:1 = true native squares.
Two harness assertions had LOCKED THE BUG IN ("water tile scale is fine (<0.4)") — they were
asserting the downscale. Both inverted to require exactly 1.

**THE PACK ART DID NOT WRAP.** Measured before touching anything: surface tiles had wrap seams of
18-35 against internal baselines of 6-11, i.e. 3-5x a normal adjacent-pixel transition. Tiling
natively would have shown a visible grid.
The project's existing roll-and-heal FAILED on these: water 34.9 -> 21.5, and lava's V-seam got
WORSE, 24.5 -> 25.3. Cause: these tiles carry a luminance GRADIENT across them, so the wrap
mismatch is inherent to the content and roll-and-heal never touches the outer edge — it only fixes
a local artifact moved to the centre.
Fix: force both wrap edges to their shared mean and feather the correction to zero inward. The
wrap becomes EXACT BY CONSTRUCTION. Result: every seam 0.00, on all 8 families.
Per-axis, deliberately: the falls already wrapped horizontally (H-seam 0.00 exactly), so only
their vertical axis was healed. No edits to art that already worked.

**STAGE 1 REGISTERED BUT NOT WIRED.** nlq2_water is healed, registered and one word from going
live, but stage 1 is under the standing never-touch rule and Mike was asleep. Left for a go/no-go.
Asserted that stage 1 still reads fx_water so this cannot drift.

**LEVEL 4 UPGRADED.** 480x2693 master -> the pack's 800x3616 gameplay scroll + dedicated 800x1000
boss arena (0.0000% residual magenta). That makes stage 4 a WIDE level, which pulled two things
with it:
 - worldWidth() updated. This is THE recurring bug class — wide:true without it is what broke
   bullet culling, tank clamps and water tiling before. Asserted.
 - All 55 VW* references in the stage-4 roster rescaled to the 800px world, or the entire cast
   would have crowded into the left 60% of the airbase. Soak confirms spawns now reach x=846.
 - Stage 4 is a TANK stage and the drivability mask is built from the master's own pixels, so it
   was re-measured against the new concrete palette BEFORE the swap: 38.51% of cells drivable,
   against an engine rejection threshold of 2%.

**A test-limitation, not a game bug:** _buildTankMask needs a real canvas + getImageData, which the
headless harness has no implementation for, so asserting it there would only ever test the stub.
extract_lvl4map.py mirrors the engine's stage-4 acceptance rule against the real master pixels and
writes _tankmask_report.json; the harness asserts on that instead.

**Still on the shelf:** stage-1 water swap (awaiting go-ahead); the Level-04 section/runway/
transition plates registered but unwired (nst4b_sec1-4, _app/_run/_exit, _tr_in/_tr_out); the
sprite-rain; CF_RivalDogfightPack-Vol1 still untouched.

---

## DROP 0724e — LEVEL 8 ELITES + HERALD FLIGHT ANIMATION

Build: 399 assertions, 0 errors. Manifest 5692 -> 5748 keys (+56).
Stage 8 gets its four elite escorts, and the Venom Reaver reels registered in 0724b are finally wired.

**THIRD frame semantic in three drops — worth writing down**
  0724a sewer cast    6f loop:true   -> continuous idle cycle
  0724d volcanic cast 6f loop:false  -> six discrete STATES
  0724e L8 elites     8f loop:true   -> states AND an authored roll sequence, plus a separate
                                        6f one-shot destruction reel
Reading each pack's own JSON before wiring is now non-negotiable; three packs in a row have had
different semantics and guessing would have broken all three differently.

**The authored roll**
flightspin frames: 0 neutral · 1 charge · 2 attack · 3 twist-left · 4 spin-edge · 5 twist-right
· 6 recovery · 7 damaged. The pack README: "Play frames 04-07 as the authored twist-and-spin
movement. The thin edge-on frame is the midpoint of the roll, not an idle pose." So 3-6 are a
TIMER-DRIVEN SEQUENCE, never free-running, and frame 4 can never be held. Verified at extract
time that frame 4 is 36-39% of neutral width on all four units — if the frame order were ever
wrong that assert fires.
The roll also DISPLACES the unit laterally (asserted). A roll that does not move you is a costume.

**Collision during the roll: NOT granted.** README says "keep collision active unless the game
design explicitly grants a short evasive window." Honoured. ELITE8_IFRAMES is a single flag if
Mike wants the roll to become a real dodge — that is a difficulty decision, not a VFX one.

**Destruction reel gets its full length.** 6f at 12fps = 0.5s, but the stock enemy death window is
0.35s and would have truncated it. Added a per-enemy `_dieDur` rather than cutting the artist's
reel short; elites also needed adding to the dying-state gate, which previously keyed only on
`e.art` (the ENEMY_ART path they do not use).

**The four:** VOID TALON (rolls away from incoming player fire, re-passes) · HELLWING REAVER
(orbits the player column, twin bolts) · CORRUPTION DISC (rolls edge-on TOWARD your lane, then an
8-shot ring) · DEATH SPIRAL (spiral descent, rolls the tight side of every turn).

**HERALD OF DEATH now flies.** nvr_idle 6f / nvr_bank 7f / nvr_roll 8f, silhouette IoU 1.0000
against the composited components, so the reel stands in for the intact layers exactly like the
VILE forms. Bank is chosen from REAL lateral velocity rather than a timer, so the art follows the
movement. Checked first that the reels matched the components: mba_vr and mba_rk turned out to be
the same art under two prefixes (both IoU 1.0000), so either was safe — but that is exactly the
check that saved the VILE swap in 0724b and it is not skippable.

**Soak lesson repeated:** the stage-8 soak initially reported NO sub-boss at all, because it did
not reset subBossDone/subBossTriggered/_sc1/_sc2 the way the stage-7 soak does, and an earlier
test section had already spawned a herald. Soak setup must reset the FULL stage-flag set.

**Still on the shelf:** the new sprite-rain (nwf_rainL/H/W/splash) — deliberate, stage 6's
full-screen sheets are the better tool. CF_RivalDogfightPack-Vol1 still untouched: it needs a game
MODE, not a wiring pass. Liquids for stages 1-4 and the Level-04 map kit still unpulled.

---

## DROP 0724d — LEVEL 2 VOLCANIC CAST

Build: 373 assertions, 0 errors. Manifest 5620 -> 5692 keys (+72).
Stage 2 stops running on generic drones/assaults and gets its authored twelve.

**FRAME SEMANTICS — the thing that would have broken this**
CF_EnemiesPack-Lvl2 ships loop:false. The six frames are STATES, not an animation cycle, and the
pack splits into two families:
  SHIP (8 units, fps10)  0 neutral  1 attack  2 bank-left  3 bank-right  4 damaged  5 destroyed
  VENT (4 units, fps 9)  0 idle     1 charge  2 attack     3 damaged     4 critical  5 destroyed
Cycling these the way the level-7 sewer reels are cycled would have strobed every enemy between
healthy and destroyed several times a second. drawVolc picks the frame from live state instead,
which is also free expressiveness: ships lean into their turns, vents visibly swell before firing.
Verified at extract time that all six states are genuinely distinct (least-distinct pair 6.3 mean
abs diff) and that loop===false, with an assert that fires if the pack's semantics ever change.

**The twelve** (behaviours follow the pack README's stated design per unit, not invented):
  magma skimmer · cinder disc · furnace eye · caldera miner · ashwing interceptor · crucible
  bomber · obsidian lancer · ember carrier · lava maw · basalt crawler · eruption pod · molten golem
Both stage-2 elites (el_em EMBER MANTIS, el_lr LAVA MAGMA REAVER) are kept — they were authored
for this stage and still fit.

**THREE BUGS FOUND, ALL MINE, ALL ROOT-CAUSED**
1. FALSY-ZERO COOLDOWN. `e._fcd = (e._fcd || X) - dt` re-seeds the cooldown whenever it lands
   exactly on 0, silently skipping the shot. Caught by the EMBER CARRIER launch assertion. Fixed
   in 12 places — 7 in the new volcanic code and 5 LATENT ONES IN sewerTick from drop 0724a.
2. ROSTER AUTHORED PAST THE STAGE END. Stage 2 is 48s; I wrote spawns out to 51s, so the tail of
   my own roster could never dispatch. Timeline compressed to fit.
3. NAME COLLISION. 'maw' already meant the level-7 BUBBLE MAW. The level-2 vent is spawned as
   'lavamaw'; asserted that spawning 'maw' still yields the sewer unit.
Also re-applied the _selfPat registration that silently killed the sewer cast on its first pass —
asserted this time so it cannot regress.

**SOAK REALISM FIX (applies to stage 7 too)**
The wave dispatcher gates on `_liveN <= _dispatchAt`. A soak player who never shoots lets the
screen fill until the roster stalls permanently — the stage-2 soak was reporting 8-10 of 12 units
purely because of this. Both soaks now clear the field periodically like a real player. Stage 2
now reports the full 12/12.

**Still on the shelf:** CF_EnemiesPack-Lvl8 (4 elites, flightspin 8f LOOPING + destruction 6f);
Venom Reaver flight reels registered but unwired; the new sprite-rain; the Rival pack.

---

## DROP 0724c — WEATHER FX: firewave (L2), snow (L3), lightning bolts (L6)

Build: 356 assertions, 0 errors. Manifest 5550 -> 5620 keys.

**MISTAKE I MADE AND FIXED (recorded so it does not repeat)**
I grepped for "weather" and saw only the cloud system, concluded stage 6 had no weather, and
registered the new rain straight onto the nwx_ prefix. That CLOBBERED 12 live keys
(nwx_rainH/rainL 0-5, 640x480 full-screen sheets) with 243x233 sprite art, and left 62 orphan
nwx_ keys pointing at a folder I then deleted. Stage 6 has had a full storm system all along
(l6WeatherUpdate / l6WeatherDraw, bands clear/windy/squall/storm).
Fix: restored the 12 originals from the shipped zip, swept the 62 orphans, and moved the entire
new pack into its own nwf_ namespace. The harness now asserts both namespaces stay separate.
LESSON: grep the KEY PREFIX, not the human word for the feature.
(The sweep also removed nwx_flash_4..7, which were already dangling in the shipped build — part
of the 168 pre-existing missing files. The draw code counts frames dynamically, so that is a
clean improvement, not a regression.)

**Registered: +74 keys, all in nwf_**
  nwf_fire 8f · nwf_snowL/snowD/snowB/bliz 6f · nwf_rainL/rainH/rainW/splash 6f · nwf_ltS/ltC/ltF 6f
Chroma gate on all 234 files across the five packs: 0 sockets, 0 semi-alpha px.

**Wired — one system (WFX / wfxUpdate / wfxDraw), three stages**
 - STAGE 2 FIREWAVE: additive sweep crossing the caldera edge-to-edge, mirrored on direction.
   COSMETIC ONLY. Making it damage the player would rebalance stage 2 — that is Mike's call,
   not a side effect of a VFX drop.
 - STAGE 3 SNOW: the precipitation bed the stage never had, plus snowburst/blizzard gusts.
 - STAGE 6 LIGHTNING: real BOLT art struck at a position. The existing flash is a generic
   full-screen exposure lift with no shape in it; bolts now fire off that same flash state
   (>0.92) so the two never contradict each other, and the lift becomes the afterglow.

**Deliberately NOT wired:** the new pack's rain (nwf_rainL/H/W/splash). Stage 6's existing rain is
authored as 640x480 full-screen sheets, which is the right tool for a wall of rain; the new rain
is sprite-sized, a different technique. Two rain systems on one stage would fight. Registered and
available if Mike wants the sprite approach instead.

**Snow density MEASURED, not guessed.** White snow over an arctic master (mean luma 144) is a
contrast trap. Visible-coverage against the bare nst3_master: 26 particles = 1.4% (effectively
invisible), 48 = 3.9%, 64 = 5.8%, 80 = 8.3%, 96 = 11.4%. Chose 64. My first attempt shipped at 26
and would have been a snow system nobody could see.

**Still on the shelf:** CF_EnemiesPack-Lvl2 (12 volcanic units x 6f) and CF_EnemiesPack-Lvl8
(4 elites x flightspin 8f + destruction 6f) — both chroma-clean, neither wired. Venom Reaver
flight reels still unwired. Rival pack still untouched.

---

## DROP 0724b — STAGE 8 CHROMA REPAIR + VILE EXISTENCE ANIMATION

Build: 335 assertions, 0 errors. Manifest 5481 -> 5550 keys (+69; 162 drop keys, 93 replacements).

**CHROMA — what was actually wrong, and what was NOT**
Full sweep of all 5382 registered files. Three different things get called "purple"; they need
different tests, and only ONE was a defect:
1. UNFILLED KEY SOCKET (the real bug): 6089 px — 3100 across form-1's clean/dam components and
   2989 across the 1>2 morph. Two flat colours (#FB03FC / #E505CA) at alpha 255 in solid interior
   blobs of 364-488 px. Real pixel art does not have 2 unique values across 1804 px. FIXED.
2. DITHERED VIOLET ART (not a defect): 1-5 px per file, every pixel a DIFFERENT value. This is the
   forms' actual venom palette. Left alone.
3. PILOT TRAIL COLOURS (not a defect): ntr_pink / ntr_purple are two members of a 12-colour swap
   family (ab/blue/cyan/fire/green/orange/pink/purple/red/smkH/smkL/yellow), all with identical
   structure — 1976 opaque px, 3 unique colours. ntr_blue flags zero with the same shape.
   Stripping purple from a purple trail would be vandalism. Left alone.
HALOS: alpha is BINARY across all 162 drop files (0 semi-transparent px), so an edge halo is
structurally impossible in this art. Verified, not assumed.

**HOW the socket was fixed without inventing art**
Rejected in order, with evidence:
 - mirror-heal from the opposite side: form 1 is NOT bilaterally symmetric (alpha IoU 0.37,
   mean colour diff 40) — would have fabricated wrong art.
 - re-derive components from the pack's 288px whole-body art: that art is a REDRAW, bbox 232x170
   vs the registered 222x228, IoU 0.53 even bbox-normalised — component boundaries would be guesswork.
 - blanking sockets to transparent: leaves holes in the boss.
The pack ships REPAIRED v1.1 components under SourceMasters/ at the same 256x256 canvas and the
same component-map rects _vileSpec() already uses. Socket-free. All 60 (4 forms x 5 components x
3 states) swapped ATOMICALLY — silhouette IoU vs v1.0 ranges 0.08-0.86, so mixing versions would
have produced a chimera. Morphs 1>2, 2>3, 3>4 re-sliced from the pack's 1536x256 sheets.

**ANIMATION (+69 keys)**
 - 4 forms x idle 6f + attack-charge 6f = 48 keys
 - VENOM REAVER flight: idle 6f + bank-turn 7f + barrel-roll 8f = 21 keys (registered, not yet wired)
The component swap was a PREREQUISITE, not a nice-to-have: the reels are v1.1, so animating them
over v1.0 components would have made the boss change shape between static and animated states.
Verified at extract time: idle frame 0 silhouette IoU = 1.0000 vs the composited clean components,
all four forms — which is exactly why the reel can stand in for the intact layers pixel-for-pixel.

**Design: the attack reel IS the tell.** vileAnimTick drives the charge reel off _mcd, engaging
VILE_TELL (0.55s) before the heavy shot and running to the muzzle. Enrage raises fire rate but
never shortens the tell — a tell you cannot react to is just noise. Mid-morph the reel yields to
the morph overlay. drawModularBoss draws the reel as the base and SKIPS only clean-tier parts, so
damaged and destroyed modules still draw their own art on top and destruction stays readable.

**Permanent guard:** audit_chroma.full_manifest_report() sweeps every registered PNG and writes
assets/fx/_chroma_report.json; the harness asserts socket_px === 0. Residue = a contiguous flat
magenta blob >=100px. The discriminator is BLOB SIZE, measured: the real defect was single blobs
of 364-488 px, the largest legitimate blob anywhere in the manifest is 44 px (ntr_purple).

**Still on the shelf:** Venom Reaver flight reels registered but not wired to the stage-8 sub-boss;
CF_RivalDogfightPack-Vol1 untouched; liquids for stages 1-4 and the Level-04 map kit unpulled.

---

## DROP 0724a — LEVEL 7 "NOT ANOTHER SEWER LEVEL" GOES LIVE

Stage 7 was the last stage still falling back to a procedural background with `boss:null`.
It is now a fully authored level. Build: 320 assertions, 0 errors.

**Art registered (+79 manifest keys, 5402 -> 5481)** — all from CF_LevelPack-Lvl7, byte-for-byte
copies of the pack's pre-keyed `-alpha` PNGs. Nothing procedural, nothing recoloured.
- `nst7_master` 800x3616 gameplay scroll, `nst7_arena` 800x1000 boss arena
  (0.0000% residual magenta, 3.02% keyed channels for the sludge bed to animate through)
- `nlq_sludge_0..5` upgraded 128px -> 256px (the old frames were unreferenced), `nlqf_sludge_0..5` falls
- 36 line-enemy frames (6 units x 6f), 14 OVERFLOW EXCAVATOR frames
- 15 CESSPOOL LEVIATHAN modular parts + 6 idle frames sliced at exact 256px boundaries

**Systems**
- `_levelCfg()` case 7: wide master + dedicated boss arena + sludge liquid bed
- New `SEWER` roster: `sewerTick` / `drawSewer`, six units with distinct signatures
  (skimmer widens its strafe as it closes; shambler lobs ahead of you; sentry holds station and
  sweeps; barge is a drifting wall; crawler hugs a world wall; maw submerges and re-surfaces elsewhere)
- CESSPOOL LEVIATHAN wired as the stage-7 boss. Its `component-map.json` is the same five-part
  256x256 layout the VILE forms use, so it drops onto `_vileSpec()` with ZERO new modular code.
- OVERFLOW EXCAVATOR replaces the borrowed `mba_rk` art on the stage-7 sub-boss slot. `mba_rk` is the
  Venom Reaver and belongs to the stage-8 HERALD OF DEATH — that art is now free again.
- 18-event authored spawn roster for stage 7.

**Root-cause fixes (three, all found by the harness)**
1. `worldWidth()` is a hardcoded stage whitelist. Setting `wide:true` in `_levelCfg` without adding
   the stage to it is THE recurring bug class (bullet culling, tank clamps, water tiling). Stage 7
   added and now asserted so it cannot silently regress.
2. `updateSubBoss` and the boss idle drift both centred on `VW/2`, so on EVERY wide stage (1, 5, 6 —
   not just 7) the boss patrolled only the left 480px of the 800px world. Both now `worldWidth()/2`.
   Pre-existing bug, fixed for free.
3. `pattern` was silently overwritten to `'sine'` for the sewer units: they weren't registered in the
   `_selfPat` allowlist, so `sewerTick` would NEVER have run. The level would have shipped dead —
   art perfect, behaviour absent. `SEWER` now folded into `_selfPat` like `ELITE_DEF`/`MINI_DEF`.

**Measured, not eyeballed**
- Component isolation: 100.0% of every Leviathan layer's opaque pixels sit inside its authored rect
- Damage states: `dam` changes 8-21% of in-rect pixels; `ruin` changes 19-59% AND drops opaque pixel
  count by 210-764 (real chunks blown away, not a recolour)
- Frame reels genuinely animate: enemies 16-37 mean abs diff, excavator reels 22-43
- Soak: full 90s headless run, no throw, all 6 unit types seen, 47 enemy bullets peak,
  sub-boss triggers and is fought, boss arrives with all 5 modular parts live

**Still staged, NOT wired**
- CF_BossSheets-Lvl8: the static components were ALREADY registered. The pack's real value is the
  ANIMATION — idle-6f + attack-charge-6f per Vile form, Reaver bank-turn-7f and barrel-roll-8f.
- CF_RivalDogfightPack-Vol1: completely untouched. 9 courses, 8 hazards, player rival jet.
- CF_LiquidsLevelMap-Lvl4: only the stage-7 sludge was pulled. Stages 1-4 surface+fall sets at 256px
  and the Level-04 map kit are still on the shelf.

---

## DROP 0719c — Tier 1 COMPLETE (2026-07-19, Fable-5 session 2)
- #2 Stage cards v5 (all 8 swapped; v4.1 in assets/ui/stagecards_v41_backup) + v5 fonts wired for stages 2-8 (stage-1 font untouched)
- #3 Death explosions: nx_* families (fire x3, nuclear big, small, smoke, ice-recolor) — explode() prefers, falls back
- #4 Liquids: nlq_lava (S2) + nlq_icewater (S3) true-16bit seamless; nlq_sludge staged for S6 (needs new S6 master)
- #1 v2.2 weapon swap (approved package): icons ALL (25 in-place + micon_ for 6 crate weapons), ice orb (nio_), firewall (nfw_), spread center-dart (nsp_), MG muzzle (nmz_), laser beam+muzzle on the LIVE beam path (nlz_) — found+fixed: Fable-5 lzr_ art was on dead kind:'laser' path. Chain: v2.2 fork-burst at nodes (nch_), straight chain_bolt arcs kept.
- KEPT: Mike's mfx_mg pellets, pilot-colored missiles, venom helix lance.
- Verified: 282-assert harness 0 errors; differential pixel proof per weapon (SPREAD 2.51%, ICE 0.27%, FIREWALL 4.65%, LASER 6.23%, MG-MUZ 0.34% of frame changed); icon originals in assets/fx/_icons_v21_backup.
- Build scripts: extract_explosions_nx.py, extract_liquids_nx.py, pack_stagefonts_v5.py, extract_v22.py, register_drop_0719b.py, verify_0719b.js, verify_v22.js, verify_v22_diff.js, make_cmp_sheets.py

## DROP 0719d — Laser glow fix + Tier 2 part 1 (2026-07-19)
- LASER: glow removed from the animated v2.2 beam per Mike (no shadowBlur/bloom, wavering side-glow + legacy muzzle orb gated off on the v2.2 path; racing pulses kept)
- STAGE MASTERS (true-16bit rebuild, fitted to CURRENT scroll; L1 untouched):
  - nst2/nst3/nst4 LIVE: 4 sections + boss arena composed w/ 128px seam overlap (800x4488), magenta liquid channels keyed, NEAREST-scaled to the 480-wide 1:1 contract (480x2693)
  - NEW stage-4 liquid: nlq_runoff (Airbase_Runoff family) — S4 had no liquid before
  - S4 TANK MASK: added stage-4-only neutral-concrete drivable rule + 1-cell erosion (jungle keeps warm-dirt + 2-cell). Mask now builds: 6.3% drivable tarmac
  - nst5/nst6 composed + registered but HELD on legacy masters: art is authored near-black (S5 brightness 11, S6 brightness 4) to sit under parallax/stage-object layers not yet wired. Flip the two _levelCfg lines when the S5/S6 object pass lands.
- Verified: harness 0 errors; per-stage renders distinct across start/mid/arena (38-77% px, S2-4); liquid animation proven at fixed scroll (S2 12.2%/S3 16.7%/S4 3.8% px animating)
- NEXT (Tier 2 cont.): enemy damage-state art (4x3 sheets + 15-jet pair) onto enemyArtState; per-stage rosters 2-8

## DROP 0719e — Tier 2 part 2: damage-state vault units (2026-07-19)
- NEW ASSETS STORED (final pre-stage-select drop): level06_aerial_warfare (1,860 png: trails 8 colors+damage smoke, 3 giant atomic missile classes w/ full lifecycle, danger/atomic alerts, radar lock, clouds, weather) -> feeds S6 authoring + clouds/weather + thruster overlays + new atomic-intercept setpiece (Tier 2-3). stats_boss_bars_ui (954 png: per-stage 1-8 boss/miniboss bars, stat bars 3 sizes + labels + critical pulses) -> supersedes bar_frame set, Tier 1-2 swap.
- 16 NEW damage-state units sliced from the 4x3 sheets -> vault keys (assets/enemies/vault0719):
  nvg green (jet/heli/truck/gunboat), nvy gray (jet/big-fighter/stealth/APC), nvi ice (jet/fighter/tank/radar-mech), nvp purple (fighter/orb/gunship/walker); each _intact_c/_dama_c/_crit_c
- STAGE-THEMED AIR POOLS (VAULT_AIR_STAGE): S2 gray, S3 ice, S4 green+gray, S5/S6 purple, mixed with ac* airframes. Stage 1 absent by design (Mike-curated roster untouched). Ground/naval slices (nvg2/3, nvi2, nvp3) registered for later tank/naval wiring.
- 15-jet intact/damaged pair SKIPPED deliberately: existing ac0-14 vault has more states + bank frames (would be a downgrade).
- Verified: harness 0 errors; per-stage picks proven (S2 nvy/S3 nvi/S5 nvp), HP-driven inta/dama/crit switching with distinct art per state.
- NEXT: per-stage spawn-table rosters (Tier 2 finale), then stats/boss-bar UI swap + trails.

## DROP 0719f — Stats/Boss Bars v2.0 wired + stage-select stored (2026-07-19)
- STAGE-SELECT PACK STORED (stage_select_worldmap, 431 png): world map + route network + progress 0-8, per-stage flags/labels/guide panels, 3 fonts, cursor, previews, STAGE_SELECT_CONFIG.json layout spec. -> Tier 3 new screen, build-to-spec, slot after rosters.
- STATS SCREEN: v2.0 animated stat fills (firepower/speed/shield/armor/bomb/missiles, 8-frame) + nsb_frame, legacy bar_frame fallback kept.
- BOSS BAR: per-stage themed frame + 8-frame animated fill (nbb<stage>_*), legacy gradient fallback kept. Miniboss bars (nmb*) registered, not yet differentiated.
- 193 bar keys extracted (assets/ui/bars_v2). Harness 0 errors; renders verified (boss bar S2 at 55% HP, stats screen).
- NEXT: per-stage spawn rosters (Tier 2 finale) -> then stage-select screen (Tier 3) + destructibles + trails.

## DROP 0719g — no-stretch bars + boots pack stored (2026-07-19)
- Mike caught it: bar fills WERE stretched (384x48 art drawn at ~432x7; boss 512x64 at ~432x13). Fixed with drawBarArtNS(): uniform scale to dest height, fill TILED repeat-x (clipped to ratio), frame end-caps at scaled size with middle band TILED. Both stats screen + boss bar routed through it. No art is stretched anywhere now.
- roster_v2_boots_logos stored: 5 boot screens + 5 title logos + CANONICAL_9_PILOT_ROSTER.json. TO-DO: boot/title swap (pick variants with Mike), Tier 1-2.

## DROP 0719h — ONE-bar fix + PER-STAGE ROSTERS (Tier 2 COMPLETE) (2026-07-19)
- BARS per Mike "only 1 bar per category": stats screen reverted to approved bar_frame + single color fill per row (nsb_* categorized fills reserved for a future pilot-stats window where the categories exist). Boss bar = ONE fill via 3-slice (caps intact, only smooth middle extends) — no tiling, no stretch. drawBarArtNS updated.
- PER-STAGE AUTHORED ROSTERS, stages 2-6 (buildStagePlan): S2 volcanic kamikaze pressure (no tanks), S3 cryo squadrons (frost/cryo/icegun/shieldd), S4 airbase armor+missiles (tanks+microturrets+jetflyby+mdrone), S5 deep space (mine belts, octo/mech weaves, twin sideswirls), S6 furious prelude (topgun trios, racer swarms, kamikaze, dense). Generic timeline remains for 7-8.
- Verified: harness 0 errors; per-stage spawn censuses distinct (S2 48 spawns/S3 27/S4 34/S5 36/S6 39, casts match themes); 14s live-sim renders per stage.
- TIER 2 COMPLETE. Next: Tier 3 — stage-select screen (config-spec'd), boot/logo picker for Mike, destructibles, trails.

## DROP 0719i — STAGE SELECT WORLD MAP live (Tier 3 opens) (2026-07-19)
- New GS.STAGESEL state built to STAGE_SELECT_CONFIG.json: 640x480 map @0.75 scale, route-progress overlay by cleared count, per-stage flags (completed/available/locked/highlight 2fr), animated cursor, screen title, per-stage guide panel + label, bonus flag locked-visible (config rule). Input: arrows cycle unlocked stages, fire deploys (beginStage). 77 nss_* keys.
- FLOW: startRun -> map (cursor on entry stage); stage clear -> map with next stage unlocked. RIVAL encounter + VICTORY branches untouched. Replay of cleared stages allowed by design (browse back).
- PIPELINE LESSON RELEARNED (owned): direct edits to assemble-owned regions (GS enum, drawScene dispatch, boot..goTitle span) broke anchors -> assemble ABORTED SILENTLY (output was piped to /dev/null) and two harness runs tested a STALE build. Fixed: enum+dispatch routed through assemble.py's own patch strings; SSEL block relocated outside the boot span; assemble output now checked. Also: the two earlier 'ASSERT FAIL's were confirmed unseeded-RNG flake in the atom-secondaries test (3x green after).
- Verified: harness 0 errors x2 on the REAL build; state/unlock/deploy flow numerically checked; 3-scenario renders.

## DROP 0719j — Trails live + boot/logo picker out (2026-07-19)
- AIRCRAFT TRAILS (aerial-warfare pack, 96 ntr_* keys): player throttle-reactive thruster (pilot-colored arcade exhaust: yuri red/maverick green/falva pink/lizzie yellow/cole blue/freezer cyan/axel orange/decker purple/juggernaut afterburner; length+alpha grow with UP held + speedLevel, additive blend). Enemy damage trails on air vault units: smoke at dama, fire at crit, streamed up-behind (flipped). Roadmap "throttle-reactive thruster overlays" DONE.
- Verified: harness 0 errors on real build (assemble output checked); trail differential 402px localized; render with falva pink burn + dama-smoke + crit-fire enemies.
- BOOT/LOGO PICKER sheet delivered to Mike (5 boots x 5 logos) — wiring waits on his canon picks.

## DROP 0719k — CANON BOOT/LOGO + MODE SELECT (2026-07-19, Mike picks)
- logo-01 Primary Inferno = title logo (drawn above menu). boot-01 = boot cinematic bg. boot-02 = difficulty bg. boot-03 = password bg. boot-04 = options bg. boot-05 = NEW MODE SELECT screen bg.
- NEW GS.MODESEL between NEW GAME and difficulty: ARCADE (straight run, no world map), CAMPAIGN (world map path), 2-PLAYER + VERSUS shown locked "COMING SOON" (planned modes). run.mode wired: arcade skips openStageSelect at startRun AND between stages; campaign uses the map. Enum+dispatch routed through assemble (lesson applied); screen fn in the safe zone; bg swaps inside patch blocks with legacy fallbacks.
- drawCanonBackdrop(key,dim): cover-fit + darkening gradient helper.
- Verified: harness 0 errors; all 6 keys ready; 6-screen renders; arcade startRun->intro direct, campaign startRun->stagesel.
- NEXT: destructible scenery system, then Tier-4 (anchors/multi-part bosses -> themed bosses -> necro finale; atomic intercept; rival dogfight AI). 2P/VERSUS implementation = new roadmap items under modes.

## DROP 0719l — logo fit + DESTRUCTIBLE SCENERY (2026-07-19)
- LOGO: height-capped to the band above '- INSERT COIN -' (h=88, y=8; INSERT COIN center y=118). No overlap.
- DESTRUCTIBLE SCENERY (Stage_Objects pairs, 72 nds_* keys + _scenery_spec.json): scenery[] system — 14 objects/stage pre-planned (seeded per stage), trigger by mapScroll, y locked EXACTLY to terrain scroll (y=-48+(mapScroll-ms0)), player-fire hittable (1 hit/frame), break -> wrecked frame + explosion + score (150 / volatile 400 + shake + 70px chain damage to enemies). Volatile pairs per manifest: S2 slag_fuel_tanker, S3 idx2, S4 idx2, S6 idx4. STAGES 2-6 ONLY — stage 1 untouched per Mike (nds_1_* registered for later). Beam/atom excluded from scenery hits v1.
- Fix owned: extracted keys weren't registered before first verify (registrar not rerun) — caught by gate debug, re-registered (793 keys).
- Verified: harness 0 errors; spawn 14 planned, scroll-locked on-screen, hit->wreck->explosion->score all proven; render captured.

## DROP 0719m — MODULAR BOSS / ANCHOR SYSTEM (Tier 4 opens) (2026-07-19)
- New anchor-point/multi-part boss system: per-part hitboxes w/ independent HP, per-part clean/damaged/ruined art, muzzle anchors locked to the moving hull. Seams: bossHitTest records struck part -> hitBoss routes to it; updateBoss/drawBoss branch on boss.modular. Boss dies when all damageable parts ruined.
- FIRST MODULAR BOSS: IRON REVENANT (stage 4, replaces benched ARACHNON 'spider'). Built from manifest: 3x4 x 64px grid, 12 modules (10 damageable: nose/2 cannons/command/3 racks/2 engines/tail), per-module HP weights, vfx anchors. 36 mbp_ir_* keys. Enrage: fire rate scales 1x->2.2x as parts fall. Racks fire homing missiles, cannons+nose fire aimed MG, all from anchors on ALIVE parts only. Ruined parts vent smoke (ntr_smkH).
- Verified: harness 0 errors; per-part routing CLEAN (all 10 parts: hit self only, 0 leak to neighbors - frozen-boss proof); anchor-to-hull offset variance 0.000px across 45px real-play sway; firing gate proven (3 rack missiles alive -> 0 after racks destroyed); full kill -> bossDie. Renders: intact assembly + wing-racks-ruined.
- Earlier apparent 'leak' was a test artifact (fixed-coord fire vs swaying hull), not a code bug - confirmed by frozen-boss retest.
- NEXT Tier 4: themed stage bosses (6) onto this system, necro finale, Siege Mammoth X (2nd modular), atomic-missile intercept, rival dogfight AI.

## DROP 0720a — mode reorder + reskin, new HUD (2026-07-20, Mike drop)
- ASSETS INTAKE (drop0720): mode-select pills, stage-select boxes L6-9, new HUD bar, menu buttons, miniboss S-pills. Arcade cabinet webpage mockup = NOT re-uploaded (blocked, needs file).
- MODE SELECT: reordered per Mike -> CAMPAIGN, ARCADE, CO-OP(locked/gray), VERSUS(locked/gray). Reskinned with pill art (nms_*), locked pills grayed + 'LOCKED'. Campaign default highlight. Locks enforced (verified: co-op select = no-op, campaign->diff). Campaign=stage-select+revisit+story; Arcade=classic progression (both already wired).
- NEW HUD: nhud_bar swapped in (SCORE/HI SCORE/LIVES/BOMBS/EQUIPMENT: SHIELD/SPEED/WEAP pips). Fills reserved 62px strip. Legacy hud_bar + custom kept as fallback chain.
- Verified: harness 0 errors; mode order/locks/pills; HUD renders live values.
- REMAINING this drop: menu buttons swap, stage-select box art L6-9 wired, miniboss bar differentiation.

## DROP 0720a-fix — HUD file mixup corrected (2026-07-20)
- OWNED: staged hud_bar.png and miniboss_pills.png were SWAPPED (cp assignments reversed). nhud_bar was extracting from the S-pills sheet -> HUD showed 4 pills. Fixed: hud_bar=ba1211a4 (real SCORE/EQUIPMENT bar), miniboss_pills=329894d6 (4 S-pills). Re-extracted nhud_bar, remeasured windows via metal dividers (SCORE .128 / HI .359 / LIVES .522 / BOMBS .64 / EQUIP subs .755/.845/.935). Pixel-diff confirms render now matches HUD art (101 vs 129 pills).

## DROP 0720b — HUD polish per Mike (2026-07-20)
- Divider line below HUD now DARK GRAY (#2a2d33 + #15171b shadow, verified 42,45,51).
- LIVES use the 8-bit drawMiniShip; BOMBS now use NEW drawMiniMissile 8-bit icon (nose/fins/flame, matches ship read) instead of circle placeholders.
- All 5 value groups (LIVES/BOMBS/SHIELD/SPEED/WEAP) CENTERED in their windows: measured offset 0px each. Pips centered with proper pitch to fit the mini boxes.
- Verified: harness 0 errors; per-window centering 0px offset; divider color confirmed.

## DROP 0720c — real HUD icons + overflow + equipment shift (2026-07-20)
- Real art icons: lifehudicons/missilehudicons sliced to nli_0-8 / nmi_0-8 (9 pilot colors), picked by pilot (yuri0/falva1/cole2/maverick3/axel4/juggernaut5/lizzie6/decker7/freezer8). Replaces hand-drawn 8-bit (kept as fallback).
- Overflow: lives/bombs <=4 draw individual icons; 5+ draws ONE icon + 'xN' (N=actual count), centered.
- Equipment shift per Mike: SPEED pips -10px, WEAP pips -20px to center in sub-boxes. SHIELD unchanged.
- Verified: harness 0 errors; shifts + icon keys confirmed in deployed game.js.

## DROP 0720d — HUD recorrect (2026-07-20)
- LIVES/BOMBS: now ALWAYS single icon + xN (N=count) across the board — no more spilling at 3+. (Removed the 1-4-individual-icons path.)
- EQUIPMENT: reverted ad-hoc -10/-20 shift (over-corrected). Sub-box centers now MEASURED by dividing the EQUIPMENT window into equal thirds: SHIELD 0.751, SPEED 0.850, WEAP 0.948 VW (px 361/408/455). Verified 0px offset each.
- Verified: harness 0; lives content x220-279 (no spill), equipment offsets 0px.

## DROP 0720e — equipment pip fit (2026-07-20)
- WEAP was out of bounds (right), SPEED last pip touched box edge. Fix: tightened pip pitch (PW 3->2.6) and recentered SHIELD 0.751 / SPEED 0.843 / WEAP 0.930 VW.
- Verified by color-matched lit-pip measurement (all level 5): each group sits 15px symmetric margin inside its box, fully in-bounds. SHIELD x352-368, SPEED x396-412, WEAP x438-454.

## DROP 0720f — equipment pips snapped to measured box interiors (2026-07-20)
- Detected the REAL dark box interiors in the pip row: SHIELD x347-379, SPEED x384-417, WEAP x422-454 (@480). Set centers to 0.757/0.835/0.913 VW.
- Result: 17px pip block sits 8px symmetric margin inside each box, IN BOUNDS all three. No more WEAP overflow / SPEED edge-touch.

## DROP 0720g — pip color order + EQUIPPED box (2026-07-20)
- HUD pips now colored by UPGRADE-TIER color per level (WLVL_COL): L1 orange #ff8a1e / L2 blue #3a8aff / L3 green #5fe07a / L4 white #f2f5ff / L5 red #ff4a48. Bar COUNT = level. Verified: shield L2 blue, speed L3 green, weap L4 white (pixel-sampled exact).
- EQUIPPED BOX (nequipbox) bottom-right corner: shows current weapon micon_ pickup icon scaled to fit inner screen. Special abilities (speed/shield) do NOT replace it. On death (weapon lost) the icon disappears. Verified: laser 46% box content, dead 16% (empty), iceorb 50% (diff icon).

## DROP 0720h — equip box repositioned + stray icons removed (2026-07-20)
- EQUIPPED box moved OUT of play area: now top-right, directly UNDER the HUD strip (by=HUDH=62), flush to the right edge (bx=VW-64). BW=64.
- REMOVED stray top-right speed-chevron + shield-circle indicators (item_speed_/item_shield/pwr_shield_ at VW-9) from BOTH drawHUDCustom (gamecode) and drawHUDCustomLegacy (patches) — redundant now that speed/shield show as HUD EQUIPMENT pips. 0 remaining in deployed build.
- Verified: box present under HUD (58 brightness, icon 47%), old stray zone blue 3.6% (clean), harness 0 errors.

## DROP 0720i — real HUD path unified + divider + box placement (2026-07-20)
- KEY FIX: the LIVE in-game HUD is drawHUDStrip (separate #hud canvas), NOT drawHUDCustom (which only runs in menu/dom contexts). All prior HUD work styled drawHUDCustom; the game still showed the old hud_bar strip. Redirected drawHUDStrip to render nhud_bar with the SAME corrected layout (score/hi windows, pilot ship+missile icons xN, level-colored pips L1 orange..L5 red at 0.757/0.835/0.913).
- DIVIDER: #hud-div CSS now dark gray (#2a2d33 + #15171b shadow, 3px) separating HUD canvas from game canvas. Verified 42,45,51.
- EQUIPPED box: top-right of the GAME view, just below the divider (by=HUDH+4, bx=VW-BW), to the right under the HUD. Renders weapon icon; hidden on death.
- Verified: page-mock shows new HUD strip + dark divider + box; harness 0 errors.

## DROP 0720j — strays fully removed + equip box OUT OF BOUNDS (2026-07-20)
- STRAY ICONS: found TWO more sources beyond the earlier fix — drawHUDCustomImg (shield/speed/missile pips at ix,HUDH+10) and drawHUDOverlay (shield/speed at ix,10). Removed both. Game-view top-right now 97.3% terrain, 0% UI metal, 0 blue chevron px.
- EQUIP BOX moved OUT OF the game canvas entirely: now a DOM canvas (#equip-dom / #equipcv) positioned via game-frame.getBoundingClientRect() to sit just right of the game screen, top under the HUD. In-canvas drawEquippedBox neutralized. run/player/XART exposed on window for the DOM renderer. Per-frame tick redraws (follows weapon change / death). Verified box x592 > game right edge x586 = OUTSIDE.

## DROP 0720k — menu buttons + stage-select boxes (2026-07-20)
- MENU BUTTONS: sliced menu_buttons.png -> nmb_newgame/password/options/credits/exit, aliased to btn_ keys that drawMenuButtons already consumes. All 5 render on title (42-70% content each).
- STAGE BOXES L6-9: sliced box_L6-9 sheets -> nlvlbox_<lvl>_<north|west|east|south> (16 keys; renamed from nsb_ to avoid collision with stat-bar nsb_ keys). Middle iso boxes (WEST/EAST) auto-split when merged. Wired into campaign drawStageSelect: boxes render at SSEL_POS map points for stages 6-9 (north='P' available/hi, south='X' locked), flags skipped for those stages. Verified all 4 render at map positions.
- REMAINING drop-0720: miniboss bar differentiation (S-pills staged), arcade cabinet webpage mockup (needs file).

## DROP 0720l — BIG CAMPAIGN PASS (2026-07-20)
- Menu buttons RESCALED down (TMENU_W 406->330, gap 66->58, Y0 168->176).
- L6-9/bonus boxes are POWERUP CRATES (nlc6-9, 4-frame spin) wired into drawCrate for stages 6-9 — NOT map markers. Removed from map select. (Renamed off nsb_/crate6 collisions.)
- CAMPAIGN BOOT: selecting campaign (first entry) runs military-computer terminal boot (TACNET, typed lines, scanline) -> fade to map -> flags appear 1-by-1 -> music fades in.
- FLAG STATES: locked=gray (saturation desat + veil) & NOT selectable (cursor skips, deploy blocked); unlocked-not-beaten=red; beaten=green default; rank tints S=gold, A=silver, B/below=green. rankFlagColor().
- UNLOCK CINEMATIC on returning from a beaten level: ding-ding-ding (SFX.blip x3), flag flashes white rapidly, window scales up from the flag to screen center with zoomed area image + 'LEVEL X UNLOCKED', holds, shrinks back to the flag, then flag settles to red until beaten.
- Per-stage rank recorded on clear (placeholder score->rank; real correlation = TODO). campaign{unlockedMax,rank,_booted}.
- TODO (added): rank<->score correlation tuning.
- Verified: harness 0; boot 99% black+green text, map brightness 39.6, unlock window blue-frame centered.

## DROP 0720m — flag tint on cloth only (2026-07-20)
- FIX: flag color states were filling the whole flag bounding BOX with a solid color rect (source-atop tinted the map behind it too). Now each tinted/grayed flag composites on an offscreen buffer (drawStageSelect._tbuf) so the color/desaturation applies ONLY to the flag's own non-transparent pixels, then stamps back. Plain flags skip the buffer.
- Verified: map background now visible around flags (19% gold / 7% red / 65% gray) vs ~0 for a solid box — tint follows cloth shape.

## DROP 0720n — flag PALETTE SWAP (no boxes, no overlays) (2026-07-20)
- Replaced color-overlay compositing with true PER-PIXEL PALETTE SWAP: each opaque flag pixel recolored by its luminance mapped onto the target color ramp (gold/silver/green/red/white) or desaturated to gray for locked. getImageData->recolor->putImageData on an offscreen canvas, CACHED per (stage+state) so it rasterizes once.
- Gray locked flags: NO box — cloth desaturated by luminance only (verified gray coverage 21-34% = flag-shaped, not 80%+ solid box; corner pixels are map terrain).
- Rank/state flags shade the target color by original luminance (dark stays dark) so the flag keeps its shading instead of a flat wash.

## DROP 0720o — miniboss bars themed (2026-07-20)
- Sliced miniboss_pills.png -> nmbp_steel/skull/void/toxic (4 themed pill frames).
- Replaced the plain amber miniboss HP bar (inside drawSubBoss b.mini branch, which returns early before the generic bar) with the themed pill: frame + colored HP fill in the central gauge band. Theme by stage: 1 steel, 2 skull, 3 void, 4 toxic, 5 steel, 6 skull. Fill colors steel #5aa0ff / skull #ff4a3a / void #b06bff / toxic #8de23a. Differentiates minibosses from the main boss bar.
- Verified: all 4 render with correct fill color (838/822/1403/919 themed px).
- Note: found the miniboss bar was a SEPARATE draw inside the b.mini early-return branch, not the generic sub-boss bar.
- REMAINING drop-0720: arcade cabinet webpage mockup (needs file re-upload).

## DROP 0720p — pills are PICKUPS not boss bars (corrected) (2026-07-20)
- CORRECTION: the S-pills are per-level POWERUP PICKUP art (float + give speed/shield like L1-5), NOT miniboss bars. Reverted both boss-bar changes back to plain amber. Removed all nmbp_ refs from boss bars (0 remaining).
- Renamed pills per Mike mapping: steel->npup6, toxic->npup7, skull->npup8, void->npup9.
- Wired into drawPowerups: speed/shield pickups on stages 6-9 render the themed npup<stage> pill instead of item_speed/item_shield. Verified npup6-9 distinct (blue-gray/brown/red/purple) and rendering.
- NOTE: pills are wide (480x162 ~3:1) squished into 34px pickup — may look squished; aspect/scale may need tuning for the float pickup.

## DROP 0720q — speed/shield 50/50 fix (2026-07-20)
- BUG: capsule pickups always spawned kind:speed (hardcoded in BOTH breakContainer line 2074 and applyPowerup capsule branch) — shield never dropped from capsules. Now a 50/50 coin flip (Math.random()<0.5) in both paths.
- Verified statistically: 4000 breaks -> 2007 speed / 1993 shield = 50/50.

## DROP 0720r — ARCADE CABINET frame (2026-07-20)
- Arcade cabinet mockup wired as the page frame. Magenta play-window keyed to transparent -> cabinet_frame.png. Window rect measured: x 0.239-0.760, y 0.241-0.913 of cabinet (aspect 1.333).
- Rebuilt index.html layout: replaced marquee+side-panels with single #cabinet-img; #game-frame positioned absolutely inside the cabinet window (HUD strip + screen), centered + aspect-fit. Fullscreen hides cabinet, centers game block.
- EQUIPPED box repositioned to the cabinet right panel area (right of the window).
- Verified: composite mock 0% magenta (game fills window), 56% window content, cabinet panels intact (orange lava L, cryo blue R).

## DROP 0720s — HUD row layout: HUD + equip box + divider, centered (2026-07-20)
- Restructured cabinet layout per Mike: HUD strip + EQUIPPED box now form ONE horizontal row (equip box directly right of HUD), a dark-gray divider spans under the row (screen width), and the game screen sits below the divider. Whole frame centered in the cabinet window.
- index.html: #hud-row flex (hud-wrap + equip-dom), #hud-div full-width divider, #screen-area below. game-frame left-aligned column so HUD strip + screen share the left edge and the box extends right. Fit recomputed against full column height (hud+3+screen).
- equip box moved back INTO the frame (from the out-of-bounds cabinet panel) as part of the HUD row.
- Verified: HUD row 42%, box 43%, divider (35,34,41) gray, screen 84%, 0% magenta.

## DROP 0720t — window halo purple -> orange (2026-07-20)
- The play-window edge glow (purple halo left after keying out the magenta) palette-swapped to ORANGE, preserving per-pixel luminance so the glow intensity is unchanged. Matches the cabinet fire theme.
- Verified: 0 purple halo px remaining, orange border 74k px.

## DROP 0720u — game fills full window below HUD (2026-07-20)
- Layout: game screen-area now fills the ENTIRE window area below the HUD row (full window width x remaining height), instead of a centered aspect-fit box. HUD strip spans window width minus the square equip box; divider full width; screen fills the rest.
- fitCanvas already stretches the canvas CSS to screen-area clientW/H, so the game fills fully.
- Verified: screen fills 99% of the below-HUD window, bottom corners 85-100%.
- NOTE: window-below-HUD aspect ~1.20 vs native game 0.94 -> game stretches horizontally to fill. Tradeoff of fill-fully; can switch to aspect-fit-with-bars if distortion is unwanted.

## DROP 0720v — aspect-locked fill (2026-07-20)
- Game now ASPECT-LOCKED in the window: native GA=0.938 preserved, screen fit into the below-HUD area (479x511), centered with ~67px pillarbox each side (shows cabinet window orange glow). No horizontal stretch.
- screen-area gets marginLeft=screenX to center; fitCanvas stretches canvas to screen-area (which is now aspect-correct).
- Verified: screen fills 99%, aspect 0.937 == native 0.938.

## DROP 0720w — explosion overhaul: rows + aircraft multi-burst (2026-07-20)
- Erased old-boss helicopter sheet (SourceFiles/enemies/generic_death_explosion.png).
- Sliced explosions_a/b/c source sheets into ROW-based anim strips -> nex_ keys: fireball(4), sparkorange(4), burstorange(4), burstblue(4), smallanim(13), single(1). 30 frames registered.
- nx_fire0 fixed to 7 FRAMES (frame 7 was a stray BLUE ice frame; excluded). nx_fire0=planes/jets primary, nx_fire1=additional bursts, nx_ice=ice-level enemies.
- PLANE/JET death now MULTI-BURST: explodeAircraft() fires 1 primary blast sized to the whole frame + 3-4 staggered secondary bursts across wings/nose/tail over ~0.4s (real jet look). Aircraft types: assault/gunship/scout/intcp/bomber/icegun/cryo/topgun/racer/sideswirl/jetflyby. Ice stages route to nx_ice (blue). updateAircraftBursts() ticked in main loop.
- Verified: assault kill -> 4 total explosions; nx_fire0 nf=7, nx_fire1 nf=8.
- TODO next: overlay smoke/fire on destroyed boss sections; bullets pass through destroyed L4 boss modules.

## DROP 0720x — explosion rows RE-SLICED at gaps (fix) (2026-07-20)
- FIX: previous slice divided each row into equal cells (total width / frame count), cutting through every frame. Now detects ACTUAL frame boundaries via empty-column gaps and crops each frame to its own bbox. Touching fireball row split into 4 equal parts of its span.
- Result: sparkorange/burstorange/burstblue each 4 clean growing frames (34->71px etc); smallanim 10 clean frames; fireball 4; single 1. Removed 3 stale manifest keys from the old bad slice.
- Verified: growth progression intact (small->big), no edge cuts.

## DROP 0720y — explosion rows: fireball uncut + magenta de-halo (2026-07-20)
- FIREBALL row: the 4 balls grow AND spread apart (centers at x25/101/192/301, not evenly spaced). Sliced at detected centers with cells spanning midway to neighbors -> frame 4 now fully captured (122x80), no cut.
- MAGENTA DE-HALO: 2-stage. (1) key true magenta only (R&B both high, G low) so blue/orange explosions are protected; (2) per-frame AFTER slicing: erode 1px alpha rim + kill magenta-tinted rim pixels + neutralize residual pink (pull B/R toward G). Applied per-frame so it doesn't fragment gap detection.
- Result: magenta/pink pixels across ALL 31 frames dropped 535 -> 5. Frame counts correct (fireball/spark/burst x4, smallanim 11, single 4).
- Existing enemy/vault sprites confirmed already clean (0-2 px).

## DROP 0720z — explosion sets trimmed + assigned by unit type (2026-07-20)
- Removed: burstblue (all 4), single (all 4), smallanim last 2 frames (now 9). Remaining: fireball(4), sparkorange(4), burstorange(4), smallanim(9).
- explode() gained a  param: kind=fireball -> nex_fireball; kind=spacecraft -> alternating nex_sparkorange/nex_burstorange.
- killEnemy routing: tanks/turrets (tank/htank/jungletank/mg/rock/turret/micro/turdrone) + ships (boat/naval/stationship) -> fireball. Space-stage aircraft -> spacecraft (spark+burst mixed). Sub-boss death chain -> fireball. Non-space planes/jets keep nx_fire multi-burst.
- Verified: tank->nex_fireball, boat->nex_fireball, space assault->nex_sparkorange+nex_burstorange, stage-2 assault->nx_fire0.

## DROP 0720aa — STORED 3 crucial source packs (2026-07-20)
- Stored + extracted 3 GPT-5.6 master packs into SourceFiles/ (originals archived in _incoming_zips/):
  1. weapon_vfx/ (84MB, 3197 files) — all player weapons L1-5 (mg/spread/missile/laser/firewall/iceorb/chain/helix) w/ muzzle+beam+impact; enemy weapons (jet/tank/naval/boss); powerup pickups L1-5.
  2. stages_true16bit/ (217MB) — per-stage Core_Roster enemies; SIX Themed_Stage_Bosses (canopy_devourer/magma_sovereign/cryo_seraph/runway_leviathan/event_horizon_harrower/ossuary_emperor) w/ clean/damaged/RUINED module atlases (breach fire/smoke meant to layer over ruined = perfect for section-destruction overlays); Modular_Bosses (Iron Revenant + Siege Mammoth X); Stage06 Furious Death finale boss.
  3. level06_aerial/ (41MB) — 7 exclusive jets (cloud-raptor/cyclone-widow/hurricane-warden/storm-talon/tempest-fang/thunder-lance); atomic-missile intercept set-piece (4 giant missiles); aircraft trails; full weather+cloud system; HUD radar; volcano FX.
- Full manifest: SourceFiles/_STORED_SOURCES.md. These are THE master sources — never regenerate.

## DROP 0720ab — 5 weapon effects rebuilt from VFX v2.2 (2026-07-20)
- Sliced from weapon_vfx pack (alpha frames, trimmed to bbox):
  1. ICE ORB -> nio_ (8f, from player-iceorb-lvl5). Wired into kind==orb render (drawImage, 12fps).
  2. MAVERICK helix laser -> nhx_ (16f, from player-helix-green-combined). Wired into venomx render (main grows by age, child animates).
  3. FALVA rollerball charge -> nrb_ (12f, from player-helix-mass-classic recolored FALVA_PINK 255,64,168). Wired into drawRollers.
  4. YURI chain lightning -> ncl_ (12f, from player-chain-lightning). Wired into drawZaps + kind==chain render.
  5. MACHINE GUN pellets -> nmg_ (6f, from player-machinegun-lvl5-projectile). Wired into kind==mg render, per-level glow color kept.
- All 5 first-choice with old art as fallback. Verified colors: iceorb blue, helix green, rollerball pink, chain gold, mg warm. Build green, all families registered.

## DROP 0720ac — MAVERICK helix CHARGE (Mega Man X style) + in-game weapon shots (2026-07-20)
- Sliced 2 more helix variants: nhxf_ (12f, blue/purple helix-mass-classic = FULL charge), nhxh_ (12f, green helix-mass-green = HALF charge).
- MAVERICK helix redesigned:
  * TAP fire -> green helix that SWIRLS as it travels (nhx_ 16f animates continuously in flight, was age-gated).
  * HOLD fire -> charges (mavCharge in updateSpecial, mirrors falvaCharge). Swirl particles spiral in, green -> violet as it tops out. MAV_HALF=0.75s, MAV_FULL=1.9s. FULL POWER ping + HELIX OVERDRIVE floattext.
  * Release >=HALF -> half-power GREEN mass helix (dmg 22+lv*5).
  * Release FULL -> BLUE/PURPLE mega helix: bigger (42x70), faster (-11.5), pierce, dmg 60+lv*10 (destroys fodder).
  * Charged shots do NOT split into strands; normal lance still does.
  * Normal auto-fire suppressed while charging past HALF.
- IN-GAME shots rendered for all rebuilt weapons (stage 1, real drawWorld at SS=2).
- Verified by color count vs baseline: normal helix +886 bright-green, half +917 green, full +1045 purple, rollerball +1053 pink. All weapons render.

## DROP 0720ad — L4 IRON REVENANT: shoot-through + breach fire/smoke (2026-07-20)
- BULLETS PASS THROUGH DESTROYED MODULES: modularPartAt() now SKIPS destroyed parts, so shots fly through blown-open cells and strike the ALIVE sections behind. Solid non-damageable hull cells still block (armor deflect chip retained for those). Verified: hitTest at destroyed part = false, at alive part = true.
- BREACH FIRE + SMOKE overlays on destroyed sections:
  * modularHit marks q._breach on destruction, breach blast now uses kind=fireball.
  * updateModularBoss vents per-breach smoke plumes (drifting up) + fire licks continuously, plus periodic cook-off explosions inside the hole (nex_fireball, every 1.1-2.6s).
  * drawModularBoss layers FIRE (nx_fire0, additive, flickers, fades with breach age) + heavy SMOKE (ntr_smkH, fallback nx_smoke) OVER the ruined module. Source pack ships ruined modules with effects intentionally NOT baked in - this is the intended layering.
- Verified: 3 breaches over 3.8s -> 742 particles + 5 nex_fireball cook-offs; render shows 224 fire px + 20109 smoke px on the boss.
- NOTE: test_fl.js assertion 'cook-offs walk outward' is FLAKY (RNG-dependent atomBooms timing, unrelated to this change) - passes on re-run.

## DROP 0720ae — boss purple halo FIX + swerving homing missiles (2026-07-20)
- PURPLE HALO FIXED: Iron Revenant modules had 1016 purple/magenta rim px (worst in the _dam states). Applied per-sprite de-halo (kill purple, erode 1px rim, neutralize residual cast) -> 0 px.
- Swept ALL sprites for the same defect using an EDGE-RIM test (purple on the alpha rim, NOT in the body) so genuinely pink/purple art is protected. 340 sprites de-haloed rim-only: 138585 -> 8318 purple px. Verified Falva pink art INTACT (special_falva 56k pink px, nrb_ rollerball 20k). Stage masters skipped (eroding their edge would open scroll seams).
- HOMING MISSILES: new eMissileHoming(x,y,dir) launches from the top racks, sweeps OUT to one side (weak turn, 0.42-0.62s), then LOCKS ON and hauls back into the player (hard turn 0.085), building speed 2.4->5.0. Boss fires a LEFT+RIGHT pair per live rack, so they converge from both directions. Verified trace: diverge to 120px spread by 0.5s, converge on player x240 by 1.25s. 3 racks -> 6 missiles per salvo.
- BUG FIX: enemy missiles had b.t incremented TWICE per frame (loop head + emissile block) — halved every missile timing. Now single.
- CRASH FIX: breach overlay used p.dx in a modulo; p.dx is NEGATIVE for left modules and JS % returns negative -> requested ntr_smkH_-3 -> drawImage(undefined) CRASH. Now positive modulo + per-key guards.
- Verified render: fire 1267 px, smoke 19369 px on breaches, purple halo 1 px.

## DROP 0720af — edge-anchored breach FX + boss fast looping scroll (2026-07-20)
- BREACH FX NOW EDGE-ANCHORED: new breachEdges(b,p) returns anchor points on the sides where a destroyed module borders STILL-ATTACHED structure (torn seams), each with an outward normal. Parts now carry r/c for neighbour lookup.
  * Smoke + fire particles vent FROM those seams, pushed along the edge normal (was: centred in the empty hole).
  * Fire + smoke SPRITES drawn per-edge too, so a hole with 3 intact neighbours burns on 3 sides.
  * Verified: centre module w/ 4 intact neighbours -> 4 anchors (correct normals); destroy the module above -> 3 anchors (top seam correctly gone).
- BOSS FIGHT = FAST LOOPING TERRAIN: while a boss is alive the master scrolls at BOSS_SCROLL_MUL=3.2x (128 px/s vs 40) and WRAPS seamlessly (window pulled modulo image height, remainder drawn from the opposite end) so the ground races continuously until the boss dies. On death it reverts to 40 px/s clamped.
  * Verified: 128 px/s boss-alive, 40 px/s boss-dead, no crash scrolling past the 2693px master height.

## DROP 0720ag — STAGE 6 HEAVY TURBULENCE authored w/ Level-06 exclusive jets (2026-07-20)
- Sliced the Level-06 Aerial Warfare pack jets: 6 airframes x 6 anim states = 210 frames.
  Keys n6j_<jet>_<state>_<frame>; states idle / bl / br / dmg / death / launch.
  Jets: raptor(CLOUD RAPTOR), widow(CYCLONE WIDOW), warden(HURRICANE WARDEN), talon(STORM TALON), fang(TEMPEST FANG), lance(THUNDER LANCE).
- Registered them as REAL enemy types: L6JETS catalog (hp 4-11, fireRate 1.0-1.6, score 460-950). spawnEnemy tags c._h6 and applies stats WITHOUT early-returning (that would have skipped enemies.push and they would never spawn).
- drawL6Jet(): animated draw picking state by context — destruction while dying, launch while firing homing, dmg under 45% hp, bank L/R by vx, else idle. Frame counts auto-detected per state.
- ROSTER FIX: stage 6 was still running the old 'FURIOUS DEATH prelude' roster despite being renamed HEAVY TURBULENCE (sub:HEAVY TURBULENCE, bg:sky). Authored a proper storm-front air-war roster: banking squadrons, skydiving widows, missile wardens, no ground armor. 13 waves.
- Verified: all 6 spawn with correct names/hp/scores, all tagged _h6, render in stage 6.

## DROP 0720ah — STAGE 6 sky: clouds, perspective, roll, thrusters, 3 attack styles (2026-07-20)
- Sliced Level-06 sky dressing: 6 CLOUD types (hi-altitude bank/stack, low-rolling, speed-wisps, storm-vortex, thunderhead) x6f + 5 THRUSTER trails (afterburner-heat, arcade blue/orange/cyan, twin-contrail) x8f = 76 keys.
- PARALLAX CLOUD DECKS: 4 decks (18 clouds) at different scale/speed/alpha. Far decks draw BEHIND everything, near decks (low-rolling + speed-wisps) sweep OVER the fight. Speeds 20-130 px/s verified distinct. Reset per stage-6 entry, cleared on other stages.
- PERSPECTIVE SCALING: l6HighDive spawns craft at _pScale 0.22 high above the field; they grow to 1.0 as they descend into the play plane (verified 0.22 -> 1.00 over ~1.1s).
- ATTACK FROM BEHIND: l6FromBehind spawns below the screen charging UP at the player (vy -2.6..-3.8) — verified y572 vy-3.17.
- FAST SIDEWAYS CROSSERS: l6Crosser screams across at vx 5.2-6.8 so you dodge fore/aft rather than left/right. Verified crossed 227px in 0.5s.
- BARREL ROLL / TWIST: the pack has NO roll art (bank-left/right only), so the roll is RENDERED — the airframe rotates (sin) and squashes through X (cos) across the roll cycle, giving a real barrel-roll read from bank frames. Crossers roll continuously (verified roll 0.00 -> 0.40).
- THRUSTERS anchored + overlaid on every L6 jet: drawThruster() scales with the craft and its perspective scale, rotates to travel direction, additive blend. Per-pattern colors (heat / orange / cyan).
- Stage 6 roster rewritten around the three styles: high dives, behind-attacks, single + pincer crosser runs. 14 waves.

## DROP 0720ai — STAGE 6: real SKY + GIANT ATOMIC MISSILES (2026-07-20)
- STORED Heavy Turbulence Environment Pack v1.0 (34MB) -> SourceFiles/level06_environment (zip archived).
- REAL SKY WIRED: nsky6_base (800x4000 base sky) as stage-6 master + nsky6_par (alpha cloud parallax, loops at 1.18x scroll) + nsky6_arena (800x1000 boss arena, LOOPS during boss instead of the master). _levelCfg case 6 flipped off the stale lvl6_master necro art. fill #2a6ac0. Verified 96% blue coverage in-scene.
- STAGE 6 IS NOW WIDE (800px world): worldWidth() extended — the recurring 800!=480 bug class struck again (was hardcoded stage 1). Camera scrolls horizontally like stage 1.
- l6Crosser fix: spawnEnemy clamps x into the field; crossers now set e.x truly offscreen post-spawn.
- GIANT ATOMIC MISSILES (164 keys: 4 missiles x fl/dmg/cd/dead/thr + shared det/debris/shock):
  * DRIFTER: rises slowly from below (hp 42). SHOOT IT -> atomic detonation + shockwave, blast R120 WIPES enemies (player-safe reward; verified by exact score math 460+520+250=1230). TOUCH IT -> you die (verified). Ignore -> exits top.
  * INTERCEPTOR: drops fast (vy 4.6-5.5) on the player lane, LOW hp 12 (focused fire or 2 homing missiles stop it), countdown-blink warning frames on approach, detonates on reach — hurts if within R84. Verified full flight -> detonation -> playerHit.
  * ESCORT (Contra-3 set-piece groundwork): rides alongside, NON-LETHAL touch (verified), unshootable, floats via SCALING (pScale 0.84-1.16 verified breathing) and inches upward — the stage-6 boss will use these as the weave-between hazards hammering the arena door.
  * Damage-state art by hp (3 tiers), per-missile thruster anchored at tail (additive), nose-down rotation for interceptors.
- Roster: 4 drifters (one double-spawn), 4 interceptors woven into the wave timeline.
- NOTE for playtest: sky top/bottom loop seam diff ~65 (cloud noise) — likely invisible at 128px/s; seam seeds shipped in pack if it shows. Missile hp/counts/radii are first-pass numbers — Mike playtest will tune.

## DROP 0720aj — STAGE 6 WEATHER: wind, rain bands, lightning (2026-07-20)
- Verified giant-missile FLIGHT sprites carry NO baked thrust (0 flame px in bottom 28% on all four) — the flames in-scene are the animated 8-frame thruster overlay only. Nothing to erase.
- Sliced weather + parallax scenery (52 keys): rain light/heavy/diagonal, storm squall, lightning flash; 12 parallax objects (wind streaks, storm turbine, radar balloon, refuel platform, weather tower, airborne debris, thundercloud, forked lightning, storm ring, cloud bank/wisp/puff).
- WEATHER BAND SYSTEM: stage walks clear -> windy -> squall -> storm (with occasional drop back to clear), 7-13s per band, HEAVY TURBULENCE floattext on storm onset. Verified all 4 bands cycle over 70s.
- WIND IS PHYSICAL: gusts shove the PLAYER sideways (verified 29.7px over 0.5s) and nudge loose aircraft — crossers exempt so their lanes stay readable. Gust strength scales with band intensity, decays naturally.
- 10 parallax storm objects drift with the scroll, drift with the gust, wind-streaks/debris rotate.
- LIGHTNING BUG FIX: the pack ships the flash as a STROBE — odd frames are intentionally EMPTY gap frames. First slice kept them, so the flash frequently sampled a blank frame (brightness 132.5 -> 133.5, invisible). Re-sliced dropping empty frames (8 -> 4 peaks) and switched the draw to ADDITIVE (partial-alpha exposure art needs it). Now 99% screen coverage, brightness 127 -> 166.
- Rain sheets tile across the 800px world width; storm layers heavy rain + squall together.

## DROP 0720ak — STAGE 6 BOSS: RUNWAY LEVIATHAN + Contra-3 door beat (2026-07-20)
- Picked RUNWAY LEVIATHAN from Themed_Stage_Bosses as the sky carrier (Siege Mammoth X is a ground super-tank — wrong for an aerial stage; parked for a ground level).
- Sliced 34 keys: 3x3 module grid x clean/damaged/ruined (mbp_rl_r#c#[_dam|_ruin], NOT trimmed so grid alignment stays exact), 5-frame bank anim, signature projectile + muzzle. Verified the 9 clean modules reassemble to exactly 192x192.
- DE-HALOED on arrival: 29 sprites, purple 1564 -> 0 (caught before wiring this time).
- LEVIATHAN_SPEC: 9 modules, scale 1.35. Centre cell is the ARMOURED DOOR.
- THE CONTRA-3 BEAT: door starts SEALED — player fire only chips it 6% (verified: 1000 dmg -> 60 lost, with a SEALED floattext). The boss launches ESCORT MISSILE waves (2-3 lanes every 3.4-5.0s) that ride up past the player and SLAM the door; impact breaches it for a 4.2s vulnerable window (140 dmg + DOOR BREACHED callout), during which normal fire does FULL damage (verified 500 dmg -> 500 lost). Window lapses -> RESEALED. ~2-3 cycles to kill.
- Escorts stay non-lethal to touch, so the player weaves between them while they do the breaching — the intended set-piece.
- Boss banks across the arena (sin drift, clamped to the 800px world). Arena backdrop already loops from drop 0720ai.
- Stage 6 boss flipped from null -> leviathan. Updated the STALE test assertion that asserted boss===null (it was a deferred-placeholder check) and added 2 new assertions for the spec + door module.
- Balance pass: first cut had the missile doing 460 of a 652hp door (one-shot). Rebalanced to missile 140 + door weight 2600->5200 so the loop is breach->pour fire->reseal.

## DROP 0720al — STAGE 8 FURIOUS DEATH: finale + 3-form boss (2026-07-20)
- Sliced the Furious Death finale boss: THREE forms (normal/super/ultra), each a 3x4 grid of 64px modules x clean/damaged/ruined = 108 module keys + 12 weapon frames. De-haloed on slice (purple 3512 -> 0). Verified each form's 12 clean modules reassemble to 192x256 and the three forms are visually distinct (31/34/42% coverage).
- FURIOUS_SPEC (12 modules) + FURIOUS_FORMS table (hpx 1.0/1.25/1.55, scale 1.15/1.28/1.42, faster missile cadence each form).
- THREE-FORM ESCALATION: clearing every module does NOT kill it — furiousBuildForm rebuilds the boss as the next shape at full (escalated) strength with a blast + form-name callout. Only ULTRA actually dies. Verified full chain: FURIOUS DEATH (2596hp) -> SUPER (mbp_fd2, 3245hp) -> ULTRA (mbp_fd3, 4024hp) -> death.
- STAGE 8 WIRED: _levelCfg case 8 -> nst6_master (the true-16bit necro finale backdrop; near-black by design, awaiting object layers like nst5). Boss flipped null -> furiousdeath. Authored an 18-wave finale roster: elite space craft, mine belts, mech walls, kamikaze pincers, octo swarms — relentless, no ground armor.
- NOTE: nst6_master avg brightness 3.4 (authored to sit UNDER unwired object/parallax layers). Reads as a dark void finale for now — fits tonally; wire the S8 object layer later for full detail.
- Stages remaining without identity: only STAGE 7 (sewer) now — no dedicated master or enemy sheet in any pack.

## DROP 0720am — campaign screen SOFT-LOCK fix + incoming-enemy HUD warnings (2026-07-20)
- CAMPAIGN "doesn't work" ROOT CAUSE: the STAGESEL cursor nav used `(sselCursor%9)+1` in a `do..while(sselCursor>unlockedMax)` loop — hardcoded for 9 stages and mis-clamped. With unlockedMax=1 (fresh game), a single left/right press silently walked the cursor 2->3->..->9->1 all the way around, so it NEVER appeared to move: the screen looked frozen/broken. Rewrote to clamp to [1, min(8,unlockedMax)] and wrap cleanly. Verified: unlockedMax=1 right stays 1; unlockedMax=4 cycles 1,2,3,4,1; left from 1 wraps to 4. (drawStageSelect/dispatch were fine; the flag loop's st<=9 was already guarded by missing SSEL_POS/art.)
- INCOMING-ENEMY WARNINGS (the requested HUD addition): drawIncomingWarnings() draws pulsing edge chevrons for threats that are OFF-SCREEN and inbound — from-behind attackers (red), fast side crossers + high-altitude divers still tiny (yellow), and giant interceptor missiles diving from above (bright red, larger). Chevron clamps to the nearest screen edge and points outward at the threat. Camera-aware (subtracts camX on the 800px-wide stages 1 & 6). Verified: 3 off-screen threats -> 3 chevrons at the correct edges (top/bottom/right), on-screen enemies produce none.
- Hooked after ctx.restore() in drawWorld so it draws in screen space over the field, under the HUD overlay.

## DROP 0720an — CAMPAIGN SCREEN v2: cinematic boot, retina sweep, camera unlock (2026-07-20)
Mega-Man-X-style map progression pass per Mike's spec (refs: MMX stage select, Magic Carpet 2, Dungeon Keeper).
- BOOT SEQUENCE rebuilt as a phase machine: TACNET terminal (1.7s) -> WHITE FLASH CUT -> map interior
  ZOOMED 1.42x past the baked border (slow drift) -> camera pulls back easeOutCubic so the border
  SWEEPS IN and LOCKS around the window (clunk SFX + shake + edge flash at land). The border is baked
  into nss_map, so the lock is done with the camera — zero new art. Verified z: 1.43 -> 1.06 -> 1.00 + clunk.
- FLAGS drop 1-by-1 (0.20s apiece, blip each, 14px drop-in ease) — SECRET level 9 excluded entirely.
- TARGET RETINA (the game's own retA_/retB_ pilot reticle art) sweeps flag-to-flag with blips (0.16s/hop),
  then LOCKS (retB + select SFX) on the playable flag. Menu music starts at the lock: IRON CAGE
  (picked from the new tracks — tense military war-room loop; battlesky/hotflight/fierceplanes read as
  flight themes, lordshadows as boss. One-line swap if preferred). Verified music log: exactly ['ironcage'].
- FLAG RULES: playable frontier flag = ORIGINAL GREEN art, NO palette swap (was red-tinted). Beaten = rank
  tints, locked = gray. Verified 681 green flag px on the live map.
- STAGE BANNER: on cursor move the panel scales in 0.45 -> 1.0 (easeOutBack overshoot) and the stage name
  TYPES ON letter-by-letter via clip-reveal with a bright type-edge cursor + tick blips (0.55s).
- UNLOCK CINEMATIC rebuilt as a CAMERA move: wait(0.45) -> fly to the new flag z1 -> 2.15 (easeInOutCubic
  0.8s) -> three dings while the gray flag flashes -> at ding-end the REAL unlock happens (unlockedMax bump
  deferred to this moment so the gray -> true-colors unfurl actually reads) + powerup SFX + LEVEL N UNLOCKED
  text -> unfurl beat -> zoom back 0.7s -> cursor lands on the new stage. openStageSelect({unlock:N}) now
  holds the stage LOCKED on entry. Verified: unlockedMax held at 2 during zoom, cursor landed on 3, cine completed.
- Camera verified numerically: border-corner diff 21.8 (borderless vs locked), unlock-zoom diff 36.1 vs final.
- PLAYTEST notes: boot is ~7.5s total (skippable? not yet — say the word); type-on tick rate 14/s may want
  taming; ironcage is my pick not a decree.

## DROP 0720ao — WEAPONS v2.3: helix strand pairs + orb-free chain lightning + Maverick coil (2026-07-20)
- Stored 6 new packs (helix/chain v2.3, Level 05, Level 07, Level 08, Bonus Warp Run, Bosses & SubBosses v1.1). Only helix/chain wired this pass; rest logged PENDING in _STORED_SOURCES.md.
- HELIX REBUILT: the pack ships TWO INDEPENDENT strands per helix (16f each) instead of one pre-composed sprite. New drawHelixPair() draws BOTH, strand B running half a cycle out of phase — that is what makes it actually intertwine. Verified 9 A/B centroid crossings in the source art and 13-of-75 rows showing two separated strands in-game (rest are crossover points) = genuine double-helix weave.
  * Cells kept UNTRIMMED (96x384, pivot 48,8): A and B must stay pixel-registered or the interlock breaks. Art grows DOWNWARD from its pivot, so the renderer flips vertically to fire upward.
  * Normal shot = GREEN pair, animating continuously in flight, sized as a long laser streak (58+lv*7).
  * HALF charge = green pair scaled up; FULL charge = CLASSIC blue/purple pair. Old nhx_/nhxf_/nhxh_ single sprites fully out (0 refs).
- CHAIN LIGHTNING REBUILT (the "ball effect" is gone — pack QA: 0 orb primitives, 0 round nodes):
  * New nchain_ 12f growth sequence (trunk -> branch spread -> peak -> recession), 384x384 pivot (192,8).
  * drawChainBolt() stretches the narrow TRUNK band (source window 150,2,84,104) along an arc — a real forked bolt, not a stretched blob. drawChainBurst() plays the BRANCHING frames at the struck node, replacing the old round ring flash.
  * Applied to BOTH chain systems, which are separate: (1) the chain WEAPON's zaps/projectile — the projectile is now a travelling bolt drawn tail-to-head instead of an orb sprite; (2) YURI's pilot signature spawnChainArc/chainarc, which was still on the old gold chain_bolt_ + nch_ fork art.
  * Verified in-game: 2345 cyan bolt px and ZERO bright blobs >150px (ball-free check passes).
- MAVERICK CHARGE VISUAL (parity with Falva's aura/orbs, built from his own weapon): the two helix strands COIL around the ship while fire is held — strand A drawn BEHIND the hull, strand B in FRONT, which is what sells the wrap. Counter-rotating, coil tightens and whips faster with charge, colour shifts green -> classic violet at full, plus an overdrive ring pulse at 100%. Hooked at both drawPlayer call sites like Falva's. Verified coil intensity climbs 84.3 -> 87.7 -> 96.5 across 18%/58%/100% charge.
- NEXT: Level 05 wiring.

## DROP 0720ap — LEVEL 5 ALL FOR ONE, NONE FOR ALL + modular _clean BUGFIX (2026-07-20)

### BUGFIX (mine, from drops 0720ak/al) — healthy boss modules were INVISIBLE
drawModularBoss builds its art key as `p.art + "_" + tier` where tier is clean|dam|ruin.
Iron Revenant was sliced with a `_clean` suffix (correct), but the LEVIATHAN (stage 6) and
FURIOUS DEATH (stage 8) were sliced with the healthy state as a BARE key. So at full health the
lookup missed and `if(!XART.rdy(k)) continue;` silently skipped the module — both bosses only
became visible as you damaged them. Verified: leviathan 9/9 and furious death 12/12 parts missing
`_clean`, iron revenant 0/12 (baseline). Renamed 81 bare healthy keys -> `_clean`. Post-fix all
three bosses resolve 0 missing. Leviathan visible structure 7% -> 25% on the same shot.

### Level 5 wired
- Background: Level05 pack v1.0 800x3616 gameplay scroll -> norb5_base (stage master), 800x1000
  boss arena -> norb5_arena (loops during boss, same pattern as stage 6). Replaces the legacy
  lvl5_master. Content verified 29% above threshold (space void with real structures, not near-black).
- STAGE 5 IS WIDE (800px world): worldWidth() extended again — S1 jungle, S5 orbit, S6 sky. That is
  the FIFTH time the 800!=480 class has come up; the pack ships 800px sections so this was expected.
- ORBITAL PARALLAX FIELD: 12 props (6 asteroids + 6 orbital hardware) across 3 decks — far hardware,
  mid asteroid belt, near debris sweeping OVER the fight. Verified 20-22px/s drift and 6 distinct
  deck speeds. Resets per stage-5 entry, cleared elsewhere.
- ELITE ORBITAL CAPITALS (dreadnought-vanguard / iron-tidal-cruiser / tempest-carrier): 12 components
  each, intact + damaged. IMPORTANT: the pack's component-map shows these are NOT a tiled grid —
  every component is a FULL 256x384 canvas overlay drawn at the same pivot (128,192). Compositing all
  12 at the origin yields the complete ship (~50% opaque); tiling them produced a 5%-opaque smear.
  Added an `overlay:true` branch to buildModularBoss: art draws full-canvas (dx/dy 0) while hitboxes
  come from a 4x3 hit grid derived from the rc indices. Verified 12/12 distinct hit cells, each
  resolving to its own component, and all `_clean` art present.
- Stage 5 roster authored: 15 waves of capital-ship engagement — fighter screens, mine belts,
  gunship drops, kamikaze pincers, octo swarms. No ground armour (respects tanks-on-1-and-4).
- Effects sliced and registered: n5_thr (thruster), n5_smk (engine damage smoke), n5_exh (missile exhaust).

### PENDING for level 5 (deliberately not rushed)
- Canonical bosses UNITY-BREAKER and FRACTURE-TWINS (22 png each) — not yet wired.
- space-event-horizon (named-component scheme + 6x3 atlas) and battlefield-command-carrier
  (6-frame damage-transition scheme) use different layouts than the 3 wired capitals.
- continental-crusher: 4x4 grid of 256x256 cells with FOUR directional variants (north/south/east/west)
  = 384 files. My first slice collapsed the directions onto the same keys; those keys were REMOVED
  rather than shipped wrong. It also reads as a tracked ground unit, which conflicts with the
  tanks-only-on-1-and-4 rule — parking it pending Mike's call.

## DROP 0720aq — LEVEL 5: space drones only, no jets (2026-07-20)
- Mike: "there should be our space drones on level 5, no jets."
- ROOT CAUSE of the jets: there were TWO `if(stageNum===5)` blocks. A STALE pre-renumber roster
  ("GOD HELP US ALL — deep space") sat EARLIER in buildStagePlan and returned first, so the orbital
  roster I authored in 0720ap never executed at all. The stale one was full of aircraft
  (sideswirl, gunship, racer, topgun, jetflyby). Removed it.
- Rewrote the stage-5 roster to space drones only: drone (the classic ROBO drone atlas — note
  `drone` resolves to recon JETS on stage 1 and ROBO drones on stage 2+), mdrone, octo, mine,
  shieldd, minidrone, minicarrier, mech, plus kamikaze pairs (which spawn drones).
- VERIFIED by firing all 14 authored waves and auditing every spawn against the engine's own
  _AIRCRAFT and _GROUND tables: {drone:27, octo:9, mine:10, mdrone:7, shieldd:4, minidrone:3,
  mech:1, minicarrier:1} -> JETS: NONE, GROUND: NONE.
- AUDITED EVERY STAGE for the same duplicate-block class: stages 1 and 2 also have duplicate
  roster blocks, BUT in both cases the CORRECT current block wins and the stale one is unreachable
  dead code, so there is no behaviour bug. Stage 1 is off-limits per standing rule — reported, not
  touched. Stages 3-8 have exactly one block each.

## DROP 0720ar — STAGE 5 ASTEROIDS: true-vacuum hazards you shoot or dodge (2026-07-20)
Mike: rotate + float like true gravity, kill on contact, shootable, beefy, flash white->orange->red
then animate to destruction. Star Fox by way of Bullets of Fury.
- NEW l5Rocks system, separate from the l5Field parallax decor. The near parallax deck no longer
  fakes asteroids (it carries orbital hardware now) — every rock in the play plane is a real object.
- TRUE-VACUUM MOTION: constant velocity and conserved angular momentum, NO drag. Heavier rocks
  drift and tumble slower (vy/sqrt(sc), spin/sc). Verified velocity and spin unchanged after 1s
  and big rocks confirmed slower-tumbling than small.
- BEEFY: hp = 30 + sc*70 -> ~68 (small) to ~135 (large). Verified 85 / 104 on sample spawns.
- DAMAGE READ: sustained heat tint by tier plus a hit flash whose colour escalates with damage.
  >66% clean + WHITE flash; 33-66% ORANGE; <33% RED. Verified in-render by colour cast —
  R-B spread +12 (clean) -> +102 (orange) -> +140 (red).
  BUG CAUGHT IN TESTING: the first tier table scanned for `frac <= threshold` and picked the last
  match, which made RED unreachable (it only matched at exactly 0 hp, i.e. the death frame).
  Replaced with an explicit l5RockTier(frac).
- SHATTER: no rock-destruction frames exist in the pack, so rather than invent any the break throws
  3-5 SMALLER COPIES of the pack's own asteroid sprites spinning outward and fading, over a
  fireball explode(). Verified debris flies apart (1px -> 30-75px in 0.5s) and cleans up after 0.9s.
- CONTACT IS LETHAL, and the existing double-tap BARREL ROLL already grants 32 i-frames for its
  full duration — so rolling through a rock punches clean through it. Verified both: walking in
  triggers playerHit and shatters the rock; rolling in takes no hit. That is the level's core loop.
- Steady field spawner: one rock every 1.6-3.1s, ~28% chance of a large one.
- PLAYTEST: rock HP, spawn cadence and blast radius are first-pass numbers. Rocks currently keep
  spawning during the boss fight — may want gating if it reads as unfair.

## DROP 0720as — ENEMY AI PATTERN LIBRARY from Mike's behaviour sheets (2026-07-20)
Stage-agnostic, mirrorable, reusable on every level. Core idea decoded from the drawings:
the LINE is a fast entry, the NUMBER on it is the depth where the craft DECELERATES to give the
player a fighting chance, and past that it keeps advancing quicker than normal but survivable.
- CORE: aiAttach(e,cfg) + aiTick() + a new 'ai' movement pattern. AI_ENTRY 3.1x -> AI_CRUISE 1.0x,
  eased by AI_DECEL. VERIFIED: 5.05 px/frame before the number -> 2.40 settled after, still advancing.
- SEQUENCED SPAWNS: aiDelay/aiQueueTick stagger a wave ~1s apart ("one mississippi, two mississippi").
  VERIFIED gaps of 0.98 / 1.02 / 1.00s and staggered slow-depths y172/228/284/318 (sheet 1's staircase).
- WAVE BUILDERS, all mirrorable via dir:
  * aiWaveRush     (sheet 1)      n craft in from the top, each slowing at its own depth.
  * aiWaveSplit    (sheet 2)      one peels LEFT, one peels RIGHT, a third CHARGES and RNG-breaks.
                                  VERIFIED net x -155 / +155, and the fork went left 8 / right 4 over 12 runs.
  * aiWaveSweep    (pattern #1)   a stack sweeping in from one side at staggered depths.
                                  VERIFIED mirror: x -46->461 from the left, 526->19 from the right.
  * aiWaveColumns  (pattern #2)   two vertical columns plus a crosser cutting the lane (dx +507 vs dx 0).
  * aiWaveLoop     (pattern #3)   looping lead craft (swings on BOTH axes) with diagonal escorts crossing.
  * aiWaveDroids                  any of the above flown by spinning droids.
  * aiWaveFromBelow               see fairness rule below.
- FAIRNESS RULE (Mike's): nothing slides in from under the player. aiWaveFromBelow spawns them
  ON-SCREEN arriving from ALTITUDE — scaling up from 0.18 with a drop shadow (aiShadowDraw) so you
  see them coming. VERIFIED every craft first appears on-screen, never below VH.
- DROIDS (sheet 3): TRUE canvas rotation, not a sprite flip — the hull is rotated live (2.6 rad/s idle,
  3.4x mid-evade) and the twist additionally squashes it through X so it reads as a barrel roll rather
  than a flat spin. Droids READ INCOMING FIRE and roll out of the lane, which forces you to bomb them,
  barrel-roll past, or swing back and re-engage. VERIFIED evade triggers on a closing round
  (_evadeT 0.23, twist 0.22, 12px out of the lane).
  Tuning caught in testing: the first evade lane was e.w*0.9 so droids only dodged dead-centre shots
  and barely read as evasive — widened to e.w*1.4.
- WOVEN INTO ROSTERS: stages 2,3,4,5,6,8 get 3-4 AI waves each (mix of sheet 1, pattern #1 both
  mirrors, sheet 2, patterns #2/#3, droids, and an altitude arrival on 5). STAGE 1 UNTOUCHED per
  standing rule — verified 0 AI waves on stage 1. Stage 7 still has no roster block of its own.
- PLAYTEST: entry/cruise speeds, the ~1s gap, evade frequency and loop radius are all first-pass numbers.

## DROP 0720at — AI corrections: pattern #3 flies STRAIGHT + edge-clamp bug (2026-07-20)
- Mike: pattern #3's escorts should go STRAIGHT ACROSS with no steer-off; the curving version is a variant.
  * Added a new 'diag' AI kind: a fixed straight diagonal that only DECELERATES at its number, never steers.
  * aiWaveLoop now = looping lead craft + two STRAIGHT diagonal escorts crossing (the X in the sheet).
  * Kept the old behaviour as aiWaveLoopCurved (steer-off variant), and added aiWaveCross for a pure X with no loop lead.
  * VERIFIED by perpendicular deviation from a start->end line: straight diagonals 0.2%, curved variant 21-28%.
    Lateral rate falls 3.57 -> 1.17 px/frame in exact step with the 3.1x -> 1.0x deceleration (ratio 0.33), i.e.
    the craft slows but its DIRECTION never changes.
- Sheet 2 confirmed already correct: the centre craft charges and RNG-breaks left or right (8 left / 4 right over 12 runs).
- BUG FOUND while verifying: a global edge clamp (with an allow-list for "drifting" patterns) was pinning any
  AI craft that crosses the screen to the wall — a "straight across" run bent and then rode the edge at x=461
  instead of exiting. AI crossers (sweep / diag / curve) are now exempt from the clamp and culled once clear.
  Post-fix a cross run exits cleanly at x=522 with 0.2% deviation.

## DROP 0720au — enemy assignments corrected across levels (2026-07-20)

### MY ERROR — the "clipped frames" were my contact sheet, not the game
Mike reported minidrone/minicarrier frames cut off and minicarrier art bleeding into mech's box.
Investigated the atlas directly: a connected-component test proved every e1_ frame FITS inside its
declared rect — nothing is clipped at source. The real cause was my lineup sheet: minidrone draws
at 128x128 and minicarrier at 155x155 (art size x e1scale 1.7), but I laid them out on a 120px grid
with 104px crop boxes, so minicarrier overflowed into mech's cell and both got cut. Rebuilt the sheet
rendering each enemy ALONE on its own canvas with a tight crop around its real ink extent —
verified 0 edge-touching pixels on all seven, i.e. nothing is cut off.

### Reassignments (all verified by firing every wave of every stage and auditing spawns)
- 'drone' is a JET (levels 1 & 6 art) -> REMOVED from level 5.
- mdrone reads as the same unit as shieldd -> level 5 flies shieldd only.
  (For the record the sprites are genuinely different art — 48% silhouette overlap — but they are
  the same role, so only one flies there.)
- minidrone + minicarrier -> LEVELS 2 and 8 (removed from 5, confirmed present on both).
- The three capitals are SURFACE VESSELS per the pack's own component map ("giant modular naval
  boss") -> re-homed from level 5 to LEVEL 6's water intro. L5CAP_SPEC/L5_CAPITALS renamed to
  L6CAP_SPEC/L6_CAPITALS (alias kept so the spawn hook still resolves).
- Battlefield Command Carrier -> LEVEL 6 water intro. New 'bcarrier' enemy type (hp46, 2600pt),
  sliced 6-frame damage transition + 17-frame destruction, with drawBCarrier() picking the damage
  frame from current HP and the destruction frames while dying.
- LEVEL 5 final roster: octo, mine, mech, shieldd + the asteroid field + the AI wave library.
  Deliberately lean until the pack's own units land next (unity-breaker, fracture-twins,
  space-event-horizon, continental-crusher).
- Level 6 opening now has water-intro waves; the WATER BACKDROP itself is still to author.

### Verified rules (all PASS)
stage 5 has no drone / no minidrone+minicarrier / no mdrone / zero jets;
levels 2 and 8 both have minidrone+minicarrier; level 6 has bcarrier.

## DROP 0720av — orbital roster found + 7 new art sheets stored (2026-07-20)

### Corrections logged
- Level 1's green miniboss is OLIVE MAULER (esB_big5, jungle-camo gunship, accent #7f8646) via the
  SUBBOSS table — NOT the 'minidrone' type. Checked both bossdrone variants: _0 is steel, _1 is red,
  neither is green. So minidrone on levels 2 & 8 does not collide with level 1's miniboss.
  Re-confirmed by roster audit that stage 1 spawns no minidrone. Level 1 untouched.
- octo confirmed staying on level 5.

### THE ORBITAL ROSTER (found, still UNWIRED) — Stage05 "Black Hole Space", true-16bit pack
4 dedicated deep-space enemies, 64x64 logical / 128x128 export, each with 3 damage states
(clean / damaged / ruined) on fixed centres for direct state swaps:
  * singularity_needle  — alien interceptor        hp 24
  * eventide_crescent   — gravity fighter          hp 44
  * void_hauler         — orbital gunship          hp 68
  * scrap_oracle        — zero-g salvage crawler   hp 56
Pack notes: enemies are never baked into the starfield; thrusters, gravity cores, shields and
weapon effects are SEPARATE overlays; damaged uses heavy_damage_smoke_8f, ruined transition uses
large_destruction_explosion_8f, aircraft breach uses wing_breach_fire_8f.
This is the proper level-5 cast — it replaces leaning on the generic octo/mine/mech/shieldd set.

## TO-DO LIST (accumulating)
### New art sheets stored 2026-07-20 -> SourceFiles/incoming_sheets_0720/ (all magenta-chroma, need keying)
 1. turrets_tanks_ships_jets_rot7.png     — turrets/tanks/ships/jets at 7 rotation angles each,
                                            multiple palettes. Feeds true-rotation ground + naval units.
 2. turrets_tanks_boats_jets_2f.png       — turrets, tanks, patrol boats, jets, 2 frames each.
                                            BOATS are the missing piece for level 6's water intro.
 3. hud_reticles_arrows_warnings.png      — targeting reticles, lock brackets, direction arrows,
                                            warning triangles, "SHOOT!" callout. Upgrades the
                                            incoming-enemy warning chevrons + retina lock art.
 4. ground_emplacements_damage_muzzle.png — bunker turrets w/ damage states, muzzle flashes,
                                            shell casings, smoke, debris, palette ramps.
 5. bunker_turrets_rot_destruction.png    — rotating bunker turrets + full destruction sequences.
 6. ui_frames_cursors_pickups.png         — UI frames, cursors, pickup/powerup icons, chevrons.
 7. helix_trails_4colour.png              — helix/lightning trails in BLUE / GREEN / PURPLE / PINK,
                                            13 frames each. Pink = Falva. Pairs with the v2.3 helix work.

### Queue
- Wire the 4 orbital enemies as level 5's real cast (with their 3 damage states + separate overlays).
- Unity Breaker + Fracture Twins (level 5 has NO boss at all yet).
- Space Event Horizon (named-component scheme) and Continental Crusher (4x4 x 4 directions;
  reads tracked/ground — awaiting Mike's call).
- Level 6 water intro BACKDROP (naval units are wired, the water itself is not authored).
- Stage 7 still has no roster block of its own.

## DROP 0720aw — LEVEL 5 ORBITAL ROSTER WIRED + halos re-inked (2026-07-20)
- HALO FIX (Mike): rather than punching the magenta/purple rim to transparent (which leaves a ragged,
  lighter silhouette), the rim is RE-INKED TO BLACK so each sprite keeps a crisp 16-bit outline.
  Only RIM pixels convert — interior purple that is part of the design (glow cores, engine light) is
  preserved. Verified: rim purple 2592 -> 0 across all 12 frames, interior glow kept
  (needle 97 / crescent 163 / hauler 44 / oracle 70 px), black outline laid in on every sprite.
- 4 enemies x 3 damage states sliced (nob_<id>_<clean|dam|ruin>); art swaps off current HP
  (>60% clean, >25% dam, else ruin) — all three states verified present for each.
- SIGNATURE BEHAVIOURS:
  * SCRAP ORACLE — PINBALLS down the field, ricocheting off the WORLD edges (800px on stage 5, not
    the 480 camera) and tumbling as it caroms. Vacuum physics: keeps its speed through every bounce.
    Verified 3 clean bounces off both walls while descending monotonically.
    BUG CAUGHT: first cut used its own bounce margin, so the engine's global edge clamp pinned it to
    the wall at x=759 before it ever reached the bounce threshold — zero bounces. Margin now matches
    the clamp exactly (max(14, w*0.66)).
  * VOID HAULER — climbs to station, LEVITATES (sine bob), drifts slowly to its chosen side, and
    CHARGES a heavy beam (visible growing charge glow) before releasing a thick sustained laser.
    Verified charge -> fire at charge 1.20, beam width 22.
  * EVENTIDE CRESCENT — FLASHES WHITE as a wind-up tell, then fires a TRIAD of real BEAMS.
    Verified 3 simultaneous beams at angles 0 / -0.34 / +0.34 and eBullets stayed 0 — genuine beams,
    never balls.
  * SINGULARITY NEEDLE — Mike had no call for this one, so PROPOSED: strafing interceptor. Knifes in,
    holds a beat, then slashes across the field and swings back. Fragile (hp24) but hard to pin.
    Verified phase loop in -> hold -> slash -> hold -> slash. EASY TO CHANGE.
- New BEAM system (orbBeams): real damaging columns of light with snap-open + fade, angle support,
  and per-frame player-intersection damage. Cleared on stage start.
- BUG CAUGHT: the new types had their pattern randomised away by the byType picker because they were
  not in the _selfPat allow-list — orbitalTick never ran at all. Added needle/crescent/hauler/oracle
  and bcarrier to _selfPat.
- Stage 5 roster rebuilt around the orbital cast (needle/crescent/hauler/oracle) with octo, mine and
  mech in support, plus the asteroid field and AI waves.

## DROP 0720ax — orbital FX use REAL art; oracle re-done with gravity (2026-07-20)
- MY ERROR: the first beam pass drew columns with ctx.fillRect — procedural, which breaks the
  standing "never create placeholder/procedural effects, search the vault first" rule. Replaced with
  the game's own art:
  * VOID HAULER heavy shot -> laserbeam_0..4 (178x896, 5-frame animated column), cycled at 22fps.
  * EVENTIDE CRESCENT triad -> beam_blue down the centre + beam_purple on both diagonals
    (46x223 stills stretched along the beam). Verified art keys in flight: ["beam_blue","beam_purple","beam_purple"].
  A drawn-rect fallback remains ONLY if a key is missing.
- CHARGE EFFECTS from the weapon-VFX pack's own enemy energy art (nothing hand-drawn):
  * nchg_orb_0..7  (enemy-boss-energy-orb, 8f)    -> Hauler: swelling, spinning orb at the muzzle
    that grows 16->62px and speeds up as the shot builds.
  * nchg_sph_0..7  (enemy-boss-energy-sphere, 8f) -> Crescent: sphere blooms 18->72px across the
    white-flash wind-up, counter-rotating, right before the triad fires.
  VERIFIED by differential render (charging frame vs idle frame, flat backdrop): hauler 2492 px
  change centred on its muzzle, crescent 1831 px — both confirmed drawing.
- SCRAP ORACLE re-done per Mike: it now JUMPS. Kicks off, ARCS under gravity (9.0/s^2), lands on an
  invisible floor and kicks again; the floor walks down the screen so it keeps advancing. Caroms off
  the walls of space to stay on screen. STAYS UPRIGHT — the tumble/spin is gone (_spinA pinned to 0).
  Verified over 6s: 7 landing kicks (arc restarts), 2 wall bounces, y rising and falling while
  trending downward, spin angle exactly 0.

## DROP 0720ay — BOSSES & SUB-BOSSES PACK OPENED: 71 units found, level 5 boss wired (2026-07-20)
I had STORED this pack back in the 6-zip intake and never inventoried it. Mike was right — it is the
single biggest content find of the project.

### What is in it (71 bosses/sub-bosses, each level-tagged by its OWN component map)
- LEVEL 4: missile-citadel-omega (BOSS), runway-reaper (sub), airbase-siege-fortress
- LEVEL 5: **unity-breaker (BOSS)**, **fracture-twins (sub)**, space-event-horizon
- LEVEL 6: storm-sovereign (BOSS), cyclone-harrier (sub), hellwing-death-carrier
- LEVEL 7 (the stage with NO identity): **cesspool-leviathan (BOSS), rat-king-excavator (sub),
  sewer-purge-barge, bio-sludge-abomination, toxic-dredger** — stage 7 finally has a cast.
- LEVEL 8 "VILE EXISTENCE" 4-FORM FINALE: form1-apostle-cocoon -> form2-venom-ascendant ->
  form3-necrotic-leviathan -> form4-furious-death, with morph-overlay + 6-frame morph transitions
  and a death-implosion overlay. Sub-boss venom-reaver ("Herald of Death"). This supersedes the
  3-form Furious Death chain wired in drop 0720al.
- Naval modular (256x384): dreadnought-vanguard, iron-tidal-cruiser, tempest-carrier, sewer-purge-barge
- Robo-jet modular (192x192): bone-wasp, cryo-scarab, ember-mantis, golden-widow, jungle-hornet, venom-reaver
- Mech modular (192x192): ice-colossus-form1/2, inferno-valkyrie
- ~20 real-world jets as full 192x256 action sheets (134 png each): f16/f22/f35/su57/mig29/rafale/
  typhoon/gripen/hornet/super-hornet/strike-eagle/black-eagle-j20/sukhoi-flanker/hawker/kawanishi
- Themed elites: jungle-thorn-predator, jungle-siege-crawler, jungle-overlord-x-helicopter,
  magma-colossus, lava-magma-reaver, cryo-behemoth, glacier-rail-fortress, ice-crystal-lancer,
  obsidian-drill-tank, rampart-zero, iron-vulture, storm/inferno units, dam-breaker, continental-crusher

### Wired this pass — LEVEL 5 FINALLY HAS A BOSS
- UNITY BREAKER = stage 5 boss (was boss:null). 256x256, 5 NAMED components
  (left_systems / front_core / central_core / rear_core / right_systems) x intact/damaged/critical.
- FRACTURE TWINS = level 5 sub-boss, 192x192, same 5-component scheme.
- Their component maps ship EXPLICIT component RECTS, so hitboxes are AUTHORED, not derived from a
  grid like the L6 capitals were. Added a `named:true` overlay branch to buildModularBoss that reads
  those rects verbatim. Verified authored hitboxes 61x184 / 62x61 / 62x61 / 62x62 / 61x184 and a
  per-component hit test resolving all five correctly.
- Pack draw rule honoured: every component drawn at the identical boss x/y, never trimmed (dx/dy 0).
- Purple rim re-inked to black on both (7944 + 5668 px), interior glow preserved.
- Unity Breaker hp 2132 across 5 parts; Fracture Twins hp 1312.
- Also available on these two and unused so far: idle-6f, bank-turn-7f and barrel-roll-8f animation
  strips — the boss can bank and barrel-roll.

### Queue after this
- Stage 7 sewer cast (boss + sub + elites now all exist).
- Level 8 Vile Existence 4-form chain (supersedes the current 3-form wiring).
- storm-sovereign / cyclone-harrier for level 6; missile-citadel-omega / runway-reaper for level 4.

## DROP 0720az — BOSS PACK QA RE-SCAN + full showcase (2026-07-20)

### RE-SCAN FINDING 1 — cross-frame bleed is REAL, and it is in the PACKED SHEETS only
Scanned all 554 multi-frame sheets in the bosses/sub-bosses pack, testing whether ink crosses the
cell boundaries implied by each sheet's own filename (-Nf, -RxC, -WxH).
  * 81 sheets have ink CROSSING a cell boundary.
  * The signature is a CONSTANT overhang at every boundary (space-event-horizon 78px at x192/384/576/768,
    airbase-siege-fortress 44px, sukhoi-flanker 38px) — i.e. the sprites are WIDER than the declared
    cell, so each frame overhangs into the next. Naive equal-division slicing would put a slice of the
    neighbour in every frame, which is exactly the "frames broken up into other frames" Mike saw.
  * Worst: rampart-zero-special-attack (710px), space-event-horizon destruction/idle/primary/damage
    (390-546px each), airbase-siege-fortress, furious-death-hellwing, sukhoi-flanker, jungle-overlord-x-rotor.
  * Affected units: furious-death-hellwing, felon-su57, sukhoi-flanker, space-event-horizon,
    strike-eagle-f15, jungle-thorn-predator, airbase-siege-fortress, kawanishi-experimental,
    black-eagle-j20, iron-vulture, ice-crystal-lancer, super-hornet, rampart-zero, rafale.

### THE SAFE PATH (rule locked in)
Every affected unit ALSO ships individual -fNN frame files — 2505 of them across the pack.
Sampled 358: **0 rim halo, 0 files needing repair**. They are self-contained.
  RULE: ALWAYS slice from the -fNN individual frames or the named component files.
        NEVER slice from a -Nf / -RxC packed sheet.
(Unity Breaker and Fracture Twins use named components and were already sliced that way — clean.)
Note: 50 of 358 sampled individual frames have art touching their own canvas edge; that is design
fill on wide airframes, not a cut, but worth eyeballing when those units get wired.

### RE-SCAN FINDING 2 — halo sweep across everything already sliced
Scanned all 4492 registered images, then scoped to the 834 pack-sliced files (Falva's pink, the
purple helix strand, pilot cards and stage masters are INTENTIONAL colour and were excluded).
  * Only 15 pack-sliced files still carried a rim fringe -> re-inked to black, 678px -> 0.
  * Mostly nchg_orb (the energy orb is legitimately purple; only its outer fringe was converted,
    the energy body keeps its colour), plus npo_turbine, nob_oracle_dam and one weather object.

### SHOWCASE rendered (BOF_pack_showcase.png) — all from clean sources
  * LEVEL 5: unity-breaker (BOSS, wired), fracture-twins (SUB, wired), space-event-horizon (63 frames),
    continental-crusher (4x4 x 4 directions)
  * REAL-WORLD JETS, 192x256 with 63 individual frames each: F-22, F-35, SU-57, MIG-29, Rafale,
    Typhoon, F-16, F/A-18, Super Hornet, F-15E, Gripen, J-20 (+ hawker, kawanishi, sukhoi-flanker)
  * ROBO-JET MODULAR (192x192, 5 components): bone-wasp, cryo-scarab, ember-mantis, golden-widow,
    jungle-hornet, venom-reaver
  * MECH MODULAR (articulated hands + separate anchors): ice-colossus form1/form2, inferno-valkyrie
  * THEMED ELITES: jungle-thorn-predator, magma-colossus, cryo-behemoth, obsidian-drill-tank,
    iron-vulture, storm-sovereign, glacier-rail-fortress, lava-magma-reaver, dam-breaker,
    rampart-zero, hellwing-death-carrier, jungle-siege-crawler

## DROP 0720ba — MIKE'S FULL ASSIGNMENT PASS (2026-07-20)

### Clipping report (all three checked at source)
- BLACK EAGLE J-20: REAL defect, exactly where Mike said. The right wing runs off the 192px canvas
  (bbox x128-191, 20px of ink on the edge) and EVERY source file is cut — idle, master, intact,
  damaged, critical, the components atlas, all of it. REPAIRED by mirroring the unit's OWN clean
  left wing (x10-63) about the canvas centre -> right wing now x128-181 with 0 edge pixels, for all
  three states. Repairs live in SourceFiles/_repairs/black-eagle-j20/ and the showcase renderer
  prefers a repaired part when one exists.
- CRYO BEHEMOTH and GLACIER RAIL FORTRESS: CLEAN at source — all 63 individual frames each,
  0 edge contact on every side, checked across idle / movement / damage-transition. Whatever looked
  clipped was my thumbnail, not the art. Both have full 12-action kits (idle, movement, primary,
  special, hit-reaction, damage-transition, destruction + muzzle/projectile/charge overlays).
- DAM BREAKER: SCRAPPED per Mike's condition — it has no rotor/spin frames anywhere in its folder.

### ASSIGNMENTS RECORDED (authoritative)
  bone-wasp            -> LEVEL 5, purple/black spreadfire-style laser      [WIRED THIS PASS]
  cryo-scarab          -> level 3
  ember-mantis         -> level 2
  golden-widow         -> level 4
  jungle-hornet        -> level 1
  venom-reaver         -> level 7
  iron-vulture         -> level 4 (as-is)
  storm-sovereign      -> level 6
  lava-magma-reaver    -> FLIP VERTICALLY to face the player; good as a straight enemy
  glacier-rail-fortress-> level 4
  rampart-zero         -> STRETCH HORIZONTALLY; breakable environment blocker that must be
                          destroyed before you can advance (mini-boss feel)
  obsidian-drill-tank  -> level 4
  cryo-behemoth        -> NEW LEVEL 3 BOSS
  magma-colossus       -> NEW LEVEL 2 BOSS
  continental-crusher  -> FLIP so the turrets face the player; destructible turret on level 4
  hellwing-death-carrier -> level 8
  jungle-siege-crawler -> NEW LEVEL 1 MINI-BOSS. Flip vertically so turrets face the player.
                          Moves ONLY up and down, slow like a tank, fires QUAD machine guns
                          (two dual-MG turrets).
                          NOTE: this is an explicit instruction to change LEVEL 1, which the
                          standing rule otherwise protects. Flagged, not yet actioned.
  real-world jets      -> levels 1, 4 and 6 (per-jet split still to be decided — see jets sheet)
  SCRAPPED: dam-breaker, ice-colossus-form1, ice-colossus-form2, inferno-valkyrie

### Wired this pass — BONE WASP (level 5)
- Sliced from NAMED COMPONENT files (never the packed sheets). 192x192, 5 components x
  intact/damaged/critical, authored rects -> hitboxes 51x154 / 51x51 / 51x51 / 51x51 / 51x154,
  per-component hit test resolves all five. Purple rim re-inked to black (82px).
- SIGNATURE WEAPON: a five-beam PURPLE fan from one muzzle at angles -0.44/-0.22/0/+0.22/+0.44,
  mirroring how the player's spreadfire opens up. Verified 5 simultaneous beams, art key
  beam_purple, and eBullets stayed 0 (real beams, never balls).

### Every unit in the pack is now assigned — nothing left over.
The only open question is WHICH jet goes to WHICH of levels 1/4/6; the 16 airframes are on the
jets sheet for Mike to split.

## DROP 0720bb — CLEANUP + MIKE'S LEVEL ASSIGNMENTS WIRED (2026-07-20)

### Stray-fragment cleanup (the units Mike flagged)
Built clean_strays.py: a blob is a leaked neighbour if it is BOTH far smaller than the unit's main
body (<22%, raised to 35% for two wing files) AND physically detached from it (>4px gap). Legitimate
detached parts (wingtip missiles, escort pods) are large or close-in and survive.
  * sukhoi-flanker 3 blobs -> 1, kawanishi-experimental -> 1, cyclone-interceptor-carrier -> 1
    (its 1484px fragment at x10-43 is gone), typhoon -> 1.
  * Ran across the whole pack: 831 files repaired into SourceFiles/_repairs/.
  * PURE-FX folders were EXCLUDED (morph-overlay, death-implosion, existence-core-pulse,
    tendril-slash, venom-orb, bone-shard, morph-transitions) plus every *fx-overlay* and
    destruction frame — detached particles are correct there and must not be stripped.
  * BLACK EAGLE J-20 right wing (a genuine source cut) was already repaired by mirroring its own
    clean left wing; all slicers now prefer a repaired file when one exists.

### Assignments WIRED
  LEVEL 1 MINI-BOSS  jungle-siege-crawler   flipped so its turrets face the player, patrols
                                            UP/DOWN ONLY at tank speed, QUAD machine guns from two
                                            dual turrets. Verified: modular, flipped, art present,
                                            vertical patrol, 4 distinct barrels per burst, 56 rounds
                                            in 5s. Replaces OLIVE MAULER in the SUBBOSS table.
                                            (Explicit Mike instruction to touch level 1.)
  LEVEL 2 BOSS       magma-colossus
  LEVEL 3 BOSS       cryo-behemoth
  LEVEL 6 SUB-BOSS   storm-sovereign        NOTE: I first overwrote stage 6's boss with it and
                                            reverted — RUNWAY LEVIATHAN keeps the boss slot because
                                            it carries the Contra-3 door set-piece already signed
                                            off. Storm Sovereign sits in the sub-boss slot instead.
  cryo-scarab -> L3 · ember-mantis -> L2 · golden-widow -> L4 · jungle-hornet -> L1
  venom-reaver -> L7 · iron-vulture -> L4 · glacier-rail -> L4 · obsidian-drill -> L4
  hellwing-death-carrier -> L8
  lava-magma-reaver  FLIPPED VERTICALLY so it faces the player
  rampart-zero       stretched 2.6x horizontally into a breakable blocker
  SCRAPPED: dam-breaker (no rotor frames), ice-colossus form1/2, inferno-valkyrie

### Engine work
- `named` overlay specs now cover three layouts: _mod5 (5 components), _air6 (6-component airframe
  with the pack's authored rects: nose/fuselage/weapons-bay/tail + two wings), and _body1 (units the
  pack ships as one body). Caught iron-vulture and lava-magma-reaver rendering nothing because they
  are 6-component airframes, not 5.
- Added vertical-flip and horizontal-stretch support to the modular renderer.
- Sub-bosses can now be modular: spawnSubBoss builds the crawler, drawSubBoss delegates to
  drawModularBoss, updateSubBoss ticks it.
- Updated the stale test assertion that pinned level 1's mini-boss to OLIVE MAULER; it now asserts
  the siege crawler AND that it is flipped.

### Still open
- Jets: which of the 16 go to level 4 vs level 6 (Mike: "level 4 uses more of the ones we didnt,
  level 6 uses the last") — needs the actual split.
- continental-crusher: flip so turrets face the player, destructible L4 turret (4x4 x 4 directions,
  needs its own slicer).
- Roster placement: the assigned units are spawnable and verified but not yet woven into wave lists.

## DROP 0720bc — JET AIRFRAMES SPLIT ACROSS LEVELS 4 AND 6 (2026-07-20)
Mike: order doesn't matter, just make sure each level gets different ones.
- All 16 real-world airframes sliced from NAMED COMPONENTS (never packed sheets), preferring the
  REPAIRED file where one exists — 59 of the sliced states came from repaired sources, including
  Black Eagle's rebuilt right wing and the stray-fragment fixes on Sukhoi / Kawanishi / Typhoon /
  Rafale / the Cyclone carrier.
- 15 use the pack's 6-component airframe layout with authored rects (nose_cockpit, center_fuselage,
  weapons_bay, tail_engines, left_wing, right_wing) at 192x256. The cyclone-interceptor-carrier has
  no component map and ships as a single body, so it uses the _body1 spec.

  LEVEL 4 (9): F-22 Raptor · F-16 Falcon · F-15E Strike Eagle · F/A-18 Hornet · Super Hornet ·
               MiG-29 Fulcrum · Sukhoi Flanker · J-20 Black Eagle · Hawker Interceptor
  LEVEL 6 (7): F-35 Lightning · Su-57 Felon · Rafale · Typhoon · Gripen · Kawanishi ·
               Cyclone Interceptor Carrier

- VERIFIED: all 16 spawn, every one resolves clean/dam/ruin on every component, ZERO overlap between
  the two levels, and all 16 render non-empty in isolation.
- Per-airframe HP multipliers vary (Gripen 1.00 lightest -> Su-57 1.35, carrier 1.9) so they don't
  all feel identical.

### Still open
- Weaving the jets and the other assigned units into actual WAVE LISTS (they are spawnable and
  verified, but the rosters have not been rewritten yet).
- continental-crusher: flip so turrets face the player, destructible L4 turret (4x4 x 4 directions).
- Level 7 sewer cast, Level 8 Vile Existence 4-form chain.

## DROP 0720bd — WAVE LISTS WRITTEN (2026-07-20)
- NEW ELITE ENEMY PATH: the pack's modular units can now fly as ORDINARY roster enemies. A boss
  occupies the single global boss slot, so instead the unit's components are composited ONCE per
  (unit, damage state) into a cached canvas and drawn as a normal sprite. Damage follows HP
  (clean >60%, dam >25%, else ruin). 26 elites defined; VERIFIED all 26 composite in all three states.
- Elites added to _selfPat so the byType randomiser can't clobber the pattern the roster gives them.
- WAVES WRITTEN into stages 1, 2, 3, 4, 6 and 8:
    L1  jungle hornet pair
    L2  ember mantis + a pair of lava magma reavers (flipped to face the player)
    L3  cryo scarab, solo then paired
    L4  the 9-airframe jet wing (F-16 / F-18 sweep / MiG-29 / F-22 rush / Flanker / F-15E + Hawkers /
        Super Hornet + J-20) woven with GOLDEN WIDOW, OBSIDIAN DRILL TANK, GLACIER RAIL, IRON VULTURE
    L6  the 7-airframe wing (Gripen / Rafale sweep / Typhoon / F-35 rush / CYCLONE CARRIER / Su-57 /
        Kawanishi) on top of the existing storm-front roster
    L8  Hellwing Death Carrier, solo then paired
- Verified by firing every wave of every stage: L4 carries jet_f15/f16/f18/f22/hwk/j20/m29/shn/su27,
  L6 carries jet_cic/f35/grp/kaw/raf/su57/typ — ZERO overlap, exactly as Mike asked.
- STAGE 7 LEFT UNTOUCHED on purpose — Mike wants to see its roster before we edit it.

### LEVEL 7 + 8 CURRENT STATE (for Mike's review before the sewer pass)
  LEVEL 7 "NOT ANOTHER SEWER LEVEL"
    * NO stageNum===7 roster block exists at all — it falls through to the generic timeline,
      which is why it currently spawns a grab-bag: assault, cryo, drone, frost, gunship, icegun,
      mech, mine, octo (borrowed from other stages, no sewer identity).
    * STAGES table: length 58, bg 'sewer', boss: null  <- NO BOSS.
    * _levelCfg has NO case 7 -> falls to default null -> procedural background, no master art.
    * Available in the pack, unwired: cesspool-leviathan (BOSS), rat-king-excavator (SUB-BOSS),
      sewer-purge-barge (naval, 256x384 modular), bio-sludge-abomination, toxic-dredger,
      venom-reaver (already assigned here by Mike).
  LEVEL 8 "FURIOUS DEATH"
    * Has a full 21-wave roster (drone/octo/mine/mech/gunship/kamikaze/topgun/racer/sideswirl/
      minidrone/minicarrier + AI waves + the new Hellwing carrier).
    * Boss: furiousdeath (the 3-form chain from drop 0720al).
    * The pack's 4-FORM "VILE EXISTENCE" chain (apostle-cocoon -> venom-ascendant ->
      necrotic-leviathan -> furious-death, with 6-frame morphs, death-implosion overlay and
      venom-reaver as "Herald of Death" sub-boss) is UNWIRED and supersedes the current 3-form boss.

## DROP 0720be — LEVEL 8 "VILE EXISTENCE" 4-FORM BOSS + sub-bosses (2026-07-20, overnight pass)

### The canonical finale is wired — it supersedes the 3-form chain from drop 0720al
  form1 APOSTLE COCOON -> form2 VENOM ASCENDANT -> form3 NECROTIC LEVIATHAN -> form4 FURIOUS DEATH
- All four forms: 256x256, 5 named components x intact/damaged/critical, authored rects.
  Sliced from named component files (never packed sheets); purple rim 2521 -> black.
- MORPHING: clearing every component does NOT kill it — the shell breaks, a 6-frame MORPH
  TRANSITION plays over the boss, and it re-forms stronger. Only form 4 dies, into a 6-frame
  DEATH IMPLOSION overlay. Morph sheets were checked for cell bleed first: 0px on all three.
- VERIFIED full chain in one run: 2596 -> 3168 -> 3843 -> 4673 -> death, every form resolving all
  5 components in all 3 states, morph art and implosion art all present.
- HP/scale escalate per form (1.00/1.22/1.48/1.80 and 0.78/0.86/0.94/1.02).

### Sub-bosses added
- LEVEL 8: HERALD OF DEATH (venom-reaver, retitled per the pack's own phase manifest).
- LEVEL 7: RAT KING EXCAVATOR (sliced, 15 states) — ready for when stage 7 gets built.
Both spawn through the modular sub-boss path and verified art-complete.

### CONTACT SHEETS delivered
- BOF_L8_boss_sheet.png   : all 4 forms + the morph transition + the death implosion + the Herald.
- BOF_L8_roster_sheet.png : all 17 stage-8 enemy types, each rendered in isolation (no bleed).
  Verified every cell non-empty, and the forms visibly grow across the chain (5.1/5.1/7.2/10.0%
  screen coverage).

### NOTE FOR MIKE
Stage 8's boss now points at 'vileexistence'. The older 3-form 'furiousdeath' boss and its art
(mbp_fd1/2/3) are still in the build and still work — nothing was deleted — so it is a one-line
revert in the STAGES table if you prefer the old one.
Stage 7 still has NO roster block, NO boss and NO background master; its cast (cesspool-leviathan,
rat-king, sewer-purge-barge, bio-sludge, toxic-dredger, venom-reaver) is all in the pack unwired.

## DROP 0720bf — LEVEL 8 BOSS WING REPAIR (2026-07-20, overnight)
Mike: "all of the level 8 bosses have additional frames clipped into them except herald of death."
He was right, and the Herald being the exception is exactly what pinned the cause.

### Diagnosis
Ran three tests before touching anything:
 1. Ink outside each component's authored rect -> 0 on every component. Components are bounded.
 2. Composite vs the pack's OWN master (form1-...-intact-256x256.png) -> 0 extra px, 0 missing.
    So the assembly was correct; the defect was already baked into the source master.
 3. LEFT vs RIGHT wing mass — this is what found it:
        form1 APOSTLE COCOON     L 9314  R 4676  ratio 0.50
        form2 VENOM ASCENDANT    L 7966  R 5088  ratio 0.64
        form3 NECROTIC LEVIATHAN L 9802  R 5130  ratio 0.52
        form4 FURIOUS DEATH      L 7852  R 6030  ratio 0.77
        venom-reaver (HERALD)    L 4504  R 4372  ratio 0.97  <- the clean one
    Every Vile form ships a right wing at HALF to three-quarters of its left, shattered into
    3-8 disconnected fragments, while the left wing is one solid piece. The Herald is symmetric,
    which is precisely why it looked right.

### Repair
These creatures are bilaterally symmetric, so each right wing was rebuilt by MIRRORING that unit's
OWN left wing about the canvas centre — repair from its own art, nothing invented. The mirror lands
exactly on the authored right_systems rect. form1's hull is narrower than the others, so its
mirrored wing was additionally seated 5px inward to close the seam.
Applied to all 4 forms x intact/damaged/critical.

### Result (verified)
  APOSTLE COCOON     L 9314 R 9314 ratio 1.00   composites as ONE piece
  VENOM ASCENDANT    L 7966 R 7966 ratio 1.00   composites as ONE piece
  NECROTIC LEVIATHAN L 9470 R 9802 ratio 1.04   composites as ONE piece
  FURIOUS DEATH      L 7810 R 7852 ratio 1.01   composites as ONE piece
  HERALD             untouched — it was already correct
Full 4-form chain re-verified after the repair: 2596 -> 3168 -> 3843 -> 4673 -> death, all art present.
Repairs live in SourceFiles/_repairs/form1..form4/ and the slicer prefers them automatically.

## DROP 0720bg — REVERTED my bad wing "repair" on the level 8 forms (2026-07-20, overnight)

### I got drop 0720bf WRONG and Mike caught it
He reported the forms were "still doubling into each other" after my fix. He was right, and the
doubling was MY doing.

WHAT I ASSUMED: the right wings measured 50-77% the mass of the left with fragmented blobs, so I
concluded they were truncated and rebuilt each one by mirroring the unit's own left wing.

WHAT WAS ACTUALLY TRUE: the right wings are a DIFFERENT DESIGN, not a truncated mirror. The test
that proves it is width, not mass —
    form1  L w71  R w50    mirrored-L vs original-R IoU 0.28
    form2  L w71  R w71    IoU 0.34
    form3  L w65  R w65    IoU 0.29
    form4  L w49  R w47    IoU 0.49
The widths match; the right wing is simply a lighter, more open design. Mirroring the left over it
duplicated the left wing's shapes onto the right — which is exactly the "doubling" Mike saw.
LESSON: mass asymmetry alone does NOT mean an asset is truncated. Check the BOUNDS before concluding
anything is cut, and treat "different" as design until the geometry says otherwise.

### Fully reverted + a second bug found while reverting
- Removed every mirrored right-wing repair for form1-4.
- Also removed the general stray-cleaner's repairs for form1-4 and venom-reaver entirely. Comparing
  our composite against the pack's own master showed we were MISSING 98-351px per form: the cleaner
  had been stripping small legitimate detail (glints/specks) that reads as "detached". Those units
  now use the pack originals VERBATIM.
- Re-sliced all four forms and the Herald from originals.

### Verified after revert
  f1 extra 0 / missing 0   EXACT MATCH to the pack master
  f2 extra 0 / missing 0   EXACT MATCH
  f3 extra 0 / missing 0   EXACT MATCH
  f4 extra 0 / missing 0   EXACT MATCH
Full chain still runs: 2596 -> 3168 -> 3843 -> 4673 -> death, all art present.

### STILL OPEN FOR MIKE
Our art is now pixel-identical to the pack's own masters, so anything that still looks doubled is
in the SOURCE masters themselves, not in our slicing or drawing. I have deliberately NOT "fixed"
it again — I would be guessing at intent twice in a row. Attached MASTER_VS_GAME.png shows the pack
master beside our in-game render for each form so the comparison is direct.

## DROP 0720bh — level 8 forms: exhaustive cut-off audit (2026-07-20, overnight)
Mike: "you're clipping the wings off form 2, form 3 and form 4 into the other frames."
Chased it through every stage of the pipeline. Every measurement came back clean:
  1. components-5x3 source sheets — ink crossing a cell boundary: 0 on all four forms.
  2. Form MASTERS (intact-256x256) — ink touching the canvas edge: 0 L/R/T/B on all four.
  3. Individual component files — ink touching their own canvas edge: 0 on every component.
  4. Our sliced composite vs the pack master — 0 extra px, 0 missing px, EXACT MATCH on all four.
  5. In-game rendered frames — no edge contact; art spans 179-204px inside a 480px canvas.
So the source is complete, the slice is exact, and the renderer draws the whole sprite. Nothing is
being cut in the data or in the game.
=> The clipping Mike is seeing is in MY CONTACT SHEETS, not the game. Rebuilt them:
   * every panel is now a BOXED 250px cell with 26px separation and 14px inner padding, so no two
     sprites can read as sharing a frame;
   * plus BOF_L8_form1..4 and BOF_L8_herald as INDIVIDUAL 3x-upscaled images with 40px margins —
     no grid at all, so there is no neighbouring frame to bleed into.
NOTE: this follows me getting drop 0720bf wrong (mirroring the wings). The lesson stands — I keep
mis-reading my own contact-sheet layout as an art defect. When Mike reports clipping, check the
SHEET GEOMETRY before touching any art.

## DROP 0720bi — retina/bomb REGRESSION fix, difficulty ease, mini tanks + ships, weapon upgrades (2026-07-20)

### BUG FIXED — "holding C for retina and firing bombs no longer works"
REPRODUCED it: the combo works for every pilot UNTIL Cole's or Lizzie's special is active and its
strikes run out. Then the bomb key went COMPLETELY DEAD — you keep a full bomb stock but nothing
fires for the rest of the special.
CAUSE: retinaFire() and lizzieFire() both ended with an unconditional `return true`, so they
swallowed the missile key even when they had no target and no strikes left. The hold-to-repeat path
in updateRetina made it worse: it branched on specialActive() and never fell through to useBomb().
FIX: both now return TRUE only when a strike actually launches, and the hold path falls through to
useBomb() when the special declines.
VERIFIED per pilot, special active, strikes 3 and 0:
  cole   strikes 3->0 bombs 9->0 FIRES  |  strikes 0 bombs 9->6 FIRES  (was: dead input)
  lizzie strikes 3->0 bombs 9->0 FIRES  |  strikes 0 bombs 9->6 FIRES  (was: dead input)

### DIFFICULTY — "too many homing missiles, especially level 1; game a little too hard"
- ENEMY MISSILE BUDGET: every enemy missile funnels through eMissile(), so the thinning is applied
  once, centrally. Per-stage allowance 45/60/70/80/85%. MEASURED over 400 attempted launches:
  stage 1 -> 40%, stage 2 -> 59%, stage 3 -> 70%, stage 4 -> 79%, stages 5+ -> ~85%.
- DIFFICULTY TABLE eased across the board. NORMAL now: enemy bullet speed 1.0 -> 0.88, enemy fire
  rate 1.0 -> 0.80, enemy HP 1.0 -> 0.88, wave density 1.0 -> 0.85, starting lives 3 -> 4,
  starting bombs 2 -> 3, drop rate 1.0 -> 1.25. Easy/Hard/Furious eased proportionally.

### MINI TANKS (levels 1 & 4) and SHIPS (level 3)
- Sliced from Mike's incoming sheet by CONNECTED-COMPONENT masking rather than a grid guess, so no
  neighbour can bleed in — 118 sprites across 9 rows, each isolated to its own label.
- Six units: minitank/2/3 (39x39) and minishipA/B/C (44x31), drawn at ~0.86-0.90 scale so they read
  as emplacements. All DESTRUCTIBLE (verified: focused fire -> hp 0 -> dead).
- They fire PELLET BALLS: a 3-round spread burst on a cadence, using the engine's existing 'pellet'
  bullet kind (real mfx_mg_2 tracer art, not a drawn blob). Verified 3-6 pellets per 3s each.
- They slowly turn to face the player so the sheet's 7 rotation steps actually get used.
- Woven into stage 1 (3 waves), stage 4 (2 waves) and stage 3 (3 waves).

### WEAPON UPGRADES
- MAVERICK helix lance — level now adds LANCES, not just length: L1-2 one, L3-4 twin, L5 triple with
  the outer pair angled out. Verified 1/2/3 lances at wlevel 1/3/5, damage 12/20/28.
- YURI chain lightning — arc reach 150 -> 150+lv*26, per-link damage 3 -> 3+lv*2, chain depth
  2+min(2,lv) -> 2+min(4,lv). Verified 4 arcs at L1 vs 7 at L3/L5 against a 7-enemy formation.
- Updated two stale test assertions that pinned venom to a single lance; they now pin their tier
  explicitly and three new assertions cover the upgrade path.

## DROP 0720bj — TERRAIN RULES for mini tanks and ships (2026-07-20)
Mike: ships must be scaled down to fit the water and cannot pass the snowy rocks; tanks cannot climb
the cliffs on level 1; each unit patrols along its own axis (vertical sprites up/down, horizontal
sprites left/right); sand is open ground and fair.

### New terrain system
- _buildTerrain(img, key, kind) classifies the STAGE MASTER by colour into a passability mask,
  cached per (master, kind). Sampled straight off the art, so it always matches what is drawn.
    'ground' (tanks): open sand/soil/light growth PASSABLE; dark rock cliffs and water BLOCKED.
    'water'  (ships): genuine water only; snow, ice shelf and rock all BLOCKED.
  Measured on the real masters: jungle 74% drivable, ice 41% navigable.
- miniTerrainOK(kind,x,y,footW) tests the unit's LEFT, CENTRE and RIGHT footprint, not just a
  centre point, so a hull cannot half-hang over a cliff edge.

### Movement
- TANKS (drawn facing up) patrol UP/DOWN; SHIPS (drawn side-on) patrol LEFT/RIGHT. On hitting
  blocked terrain the unit reverses instead of pushing through.
- Ships now HOLD their water lane (no independent vy) because the channel scrolls past them;
  tanks still roll down with the map.
- The master scrolls underneath, so units can be carried into blocked ground. Recovery searches
  BOTH axes (8 directions, out to 140px) for the nearest valid footing and slides the unit there —
  a boat tracks its channel, a tank steps back off the rock. If no footing exists at all the unit
  retires rather than beaching.

### Sizes
- Ships scaled down to fit the ice channels: 34x24 -> 24x17 (A/B) and 26x18 (C), draw scale
  0.90 -> 0.62/0.64. Tanks unchanged at 30x30 / 0.86.

### Verified over 400 frames each
  TANKS  400/400 frames on valid ground (0 violations), vertical patrol, 0px lateral drift
  SHIPS  400/400 frames on valid water  (0 violations), horizontal patrol, 0px vertical drift
  (first cut had ships at 184/400 — they were sinking through their channel because the pattern
   applied vy and the recovery only searched sideways; both fixed.)

## DROP 0720bk — HUD ICON SET sliced + wired (2026-07-20)
All icons pulled from Mike's two sheets. Purple/magenta fringe RE-INKED TO BLACK (not deleted) so
the icons keep a hard edge and pop — verified 0px purple remaining on all 25.

### SPEED BOOSTERS (Mike: level 6 + rival dogfights)
- nspd_up/down/left/right from the chevron ranks. Laid through level 6 in 5 groups.
- Ride over one and it shoves the ship 4.6px/frame in its heading for 0.55s and bumps the speed
  stat — that is how you slip an incoming asteroid or missile.
- The chevron FLASHES WHITE at 7fps (additive over-draw every other 1/7s) so a live pad reads from
  across the screen; a used pad scales up and fades out.
- Verified: rode a pad, boost applied, player displaced 106px.
- Rival-dogfight use is ready to hook when that mode gets rebuilt.

### BOSS RETINA (Mike: the box outgrows big units)
- nbret_<pilot> from the crosshair ring, recoloured for ALL 9 pilots (luminance-preserving tint).
- _bigTarget() routes boss / sub-boss / any unit >=64px to the crosshair, which sits DEAD CENTRE on
  the unit at a FIXED 58px — it never balloons with the target. Small enemies keep the bracket retina.
- Verified: Iron Revenant (w 172.8) uses it, a drone (w 29) does not. Homing missiles work unchanged
  since it is the same retina lock.

### OBJECT-INCOMING ARROWS
- nobj_blue/red x up/down/left/right. These REPLACE the hand-drawn chevrons I had been using for
  the incoming-enemy indicators — red for lethal (from-behind / interceptors), blue for the rest.

### WARNINGS + SHOOT
- nwarn_yield / nwarn_alert / nwarn_shoot, plus showCallout(kind) -> a centred callout that snaps
  in, strobes at 7fps and fades.

### MENU SELECTOR
- nsel_arrow: the north triangle rotated 90 deg RIGHT at slice time, now flanking the selected
  menu button (mirrored on the right side) in place of the old text glyphs.

## DROP 0720bl — MENU CURSOR rising-white animation + chroma-key fix (2026-07-20)
Mike: the cursor should flash white starting at the BOTTOM, with the white RISING quickly to the
top, then a flash, short delay, repeat.

### The animation
- drawSelArrow(x,y,h,mirror) with a 3-phase cycle: RISE 0.20s -> FLASH 0.10s -> REST 0.62s
  (0.92s total). The rise is a clip band that climbs from the arrow's bottom edge to its top,
  revealing a cached WHITE SILHOUETTE of the sprite; at the top the whole unit pops, then it rests.
- Verified frame-by-frame: white pixels climb 2257 -> 3090 -> 4771 -> 7244 -> 9322 -> 11075 -> 11869
  (peak = the flash), then fall back to the 2257 baseline and hold through the rest.

### BUILD TRAP hit and fixed
My first version went into gamecode.js right before drawMenuButtons — which sits INSIDE the span
assemble.py replaces with blocks['B_TITLE'] from patches.js. The build silently dropped all of it
(0 occurrences in the output). Moved the helpers into the SAFE ZONE after the goTitle one-liner and
pointed the real title menu in patches.js at drawSelArrow. Confirmed present in the built game.js.

### CHROMA-KEY BUG fixed (this was the blue box behind the cursor)
The strict key (r>200 & b>200 & g<90) missed ANTI-ALIASED magenta, so semi-dark magenta survived as
OPAQUE pixels — nsel_arrow came out 57.8% opaque with solid corners, drawing a box behind the arrow.
Replaced with a FLOOD-FILL key: a loose magenta test is labelled, then only components CONNECTED TO
THE SHEET BORDER are cleared, so background goes and interior detail stays.
Verified: all four corners now alpha 0, fully-opaque columns 4 -> 0, and a rendered frame has zero
fully-set rows/columns (a box would show many). Re-sliced all 25 HUD icons through the new key.

### Delivered
BOF_menu_cursor.gif (55 frames, 30fps, ~50KB) and BOF_menu_cursor_frames.png (labelled strip).

## DROP 0720bm — BUNKER TURRETS + ground emplacements wired (2026-07-20)
Two of the incoming sheets were still unused; both are now sliced and one family is fully in play.

### Slicing
- Flood-fill chroma key (the fix from 0720bl) + connected-component isolation, so no sprite carries
  a neighbour and no anti-aliased magenta survives as opaque pixels.
- bunker_turrets_rot_destruction -> 36 sprites: TWO turret types, each with a base, 7 ROTATION
  STEPS and a 6-FRAME DESTRUCTION sequence.
- ground_emplacements_damage_muzzle -> 77 sprites: emplacements with damage states, muzzle flashes,
  shell casings and debris. Sliced and registered; not yet wired to a unit.

### BUNKER TURRETS (levels 1 and 4)
- Dug-in, stationary. They TRACK the player through the 7 authored rotation steps, fire a twin
  pellet burst with a muzzle pop, and are fully destructible.
- Killed bunkers do NOT pop instantly: they play their own 6-frame COLLAPSE, then clear.
  Verified frames 0,1,2,3,4,5 all play in order (rubble ink grows 5887 -> 9453 as it spreads).
- bunkerA hp26 / 900pts, bunkerB hp32 / 1100pts. Placed on stage 1 (2 waves) and stage 4 (2 waves).

### Two bugs caught in testing
- The per-frame `hp<=0` sweep re-entered killEnemy on an already-collapsing bunker and the second
  pass killed it instantly, so only frame 0 ever drew. Added an early return for units mid-collapse.
- Aim mapped the FULL circle across 7 steps, but the player is nearly always BELOW an emplacement,
  so 5 of the 7 steps were unreachable and the turret barely turned (steps 4-5 only). Remapped to
  the right->down->left arc: the turret now sweeps 4 -> 3 -> 2 as the player crosses the screen.

### Still open
- ground emplacement family (77 sprites) sliced but unwired.
- helix_trails_4colour (pink = Falva), turrets_tanks_boats_jets_2f (boats for the L6 water intro).
- Stage 7 sewer build, continental-crusher flip, rival dogfight rebuild.

## DROP 0720bn — 360-DEGREE TURRETS (24 frames @ 15 deg) + a major wide-stage spawn bug (2026-07-20)
Mike: turrets need full 360 motion with 15-degree frames, placed in the SAND on the SIDES of level 1,
firing dual MG bursts or single missiles, never moving.

### The frames
- The sheet only ships 7 rotation steps. Measured the barrel bearing on each and found frame 0 of
  both types points UP (~95-100 deg), so that frame is the canonical origin and the full circle is
  GENERATED from it — 24 frames at 15-degree steps per turret, 48 total.
- Canvas squared and centred before rotating so every frame shares one pivot: 0 frames clipped.
- VERIFIED end to end: a player orbiting the turret produces 24/24 DISTINCT frames, with
  0deg->frame 0, 90deg->6, 180deg->12, 270deg->18. Exact mapping.

### Behaviour
- turretMG  : DUAL machine guns — a 3-round burst from two barrels offset perpendicular to the aim.
- turretMSL : SINGLE missile per cycle (routed through eMissile so it respects the per-stage
  missile budget from 0720bi).
- Both are STATIONARY: verified 0px lateral drift over 3s. They only turn.
- Destructible, reusing the 6-frame bunker collapse.
- turretSpawnSide() places them on OPEN SAND near either flank using the ground terrain mask,
  retrying up to 26 times. Verified 16/16 landing on valid sand.
- Placed on stage 1 in 4 waves, both flanks.

### BUG FOUND — wide stages could not spawn in their right 40%
spawnEnemy normalised the authored x by VW (the 480 CAMERA width) and remapped it into PLAY:
    base.x = PLAY.x + clamp(base.x/VW,0,1)*PLAY.w
On the WIDE 800px stages (1, 5, 6) every x past 480 saturated to 476 — the entire right side of
those worlds was unreachable for spawns, which is why the right-flank turrets were all landing
mid-screen. Wide stages now map level space straight to world space.
VERIFIED: right-flank turrets now land at x 593-680 on the 800-wide jungle (were pinned at 476).
This is the SIXTH appearance of the 800!=480 class.

### Enemy-cap rebalance
Stationary emplacements never leave, so counting them against the wave-dispatch cap starved stage 1's
later waves (bomber/intcp/mdrone stopped appearing). Emplacements are now excluded from the WAVE cap
and given their own EMPLACE_CAP=4 budget so the flanks stay readable. Test assertions restated to
check both separately: wave pressure <=7 AND emplacements <= EMPLACE_CAP.

## DROP 0720bo — turret fix: only the GUN rotates, sandbags stay put (2026-07-20)
Mike: "Only the turret itself should rotate, not the sandbags." My 0720bn version rotated the whole
sprite, base and all.

### How the gun was isolated
First attempt derived the base as the pixel INTERSECTION of the 7 assembled rotation frames, but the
gun overlaps itself between angles so too much got classified as base — the extracted gun came out
at only 1457px and 6-9 rotations clipped.
Better source: the sheet already ships a BARE SANDBAG BASE (row 0/3, the 119x102 sprites) next to the
assembled frames. Aligning that real base under an assembled frame and subtracting it gives the gun
exactly, with no guessing:
  turret a: base 9679px, gun 749px (bbox 44x34)
  turret b: base 9787px, gun 1073px (bbox 55x36)
Alignment is by ink-bbox horizontal centre + BOTTOM edge (the sandbags sit on the ground line), the
base mask is dilated 2px so its anti-aliased rim goes with it, and stray specks are dropped by
keeping only the largest remaining blob.

### Result
- ntur_<a|b>_base : ONE static sandbag emplacement, drawn unrotated every frame.
- ntur_<a|b>_0..23: the GUN only, rotated about the mount point in 15-degree steps. 0 clipped.
- Both share one canvas and one pivot, so they composite with the identical destination rect —
  the gun always sits correctly on its mount.
- VERIFIED: gun centroid bearing tracks its target heading within ~4 degrees at every step
  (0/45/90/135/180/225/270/315 measured at 359.8/46.7/93.7/139.3/183.5/226.5/269.8/313.9),
  all 24 consecutive frames differ, and full-orbit tracking still uses 24/24 distinct frames.

### Also fixed
Bunkers spawned through spawnEnemy directly and bypassed EMPLACE_CAP, so emplacements could peak at
5. The budget is now enforced at the spawn site for BOTH turrets and bunkers.

## DROP 0720bp — Yuri's chain lightning: upgrade COMPLETED (2026-07-20)
Mike asked whether Yuri's chain was upgraded. It was only PARTLY done in 0720bi — reporting that
honestly and finishing it.

WHAT 0720bi ACTUALLY DID: upgraded chainZap() (arc reach 150 -> 150+lv*26, per-link damage
3 -> 3+lv*2) and the chain DEPTH on the enemy branch only.
WHAT WAS STILL MISSING:
  * the PRIMARY bolt damage barely moved (3+lv -> 4 at L1, 8 at L5);
  * the boss, sub-boss and powerup branches all called chainZap at a FIXED depth of 2, so hitting a
    boss or a crate collapsed the chain back to its base length regardless of level.
NOW: primary damage 4+lv*3, and one level-scaled depth (2+min(4,lv)) shared by every branch.

### Verified curve
  lv | primary dmg | depth | reach | per-link | arcs vs a 7-enemy line
   1 |      7      |   3   |  176  |    5     | 4
   2 |     10      |   4   |  202  |    7     | 6
   3 |     13      |   5   |  228  |    9     | 7
   4 |     16      |   6   |  254  |   11     | 7
   5 |     19      |   6   |  280  |   13     | 7
Boss branch: 3 arcs at L1 -> 5 arcs at L5 (was pinned at 2 regardless of level).

## REMAINING TO-DO (current state)
  1. STAGE 7 SEWER — still the biggest gap: no roster block, no boss, no background master.
     Full cast waiting in the pack (cesspool-leviathan, rat-king, sewer-purge-barge,
     bio-sludge-abomination, toxic-dredger, venom-reaver).
  2. LEVEL 8 four-form boss — Mike parked it; art is pixel-exact to the pack masters.
  3. CONTINENTAL CRUSHER — flip so turrets face the player, destructible L4 turret
     (4x4 grid x 4 directional variants, needs its own slicer).
  4. LEVEL 6 WATER INTRO backdrop — naval units are wired, the water itself is not authored.
  5. RIVAL DOGFIGHT rebuild — speed pads are already built and ready to hook.
  6. Unwired art: ground emplacement family (77 sprites, sliced), helix_trails_4colour
     (pink = Falva), turrets_tanks_boats_jets_2f (boats for the L6 water intro).

## DROP 0720bq — CORRECTION: pink is Maverick's, not Falva's (2026-07-20)
I had recorded "helix_trails_4colour (pink = Falva)" in the to-do list. That is WRONG and is
corrected here: FALVA HAS NO HELIX WEAPON AT ALL. The blue-and-pink helix is Maverick's
FULL-CHARGE release.

### Fixed
The v2.3 pack ships the classic helix as blue (strand A) + PURPLE (strand B), so the full-charge
release was coming out blue+purple. Added nhxpb_0..15 — strand B recoloured purple -> PINK with a
luminance-preserving tint, so the shading, core highlight and black rim all survive and only the hue
moves. Maverick's full charge and his charge-up coil preview now both use BLUE + PINK.
VERIFIED by colour sampling the three shot tiers side by side:
  normal shot  green 243  blue   0  pink   0
  half charge  green 241  blue   0  pink   0
  FULL CHARGE  green   0  blue  47  pink 146
Normal and half remain the green pair, exactly as before.

## UNWIRED ART — current inventory (sheets delivered to Mike)
 1. helix_trails_4colour  — 61 trail sprites across 4 colour bands (blue/green/purple/pink),
    ~15 frames each. UNSLICED. Intended as flight trails behind the helix shots.
 2. ground_emplacements_damage_muzzle — 77 sprites, SLICED as nge_* and registered, UNWIRED.
    Emplacements + damage states + muzzle flashes + shell casings + smoke + debris.
 3. turrets_tanks_boats_jets_2f — 35 sprites, UNSLICED. Contains the BOATS needed for level 6's
    water intro (the naval units are already wired; only the water backdrop and these boats remain).

## DROP 0720br — Maverick's helix now BRAIDS as one attack (2026-07-20)
Mike: both left and right lasers should helix into, over and around each other as ONE solid attack —
and if that is not achievable, animate the existing helix art with colour flashes and flips like the
menu cursor. Did BOTH.

### The braid (drawHelixPair rewritten)
Previously the two strands were drawn at the SAME position with only a frame-phase offset, so they
read as stacked rather than woven. Now:
  * one phase drives an EQUAL AND OPPOSITE lateral sway on the two strands, so they open to a
    maximum and cross back through each other at every phase zero;
  * at each crossing the DRAW ORDER SWAPS, so whichever strand is on the outgoing side passes IN
    FRONT — that depth flip is what actually sells "wrapping around each other";
  * the trailing strand is MIRRORED on alternate half-cycles so the braid direction reads cleanly.
  MEASURED on a single beam: strand separation oscillates 58 -> 89 -> 58 px, i.e. the pair opens
  and closes by 31px per cycle and passes through a crossing each time.

### The colour-unit flash (the cursor trick, applied to the beam)
A cached WHITE silhouette of the current strand frame is revealed by a clip band that RISES along
the beam over 0.30s, then rests — the same rising-white technique built for the menu cursor.

### Colours confirmed in the same render
  LEFT beam  (normal shot)  green 3463  blue    0  pink   0
  RIGHT beam (full charge)  green    0  blue 3517  pink 687
So the normal shot stays the green pair and the full-charge release is blue + pink, per 0720bq.

Delivered: BOF_helix_weave.gif (48 frames, 30fps) and BOF_helix_weave_frames.png.

## DROP 0720bs — Maverick's helix now uses MIKE'S ACTUAL BEAM ART (2026-07-20)
Mike: "Wtf are these weird effects? You should be using my 2nd shot. Those laser beams."
He was right — I had been compositing the two separate STRAND sprites and trying to fake a braid
out of them, when the trails sheet he sent already IS a finished helix laser beam, animated, in four
colours. The braid is in the artwork; it never needed simulating.

### Replaced
- Sliced helix_trails_4colour into real beam animations, classified by COLOUR rather than row
  (the rows interleave) and filtered to beam-shaped sprites so the "BLUE"/"GREEN"/"PURPLE" label art
  and stray specks are excluded:
      blue 14 frames · green 14 · white 14 · pink 12   (avg ~69x170)
- drawHelixPair rewritten to play those directly:
      normal / half charge -> GREEN
      FULL charge          -> BLUE + PINK layered as two ribbons of one beam
  The old two-strand compositing, the equal-and-opposite sway, the draw-order swap and the
  rising-white flash are all GONE — they were solving a problem that only existed because I was
  using the wrong art.
- The charge-up coil preview now pulls from the same beam sets (green while building, blue+pink at
  full) and derives its frame count from the art instead of assuming 16.

### Second pass — killed the glow blob
The first render still had a big soft lavender/green haze behind each beam: I was stacking a canvas
shadowBlur on art that already carries its own glow. Removed it, and dropped the 'lighter' composite
that was blowing out the pink layer.
MEASURED after the fix: soft-haze 1432 px vs solid beam 15827 px — a haze:beam ratio of 0.09, i.e.
the beam is now crisp rather than a cloud.

### Colours verified in the same render
  LEFT  (normal shot)   green 2575   blue     0   pink    1
  RIGHT (full charge)   green    0   blue 10617   pink 7975

## DROP 0720bt — Maverick's lance TRAVELS animating, then BURSTS (2026-07-20)
Mike: make the attack travel with both lasers animating like a helix, smoother, with a powerful
burst at the end. Two versions — half charge FULL GREEN, full charge BLUE/PINK.

### Smoother
The beam frame was being advanced by a per-DRAW counter (b._cf / b._hf), which ties the animation to
render cadence and stutters. It is now driven off the bullet's own FLIGHT TIME
(fi = floor(age * 26)), so the helix rolls smoothly and at a constant rate regardless of frame rate.
Also dropped the leftover canvas glow argument on both draw calls — the beam art carries its own.

### The two versions
  HALF charge -> nhb_green   (full green)
  FULL charge -> nhb_blue + nhb_pink, layered as two ribbons of one beam
This is decided by b._full, exactly as Mike specified.

### The terminal burst
New helixBursts system: when a charged lance reaches the end of its run (0.85s half / 1.05s full) or
leaves the field, it blooms. The burst REUSES THE SAME BEAM ART — scaled up 0.55 -> 2.95x, fading on
a quadratic, with the two ribbons COUNTER-SPINNING as they blow out — so the colour identity carries
(green bloom for half, blue+pink bloom for full) and nothing is invented. Screen shake 4 / 7.
VERIFIED over a 42-frame run on a flat backdrop:
  frames  0-24  both lances in flight (2 bullets, 0 bursts)
  frame  30     first lance spent, burst active
  frame  36     both spent, burst still blooming
  peak ink 10867 at the bloom vs 4572 in steady flight -> the burst is a 2.4x expansion
Cleared on stage start so a burst cannot leak between levels.

Delivered: BOF_helix_lance.gif (42 frames) and BOF_helix_lance_frames.png.

## DROP 0720bu — lance SPINS as it travels + green is a PAIR (2026-07-20)
Mike: make the attack appear to be spinning as it travels, and the green should also have two
greens going.

### Two ribbons either way
  HALF charge -> nhb_green + nhb_green at a 6-frame offset (two green ribbons, never identical)
  FULL charge -> nhb_blue + nhb_pink
The terminal burst matches: a green pair blooms green, a full charge blooms blue+pink.

### Axial spin
A helix rolling about its own long axis reads in 2D as the silhouette swinging side to side and
narrowing when it turns edge-on. First cut put the two ribbons a QUARTER turn apart, which kept the
overall width nearly constant and hid the roll (only 12px of travel).
Corrected to a HALF turn, which is the true double-helix relationship: as it rolls, one ribbon
swings to the near side while the other goes far, and they cross through the centre twice per turn.
  * lateral offset from sin(phase), up to 30% of beam width
  * DRAW ORDER swaps on cos(phase) so the nearer ribbon always passes in front
  * the far ribbon is dimmed and slightly shortened, so depth reads
  * scaleX narrows toward edge-on but never fully collapses, so the beam stays readable
MEASURED across the roll: half-charge width now travels 33 -> 57 px (24px), full charge 45 -> 81 px
(36px) — up from 12px and 18px before the fix.

### Colours confirmed mid-flight
  HALF beam  green 379  blue   0  pink   0
  FULL beam  green   0  blue 330  pink 404

## DROP 0720bv — the two strands now COMBINE into a DNA double helix (2026-07-20)
Mike: it needs to appear and combine as they turn, into a DNA-strand-like helix laser.

### Why the previous pass was not it
0720bu swung each ribbon side to side as a WHOLE UNIT. That reads as two beams orbiting one another,
not as a helix — because a real DNA strand twists ALONG its length: at any instant it is crossed at
some heights and wide open at others, and those crossing points travel down the beam.

### How it works now
The beam sprite is cut into 14 horizontal SEGMENTS and every segment gets its own phase, advancing
down the length (TURNS=2.1 visible twists), with the whole helix also rolling as it travels.
Segments from BOTH strands are pooled, sorted by depth (cos of their phase) and drawn FAR TO NEAR,
so the strands genuinely pass through one another instead of one always sitting on top.
Far segments are dimmed and narrowed; near ones are full width. The two strands stay half a turn
apart, which is the true double-helix relationship.

### Verified — the DNA signature is the pinch/bulge pattern DOWN the beam
Measuring width row by row within a SINGLE frame:
  HALF (two greens) : 4, 12, 41, 56, 56, 51, 28, 27, 12, 14, 24, 14, 27, 17, 18, 20, 40, 52, 54, 38
                      pinches to 4px at the crossings, opens to 56px between them
  FULL (blue+pink)  : 11, 22, 61, 82, 79, 72, 40, 39, 16, 19, 31, 14, 39, 24, 25, 20, 57, 65, 70, 52
                      pinches to 11px, opens to 82px
That alternation along the length is the helix; the previous version had a constant width.

Tuning constants all sit together: SEG=14 (slice count), TURNS=2.1 (twists visible),
spin rate 0.30, lateral amplitude 34% of beam width.

Delivered: BOF_helix_dna.gif (42 frames) and BOF_helix_dna_frames.png.

## DROP 0720bw — Yuri chain lightning: visual delivered (2026-07-20)
Rendered the upgraded chain against an identical 9-enemy formation at weapon level 1 and level 5,
same instant in the strike, so the only variable is the tier.

  WEAPON LEVEL 1 : 5 arcs · primary 7  · depth 3 · reach 176 · per-link 5
  WEAPON LEVEL 5 : 8 arcs · primary 19 · depth 6 · reach 280 · per-link 13

Measured lightning ink on screen: L1 peaks at 6802 px, L5 at 10726 px — L5 puts 1.6x more chain
on screen from the same shot, and reaches further so it picks up targets L1 cannot see.
Delivered BOF_yuri_chain.gif (32 frames, both tiers back to back) and BOF_yuri_chain_frames.png.

## DROP 0720bx — chain lightning: thicker bolts + white/yellow strike flash (2026-07-20)
Mike: thicker lightning, and units should flash white/yellow when the chain hits them.

### Thicker
drawChainBolt trunk width raised from max(7, len*0.14) to max(16, len*0.30), glow 10 -> 14, and the
trunk is now drawn TWICE — a wide soft core plus a tighter hot centre at 85% alpha — so the bolt
reads heavy instead of thin. The no-art fallback stroke went from 2px to 5px to match.
MEASURED on the same shot: L1 peak lightning 6802 -> 7844 px, L5 peak 10726 -> 12390 px.

### Strike flash
Anything the chain hits now sets _zapFlash (0.20s on a chained link, 0.22s on the primary target).
While it burns, the unit is drawn through a brightness+desaturate filter and then washed with an
additive radial gradient: WHITE at the core while the flash is fresh, cooling through YELLOW as it
fades. So a struck unit blows out white and cools to yellow rather than just tinting.
MEASURED: strike-flash pixels peak at 561 (L1) and 846 (L5) on the strike frame and fall to ~20
within a few frames — a sharp pop, not a lingering glow.

## DROP 0720by — chain now TRICKLES through the whole group and SPIKES RIGHT (2026-07-20)
Mike: it should trickle through all those enemies and spike out and to the right.

### Targeting is SCORED, not nearest-first
The old rule picked the closest unhit enemy, which made the arc ping-pong between the two nearest
bodies and stall in one corner of a formation. Candidates are now scored:
  * distance still counts, but only as 0.75 of the weight — nearest no longer wins automatically
  * doubling back on the arc's own heading is PENALISED (the previous hop's direction is passed
    down the recursion, so each jump knows where it came from)
  * continuing outward is rewarded, with an explicit RIGHTWARD lean
Depth also raised from 2+min(4,lv) to 4+lv*2, so there are enough hops to actually clear a group.

### Verified coverage on a 9-enemy formation
  wlevel 1: 8 arcs, 8 of 9 struck
  wlevel 3: 9 arcs, 9 of 9 struck
  wlevel 5: 9 arcs, 9 of 9 struck
### Verified rightward spike
Player at x=120 against a formation spanning x=90..412: the chain struck 8 of 8 and its furthest
node landed at x=412 — it crossed the entire field left to right instead of clustering near the
launch point.
