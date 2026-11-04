# Pixel divider and scrolling color panels

The generated divider is normalized to a 228 x 128 native grid, hard alpha and five flat grayscale tones. Exact 4x export gives chunky stepped edges. The full footer still covers the pilot chest cutoffs.

Nine generated background tiles use a solid base plus sparse horizontal pixel bars. Each is exported on a 64 x 64 native grid with exactly two flat colors; no gradients remain. The default character mappings use all nine requested colors. Cole's black field has green bars and Falva's white field pink bars.

Sixteen authored color-panel phases scroll left and right fields in opposite directions, with exact loop closure. Playback selects frames at 8fps from the scene's elapsed time, preserving motion across dialogue beats. The gray divider and all pilot artwork remain fixed in place. No runtime image transform, generated mask, opacity animation or graphical effect is added.

Only comic-border changes among the previous 117 banks. The other 116 banks, including all 216 pilot drawings, stay byte-identical. Nine color-panel banks are added for 126 banks / 2,354 frames total. Source masters, palette roles and metadata are in comic_scroll_1103; editable timelines are in aseprite.
