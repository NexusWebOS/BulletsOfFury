# Pilot headset motion and emotions

Nine pilots, 24 newly generated 16-bit frames each (216 native drawings). Fixed 128 x 128 cells, common chest pivot (64,124), hard alpha and a shared maximum 32-color palette per pilot. Actual redraws provide front, left/right three-quarter and full profiles. Talking mouths and six emotional pairs are authored into the source frames. Cole retains neon green.

Runtime panels use exact 3x exports and fixed positions. Frame selection follows the current speaker, text-reveal state and authored line emotion. Inactive pilots listen; mouths stop when text finishes. No runtime image transformation or new effect is used. The prior comic divider/footer and seated Decker, drone descent and landing-pad corrections remain.

The source masters are preserved; normalization uses one proportional grid scale with at most two native pixels of vertical translation to a common baseline. Each pilot has tagged Aseprite timelines. All 117 banks / 2,210 frames round-trip without pixel differences. Only the nine former headset banks change from revision 4; eleven banks are added, and the other 97 prior banks are byte-identical.
