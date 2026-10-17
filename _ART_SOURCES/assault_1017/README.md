# October 17 gameplay art

Generated with the built-in image generator, using the current authored
ENC30 tank/jet parts as a palette and pixel-art reference. Wind ammunition
also used the existing Wind rounds as a subject/color reference. No PixelLab
generation is claimed. Mike subsequently requested waiting for PixelLab for
the separate Stage 7–8 portal/void/arena pass; those drafts remain unused.

Eight banks, 16 distinct drawings each: lightning guard jet, bare highway tank
hull/treads, independent recoiling twin-cannon turret, cannon shell, Wind MG,
spread and chaingun rounds, and one continuous Wind laser shaft.

Prompt headers required fixed equal cells, even dimensions, shared physical
pivots and one proportional scale. The generator returned larger source
canvases; `build_assault_1017.py` records the actual source rectangles and
physical socket registration, solves one scale per complete bank and exports
256×256 hull/jet/module cells, 64×96 rounds, and 128×512 laser cells. It retains
the generated alpha and removes only near-transparent alpha noise below 8.
No individual frame is stretched or fitted to its own bounds.

Rebuild: `python _BUILD_SOURCE/build_assault_1017.py`.
`manifest.json` records raw hashes, source rectangles/pivots, common scales,
final bounds and distinct-frame counts. Onion previews are emitted under the
ignored `_shots/assault_revision_1017/art/` directory. The native probe uses
the game's own XART images and drawImage paths. Source files are retained
here for reproducible exports; portable builds can omit this source archive.
