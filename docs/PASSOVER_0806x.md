# PASSOVER — drop 0806x   (SHEETS REGROUPED BY STAGE)

Build: `BulletsOfFury_0806x`
Harness: **2,061 assertions / 187 sections / 0 failing**, twice, reaching the banner.
**9,535 / 9,535 cells resolve, 0 at the wrong size.**

---

## 1. THE PROBLEM I SHIPPED IN 0806w

0806w grouped 9,535 cells into 67 sheets **by key prefix**, merged to fill a pixel budget. That
is not the same as "loads together", and I said so at the time without being able to measure it:
a stage could touch any number of those sheets, and each one it touches costs its WHOLE size.
Worst case was an unbounded slice of 2,491 MB.

## 2. MEASURED PROPERLY THIS TIME

The earlier probes returned zero because atlasing collapsed every cell key onto a sheet path, so
the drawImage recorder could no longer see key names. **Hooking `XART._touch` instead** — the one
place every art request passes through — reads the KEY and is immune to that:

    s1 430 · s2 522 · s3 596 · s4 491 · s5 473 · s6 649 · s7 462 · s8 501
    union: 1,633 of 9,535 cells ever touched by a driven playthrough

Regrouped on that: cells used by exactly one stage go in that stage's sheets, cells used by two
or more go in `common`, and everything a stage never touched goes in `rest`.

    group    sheets   decoded          COST TO PLAY A STAGE (own + common)
    common      2       68 MB            stage 1   108 MB     stage 5   107 MB
    s1          2       40 MB            stage 2   125 MB     stage 6   186 MB
    s2          2       57 MB            stage 3   123 MB     stage 7    97 MB
    s3          2       55 MB            stage 4    81 MB     stage 8   136 MB
    s4          1       12 MB
    s5          1       39 MB          78 sheets, 258 files
    s6          3      118 MB
    s7          1       29 MB          `rest` is 62 sheets / 2,153 MB of menu, cutscene, boot
    s8          2       68 MB           and untouched art — lazy, only if reached
    rest       62    2,153 MB

**A stage costs 81-186 MB instead of an unbounded slice of 2,491.**

## 3. TWO THINGS THAT WENT WRONG ON THE WAY

**Out of memory.** Repacking held all 67 source sheets open in PIL at once and the process was
killed. Fixed by extracting all 9,535 cells to disk one SOURCE sheet at a time, then packing from
disk — bounded memory regardless of how many sheets exist.

**A chunk that would not pack.** The first attempt crashed unpacking a `None`. It splits the chunk
and retries now rather than failing, which is why 78 sheets exist where the budget predicted
fewer.

## 4. THREE MORE ASSERTIONS THAT MEASURED THE SHEET

Every assertion that reads a key's SIZE has to go through `cellSize()` now. Three were still
reading the file the key names — and since that file is a 3648x2468 sheet, the pellet
orientation check declared vertical 25x14 pellets "horizontal". Routed through the cell table.

## 5. STILL OPEN

* **`rest` is 7,902 cells / 2,153 MB** — menus, cutscenes, boot, and art nothing reaches. Worth
  auditing: some of it is certainly dead.
* Audio sprites, if you want below ~134 art files.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
