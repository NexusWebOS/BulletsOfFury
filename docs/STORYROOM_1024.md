# Fury Storyroom

Double-click **OPEN_STORYBOARD.bat** in the game folder. The program opens at http://127.0.0.1:8795/tools/storyboard/. Python and your browser are the only requirements; both are already present here. Keep its server running while you edit. A second launch reopens the existing editor.

## Editing

1. Choose a scene on the left and its lead-pilot version at the top.
2. Select a shot. Edit the speaker, dialogue, minimum hold, authored artwork, aircraft movement, sound cue and director notes where that scene supports them.
3. Drag cards, or use Earlier/Later. Duplicate, add, skip or delete shots. Storyboard and Script views show the same sequence.
4. Use **Shot** to rehearse the selection, **Scene** to play from the start, pause/step between cards, and expand the preview. The opening and invasion ending use their actual native sequences. Monologues and timed responses use a dialogue rehearsal; their physical boss actions retain their existing game owners.
5. **Apply to game** saves the project and the shipping runtime data. Restart an already-running game to pick up disk changes. No code editing is required. Export/Import moves the project as JSON.

Ctrl+Z / Ctrl+Shift+Z undo or redo storyboard operations (text fields retain normal text-editing undo). Ctrl+S applies the draft. Changes are saved locally as a draft and recovered after reopening against the same game version. If the saved game version changed, Restore local draft offers the older draft without overwriting it silently.

Pilot versions stay separate. **Copy this version to every pilot** explicitly replaces their personalized wording after confirmation. The selected lead version also applies when that pilot leads co-op. Untouched versions continue to use the live native scripts, including dynamic co-op wording.

## Scene order and game events

Dragging the left-hand scene list changes the review order. **Scene settings → Play this scene at** assigns a director sequence to a different game event. For example, a different debrief can play after Stage3. The original event still owns its stage clear, rewards and next-level callback. This editor changes the story, not the order of playable levels.

The campaign opening, opening narration, Dracodia monologue/response events and invasion ending have fixed game events. Their cards can be rewritten/reordered within those sequences. Timed responses keep their native action clocks; their hold fields are read-only. Director hold times are minimums: the native text-reveal/read window can take longer.

The catalog includes the25-shot opening; opening narration; debriefs1–9; Chronos contact/trap; Stage6 route dialogue; Rebel contact and StageX pilots; the river approach; Dracodia monologue, rebirth/transformation/final responses; and the current invasion ending. It reads the game's actual authored scripts rather than a second handwritten screenplay. Additional director scenes encountered in that session can appear under Discovered. Ordinary combat barks and unused archived cinematic systems are not a global text-replacement target.

## Files and recovery

- Editor: `tools/storyboard/`
- Launcher/server: `OPEN_STORYBOARD.bat`, `_BUILD_SOURCE/storyboard_server_1024.py`
- Saved edits: `assets/data/storyboard_1024.json`
- Generated shipping data: `assets/storyboard_data_1024.js`
- Native integration: `assets/storyboard_1024.js`, loaded last after the game owners.
- Previous applied projects: `_ART_SOURCES/storyboard_1024/backups/` (ignored by Git, preserved on disk).

Reset this version restores one native scene/pilot draft; apply afterward. Undo can reverse it before closing. Importing an empty version1 project restores all native dialogue after applying. The runtime with empty overrides is a native pass-through. The integration merges only changed fields and reorders native beat records; root callbacks are never saved as editable code.

The server binds127.0.0.1 only, rejects foreign-origin writes, accepts structured scene data only and writes only the two fixed project/runtime paths. It preserves the previous JSON before each apply. Exported projects contain narrative data, never executable callback code.

## Verification — October24

Native Chromium editor workflow19/0: catalog/nine pilots, visible shot dialogue, actual drag/drop, earlier/later, undo/redo, separate pilot edits, native preview, import/export, rejected invalid import, draft reopening, apply and fresh-game load, callback-once, scene-event reassignment,1100/480px layout and no console/page errors.

Native runtime8/0: opening flight identity and timing, Dracodia text/expression and empty-speech safety, timed response reorder, actual ending shot/caption/end-time mapping, skipped director continuation once, reset and no errors. Server10/0: empty project, local-origin restrictions, real JSON/script writes, invalid field/duration/null-text rejection, backups, atomic temporary-file cleanup, exclusive port and reopening the running editor. **37 focused checks total.** QA save tests restore the original saved project; the delivered game contains no test dialogue.

Required game syntax, new JavaScript syntax and Python compilation pass. Required full `_BUILD_SOURCE/test_fl.js` still exits1 before assertions/final summary because the downloaded build lacks `retired_art_archive_1022.cjs`. No full-suite pass is claimed. Existing unrelated work is preserved; no commit or push requested.
