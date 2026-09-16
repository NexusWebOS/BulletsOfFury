# Stage 7 Toxic Portal Warden cripple-rail warning — September 16, 2026

The Toxic Portal Warden's cripple phase no longer re-aims an unwarned rail shot at the player every 0.19 seconds. It now commits one rail group before a 0.58-second shared green/yellow/red warning. Four fields show the three straight single shots and the paired offset finisher. Their origins follow the crawling hull while every committed angle stays fixed, so a late dodge cannot move the promised lanes.

The release preserves the original pressure: three alternating single rails at speed `5.25`, followed by the left/right dual finisher at speed `4.65` and offsets `-0.07/+0.07` radians. The next group samples a fresh player position only after the previous group completes. Leaving the cripple phase cancels a pending warning. The authored cripple hull, rail-spear projectile, physical cannon hardpoints, muzzle effects and sound route remain in use.

Focused section 356 passes **13/13**. The full suite reaches its final summary with **4,510 passing assertions / 57 failures**: the established 56-name baseline plus the documented intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **18/18** with zero page, console or game-loop errors. Five native 960×1024 frames were inspected from green through the complete group; the fields remain behind the authored hull, the alert remains readable above it, and the warning clears before the solid rail spears release.

Machine-readable proof: [qa/stage7_warden_cripple_rail_warning_0916.json](qa/stage7_warden_cripple_rail_warning_0916.json).
