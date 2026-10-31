BOF animation audit - 2026-10-23

The exact approved hammer is locked-hammer.png. Never ask an animation model
to recreate or redesign it. PixelLab animates body-only reels; the accepted
whole actor plates bake that fixed prop into measured glove mounts offline.
Purple/red palettes share the same physical design and .13 weapon unit.

The first two side attempts were rejected for a false crescent blade and weak
two-hand grip. Only the 63077c51 overhead and 85c23e09 side bodies are used.
The 1558d1c2 and 3d5c0b49 heavy-ship reels supply charge/recoil/recovery only.
Detached generated beam tails are excluded offline; native projectiles own
damage. Four ships use fixed model units, authored white sheets and measured
pod sockets. Primary and delayed follow-up warnings match their real releases.

Rebuild owners are in _BUILD_SOURCE. Owned manifests and SHA256 texture hashes
are in assets/game/shared/combat and assets/game/levels/stage_08/enemies.
Native QA tools live in _BUILD_SOURCE/animation_audit_1023. The complete local
review is _shots/animation_audit_1023/review/index.html, including three MP4s.
The local _shots folder is review evidence and is normally ignored by Git.
No commit or push was performed. Existing unrelated edits were preserved.
