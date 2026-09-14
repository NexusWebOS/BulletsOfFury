# September 14 build publication

This build collects the local Bullets of Fury work through Frost Cruiser's corrected nose lasers: encounter and weapon fixes, Retina and missile systems, pause and Arcade rules, Furyship transformation and animation assets, updated Yuri/dialogue/font presentation, project guidance, request checklist and verification records. Three additional boss-music WAVs are stored in assets/game/music/newboss with an inventory; they are not assigned to encounters.

The request checklist has 139 entries: 62 complete, 10 partial and 67 pending. The 77 unfinished items remain tracked; this publication does not claim the entire feature backlog is complete.

Latest gameplay verification: syntax passed; 15 native Chromium checks passed, no page/console/game-loop errors. Full suite reached its final summary with 3,852 passing assertions and 58 existing failures (exit 1), with no new failing names. See qa/frost_nose_laser_0914.json.

GitHub's three incoming Tempest commits through f936f106 were inspected before integration. They preserve the staged source encounter and Herald's stored ALTBOSS[8] slot. The local game includes the Stage-6 duo. The incoming Stage-8 empty-miniboss decision is retained during integration.

Publication scope includes the game's runtime assets, source/build tools, art sources, project notes and verification records. Unrelated nested projects, personal tool settings and ignored scratch captures remain local. Original music recordings on the Desktop are preserved.

After integration: syntax passed, 15/15 native checks passed, zero browser errors. Full suite completed with 3,850 passing assertions and 58 inherited failures (exit 1), no new failing names. See [integration proof](qa/github_build_0914.json).
