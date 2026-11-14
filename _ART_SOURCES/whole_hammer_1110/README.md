# Complete generated held-hammer attacks — November 10, 2026

Mike rejected the former body/weapon assembly. These complete generated figures supersede the held-attack portions of rigid_hammer_1110 and hammer_face_1110. Never rebuild those older assembled attack sheets over these banks.

The accepted raw groups and exact prompts are in source-index.json. Each used source cell contains the entire robot, hands and held hammer. The approved hammer references guide identity; they are never stamped onto the production actor. Each editable Aseprite has exactly one complete figure layer. build.py only registers/downsizes complete source cells, mirrors complete poses and makes whole-frame material derivatives. No head/body/held-weapon compositing.

56 unique complete source poses become six held-attack and two empty-handed 16-cell timelines (128 cells, with intentional transition holds and complete-pose mirrors). 640×640 even cells; pivot 320,320; boot baseline474; one proportional nearest-neighbor scale per bank (0.63 for held attacks and Chronos empty hands;0.75 for the more padded Dracodia empty-hand source). Regular/chromium/red/white-hit/red-hit textures preserve alpha. Separate immutable approved weapon headings remain in their original production flight directories and are selected only for detached flight.

Set ASEPRITE to the local executable and run python build.py with Pillow and NumPy installed. Runtime installation is _BUILD_SOURCE/whole_hammer_1110/install.py. Set BOF_ROOT if the game source is elsewhere. The installer stops if its boss-animation owner changed; inspect concurrent work instead of overwriting it. It does not rewrite game.js.

Source audit: eight16-frame single-layer Aseprites export pixel-identically to the regular sheets; all128 cells have transparent padding. Native contacts, actual white hit pixels, whole actor alpha collision, release/catch and detached targeting are checked in docs/qa/whole_hammer_*1110.*. Clips are local review artifacts under _shots/whole_hammer_1110/.
